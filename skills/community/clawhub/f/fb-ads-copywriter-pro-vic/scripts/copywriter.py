#!/usr/bin/env python3
"""
Copywriter - AI 营销文案生成器
生成高转化率的广告文案、社交媒体内容、邮件营销内容
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# 尝试导入 OpenAI 兼容客户端（用于 Qwen 等模型）
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


# 文案模板库
TEMPLATES = {
    "ad": {
        "facebook": """
生成一个 Facebook 广告文案，要求：
- 产品/服务：{product}
- 语气风格：{tone}
- 目标受众：{audience}
- 包含：吸引人的标题、正文、行动号召 (CTA)
- 适当使用 emoji（3-5 个）
- 长度：标题<40 字，正文<125 字

输出 JSON 格式：
{{
  "headline": "标题",
  "body": "正文",
  "cta": "行动号召",
  "hashtags": ["标签 1", "标签 2"]
}}
""",
        "google": """
生成一个 Google 搜索广告文案，要求：
- 产品/服务：{product}
- 语气风格：{tone}
- 包含：3 个标题（各<30 字）、2 个描述（各<90 字）
- 突出卖点和差异化

输出 JSON 格式：
{{
  "headlines": ["标题 1", "标题 2", "标题 3"],
  "descriptions": ["描述 1", "描述 2"]
}}
""",
        "tiktok": """
生成一个抖音/TikTok 广告文案，要求：
- 产品/服务：{product}
- 语气风格：{tone}
- 目标受众：{audience}
- 包含：视频开头 hook、主体内容、行动号召
- 使用流行语和 emoji
- 长度：<60 字

输出 JSON 格式：
{{
  "hook": "开头吸引语",
  "body": "主体内容",
  "cta": "行动号召",
  "hashtags": ["#标签 1", "#标签 2"]
}}
"""
    },
    "social": {
        "xiaohongshu": """
生成一个小红书种草文案，要求：
- 主题：{topic}
- 语气风格：{tone}
- 目标受众：{audience}
- 包含：吸引人的标题、详细内容、互动引导
- 使用 emoji 和分隔线
- 长度：300-500 字
- 结尾添加 5-8 个相关标签

输出 JSON 格式：
{{
  "title": "标题",
  "content": "正文内容",
  "hashtags": ["#标签 1", "#标签 2"]
}}
""",
        "weibo": """
生成一个微博文案，要求：
- 主题：{topic}
- 语气风格：{tone}
- 包含：正文、话题标签、互动引导
- 长度：<140 字
- 使用热门话题格式

输出 JSON 格式：
{{
  "content": "正文内容",
  "topics": ["#话题 1#", "#话题 2#"],
  "cta": "互动引导"
}}
""",
        "twitter": """
生成一个 Twitter/X 推文，要求：
- 主题：{topic}
- 语气风格：{tone}
- 包含：正文、hashtags
- 长度：<280 字符
- 可以有 thread 提示

输出 JSON 格式：
{{
  "content": "推文内容",
  "hashtags": ["#tag1", "#tag2"],
  "thread": false
}}
"""
    },
    "email": {
        "promotion": """
生成一个促销邮件，要求：
- 产品/活动：{product}
- 语气风格：{tone}
- 包含：主题行、问候语、正文、行动号召、结尾
- 创造紧迫感（限时优惠等）
- 长度：200-400 字

输出 JSON 格式：
{{
  "subject": "邮件主题",
  "greeting": "问候语",
  "body": "正文",
  "cta": "行动号召",
  "closing": "结尾"
}}
""",
        "newsletter": """
生成一个新闻通讯邮件，要求：
- 主题：{topic}
- 语气风格：{tone}
- 包含：主题行、开场、主要内容、行动号召
- 长度：300-500 字

输出 JSON 格式：
{{
  "subject": "邮件主题",
  "opening": "开场白",
  "content": "主要内容",
  "cta": "行动号召"
}}
"""
    },
    "product": {
        "ecommerce": """
生成一个电商产品描述，要求：
- 产品：{product}
- 语气风格：{tone}
- 目标受众：{audience}
- 包含：吸引人的标题、产品亮点、详细参数、使用场景
- 突出卖点和差异化
- 长度：300-500 字

输出 JSON 格式：
{{
  "title": "产品标题",
  "highlights": ["亮点 1", "亮点 2", "亮点 3"],
  "description": "详细描述",
  "specs": "规格参数",
  "usage": "使用场景"
}}
"""
    }
}


def get_prompt(template_type: str, platform: str, **kwargs) -> str:
    """获取文案生成提示词"""
    try:
        template = TEMPLATES[template_type][platform]
    except KeyError:
        # 使用默认模板
        template = TEMPLATES[template_type].get("facebook", TEMPLATES["ad"]["facebook"])
    
    # 填充默认值
    defaults = {
        "product": kwargs.get("product", "产品"),
        "topic": kwargs.get("topic", "主题"),
        "tone": kwargs.get("tone", "professional"),
        "audience": kwargs.get("audience", "一般受众"),
        "purpose": kwargs.get("purpose", "推广")
    }
    
    return template.format(**defaults)


def generate_copy(type_: str, platform: str, variations: int = 1, **kwargs) -> dict:
    """生成文案"""
    results = []
    
    for i in range(variations):
        prompt = get_prompt(type_, platform, **kwargs)
        
        # 模拟生成（实际使用时调用 API）
        # 这里返回示例输出
        result = {
            "variation": i + 1,
            "prompt": prompt,
            "status": "ready_for_api"
        }
        results.append(result)
    
    return {
        "type": type_,
        "platform": platform,
        "variations": variations,
        "results": results,
        "metadata": {
            "generatedAt": datetime.now().isoformat(),
            "model": "qwen3.5-plus",
            "version": "0.1.0"
        }
    }


def main():
    parser = argparse.ArgumentParser(description="AI 营销文案生成器")
    parser.add_argument("command", choices=["generate", "test"], help="命令")
    parser.add_argument("--type", "-t", required=True, 
                       choices=["ad", "social", "email", "product", "landing", "blog", "video"],
                       help="文案类型")
    parser.add_argument("--platform", "-p", default="facebook",
                       help="目标平台")
    parser.add_argument("--product", help="产品/服务名称")
    parser.add_argument("--topic", help="内容主题")
    parser.add_argument("--tone", default="professional",
                       choices=["professional", "casual", "persuasive", "humorous", "urgent", "friendly", "luxury"],
                       help="语气风格")
    parser.add_argument("--audience", default="一般受众", help="目标受众")
    parser.add_argument("--variations", "-n", type=int, default=1, help="生成变体数量")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="json", help="输出格式")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        result = generate_copy(
            type_=args.type,
            platform=args.platform,
            variations=args.variations,
            product=args.product,
            topic=args.topic,
            tone=args.tone,
            audience=args.audience
        )
        
        if args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"文案类型：{args.type}")
            print(f"平台：{args.platform}")
            print(f"变体数量：{args.variations}")
            print("-" * 50)
            for v in result["results"]:
                print(f"\n【变体 {v['variation']}】")
                print(v["prompt"][:200] + "...")
    
    elif args.command == "test":
        # 测试模式
        print("Copywriter 营销文案生成器 v0.1.0")
        print("测试运行成功！")
        print(f"支持类型：{list(TEMPLATES.keys())}")


if __name__ == "__main__":
    main()
