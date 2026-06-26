#!/usr/bin/env python3
"""
AI 文案生成器
用途：一键生成爆款营销文案，支持多平台
"""

import os
import json
from openclaw import OpenClaw

class CopywritingGenerator:
    """文案生成器"""
    
    PLATFORMS = {
        "xiaohongshu": {
            "tone": "种草风，真诚分享",
            "style": "emoji + 短段落 + 情感共鸣",
            "keywords": ["绝了", "真的", "姐妹们", "yyds", "必入"]
        },
        "douyin": {
            "tone": "快节奏，抓眼球",
            "style": "前3秒吸睛 + 痛点 + 解决方案 + CTA",
            "keywords": ["必看", "教程", "技巧", "干货", "分享"]
        },
        "wechat": {
            "tone": "朋友圈风格，自然",
            "style": "简洁 + 个人体验 + 推荐",
            "keywords": ["推荐", "好用", "值得", "买了"]
        },
        "ecommerce": {
            "tone": "专业营销，突出卖点",
            "style": "标题 + 卖点 + 信任背书 + CTA",
            "keywords": ["优惠", "限时", "热销", "推荐"]
        }
    }
    
    def __init__(self, model="deepseek-chat"):
        self.model = model
        self.api_key = os.getenv("OPENCLAW_API_KEY")
        if not self.api_key:
            raise ValueError("请设置环境变量 OPENCLAW_API_KEY")
    
    def generate(self, platform, product, features, target, length=200):
        """生成文案"""
        platform_info = self.PLATFORMS.get(platform, self.PLATFORMS["wechat"])
        
        prompt = f"""你是专业的营销文案专家，擅长{platform}平台文案。

平台特点：
- 语气：{platform_info['tone']}
- 风格：{platform_info['style']}
- 爆款关键词：{', '.join(platform_info['keywords'])}

产品信息：
- 产品名称：{product}
- 核心卖点：{', '.join(features)}
- 目标用户：{target}

请生成一篇{length}字的{platform}营销文案，要求：
1. 符合平台调性
2. 包含爆款关键词
3. 突出产品卖点
4. 有明确行动呼吁（CTA）

直接输出文案内容，不要解释。"""

        client = OpenClaw(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=800
        )
        
        return response.choices[0].message.content
    
    def optimize_title(self, title, platform="xiaohongshu"):
        """优化标题，提高点击率"""
        prompt = f"""优化以下标题，使其更适合{platform}平台，点击率更高：
原标题：{title}

要求：
1. 简洁有力（15字以内）
2. 包含数字/疑问/利益点
3. 使用热门关键词

输出5个优化版本。"""

        client = OpenClaw(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    
    def get_hot_keywords(self, category="美妆"):
        """获取热门关键词"""
        keywords_map = {
            "美妆": ["绝美", "显白", "高级感", "平价", "大牌平替"],
            "数码": ["神器", "黑科技", "高颜值", "性价比", "必备"],
            "家居": ["ins风", "提升幸福感", "收纳神器", "高颜值", "好用"],
            "穿搭": ["显瘦", "高级感", "韩系", "日系", "ins风"],
            "美食": ["好吃到哭", "绝绝子", "必吃", "宝藏", "yyds"]
        }
        return keywords_map.get(category, [])

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI 文案生成器")
    parser.add_argument("--platform", default="xiaohongshu", help="平台")
    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument("--features", required=True, help="卖点（逗号分隔）")
    parser.add_argument("--target", required=True, help="目标用户")
    parser.add_argument("--length", type=int, default=200, help="文案长度")
    args = parser.parse_args()
    
    gen = CopywritingGenerator()
    features = args.features.split(",")
    
    print(f"\n📱 平台：{args.platform}")
    print(f"🛍️ 产品：{args.product}")
    print(f"✨ 卖点：{', '.join(features)}")
    print(f"👥 目标：{args.target}")
    print("-" * 50)
    
    copy = gen.generate(args.platform, args.product, features, args.target, args.length)
    print(f"📝 生成的文案：\n\n{copy}")
    print("\n" + "-" * 50)
    
    # 优化标题
    print("\n💡 标题优化建议：")
    titles = gen.optimize_title(args.product, args.platform)
    print(titles)

if __name__ == "__main__":
    main()