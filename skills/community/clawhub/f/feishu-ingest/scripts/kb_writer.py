import json
from pathlib import Path

from catalog import catalog_entry, catalog_from_raw, merge_catalog, render_index
from gitea_api import GiteaClient
from utils import extract_keywords, now, safe_relpath, sha256_text, strip_frontmatter, unique


ALLOWED_ROOTS = {
    "overview",
    "projects",
    "papers",
    "surveys",
    "code",
    "meetings",
    "experiments",
    "tech-notes",
    "notes",
    "concepts",
    "resources",
}
TYPE_BY_ROOT = {
    "overview": "overview",
    "projects": "project",
    "papers": "paper",
    "surveys": "survey",
    "code": "code",
    "meetings": "meeting",
    "experiments": "experiment",
    "tech-notes": "tech-note",
    "notes": "note",
    "concepts": "concept",
    "resources": "resource",
}
RELATION_ROOTS = ALLOWED_ROOTS | {"qa"}
RELATION_FIELDS = (
    ("relatedConcepts", "相关概念"),
    ("relatedResources", "相关资源"),
    ("relatedCodePages", "相关代码页"),
    ("relatedPages", "相关页面"),
)


def apply_pages(payload, pages_doc, context=None):
    context = context or {}
    pages_doc = pages_doc if isinstance(pages_doc, dict) else {"pages": pages_doc if isinstance(pages_doc, list) else []}
    pages = normalize_pages(pages_doc)
    source = payload.get("source") or {}
    source_id = source.get("id") or payload.get("sourceId") or "unknown"
    items = {str(item.get("itemKey") or ""): item for item in context.get("inputItems") or [] if item.get("itemKey")}
    if not items:
        items = source_items_from_payload(payload)

    required_keys = {key for key, item in items.items() if bool(item.get("required"))}
    if not pages:
        if required_keys:
            raise ValueError("Feishu files/documents require at least one generated page; missing required sourceItemKeys: " + ", ".join(sorted(required_keys)))
        return empty_success(payload, pages_doc, context)

    normalized_pages = []
    covered_item_keys = set()
    for page in pages:
        normalized = normalize_page(page, items)
        normalized_pages.append(normalized)
        covered_item_keys.update(normalized.get("sourceItemKeys") or [])

    missing = sorted(required_keys - covered_item_keys)
    if missing:
        raise ValueError("Every required Feishu file/document must appear in at least one page; missing sourceItemKeys: " + ", ".join(missing))

    client = GiteaClient(payload)
    archive_map = archive_source_files(client, source_id, items, covered_item_keys)
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    created = []
    updated = []
    entries = []
    commit = ""

    for page in normalized_pages:
        path = page["path"]
        content = build_page_content(payload, page, items, archive_map)
        page["contentHash"] = sha256_text(strip_frontmatter(content))
        existed = client.exists(path)
        client.upsert_text(path, content, f"OpenClaw update {path}")
        commit = client.last_commit
        entry = catalog_entry(page)
        entries.append(entry)
        (updated if existed else created).append(entry)

    catalog = merge_catalog(catalog, entries)
    client.upsert_text("catalog.json", json.dumps(catalog, ensure_ascii=False, indent=2), "OpenClaw update catalog.json")
    commit = client.last_commit
    client.upsert_text("index.md", render_index(catalog), "OpenClaw update index.md")
    commit = client.last_commit

    skipped_sources = normalize_skipped(context.get("skippedSources") or []) + normalize_skipped(pages_doc.get("skippedSources") or [])
    errors = normalize_errors(pages_doc.get("errors") or [])
    snapshot = build_snapshot(pages_doc, context, source_id, covered_item_keys, archive_map)
    source_items = source_items_for_result(context, items, covered_item_keys, archive_map, normalized_pages)
    return {
        "success": True,
        "processedSources": sorted(covered_item_keys),
        "createdPages": created,
        "updatedPages": updated,
        "archivedFiles": [archive_map[key] for key in sorted(archive_map)],
        "skippedSources": skipped_sources,
        "errors": errors,
        "commitId": commit,
        "snapshot": snapshot,
        "sourceItems": source_items,
    }


def empty_success(payload, pages_doc, context):
    source = payload.get("source") or {}
    source_id = source.get("id") or payload.get("sourceId") or "feishu"
    skipped = normalize_skipped(context.get("skippedSources") or []) + normalize_skipped(pages_doc.get("skippedSources") or [])
    if not skipped:
        skipped = [{"reason": "no_valuable_feishu_messages", "message": "OpenClaw judged the fetched Feishu message segments not worth writing to the KB."}]
    snapshot = build_snapshot(pages_doc, context, source_id, set(), {})
    items = {str(item.get("itemKey") or ""): item for item in context.get("inputItems") or [] if item.get("itemKey")}
    if not items:
        items = source_items_from_payload(payload)
    source_items = source_items_for_result(context, items, set(), {}, [])
    return {
        "success": True,
        "processedSources": [source_id],
        "createdPages": [],
        "updatedPages": [],
        "archivedFiles": [],
        "skippedSources": skipped,
        "errors": normalize_errors(pages_doc.get("errors") or []),
        "commitId": "",
        "snapshot": snapshot,
        "sourceItems": source_items,
    }


def normalize_pages(pages_doc):
    if isinstance(pages_doc, list):
        return [page for page in pages_doc if isinstance(page, dict)]
    if not isinstance(pages_doc, dict):
        raise ValueError("pages JSON must be an object or array")
    pages = pages_doc.get("pages")
    if pages is None:
        pages = (pages_doc.get("createdPages") or []) + (pages_doc.get("updatedPages") or [])
    if not isinstance(pages, list):
        raise ValueError("pages must be a list")
    return [page for page in pages if isinstance(page, dict)]


def normalize_page(page, items):
    path = validate_page_path(page.get("path") or "")
    content = str(page.get("content") or page.get("body") or "").strip()
    if not content:
        raise ValueError(f"Page {path} is missing content/body")
    source_item_keys = source_keys_for_page(page, items)
    if not source_item_keys:
        raise ValueError(f"Page {path} must include sourceItemKeys referencing input items")
    page = dict(page)
    page["path"] = path
    page["type"] = page.get("type") or type_from_path(path)
    page["title"] = page.get("title") or title_from_path(path)
    page["kbType"] = page.get("kbType") or page.get("kb_type") or kb_type_for_path(path)
    page["sourceItemKeys"] = source_item_keys
    page["sourceIds"] = unique(page.get("sourceIds") or [items[key].get("sourceId") for key in source_item_keys if key in items and items[key].get("sourceId") not in (None, "")])
    page["projectIds"] = unique(page.get("projectIds") or ["general"])
    page["keywords"] = unique(page.get("keywords") or extract_keywords((page.get("title") or "") + "\n" + content))
    page["relatedConcepts"] = normalize_relation_paths(page.get("relatedConcepts") or [])
    page["relatedResources"] = normalize_relation_paths(page.get("relatedResources") or [])
    page["relatedCodePages"] = normalize_relation_paths(page.get("relatedCodePages") or [])
    page["relatedPages"] = normalize_relation_paths(page.get("relatedPages") or [])
    page["sourceStatus"] = page.get("sourceStatus") or "active"
    return page


def source_keys_for_page(page, items):
    raw = page.get("sourceItemKeys") or page.get("sourceItemKey") or page.get("itemKeys") or page.get("itemKey") or []
    if isinstance(raw, (str, int)):
        raw = [raw]
    keys = []
    for key in raw or []:
        keys.extend(match_source_candidate(key, items))
    for source in page.get("sources") or []:
        if not isinstance(source, dict):
            continue
        for candidate in [source.get("itemKey"), source.get("sourceItemKey"), source.get("sha256")]:
            keys.extend(match_source_candidate(candidate, items))
    if not keys and len(items) == 1:
        keys = list(items.keys())
    return unique(keys)


def match_source_candidate(candidate, items):
    key = str(candidate or "")
    if not key:
        return []
    if key in items:
        return [key]
    matches = [item_key for item_key, item in items.items() if str(item.get("sha256") or "") == key]
    return matches if len(matches) == 1 else []


def normalize_relation_paths(values):
    result = []
    for raw in values or []:
        value = raw
        if isinstance(raw, dict):
            value = raw.get("path") or raw.get("target") or raw.get("href") or ""
        if not isinstance(value, str):
            continue
        value = value.strip()
        if value.startswith("[[") and "]]" in value:
            value = value[2:value.find("]]")]
        if "|" in value:
            value = value.split("|", 1)[0].strip()
        if not value:
            continue
        if not value.endswith(".md"):
            value = value.rstrip("/") + ".md"
        try:
            path = safe_relpath(value)
        except ValueError:
            continue
        root = path.split("/", 1)[0]
        if root not in RELATION_ROOTS or path.startswith("source_files/") or "/" not in path:
            continue
        result.append(path)
    return unique(result)


def validate_page_path(path):
    value = safe_relpath(path)
    if not value.endswith(".md"):
        raise ValueError(f"Page path must end with .md: {path}")
    root = value.split("/", 1)[0]
    if root == "qa":
        raise ValueError("feishu_ingest must not write qa/ pages")
    if root not in ALLOWED_ROOTS:
        raise ValueError(f"feishu_ingest cannot write {path}. Allowed roots: {', '.join(sorted(ALLOWED_ROOTS))}")
    return value


def archive_source_files(client, source_id, items, keys_to_archive):
    archive_map = {}
    for key in sorted(keys_to_archive):
        item = items.get(key)
        if not item:
            continue
        storage_path = item.get("storagePath") or item.get("archived_path") or item.get("archivedPath")
        source_path = Path(str(storage_path or ""))
        if not source_path.exists() or not source_path.is_file():
            continue
        sha = item.get("sha256") or key
        identity8 = sha256_text(str(key) + "\n" + str(item.get("relativePath") or item.get("fileName") or ""))[:8]
        ext = source_path.suffix or Path(str(item.get("fileName") or "")).suffix or ".bin"
        base = slug_for_archive(item)
        subdir = archive_subdir(item)
        archive_path = f"source_files/feishu/{source_id}/{subdir}/{now()[:10]}-{base}-{str(sha)[:8]}-{identity8}{ext}"
        try:
            client.upsert_bytes(archive_path, source_path.read_bytes(), f"Archive Feishu source file {archive_path}")
        except Exception as exc:
            archive_path = f"source_files/feishu/{source_id}/{subdir}/{now()[:10]}-{base}-{identity8}.md"
            client.upsert_text(archive_path, render_source_registration(item, str(exc)), f"Register Feishu source file {archive_path}")
        archive_map[key] = archive_path
    return archive_map


def slug_for_archive(item):
    name = item.get("fileName") or item.get("title") or item.get("itemKey") or "source"
    return safe_slug(Path(str(name)).stem or name)


def archive_subdir(item):
    kind = item.get("sourceKind") or ""
    if kind == "feishu_message_segment":
        return "messages"
    if kind == "feishu_document":
        return "documents"
    return "files"


def build_page_content(payload, page, items, archive_map):
    body = strip_frontmatter(page.get("content") or page.get("body") or "")
    title = page.get("title") or title_from_path(page.get("path"))
    if not body.startswith("#"):
        body = f"# {title}\n\n{body}".strip()
    body = append_relation_section(body, page)
    data = {
        "id": page.get("id") or page.get("path", "").replace("/", "-").replace(".md", ""),
        "title": title,
        "type": page.get("type") or type_from_path(page.get("path")),
        "kbType": page.get("kbType") or kb_type_for_path(page.get("path")),
        "projectIds": page.get("projectIds") or ["general"],
        "tags": page.get("tags") or [],
        "keywords": page.get("keywords") or extract_keywords(title + "\n" + body),
        "createdAt": page.get("createdAt") or now(),
        "updatedAt": now(),
        "generatedBy": "openclaw:feishu_ingest",
        "contentHash": sha256_text(body),
        "sourceStatus": page.get("sourceStatus") or "active",
        "relatedConcepts": page.get("relatedConcepts") or [],
        "relatedResources": page.get("relatedResources") or [],
        "relatedCodePages": page.get("relatedCodePages") or [],
        "relatedPages": page.get("relatedPages") or [],
        "sources": source_traces(payload, page, items, archive_map),
    }
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def append_relation_section(body, page):
    if any(heading in body for heading in ("## 关联页面", "## 知识关联", "## 相关页面")):
        return body
    lines = []
    seen = set()
    for field, label in RELATION_FIELDS:
        for raw in page.get(field) or []:
            path, title = relation_target(raw)
            if not path or path in seen:
                continue
            seen.add(path)
            lines.append(f"- {label}: [[{path}|{title}]]")
    if not lines:
        return body
    return body.rstrip() + "\n\n## 关联页面\n\n" + "\n".join(lines)


def relation_target(raw):
    title = ""
    value = raw
    if isinstance(raw, dict):
        title = str(raw.get("title") or raw.get("label") or "")
        value = raw.get("path") or raw.get("target") or ""
    if not isinstance(value, str):
        return "", ""
    value = value.strip()
    if value.startswith("[[") and "]]" in value:
        value = value[2:value.find("]]")]
    if "|" in value:
        value, alias = value.split("|", 1)
        title = title or alias.strip()
    if value.endswith(".md"):
        value = value[:-3]
    try:
        path = safe_relpath(value)
    except ValueError:
        return "", ""
    if not path or path.startswith("source_files/"):
        return "", ""
    return path, title or title_from_path(path)


def source_traces(payload, page, items, archive_map):
    source = payload.get("source") or {}
    traces = []
    for key in page.get("sourceItemKeys") or []:
        item = items.get(key)
        if not item:
            continue
        traces.append({
            "sourceId": source.get("id") or payload.get("sourceId") or item.get("sourceId"),
            "sourceType": "feishu",
            "platform": "feishu",
            "sourceKind": item.get("sourceKind") or "",
            "title": item.get("title") or item.get("fileName") or key,
            "fileName": item.get("fileName") or "",
            "originalPath": item.get("relativePath") or "",
            "archivedPath": archive_map.get(key) or "",
            "url": item.get("url") or "",
            "externalId": item.get("externalId") or item.get("messageId") or item.get("fileKey") or "",
            "chatId": item.get("chatId") or "",
            "messageId": item.get("messageId") or "",
            "messageIds": item.get("messageIds") or [],
            "sentAt": item.get("sentAt") or item.get("firstMessageAt") or "",
            "sha256": item.get("sha256") or key,
            "status": "active",
            "ingestedAt": now(),
        })
    return traces


def build_snapshot(pages_doc, context, source_id, covered_item_keys, archive_map):
    snapshot = {}
    snapshot.update(context.get("snapshot") or {})
    snapshot.update(pages_doc.get("snapshot") or {})
    scan = context.get("scanWindow") or {}
    if scan.get("latestMessageCreateTime"):
        snapshot["lastMessageCreateTime"] = scan.get("latestMessageCreateTime")
        snapshot["lastMessageCreateTimeIso"] = scan.get("latestMessageCreateTimeIso") or snapshot.get("lastMessageCreateTimeIso") or ""
    snapshot.update({
        "sourceId": source_id,
        "processedItemKeys": sorted(covered_item_keys),
        "archivedFiles": [archive_map[key] for key in sorted(archive_map)],
        "messageCandidateCount": len([item for item in context.get("inputItems") or [] if item.get("sourceKind") == "feishu_message_segment"]),
        "requiredItemCount": len([item for item in context.get("inputItems") or [] if item.get("required")]),
        "writtenPageCount": len(normalize_pages(pages_doc)),
    })
    return snapshot



def source_items_for_result(context, items, covered_item_keys, archive_map, pages):
    page_paths_by_key = {}
    for page in pages or []:
        path = page.get("path") or ""
        for key in page.get("sourceItemKeys") or []:
            page_paths_by_key.setdefault(str(key), []).append(path)
    records = {}
    for key, item in (items or {}).items():
        covered = key in covered_item_keys
        record = source_item_record_for_item(
            key,
            item,
            "ingested" if covered else "skipped",
            archive_map.get(key) or item.get("archivedPath") or item.get("archived_path") or "",
            unique(page_paths_by_key.get(key) or []),
            "" if covered else "OpenClaw did not select this optional Feishu item for KB writing.",
        )
        records[key] = record
    for raw in context.get("sourceItems") or []:
        if not isinstance(raw, dict):
            continue
        key = str(raw.get("itemKey") or raw.get("item_key") or raw.get("sha256") or "")
        if not key or key in records:
            continue
        record = dict(raw)
        record.setdefault("kind", record.get("sourceKind") or "feishu_item")
        record.setdefault("sourceKind", record.get("kind") or "feishu_item")
        record.setdefault("status", "skipped")
        record.setdefault("metadata", {k: v for k, v in raw.items() if k not in {"metadata"}})
        records[key] = record
    return [records[key] for key in sorted(records)]


def source_item_record_for_item(key, item, status, archived_path, page_paths, last_error):
    metadata = dict(item)
    metadata.pop("storagePath", None)
    metadata.pop("textPreview", None)
    metadata["pagePaths"] = page_paths
    metadata["statusReason"] = last_error
    return {
        "sourceId": item.get("sourceId"),
        "itemKey": key,
        "sourceKind": item.get("sourceKind") or item.get("kind") or "feishu_item",
        "kind": item.get("sourceKind") or item.get("kind") or "feishu_item",
        "status": status,
        "title": item.get("title") or item.get("fileName") or key,
        "fileName": item.get("fileName") or "",
        "relativePath": item.get("relativePath") or item.get("originalPath") or "",
        "archivedPath": archived_path,
        "url": item.get("url") or "",
        "externalId": item.get("externalId") or item.get("messageId") or item.get("fileKey") or "",
        "messageTime": item.get("messageTime") or item.get("sentAt") or item.get("firstMessageAt") or "",
        "sha256": item.get("sha256") or key,
        "size": item.get("size") or 0,
        "pagePaths": page_paths,
        "lastError": last_error,
        "metadata": metadata,
    }

def source_items_from_payload(payload):
    source = payload.get("source") or {}
    result = {}
    for item in source.get("items") or []:
        if not isinstance(item, dict):
            continue
        key = str(item.get("itemKey") or item.get("item_key") or item.get("sha256") or "")
        if not key:
            continue
        result[key] = {
            "sourceId": source.get("id") or payload.get("sourceId"),
            "itemKey": key,
            "sourceKind": item.get("kind") or "feishu_item",
            "required": False,
            "title": item.get("title") or key,
            "fileName": item.get("fileName") or item.get("file_name") or "",
            "relativePath": item.get("original_path") or item.get("title") or "",
            "storagePath": item.get("storagePath") or item.get("archived_path") or item.get("archivedPath") or "",
            "sha256": item.get("sha256") or key,
            "readable": True,
        }
    return result


def render_source_registration(item, error):
    title = item.get("title") or item.get("fileName") or item.get("itemKey") or "Feishu source"
    data = dict(item)
    data["archiveError"] = error
    data["registeredAt"] = now()
    data.pop("textPreview", None)
    return "\n".join([
        f"# 飞书源文件登记：{title}",
        "",
        "原始字节未能归档，以下为来源登记。",
        "",
        "```json",
        json.dumps(data, ensure_ascii=False, indent=2),
        "```",
        "",
    ])


def type_from_path(path):
    root = str(path or "").split("/", 1)[0]
    return TYPE_BY_ROOT.get(root, root or "wiki")


def kb_type_for_path(path):
    root = str(path or "").split("/", 1)[0]
    if root == "concepts":
        return "concept"
    if root == "resources":
        return "resource"
    if root == "projects":
        return "project"
    return "wiki"


def title_from_path(path):
    return str(path or "page.md").rsplit("/", 1)[-1].replace(".md", "")


def normalize_skipped(items):
    result = []
    for item in items or []:
        if isinstance(item, str):
            result.append({"reason": item})
        elif isinstance(item, dict):
            result.append(item)
    return result


def normalize_errors(items):
    result = []
    for item in items or []:
        if isinstance(item, str):
            result.append({"message": item})
        elif isinstance(item, dict):
            result.append(item)
    return result


def safe_slug(value):
    text = str(value or "source").strip().lower()
    import re
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:80] or "source"
