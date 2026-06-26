#!/usr/bin/env python3
"""bj_nonlisted_v2.py — enriched non-listed banker memo for 非上市 CN companies.

Improvements over v1:
  - Calls PrimeMatrixData__judicial_info  (诉讼/行政处罚/失信)
  - Calls PrimeMatrixData__shareholder_info (十大股东 + 工商登记股东)
  - Surfaces a "clean-bill" summary when all risk counts are zero
  - Consecutive section numbering

Usage:
    python3 bj_nonlisted_v2.py <root_dir>

The script hard-codes two Beijing non-listed targets (ByteDance + JD-Tech) for
the smoke-test suite. Parameterise the TARGETS list to add more.
"""
from __future__ import annotations
import json, os, pathlib, subprocess, sys


TARGETS = [
    ("bytedance", "字节跳动 (抖音有限公司)", "抖音有限公司"),
    ("jd-tech",   "京东科技",                  "京东科技控股股份有限公司"),
]


def pm_call(tool: str, fullname: str, env: dict) -> dict | list | None:
    bridge = (pathlib.Path.home() /
              ".openclaw/extensions/aigroup-lead-discovery-openclaw"
              "/scripts/mcp_compat/prime_matrix_stdio_bridge.mjs")
    child_env = {**os.environ,
                 "MCP_API_KEY": env.get("PRIMEMATRIX_MCP_API_KEY", ""),
                 "BASE_URL":    env.get("PRIMEMATRIX_BASE_URL", "")}
    r = subprocess.run(
        ["node", str(bridge), tool,
         json.dumps({"company_name": fullname})],
        capture_output=True, text=True, timeout=30, env=child_env)
    if r.returncode != 0:
        sys.stderr.write(f"  (PM {tool} failed: {r.stderr.strip()[:120]})\n")
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"_raw_text": r.stdout[:500]}


def count_records(payload) -> int:
    """Best-effort record count for risk/judicial/shareholder payloads."""
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        total = 0
        for v in payload.values():
            if isinstance(v, list):
                total += len(v)
        return total
    return 0


def summarise_judicial(payload) -> tuple[int, list[str]]:
    """Return (total_count, breakdown lines). PM returns e.g.
    {'立案信息': {'数量': N, '最新信息': [...]}, '裁判文书': {...}, '行政处罚': {...}}
    where each category has a nested 数量 count. Zero across all → clean bill."""
    if not isinstance(payload, dict):
        return 0, ["🟡 judicial_info 返回非字典，见 raw-data"]
    breakdown: list[str] = []
    total = 0
    for cat_key, cat_val in payload.items():
        if cat_key == "公司名称":
            continue
        if isinstance(cat_val, dict):
            n = cat_val.get("数量")
            if isinstance(n, int):
                total += n
                if n > 0:
                    breakdown.append(f"- {cat_key}: {n} 条")
        elif isinstance(cat_val, list):
            total += len(cat_val)
            if cat_val:
                breakdown.append(f"- {cat_key}: {len(cat_val)} 条")
    if total == 0:
        return 0, ["🟢 无诉讼 / 行政处罚 / 失信记录（PrimeMatrix 返回 0 条）"]
    return total, [f"⚠️ PrimeMatrix 返回 {total} 条司法记录，分布如下："] + breakdown


def summarise_shareholder(payload) -> tuple[int, list[str]]:
    """Return (count, top-N holder lines). PM returns 工商登记股东信息 list
    with 股东名称 / 出资比例 keys."""
    if not isinstance(payload, dict):
        return 0, []
    for key in ("工商登记股东信息", "上市公司十大流通股（非上市公司为空）",
                "shareholders", "top10", "十大股东"):
        rows = payload.get(key)
        if isinstance(rows, list) and rows:
            display = []
            for row in rows[:5]:
                if isinstance(row, dict):
                    name = row.get("股东名称") or row.get("name") or row.get("holder_name") or "?"
                    pct = row.get("出资比例") or row.get("持股比例") or row.get("ratio") or row.get("percent")
                    pct_str = f"{pct}%" if pct is not None else ""
                    display.append(f"- {name}: {pct_str}")
                else:
                    display.append(f"- {row}")
            return len(rows), display
    return 0, []


def build_one(d: pathlib.Path, slug: str, name: str, fullname: str, env: dict) -> None:
    raw = d / "raw-data"
    raw.mkdir(parents=True, exist_ok=True)

    basic = pm_call("basic_info", fullname, env) or {}
    uscc = (basic or {}).get("统一社会信用代码", "UNKNOWN")
    (raw / f"{uscc}-primematrix-basic_info.json").write_text(
        json.dumps(basic, ensure_ascii=False, indent=2))

    risk = pm_call("risk_info", fullname, env)
    if risk is not None:
        (raw / f"{uscc}-primematrix-risk_info.json").write_text(
            json.dumps(risk, ensure_ascii=False, indent=2))

    judicial = pm_call("judicial_info", fullname, env)
    if judicial is not None:
        (raw / f"{uscc}-primematrix-judicial_info.json").write_text(
            json.dumps(judicial, ensure_ascii=False, indent=2))

    shareholder = pm_call("shareholder_info", fullname, env)
    if shareholder is not None:
        (raw / f"{uscc}-primematrix-shareholder_info.json").write_text(
            json.dumps(shareholder, ensure_ascii=False, indent=2))

    address = basic.get("住所（地址）", "N/A")
    reg_cap = basic.get("注册资金(万元)")
    reg_cap_str = f"{reg_cap/10000:.2f} 亿元" if reg_cap else "N/A"
    legal_rep = basic.get("法定代表人或负责人或执行事务合伙人姓名", "N/A")
    founded = basic.get("成立日期", "N/A")
    status = basic.get("企业状态", "N/A")
    etype = basic.get("企业类型", "N/A")

    # Build sections list so numbering is consecutive regardless of which
    # optional PM calls returned data.
    sections: list[tuple[str, list[str]]] = []
    sections.append(("工商核验（PrimeMatrix basic_info）", [
        f"- 企业全称: {fullname}",
        f"- 企业类型: {etype}",
        f"- 注册资本: {reg_cap_str}",
        f"- 成立日期: {founded}",
        f"- 法定代表人: {legal_rep}",
        f"- 注册住所: {address}",
        f"- 企业状态: {status}",
    ]))

    risk_body: list[str] = []
    risk_count = count_records(risk) if risk is not None else None
    if risk_count == 0:
        risk_body.append("🟢 PrimeMatrix risk_info 返回 0 条风险记录（经营异常 / 股权出质 / 动产抵押 / 限制消费 / 失信被执行 均无命中）")
    elif risk_count:
        risk_body.append(f"⚠️ PrimeMatrix risk_info 返回 {risk_count} 条风险记录，原始 JSON 见 `raw-data/`")
    else:
        risk_body.append("risk_info 未返回结构化数据，见 raw-data/")
    sections.append(("风险概览（PrimeMatrix risk_info）", risk_body))

    if judicial is not None:
        jn, jlines = summarise_judicial(judicial)
        sections.append(("司法核验（PrimeMatrix judicial_info）", jlines))

    if shareholder is not None:
        sn, slines = summarise_shareholder(shareholder)
        body = [f"股东总数: {sn}"] + (slines or ["(返回格式非标准，见 raw-data)"])
        sections.append(("股权结构（PrimeMatrix shareholder_info）", body))

    sections.append(("数据来源", [
        "所有事实来自 PrimeMatrixData 单一 MCP（非上市公司无 Tushare 行情数据）。"
        "raw JSON 见 `raw-data/`；每个章节的数字/标记可回溯到对应 `{uscc}-primematrix-{tool}.json`。",
    ]))

    header = [
        f"# {name}（非上市）— 客户尽调 v2",
        "",
        f"**更新日期**: 2026-04-20  **统一社会信用代码**: `{uscc}`",
        "",
    ]
    lines = list(header)
    for idx, (title, body) in enumerate(sections, start=1):
        lines.append(f"## {idx}. {title}")
        lines.append("")
        lines.extend(body)
        lines.append("")
    (d / "analysis.md").write_text("\n".join(lines) + "\n")

    stems = {
        "basic":   f"{uscc}-primematrix-basic_info",
        "risk":    f"{uscc}-primematrix-risk_info",
        "jud":     f"{uscc}-primematrix-judicial_info",
        "share":   f"{uscc}-primematrix-shareholder_info",
    }
    prov = [
        f"# {name} (non-listed v2) — Data Provenance",
        "",
        "| 指标 | 数值 | 单位 | 期间 | Tier | Source | URL/Tool | 取数时间 | 备注 |",
        "|------|------|------|------|------|--------|----------|----------|------|",
        f"| 统一社会信用代码 | {uscc} | — | 工商登记 | T1 | {stems['basic']} | "
        f"PrimeMatrixData__basic_info | 2026-04-20 | — |",
    ]
    if reg_cap:
        prov.append(
            f"| 注册资本 | {reg_cap/10000:.2f} | 亿元 | 当前 | T1 | {stems['basic']} | "
            f"PrimeMatrixData__basic_info | 2026-04-20 | 原值 {reg_cap} 万元 |"
        )
    prov.append(
        f"| 法定代表人 | {legal_rep} | — | 当前 | T1 | {stems['basic']} | "
        f"PrimeMatrixData__basic_info | 2026-04-20 | — |"
    )
    prov.append(
        f"| 注册住所 | {address[:40]} | — | 当前 | T1 | {stems['basic']} | "
        f"PrimeMatrixData__basic_info | 2026-04-20 | — |"
    )
    if risk is not None:
        prov.append(
            f"| 风险概览 | {risk_count if risk_count is not None else '—'} | 条 | 当前 | T1 | "
            f"{stems['risk']} | PrimeMatrixData__risk_info | 2026-04-20 | 司法+经营+关联 |"
        )
    if judicial is not None:
        jn, _ = summarise_judicial(judicial)
        prov.append(
            f"| 司法记录 | {jn} | 条 | 当前 | T1 | {stems['jud']} | "
            f"PrimeMatrixData__judicial_info | 2026-04-20 | 诉讼+处罚+失信 |"
        )
    if shareholder is not None:
        sn, _ = summarise_shareholder(shareholder)
        prov.append(
            f"| 股东数 | {sn} | — | 当前 | T1 | {stems['share']} | "
            f"PrimeMatrixData__shareholder_info | 2026-04-20 | 十大 / 工商登记 |"
        )
        # Top-5 shareholder percentages also appear in analysis.md — register
        # each so provenance_verify can cross-check.
        if isinstance(shareholder, dict):
            rows = shareholder.get("工商登记股东信息", [])[:5]
            for row in rows:
                if isinstance(row, dict):
                    name = row.get("股东名称", "?")
                    pct = row.get("出资比例")
                    if pct is not None:
                        prov.append(
                            f"| 股东出资比例 | {pct} | % | 当前 | T1 | "
                            f"{stems['share']} | PrimeMatrixData__shareholder_info | "
                            f"2026-04-20 | {name[:25]} |"
                        )
    (d / "data-provenance.md").write_text("\n".join(prov) + "\n")


def main() -> None:
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.cwd()
    cfg = json.loads(pathlib.Path.home().joinpath(".openclaw/openclaw.json").read_text())
    env = cfg.get("env", {})
    for slug, name, fullname in TARGETS:
        d = root / slug
        print(f"\n--- {name} ---")
        try:
            build_one(d, slug, name, fullname, env)
            files = list((d / "raw-data").glob("*.json"))
            print(f"  wrote {d}/analysis.md + data-provenance.md + {len(files)} raw JSON")
        except Exception as e:
            print(f"  FAIL: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
