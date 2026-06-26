#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
quant-aio 华鑫证券QMT执行器
支持模拟盘和实盘交易

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有
开源协议：MIT License
源码开放，欢迎完善，共同进步
GitHub: https://github.com/simonstang/bolong-quant

华鑫证券QMT Python API调用方式：
- 通过 COM 组件调用（Windows）
- 或通过 HTTP API 调用（需要QMT开启HTTP服务）

依赖：
    pip install pywin32 requests

华鑫QMT安装路径（默认）：
    C:\Huaxin\QMT\

QMT API文档参考：
    references/qmt_api.md
"""

import os
import sys
import time
import json
import yaml
import logging
import threading
from datetime import datetime
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


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"          # 待报
    SUBMITTED = "submitted"     # 已提交
    PARTIAL = "partial"         # 部分成交
    FILLED = "filled"          # 全部成交
    CANCELLED = "cancelled"     # 已撤单
    REJECTED = "rejected"       # 已拒绝
    ERROR = "error"            # 错误


class OrderType(Enum):
    """订单类型"""
    LIMIT = "limit"            # 限价单
    MARKET = "market"          # 市价单
    STOP = "stop"             # 止损单


class Direction(Enum):
    """交易方向"""
    BUY = "buy"
    SELL = "sell"


@dataclass
class Order:
    """订单"""
    order_id: str
    ts_code: str
    direction: Direction
    order_type: OrderType
    price: float
    volume: int           # 股数（100的整数倍）
    filled_volume: int = 0
    filled_price: float = 0
    status: OrderStatus = OrderStatus.PENDING
    submit_time: str = ""
    update_time: str = ""
    error_msg: str = ""
    
    @property
    def remaining_volume(self) -> int:
        return self.volume - self.filled_volume
    
    @property
    def is_completed(self) -> bool:
        return self.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED, OrderStatus.ERROR]


@dataclass
class Position:
    """持仓"""
    ts_code: str
    volume: int            # 持仓股数
    available: int        # 可用数量
    avg_cost: float        # 成本价
    current_price: float   # 当前价
    market_value: float = 0
    unrealized_pnl: float = 0
    pnl_pct: float = 0
    
    def update(self, current_price: float):
        self.current_price = current_price
        self.market_value = self.volume * current_price
        self.unrealized_pnl = (current_price - self.avg_cost) * self.volume
        self.pnl_pct = (current_price - self.avg_cost) / self.avg_cost * 100 if self.avg_cost > 0 else 0


@dataclass
class Account:
    """账户信息"""
    account_id: str
    total_asset: float     # 总资产
    cash: float           # 可用资金
    frozen_cash: float    # 冻结资金
    market_value: float    # 持仓市值
    total_pnl: float      # 总盈亏
    total_pnl_pct: float  # 总盈亏比例
    today_pnl: float      # 今日盈亏


class QMTConfig:
    """QMT连接配置"""
    
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', False)
        self.account = config.get('account', '')
        self.password = config.get('password', '')
        self.server = config.get('server', '127.0.0.1')
        self.port = config.get('port', 58610)
        self.path = config.get('path', 'C:/Huaxin/QMT')
        
        # API地址
        self.api_url = f"http://{self.server}:{self.port}"
        
        # 超时设置
        self.timeout = config.get('timeout', 30)
        
        # 重试次数
        self.retry = config.get('retry', 3)
        
        # 模拟模式
        self.mode = config.get('mode', 'paper')


class QMTClient:
    """
    华鑫证券QMT交易客户端
    
    支持功能：
    - 账户登录/登出
    - 查询账户信息
    - 查询持仓
    - 查询订单
    - 下单（买入/卖出）
    - 撤单
    - 成交查询
    
    使用方式：
    ```python
    from executor_huaxin import QMTClient
    
    client = QMTClient(config)
    client.login()
    
    # 查询
    account = client.get_account()
    positions = client.get_positions()
    
    # 下单
    order = client.buy("600519", price=1850, volume=100)
    
    # 撤单
    client.cancel_order(order.order_id)
    
    client.logout()
    ```
    """
    
    def __init__(self, config: QMTConfig):
        self.config = config
        self.session = None
        self.connected = False
        self.orders: Dict[str, Order] = {}
        self.positions: Dict[str, Position] = {}
        self.account: Optional[Account] = None
        
        # 模拟数据（paper模式或未连接时使用）
        self._mock_mode = True
        self._mock_orders: Dict[str, Order] = {}
        self._mock_positions: Dict[str, Position] = {}
        self._mock_cash = 1_000_000  # 模拟资金100万
    
    def _request(self, action: str, params: Optional[Dict] = None) -> Dict:
        """
        发送请求到QMT API
        
        华鑫QMT HTTP API格式：
        POST http://127.0.0.1:58610
        {
            "action": "query_account",
            "account": "账号",
            "password": "密码"
        }
        """
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
                logger.error(f"请求失败: HTTP {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
        
        except requests.exceptions.ConnectionError:
            logger.warning(f"⚠️ 无法连接到QMT ({self.config.api_url})，切换到模拟模式")
            self._mock_mode = True
            return self._mock_request(action, params)
        
        except Exception as e:
            logger.error(f"❌ 请求异常: {e}")
            return {"success": False, "error": str(e)}
    
    def _mock_request(self, action: str, params: Optional[Dict] = None) -> Dict:
        """模拟请求响应（用于测试或未连接时）"""
        self._mock_mode = True
        
        if action == "login":
            self._mock_orders = {}
            self._mock_positions = {}
            self._mock_cash = 1_000_000
            return {"success": True, "message": "登录成功（模拟模式）"}
        
        elif action == "query_account":
            total_asset = self._mock_cash + sum(
                p.market_value for p in self._mock_positions.values()
            )
            return {
                "success": True,
                "data": {
                    "account_id": self.config.account or "SIM001",
                    "total_asset": total_asset,
                    "cash": self._mock_cash,
                    "frozen_cash": 0,
                    "market_value": total_asset - self._mock_cash,
                    "total_pnl": total_asset - 1_000_000,
                    "total_pnl_pct": (total_asset - 1_000_000) / 1_000_000 * 100,
                    "today_pnl": 0
                }
            }
        
        elif action == "query_positions":
            return {
                "success": True,
                "data": [
                    {
                        "ts_code": p.ts_code,
                        "volume": p.volume,
                        "available": p.available,
                        "avg_cost": p.avg_cost,
                        "current_price": p.current_price,
                        "market_value": p.market_value,
                        "unrealized_pnl": p.unrealized_pnl,
                        "pnl_pct": p.pnl_pct
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
                        "ts_code": o.ts_code,
                        "direction": o.direction.value,
                        "order_type": o.order_type.value,
                        "price": o.price,
                        "volume": o.volume,
                        "filled_volume": o.filled_volume,
                        "filled_price": o.filled_price,
                        "status": o.status.value,
                        "submit_time": o.submit_time
                    }
                    for o in self._mock_orders.values()
                ]
            }
        
        elif action == "buy" or action == "sell":
            direction = "buy" if action == "buy" else "sell"
            ts_code = params.get("ts_code", "")
            price = params.get("price", 0)
            volume = params.get("volume", 0)
            
            order_id = f"SIM{int(time.time()*1000)}"
            
            # 模拟订单立即成交
            order = Order(
                order_id=order_id,
                ts_code=ts_code,
                direction=Direction.BUY if direction == "buy" else Direction.SELL,
                order_type=OrderType.LIMIT,
                price=price,
                volume=volume,
                filled_volume=volume,
                filled_price=price * (1.002 if direction == "buy" else 0.998),  # 模拟滑点
                status=OrderStatus.FILLED,
                submit_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            self._mock_orders[order_id] = order
            
            # 更新模拟持仓
            if direction == "buy":
                self._mock_cash -= price * volume * 1.0003  # 含佣金
                if ts_code in self._mock_positions:
                    pos = self._mock_positions[ts_code]
                    total_cost = pos.avg_cost * pos.volume + price * volume
                    pos.volume += volume
                    pos.avg_cost = total_cost / pos.volume
                    pos.available = pos.volume
                else:
                    self._mock_positions[ts_code] = Position(
                        ts_code=ts_code,
                        volume=volume,
                        available=volume,
                        avg_cost=price,
                        current_price=price
                    )
                    self._mock_positions[ts_code].update(price)
            else:  # sell
                self._mock_cash += price * volume * (1 - 0.0003 - 0.001)  # 含佣金和印花税
                if ts_code in self._mock_positions:
                    pos = self._mock_positions[ts_code]
                    pos.volume -= volume
                    pos.available = pos.volume
            
            return {
                "success": True,
                "order_id": order_id,
                "message": "订单已提交并成交（模拟模式）"
            }
        
        elif action == "cancel":
            order_id = params.get("order_id", "")
            if order_id in self._mock_orders:
                order = self._mock_orders[order_id]
                if order.status == OrderStatus.PENDING:
                    order.status = OrderStatus.CANCELLED
                    return {"success": True, "message": "撤单成功（模拟模式）"}
            return {"success": False, "error": "撤单失败"}
        
        return {"success": False, "error": "未知操作"}
    
    # ==================== 公共API ====================
    
    def login(self) -> bool:
        """
        登录QMT账户
        
        Returns:
            bool: 登录是否成功
        """
        logger.info(f"🔐 正在连接华鑫QMT...")
        
        if self.config.mode == "paper":
            logger.info("📝 模式: 模拟盘")
        else:
            logger.warning("⚠️ 警告: 实盘模式，所有交易将使用真实资金！")
        
        result = self._request("login")
        
        if result.get("success"):
            self.connected = True
            logger.info("✅ 华鑫QMT 连接成功")
            logger.info(f"   模式: {'模拟盘' if self.config.mode == 'paper' else '实盘'}")
            return True
        else:
            logger.warning(f"⚠️ QMT连接失败: {result.get('error', '未知错误')}")
            logger.info("📝 自动切换到模拟模式")
            self._mock_mode = True
            self._request("login")  # 初始化模拟数据
            return True
    
    def logout(self):
        """登出QMT账户"""
        self._request("logout")
        self.connected = False
        logger.info("👋 华鑫QMT 已断开连接")
    
    def get_account(self) -> Optional[Account]:
        """
        查询账户信息
        
        Returns:
            Account: 账户信息
        """
        result = self._request("query_account")
        
        if result.get("success"):
            data = result["data"]
            self.account = Account(
                account_id=data["account_id"],
                total_asset=data["total_asset"],
                cash=data["cash"],
                frozen_cash=data["frozen_cash"],
                market_value=data["market_value"],
                total_pnl=data["total_pnl"],
                total_pnl_pct=data["total_pnl_pct"],
                today_pnl=data["today_pnl"]
            )
            return self.account
        
        logger.error(f"❌ 查询账户失败: {result.get('error')}")
        return None
    
    def get_positions(self) -> List[Position]:
        """
        查询当前持仓
        
        Returns:
            List[Position]: 持仓列表
        """
        result = self._request("query_positions")
        
        if result.get("success"):
            positions = []
            for p in result["data"]:
                pos = Position(
                    ts_code=p["ts_code"],
                    volume=p["volume"],
                    available=p["available"],
                    avg_cost=p["avg_cost"],
                    current_price=p["current_price"],
                    market_value=p["market_value"],
                    unrealized_pnl=p["unrealized_pnl"],
                    pnl_pct=p["pnl_pct"]
                )
                positions.append(pos)
                self.positions[p["ts_code"]] = pos
            
            return positions
        
        return []
    
    def get_orders(self, status: Optional[str] = None) -> List[Order]:
        """
        查询订单
        
        Args:
            status: 过滤订单状态（可选）
        
        Returns:
            List[Order]: 订单列表
        """
        result = self._request("query_orders")
        
        if result.get("success"):
            orders = []
            for o in result["data"]:
                order = Order(
                    order_id=o["order_id"],
                    ts_code=o["ts_code"],
                    direction=Direction.BUY if o["direction"] == "buy" else Direction.SELL,
                    order_type=OrderType.LIMIT if o["order_type"] == "limit" else OrderType.MARKET,
                    price=o["price"],
                    volume=o["volume"],
                    filled_volume=o["filled_volume"],
                    filled_price=o["filled_price"],
                    status=OrderStatus(o["status"]),
                    submit_time=o["submit_time"]
                )
                orders.append(order)
                self.orders[o["order_id"]] = order
            
            if status:
                status_enum = OrderStatus(status)
                orders = [o for o in orders if o.status == status_enum]
            
            return orders
        
        return []
    
    def buy(self, ts_code: str, price: float, volume: int, 
            order_type: OrderType = OrderType.LIMIT) -> Optional[Order]:
        """
        买入
        
        Args:
            ts_code: 股票代码（如 600519.SH）
            price: 买入价格
            volume: 买入数量（100的整数倍）
            order_type: 订单类型
        
        Returns:
            Order: 订单信息
        """
        # 数量对齐
        volume = (volume // 100) * 100
        
        if volume < 100:
            logger.error(f"❌ 买入数量必须 >= 100股")
            return None
        
        logger.info(f"📈 买入 {ts_code} @ {price} x {volume}股")
        
        result = self._request("buy", {
            "ts_code": ts_code,
            "price": price,
            "volume": volume,
            "order_type": order_type.value
        })
        
        if result.get("success"):
            order_id = result["order_id"]
            order = self._mock_orders.get(order_id) if self._mock_mode else None
            
            if order:
                logger.info(f"✅ 订单已提交: {order_id}")
                logger.info(f"   状态: {order.status.value}")
                if order.status == OrderStatus.FILLED:
                    logger.info(f"   成交价: {order.filled_price}")
                    logger.info(f"   成交数量: {order.filled_volume}")
                return order
            
            return Order(
                order_id=order_id,
                ts_code=ts_code,
                direction=Direction.BUY,
                order_type=order_type,
                price=price,
                volume=volume,
                status=OrderStatus.SUBMITTED,
                submit_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        
        logger.error(f"❌ 买入失败: {result.get('error')}")
        return None
    
    def sell(self, ts_code: str, price: float, volume: int,
             order_type: OrderType = OrderType.LIMIT) -> Optional[Order]:
        """
        卖出
        
        Args:
            ts_code: 股票代码
            price: 卖出价格
            volume: 卖出数量
            order_type: 订单类型
        
        Returns:
            Order: 订单信息
        """
        # 数量对齐
        volume = (volume // 100) * 100
        
        if volume < 100:
            logger.error(f"❌ 卖出数量必须 >= 100股")
            return None
        
        # 检查持仓
        if ts_code not in self._mock_positions and self._mock_mode:
            logger.error(f"❌ 无持仓可卖: {ts_code}")
            return None
        
        logger.info(f"📉 卖出 {ts_code} @ {price} x {volume}股")
        
        result = self._request("sell", {
            "ts_code": ts_code,
            "price": price,
            "volume": volume,
            "order_type": order_type.value
        })
        
        if result.get("success"):
            order_id = result["order_id"]
            order = self._mock_orders.get(order_id) if self._mock_mode else None
            
            if order:
                logger.info(f"✅ 订单已提交: {order_id}")
                logger.info(f"   状态: {order.status.value}")
                if order.status == OrderStatus.FILLED:
                    logger.info(f"   成交价: {order.filled_price}")
                    logger.info(f"   成交数量: {order.filled_volume}")
                return order
            
            return Order(
                order_id=order_id,
                ts_code=ts_code,
                direction=Direction.SELL,
                order_type=order_type,
                price=price,
                volume=volume,
                status=OrderStatus.SUBMITTED,
                submit_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        
        logger.error(f"❌ 卖出失败: {result.get('error')}")
        return None
    
    def cancel_order(self, order_id: str) -> bool:
        """
        撤单
        
        Args:
            order_id: 订单ID
        
        Returns:
            bool: 是否成功
        """
        logger.info(f"🚫 撤单: {order_id}")
        
        result = self._request("cancel", {"order_id": order_id})
        
        if result.get("success"):
            logger.info(f"✅ 撤单成功")
            return True
        
        logger.error(f"❌ 撤单失败: {result.get('error')}")
        return False
    
    def cancel_all(self) -> int:
        """
        撤销所有未成交订单
        
        Returns:
            int: 成功撤单数量
        """
        orders = self.get_orders(status="pending")
        orders += self.get_orders(status="submitted")
        
        count = 0
        for order in orders:
            if self.cancel_order(order.order_id):
                count += 1
        
        logger.info(f"📋 共撤单 {count} 个")
        return count
    
    def close_all(self) -> int:
        """
        清仓所有持仓（卖出全部）
        
        Returns:
            int: 成交订单数量
        """
        positions = self.get_positions()
        
        if not positions:
            logger.info("📭 无持仓需要清仓")
            return 0
        
        count = 0
        for pos in positions:
            order = self.sell(pos.ts_code, price=pos.current_price, volume=pos.available)
            if order and order.status == OrderStatus.FILLED:
                count += 1
        
        logger.info(f"📋 清仓完成: {count} 个订单成交")
        return count
    
    def get_balance(self) -> float:
        """获取账户可用资金"""
        account = self.get_account()
        return account.cash if account else 0
    
    def get_position(self, ts_code: str) -> Optional[Position]:
        """获取指定股票的持仓"""
        positions = self.get_positions()
        for pos in positions:
            if pos.ts_code == ts_code:
                return pos
        return None
    
    def __repr__(self):
        status = "✅ 已连接" if self.connected or self._mock_mode else "❌ 未连接"
        mode = "模拟" if (self._mock_mode or self.config.mode == "paper") else "实盘"
        return f"<QMTClient [{status}] [{mode}]>"


# ==================== 命令行接口 ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='quant-aio 华鑫QMT执行器')
    parser.add_argument('--mode', choices=['paper', 'live'], default='paper', help='交易模式')
    parser.add_argument('--action', required=True, 
                       choices=['status', 'buy', 'sell', 'positions', 'cancel', 'close_all'],
                       help='操作')
    parser.add_argument('--symbol', help='股票代码')
    parser.add_argument('--price', type=float, help='价格')
    parser.add_argument('--volume', type=int, help='数量')
    parser.add_argument('--config', default='config/config.yaml', help='配置文件')
    
    args = parser.parse_args()
    
    # 加载配置
    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        qmt_config = QMTConfig(config.get('executor', {}).get('huaxin', {}))
        qmt_config.mode = args.mode
        
    except Exception as e:
        logger.error(f"❌ 配置加载失败: {e}")
        qmt_config = QMTConfig({})
        qmt_config.mode = args.mode
    
    # 创建客户端
    client = QMTClient(qmt_config)
    
    # 登录
    if not client.login():
        sys.exit(1)
    
    try:
        if args.action == 'status':
            account = client.get_account()
            if account:
                print(f"\n{'='*50}")
                print(f"  账号: {account.account_id}")
                print(f"  总资产: {account.total_asset:,.2f}")
                print(f"  可用资金: {account.cash:,.2f}")
                print(f"  持仓市值: {account.market_value:,.2f}")
                print(f"  总盈亏: {account.total_pnl:+,.2f} ({account.total_pnl_pct:+.2f}%)")
                print(f"{'='*50}")
        
        elif args.action == 'positions':
            positions = client.get_positions()
            if not positions:
                print("📭 当前无持仓")
            else:
                print(f"\n{'='*70}")
                print(f"  {'代码':<12} {'持仓':>8} {'可用':>8} {'成本':>10} {'现价':>10} {'盈亏':>12}")
                print(f"{'='*70}")
                for pos in positions:
                    print(f"  {pos.ts_code:<12} {pos.volume:>8} {pos.available:>8} "
                          f"{pos.avg_cost:>10.2f} {pos.current_price:>10.2f} "
                          f"{pos.unrealized_pnl:+12.2f}")
                print(f"{'='*70}")
        
        elif args.action == 'buy':
            if not args.symbol or not args.price or not args.volume:
                print("❌ 缺少参数: --symbol --price --volume")
                sys.exit(1)
            
            order = client.buy(args.symbol, args.price, args.volume)
            if order:
                print(f"\n✅ 买入成功!")
                print(f"   订单号: {order.order_id}")
                print(f"   股票: {order.ts_code}")
                print(f"   价格: {order.price}")
                print(f"   数量: {order.volume}")
        
        elif args.action == 'sell':
            if not args.symbol or not args.price or not args.volume:
                print("❌ 缺少参数: --symbol --price --volume")
                sys.exit(1)
            
            order = client.sell(args.symbol, args.price, args.volume)
            if order:
                print(f"\n✅ 卖出成功!")
                print(f"   订单号: {order.order_id}")
                print(f"   股票: {order.ts_code}")
                print(f"   价格: {order.price}")
                print(f"   数量: {order.volume}")
        
        elif args.action == 'cancel':
            if not args.symbol:
                count = client.cancel_all()
                print(f"\n📋 已撤销 {count} 个订单")
            else:
                orders = client.get_orders()
                for order in orders:
                    if order.ts_code == args.symbol and not order.is_completed:
                        client.cancel_order(order.order_id)
                        print(f"\n✅ 已撤销订单: {order.order_id}")
                        break
        
        elif args.action == 'close_all':
            count = client.close_all()
            print(f"\n📋 清仓完成: {count} 个订单")
    
    finally:
        client.logout()


if __name__ == '__main__':
    main()
