#!/usr/bin/env python3
"""
ABTest Runner v1.0
多智能体双盲测试驱动引擎。

用法：
  python runner.py --prompt "写一首关于春天的诗" --rounds 3
  python runner.py --prompt "用Python实现快速排序" --rounds 2 --output json
  python runner.py --task-file tasks/code_gen.txt --rounds 3
  python runner.py --test                    # 自测模式（单会话内模拟）

依赖：
  - sessions_spawn (runtime="subagent") → Contestant A/B/Judge
  - sessions_send → 向子会话发送消息
  - judge_prompts.py → Judge 提示词构建 + 解析
  - anonymizer.py → 匿名化处理
"""

import argparse
import json
import random
import re
import sys
import os

# 强制 UTF-8 输出
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# 尝试导入本地模块（完整功能）
# 如果导入失败，使用内联降级实现
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from judge_prompts import build_judge_prompt, parse_judge_response, get_default_rubric
    from anonymizer import Anonymizer
except ImportError:
    # 内联降级实现
    get_default_rubric = lambda t: ["准确性", "完整性", "表达质量", "创意"]
    build_judge_prompt = None  # runner.py 自带的模板
    Anonymizer = None
    print("[警告] judge_prompts.py / anonymizer.py 未找到，使用内联模式", file=sys.stderr)

from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict, Any


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RoundResult:
    round_num: int
    solution_a: str       # Contestant A 原始输出
    solution_b: str       # Contestant B 原始输出
    order: tuple         # 展示顺序 (first_label, second_label)
    solution_1: str       # 匿名方案1内容
    solution_2: str       # 匿名方案2内容
    label_1: str          # 方案1 对应 A 或 B
    label_2: str          # 方案2 对应 A 或 B
    judge_scores_a: Dict[str, float]
    judge_scores_b: Dict[str, float]
    judge_total_a: float
    judge_total_b: float
    judge_comment: str
    winner: str            # "contestant_a" | "contestant_b" | "tie"
    winner_label: str       # "方案1" | "方案2"（揭示前）


@dataclass
class TestReport:
    task: str
    rounds: int
    rubric: List[str]
    results: List[RoundResult] = field(default_factory=list)
    final_winner: str = ""
    final_score_a: float = 0.0
    final_score_b: float = 0.0
    wins_a: int = 0
    wins_b: int = 0
    ties: int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT TEMPLATES（Contestant）
# ═══════════════════════════════════════════════════════════════════════════════

CONTESTANT_A_TEMPLATE = """你是 Contestant A（参赛者A）。请完成以下任务，**只输出结果内容**，不要在回复中提及你是谁、不要解释、不要加前缀。

任务：
{task}

输出格式（严格遵守）：
[CONTENT_A]
[你的完整输出]
[/CONTENT_A]"""

CONTESTANT_B_TEMPLATE = """你是 Contestant B（参赛者B）。请完成以下任务，**只输出结果内容**，不要在回复中提及你是谁、不要解释、不要加前缀。

任务：
{task}

输出格式（严格遵守）：
[CONTENT_B]
[你的完整输出]
[/CONTENT_B]"""


# ═══════════════════════════════════════════════════════════════════════════════
# JUDGE TEMPLATE（降级用内联版本）
# ═══════════════════════════════════════════════════════════════════════════════

def build_judge_prompt_inline(task, solution_1, solution_2, rubric):
    rubric_display = "\n".join(
        f"  {i+1}. {d}（满分10分）" for i, d in enumerate(rubric)
    )
    detail_lines = []
    for d in rubric:
        detail_lines.append(f"方案1-{d}: X/10（简短说明）")
        detail_lines.append(f"方案2-{d}: X/10（简短说明）")
    rubric_detail = "\n".join(detail_lines)
    return f"""你是一位严格公正的 AI 评测专家。请对以下两个匿名方案进行盲评——你不知道方案1来自哪个参赛者，也不知道方案2来自哪个参赛者。

【评测任务】
{task}

【评分维度】（每项满分 10 分）
{rubric_display}

【方案1内容】
{solution_1}

【方案2内容】
{solution_2}

【输出要求】严格按以下格式输出，不要有任何其他内容：

[SCORES]
{rubric_detail}
[/SCORES]
[TOTAL_A]{len(rubric)}项得分之和[/TOTAL_A]
[TOTAL_B]{len(rubric)}项得分之和[/TOTAL_B]
[WINNER]方案1 或 方案2 或 平局[/WINNER]
[COMMENT]总体评语（150字以内）[/COMMENT]"""


def parse_judge_inline(text, rubric):
    """内联解析 Judge 输出"""
    result = {
        "scores_a": {},
        "scores_b": {},
        "total_a": 0.0,
        "total_b": 0.0,
        "winner": "tie",
        "comment": "",
    }
    lines = text.split("\n")
    for i, dim in enumerate(rubric):
        for line in lines:
            if "方案1" in line and any(c in line for c in dim[:3]):
                m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", line)
                if m:
                    result["scores_a"][dim] = float(m.group(1))
            if "方案2" in line and any(c in line for c in dim[:3]):
                m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", line)
                if m:
                    result["scores_b"][dim] = float(m.group(1))

    ta = re.search(r"\[TOTAL_A\](.*?)\[/TOTAL_A\]", text, re.DOTALL)
    tb = re.search(r"\[TOTAL_B\](.*?)\[/TOTAL_B\]", text, re.DOTALL)
    if ta:
        try:
            result["total_a"] = float(ta.group(1).strip())
        except ValueError:
            result["total_a"] = sum(result["scores_a"].values())
    if tb:
        try:
            result["total_b"] = float(tb.group(1).strip())
        except ValueError:
            result["total_b"] = sum(result["scores_b"].values())
    if result["total_a"] == 0:
        result["total_a"] = sum(result["scores_a"].values())
    if result["total_b"] == 0:
        result["total_b"] = sum(result["scores_b"].values())

    w = re.search(r"\[WINNER\](.*?)\[/WINNER\]", text, re.DOTALL)
    if w:
        raw = w.group(1).strip()
        if "方案1" in raw:
            result["winner"] = "solution_1"
        elif "方案2" in raw:
            result["winner"] = "solution_2"
        else:
            result["winner"] = "tie"

    c = re.search(r"\[COMMENT\](.*?)\[/COMMENT\]", text, re.DOTALL)
    if c:
        result["comment"] = c.group(1).strip()
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_content(text: str, tag: str) -> str:
    """从 LLM 输出中提取 [TAG]...[/TAG] 包裹的内容。"""
    pattern = rf"\[{tag}\]\s*(.*?)\s*\[/{tag}\]"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW DRIVER（供 Agent 调用）
# ═══════════════════════════════════════════════════════════════════════════════

def run_workflow(
    task: str,
    rounds: int = 3,
    rubric: Optional[List[str]] = None,
) -> TestReport:
    """
    运行完整双盲测试工作流（参考实现）。
    实际执行由 AI Agent 在会话中通过 sessions_spawn 完成。
    此函数作为文档和测试桩存在。
    """
    if rubric is None:
        rubric = get_default_rubric("general")

    report = TestReport(task=task, rounds=rounds, rubric=rubric)

    for round_num in range(1, rounds + 1):
        print(f"[Round {round_num}/{rounds}] 工作流占位", file=sys.stderr)
        round_result = RoundResult(
            round_num=round_num,
            solution_a=f"[待填充 - Round {round_num}]",
            solution_b=f"[待填充 - Round {round_num}]",
            order=("A", "B"),
            solution_1="",
            solution_2="",
            label_1="A",
            label_2="B",
            judge_scores_a={d: 0.0 for d in rubric},
            judge_scores_b={d: 0.0 for d in rubric},
            judge_total_a=0.0,
            judge_total_b=0.0,
            judge_comment="",
            winner="tie",
            winner_label="方案1",
        )
        report.results.append(round_result)

    _summarize(report)
    return report


def _summarize(report: TestReport):
    """汇总所有轮次结果。根据每轮实际得分判断胜者。"""
    report.wins_a = sum(1 for r in report.results if r.judge_total_a > r.judge_total_b)
    report.wins_b = sum(1 for r in report.results if r.judge_total_b > r.judge_total_a)
    report.ties = sum(1 for r in report.results if r.judge_total_a == r.judge_total_b)
    report.final_score_a = sum(r.judge_total_a for r in report.results)
    report.final_score_b = sum(r.judge_total_b for r in report.results)

    if report.wins_a > report.wins_b:
        report.final_winner = "Contestant A 胜出"
    elif report.wins_b > report.wins_a:
        report.final_winner = "Contestant B 胜出"
    else:
        # 平局时看总分
        if report.final_score_a > report.final_score_b:
            report.final_winner = "平局（A总分略高）"
        elif report.final_score_b > report.final_score_a:
            report.final_winner = "平局（B总分略高）"
        else:
            report.final_winner = "平局（完全持平）"


# ═══════════════════════════════════════════════════════════════════════════════
# SELF-TEST（单会话模拟，无 subagent）
# ═══════════════════════════════════════════════════════════════════════════════

def run_self_test(task: str, rounds: int = 3, rubric: Optional[List[str]] = None):
    """
    自测模式：在单个会话中模拟三轮双盲测试。
    Contestant A = "答案1"；Contestant B = "答案2"
    Judge = 本会话评判（随机分数）
    用于验证工作流逻辑完整性。
    """
    if rubric is None:
        rubric = get_default_rubric("general")

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  [自测模式] 三轮双盲测试", file=sys.stderr)
    print(f"  任务: {task}", file=sys.stderr)
    print(f"  轮次: {rounds} | 评分维度: {rubric}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    # 模拟 Contestant 输出（占位符）
    mock_outputs = [
        ("方案A内容占位（实际为AI生成）", "方案B内容占位（实际为AI生成）"),
        ("Contestant A 在 Round 2 的输出", "Contestant B 在 Round 2 的输出"),
        ("A 在第3轮生成的完整回答", "B 在第3轮生成的完整回答"),
    ]

    report = TestReport(task=task, rounds=rounds, rubric=rubric)

    for i, round_num in enumerate(range(1, rounds + 1)):
        # 模拟 Contestant 输出
        sol_a, sol_b = mock_outputs[i] if i < len(mock_outputs) else ("A回答", "B回答")

        # 模拟匿名化（随机顺序）
        if random.random() < 0.5:
            sol_1, sol_2, label_1, label_2 = sol_a, sol_b, "A", "B"
        else:
            sol_1, sol_2, label_1, label_2 = sol_b, sol_a, "B", "A"

        # 模拟 Judge（随机评分）
        scores_a = {d: round(random.uniform(6.0, 9.5), 1) for d in rubric}
        scores_b = {d: round(random.uniform(6.0, 9.5), 1) for d in rubric}
        total_a = round(sum(scores_a.values()), 1)
        total_b = round(sum(scores_b.values()), 1)

        # 模拟 winner
        if total_a > total_b:
            winner = "solution_1"
            winner_label = "方案1"
            winner_actual = f"Contestant {label_1}"
        elif total_b > total_a:
            winner = "solution_2"
            winner_label = "方案2"
            winner_actual = f"Contestant {label_2}"
        else:
            winner = "tie"
            winner_label = "平局"
            winner_actual = "平局"

        comment = f"Round {round_num} 自测评分：{winner_actual} 略优"

        print(f"\n  Round {round_num}: 方案1={label_1}({total_a}) vs 方案2={label_2}({total_b})", file=sys.stderr)
        print(f"  → Judge: {winner_label} 胜出", file=sys.stderr)

        round_result = RoundResult(
            round_num=round_num,
            solution_a=sol_a,
            solution_b=sol_b,
            order=(label_1, label_2),
            solution_1=sol_1,
            solution_2=sol_2,
            label_1=label_1,
            label_2=label_2,
            judge_scores_a=scores_a,
            judge_scores_b=scores_b,
            judge_total_a=total_a,
            judge_total_b=total_b,
            judge_comment=comment,
            winner="contestant_a" if label_1 == "A" and winner == "solution_1"
                      or label_1 == "B" and winner == "solution_2"
                      else "contestant_b" if winner != "tie" else "tie",
            winner_label=winner_label,
        )
        report.results.append(round_result)

    _summarize(report)

    # 打印报告
    lines = [
        "",
        "═" * 60,
        f"  A/B 测试报告 — {report.rounds} 轮（自测）",
        "═" * 60,
        f"  任务: {report.task}",
        f"  评分维度: {', '.join(report.rubric)}",
    ]
    for r in report.results:
        lines += [
            "",
            f"  ─── 第 {r.round_num} 轮 ───",
            f"  方案1=Contestant {r.label_1} | 方案2=Contestant {r.label_2}",
            f"  {r.label_1} 总分: {r.judge_total_a:.1f} | {r.label_2} 总分: {r.judge_total_b:.1f}",
            f"  胜出: {r.winner_label}",
        ]
    lines += [
        "",
        "═" * 60,
        f"  最终结果",
        "═" * 60,
        f"  Contestant A 总分: {report.final_score_a:.1f} | 胜 {report.wins_a} 轮",
        f"  Contestant B 总分: {report.final_score_b:.1f} | 胜 {report.wins_b} 轮",
        f"  平局: {report.ties} 轮",
        "",
        f"  🏆 {report.final_winner}",
        "═" * 60,
    ]
    print("\n".join(lines))
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="多智能体双盲 A/B 测试驱动引擎")
    parser.add_argument("--prompt", "-p", type=str, default="", help="测试任务 Prompt")
    parser.add_argument("--task-file", "-f", type=str, default="", help="从文件读取任务")
    parser.add_argument("--rounds", "-r", type=int, default=3, help="测试轮次（默认3）")
    parser.add_argument("--rubric", nargs="+", default=None, help="评分维度（空格分隔）")
    parser.add_argument("--output", "-o", choices=["text", "json"], default="text")
    parser.add_argument("--task-type", "-t", default="general",
                        choices=["general", "creative_writing", "code_generation",
                                "logical_reasoning", "knowledge_qa", "multi_step_task"],
                        help="任务类型（决定默认评分维度）")
    parser.add_argument("--test", action="store_true", help="自测模式（单会话模拟）")
    parser.add_argument("--skip-spawn", action="store_true",
                        help="仅打印工作流步骤，不实际执行")
    args = parser.parse_args()

    # Load task
    if args.task_file:
        with open(args.task_file, "r", encoding="utf-8") as f:
            task = f.read().strip()
    elif args.prompt:
        task = args.prompt
    elif args.test:
        task = "[自测] 用Python写一个快速排序函数"
    else:
        print("错误: 必须提供 --prompt 或 --task-file", file=sys.stderr)
        sys.exit(1)

    rubric = args.rubric or get_default_rubric(args.task_type)

    # 自测模式
    if args.test:
        run_self_test(task, args.rounds, rubric)
        return

    # 打印模式
    if args.skip_spawn:
        print(f"\n任务: {task}", file=sys.stderr)
        print(f"轮次: {args.rounds}", file=sys.stderr)
        print(f"评分维度: {', '.join(rubric)}", file=sys.stderr)
        print("\n[skip-spawn 模式：仅打印工作流步骤]\n", file=sys.stderr)
        print("--- Contestant A Prompt ---")
        print(CONTESTANT_A_TEMPLATE.format(task=task))
        print("\n--- Contestant B Prompt ---")
        print(CONTESTANT_B_TEMPLATE.format(task=task))
        print("\n--- Judge Prompt ---")
        print(build_judge_prompt_inline(task, "[方案1内容占位]", "[方案2内容占位]", rubric))
        return

    # 正常执行
    report = run_workflow(task, args.rounds, rubric)

    if args.output == "json":
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    else:
        _print_text_report(report)


def _print_text_report(report: TestReport):
    lines = [
        "",
        "═" * 60,
        f"  A/B 测试报告 — {report.rounds} 轮",
        "═" * 60,
        f"  任务: {report.task}",
        f"  评分维度: {', '.join(report.rubric)}",
    ]
    for r in report.results:
        lines += [
            "",
            f"  ─── 第 {r.round_num} 轮 ───",
            f"  方案展示顺序: 方案1={r.label_1}, 方案2={r.label_2}",
            f"  方案1({r.label_1})得分: {r.judge_total_a:.1f} | 方案2({r.label_2})得分: {r.judge_total_b:.1f}",
            f"  胜出: {r.winner_label}",
        ]
        if r.judge_comment:
            lines.append(f"  评语: {r.judge_comment}")
    lines += [
        "",
        "═" * 60,
        f"  最终结果",
        "═" * 60,
        f"  Contestant A 总分: {report.final_score_a:.1f} | 胜 {report.wins_a} 轮",
        f"  Contestant B 总分: {report.final_score_b:.1f} | 胜 {report.wins_b} 轮",
        f"  平局: {report.ties} 轮",
        "",
        f"  🏆 {report.final_winner}",
        "═" * 60,
    ]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
