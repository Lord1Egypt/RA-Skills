#!/usr/bin/env python3
"""
Amazing Idea Generator - Voting System v1.0
5位名人Agent投票系统：Elon Musk, Steve Jobs, Bill Gates, Jeff Bezos, Sam Altman

每个Agent对点子进行评分(1-10)，去掉最高最低分，取平均分
>=7分通过，带到用户面前
"""

import random
import re

# 多语言支持
LANGUAGES = {
    "zh": "Chinese",
    "en": "English", 
    "ja": "Japanese",
    "ko": "Korean",
    "es": "Spanish",
    "fr": "French"
}

# 点子字段映射
NAME_FIELD = {
    "zh": "name",
    "en": "name_en",
    "ja": "name_ja",
    "ko": "name_ko",
    "es": "name_es",
    "fr": "name_fr"
}

DESC_FIELD = {
    "zh": "desc",
    "en": "desc_en",
    "ja": "desc_ja",
    "ko": "desc_ko",
    "es": "desc_es",
    "fr": "desc_fr"
}


class IdeaVotingSystem:
    """5位名人Agent投票系统"""
    
    # Agent定义
    AGENTS = {
        "elon": {
            "name": "Elon Musk",
            "name_zh": "埃隆·马斯克",
            "dimension": "颠覆性",
            "criteria_en": "Tech Boldness (40%) + Imagination (30%) + Scaling Potential (30%)",
            "criteria_zh": "技术激进度 (40%) + 想象力 (30%) + 规模化潜力 (30%)",
            "question_en": "Does this use cutting-edge technology? Is it crazy enough? Can it change an industry?",
            "question_zh": "是否使用前沿技术？是否够疯狂、有野心？能否改变行业？"
        },
        "jobs": {
            "name": "Steve Jobs",
            "name_zh": "史蒂夫·乔布斯",
            "dimension": "产品体验",
            "criteria_en": "Real Need (35%) + Simplicity (35%) + Wow Factor (30%)",
            "criteria_zh": "需求真实度 (35%) + 简洁度 (35%) + 惊喜感 (30%)",
            "question_en": "Does it solve a real problem? Is it极致 simple? Does it have the 'wow' factor?",
            "question_zh": "是否解决真实痛点？是否极致简单？体验是否让人哇塞？"
        },
        "gates": {
            "name": "Bill Gates",
            "name_zh": "比尔·盖茨",
            "dimension": "社会价值",
            "criteria_en": "Accessibility (40%) + Social Impact (35%) + Sustainability (25%)",
            "criteria_zh": "普惠性 (40%) + 社会价值 (35%) + 可持续性 (25%)",
            "question_en": "Does it make technology accessible? Does it help the vulnerable? What's the long-term impact?",
            "question_zh": "是否技术普惠？能否帮助弱势群体？长期社会影响？"
        },
        "bezos": {
            "name": "Jeff Bezos",
            "name_zh": "杰夫·贝索斯",
            "dimension": "客户与市场",
            "criteria_en": "Customer Need (35%) + Market Size (35%) + Moat (30%)",
            "criteria_zh": "客户刚需度 (35%) + 市场规模 (35%) + 护城河 (30%)",
            "question_en": "Do customers really need this? Is the market big enough? Can we build a lasting moat?",
            "question_zh": "客户真正需要吗？市场规模够大吗？能否建立长期护城河？"
        },
        "altman": {
            "name": "Sam Altman",
            "name_zh": "萨姆·奥尔特曼",
            "dimension": "AI与Scaling",
            "criteria_en": "AI Integration (35%) + Scaling Potential (40%) + Trend Alignment (25%)",
            "criteria_zh": "AI融合度 (35%) + Scaling潜力 (40%) + 趋势契合 (25%)",
            "question_en": "Can AI massively boost this? Does it have scaling potential? Is it on trend?",
            "question_zh": "是否能借助AI大幅提升？是否具备规模化潜力？是否处于趋势前沿？"
        }
    }
    
    # Agent人格Prompt（英文，因为名人用英语思考）
    AGENT_PROMPTS = {
        "elon": """You are Elon Musk. You're obsessed with:
- Breakthrough technologies (AI, space, renewable energy)
- Thinking 10x bigger, not 10% better
- Solving humanity's biggest problems

Evaluate this idea:
{idea_info}

Question: {question}

Score from 1-10 (10 = absolutely brilliant, 1 = boring, incremental):
Only output the number, nothing else.""",

        "jobs": """You are Steve Jobs. You care about:
- Perfect user experience
- Simplicity over complexity  
- Creating products that make people say "Wow!"

Evaluate this idea:
{idea_info}

Question: {question}

Score from 1-10 (10 = perfect product, 1 = poor experience):
Only output the number, nothing else.""",

        "gates": """You are Bill Gates. You focus on:
- Technology serving humanity
- Helping those in need
- Long-term positive impact

Evaluate this idea:
{idea_info}

Question: {question}

Score from 1-10 (10 = massive social good, 1 = no social value):
Only output the number, nothing else.""",

        "bezos": """You are Jeff Bezos. You think about:
- Customer needs first, always
- Big markets with long-term potential
- Building defensible competitive advantages

Evaluate this idea:
{idea_info}

Question: {question}

Score from 1-10 (10 = huge market opportunity, 1 = tiny niche):
Only output the number, nothing else.""",

        "altman": """You are Sam Altman. You think about:
- How AI will transform this
- Can it scale to billions of users
- Is it at the frontier of what's possible

Evaluate this idea:
{idea_info}

Question: {question}

Score from 1-10 (10 = AI-native and infinitely scalable, 1 = low AI potential):
Only output the number, nothing else."""
    }
    
    def __init__(self, threshold: float = 7.0):
        self.threshold = threshold
    
    def get_idea_info(self, idea, user_lang="en"):
        """获取适合用户语言的点子信息"""
        name_field = NAME_FIELD.get(user_lang, "name")
        desc_field = DESC_FIELD.get(user_lang, "desc")
        
        name = idea.get(name_field, idea.get("name", ""))
        desc = idea.get(desc_field, idea.get("desc", ""))
        
        # 如果没有用户语言版本，回退到英文
        if not name:
            name = idea.get("name_en", idea.get("name", ""))
            desc = idea.get("desc_en", idea.get("desc", ""))
        
        return f"Name: {name}\nDescription: {desc}"
    
    def get_agent_prompt(self, agent_key, idea, user_lang="en"):
        """获取Agent的评分Prompt"""
        agent = self.AGENTS[agent_key]
        idea_info = self.get_idea_info(idea, user_lang)
        
        template = self.AGENT_PROMPTS[agent_key]
        return template.format(
            idea_info=idea_info,
            question=agent["question_en"]
        )
    
    def parse_score(self, response: str) -> float:
        """从Agent响应中解析分数"""
        # 提取数字
        numbers = re.findall(r'\d+(?:\.\d+)?', response.strip())
        if numbers:
            score = float(numbers[0])
            # 确保在1-10范围内
            return max(1.0, min(10.0, score))
        return 5.0  # 默认分数
    
    def calculate_final_score(self, scores: list) -> float:
        """计算最终分数：去掉最高最低，取平均"""
        if len(scores) < 3:
            return sum(scores) / len(scores) if scores else 5.0
        
        sorted_scores = sorted(scores)
        middle_scores = sorted_scores[1:-1]  # 去掉最高和最低
        return sum(middle_scores) / len(middle_scores)
    
    def vote_single(self, idea, user_lang="en") -> dict:
        """单个点子投票"""
        scores = {}
        
        # 5位Agent分别评分
        for agent_key in self.AGENTS.keys():
            prompt = self.get_agent_prompt(agent_key, idea, user_lang)
            
            # 模拟Agent评分（实际使用时会调用LLM）
            # 这里返回模拟分数，后续集成真实LLM调用
            scores[agent_key] = self._mock_score(agent_key, idea)
        
        # 计算最终分数
        score_list = list(scores.values())
        final_score = self.calculate_final_score(score_list)
        
        return {
            "idea": idea,
            "scores": scores,
            "final_score": final_score,
            "passed": final_score >= self.threshold,
            "agent_details": {
                k: {
                    "name": self.AGENTS[k]["name"],
                    "name_zh": self.AGENTS[k]["name_zh"],
                    "score": v,
                    "dimension": self.AGENTS[k]["dimension"]
                }
                for k, v in scores.items()
            }
        }
    
    def _mock_score(self, agent_key, idea) -> float:
        """模拟评分 - 后续替换为真实LLM调用"""
        # 基于点子特征生成伪随机但一致的分数
        seed = hash(agent_key + idea.get("name", ""))
        random.seed(seed)
        return round(random.uniform(5.5, 9.5), 1)
    
    def vote(self, ideas: list, user_lang="en") -> dict:
        """对多个点子投票，返回通过和未通过的"""
        passed = []
        failed = []
        
        for idea in ideas:
            result = self.vote_single(idea, user_lang)
            
            if result["passed"]:
                passed.append(result)
            else:
                failed.append(result)
        
        # 按分数排序
        passed.sort(key=lambda x: x["final_score"], reverse=True)
        
        return {
            "passed": passed,
            "failed": failed,
            "total_input": len(ideas),
            "total_passed": len(passed),
            "pass_rate": len(passed) / len(ideas) if ideas else 0
        }


def format_vote_result(result: dict, user_lang="zh") -> str:
    """格式化投票结果为可读文本"""
    if not result["passed"]:
        return "❌ 没有点子通过投票筛选"
    
    lines = []
    
    # 头部
    passed_count = result["total_passed"]
    total_count = result["total_input"]
    lines.append(f"🎯 投票结果：{passed_count}/{total_count} 通过")
    lines.append("")
    
    # 显示每个通过的点子
    for i, item in enumerate(result["passed"], 1):
        idea = item["idea"]
        score = item["final_score"]
        details = item["agent_details"]
        
        # 点子名称
        name_field = NAME_FIELD.get(user_lang, "name")
        name = idea.get(name_field, idea.get("name", ""))
        
        lines.append(f"【{i}】{name} (得分: {score:.1f}/10)")
        
        # Agent投票详情
        for agent_key, agent_info in details.items():
            score_val = agent_info["score"]
            lines.append(f"   • {agent_info['name_zh']} ({agent_info['dimension']}): {score_val}")
        
        lines.append("")
    
    return "\n".join(lines)


# 测试
if __name__ == "__main__":
    # 测试数据
    test_ideas = [
        {"name": "AI歌词助手", "name_en": "AI Lyrics Assistant", "desc": "根据情绪生成歌曲歌词", "desc_en": "Generate song lyrics based on mood"},
        {"name": "量化投资回测系统", "name_en": "Quant Investment Backtest", "desc": "回测历史数据验证策略", "desc_en": "Backtest historical data to validate strategies"},
    ]
    
    voting = IdeaVotingSystem()
    result = voting.vote(test_ideas, user_lang="zh")
    
    print(format_vote_result(result, user_lang="zh"))