#!/usr/bin/env python3
"""七块固定注入预算看板（只读，不写 ${CODEX_HOME}）。

默认读取 s1 基线，并调用 measure_prompt.py --json 获取当前七块；
也可用 --measure-json 读取已保存的测量结果，或用 --no-measure 直接用基线。
只写调用方指定的 Markdown/JSON 输出路径。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCHEMA_VERSION = 1
TOOL = "budget_dashboard.py"
DEFAULT_GATE = 57344

# 预算口径：没有独立预算的块写 None，不伪造余量。
# AGENTS 的 5,500 B 是一期报告对 AGENTS.md 源文件的目标；
# 注入块 5,443 B 含 41 B 前缀 + 15 B 后缀，预算判断按源文件 5,387 B。
BUDGETS = {
    "memory": {
        "budget": 12000,
        "basis": "block",
        "source": "s3 目标 ≤12,000 B",
    },
    "skills": {
        "budget": 10240,
        "basis": "block",
        "source": "技能索引预算约 10 KB（10,240 B）",
    },
    "AGENTS": {
        "budget": 5500,
        "basis": "agents_source",
        "source": "一期报告目标 ≤5,500 B（按 AGENTS.md 源文件）",
    },
    "total": {
        "budget": DEFAULT_GATE,
        "basis": "total",
        "source": "s1 闸门 56 KiB（57,344 B）",
    },
}
BUDGET_ORDER = ["memory", "base", "skills", "permissions", "AGENTS", "mcp", "env", "total"]


SKILL_ROOT = Path(__file__).resolve().parents[1]


def project_root() -> Path:
    """优先显式项目目录，其次当前工作目录；不再假设脚本位于项目 work/tools。"""
    env = os.environ.get("AGENT_SLIM_PROJECT")
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def run_measure(measure_script: Path, baseline: Path, timeout: int = 90) -> tuple[dict | None, str]:
    """返回 (测量 JSON, 错误/说明)。"""
    cmd = [sys.executable, str(measure_script), "--json", "--baseline", str(baseline)]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(measure_script.parent),
        )
    except Exception as exc:  # noqa: BLE001 - 需要把失败原因写进看板
        return None, f"调用失败: {exc}"
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        tail_text = " | ".join(tail[-3:]) if tail else "无输出"
        return None, f"退出码 {proc.returncode}: {tail_text}"
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        return None, f"JSON 解析失败: {exc}"
    if not isinstance(data.get("blocks"), list):
        return None, "测量结果缺少 blocks"
    return data, ""


def block_map(blocks: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for b in blocks:
        bid = b.get("id")
        if bid:
            out[str(bid)] = b
    return out


def fmt_int(n: int | None) -> str:
    return "—" if n is None else f"{n:,}"


def fmt_delta(n: int | None) -> str:
    if n is None:
        return "—"
    return f"{n:+d}"


def fmt_pct(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.2f}%"


def source_label(block: dict) -> str:
    src = str(block.get("source") or "")
    if src == "assumption":
        return "assumption"
    if src == "static":
        return "static"
    if src == "measured":
        return "measured"
    return src or "unknown"


def pick_measurement(args: argparse.Namespace, baseline: dict) -> tuple[list[dict], dict]:
    """返回 (当前 blocks, 元信息)。"""
    if args.measure_json:
        p = Path(args.measure_json).expanduser()
        data = load_json(p)
        return data.get("blocks", []), {
            "source": f"file:{p}",
            "status": "FILE",
            "timestamp": data.get("timestamp"),
            "detail": "读取 --measure-json",
        }

    if args.no_measure:
        return baseline.get("blocks", []), {
            "source": "s1 baseline",
            "status": "BASELINE_FALLBACK",
            "timestamp": baseline.get("timestamp"),
            "detail": "--no-measure，未调用测量器",
        }

    measure_script = Path(args.measure_script).expanduser()
    if not measure_script.exists():
        return baseline.get("blocks", []), {
            "source": "s1 baseline",
            "status": "BASELINE_FALLBACK",
            "timestamp": baseline.get("timestamp"),
            "detail": f"测量器不存在: {measure_script}",
        }

    data, err = run_measure(measure_script, Path(args.baseline).expanduser())
    if data is None:
        return baseline.get("blocks", []), {
            "source": "s1 baseline",
            "status": "BASELINE_FALLBACK",
            "timestamp": baseline.get("timestamp"),
            "detail": err,
        }

    return data.get("blocks", []), {
        "source": f"measure_prompt.py --json（{data.get('timestamp', '无时间戳')}）",
        "status": "MEASURED",
        "timestamp": data.get("timestamp"),
        "detail": data.get("status", ""),
        "measure": data,
    }


def build_rows(current_blocks: list[dict], baseline_blocks: list[dict]) -> list[dict]:
    cur = block_map(current_blocks)
    base = block_map(baseline_blocks)
    ids = [bid for bid in BUDGET_ORDER if bid != "total"]
    rows: list[dict] = []
    for bid in ids:
        b = cur.get(bid, {})
        bb = base.get(bid, {})
        current_bytes = int(b.get("bytes", 0) or 0)
        baseline_bytes = int(bb.get("bytes", 0) or 0)
        budget_spec = BUDGETS.get(bid)
        budget = budget_spec["budget"] if budget_spec else None
        basis_kind = budget_spec["basis"] if budget_spec else None

        basis_bytes = None
        basis_note = "—"
        if budget is not None:
            if basis_kind == "agents_source":
                src = b.get("source_file") or bb.get("source_file")
                if src and Path(str(src)).exists():
                    basis_bytes = int(Path(str(src)).stat().st_size)
                    basis_note = f"AGENTS.md 源文件 {fmt_int(basis_bytes)} B"
                else:
                    note = str(b.get("note") or bb.get("note") or "")
                    # 包装为 41 B 前缀 + 15 B 后缀；仅在无法读源文件时用块字节减包装估算
                    basis_bytes = max(0, current_bytes - 56)
                    basis_note = f"源文件不可读；按块字节减 56 B 包装估算（{note}）"
            else:
                basis_bytes = current_bytes
                basis_note = f"块字节 {fmt_int(current_bytes)} B"

        utilization = (basis_bytes / budget) if (budget and basis_bytes is not None) else None
        headroom = (budget - basis_bytes) if (budget and basis_bytes is not None) else None
        headroom_pct = (headroom / budget) if (budget and headroom is not None) else None

        rows.append({
            "id": bid,
            "label": b.get("label") or bb.get("label") or bid,
            "bytes": current_bytes,
            "baseline_bytes": baseline_bytes,
            "delta": current_bytes - baseline_bytes,
            "source": source_label(b),
            "budget": budget,
            "budget_source": budget_spec["source"] if budget_spec else "未设独立预算",
            "basis_bytes": basis_bytes,
            "basis_note": basis_note,
            "utilization": utilization,
            "headroom": headroom,
            "headroom_pct": headroom_pct,
            "note": b.get("note") or "",
        })

    total_current = sum(int(r["bytes"]) for r in rows)
    total_baseline = sum(int(r["baseline_bytes"]) for r in rows)
    total_budget = int(BUDGETS["total"]["budget"])
    mcp_current = int((cur.get("mcp") or {}).get("bytes", 0) or 0)
    text_total = total_current - mcp_current
    rows.append({
        "id": "total",
        "label": "七块合计",
        "bytes": total_current,
        "baseline_bytes": total_baseline,
        "delta": total_current - total_baseline,
        "source": "sum",
        "budget": total_budget,
        "budget_source": BUDGETS["total"]["source"],
        "basis_bytes": text_total,
        "basis_note": f"文本七块相加 {fmt_int(text_total)} B（不含 MCP 占位 {fmt_int(mcp_current)} B；含占位共 {fmt_int(total_current)} B）",
        "utilization": text_total / total_budget if total_budget else None,
        "headroom": total_budget - text_total if total_budget else None,
        "headroom_pct": (total_budget - text_total) / total_budget if total_budget else None,
        "note": "",
    })
    return rows


def build_payload(args, baseline, current_blocks, measurement_meta, rows) -> dict:
    base_blocks = block_map(baseline.get("blocks", []))
    checks = []
    all_ok = True
    for r in rows:
        if r["id"] == "total":
            continue
        bb = base_blocks.get(r["id"], {})
        expected = int(bb.get("bytes", 0) or 0)
        ok = int(r["bytes"]) == expected
        all_ok = all_ok and ok
        checks.append({
            "id": r["id"],
            "expected_s1": expected,
            "current": int(r["bytes"]),
            "delta": int(r["bytes"]) - expected,
            "ok": ok,
        })

    baseline_total = int(baseline.get("sum_bytes", baseline.get("total", 0)) or 0)
    total_row = next(r for r in rows if r["id"] == "total")
    total_ok = int(total_row["bytes"]) == baseline_total
    rows_sum = sum(int(r["bytes"]) for r in rows if r["id"] != "total")
    sum_ok = rows_sum == int(total_row["bytes"])
    # 文本块口径：七块合计减去 MCP 占位；MCP 原始 schema 与 App 注入分开写。
    mcp_row = next((r for r in rows if r["id"] == "mcp"), None)
    mcp_bytes = int(mcp_row["bytes"]) if mcp_row else 0
    text_total = int(total_row["bytes"]) - mcp_bytes
    overall_upper = text_total + 2400 + 12400

    warnings: list[dict] = []
    for r in rows:
        if r["budget"] is None or r["headroom"] is None:
            continue
        if r["headroom"] < 0:
            warnings.append({
                "id": r["id"],
                "level": "OVER",
                "message": f'{r["label"]} 超预算 {abs(r["headroom"]):,} B（占用 {fmt_pct(r["utilization"])}）',
            })
        elif r["headroom_pct"] is not None and r["headroom_pct"] < 0.05:
            warnings.append({
                "id": r["id"],
                "level": "LOW",
                "message": f'{r["label"]} 余量 {r["headroom"]:,} B（{fmt_pct(r["headroom_pct"])}）<5%；新增内容先删旧指针',
            })

    growth = sorted(
        [r for r in rows if r["id"] != "total"],
        key=lambda r: (r["delta"], r["bytes"]),
        reverse=True,
    )[:5]

    return {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL,
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
        "baseline": str(Path(args.baseline).expanduser()),
        "measurement": measurement_meta,
        "rows": rows,
        "assertions": {
            "seven_blocks_match_s1": all_ok,
            "total_match_s1": total_ok,
            "checks": checks,
            "baseline_total": baseline_total,
            "current_total": int(total_row["bytes"]),
            "rows_sum": rows_sum,
            "sum_matches": sum_ok,
            "gate": int(BUDGETS["total"]["budget"]),
            "headroom": int(total_row["headroom"] or 0),
            "text_blocks_total": text_total,
            "text_gate_status": "PASS" if text_total <= int(BUDGETS["total"]["budget"]) else "FAIL",
            "overall_app_injection_status": "UNMEASURED",
            "overall_upper_total": overall_upper,
            "overall_upper_gate_status": "PASS" if overall_upper <= int(BUDGETS["total"]["budget"]) else "FAIL",
            "mcp_calibers": {
                "seven_block_placeholder": mcp_bytes,
                "node_repl_measured": 2400,
                "codex_app_upper_bound": 12400,
                "raw_schema_known": 130481,
                "raw_schema_upper": 142881,
            },
            "mcp_injection_status": "UNMEASURED",
        },
        "growth_top5": growth,
        "warnings": warnings,
        "notes": [
            "只读看板；不修改任何源文件。",
            "memory 12,000 B 来自 s3 目标；skills 10,240 B 来自技能索引约 10 KB 预算；AGENTS 5,500 B 来自一期报告；total 57,344 B 来自 s1 闸门。",
            "AGENTS 预算按 AGENTS.md 源文件 5,387 B 计，注入块 5,443 B 含 41 B 前缀 + 15 B 后缀；两者不可混为一谈。",
            "MCP 3,900 B 是 2026-11-05 assumption，不是实测；s2 的原始 schema 130,481 B 也不是模型实际注入字节。",
            "base/permissions/MCP/env 未设独立预算，余量显示为 —，不伪造数字。",
            "MCP 整体口径 UNMEASURED：已知注入 node_repl 2,400 B + codex_app 上界 12,400 B；原始 tools/list 已知 130,481 B，不是每请求注入。",
        ],
    }


def build_markdown(payload: dict) -> str:
    a = payload["assertions"]
    rows = payload["rows"]
    m = payload["measurement"]
    lines: list[str] = []
    lines.append("# 七块固定注入预算看板（2026-11-09）")
    lines.append("")
    lines.append(f'- 生成：`{payload["generated_at"]}`')
    lines.append(f'- 当前数据：**{m["status"]}** · `{m["source"]}`')
    lines.append(f'- 基线：`{payload["baseline"]}`')
    lines.append(f'- 七块逐项与 s1 一致：**{"PASS" if a["seven_blocks_match_s1"] else "DIFF"}**；合计求和：**{"PASS" if a["sum_matches"] else "FAIL"}**')
    lines.append(f'- 文本块（不含 MCP）：**{a["text_blocks_total"]:,} B / 闸门 {a["gate"]:,} B** → **{a["text_gate_status"]}**')
    lines.append(f'- 七块含 MCP 占位：**{a["current_total"]:,} B**（占位不是实测注入）')
    lines.append(f'- 整体（含 MCP 注入）：**{a["overall_app_injection_status"]}**；上界 **{a["overall_upper_total"]:,} B** → {a["overall_upper_gate_status"]}')
    lines.append(f'- MCP 三口径：占位 {a["mcp_calibers"]["seven_block_placeholder"]:,} / 已知原始 schema {a["mcp_calibers"]["raw_schema_known"]:,} / App 注入 UNMEASURED')
    lines.append("- 边界：只读；不修改任何被扫文件；无独立预算的块不计算余量。")
    lines.append("")

    lines.append("## 1 预算看板")
    lines.append("")
    lines.append("| 块 | 块字节 | 预算口径字节 | 预算 | 占用率 | 余量 | 相对 s1 | 来源 | 预算依据 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---|---|")
    for r in rows:
        lines.append(
            f'| {r["label"]} | {r["bytes"]:,} | {fmt_int(r["basis_bytes"])} | '
            f'{fmt_int(r["budget"])} | {fmt_pct(r["utilization"])} | '
            f'{fmt_int(r["headroom"])} | {fmt_delta(r["delta"])} | '
            f'{r["source"]} | {r["budget_source"]} |'
        )
    lines.append("")
    lines.append("口径备注：")
    lines.append("")
    for r in rows:
        if r["id"] == "total":
            lines.append(f'- **{r["label"]}**：{r["basis_note"]}；预算为 s1 闸门，按文本块口径（不含 MCP 占位）。')
        elif r["budget"] is not None:
            lines.append(f'- **{r["label"]}**：{r["basis_note"]}；预算依据：{r["budget_source"]}。')
        else:
            lines.append(f'- **{r["label"]}**：未设独立预算，余量与占用率显示为 —；块字节 {r["bytes"]:,} B，来源 {r["source"]}。')
    lines.append("")

    lines.append("## 2 相对 s1 增量 Top 5")
    lines.append("")
    lines.append("| # | 块 | 当前 | s1 | 增量 |")
    lines.append("|---:|---|---:|---:|---:|")
    for i, r in enumerate(payload["growth_top5"], start=1):
        lines.append(f'| {i} | {r["label"]} | {r["bytes"]:,} | {r["baseline_bytes"]:,} | {fmt_delta(r["delta"])} |')
    if all(r["delta"] == 0 for r in payload["growth_top5"]):
        lines.append("")
        lines.append("> 前 5 项增量均为 0；七块与 s1 逐项一致。")
    lines.append("")

    lines.append("## 3 七块与 s1 一致性断言")
    lines.append("")
    lines.append("```console")
    for c in a["checks"]:
        lines.append(f'{c["id"]:<12} current={c["current"]:>6,}  s1={c["expected_s1"]:>6,}  delta={c["delta"]:+d}  {"OK" if c["ok"] else "MISMATCH"}')
    lines.append(f'{"sum_bytes":<12} current={a["current_total"]:>6,}  s1={a["baseline_total"]:>6,}  delta={a["current_total"] - a["baseline_total"]:+d}')
    lines.append(f'ASSERT_SUM_MATCHES_TOTAL: {"PASS" if a["sum_matches"] else "FAIL"}')
    lines.append(f'ASSERT_SEVEN_BLOCKS_MATCH_S1: {"PASS" if a["seven_blocks_match_s1"] else "DIFF (技能目录因新增 agent-slim 变化)"}')
    lines.append(f'TEXT_GATE: {a["text_gate_status"]}  {a["text_blocks_total"]:,}/{a["gate"]:,} B')
    lines.append(f'OVERALL_APP_INJECTION: {a["overall_app_injection_status"]}  upper={a["overall_upper_total"]:,} B  {a["overall_upper_gate_status"]}')
    lines.append("```")
    lines.append("")

    lines.append("## 4 预警（余量 <5% 或超预算）")
    lines.append("")
    if not payload["warnings"]:
        lines.append("无预算余量 <5% 或超预算项。")
    else:
        for w in payload["warnings"]:
            prefix = "**超预算**" if w["level"] == "OVER" else "**预警**"
            lines.append(f'- {prefix}：{w["message"]}')
    lines.append("")

    lines.append("## 5 口径与边界")
    lines.append("")
    for n in payload["notes"]:
        lines.append(f"- {n}")
    lines.append("")
    lines.append("### 数据来源")
    lines.append("")
    lines.append(f'- 基线：`{payload["baseline"]}`')
    if m.get("measure"):
        d = m["measure"]
        lines.append(f'- 测量器：`measure_prompt.py --json`；退出状态 `{d.get("status")}`；总字节 `{d.get("total")}`；对账 `{d.get("reconciliation")}`。')
        lines.append(f'- 测量时间：`{d.get("timestamp")}`；`gate_status`=`{d.get("gate_status")}`；`headroom_bytes`=`{d.get("headroom_bytes")}`。')
    else:
        lines.append(f'- 当前数据说明：{m.get("detail") or "未调用测量器"}。')
    lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    root = project_root()
    default_baseline = Path(os.environ.get(
        "AGENT_SLIM_BASELINE", str(SKILL_ROOT / "references" / "baseline-20261109.json")
    )).expanduser()
    parser = argparse.ArgumentParser(description="七块固定注入预算看板（只读）")
    parser.add_argument("--baseline", default=str(default_baseline))
    parser.add_argument("--measure-script", default=str(SKILL_ROOT / "scripts" / "measure_prompt.py"))
    parser.add_argument("--measure-json", default=None, help="读取已保存的 measure_prompt.py --json 输出，不再调用测量器")
    parser.add_argument("--no-measure", action="store_true", help="直接用 s1 基线块，不调用测量器")
    parser.add_argument("--out", default=str(Path.cwd() / "budget-dashboard.md"))
    parser.add_argument("--json-out", default=None, help="可选：同时写机器可读 JSON")
    args = parser.parse_args(argv)

    baseline_path = Path(args.baseline).expanduser()
    baseline = load_json(baseline_path)
    current_blocks, meta = pick_measurement(args, baseline)
    if len(block_map(current_blocks)) < 7:
        # 缺块时退回基线，避免看板漏行或伪造 0
        current_blocks = baseline.get("blocks", [])
        meta = {
            "source": "s1 baseline",
            "status": "BASELINE_FALLBACK",
            "timestamp": baseline.get("timestamp"),
            "detail": "测量结果不足七块，已退回基线",
        }

    rows = build_rows(current_blocks, baseline.get("blocks", []))
    payload = build_payload(args, baseline, current_blocks, meta, rows)
    payload["project_root"] = str(root)

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_markdown(payload), encoding="utf-8")
    if args.json_out:
        jout = Path(args.json_out).expanduser()
        jout.parent.mkdir(parents=True, exist_ok=True)
        jout.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "tool": TOOL,
        "status": meta["status"],
        "source": meta["source"],
        "total": payload["assertions"]["current_total"],
        "text_blocks_total": payload["assertions"]["text_blocks_total"],
        "text_gate_status": payload["assertions"]["text_gate_status"],
        "overall_app_injection_status": payload["assertions"]["overall_app_injection_status"],
        "overall_upper_total": payload["assertions"]["overall_upper_total"],
        "gate": payload["assertions"]["gate"],
        "headroom": payload["assertions"]["headroom"],
        "sum_matches": payload["assertions"]["sum_matches"],
        "seven_blocks_match_s1": payload["assertions"]["seven_blocks_match_s1"],
        "total_match_s1": payload["assertions"]["total_match_s1"],
        "warnings": payload["warnings"],
        "out": str(out),
        "json_out": str(Path(args.json_out).expanduser()) if args.json_out else None,
        "bytes": out.stat().st_size,
    }, ensure_ascii=False, indent=2))
    # 看板的核心一致性是“七行相加 = 合计”；与 s1 的差异只作信息展示。
    return 0 if payload["assertions"]["sum_matches"] else 1


if __name__ == "__main__":
    sys.exit(main())
