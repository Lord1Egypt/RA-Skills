"""Daily Decision Helper - 日常决策助手"""
import json
import re
from typing import List

def parse_decision(text: str) -> dict:
    return {"question": text.strip(), "type": None}

def categorize_decision(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["买", "购物", "选哪个", "性价比"]): return "消费选择"
    if any(k in t for k in ["工作", "跳槽", "辞职", "offer"]): return "职业发展"
    if any(k in t for k in ["孩子", "上学", "培训班", "教育"]): return "教育决策"
    if any(k in t for k in ["搬家", "买房", "换房", "定居"]): return "居住决策"
    return "一般决策"

def pros_cons_list(question: str) -> dict:
    return {
        "question": question,
        "pros": ["请列出你认为选择A的主要好处（至少3条）"],
        "cons": ["请列出你认为选择A的主要代价/风险（至少3条）"],
        "alternatives": ["还有没有第3种选择？"],
        "weighted_factors": [
            {"factor": "经济成本", "weight": "高/中/低"},
            {"factor": "时间成本", "weight": "高/中/低"},
            {"factor": "情绪影响", "weight": "高/中/低"},
            {"factor": "长期影响", "weight": "高/中/低"}
        ]
    }

def six_months_test(question: str) -> str:
    return f"问自己：6个月后回头看，这个决定还重要吗？如果不重要，说明现在过度担忧了。如果重要，6个月后你会后悔吗？"

def handle(text: str) -> dict:
    parsed = parse_decision(text)
    dtype = categorize_decision(text)
    pc = pros_cons_list(parsed["question"])
    return {
        "decisionType": dtype,
        "question": parsed["question"],
        "prosConsFramework": pc,
        "decisionTools": {
            "sixMonthsTest": six_months_test(parsed["question"]),
            "worseFirst": "先想象最坏结果，然后问自己：我能接受吗？能接受就去做，不能接受就调整方案。",
            "reversed": "想象你选了B（反向选项），6个月后你会怎么想？"
        },
        "recommendedProcess": [
            "第一步：清晰描述你要做的决定（不是你的担忧）",
            "第二步：用利弊清单结构化分析（让ChatGPT帮你写）",
            "第三步：做加法（列出所有好处）+ 做减法（列出所有风险）",
            "第四步：问6个月后测试",
            "第五步：做出选择，然后全力执行"
        ]
    }

if __name__ == "__main__":
    for tc in ["要不要给孩子报那个思维课，5800一学期", "现在工作还可以，但有个新机会要去面试，跳槽"]:
        r = handle(tc)
        print(f"Input: {tc}\n  -> 类型: {r['decisionType']}\n  -> 第一步: {r['recommendedProcess'][0]}\n  -> 6个月测试: {r['decisionTools']['sixMonthsTest'][:30]}...\n")
