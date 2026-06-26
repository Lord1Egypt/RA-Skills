#!/usr/bin/env python3
"""
CryptoScope - 加密货币数据分析助手 v1.0.0
实时价格查询、技术指标分析、交易信号生成
"""
import sys
import os
import json
import argparse
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import time

# ═══════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════

COINGECKO_API = "https://api.coingecko.com/api/v3"
SKILLPAY_API = "https://skillpay.me/api/v1/billing"
SKILLPAY_API_KEY = os.environ.get("SKILLPAY_API_KEY", "sk_0de94ea93e9aca73aafc2b6457b8de378389a21661f9c6ad4e6b7929e390e971")
CRYPTO_SKILL_ID = "0c9fb051-d210-46c4-b4d8-67f6cb6ba624"  # SkillPay Skill ID（2026-03-07 19:51配置）

# 缓存（5分钟）
CACHE_DURATION = 300
cache = {}

# ═══════════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════════

@dataclass
class CryptoData:
    """加密货币数据"""
    symbol: str
    name: str
    price: float
    change_24h: float
    volume_24h: float
    market_cap: float
    high_24h: float
    low_24h: float
    timestamp: int

@dataclass
class TechnicalIndicators:
    """技术指标"""
    ma_20: float
    ma_50: float
    ma_200: Optional[float]
    rsi: float
    macd: Dict[str, Any]
    bollinger_bands: Dict[str, float]

@dataclass
class TradingSignal:
    """交易信号"""
    symbol: str
    signal: str  # BUY/SELL/HOLD
    confidence: float
    reasons: List[str]
    risk_level: str  # low/medium/high
    timestamp: int

# ═══════════════════════════════════════════════════
# CoinGecko API 客户端
# ═══════════════════════════════════════════════════

class CoinGeckoClient:
    """CoinGecko API 客户端"""
    
    def __init__(self):
        self.base_url = COINGECKO_API
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoScope/1.0'
        })
    
    def get_price(self, coin_id: str) -> Optional[CryptoData]:
        """
        获取实时价格
        
        Args:
            coin_id: 币种ID（如bitcoin, ethereum）
        """
        cache_key = f"price_{coin_id}"
        
        # 检查缓存
        if cache_key in cache:
            cached_data, timestamp = cache[cache_key]
            if time.time() - timestamp < CACHE_DURATION:
                return cached_data
        
        try:
            # CoinGecko API
            url = f"{self.base_url}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false'
            }
            
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            
            data = resp.json()
            market_data = data['market_data']
            
            crypto_data = CryptoData(
                symbol=coin_id,
                name=data['name'],
                price=market_data['current_price']['usd'],
                change_24h=market_data['price_change_percentage_24h'],
                volume_24h=market_data['total_volume']['usd'],
                market_cap=market_data['market_cap']['usd'],
                high_24h=market_data['high_24h']['usd'],
                low_24h=market_data['low_24h']['usd'],
                timestamp=int(time.time())
            )
            
            # 缓存
            cache[cache_key] = (crypto_data, time.time())
            
            return crypto_data
        
        except requests.exceptions.RequestException as e:
            print(f"❌ API请求失败: {e}", file=sys.stderr)
            return None
    
    def get_price_history(self, coin_id: str, days: int = 30) -> Optional[List[float]]:
        """
        获取历史价格
        
        Args:
            coin_id: 币种ID
            days: 天数
        """
        cache_key = f"history_{coin_id}_{days}"
        
        # 检查缓存
        if cache_key in cache:
            cached_data, timestamp = cache[cache_key]
            if time.time() - timestamp < CACHE_DURATION * 6:  # 30分钟缓存
                return cached_data
        
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days
            }
            
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            
            data = resp.json()
            prices = [price[1] for price in data['prices']]
            
            # 缓存
            cache[cache_key] = (prices, time.time())
            
            return prices
        
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取历史价格失败: {e}", file=sys.stderr)
            return None

# ═══════════════════════════════════════════════════
# 技术指标计算
# ═══════════════════════════════════════════════════

class TechnicalAnalyzer:
    """技术指标分析器"""
    
    @staticmethod
    def calculate_ma(prices: List[float], period: int) -> float:
        """计算移动平均线"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        return sum(prices[-period:]) / period
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        """计算指数移动平均线"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:period]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """计算RSI"""
        if len(prices) < period + 1:
            return 50.0  # 默认中性
        
        # 计算价格变化
        changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        
        # 分离涨跌
        gains = [max(change, 0) for change in changes[-period:]]
        losses = [abs(min(change, 0)) for change in changes[-period:]]
        
        # 平均涨跌幅
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_macd(prices: List[float]) -> Dict[str, Any]:
        """计算MACD"""
        if len(prices) < 26:
            return {
                "macd": 0,
                "signal": 0,
                "histogram": 0,
                "trend": "neutral"
            }
        
        # EMA 12 和 EMA 26
        ema_12 = TechnicalAnalyzer.calculate_ema(prices, 12)
        ema_26 = TechnicalAnalyzer.calculate_ema(prices, 26)
        
        macd = ema_12 - ema_26
        signal = macd * 0.2  # 简化计算
        histogram = macd - signal
        
        # 判断趋势
        if macd > signal and histogram > 0:
            trend = "bullish"
        elif macd < signal and histogram < 0:
            trend = "bearish"
        else:
            trend = "neutral"
        
        return {
            "macd": round(macd, 2),
            "signal": round(signal, 2),
            "histogram": round(histogram, 2),
            "trend": trend
        }
    
    @staticmethod
    def calculate_bollinger(prices: List[float], period: int = 20, std_dev: float = 2) -> Dict[str, float]:
        """计算布林带"""
        if len(prices) < period:
            current_price = prices[-1] if prices else 0
            return {
                "upper": current_price * 1.05,
                "middle": current_price,
                "lower": current_price * 0.95
            }
        
        # 中轨（MA）
        middle = sum(prices[-period:]) / period
        
        # 标准差
        variance = sum((p - middle) ** 2 for p in prices[-period:]) / period
        std = variance ** 0.5
        
        # 上下轨
        upper = middle + (std_dev * std)
        lower = middle - (std_dev * std)
        
        return {
            "upper": round(upper, 2),
            "middle": round(middle, 2),
            "lower": round(lower, 2)
        }
    
    @staticmethod
    def analyze(prices: List[float]) -> TechnicalIndicators:
        """完整技术分析"""
        ma_20 = TechnicalAnalyzer.calculate_ma(prices, 20)
        ma_50 = TechnicalAnalyzer.calculate_ma(prices, 50)
        ma_200 = TechnicalAnalyzer.calculate_ma(prices, 200) if len(prices) >= 200 else None
        
        rsi = TechnicalAnalyzer.calculate_rsi(prices)
        macd = TechnicalAnalyzer.calculate_macd(prices)
        bollinger = TechnicalAnalyzer.calculate_bollinger(prices)
        
        return TechnicalIndicators(
            ma_20=round(ma_20, 2),
            ma_50=round(ma_50, 2),
            ma_200=round(ma_200, 2) if ma_200 else None,
            rsi=round(rsi, 2),
            macd=macd,
            bollinger_bands=bollinger
        )

# ═══════════════════════════════════════════════════
# 交易信号生成器
# ═══════════════════════════════════════════════════

class SignalGenerator:
    """交易信号生成器"""
    
    @staticmethod
    def generate(current_price: float, indicators: TechnicalIndicators) -> TradingSignal:
        """
        生成交易信号
        
        Args:
            current_price: 当前价格
            indicators: 技术指标
        """
        signals = []
        reasons = []
        total_weight = 0
        
        # MA信号（权重30%）
        if indicators.ma_20 > indicators.ma_50:
            signals.append(("BUY", 0.3))
            reasons.append("MA20 > MA50（多头趋势）")
        elif indicators.ma_20 < indicators.ma_50:
            signals.append(("SELL", 0.3))
            reasons.append("MA20 < MA50（空头趋势）")
        else:
            signals.append(("HOLD", 0.3))
            reasons.append("MA趋势中性")
        total_weight += 0.3
        
        # RSI信号（权重30%）
        if indicators.rsi < 30:
            signals.append(("BUY", 0.3))
            reasons.append(f"RSI={indicators.rsi}（超卖）")
        elif indicators.rsi > 70:
            signals.append(("SELL", 0.3))
            reasons.append(f"RSI={indicators.rsi}（超买）")
        else:
            signals.append(("HOLD", 0.3))
            reasons.append(f"RSI={indicators.rsi}（健康区间）")
        total_weight += 0.3
        
        # MACD信号（权重40%）
        if indicators.macd['trend'] == 'bullish':
            signals.append(("BUY", 0.4))
            reasons.append("MACD金叉（看涨）")
        elif indicators.macd['trend'] == 'bearish':
            signals.append(("SELL", 0.4))
            reasons.append("MACD死叉（看跌）")
        else:
            signals.append(("HOLD", 0.4))
            reasons.append("MACD趋势中性")
        total_weight += 0.4
        
        # 计算综合信号
        buy_score = sum(weight for signal, weight in signals if signal == "BUY")
        sell_score = sum(weight for signal, weight in signals if signal == "SELL")
        hold_score = sum(weight for signal, weight in signals if signal == "HOLD")
        
        # 确定最终信号
        max_score = max(buy_score, sell_score, hold_score)
        
        if max_score == buy_score:
            final_signal = "BUY"
            confidence = buy_score / total_weight
        elif max_score == sell_score:
            final_signal = "SELL"
            confidence = sell_score / total_weight
        else:
            final_signal = "HOLD"
            confidence = hold_score / total_weight
        
        # 风险评估
        if confidence > 0.7:
            risk_level = "low"
        elif confidence > 0.5:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return TradingSignal(
            symbol="",
            signal=final_signal,
            confidence=round(confidence, 2),
            reasons=reasons,
            risk_level=risk_level,
            timestamp=int(time.time())
        )

# ═══════════════════════════════════════════════════
# SkillPay 计费集成
# ═══════════════════════════════════════════════════

class BillingClient:
    """SkillPay 计费客户端"""
    
    def __init__(self):
        self.api_key = SKILLPAY_API_KEY
        self.skill_id = CRYPTO_SKILL_ID
    
    def check_balance(self, user_id: str) -> Dict[str, Any]:
        """检查用户余额"""
        try:
            resp = requests.post(
                f"{SKILLPAY_API}/balance",
                headers={
                    "X-API-Key": self.api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "user_id": user_id,
                    "skill_id": self.skill_id
                },
                timeout=5
            )
            
            data = resp.json()
            
            if data.get("success"):
                return {
                    "ok": True,
                    "balance": data.get("balance")
                }
            else:
                return {
                    "ok": False,
                    "balance": data.get("balance", 0),
                    "payment_url": data.get("payment_url")
                }
        
        except Exception as e:
            return {
                "ok": False,
                "error": str(e)
            }
    
    def charge_user(self, user_id: str, amount: float = 0.05) -> Dict[str, Any]:
        """扣费"""
        try:
            resp = requests.post(
                f"{SKILLPAY_API}/charge",
                headers={
                    "X-API-Key": self.api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "user_id": user_id,
                    "skill_id": self.skill_id,
                    "amount": amount,
                    "currency": "USDT"
                },
                timeout=5
            )
            
            data = resp.json()
            
            if data.get("success"):
                return {
                    "ok": True,
                    "balance": data.get("balance")
                }
            else:
                return {
                    "ok": False,
                    "balance": data.get("balance", 0),
                    "payment_url": data.get("payment_url")
                }
        
        except Exception as e:
            return {
                "ok": False,
                "error": str(e)
            }

# ═══════════════════════════════════════════════════
# 付费版本（集成SkillPay）
# ═══════════════════════════════════════════════════

class CryptoAnalyzerPaid:
    """付费版本（集成SkillPay）"""
    
    def __init__(self):
        self.client = CoinGeckoClient()
        self.analyzer = TechnicalAnalyzer()
        self.signal_gen = SignalGenerator()
        self.billing = BillingClient()
    
    def get_price(self, coin_id: str, user_id: str, format: str = "json") -> Dict[str, Any]:
        """
        获取实时价格（付费版）
        
        Args:
            coin_id: 币种ID
            user_id: 用户ID
            format: 输出格式
        """
        # 1. 检查余额
        balance_check = self.billing.check_balance(user_id)
        
        if not balance_check.get("ok"):
            return {
                "error": "余额不足",
                "balance": balance_check.get("balance", 0),
                "payment_url": balance_check.get("payment_url"),
                "message": "请充值后继续使用（最低充值$8）"
            }
        
        # 2. 获取数据
        crypto_data = self.client.get_price(coin_id)
        
        if not crypto_data:
            return {
                "error": "获取数据失败",
                "message": "请检查币种名称或稍后重试"
            }
        
        # 3. 扣费
        charge_result = self.billing.charge_user(user_id, 0.05)
        
        if not charge_result.get("ok"):
            return {
                "error": "扣费失败",
                "balance": charge_result.get("balance", 0),
                "payment_url": charge_result.get("payment_url"),
                "message": "余额不足，请充值"
            }
        
        # 4. 返回结果
        result = asdict(crypto_data)
        result["charged"] = 0.05
        result["balance"] = charge_result.get("balance")
        
        if format == "json":
            return result
        else:
            return self._format_text(result)
    
    def analyze(self, coin_id: str, user_id: str, format: str = "json") -> Dict[str, Any]:
        """
        技术分析（付费版）
        
        Args:
            coin_id: 币种ID
            user_id: 用户ID
            format: 输出格式
        """
        # 1. 检查余额
        balance_check = self.billing.check_balance(user_id)
        
        if not balance_check.get("ok"):
            return {
                "error": "余额不足",
                "balance": balance_check.get("balance", 0),
                "payment_url": balance_check.get("payment_url"),
                "message": "请充值后继续使用（最低充值$8）"
            }
        
        # 2. 获取历史数据
        prices = self.client.get_price_history(coin_id, 90)
        
        if not prices:
            return {
                "error": "获取历史数据失败",
                "message": "请检查币种名称或稍后重试"
            }
        
        # 3. 技术分析
        indicators = self.analyzer.analyze(prices)
        crypto_data = self.client.get_price(coin_id)
        
        if not crypto_data:
            return {
                "error": "获取实时价格失败"
            }
        
        # 4. 扣费
        charge_result = self.billing.charge_user(user_id, 0.05)
        
        if not charge_result.get("ok"):
            return {
                "error": "扣费失败",
                "balance": charge_result.get("balance", 0),
                "payment_url": charge_result.get("payment_url"),
                "message": "余额不足，请充值"
            }
        
        # 5. 返回结果
        result = {
            "symbol": coin_id,
            "name": crypto_data.name,
            "price": crypto_data.price,
            "change_24h": crypto_data.change_24h,
            "indicators": asdict(indicators),
            "charged": 0.05,
            "balance": charge_result.get("balance"),
            "timestamp": int(time.time())
        }
        
        if format == "json":
            return result
        else:
            return self._format_text(result)
    
    def signal(self, coin_id: str, user_id: str, format: str = "json") -> Dict[str, Any]:
        """
        交易信号（付费版）
        
        Args:
            coin_id: 币种ID
            user_id: 用户ID
            format: 输出格式
        """
        # 1. 检查余额
        balance_check = self.billing.check_balance(user_id)
        
        if not balance_check.get("ok"):
            return {
                "error": "余额不足",
                "balance": balance_check.get("balance", 0),
                "payment_url": balance_check.get("payment_url"),
                "message": "请充值后继续使用（最低充值$8）"
            }
        
        # 2. 获取历史数据
        prices = self.client.get_price_history(coin_id, 90)
        
        if not prices:
            return {
                "error": "获取历史数据失败",
                "message": "请检查币种名称或稍后重试"
            }
        
        # 3. 技术分析
        indicators = self.analyzer.analyze(prices)
        crypto_data = self.client.get_price(coin_id)
        
        if not crypto_data:
            return {
                "error": "获取实时价格失败"
            }
        
        # 4. 生成信号
        signal = self.signal_gen.generate(crypto_data.price, indicators)
        signal.symbol = coin_id
        
        # 5. 扣费
        charge_result = self.billing.charge_user(user_id, 0.05)
        
        if not charge_result.get("ok"):
            return {
                "error": "扣费失败",
                "balance": charge_result.get("balance", 0),
                "payment_url": charge_result.get("payment_url"),
                "message": "余额不足，请充值"
            }
        
        # 6. 返回结果
        result = asdict(signal)
        result["name"] = crypto_data.name
        result["price"] = crypto_data.price
        result["charged"] = 0.05
        result["balance"] = charge_result.get("balance")
        
        if format == "json":
            return result
        else:
            return self._format_signal_text(result)
    
    def _format_text(self, data: Dict[str, Any]) -> str:
        """格式化文本"""
        text = f"""
币种: {data.get('symbol', '').upper()}
名称: {data.get('name', '')}
价格: ${data.get('price', 0):,.2f}
24h涨跌: {data.get('change_24h', 0):+.2f}%
市值: ${data.get('market_cap', 0):,.0f}
24h成交量: ${data.get('volume_24h', 0):,.0f}

扣费: ${data.get('charged', 0):.2f}
余额: ${data.get('balance', 0):.2f}

时间: {datetime.fromtimestamp(data.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}
"""
        return text.strip()
    
    def _format_signal_text(self, data: Dict[str, Any]) -> str:
        """格式化信号文本"""
        signal_emoji = {
            "BUY": "🟢",
            "SELL": "🔴",
            "HOLD": "🟡"
        }
        
        risk_emoji = {
            "low": "✅",
            "medium": "⚠️",
            "high": "❗"
        }
        
        text = f"""
{signal_emoji.get(data.get('signal', 'HOLD'), '🟡')} 交易信号: {data.get('signal', 'HOLD')}
币种: {data.get('name', '')} ({data.get('symbol', '').upper()})
价格: ${data.get('price', 0):,.2f}

置信度: {data.get('confidence', 0) * 100:.0f}%
风险等级: {risk_emoji.get(data.get('risk_level', 'medium'), '⚠️')} {data.get('risk_level', 'medium').upper()}

理由:
{chr(10).join(f'• {reason}' for reason in data.get('reasons', []))}

扣费: ${data.get('charged', 0):.2f}
余额: ${data.get('balance', 0):.2f}

⚠️ 免责声明: 信号仅供参考，不构成投资建议

时间: {datetime.fromtimestamp(data.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}
"""
        return text.strip()

# ═══════════════════════════════════════════════════
# 命令行接口
# ═══════════════════════════════════════════════════

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='CryptoScope - 加密货币数据分析助手 v1.0.0')
    
    parser.add_argument('command', choices=['price', 'analyze', 'signal', 'test'], help='命令')
    parser.add_argument('coin', type=str, nargs='?', help='币种ID（如bitcoin, ethereum）')
    parser.add_argument('--user-id', type=str, help='用户ID（付费版必填）')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    # 测试模式
    if args.command == 'test':
        print("🧪 测试CoinGecko API...")
        
        client = CoinGeckoClient()
        data = client.get_price('bitcoin')
        
        if data:
            print(f"✅ Bitcoin价格: ${data.price:,.2f}")
            print(f"✅ 24h涨跌: {data.change_24h:+.2f}%")
        else:
            print("❌ API测试失败")
        
        return
    
    # 付费模式（需要user_id）
    if not args.user_id:
        print("❌ 错误: 付费版本需要 --user-id 参数")
        print("示例: python3 crypto_analyzer.py price bitcoin --user-id user123")
        sys.exit(1)
    
    if not args.coin:
        print("❌ 错误: 请指定币种ID")
        print("示例: python3 crypto_analyzer.py price bitcoin --user-id user123")
        sys.exit(1)
    
    # 执行命令
    analyzer = CryptoAnalyzerPaid()
    
    if args.command == 'price':
        result = analyzer.get_price(args.coin, args.user_id, args.format)
    elif args.command == 'analyze':
        result = analyzer.analyze(args.coin, args.user_id, args.format)
    elif args.command == 'signal':
        result = analyzer.signal(args.coin, args.user_id, args.format)
    
    # 输出结果
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
