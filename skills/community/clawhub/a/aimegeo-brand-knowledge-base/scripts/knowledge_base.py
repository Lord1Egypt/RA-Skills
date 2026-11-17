#!/usr/bin/env python3
"""Validate agent-curated facts, merge evidence, and render a local knowledge base."""

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path, PurePosixPath


class KnowledgeError(ValueError):
    pass


KINDS = {"company": "公司", "product": "产品", "topic": "主题"}
CATEGORIES = {
    "identity": "身份说明", "product": "产品能力", "howto": "操作教程",
    "faq": "常见问答", "trust": "信任材料", "industry": "行业问题",
    "contact": "联系与购买",
}
STATUS = {
    "supported": "有来源支持", "pending": "待核实", "conflict": "存在冲突，暂停用于写作",
    "superseded": "已被新记录替代，仅供追溯",
}


def require(condition, message):
    if not condition:
        raise KnowledgeError(message)


def string(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label} 必须为非空字符串")
    return value


def identifier(value, label):
    string(value, label)
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", value)), f"{label} 必须为小写字母、数字、短横线或下划线，最长64字符")
    return value


def fields(obj, required, optional, label):
    require(isinstance(obj, dict), f"{label} 必须为对象")
    require(set(required) <= obj.keys(), f"{label} 缺少字段：{sorted(set(required) - obj.keys())}")
    require(obj.keys() <= set(required) | set(optional), f"{label} 含未支持字段：{sorted(obj.keys() - set(required) - set(optional))}")


def array(value, label):
    require(isinstance(value, list), f"{label} 必须为数组")
    return value


def iso_date(value, label):
    string(value, label)
    require(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), f"{label} 必须为 YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise KnowledgeError(f"{label} 不是有效日期") from exc
    return value


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).split())


def digest(content):
    return hashlib.sha256(content).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_json(file_path):
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise KnowledgeError(f"无法读取 JSON {file_path.name}: {exc}") from exc


def local_path(root, relative):
    string(relative, "相对路径")
    parts = PurePosixPath(relative)
    require(not parts.is_absolute() and ".." not in parts.parts and "\\" not in relative and ":" not in relative,
            f"路径必须位于资料目录内：{relative}")
    require(relative not in (".", ""), "路径不能指向目录自身")
    candidate = root.joinpath(*parts.parts)
    require(candidate.resolve().is_relative_to(root.resolve()), f"路径越界：{relative}")
    cursor = candidate
    while cursor != root:
        require(not cursor.is_symlink(), f"不读取或覆盖符号链接：{relative}")
        cursor = cursor.parent
    return candidate


def scoped_ids(value, allowed, label):
    array(value, label)
    require(bool(value), f"{label} 不能为空")
    for item in value:
        identifier(item, label)
    require(len(value) == len(set(value)), f"{label} 不能重复")
    require(set(value) <= set(allowed), f"{label} 引用了未知或不适用项目")
    return sorted(value)


def add_immutable(mapping, item, label):
    old = mapping.get(item["id"])
    require(old is None or old == item, f"{label} ID {item['id']} 已存在且内容不同；使用新ID并显式关联更新")
    mapping[item["id"]] = item


def load_previous(output):
    index_path = output / "知识索引.json"
    if not index_path.exists():
        return None
    require(not index_path.is_symlink(), "知识索引不能是符号链接")
    state = read_json(index_path)
    require(isinstance(state, dict) and state.get("schema_version") == 1, "已有知识索引版本不受支持")
    for key in ("kb", "as_of", "projects", "entities", "sources", "records", "gaps", "managed_files"):
        require(key in state, f"已有索引缺少 {key}")
    require(isinstance(state["managed_files"], dict), "已有索引缺少受管文件校验值")
    for relative, expected in state["managed_files"].items():
        file_path = local_path(output, relative)
        require(file_path.is_file() and digest(file_path.read_bytes()) == expected,
                f"原资料或受管文件被修改，停止覆盖：{relative}；先保留改动并将其作为新来源导入")
    return state


def load_sources(payload, previous, input_root, output):
    sources, contents = {}, {}
    for source in (previous or {}).get("sources", []):
        source_path = local_path(output, source["snapshot_path"])
        raw = source_path.read_bytes()
        require(digest(raw) == source["sha256"], f"原始资料校验失败：{source['id']}")
        sources[source["id"]] = source
        contents[source["id"]] = raw
    for source in array(payload.get("sources", []), "sources"):
        fields(source, ["id", "title", "path", "captured_at"], ["url"], "source")
        sid = identifier(source["id"], "source.id")
        string(source["title"], "source.title")
        iso_date(source["captured_at"], "source.captured_at")
        require(source["captured_at"] <= payload["as_of"], "来源日期晚于知识库整理日期")
        source_path = local_path(input_root, source["path"])
        require(source_path.suffix.lower() in (".md", ".txt", ".json"), "来源仅支持 UTF-8 Markdown、TXT、JSON")
        require(source_path.is_file(), f"来源文件不存在：{source['path']}")
        raw = source_path.read_bytes()
        try:
            require(bool(raw.decode("utf-8").strip()), f"来源文件为空：{source['path']}")
        except UnicodeError as exc:
            raise KnowledgeError(f"来源不是 UTF-8：{source['path']}") from exc
        stored = {
            "id": sid, "title": source["title"], "origin": source["path"],
            "captured_at": source["captured_at"], "sha256": digest(raw),
            "snapshot_path": f"原始资料/{sid}{source_path.suffix.lower()}",
        }
        if "url" in source:
            require(isinstance(source["url"], str) and source["url"].startswith(("https://", "http://")), "source.url 必须为HTTP(S)来源地址；脚本不会访问它")
            stored["url"] = source["url"]
        add_immutable(sources, stored, "来源")
        contents[sid] = raw
    return sources, contents


def merge_payload(payload, previous, input_root, output):
    fields(payload, ["schema_version", "kb", "as_of"], ["projects", "entities", "sources", "records", "gaps"], "输入")
    require(type(payload["schema_version"]) is int and payload["schema_version"] == 1, "schema_version 必须为1")
    fields(payload["kb"], ["id", "name"], [], "kb")
    identifier(payload["kb"]["id"], "kb.id")
    string(payload["kb"]["name"], "kb.name")
    iso_date(payload["as_of"], "as_of")
    if previous:
        require(payload["kb"] == previous["kb"], "目标知识库身份不一致：kb.id和kb.name必须同时匹配")
        require(payload["as_of"] >= previous["as_of"], "增量日期不能早于已有知识库日期")
    projects = {p["id"]: p for p in (previous or {}).get("projects", [])}
    for project in array(payload.get("projects", []), "projects"):
        fields(project, ["id", "name"], [], "project")
        identifier(project["id"], "project.id")
        string(project["name"], "project.name")
        add_immutable(projects, project, "项目")
    require(bool(projects), "至少提供一个适用项目")
    entities = {e["id"]: e for e in (previous or {}).get("entities", [])}
    for original in array(payload.get("entities", []), "entities"):
        fields(original, ["id", "kind", "name", "project_ids"], ["parent_id"], "entity")
        entity = dict(original)
        identifier(entity["id"], "entity.id")
        string(entity["name"], "entity.name")
        require(entity["kind"] in KINDS, "entity.kind 必须为 company、product 或 topic")
        entity["project_ids"] = scoped_ids(entity["project_ids"], projects, "entity.project_ids")
        add_immutable(entities, entity, "对象")
    require(bool(entities), "至少提供一个公司、产品或主题对象")
    for entity in entities.values():
        if "parent_id" in entity:
            parent = entities.get(entity["parent_id"])
            require(parent is not None, "entity.parent_id 不存在")
            require((entity["kind"] == "product" and parent["kind"] == "company") or
                    (entity["kind"] == "topic" and parent["kind"] in ("company", "product")), "对象父子类型不匹配")
            require(set(entity["project_ids"]) <= set(parent["project_ids"]), "子对象项目超出父对象适用范围")
    sources, contents = load_sources(payload, previous, input_root, output)
    records = {r["id"]: r for r in (previous or {}).get("records", [])}
    for original in array(payload.get("records", []), "records"):
        fields(original, ["id", "entity_id", "category", "key", "value", "text", "status", "project_ids", "sources"],
               ["question", "supersedes"], "record")
        record = dict(original)
        identifier(record["id"], "record.id")
        identifier(record["key"], "record.key")
        require(record["entity_id"] in entities, "事实引用了未知对象")
        require(record["category"] in CATEGORIES, "事实 category 不受支持")
        for key in ("value", "text"):
            string(record[key], f"record.{key}")
        require(record["status"] in ("supported", "pending"), "输入事实状态只能是 supported 或 pending")
        record["project_ids"] = scoped_ids(record["project_ids"], entities[record["entity_id"]]["project_ids"], "record.project_ids")
        refs = array(record["sources"], "record.sources")
        require(record["status"] != "supported" or bool(refs), "有来源支持的事实必须提供可定位的来源摘录")
        for ref in refs:
            fields(ref, ["source_id", "locator", "quote"], [], "来源引用")
            require(ref["source_id"] in sources, "事实引用了未知来源")
            string(ref["locator"], "来源定位")
            string(ref["quote"], "来源摘录")
            require(normalized(ref["quote"]) in normalized(contents[ref["source_id"]].decode("utf-8")),
                    f"来源摘录与原文不匹配：{record['id']} / {ref['source_id']}")
        if "question" in record:
            string(record["question"], "record.question")
        if record["category"] == "faq":
            require("question" in record, "FAQ必须提供实际问题")
        record["supersedes"] = sorted(array(record.get("supersedes", []), "record.supersedes"))
        require(len(record["supersedes"]) == len(set(record["supersedes"])), "supersedes不能重复")
        add_immutable(records, record, "事实")
    require(bool(records), "没有可交付的正文记录；先整理实际资料，不能仅创建空目录")
    categories = {}
    replacement_scopes = defaultdict(set)
    for record in records.values():
        prop = (record["entity_id"], record["key"])
        require(prop not in categories or categories[prop] == record["category"], "同一对象的事实key不能跨分类使用")
        categories[prop] = record["category"]
        for target_id in record["supersedes"]:
            require(target_id in records and target_id != record["id"], "supersedes必须引用其他已存在事实")
            target = records[target_id]
            require(record["status"] == "supported", "只有有来源支持的新事实可以替代旧事实")
            require(all(record[k] == target[k] for k in ("entity_id", "category", "key")), "替代事实必须属于同一对象、分类和属性")
            require(set(record["project_ids"]) <= set(target["project_ids"]),
                    f"替代事实的项目范围必须是旧记录 {target_id} 的项目范围子集")
            replacement_scopes[target_id].update(record["project_ids"])
    # A record becomes history as a whole. Split successors must retain every
    # original project, including projects whose value did not change.
    for target_id, covered in sorted(replacement_scopes.items()):
        missing = set(records[target_id]["project_ids"]) - covered
        require(not missing,
                f"替代事实必须完整覆盖旧记录 {target_id} 的项目范围；尚缺项目：{', '.join(sorted(missing))}；为未变更项目新增保留原值的替代记录")
    visited, visiting = set(), set()

    def visit(rid):
        require(rid not in visiting, "supersedes存在循环")
        if rid in visited:
            return
        visiting.add(rid)
        for target in records[rid]["supersedes"]:
            visit(target)
        visiting.remove(rid)
        visited.add(rid)

    for rid in records:
        visit(rid)
    gaps = {g["id"]: g for g in (previous or {}).get("gaps", [])}
    for original in array(payload.get("gaps", []), "gaps"):
        fields(original, ["id", "entity_id", "project_ids", "question", "reason"], ["resolved_by"], "gap")
        gap = dict(original)
        identifier(gap["id"], "gap.id")
        require(gap["entity_id"] in entities, "缺失项引用了未知对象")
        gap["project_ids"] = scoped_ids(gap["project_ids"], entities[gap["entity_id"]]["project_ids"], "gap.project_ids")
        string(gap["question"], "gap.question")
        string(gap["reason"], "gap.reason")
        gap["resolved_by"] = sorted(array(gap.get("resolved_by", []), "gap.resolved_by"))
        old = gaps.get(gap["id"])
        require(old is None or {k: v for k, v in old.items() if k != "resolved_by"} ==
                {k: v for k, v in gap.items() if k != "resolved_by"}, "缺失项原始问题不可覆盖；可更新resolved_by")
        gaps[gap["id"]] = gap
    for gap in gaps.values():
        required_projects = set(gap["project_ids"])
        covered_projects = set()
        for rid in gap["resolved_by"]:
            require(rid in records, "缺失项resolved_by引用了未知事实")
            require(records[rid]["entity_id"] == gap["entity_id"] and
                    bool(required_projects & set(records[rid]["project_ids"])),
                    "缺失项解决证据的对象或项目范围不匹配")
            covered_projects.update(records[rid]["project_ids"])
        missing = required_projects - covered_projects
        require(not gap["resolved_by"] or not missing,
                "缺失项解决证据未完整覆盖项目：" + ", ".join(sorted(missing)))
    return projects, entities, sources, contents, records, gaps


def derive_facts(records):
    replaced_by = defaultdict(list)
    for record in records.values():
        for target in record["supersedes"]:
            replaced_by[target].append(record["id"])
    groups = defaultdict(list)
    for rid in sorted(records):
        record = records[rid]
        signature = (record["entity_id"], record["category"], record["key"], normalized(record["value"]),
                     tuple(record["project_ids"]), rid in replaced_by, record["status"])
        groups[signature].append(record)
    facts = []
    for members in groups.values():
        first = members[0]
        refs = {json.dumps(ref, ensure_ascii=False, sort_keys=True): ref for member in members for ref in member["sources"]}
        fact = {k: first[k] for k in ("id", "entity_id", "category", "key", "value", "project_ids")}
        fact.update({
            "record_ids": [member["id"] for member in members],
            "texts": list(dict.fromkeys(member["text"] for member in members)),
            "sources": [refs[key] for key in sorted(refs)],
            "status": "superseded" if first["id"] in replaced_by else
                      ("supported" if any(member["status"] == "supported" for member in members) else "pending"),
            "superseded_by": sorted({new_id for member in members for new_id in replaced_by[member["id"]]}),
            "conflicts_with": [],
        })
        if "question" in first:
            fact["question"] = first["question"]
        facts.append(fact)
    active = [fact for fact in facts if fact["status"] == "supported"]
    for i, left in enumerate(active):
        for right in active[i + 1:]:
            if (left["entity_id"], left["key"]) == (right["entity_id"], right["key"]) and \
                    normalized(left["value"]) != normalized(right["value"]) and \
                    set(left["project_ids"]) & set(right["project_ids"]):
                left["conflicts_with"].append(right["id"])
                right["conflicts_with"].append(left["id"])
    for fact in facts:
        if fact["conflicts_with"]:
            fact["status"] = "conflict"
    return sorted(facts, key=lambda item: item["id"])


def render(payload, projects, entities, sources, contents, records, gaps):
    facts = derive_facts(records)
    files = {source["snapshot_path"]: contents[source["id"]] for source in sources.values()}
    documents = []
    groups = defaultdict(list)
    for fact in facts:
        entity = entities[fact["entity_id"]]
        relative = f"{KINDS[entity['kind']]}/{entity['id']}/{fact['category']}.md"
        fact["document_path"] = relative
        groups[relative].append(fact)
    for relative, members in sorted(groups.items()):
        entity = entities[members[0]["entity_id"]]
        lines = [f"# {entity['name']} · {CATEGORIES[members[0]['category']]}", "",
                 f"对象：{entity['id']}（{KINDS[entity['kind']]}）；整理日期：{payload['as_of']}。", "",
                 "仅“有来源支持”的当前事实可作为写作依据。待核实、冲突和历史记录需保留状态。", ""]
        for fact in members:
            lines += [f"## {fact['question'] if 'question' in fact else fact['key']}", "",
                      f"- 事实ID：{fact['id']}；原记录：{', '.join(fact['record_ids'])}",
                      f"- 状态：{STATUS[fact['status']]}",
                      f"- 适用项目：{', '.join(projects[pid]['name'] + ' (' + pid + ')' for pid in fact['project_ids'])}", ""]
            for text in fact["texts"]:
                lines += [text, ""]
            if fact["conflicts_with"]:
                lines += [f"冲突对象：{', '.join(fact['conflicts_with'])}。需补充版本、适用条件或明确替代关系。", ""]
            if fact["superseded_by"]:
                lines += [f"替代记录：{', '.join(fact['superseded_by'])}。", ""]
            if not fact["sources"]:
                lines += ["来源：尚无可定位材料，不能按已证实事实使用。", ""]
            for ref in fact["sources"]:
                source = sources[ref["source_id"]]
                link = os.path.relpath(source["snapshot_path"], str(PurePosixPath(relative).parent)).replace(os.sep, "/")
                lines += [f"来源：[{source['title']}]({link})；{ref['source_id']}；{ref['locator']}；保存日期 {source['captured_at']}。", "",
                          "> " + ref["quote"].replace("\n", "\n> "), ""]
        files[relative] = ("\n".join(lines).rstrip() + "\n").encode("utf-8")
        documents.append({"path": relative, "entity_id": entity["id"], "category": members[0]["category"],
                          "fact_ids": [fact["id"] for fact in members]})
    effective = {rid: fact["status"] for fact in facts for rid in fact["record_ids"]}
    gap_results = []
    for gap in sorted(gaps.values(), key=lambda item: item["id"]):
        usable = [rid for rid in gap["resolved_by"] if effective[rid] == "supported"]
        covered = {pid for rid in usable for pid in records[rid]["project_ids"]}
        gap_results.append({**gap, "resolved": bool(gap["resolved_by"])
            and len(usable) == len(gap["resolved_by"]) and set(gap["project_ids"]) <= covered})
    stats = {
        "source_count": len(sources), "record_count": len(records), "fact_count": len(facts),
        "usable_fact_count": sum(f["status"] == "supported" for f in facts),
        "conflict_fact_count": sum(f["status"] == "conflict" for f in facts),
        "pending_fact_count": sum(f["status"] == "pending" for f in facts),
        "superseded_fact_count": sum(f["status"] == "superseded" for f in facts),
        "open_gap_count": sum(not gap["resolved"] for gap in gap_results),
    }
    checklist = ["# 缺失与更新清单", "", f"知识库：{payload['kb']['name']}；整理日期：{payload['as_of']}。", "",
                 "## 需要补充的资料", ""]
    if not gap_results:
        checklist += ["本次输入未列出缺失项；这不表示企业所有资料均已齐备。", ""]
    for gap in gap_results:
        checklist += [f"- [{'x' if gap['resolved'] else ' '}] {gap['id']} · {entities[gap['entity_id']]['name']} · {gap['question']}",
                      f"  适用项目：{', '.join(gap['project_ids'])}。原因：{gap['reason']}"]
        if gap["resolved_by"]:
            checklist += [f"  解决证据：{', '.join(gap['resolved_by'])}；{'已解决' if gap['resolved'] else '证据仍不可用，保留缺口'}。"]
    checklist += ["", "## 冲突、待核实与历史", ""]
    needs_attention = [fact for fact in facts if fact["status"] != "supported"]
    if not needs_attention:
        checklist += ["当前记录没有属性冲突或待核实项；来源支持仍需由整理者核对语义。"]
    for fact in needs_attention:
        checklist += [f"- {fact['id']} · {entities[fact['entity_id']]['name']} · {fact['key']}：{STATUS[fact['status']]}。"]
        if fact["conflicts_with"]:
            checklist += [f"  对照记录：{', '.join(fact['conflicts_with'])}。保留双方材料，明确版本或条件后再用supersedes处理。"]
    checklist += ["", "## 后续更新", "",
                  "新增材料使用新来源ID；新事实使用新记录ID。只有明确替代关系才填写supersedes，未提供的旧资料不会删除。",
                  "原文已保存在原始资料目录。手写补充文件会保留；受管正文被人工修改时停止覆盖，请先将改动保存为新来源再导入。", "",
                  "本次仅整理所提供资料，未执行AI回答采集或引用检测；不能据此推断已收录、提及或原生引用数量。", ""]
    files["缺失与更新清单.md"] = ("\n".join(checklist)).encode("utf-8")
    overview = [f"# {payload['kb']['name']}", "", "本地品牌事实源；按公司、产品与主题检索。", "",
                f"整理日期：{payload['as_of']}；来源 {len(sources)} 份；原记录 {len(records)} 条；归并事实 {len(facts)} 条；当前可用 {stats['usable_fact_count']} 条。", "",
                "## 资料索引", ""]
    for document in documents:
        overview += [f"- [{entities[document['entity_id']]['name']} · {CATEGORIES[document['category']]}]({document['path']})"]
    overview += ["", "[知识索引.json](知识索引.json) · [缺失与更新清单](缺失与更新清单.md)", "",
                 "检索时先匹配entity_id与project_ids，再选择status=supported的事实。冲突、待核实和被替代记录不可直接用于肯定陈述。", ""]
    files["知识库目录.md"] = ("\n".join(overview)).encode("utf-8")
    state = {
        "schema_version": 1, "kb": payload["kb"], "as_of": payload["as_of"],
        "projects": sorted(projects.values(), key=lambda item: item["id"]),
        "entities": sorted(entities.values(), key=lambda item: item["id"]),
        "sources": sorted(sources.values(), key=lambda item: item["id"]),
        "records": sorted(records.values(), key=lambda item: item["id"]),
        "gaps": [{k: v for k, v in gap.items() if k != "resolved"} for gap in gap_results],
        "gap_results": gap_results, "facts": facts, "documents": documents, "stats": stats,
        "managed_files": {relative: digest(raw) for relative, raw in sorted(files.items())},
    }
    files["知识索引.json"] = encoded(state)
    return files, stats


def build(input_file, output):
    input_file = input_file.resolve()
    require(input_file.is_file(), "输入JSON不存在")
    require(not output.is_symlink(), "输出目录不能是符号链接")
    output = output.resolve()
    require(not output.is_relative_to(input_file.parent), "输出目录必须位于输入资料目录之外，避免覆盖原资料")
    require(not output.exists() or output.is_dir(), "输出位置不是目录")
    payload = read_json(input_file)
    previous = load_previous(output)
    merged = merge_payload(payload, previous, input_file.parent, output)
    files, stats = render(payload, *merged)
    managed = (previous or {}).get("managed_files", {})
    for relative in files:
        target = local_path(output, relative)
        require(not target.exists() or (target.is_file() and (relative in managed or
                (previous is not None and relative == "知识索引.json"))), f"拒绝覆盖非本工具管理的文件：{relative}")
        for ancestor in target.parents:
            if ancestor == output:
                break
            require(not ancestor.exists() or ancestor.is_dir(), f"输出父路径不是目录：{relative}")
    for relative, raw in files.items():
        target = local_path(output, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() == raw:
            continue
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".kb-", delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(raw)
            os.replace(temporary, target)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    return {"status": "ok", "kb_id": payload["kb"]["id"], "stats": stats}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    builder = sub.add_parser("build", help="校验、增量归并并导出知识库")
    builder.add_argument("--input", required=True, type=Path)
    builder.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = build(args.input, args.output)
    except (KnowledgeError, OSError, UnicodeError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
