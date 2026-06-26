# Content Writer Pro / 文案生成专家

[![Skill](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

> 专业文案生成工具 - 支持营销文案、社媒内容、广告文案、品牌故事等多种场景
> Professional copywriting generator for marketing, social media, ads, brand storytelling

## Features / 功能特性

### Marketing Copy / 营销文案
- Product descriptions / 产品描述
- Value propositions / 价值主张
- Feature highlights / 功能亮点
- Use case scenarios / 使用场景

### Social Media Content / 社媒内容
- LinkedIn posts / LinkedIn动态
- Twitter/X tweets / 推文
- Instagram captions / Instagram文案
- Facebook updates / Facebook更新

### Ad Copy / 广告文案
- Headlines / 标题
- Body copy / 正文
- Call-to-action / 行动号召
- A/B test variations / A/B测试变体

### Brand Story / 品牌故事
- Origin stories / 起源故事
- Mission statements / 使命宣言
- Vision statements / 愿景宣言
- Company values / 企业价值观

### Email Templates / 邮件模板
- Newsletters / 新闻简报
- Promotional emails / 促销邮件
- Welcome sequences / 欢迎序列
- Follow-up emails / 跟进邮件

## Installation / 安装

```bash
# Clone the repository
git clone https://github.com/yourusername/content-writer-pro.git
cd content-writer-pro

# Install dependencies
pip install -r requirements.txt
```

## Quick Start / 快速开始

```python
from content_writer import ContentWriterPro

# Initialize the writer
writer = ContentWriterPro()

# Generate marketing copy
copy = writer.generate_marketing_copy(
    product="AI Writing Assistant",
    audience="Content marketers",
    tone="professional"
)
print(copy)

# Create social media post
post = writer.create_social_post(
    platform="linkedin",
    topic="AI in content creation",
    tone="casual"
)
print(post)
```

## Usage Examples / 使用示例

### Marketing Copy Generation / 营销文案生成

```python
from content_writer import ContentWriterPro

writer = ContentWriterPro()

# Product description
description = writer.write_product_description(
    product_name="Smart Translator",
    features=["Multi-language", "Context-aware", "Terminology preservation"],
    target_audience="Global businesses"
)

# Value proposition
value_prop = writer.write_value_proposition(
    product="SEO Optimizer",
    benefit="Rank higher in search results",
    differentiator="AI-powered analysis"
)
```

### Social Media Content / 社交媒体内容

```python
# LinkedIn post
linkedin_post = writer.create_social_post(
    platform="linkedin",
    topic="Remote work productivity",
    tone="professional",
    length="medium"
)

# Twitter thread
tweets = writer.create_twitter_thread(
    topic="Startup lessons",
    num_tweets=5
)
```

### Ad Copy / 广告文案

```python
# Google Ads style
ad = writer.write_ad_copy(
    product="Project Management Tool",
    headline_options=3,
    description_options=2
)

# Facebook ad
fb_ad = writer.write_facebook_ad(
    product="Online Course",
    hook="Learn in 30 days",
    cta="Enroll now"
)
```

## API Reference / API 参考

### ContentWriterPro Class

```python
class ContentWriterPro:
    """Main class for content generation."""
    
    def generate_marketing_copy(self, product, audience, tone="professional"):
        """Generate marketing copy."""
        pass
    
    def create_social_post(self, platform, topic, tone="casual", length="short"):
        """Create social media post."""
        pass
    
    def write_ad_copy(self, product, headline_options=3, description_options=2):
        """Write advertising copy."""
        pass
    
    def write_brand_story(self, company_name, origin_story, values):
        """Write brand story content."""
        pass
    
    def write_email(self, email_type, purpose, tone="professional"):
        """Write email content."""
        pass
```

## Configuration / 配置

```python
# Custom configuration
config = {
    'default_tone': 'professional',
    'max_length': 500,
    'language': 'zh-CN'
}

writer = ContentWriterPro(config=config)
```

## Running Tests / 运行测试

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_writer.py -v

# Run with coverage
python -m pytest tests/ --cov=content_writer --cov-report=html
```

## License / 许可证

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。
