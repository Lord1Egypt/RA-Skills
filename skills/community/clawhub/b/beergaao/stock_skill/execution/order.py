"""执行层 - 订单管理 + 券商接口抽象 + 成交确认 + T+1 约束"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIAL = "partial"
    FILLED = "filled"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class TradingSession(str, Enum):
    PRE_OPEN = "pre_open"       # 9:15 - 9:25
    CONTINUOUS = "continuous"   # 9:30 - 11:30, 13:00 - 14:57
    CLOSING = "closing"         # 14:57 - 15:00
    CLOSED = "closed"


@dataclass
class OrderRequest:
    """订单请求"""
    code: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    price: float = 0.0
    strategy_name: str = ""
    reason: str = ""


@dataclass
class OrderResponse:
    """订单响应"""
    order_id: str
    code: str
    side: OrderSide
    status: OrderStatus
    request_quantity: int
    filled_quantity: int = 0
    filled_price: float = 0.0
    commission: float = 0.0
    timestamp: str = ""
    message: str = ""


@dataclass
class TradeRecord:
    """成交记录"""
    order_id: str
    code: str
    side: OrderSide
    price: float
    quantity: int
    commission: float
    timestamp: str


# ===================== T+1 管理 =====================

class T1Manager:
    """T+1 交易规则管理"""

    def __init__(self):
        self._buy_dates: Dict[str, str] = {}  # code -> buy_date

    def record_buy(self, code: str, trade_date: str):
        self._buy_dates[code] = trade_date

    def can_sell(self, code: str, current_date: str) -> bool:
        buy_date = self._buy_dates.get(code)
        if not buy_date:
            return True
        return current_date > buy_date

    def clear(self, code: str):
        self._buy_dates.pop(code, None)


# ===================== 交易时段管理 =====================

class SessionManager:
    """A 股交易时段管理"""

    @staticmethod
    def get_session(current_time: datetime | None = None) -> TradingSession:
        if current_time is None:
            current_time = datetime.now()

        t = current_time.hour * 60 + current_time.minute

        if 9 * 60 + 15 <= t < 9 * 60 + 25:
            return TradingSession.PRE_OPEN
        elif (9 * 60 + 30 <= t < 11 * 60 + 30) or (13 * 60 <= t < 14 * 60 + 57):
            return TradingSession.CONTINUOUS
        elif 14 * 60 + 57 <= t < 15 * 60:
            return TradingSession.CLOSING
        else:
            return TradingSession.CLOSED

    @staticmethod
    def can_trade(current_time: datetime | None = None) -> bool:
        session = SessionManager.get_session(current_time)
        return session in (TradingSession.CONTINUOUS, TradingSession.CLOSING)

    @staticmethod
    def is_closing_auction(current_time: datetime | None = None) -> bool:
        return SessionManager.get_session(current_time) == TradingSession.CLOSING


# ===================== 限仓检查 =====================

class PositionLimitChecker:
    """仓位限制检查"""

    def __init__(
        self,
        max_single: float = 0.30,
        max_total: float = 0.80,
        max_shares_per_order: int = 100000,
    ):
        self.max_single = max_single
        self.max_total = max_total
        self.max_shares = max_shares_per_order

    def check(
        self,
        order: OrderRequest,
        current_positions: Dict[str, float],
        total_value: float,
        cash: float,
    ) -> Tuple[bool, str]:
        """检查订单是否符合仓位限制"""

        # 单笔最大股数
        if order.quantity > self.max_shares:
            return False, f"单笔委托 {order.quantity} 超过上限 {self.max_shares}"

        if order.side == OrderSide.BUY:
            order_value = order.quantity * order.price

            # 资金检查
            if order_value > cash:
                return False, f"资金不足: 需要 {order_value:.0f}，可用 {cash:.0f}"

            # 单只仓位检查
            existing = current_positions.get(order.code, 0)
            new_position = (existing + order_value) / total_value if total_value > 0 else 0
            if new_position > self.max_single:
                return False, f"单只仓位 {new_position:.0%} 超过 {self.max_single:.0%}"

            # 总仓位检查
            total_position = sum(current_positions.values()) + order_value
            total_ratio = total_position / total_value if total_value > 0 else 0
            if total_ratio > self.max_total:
                return False, f"总仓位 {total_ratio:.0%} 超过 {self.max_total:.0%}"

        return True, "OK"


# ===================== 券商接口抽象 =====================

class BrokerInterface(ABC):
    """券商接口抽象基类"""

    @abstractmethod
    def submit_order(self, order: OrderRequest) -> OrderResponse:
        """提交订单"""
        ...

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """撤单"""
        ...

    @abstractmethod
    def query_orders(self) -> List[OrderResponse]:
        """查询当日委托"""
        ...

    @abstractmethod
    def query_positions(self) -> Dict[str, Dict]:
        """查询持仓"""
        ...

    @abstractmethod
    def query_balance(self) -> Dict[str, float]:
        """查询资金"""
        ...


class SimulatedBroker(BrokerInterface):
    """模拟券商（Paper Trading）"""

    def __init__(self, initial_capital: float = 1_000_000):
        self.cash = initial_capital
        self.positions: Dict[str, Dict] = {}
        self.orders: List[OrderResponse] = []
        self.trades: List[TradeRecord] = []
        self._order_counter = 0
        self._t1 = T1Manager()

    def submit_order(self, order: OrderRequest) -> OrderResponse:
        self._order_counter += 1
        order_id = f"SIM_{self._order_counter:06d}"
        now = datetime.now().isoformat()

        if order.side == OrderSide.BUY:
            cost = order.quantity * order.price
            if cost > self.cash:
                resp = OrderResponse(
                    order_id=order_id, code=order.code,
                    side=order.side, status=OrderStatus.REJECTED,
                    request_quantity=order.quantity,
                    timestamp=now, message="资金不足",
                )
                self.orders.append(resp)
                return resp

            commission = max(cost * 0.0003, 5)
            self.cash -= cost + commission

            pos = self.positions.get(order.code, {"shares": 0, "avg_cost": 0})
            total_shares = pos["shares"] + order.quantity
            pos["avg_cost"] = (pos["avg_cost"] * pos["shares"] + order.price * order.quantity) / total_shares
            pos["shares"] = total_shares
            self.positions[order.code] = pos

            self._t1.record_buy(order.code, date.today().isoformat())

            resp = OrderResponse(
                order_id=order_id, code=order.code,
                side=order.side, status=OrderStatus.FILLED,
                request_quantity=order.quantity,
                filled_quantity=order.quantity,
                filled_price=order.price,
                commission=commission,
                timestamp=now, message="成交",
            )

        else:  # SELL
            pos = self.positions.get(order.code)
            if not pos or pos["shares"] < order.quantity:
                resp = OrderResponse(
                    order_id=order_id, code=order.code,
                    side=order.side, status=OrderStatus.REJECTED,
                    request_quantity=order.quantity,
                    timestamp=now, message="持仓不足",
                )
                self.orders.append(resp)
                return resp

            if not self._t1.can_sell(order.code, date.today().isoformat()):
                resp = OrderResponse(
                    order_id=order_id, code=order.code,
                    side=order.side, status=OrderStatus.REJECTED,
                    request_quantity=order.quantity,
                    timestamp=now, message="T+1限制，今日买入不可卖出",
                )
                self.orders.append(resp)
                return resp

            proceeds = order.quantity * order.price
            commission = max(proceeds * 0.0003, 5)
            tax = proceeds * 0.001
            self.cash += proceeds - commission - tax

            pos["shares"] -= order.quantity
            if pos["shares"] <= 0:
                del self.positions[order.code]
                self._t1.clear(order.code)

            resp = OrderResponse(
                order_id=order_id, code=order.code,
                side=order.side, status=OrderStatus.FILLED,
                request_quantity=order.quantity,
                filled_quantity=order.quantity,
                filled_price=order.price,
                commission=commission + tax,
                timestamp=now, message="成交",
            )

        self.orders.append(resp)
        self.trades.append(TradeRecord(
            order_id=order_id, code=order.code,
            side=order.side, price=order.price,
            quantity=order.quantity,
            commission=resp.commission,
            timestamp=now,
        ))
        return resp

    def cancel_order(self, order_id: str) -> bool:
        for o in self.orders:
            if o.order_id == order_id and o.status == OrderStatus.PENDING:
                o.status = OrderStatus.CANCELLED
                return True
        return False

    def query_orders(self) -> List[OrderResponse]:
        return self.orders

    def query_positions(self) -> Dict[str, Dict]:
        return self.positions

    def query_balance(self) -> Dict[str, float]:
        return {"cash": self.cash, "total": self.cash + sum(
            p["shares"] * p["avg_cost"] for p in self.positions.values()
        )}


# ===================== 订单管理器 =====================

class OrderManager:
    """订单管理器"""

    def __init__(
        self,
        broker: BrokerInterface,
        position_checker: PositionLimitChecker | None = None,
        on_fill: Callable[[OrderResponse], None] | None = None,
    ):
        self.broker = broker
        self.checker = position_checker or PositionLimitChecker()
        self._on_fill = on_fill

    def submit(
        self,
        code: str,
        side: OrderSide,
        quantity: int,
        price: float,
        order_type: OrderType = OrderType.MARKET,
        strategy_name: str = "",
    ) -> OrderResponse:
        """提交订单（含风控检查）"""
        order = OrderRequest(
            code=code, side=side, order_type=order_type,
            quantity=quantity, price=price,
            strategy_name=strategy_name,
        )

        balance = self.broker.query_balance()
        positions = self.broker.query_positions()
        pos_values = {k: v["shares"] * v["avg_cost"] for k, v in positions.items()}

        ok, msg = self.checker.check(order, pos_values, balance["total"], balance["cash"])
        if not ok:
            return OrderResponse(
                order_id="", code=code, side=side,
                status=OrderStatus.REJECTED,
                request_quantity=quantity, message=msg,
            )

        resp = self.broker.submit_order(order)

        if resp.status == OrderStatus.FILLED and self._on_fill:
            self._on_fill(resp)

        return resp

    def get_today_trades(self) -> List[TradeRecord]:
        if isinstance(self.broker, SimulatedBroker):
            return self.broker.trades
        return []
