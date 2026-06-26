#!/usr/bin/env python3
"""
币安资金费率套利策略 (Binance Funding Rate Arbitrage)
策略：做多负资金费率币种 + 做空正资金费率币种，赚取资金费差价
"""

import os
import sys
import json
import time
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/zc/.openclaw/workspace/logs/funding_arbitrage.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('funding_arbitrage')

@dataclass
class Position:
    symbol: str
    side: str  # 'LONG' or 'SHORT'
    margin: float  # 保证金
    notional: float  # 名义价值
    entry_price: float
    funding_rate: float
    unrealized_pnl: float = 0

class FundingRateArbitrage:
    """资金费率套利策略"""
    
    # 风控参数
    PARAMS = {
        'margin_per_position': 3.0,      # 每币种保证金 3U
        'leverage': 10,                   # 10x 杠杆
        'notional_per_position': 30.0,    # 名义价值 30U
        'max_total_margin': 60.0,         # 最大总保证金 60U
        'cash_buffer_ratio': 0.5,         # 50% 现金缓冲
        'max_positions': 6,               # 最大持仓币种数
        'min_funding_rate_abs': 0.001,    # 最小资金费率绝对值 0.1%
        'stop_loss_threshold': -20.0,     # 单币种止损线 -20U
        'top_n_symbols': 20,              # 监控前20交易对
    }
    
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.base_url = 'https://fapi.binance.com'  # 合约API
        self.positions: Dict[str, Position] = {}
        self.traded_symbols: set = set()  # 记录已交易币种，避免重复
        
        if not self.api_key or not self.api_secret:
            raise ValueError("缺少 BINANCE_API_KEY 或 BINANCE_API_SECRET 环境变量")
    
    def _generate_signature(self, query_string: str) -> str:
        """生成API签名"""
        import hmac
        import hashlib
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _request(self, method: str, endpoint: str, params: dict = None, signed: bool = False) -> dict:
        """发送HTTP请求"""
        import requests
        
        url = f"{self.base_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}
        
        if params is None:
            params = {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['recvWindow'] = 5000
            query = '&'.join([f"{k}={v}" for k, v in params.items()])
            params['signature'] = self._generate_signature(query)
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=params, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, data=params, timeout=10)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API请求失败: {url}, 错误: {e}")
            raise
    
    def get_funding_rates(self) -> List[dict]:
        """获取所有合约的资金费率"""
        try:
            data = self._request('GET', '/fapi/v1/premiumIndex')
            # 过滤有效数据
            rates = []
            for item in data:
                if 'symbol' in item and 'lastFundingRate' in item:
                    try:
                        rate = float(item['lastFundingRate'])
                        rates.append({
                            'symbol': item['symbol'],
                            'rate': rate,
                            'mark_price': float(item.get('markPrice', 0)),
                            'next_funding_time': item.get('nextFundingTime', 0)
                        })
                    except (ValueError, TypeError):
                        continue
            return rates
        except Exception as e:
            logger.error(f"获取资金费率失败: {e}")
            return []
    
    def get_account_balance(self) -> Tuple[float, float]:
        """获取账户余额 (总权益, 可用余额)"""
        try:
            data = self._request('GET', '/fapi/v2/account', signed=True)
            total_balance = float(data.get('totalWalletBalance', 0))
            available = float(data.get('availableBalance', 0))
            return total_balance, available
        except Exception as e:
            logger.error(f"获取账户余额失败: {e}")
            return 0.0, 0.0
    
    def get_positions(self) -> List[dict]:
        """获取当前持仓"""
        try:
            data = self._request('GET', '/fapi/v2/positionRisk', signed=True)
            positions = []
            for pos in data:
                amt = float(pos.get('positionAmt', 0))
                if abs(amt) > 0:
                    positions.append({
                        'symbol': pos['symbol'],
                        'side': 'LONG' if amt > 0 else 'SHORT',
                        'amount': abs(amt),
                        'entry_price': float(pos.get('entryPrice', 0)),
                        'mark_price': float(pos.get('markPrice', 0)),
                        'unrealized_pnl': float(pos.get('unrealizedProfit', 0)),
                        'margin': float(pos.get('isolatedMargin', 0)) or float(pos.get('positionInitialMargin', 0))
                    })
            return positions
        except Exception as e:
            logger.error(f"获取持仓失败: {e}")
            return []
    
    def select_symbols(self, rates: List[dict]) -> Tuple[List[str], List[str]]:
        """
        选币逻辑
        返回: (做空列表-正费率, 做多列表-负费率)
        """
        # 过滤掉已经交易过的币种和费率绝对值不够的
        min_rate = self.PARAMS['min_funding_rate_abs']
        
        eligible = [
            r for r in rates 
            if abs(r['rate']) >= min_rate and r['symbol'] not in self.traded_symbols
        ]
        
        # 按费率绝对值排序
        eligible.sort(key=lambda x: abs(x['rate']), reverse=True)
        
        # 做空：正费率（资金费率为正，做空方收资金费）
        short_candidates = [r['symbol'] for r in eligible if r['rate'] > 0]
        
        # 做多：负费率（资金费率为负，做多方收资金费）
        long_candidates = [r['symbol'] for r in eligible if r['rate'] < 0]
        
        # 限制数量
        max_pos = self.PARAMS['max_positions']
        current_positions = len(self.positions)
        available_slots = max_pos - current_positions
        
        # 平均分配多空仓位
        slots_per_side = available_slots // 2
        
        return short_candidates[:slots_per_side], long_candidates[:slots_per_side]
    
    def calculate_position_size(self, symbol: str, mark_price: float) -> float:
        """计算开仓数量"""
        notional = self.PARAMS['notional_per_position']
        quantity = notional / mark_price if mark_price > 0 else 0
        
        # 获取交易对精度
        try:
            info = self._request('GET', '/fapi/v1/exchangeInfo')
            for s in info.get('symbols', []):
                if s['symbol'] == symbol:
                    qty_precision = int(s.get('quantityPrecision', 3))
                    return round(quantity, qty_precision)
        except:
            pass
        
        return round(quantity, 3)
    
    def open_position(self, symbol: str, side: str, quantity: float) -> bool:
        """开仓"""
        try:
            # 设置杠杆
            self._request('POST', '/fapi/v1/leverage', {
                'symbol': symbol,
                'leverage': self.PARAMS['leverage']
            }, signed=True)
            
            # 下单
            order_side = 'BUY' if side == 'LONG' else 'SELL'
            params = {
                'symbol': symbol,
                'side': order_side,
                'type': 'MARKET',
                'quantity': quantity,
                'positionSide': 'BOTH'  # 单向持仓模式
            }
            
            result = self._request('POST', '/fapi/v1/order', params, signed=True)
            
            if result.get('status') == 'FILLED':
                logger.info(f"开仓成功: {symbol} {side} 数量:{quantity}")
                self.traded_symbols.add(symbol)
                return True
            else:
                logger.warning(f"开仓状态: {result}")
                return False
                
        except Exception as e:
            logger.error(f"开仓失败 {symbol} {side}: {e}")
            return False
    
    def close_position(self, symbol: str, side: str, quantity: float) -> bool:
        """平仓"""
        try:
            order_side = 'SELL' if side == 'LONG' else 'BUY'
            params = {
                'symbol': symbol,
                'side': order_side,
                'type': 'MARKET',
                'quantity': quantity,
                'reduceOnly': 'true'  # 只减仓
            }
            
            result = self._request('POST', '/fapi/v1/order', params, signed=True)
            
            if result.get('status') in ['FILLED', 'PARTIALLY_FILLED']:
                logger.info(f"平仓成功: {symbol} {side}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"平仓失败 {symbol}: {e}")
            return False
    
    def check_stop_loss(self) -> List[dict]:
        """检查止损条件"""
        positions_to_close = []
        
        for pos in self.get_positions():
            # 检查浮亏
            if pos['unrealized_pnl'] <= self.PARAMS['stop_loss_threshold']:
                # 检查是否有资金费收入和盈利
                funding_pnl = self._estimate_funding_pnl(pos['symbol'], pos['side'])
                if funding_pnl + pos['unrealized_pnl'] > 0:
                    positions_to_close.append(pos)
                    logger.info(f"触发平仓: {pos['symbol']} 浮亏:{pos['unrealized_pnl']:.2f} 资金费:{funding_pnl:.2f}")
        
        return positions_to_close
    
    def _estimate_funding_pnl(self, symbol: str, side: str) -> float:
        """估算已收资金费（简化计算）"""
        # 这里需要查询历史资金费记录
        # 简化处理：实际实现需要调用 /fapi/v1/income 接口
        return 0
    
    def rebalance(self):
        """主策略循环"""
        logger.info("=== 开始资金费率套利调仓 ===")
        
        # 1. 获取账户状态
        total_balance, available = self.get_account_balance()
        logger.info(f"账户权益: {total_balance:.2f} USDT, 可用: {available:.2f} USDT")
        
        # 2. 检查风控
        used_margin = total_balance - available
        if used_margin > self.PARAMS['max_total_margin']:
            logger.warning(f"超过最大保证金限制: {used_margin:.2f} > {self.PARAMS['max_total_margin']}")
            return
        
        # 3. 获取持仓并检查止损
        current_positions = self.get_positions()
        self.positions = {p['symbol']: Position(
            symbol=p['symbol'],
            side=p['side'],
            margin=p.get('margin', 3),
            notional=abs(p['amount'] * p['mark_price']),
            entry_price=p['entry_price'],
            funding_rate=0,
            unrealized_pnl=p['unrealized_pnl']
        ) for p in current_positions}
        
        # 检查止损
        for pos in self.check_stop_loss():
            self.close_position(pos['symbol'], pos['side'], pos['amount'])
        
        # 4. 获取资金费率并选币
        rates = self.get_funding_rates()
        if not rates:
            logger.error("无法获取资金费率")
            return
        
        short_list, long_list = self.select_symbols(rates)
        logger.info(f"候选做空: {short_list}")
        logger.info(f"候选做多: {long_list}")
        
        # 5. 开新仓位
        current_count = len(self.positions)
        max_new = self.PARAMS['max_positions'] - current_count
        
        if max_new <= 0:
            logger.info("已达到最大持仓数，等待调仓")
            return
        
        # 多空均衡开仓
        slots = min(max_new // 2, len(short_list), len(long_list))
        
        for symbol in short_list[:slots]:
            rate_info = next((r for r in rates if r['symbol'] == symbol), None)
            if rate_info:
                qty = self.calculate_position_size(symbol, rate_info['mark_price'])
                if qty > 0:
                    self.open_position(symbol, 'SHORT', qty)
        
        for symbol in long_list[:slots]:
            rate_info = next((r for r in rates if r['symbol'] == symbol), None)
            if rate_info:
                qty = self.calculate_position_size(symbol, rate_info['mark_price'])
                if qty > 0:
                    self.open_position(symbol, 'LONG', qty)
        
        logger.info("=== 调仓完成 ===")


def main():
    """主函数"""
    trader = FundingRateArbitrage()
    
    # 每8小时执行一次（资金费结算周期）
    # 可以在 cron 中设置: 0 0,8,16 * * *
    trader.rebalance()


if __name__ == '__main__':
    main()
