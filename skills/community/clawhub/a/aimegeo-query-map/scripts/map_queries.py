#!/usr/bin/env python3
"""Validate Agent annotations, merge question groups, and export a content map.

Uses the Python standard library only. It never fetches URLs or writes articles.
"""

import argparse
import csv
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unicodedata
from collections import Counter
from datetime import datetime
from urllib.parse import urlparse


CSV_NAME = "问题—主题—内容形式映射表.csv"
AUDIT_NAME = "map-audit.json"
INTENTS = {"information", "navigation", "operation", "troubleshooting", "comparison", "decision"}
ORIGINS = {"user_question", "agent_hypothesis", "model_simulation"}
ORIGIN_LABELS = {"user_question": "输入原题", "agent_hypothesis": "待验证假设", "model_simulation": "模拟假设"}
STATUS_LABELS = {"simulated": "模拟", "not_run": "未运行", "query_failed": "查询失败", "observed": "已提供回答记录"}
COVERAGE_LABELS = {"gap": "主题缺口", "partial": "部分覆盖", "covered": "已覆盖", "unknown": "覆盖未知"}
IMPACT_ORDER = {"high": 0, "medium": 1, "low": 2}


class MapError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(condition, code, message):
    if not condition:
        raise MapError(code, message)


def obj(value, keys, where, optional=()):
    require(isinstance(value, dict), "SCHEMA", f"{where} 必须是对象")
    require(set(keys) <= set(value) <= set(keys) | set(optional), "SCHEMA", f"{where} 字段缺失或含不支持字段")


def string(value, where, empty=False):
    require(isinstance(value, str) and (empty or value.strip()), "SCHEMA", f"{where} 必须是{'可为空的' if empty else '非空'}字符串")
    return value


def sequence(value, where, nonempty=False):
    require(isinstance(value, list) and (not nonempty or value), "SCHEMA", f"{where} 必须是{'非空' if nonempty else ''}数组")
    return value


def choice(value, values, where):
    require(isinstance(value, str) and value in values, "SCHEMA", f"{where} 不在允许值中")


def unique_id(value, seen, where):
    string(value, where)
    require(value not in seen, "DUPLICATE_ID", f"{where} ID 重复：{value}")
    seen.add(value)


def normalized(text):
    return "".join(c for c in unicodedata.normalize("NFKC", text).casefold()
                   if not c.isspace() and not unicodedata.category(c).startswith("P"))


def dedupe(items):
    result = []
    seen = set()
    for item in items:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def validate_records(records, keys):
    ids = set()
    for record in sequence(records, "answer_records"):
        obj(record, ("id", "merge_key", "status", "platform", "prompt", "answer", "source", "captured_at", "native_citations", "mentions", "error"), "answer_records[]")
        unique_id(record["id"], ids, "answer_records[].id")
        string(record["merge_key"], "record.merge_key")
        require(record["merge_key"] in keys, "UNKNOWN_GROUP", "回答记录关联的问题组不存在")
        status = record["status"]
        choice(status, STATUS_LABELS, "record.status")
        string(record["platform"], "record.platform")
        string(record["prompt"], "record.prompt")
        string(record["source"], "record.source", empty=True)
        if record["captured_at"] is not None:
            try:
                stamp = datetime.fromisoformat(string(record["captured_at"], "record.captured_at").replace("Z", "+00:00"))
                require(stamp.tzinfo is not None and stamp.utcoffset() is not None, "RECORD_STATE", "时间必须含时区")
            except ValueError as exc:
                raise MapError("RECORD_STATE", "captured_at 必须是带时区的 ISO 8601 时间") from exc
        if status == "observed":
            string(record["answer"], "record.answer")
            string(record["source"], "record.source")
            require(record["captured_at"] is not None and record["error"] is None, "RECORD_STATE", "已提供回答须含时间且无错误")
            if record["mentions"] is not None:
                for mention in sequence(record["mentions"], "record.mentions"):
                    string(mention, "mention")
                    require(mention in record["answer"], "MENTION_EVIDENCE", "提及文本须出现在所提供回答中")
            if record["native_citations"] is not None:
                for citation in sequence(record["native_citations"], "record.native_citations"):
                    obj(citation, ("url", "label"), "citation")
                    string(citation["url"], "citation.url")
                    string(citation["label"], "citation.label")
                    parsed = urlparse(citation["url"])
                    require(parsed.scheme in {"http", "https"} and parsed.netloc, "CITATION_URL", "原生引用须有 HTTP(S) URL")
        else:
            require(record["native_citations"] is None and record["mentions"] is None, "RECORD_STATE", "模拟、未运行、查询失败的提及和原生引用必须为 null")
            if status == "simulated":
                string(record["answer"], "simulated.answer")
                require(record["error"] is None, "RECORD_STATE", "模拟记录不能含查询错误")
            else:
                require(record["answer"] is None, "RECORD_STATE", "未运行、查询失败的回答必须为 null")
                if status == "query_failed":
                    string(record["error"], "query_failed.error")
                else:
                    require(record["error"] is None, "RECORD_STATE", "未运行不能含查询错误")


def validate(data):
    obj(data, ("business", "articles", "questions"), "root", optional=("answer_records",))
    business = data["business"]
    obj(business, ("description", "audience", "goal", "inventory_status"), "business")
    for key in ("description", "audience", "goal"):
        string(business[key], f"business.{key}")
    choice(business["inventory_status"], {"unprovided", "partial", "reviewed"}, "business.inventory_status")
    articles = {}
    for article in sequence(data["articles"], "articles"):
        obj(article, ("id", "title", "material", "text", "source"), "article")
        string(article["id"], "article.id")
        require(article["id"] not in articles, "DUPLICATE_ID", "文章 ID 重复")
        articles[article["id"]] = article
        for key in ("title", "source"):
            string(article[key], f"article.{key}")
        choice(article["material"], {"title", "excerpt", "full_text"}, "article.material")
        string(article["text"], "article.text", empty=article["material"] == "title")
        require(article["material"] != "title" or article["text"] == "", "INVENTORY_STATE", "仅标题资料的 text 必须为空")
    inventory = business["inventory_status"]
    require(inventory != "unprovided" or not articles, "INVENTORY_STATE", "未提供库存时 articles 须为空")
    require(inventory != "reviewed" or all(a["material"] == "full_text" for a in articles.values()), "INVENTORY_STATE", "完整核对库存须提供每篇全文；标题或节选只能记 partial")
    ids, literal_groups, groups = set(), {}, {}
    fields = ("id", "question", "merge_key", "audience", "entity", "intent", "scope", "theme", "origin", "facts", "format", "next_step", "impact", "impact_reason", "article_links")
    for question in sequence(data["questions"], "questions", nonempty=True):
        obj(question, fields, "question")
        unique_id(question["id"], ids, "question.id")
        for key in ("question", "merge_key", "audience", "entity", "scope", "theme", "format", "next_step", "impact_reason"):
            string(question[key], f"question.{key}")
        require(normalized(question["question"]), "SCHEMA", "问题不能仅由标点组成")
        choice(question["intent"], INTENTS, "question.intent")
        choice(question["impact"], IMPACT_ORDER, "question.impact")
        obj(question["origin"], ("kind", "source"), "question.origin")
        choice(question["origin"]["kind"], ORIGINS, "origin.kind")
        string(question["origin"]["source"], "origin.source")
        for fact in sequence(question["facts"], "question.facts", nonempty=True):
            obj(fact, ("need", "status", "source"), "fact")
            string(fact["need"], "fact.need")
            choice(fact["status"], {"available", "missing"}, "fact.status")
            string(fact["source"], "fact.source", empty=fact["status"] == "missing")
            require(fact["status"] != "missing" or fact["source"] == "", "FACT_STATE", "缺失事实不能填写已用来源")
        for link in sequence(question["article_links"], "question.article_links"):
            obj(link, ("article_id", "coverage", "evidence", "reason"), "article_link")
            string(link["article_id"], "link.article_id")
            require(link["article_id"] in articles, "UNKNOWN_ARTICLE", "文章关联 ID 不存在")
            article = articles[link["article_id"]]
            choice(link["coverage"], {"full", "partial", "unknown"}, "link.coverage")
            string(link["reason"], "link.reason")
            string(link["evidence"], "link.evidence", empty=link["coverage"] == "unknown")
            if link["coverage"] != "unknown":
                require(article["material"] != "title", "TITLE_ONLY_COVERAGE", "文章标题不能证明已覆盖问题")
                require(link["evidence"] in article["text"], "COVERAGE_EVIDENCE", "覆盖证据须逐字出现在所提供正文中")
        signature = tuple(question[key] for key in ("audience", "entity", "intent", "scope", "theme"))
        literal = (normalized(question["question"]), signature)
        merge_key = question["merge_key"]
        require(literal not in literal_groups or literal_groups[literal] == merge_key, "DUPLICATE_SPLIT", "同一受众和意图的字面重复问题须使用同一 merge_key")
        literal_groups[literal] = merge_key
        if merge_key in groups:
            require(signature == groups[merge_key][0], "MERGE_CONFLICT", "同一组的受众、实体、意图、范围与主题须一致")
            groups[merge_key][1].append(question)
        else:
            groups[merge_key] = (signature, [question])
    for _, members in groups.values():
        fact_states = {}
        for member in members:
            for fact in member["facts"]:
                key = normalized(fact["need"])
                require(key not in fact_states or fact_states[key] == fact["status"], "FACT_CONFLICT", "合并组内同一事实的缺失/可用状态冲突，须先核实")
                fact_states[key] = fact["status"]
    validate_records(data.get("answer_records", []), set(groups))
    return groups


def build_map(data):
    groups = validate(data)
    result = []
    for merge_key, (_, members) in groups.items():
        first = members[0]
        links = dedupe([link for q in members for link in q["article_links"]])
        facts = dedupe([fact for q in members for fact in q["facts"]])
        levels = {link["coverage"] for link in links}
        if "full" in levels:
            coverage = "covered"
        elif "partial" in levels:
            coverage = "partial"
        elif links or data["business"]["inventory_status"] != "reviewed":
            coverage = "unknown"
        else:
            coverage = "gap"
        ready = all(fact["status"] == "available" for fact in facts)
        impact = min((q["impact"] for q in members), key=IMPACT_ORDER.get)
        if not ready:
            priority, reason = "P1", "先补事实资料，再决定新建或更新"
        elif coverage == "unknown":
            priority, reason = "P1", "先核对已有文章，避免重复生产"
        elif coverage == "covered":
            priority, reason = "P2", "已有文章可回答，优先复用与维护"
        elif impact == "high":
            priority, reason = "P0", "高决策影响且资料可用，安排新建或补充"
        else:
            priority, reason = "P1", "存在缺口，按团队产能排期"
        result.append({
            "id": first["id"], "merge_key": merge_key, "question": first["question"],
            "source_ids": [q["id"] for q in members],
            "variants": dedupe([q["question"] for q in members]),
            "audience": first["audience"], "entity": first["entity"], "intent": first["intent"],
            "scope": first["scope"], "theme": first["theme"],
            "origins": [{"question_id": q["id"], "question": q["question"], **q["origin"]} for q in members],
            "facts": facts, "formats": dedupe([q["format"] for q in members]),
            "next_steps": dedupe([q["next_step"] for q in members]),
            "impact": impact, "impact_reasons": dedupe([q["impact_reason"] for q in members]),
            "article_links": links, "coverage": coverage, "facts_ready": ready,
            "priority": priority, "priority_reason": reason,
            "answer_statuses": dedupe([r["status"] for r in data.get("answer_records", []) if r["merge_key"] == merge_key]) or ["not_run"],
            "search_volume": None,
        })
    result.sort(key=lambda g: (g["priority"], IMPACT_ORDER[g["impact"]], g["merge_key"]))
    return {
        "business": data["business"],
        "summary": {"input_questions": len(data["questions"]), "canonical_questions": len(result),
                    "merged_questions": len(data["questions"]) - len(result),
                    "coverage": dict(Counter(g["coverage"] for g in result)),
                    "priorities": dict(Counter(g["priority"] for g in result))},
        "groups": result, "articles": data["articles"], "answer_records": data.get("answer_records", []),
    }


def safe_cell(value):
    text = str(value)
    if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
        return "'" + text
    return text


def render_csv(report):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(("问题ID", "归并键", "用户问题", "原题ID", "问题说法", "问题依据", "受众", "实体", "意图", "主题", "范围", "事实资料", "资料是否齐备", "已有文章", "覆盖状态", "建议形式", "下一步", "优先级", "排序理由", "业务影响理由", "搜索量", "回答核验状态"))
    for group in report["groups"]:
        facts = "；".join(f"{f['need']}：{'可用，来源 '+f['source'] if f['status']=='available' else '待补'}" for f in group["facts"])
        origins = "；".join(f"{o['question_id']} {ORIGIN_LABELS[o['kind']]}（{o['source']}）：{o['question']}" for o in group["origins"])
        row = (group["id"], group["merge_key"], group["question"], "；".join(group["source_ids"]),
               "；".join(group["variants"]), origins, group["audience"], group["entity"], group["intent"], group["theme"], group["scope"], facts,
               "是" if group["facts_ready"] else "否", "；".join(dedupe([l["article_id"] for l in group["article_links"]])),
               COVERAGE_LABELS[group["coverage"]], "；".join(group["formats"]), "；".join(group["next_steps"]), group["priority"],
               group["priority_reason"], "；".join(group["impact_reasons"]), "未知（未提供测量）",
               "；".join(STATUS_LABELS[s] for s in group["answer_statuses"]))
        writer.writerow([safe_cell(cell) for cell in row])
    return stream.getvalue()


def no_duplicate_json_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "SCHEMA", f"JSON 键重复：{key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Agent 标注的本地 JSON")
    parser.add_argument("--output-dir", type=Path, required=True, help="输出目录；不会覆盖已有结果")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"), object_pairs_hook=no_duplicate_json_keys)
        report = build_map(data)
        output = args.output_dir
        require(not output.exists() or output.is_dir(), "OUTPUT_PATH", "输出路径不是目录")
        require(not any((output / name).exists() or (output / name).is_symlink() for name in (CSV_NAME, AUDIT_NAME)), "OUTPUT_EXISTS", "输出文件已存在，请选择新目录")
        csv_text = render_csv(report)
        audit_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        output.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".query-map-", dir=output) as stage:
            stage = Path(stage)
            (stage / CSV_NAME).write_text(csv_text, encoding="utf-8-sig", newline="")
            (stage / AUDIT_NAME).write_text(audit_text, encoding="utf-8")
            for name in (CSV_NAME, AUDIT_NAME):
                os.replace(stage / name, output / name)
        print(json.dumps({"ok": True, **report["summary"], "files": [CSV_NAME, AUDIT_NAME]}, ensure_ascii=False))
        return 0
    except (MapError, OSError, ValueError, TypeError, RecursionError) as exc:
        print(json.dumps({"ok": False, "code": getattr(exc, "code", "INPUT_OUTPUT"), "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
