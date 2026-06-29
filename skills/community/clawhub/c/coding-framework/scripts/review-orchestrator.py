#!/usr/bin/env python3
"""
review-orchestrator.py — 多代理审查编排器

协调多个审查代理并行执行代码审查，收集结果并汇总为统一报告。

v10.1 改进:
  - 合并策略: 按文件+行号归组，严重度取最高，标记来源代理
  - 输入校验: 文件路径存在、代理名称合法
  - 置信度分级: Critical ≥50, High ≥70, Medium ≥80, Low ≥90
  - 分层过滤: --fast-fail 发现 critical 立即中断
  - JSON 输出: 所有输出均为结构化 JSON

功能:
  - 根据代码特征自动选择代理
  - 生成每个代理的任务描述
  - 收集并合并结构化结果
  - 置信度分级过滤
  - 冲突检测与解决
  - 生成汇总报告

用法:
  python review-orchestrator.py --files "src/main.py" --agents "code-reviewer,security-auditor"
  python review-orchestrator.py --files "src/" --all-agents --fast-fail
  python review-orchestrator.py --files "src/" --auto-select --output report.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ─── 常量 ───────────────────────────────────────────────────────────────────

AGENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents")
DEFAULT_CONFIDENCE = 80

# v10.1: 置信度分级阈值
CONFIDENCE_THRESHOLDS = {
    "critical": 50,  # 安全漏洞、数据丢失风险，低阈值确保不漏报
    "high": 70,      # 逻辑错误、性能问题
    "medium": 80,    # 代码风格、最佳实践
    "low": 90,       # 风格建议、可选优化，高阈值避免噪声
}

ALL_AGENTS = [
    "code-reviewer",
    "security-auditor",
    "test-engineer",
    "architecture-critic",
    "performance-analyst",
    "maintainability-reviewer",
    "documentation-checker",
]

# 代理选择规则（根据文件特征自动选择）
AGENT_SELECTION_RULES = {
    "security-auditor": {
        "patterns": [r"password", r"secret", r"token", r"auth", r"login", r"encrypt", r"credential"],
        "extensions": [".env", ".pem", ".key", ".cert"],
        "keywords": ["security", "安全", "漏洞", "audit"],
    },
    "test-engineer": {
        "patterns": [r"def test_", r"class Test", r"describe\(", r"it\("],
        "extensions": [".test.", ".spec."],
        "keywords": ["test", "测试", "覆盖率", "coverage"],
    },
    "architecture-critic": {
        "patterns": [r"import\s+\w+\.\w+", r"from\s+\w+\s+import", r"class\s+\w+.*:"],
        "extensions": [],
        "keywords": ["架构", "模块", "依赖", "architecture", "module"],
    },
    "performance-analyst": {
        "patterns": [r"for\s+.*\s+in\s+.*:\s*\n\s*for\s+", r"\.query\(", r"\.find_all\("],
        "extensions": [],
        "keywords": ["性能", "优化", "瓶颈", "performance", "slow"],
    },
    "maintainability-reviewer": {
        "patterns": [r"TODO|FIXME|HACK|XXX"],
        "extensions": [],
        "keywords": ["可维护", "技术债务", "清晰度", "maintainability"],
    },
    "documentation-checker": {
        "patterns": [r'"""', r"'''", r"/\*\*", r"///"],
        "extensions": [".md", ".rst", ".txt"],
        "keywords": ["文档", "注释", "documentation", "readme"],
    },
    "code-reviewer": {
        "patterns": [],
        "extensions": [".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c"],
        "keywords": ["审查", "review", "代码质量", "code quality"],
    },
}


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_agent_definition(agent_name: str) -> dict:
    """加载代理 YAML 定义文件。"""
    yaml_path = os.path.join(AGENTS_DIR, f"{agent_name}.yaml")
    if not os.path.exists(yaml_path):
        return {"name": agent_name, "error": f"代理定义文件不存在: {yaml_path}"}

    # 简单 YAML 解析（提取关键字段）
    result = {"name": agent_name}
    with open(yaml_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取 display_name
    match = re.search(r'display_name:\s*"([^"]+)"', content)
    if match:
        result["display_name"] = match.group(1)

    # 提取 description
    match = re.search(r'description:\s*"([^"]+)"', content)
    if match:
        result["description"] = match.group(1)

    # 提取 color
    match = re.search(r'color:\s*(\w+)', content)
    if match:
        result["color"] = match.group(1)

    # 提取 system_prompt
    match = re.search(r'system_prompt:\s*\|\s*\n(.*?)(?:\n\w|\Z)', content, re.DOTALL)
    if match:
        result["system_prompt"] = match.group(1).strip()

    return result


def auto_select_agents(files: list, user_keywords: str = "") -> list:
    """根据文件特征和关键词自动选择代理。"""
    selected = set()
    all_content = ""

    # 收集文件扩展名和内容样本
    extensions = set()
    for f in files:
        p = Path(f)
        extensions.add(p.suffix.lower())
        if p.exists() and p.is_file():
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                    all_content += fh.read(5000)  # 读取前 5000 字符
            except (OSError, IOError):
                pass

    # 根据规则匹配
    for agent_name, rules in AGENT_SELECTION_RULES.items():
        score = 0

        # 检查扩展名
        for ext in rules.get("extensions", []):
            if any(ext in e for e in extensions):
                score += 1
            if ext in all_content[:1000]:
                score += 2

        # 检查内容模式
        for pattern in rules.get("patterns", []):
            if re.search(pattern, all_content, re.IGNORECASE):
                score += 1

        # 检查关键词
        for keyword in rules.get("keywords", []):
            if keyword.lower() in user_keywords.lower():
                score += 3
            if keyword.lower() in all_content.lower():
                score += 1

        if score >= 2:
            selected.add(agent_name)

    # 至少选择 code-reviewer
    if not selected:
        selected.add("code-reviewer")

    return sorted(selected)


def generate_task_prompt(agent_name: str, files: list, focus: str = "") -> dict:
    """为指定代理生成任务提示。"""
    agent_def = load_agent_definition(agent_name)

    file_contents = {}
    for f in files:
        p = Path(f)
        if p.exists() and p.is_file():
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                    file_contents[str(f)] = fh.read()
            except (OSError, IOError):
                file_contents[str(f)] = "[无法读取文件]"
        elif p.is_dir():
            file_contents[str(f)] = "[目录，需递归读取]"

    task = {
        "agent": agent_name,
        "agent_display_name": agent_def.get("display_name", agent_name),
        "system_prompt": agent_def.get("system_prompt", ""),
        "files": file_contents,
        "focus": focus,
        "instruction": f"请审查以下代码，重点关注你的专业领域。返回 JSON 格式结果。",
    }

    return task


def filter_by_confidence(findings: list, use_tiered: bool = True) -> dict:
    """按置信度过滤发现（v10.1 改进：分级阈值）。
    
    v10.1 改进:
      - Critical ≥50: 安全漏洞、数据丢失风险，低阈值确保不漏报
      - High ≥70: 逻辑错误、性能问题
      - Medium ≥80: 代码风格、最佳实践
      - Low ≥90: 风格建议、可选优化，高阈值避免噪声
    """
    included = []
    pending = []
    discarded = []

    for finding in findings:
        confidence = finding.get("confidence", 0)
        severity = finding.get("severity", "medium").lower()
        
        # 根据严重度获取阈值
        if use_tiered:
            threshold = CONFIDENCE_THRESHOLDS.get(severity, DEFAULT_CONFIDENCE)
        else:
            threshold = DEFAULT_CONFIDENCE
        
        if confidence >= threshold:
            finding["confidence_threshold_used"] = threshold
            included.append(finding)
        elif confidence >= threshold - 20:
            finding["confidence_threshold_used"] = threshold
            pending.append(finding)
        else:
            discarded.append(finding)

    return {
        "included": included,
        "pending_confirmation": pending,
        "discarded": discarded,
    }


def resolve_conflicts(all_findings: list) -> list:
    """检测并解决多代理间的冲突（v10.1 改进：合并策略）。
    
    v10.1 合并策略:
      - 按文件+行号归组
      - 同一位置多个代理报告 → 严重度取最高
      - 合并建议文本，标记来源代理
      - 冲突报告（同一位置不同结论）→ 保留两者，标记"需人工判断"
    """
    # 按位置分组（文件+行号）
    by_location = {}
    for f in all_findings:
        # 构建位置键: file:line
        file_path = f.get("file", "unknown")
        line = f.get("line", 0)
        loc = f"{file_path}:{line}" if line else file_path
        
        if loc not in by_location:
            by_location[loc] = []
        by_location[loc].append(f)

    conflicts = []
    merged_findings = []
    
    for loc, findings in by_location.items():
        if len(findings) == 1:
            # 单代理报告，直接保留
            merged_findings.append(findings[0])
            continue
        
        # 多代理报告同一位置
        severities = [f.get("severity", "low") for f in findings]
        unique_severities = set(severities)
        
        if len(unique_severities) == 1:
            # 所有代理意见一致，合并建议
            merged = findings[0].copy()
            merged["sources"] = [f.get("agent", "unknown") for f in findings]
            merged["merged_suggestions"] = [f.get("suggestion", "") for f in findings]
            merged["merge_type"] = "consistent"
            merged_findings.append(merged)
        else:
            # 意见冲突，按严重性排序，取最严重的
            severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            findings.sort(key=lambda x: severity_order.get(x.get("severity", "low"), 0), reverse=True)
            
            conflicts.append({
                "location": loc,
                "findings": findings,
                "sources": [f.get("agent", "unknown") for f in findings],
                "severities": severities,
                "resolution": "取严重性最高的意见",
                "selected": findings[0],
                "needs_human_review": True,  # 标记需人工判断
            })
            
            # 保留最严重的发现
            merged_findings.append(findings[0])

    return conflicts, merged_findings


def generate_report(
    agents_used: list,
    all_findings: list,
    conflicts: list,
    files_reviewed: list,
    use_tiered_thresholds: bool = True,
) -> dict:
    """生成汇总审查报告（v10.1 改进）。"""
    filtered = filter_by_confidence(all_findings, use_tiered=use_tiered_thresholds)

    # 按严重性排序
    severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    filtered["included"].sort(
        key=lambda x: severity_order.get(x.get("severity", "low"), 0), reverse=True
    )

    # 统计
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in filtered["included"]:
        sev = f.get("severity", "low")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    # 各代理评分
    agent_scores = {}
    for f in all_findings:
        agent = f.get("agent", "unknown")
        if agent not in agent_scores:
            agent_scores[agent] = []
        if "score" in f:
            agent_scores[agent].append(f["score"])

    avg_scores = {}
    for agent, scores in agent_scores.items():
        if scores:
            avg_scores[agent] = sum(scores) / len(scores)

    report = {
        "report_type": "multi-agent-code-review",
        "version": "10.1.0",
        "generated_at": now_iso(),
        "files_reviewed": files_reviewed,
        "agents_used": agents_used,
        "confidence_thresholds": CONFIDENCE_THRESHOLDS if use_tiered_thresholds else {"default": DEFAULT_CONFIDENCE},
        "summary": {
            "total_findings": len(filtered["included"]),
            "severity_counts": severity_counts,
            "pending_confirmation": len(filtered["pending_confirmation"]),
            "discarded": len(filtered["discarded"]),
            "conflicts": len(conflicts),
        },
        "agent_scores": avg_scores,
        "findings": filtered["included"],
        "pending_findings": filtered["pending_confirmation"],
        "conflicts": conflicts,
    }

    return report


def validate_files(files: list) -> tuple:
    """验证文件路径（v10.1 新增）。返回 (valid_files, errors)。"""
    valid = []
    errors = []
    
    for f in files:
        p = Path(f)
        if p.exists():
            valid.append(f)
        else:
            errors.append(f"文件不存在: {f}")
    
    return valid, errors


def check_fast_fail(findings: list) -> Optional[dict]:
    """检查是否应快速失败（v10.1 新增）。
    
    如果发现 critical 级别问题，立即返回中断信息。
    """
    for f in findings:
        if f.get("severity") == "critical" and f.get("confidence", 0) >= CONFIDENCE_THRESHOLDS["critical"]:
            return {
                "fast_fail": True,
                "reason": "发现 critical 级别问题",
                "finding": f,
                "message": f"⚠️ 快速中断: {f.get('file', 'unknown')}:{f.get('line', 0)} - {f.get('title', '未知问题')}"
            }
    return None


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="多代理审查编排器 — 协调多个审查代理并行执行代码审查 (v10.1)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--files", nargs="+", required=True, help="要审查的文件或目录")
    parser.add_argument("--agents", help="指定代理列表（逗号分隔）")
    parser.add_argument("--all-agents", action="store_true", help="使用所有代理")
    parser.add_argument("--auto-select", action="store_true", help="根据代码特征自动选择代理")
    parser.add_argument("--confidence", type=int, default=DEFAULT_CONFIDENCE, 
                        help=f"置信度阈值（默认 {DEFAULT_CONFIDENCE}，v10.1 已改为分级阈值）")
    parser.add_argument("--focus", help="特殊关注点")
    parser.add_argument("--output", help="输出报告文件路径（JSON）")
    parser.add_argument("--tasks-only", action="store_true", help="仅输出任务分配（不执行审查）")
    parser.add_argument("--fast-fail", action="store_true", 
                        help="v10.1: 发现 critical 问题立即中断")
    parser.add_argument("--no-tiered", action="store_true", 
                        help="v10.1: 禁用分级置信度阈值，使用统一阈值")

    args = parser.parse_args()

    # v10.1: 输入校验 - 验证文件路径
    valid_files, file_errors = validate_files(args.files)
    if file_errors:
        for err in file_errors:
            print(json.dumps({"warning": err}, ensure_ascii=False))
    if not valid_files:
        print(json.dumps({"error": "没有有效的文件", "success": False}, ensure_ascii=False))
        sys.exit(1)

    # 确定代理列表
    if args.all_agents:
        agents = ALL_AGENTS[:]
    elif args.agents:
        agents = [a.strip() for a in args.agents.split(",")]
    elif args.auto_select:
        agents = auto_select_agents(valid_files, args.focus or "")
    else:
        agents = ["code-reviewer"]

    # v10.1: 输入校验 - 验证代理名称
    valid_agents = []
    invalid_agents = []
    for agent in agents:
        if agent in ALL_AGENTS:
            valid_agents.append(agent)
        else:
            invalid_agents.append(agent)
    
    if invalid_agents:
        print(json.dumps({
            "warning": f"未知代理已跳过: {', '.join(invalid_agents)}",
            "valid_agents": ALL_AGENTS
        }, ensure_ascii=False))

    if not valid_agents:
        print(json.dumps({"error": "没有有效的代理", "success": False}, ensure_ascii=False))
        sys.exit(1)

    # 生成任务
    tasks = []
    for agent in valid_agents:
        task = generate_task_prompt(agent, valid_files, args.focus or "")
        tasks.append(task)

    if args.tasks_only:
        output = {
            "version": "10.1.0",
            "agents": valid_agents,
            "tasks": tasks,
            "files": valid_files,
            "confidence_thresholds": CONFIDENCE_THRESHOLDS if not args.no_tiered else {"default": args.confidence},
            "fast_fail": args.fast_fail,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # 输出编排计划
    plan = {
        "version": "10.1.0",
        "action": "review_plan",
        "agents": valid_agents,
        "agent_count": len(valid_agents),
        "files": valid_files,
        "confidence_thresholds": CONFIDENCE_THRESHOLDS if not args.no_tiered else {"default": args.confidence},
        "fast_fail": args.fast_fail,
        "focus": args.focus or "",
        "tasks": [{"agent": t["agent"], "display_name": t["agent_display_name"]} for t in tasks],
        "instruction": "使用 sessions_spawn 并行启动以上代理，每个代理使用对应的 system_prompt 和 task",
        "merge_strategy": "按文件+行号归组，严重度取最高，标记来源代理",
        "timestamp": now_iso(),
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(json.dumps({
            "success": True, 
            "output": args.output, 
            "message": f"审查计划已写入 {args.output}"
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
