"""
Amazon FBA Finder - 主入口
高利润产品发现与分析工具
"""

import asyncio
from typing import Dict, List, Optional
from dataclasses import asdict

from .product_finder import ProductFinder, ProductOpportunity
from .competition_analyzer import CompetitionAnalyzer, MarketAnalysis
from .supplier_recommender import SupplierRecommender, SupplierRecommendation
from .profit_calculator import ProfitCalculator, ProductDimensions, ProfitAnalysis


class AmazonFBAFinder:
    """
    Amazon FBA 产品发现与分析引擎
    
    功能:
    - 高利润产品发现
    - 市场竞争分析
    - 供应商推荐
    - 利润计算
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.product_finder = ProductFinder(
            api_key=self.config.get('amazon_api_key')
        )
        self.competition_analyzer = CompetitionAnalyzer()
        self.supplier_recommender = SupplierRecommender(
            api_key=self.config.get('alibaba_api_key')
        )
        self.profit_calculator = ProfitCalculator(
            marketplace=self.config.get('marketplace', 'US')
        )
    
    async def find_opportunities(self,
                                category: str,
                                min_price: float = 20,
                                max_price: float = 100,
                                min_margin: float = 0.25,
                                limit: int = 20) -> List[Dict]:
        """
        发现高利润产品机会
        
        Args:
            category: 产品类目
            min_price: 最低售价
            max_price: 最高售价
            min_margin: 最低利润率
            limit: 返回数量
            
        Returns:
            产品机会列表
        """
        async with self.product_finder:
            products = await self.product_finder.search_products(
                category=category,
                min_price=min_price,
                max_price=max_price,
                min_margin=min_margin,
                limit=limit
            )
            
            # 筛选优胜者
            winners = self.product_finder.filter_winners(products, min_score=70)
            
            return [asdict(p) for p in winners]
    
    def analyze_competition(self,
                           category: str,
                           products: List[Dict]) -> Dict:
        """
        分析市场竞争情况
        
        Args:
            category: 类目名称
            products: 竞品数据列表
            
        Returns:
            市场分析结果
        """
        analysis = self.competition_analyzer.analyze_market(
            products=products,
            category=category
        )
        return asdict(analysis)
    
    def find_suppliers(self,
                      product_keyword: str,
                      target_price: float,
                      min_order: int = 100) -> Dict:
        """
        寻找合适供应商
        
        Args:
            product_keyword: 产品关键词
            target_price: 目标采购价
            min_order: 最小起订量
            
        Returns:
            供应商推荐结果
        """
        recommendation = self.supplier_recommender.find_suppliers(
            product_keyword=product_keyword,
            target_price=target_price,
            min_order=min_order
        )
        return asdict(recommendation)
    
    def calculate_profit(self,
                        selling_price: float,
                        product_cost: float,
                        length: float,
                        width: float,
                        height: float,
                        weight: float,
                        shipping_cost: float = 0,
                        monthly_sales: int = 300) -> Dict:
        """
        计算产品利润
        
        Args:
            selling_price: 售价 ($)
            product_cost: 产品成本 ($)
            length: 长度 (英寸)
            width: 宽度 (英寸)
            height: 高度 (英寸)
            weight: 重量 (磅)
            shipping_cost: 头程运费 ($)
            monthly_sales: 月销量
            
        Returns:
            利润分析结果
        """
        dimensions = ProductDimensions(
            length=length,
            width=width,
            height=height,
            weight=weight
        )
        
        analysis = self.profit_calculator.calculate_profit(
            selling_price=selling_price,
            product_cost=product_cost,
            dimensions=dimensions,
            shipping_cost=shipping_cost,
            monthly_sales=monthly_sales
        )
        
        return asdict(analysis)
    
    async def full_analysis(self,
                           category: str,
                           product_keyword: str,
                           target_price: float) -> Dict:
        """
        完整产品分析（一站式）
        
        Args:
            category: 类目
            product_keyword: 产品关键词
            target_price: 目标售价
            
        Returns:
            完整分析报告
        """
        # 1. 发现产品机会
        opportunities = await self.find_opportunities(
            category=category,
            min_price=target_price * 0.8,
            max_price=target_price * 1.2,
            limit=10
        )
        
        # 2. 竞争分析
        competition = self.analyze_competition(
            category=category,
            products=opportunities
        )
        
        # 3. 供应商推荐
        suppliers = self.find_suppliers(
            product_keyword=product_keyword,
            target_price=target_price * 0.25  # 目标采购价为售价的 25%
        )
        
        # 4. 利润计算（示例）
        if opportunities:
            sample_product = opportunities[0]
            profit = self.calculate_profit(
                selling_price=sample_product.get('price', target_price),
                product_cost=suppliers.get('avg_unit_cost', target_price * 0.25),
                length=10,
                width=8,
                height=6,
                weight=2,
                monthly_sales=sample_product.get('estimated_sales', 300)
            )
        else:
            profit = None
        
        return {
            "category": category,
            "product_keyword": product_keyword,
            "opportunities": opportunities,
            "competition_analysis": competition,
            "supplier_recommendations": suppliers,
            "profit_analysis": profit,
            "overall_recommendation": self._generate_overall_recommendation(
                opportunities, competition, suppliers, profit
            )
        }
    
    def _generate_overall_recommendation(self,
                                        opportunities: List,
                                        competition: Dict,
                                        suppliers: Dict,
                                        profit: Optional[Dict]) -> Dict:
        """生成综合推荐建议"""
        score = 0
        factors = []
        
        # 机会评分
        if opportunities:
            avg_score = sum(o.get('opportunity_score', 0) for o in opportunities) / len(opportunities)
            if avg_score >= 70:
                score += 30
                factors.append("✅ 高潜力产品机会")
            elif avg_score >= 50:
                score += 15
                factors.append("⚠️ 中等潜力")
        
        # 竞争评分
        comp_level = competition.get('competition_level', 'medium')
        if comp_level == 'low':
            score += 25
            factors.append("✅ 竞争程度低")
        elif comp_level == 'medium':
            score += 15
            factors.append("⚠️ 竞争中等")
        
        # 供应商评分
        if suppliers.get('recommended_suppliers'):
            score += 20
            factors.append("✅ 有合适供应商")
        
        # 利润评分
        if profit and profit.get('profit_margin', 0) >= 25:
            score += 25
            factors.append("✅ 利润率优秀")
        elif profit and profit.get('profit_margin', 0) >= 15:
            score += 12
            factors.append("⚠️ 利润率一般")
        
        # 总体建议
        if score >= 70:
            recommendation = "强烈推荐进入"
            confidence = "high"
        elif score >= 50:
            recommendation = "可以考虑，需进一步优化"
            confidence = "medium"
        else:
            recommendation = "建议寻找其他机会"
            confidence = "low"
        
        return {
            "score": score,
            "recommendation": recommendation,
            "confidence": confidence,
            "key_factors": factors
        }


# CLI 入口
async def main():
    """命令行入口"""
    import json
    
    finder = AmazonFBAFinder()
    
    # 示例：完整分析
    result = await finder.full_analysis(
        category="Home & Kitchen",
        product_keyword="bamboo cutting board",
        target_price=35.99
    )
    
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
