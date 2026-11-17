from dataclasses import dataclass


@dataclass
class Trade:
    side: str
    symbol: str
    qty: float
    amount: float
    currency: str
    date: str
    source: str
    price: float | None = None
    fees: float | None = None
    account: str | None = None


@dataclass
class Gap:
    kind: str
    trade: Trade
    message: str


@dataclass
class MatchedSale:
    sale: Trade
    buy: Trade
    qty: float
    proceeds: float
    cost: float
    gain: float
    year: int | None = None


@dataclass
class UnmatchedSale:
    sale: Trade
    qty: float
    proceeds: float
    estimated_cost: float | None = None


@dataclass
class IncomeItem:
    kind: str
    amount: float
    year: int


@dataclass
class OffsetResult:
    transfer_net: float
    dividend_net: float
    interest_net: float = 0
    dividend_tax: float = 0
    transfer_tax: float = 0
