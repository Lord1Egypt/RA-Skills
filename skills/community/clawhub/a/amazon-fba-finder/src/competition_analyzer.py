"""
竞争分析模块
分析市场竞争程度、竞品优劣势、进入壁垒
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class CompetitionLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class CompetitorAnalysis:
    """竞品分析数据"""
    asin: str
    title: str
    price: float
    rating: float
    review_count: int
    estimated_monthly_sales: int
    listing_quality_score: float
    keyword_rankings: Dict[str, int]
    strengths: List[str]
    weaknesses: List[str]


@dataclass
class MarketAnalysis:
    """市场分析结果"""
    category: str
    total_competitors: int
    top_10_avg_reviews: int
    top_10_avg_rating: float
    price_range: tuple
    competition_level: CompetitionLevel
    entry_barrier: str  # low/medium/high
    differentiation_opportunities: List[str]
    recommended_strategy: str


class CompetitionAnalyzer:
    """竞争分析引擎"""
    
    def __init__(self):
        self.competitors = []
    
    def analyze_market(self, 
                      products: List[Dict],
                      category: str) -> MarketAnalysis:
        """
        分析市场竞争情况
        
        Args:
            products: 竞品列表
            category: 类目名称
            
        Returns:
            市场分析结果
        """
        if not products:
            return self._empty_analysis(category)
        
        # 计算关键指标
        total_competitors = len(products)
        top_10 = sorted(products, key=lambda x: x.get('review_count', 0), reverse=True)[:10]
        
        avg_reviews = sum(p.get('review_count', 0) for p in top_10) / len(top_10) if top_10 else 0
        avg_rating = sum(p.get('rating', 0) for p in top_10) / len(top_10) if top_10 else 0
        
        prices = [p.get('price', 0) for p in products if p.get('price')]
        price_range = (min(prices), max(prices)) if prices else (0, 0)
        
        # 评估竞争程度
        competition_level = self._evaluate_competition(avg_reviews, total_competitors, avg_rating)
        
        # 评估进入壁垒
        entry_barrier = self._evaluate_barrier(competition_level, avg_reviews)
        
        # 识别差异化机会
        opportunities = self._identify_opportunities(products)
        
        # 推荐策略
        strategy = self._recommend_strategy(competition_level, opportunities)
        
        return MarketAnalysis(
            category=category,
            total_competitors=total_competitors,
            top_10_avg_reviews=int(avg_reviews),
            top_10_avg_rating=round(avg_rating, 2),
            price_range=price_range,
            competition_level=competition_level,
            entry_barrier=entry_barrier,
            differentiation_opportunities=opportunities,
            recommended_strategy=strategy
        )
    
    def _evaluate_competition(self, 
                             avg_reviews: float,
                             total_competitors: int,
                             avg_rating: float) -> CompetitionLevel:
        """评估竞争程度"""
        if avg_reviews < 100 and total_competitors < 50:
            return CompetitionLevel.LOW
        elif avg_reviews < 500 and total_competitors < 200:
            return CompetitionLevel.MEDIUM
        elif avg_reviews < 2000:
            return CompetitionLevel.HIGH
        else:
            return CompetitionLevel.VERY_HIGH
    
    def _evaluate_barrier(self, 
                         competition: CompetitionLevel,
                         avg_reviews: float) -> str:
        """评估进入壁垒"""
        if competition == CompetitionLevel.LOW:
            return "low"
        elif competition == CompetitionLevel.MEDIUM:
            return "medium"
        elif avg_reviews > 1000:
            return "high"
        else:
            return "medium"
    
    def _identify_opportunities(self, products: List[Dict]) -> List[str]:
        """识别差异化机会"""
        opportunities = []
        
        # 分析评论找出痛点
        common_complaints = self._extract_common_complaints(products)
        
        if "quality" in common_complaints:
            opportunities.append("提升产品质量")
        if "shipping" in common_complaints:
            opportunities.append("优化物流体验")
        if "instructions" in common_complaints:
            opportunities.append("改进使用说明")
        if "durability" in common_complaints:
            opportunities.append("增强产品耐用性")
        
        # 价格机会
        prices = [p.get('price', 0) for p in products if p.get('price')]
        if prices:
            avg_price = sum(prices) / len(prices)
            if avg_price > 50:
                opportunities.append("提供性价比更高的选择")
        
        if not opportunities:
            opportunities.append("通过 bundling 增加价值")
        
        return opportunities
    
    def _extract_common_complaints(self, products: List[Dict]) -> List[str]:
        """从评论中提取常见投诉"""
        # 实际实现需要分析评论文本
        # 这里提供框架
        return ["quality", "durability"]
    
    def _recommend_strategy(self, 
                           competition: CompetitionLevel,
                           opportunities: List[str]) -> str:
        """推荐进入策略"""
        if competition == CompetitionLevel.LOW:
            return "快速进入，建立品牌认知"
        elif competition == CompetitionLevel.MEDIUM:
            return f"差异化定位：{', '.join(opportunities[:2])}"
        elif competition == CompetitionLevel.HIGH:
            return "寻找细分市场，避免正面竞争"
        else:
            return "建议寻找其他类目，竞争过于激烈"
    
    def _empty_analysis(self, category: str) -> MarketAnalysis:
        """返回空分析结果"""
        return MarketAnalysis(
            category=category,
            total_competitors=0,
            top_10_avg_reviews=0,
            top_10_avg_rating=0,
            price_range=(0, 0),
            competition_level=CompetitionLevel.LOW,
            entry_barrier="unknown",
            differentiation_opportunities=[],
            recommended_strategy="数据不足，无法推荐"
        )
    
    def calculate_market_share(self, 
                              your_estimated_sales: int,
                              total_market_sales: int) -> float:
        """计算预期市场份额"""
        if total_market_sales == 0:
            return 0
        return (your_estimated_sales / total_market_sales) * 100
