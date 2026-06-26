# AI Listing生成服务
import os
import json
import random
from typing import List, Optional
from models import AIListing


class AIListingGenerator:
    """AI Listing生成器"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.use_mock = not bool(self.api_key)
    
    def generate(
        self,
        product_name: str,
        keyword_analysis: dict = None,
        competitor_data: dict = None,
        target_market: str = "US"
    ) -> AIListing:
        """
        生成AI Listing
        
        Args:
            product_name: 产品名称
            keyword_analysis: 关键词分析数据
            competitor_data: 竞品分析数据
            target_market: 目标市场
        """
        if self.use_mock:
            return self._generate_mock(product_name, keyword_analysis, competitor_data, target_market)
        
        return self._call_openai(product_name, keyword_analysis, competitor_data, target_market)
    
    def _generate_mock(
        self,
        product_name: str,
        keyword_analysis: dict = None,
        competitor_data: dict = None,
        target_market: str = "US"
    ) -> AIListing:
        """生成模拟Listing(无API Key时使用)"""
        # 生成标题
        title = self._mock_title(product_name, keyword_analysis)
        
        # 生成5点描述
        short_desc = self._mock_short_description(product_name)
        
        # 生成完整描述
        full_desc = self._mock_full_description(product_name)
        
        # 生成关键词
        keywords = self._mock_keywords(product_name, keyword_analysis)
        
        # 建议价格
        suggested_price = self._mock_suggested_price(product_name, competitor_data)
        
        return AIListing(
            title=title,
            short_description=short_desc,
            full_description=full_desc,
            keywords=keywords,
            suggested_price=suggested_price
        )
    
    def _mock_title(self, product_name: str, keyword_analysis: dict = None) -> str:
        """生成模拟标题"""
        templates = [
            f"Premium {product_name} - High Quality, Durable & Portable Design",
            f"{product_name} - Professional Grade with Advanced Features",
            f"Upgraded {product_name} - Best Seller, 100% Satisfaction Guaranteed",
            f"{product_name} | Ergonomic Design | Perfect for Home & Office",
            f"Top Rated {product_name} - Compact, Lightweight & Easy to Use"
        ]
        return random.choice(templates)
    
    def _mock_short_description(self, product_name: str) -> str:
        """生成5点描述"""
        features = [
            "✓ PREMIUM QUALITY: Made from high-grade materials for durability and long-lasting performance",
            "✓ ERGONOMIC DESIGN: Designed for comfort with non-slip grip, perfect for extended use",
            "✓ MULTI-FUNCTIONAL: Versatile features meet all your daily needs, great value for money",
            "✓ PERFECT GIFT: Ideal birthday, holiday, or special occasion gift for friends and family",
            "✓ 100% SATISFACTION: Backed by our hassle-free 30-day money-back guarantee"
        ]
        return "\n".join(features)
    
    def _mock_full_description(self, product_name: str) -> str:
        """生成完整描述"""
        return f"""Product Description

Introducing our Premium {product_name}, designed to deliver exceptional quality and performance. Whether you're at home, in the office, or on the go, this product is built to exceed your expectations.

**Why Choose Our {product_name}?**

Our {product_name} stands out from the competition with its superior craftsmanship and attention to detail. Each unit undergoes rigorous quality testing to ensure it meets our high standards before reaching you.

**Key Features:**
- Premium materials for maximum durability
- Sleek, modern design that fits any setting
- Easy to use, no complicated setup required
- Compact and lightweight for convenient storage and travel
- Backed by our 30-day satisfaction guarantee

**What's Included:**
1x {product_name}
1x User Manual
1x Warranty Card

**Customer Satisfaction Guaranteed:**
We stand behind our products with confidence. If you're not completely satisfied with your purchase, simply contact us for a full refund - no questions asked.

Shop with confidence and experience the difference quality makes. Order now!

---

*Note: This is a product listing example generated for demonstration purposes.*"""
    
    def _mock_keywords(self, product_name: str, keyword_analysis: dict = None) -> List[str]:
        """生成关键词"""
        base_keywords = [
            product_name.lower(),
            f"best {product_name.lower()}",
            f"{product_name.lower()} for home",
            f"premium {product_name.lower()}",
            f"professional {product_name.lower()}",
            f"{product_name.lower()} portable",
            f"top rated {product_name.lower()}",
            f"quality {product_name.lower()}",
            f"{product_name.lower()} gift",
            f"2024 {product_name.lower()}"
        ]
        
        if keyword_analysis and "related_keywords" in keyword_analysis:
            base_keywords.extend(keyword_analysis["related_keywords"][:3])
        
        return list(set(base_keywords))[:10]
    
    def _mock_suggested_price(self, product_name: str, competitor_data: dict = None) -> float:
        """建议价格"""
        if competitor_data and "avg_price" in competitor_data:
            return round(competitor_data["avg_price"] * 0.95, 2)
        
        return round(random.uniform(19.99, 59.99), 2)
    
    def _call_openai(
        self,
        product_name: str,
        keyword_analysis: dict = None,
        competitor_data: dict = None,
        target_market: str = "US"
    ) -> AIListing:
        """调用OpenAI API生成Listing"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""Create an optimized Amazon product listing for:
Product: {product_name}
Market: {target_market}

{'-' * 50}
Keyword Analysis: {json.dumps(keyword_analysis, indent=2) if keyword_analysis else 'N/A'}
Competitor Data: {json.dumps(competitor_data, indent=2) if competitor_data else 'N/A'}
{'-' * 50}

Generate a JSON response with:
1. title: SEO-optimized product title (max 200 chars)
2. short_description: 5 bullet points with key features (use ✓ prefix)
3. full_description: Detailed product description (2-3 paragraphs)
4. keywords: 10 relevant search keywords
5. suggested_price: Recommended selling price in USD

Return ONLY valid JSON, no markdown formatting."""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # 尝试解析JSON
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            data = json.loads(content)
            
            return AIListing(
                title=data.get("title", ""),
                short_description=data.get("short_description", ""),
                full_description=data.get("full_description", ""),
                keywords=data.get("keywords", []),
                suggested_price=float(data.get("suggested_price", 29.99))
            )
            
        except Exception as e:
            print(f"OpenAI API error: {e}, falling back to mock")
            return self._generate_mock(product_name, keyword_analysis, competitor_data, target_market)
    
    def batch_generate(self, products: list) -> list:
        """批量生成"""
        return [self.generate(
            product_name=p.get("product_name", ""),
            keyword_analysis=p.get("keyword_analysis"),
            competitor_data=p.get("competitor_data"),
            target_market=p.get("target_market", "US")
        ) for p in products]
