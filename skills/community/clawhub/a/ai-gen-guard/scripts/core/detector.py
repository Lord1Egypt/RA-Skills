"""
生成式 AI 服务合规检测引擎
对输入文本进行生成式 AI 服务合规分析，输出结构化裁决结果
基于《生成式人工智能服务管理暂行办法》（2023年8月15日施行）
+ 强制性国家标准《网络安全技术 生成式人工智能服务安全基本要求》
"""

import re
from .rules import RULES

# 否定前缀词表 - 出现在正面信号前 10 字符内视为否定
NEGATION_PREFIXES = [
    "未", "没有", "无", "不", "尚未", "暂未", "并未", "并无",
    "缺失", "缺少", "缺", "遗漏", "未做", "未完成", "未进行",
    "没", "未申报", "未通过", "未建立", "未签", "未防范",
]

# fail 信号若以这些否定词开头，本身已表达"缺失"，不做否定检测，
# 避免"并未备案""仍未备案"等表达被误判为合规而漏检
_FAIL_START_NEGATIONS = (
    "未", "没有", "无", "没", "不", "尚未", "暂未",
    "并未", "并无", "缺失", "缺少", "缺", "遗漏",
)


def _match_indicators(text: str, indicators: list[str]) -> list[str]:
    """匹配文本中的生成式AI服务相关关键词"""
    found = []
    text_lower = text.lower()
    for keyword in indicators:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return found


def _starts_with_negation(signal: str) -> bool:
    """判断 fail 信号是否以否定词开头（本身已表达缺失状态）"""
    return any(signal.startswith(n) for n in _FAIL_START_NEGATIONS)


def _is_negated(text: str, signal: str, pos: int) -> bool:
    """
    检查正面信号是否被否定前缀修饰。
    在信号位置前 10 个字符窗口内查找否定词。
    """
    window_start = max(0, pos - 10)
    preceding = text[window_start:pos]
    for neg in NEGATION_PREFIXES:
        if neg in preceding:
            return True
    return False


def _detect_compliance_signals(text: str) -> dict:
    """
    检测文本中的合规信号 - 使用模式匹配判断每项规则的合规状态。
    否定前缀优先：如果正面信号被否定词修饰，则归类为负面信号。
    """
    # 合规信号词库 - 正面信号（已做合规），含核心词以便否定前缀检测
    pass_signals = {
        "filing_registration": [
            "已备案", "已完成备案", "已登记", "算法备案", "安全评估通过",
            "已通过安全评估", "已申报", "已履行备案", "备案完成",
            "备案", "安全评估", "生成式AI服务备案",
        ],
        "training_data": [
            "合法来源", "数据台账", "已取得同意", "标注规则", "知识产权清晰",
            "数据来源合法", "单独同意", "来源台账", "建立台账", "已建台账",
            "训练数据", "数据台账", "合法来源数据", "数据合规",
        ],
        "content_safety": [
            "拒绝生成", "拒答", "已处置", "投诉机制", "举报入口", "模型优化",
            "内容审核", "安全过滤", "已建立投诉", "风险过滤", "处置违法",
            "内容安全", "投诉举报", "安全评估机制",
        ],
        "user_protection": [
            "服务协议", "防沉迷", "未成年人模式", "输入信息保护", "已删除",
            "查阅复制", "隐私保护", "用户协议", "防依赖", "防过度依赖",
            "签订协议", "服务条款", "个人信息删除",
        ],
        "labeling": [
            "已标识", "已添加标识", "显式标识", "隐式标识", "按深度合成规定",
            "添加水印", "元数据标识", "做了标识", "深度合成标识",
            "标识", "AI标识", "内容标识",
        ],
    }

    # 负面信号 - 合规缺失（精确子串匹配）
    fail_signals = {
        "filing_registration": [
            "未备案", "没有备案", "没备案", "缺少备案", "未做安全评估",
            "未通过安全评估", "未登记", "未进行备案", "未申报备案",
            "未办理备案", "未做备案",
        ],
        "training_data": [
            "无合法来源", "未授权数据", "未做数据台账", "非法数据", "没有数据台账",
            "来源不明", "未做标注", "未建立台账", "缺少台账", "数据不合规",
            "数据来源不明", "未建台账",
        ],
        "content_safety": [
            "未拒答", "未处置", "无投诉入口", "没有投诉", "未过滤",
            "缺少投诉", "未做内容审核", "未建立举报", "无举报入口",
            "未建投诉机制", "未做安全过滤",
        ],
        "user_protection": [
            "无服务协议", "未签协议", "未防沉迷", "没有防沉迷", "未保护输入",
            "未提供删除", "无隐私保护", "缺少协议", "未防范沉迷",
            "未签服务协议", "未做输入保护", "不支持删除",
        ],
        "labeling": [
            "未标识", "未添加标识", "没有标识", "缺少标识", "未按深度合成",
            "未做标识", "未加标识", "没标识", "未做深度合成标识",
        ],
    }

    results = {}
    for rule_id in [r["id"] for r in RULES]:
        # 检查正面信号（含否定前缀检测）
        passes = []
        negated_passes = []
        for signal in pass_signals.get(rule_id, []):
            search_from = 0
            while True:
                pos = text.find(signal, search_from)
                if pos < 0:
                    break
                if _is_negated(text, signal, pos):
                    negated_passes.append(f"否定:{signal}")
                else:
                    passes.append(signal)
                search_from = pos + len(signal)

        # 检查负面信号
        # 严谨逻辑：信号以否定词开头（如"未备案"）→ 直接判违规，不做否定检测，
        # 避免"并未备案/仍未备案"漏检；否则（正性动作短语）被否定词修饰时
        # 不算违规（如"不向未成年人提供"中的"向未成年人提供"）
        fails = []
        for signal in fail_signals.get(rule_id, []):
            pos = text.find(signal)
            if pos < 0:
                continue
            if _starts_with_negation(signal) or not _is_negated(text, signal, pos):
                fails.append(signal)

        # 被否定的正面信号归入负面
        fails.extend(negated_passes)

        # 清理：如果正面信号是被否定信号的子串，也移除
        negated_texts = [s.replace("否定:", "") for s in negated_passes]
        passes = [p for p in passes if not any(p in nt for nt in negated_texts)]

        # 检查相关概念词
        rule = next(r for r in RULES if r["id"] == rule_id)
        related_keywords = []
        for q in rule.get("questions", []):
            phrases = re.findall(r'[\u4e00-\u9fa5]{3,10}', q)
            for phrase in phrases:
                if phrase in text and phrase not in related_keywords:
                    related_keywords.append(phrase)

        results[rule_id] = {
            "pass_signals": passes,
            "fail_signals": fails,
            "related_keywords": related_keywords,
        }

    return results


def _assess_scenario(text: str) -> dict:
    """初步评估：文本是否涉及生成式AI服务合规场景"""
    all_indicators = []
    for rule in RULES:
        if "indicators" in rule:
            extracted = _match_indicators(text, rule.get("indicators", []))
            idx = RULES.index(rule)
            all_indicators.extend([(idx, kw) for kw in extracted])

    has_ai_content = len(all_indicators) > 0
    hit_rules = list(set(idx for idx, _ in all_indicators))
    return {
        "has_ai_content": has_ai_content,
        "matched_indicators": [kw for _, kw in all_indicators],
        "hit_rules": hit_rules,
    }


def _assess_compliance_reading(text: str) -> list[dict]:
    """
    评估文本中描述的合规状态。
    使用合规信号检测 + 关键词匹配。
    否定前缀优先于正面信号判断。
    """
    signals = _detect_compliance_signals(text)
    results = []

    for rule in RULES:
        sig = signals.get(rule["id"], {})
        pass_sigs = sig.get("pass_signals", [])
        fail_sigs = sig.get("fail_signals", [])
        related = sig.get("related_keywords", [])

        if fail_sigs:
            status = "fail"
            detail = f"检测到合规缺失信号: {', '.join(fail_sigs[:3])}"
        elif pass_sigs:
            status = "pass"
            detail = f"检测到合规信号: {', '.join(pass_sigs[:3])}"
        elif related:
            status = "possible_pass"
            detail = f"文本涉及相关概念 ({len(related)}处)，建议补充确认"
        else:
            status = "unchecked"
            detail = "未提供足够信息进行评估"

        results.append({
            "id": rule["id"],
            "label": rule["label"],
            "regulation": rule["regulation"],
            "standard_ref": rule.get("standard_ref", ""),
            "status": status,
            "detail": detail,
            "findings": pass_sigs[:5] if pass_sigs else [],
            "questions": rule.get("questions", []),
        })

    return results


def scan_text(text: str) -> dict:
    """
    扫描输入文本，输出结构化生成式AI服务合规评估结果。
    """
    scenario = _assess_scenario(text)
    checks = _assess_compliance_reading(text)

    # 计算风险等级
    if not scenario["has_ai_content"]:
        risk_level = "low"
        summary = "未检测到生成式AI服务相关场景"
    else:
        fail_count = sum(1 for c in checks if c["status"] == "fail")
        pass_count = sum(1 for c in checks if c["status"] == "pass")
        unchecked = sum(1 for c in checks if c["status"] == "unchecked")
        total = len(checks)

        if fail_count > 0:
            risk_level = "high"
        elif unchecked >= 3:
            risk_level = "medium"
        elif pass_count >= 3:
            risk_level = "low"
        else:
            risk_level = "medium"

        summary = (
            f"检测到生成式AI服务合规相关信号 ({len(scenario['matched_indicators'])}项关键词触发)，"
            f"合规检查: {pass_count}/{total} 项通过"
        )

    suggested_actions = _generate_actions(checks, risk_level)

    return {
        "risk_level": risk_level,
        "summary": summary,
        "scenario": scenario,
        "checks": checks,
        "suggested_actions": suggested_actions,
    }


def _generate_actions(checks: list[dict], risk_level: str) -> list[str]:
    """生成建议动作"""
    actions = []
    for c in checks:
        if c["status"] == "fail":
            actions.append(f"🔴 【{c['label']}】{c['regulation']}：{c['detail']}")
        elif c["status"] == "unchecked":
            actions.append(f"⚪ 【{c['label']}】{c['regulation']}：缺少相关信息，建议补充")

    if not actions:
        actions.append("当前描述未发现明显合规缺口")
    else:
        actions.insert(0, "建议对照《生成式人工智能服务管理暂行办法》及配套强制国标进行正式合规评估")
    return actions
