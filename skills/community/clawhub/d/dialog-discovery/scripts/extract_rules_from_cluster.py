#!/usr/bin/env python3
"""
基于 seed 分桶的规则提取脚本（v2 - LLM 深度提取版）

v1 问题：只做信号名频率统计，输出机械复读 "good_seed中高频出现 explicit_acceptance"，
        等于把信号名重说一遍，毫无实质价值。

v2 改动：
- 新增 LLM 模式（默认）：从每个桶抽样对话原文，让 LLM 深度归纳规则、话术、问题模式
- 保留 stats 模式：原有信号统计逻辑，作为辅助证据
- 输出路径对齐 warm 层规范结构：
    warm/candidates/rules.md
    warm/candidates/utterances.md
    warm/evidence/rules.md
    warm/evidence/utterances.md
    warm/learnings/insights.md
    warm/learnings/issues.md
"""
import argparse
import json
import os
import random
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from common import WORKSPACE_DIR
from llm_client import call_messages, parse_json_response

MEMORY_BASE = os.path.expanduser("~/pe-self-improving/memory")

# ── LLM 提取 Prompt 模板 ──

PROMPT_EXTRACT_RULES = """你是对话分析专家。以下是从{bucket}桶抽样的{scene}场景真实对话（ASR转写）。

请深度分析这些对话，提取**实质性**规则和话术。

要求：
1. 规则必须具体可执行，不能是信号名的复读（如"出现explicit_acceptance"是废话）
2. 每条规则必须给出：规则标题、规则描述、支撑对话片段（原文引用）
3. 话术必须来自对话原文，标注来自哪个对话
4. 区分"底线规则"（违规即失败）、"核心规则"（关键成功因素）、"增效规则"（锦上添花）

对话内容：
{dialogs}

请输出 JSON：
{{
  "rules": [
    {{
      "id": "RULE-{scene}-{bucket_tag}-001",
      "category": "底线|核心|增效",
      "title": "规则标题",
      "description": "具体描述，说明什么情况下应该怎么做",
      "evidence": "支撑的对话原文片段",
      "dialog_ids": ["对话ID"]
    }}
  ],
  "utterances": [
    {{
      "id": "UTTR-{scene}-{bucket_tag}-001",
      "category": "开场|利益|异议|引导|收尾",
      "text": "话术原文",
      "context": "使用场景说明",
      "dialog_ids": ["对话ID"]
    }}
  ]
}}"""

PROMPT_EXTRACT_BAD_PATTERNS = """你是对话分析专家。以下是从{bucket}桶抽样的{scene}场景真实对话（ASR转写）。

这些是对话效果较差的样本。请深度分析：

1. 提取**具体的问题模式**：不是信号名复读，而是描述"客服做了什么→导致什么结果"的因果链
2. 提取**洞察**：从失败中能学到的反直觉发现
3. 每条都要有对话原文支撑

对话内容：
{dialogs}

请输出 JSON：
{{
  "issues": [
    {{
      "id": "ISSUE-{scene}-001",
      "severity": "高|中|低",
      "title": "问题模式标题",
      "description": "具体的问题模式描述，包含因果链",
      "evidence": "支撑的对话原文片段",
      "dialog_ids": ["对话ID"]
    }}
  ],
  "insights": [
    {{
      "id": "INSIGHT-{scene}-001",
      "title": "洞察标题",
      "description": "具体的洞察描述",
      "evidence": "支撑的对话原文片段",
      "dialog_ids": ["对话ID"]
    }}
  ]
}}"""

PROMPT_EXTRACT_GRAY_HYPOTHESES = """你是对话分析专家。以下是从{bucket}桶抽样的{scene}场景真实对话（ASR转写）。

这些是边界样本——既不是明确的成功也不是明确的失败。请分析：

1. 这些对话有什么共同特征让它们落入了灰色地带？
2. 有哪些假设可以解释它们的模糊状态？
3. 有哪些待验证的假设值得后续人工确认？

对话内容：
{dialogs}

请输出 JSON：
{{
  "hypotheses": [
    {{
      "title": "假设标题",
      "description": "假设的具体描述",
      "confidence": "低|中|高",
      "evidence": "支撑的对话原文片段",
      "dialog_ids": ["对话ID"],
      "suggested_action": "建议的验证方式"
    }}
  ]
}}"""


def load_clusters(clusters_path: str) -> Dict[str, Any]:
    with open(clusters_path, "r", encoding="utf-8") as f:
        return json.load(f)


def sample_dialogs(cluster: List[Dict[str, Any]], n: int = 20, max_chars: int = 30000) -> str:
    """从分桶中抽样对话，拼成文本供 LLM 分析"""
    if not cluster:
        return "（无样本）"
    n = min(n, len(cluster))
    samples = random.sample(cluster, n)
    parts = []
    total_chars = 0
    for item in samples:
        dialog_id = item.get("dialog_id", "unknown")
        dialog = item.get("dialog", {})
        agent_text = dialog.get("agent_text", "")
        user_text = dialog.get("user_text", "")
        raw = dialog.get("raw_text", "") or dialog.get("clean_text", "")
        # 优先用 agent_text + user_text，否则用 raw_text
        if agent_text or user_text:
            text = f"客服: {agent_text}\n客户: {user_text}"
        else:
            text = raw
        entry = f"---\n【对话 {dialog_id}】\n{text}\n"
        if total_chars + len(entry) > max_chars:
            break
        parts.append(entry)
        total_chars += len(entry)
    return "\n".join(parts)


# ── stats 模式（原有逻辑，简化保留） ──

def aggregate_signal_support(cluster: List[Dict[str, Any]], signal_group: str) -> Dict[str, Dict[str, Any]]:
    support: Dict[str, Dict[str, Any]] = {}
    for item in cluster:
        dialog_id = item.get("dialog_id")
        for signal in item.get("signals", {}).get(signal_group, []):
            if signal not in support:
                support[signal] = {"count": 0, "dialog_ids": []}
            support[signal]["count"] += 1
            support[signal]["dialog_ids"].append(dialog_id)
    return support


def run_stats_mode(clusters: Dict[str, Any], scene: str, output_path: str) -> None:
    """原有统计模式，输出信号频率报告（辅助参考，非实质规则）"""
    good_seed = clusters.get("good_seed", [])
    bad_seed = clusters.get("bad_seed", [])

    lines = [f"# 信号频率统计（辅助参考）\n", f"场景: {scene}", f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

    if good_seed:
        lines.append("## good_seed 信号频率\n")
        for group in ["positive", "quality"]:
            support = aggregate_signal_support(good_seed, group)
            for name, info in sorted(support.items(), key=lambda x: x[1]["count"], reverse=True):
                pct = info["count"] / len(good_seed) * 100
                lines.append(f"- {name}: {info['count']}/{len(good_seed)} ({pct:.1f}%)")

    if bad_seed:
        lines.append("\n## bad_seed 信号频率\n")
        for group in ["negative", "risk"]:
            support = aggregate_signal_support(bad_seed, group)
            for name, info in sorted(support.items(), key=lambda x: x[1]["count"], reverse=True):
                pct = info["count"] / len(bad_seed) * 100
                lines.append(f"- {name}: {info['count']}/{len(bad_seed)} ({pct:.1f}%)")

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 信号统计已保存: {output_path}")


# ── LLM 模式（v2 核心新增） ──

def call_llm_extract(prompt: str, max_retries: int = 2) -> Optional[Dict[str, Any]]:
    """调用 LLM 提取，带重试"""
    messages = [{"role": "user", "content": prompt}]
    for attempt in range(max_retries):
        try:
            result = call_messages(messages, max_tokens=8000)
            parsed = parse_json_response(result)
            if parsed:
                return parsed
            print(f"  ⚠ LLM 返回非 JSON（尝试 {attempt+1}/{max_retries}）")
        except Exception as e:
            print(f"  ⚠ LLM 调用失败: {e}（尝试 {attempt+1}/{max_retries}）")
    return None


def extract_good_rules(clusters: Dict[str, Any], scene: str) -> Dict[str, Any]:
    """从 good_seed 提取正向规则和话术"""
    good_seed = clusters.get("good_seed", [])
    if not good_seed:
        print("  good_seed 为空，跳过")
        return {"rules": [], "utterances": []}

    print(f"  抽样 good_seed ({len(good_seed)} 条)...")
    dialogs_text = sample_dialogs(good_seed, n=20, max_chars=30000)
    prompt = PROMPT_EXTRACT_RULES.format(
        bucket="good_seed",
        scene=scene,
        dialogs=dialogs_text,
    )
    result = call_llm_extract(prompt)
    if not result:
        print("  ⚠ good_seed LLM 提取失败，返回空结果")
        return {"rules": [], "utterances": []}
    print(f"  ✅ 提取规则 {len(result.get('rules', []))} 条，话术 {len(result.get('utterances', []))} 条")
    return result


def extract_bad_patterns(clusters: Dict[str, Any], scene: str) -> Dict[str, Any]:
    """从 bad_seed 提取问题模式和洞察"""
    bad_seed = clusters.get("bad_seed", [])
    if not bad_seed:
        print("  bad_seed 为空，跳过")
        return {"issues": [], "insights": []}

    print(f"  抽样 bad_seed ({len(bad_seed)} 条)...")
    dialogs_text = sample_dialogs(bad_seed, n=20, max_chars=30000)
    prompt = PROMPT_EXTRACT_BAD_PATTERNS.format(
        bucket="bad_seed",
        scene=scene,
        dialogs=dialogs_text,
    )
    result = call_llm_extract(prompt)
    if not result:
        print("  ⚠ bad_seed LLM 提取失败，返回空结果")
        return {"issues": [], "insights": []}
    print(f"  ✅ 提取问题模式 {len(result.get('issues', []))} 条，洞察 {len(result.get('insights', []))} 条")
    return result


def extract_gray_hypotheses(clusters: Dict[str, Any], scene: str) -> List[Dict[str, Any]]:
    """从灰色地带提取待验证假设"""
    hypotheses = []
    for bucket_name in ["gray_high_risk", "gray_potential_good"]:
        bucket = clusters.get(bucket_name, [])
        if not bucket:
            continue
        print(f"  抽样 {bucket_name} ({len(bucket)} 条)...")
        dialogs_text = sample_dialogs(bucket, n=15, max_chars=20000)
        prompt = PROMPT_EXTRACT_GRAY_HYPOTHESES.format(
            bucket=bucket_name,
            scene=scene,
            dialogs=dialogs_text,
        )
        result = call_llm_extract(prompt)
        if result and result.get("hypotheses"):
            for h in result["hypotheses"]:
                h["source_bucket"] = bucket_name
            hypotheses.extend(result["hypotheses"])
            print(f"  ✅ {bucket_name} 提取假设 {len(result['hypotheses'])} 条")
        else:
            print(f"  ⚠ {bucket_name} LLM 提取失败")
    return hypotheses


# ── 写入 warm 层（对齐规范路径） ──

def write_warm_candidates_rules(rules: List[Dict[str, Any]], scene: str) -> str:
    """写入 warm/candidates/rules.md"""
    path = os.path.join(MEMORY_BASE, scene, "warm", "candidates", "rules.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 候选规则（LLM 提取）\n",
        f"> 场景: {scene}",
        f"> 提取时间: {now}",
        f"> 来源: good_seed 分桶抽样 → LLM 深度分析",
        f"> 状态: WARM（待验证晋升）\n",
    ]
    for cat in ["底线", "核心", "增效"]:
        cat_rules = [r for r in rules if r.get("category") == cat]
        if not cat_rules:
            continue
        lines.append(f"\n## {cat}规则\n")
        for r in cat_rules:
            lines.append(f"### {r.get('id', '?')} {r.get('title', '')}\n")
            lines.append(f"{r.get('description', '')}\n")
            lines.append(f"**证据**: {r.get('evidence', '无')}")
            lines.append(f"**对话**: {', '.join(r.get('dialog_ids', []))}\n")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已写入: {path}")
    return path


def write_warm_candidates_utterances(utterances: List[Dict[str, Any]], scene: str) -> str:
    """写入 warm/candidates/utterances.md"""
    path = os.path.join(MEMORY_BASE, scene, "warm", "candidates", "utterances.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 候选话术（LLM 提取）\n",
        f"> 场景: {scene}",
        f"> 提取时间: {now}",
        f"> 来源: good_seed 分桶抽样 → LLM 深度分析",
        f"> 状态: WARM（待验证晋升）\n",
    ]
    for cat in ["开场", "利益", "异议", "引导", "收尾"]:
        cat_utts = [u for u in utterances if u.get("category") == cat]
        if not cat_utts:
            continue
        lines.append(f"\n## {cat}话术\n")
        for u in cat_utts:
            lines.append(f"### {u.get('id', '?')} {u.get('context', '')}\n")
            lines.append(f"> {u.get('text', '')}\n")
            lines.append(f"**对话**: {', '.join(u.get('dialog_ids', []))}\n")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已写入: {path}")
    return path


def write_warm_evidence_rules(rules: List[Dict[str, Any]], scene: str) -> str:
    """写入 warm/evidence/rules.md"""
    path = os.path.join(MEMORY_BASE, scene, "warm", "evidence", "rules.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 规则证据来源\n",
        f"> 场景: {scene}",
        f"> 时间: {now}\n",
    ]
    for r in rules:
        lines.append(f"### {r.get('id', '?')} {r.get('title', '')}\n")
        lines.append(f"- 原文片段: {r.get('evidence', '无')}")
        lines.append(f"- 对话ID: {', '.join(r.get('dialog_ids', []))}\n")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已写入: {path}")
    return path


def write_warm_evidence_utterances(utterances: List[Dict[str, Any]], scene: str) -> str:
    """写入 warm/evidence/utterances.md"""
    path = os.path.join(MEMORY_BASE, scene, "warm", "evidence", "utterances.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 话术证据来源\n",
        f"> 场景: {scene}",
        f"> 时间: {now}\n",
    ]
    for u in utterances:
        lines.append(f"### {u.get('id', '?')}\n")
        lines.append(f"- 话术: {u.get('text', '')}")
        lines.append(f"- 上下文: {u.get('context', '')}")
        lines.append(f"- 对话ID: {', '.join(u.get('dialog_ids', []))}\n")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已写入: {path}")
    return path


def write_warm_learnings_issues(issues: List[Dict[str, Any]], scene: str) -> str:
    """写入 warm/learnings/issues.md"""
    path = os.path.join(MEMORY_BASE, scene, "warm", "learnings", "issues.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 问题模式（LLM 提取）\n",
        f"> 场景: {scene}",
        f"> 提取时间: {now}",
        f"> 来源: bad_seed 分桶抽样 → LLM 深度分析",
        f"> 状态: WARM（待验证晋升）\n",
    ]
    for sev in ["高", "中", "低"]:
        sev_issues = [i for i in issues if i.get("severity") == sev]
        if not sev_issues:
            continue
        lines.append(f"\n## {sev}严重度\n")
        for i in sev_issues:
            lines.append(f"### {i.get('id', '?')} {i.get('title', '')}\n")
            lines.append(f"{i.get('description', '')}\n")
            lines.append(f"**证据**: {i.get('evidence', '无')}")
            lines.append(f"**对话**: {', '.join(i.get('dialog_ids', []))}\n")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已写入: {path}")
    return path


def write_warm_learnings_insights(insights: List[Dict[str, Any]], hypotheses: List[Dict[str, Any]], scene: str) -> str:
    """写入 warm/learnings/insights.md"""
    path = os.path.join(MEMORY_BASE, scene, "warm", "learnings", "insights.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 洞察与假设（LLM 提取）\n",
        f"> 场景: {scene}",
        f"> 提取时间: {now}",
        f"> 来源: bad_seed 洞察 + 灰区假设",
        f"> 状态: WARM（待验证晋升）\n",
    ]
    if insights:
        lines.append("\n## 从 bad_seed 提取的洞察\n")
        for i in insights:
            lines.append(f"### {i.get('id', '?')} {i.get('title', '')}\n")
            lines.append(f"{i.get('description', '')}\n")
            lines.append(f"**证据**: {i.get('evidence', '无')}")
            lines.append(f"**对话**: {', '.join(i.get('dialog_ids', []))}\n")

    if hypotheses:
        lines.append("\n## 从灰区提取的待验证假设\n")
        for h in hypotheses:
            conf = h.get("confidence", "中")
            src = h.get("source_bucket", "?")
            lines.append(f"### {h.get('title', '')}\n")
            lines.append(f"- 来源: {src}")
            lines.append(f"- 置信度: {conf}")
            lines.append(f"- 描述: {h.get('description', '')}")
            lines.append(f"- 证据: {h.get('evidence', '无')}")
            lines.append(f"- 建议验证: {h.get('suggested_action', '人工抽样确认')}\n")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已写入: {path}")
    return path


def run_llm_mode(clusters: Dict[str, Any], scene: str, output_dir: str) -> None:
    """LLM 深度提取模式"""
    print("\n📊 LLM 深度提取模式")
    print("=" * 50)

    # 1. 从 good_seed 提取规则和话术
    print("\n[1/3] 提取 good_seed 规则与话术...")
    good_result = extract_good_rules(clusters, scene)

    # 2. 从 bad_seed 提取问题模式和洞察
    print("\n[2/3] 提取 bad_seed 问题模式与洞察...")
    bad_result = extract_bad_patterns(clusters, scene)

    # 3. 从灰区提取假设
    print("\n[3/3] 提取灰区假设...")
    hypotheses = extract_gray_hypotheses(clusters, scene)

    # 汇总
    rules = good_result.get("rules", [])
    utterances = good_result.get("utterances", [])
    issues = bad_result.get("issues", [])
    insights = bad_result.get("insights", [])

    print(f"\n📈 提取汇总:")
    print(f"  规则: {len(rules)} 条")
    print(f"  话术: {len(utterances)} 条")
    print(f"  问题模式: {len(issues)} 条")
    print(f"  洞察: {len(insights)} 条")
    print(f"  灰区假设: {len(hypotheses)} 条")

    # 写入 warm 层（对齐规范路径）
    print(f"\n📝 写入 warm 层...")
    write_warm_candidates_rules(rules, scene)
    write_warm_candidates_utterances(utterances, scene)
    write_warm_evidence_rules(rules, scene)
    write_warm_evidence_utterances(utterances, scene)
    write_warm_learnings_issues(issues, scene)
    write_warm_learnings_insights(insights, hypotheses, scene)

    # 同时写一份汇总 JSON 到 workspace
    summary = {
        "scene": scene,
        "extracted_at": datetime.now().isoformat(),
        "mode": "llm",
        "counts": {
            "rules": len(rules),
            "utterances": len(utterances),
            "issues": len(issues),
            "insights": len(insights),
            "hypotheses": len(hypotheses),
        },
        "rules": rules,
        "utterances": utterances,
        "issues": issues,
        "insights": insights,
        "hypotheses": hypotheses,
    }
    summary_path = os.path.join(output_dir, "loan-rules-extracted.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"✅ 汇总 JSON: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description="基于 seed 分桶提取候选规则（v2 - LLM 深度提取）")
    parser.add_argument("--clusters", required=True, help="分桶结果文件（json）")
    parser.add_argument("--scene", required=True, help="场景名称")
    parser.add_argument("--output", default="", help="输出文件（stats 模式用）")
    parser.add_argument(
        "--mode",
        choices=["llm", "stats"],
        default="llm",
        help="提取模式: llm=LLM深度提取(默认), stats=信号频率统计",
    )
    parser.add_argument("--sample-size", type=int, default=20, help="每桶抽样数量（LLM 模式）")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()

    random.seed(args.seed)

    clusters = load_clusters(args.clusters)
    print(f"✅ 已加载分桶结果")
    for bucket_name in ["good_seed", "bad_seed", "gray_high_risk", "gray_potential_good"]:
        print(f"  {bucket_name}: {len(clusters.get(bucket_name, []))} 条")

    output_dir = os.path.dirname(args.clusters) or WORKSPACE_DIR

    if args.mode == "stats":
        output_path = args.output or os.path.join(output_dir, "loan-rules-stats.md")
        run_stats_mode(clusters, args.scene, output_path)
    else:
        run_llm_mode(clusters, args.scene, output_dir)


if __name__ == "__main__":
    main()
