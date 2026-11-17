#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Token 首请求 input 观测器（不是账单）。

数据源：`${CODEX_HOME}/scripts/token-usage.sh --days N --top 200 --json`。
只比较每会话 first_request_input：按开工日期、模型、项目过滤，给出
基线窗口 / 瘦身后窗口的样本数、中位数、均值；样本不足时明确写“样本不足”。

固定声明：
  billing_claim = false
  claim_type = observational_first_request_input

退出码：
  0 正常输出（样本足或不足都算正常）
  2 输入/参数错误
  3 token-usage 调用或 JSON 解析失败
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Asia/Shanghai")
except Exception:  # pragma: no cover
    TZ = None

SCHEMA_VERSION = 1
TOOL = "token_experiment.py"
DEFAULT_TOKEN_USAGE = Path.home() / ".codex" / "scripts" / "token-usage.sh"
DEFAULT_MIN_SAMPLES = 5


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds") if TZ else datetime.now().astimezone().isoformat(timespec="seconds")


def parse_day(value: str | None, label: str) -> datetime | None:
    if not value:
        return None
    try:
        day = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{label} 必须是 YYYY-MM-DD: {value}") from exc
    if TZ:
        return day.replace(tzinfo=TZ)
    return day.astimezone()


def to_epoch(dt: datetime | None) -> int | None:
    return int(dt.timestamp()) if dt else None


def load_token_usage(args: argparse.Namespace) -> tuple[dict, str]:
    if args.input_json:
        path = Path(args.input_json).expanduser()
        try:
            return json.loads(path.read_text(encoding="utf-8")), f"file:{path}"
        except OSError as exc:
            raise RuntimeError(f"读不到 --input-json: {path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"--input-json 不是合法 JSON: {exc}") from exc

    script = Path(args.token_usage).expanduser()
    if not script.exists():
        raise RuntimeError(f"找不到 token-usage.sh: {script}")
    cmd = ["bash", str(script), "--days", str(args.days), "--top", str(args.top), "--json"]
    if args.model:
        cmd += ["--model", args.model]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout, check=False)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"调用 token-usage.sh 失败: {exc}") from exc
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        raise RuntimeError(f"token-usage.sh rc={proc.returncode}: {' | '.join(tail[-3:])}")
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"token-usage.sh 输出不是合法 JSON: {exc}") from exc
    return data, "token-usage.sh --days %d --top %d --json%s" % (
        args.days, args.top, f" --model {args.model}" if args.model else ""
    )


def session_model(session: dict) -> str:
    for p in session.get("providers") or []:
        p = str(p)
        if p.startswith("直连/"):
            return p.split("/", 1)[1]
    if len(session.get("providers") or []) == 1:
        return str(session["providers"][0])
    return "mixed/proxy"


def session_row(session: dict) -> dict:
    ts = session.get("first_timestamp")
    return {
        "id": session.get("id"),
        "first_request_input": int(session.get("first_request_input") or 0),
        "first_timestamp": ts,
        "first_time": datetime.fromtimestamp(ts, TZ).isoformat(timespec="seconds") if ts and TZ else None,
        "model": session_model(session),
        "cwd": session.get("cwd"),
        "requests": session.get("requests"),
        "peak_input": session.get("peak_input"),
    }


def filter_sessions(data: dict, args: argparse.Namespace) -> tuple[list[dict], dict]:
    sessions = data.get("sessions") or []
    start = to_epoch(parse_day(args.start, "--start"))
    base_start = to_epoch(parse_day(args.baseline_start, "--baseline-start"))
    base_end_day = parse_day(args.baseline_end, "--baseline-end")
    base_end = to_epoch(base_end_day + timedelta(days=1)) if base_end_day else None
    after_start = to_epoch(parse_day(args.after_start, "--after-start"))
    if args.baseline_start and not args.baseline_end:
        base_end_day = parse_day(args.baseline_start, "--baseline-start")
        base_end = to_epoch(base_end_day + timedelta(days=1))
    if args.baseline_end and not args.baseline_start:
        raise ValueError("--baseline-end 需要同时给 --baseline-start")

    kept: list[dict] = []
    excluded = {"no_first_input": 0, "before_start": 0, "project_mismatch": 0}
    for s in sessions:
        first_input = int(s.get("first_request_input") or 0)
        if first_input <= 0:
            excluded["no_first_input"] += 1
            continue
        ts = s.get("first_timestamp")
        if start is not None and (not ts or int(ts) < start):
            excluded["before_start"] += 1
            continue
        cwd = s.get("cwd") or ""
        if args.project and args.project not in str(cwd):
            excluded["project_mismatch"] += 1
            continue
        row = session_row(s)
        row["_ts"] = int(ts) if ts else 0
        kept.append(row)
    meta = {
        "input_sessions": len(sessions),
        "kept": len(kept),
        "excluded": excluded,
        "windows": {
            "start": args.start,
            "baseline_start": args.baseline_start,
            "baseline_end": args.baseline_end,
            "after_start": args.after_start,
            "baseline_epoch": [base_start, base_end],
            "after_epoch_start": after_start,
        },
    }
    return kept, meta


def summarize(rows: list[dict], min_samples: int, name: str) -> dict:
    values = [r["first_request_input"] for r in rows]
    n = len(values)
    summary = {
        "name": name,
        "sample_count": n,
        "median_first_request_input": statistics.median(values) if values else None,
        "mean_first_request_input": (sum(values) / n) if values else None,
        "min_first_request_input": min(values) if values else None,
        "max_first_request_input": max(values) if values else None,
        "min_samples_required": min_samples,
        "sample_sufficient": n >= min_samples,
        "sessions": sorted(rows, key=lambda r: r["first_request_input"]),
    }
    return summary


def build_payload(data: dict, rows: list[dict], meta: dict, args: argparse.Namespace, source: str) -> dict:
    base_start, base_end = meta["windows"]["baseline_epoch"]
    after_start = meta["windows"]["after_epoch_start"]

    baseline_rows = [r for r in rows if base_start is not None and base_end is not None and base_start <= r["_ts"] < base_end]
    after_rows = [r for r in rows if after_start is not None and r["_ts"] >= after_start]
    all_rows = list(rows)

    groups = {
        "all": summarize(all_rows, args.min_samples, "全部（过滤后）"),
        "baseline": summarize(baseline_rows, args.min_samples, "瘦身前基线窗口"),
        "after": summarize(after_rows, args.min_samples, "瘦身后窗口"),
    }

    observed_delta_pct = None
    if (
        groups["baseline"]["sample_sufficient"]
        and groups["after"]["sample_sufficient"]
        and groups["baseline"]["mean_first_request_input"]
    ):
        observed_delta_pct = (
            (groups["after"]["mean_first_request_input"] - groups["baseline"]["mean_first_request_input"])
            / groups["baseline"]["mean_first_request_input"]
            * 100
        )

    if not groups["baseline"]["sample_sufficient"] or not groups["after"]["sample_sufficient"]:
        conclusion = (
            "样本不足：baseline n=%d、after n=%d（每组至少 %d）；"
            "待 2026-11-12 后正式跑，不计算节省比例。"
            % (groups["baseline"]["sample_count"], groups["after"]["sample_count"], args.min_samples)
        )
        status = "INSUFFICIENT_SAMPLES"
    else:
        conclusion = (
            "观测：after 均值相对 baseline %+.2f%%；这是首请求 input 观测，不是账单节省，"
            "仍需排除模型、项目、缓存与请求类型混杂。"
            % observed_delta_pct
        )
        status = "OBSERVATION_ONLY"

    for g in groups.values():
        for r in g["sessions"]:
            r.pop("_ts", None)

    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL,
        "generated_at": now_iso(),
        "billing_claim": False,
        "claim_type": "observational_first_request_input",
        "metric": "每会话 first_request_input（首请求 input_tokens）",
        "source": source,
        "token_usage_days": data.get("days"),
        "filters": {
            "start": args.start,
            "model": args.model,
            "project": args.project,
            "baseline_start": args.baseline_start,
            "baseline_end": args.baseline_end,
            "after_start": args.after_start,
            "min_samples": args.min_samples,
        },
        "meta": meta,
        "groups": groups,
        "observed_delta_pct": observed_delta_pct,
        "status": status,
        "conclusion": conclusion,
        "caveats": [
            "first_request_input 受项目、模型、系统提示版本、缓存命中与请求类型影响，不能单独归因于瘦身。",
            "不把 cache_read 二次相加；token-usage.sh 已按 input+output 口径去重。",
            "样本不足时不给节省比例；正式窗口为 2026-11-12 之后。",
            "本输出不是账单，billing_claim=false。",
        ],
    }


def fmt_num(value: Any, digits: int = 1) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:,.{digits}f}"
    return f"{value:,}"


def render_markdown(payload: dict) -> str:
    lines: list[str] = [
        "# Token 首请求 input 观测（非账单）",
        "",
        f"- 生成：`{payload['generated_at']}`",
        f"- 数据源：`{payload['source']}`",
        f"- 指标：{payload['metric']}",
        f"- 结论状态：**{payload['status']}**",
        "- **billing_claim = false**；只写观测，不写账单节省。",
        "",
        "## 1 过滤条件",
        "",
        "| 项 | 值 |",
        "|---|---|",
    ]
    for k, v in payload["filters"].items():
        lines.append(f"| {k} | `{v}` |")
    lines += [
        "",
        f"- 输入会话 {payload['meta']['input_sessions']}；保留 {payload['meta']['kept']}；"
        f"排除 {payload['meta']['excluded']}",
        "",
        "## 2 分组统计",
        "",
        "| 组 | 样本数 | 中位数 | 均值 | 最小 | 最大 | 样本足够 |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for key in ("all", "baseline", "after"):
        g = payload["groups"][key]
        lines.append(
            f"| {g['name']} | {g['sample_count']} | {fmt_num(g['median_first_request_input'])} | "
            f"{fmt_num(g['mean_first_request_input'])} | {fmt_num(g['min_first_request_input'])} | "
            f"{fmt_num(g['max_first_request_input'])} | {'YES' if g['sample_sufficient'] else 'NO'} |"
        )
    lines += [
        "",
        f"- 观测差值（仅两组样本足够时计算）：`{fmt_num(payload['observed_delta_pct'], 2)}%`",
        "",
        "## 3 每会话 first_request_input",
        "",
    ]
    for key in ("baseline", "after", "all"):
        g = payload["groups"][key]
        lines.append(f"### {g['name']}")
        lines.append("")
        if not g["sessions"]:
            lines.append("无样本。")
            lines.append("")
            continue
        lines.append("| 会话 | 首请求 input | 时间 | 模型 | 请求数 | cwd |")
        lines.append("|---|---:|---|---|---:|---|")
        shown = g["sessions"][:50]
        for r in shown:
            lines.append(
                f"| `{str(r['id'])[:8]}` | {r['first_request_input']:,} | {r.get('first_time') or '—'} | "
                f"{r.get('model') or '—'} | {r.get('requests') or 0} | `{r.get('cwd') or '—'}` |"
            )
        if len(g["sessions"]) > len(shown):
            lines.append(f"| … | 其余 {len(g['sessions']) - len(shown)} 条省略 | | | | |")
        lines.append("")

    lines += [
        "## 4 结论",
        "",
        f"- {payload['conclusion']}",
        "",
        "## 5 限制",
        "",
    ]
    for c in payload["caveats"]:
        lines.append(f"- {c}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Token 首请求 input 观测（非账单）")
    parser.add_argument("--days", type=int, default=30, help="传给 token-usage.sh 的天数，默认 30")
    parser.add_argument("--top", type=int, default=200, help="传给 token-usage.sh 的会话上限，默认 200")
    parser.add_argument("--start", default=None, help="开工日期 YYYY-MM-DD；只保留此日期及之后的会话")
    parser.add_argument("--model", default=None, help="模型过滤（传给 token-usage.sh --model）")
    parser.add_argument("--project", default=None, help="项目过滤（匹配会话 cwd 子串）")
    parser.add_argument("--baseline-start", default=None, help="基线窗口开始 YYYY-MM-DD")
    parser.add_argument("--baseline-end", default=None, help="基线窗口结束 YYYY-MM-DD（含当天）")
    parser.add_argument("--after-start", default=None, help="瘦身后窗口开始 YYYY-MM-DD")
    parser.add_argument("--min-samples", type=int, default=DEFAULT_MIN_SAMPLES, help="每组最小样本，默认 5")
    parser.add_argument("--token-usage", default=str(DEFAULT_TOKEN_USAGE))
    parser.add_argument("--input-json", default=None, help="读取已保存的 token-usage JSON（测试/复算）")
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--md-out", default=None)
    parser.add_argument("--json", action="store_true", help="把完整 JSON 打到 stdout")
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args(argv)

    if args.min_samples <= 0:
        parser.error("--min-samples 必须是正整数")

    try:
        data, source = load_token_usage(args)
        rows, meta = filter_sessions(data, args)
        payload = build_payload(data, rows, meta, args, source)
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_out:
        p = Path(args.json_out).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.md_out:
        p = Path(args.md_out).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render_markdown(payload), encoding="utf-8")

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif not args.json_out and not args.md_out:
        print(render_markdown(payload))
    else:
        print(json.dumps({
            "tool": TOOL,
            "billing_claim": False,
            "status": payload["status"],
            "sample_count": {k: payload["groups"][k]["sample_count"] for k in ("baseline", "after", "all")},
            "observed_delta_pct": payload["observed_delta_pct"],
            "conclusion": payload["conclusion"],
            "json_out": args.json_out,
            "md_out": args.md_out,
        }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
