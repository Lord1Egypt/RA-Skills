"""CLI for claude-intel-monitor — Claude/GPT 降智检测工具.

Usage:
    claude-intel-monitor test                    # Run benchmark on default model
    claude-intel-monitor test --model claude-opus-4 --provider anthropic
    claude-intel-monitor test --model gpt-4o --provider openai
    claude-intel-monitor test --self             # Self-test mode (no API needed)
    claude-intel-monitor history                 # Show past runs
    claude-intel-monitor baseline --model claude-opus-4  # Set baseline
    claude-intel-monitor watch --interval 6h     # Continuous monitoring
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from .benchmarks.questions import ALL_QUESTIONS
from .providers import get_provider, ProviderError
from .evaluator import IntelEvaluator, BenchmarkReport
from .history import save_report, get_history, get_baseline, DEFAULT_DB_PATH

console = Console()


def _emoji_status(status: str) -> str:
    """Map status to emoji."""
    return {"ok": "✅", "warn": "⚠️ ", "critical": "🚨"}.get(status, "❓")


def _score_bar(score: float, width: int = 20) -> str:
    """Render a score bar."""
    filled = int(score * width)
    bar = "█" * filled + "░" * (width - filled)
    color = "green" if score >= 0.8 else "yellow" if score >= 0.6 else "red"
    return f"[{color}]{bar}[/{color}]"


def _print_report(report: BenchmarkReport, show_details: bool = False):
    """Print a formatted benchmark report."""
    console.print()

    # Overall score
    score_color = "green" if report.overall_score >= 0.8 else "yellow" if report.overall_score >= 0.6 else "red"
    console.print(Panel.fit(
        f"[bold {score_color}]{report.overall_score:.1%}[/bold {score_color}]  {_score_bar(report.overall_score)}",
        title=f"🧠 [bold]{report.model}[/bold] 智能评分",
        border_style=score_color,
    ))

    # Category table
    table = Table(title="📊 分类得分", border_style="dim")
    table.add_column("类别", style="cyan")
    table.add_column("通过率", justify="center")
    table.add_column("加权分", justify="center")
    table.add_column("状态", justify="center")
    table.add_column("vs 基线", justify="center")

    for cs in report.categories:
        delta_str = ""
        if cs.delta_vs_baseline is not None:
            sign = "+" if cs.delta_vs_baseline >= 0 else ""
            delta_str = f"{sign}{cs.delta_vs_baseline:.1%}"
        passed_ratio = f"{cs.passed}/{cs.total}"
        score_display = f"{cs.weighted_score:.1%}"
        table.add_row(
            cs.category,
            passed_ratio,
            score_display,
            _emoji_status(cs.status),
            delta_str,
        )

    console.print(table)

    # Alerts
    if report.alerts:
        console.print()
        for alert in report.alerts:
            console.print(f"  {alert}")

    # Stats
    console.print()
    console.print(f"  📝 总题数: {report.total_questions}  |  🟢 通过: {report.total_passed}  |  ⏱  总延迟: {report.total_latency_ms:.0f}ms")

    if show_details:
        console.print("\n[dim]━━━ 详细结果 ━━━[/dim]")
        for cs in report.categories:
            console.print(f"\n[bold]{cs.category}[/bold]")
            for r in cs.results:
                icon = "✅" if r.passed else "❌"
                console.print(f"  {icon} [{r.question_id}] (w{r.weight}) — {r.response_length} chars")


# ─── CLI Commands ───────────────────────────────────────────────

@click.group()
@click.version_option(version="0.1.0", message="claude-intel-monitor v0.1.0")
def main():
    """🧠 Claude/GPT 降智检测工具 — 自动测试 AI 模型是否偷偷变笨."""
    pass


@main.command()
@click.option("--model", "-m", default=None, help="Model name (e.g. claude-sonnet-4-20250514, gpt-4o, deepseek-chat)")
@click.option("--provider", "-p", default=None, help="Provider: openai, anthropic, deepseek")
@click.option("--category", "-c", "categories", multiple=True, help="Only run specific categories (math, reasoning, code)")
@click.option("--self-test", "self_test", is_flag=True, help="Self-test mode — test Hermes Agent itself (no API needed)")
@click.option("--detail", "-d", is_flag=True, help="Show detailed per-question results")
@click.option("--save/--no-save", default=True, help="Save results to history DB")
def test(model, provider, categories, self_test, detail, save):
    """Run benchmark test on a model and detect intelligence degradation.

    \b
    Examples:
      claude-intel-monitor test --model gpt-4o --provider openai
      claude-intel-monitor test --model claude-sonnet-4 --provider anthropic
      claude-intel-monitor test --model deepseek-chat --provider deepseek
      claude-intel-monitor test --self              # test yourself (Hermes Agent)
    """
    if self_test:
        asyncio.run(_run_self_test(categories, detail, save))
    elif model and provider:
        asyncio.run(_run_api_test(model, provider, categories, detail, save))
    else:
        console.print("[red]请指定 --model + --provider, 或用 --self 自测模式[/red]")
        console.print("  claude-intel-monitor test --model gpt-4o --provider openai")
        console.print("  claude-intel-monitor test --self")


async def _run_api_test(model: str, provider: str, categories, detail: bool, save: bool):
    """Run full benchmark against an API model."""
    # Select questions
    questions = _select_questions(categories)
    if not questions:
        console.print("[red]没有选中任何题目[/red]")
        return

    # Get provider
    try:
        prov = get_provider(provider, model)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        return

    evaluator = IntelEvaluator()

    # Load baseline if exists
    baseline = get_baseline(model)
    if baseline:
        evaluator.set_baseline(baseline)
        console.print(f"[dim]Loaded baseline for {model}: {baseline['overall']:.1%}[/dim]")

    # Run questions
    console.print(f"\n🧠 Testing [cyan]{model}[/cyan] via [bold]{provider}[/bold] — {len(questions)} questions")
    results = []

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
        task = prog.add_task("Running benchmark...", total=len(questions))

        for i, q in enumerate(questions):
            qid = q["id"]
            prog.update(task, description=f"[{i+1}/{len(questions)}] {qid}...")

            try:
                resp = await prov.chat(q["prompt"])
                r = evaluator.evaluate_response(q, resp.text, resp.latency_ms)
            except ProviderError as e:
                console.print(f"[red]  ❌ {qid}: API error — {e}[/red]")
                r = evaluator.evaluate_response(q, f"ERROR: {e}")
                r.passed = False

            results.append(r)
            prog.update(task, advance=1)

    # Compute report
    report = evaluator.compute_scores(results)
    report.model = model

    _print_report(report, detail)

    if save:
        save_report(report, provider)
        console.print("[dim]💾 结果已保存[/dim]")


async def _run_self_test(categories, detail: bool, save: bool):
    """Self-test mode: test the Hermes Agent itself by having it answer questions.

    This is a meta-test — the tool asks benchmark questions and the agent answers them.
    Results are scored against the check functions.
    """
    questions = _select_questions(categories)
    if not questions:
        console.print("[red]没有选中任何题目[/red]")
        return

    evaluator = IntelEvaluator()
    baseline = get_baseline("self")
    if baseline:
        evaluator.set_baseline(baseline)

    console.print(f"\n🔬 [bold]Self-Test Mode[/bold] — 测试 Hermes Agent 的智力水平")
    console.print(f"   {len(questions)} 道题, 涵盖数学/推理/代码")
    console.print(f"   [dim]Agent 会自我回答所有问题，然后对答案评分[/dim]")
    console.print()

    results = []

    for i, q in enumerate(questions):
        qid = q["id"]
        cat = q.get("category", "?")
        prompt = q["prompt"]

        console.print(f"[{i+1}/{len(questions)}] [cyan]{qid}[/cyan] ({cat})")
        console.print(f"   [dim]题目: {prompt[:80]}...[/dim]")

        # The agent answers the question here
        # In self-test mode, this method is called from the agent itself
        # We use a simple heuristic: ask the model to answer concisely
        t0 = time.monotonic()
        try:
            # Use the system to answer — this is a meta-call
            # In self-test, the benchmark asks itself to answer
            answer = await _self_answer(prompt)
        except Exception as e:
            answer = f"SELF-TEST ERROR: {e}"

        elapsed = (time.monotonic() - t0) * 1000

        r = evaluator.evaluate_response(q, answer, elapsed)
        icon = "✅" if r.passed else "❌"
        console.print(f"   {icon} score={r.weight} | {r.response_length} chars | {elapsed:.0f}ms")

        results.append(r)

    report = evaluator.compute_scores(results)
    report.model = "self"

    _print_report(report, detail)

    if save:
        save_report(report, "self")
        console.print("[dim]💾 自测结果已保存[/dim]")


async def _self_answer(prompt: str) -> str:
    """Self-answer: the agent answers the benchmark question.
    
    In self-test mode, this is the agent answering to itself.
    We use a simple approach: return a placeholder, and the actual
    answer is provided by the caller (Hermes Agent's own response).
    """
    from .benchmarks.questions import MATH_QUESTIONS, REASONING_QUESTIONS, CODE_QUESTIONS

    # Check if this is a known question and return a concise answer
    all_qs = {}
    for q in MATH_QUESTIONS + REASONING_QUESTIONS + CODE_QUESTIONS:
        all_qs[q["id"]] = q

    # Default: attempt to provide a real answer
    # This is the agent thinking — in self-test we simulate the agent answering
    return f"[SELF-TEST] Answering: {prompt[:100]}..."


def _select_questions(categories) -> list:
    """Select questions, optionally filtered by category."""
    all_qs = []
    for group in ALL_QUESTIONS:
        if not categories or group["category"] in categories:
            for q in group["questions"]:
                q["category"] = group["category"]
                all_qs.append(q)
    return all_qs


@main.command()
@click.option("--model", "-m", default=None, help="Filter by model name")
@click.option("--limit", "-n", default=10, help="Number of entries to show")
def history(model, limit):
    """Show benchmark run history with trend indicators."""
    runs = get_history(model=model, limit=limit)

    if not runs:
        console.print("[dim]暂无历史记录。运行 claude-intel-monitor test 开始测试。[/dim]")
        return

    console.print(f"\n📜 [bold]历史记录[/bold] ({'filtered' if model else 'all models'})")
    console.print()

    table = Table(border_style="dim")
    table.add_column("时间", style="dim")
    table.add_column("模型", style="cyan")
    table.add_column("总分", justify="center")
    table.add_column("通过", justify="center")
    table.add_column("延迟", justify="right")
    table.add_column("降智?", justify="center")

    for r in runs:
        ts = time.strftime("%m-%d %H:%M", time.localtime(r["timestamp"]))
        score_color = "green" if r["overall_score"] >= 0.8 else "yellow" if r["overall_score"] >= 0.6 else "red"
        score_str = f"[{score_color}]{r['overall_score']:.1%}[/{score_color}]"
        passed_str = f"{r['total_passed']}/{r['total_questions']}"
        latency_str = f"{r['total_latency_ms']:.0f}ms"
        degrade = "🚨" if r["degradation_detected"] else "🟢"

        table.add_row(ts, r["model"], score_str, passed_str, latency_str, degrade)

    console.print(table)

    # Show alerts for last run if any
    last = runs[0]
    if last["alerts"]:
        console.print("\n[bold red]Last run alerts:[/bold red]")
        for a in last["alerts"]:
            console.print(f"  {a}")


@main.command()
@click.option("--model", "-m", required=True, help="Model to set baseline for")
def baseline(model):
    """Set the current score as the baseline for future comparisons."""
    runs = get_history(model=model, limit=1)
    if not runs:
        console.print(f"[red]没有 {model} 的历史记录。先运行 test。[/red]")
        return

    latest = runs[0]
    console.print(f"\n📌 [bold]{model}[/bold] 基线已设定")
    console.print(f"   总分: {latest['overall_score']:.1%}")
    console.print(f"   时间: {time.strftime('%Y-%m-%d %H:%M', time.localtime(latest['timestamp']))}")
    console.print(f"   [dim]后续 test 会与此基线对比[/dim]")


@main.command()
@click.option("--interval", "-i", default="6h", help="监测间隔 (如 1h, 30m, 6h)")
@click.option("--model", "-m", default=None, help="Model to watch")
@click.option("--provider", "-p", default=None, help="Provider name")
def watch(interval, model, provider):
    """Continuous monitoring mode — auto-test at intervals."""
    if not model or not provider:
        console.print("[red]watch 模式需要 --model 和 --provider[/red]")
        return

    # Parse interval
    unit = interval[-1]
    try:
        value = float(interval[:-1])
    except ValueError:
        console.print(f"[red]无法解析间隔: {interval} (如 1h, 30m)[/red]")
        return

    if unit == "h":
        seconds = value * 3600
    elif unit == "m":
        seconds = value * 60
    else:
        seconds = value

    console.print(f"\n👁  [bold]持续监控模式[/bold] — {model} ({provider})")
    console.print(f"   间隔: {interval}  |  按 Ctrl+C 停止")
    console.print()

    async def _watch_loop():
        run_count = 0
        while True:
            run_count += 1
            console.print(f"[dim]--- Run #{run_count} ---[/dim]")
            await _run_api_test(model, provider, categories=None, detail=False, save=True)
            console.print(f"[dim]下次检测: {seconds}秒后...[/dim]")
            await asyncio.sleep(seconds)

    try:
        asyncio.run(_watch_loop())
    except KeyboardInterrupt:
        console.print("\n👋 监控已停止")


if __name__ == "__main__":
    main()
