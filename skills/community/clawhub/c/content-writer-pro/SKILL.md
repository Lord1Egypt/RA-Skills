# Content Writer Pro / 文案生成专家

## Metadata / 元数据

| Field | Value |
|-------|-------|
| **name** | content-writer-pro |
| **homepage** | https://clawhub.com/skills/content-writer-pro |
| **description** | 专业文案生成工具 - 支持营销文案、社媒内容、广告文案、品牌故事等多种场景 | Professional copywriting generator for marketing, social media, ads, brand storytelling |
| **category** | content |
| **tags** | content, copywriting, marketing, generator, 文案, 营销, 内容创作 |

## Overview / 概述

Content Writer Pro is a professional copywriting tool for marketers and content creators. It provides templates and AI-powered generation for various content types.

文案生成专家是为营销人员和内容创作者打造的专业文案工具，提供多种内容类型的模板和AI生成能力。

## Features / 功能特性

- **Marketing Copy** / 营销文案: Product descriptions, value propositions
- **Social Media** / 社媒内容: Posts for various platforms
- **Ad Copy** / 广告文案: Headlines, body copy, CTAs
- **Brand Story** / 品牌故事: Origin stories, mission statements
- **Email Templates** / 邮件模板: Newsletters, promotional emails
- **Tone Adaptation** / 语调适配: Professional, casual, playful, etc.

## Installation / 安装

```bash
pip install -r requirements.txt
```

## Quick Start / 快速开始

```python
from content_writer import ContentWriterPro

writer = ContentWriterPro()

# Generate marketing copy
copy = writer.generate_marketing_copy(
    product="AI Assistant",
    audience="Small business owners",
    tone="professional"
)

# Create social media post
post = writer.create_social_post(
    platform="linkedin",
    topic="Productivity tips",
    tone="casual"
)
```

## API Reference / API 参考

See `content_writer.py` for full API documentation.

## License / 许可证

MIT License
