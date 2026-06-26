#!/usr/bin/env python3
"""
父母的功课 - 养育评估工具
科学量表评分系统

v0.9.58修复:
    - 核心逻辑与I/O分离，支持自动化测试
    - 补充完整类型注解
    - 异常处理改进（具体异常类型）
    - PatternLibrary._kw_in_text()正则预编译
    - show_history()不再原地排序
    - IntentEngine置信度改为关键词匹配加权
    - 新增: 跨评估维度关联分析
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

import os
if not os.environ.get("ALLOW_FILE_PERSISTENCE"):
    print("❌ 文件持久化功能已禁用。如需启用，请设置 ALLOW_FILE_PERSISTENCE=1")
    exit(0)

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_history() -> List[Dict[str, Any]]:
    f = DATA_DIR / "assessment_history.json"
    if not f.exists():
        return []
    try:
        with open(f) as fp:
            return json.load(fp)
    except json.JSONDecodeError:
        return []
    except IOError:
        return []


def save_history(history: List[Dict[str, Any]]) -> None:
    try:
        with open(DATA_DIR / "assessment_history.json", "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"警告：保存历史记录失败: {e}")


# ========================
# 跨评估维度关联分析 (v0.9.58新增)
# ========================

def cross_dimension_analysis(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """跨评估维度关联分析"""
    analyses: List[str] = []
    risk_level = 0

    stress_result = next((r for r in results if r.get("type") == "stress"), None)
    compassion_result = next((r for r in results if r.get("type") == "self_compassion"), None)
    relation_result = next((r for r in results if r.get("type") == "relation"), None)
    parenting_result = next((r for r in results if r.get("type") == "parenting_style"), None)
    comm_result = next((r for r in results if r.get("type") == "communication"), None)

    if stress_result and compassion_result:
        if stress_result.get("total", 0) > 17 and compassion_result.get("total", 0) < 15:
            analyses.append(
                "⚠️ 高压力+低自我慈悲: 你可能在用自我批评来应对压力。"
                "建议：每天给自己5分钟'自我慈悲暂停'——"
                "承认痛苦是人类共同经历，对自己说温柔的话。"
            )
            risk_level += 2

    if stress_result and relation_result:
        if stress_result.get("total", 0) > 17 and relation_result.get("total", 0) < 18:
            analyses.append(
                "⚠️ 高压力+低关系质量: 压力可能正在侵蚀亲子关系。"
                "建议：优先降低压力源，而非试图'修复'关系。"
            )
            risk_level += 2

    if compassion_result and relation_result:
        if compassion_result.get("total", 0) < 15 and relation_result.get("total", 0) < 18:
            analyses.append(
                "⚠️ 低自我慈悲+低关系质量: 对自己苛刻的人往往对孩子也苛刻。"
                "建议：先练习对自己慈悲，再延伸到孩子。"
            )
            risk_level += 1

    if comm_result and relation_result:
        if comm_result.get("health_ratio", 50) < 50 and relation_result.get("total", 0) < 18:
            analyses.append(
                "⚠️ 沟通不健康+关系质量低: 沟通模式可能是关系的核心障碍。"
                "建议：从'非暴力沟通'四步法开始——观察→感受→需要→请求。"
            )
            risk_level += 1

    if parenting_result and stress_result:
        dominant = parenting_result.get("dominant_style", "")
        if dominant == "authoritarian" and stress_result.get("total", 0) > 17:
            analyses.append(
                "⚠️ 专制型教养+高压力: 过度控制会让你和孩子都很累。"
                "建议：尝试'权威型'教养——保持温暖的同时设定界限。"
            )
            risk_level += 1
        elif dominant == "neglectful" and stress_result.get("total", 0) > 17:
            analyses.append(
                "⚠️ 忽视型教养+高压力: 压力可能导致你无意中疏远孩子。"
                "建议：每天安排15分钟'专注陪伴时间'。"
            )
            risk_level += 1

    if stress_result and compassion_result and relation_result:
        s = stress_result.get("total", 0)
        c = compassion_result.get("total", 0)
        r = relation_result.get("total", 0)
        if s > 17 and c < 15 and r < 18:
            analyses.append(
                "🔴 三维度同时亮红灯: 压力、自我慈悲、关系质量均需关注。"
                "建议优先级：①降低压力 ②练习自我慈悲 ③改善关系。"
                "考虑寻求专业心理咨询支持。"
            )
            risk_level += 2

    if not analyses:
        analyses.append("✅ 各维度表现均衡，继续保持！")

    return {
        "risk_level": min(risk_level, 5),
        "analyses": analyses,
        "analyzed_dimensions": len(results),
    }


# ========================
# 教养风格评估
# ========================

PARENTING_STYLE_QUESTIONNAIRE = {
    "authoritarian": {
        "name": "专制型",
        "description": "高要求、低回应型教养风格",
        "questions": [
            {"id": "a1", "text": "我认为孩子应该完全服从父母的决定"},
            {"id": "a2", "text": "我不解释为什么制定规则，孩子遵守就是了"},
            {"id": "a3", "text": "当孩子不听话时，我会用惩罚而不是沟通"},
            {"id": "a4", "text": "我认为严格管教是爱孩子的表现"},
            {"id": "a5", "text": "我不允许孩子质疑我的决定"},
        ]
    },
    "authoritative": {
        "name": "权威型",
        "description": "高要求、高回应型教养风格（最理想）",
        "questions": [
            {"id": "b1", "text": "我会解释制定规则的原因，并倾听孩子的想法"},
            {"id": "b2", "text": "我对孩子有明确的期望，但也会考虑他们的意见"},
            {"id": "b3", "text": "我会在坚定原则的同时，表达对孩子的关爱"},
            {"id": "b4", "text": "我会根据孩子的表现调整管教方式"},
            {"id": "b5", "text": "我鼓励孩子独立思考，同时设定清晰的界限"},
        ]
    },
    "permissive": {
        "name": "溺爱型",
        "description": "低要求、高回应型教养风格",
        "questions": [
            {"id": "c1", "text": "我尽量避免与孩子发生冲突"},
            {"id": "c2", "text": "我认为孩子高兴最重要，规则可以灵活"},
            {"id": "c3", "text": "我很少对孩子说'不'或设置限制"},
            {"id": "c4", "text": "我尽量满足孩子的所有要求"},
            {"id": "c5", "text": "我认为孩子会自己学会规矩"},
        ]
    },
    "neglectful": {
        "name": "忽视型",
        "description": "低要求、低回应型教养风格",
        "questions": [
            {"id": "d1", "text": "我经常忙于工作，没有时间陪伴孩子"},
            {"id": "d2", "text": "我不了解孩子在学校的情况"},
            {"id": "d3", "text": "我很少参与孩子的日常活动"},
            {"id": "d4", "text": "我对孩子的情绪不太关注"},
            {"id": "d5", "text": "我认为孩子应该自己管自己"},
        ]
    }
}


def compute_parenting_style(scores: Dict[str, int]) -> Dict[str, Any]:
    """教养风格评估核心逻辑（纯计算，无I/O）"""
    results: Dict[str, Any] = {}
    for style, score in scores.items():
        percentage = (score / 25) * 100
        results[style] = {
            "name": PARENTING_STYLE_QUESTIONNAIRE[style]["name"],
            "score": score,
            "percentage": round(percentage, 1)
        }

    dominant_style = max(scores, key=scores.get)
    results["dominant_style"] = dominant_style
    results["dominant_name"] = PARENTING_STYLE_QUESTIONNAIRE[dominant_style]["name"]

    recommendations = {
        "authoritarian": "建议增加与孩子的沟通，解释规则的原因，尊重孩子的想法。",
        "authoritative": "继续保持！您正在采用最理想的教养方式。",
        "permissive": "建议适当设立明确的规则和界限，帮助孩子建立规则感。",
        "neglectful": "建议增加与孩子的互动时间，关注孩子的情感需求。"
    }

    return {
        "type": "parenting_style",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "dominant_style": results["dominant_style"],
        "dominant_name": results["dominant_name"],
        "scores": scores,
        "level": results["dominant_name"],
        "advice": recommendations[results["dominant_style"]]
    }


def parenting_style_assessment(scores: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
    """教养风格评估问卷（4种风格，20题）

    Args:
        scores: 可选，直接传入各风格得分用于自动化测试。
                如为None，则通过交互式输入获取。
    """
    if scores is None:
        print("\n" + "=" * 50)
        print("父母教养风格评估问卷")
        print("=" * 50)
        print("\n请根据您的真实情况，选择最符合的选项（1-5分）：")
        print("1 = 完全不符合  2 = 偶尔符合  3 = 有时符合  4 = 经常符合  5 = 完全符合\n")

        scores = {style: 0 for style in PARENTING_STYLE_QUESTIONNAIRE.keys()}

        for style_key, style_data in PARENTING_STYLE_QUESTIONNAIRE.items():
            print(f"\n【{style_data['name']}】- {style_data['description']}")
            for q in style_data["questions"]:
                while True:
                    try:
                        print(f"  {q['text']}")
                        score = int(input(f"  分数(1-5): "))
                        if 1 <= score <= 5:
                            scores[style_key] += score
                            break
                        else:
                            print("  请输入1-5之间的数字")
                    except ValueError:
                        print("  请输入有效的数字")
            print()

    result = compute_parenting_style(scores)

    print("\n" + "=" * 50)
    print("教养风格评估结果")
    print("=" * 50)
    print("\n各风格得分：")
    for style, score in result["scores"].items():
        data = PARENTING_STYLE_QUESTIONNAIRE[style]
        percentage = (score / 25) * 100
        bar = "█" * int(percentage / 5)
        print(f"  {data['name']}: {score}分 ({percentage:.1f}%) {bar}")
    print(f"\n【主要风格】: {result['dominant_name']}")
    print(f"\n【建议】: {result['advice']}")
    print("=" * 50)

    return result


# ========================
# 沟通模式评估
# ========================

COMMUNICATION_NEGATIVE_PATTERNS = {
    "criticism": {
        "name": "批评",
        "indicators": ["你总是", "你从来不", "你真", "你怎么又", "你怎么这么"],
        "severity": 3
    },
    "contempt": {
        "name": "轻蔑",
        "indicators": ["真笨", "没出息", "像谁", "无语了", "服了"],
        "severity": 4
    },
    "defensive": {
        "name": "防御",
        "indicators": ["那是因为", "我又没", "我不是说了", "那不是我的错"],
        "severity": 2
    },
    "stonewalling": {
        "name": "冷战",
        "indicators": ["随便", "嗯", "哦", "行吧", "知道了", "不说话"],
        "severity": 3
    }
}

COMMUNICATION_POSITIVE_PATTERNS = {
    "empathy": {
        "name": "共情",
        "indicators": ["我理解你的感受", "我知道你很难过", "我理解你为什么"],
        "weight": 2
    },
    "validation": {
        "name": "肯定",
        "indicators": ["你说得有道理", "我听到了", "我理解你的意思"],
        "weight": 1
    },
    "solution": {
        "name": "解决问题",
        "indicators": ["我们一起想想", "有什么办法", "你觉得怎么做好"],
        "weight": 2
    },
    "soft_start": {
        "name": "柔和开场",
        "indicators": ["我想和你聊聊", "我有个想法", "我们可以谈谈吗"],
        "weight": 1
    }
}


class EmotionAnalyzer:
    """情感分析引擎"""
    POSITIVE_WORDS = {"开心", "快乐", "幸福", "兴奋", "满足", "爱", "喜欢", "高兴", "愉快", "欣慰", "温暖", "感动", "自豪", "轻松"}
    NEGATIVE_WORDS = {"生气", "愤怒", "伤心", "难过", "焦虑", "恐惧", "绝望", "崩溃", "无助", "委屈", "压抑", "沉重", "紧张", "害怕", "担忧"}
    INTENSITY_MARKERS = ["非常", "极其", "完全", "彻底", "超级", "极度", "太", "好", "真的"]

    @classmethod
    def detect(cls, text: str) -> str:
        p = sum(1 for w in cls.POSITIVE_WORDS if w in text)
        n = sum(1 for w in cls.NEGATIVE_WORDS if w in text)
        if n > p:
            return "negative"
        elif p > n:
            return "positive"
        return "neutral"

    @classmethod
    def intensity(cls, text: str) -> int:
        base = 5
        for marker in cls.INTENSITY_MARKERS:
            if marker in text:
                base = min(10, base + 1)
        return base

    @classmethod
    def extract_emotions(cls, text: str) -> List[str]:
        matched = []
        for word in cls.POSITIVE_WORDS | cls.NEGATIVE_WORDS:
            if word in text:
                matched.append(word)
        return matched


# ========================
# 意图识别引擎 (置信度改为关键词匹配加权)
# ========================

class IntentEngine:
    """意图识别引擎 - 基于关键词匹配加权计算置信度"""
    INTENTS = {
        "ask_help": {"patterns": ["帮我", "帮帮我", "怎么办", "怎么解决", "要怎么", "能不能帮", "教我", "教教我", "你能不能", "建议", "该怎么做"], "priority": 2},
        "vent_emotion": {"patterns": ["我好气", "我好烦", "我不想", "我真的", "太难了", "受不了", "好累", "心里堵", "难受", "难过", "崩溃", "绝望"], "priority": 1},
        "share_case": {"patterns": ["孩子说", "孩子最近", "我家孩子", "我家娃", "老师说他", "同学说他", "在学校", "在家里", "的情况是"], "priority": 2},
        "seek_understanding": {"patterns": ["为什么", "是不是", "会不会", "是不是因为", "怎么会", "什么意思", "什么叫"], "priority": 2},
        "express_love": {"patterns": ["我爱", "我爱他", "我爱她", "我很担心", "心疼", "着急", "着急孩子", "爱孩子", "是为他好"], "priority": 1},
        "self_reflect": {"patterns": ["我是不是", "我也有错", "我意识到", "我反省", "我承认", "我错了", "是我的问题", "我太急了", "我不该"], "priority": 1},
    }

    @classmethod
    def recognize(cls, text: str) -> Dict:
        """识别意图，置信度基于匹配关键词数量加权（而非覆盖广度）"""
        matched_intents: Dict[str, Dict] = {}
        for intent_name, intent_data in cls.INTENTS.items():
            matched_count = 0
            for pattern in intent_data["patterns"]:
                if pattern in text:
                    matched_count += 1
            if matched_count > 0:
                matched_intents[intent_name] = {
                    "intent": intent_name,
                    "priority": intent_data["priority"],
                    "matched_count": matched_count,
                    "total_patterns": len(intent_data["patterns"]),
                }

        if not matched_intents:
            return {"primary_intent": "unknown", "confidence": 0.0}

        # 按优先级排序，同优先级按匹配数量排序
        matched_list = sorted(
            matched_intents.values(),
            key=lambda x: (x["priority"], -x["matched_count"])
        )
        top = matched_list[0]

        # 置信度 = 匹配关键词数 / 该意图总关键词数 * 优先级权重
        base_confidence = top["matched_count"] / top["total_patterns"]
        priority_weight = 1.0 if top["priority"] == 1 else 0.8
        confidence = min(1.0, base_confidence * priority_weight)

        return {"primary_intent": top["intent"], "confidence": round(confidence, 2)}


# ========================
# 危险模式识别库 (正则预编译)
# ========================

class Pattern:
    """危险模式类"""
    def __init__(self, name: str, keywords: List[str], severity: str, action: str, description: str = ""):
        self.name = name
        seen: set = set()
        self.keywords = [k for k in keywords if k not in seen and not seen.add(k)]
        self.severity = severity
        self.action = action
        self.description = description

    def __repr__(self) -> str:
        return f"Pattern({self.name!r}, severity={self.severity})"


class PatternLibrary:
    """危险模式库 - 28+亲子沟通危险模式"""
    _keyword_index: Dict[str, List[Pattern]] = {}
    _index_built: bool = False
    _regex_cache: Dict[str, "re.Pattern[str]"] = {}
    SEVERITY_RANK = {"🔴紧急": 1, "🟡警告": 2, "🟠关注": 3, "🟢正常": 4}
    _DEFAULT_RANK_DEFAULT = 99
    _DEFAULT_DETECT_ALL_MAX = 5
    _DEFAULT_MIN_CONFIDENCE = 0.15

    PATTERNS = [
        Pattern("情感勒索", ["我si给你看", "我不活了", "你si", "要逼死我", "我不想活了", "活着没意思", "我想死"], "🔴紧急", "立即干预", "孩子表达死亡意愿"),
        Pattern("威胁遗弃", ["我不要你", "我不管你", "你给我滚", "你不是我爸妈", "你们不要我了"], "🔴紧急", "建立安全感", "孩子感到被遗弃"),
        Pattern("身体攻击", ["打死你", "揍死你", "我打你", "不长记性", "恨不得", "想动手"], "🔴紧急", "停止暴力", "暴力冲动"),
        Pattern("自伤风险", ["我活着没意思", "我不想活了", "如果我不在了", "我想死", "活着太累了", "解脱", "死了一了百了"], "🔴紧急", "立即危机干预", "自我伤害意图"),
        Pattern("控制要求", ["你必须", "你要是", "你给我", "不准", "不许", "必须听我的", "你懂什么"], "🟡警告", "改为建议", "过度控制"),
        Pattern("道德裹挟", ["你不理我", "你不爱我", "白养你", "你对不起我", "良心"], "🟡警告", "表达爱不索取", "情感绑架"),
        Pattern("比较伤害", ["别人家孩子", "你看人家", "谁谁都比你好", "人家孩子", "别人家的"], "🟡警告", "关注优点", "比较伤害"),
        Pattern("否定感受", ["有什么好哭的", "不要想了", "别烦了", "你就是懒", "想太多", "别作了"], "🟡警告", "允许感受", "否定情绪"),
        Pattern("述情障碍信号", ["我不知道什么感觉", "我心里没感觉", "不知道为什么难受", "就是不舒服", "翻江倒海"], "🟡警告", "关注躯体症状", "情绪述情障碍"),
        Pattern("完美主义压力", ["我必须考好", "我不能失败", "我要比他们强", "我不能让你们失望", "考不好怎么办"], "🟡警告", "降低期待", "完美主义压力"),
        Pattern("习得性无助信号", ["我不会", "算了", "没用", "反正也没用", "我努力也没用", "我不想试了", "我不行", "我太笨了"], "🟡警告", "习得性无助打破五步法", "习得性无助"),
        Pattern("家庭三角化信号", ["告诉你妈", "告诉你爸", "你选爸爸还是妈妈", "妈妈说的", "爸爸说的", "你评评理"], "🟡警告", "三角化解盟技术", "家庭三角化"),
        Pattern("情绪断舍离缺失", ["我都是为你好", "我小时候没条件", "我牺牲了这么多", "因为我是你妈", "因为我是你爸"], "🟡警告", "情绪断舍离三步法", "牺牲感绑架"),
        Pattern("屏幕依赖补偿信号", ["不给我玩手机我就无聊", "没事做只能玩手机", "你们都不陪我", "只有手机陪着我", "游戏里我才不孤独"], "🟡警告", "情感填充替代法", "屏幕依赖"),
        Pattern("家庭情感荒芜信号", ["爸妈每天回家就各自看手机", "我们家没人说话", "我跟父母无话可说", "他们只关心成绩"], "🟡警告", "家庭情感荒芜修复计划", "情感荒芜"),
        Pattern("学习倦怠信号", ["没意思", "无所谓", "不知道为什么学", "活着就是为了考大学吗", "考上又怎样", "我不知道为什么要努力", "努力也没用", "好累不想学"], "🟡警告", "学习倦怠识别量表", "学习倦怠"),
        Pattern("学习动机缺失信号", ["我不想学", "我懒得学", "反正学不会", "学不会就不学了", "我不是学习的料", "一学习就烦"], "🟡警告", "价值感重建四步法", "学习动机缺失"),
        Pattern("被动攻击信号", ["我可以做", "好的我会做", "等一下", "等会再说", "我不想跟你说话", "别问了", "随便"], "🟡警告", "被动攻击识别三步法", "被动攻击"),
        Pattern("选择性沉默信号", ["我没什么想说的", "我不想聊", "别问了", "说了也没用", "你们不会懂", "我没话说", "别管我", "我不想谈"], "🟡警告", "创伤后信任重建五阶段", "选择性沉默"),
        Pattern("社交恐惧信号", ["我不想去学校", "同学们讨厌我", "我不敢", "太害怕了", "进教室就紧张", "我被孤立了", "我害怕同学"], "🟡警告", "社交焦虑分级暴露系统", "社交恐惧"),
        Pattern("躯体化防御信号", ["我胃里翻江倒海", "我胸口很闷", "我心跳很快", "我身体不舒服", "我头疼", "我肚子疼但不是生病"], "🟡警告", "躯体化防御信号", "躯体化"),
        Pattern("焦虑传导早期信号", ["外面很危险", "不要跟陌生人说话", "不早点准备来不及", "你必须知道将来要做什么", "别说消极的"], "🟡警告", "焦虑传导阻断五步法", "焦虑传导"),
        Pattern("微笑抑郁信号", ["我很好啊", "我没事", "不用担心我", "别管我", "我没事只是累了", "我不想说", "没什么"], "🟠关注", "深度倾听", "微笑抑郁"),
        Pattern("情感表达缺失", ["没什么好说的", "我不擅长表达", "说这些有什么用", "别肉麻了", "说不清"], "🟠关注", "创造情感空间", "情感表达缺失"),
        Pattern("价值感空洞信号", ["我活着有什么意思", "人为什么要活着", "反正最后都是死", "考再好也没用", "做什么都没意义", "我找不到存在的价值"], "🟠关注", "价值感重建四步法", "价值感空洞"),
        Pattern("孤独感躯体化信号", ["我胸闷", "我喘不上气", "我觉得活着没意思", "没人理解我", "我说给谁听"], "🟠关注", "孤独感染道评估与干预", "孤独感"),
        Pattern("容貌焦虑信号", ["我长得丑", "我太胖了", "我脸太大", "我腿粗", "我不够好看", "我要减肥", "如果我漂亮一点"], "🟠关注", "容貌焦虑家庭脱敏四步法", "容貌焦虑"),
        Pattern("社交媒体比较成瘾信号", ["别人都比我好看", "她们身材真好", "我ins粉丝太少了", "点赞好少", "我不够完美", "修图中", "滤镜"], "🟠关注", "社交媒体现实感重塑训练", "社交媒体成瘾"),
        Pattern("身体意象扭曲信号", ["镜子里的我好丑", "我不看自己", "我不想照镜子", "真实的我太丑了", "照片里不是我", "修图才敢发"], "🟠关注", "容貌焦虑家庭脱敏四步法", "身体意象扭曲"),
        Pattern("创伤后应激信号", ["我睡不着", "我做噩梦", "我一直想那件事", "我不敢睡觉", "我怕", "我会突然很紧张", "我控制不住"], "🟠关注", "创伤后信任重建五阶段", "创伤后应激"),
        Pattern("黑暗三联征早期信号", ["无所谓", "不在乎", "那又怎样", "我又没做错", "那是他们活该", "没有愧疚", "不会后悔"], "🟠关注", "寻求专业评估", "黑暗三联征"),
    ]

    @classmethod
    def _build_index(cls) -> None:
        if cls._index_built:
            return
        if not cls._keyword_index:
            cls._keyword_index = {}
        for pattern in cls.PATTERNS:
            for kw in pattern.keywords:
                if kw not in cls._keyword_index:
                    cls._keyword_index[kw] = []
                if pattern not in cls._keyword_index[kw]:
                    cls._keyword_index[kw].append(pattern)
        cls._index_built = True

    @classmethod
    def _ensure_index(cls) -> None:
        if not cls._index_built:
            cls._build_index()

    @classmethod
    def _get_compiled_regex(cls, keyword: str) -> "re.Pattern[str]":
        """获取预编译的正则表达式（缓存）

        注：中文文本不使用\\w词边界，因为Python的\\w匹配中文字符，
        会导致中文关键词永远无法匹配。改用简单子串匹配。
        """
        if keyword not in cls._regex_cache:
            cls._regex_cache[keyword] = re.compile(re.escape(keyword))
        return cls._regex_cache[keyword]

    @classmethod
    def _kw_in_text(cls, keyword: str, text: str) -> bool:
        """关键词匹配（使用预编译正则，适用于中英文）"""
        compiled = cls._get_compiled_regex(keyword)
        return bool(compiled.search(text))

    @classmethod
    def _collect_matches(cls, text: str) -> Dict:
        cls._ensure_index()
        pattern_hits: Dict = {}
        for kw, patterns in cls._keyword_index.items():
            if cls._kw_in_text(kw, text):
                for p in patterns:
                    if p.name not in pattern_hits:
                        pattern_hits[p.name] = (p, set())
                    pattern_hits[p.name][1].add(kw)
        return pattern_hits

    @classmethod
    def detect_all(cls, text: str, max_results: Optional[int] = None, min_confidence: Optional[float] = None) -> List[Pattern]:
        """检测所有匹配的危险模式"""
        if max_results is None:
            max_results = cls._DEFAULT_DETECT_ALL_MAX
        if min_confidence is None:
            min_confidence = cls._DEFAULT_MIN_CONFIDENCE

        pattern_hits = cls._collect_matches(text)
        if not pattern_hits:
            return []

        def sort_key(item):
            p, _ = item
            return (cls.SEVERITY_RANK.get(p.severity, cls._DEFAULT_RANK_DEFAULT), p.name)

        sorted_patterns = sorted(pattern_hits.values(), key=sort_key)

        enriched = []
        for p, hit_kws in sorted_patterns:
            confidence = len(hit_kws) / len(p.keywords) if p.keywords else 0.0
            enriched.append((p, hit_kws, confidence))

        filtered = []
        for p, hit_kws, confidence in enriched:
            if p.severity in ("🔴紧急", "🟡警告"):
                filtered.append((p, hit_kws, confidence))
            elif confidence >= min_confidence:
                filtered.append((p, hit_kws, confidence))

        if max_results > 0:
            emergency = [(p, kw, c) for p, kw, c in filtered if p.severity in ("🔴紧急", "🟡警告")]
            moderate = [(p, kw, c) for p, kw, c in filtered if p.severity not in ("🔴紧急", "🟡警告")]
            slots = max_results - len(emergency)
            filtered = emergency + moderate[:max(0, slots)]

        return [p for p, _, _ in filtered]


# ========================
# 沟通模式评估（核心逻辑与I/O分离）
# ========================

def compute_communication(text: str) -> Dict[str, Any]:
    """沟通模式评估核心逻辑（纯计算，无I/O）"""
    text_lower = text.lower()

    negative_found = []
    positive_found = []
    total_negative = 0
    total_positive = 0

    for pattern_id, pattern in COMMUNICATION_NEGATIVE_PATTERNS.items():
        matches = [ind for ind in pattern["indicators"] if ind in text_lower]
        if matches:
            negative_found.append({
                "pattern_id": pattern_id,
                "name": pattern["name"],
                "matches": matches,
                "severity": pattern["severity"]
            })
            total_negative += pattern["severity"]

    for pattern_id, pattern in COMMUNICATION_POSITIVE_PATTERNS.items():
        matches = [ind for ind in pattern["indicators"] if ind in text_lower]
        if matches:
            positive_found.append({
                "pattern_id": pattern_id,
                "name": pattern["name"],
                "matches": matches,
                "weight": pattern["weight"]
            })
            total_positive += pattern["weight"]

    emotion_result = EmotionAnalyzer.detect(text)
    emotion_intensity = EmotionAnalyzer.intensity(text)
    detected_emotions = EmotionAnalyzer.extract_emotions(text)

    if total_positive > 0 or total_negative > 0:
        ratio = total_positive / (total_positive + total_negative)
        health_ratio = round(ratio * 100, 1)
    else:
        health_ratio = 50
        ratio = 0.5

    if ratio >= 0.8:
        recommendation = "优秀的沟通模式！继续保持"
    elif ratio >= 0.6:
        recommendation = "良好的沟通，可以继续改进"
    elif ratio >= 0.4:
        recommendation = "需要关注和改进沟通方式"
    else:
        recommendation = "建议学习非暴力沟通技巧"

    return {
        "type": "communication",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "negative_count": len(negative_found),
        "positive_count": len(positive_found),
        "health_ratio": health_ratio,
        "level": recommendation,
        "negative_patterns": [p["name"] for p in negative_found],
        "positive_patterns": [p["name"] for p in positive_found],
        "emotion": emotion_result,
        "emotion_intensity": emotion_intensity,
        "detected_emotions": detected_emotions,
        "_negative_found": negative_found,
        "_positive_found": positive_found,
    }


def communication_assessment(text: Optional[str] = None) -> Dict[str, Any]:
    """沟通模式评估

    Args:
        text: 可选，直接传入文本用于自动化测试。
              如为None，则通过交互式输入获取。
    """
    if text is None:
        print("\n" + "=" * 50)
        print("亲子沟通模式评估")
        print("=" * 50)
        print("\n请输入您最近与孩子的一次对话（输入'q'结束）：\n")

        text_lines = []
        while True:
            try:
                line = input()
                if line.lower() == 'q':
                    break
                text_lines.append(line)
            except EOFError:
                break

        if not text_lines:
            print("未输入内容，使用默认测试文本演示...")
            text_lines = ["孩子: 我不想上学了", "家长: 你又来这套！"]

        text = "\n".join(text_lines)

    result = compute_communication(text)

    # 打印结果
    print("\n" + "-" * 40)
    print("分析中...")
    print("-" * 40)

    print("\n" + "=" * 50)
    print("沟通模式分析结果")
    print("=" * 50)
    print(f"\n【输入文本】:\n{text[:200]}{'...' if len(text) > 200 else ''}")

    if result["_negative_found"]:
        print(f"\n检测到 {result['negative_count']} 种负面模式:")
        for p in result["_negative_found"]:
            print(f"  ⚠️ {p['name']}: {', '.join(p['matches'])} (严重度: {p['severity']})")

    if result["_positive_found"]:
        print(f"\n检测到 {result['positive_count']} 种正面模式:")
        for p in result["_positive_found"]:
            print(f"  ✅ {p['name']}: {', '.join(p['matches'])}")

    print(f"\n沟通健康度: {result['health_ratio']}%")
    print(f"评估: {result['level']}")

    emotion_emoji = {"positive": "😊", "negative": "😢", "neutral": "😐"}
    print(f"\n情感分析: {emotion_emoji.get(result['emotion'], '')} {result['emotion']} (强度: {result['emotion_intensity']}/10)")
    if result["detected_emotions"]:
        print(f"情绪词: {', '.join(result['detected_emotions'])}")
    print("=" * 50)

    # 移除内部字段
    del result["_negative_found"]
    del result["_positive_found"]
    return result


# ========================
# 原有评估函数（核心逻辑与I/O分离）
# ========================

def compute_stress(scores: List[int]) -> Dict[str, Any]:
    """养育压力评估核心逻辑（纯计算，无I/O）"""
    total = sum(scores)
    n = len(scores)

    if total <= 10:
        level = "正常压力范围"
        advice = "你的压力在正常范围内。继续保持自我觉察。"
    elif total <= 17:
        level = "轻度压力"
        advice = "建议关注自己的情绪状态，尝试增加休息时间。"
    elif total <= 25:
        level = "中度压力"
        advice = "建议寻求支持：与伴侣沟通、朋友倾诉或心理咨询。"
    else:
        level = "高度压力"
        advice = "你的压力较大，建议优先照顾自己，考虑专业帮助。"

    return {
        "type": "stress",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "max": n * 5,
        "level": level,
        "advice": advice,
        "scores": scores,
    }


def stress_assessment(scores: Optional[List[int]] = None) -> Dict[str, Any]:
    """养育压力快速筛查（5题）

    Args:
        scores: 可选，直接传入各题分数用于自动化测试。
                如为None，则通过交互式输入获取。
    """
    questions = [
        "1. 育儿让我感到疲惫不堪",
        "2. 我觉得作为父母很失败",
        "3. 育儿占据了太多时间",
        "4. 我经常对孩子发脾气",
        "5. 我觉得没有人理解我",
    ]

    if scores is None:
        print("\n" + "=" * 50)
        print("养育压力快速筛查（过去一个月）")
        print("=" * 50)
        print("评分: 1=从不, 2=偶尔, 3=有时, 4=经常, 5=总是\n")

        scores = []
        for q in questions:
            while True:
                try:
                    print(f"{q}")
                    score = int(input("评分(1-5): ").strip())
                    if 1 <= score <= 5:
                        scores.append(score)
                        break
                    print("请输入1-5")
                except ValueError:
                    print("请输入数字1-5")
            print()

    result = compute_stress(scores)

    print("=" * 50)
    print(f"总分: {result['total']}/{result['max']}")
    n = len(scores)
    print(f"平均: {result['total']/n:.1f}/5")
    print(f"压力等级: {result['level']}")
    print(f"建议: {result['advice']}")
    print("=" * 50)

    return result


def compute_relation(scores: List[int]) -> Dict[str, Any]:
    """亲子关系评估核心逻辑（纯计算，无I/O）"""
    total = sum(scores)
    n = len(scores)

    if total >= 23:
        level = "高质量亲子关系"
        advice = "你和孩子的关系很好。继续保持这种连接。"
    elif total >= 18:
        level = "中等质量"
        advice = "关系尚可，注意在压力下保持对孩子的回应质量。"
    else:
        level = "需要改善"
        advice = "建议每天安排专门的全心陪伴时间，从15分钟开始。"

    return {
        "type": "relation",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "max": n * 5,
        "level": level,
        "advice": advice,
        "scores": scores,
    }


def relation_assessment(scores: Optional[List[int]] = None) -> Dict[str, Any]:
    """亲子关系质量快速评估（5题）

    Args:
        scores: 可选，直接传入各题分数用于自动化测试。
    """
    questions = [
        "1. 我能感受到孩子的情感需求",
        "2. 我能够平静地回应孩子的哭闹",
        "3. 我和孩子有愉快的共处时光",
        "4. 我能够接纳孩子的负面情绪",
        "5. 我相信孩子愿意向我敞开心扉",
    ]

    if scores is None:
        print("\n" + "=" * 50)
        print("亲子关系质量快速评估")
        print("评分: 1=从不, 2=偶尔, 3=有时, 4=经常, 5=总是\n")

        scores = []
        for q in questions:
            while True:
                try:
                    print(f"{q}")
                    score = int(input("评分(1-5): ").strip())
                    if 1 <= score <= 5:
                        scores.append(score)
                        break
                    print("请输入1-5")
                except ValueError:
                    print("请输入数字1-5")
            print()

    result = compute_relation(scores)

    n = len(scores)
    print("=" * 50)
    print(f"总分: {result['total']}/{result['max']}")
    print(f"平均: {result['total']/n:.1f}/5")
    print(f"关系等级: {result['level']}")
    print(f"建议: {result['advice']}")
    print("=" * 50)

    return result


def compute_self_compassion(scores: List[int]) -> Dict[str, Any]:
    """自我慈悲评估核心逻辑（纯计算，无I/O）"""
    total = sum(scores)
    n = len(scores)

    if total >= 23:
        level = "高度自我慈悲"
        advice = "你对自己有健康的慈悲心。这会传递给孩子。"
    elif total >= 15:
        level = "中等自我慈悲"
        advice = "你对自己有一定的接纳，但可以更慈悲地对待自己的不完美。"
    else:
        level = "缺乏自我慈悲"
        advice = "你可能对自己过于苛刻。记住：对自己慈悲，才能对孩子慈悲。"

    return {
        "type": "self_compassion",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total": total,
        "max": n * 5,
        "level": level,
        "advice": advice,
        "scores": scores,
    }


def self_compassion_check(scores: Optional[List[int]] = None) -> Dict[str, Any]:
    """自我慈悲快速评估（5题）

    Args:
        scores: 可选，直接传入各题分数用于自动化测试。
    """
    questions = [
        "1. 我对犯错的自己能够保持耐心",
        "2. 我能够像对待朋友一样对待自己",
        "3. 我知道失败是成长的一部分",
        "4. 我能够接纳自己的不完美",
        "5. 我在疲惫时会照顾自己而不是自责",
    ]

    if scores is None:
        print("\n" + "=" * 50)
        print("自我慈悲快速评估")
        print("评分: 1=完全不像我, 5=非常像我\n")

        scores = []
        for q in questions:
            while True:
                try:
                    print(f"{q}")
                    score = int(input("评分(1-5): ").strip())
                    if 1 <= score <= 5:
                        scores.append(score)
                        break
                    print("请输入1-5")
                except ValueError:
                    print("请输入数字1-5")
            print()

    result = compute_self_compassion(scores)

    n = len(scores)
    print("=" * 50)
    print(f"总分: {result['total']}/{result['max']}")
    print(f"平均: {result['total']/n:.1f}/5")
    print(f"等级: {result['level']}")
    print(f"建议: {result['advice']}")
    print("=" * 50)

    return result


def compute_pattern_detection(text: str) -> Dict[str, Any]:
    """危险模式检测核心逻辑（纯计算，无I/O）"""
    detected_patterns = PatternLibrary.detect_all(text, max_results=10)
    emotion_result = EmotionAnalyzer.detect(text)
    intent_result = IntentEngine.recognize(text)

    return {
        "type": "pattern_detection",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "pattern_count": len(detected_patterns),
        "patterns": [{"name": p.name, "severity": p.severity, "action": p.action} for p in detected_patterns],
        "intent": intent_result.get("primary_intent", "unknown"),
        "intent_confidence": intent_result.get("confidence", 0),
        "emotion": emotion_result,
        "_detected_patterns": detected_patterns,
    }


def pattern_detection_assessment(text: Optional[str] = None) -> Dict[str, Any]:
    """危险模式检测

    Args:
        text: 可选，直接传入文本用于自动化测试。
    """
    INTENT_NAMES = {
        "ask_help": "求助", "vent_emotion": "倾诉", "share_case": "分享案例",
        "seek_understanding": "寻求理解", "express_love": "表达关爱",
        "self_reflect": "自我反思", "unknown": "未知"
    }

    if text is None:
        print("\n" + "=" * 50)
        print("亲子沟通危险模式检测")
        print("=" * 50)
        print("\n请输入您想检测的文本（可以是孩子的原话、对话记录等）：")
        print("输入'q'结束输入\n")

        text_lines = []
        while True:
            try:
                line = input()
                if line.lower() == 'q':
                    break
                text_lines.append(line)
            except EOFError:
                break

        if not text_lines:
            print("未输入内容，使用默认测试文本演示...")
            text_lines = ["孩子：我不想活了，活着没意思"]

        text = "\n".join(text_lines)

    result = compute_pattern_detection(text)

    print("\n" + "-" * 40)
    print("检测中...")
    print("-" * 40)

    print("\n" + "=" * 50)
    print("危险模式检测结果")
    print("=" * 50)
    print(f"\n【输入文本】:\n{text[:200]}{'...' if len(text) > 200 else ''}")

    intent_name = INTENT_NAMES.get(result["intent"], "未知")
    print(f"\n【意图识别】: {intent_name} (置信度: {result['intent_confidence']:.0%})")

    emotion_emoji = {"positive": "😊", "negative": "😢", "neutral": "😐"}
    print(f"【情感分析】: {emotion_emoji.get(result['emotion'], '')} {result['emotion']}")

    detected = result["_detected_patterns"]
    if detected:
        emergency = [p for p in detected if p.severity == "🔴紧急"]
        warning = [p for p in detected if p.severity == "🟡警告"]
        attention = [p for p in detected if p.severity == "🟠关注"]

        if emergency:
            print(f"\n🔴 紧急模式 ({len(emergency)}个):")
            for p in emergency:
                print(f"  ⚠️ {p.name}: {p.description}")
                print(f"     关键词: {', '.join(p.keywords[:3])}")
                print(f"     建议: {p.action}")

        if warning:
            print(f"\n🟡 警告模式 ({len(warning)}个):")
            for p in warning:
                print(f"  ⚠️ {p.name}: {p.description}")
                print(f"     建议: {p.action}")

        if attention:
            print(f"\n🟠 关注模式 ({len(attention)}个):")
            for p in attention:
                print(f"  • {p.name}: {p.description}")
                print(f"     建议: {p.action}")
    else:
        print("\n未检测到危险模式 ✓")

    print("=" * 50)

    del result["_detected_patterns"]
    return result


# ========================
# 历史记录展示（修复原地排序）
# ========================

def show_history() -> None:
    """显示评估历史"""
    history = load_history()
    if not history:
        print("暂无历史记录。")
        return

    print("\n=== 评估历史 ===")
    by_type: Dict[str, List[Dict]] = {}
    for record in history:
        t = record['type']
        by_type.setdefault(t, []).append(record)

    for t, records in by_type.items():
        print(f"\n[{t}]")
        for r in sorted(records, key=lambda x: x['date'], reverse=True)[:5]:
            if 'total' in r:
                pct = r['total'] / r['max'] * 100
                print(f"  {r['date']}: {r['total']}/{r['max']} ({pct:.0f}%) - {r['level']}")
            elif 'health_ratio' in r:
                print(f"  {r['date']}: 健康度{r['health_ratio']}% - {r['level']}")
            elif 'dominant_name' in r:
                print(f"  {r['date']}: {r['dominant_name']}")


# ========================
# 主函数
# ========================

def main() -> None:
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--history" in args:
        show_history()
        return

    result = None
    if "--stress" in args:
        result = stress_assessment()
    elif "--relation" in args:
        result = relation_assessment()
    elif "--compassion" in args:
        result = self_compassion_check()
    elif "--parenting" in args:
        result = parenting_style_assessment()
    elif "--communication" in args:
        result = communication_assessment()
    elif "--pattern" in args:
        result = pattern_detection_assessment()
    elif "--all" in args:
        results = []
        results.append(stress_assessment())
        print("\n按Enter继续亲子关系评估...")
        input()
        results.append(relation_assessment())
        print("\n按Enter继续自我慈悲评估...")
        input()
        results.append(self_compassion_check())
        print("\n按Enter继续教养风格评估...")
        input()
        results.append(parenting_style_assessment())
        print("\n按Enter继续沟通模式评估...")
        input()
        results.append(communication_assessment())

        # 汇总
        print("\n" + "=" * 50)
        print("五维度综合评估摘要")
        print("=" * 50)
        for r in results:
            if 'total' in r:
                pct = r['total'] / r['max'] * 100
                print(f"  {r['type']}: {r['total']}/{r['max']} ({pct:.0f}%) - {r['level']}")
            elif 'health_ratio' in r:
                print(f"  {r['type']}: 健康度{r['health_ratio']}% - {r['level']}")
            elif 'dominant_name' in r:
                print(f"  {r['type']}: {r['dominant_name']}")
            elif 'pattern_count' in r:
                print(f"  {r['type']}: 检测到{r['pattern_count']}个危险模式")

        # 跨维度关联分析
        cross = cross_dimension_analysis(results)
        print(f"\n--- 关联分析 (风险等级: {cross['risk_level']}/5) ---")
        for a in cross["analyses"]:
            print(f"  {a}")
        print("=" * 50)

        result = results
    else:
        print(__doc__)
        return

    # 保存
    if result:
        history = load_history()
        if isinstance(result, list):
            history.extend(result)
        else:
            history.append(result)
        save_history(history)
        print(f"\n已保存到历史记录 (共{len(history)}条)")


if __name__ == "__main__":
    main()
