#!/usr/bin/env python3
"""
Unit tests for Content Writer Pro / 文案生成专家的单元测试

Run with: python -m pytest tests/test_writer.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from content_writer import (
    ContentWriterPro,
    ContentTone,
    ContentType,
    SocialPlatform,
    CopyResult,
    AdCopyResult,
    ContentWriterError,
    quick_marketing_copy,
)


class TestContentWriterPro(unittest.TestCase):
    """Test cases for ContentWriterPro class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.writer = ContentWriterPro()
    
    # =================================================================
    # Marketing Copy Tests / 营销文案测试
    # =================================================================
    
    def test_generate_marketing_copy_basic(self):
        """Test basic marketing copy generation"""
        result = self.writer.generate_marketing_copy(
            product="Test Product",
            audience="Testers"
        )
        self.assertIsInstance(result, CopyResult)
        self.assertEqual(result.content_type, "marketing")
        self.assertGreater(len(result.content), 0)
    
    def test_generate_marketing_copy_with_benefit(self):
        """Test marketing copy with benefit specified"""
        result = self.writer.generate_marketing_copy(
            product="AI Tool",
            audience="Developers",
            benefit="faster coding"
        )
        self.assertIn("faster", result.content.lower())
    
    def test_generate_marketing_copy_with_tone(self):
        """Test marketing copy with specific tone"""
        result = self.writer.generate_marketing_copy(
            product="App",
            audience="Users",
            tone="casual"
        )
        self.assertEqual(result.tone, "casual")
    
    def test_generate_marketing_copy_empty_product_raises_error(self):
        """Test that empty product raises error"""
        with self.assertRaises(ContentWriterError):
            self.writer.generate_marketing_copy("", "Audience")
    
    def test_generate_marketing_copy_empty_audience_raises_error(self):
        """Test that empty audience raises error"""
        with self.assertRaises(ContentWriterError):
            self.writer.generate_marketing_copy("Product", "")
    
    def test_generate_marketing_copy_has_variations(self):
        """Test that result includes variations"""
        result = self.writer.generate_marketing_copy("Product", "Audience")
        self.assertIsInstance(result.variations, list)
        self.assertGreater(len(result.variations), 0)
    
    # =================================================================
    # Social Media Tests / 社媒内容测试
    # =================================================================
    
    def test_create_social_post_basic(self):
        """Test basic social post creation"""
        result = self.writer.create_social_post(
            platform="linkedin",
            topic="AI"
        )
        self.assertIsInstance(result, CopyResult)
        self.assertEqual(result.content_type, "social_media")
    
    def test_create_social_post_different_platforms(self):
        """Test social posts for different platforms"""
        platforms = ["linkedin", "twitter", "instagram"]
        for platform in platforms:
            result = self.writer.create_social_post(
                platform=platform,
                topic="Test"
            )
            self.assertIsInstance(result, CopyResult)
            self.assertEqual(result.metadata["platform"], platform)
    
    def test_create_social_post_empty_topic_raises_error(self):
        """Test that empty topic raises error"""
        with self.assertRaises(ContentWriterError):
            self.writer.create_social_post("linkedin", "")
    
    def test_create_social_post_with_tone(self):
        """Test social post with specific tone"""
        result = self.writer.create_social_post(
            platform="twitter",
            topic="Startup",
            tone="casual"
        )
        self.assertEqual(result.tone, "casual")
    
    # =================================================================
    # Ad Copy Tests / 广告文案测试
    # =================================================================
    
    def test_write_ad_copy_basic(self):
        """Test basic ad copy generation"""
        result = self.writer.write_ad_copy(product="Test Product")
        self.assertIsInstance(result, AdCopyResult)
        self.assertGreater(len(result.headlines), 0)
        self.assertGreater(len(result.body_copies), 0)
        self.assertGreater(len(result.ctas), 0)
    
    def test_write_ad_copy_with_options(self):
        """Test ad copy with specific option counts"""
        result = self.writer.write_ad_copy(
            product="Product",
            headline_options=5,
            description_options=3
        )
        self.assertLessEqual(len(result.headlines), 5)
        self.assertLessEqual(len(result.body_copies), 3)
    
    def test_write_ad_copy_empty_product_raises_error(self):
        """Test that empty product raises error"""
        with self.assertRaises(ContentWriterError):
            self.writer.write_ad_copy("")
    
    def test_write_ad_copy_has_ctas(self):
        """Test that ad copy includes CTAs"""
        result = self.writer.write_ad_copy(product="Product")
        self.assertIsInstance(result.ctas, list)
        self.assertGreater(len(result.ctas), 0)
    
    # =================================================================
    # Brand Story Tests / 品牌故事测试
    # =================================================================
    
    def test_write_brand_story_basic(self):
        """Test basic brand story generation"""
        result = self.writer.write_brand_story(company_name="Test Co")
        self.assertIsInstance(result, CopyResult)
        self.assertEqual(result.content_type, "brand_story")
        self.assertIn("Test Co", result.content)
    
    def test_write_brand_story_with_all_params(self):
        """Test brand story with all parameters"""
        result = self.writer.write_brand_story(
            company_name="TechCorp",
            founder_name="John Doe",
            origin_story="a garage project",
            mission="to change the world",
            values=["Innovation", "Integrity"]
        )
        self.assertIn("John Doe", result.content)
        self.assertIn("change the world", result.content)
    
    def test_write_brand_story_empty_company_raises_error(self):
        """Test that empty company name raises error"""
        with self.assertRaises(ContentWriterError):
            self.writer.write_brand_story("")
    
    # =================================================================
    # Email Tests / 邮件测试
    # =================================================================
    
    def test_write_email_newsletter(self):
        """Test newsletter email generation"""
        result = self.writer.write_email(
            email_type="newsletter",
            topic="AI News",
            name="Reader"
        )
        self.assertIsInstance(result, CopyResult)
        self.assertEqual(result.content_type, "email_newsletter")
    
    def test_write_email_promotional(self):
        """Test promotional email generation"""
        result = self.writer.write_email(
            email_type="promotional",
            product="Pro Plan",
            discount=20
        )
        self.assertIn("20%", result.content)
    
    def test_write_email_welcome(self):
        """Test welcome email generation"""
        result = self.writer.write_email(
            email_type="welcome",
            company="Startup",
            name="New User"
        )
        self.assertIn("Startup", result.content)
    
    def test_write_email_unknown_type_raises_error(self):
        """Test that unknown email type raises error"""
        with self.assertRaises(ContentWriterError):
            self.writer.write_email(email_type="unknown")
    
    # =================================================================
    # Product Description Tests / 产品描述测试
    # =================================================================
    
    def test_write_product_description_basic(self):
        """Test basic product description generation"""
        result = self.writer.write_product_description(
            product_name="Test Product",
            features=["Feature 1", "Feature 2"]
        )
        self.assertIsInstance(result, CopyResult)
        self.assertEqual(result.content_type, "product_description")
        self.assertIn("Test Product", result.content)
    
    def test_write_product_description_empty_features_raises_error(self):
        """Test that empty features list raises error"""
        with self.assertRaises(ContentWriterError):
            self.writer.write_product_description("Product", [])
    
    def test_write_product_description_includes_features(self):
        """Test that description includes all features"""
        features = ["AI-powered", "Cloud-based", "Secure"]
        result = self.writer.write_product_description(
            product_name="App",
            features=features
        )
        for feature in features:
            self.assertIn(feature, result.content)
    
    # =================================================================
    # Twitter Thread Tests / Twitter串推测试
    # =================================================================
    
    def test_create_twitter_thread_basic(self):
        """Test basic Twitter thread creation"""
        tweets = self.writer.create_twitter_thread(
            topic="Startup",
            num_tweets=5
        )
        self.assertIsInstance(tweets, list)
        self.assertEqual(len(tweets), 5)
    
    def test_create_twitter_thread_min_max(self):
        """Test Twitter thread with min and max tweet counts"""
        with self.assertRaises(ContentWriterError):
            self.writer.create_twitter_thread("Topic", 1)
        
        with self.assertRaises(ContentWriterError):
            self.writer.create_twitter_thread("Topic", 11)
    
    def test_create_twitter_thread_has_numbering(self):
        """Test that tweets have numbering"""
        tweets = self.writer.create_twitter_thread("Topic", 3)
        self.assertIn("1/3", tweets[0])
        self.assertIn("2/3", tweets[1])
        self.assertIn("3/3", tweets[2])
    
    # =================================================================
    # Configuration Tests / 配置测试
    # =================================================================
    
    def test_default_config(self):
        """Test default configuration"""
        writer = ContentWriterPro()
        self.assertEqual(writer.default_tone, ContentTone.PROFESSIONAL)
        self.assertEqual(writer.max_length, 1000)
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = {
            'default_tone': 'casual',
            'max_length': 500,
            'language': 'zh'
        }
        writer = ContentWriterPro(config=config)
        self.assertEqual(writer.default_tone, ContentTone.CASUAL)
        self.assertEqual(writer.max_length, 500)
    
    # =================================================================
    # List Options Tests / 选项列表测试
    # =================================================================
    
    def test_get_supported_tones(self):
        """Test getting supported tones"""
        tones = self.writer.get_supported_tones()
        self.assertIsInstance(tones, list)
        self.assertIn("professional", tones)
        self.assertIn("casual", tones)
    
    def test_get_supported_platforms(self):
        """Test getting supported platforms"""
        platforms = self.writer.get_supported_platforms()
        self.assertIsInstance(platforms, list)
        self.assertIn("linkedin", platforms)
        self.assertIn("twitter", platforms)
    
    # =================================================================
    # Quick Function Tests / 快速函数测试
    # =================================================================
    
    def test_quick_marketing_copy(self):
        """Test quick marketing copy function"""
        copy = quick_marketing_copy("Product", "Audience")
        self.assertIsInstance(copy, str)
        self.assertGreater(len(copy), 0)
    
    def test_quick_marketing_copy_with_benefit(self):
        """Test quick marketing copy with benefit"""
        copy = quick_marketing_copy("Tool", "Devs", "efficiency")
        self.assertIn("Tool", copy)


class TestCopyResult(unittest.TestCase):
    """Test cases for CopyResult dataclass"""
    
    def test_default_creation(self):
        """Test default CopyResult creation"""
        result = CopyResult(
            content="Test content",
            content_type="marketing",
            tone="professional"
        )
        self.assertEqual(result.content, "Test content")
        self.assertEqual(result.content_type, "marketing")
        self.assertEqual(result.tone, "professional")
    
    def test_to_dict(self):
        """Test to_dict method"""
        result = CopyResult(
            content="Test",
            content_type="test",
            tone="neutral",
            variations=["v1", "v2"]
        )
        d = result.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d['content'], "Test")
        self.assertEqual(d['variations'], ["v1", "v2"])


class TestAdCopyResult(unittest.TestCase):
    """Test cases for AdCopyResult dataclass"""
    
    def test_to_dict(self):
        """Test to_dict method"""
        result = AdCopyResult(
            headlines=["H1", "H2"],
            body_copies=["B1"],
            ctas=["CTA1"]
        )
        d = result.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(len(d['headlines']), 2)


class TestContentWriterError(unittest.TestCase):
    """Test cases for ContentWriterError exception"""
    
    def test_error_message(self):
        """Test error message"""
        error = ContentWriterError("Test error")
        self.assertEqual(str(error), "Test error")
    
    def test_error_is_exception(self):
        """Test that ContentWriterError is an Exception"""
        with self.assertRaises(Exception):
            raise ContentWriterError("test")


class TestEnums(unittest.TestCase):
    """Test cases for Enum classes"""
    
    def test_content_tone_values(self):
        """Test ContentTone enum values"""
        self.assertEqual(ContentTone.PROFESSIONAL.value, "professional")
        self.assertEqual(ContentTone.CASUAL.value, "casual")
    
    def test_social_platform_values(self):
        """Test SocialPlatform enum values"""
        self.assertEqual(SocialPlatform.LINKEDIN.value, "linkedin")
        self.assertEqual(SocialPlatform.TWITTER.value, "twitter")


if __name__ == '__main__':
    unittest.main(verbosity=2)
