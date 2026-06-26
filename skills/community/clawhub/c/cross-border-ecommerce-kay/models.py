# 数据模型定义
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class KeywordAnalysis:
    """关键词分析结果"""
    keyword: str
    search_volume: int          # 月搜索量
    competition: float          # 竞争度 0-1
    trend: str                   # 趋势: rising/falling/stable
    related_keywords: List[str]  # 相关关键词
    suggested_bid: float         # 建议竞价


@dataclass
class CompetitorProduct:
    """竞品信息"""
    platform: str                # amazon/ebay
    title: str
    price: float
    currency: str
    rating: float                # 评分 0-5
    reviews_count: int           # 评论数
    sales_rank: int              # 销量排名
    asin: Optional[str] = None   # 亚马逊ASIN
    url: Optional[str] = None


@dataclass
class ProfitCalculation:
    """利润计算结果"""
    product_cost: float          # 产品成本
    shipping_cost: float         # 运费
    platform_fee: float          # 平台费
    referral_fee: float          # 佣金
    other_cost: float            # 其他成本
    selling_price: float         # 售价
    total_cost: float            # 总成本
    profit: float                # 利润
    profit_margin: float         # 利润率


@dataclass
class AIListing:
    """AI生成的Listing"""
    title: str
    short_description: str       # 短描述(5点描述)
    full_description: str        # 完整描述
    keywords: List[str]         # 关键词标签
    suggested_price: float      # 建议价格
