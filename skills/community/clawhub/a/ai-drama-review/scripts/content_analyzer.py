"""
AI 深度内容分析模块

调用 OpenAI / Anthropic API 进行深层内容理解。
使用 urllib.request，零外部依赖。
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from credential_manager import get_credential, list_available_providers


def _call_openai(prompt: str, system_prompt: str = "",
                 model: str = "gpt-4o") -> str:
    """调用 OpenAI API。"""
    api_key = get_credential("openai")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2000,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]


def _call_anthropic(prompt: str, system_prompt: str = "",
                    model: str = "claude-sonnet-4-20250514") -> str:
    """调用 Anthropic API。"""
    api_key = get_credential("anthropic")

    payload = json.dumps({
        "model": model,
        "max_tokens": 2000,
        "system": system_prompt or "You are a content compliance analyst.",
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        },
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
        return data["content"][0]["text"]


def call_ai(prompt: str, system_prompt: str = "",
            preferred_provider: str = None) -> Optional[str]:
    """
    统一 AI 调用接口，自动选择可用 provider。

    Returns:
        AI 回复文本，无可用 provider 时返回 None
    """
    available = list_available_providers()

    if not available:
        return None

    # 确定调用顺序
    providers_to_try = []
    if preferred_provider and preferred_provider in available:
        providers_to_try.append(preferred_provider)
    for p in ["openai", "anthropic"]:
        if p in available and p not in providers_to_try:
            providers_to_try.append(p)

    for provider in providers_to_try:
        try:
            if provider == "openai":
                return _call_openai(prompt, system_prompt)
            elif provider == "anthropic":
                return _call_anthropic(prompt, system_prompt)
        except Exception:
            continue

    return None


# === 版权分析 ===

def analyze_plagiarism_context(suspicious_pairs: list) -> Optional[dict]:
    """
    让 AI 判断可疑相似段落是否构成实质性侵权。

    Args:
        suspicious_pairs: [{"source": str, "reference": str, "score": float}, ...]

    Returns:
        {"confirmed": [...], "false_positives": [...], "analysis": str}
    """
    if not suspicious_pairs:
        return None

    pairs_text = ""
    for i, pair in enumerate(suspicious_pairs[:10]):  # 限制数量
        pairs_text += (
            f"\n--- 可疑对 {i + 1} (相似度: {pair['score']:.2f}) ---\n"
            f"待检文本: {pair['source'][:200]}\n"
            f"参考文本: {pair['reference'][:200]}\n"
        )

    prompt = (
        f"以下是文本版权侵权检测中发现的可疑相似段落对。"
        f"请分析每一对是否构成实质性侵权，考虑以下因素：\n"
        f"1. 是否为通用表达或公共领域内容\n"
        f"2. 是否存在独创性的实质相似\n"
        f"3. 是否仅为同义改写但核心表达一致\n\n"
        f"{pairs_text}\n\n"
        f"请以 JSON 格式回复：\n"
        f'{{"confirmed": [编号列表], "false_positives": [编号列表], '
        f'"analysis": "整体分析说明"}}'
    )

    system = "你是一位版权合规分析专家，擅长判断文本是否存在侵权。请客观、准确地分析。"
    result = call_ai(prompt, system)

    if result:
        try:
            # 尝试提取 JSON
            json_match = result[result.find("{"):result.rfind("}") + 1]
            return json.loads(json_match)
        except (json.JSONDecodeError, ValueError):
            return {"analysis": result}

    return None


# === 分级分析 ===

def analyze_age_rating_context(hits_with_context: list,
                                target_rating: str) -> Optional[dict]:
    """
    让 AI 分析关键词命中的上下文，排除误报。

    Args:
        hits_with_context: [{"keyword": str, "context": str, "category": str}, ...]
        target_rating: 目标分级

    Returns:
        {"confirmed": [...], "false_positives": [...], "final_rating": str}
    """
    if not hits_with_context:
        return None

    hits_text = ""
    for i, hit in enumerate(hits_with_context[:15]):
        hits_text += (
            f"\n{i + 1}. 关键词: {hit['keyword']} (类别: {hit['category']})\n"
            f"   上下文: {hit['context']}\n"
        )

    prompt = (
        f"以下是内容分级检测中的关键词命中项。目标分级为: {target_rating}\n"
        f"请分析每个命中是否为真正的不当内容，排除以下误报情况：\n"
        f"1. 否定语境（如 '不要杀人' 中的 '杀'）\n"
        f"2. 文学修辞或比喻用法\n"
        f"3. 历史/教育引用\n"
        f"4. 角色对话中的合理表达\n\n"
        f"{hits_text}\n\n"
        f"请以 JSON 格式回复：\n"
        f'{{"confirmed": [编号列表], "false_positives": [编号列表], '
        f'"final_rating": "建议分级", "reasoning": "分析说明"}}'
    )

    system = "你是一位内容分级审核专家，擅长判断内容的年龄适宜性。请准确区分真正的不当内容和误报。"
    result = call_ai(prompt, system)

    if result:
        try:
            json_match = result[result.find("{"):result.rfind("}") + 1]
            return json.loads(json_match)
        except (json.JSONDecodeError, ValueError):
            return {"analysis": result}

    return None


# === 改编分析 ===

def extract_plot_and_characters(text: str) -> Optional[dict]:
    """让 AI 提取结构化的情节点和角色概要。"""
    # 截断过长文本
    truncated = text[:5000]

    prompt = (
        f"请分析以下文本，提取结构化信息：\n\n"
        f"{truncated}\n\n"
        f"请以 JSON 格式回复：\n"
        f'{{"plot_points": [{{"index": 1, "summary": "情节摘要", '
        f'"characters": ["角色名"], "importance": "core|normal|minor"}}], '
        f'"characters": [{{"name": "角色名", "traits": ["性格"], '
        f'"relationships": {{"角色名": "关系"}}}}]}}'
    )

    system = "你是一位文学分析专家，擅长提取叙事结构和角色信息。"
    result = call_ai(prompt, system)

    if result:
        try:
            json_match = result[result.find("{"):result.rfind("}") + 1]
            return json.loads(json_match)
        except (json.JSONDecodeError, ValueError):
            return {"raw_analysis": result}

    return None


def analyze_adaptation_significance(deviations: list) -> Optional[dict]:
    """让 AI 评估改编偏差的严重程度和合理性。"""
    if not deviations:
        return None

    dev_text = ""
    for i, dev in enumerate(deviations[:10]):
        dev_text += (
            f"\n{i + 1}. 类型: {dev.get('type', 'unknown')}\n"
            f"   原文: {dev.get('original', '')[:150]}\n"
            f"   改编: {dev.get('adapted', '')[:150]}\n"
        )

    prompt = (
        f"以下是原著与改编版之间的偏差列表。请评估：\n"
        f"1. 每个偏差是否合理\n"
        f"2. 是否偏离了原著的核心精神\n"
        f"3. 整体改编质量\n\n"
        f"{dev_text}\n\n"
        f"请以 JSON 格式回复：\n"
        f'{{"overall_assessment": "忠实改编|合理改编|严重魔改", '
        f'"justified_changes": [编号], "unjustified_changes": [编号], '
        f'"reasoning": "分析说明"}}'
    )

    system = "你是一位文学评论专家，擅长评估小说改编的质量和忠实度。"
    result = call_ai(prompt, system)

    if result:
        try:
            json_match = result[result.find("{"):result.rfind("}") + 1]
            return json.loads(json_match)
        except (json.JSONDecodeError, ValueError):
            return {"analysis": result}

    return None


# === 综合风险评估 ===

def generate_risk_assessment(all_findings: dict) -> Optional[dict]:
    """让 AI 综合所有发现，生成整体风险评估。"""
    findings_text = json.dumps(all_findings, ensure_ascii=False, indent=2)

    # 截断过长内容
    if len(findings_text) > 4000:
        findings_text = findings_text[:4000] + "\n... (已截断)"

    prompt = (
        f"以下是AI短剧合规审查的全部检测结果：\n\n"
        f"{findings_text}\n\n"
        f"请综合分析，给出：\n"
        f"1. 整体风险评级（low/medium/high/critical）\n"
        f"2. 最紧迫的合规问题\n"
        f"3. 具体的整改建议\n\n"
        f"请以 JSON 格式回复：\n"
        f'{{"risk_level": "等级", "top_issues": ["问题列表"], '
        f'"remediation": ["整改建议列表"], "summary": "总结"}}'
    )

    system = "你是一位内容合规顾问，擅长评估AI生成内容的法律和道德风险。"
    result = call_ai(prompt, system)

    if result:
        try:
            json_match = result[result.find("{"):result.rfind("}") + 1]
            return json.loads(json_match)
        except (json.JSONDecodeError, ValueError):
            return {"analysis": result}

    return None
