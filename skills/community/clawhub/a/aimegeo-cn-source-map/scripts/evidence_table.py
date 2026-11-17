#!/usr/bin/env python3
"""Validate an agent-reviewed evidence ledger and export its factual records.

No network access, content scoring, article generation, or AI citation inference.
"""

import argparse
import csv
import io
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


class EvidenceError(ValueError):
    """A ledger is internally inconsistent or unsafe to cite as declared."""


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def string(value, label, optional=False):
    require(isinstance(value, str), f"{label}: 必须是字符串")
    require(optional or bool(value.strip()), f"{label}: 不能为空")
    return value


def choice(value, choices, label):
    require(isinstance(value, str) and value in choices, f"{label}: 无效枚举值")


def day(value, label, nullable=False):
    if value is None and nullable:
        return None
    require(isinstance(value, str), f"{label}: 使用 YYYY-MM-DD 或允许的 null")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise EvidenceError(f"{label}: 无效日期") from exc
    require(parsed.isoformat() == value, f"{label}: 使用 YYYY-MM-DD")
    return parsed


def url(value, label, optional=False):
    string(value, label, optional=optional)
    if not value and optional:
        return
    try:
        parsed = urlsplit(value)
        require(parsed.scheme in {"http", "https"} and bool(parsed.hostname),
                f"{label}: 必须是完整 http(s) 页面 URL")
        require(not parsed.username and not parsed.password, f"{label}: 禁止带登录凭据")
        require(not any(ch.isspace() for ch in value), f"{label}: URL 不能含空白")
    except ValueError as exc:
        raise EvidenceError(f"{label}: 无效 URL") from exc


def objects(value, label, allow_empty=False):
    require(isinstance(value, list), f"{label}: 必须是数组")
    require(allow_empty or len(value) > 0, f"{label}: 不能为空")
    require(all(isinstance(item, dict) for item in value), f"{label}: 每项必须是对象")
    return value


def index(items, label):
    result = {}
    for item in items:
        key = string(item.get("id"), f"{label}.id")
        require(key not in result, f"{label}: 重复 id {key}")
        result[key] = item
    return result


def validate(ledger):
    require(isinstance(ledger, dict), "输入必须是 JSON 对象")
    require(type(ledger.get("schema_version")) is int and ledger["schema_version"] == 1,
            "schema_version 必须为整数 1")
    string(ledger.get("task"), "task")
    claims = index(objects(ledger.get("claims"), "claims"), "claims")
    sources = index(objects(ledger.get("sources"), "sources"), "sources")
    for cid, claim in claims.items():
        string(claim.get("text"), f"{cid}.text")
        choice(claim.get("kind"), {"industry_context", "industry_statistic", "product_fact", "effectiveness"},
               f"{cid}.kind")
        string(claim.get("subject"), f"{cid}.subject")
    for sid, source in sources.items():
        required = {"id", "title", "publisher", "source_type", "relationship", "url", "input_ref",
                    "published_on", "publication_date_note", "period", "scope", "locator", "excerpt",
                    "access_status", "accessed_on", "access_note", "trace"}
        require(required <= source.keys(), f"{sid}: 缺少字段 {', '.join(sorted(required - source.keys()))}")
        for key in ("title", "publisher", "scope", "period", "locator"):
            string(source.get(key), f"{sid}.{key}")
        choice(source.get("source_type"), {"government", "research", "media", "company", "other"},
               f"{sid}.source_type")
        choice(source.get("relationship"), {"primary", "reprint"}, f"{sid}.relationship")
        state = source.get("access_status")
        choice(state, {"fetched", "supplied", "unrun", "failed", "simulated"}, f"{sid}.access_status")
        url(source.get("url"), f"{sid}.url", optional=state != "fetched")
        string(source.get("input_ref"), f"{sid}.input_ref", optional=state != "supplied")
        string(source.get("excerpt"), f"{sid}.excerpt", optional=True)
        string(source.get("summary", ""), f"{sid}.summary", optional=True)
        if state in {"fetched", "supplied"}:
            require(bool(source["excerpt"].strip() or source.get("summary", "").strip()),
                    f"{sid}: fetched/supplied 至少提供可合规使用的原文摘录或独立摘要")
        published = day(source.get("published_on"), f"{sid}.published_on", nullable=True)
        accessed = day(source.get("accessed_on"), f"{sid}.accessed_on", nullable=True)
        string(source.get("publication_date_note"), f"{sid}.publication_date_note", optional=published is not None)
        string(source.get("access_note"), f"{sid}.access_note")
        if state in {"fetched", "supplied", "failed"}:
            require(accessed is not None, f"{sid}: 已采集/收到资料/失败需记实际日期")
        if published and accessed:
            require(published <= accessed, f"{sid}: 发布日期晚于采集日期，请复核")
        if source["source_type"] == "company":
            string(source.get("subject"), f"{sid}.subject")
        trace = source.get("trace")
        require(isinstance(trace, dict), f"{sid}.trace: 必须是对象")
        choice(trace.get("status"), {"not_applicable", "not_attempted", "original_found", "not_found"},
               f"{sid}.trace.status")
        attempts = objects(trace.get("attempts"), f"{sid}.trace.attempts", allow_empty=True)
        for attempt in attempts:
            string(attempt.get("query"), f"{sid}.trace.query")
            string(attempt.get("outcome"), f"{sid}.trace.outcome")
        url(trace.get("original_url"), f"{sid}.trace.original_url", optional=trace["status"] != "original_found")
        if source["relationship"] == "reprint":
            require(trace["status"] != "not_applicable", f"{sid}: 转载必须记录溯源状态")
            if trace["status"] in {"original_found", "not_found"}:
                require(bool(attempts), f"{sid}: 溯源结论需要实际尝试记录")
        else:
            require(trace["status"] == "not_applicable", f"{sid}: 一手资料使用 not_applicable")
    edges = objects(ledger.get("evidence"), "evidence")
    pairs = set()
    represented = set()
    for edge in edges:
        cid, sid = edge.get("claim_id"), edge.get("source_id")
        require(isinstance(cid, str) and cid in claims, "evidence: 未知 claim_id")
        require(isinstance(sid, str) and sid in sources, "evidence: 未知 source_id")
        require((cid, sid) not in pairs, f"{cid}/{sid}: 重复证据行")
        pairs.add((cid, sid))
        represented.add(cid)
        support, use = edge.get("support"), edge.get("use")
        choice(support, {"direct", "background", "self_statement", "none"}, f"{cid}/{sid}.support")
        choice(use, {"cite", "pending", "reject"}, f"{cid}/{sid}.use")
        string(edge.get("reason"), f"{cid}/{sid}.reason")
        string(edge.get("citation_text"), f"{cid}/{sid}.citation_text", optional=use != "cite")
        string(edge.get("next_step"), f"{cid}/{sid}.next_step", optional=use == "cite")
        source, claim = sources[sid], claims[cid]
        if use != "cite":
            require(not edge["citation_text"].strip(), f"{cid}/{sid}: 待核实/弃用行不能填可引用句")
            continue
        require(source["access_status"] in {"fetched", "supplied"},
                f"{cid}/{sid}: 未运行/失败/模拟材料不能用作已核实证据")
        require(support != "none", f"{cid}/{sid}: 无支撑不能引用")
        if source["source_type"] == "company":
            require(support == "self_statement" and claim["kind"] == "product_fact"
                    and claim["subject"] == source["subject"],
                    f"{cid}/{sid}: 企业自述只能支持该企业自身产品事实")
        if support == "self_statement":
            require(source["source_type"] == "company", f"{cid}/{sid}: self_statement 需企业来源")
        if source["relationship"] == "reprint":
            require(source["trace"]["status"] in {"original_found", "not_found"},
                    f"{cid}/{sid}: 只有转载时需先尝试溯源")
            require(support == "background", f"{cid}/{sid}: 转载只能作为明确归属的背景转述")
    require(represented == set(claims), "每个论点至少有一行证据或待核实记录")
    return claims, sources, edges


COLUMNS = [
    "论点ID", "论点", "论点类型", "信源ID", "材料标题", "发布者", "信源类型", "一手或转载",
    "精确页面", "用户资料", "发布日期", "日期说明", "统计或适用时期", "适用范围", "定位",
    "原文摘录", "独立摘要", "采集状态", "采集日期", "采集说明", "原文溯源状态", "原始页面", "溯源尝试",
    "支撑关系", "使用决定", "判断理由", "可引用句", "下一步",
]


def cell(value):
    """Keep spreadsheet consumers from treating untrusted text as a formula."""
    value = str(value) if value is not None else ""
    probe = value.lstrip()
    return "'" + value if (probe.startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r"))) else value


def markdown(value):
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def render(ledger):
    claims, sources, edges = validate(ledger)
    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow(COLUMNS)
    for edge in edges:
        claim, source = claims[edge["claim_id"]], sources[edge["source_id"]]
        values = [
            edge["claim_id"], claim["text"], claim["kind"], edge["source_id"], source["title"], source["publisher"],
            source["source_type"], source["relationship"], source["url"], source["input_ref"], source["published_on"],
            source["publication_date_note"], source["period"], source["scope"], source["locator"], source["excerpt"],
            source.get("summary", ""),
            source["access_status"], source["accessed_on"], source["access_note"], source["trace"]["status"],
            source["trace"]["original_url"], json.dumps(source["trace"]["attempts"], ensure_ascii=False),
            edge["support"], edge["use"], edge["reason"], edge["citation_text"], edge["next_step"],
        ]
        writer.writerow([cell(value) for value in values])
    usable = {edge["claim_id"] for edge in edges if edge["use"] == "cite"}
    full = {edge["claim_id"] for edge in edges if edge["use"] == "cite" and edge["support"] == "direct"}
    summary = {
        "claims_total": len(claims), "sources_total": len(sources), "evidence_rows": len(edges),
        "claims_with_usable_material": len(usable), "claims_with_direct_support": len(full),
        "claims_without_usable_material": sorted(set(claims) - usable),
        "decisions": dict(sorted(Counter(edge["use"] for edge in edges).items())),
        "access_statuses": dict(sorted(Counter(source["access_status"] for source in sources.values()).items())),
        "meaning": "仅统计输入台账；可用背景或企业自述不等于论点获直接证实，也不是AI引用检测结果。",
    }
    lines = ["# 未核实清单", "", "仅汇总台账中的待核实、弃用和引用限制；不表示已进行网页或AI查询。", ""]
    unresolved = [edge for edge in edges if edge["use"] != "cite"]
    if unresolved:
        lines.extend(["| 论点/信源 | 决定 | 采集状态 | 原因 | 下一步 |", "|---|---|---|---|---|"])
        for edge in unresolved:
            values = [edge["claim_id"] + "/" + edge["source_id"], edge["use"],
                      sources[edge["source_id"]]["access_status"], edge["reason"], edge["next_step"]]
            lines.append("| " + " | ".join(markdown(value) for value in values) + " |")
    else:
        lines.append("台账没有待核实或弃用行；这不代表完成了全网核验。")
    lines.extend(["", "## 可用材料的限制", ""])
    for edge in edges:
        if edge["use"] != "cite":
            continue
        source = sources[edge["source_id"]]
        limits = [edge["reason"]]
        if source["access_status"] == "supplied":
            limits.append("仅核对用户提供材料，未在线核验页面")
        if source["published_on"] is None:
            limits.append("发布日期未标明：" + source["publication_date_note"])
        if source["relationship"] == "reprint":
            limits.append("转载溯源：" + source["trace"]["status"])
        lines.append(f"- {markdown(edge['claim_id'])}/{markdown(edge['source_id'])}：" + "；".join(markdown(x) for x in limits))
    return {"论点与信源表.csv": "\ufeff" + out.getvalue(), "未核实清单.md": "\n".join(lines) + "\n",
            "校验汇总.json": json.dumps(summary, ensure_ascii=False, indent=2) + "\n"}


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON 重复键: {key}")
        result[key] = value
    return result


def read_ledger(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_keys)


def main(argv=None):
    parser = argparse.ArgumentParser(description="校验Agent审阅的中文证据台账，导出CSV及未核实清单；不生成文章或评分。")
    parser.add_argument("--input", required=True, type=Path, help="证据台账 JSON")
    parser.add_argument("--out-dir", required=True, type=Path, help="导出目录")
    args = parser.parse_args(argv)
    try:
        files = render(read_ledger(args.input))
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for name in files:
            target = args.out_dir / name
            require(target.resolve() != args.input.resolve(), "导出不能覆盖输入台账")
            require(not target.is_symlink(), f"导出路径不能是符号链接: {name}")
            require(not target.exists() or target.is_file(), f"导出路径不是普通文件: {name}")
        for name, content in files.items():
            with (args.out_dir / name).open("w", encoding="utf-8", newline="") as handle:
                handle.write(content)
    except (EvidenceError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"证据校验失败: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"result": "ok", "files": sorted(files)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
