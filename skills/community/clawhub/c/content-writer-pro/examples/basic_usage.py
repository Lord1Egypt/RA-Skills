#!/usr/bin/env python3
"""
Basic usage examples for Content Writer Pro
文案生成专家基础使用示例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from content_writer import ContentWriterPro, quick_marketing_copy


def example_marketing_copy():
    """Example: Generate marketing copy / 生成营销文案示例"""
    print("=" * 60)
    print("Marketing Copy Example / 营销文案示例")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    # Professional tone / 专业语调
    result = writer.generate_marketing_copy(
        product="AI Analytics Platform",
        audience="Data Scientists",
        benefit="faster insights",
        tone="professional"
    )
    print("\nProfessional Tone:")
    print(result.content)
    
    # Casual tone / 随意语调
    result = writer.generate_marketing_copy(
        product="Task Manager App",
        audience="Freelancers",
        benefit="staying organized",
        tone="casual"
    )
    print("\nCasual Tone:")
    print(result.content)
    
    # Urgent tone / 紧急语调
    result = writer.generate_marketing_copy(
        product="SEO Masterclass",
        audience="Marketers",
        benefit="higher rankings",
        tone="urgent"
    )
    print("\nUrgent Tone:")
    print(result.content)


def example_social_media():
    """Example: Create social media posts / 创建社交媒体帖子示例"""
    print("\n" + "=" * 60)
    print("Social Media Example / 社媒内容示例")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    # LinkedIn post / LinkedIn帖子
    result = writer.create_social_post(
        platform="linkedin",
        topic="Remote Work Best Practices",
        tone="professional"
    )
    print("\nLinkedIn Post:")
    print(result.content)
    
    # Twitter post / Twitter帖子
    result = writer.create_social_post(
        platform="twitter",
        topic="AI Tools",
        tone="casual"
    )
    print("\nTwitter Post:")
    print(result.content)


def example_ad_copy():
    """Example: Write ad copy / 撰写广告文案示例"""
    print("\n" + "=" * 60)
    print("Ad Copy Example / 广告文案示例")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    result = writer.write_ad_copy(
        product="Cloud Storage Pro",
        product_category="Cloud Storage",
        audience="Small Businesses",
        benefit="secure file management",
        headline_options=3,
        description_options=2
    )
    
    print("\nHeadlines:")
    for i, headline in enumerate(result.headlines, 1):
        print(f"  {i}. {headline}")
    
    print("\nBody Copies:")
    for i, body in enumerate(result.body_copies, 1):
        print(f"  {i}. {body}")
    
    print("\nCTAs:")
    for i, cta in enumerate(result.ctas, 1):
        print(f"  {i}. {cta}")


def example_brand_story():
    """Example: Write brand story / 撰写品牌故事示例"""
    print("\n" + "=" * 60)
    print("Brand Story Example / 品牌故事示例")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    result = writer.write_brand_story(
        company_name="TechFlow",
        founder_name="Sarah Chen",
        origin_story="a passion for making technology accessible to everyone",
        mission="to democratize tech education",
        values=["Innovation", "Accessibility", "Community"]
    )
    
    print("\nBrand Story:")
    print(result.content)


def example_email():
    """Example: Write emails / 撰写邮件示例"""
    print("\n" + "=" * 60)
    print("Email Example / 邮件示例")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    # Newsletter / 新闻简报
    result = writer.write_email(
        email_type="newsletter",
        topic="AI Trends",
        name="John",
        content="• New AI models released\n• Industry insights\n• Upcoming events"
    )
    print("\nNewsletter:")
    print(result.content)
    
    # Promotional email / 促销邮件
    result = writer.write_email(
        email_type="promotional",
        name="Jane",
        product="Premium Plan",
        discount=20,
        benefits="• Unlimited storage\n• Priority support\n• Advanced analytics",
        cta="Get 20% Off"
    )
    print("\nPromotional Email:")
    print(result.content)


def example_product_description():
    """Example: Write product description / 撰写产品描述示例"""
    print("\n" + "=" * 60)
    print("Product Description Example / 产品描述示例")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    result = writer.write_product_description(
        product_name="Smart Hub X1",
        features=[
            "Voice control with AI assistant",
            "Compatible with 500+ smart devices",
            "Privacy-first design",
            "Energy monitoring dashboard"
        ],
        target_audience="smart home enthusiasts",
        unique_selling_point="the smartest home hub that actually respects your privacy"
    )
    
    print("\nProduct Description:")
    print(result.content)


def example_twitter_thread():
    """Example: Create Twitter thread / 创建Twitter串推示例"""
    print("\n" + "=" * 60)
    print("Twitter Thread Example / Twitter串推示例")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    tweets = writer.create_twitter_thread(
        topic="Startup Fundraising",
        num_tweets=5,
        tone="professional"
    )
    
    print("\nTwitter Thread:")
    for tweet in tweets:
        print(f"\n---\n{tweet}")


def example_quick_function():
    """Example: Quick marketing copy function / 快速营销文案函数示例"""
    print("\n" + "=" * 60)
    print("Quick Function Example / 快速函数示例")
    print("=" * 60)
    
    copy = quick_marketing_copy(
        product="Fitness App",
        audience="Busy Professionals",
        benefit="staying fit"
    )
    
    print("\nQuick Marketing Copy:")
    print(copy)


def example_list_options():
    """Example: List supported options / 列出支持的选项示例"""
    print("\n" + "=" * 60)
    print("Available Options / 可用选项")
    print("=" * 60)
    
    writer = ContentWriterPro()
    
    print("\nSupported Tones / 支持语调:")
    for tone in writer.get_supported_tones():
        print(f"  - {tone}")
    
    print("\nSupported Platforms / 支持平台:")
    for platform in writer.get_supported_platforms():
        print(f"  - {platform}")


if __name__ == "__main__":
    # Run all examples / 运行所有示例
    example_marketing_copy()
    example_social_media()
    example_ad_copy()
    example_brand_story()
    example_email()
    example_product_description()
    example_twitter_thread()
    example_quick_function()
    example_list_options()
    
    print("\n" + "=" * 60)
    print("All examples completed! / 所有示例完成！")
    print("=" * 60)
