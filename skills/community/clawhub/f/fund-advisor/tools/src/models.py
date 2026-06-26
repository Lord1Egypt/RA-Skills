"""
基金持仓管理系统 - 数据模型定义
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class FundType(Enum):
    """基金类型枚举，为未来扩展场内基金预留"""
    PUBLIC_FUND = "public"  # 公募基金
    ETF = "etf"  # 场内基金-ETF
    LOF = "lof"  # 场内基金-LOF
    CLOSED_END = "closed_end"  # 封闭式基金


class GroupColumn(Enum):
    """分组统计列名"""
    FUND_CODE = "fund_code"           # 基金代码
    FUND_NAME = "fund_name"           # 基金名称
    FUND_MANAGER = "fund_manager"     # 基金管理人
    FUND_ACCOUNT = "fund_account"     # 基金账户
    TRADE_ACCOUNT = "trade_account"   # 交易账户
    SALES_AGENCY = "sales_agency"     # 销售机构
    INVEST_TYPE = "invest_type"       # 投资类型
    CURRENCY = "currency"             # 结算币种
    DIVIDEND_METHOD = "dividend_method"  # 分红方式

    @classmethod
    def get_display_name(cls, column: 'GroupColumn') -> str:
        """获取列的中文显示名称"""
        names = {
            cls.FUND_CODE: "基金代码",
            cls.FUND_NAME: "基金名称",
            cls.FUND_MANAGER: "基金管理人",
            cls.FUND_ACCOUNT: "基金账户",
            cls.TRADE_ACCOUNT: "交易账户",
            cls.SALES_AGENCY: "销售机构",
            cls.INVEST_TYPE: "投资类型",
            cls.CURRENCY: "结算币种",
            cls.DIVIDEND_METHOD: "分红方式",
        }
        return names.get(column, column.value)


@dataclass
class FundHolding:
    """公募基金持有信息"""
    fund_code: str
    fund_name: str
    share_class: str
    fund_manager: str
    fund_account: str
    sales_agency: str
    trade_account: str
    holding_shares: float
    share_date: date
    nav: float
    nav_date: date
    asset_value: float
    settlement_currency: str
    dividend_method: str
    fund_type: FundType = FundType.PUBLIC_FUND
    id: Optional[int] = None

    @property
    def primary_key(self) -> tuple:
        """返回联合主键"""
        return (self.fund_account, self.trade_account, self.fund_code)


@dataclass
class FundInfo:
    """基金基础信息"""
    fund_code: str
    fund_name: str
    fund_invest_type: Optional[str] = None
    risk_5_level: Optional[int] = None
    nav: Optional[float] = None
    nav_date: Optional[date] = None
    net_asset: Optional[float] = None
    setup_date: Optional[date] = None
    yearly_roe: Optional[float] = None  # 七日年化收益率（货币基金）
    one_year_return: Optional[float] = None
    setup_day_return: Optional[float] = None
    manager_names: Optional[str] = None
    stock_ratio: Optional[float] = None
    bond_ratio: Optional[float] = None
    cash_ratio: Optional[float] = None
    data_update_time: Optional[datetime] = None

    def is_money_market_fund(self) -> bool:
        """判断是否为货币基金"""
        return self.fund_invest_type == "货币型"


@dataclass
class StockHolding:
    """股票持仓明细"""
    stock_code: str
    stock_name: str
    holding_ratio: float
    holding_amount: Optional[float] = None


@dataclass
class BondHolding:
    """债券持仓明细"""
    bond_code: str
    bond_name: str
    holding_ratio: float
    holding_amount: Optional[float] = None


@dataclass
class FundHoldingsDetail:
    """基金持仓详情"""
    fund_code: str
    report_date: Optional[date] = None
    stock_invest_ratio: Optional[float] = None
    bond_invest_ratio: Optional[float] = None
    top_stocks: List[StockHolding] = field(default_factory=list)
    top_bonds: List[BondHolding] = field(default_factory=list)
    data_update_time: Optional[datetime] = None
