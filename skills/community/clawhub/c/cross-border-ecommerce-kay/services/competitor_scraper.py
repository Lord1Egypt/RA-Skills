# 竞品分析爬虫服务
import random
from typing import List
from models import CompetitorProduct


class CompetitorScraper:
    """竞品分析服务(使用模拟数据)"""
    
    def __init__(self):
        self.platforms = ["amazon", "ebay"]
    
    def scrape_competitors(self, keyword: str, platform: str = "amazon", limit: int = 10) -> List[CompetitorProduct]:
        """抓取竞品数据"""
        if platform not in self.platforms:
            platform = "amazon"
        
        return self._generate_mock_competitors(keyword, platform, limit)
    
    def _generate_mock_competitors(self, keyword: str, platform: str, limit: int) -> List[CompetitorProduct]:
        """生成模拟竞品数据"""
        competitors = []
        
        price_ranges = {
            "amazon": (15.99, 89.99),
            "ebay": (12.99, 79.99)
        }
        
        min_price, max_price = price_ranges.get(platform, (15, 90))
        
        for i in range(min(limit, 10)):
            price = round(random.uniform(min_price, max_price), 2)
            competitors.append(CompetitorProduct(
                platform=platform,
                title=f"{keyword.title()} - Premium Quality Model {i+1}",
                price=price,
                currency="USD",
                rating=round(random.uniform(3.5, 5.0), 1),
                reviews_count=random.randint(50, 5000),
                sales_rank=random.randint(1, 10000),
                asin=f"ASIN{random.randint(10000000, 99999999)}" if platform == "amazon" else None,
                url=f"https://www.{platform}.com/dp/product/{random.randint(100000, 999999)}"
            ))
        
        # 按评分排序
        competitors.sort(key=lambda x: x.rating, reverse=True)
        return competitors
    
    def analyze_market(self, keyword: str, platform: str = "amazon") -> dict:
        """分析市场概况"""
        competitors = self.scrape_competitors(keyword, platform, 20)
        
        if not competitors:
            return {}
        
        prices = [c.price for c in competitors]
        ratings = [c.rating for c in competitors]
        reviews = [c.reviews_count for c in competitors]
        
        return {
            "avg_price": round(sum(prices) / len(prices), 2),
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_rating": round(sum(ratings) / len(ratings), 1),
            "avg_reviews": int(sum(reviews) / len(reviews)),
            "total_competitors": len(competitors),
            "top_competitors": competitors[:5]
        }
