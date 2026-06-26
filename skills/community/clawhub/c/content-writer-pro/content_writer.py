"""
Content Writer Pro - Professional copywriting generator
文案生成专家 - 专业文案生成工具

Features:
- Marketing copy generation / 营销文案生成
- Social media post templates / 社媒内容模板
- Ad copy variations / 广告文案变体
- Brand storytelling / 品牌故事
- Email templates / 邮件模板
- Product descriptions / 产品描述
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class ContentTone(Enum):
    """Content tone options / 内容语调选项"""
    PROFESSIONAL = "professional"  # 专业
    CASUAL = "casual"              # 随意
    PLAYFUL = "playful"            # 活泼
    FORMAL = "formal"              # 正式
    FRIENDLY = "friendly"          # 友好
    URGENT = "urgent"              # 紧急
    INSPIRATIONAL = "inspirational"  # 励志


class ContentType(Enum):
    """Content type options / 内容类型选项"""
    MARKETING = "marketing"
    SOCIAL_MEDIA = "social_media"
    AD_COPY = "ad_copy"
    BRAND_STORY = "brand_story"
    EMAIL = "email"
    PRODUCT_DESC = "product_description"


class SocialPlatform(Enum):
    """Social media platforms / 社交媒体平台"""
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    WEIBO = "weibo"
    XIAOHONGSHU = "xiaohongshu"


@dataclass
class CopyResult:
    """Result of copy generation / 文案生成结果"""
    content: str
    content_type: str
    tone: str
    variations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "content_type": self.content_type,
            "tone": self.tone,
            "variations": self.variations,
            "metadata": self.metadata
        }


@dataclass
class AdCopyResult:
    """Result of ad copy generation / 广告文案生成结果"""
    headlines: List[str]
    body_copies: List[str]
    ctas: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "headlines": self.headlines,
            "body_copies": self.body_copies,
            "ctas": self.ctas
        }


class ContentWriterError(Exception):
    """Custom exception for content writer errors / 文案生成器自定义异常"""
    pass


class ContentWriterPro:
    """
    Professional copywriting generator
    专业文案生成工具
    """
    
    # Templates for different content types / 不同内容类型的模板
    MARKETING_TEMPLATES = {
        ContentTone.PROFESSIONAL: [
            "Introducing {product}: The solution designed for {audience}. Experience {benefit} with our cutting-edge technology.",
            "{product} empowers {audience} to achieve {benefit}. Join thousands of professionals who trust our platform.",
            "Transform your workflow with {product}. Built specifically for {audience} who demand excellence.",
        ],
        ContentTone.CASUAL: [
            "Hey {audience}! Check out {product} - it's perfect for getting {benefit} without the hassle.",
            "Looking for {benefit}? {product} has got you covered! Made with {audience} in mind.",
            "Meet {product}: your new favorite tool for {benefit}. Designed especially for {audience} like you!",
        ],
        ContentTone.URGENT: [
            "Don't miss out! {product} is helping {audience} achieve {benefit} right now. Limited time offer!",
            "Act fast! {product} is revolutionizing how {audience} achieve {benefit}. Join before it's too late!",
        ],
        ContentTone.INSPIRATIONAL: [
            "Imagine achieving {benefit} effortlessly. With {product}, {audience} everywhere are making it happen.",
            "Your journey to {benefit} starts here. {product} - created for {audience} who dream big.",
        ]
    }
    
    SOCIAL_TEMPLATES = {
        SocialPlatform.LINKEDIN: {
            ContentTone.PROFESSIONAL: [
                "Excited to share insights on {topic}. In my experience, the key is consistent effort and strategic thinking. What are your thoughts? #ProfessionalGrowth",
                "Reflection on {topic}: Success doesn't happen overnight. It takes dedication, learning, and adaptability. Would love to hear your perspective. #Leadership",
                "Just published my thoughts on {topic}. After years in the industry, I've learned that {topic} requires both patience and innovation. Link in comments!",
            ],
            ContentTone.CASUAL: [
                "Quick thought on {topic} - sometimes the simplest approach works best. What's your take?",
                "Been thinking about {topic} lately. Anyone else feeling the same way about where things are headed?",
            ]
        },
        SocialPlatform.TWITTER: {
            ContentTone.PROFESSIONAL: [
                "Key insight on {topic}: Focus on what matters most. The rest will follow. #ProfessionalTips",
                "Thread on {topic} 🧵\n\n1/ Understanding the fundamentals is crucial before diving into advanced strategies.",
            ],
            ContentTone.CASUAL: [
                "Hot take on {topic} 👀\n\nChange my mind.",
                "Unpopular opinion: {topic} isn't as complicated as people make it out to be.",
            ]
        },
        SocialPlatform.INSTAGRAM: {
            ContentTone.CASUAL: [
                "✨ {topic} vibes only ✨\n\nWhat's your {topic} routine? Drop a 🙌 if you're all about it!",
                "When {topic} just clicks 🎯\n\nTag someone who needs to see this!",
            ],
            ContentTone.INSPIRATIONAL: [
                "Your {topic} journey is unique. Don't compare your chapter 1 to someone else's chapter 20. 💪",
                "Dream big. Work hard. Make {topic} happen. 🌟\n\nWho's with me?",
            ]
        }
    }
    
    AD_TEMPLATES = {
        "headlines": {
            ContentTone.URGENT: [
                "Limited Time: Transform Your {product_category} Today",
                "Don't Miss Out - {benefit} Awaits!",
                "Last Chance: Get {benefit} with {product}",
            ],
            ContentTone.PROFESSIONAL: [
                "The {product_category} Solution Trusted by {audience}",
                "Achieve {benefit} with {product}",
                "Professional-Grade {product_category} for {audience}",
            ],
            ContentTone.INSPIRATIONAL: [
                "Unlock Your Potential with {product}",
                "Your Journey to {benefit} Starts Here",
                "Imagine {benefit} - Now Make It Real",
            ]
        },
        "ctas": [
            "Get Started Now",
            "Learn More",
            "Try It Free",
            "Join Today",
            "Discover How",
            "Start Your Journey",
        ]
    }
    
    EMAIL_TEMPLATES = {
        "newsletter": {
            "subject": [
                "This Week's Insights: {topic}",
                "Your Weekly {topic} Digest",
                "What's New in {topic}?",
            ],
            "body": """Hi {name},

Welcome to this week's edition of our newsletter!

{topic} continues to evolve, and we're here to keep you informed. Here are this week's highlights:

{content}

Until next time,
The Team
"""
        },
        "promotional": {
            "subject": [
                "Special Offer: {discount}% Off {product}!",
                "Don't Miss: Exclusive Deal on {product}",
                "Your Invitation: Save on {product}",
            ],
            "body": """Hi {name},

We have something special for you!

For a limited time, enjoy {discount}% off {product}. Here's what you'll get:

{benefits}

[Shop Now - {cta}]

This offer expires soon, so don't wait!

Best regards,
The Team
"""
        },
        "welcome": {
            "subject": [
                "Welcome to {company}!",
                "Your Journey Starts Here",
                "Thanks for Joining {company}",
            ],
            "body": """Hi {name},

Welcome to the {company} family! 🎉

We're thrilled to have you on board. Here's what you can expect:

{onboarding_steps}

If you have any questions, just reply to this email.

Cheers,
The {company} Team
"""
        }
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize ContentWriterPro
        
        Args:
            config: Optional configuration dictionary
                   可选的配置字典
        """
        self.config = config or {}
        self.default_tone = ContentTone(self.config.get('default_tone', 'professional'))
        self.max_length = self.config.get('max_length', 1000)
        self.language = self.config.get('language', 'en')
    
    def _get_random_template(self, templates: List[str]) -> str:
        """Get a random template from the list"""
        return random.choice(templates)
    
    def _validate_input(self, text: str, min_length: int = 1) -> None:
        """Validate input text"""
        if not text or len(text.strip()) < min_length:
            raise ContentWriterError(f"Input must be at least {min_length} characters")
    
    def generate_marketing_copy(
        self,
        product: str,
        audience: str,
        benefit: Optional[str] = None,
        tone: Optional[str] = None
    ) -> CopyResult:
        """
        Generate marketing copy
        生成营销文案
        
        Args:
            product: Product or service name
            audience: Target audience
            benefit: Key benefit (optional)
            tone: Content tone (optional)
            
        Returns:
            CopyResult with generated content
        """
        self._validate_input(product)
        self._validate_input(audience)
        
        tone_enum = ContentTone(tone) if tone else self.default_tone
        benefit = benefit or "amazing results"
        
        if tone_enum not in self.MARKETING_TEMPLATES:
            tone_enum = ContentTone.PROFESSIONAL
        
        templates = self.MARKETING_TEMPLATES[tone_enum]
        template = self._get_random_template(templates)
        
        content = template.format(
            product=product,
            audience=audience,
            benefit=benefit
        )
        
        # Generate variations
        variations = [
            t.format(product=product, audience=audience, benefit=benefit)
            for t in templates[:3]
        ]
        
        return CopyResult(
            content=content,
            content_type="marketing",
            tone=tone_enum.value,
            variations=variations,
            metadata={"product": product, "audience": audience}
        )
    
    def create_social_post(
        self,
        platform: str,
        topic: str,
        tone: Optional[str] = None,
        length: str = "medium"
    ) -> CopyResult:
        """
        Create social media post
        创建社交媒体帖子
        
        Args:
            platform: Social platform (linkedin, twitter, instagram)
            topic: Post topic
            tone: Content tone (optional)
            length: Post length (short, medium, long)
            
        Returns:
            CopyResult with generated post
        """
        self._validate_input(topic)
        
        try:
            platform_enum = SocialPlatform(platform.lower())
        except ValueError:
            platform_enum = SocialPlatform.LINKEDIN
        
        tone_enum = ContentTone(tone) if tone else ContentTone.CASUAL
        
        if platform_enum not in self.SOCIAL_TEMPLATES:
            platform_enum = SocialPlatform.LINKEDIN
        
        platform_templates = self.SOCIAL_TEMPLATES[platform_enum]
        
        if tone_enum not in platform_templates:
            tone_enum = list(platform_templates.keys())[0]
        
        templates = platform_templates[tone_enum]
        content = self._get_random_template(templates).format(topic=topic)
        
        return CopyResult(
            content=content,
            content_type="social_media",
            tone=tone_enum.value,
            variations=[t.format(topic=topic) for t in templates],
            metadata={"platform": platform, "topic": topic, "length": length}
        )
    
    def write_ad_copy(
        self,
        product: str,
        product_category: Optional[str] = None,
        audience: Optional[str] = None,
        benefit: Optional[str] = None,
        headline_options: int = 3,
        description_options: int = 2
    ) -> AdCopyResult:
        """
        Write advertising copy
        撰写广告文案
        
        Args:
            product: Product name
            product_category: Category of product
            audience: Target audience
            benefit: Key benefit
            headline_options: Number of headline variations
            description_options: Number of description variations
            
        Returns:
            AdCopyResult with headlines, body copies, and CTAs
        """
        self._validate_input(product)
        
        product_category = product_category or "Solution"
        audience = audience or "Professionals"
        benefit = benefit or "Success"
        
        headlines = []
        for tone in [ContentTone.URGENT, ContentTone.PROFESSIONAL, ContentTone.INSPIRATIONAL]:
            templates = self.AD_TEMPLATES["headlines"][tone]
            for template in templates[:max(1, headline_options // 3 + 1)]:
                headlines.append(template.format(
                    product=product,
                    product_category=product_category,
                    audience=audience,
                    benefit=benefit
                ))
        
        headlines = headlines[:headline_options]
        
        body_templates = [
            f"Discover how {product} helps {audience} achieve {benefit}. Our innovative approach sets us apart.",
            f"Join thousands of {audience} who trust {product} for {benefit}. Experience the difference today.",
            f"{product} is the {product_category} solution you've been looking for. Get {benefit} starting now.",
        ]
        body_copies = body_templates[:description_options]
        
        ctas = random.sample(self.AD_TEMPLATES["ctas"], min(3, len(self.AD_TEMPLATES["ctas"])))
        
        return AdCopyResult(
            headlines=headlines,
            body_copies=body_copies,
            ctas=ctas
        )
    
    def write_brand_story(
        self,
        company_name: str,
        founder_name: Optional[str] = None,
        origin_story: Optional[str] = None,
        mission: Optional[str] = None,
        values: Optional[List[str]] = None
    ) -> CopyResult:
        """
        Write brand story content
        撰写品牌故事内容
        
        Args:
            company_name: Company name
            founder_name: Founder name (optional)
            origin_story: Brief origin story (optional)
            mission: Company mission (optional)
            values: Company values (optional)
            
        Returns:
            CopyResult with brand story content
        """
        self._validate_input(company_name)
        
        values = values or ["Innovation", "Integrity", "Customer Focus"]
        mission = mission or f"To make a positive impact through our work at {company_name}"
        
        story_parts = [f"Welcome to {company_name}."]
        
        if origin_story:
            story_parts.append(f"Our journey began with a simple idea: {origin_story}")
        
        story_parts.append(f"Our mission is clear: {mission}")
        story_parts.append(f"We live by our values: {', '.join(values)}.")
        
        if founder_name:
            story_parts.append(f"Founded by {founder_name}, we continue to push boundaries every day.")
        
        story_parts.append(f"Join us as we write the next chapter of {company_name}.")
        
        content = "\n\n".join(story_parts)
        
        return CopyResult(
            content=content,
            content_type="brand_story",
            tone="inspirational",
            metadata={"company": company_name, "mission": mission, "values": values}
        )
    
    def write_email(
        self,
        email_type: str,
        topic: Optional[str] = None,
        name: Optional[str] = None,
        tone: Optional[str] = None,
        **kwargs
    ) -> CopyResult:
        """
        Write email content
        撰写邮件内容
        
        Args:
            email_type: Type of email (newsletter, promotional, welcome)
            topic: Email topic (optional)
            name: Recipient name (optional)
            tone: Email tone (optional)
            **kwargs: Additional template variables
            
        Returns:
            CopyResult with email subject and body
        """
        if email_type not in self.EMAIL_TEMPLATES:
            raise ContentWriterError(f"Unknown email type: {email_type}")
        
        topic = topic or "Updates"
        name = name or "there"
        
        templates = self.EMAIL_TEMPLATES[email_type]
        subject = self._get_random_template(templates["subject"]).format(
            topic=topic,
            **kwargs
        )
        
        body = templates["body"].format(
            name=name,
            topic=topic,
            **kwargs
        )
        
        content = f"Subject: {subject}\n\n{body}"
        
        return CopyResult(
            content=content,
            content_type=f"email_{email_type}",
            tone=tone or "professional",
            metadata={"email_type": email_type, "subject": subject}
        )
    
    def write_product_description(
        self,
        product_name: str,
        features: List[str],
        target_audience: Optional[str] = None,
        unique_selling_point: Optional[str] = None
    ) -> CopyResult:
        """
        Write product description
        撰写产品描述
        
        Args:
            product_name: Product name
            features: List of product features
            target_audience: Target audience (optional)
            unique_selling_point: USP (optional)
            
        Returns:
            CopyResult with product description
        """
        self._validate_input(product_name)
        if not features:
            raise ContentWriterError("At least one feature is required")
        
        target_audience = target_audience or "professionals"
        usp = unique_selling_point or f"the best choice for {target_audience}"
        
        intro = f"Introducing {product_name} - {usp}."
        
        feature_text = "Key features include:\n"
        for feature in features:
            feature_text += f"• {feature}\n"
        
        closing = f"Designed for {target_audience} who demand excellence. Experience {product_name} today."
        
        content = f"{intro}\n\n{feature_text}\n{closing}"
        
        return CopyResult(
            content=content,
            content_type="product_description",
            tone="professional",
            metadata={"product": product_name, "features": features}
        )
    
    def create_twitter_thread(
        self,
        topic: str,
        num_tweets: int = 5,
        tone: Optional[str] = None
    ) -> List[str]:
        """
        Create a Twitter thread
        创建 Twitter 串推
        
        Args:
            topic: Thread topic
            num_tweets: Number of tweets in thread
            tone: Content tone (optional)
            
        Returns:
            List of tweet texts
        """
        self._validate_input(topic)
        if num_tweets < 2 or num_tweets > 10:
            raise ContentWriterError("Number of tweets must be between 2 and 10")
        
        tone_enum = ContentTone(tone) if tone else ContentTone.PROFESSIONAL
        
        tweets = []
        
        # Opening tweet
        if tone_enum == ContentTone.PROFESSIONAL:
            tweets.append(f"Thread on {topic} 🧵\n\n1/{num_tweets} Understanding {topic} requires looking at multiple perspectives.")
        else:
            tweets.append(f"{topic} thread incoming 🧵\n\n1/{num_tweets} Let's dive in!")
        
        # Middle tweets
        for i in range(2, num_tweets):
            if tone_enum == ContentTone.PROFESSIONAL:
                tweets.append(f"{i}/{num_tweets} Key insight: {topic} is about continuous learning and adaptation.")
            else:
                tweets.append(f"{i}/{num_tweets} Here's something interesting about {topic}...")
        
        # Closing tweet
        if tone_enum == ContentTone.PROFESSIONAL:
            tweets.append(f"{num_tweets}/{num_tweets} Thanks for reading! What's your experience with {topic}? Let's discuss. 👇")
        else:
            tweets.append(f"{num_tweets}/{num_tweets} That's a wrap! Thoughts on {topic}? Drop a comment! 💬")
        
        return tweets
    
    def get_supported_tones(self) -> List[str]:
        """Get list of supported tones / 获取支持的语调列表"""
        return [tone.value for tone in ContentTone]
    
    def get_supported_platforms(self) -> List[str]:
        """Get list of supported social platforms / 获取支持的社交平台列表"""
        return [platform.value for platform in SocialPlatform]


# Convenience function for quick copy generation
def quick_marketing_copy(product: str, audience: str, benefit: str = "great results") -> str:
    """
    Quick function to generate marketing copy
    快速生成营销文案的函数
    
    Args:
        product: Product name
        audience: Target audience
        benefit: Key benefit
        
    Returns:
        Generated marketing copy string
    """
    writer = ContentWriterPro()
    result = writer.generate_marketing_copy(product, audience, benefit)
    return result.content
