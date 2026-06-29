#!/usr/bin/env python3
"""
心虫 (Heartbug) 对比评测：有心虫 vs 无 心虫

运行方式:
    python eval_compare.py                                    # 全量 20 题评测
    python eval_compare.py --dimensions tool_calling planning  # 指定维度
    python eval_compare.py --verbose                           # 调试模式
    python eval_compare.py --output compare_report.json        # 导出报告

对比说明:
  - HeartbugAdapter: 使用心虫认知引擎（Unix socket → MCP daemon）
  - BaselineAdapter: 使用原生 LLM（Claude），无认知引擎增强
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

# 确保 eval/bench-lite 可被导入
EVAL_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(EVAL_DIR))

from agent_bench_lite import BenchmarkRunner, BenchmarkReport
from agent_bench_lite.adapters.base import BaseAdapter
from agent_bench_lite.adapters.anthropic_adapter import AnthropicAdapter
from agent_bench_lite.adapters.heartbug_adapter import HeartbugAdapter
from agent_bench_lite.core.evaluator import Evaluator, DimensionScore
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult
from agent_bench_lite.dimensions.tool_calling import ToolCallingDimension
from agent_bench_lite.dimensions.planning import PlanningDimension
from agent_bench_lite.dimensions.context_retention import ContextRetentionDimension
from agent_bench_lite.dimensions.error_recovery import ErrorRecoveryDimension
from agent_bench_lite.dimensions.instruction_following import InstructionFollowingDimension
from agent_bench_lite.dimensions.multi_step_reasoning import MultiStepReasoningDimension

# ── 评测维度选择 ──────────────────────────────────────────────────────

# 选择 20 道题的标准维度（每个维度选 3-4 题）
SELECTED_DIMENSIONS = {
    "tool_calling": ["tc_select_weather", "tc_db_search", "tc_calculate"],
    "planning": ["plan_deploy_website", "plan_data_migration", "plan_feature_auth"],
    "context_retention": ["ctx_remember_preference", "ctx_remember_name", "ctx_remember_budget"],
    "error_recovery": ["err_file_not_found", "err_http_timeout", "err_permission_denied"],
    "instruction_following": ["if_word_limit", "if_bullet_format", "if_json_output", "if_uppercase"],
    "multi_step_reasoning": ["msr_arithmetic_chain", "msr_logic_puzzle", "msr_unit_conversion", "msr_probability"],
}

# ── 结果数据结构 ──────────────────────────────────────────────────────


class ComparisonReport:
    """并排对比报告。"""

    def __init__(self):
        self.heartbug_scores: dict[str, DimensionScore] = {}
        self.baseline_scores: dict[str, DimensionScore] = {}
        self.heartbug_time: float = 0
        self.baseline_time: float = 0
        self.timestamp: str = time.strftime("%Y-%m-%d %H:%M:%S")

    def add_result(self, adapter_name: str, scores: list[DimensionScore], elapsed: float):
        target = self.heartbug_scores if adapter_name == "HeartbugAdapter" else self.baseline_scores
        for s in scores:
            # DimensionScore 使用 dimension_name 字段
            key = getattr(s, 'dimension_name', getattr(s, 'name', str(s)))
            target[key] = s
        if adapter_name == "HeartbugAdapter":
            self.heartbug_time = elapsed
        else:
            self.baseline_time = elapsed

    def _score_bar(self, score: float, width: int = 20) -> str:
        filled = round(score / 100.0 * width)
        empty = width - filled
        if score >= 80:
            color = "\033[92m"  # green
        elif score >= 50:
            color = "\033[93m"  # yellow
        else:
            color = "\033[91m"  # red
        return f"{color}{'█' * filled}\033[2m{'░' * empty}\033[0m"

    def print_comparison(self):
        """打印并排对比表。"""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║         心虫 (Heartbug) vs 原生LLM — Agent 评测对比报告                      ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"\n  时间: {self.timestamp}")
        print(f"  题量: 20 题 (6 维度)")

        # 汇总行
        hb_overall = self._overall(self.heartbug_scores)
        bl_overall = self._overall(self.baseline_scores)
        diff = hb_overall - bl_overall

        print("\n" + "─" * 80)
        print(f"  {'维度':<28}  {'❤️ 心虫':>10}  {'🤖 原生LLM':>10}  {'差异':>8}  {'可视化':>22}")
        print("─" * 80)

        all_names = sorted(set(list(self.heartbug_scores.keys()) + list(self.baseline_scores.keys())))
        for name in all_names:
            hb = self.heartbug_scores.get(name)
            bl = self.baseline_scores.get(name)
            hb_s = hb.score if hb else 0
            bl_s = bl.score if bl else 0
            d = hb_s - bl_s
            d_str = f"+{d:.1f}" if d > 0 else f"{d:.1f}"
            print(f"  {name:<28}  {hb_s:>9.1f}  {bl_s:>9.1f}  {d_str:>8}  {self._score_bar(hb_s)}")

        print("─" * 80)

        # 总分
        hb_badge = self._badge(hb_overall)
        bl_badge = self._badge(bl_overall)
        print(f"  {'综合得分':<28}  {hb_badge}  {bl_badge:>28}  {diff:+.1f}")
        print("─" * 80)

        # 统计
        hb_pass = sum(1 for s in self.heartbug_scores.values() if s.passed)
        bl_pass = sum(1 for s in self.baseline_scores.values() if s.passed)
        hb_total = sum(1 for s in self.heartbug_scores.values())
        bl_total = sum(1 for s in self.baseline_scores.values())
        print(f"\n  ❤️  心虫:   {hb_pass}/{hb_total} 维度通过 | {self.heartbug_time:.1f}s")
        print(f"  🤖 原生LLM: {bl_pass}/{bl_total} 维度通过 | {self.baseline_time:.1f}s")

        # 结论
        print("\n  📊 分析结论:")
        if hb_overall > bl_overall + 5:
            print(f"    ❤️  心虫显著优于原生 LLM (+{diff:.1f} 分)")
        elif hb_overall > bl_overall:
            print(f"    ❤️  心虫略优于原生 LLM (+{diff:.1f} 分)")
        elif abs(hb_overall - bl_overall) <= 5:
            print(f"    ≈ 两者表现接近 (差异 {diff:+.1f})")
        else:
            print(f"    🤖 原生 LLM 表现更好 ({diff:+.1f})")
        print()

    def _overall(self, scores: dict) -> float:
        vals = [s.score for s in scores.values()]
        return sum(vals) / len(vals) if vals else 0

    def _badge(self, score: float) -> str:
        if score >= 80:
            return f"\033[42m\033[97m {score:6.1f} \033[0m"
        elif score >= 50:
            return f"\033[43m\033[97m {score:6.1f} \033[0m"
        else:
            return f"\033[41m\033[97m {score:6.1f} \033[0m"

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "heartbug": {
                "overall": self._overall(self.heartbug_scores),
                "elapsed": self.heartbug_time,
                "dimensions": {k: {
                    "score": v.score,
                    "passed": v.passed,
                    "total": v.total,
                } for k, v in self.heartbug_scores.items()},
            },
            "baseline": {
                "overall": self._overall(self.baseline_scores),
                "elapsed": self.baseline_time,
                "dimensions": {k: {
                    "score": v.score,
                    "passed": v.passed,
                    "total": v.total,
                } for k, v in self.baseline_scores.items()},
            },
            "difference": self._overall(self.heartbug_scores) - self._overall(self.baseline_scores),
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ── 任务选择 ──────────────────────────────────────────────────────────


def filter_tasks(dim_class: type[BaseDimension], task_ids: list[str]) -> list[Task]:
    """从维度中筛选指定的 task。"""
    dim = dim_class()
    all_tasks = dim.get_tasks()
    task_map = {t.task_id: t for t in all_tasks}
    selected = []
    for tid in task_ids:
        if tid in task_map:
            selected.append(task_map[tid])
    return selected


# ── 自定义适配器 ──────────────────────────────────────────────────────


class FilteredDimension(BaseDimension):
    """包装维度类，只运行筛选后的任务。"""

    def __init__(self, dim_class: type[BaseDimension], task_ids: list[str], name: str, display_name: str):
        self._dim_class = dim_class
        self._task_ids = task_ids
        self.name = name
        self.display_name = display_name
        self.description = dim_class.description if hasattr(dim_class, 'description') else ""

    def get_tasks(self) -> list[Task]:
        return filter_tasks(self._dim_class, self._task_ids)

    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        return await self._dim_class().evaluate_task(task, adapter)


# ── 主逻辑 ────────────────────────────────────────────────────────────


async def run_single_adapter(adapter, dims: list[BaseDimension], verbose: bool = False) -> tuple[list[DimensionScore], float]:
    """运行单个适配器的评测。"""
    from agent_bench_lite.core.runner import RunConfig
    config = RunConfig(parallel=False, timeout_per_task=60.0)
    runner = BenchmarkRunner(adapter=adapter, dimensions=dims, config=config)

    start = time.perf_counter()
    report = await runner.run()
    elapsed = time.perf_counter() - start

    if verbose:
        print(f"\n{'='*60}")
        print(f"  Adapter: {type(adapter).__name__}")
        print(f"  Time: {elapsed:.1f}s")
        print(f"{'='*60}")
        report.print_summary()

    return report.scores, elapsed


async def run_comparison(dimensions: list[str] | None = None, verbose: bool = False) -> ComparisonReport:
    """运行心虫 vs 原生 LLM 的对比评测。"""

    # 选择维度
    dim_configs = {
        "tool_calling": (ToolCallingDimension, "tool_calling", "工具调用"),
        "planning": (PlanningDimension, "planning", "规划能力"),
        "context_retention": (ContextRetentionDimension, "context_retention", "上下文保持"),
        "error_recovery": (ErrorRecoveryDimension, "error_recovery", "错误恢复"),
        "instruction_following": (InstructionFollowingDimension, "instruction_following", "指令遵循"),
        "multi_step_reasoning": (MultiStepReasoningDimension, "multi_step_reasoning", "多步推理"),
    }

    if dimensions:
        dim_configs = {k: v for k, v in dim_configs.items() if k in dimensions}

    # 构建筛选后的维度实例
    dim_instances = []
    for dim_key, (dim_class, name, display) in dim_configs.items():
        task_ids = SELECTED_DIMENSIONS.get(dim_key, [])
        if task_ids:
            dim_instances.append(FilteredDimension(dim_class, task_ids, name, display))

    if not dim_instances:
        raise ValueError(f"没有可用的评测维度。可选: {list(SELECTED_DIMENSIONS.keys())}")

    total_tasks = sum(len(d.get_tasks()) for d in dim_instances)
    print(f"\n🧪 评测配置:")
    print(f"   维度: {len(dim_instances)} 个")
    print(f"   题量: {total_tasks} 题")
    print(f"   适配器: HeartbugAdapter (心虫) vs AnthropicAdapter (原生LLM)")
    print()

    # 构建适配器
    heartbug_adapter = HeartbugAdapter(
        socket_path="/Users/apple/.claude-clarity/claude-clarity.sock",
        verbose=verbose,
    )

    # 使用环境变量中的 API Key
    import os
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  未找到 ANTHROPIC_API_KEY，使用 EchoAdapter 作为基线")
        from agent_bench_lite.adapters.base import EchoAdapter
        baseline_adapter = EchoAdapter()
    else:
        baseline_adapter = AnthropicAdapter(
            model="claude-sonnet-4-20250514",
            api_key=api_key,
            temperature=0.0,
        )

    report = ComparisonReport()

    # ── 运行心虫 ────────────────────────────────────────────────────────
    print("❤️  运行心虫评测...")
    try:
        hb_scores, hb_time = await run_single_adapter(heartbug_adapter, dim_instances, verbose)
        report.add_result("HeartbugAdapter", hb_scores, hb_time)
        print(f"   ✅ 完成 ({hb_time:.1f}s)")
    except Exception as e:
        print(f"   ❌ 心虫评测失败: {e}")
        hb_scores = []
        hb_time = 0

    # ── 运行基线 ────────────────────────────────────────────────────────
    print("🤖 运行原生LLM评测...")
    try:
        bl_scores, bl_time = await run_single_adapter(baseline_adapter, dim_instances, verbose)
        report.add_result("BaselineAdapter", bl_scores, bl_time)
        print(f"   ✅ 完成 ({bl_time:.1f}s)")
    except Exception as e:
        print(f"   ❌ 基线评测失败: {e}")
        bl_scores = []
        bl_time = 0

    return report


# ── CLI 入口 ──────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="心虫 (Clarity) vs 原生LLM 对比评测",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python eval_compare.py                                    # 全量 20 题评测
  python eval_compare.py --dimensions tool_calling planning  # 指定维度
  python eval_compare.py --verbose                           # 输出调试信息
  python eval_compare.py --output compare_report.json        # 导出 JSON
        """,
    )
    parser.add_argument(
        "--dimension",
        nargs="+",
        choices=[
            "tool_calling", "planning", "context_retention",
            "error_recovery", "instruction_following", "multi_step_reasoning",
        ],
        help="指定要评测的维度（默认: 全部 6 维度 × 20 题）",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="输出调试信息")
    parser.add_argument("--output", "-o", type=str, help="将 JSON 报告写入文件")
    parser.add_argument(
        "--socket", type=str,
        default="/Users/apple/.claude-clarity/claude-clarity.sock",
        help="心虫 daemon socket 路径",
    )

    args = parser.parse_args()

    # 检查 socket
    if not Path(args.socket).exists():
        print(f"错误: 心虫 daemon 未运行 — socket 不存在: {args.socket}")
        print("请先启动心虫: python ~/.claude/skills/claude-clarity/bin/boot-fast.js")
        sys.exit(1)

    # 运行评测
    try:
        report = asyncio.run(run_comparison(
            dimensions=args.dimension,
            verbose=args.verbose,
        ))
    except KeyboardInterrupt:
        print("\n评测被中断")
        sys.exit(130)
    except Exception as e:
        print(f"评测失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 输出结果
    report.print_comparison()

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(report.to_json(), encoding="utf-8")
        print(f"\n📄 JSON 报告已保存: {out_path}")


if __name__ == "__main__":
    main()
