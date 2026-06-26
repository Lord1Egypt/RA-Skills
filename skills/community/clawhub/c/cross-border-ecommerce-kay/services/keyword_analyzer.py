# 关键词分析服务
import random
from models import KeywordAnalysis


class KeywordAnalyzer:
    """关键词分析服务(使用模拟数据)"""
    
    def __init__(self):
        self.mock_db = self._init_mock_data()
    
    def _init_mock_data(self):
        """初始化模拟数据"""
        return {
            "wireless earbuds": {
                "search_volume": 125000,
                "competition": 0.85,
                "trend": "rising",
                "related": ["bluetooth earbuds", "noise cancelling earbuds", "sports earbuds"],
                "suggested_bid": 2.50
            },
            "phone case": {
                "search_volume": 89000,
                "competition": 0.72,
                "trend": "stable",
                "related": ["iphone case", "samsung case", "waterproof phone case"],
                "suggested_bid": 1.20
            },
            "laptop stand": {
                "search_volume": 45000,
                "competition": 0.55,
                "trend": "rising",
                "related": ["adjustable laptop stand", "macbook stand", "aluminum laptop stand"],
                "suggested_bid": 1.80
            },
            "yoga mat": {
                "search_volume": 67000,
                "competition": 0.68,
                "trend": "stable",
                "related": ["exercise mat", "pilates mat", "non slip yoga mat"],
                "suggested_bid": 1.50
            },
            "smart watch": {
                "search_volume": 156000,
                "competition": 0.91,
                "trend": "rising",
                "related": ["fitness tracker", "apple watch", "samsung watch"],
                "suggested_bid": 3.20
            }
        }
    
    def analyze(self, keyword: str) -> KeywordAnalysis:
        """分析关键词"""
        keyword_lower = keyword.lower().strip()
        
        # 如果有精确匹配，使用精确数据
        if keyword_lower in self.mock_db:
            data = self.mock_db[keyword_lower]
        else:
            # 否则生成模拟数据
            data = self._generate_mock_data(keyword_lower)
        
        return KeywordAnalysis(
            keyword=keyword,
            search_volume=data["search_volume"],
            competition=data["competition"],
            trend=data["trend"],
            related_keywords=data["related"],
            suggested_bid=data["suggested_bid"]
        )
    
    def _generate_mock_data(self, keyword: str) -> dict:
        """为未知关键词生成模拟数据"""
        base_volume = random.randint(10000, 150000)
        return {
            "search_volume": base_volume,
            "competition": round(random.uniform(0.3, 0.95), 2),
            "trend": random.choice(["rising", "stable", "stable", "falling"]),
            "related": [
                f"best {keyword}",
                f"{keyword} for beginners",
                f"premium {keyword}",
                f"cheap {keyword}"
            ],
            "suggested_bid": round(random.uniform(0.5, 4.0), 2)
        }
    
    def batch_analyze(self, keywords: list) -> list:
        """批量分析关键词"""
        return [self.analyze(kw) for kw in keywords]
