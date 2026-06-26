#!/usr/bin/env python3
"""
AI Prompt Generator
AI 提示词生成器
为不同AI模型生成优化的提示词
"""

import sys
import json

def generate_prompt(category, topic, style="concise", audience="general", length="medium"):
    """生成AI提示词"""
    
    templates = {
        "writing": {
            "creative": "创作{topic}的{length}内容，风格{style}，面向{audience}受众。要求原创、有创意、引人入胜。",
            "technical": "撰写关于{topic}的技术文档，风格{style}，面向{audience}受众。要求准确、清晰、专业。",
            "business": "撰写{topic}的商业分析报告，风格{style}，面向{audience}受众。要求数据驱动、逻辑清晰、实用。"
        },
        "coding": {
            "algorithm": "用Python实现{topic}算法，要求代码{style}、可读性强、包含注释和测试用例。",
            "web": "开发{topic}网页应用，使用现代技术栈，代码{style}，面向{audience}开发者。",
            "data": "分析{topic}数据集，使用Python进行数据清洗、可视化和建模，方法{style}。"
        },
        "marketing": {
            "seo": "为{topic}制定SEO优化策略，包括关键词研究、内容优化、外链建设，策略{style}。",
            "social": "策划{topic}的社交媒体营销活动，面向{audience}受众，内容{style}。",
            "email": "设计{topic}的邮件营销活动，包括主题行、内容、CTA，转化率{style}。"
        },
        "design": {
            "logo": "设计{topic}的logo，风格{style}，适合{audience}受众，包含设计理念说明。",
            "ui": "设计{topic}的用户界面，用户体验{style}，面向{audience}用户。",
            "brand": "制定{topic}的品牌设计指南，包括色彩、字体、视觉风格，整体{style}。"
        },
        "research": {
            "market": "研究{topic}市场趋势，包括竞争分析、用户画像、机会点，报告{style}。",
            "technical": "调研{topic}技术方案，比较优缺点、适用场景、实施难度，分析{style}。",
            "academic": "撰写{topic}学术综述，引用权威文献，论证{style}，面向{audience}。"
        },
        "analysis": {
            "financial": "分析{topic}财务数据，包括趋势、比率、预测，方法{style}，面向{audience}。",
            "business": "进行{topic}业务分析，识别问题、机会、改进方案，建议{style}。",
            "data": "分析{topic}数据集，发现模式、洞察、异常，可视化{style}。"
        }
    }
    
    if category not in templates:
        return None
    
    if style == "creative":
        style_desc = "富有创意"
    elif style == "technical":
        style_desc = "技术性强"
    elif style == "concise":
        style_desc = "简洁明了"
    elif style == "detailed":
        style_desc = "详细全面"
    else:
        style_desc = style
    
    if length == "short":
        length_desc = "简短"
    elif length == "medium":
        length_desc = "中等长度"
    elif length == "long":
        length_desc = "长篇"
    else:
        length_desc = length
    
    # 选择模板
    if "creative" in templates[category]:
        template = templates[category]["creative"]
    elif "technical" in templates[category]:
        template = templates[category]["technical"]
    else:
        template = list(templates[category].values())[0]
    
    prompt = template.format(
        topic=topic,
        style=style_desc,
        audience=audience,
        length=length_desc
    )
    
    return prompt

def generate_chatgpt_prompt(role, task, context="", constraints=""):
    """生成ChatGPT专用提示词"""
    prompt = f"""你是一个{role}，需要完成以下任务：

任务：{task}

"""
    
    if context:
        prompt += f"背景信息：{context}\n\n"
    
    if constraints:
        prompt += f"约束条件：{constraints}\n\n"
    
    prompt += "请根据以上信息，提供专业、准确、有用的回答。"
    
    return prompt

def generate_midjourney_prompt(subject, style, mood, quality="high"):
    """生成Midjourney绘画提示词"""
    
    styles = {
        "realistic": "photorealistic, realistic, 8k, ultra detailed",
        "artistic": "artistic, creative, imaginative, masterpiece",
        "cartoon": "cartoon style, animated, cute, colorful",
        "minimalist": "minimalist, simple, clean, elegant",
        "vintage": "vintage, retro, nostalgic, old-fashioned",
        "futuristic": "futuristic, sci-fi, cyberpunk, advanced"
    }
    
    qualities = {
        "high": "high quality, sharp focus, intricate details",
        "medium": "good quality, clear, well-defined",
        "low": "basic quality, simple, rough"
    }
    
    style_desc = styles.get(style, style)
    quality_desc = qualities.get(quality, quality)
    
    prompt = f"{subject}, {style_desc}, {mood}, {quality_desc}"
    
    return prompt

def generate_code_prompt(language, task, difficulty="intermediate"):
    """生成代码生成提示词"""
    
    difficulties = {
        "beginner": "初学者友好，代码简单易懂，包含详细注释",
        "intermediate": "中级难度，代码结构良好，包含测试用例",
        "advanced": "高级难度，代码优化，包含错误处理和性能考虑"
    }
    
    difficulty_desc = difficulties.get(difficulty, difficulty)
    
    prompt = f"""用{language}语言实现{task}功能。
要求：
- {difficulty_desc}
- 代码可读性强
- 遵循最佳实践
- 包含必要的注释
"""
    
    return prompt

def analyze_prompt(prompt):
    """分析提示词质量"""
    score = 0
    feedback = []
    
    if len(prompt) > 50:
        score += 1
    else:
        feedback.append("提示词太短，需要更详细的描述")
    
    if "要求" in prompt or "需求" in prompt or "目标" in prompt:
        score += 1
    else:
        feedback.append("建议明确说明要求和目标")
    
    if "背景" in prompt or "context" in prompt.lower():
        score += 1
    else:
        feedback.append("可以添加背景信息帮助理解")
    
    if "约束" in prompt or "限制" in prompt or "constraint" in prompt.lower():
        score += 1
    else:
        feedback.append("考虑添加约束条件")
    
    if score >= 3:
        rating = "优秀"
    elif score >= 2:
        rating = "良好"
    elif score >= 1:
        rating = "一般"
    else:
        rating = "需要改进"
    
    return {
        "score": score,
        "rating": rating,
        "feedback": feedback
    }

def main():
    if len(sys.argv) < 2:
        print("用法: ai-prompt-gen <command> [args]")
        print("")
        print("命令:")
        print("  ai-prompt-gen general <类别> <主题> [风格] [受众] [长度]  通用提示词")
        print("  ai-prompt-gen chatgpt <角色> <任务> [背景] [约束]      ChatGPT提示词")
        print("  ai-prompt-gen midjourney <主体> <风格> <氛围> [质量]  绘画提示词")
        print("  ai-prompt-gen code <语言> <任务> [难度]                代码提示词")
        print("  ai-prompt-gen analyze <提示词>                        分析提示词")
        print("  ai-prompt-gen list                                     列出模板")
        print("")
        print("类别: writing, coding, marketing, design, research, analysis")
        print("风格: concise, creative, technical, detailed")
        print("长度: short, medium, long")
        print("难度: beginner, intermediate, advanced")
        print("")
        print("示例:")
        print("  ai-prompt-gen general writing '人工智能' creative general long")
        print("  ai-prompt-gen chatgpt '专业作家' '写一篇关于AI的文章' '背景信息' '字数500字'")
        print("  ai-prompt-gen midjourney '未来城市' 'futuristic' '科技感' 'high'")
        print("  ai-prompt-gen code 'Python' '排序算法' 'intermediate'")
        print("  ai-prompt-gen analyze '写一个关于AI的文章'")
        return 1

    command = sys.argv[1]

    if command == "general":
        if len(sys.argv) < 4:
            print("错误: 请提供类别和主题")
            return 1
        
        category = sys.argv[2]
        topic = sys.argv[3]
        style = sys.argv[4] if len(sys.argv) > 4 else "concise"
        audience = sys.argv[5] if len(sys.argv) > 5 else "general"
        length = sys.argv[6] if len(sys.argv) > 6 else "medium"
        
        prompt = generate_prompt(category, topic, style, audience, length)
        
        if prompt is None:
            print(f"错误: 不支持的类别 '{category}'")
            return 1
        
        print(f"\n🎯 AI提示词生成")
        print(f"类别: {category}")
        print(f"主题: {topic}")
        print(f"风格: {style}")
        print(f"受众: {audience}")
        print(f"长度: {length}")
        print(f"\n📝 生成的提示词:")
        print(f"{prompt}")
        print()

    elif command == "chatgpt":
        if len(sys.argv) < 4:
            print("错误: 请提供角色和任务")
            return 1
        
        role = sys.argv[2]
        task = sys.argv[3]
        context = sys.argv[4] if len(sys.argv) > 4 else ""
        constraints = sys.argv[5] if len(sys.argv) > 5 else ""
        
        prompt = generate_chatgpt_prompt(role, task, context, constraints)
        
        print(f"\n🤖 ChatGPT提示词")
        print(f"角色: {role}")
        print(f"任务: {task}")
        if context:
            print(f"背景: {context}")
        if constraints:
            print(f"约束: {constraints}")
        print(f"\n📝 生成的提示词:")
        print(f"{prompt}")
        print()

    elif command == "midjourney":
        if len(sys.argv) < 5:
            print("错误: 请提供主体、风格和氛围")
            return 1
        
        subject = sys.argv[2]
        style = sys.argv[3]
        mood = sys.argv[4]
        quality = sys.argv[5] if len(sys.argv) > 5 else "high"
        
        prompt = generate_midjourney_prompt(subject, style, mood, quality)
        
        print(f"\n🎨 Midjourney绘画提示词")
        print(f"主体: {subject}")
        print(f"风格: {style}")
        print(f"氛围: {mood}")
        print(f"质量: {quality}")
        print(f"\n📝 生成的提示词:")
        print(f"{prompt}")
        print()

    elif command == "code":
        if len(sys.argv) < 4:
            print("错误: 请提供语言和任务")
            return 1
        
        language = sys.argv[2]
        task = sys.argv[3]
        difficulty = sys.argv[4] if len(sys.argv) > 4 else "intermediate"
        
        prompt = generate_code_prompt(language, task, difficulty)
        
        print(f"\n💻 代码生成提示词")
        print(f"语言: {language}")
        print(f"任务: {task}")
        print(f"难度: {difficulty}")
        print(f"\n📝 生成的提示词:")
        print(f"{prompt}")
        print()

    elif command == "analyze":
        if len(sys.argv) < 3:
            print("错误: 请提供要分析的提示词")
            return 1
        
        prompt = sys.argv[2]
        result = analyze_prompt(prompt)
        
        print(f"\n🔍 提示词分析")
        print(f"提示词: {prompt}")
        print(f"\n📊 评分: {result['score']}/4 ({result['rating']})")
        
        if result['feedback']:
            print(f"\n💡 改进建议:")
            for feedback in result['feedback']:
                print(f"  - {feedback}")
        print()

    elif command == "list":
        print("\n📋 可用模板")
        print(f"\n写作 (writing):")
        print(f"  - 创意写作: 创作引人入胜的原创内容")
        print(f"  - 技术写作: 撰写专业、准确的技术文档")
        print(f"  - 商业写作: 编写数据驱动的商业报告")
        
        print(f"\n编程 (coding):")
        print(f"  - 算法实现: 用指定语言实现算法")
        print(f"  - 网页开发: 开发现代网页应用")
        print(f"  - 数据分析: 进行数据清洗和可视化")
        
        print(f"\n营销 (marketing):")
        print(f"  - SEO优化: 制定搜索引擎优化策略")
        print(f"  - 社交媒体: 策划社媒营销活动")
        print(f"  - 邮件营销: 设计邮件营销活动")
        
        print(f"\n设计 (design):")
        print(f"  - Logo设计: 创作品牌标识")
        print(f"  - UI设计: 设计用户界面")
        print(f"  - 品牌设计: 制定品牌设计指南")
        
        print(f"\n研究 (research):")
        print(f"  - 市场研究: 分析市场趋势和竞争")
        print(f"  - 技术研究: 调研技术方案")
        print(f"  - 学术研究: 撰写学术综述")
        
        print(f"\n分析 (analysis):")
        print(f"  - 财务分析: 分析财务数据和趋势")
        print(f"  - 业务分析: 进行业务诊断")
        print(f"  - 数据分析: 发现数据洞察")
        print()

    else:
        print(f"未知命令: {command}")
        print("使用 'ai-prompt-gen' 查看帮助")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
