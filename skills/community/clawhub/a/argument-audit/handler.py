#!/usr/bin/env python3
"""Argument Audit Handler - 论点审计核心模块"""
import json
import sys
import re

# ===== 逻辑谬误库 =====

FALLACIES = {
    "ad_hominem": {
        "name": "人身攻击 (Ad Hominem)",
        "description": "攻击提出论点的人而非论点本身",
        "example": "你说得不对因为你是个坏人"
    },
    "straw_man": {
        "name": "稻草人谬误 (Straw Man)",
        "description": "歪曲或夸大对方观点再加以反驳",
        "example": "对方说应该控烟，你说对方要禁所有工业"
    },
    "false_dilemma": {
        "name": "虚假二分法 (False Dilemma)",
        "description": "只给出两个极端选项，忽略中间可能",
        "example": "要么支持我，要么支持敌人"
    },
    "slippery_slope": {
        "name": "滑坡谬误 (Slippery Slope)",
        "description": "假设一个小步骤必然导致极端后果",
        "example": "如果允许同性恋结婚，就会导致人兽婚姻合法化"
    },
    "circular_reasoning": {
        "name": "循环论证 (Circular Reasoning)",
        "description": "用论点本身来支持论点",
        "example": "这本书是经典因为它很经典"
    },
    "appeal_to_authority": {
        "name": "诉诸权威 (Appeal to Authority)",
        "description": "仅以权威身份而非证据支持论点",
        "example": "某明星说这个产品好所以真的好"
    },
    "appeal_to_emotion": {
        "name": "诉诸情感 (Appeal to Emotion)",
        "description": "用情感而非逻辑来论证",
        "example": "想想那些受苦的孩子，你应该支持这个政策"
    },
    "hasty_generalization": {
        "name": "草率概括 (Hasty Generalization)",
        "description": "以少量案例得出普遍结论",
        "example": "我遇到的东北人都很豪爽，所以东北人都豪爽"
    },
    "post_hoc": {
        "name": "事后归因 (Post Hoc Ergo Propter Hoc)",
        "description": "仅凭时间先后认定因果",
        "example": "公鸡叫后天亮了，所以是公鸡叫醒了太阳"
    },
    "red_herring": {
        "name": "转移话题 (Red Herring)",
        "description": "引入无关话题转移注意力",
        "example": "讨论是否应该加薪时说'公司还很困难'"
    },
    "bandwagon": {
        "name": "从众谬误 (Bandwagon)",
        "description": "以多数人意见为正确依据",
        "example": "大家都这么做，所以是对的"
    },
    "tu_quoque": {
        "name": "你也一样 (Tu Quoque)",
        "description": "以对方的类似行为反驳论点",
        "example": "你自己也这么做，凭什么说我"
    },
    "no_true_scotsman": {
        "name": "特殊抗辩 (No True Scotsman)",
        "description": "以定义排除反例来保护论点",
        "example": "真正的基督徒不会这样做，所以这个人不是真正的基督徒"
    }
}

def detect_fallacies(text):
    """检测文本中的逻辑谬误"""
    detected = []
    text_lower = text.lower()
    sentences = re.split(r'[。！？\n]', text)
    
    # 人身攻击
    ad_hominem_kws = ["你这种人", "你当然", "你懂什么", "你算什么东西", "不读书", "脑残", "蠢货", "人渣", "弱智"]
    if any(kw in text_lower for kw in ad_hominem_kws):
        detected.append("ad_hominem")
    
    # 稻草人
    if any(kw in text_lower for kw in ["你的意思是", "你说要", "你主张", "你认为"]) and \
       any(kw in text_lower for kw in ["就等于是", "就是要", "就是", "就是说"]):
        detected.append("straw_man")
    
    # 虚假二分法（增强：需要有"要么"或"只能二选一"类结构）
    false_dilemma_kws = ["要么", "不然就", "二选一", "只能", "不是...就是", "没有中间路线"]
    if any(kw in text_lower for kw in false_dilemma_kws):
        detected.append("false_dilemma")
    
    # 滑坡（增强）
    slippery_kws_first = ["一旦", "如果允许", "如果", "一旦", "从"]
    slippery_kws_second = ["必然导致", "最终会", "最后必然", "最终必然", "必将", "无可挽回", "一发不可收拾", "就会导致"]
    if any(kw1 in text_lower for kw1 in slippery_kws_first):
        for kw2 in slippery_kws_second:
            if kw2 in text_lower:
                detected.append("slippery_slope")
                break
    
    # 循环论证
    for s in sentences:
        s_stripped = s.strip()
        if len(s_stripped) > 5:
            words = re.findall(r'[\u4e00-\u9fa5a-zA-Z]+', s_stripped)
            if len(words) >= 3:
                if words[0] == words[-1]:
                    if "circular_reasoning" not in detected:
                        detected.append("circular_reasoning")
                        break
                # 重复关键词出现多次
                if len(words) > 0:
                    first_word = words[0]
                    # 出现3次以上则可能是循环
                    if sum(1 for w in words if w == first_word) >= 3 and len(set(words)) <= 3:
                        if "circular_reasoning" not in detected:
                            detected.append("circular_reasoning")
                            break
    
    # 诉诸权威（增强：支持机构、奖项、头衔、审批机构）
    authority_kws = ["专家", "权威", "教授", "科学家", "FDA", "WHO", "NMPA", "药监局", 
                      "审批", "批准", "推荐", "代言", "名人", "明星", "网红"]
    evidence_kws = ["数据", "研究", "统计", "证明", "实验", "临床试验", "双盲", "随机对照",
                    "表明", "显示", "显示", "证实", "发现"]
    has_authority = any(kw in text_lower for kw in authority_kws)
    has_evidence = any(kw in text_lower for kw in evidence_kws)
    # 如果提到权威/审批/推荐但没有具体数据支撑，则为诉诸权威
    if has_authority and not has_evidence:
        # 特例：如果明确说"研究表明...专家说"则不算
        if "说" in text_lower and "研究" in text_lower:
            pass  # 暂时不判
        else:
            detected.append("appeal_to_authority")
    
    # 诉诸情感（增强）
    emotion_kws = ["可怜", "悲惨", "令人心痛", "触目惊心", "无法想象", "难道你忍心",
                    "可悲", "令人惋惜", "令人愤怒", "多么可怕", "孩子的未来",
                    "老人的眼泪", "无辜的", "心痛", "无法接受", "不能容忍"]
    if any(kw in text_lower for kw in emotion_kws):
        detected.append("appeal_to_emotion")
    
    # 草率概括（增强）
    universal_kws = ["所有", "全部", "没有一个", "都是", "从不", "永远", "一切", "毫无例外",
                      "必然", "100%", "毫无例外", "无一例外", "没有一个"]
    if any(kw in text_lower for kw in universal_kws):
        detected.append("hasty_generalization")
    
    # 事后归因
    if any(kw in text_lower for kw in ["之后", "然后", "后来"]) and \
       any(kw in text_lower for kw in ["于是", "所以", "导致", "造成"]):
        detected.append("post_hoc")
    
    # 从众谬误
    if any(kw in text_lower for kw in ["大家都", "所有人", "人们都", "大家都知道", "众所周知", "都认为", "都在"]):
        detected.append("bandwagon")
    
    # 转移话题
    if any(kw in text_lower for kw in ["说到底", "其实", "不过", "重点是", "关键是", "问题是"]):
        # 排除明确在展开论述的情况
        if len(text_lower) < 200 or "综上所述" in text_lower:
            detected.append("red_herring")
    
    # Tu quoque
    tu_quoque_kws = ["你也", "你自己", "你也一样", "你不也", "你之前也", "你自己还不是"]
    if any(kw in text_lower for kw in tu_quoque_kws):
        detected.append("tu_quoque")
    
    return list(dict.fromkeys(detected))  # 去重保持顺序

def rate_strength(clarity, validity, soundness, completeness, fallacy_count):
    """综合评分"""
    base = (clarity + validity + soundness + completeness) / 4
    penalty = min(fallacy_count * 1.5, 4)
    overall = max(1, min(10, base - penalty))
    return round(overall, 1)

def parse_arguments(text):
    """解析论点结构"""
    arguments = []
    sentences = re.split(r'[。！？\n]', text)
    for s in sentences:
        s = s.strip()
        if len(s) < 5:
            continue
        # 检测结论词
        conclusion_markers = ["应该", "必须", "不应该", "不能", "可以", "是对的", "是错的", "是正确的", "是错误的", "所以", "因此", "可见", "总之", "故", "合理", "不合理", "有效", "无效"]
        if any(m in s for m in conclusion_markers):
            arguments.append({"type": "claim", "content": s})
        elif any(m in s for m in ["认为", "指出", "提出", "说", "观点", "论点"]):
            arguments.append({"type": "premise", "content": s})
    return arguments[:10]

def analyze_structure(text):
    """分析论点结构"""
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    structure = []
    for s in sentences:
        if any(kw in s for kw in ["因为", "由于", "首先", "其次"]):
            structure.append({"type": "premise", "content": s})
        elif any(kw in s for kw in ["所以", "因此", "结论", "综上所述"]):
            structure.append({"type": "conclusion", "content": s})
        else:
            structure.append({"type": "claim", "content": s})
    return structure

def handle(topic, user_input, history=None, args=None):
    """处理论点审计请求"""
    if not user_input or not user_input.strip():
        return {"status": "error", "message": "请提供需要审计的论点内容"}
    
    user_input = user_input.strip()
    topic = (topic or "").strip()
    
    fallacies_found_ids = detect_fallacies(user_input)
    fallacies_found = []
    for fid in fallacies_found_ids:
        if fid in FALLACIES:
            fallacies_found.append({
                "type": fid,
                "name": FALLACIES[fid]["name"],
                "description": FALLACIES[fid]["description"],
                "example": FALLACIES[fid]["example"]
            })
    
    arguments = parse_arguments(user_input)
    structure = analyze_structure(user_input)
    
    # 评分
    has_conclusion = "所以" in user_input or "因此" in user_input or "应该" in user_input or "必须" in user_input
    has_evidence = any(kw in user_input.lower() for kw in ["因为", "数据", "研究", "统计", "显示", "表明", "根据", "来源"])
    has_example = any(kw in user_input.lower() for kw in ["例如", "比如", "比如", "案例", "实例", "事实", "例子"])
    
    clarity = 5.0 if len(user_input) > 20 else 4.0
    validity = 7.0 if has_conclusion else 5.0
    soundness = 6.5 if has_evidence else 4.5
    completeness = 6.0 if has_example else 4.5
    
    overall = rate_strength(clarity, validity, soundness, completeness, len(fallacies_found))
    
    # 建议
    recommendations = []
    if len(fallacies_found) > 0:
        recommendations.append(f"⚠️ 检测到 {len(fallacies_found)} 种逻辑谬误，建议逐一检视")
    else:
        recommendations.append("✅ 未检测到常见逻辑谬误")
    
    if not has_evidence:
        recommendations.append("📌 论据支撑不足，建议补充数据、研究或具体案例")
    if not has_conclusion:
        recommendations.append("📌 缺少明确结论或论点，建议开篇亮明核心观点")
    if not has_example:
        recommendations.append("📌 建议增加具体案例或实例以增强说服力")
    if len(user_input) < 50:
        recommendations.append("📌 论点内容较短，建议展开论述以便全面评估")
    
    return {
        "status": "success",
        "argument_count": len(arguments) or 1,
        "structure": structure,
        "scores": {
            "clarity": clarity,
            "validity": validity,
            "soundness": soundness,
            "completeness": completeness,
            "overall": overall
        },
        "fallacy_count": len(fallacies_found),
        "fallacy_details": fallacies_found,
        "arguments": arguments,
        "recommendations": recommendations,
        "audit_summary": f"论点{'较弱' if overall < 6 else '中等' if overall < 7.5 else '较强'}，综合得分 {overall}/10"
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = handle(None, user_input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Usage: python handler.py '<论点内容>'")
        print("Example: python handler.py '人工智能会取代所有工作，所以不应该发展AI。'")
