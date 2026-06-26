"""Family Conflict Mediator - 家庭冲突调解员"""
import json
import re

def parse_conflict(text: str) -> dict:
    parties = []
    if any(k in text for k in ["夫妻", "老婆", "老公", "伴侣"]): parties.append("伴侣")
    if any(k in text for k in ["孩子", "儿子", "女儿", "亲子"]): parties.append("子女")
    if any(k in text for k in ["父母", "婆婆", "岳母", "公婆"]): parties.append("长辈")
    parties = parties or ["家庭成员"]
    return {"parties": parties, "raw_text": text[:100]}

def assess_conflict_level(text: str) -> str:
    if any(k in text for k in ["大打出手", "暴力", "报警", "砸东西"]): return "high"
    if any(k in text for k in ["冷战", "分房", "离婚", "不过了"]): return "medium-high"
    if any(k in text for k in ["争吵", "生气", "矛盾", "冲突"]): return "medium"
    return "low"

def generate_mediation_steps(parties: list, level: str) -> dict:
    steps = [
        {"phase": "暂停", "duration": "等24-48小时", "action": "双方暂停直接对话，给情绪冷静时间"},
        {"phase": "降温", "duration": "冷静期", "action": "各自写下：对方让我不舒服的具体行为 + 我的感受"},
        {"phase": "复盘", "duration": "冷静后", "action": "用我感到XX当你说/做XX时格式沟通，避免指责"},
        {"phase": "约定", "duration": "对话后", "action": "明确双方都能接受的解决方案，写下来"},
    ]
    if level == "high":
        steps.insert(0, {"phase": "安全第一", "duration": "立即", "action": "如有身体暴力风险，优先保证人身安全，必要时联系外部帮助"})
    return {"steps": steps, "mediation_principle": "调解的目标不是分对错，而是找到双方都能接受的共存方式"}

def handle(text: str) -> dict:
    parsed = parse_conflict(text)
    level = assess_conflict_level(text)
    mediation = generate_mediation_steps(parsed["parties"], level)
    return {
        "detectedParties": parsed["parties"],
        "conflictLevel": level,
        "mediationSteps": mediation["steps"],
        "principle": mediation["mediation_principle"],
        "crisisResources": {
            "报警": "110",
            "心理援助": "全国心理援助热线：400-161-9995",
            "家暴热线": "12338（妇联热线）"
        } if level in ["high", "medium-high"] else {}
    }

if __name__ == "__main__":
    for tc in ["和老婆冷战3天了怎么办", "和青春期孩子大吵了一架"]:
        r = handle(tc)
        print(f"Input: {tc}\n  -> 当事人: {r['detectedParties']} | 等级: {r['conflictLevel']}\n  -> 第一步: {r['mediationSteps'][0]['action']}\n")
