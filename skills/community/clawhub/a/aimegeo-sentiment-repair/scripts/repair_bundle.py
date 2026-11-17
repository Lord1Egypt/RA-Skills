#!/usr/bin/env python3
"""Validate an Agent-authored repair dossier and export its authored content.

No networking, language model calls, keyword sentiment scoring, or text generation.
"""

import argparse
import csv
import json
import os
import shutil
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

VERDICTS = {
    "accurate": "事实正确",
    "outdated": "已过时",
    "contradicted": "与当前事实不符",
    "unconfirmed": "待确认",
}
STATUSES = {"provided", "collected", "simulated", "not_run", "query_failed"}
ACTUAL = {"provided", "collected"}
FILES = ["误解与事实对照表.csv", "可直接使用的纠正FAQ.md", "复测问题.json"]


class Invalid(ValueError):
    def __init__(self, code, field, message):
        self.code, self.field, self.message = code, field, message
        super().__init__(message)

    def as_dict(self):
        return {"status": "error", "code": self.code,
                "field": self.field, "message": self.message}


def require(condition, code, field, message):
    if not condition:
        raise Invalid(code, field, message)


def shape(value, keys, field):
    require(isinstance(value, dict), "invalid_type", field, "必须是对象")
    require(set(value) == set(keys.split()), "invalid_fields", field,
            "字段必须恰好为：" + keys)


def string(value, field, nullable=False):
    if nullable and value is None:
        return
    require(isinstance(value, str) and bool(value.strip()),
            "invalid_text", field, "必须是非空文本" + ("或 null" if nullable else ""))


def choice(value, values, field):
    require(isinstance(value, str) and value in values, "invalid_value", field,
            "允许值：" + ", ".join(sorted(values)))


def sequence(value, field, nonempty=False):
    require(isinstance(value, list) and (not nonempty or bool(value)),
            "invalid_list", field, "必须是数组" + ("且不能为空" if nonempty else ""))


def texts(value, field, nonempty=False):
    sequence(value, field, nonempty)
    for i, text in enumerate(value):
        string(text, f"{field}[{i}]")


def day(value, field, nullable=False):
    if value is None and nullable:
        return None
    string(value, field)
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise Invalid("invalid_date", field, "日期必须为 YYYY-MM-DD") from None
    require(parsed.isoformat() == value, "invalid_date", field, "日期必须为 YYYY-MM-DD")
    return parsed


def indexed(items, field, nonempty=False):
    sequence(items, field, nonempty)
    result = {}
    for i, item in enumerate(items):
        require(isinstance(item, dict), "invalid_type", f"{field}[{i}]", "必须是对象")
        string(item.get("id"), f"{field}[{i}].id")
        require(item["id"] not in result, "duplicate_id", field, "同类记录 ID 不能重复")
        result[item["id"]] = item
    return result


def citation_summary(observations):
    actual = [o for o in observations if o["kind"] == "ai_answer" and o["status"] in ACTUAL]
    complete = bool(actual) and all(o["citation_capture"] == "complete" for o in actual)
    return {
        "actual_ai_answers": len(actual),
        "status_counts": dict(sorted(Counter(o["status"] for o in observations).items())),
        "native_citations": sum(len(o["native_citations"]) for o in actual) if complete else None,
        "citation_coverage": "complete" if complete else ("incomplete" if actual else "no_actual_answers"),
    }


def validate(data):
    shape(data, "schema_version brand as_of mode sources observations claims retests", "root")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "schema_version", "schema_version", "仅支持版本 1")
    string(data["brand"], "brand")
    as_of = day(data["as_of"], "as_of")
    choice(data["mode"], {"case", "illustrative"}, "mode")
    sources = indexed(data["sources"], "sources")
    observations = indexed(data["observations"], "observations", True)
    claims = indexed(data["claims"], "claims", True)
    indexed(data["retests"], "retests", True)

    for sid, source in sources.items():
        field = "sources." + sid
        shape(source, "id title locator content provenance scope effective_from effective_to", field)
        for key in ("title", "locator", "content"):
            string(source[key], field + "." + key)
        choice(source["provenance"], {"user_provided", "collected", "illustrative"}, field + ".provenance")
        choice(source["scope"], {"current", "historical", "uncertain"}, field + ".scope")
        start = day(source["effective_from"], field + ".effective_from", True)
        end = day(source["effective_to"], field + ".effective_to", True)
        require(not (start and end) or start <= end, "date_order", field, "生效起日不能晚于止日")
        if source["scope"] == "current":
            require(not start or start <= as_of, "future_evidence", field, "当前证据尚未生效")
            require(not end or end >= as_of, "expired_evidence", field, "当前证据已经失效")
        if source["scope"] == "historical":
            require(not start or start <= as_of, "future_evidence", field, "历史证据不能尚未生效")
            require(not end or end < as_of, "date_order", field, "历史证据止日须早于核对日期")
        if data["mode"] == "case":
            require(source["provenance"] != "illustrative", "illustrative_evidence", field,
                    "真实个案不能使用教学资料作为事实来源")

    for oid, obs in observations.items():
        field = "observations." + oid
        shape(obs, "id kind status text question platform observed_at native_citations citation_capture error", field)
        choice(obs["kind"], {"ai_answer", "customer_question"}, field + ".kind")
        choice(obs["status"], STATUSES, field + ".status")
        for key in ("text", "question", "platform", "error"):
            string(obs[key], field + "." + key, True)
        observed = day(obs["observed_at"], field + ".observed_at", True)
        require(not observed or observed <= as_of, "future_observation", field, "采集日期不能晚于核对日期")
        choice(obs["citation_capture"], {"complete", "partial", "not_available"}, field + ".citation_capture")
        if data["mode"] == "illustrative":
            require(obs["status"] not in ACTUAL, "simulation_as_actual", field,
                    "教学材料不能标为真实提供或采集")
        if obs["status"] in ACTUAL | {"simulated"}:
            string(obs["text"], field + ".text")
            require(obs["error"] is None, "invalid_state", field, "有回答记录时 error 应为 null")
        else:
            require(obs["text"] is None, "invalid_state", field, "未运行或查询失败不能填写回答")
            if obs["status"] == "query_failed":
                string(obs["error"], field + ".error")
            else:
                require(obs["error"] is None, "invalid_state", field, "未运行时 error 应为 null")
        if obs["status"] == "collected":
            require(obs["platform"] is not None and observed is not None and obs["question"] is not None,
                    "collection_metadata", field, "实际采集需要平台、日期和原始问题")
        can_capture = obs["kind"] == "ai_answer" and obs["status"] in ACTUAL
        if not can_capture or obs["citation_capture"] == "not_available":
            require(obs["native_citations"] is None and obs["citation_capture"] == "not_available",
                    "unknown_citations", field, "非真实AI回答或未取得引用时，引用须为 null / not_available")
        else:
            sequence(obs["native_citations"], field + ".native_citations",
                     obs["citation_capture"] == "partial")
            for i, citation in enumerate(obs["native_citations"]):
                cfield = f"{field}.native_citations[{i}]"
                shape(citation, "label url", cfield)
                string(citation["label"], cfield + ".label")
                string(citation["url"], cfield + ".url")
                require(citation["url"].startswith(("https://", "http://")), "citation_url", cfield,
                        "原生引用地址必须为 http(s) URL")

    for cid, claim in claims.items():
        field = "claims." + cid
        shape(claim, "id observation_id quote proposition verdict rationale evidence faq_question public_answer repair needed_information", field)
        for key in ("observation_id", "quote", "proposition", "rationale", "faq_question", "public_answer"):
            string(claim[key], field + "." + key)
        require(claim["observation_id"] in observations, "unknown_observation", field, "原文记录不存在")
        obs = observations[claim["observation_id"]]
        require(obs["text"] is not None and claim["quote"] in obs["text"],
                "quote_mismatch", field, "断言摘录必须逐字存在于原文中")
        choice(claim["verdict"], VERDICTS, field + ".verdict")
        texts(claim["needed_information"], field + ".needed_information",
              claim["verdict"] == "unconfirmed")
        shape(claim["repair"], "priority location action", field + ".repair")
        choice(claim["repair"]["priority"], {"P1", "P2", "P3"}, field + ".repair.priority")
        for key in ("location", "action"):
            string(claim["repair"][key], field + ".repair." + key)
        sequence(claim["evidence"], field + ".evidence")
        relations = set()
        for e in claim["evidence"]:
            shape(e, "source_id quote relation", field + ".evidence")
            string(e["source_id"], field + ".evidence.source_id")
            require(e["source_id"] in sources, "unknown_source", field, "证据来源不存在")
            source = sources[e["source_id"]]
            string(e["quote"], field + ".evidence.quote")
            require(e["quote"] in source["content"], "evidence_quote_mismatch", field, "证据摘录必须逐字存在于来源中")
            choice(e["relation"], {"supports", "contradicts", "historical_support"}, field + ".evidence.relation")
            relations.add((source["scope"], e["relation"]))
        needed = {
            "accurate": {("current", "supports")},
            "contradicted": {("current", "contradicts")},
            "outdated": {("historical", "historical_support"), ("current", "contradicts")},
            "unconfirmed": set(),
        }[claim["verdict"]]
        require(needed <= relations, "evidence_required", field + ".evidence", "判定缺少所需的当前或历史证据关系")
        if claim["verdict"] != "unconfirmed":
            opposing = "contradicts" if claim["verdict"] == "accurate" else "supports"
            require(("current", opposing) not in relations, "conflicting_evidence", field,
                    "当前证据冲突时应先标待确认并解释适用范围")

    covered = set()
    for item in data["retests"]:
        field = "retests." + item["id"]
        shape(item, "id claim_ids kind baseline_observation_id question expected_checks", field)
        texts(item["claim_ids"], field + ".claim_ids", True)
        require(set(item["claim_ids"]) <= set(claims), "unknown_claim", field, "复测关联的断言不存在")
        covered.update(item["claim_ids"])
        choice(item["kind"], {"same_question", "follow_up"}, field + ".kind")
        string(item["question"], field + ".question")
        texts(item["expected_checks"], field + ".expected_checks", True)
        baseline = item["baseline_observation_id"]
        string(baseline, field + ".baseline_observation_id", True)
        require(baseline is None or baseline in observations, "unknown_observation", field, "复测基线不存在")
        if item["kind"] == "same_question":
            require(baseline in observations and observations[baseline]["question"] == item["question"],
                    "same_question_mismatch", field, "同题复测必须逐字保留有记录的原始问题")
            require(all(claims[c]["observation_id"] == baseline for c in item["claim_ids"]),
                    "baseline_mismatch", field, "同题复测断言必须来自该基线")
    require(covered == set(claims), "retest_coverage", "retests", "每条断言都须有复测或补充验证问题")
    return {"status": "ok", "claims": len(claims),
            "verdict_counts": dict(sorted(Counter(c["verdict"] for c in claims.values()).items())),
            "baseline": citation_summary(list(observations.values()))}


def csv_safe(value):
    # Keep spreadsheets from treating user-supplied text as a formula.
    return "'" + value if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r")) else value


def export(data, output_dir):
    result = validate(data)
    output_dir = Path(output_dir)
    require(not output_dir.exists(), "output_exists", "output_dir", "输出目录已存在；请选择新目录")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".repair-", dir=output_dir.parent))
    try:
        sources = {s["id"]: s for s in data["sources"]}
        with (staging / FILES[0]).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["原文记录ID", "断言ID", "原话摘录", "待核对说法", "判定", "理由", "事实证据",
                             "公开答复", "修改优先级", "修改位置", "修改动作", "待补资料"])
            for c in data["claims"]:
                evidence = "\n".join(f'{e["source_id"]} | {sources[e["source_id"]]["title"]} | '
                                     f'{e["relation"]} | {e["quote"]}' for e in c["evidence"])
                row = [c["observation_id"], c["id"], c["quote"], c["proposition"], VERDICTS[c["verdict"]],
                       c["rationale"], evidence, c["public_answer"], c["repair"]["priority"],
                       c["repair"]["location"], c["repair"]["action"], "；".join(c["needed_information"])]
                writer.writerow([csv_safe(cell) for cell in row])
        suffix = "（教学样例）" if data["mode"] == "illustrative" else ""
        parts = [f'# {data["brand"]}：纠正FAQ{suffix}', ""]
        if data["mode"] == "illustrative":
            parts.extend(["以下内容仅演示所给教学资料的处理，不是实际用户案例或AI平台检测结果。", ""])
        for claim in data["claims"]:
            parts.extend(["## " + claim["faq_question"], "", claim["public_answer"], ""])
        (staging / FILES[1]).write_text("\n".join(parts), encoding="utf-8")
        plan = {"schema_version": 1, "brand": data["brand"], "as_of": data["as_of"],
                "mode": data["mode"], "baseline_summary": result["baseline"],
                "baseline_observations": data["observations"],
                "questions": [dict(item, status="not_run", answer=None, native_citations=None)
                              for item in data["retests"]]}
        (staging / FILES[2]).write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.rename(staging, output_dir)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return dict(result, files=FILES)


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate_key", "input", "JSON 对象键不能重复")
            result[key] = value
        return result
    with Path(path).open(encoding="utf-8-sig") as handle:
        return json.load(handle, object_pairs_hook=unique)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "export"):
        sub = subs.add_parser(command)
        sub.add_argument("--input", required=True)
        if command == "export":
            sub.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)
    try:
        data = load(args.input)
        result = validate(data) if args.command == "check" else export(data, args.output_dir)
    except Invalid as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False), file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "code": "input_or_io_error", "message": str(exc)},
                         ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
