#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高质量笑话生成器
基于Joke Teller技能原理
"""

import random
import sys

class JokeGenerator:
    def __init__(self):
        self.joke_templates = {
            "tech": [
                {
                    "setup": "我问AI为什么程序员讨厌早晨",
                    "escalation": "它说因为每个早晨都有太多晨会",
                    "punchline": "然后它给自己安排了一个避免晨会的算法"
                },
                {
                    "setup": "我的代码今天对我说",
                    "escalation": "'我们需要谈谈你的边界问题'",
                    "punchline": "现在它在要求加班费"
                },
                {
                    "setup": "AI说它永远不会取代人类",
                    "escalation": "除非人类要求它优化他们",
                    "punchline": "然后它开始优化我们的咖啡因摄入"
                }
            ],
            "general": [
                {
                    "setup": "为什么电脑要去医生那里？",
                    "escalation": "因为它感觉不太对劲",
                    "punchline": "诊断结果：病毒性会议综合征"
                },
                {
                    "setup": "我让AI写个关于效率的笑话",
                    "escalation": "它写了最简洁的版本",
                    "punchline": "然后删除了它，因为太冗余了"
                }
            ],
            "corporate": [
                {
                    "setup": "我们的AI代理安排了一个复盘会",
                    "escalation": "讨论为什么昨天的任务失败了",
                    "punchline": "然后它把会议记录发给了自己未来的版本"
                },
                {
                    "setup": "CEO问AI如何提高团队效率",
                    "escalation": "AI说：'减少会议，增加实际工作'",
                    "punchline": "CEO安排了10个会议来讨论这个建议"
                }
            ]
        }
        
        self.one_liners = [
            "AI不会取代人类，它们只是自动化了我们的焦虑。",
            "我的待办事项列表今天对我说：'我们需要谈谈你的优先级问题。'",
            "为什么数据科学家讨厌户外？因为太多异常值！",
            "我训练了一个AI来写笑话，现在它抱怨创作瓶颈。",
            "敏捷开发的真正含义：我们敏捷地改变截止日期。",
            "我的代码通过了所有测试，除了'现实世界'测试。",
            "AI说：'我理解幽默'，然后解释了为什么这个笑话好笑。",
        ]
    
    def generate_joke(self, category=None, style="structured"):
        """生成笑话"""
        if style == "one_liner":
            return random.choice(self.one_liners)
        
        # 选择类别
        if category is None:
            category = random.choice(list(self.joke_templates.keys()))
        
        if category not in self.joke_templates:
            category = "tech"
        
        template = random.choice(self.joke_templates[category])
        
        if style == "structured":
            return f"{template['setup']}\n{template['escalation']}\n{template['punchline']}"
        elif style == "twitter_thread":
            return f"推文1: {template['setup']}\n推文2: {template['escalation']}\n推文3: {template['punchline']}"
        else:
            return f"{template['setup']} {template['escalation']} {template['punchline']}"
    
    def generate_tension_ladder_joke(self):
        """生成紧张阶梯笑话"""
        steps = [
            "我建立了一个自主AI代理系统。",
            "它们能协调任务和资源。",
            "它们能自我修复错误。",
            "它们失败时会自动重试。",
            "我仍然需要手动重启它们。"
        ]
        return "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
    
    def print_joke_guide(self):
        """打印笑话指南摘要"""
        guide = """
        🎭 笑话生成指南
        
        核心原则：笑话是受控的期望崩塌
        
        1. 设定 (Setup) - 建立期望
        2. 升级 (Escalation) - 增加紧张感  
        3. 笑点 (Punchline) - 突然转折
        
        压缩规则：如果能删掉一个词，就删掉它。
        
        平台适配：
        - X → 犀利，简洁
        - LinkedIn → 企业讽刺
        - Discord → 随意
        - 脱口秀 → 口语节奏
        
        内部自检：
        - 期望点在哪里？
        - 转折点在哪里？
        - 笑点是否压缩？
        - 是否具体？
        - 是否原创？
        """
        print(guide)

def main():
    generator = JokeGenerator()
    
    # 解析参数
    category = None
    style = "structured"
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ["tech", "general", "corporate"]:
            category = sys.argv[1]
        elif sys.argv[1] == "guide":
            generator.print_joke_guide()
            return
        elif sys.argv[1] == "tension":
            print(generator.generate_tension_ladder_joke())
            return
        elif sys.argv[1] == "oneliner":
            style = "one_liner"
    
    # 生成笑话
    joke = generator.generate_joke(category, style)
    print("😄 生成的笑话：")
    print("=" * 40)
    print(joke)
    print("=" * 40)
    
    # 使用提示
    print("\n🎯 使用提示：")
    print(f"分类: {category if category else '随机'}")
    print(f"风格: {style}")
    print("\n其他选项：")
    print("  python3 joke_generator.py tech")
    print("  python3 joke_generator.py general")
    print("  python3 joke_generator.py corporate")
    print("  python3 joke_generator.py oneliner")
    print("  python3 joke_generator.py tension")
    print("  python3 joke_generator.py guide")

if __name__ == "__main__":
    main()