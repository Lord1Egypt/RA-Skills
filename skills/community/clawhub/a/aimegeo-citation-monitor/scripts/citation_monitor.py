#!/usr/bin/env python3
"""Offline, deterministic mention/citation accounting with modern IDNA matching."""

import argparse
from collections import defaultdict
from datetime import datetime
import json
import math
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlsplit

try:
    import idna
except ModuleNotFoundError:
    idna = None


STATUSES = ("success", "error", "timeout", "not_run", "simulated")
CONDITIONS = ("model", "search_mode", "context")


class InputError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InputError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def object_value(value, where):
    require(isinstance(value, dict), f"{where}: expected object")
    return value


def timestamp(value, where):
    require(nonempty(value), f"{where}: timestamp required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InputError(f"{where}: invalid ISO timestamp") from exc
    require(parsed.tzinfo is not None, f"{where}: timezone required")
    return parsed


def domain_name(value):
    require(nonempty(value), "domain must be a nonempty hostname")
    require(not any(c in value for c in "/:@?#*\\%"), f"invalid hostname: {value}")
    require(idna is not None, "IDNA support requires idna; install this skill's requirements.txt")
    try:
        # Nontransitional UTS #46 preserves modern IDNA identities (e.g. ß != ss).
        # Python's built-in IDNA2003 codec would conflate those distinct domains.
        host = idna.encode(value.rstrip("."), uts46=True, transitional=False,
                           std3_rules=True).decode("ascii").lower()
    except UnicodeError as exc:
        raise InputError(f"invalid hostname: {value}") from exc
    require(len(host) <= 253 and all(
        re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
        for label in host.split(".")
    ), f"invalid hostname: {value}")
    return host


def url_host(value):
    require(nonempty(value) and not re.search(r"[\s\\]", value), "invalid citation URL")
    try:
        url = urlsplit(value)
        require(url.scheme.lower() in ("http", "https") and url.hostname,
                "citation URL must be absolute HTTP(S)")
        require(url.username is None and url.password is None,
                "citation URL must not contain userinfo")
        _ = url.port
        return domain_name(url.hostname)
    except ValueError as exc:
        raise InputError(f"invalid citation URL: {value}") from exc


def normalize(text):
    return unicodedata.normalize("NFKC", text).casefold()


def alias_in_answer(alias, answer):
    term = normalize(alias)
    # Bound ASCII names without preventing Chinese names from appearing in sentences.
    left = r"(?<![a-z0-9_])" if re.match(r"[a-z0-9_]", term[0]) else ""
    right = r"(?![a-z0-9_])" if re.match(r"[a-z0-9_]", term[-1]) else ""
    return re.search(left + re.escape(term) + right, normalize(answer)) is not None


def inspect_answer(record, brand):
    aliases = list(dict.fromkeys([brand["name"]] + brand.get("aliases", [])))
    matches = [alias for alias in aliases if alias_in_answer(alias, record["answer"])]
    native = record["citations"]
    hits = None
    if native is not None:
        hits = []
        for position, citation in enumerate(native, 1):
            link = citation if isinstance(citation, str) else citation["url"]
            host = url_host(link)
            if any(host == domain or (brand.get("include_subdomains", True)
                                     and host.endswith("." + domain))
                   for domain in map(domain_name, brand["domains"])):
                hits.append({"position": position, "url": link, "host": host})
    return {"mentioned": bool(matches), "matched_aliases": matches,
            "native_cited": bool(hits) if hits is not None else None,
            "matched_native_citations": hits,
            "first_native_position": hits[0]["position"] if hits else None}


def validate(data):
    object_value(data, "input")
    # JSON exponent overflow becomes inf without invoking parse_constant. Inspect
    # every value, including native metadata preserved verbatim in raw_record.
    pending = [data]
    while pending:
        value = pending.pop()
        if isinstance(value, float):
            require(math.isfinite(value), "non-finite JSON number")
        elif isinstance(value, dict):
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
    require(type(data.get("schema_version")) is int and data["schema_version"] == 1,
            "schema_version must be integer 1")
    require(data.get("dataset_kind") in ("observed", "simulated"),
            "dataset_kind must be observed or simulated")
    brand = object_value(data.get("brand"), "brand")
    require(nonempty(brand.get("name")), "brand.name required")
    aliases = brand.get("aliases", [])
    require(isinstance(aliases, list) and all(nonempty(a) for a in aliases),
            "brand.aliases must be a list of nonempty strings")
    require(isinstance(brand.get("domains"), list) and brand["domains"],
            "brand.domains requires at least one hostname")
    for domain in brand["domains"]:
        domain_name(domain)
    require(isinstance(brand.get("include_subdomains", True), bool),
            "include_subdomains must be boolean")
    queries = data.get("queries")
    require(isinstance(queries, list) and queries, "queries must be a nonempty list")
    query_ids = set()
    for query in queries:
        object_value(query, "query")
        require(all(nonempty(query.get(k)) for k in ("id", "text", "category")),
                "each query needs id, text, category")
        require(query["id"] not in query_ids, "duplicate query id")
        require(query.get("priority", "normal") in ("normal", "high", "critical"),
                "query priority must be normal/high/critical")
        require(isinstance(query.get("expected_native_citation", False), bool),
                "expected_native_citation must be boolean")
        query_ids.add(query["id"])
    platforms = data.get("platforms")
    require(isinstance(platforms, list) and platforms and all(nonempty(p) for p in platforms),
            "platforms must be a nonempty list of platform IDs")
    require(len(set(platforms)) == len(platforms), "duplicate platform")
    runs = data.get("runs")
    require(isinstance(runs, list) and runs, "runs must be a nonempty list")
    run_ids = set()
    for run in runs:
        object_value(run, "run")
        require(nonempty(run.get("id")) and run["id"] not in run_ids,
                "run id missing or duplicated")
        run_ids.add(run["id"])
        timestamp(run.get("started_at"), "run.started_at")
        records = run.get("records")
        require(isinstance(records, list), "run.records must be a list (may be empty)")
        keys = set()
        for record in records:
            object_value(record, "record")
            require(nonempty(record.get("platform")) and record["platform"] in platforms,
                    "record has unplanned platform")
            require(nonempty(record.get("query_id")) and record["query_id"] in query_ids,
                    "record has unplanned query_id")
            key = (record["platform"], record["query_id"])
            require(key not in keys, "duplicate platform/query in one run; use separate runs for retries")
            keys.add(key)
            status = record.get("status")
            require(status in STATUSES, f"unknown status: {status}")
            if status in ("error", "timeout", "not_run"):
                require(nonempty(record.get("reason")), "unsuccessful record requires reason")
                require(not record.get("answer") and not record.get("citations"),
                        "unsuccessful record must not contain answer/citations")
            source = record.get("source")
            if status != "not_run" or source is not None:
                source = object_value(source, "record.source")
                require(source.get("kind") in ("export", "api", "browser", "simulation"),
                        "source.kind must be export/api/browser/simulation")
                require(nonempty(source.get("executor")) and nonempty(source.get("reference")),
                        "source needs actual executor and evidence reference")
                if data["dataset_kind"] == "observed" and status == "success":
                    require(source["kind"] != "simulation", "simulation cannot be observed success")
            if status in ("success", "simulated"):
                require(nonempty(record.get("answer")), "successful/simulated record needs answer")
                require(nonempty(record.get("query")), "actual query text required")
                timestamp(record.get("collected_at"), "record.collected_at")
                conditions = object_value(record.get("conditions"), "record.conditions")
                require(all(nonempty(conditions.get(k)) for k in CONDITIONS),
                        "conditions needs model, search_mode, context (use unknown when unknown)")
                require("citations" in record, "citations required: null means not captured, [] means empty")
                citations = record["citations"]
                require(citations is None or isinstance(citations, list), "citations must be list or null")
                for citation in citations or []:
                    if isinstance(citation, dict):
                        url_host(citation.get("url"))
                    else:
                        require(isinstance(citation, str), "citation must be URL string or object with url")
                        url_host(citation)
    return data


def materialize(data):
    rows = []
    for run in sorted(data["runs"], key=lambda r: (timestamp(r["started_at"], "run"), r["id"])):
        index = {(r["platform"], r["query_id"]): r for r in run["records"]}
        for platform in data["platforms"]:
            for query in data["queries"]:
                raw = index.get((platform, query["id"]))
                status = raw["status"] if raw else "not_run"
                if status == "success" and data["dataset_kind"] == "simulated":
                    status = "simulated"
                row = {"run_id": run["id"], "started_at": run["started_at"],
                       "platform": platform, "query_id": query["id"],
                       "category": query["category"], "priority": query.get("priority", "normal"),
                       "expected_native_citation": query.get("expected_native_citation", False),
                       "query": raw.get("query", query["text"]) if raw else query["text"],
                       "status": status, "reason": raw.get("reason") if raw else "No record supplied for planned sample",
                       "source": raw.get("source") if raw else None,
                       "conditions": raw.get("conditions") if raw else None,
                       "collected_at": raw.get("collected_at") if raw else None,
                       "raw_record": raw,
                       "mentioned": None, "native_cited": None, "matched_aliases": None,
                       "matched_native_citations": None, "first_native_position": None}
                if status == "success":
                    row.update(inspect_answer(raw, data["brand"]))
                elif status == "simulated":
                    row["simulation_preview"] = inspect_answer(raw, data["brand"])
                    row["reason"] = row["reason"] or "Simulation excluded from observed metrics"
                rows.append(row)
    return rows


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def summary(rows):
    effective = [r for r in rows if r["status"] == "success"]
    observed_citations = [r for r in effective if r["native_cited"] is not None]
    mentions = sum(r["mentioned"] for r in effective) if effective else None
    cited = sum(r["native_cited"] for r in observed_citations) if observed_citations else None
    return {"planned": len(rows), "effective_answers": len(effective),
            "citation_observed_answers": len(observed_citations),
            "status_counts": {k: sum(r["status"] == k for r in rows) for k in STATUSES},
            "mentioned_answers": mentions, "native_cited_answers": cited,
            "mention_rate": ratio(mentions, len(effective)),
            "native_citation_rate": ratio(cited, len(observed_citations)),
            "citation_unknown_answers": len(effective) - len(observed_citations),
            "critical_native_gaps": [
                {"run_id": r["run_id"], "platform": r["platform"], "query_id": r["query_id"]}
                for r in observed_citations if r["priority"] == "critical"
                and r["expected_native_citation"] and not r["native_cited"]]}


def grouped(rows, keys):
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    return [{**dict(zip(keys, key)), **summary(values)} for key, values in sorted(groups.items())]


def transition_stats(pairs, field):
    values = [p[field] for p in pairs if p[field] is not None]
    n = len(values)
    if not n:
        return {"paired": 0, "before_count": None, "after_count": None,
                "before_rate": None, "after_rate": None, "delta_percentage_points": None,
                "gained": None, "lost": None}
    before = sum(p["before"] for p in values)
    after = sum(p["after"] for p in values)
    return {"paired": n, "before_count": before, "after_count": after,
            "before_rate": before / n, "after_rate": after / n,
            "delta_percentage_points": 100 * (after - before) / n,
            "gained": sum(not p["before"] and p["after"] for p in values),
            "lost": sum(p["before"] and not p["after"] for p in values)}


def compare(rows, before, after):
    earlier = {(r["platform"], r["query_id"]): r for r in rows if r["run_id"] == before}
    later = {(r["platform"], r["query_id"]): r for r in rows if r["run_id"] == after}
    pairs = []
    for key, old in earlier.items():
        new = later[key]
        reasons = []
        if old["status"] != "success" or new["status"] != "success":
            reasons.append(f"status: {old['status']} -> {new['status']}")
        else:
            if old["query"] != new["query"]:
                reasons.append("actual query text changed")
            for condition in CONDITIONS:
                a, b = old["conditions"][condition], new["conditions"][condition]
                if normalize(a).strip() == "unknown" or normalize(b).strip() == "unknown":
                    reasons.append(f"unknown {condition}")
                elif a != b:
                    reasons.append(f"{condition} changed")
            if any(old["source"][k] != new["source"][k] for k in ("kind", "executor")):
                reasons.append("collection source/executor changed")
            if any(normalize(r["source"]["executor"]).strip() == "unknown" for r in (old, new)):
                reasons.append("unknown collection executor")
        mention = None if reasons else {"before": old["mentioned"], "after": new["mentioned"]}
        citation_reasons = list(reasons)
        if old["native_cited"] is None or new["native_cited"] is None:
            citation_reasons.append("native citations not observed on both sides")
        citation = None if citation_reasons else {"before": old["native_cited"], "after": new["native_cited"]}
        pairs.append({"platform": key[0], "query_id": key[1], "category": old["category"],
                      "before_status": old["status"], "after_status": new["status"],
                      "mention": mention, "native_citation": citation,
                      "mention_exclusions": reasons, "citation_exclusions": citation_reasons})
    return {"before": before, "after": after, "planned_pairs": len(pairs),
            "mention": transition_stats(pairs, "mention"),
            "native_citation": transition_stats(pairs, "native_citation"), "pairs": pairs}


def analyze(data, before=None, after=None):
    validate(data)
    require(bool(before) == bool(after), "supply both --before and --after")
    if before:
        runs = {r["id"]: r for r in data["runs"]}
        require(before in runs and after in runs, "comparison run ID not found")
        require(timestamp(runs[before]["started_at"], "before") <
                timestamp(runs[after]["started_at"], "after"), "before must precede after")
    rows = materialize(data)
    history = sorted(grouped(rows, ("run_id", "started_at")),
                     key=lambda r: (timestamp(r["started_at"], "run"), r["run_id"]))
    return {"schema_version": 1, "dataset_kind": data["dataset_kind"], "brand": data["brand"],
            "overall": summary(rows), "history": history,
            "by_platform": grouped(rows, ("run_id", "platform")),
            "by_category": grouped(rows, ("run_id", "category")),
            "comparison": compare(rows, before, after) if before else None,
            "results": rows}


def cell(value):
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def metric(count, denominator, rate):
    return f"{count}/{denominator} ({rate * 100:.1f}%)" if rate is not None else f"N/A（有效分母 {denominator}）"


def report_text(result):
    s = result["overall"]
    lines = [f"# {cell(result['brand']['name'])}：AI 提及与引用复测", "",
             f"数据类型：`{result['dataset_kind']}`。本报告仅汇总输入记录，未执行在线查询。", "",
             f"计划 {s['planned']}；真实有效回答 {s['effective_answers']}；原生引用可判定回答 {s['citation_observed_answers']}。",
             f"提及：{metric(s['mentioned_answers'], s['effective_answers'], s['mention_rate'])}；"
             f"原生域名引用：{metric(s['native_cited_answers'], s['citation_observed_answers'], s['native_citation_rate'])}。", "",
             "状态：" + "；".join(f"{k}={v}" for k, v in s["status_counts"].items()) + "。",
             f"真实有效回答中有 {s['citation_unknown_answers']} 条未提供原生引用列表，未按零引用处理。", ""]
    if result["dataset_kind"] == "simulated":
        lines += ["此输入为模拟样例；模拟命中仅保留在 JSON 的 simulation_preview，不代表平台实际提及、引用或收录。", ""]
    if not s["effective_answers"]:
        lines += ["没有真实有效回答，无法判断提及率或引用率。", ""]
    lines += ["## 历史批次", "", "| 批次 | 开始时间 | 计划 | 有效 | 提及 | 原生域名引用 |", "| --- | --- | --- | --- | --- | --- |"]
    for row in result["history"]:
        lines.append(f"| {cell(row['run_id'])} | {cell(row['started_at'])} | {row['planned']} | {row['effective_answers']} | "
                     f"{metric(row['mentioned_answers'], row['effective_answers'], row['mention_rate'])} | "
                     f"{metric(row['native_cited_answers'], row['citation_observed_answers'], row['native_citation_rate'])} |")
    lines += ["", "## 平台与类别", "", "| 批次 | 分组 | 计划 | 有效 | 提及 | 原生域名引用 |", "| --- | --- | --- | --- | --- | --- |"]
    for group, label in (("by_platform", "platform"), ("by_category", "category")):
        for row in result[group]:
            lines.append(f"| {cell(row['run_id'])} | {cell(label)}: {cell(row[label])} | {row['planned']} | {row['effective_answers']} | "
                         f"{metric(row['mentioned_answers'], row['effective_answers'], row['mention_rate'])} | "
                         f"{metric(row['native_cited_answers'], row['citation_observed_answers'], row['native_citation_rate'])} |")
    comparison = result["comparison"]
    if comparison:
        lines += ["", f"## 同题比较：{cell(comparison['before'])} → {cell(comparison['after'])}", "",
                  f"计划配对 {comparison['planned_pairs']}；按同平台、相同实际题文、采集来源及模型/搜索/上下文条件配对。", ""]
        for field, label in (("mention", "提及"), ("native_citation", "原生域名引用")):
            stats = comparison[field]
            if not stats["paired"]:
                lines.append(f"- {label}：N/A，真实有效配对 0，无法比较。")
            else:
                lines.append(f"- {label}：{stats['before_count']}/{stats['paired']} → {stats['after_count']}/{stats['paired']}；"
                             f"变化 {stats['delta_percentage_points']:+.1f} 个百分点；新增 {stats['gained']}，失去 {stats['lost']}。")
        lines += ["", "| 平台 | 问题 | 提及前后 | 引用前后 | 排除原因（提及 / 引用） |", "| --- | --- | --- | --- | --- |"]
        for pair in comparison["pairs"]:
            def change(value):
                return f"{value['before']} → {value['after']}" if value is not None else "N/A"
            lines.append(f"| {cell(pair['platform'])} | {cell(pair['query_id'])} | {change(pair['mention'])} | {change(pair['native_citation'])} | "
                         f"{cell('; '.join(pair['mention_exclusions']) or '—')} / {cell('; '.join(pair['citation_exclusions']) or '—')} |")
    lines += ["", "## 逐项证据与采集缺口", "", "| 批次 | 平台 | 问题 | 状态 | 来源 / 执行器 / 证据 | 原因 |", "| --- | --- | --- | --- | --- | --- |"]
    for row in result["results"]:
        source = row.get("source")
        provenance = " / ".join(source[k] for k in ("kind", "executor", "reference")) if source else "无采集来源"
        lines.append(f"| {cell(row['run_id'])} | {cell(row['platform'])} | {cell(row['query_id'])} | {row['status']} | {cell(provenance)} | {cell(row['reason'] or '—')} |")
    lines += ["", "原始回答、引用列表、匹配 URL 和引用列表位置见《逐平台问题结果.json》。位置是原生引用列表序号，不是推荐排名。",
              "高优先级且预期引用的已判定缺口见 JSON 的 critical_native_gaps；采集失败和引用未知不算缺口。",
              "结果只代表这些输入样本，不能证明平台收录、完整平台覆盖或优化造成了变化。", ""]
    return "\n".join(lines)


def failures_text(rows):
    lines = ["# 未成功采集清单", "", "模拟记录另列，均不进入真实分母；有效回答缺少原生引用也单独列出。", "",
             "| 批次 | 平台 | 问题 | 状态 | 原因 |", "| --- | --- | --- | --- | --- |"]
    for row in rows:
        if row["status"] != "success" or row["native_cited"] is None:
            reason = row["reason"] or "Native citations not captured; mention remains usable"
            lines.append(f"| {cell(row['run_id'])} | {cell(row['platform'])} | {cell(row['query_id'])} | {row['status']} | {cell(reason)} |")
    return "\n".join(lines) + "\n"


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def invalid_constant(value):
    raise InputError(f"non-finite JSON number: {value}")


def write_outputs(result, output):
    payloads = {"逐平台问题结果.json": json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                "前后对照报告.md": report_text(result),
                "未成功采集清单.md": failures_text(result["results"])}
    # Refuse accidental replacement of previous evidence; use a new directory per analysis.
    require(not output.exists() or (output.is_dir() and not any(output.iterdir())),
            "output directory must be new or empty")
    output.mkdir(parents=True, exist_ok=True)
    for name, text in payloads.items():
        (output / name).write_text(text, encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="export JSON, schema_version=1")
    parser.add_argument("--output", type=Path, required=True, help="new or empty output directory")
    parser.add_argument("--before", help="baseline run ID; requires --after")
    parser.add_argument("--after", help="follow-up run ID; requires --before")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                          parse_constant=invalid_constant)
        result = analyze(data, args.before, args.after)
        write_outputs(result, args.output)
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Input/output error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"output": str(args.output), "dataset_kind": result["dataset_kind"],
                      "planned": result["overall"]["planned"],
                      "effective_answers": result["overall"]["effective_answers"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
