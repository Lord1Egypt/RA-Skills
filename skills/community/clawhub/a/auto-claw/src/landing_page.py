"""
Smart Landing Page + Review Summarizer — WordPress 智能落地页引擎
支持UGC评价摘要 + 信任信号 + 转化优化
"""
import re
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Review:
    """用户评价"""
    review_id: str
    author: str = ""
    rating: float = 1.0  # 1-5
    title: str = ""
    body: str = ""
    date: str = ""
    
    # 验证
    is_verified: bool = False  # 已购买
    is_recommended: bool = True
    
    # 标签
    sentiment: str = ""  # positive / neutral / negative
    keywords: List[str] = field(default_factory=list)
    
    # 来源
    source: str = ""  # internal / yotpo / trustpilot

@dataclass
class ReviewSummary:
    """评价摘要"""
    total_reviews: int = 0
    average_rating: float = 0.0
    rating_distribution: Dict[int, int] = field(default_factory=dict)  # star: count
    
    # 摘要
    top_pros: List[str] = field(default_factory=list)
    top_cons: List[str] = field(default_factory=list)
    best_aspects: List[str] = field(default_factory=list)  # "易用性好" / "支持优秀"
    
    # 情感
    positive_pct: float = 0.0
    neutral_pct: float = 0.0
    negative_pct: float = 0.0
    
    # 推荐
    recommendation_rate: float = 0.0  # 多少%用户推荐

@dataclass
class LandingPageVariant:
    """落地页变体"""
    variant_id: str
    name: str = ""  # "Control" / "Social Proof Heavy"
    
    # Hero
    hero_headline: str = ""
    hero_subheadline: str = ""
    hero_image_url: str = ""
    
    # Social Proof
    show_rating_summary: bool = True
    show_review_carousel: bool = True
    review_count: int = 3
    show_trust_badges: bool = True
    trust_score: str = ""  # "4.8/5 from 2,847 reviews"
    
    # 转化
    cta_text: str = "Start Free Trial"
    cta_color: str = "#e74c3c"
    
    # 统计
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    
    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions > 0 else 0.0
    
    @property
    def cvr(self) -> float:
        return self.conversions / self.impressions if self.impressions > 0 else 0.0

class ReviewSummarizer:
    """评价摘要生成器"""
    
    POSITIVE_WORDS = [
        "great", "excellent", "amazing", "love", "perfect", "best",
        "awesome", "fantastic", "wonderful", "outstanding", "superb",
        "easy", "fast", "helpful", "recommend", "reliable", "quality",
        "professional", "responsive", "intuitive", "powerful", "value"
    ]
    NEGATIVE_WORDS = [
        "bad", "terrible", "awful", "worst", "hate", "poor",
        "slow", "buggy", "difficult", "confusing", "broken",
        "disappointing", "frustrating", "unreliable", "overpriced"
    ]
    ASPECT_PATTERNS = {
        "易用性": [r"(?:easy|simple|intuitive|user-friendly)", r"(?:difficult|confusing)"],
        "性能": [r"(?:fast|quick|speed|performance)", r"(?:slow|laggy)"],
        "支持": [r"(?:support|help|service|team|responsive)", r"(?:no support|unresponsive)"],
        "质量": [r"(?:quality|reliable|solid)", r"(?:buggy|broken)"],
        "性价比": [r"(?:value|worth|price|affordable)", r"(?:overpriced|expensive)"],
        "功能": [r"(?:feature|powerful|comprehensive)", r"(?:limited|missing)"],
    }
    
    def __init__(self):
        pass
    
    def analyze_sentiment(self, text: str) -> str:
        text_lower = text.lower()
        pos = sum(1 for w in self.POSITIVE_WORDS if w in text_lower)
        neg = sum(1 for w in self.NEGATIVE_WORDS if w in text_lower)
        if pos > neg:
            return "positive"
        elif neg > pos:
            return "negative"
        return "neutral"
    
    def extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        freq = defaultdict(int)
        for w in words:
            if w in self.POSITIVE_WORDS or w in self.NEGATIVE_WORDS:
                freq[w] += 1
        return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:5]]
    
    def summarize(self, reviews: List[Review]) -> ReviewSummary:
        if not reviews:
            return ReviewSummary()
        
        total = len(reviews)
        avg = sum(r.rating for r in reviews) / total
        
        # 评分分布
        dist = defaultdict(int)
        for r in reviews:
            star = int(round(r.rating))
            dist[star] += 1
        
        # 情感分析
        sentiments = [self.analyze_sentiment(r.body) for r in reviews]
        pos = sum(1 for s in sentiments if s == "positive") / total
        neu = sum(1 for s in sentiments if s == "neutral") / total
        neg = sum(1 for s in sentiments if s == "negative") / total
        
        # 推荐率
        rec = sum(1 for r in reviews if r.is_recommended) / total
        
        # 提取优点/缺点
        all_text = " ".join(r.body for r in reviews)
        keywords = self.extract_keywords(all_text)
        
        # 简化：直接统计情感关键词频率
        pos_words = [w for w in keywords if w in self.POSITIVE_WORDS][:5]
        neg_words = [w for w in keywords if w in self.NEGATIVE_WORDS][:5]
        
        return ReviewSummary(
            total_reviews=total,
            average_rating=avg,
            rating_distribution=dict(dist),
            top_pros=pos_words,
            top_cons=neg_words,
            positive_pct=pos * 100,
            neutral_pct=neu * 100,
            negative_pct=neg * 100,
            recommendation_rate=rec * 100
        )
    
    def generate_summary_text(self, summary: ReviewSummary) -> str:
        stars = "⭐" * int(round(summary.average_rating))
        lines = [
            f"{summary.average_rating:.1f}/5 {stars}",
            f"基于 {summary.total_reviews} 条评价",
        ]
        
        if summary.top_pros:
            lines.append(f"用户好评: {', '.join(summary.top_pros[:3])}")
        if summary.top_cons:
            lines.append(f"待改进: {', '.join(summary.top_cons[:2])}")
        
        return " | ".join(lines)


class SmartLandingPage:
    """
    WordPress 智能落地页引擎
    
    功能：
    1. 落地页变体A/B测试
    2. 社交证明自动注入（评价摘要/信任徽章）
    3. 动态内容优化
    4. 生成高转化落地页HTML
    5. 实时数据追踪
    """
    
    def __init__(self, site_url: str = ""):
        self.site_url = site_url
        self.variants: Dict[str, LandingPageVariant] = {}
        self.reviews: List[Review] = []
        self.review_summarizer = ReviewSummarizer()
        self.review_summary: Optional[ReviewSummary] = None
    
    def add_review(self, rating: float, title: str, body: str,
                  author: str = "Verified Buyer", is_verified: bool = True,
                  date: str = "") -> Review:
        review_id = hashlib.md5(body.encode()).hexdigest()[:8]
        sentiment = self.review_summarizer.analyze_sentiment(body)
        keywords = self.review_summarizer.extract_keywords(body)
        
        review = Review(
            review_id=review_id,
            author=author,
            rating=rating,
            title=title,
            body=body,
            date=date or time.strftime("%Y-%m-%d"),
            is_verified=is_verified,
            sentiment=sentiment,
            keywords=keywords
        )
        self.reviews.append(review)
        self.review_summary = self.review_summarizer.summarize(self.reviews)
        return review
    
    def create_variant(self, name: str) -> LandingPageVariant:
        variant = LandingPageVariant(
            variant_id=hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8],
            name=name
        )
        self.variants[variant.variant_id] = variant
        return variant
    
    def generate_html(self, variant: LandingPageVariant) -> str:
        """生成落地页HTML"""
        summary = self.review_summary
        trust_line = variant.trust_score
        
        if summary and variant.show_rating_summary:
            stars = "⭐" * int(round(summary.average_rating))
            trust_line = f"{summary.average_rating:.1f}/5 {stars} · {summary.total_reviews} 条真实评价"
        
        html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{variant.hero_headline or "Transform Your Business Today"}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #222; line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
.hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 80px 0; text-align: center; }}
.hero h1 {{ font-size: 48px; margin-bottom: 16px; font-weight: 800; }}
.hero p {{ font-size: 20px; opacity: 0.9; margin-bottom: 32px; }}
.cta-button {{ display: inline-block; background: {variant.cta_color}; color: white; padding: 16px 48px; font-size: 18px; font-weight: 700; border-radius: 8px; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; }}
.cta-button:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }}
.trust-bar {{ background: #f8f9fa; padding: 24px 0; text-align: center; border-bottom: 1px solid #eee; }}
.trust-bar p {{ color: #666; font-size: 16px; }}
.stars {{ color: #f39c12; font-size: 20px; }}
.reviews-section {{ padding: 60px 0; background: white; }}
.reviews-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 32px; }}
.review-card {{ border: 1px solid #eee; border-radius: 12px; padding: 24px; }}
.review-stars {{ color: #f39c12; margin-bottom: 8px; }}
.review-title {{ font-weight: 700; margin-bottom: 8px; }}
.review-body {{ color: #555; font-size: 15px; }}
.review-author {{ margin-top: 12px; font-size: 13px; color: #999; }}
.verified {{ color: #27ae60; font-size: 12px; }}
</style>
</head>
<body>

<section class="hero">
  <div class="container">
    <h1>{variant.hero_headline or "Transform Your Business Today"}</h1>
    <p>{variant.hero_subheadline or "Join thousands of teams already growing with our platform"}</p>
    <a href="#" class="cta-button">{variant.cta_text}</a>
  </div>
</section>

<section class="trust-bar">
  <div class="container">
    <p class="stars">{"⭐" * 5}</p>
    <p><strong>{trust_line or "Trusted by 10,000+ teams worldwide"}</strong></p>
  </div>
</section>

'''
        
        # 评价区
        if variant.show_review_carousel and self.reviews:
            html += '''<section class="reviews-section">
  <div class="container">
    <h2 style="text-align:center">用户真实评价</h2>
    <div class="reviews-grid">
'''
            for review in self.reviews[:variant.review_count]:
                stars = "⭐" * int(round(review.rating))
                verified_html = '<span class="verified">✓ 已验证购买</span>' if review.is_verified else ''
                html += f'''      <div class="review-card">
        <div class="review-stars">{stars}</div>
        <div class="review-title">{review.title}</div>
        <div class="review-body">"{review.body[:150]}{'...' if len(review.body) > 150 else ''}"</div>
        <div class="review-author">{review.author} · {review.date} {verified_html}</div>
      </div>
'''
            html += '''    </div>
  </div>
</section>
'''
        
        html += '''
<section style="padding: 60px 0; text-align: center; background: #f8f9fa;">
  <div class="container">
    <h2>准备好开始了吗？</h2>
    <p style="margin: 16px 0 32px">14天免费试用，无需信用卡</p>
    <a href="#" class="cta-button">立即开始</a>
  </div>
</section>

</body>
</html>'''
        return html
    
    def export_wp_shortcode(self, variant: LandingPageVariant) -> str:
        return f'''[smart-landing id="{variant.variant_id}" name="{variant.name}"]
[landing-hero headline="{variant.hero_headline}" cta="{variant.cta_text}"]
[review-carousel count="{variant.review_count}"]
[/smart-landing]'''

def demo():
    page = SmartLandingPage()
    
    # 添加评价
    page.add_review(5.0, "绝对值得！", "This product is amazing. Easy to use and the support team is incredibly responsive. Highly recommend to anyone looking for a reliable solution.", "Sarah M.", is_verified=True)
    page.add_review(4.0, "很好用", "Great tool for our team. We have been using it for 6 months and it has significantly improved our workflow. The only minor issue is the mobile app needs some work.", "John D.", is_verified=True)
    page.add_review(5.0, "物超所值", "Outstanding value for money. The features are comprehensive and the performance is excellent. Customer service is also top-notch.", "Mike R.", is_verified=True)
    page.add_review(4.0, "不错的选择", "Solid product overall. Does what it promises. A bit pricey but worth it for the quality you get.", "Lisa K.", is_verified=False)
    page.add_review(5.0, "完美", "Perfect solution for our needs. The AI features are game-changing and have saved us countless hours.", "Alex T.", is_verified=True)
    
    # 摘要
    summary = page.review_summary
    print(f"\n⭐ 评价摘要: {summary.average_rating:.1f}/5 ({summary.total_reviews}条)")
    print(f"   好评: {summary.positive_pct:.0f}% | 中评: {summary.neutral_pct:.0f}% | 差评: {summary.negative_pct:.0f}%")
    print(f"   推荐率: {summary.recommendation_rate:.0f}%")
    print(f"   优点: {', '.join(summary.top_pros[:5])}")
    
    # 落地页
    variant = page.create_variant("Social Proof Heavy")
    variant.hero_headline = "AI驱动团队协作，让效率提升10倍"
    variant.hero_subheadline = "全球10,000+团队信赖，已验证的业绩提升"
    variant.cta_text = "免费试用14天"
    variant.review_count = 3
    variant.show_rating_summary = True
    variant.show_review_carousel = True
    
    html = page.generate_html(variant)
    
    # 保存
    with open("/tmp/landing_page_demo.html", "w") as f:
        f.write(html)
    print(f"\n✅ 落地页生成完成: /tmp/landing_page_demo.html")
    print(f"   变体: {variant.name}")
    print(f"   短代码: {page.export_wp_shortcode(variant)[:60]}...")

if __name__ == "__main__":
    demo()
