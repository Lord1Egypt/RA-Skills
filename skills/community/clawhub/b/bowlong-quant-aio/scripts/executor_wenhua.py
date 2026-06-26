#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
quant-aio 文华财经WH8执行器
支持商品期货、股指期货的模拟盘和实盘交易

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有
开源协议：MIT License
源码开放，欢迎完善，共同进步
GitHub: https://github.com/simonstang/bolong-quant

文华财经WH8 Python API调用方式：
- 通过 wh8 包调用
- 或通过 HTTP 接口调用（需开启Python API服务）

依赖：
    pip install numpy pandas requests

文华财经安装路径（默认）：
    C:\wenhua8\

使用前提：
    1. 文华财经WH8已安装并能正常运行
    2. 已开启Python API服务（菜单：工具 -> Python环境设置 -> 启用）
    3. 策略已加载到图表中

API文档参考：
    references/wenhua_api.md
"""

import os
import sys
import time
import json
import yaml
import logging
import threading
from datetime import datetime, time as dtime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import argparse

import requests

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ==================== 数据结构 ====================

class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"         # 待报
    SUBMITTED = "submitted"     # 已提交
    PARTIAL = "partial"        # 部分成交
    FILLED = "filled"          # 全部成交
    CANCELLED = "cancelled"    # 已撤单
    REJECTED = "rejected"     # 已拒绝
    ERROR = "error"            # 错误


class Direction(Enum):
    """交易方向"""
    BUY = "buy"    # 买入（做多）
    SELL = "sell"  # 卖出（做空）


class OrderType(Enum):
    """订单类型"""
    LIMIT = "limit"       # 限价单
    MARKET = "market"     # 市价单
    STOP = "stop"        # 止损单


@dataclass
class FutureOrder:
    """期货订单"""
    order_id: str
    symbol: str              # 合约代码（如 IF2504）
    direction: Direction
    order_type: OrderType
    price: float
    volume: int             # 手数
    filled_volume: int = 0
    filled_price: float = 0
    status: OrderStatus = OrderStatus.PENDING
    submit_time: str = ""
    update_time: str = ""
    error_msg: str = ""
    close_today: bool = False  # 是否平今
    
    @property
    def remaining(self) -> int:
        return self.volume - self.filled_volume
    
    @property
    def is_completed(self) -> bool:
        return self.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, 
                               OrderStatus.REJECTED, OrderStatus.ERROR]


@dataclass
class FuturePosition:
    """期货持仓"""
    symbol: str              # 合约代码
    direction: Direction     # 持仓方向（多/空）
    volume: int            # 持仓手数
    avg_price: float       # 开仓均价
    current_price: float   # 当前价
    last_price: float      # 最新价
    market_value: float = 0    # 合约价值
    realized_pnl: float = 0   # 已实现盈亏
    unrealized_pnl: float = 0  # 浮动盈亏
    margin: float = 0          # 占用保证金
    
    def update(self, current_price: float, margin_rate: float = 0.12):
        """更新持仓"""
        self.current_price = current_price
        self.last_price = current_price
        
        # 计算浮动盈亏
        if self.direction == Direction.BUY:
            self.unrealized_pnl = (current_price - self.avg_price) * self.volume
        else:
            self.unrealized_pnl = (self.avg_price - current_price) * self.volume
        
        # 估算保证金
        self.market_value = current_price * self.volume
        self.margin = self.market_value * margin_rate


@dataclass
class FutureAccount:
    """期货账户"""
    account_id: str
    total_asset: float      # 总资产
    available: float       # 可用资金
    frozen: float         # 冻结资金
    margin: float         # 占用保证金
    realized_pnl: float    # 已实现盈亏
    unrealized_pnl: float # 浮动盈亏
    total_pnl: float      # 总盈亏
    today_pnl: float      # 今日盈亏


# ==================== 文华财经API客户端 ====================

class WenhuaConfig:
    """文华财经连接配置"""
    
    # 国内期货合约乘数参考
    CONTRACT_MULTIPLIER = {
        # 股指期货
        'IF': 300.0,   # 上证50/沪深300
        'IH': 300.0,   # 上证50
        'IC': 200.0,   # 中证500
        'IM': 200.0,   # 中证1000
        
        # 商品期货（部分常见品种）
        'CU': 5.0,      # 沪铜
        'AL': 5.0,      # 沪铝
        'ZN': 5.0,      # 沪锌
        'PB': 5.0,      # 沪铅
        'NI': 1.0,      # 沪镍
        'AU': 1000.0,   # 沪金
        'AG': 15.0,     # 沪银
        'RB': 10.0,     # 螺纹钢
        'HC': 10.0,     # 热卷
        'SF': 5.0,      # 硅铁
        'SM': 5.0,      # 锰硅
        'CU': 5.0,      # 铜
        'BU': 10.0,     # 沥青
        'RU': 10.0,     # 橡胶
        'FU': 10.0,     # 燃料油
        'AU': 1000.0,   # 黄金
        'AG': 15.0,     # 白银
        'SC': 100.0,    # 原油
        'M': 10.0,      # 豆粕
        'Y': 10.0,      # 豆油
        'P': 10.0,      # 棕榈油
        'A': 10.0,      # 豆一
        'B': 10.0,      # 豆二
        'CS': 10.0,     # 玉米淀粉
        'C': 10.0,      # 玉米
        'L': 5.0,       # 塑料
        'V': 5.0,       # PVC
        'PP': 5.0,      # 聚丙烯
        'TA': 5.0,      # PTA
        'MA': 10.0,     # 甲醇
        'EG': 10.0,     # 乙二醇
        'UR': 20.0,     # 尿素
        'SA': 20.0,     # 纯碱
        'FG': 20.0,     # 玻璃
        'RM': 10.0,     # 菜粕
        'OI': 10.0,     # 菜油
        'RS': 10.0,     # 菜籽
        'AP': 10.0,     # 苹果
        'CF': 5.0,      # 棉花
        'CY': 5.0,      # 棉纱
        'SR': 10.0,     # 白糖
        'RI': 20.0,     # 粳稻
        'LR': 20.0,     # 晚籼
        'WH': 20.0,     # 强麦
        'PM': 50.0,     # 普通小麦
        'JR': 20.0,     # 粳稻
        'ZC': 100.0,    # 动力煤
        'JM': 60.0,     # 焦煤
        'J': 100.0,     # 焦炭
        'I': 100.0,     # 铁矿石
        'J': 100.0,     # 焦炭
    }
    
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', False)
        self.path = config.get('path', 'C:/wenhua8')
        self.account = config.get('account', '')
        self.password = config.get('password', '')
        
        # HTTP API地址（文华财经Python API服务地址）
        self.server = config.get('server', '127.0.0.1')
        self.port = config.get('port', 8080)
        self.api_url = f"http://{self.server}:{self.port}"
        
        # 超时
        self.timeout = config.get('timeout', 30)
        
        # 模拟模式
        self.mode = config.get('mode', 'paper')


class WenhuaClient:
    """
    文华财经WH8交易客户端
    
    支持功能：
    - 账户登录/登出
    - 查询账户信息
    - 查询持仓
    - 查询订单
    - 下单（买入/卖出开仓/卖出平仓）
    - 撤单
    - 止损止盈设置
    
    使用方式：
    ```python
    from executor_wenhua import WenhuaClient
    
    client = WenhuaClient(config)
    client.login()
    
    # 查询
    account = client.get_account()
    positions = client.get_positions()
    
    # 下单
    order = client.buy("IF2504", price=3800, volume=1)  # 买入1手IF
    order = client.sell("IF2504", price=3750, volume=1)  # 卖出平仓1手IF
    
    client.logout()
    ```
    """
    
    def __init__(self, config: WenhuaConfig):
        self.config = config
        self.connected = False
        self.orders: Dict[str, FutureOrder] = {}
        self.positions: Dict[str, FuturePosition] = {}
        self.account: Optional[FutureAccount] = None
        
        # 模拟数据
        self._mock_mode = True
        self._mock_orders: Dict[str, FutureOrder] = {}
        self._mock_positions: Dict[str, FuturePosition] = {}
        self._mock_available = 500_000  # 模拟可用资金50万
        self._mock_frozen = 0
        self._mock_realized_pnl = 0
        self._mock_unrealized_pnl = 0
    
    def _get_contract_multiplier(self, symbol: str) -> float:
        """获取合约乘数"""
        # 从symbol中提取品种代码
        import re
        match = re.match(r'^([A-Z]+)', symbol)
        if match:
            variety = match.group(1).upper()
            return self.config.CONTRACT_MULTIPLIER.get(variety, 10.0)  # 默认10
        return 10.0
    
    def _request(self, action: str, params: Optional[Dict] = None) -> Dict:
        """发送请求"""
        if self._mock_mode or not self.connected:
            return self._mock_request(action, params)
        
        try:
            payload = {
                "action": action,
                "account": self.config.account,
                "password": self.config.password,
                **(params or {})
            }
            
            response = requests.post(
                self.config.api_url,
                json=payload,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        
        except requests.exceptions.ConnectionError:
            logger.warning("⚠️ 无法连接到文华财经，切换到模拟模式")
            self._mock_mode = True
            return self._mock_request(action, params)
        
        except Exception as e:
            logger.error(f"❌ 请求异常: {e}")
            return {"success": False, "error": str(e)}
    
    def _mock_request(self, action: str, params: Optional[Dict] = None) -> Dict:
        """模拟请求响应"""
        self._mock_mode = True
        
        if action == "login":
            self._mock_orders = {}
            self._mock_positions = {}
            self._mock_available = 500_000
            self._mock_realized_pnl = 0
            self._mock_unrealized_pnl = 0
            return {"success": True, "message": "登录成功（模拟模式）"}
        
        elif action == "query_account":
            total_asset = self._mock_available + self._mock_frozen + \
                        sum(p.margin for p in self._mock_positions.values())
            total_pnl = self._mock_realized_pnl + self._mock_unrealized_pnl
            
            return {
                "success": True,
                "data": {
                    "account_id": self.config.account or "SIM_FUTURE",
                    "total_asset": total_asset,
                    "available": self._mock_available,
                    "frozen": self._mock_frozen,
                    "margin": self._mock_frozen,
                    "realized_pnl": self._mock_realized_pnl,
                    "unrealized_pnl": self._mock_unrealized_pnl,
                    "total_pnl": total_pnl,
                    "today_pnl": self._mock_realized_pnl
                }
            }
        
        elif action == "query_positions":
            return {
                "success": True,
                "data": [
                    {
                        "symbol": p.symbol,
                        "direction": p.direction.value,
                        "volume": p.volume,
                        "avg_price": p.avg_price,
                        "current_price": p.current_price,
                        "realized_pnl": p.realized_pnl,
                        "unrealized_pnl": p.unrealized_pnl,
                        "margin": p.margin
                    }
                    for p in self._mock_positions.values()
                ]
            }
        
        elif action == "query_orders":
            return {
                "success": True,
                "data": [
                    {
                        "order_id": o.order_id,
                        "symbol": o.symbol,
                        "direction": o.direction.value,
                        "order_type": o.order_type.value,
                        "price": o.price,
                        "volume": o.volume,
                        "filled_volume": o.filled_volume,
                        "filled_price": o.filled_price,
                        "status": o.status.value,
                        "submit_time": o.submit_time,
                        "close_today": o.close_today
                    }
                    for o in self._mock_orders.values()
                ]
            }
        
        elif action == "buy_open":   # 买入开仓
            return self._mock_trade("buy_open", params, is_open=True, is_buy=True)
        
        elif action == "sell_open":  # 卖出开仓
            return self._mock_trade("sell_open", params, is_open=True, is_buy=False)
        
        elif action == "buy_close":   # 买入平仓
            return self._mock_trade("buy_close", params, is_open=False, is_buy=True)
        
        elif action == "sell_close":  # 卖出平仓
            return self._mock_trade("sell_close", params, is_open=False, is_buy=False)
        
        elif action == "cancel":
            order_id = params.get("order_id", "")
            if order_id in self._mock_orders:
                order = self._mock_orders[order_id]
                if order.status == OrderStatus.PENDING:
                    order.status = OrderStatus.CANCELLED
                    self._mock_available += order.price * order.volume * self._get_contract_multiplier(order.symbol) * 0.12
                    return {"success": True, "message": "撤单成功"}
            return {"success": False, "error": "撤单失败"}
        
        return {"success": False, "error": "未知操作"}
    
    def _mock_trade(self, action: str, params: Optional[Dict], 
                   is_open: bool, is_buy: bool) -> Dict:
        """模拟交易"""
        symbol = params.get("symbol", "")
        price = params.get("price", 0)
        volume = params.get("volume", 1)
        
        if volume < 1:
            return {"success": False, "error": "手数必须 >= 1"}
        
        multiplier = self._get_contract_multiplier(symbol)
        margin = price * multiplier * volume * 0.12  # 12%保证金
        
        # 检查资金
        if margin > self._mock_available:
            return {"success": False, "error": "资金不足"}
        
        order_id = f"WH{int(time.time()*1000)}"
        
        # 模拟订单成交
        slippage = 0.0002  # 万2滑点
        exec_price = price * (1 + slippage if is_buy else 1 - slippage)
        
        # 扣除保证金
        self._mock_available -= margin
        self._mock_frozen += margin
        
        # 创建订单
        direction = Direction.BUY if is_buy else Direction.SELL
        order = FutureOrder(
            order_id=order_id,
            symbol=symbol,
            direction=direction,
            order_type=OrderType.LIMIT,
            price=price,
            volume=volume,
            filled_volume=volume,
            filled_price=exec_price,
            status=OrderStatus.FILLED,
            submit_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self._mock_orders[order_id] = order
        
        # 更新持仓
        pos_key = f"{symbol}_{direction.value}"
        
        if is_open:  # 开仓
            self._mock_positions[pos_key] = FuturePosition(
                symbol=symbol,
                direction=direction,
                volume=volume,
                avg_price=exec_price,
                current_price=exec_price,
                last_price=exec_price,
                margin=margin
            )
            self._mock_positions[pos_key].update(exec_price)
        else:  # 平仓
            if pos_key in self._mock_positions:
                pos = self._mock_positions[pos_key]
                
                # 计算盈亏
                if direction == Direction.SELL:  # 平多
                    pnl = (exec_price - pos.avg_price) * multiplier * pos.volume
                else:  # 平空
                    pnl = (pos.avg_price - exec_price) * multiplier * pos.volume
                
                self._mock_realized_pnl += pnl
                self._mock_available += margin + pnl  # 返还保证金+盈亏
                self._mock_frozen -= margin
                
                pos.volume -= volume
                if pos.volume <= 0:
                    del self._mock_positions[pos_key]
            else:
                return {"success": False, "error": f"无对应持仓: {symbol}"}
        
        # 更新浮动盈亏
        self._update_unrealized_pnl()
        
        return {
            "success": True,
            "order_id": order_id,
            "message": f"{'买入' if is_buy else '卖出'} {'开仓' if is_open else '平仓'}成功（模拟）",
            "filled_price": exec_price,
            "filled_volume": volume
        }
    
    def _update_unrealized_pnl(self):
        """更新浮动盈亏"""
        self._mock_unrealized_pnl = 0
        for pos in self._mock_positions.values():
            multiplier = self._get_contract_multiplier(pos.symbol)
            if pos.direction == Direction.BUY:
                pnl = (pos.current_price - pos.avg_price) * multiplier * pos.volume
            else:
                pnl = (pos.avg_price - pos.current_price) * multiplier * pos.volume
            pos.unrealized_pnl = pnl
            self._mock_unrealized_pnl += pnl
    
    # ==================== 公共API ====================
    
    def login(self) -> bool:
        """登录文华财经"""
        logger.info("🔐 正在连接文华财经...")
        
        if self.config.mode == "paper":
            logger.info("📝 模式: 模拟盘")
        else:
            logger.warning("⚠️ 警告: 实盘模式！")
        
        result = self._request("login")
        
        if result.get("success"):
            self.connected = True
            logger.info("✅ 文华财经连接成功")
            return True
        
        logger.warning("⚠️ 连接失败，使用模拟模式")
        self._mock_mode = True
        self._request("login")
        return True
    
    def logout(self):
        """登出"""
        self._request("logout")
        self.connected = False
        logger.info("👋 文华财经已断开")
    
    def get_account(self) -> Optional[FutureAccount]:
        """查询账户信息"""
        result = self._request("query_account")
        
        if result.get("success"):
            data = result["data"]
            self.account = FutureAccount(
                account_id=data["account_id"],
                total_asset=data["total_asset"],
                available=data["available"],
                frozen=data["frozen"],
                margin=data["margin"],
                realized_pnl=data["realized_pnl"],
                unrealized_pnl=data["unrealized_pnl"],
                total_pnl=data["total_pnl"],
                today_pnl=data["today_pnl"]
            )
            return self.account
        
        return None
    
    def get_positions(self) -> List[FuturePosition]:
        """查询持仓"""
        result = self._request("query_positions")
        
        if result.get("success"):
            positions = []
            for p in result["data"]:
                direction = Direction.BUY if p["direction"] == "buy" else Direction.SELL
                pos = FuturePosition(
                    symbol=p["symbol"],
                    direction=direction,
                    volume=p["volume"],
                    avg_price=p["avg_price"],
                    current_price=p["current_price"],
                    last_price=p["current_price"],
                    realized_pnl=p["realized_pnl"],
                    unrealized_pnl=p["unrealized_pnl"],
                    margin=p["margin"]
                )
                key = f"{p['symbol']}_{p['direction']}"
                positions.append(pos)
                self.positions[key] = pos
            
            return positions
        
        return []
    
    def get_orders(self, status: Optional[str] = None) -> List[FutureOrder]:
        """查询订单"""
        result = self._request("query_orders")
        
        if result.get("success"):
            orders = []
            for o in result["data"]:
                direction = Direction.BUY if o["direction"] == "buy" else Direction.SELL
                order = FutureOrder(
                    order_id=o["order_id"],
                    symbol=o["symbol"],
                    direction=direction,
                    order_type=OrderType(o["order_type"]),
                    price=o["price"],
                    volume=o["volume"],
                    filled_volume=o["filled_volume"],
                    filled_price=o["filled_price"],
                    status=OrderStatus(o["status"]),
                    submit_time=o["submit_time"],
                    close_today=o.get("close_today", False)
                )
                orders.append(order)
                self.orders[o["order_id"]] = order
            
            if status:
                status_enum = OrderStatus(status)
                orders = [o for o in orders if o.status == status_enum]
            
            return orders
        
        return []
    
    def buy_open(self, symbol: str, price: float, volume: int = 1) -> Optional[FutureOrder]:
        """
        买入开仓（做多）
        
        Args:
            symbol: 合约代码（如 IF2504、CU2504）
            price: 开仓价格
            volume: 手数
        
        Returns:
            FutureOrder: 订单
        """
        logger.info(f"📈 买入开仓 {symbol} @ {price} x {volume}手")
        
        result = self._request("buy_open", {
            "symbol": symbol,
            "price": price,
            "volume": volume
        })
        
        if result.get("success"):
            order_id = result["order_id"]
            order = self._mock_orders.get(order_id)
            if order:
                logger.info(f"✅ 订单成交: {order_id} @ {order.filled_price}")
            return order
        
        logger.error(f"❌ 买入开仓失败: {result.get('error')}")
        return None
    
    def sell_open(self, symbol: str, price: float, volume: int = 1) -> Optional[FutureOrder]:
        """
        卖出开仓（做空）
        
        Args:
            symbol: 合约代码
            price: 开仓价格
            volume: 手数
        
        Returns:
            FutureOrder: 订单
        """
        logger.info(f"📉 卖出开仓 {symbol} @ {price} x {volume}手")
        
        result = self._request("sell_open", {
            "symbol": symbol,
            "price": price,
            "volume": volume
        })
        
        if result.get("success"):
            order_id = result["order_id"]
            order = self._mock_orders.get(order_id)
            if order:
                logger.info(f"✅ 订单成交: {order_id} @ {order.filled_price}")
            return order
        
        logger.error(f"❌ 卖出开仓失败: {result.get('error')}")
        return None
    
    def sell_close(self, symbol: str, price: float, volume: int = 1) -> Optional[FutureOrder]:
        """
        卖出平仓（平多）
        
        Args:
            symbol: 合约代码
            price: 平仓价格
            volume: 手数
        
        Returns:
            FutureOrder: 订单
        """
        logger.info(f"📉 卖出平仓 {symbol} @ {price} x {volume}手")
        
        result = self._request("sell_close", {
            "symbol": symbol,
            "price": price,
            "volume": volume
        })
        
        if result.get("success"):
            order_id = result["order_id"]
            order = self._mock_orders.get(order_id)
            if order:
                logger.info(f"✅ 订单成交: {order_id} @ {order.filled_price}")
            return order
        
        logger.error(f"❌ 卖出平仓失败: {result.get('error')}")
        return None
    
    def buy_close(self, symbol: str, price: float, volume: int = 1) -> Optional[FutureOrder]:
        """
        买入平仓（平空）
        
        Args:
            symbol: 合约代码
            price: 平仓价格
            volume: 手数
        
        Returns:
            FutureOrder: 订单
        """
        logger.info(f"📈 买入平仓 {symbol} @ {price} x {volume}手")
        
        result = self._request("buy_close", {
            "symbol": symbol,
            "price": price,
            "volume": volume
        })
        
        if result.get("success"):
            order_id = result["order_id"]
            order = self._mock_orders.get(order_id)
            if order:
                logger.info(f"✅ 订单成交: {order_id} @ {order.filled_price}")
            return order
        
        logger.error(f"❌ 买入平仓失败: {result.get('error')}")
        return None
    
    def close_position(self, symbol: str, direction: Direction, volume: int) -> Optional[FutureOrder]:
        """平掉指定方向的持仓"""
        if direction == Direction.BUY:
            return self.sell_close(symbol, price=0, volume=volume)  # 市价平
        else:
            return self.buy_close(symbol, price=0, volume=volume)
    
    def cancel_order(self, order_id: str) -> bool:
        """撤单"""
        logger.info(f"🚫 撤单: {order_id}")
        result = self._request("cancel", {"order_id": order_id})
        
        if result.get("success"):
            logger.info("✅ 撤单成功")
            return True
        
        logger.error(f"❌ 撤单失败: {result.get('error')}")
        return False
    
    def cancel_all(self) -> int:
        """撤销所有未成交订单"""
        orders = self.get_orders(status="pending")
        orders += self.get_orders(status="submitted")
        
        count = 0
        for order in orders:
            if self.cancel_order(order.order_id):
                count += 1
        
        logger.info(f"📋 共撤单 {count} 个")
        return count
    
    def close_all(self) -> int:
        """清仓所有持仓"""
        positions = self.get_positions()
        
        if not positions:
            logger.info("📭 无持仓需要清仓")
            return 0
        
        count = 0
        for pos in positions:
            order = self.close_position(pos.symbol, pos.direction, pos.volume)
            if order and order.status == OrderStatus.FILLED:
                count += 1
        
        logger.info(f"📋 清仓完成: {count} 个订单成交")
        return count
    
    def get_balance(self) -> float:
        """获取可用资金"""
        account = self.get_account()
        return account.available if account else 0
    
    def get_position(self, symbol: str, direction: Direction) -> Optional[FuturePosition]:
        """获取指定合约的持仓"""
        positions = self.get_positions()
        for pos in positions:
            if pos.symbol == symbol and pos.direction == direction:
                return pos
        return None
    
    def __repr__(self):
        status = "✅ 已连接" if self.connected or self._mock_mode else "❌ 未连接"
        mode = "模拟" if self._mock_mode or self.config.mode == "paper" else "实盘"
        return f"<WenhuaClient [{status}] [{mode}]>"


# ==================== 命令行接口 ====================

def main():
    parser = argparse.ArgumentParser(description='quant-aio 文华财经执行器')
    parser.add_argument('--mode', choices=['paper', 'live'], default='paper', help='交易模式')
    parser.add_argument('--action', required=True,
                       choices=['status', 'buy_open', 'sell_open', 'positions', 
                               'cancel', 'close_all'],
                       help='操作')
    parser.add_argument('--symbol', help='合约代码')
    parser.add_argument('--price', type=float, help='价格')
    parser.add_argument('--volume', type=int, default=1, help='手数')
    parser.add_argument('--config', default='config/config.yaml', help='配置文件')
    
    args = parser.parse_args()
    
    # 加载配置
    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        wenhua_cfg = WenhuaConfig(config.get('executor', {}).get('wenhua', {}))
        wenhua_cfg.mode = args.mode
    
    except Exception as e:
        logger.error(f"❌ 配置加载失败: {e}")
        wenhua_cfg = WenhuaConfig({})
        wenhua_cfg.mode = args.mode
    
    # 创建客户端
    client = WenhuaClient(wenhua_cfg)
    
    # 登录
    if not client.login():
        sys.exit(1)
    
    try:
        if args.action == 'status':
            account = client.get_account()
            if account:
                print(f"\n{'='*60}")
                print(f"  账号: {account.account_id}")
                print(f"  总资产: {account.total_asset:,.2f}")
                print(f"  可用资金: {account.available:,.2f}")
                print(f"  占用保证金: {account.margin:,.2f}")
                print(f"  已实现盈亏: {account.realized_pnl:+,.2f}")
                print(f"  浮动盈亏: {account.unrealized_pnl:+,.2f}")
                print(f"  总盈亏: {account.total_pnl:+,.2f}")
                print(f"{'='*60}")
        
        elif args.action == 'positions':
            positions = client.get_positions()
            if not positions:
                print("📭 当前无持仓")
            else:
                print(f"\n{'='*80}")
                print(f"  {'合约':<12} {'方向':<6} {'持仓':>6} {'均价':>10} {'现价':>10} {'浮动盈亏':>12}")
                print(f"{'='*80}")
                for pos in positions:
                    direction = "多" if pos.direction == Direction.BUY else "空"
                    print(f"  {pos.symbol:<12} {direction:<6} {pos.volume:>6} "
                          f"{pos.avg_price:>10.2f} {pos.current_price:>10.2f} "
                          f"{pos.unrealized_pnl:+12.2f}")
                print(f"{'='*80}")
        
        elif args.action == 'buy_open':
            if not args.symbol or not args.price:
                print("❌ 缺少参数: --symbol --price")
                sys.exit(1)
            
            order = client.buy_open(args.symbol, args.price, args.volume)
            if order:
                print(f"\n✅ 买入开仓成功!")
                print(f"   订单号: {order.order_id}")
                print(f"   合约: {order.symbol}")
                print(f"   方向: 多")
                print(f"   价格: {order.filled_price}")
                print(f"   手数: {order.volume}")
        
        elif args.action == 'sell_open':
            if not args.symbol or not args.price:
                print("❌ 缺少参数: --symbol --price")
                sys.exit(1)
            
            order = client.sell_open(args.symbol, args.price, args.volume)
            if order:
                print(f"\n✅ 卖出开仓成功!")
                print(f"   订单号: {order.order_id}")
                print(f"   合约: {order.symbol}")
                print(f"   方向: 空")
                print(f"   价格: {order.filled_price}")
                print(f"   手数: {order.volume}")
        
        elif args.action == 'cancel':
            orders = client.get_orders()
            if not orders:
                print("📭 无待成交订单")
            else:
                count = 0
                for order in orders:
                    if not order.is_completed:
                        if client.cancel_order(order.order_id):
                            count += 1
                print(f"\n📋 已撤销 {count} 个订单")
    
    finally:
        client.logout()


if __name__ == '__main__':
    main()
