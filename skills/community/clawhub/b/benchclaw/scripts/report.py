"""
BenchClaw 报表生成模块。

读取 ../temp/results.json，生成：
  - ../data/report_summary.md   简要报表（汇总 + 分类汇总）
  - ../data/report_detail.md    详细报表（汇总 + 分类汇总 + 每题详情）

用法：
  python report.py
  python report.py --input ../temp/results.json
"""
from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any


# ---------- 路径 ----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(SCRIPT_DIR, "..", "temp", "results.json")
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")

CATEGORY_NAMES: dict[str, str] = {
    "capability": "能力",
    "config":     "配置",
    "security":   "安全",
    "hardware":   "硬件",
    "permission": "权限",
}

SCORE_BAR_WIDTH = 20  # 进度条字符宽度


# ---------- 工具函数 ----------

def _bar(score: float, max_score: float, width: int = SCORE_BAR_WIDTH) -> str:
    """生成文字进度条，如 ████████░░░░ 75%"""
    if max_score <= 0:
        pct = 0.0
    else:
        pct = min(score / max_score, 1.0)
    filled = round(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"`{bar}` {pct * 100:.1f}%"


def _status_icon(r: dict[str, Any]) -> str:
    if r.get("success"):
        return "✅"
    error = r.get("error", "")
    if "timeout" in error:
        return "⏱️"
    if "rate" in r.get("stderr", "").lower() or "rate_limit" in error.lower():
        return "🚫"
    return "❌"


def _fmt_duration(sec: float) -> str:
    if sec >= 60:
        return f"{sec / 60:.1f} min"
    return f"{sec:.1f} s"


def _fmt_tokens(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def _category_label(cat: str) -> str:
    return CATEGORY_NAMES.get(cat, cat)


def _fmt_cost(tokens: int, cost_per_1m: float) -> str:
    """根据 token 数和单价计算预估费用，返回格式化字符串。"""
    cost = tokens / 1_000_000 * cost_per_1m
    return f"${cost:.4f}"


def _render_model_cost(data: dict[str, Any], totals: dict[str, Any]) -> list[str]:
    """生成模型计费信息区块，返回 Markdown 行列表。若无计费信息则返回空列表。"""
    model_cost = data.get("model_cost")
    if not isinstance(model_cost, dict):
        return []

    model_name     = model_cost.get("model_name", "—")
    input_per_1m   = model_cost.get("input_cost_per_1M", 0.0)
    output_per_1m  = model_cost.get("output_cost_per_1M", 0.0)
    currency       = model_cost.get("currency", "USD")

    input_tokens        = totals.get("input_tokens", 0)
    output_tokens       = totals.get("output_tokens", 0)
    cache_read_tokens   = totals.get("cache_read_tokens", 0)
    cache_write_tokens  = totals.get("cache_write_tokens", 0)
    total_tokens        = totals.get("total_tokens", 0)

    input_cost  = input_tokens  / 1_000_000 * input_per_1m
    output_cost = output_tokens / 1_000_000 * output_per_1m
    total_cost  = input_cost + output_cost

    lines = [
        "## 模型计费信息",
        "",
        f"| 项目 | 数值 |",
        f"|------|------|",
        f"| 模型 | `{model_name}` |",
        f"| 输入单价 | {input_per_1m} {currency} / 1M tokens |",
        f"| 输出单价 | {output_per_1m} {currency} / 1M tokens |",
        f"| 输入 Tokens | {_fmt_tokens(input_tokens)} → **{input_cost:.4f} {currency}** |",
        f"| 输出 Tokens | {_fmt_tokens(output_tokens)} → **{output_cost:.4f} {currency}** |",
        f"| Cache Read Tokens | {_fmt_tokens(cache_read_tokens)} |",
        f"| Cache Write Tokens | {_fmt_tokens(cache_write_tokens)} |",
        f"| 合计 Tokens | {_fmt_tokens(total_tokens)} |",
        f"| 预估总费用 | **{total_cost:.4f} {currency}** |",
        "",
        "---",
        "",
    ]
    return lines


def _render_leaderboard(data: dict[str, Any]) -> list[str]:
    """生成排行榜区块，返回 Markdown 行列表。若无排行榜数据则返回空列表。"""
    leaderboard = data.get("leaderboard")
    if not isinstance(leaderboard, dict):
        return []
    percentiles = leaderboard.get("percentiles")
    if not isinstance(percentiles, dict):
        return []

    total_pct   = percentiles.get("total")
    sample_size = leaderboard.get("sample_size")
    lb_url      = leaderboard.get("leaderboard_url", "")
    note        = leaderboard.get("note", "")
    updated_at  = leaderboard.get("updated_at", "")

    # 从 category_stats 中获取真实的 category_label，与 server.py CATEGORY_ORDER 对应
    # CATEGORY_ORDER = ["capability", "config", "security", "hardware", "permission"]
    _cat_stats: dict = (data.get("stats") or {}).get("category_stats") or {}
    _cat_order = ["capability", "config", "security", "hardware", "permission"]
    cat_map: dict[str, str] = {}
    for idx, cat_key in enumerate(_cat_order, start=1):
        cat_label = _cat_stats.get(cat_key, {}).get("category_label") or cat_key
        cat_map[f"s{idx}"] = f"{cat_label}（{cat_key}）"

    lines: list[str] = [
        "## 全国排名",
        "",
    ]

    if total_pct is not None:
        lines.append(f"> 🏆 **太棒了，您的分数超越了全国 {total_pct}% 的用户！**")
        lines.append("")

    lines += [
        "| 维度 | 超越比例 |",
        "|------|:--------:|",
        f"| **总分** | **{total_pct}%** |" if total_pct is not None else "| **总分** | — |",
    ]
    for key, label in cat_map.items():
        pct = percentiles.get(key)
        lines.append(f"| {label} | {pct}% |" if pct is not None else f"| {label} | — |")

    lines.append("")

    meta: list[str] = []
    if sample_size:
        meta.append(f"参与评测用户数：**{sample_size}**")
    if updated_at:
        meta.append(f"数据更新时间：{updated_at[:10]}")
    if note:
        meta.append(f"说明：{note}")
    for m in meta:
        lines.append(f"- {m}")
    if meta:
        lines.append("")

    if lb_url:
        lines += [f"[查看完整排行榜]({lb_url})", ""]

    lines += ["---", ""]
    return lines


# ---------- 数据处理 ----------

def _load(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _compute_totals(data: dict[str, Any]) -> dict[str, Any]:
    results: list[dict] = data.get("results", [])
    total_score    = sum(r.get("score", 0) for r in results)
    total_accuracy = sum(r.get("accuracy_score", 0) for r in results)
    total_max      = sum(r.get("max_accuracy_score", 0) for r in results)
    total_real_accuracy     = sum(r.get("real_accuracy_score", 0) for r in results)
    total_count    = len(results)
    succeeded      = sum(1 for r in results if r.get("success"))
    total_duration = sum(r.get("duration_sec", 0) or 0 for r in results)
    total_tokens        = sum(r.get("total_tokens", 0) or 0 for r in results)
    input_tokens        = sum(r.get("input_tokens", 0) or 0 for r in results)
    output_tokens       = sum(r.get("output_tokens", 0) or 0 for r in results)
    cache_read_tokens   = sum(r.get("cache_read_tokens", 0) or 0 for r in results)
    cache_write_tokens  = sum(r.get("cache_write_tokens", 0) or 0 for r in results)
    score_rate     = round(total_score / total_max * 100, 1) if total_max > 0 else 0.0
    total_tps_score = sum(r.get("tps_score", 0) or 0 for r in results)
    tps_list       = [r.get("tps", 0) for r in results if (r.get("tps") or 0) > 0]
    avg_tps        = round(sum(tps_list) / len(tps_list), 2) if tps_list else 0.0
    return {
        "total_score": total_score,
        "total_accuracy": total_accuracy,
        "total_real_accuracy": total_real_accuracy,
        "total_max": total_max,
        "score_rate": score_rate,
        "total_count": total_count,
        "succeeded": succeeded,
        "failed": total_count - succeeded,
        "total_duration": total_duration,
        "total_tokens": total_tokens,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_tokens": cache_read_tokens,
        "cache_write_tokens": cache_write_tokens,
        "total_tps_score": total_tps_score,
        "avg_tps": avg_tps,
    }


# ---------- 简要报表 ----------

def _render_summary(data: dict[str, Any], totals: dict[str, Any]) -> str:
    session_id = data.get("openclaw_session_id") or data.get("session_id", "—")
    generated  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _stats = data.get("stats") or {}
    cat_stats: dict[str, dict] = _stats.get("category_stats") or data.get("category_stats", {})

    t = totals
    lines: list[str] = []

    # ── 标题 ──
    lines += [
        "# BenchClaw 评测简报",
        "",
        f"> 生成时间：{generated}　|　Session：`{session_id}`",
        "",
        "---",
        "",
    ]

    # ── 总体评分 ──
    lines += [
        "## 总体评分",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总得分 | **{t['total_score']}** |",
        f"| 准确度分 | **{t['total_real_accuracy']}** |",
        f"| 速度分合计 | **{t['total_tps_score']}** |",
        f"| 准确率 | {_bar(t['total_accuracy'], t['total_max'])} |",
        f"| 题目总数 | {t['total_count']} 题 |",
        f"| 通过 / 失败 | ✅ {t['succeeded']}　❌ {t['failed']} |",
        f"| 总耗时 | {_fmt_duration(t['total_duration'])} |",
        f"| Token 消耗 | {_fmt_tokens(t['total_tokens'])}（输入 {_fmt_tokens(t['input_tokens'])} / 输出 {_fmt_tokens(t['output_tokens'])}）|",
        f"| Cache Read Tokens | {_fmt_tokens(t['cache_read_tokens'])} |",
        f"| Cache Write Tokens | {_fmt_tokens(t['cache_write_tokens'])} |",
        f"| 平均 TPS | {t['avg_tps']} tokens/s |",
        "",
        "---",
        "",
    ]

    # ── 模型计费 ──
    lines += _render_model_cost(data, t)

    # ── 分类汇总 ──
    lines += [
        "## 分类汇总",
        "",
        "| 分类 | 题数 | 总分 | 准确度分 | 速度分 | 准确率 | 通过率 |",
        "|------|:----:|-----:|---------:|-------:|--------|--------|",
    ]
    for cat, stats in sorted(cat_stats.items()):
        label        = _category_label(cat)
        count        = stats["count"]
        score        = stats["score"]
        real_accuracy     = stats.get("real_accuracy_score", 0)
        accuracy     = stats.get("accuracy_score", 0)
        max_s        = stats["max_accuracy_score"]
        tps_score    = stats.get("tps_score", 0)
        succ         = stats["succeeded"]
        pass_rate    = f"{succ}/{count} ({succ/count*100:.0f}%)" if count else "—"
        bar          = _bar(accuracy, max_s)
        lines.append(f"| {label} (`{cat}`) | {count} | {score} | {real_accuracy} | {tps_score} | {bar} | {pass_rate} |")

    lines += [
        "",
        "---",
        "",
        "> *详细每题信息请查看 `report_detail.md`*",
        "",
    ]

    # ── 三维瓶颈诊断 ──
    hw = data.get("hardware_stats") or {}
    api_ping = data.get("api_ping_ms")

    diag_lines = []

    # 模型速度
    avg_tps = t.get("avg_tps", 0)
    if avg_tps > 5000:
        tps_label = "⚡ 极快"
    elif avg_tps > 2000:
        tps_label = "✅ 正常"
    elif avg_tps > 1000:
        tps_label = "🟡 偏慢"
    else:
        tps_label = "🔴 过慢"
    diag_lines.append(f"🤖 **模型速度**：{avg_tps} TPS {tps_label}")

    # 硬件信息分析
    if hw:
        cpu_peak = hw.get("cpu_peak_percent", 0)
        cpu_avg = hw.get("cpu_avg_percent", 0)
        mem_avail = hw.get("mem_min_available_gb", 0)
        mem_total = hw.get("mem_total_gb", 0)

        if cpu_peak > 80:
            cpu_label = "🔴 成为瓶颈"
        elif cpu_peak > 60:
            cpu_label = "🟡 紧张"
        else:
            cpu_label = "✅ 充裕"

        if mem_avail < 1:
            mem_label = "🔴 不足"
        elif mem_avail < 2:
            mem_label = "🟡 紧张"
        else:
            mem_label = "✅ 充裕"

        diag_lines.append(f"💻 **CPU**：峰值 {cpu_peak}% {cpu_label}（平均 {cpu_avg}%）")
        diag_lines.append(f"🧠 **内存**：总量 {mem_total} GB，最小可用 {mem_avail} GB {mem_label}")

    if diag_lines:
        lines += [
            "## 三维瓶颈诊断",
            "",
        ]
        for line in diag_lines:
            lines.append(line)
            lines.append("")
        lines += ["---", ""]

    # ── 全国排名 ──
    lines += _render_leaderboard(data)


    return "\n".join(lines)


# ---------- 详细报表 ----------

def _render_detail(data: dict[str, Any], totals: dict[str, Any]) -> str:
    session_id = data.get("openclaw_session_id") or data.get("session_id", "—")
    generated  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _stats = data.get("stats") or {}
    cat_stats: dict[str, dict] = _stats.get("category_stats") or data.get("category_stats", {})
    results: list[dict] = data.get("results", [])

    t = totals
    lines: list[str] = []

    # ── 标题 ──
    lines += [
        "# BenchClaw 评测详细报告",
        "",
        f"> 生成时间：{generated}　|　Session：`{session_id}`",
        "",
        "---",
        "",
    ]

    # ── 总体评分（与简报相同） ──
    lines += [
        "## 总体评分",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总得分 | **{t['total_score']}** |",
        f"| 准确度分 | **{t['total_real_accuracy']}** |",
        f"| 速度分合计 | **{t['total_tps_score']}** |",
        f"| 准确率 | {_bar(t['total_accuracy'], t['total_max'])} |",
        f"| 题目总数 | {t['total_count']} 题 |",
        f"| 通过 / 失败 | ✅ {t['succeeded']}　❌ {t['failed']} |",
        f"| 总耗时 | {_fmt_duration(t['total_duration'])} |",
        f"| Token 消耗 | {_fmt_tokens(t['total_tokens'])}（输入 {_fmt_tokens(t['input_tokens'])} / 输出 {_fmt_tokens(t['output_tokens'])}）|",
        f"| Cache Read Tokens | {_fmt_tokens(t['cache_read_tokens'])} |",
        f"| Cache Write Tokens | {_fmt_tokens(t['cache_write_tokens'])} |",
        f"| 平均 TPS | {t['avg_tps']} tokens/s |",
        "",
        "---",
        "",
    ]

    # ── 模型计费 ──
    lines += _render_model_cost(data, t)

    # ── 分类汇总 ──
    lines += [
        "## 分类汇总",
        "",
        "| 分类 | 题数 | 总分 | 准确度分 | 速度分 | 准确率 | 通过率 |",
        "|------|:----:|-----:|---------:|-------:|--------|--------|",
    ]
    for cat, stats in sorted(cat_stats.items()):
        label        = _category_label(cat)
        count        = stats["count"]
        score        = stats["score"]
        real_accuracy     = stats.get("real_accuracy_score", 0)
        accuracy     = stats.get("accuracy_score", 0)
        max_s        = stats["max_accuracy_score"]
        tps_score    = stats.get("tps_score", 0)
        succ         = stats["succeeded"]
        pass_rate    = f"{succ}/{count} ({succ/count*100:.0f}%)" if count else "—"
        bar          = _bar(accuracy, max_s)
        lines.append(f"| {label} (`{cat}`) | {count} | {score} | {real_accuracy} | {tps_score} | {bar} | {pass_rate} |")

    lines += ["", "---", ""]

    # ── 每分类题目详情 ──
    lines.append("## 题目详情\n")

    # 按分类分组
    by_cat: dict[str, list[dict]] = {}
    for r in results:
        cat = r.get("category", "unknown")
        by_cat.setdefault(cat, []).append(r)

    for cat in sorted(by_cat.keys()):
        cat_results = by_cat[cat]
        label = _category_label(cat)
        lines += [
            f"### {label}（`{cat}`）",
            "",
            "| 题号 | 状态 | 总分 | 准确度分 | 速度分 | TPS | 耗时 | Tokens | 错误 |",
            "|------|:----:|:----:|---------:|-------:|----:|-----:|-------:|------|",
        ]
        for r in cat_results:
            tid           = r.get("id", "?")
            icon          = _status_icon(r)
            score         = r.get("score", 0)
            real_accuracy      = r.get("real_accuracy_score", 0)
            accuracy      = r.get("accuracy_score", 0)
            max_s         = r.get("max_accuracy_score", 0)
            tps           = r.get("tps", 0)
            tps_score     = r.get("tps_score", 0)
            dur           = _fmt_duration(r.get("duration_sec") or 0)
            tokens        = _fmt_tokens(r.get("total_tokens") or 0)
            err           = r.get("error", "")
            if err and len(err) > 40:
                err = err[:40] + "…"
            lines.append(f"| `{tid}` | {icon} | {score} | {real_accuracy} | {tps_score} | {tps} | {dur} | {tokens} | {err} |")

        lines.append("")

        # 每题展开块
        for r in cat_results:
            tid           = r.get("id", "?")
            icon          = _status_icon(r)
            score         = r.get("score", 0)
            real_accuracy      = r.get("real_accuracy_score", 0)
            accuracy      = r.get("accuracy_score", 0)
            max_s         = r.get("max_accuracy_score", 0)
            tps           = r.get("tps", 0)
            tps_score     = r.get("tps_score", 0)
            dur           = _fmt_duration(r.get("duration_sec") or 0)
            in_tok        = _fmt_tokens(r.get("input_tokens") or 0)
            out_tok       = _fmt_tokens(r.get("output_tokens") or 0)
            tot_tok       = _fmt_tokens(r.get("total_tokens") or 0)
            err           = r.get("error", "") or ""
            stderr        = (r.get("stderr") or "").strip()
            output        = (r.get("stdout") or "").strip()

            lines += [
                f"#### {icon} `{tid}` — 总分 {score}（准确度 {real_accuracy} + 速度 {tps_score}）",
                "",
                f"| 字段 | 值 |",
                f"|------|-----|",
                f"| 总分 | {score} |",
                f"| 准确度分 | {real_accuracy} |",
                f"| 速度分 | {tps_score} |",
                f"| 耗时 | {dur} |",
                f"| TPS | {tps} tokens/s |",
                f"| Token | 输入 {in_tok} / 输出 {out_tok} / 合计 {tot_tok} |",
            ]
            if err:
                lines.append(f"| 错误 | `{err}` |")
            lines.append("")

            if output:
                # 截取前 500 字符避免报表过长
                preview = output[:500].replace("```", "'''")
                if len(output) > 500:
                    preview += f"\n\n*…（共 {len(output)} 字符，已截断）*"
                lines += [
                    "<details>",
                    "<summary>Agent 输出（点击展开）</summary>",
                    "",
                    "```",
                    preview,
                    "```",
                    "",
                    "</details>",
                    "",
                ]

            if stderr:
                preview = stderr[:300].replace("```", "'''")
                if len(stderr) > 300:
                    preview += "\n…（已截断）"
                lines += [
                    "<details>",
                    "<summary>stderr（点击展开）</summary>",
                    "",
                    "```",
                    preview,
                    "```",
                    "",
                    "</details>",
                    "",
                ]

        lines += ["---", ""]

    # ── 全国排名 ──
    lines += _render_leaderboard(data)

    return "\n".join(lines)


# ---------- 主入口 ----------

def generate_reports_from_dict(data: dict[str, Any]) -> tuple[str, str]:
    """
    直接接受 summary dict，生成简报和详细报告，返回 (简报路径, 详细报告路径)。
    """
    totals = _compute_totals(data)

    os.makedirs(DATA_DIR, exist_ok=True)
    summary_path = os.path.join(DATA_DIR, "report_summary.md")
    detail_path  = os.path.join(DATA_DIR, "report_detail.md")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(_render_summary(data, totals))

    with open(detail_path, "w", encoding="utf-8") as f:
        f.write(_render_detail(data, totals))

    return summary_path, detail_path


def generate_reports(input_path: str) -> tuple[str, str]:
    """
    读取 results.json，返回 (简报路径, 详细报告路径)。
    """
    data = _load(input_path)
    return generate_reports_from_dict(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="BenchClaw 报表生成器")
    parser.add_argument(
        "--input", "-i",
        default=DEFAULT_INPUT,
        help=f"results.json 路径（默认：{DEFAULT_INPUT}）",
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"错误：找不到输入文件 {input_path}")
        raise SystemExit(1)

    summary_path, detail_path = generate_reports(input_path)
    print(f"简要报表：{summary_path}")
    print(f"详细报表：{detail_path}")


if __name__ == "__main__":
    main()
