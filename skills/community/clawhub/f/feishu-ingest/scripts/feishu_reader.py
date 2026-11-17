import json
import mimetypes
import os
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from catalog import catalog_from_raw
from feishu_platform import download_message_resource, extract_refs, fetch_messages, message_create_seconds, message_id, read_reference
from gitea_api import GiteaClient
from text_extractors import read_text_preview
from utils import query_tokens, sha256_file, sha256_text, slugify, strip_frontmatter, unique


MAX_CONTEXT_CHARS = 12000
MAX_CATALOG_PAGES = 1000
MAX_RELATED_CARDS = 36
MAX_CARD_CHARS = 3500
CONFIG_REF_KEYS = ["urls", "docUrls", "wikiUrls", "tokens", "documents", "links"]
PAGE_ROOTS = ["overview", "projects", "papers", "surveys", "code", "meetings", "experiments", "tech-notes", "notes", "concepts", "resources"]
ENTITY_TYPE_TO_ROOT = {
    "paper": "papers", "survey": "surveys", "project": "projects", "code": "code",
    "meeting": "meetings", "experiment": "experiments", "tech-note": "tech-notes",
    "note": "notes", "concept": "concepts", "resource": "resources",
}
ANALYSIS_TEMPLATES = {
    "paper": {"preferredRoot": "papers", "sections": ["摘要", "研究问题", "方法", "数据/实验", "主要结论", "局限", "可复用点", "相关概念与资源"], "instruction": "面向论文或技术报告。提取研究问题、方法、实验设置、结论和局限。"},
    "survey": {"preferredRoot": "surveys", "sections": ["范围", "分类框架", "对比表", "趋势", "空白/争议", "推荐阅读", "相关概念与资源"], "instruction": "面向综述、调研和对比资料。优先形成分类框架和比较表。"},
    "project": {"preferredRoot": "projects", "sections": ["背景", "目标", "范围", "里程碑", "关键决策", "风险", "下一步", "相关页面"], "instruction": "面向需求、计划、方案、路线图和项目资料。保留决策依据和后续动作。"},
    "code": {"preferredRoot": "code", "sections": ["仓库/模块", "架构", "入口", "关键 API", "运行/部署", "风险与 TODO", "相关概念"], "instruction": "面向代码、仓库说明和接口资料。说明入口、依赖、运行方式和可复用模块。"},
    "meeting": {"preferredRoot": "meetings", "sections": ["背景", "讨论要点", "决策", "行动项", "开放问题", "相关页面"], "instruction": "面向会议纪要和讨论记录。不要逐字转写，优先沉淀结论、责任人和行动项。"},
    "experiment": {"preferredRoot": "experiments", "sections": ["假设", "设置", "指标", "结果", "分析", "复现信息", "后续实验"], "instruction": "面向实验、评测和 benchmark。保留配置、指标、结果和可复现信息。"},
    "tech-note": {"preferredRoot": "tech-notes", "sections": ["问题", "环境", "步骤", "配置", "排错", "参考", "相关页面"], "instruction": "面向操作手册、部署文档和排障资料。把步骤写成可执行的技术笔记。"},
    "note": {"preferredRoot": "notes", "sections": ["背景", "要点", "结论/价值", "后续动作", "消息定位"], "instruction": "面向群消息片段。先判断是否有长期研究价值，只沉淀决策、需求、解释、实验结果、项目上下文或带上下文的重要链接。"},
    "concept": {"preferredRoot": "concepts", "sections": ["定义", "使用场景", "相关方法", "常见误区", "相关资源"], "instruction": "面向概念页。给出稳定定义、边界、例子和与资料页的反向链接。"},
    "resource": {"preferredRoot": "resources", "sections": ["资源是什么", "内容摘要", "使用方法", "适用场景", "限制", "相关页面"], "instruction": "面向工具、链接、附件、图片、数据集或暂不能深度解析的资料。说明是什么、怎么用、限制在哪里。"},
}


def prepare_context(payload):
    source = payload.get("source") or {}
    if source.get("type") != "feishu":
        raise ValueError("feishu_ingest requires source.type=feishu")
    config = source.get("config") or {}
    chat_id = first_text(config.get("chatId"), config.get("openChatId"), config.get("open_chat_id"))
    include_files = bool_value(config.get("includeFiles"), True)
    include_messages = bool_value(config.get("includeMessages"), True)
    include_documents = bool_value(config.get("includeDocuments"), True)
    work_root = work_root_for(payload)
    reset_work_root(work_root)
    (work_root / "files").mkdir(parents=True, exist_ok=True)
    (work_root / "messages").mkdir(parents=True, exist_ok=True)
    (work_root / "documents").mkdir(parents=True, exist_ok=True)

    previous_snapshot = source.get("lastSnapshot") or source.get("last_snapshot") or {}
    previous_ts = int_value(previous_snapshot.get("lastMessageCreateTime"), 0) if isinstance(previous_snapshot, dict) else 0
    end_ts = int(time.time())
    start_ts = previous_ts + 1 if previous_ts else end_ts - int_value(config.get("initialLookbackHours"), 168) * 3600
    max_messages = int_value(config.get("maxMessages"), 200)
    trigger = payload.get("trigger") or "scheduled_scan"

    skipped = []
    status_records = []
    messages = collect_payload_messages(source, previous_ts, trigger)
    fetched_count = 0
    if chat_id and str(config.get("fetchRecentMessages", "true")).lower() != "false" and trigger != "feishu_event":
        try:
            fetched = fetch_messages(payload, chat_id, start_ts, end_ts, max_messages=max_messages)
            fetched_count = len(fetched)
            messages.extend(fetched)
        except Exception as exc:
            skip = skip_record("need_authorization", "feishu_message_history", "读取飞书群历史消息失败", exc, {"itemKey": f"feishu-message-history:{chat_id}", "externalId": chat_id})
            skipped.append(skip)
            status_records.append(source_item_from_skip(source, skip))
    elif not chat_id:
        skip = {"reason": "missing_chat_id", "kind": "feishu_message_history", "sourceKind": "feishu_message_history", "title": "未配置飞书群 ID", "message": "飞书资料源未配置 chatId/openChatId", "itemKey": "feishu-message-history:missing-chat-id"}
        skipped.append(skip)
        status_records.append(source_item_from_skip(source, skip))

    messages = dedupe_messages(messages)
    messages.sort(key=lambda item: (message_create_seconds(item), message_id(item)))
    latest_message_ts = max([message_create_seconds(item) for item in messages] + [previous_ts, 0])

    input_items = []
    message_records = []
    refs = collect_config_refs(config)
    for message in messages:
        normalized = normalize_message(message, source, chat_id)
        if not normalized.get("messageId"):
            skip = {"reason": "message_missing_id", "kind": "feishu_message", "sourceKind": "feishu_message", "title": "缺少 message_id 的飞书消息", "message": compact(message, 800)}
            skipped.append(skip)
            status_records.append(source_item_from_skip(source, skip))
            continue
        message_records.append(normalized)
        refs.extend(normalized.get("refs") or [])
        for asset in normalized.get("assets") or []:
            if not include_files:
                file_key = asset.get("fileKey") or asset.get("fileName") or "unknown"
                skip = skip_record("skipped", "feishu_file", asset.get("fileName") or file_key, RuntimeError("includeFiles=false"), {"itemKey": f"feishu-file:{normalized.get('messageId')}:{file_key}", "messageId": normalized.get("messageId"), "fileKey": asset.get("fileKey") or "", "messageTime": normalized.get("createTimeIso") or ""})
                skipped.append(skip)
                status_records.append(source_item_from_skip(source, skip))
                continue
            item, skip = materialize_asset(payload, source, work_root, normalized, asset, config)
            if skip:
                skipped.append(skip)
                status_records.append(source_item_from_skip(source, skip))
            if item:
                input_items.append(item)

    if include_messages:
        input_items.extend(materialize_message_segments(source, work_root, message_records, config))
    elif message_records:
        skipped.append({"reason": "messages_disabled_by_config", "kind": "feishu_message_segment", "message": "群消息编译已在资料源配置中关闭", "messageCount": len(message_records)})

    if include_documents:
        input_items.extend(materialize_document_refs(payload, source, work_root, refs, skipped, status_records))
    elif refs:
        for ref in refs:
            key = ref_key(ref) or sha256_text(json.dumps(ref, ensure_ascii=False))[:12]
            skip = {"reason": "skipped", "kind": "feishu_document", "sourceKind": "feishu_document", "title": key, "message": "includeDocuments=false", "itemKey": "feishu-doc:" + sha256_text(key)[:20], "externalId": key, "url": ref.get("url") or ""}
            skipped.append(skip)
            status_records.append(source_item_from_skip(source, skip))
    input_items = [annotate_input_item(item) for item in dedupe_input_items(input_items)]
    status_records = dedupe_source_item_records(status_records)

    client = GiteaClient(payload)
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    index_preview = clip(strip_frontmatter(client.read_text("index.md")), 18000)
    tokens = query_tokens("\n".join((item.get("title") or "") + "\n" + (item.get("textPreview") or "")[:2000] for item in input_items))
    related_cards = related_page_cards(client, catalog.get("pages") or [], tokens)
    snapshot = {
        "sourceId": source.get("id") or payload.get("sourceId"),
        "chatId": chat_id,
        "lastMessageCreateTime": latest_message_ts,
        "lastMessageCreateTimeIso": iso_time(latest_message_ts) if latest_message_ts else "",
        "fetchedMessageCount": fetched_count,
        "candidateItemCount": len(input_items),
        "skippedItemCount": len(status_records),
    }

    context = {
        "schema": "research-kb/feishu-ingest-context@1",
        "mode": "feishu_ingest_prepare",
        "taskId": payload.get("taskId"),
        "trigger": trigger,
        "team": payload.get("team") or {},
        "platform": safe_platform(payload.get("platform") or {}),
        "source": {"id": source.get("id") or payload.get("sourceId"), "name": source.get("name") or "", "type": source.get("type") or "", "config": safe_source_config(config)},
        "scanWindow": {
            "chatId": chat_id, "startTime": start_ts, "startTimeIso": iso_time(start_ts),
            "endTime": end_ts, "endTimeIso": iso_time(end_ts),
            "previousLastMessageCreateTime": previous_ts,
            "latestMessageCreateTime": latest_message_ts,
            "latestMessageCreateTimeIso": iso_time(latest_message_ts) if latest_message_ts else "",
            "fetchedMessageCount": fetched_count,
            "mergedMessageCount": len(messages),
        },
        "inputItems": input_items,
        "sourceItems": status_records,
        "skippedSources": skipped,
        "kb": {
            "catalogPageCount": len(catalog.get("pages") or []),
            "catalogPages": compact_catalog_pages((catalog.get("pages") or [])[:MAX_CATALOG_PAGES]),
            "indexPreview": index_preview,
            "relatedPageCards": related_cards,
        },
        "instructions": {
            "mustProcessOnlyInputItems": True,
            "requiredItemRule": "Every input item with required=true must appear in at least one generated or updated page via sourceItemKeys.",
            "messageValueRule": "Feishu message segments are optional. Create notes/ pages only for durable research value: decisions, requirements, reusable explanations, project context, meeting-like conclusions, experiment results, useful links with context, or insights worth future retrieval.",
            "messageNoiseRule": "Do not create a page for casual acknowledgements, scheduling chatter, duplicate notifications, low-context links, or transient coordination.",
            "sourceItemKeyRule": "Every generated/updated page must include sourceItemKeys listing supporting input itemKey values.",
            "archiveRule": "Do not write source_files directly in pages.json. The apply script archives downloaded Feishu files and compiled message/document source markdown under source_files/feishu/<sourceId>/... and injects archivedPath into page sources.",
            "allowedPageRoots": PAGE_ROOTS,
            "entityTypeRouting": ENTITY_TYPE_TO_ROOT,
            "analysisTemplates": ANALYSIS_TEMPLATES,
            "inputItemTemplateRule": "Use each input item's analysisTemplate/templateSections as the default page structure unless the evidence clearly calls for a concept/resource companion page.",
            "knowledgeGraphRule": "Before writing pages.json, make a private graph plan: preserve only valuable Feishu messages as entity pages, then decide whether existing overview/project/concept/resource/other pages should be updated. Concepts are stable reusable abstractions; resources are concrete reusable objects; overview pages are navigation or synthesis pages for themes, projects, source packages, or research areas. Do not force a page when evidence is weak, but do not skip an update when it would materially improve navigation or reuse.",
            "linkingRule": "When evidence supports it, add markdown links between entity pages and include relatedConcepts/relatedResources/relatedCodePages/relatedPages path arrays so catalog graph edges can be updated. relatedPages is for ordinary wiki pages such as overview/, projects/, papers/, surveys/, meetings/, experiments/, tech-notes/, and notes/.",
            "outputContract": {"pagesJson": {"pages": [{"path": "notes/example.md", "title": "Example", "type": "note", "kbType": "wiki", "sourceItemKeys": ["input-item-key"], "content": "Markdown body without frontmatter", "keywords": [], "projectIds": [], "relatedConcepts": ["concepts/example.md"], "relatedResources": ["resources/example.md"], "relatedPages": ["overview/example.md"]}], "skippedSources": [], "errors": [], "snapshot": {}}},
        },
        "snapshot": snapshot,
    }
    if not input_items:
        context["mode"] = "skip"
        context["skipResult"] = {
            "success": True,
            "processedSources": [source.get("id") or payload.get("sourceId") or chat_id or "feishu"],
            "createdPages": [],
            "updatedPages": [],
            "archivedFiles": [],
            "skippedSources": skipped or [{"reason": "no_new_feishu_items"}],
            "errors": [],
            "commitId": "",
            "snapshot": snapshot,
            "sourceItems": status_records,
        }
    return context


def collect_payload_messages(source, previous_ts, trigger):
    result = []
    for item in source.get("items") or []:
        if not isinstance(item, dict):
            continue
        metadata = item_metadata(item)
        message = item.get("message") or metadata.get("message") or item
        if not isinstance(message, dict):
            continue
        seconds = message_create_seconds(message)
        if trigger != "feishu_event" and previous_ts and seconds and seconds <= previous_ts:
            continue
        result.append(message)
    return result


def item_metadata(item):
    metadata = item.get("metadata") or {}
    if isinstance(metadata, dict):
        return metadata
    raw = item.get("metadata_json") or item.get("metadataJson") or ""
    if raw:
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}


def dedupe_messages(messages):
    by_id = {}
    anonymous = []
    for message in messages or []:
        if not isinstance(message, dict):
            continue
        mid = message_id(message)
        if mid:
            by_id[mid] = message
        else:
            anonymous.append(message)
    return list(by_id.values()) + anonymous


def normalize_message(message, source, chat_id):
    content = parse_message_content(message)
    text = extract_plain_text(content)
    refs = extract_refs(json.dumps(content, ensure_ascii=False)) + extract_refs(text)
    msg_type = first_text(message.get("msg_type"), message.get("message_type"), message.get("type"))
    seconds = message_create_seconds(message)
    return {
        "messageId": message_id(message),
        "chatId": first_text(message.get("chat_id"), chat_id),
        "msgType": msg_type,
        "createTime": seconds,
        "createTimeIso": iso_time(seconds) if seconds else "",
        "sender": sender_label(message.get("sender") or {}),
        "text": text,
        "refs": refs,
        "assets": extract_assets(content, msg_type),
        "rawContent": content,
        "sourceId": source.get("id"),
    }


def parse_message_content(message):
    body = message.get("body") or {}
    raw = body.get("content") if isinstance(body, dict) else ""
    raw = raw or message.get("content") or ""
    if isinstance(raw, (dict, list)):
        return raw
    try:
        return json.loads(str(raw)) if str(raw).strip() else {}
    except Exception:
        return {"text": str(raw)}


def extract_plain_text(node):
    chunks = []
    def walk(value, key=""):
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(child, child_key)
        elif isinstance(value, list):
            for child in value:
                walk(child, key)
        elif isinstance(value, str):
            text = value.strip()
            if text and (key in {"text", "title", "file_name", "fileName", "name", "href", "url", "link"} or len(text) > 8):
                chunks.append(text)
    walk(node)
    return "\n".join(unique(chunks)).strip()


def extract_assets(node, msg_type=""):
    assets = []
    seen = set()
    def add(file_key, resource_type, file_name="", unsupported_reason=""):
        key = f"{resource_type}:{file_key or file_name}"
        if (not file_key and not file_name) or key in seen:
            return
        seen.add(key)
        assets.append({"fileKey": str(file_key or ""), "resourceType": resource_type, "fileName": str(file_name or file_key or "file"), "unsupportedReason": unsupported_reason})
    def walk(value, inherited_type=""):
        if isinstance(value, dict):
            tag = str(value.get("tag") or value.get("type") or inherited_type or msg_type or "").lower()
            if tag == "folder" or msg_type == "folder":
                add(value.get("file_key"), "file", value.get("file_name") or value.get("name"), "folder_not_downloadable")
            elif value.get("file_key"):
                add(value.get("file_key"), "file", value.get("file_name") or value.get("fileName") or value.get("name") or value.get("title"))
            if value.get("image_key"):
                add(value.get("image_key"), "image", value.get("file_name") or value.get("name") or (str(value.get("image_key")) + ".jpg"))
            for child in value.values():
                walk(child, tag)
        elif isinstance(value, list):
            for child in value:
                walk(child, inherited_type)
    walk(node)
    return assets

def materialize_asset(payload, source, work_root, message, asset, config):
    file_key = asset.get("fileKey") or ""
    message_id_value = message.get("messageId") or ""
    file_name = safe_filename(asset.get("fileName") or file_key or "file")
    item_key = f"feishu-file:{message_id_value}:{file_key or sha256_text(file_name)[:12]}"
    common = {"itemKey": item_key, "messageId": message_id_value, "fileKey": file_key, "messageTime": message.get("createTimeIso") or "", "externalId": file_key or message_id_value, "sourceKind": "feishu_file"}
    if asset.get("unsupportedReason"):
        return None, skip_record("unsupported", "feishu_file", file_name, RuntimeError(asset.get("unsupportedReason")), common)
    local_path = work_root / "files" / slugify(message_id_value, 64) / file_name
    try:
        download_message_resource(payload, message_id_value, file_key, asset.get("resourceType") or "file", local_path)
    except Exception as exc:
        return None, skip_record(classify_download_error(exc), "feishu_file", file_name, exc, common)
    stat = local_path.stat()
    max_mb = int_value(config.get("maxFileSizeMb"), 100)
    if stat.st_size > max_mb * 1024 * 1024:
        try:
            local_path.unlink()
        except Exception:
            pass
        return None, skip_record("unsupported", "feishu_file", file_name, RuntimeError(f"file size {stat.st_size} exceeds maxFileSizeMb={max_mb}"), {**common, "size": stat.st_size})
    sha = sha256_file(local_path)
    preview = read_text_preview(local_path, MAX_CONTEXT_CHARS)
    return {
        "sourceId": source.get("id"), "itemKey": item_key, "sourceKind": "feishu_file", "required": True,
        "title": file_name, "fileName": file_name, "relativePath": f"{message.get('createTimeIso', '')[:10]}/{file_name}".strip("/"),
        "storagePath": str(local_path), "sha256": sha, "size": stat.st_size,
        "mimeType": mimetypes.guess_type(file_name)[0] or "", "extension": local_path.suffix.lower(),
        "readable": bool(preview.strip()), "extractionMethod": "feishu-message-resource" if preview else "binary-or-unreadable",
        "textPreview": clip(preview, MAX_CONTEXT_CHARS), "parseWarnings": [] if preview else ["no_text_extracted"],
        "messageId": message_id_value, "chatId": message.get("chatId") or "", "sentAt": message.get("createTimeIso") or "",
        "sender": message.get("sender") or "", "fileKey": file_key, "externalId": file_key or message_id_value,
        "weakTypeHints": weak_type_hints(file_name + "\n" + preview, local_path.suffix.lower()), "status": "candidate",
    }, None


def materialize_message_segments(source, work_root, records, config):
    window_seconds = int_value(config.get("messageSegmentWindowMinutes"), 10) * 60
    max_messages_per_segment = int_value(config.get("maxMessagesPerSegment"), 12)
    text_records = [record for record in records if (record.get("text") or "").strip()]
    segments = []
    current = []
    last_ts = 0
    for record in text_records:
        seconds = int(record.get("createTime") or 0)
        if current and ((seconds and last_ts and seconds - last_ts > window_seconds) or len(current) >= max_messages_per_segment):
            segments.append(current)
            current = []
        current.append(record)
        if seconds:
            last_ts = seconds
    if current:
        segments.append(current)
    items = []
    for segment in segments:
        first = segment[0]
        last = segment[-1]
        ids = [record.get("messageId") for record in segment if record.get("messageId")]
        if not ids:
            continue
        title = f"飞书群消息片段 {first.get('createTimeIso', '')[:16]}"
        item_key = "feishu-message-segment:" + sha256_text("\n".join(ids))[:16]
        content = render_message_segment_source(source, title, segment)
        local_path = work_root / "messages" / (slugify(first.get("createTimeIso") or ids[0], 40) + "-" + sha256_text(item_key)[:8] + ".md")
        local_path.write_text(content, encoding="utf-8")
        sha = sha256_file(local_path)
        items.append({
            "sourceId": source.get("id"), "itemKey": item_key, "sourceKind": "feishu_message_segment", "required": False,
            "preferredRoot": "notes", "title": title, "fileName": local_path.name, "relativePath": f"messages/{local_path.name}",
            "storagePath": str(local_path), "sha256": sha, "size": local_path.stat().st_size, "mimeType": "text/markdown", "extension": ".md",
            "readable": True, "extractionMethod": "compiled-feishu-message-segment", "textPreview": clip(strip_machine_block(content), MAX_CONTEXT_CHARS),
            "messageIds": ids, "externalId": ids[0], "firstMessageAt": first.get("createTimeIso") or "", "lastMessageAt": last.get("createTimeIso") or "",
            "chatId": first.get("chatId") or "", "senderSummary": unique([record.get("sender") for record in segment])[:8],
            "weakTypeHints": ["note"], "analysisTemplate": "note", "status": "candidate",
        })
    return items


def render_message_segment_source(source, title, segment):
    lines = [
        f"# {title}", "", "## 定位信息", "",
        f"- 资料源 ID：`{source.get('id') or ''}`", f"- 资料源名称：{source.get('name') or ''}",
        f"- chat_id：`{segment[0].get('chatId') or ''}`",
        f"- 起止时间：{segment[0].get('createTimeIso') or ''} - {segment[-1].get('createTimeIso') or ''}",
        f"- message_id：{', '.join(record.get('messageId') or '' for record in segment)}", "", "## 消息原文", "",
    ]
    for record in segment:
        lines.extend([f"### {record.get('createTimeIso') or ''} · {record.get('sender') or 'unknown'} · {record.get('msgType') or ''}", "", record.get("text") or "（无文本）", ""])
        if record.get("refs"):
            lines.append("链接/引用：")
            for ref in record.get("refs") or []:
                label = ref.get("url") or ref.get("token") or json.dumps(ref, ensure_ascii=False)
                lines.append(f"- {label}")
            lines.append("")
    lines.extend(["## 机器可读定位", "", "```json", json.dumps({"messages": segment}, ensure_ascii=False, indent=2), "```", ""])
    return "\n".join(lines)


def materialize_document_refs(payload, source, work_root, refs, skipped, status_records):
    items = []
    seen = set()
    for ref in refs:
        key = ref_key(ref)
        if not key or key in seen:
            continue
        seen.add(key)
        item_key = "feishu-doc:" + sha256_text(key)[:20]
        try:
            doc = read_reference(payload, ref)
            if not doc or not (doc.get("content") or "").strip():
                skip = {"reason": "empty_feishu_document", "kind": "feishu_document", "sourceKind": "feishu_document", "title": key, "message": "文档为空或未读取到正文", "itemKey": item_key, "externalId": key, "url": ref.get("url") or ""}
                skipped.append(skip)
                status_records.append(source_item_from_skip(source, skip))
                continue
        except Exception as exc:
            skip = skip_record(classify_download_error(exc), "feishu_document", key, exc, {"ref": ref, "itemKey": item_key, "externalId": key, "url": ref.get("url") or ""})
            skipped.append(skip)
            status_records.append(source_item_from_skip(source, skip))
            continue
        title = doc.get("title") or key
        content = render_document_source(source, doc, ref)
        local_path = work_root / "documents" / (slugify(title, 60) + "-" + sha256_text(key)[:8] + ".md")
        local_path.write_text(content, encoding="utf-8")
        sha = sha256_file(local_path)
        items.append({
            "sourceId": source.get("id"), "itemKey": item_key, "sourceKind": "feishu_document", "required": True,
            "title": title, "fileName": local_path.name, "relativePath": f"documents/{local_path.name}", "storagePath": str(local_path),
            "sha256": sha, "size": local_path.stat().st_size, "mimeType": "text/markdown", "extension": ".md", "readable": True,
            "extractionMethod": "feishu-cloud-document", "textPreview": clip(doc.get("content") or "", MAX_CONTEXT_CHARS),
            "url": doc.get("url") or ref.get("url") or "", "externalId": doc.get("externalId") or doc.get("token") or ref.get("token") or key,
            "documentType": doc.get("type") or ref.get("type") or "docx", "weakTypeHints": weak_type_hints(title + "\n" + (doc.get("content") or "")[:4000], ".md"),
            "status": "candidate",
        })
    return items


def render_document_source(source, doc, ref):
    data = {"sourceType": "feishu", "sourceId": source.get("id") or "", "sourceName": source.get("name") or "", "documentType": doc.get("type") or ref.get("type") or "", "externalId": doc.get("externalId") or doc.get("token") or ref.get("token") or "", "url": doc.get("url") or ref.get("url") or ""}
    return "\n".join([f"# 飞书文档来源：{doc.get('title') or data.get('externalId') or '未命名文档'}", "", "## 来源定位", "", "```json", json.dumps(data, ensure_ascii=False, indent=2), "```", "", "## 文档正文", "", doc.get("content") or "", ""])

def annotate_input_item(item):
    enriched = dict(item)
    template = enriched.get("analysisTemplate") or infer_analysis_template(enriched)
    enriched["analysisTemplate"] = template
    enriched["templateSections"] = ANALYSIS_TEMPLATES[template]["sections"]
    enriched["templateInstruction"] = ANALYSIS_TEMPLATES[template]["instruction"]
    enriched.setdefault("preferredRoot", ANALYSIS_TEMPLATES[template]["preferredRoot"])
    enriched.setdefault("status", "candidate")
    return enriched


def infer_analysis_template(item):
    kind = item.get("sourceKind") or ""
    if kind == "feishu_message_segment":
        return "note"
    if kind == "feishu_file" and not item.get("readable", True):
        return "resource"
    hints = [str(value).strip().lower() for value in item.get("weakTypeHints") or []]
    for hint in hints:
        if hint in ANALYSIS_TEMPLATES and hint != "note":
            return hint
    for hint in hints:
        if hint in ANALYSIS_TEMPLATES:
            return hint
    return "resource" if kind in {"feishu_file", "feishu_document"} else "note"


def collect_config_refs(config):
    refs = []
    for key in CONFIG_REF_KEYS:
        for value in as_list(config.get(key)):
            if isinstance(value, dict):
                refs.append(value)
            else:
                text = str(value or "").strip()
                found = extract_refs(text)
                refs.extend(found)
                if text and not found:
                    refs.append({"token": text})
    return refs


def ref_key(ref):
    if not isinstance(ref, dict):
        return str(ref or "")
    return first_text(ref.get("url"), ref.get("token"), ref.get("docToken"), ref.get("wikiToken"), ref.get("spreadsheetToken"), ref.get("appToken"))


def dedupe_input_items(items):
    by_key = {}
    for item in items or []:
        key = item.get("itemKey") or item.get("sha256")
        if key:
            by_key[str(key)] = item
    return list(by_key.values())


def dedupe_source_item_records(items):
    by_key = {}
    for item in items or []:
        key = item.get("itemKey") or item.get("item_key")
        if key:
            by_key[str(key)] = item
    return list(by_key.values())


def weak_type_hints(text, ext):
    value = (text or "").lower()
    ext = (ext or "").lower()
    hints = []
    if ext in {".py", ".java", ".js", ".jsx", ".ts", ".tsx", ".vue", ".html", ".css", ".sql", ".ipynb", ".go", ".rs"}:
        hints.append("code")
    if ext in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".zip", ".rar", ".7z"}:
        hints.append("resource")
    if any(word in value for word in ["abstract", "method", "experiment", "references", "doi", "arxiv"]):
        hints.append("paper")
    if any(word in value for word in ["综述", "调研", "survey", "review", "landscape", "趋势", "比较"]):
        hints.append("survey")
    if any(word in value for word in ["会议", "meeting", "纪要", "议程", "行动项", "决议"]):
        hints.append("meeting")
    if any(word in value for word in ["实验", "experiment", "ablation", "baseline", "metric", "结果"]):
        hints.append("experiment")
    if any(word in value for word in ["api", "配置", "安装", "部署", "命令", "troubleshoot", "排障"]):
        hints.append("tech-note")
    if any(word in value for word in ["项目", "需求", "roadmap", "milestone", "验收", "范围"]):
        hints.append("project")
    if any(word in value for word in ["概念", "定义", "术语", "principle", "theory"]):
        hints.append("concept")
    if not hints:
        hints.append("note")
    return unique(hints)[:5]


def source_item_from_skip(source, skip):
    item_key = skip.get("itemKey") or skip.get("item_key") or "feishu-skip:" + sha256_text(json.dumps(skip, ensure_ascii=False, sort_keys=True))[:20]
    kind = skip.get("sourceKind") or skip.get("kind") or "feishu_item"
    metadata = dict(skip)
    return {
        "sourceId": source.get("id"),
        "itemKey": item_key,
        "sourceKind": kind,
        "kind": kind,
        "status": status_from_reason(skip.get("reason")),
        "title": skip.get("title") or skip.get("fileName") or item_key,
        "fileName": skip.get("fileName") or skip.get("title") or "",
        "relativePath": skip.get("relativePath") or skip.get("originalPath") or "",
        "archivedPath": "",
        "url": skip.get("url") or "",
        "externalId": skip.get("externalId") or skip.get("messageId") or skip.get("fileKey") or "",
        "messageTime": skip.get("messageTime") or skip.get("sentAt") or "",
        "sha256": skip.get("sha256") or "",
        "size": int_value(skip.get("size"), 0),
        "lastError": skip.get("message") or skip.get("detail") or skip.get("reason") or "",
        "metadata": metadata,
    }


def status_from_reason(reason):
    value = str(reason or "").lower()
    if value == "need_authorization":
        return "need_authorization"
    if value in {"unsupported", "empty_feishu_document"}:
        return "unsupported"
    if value == "fetch_failed":
        return "fetch_failed"
    return "skipped"


def related_page_cards(client, pages, tokens):
    if not tokens:
        return []
    ranked = []
    for page in pages or []:
        haystack = " ".join(str(page.get(key) or "") for key in ["path", "title", "type"]) + " " + " ".join(page.get("keywords") or [])
        score = sum(1 for token in tokens if str(token).lower() in haystack.lower())
        if score:
            ranked.append((score, page))
    cards = []
    for _, page in sorted(ranked, key=lambda pair: pair[0], reverse=True)[:MAX_RELATED_CARDS]:
        path = page.get("path") or ""
        if not path or path.startswith("source_files/"):
            continue
        raw = client.read_text(path)
        cards.append({"path": path, "title": page.get("title") or path, "type": page.get("type") or path.split("/", 1)[0], "keywords": page.get("keywords") or [], "relatedConcepts": page.get("relatedConcepts") or [], "relatedResources": page.get("relatedResources") or [], "relatedCodePages": page.get("relatedCodePages") or [], "relatedPages": page.get("relatedPages") or [], "contentPreview": clip(strip_frontmatter(raw), MAX_CARD_CHARS)})
    return cards


def compact_catalog_pages(pages):
    result = []
    for page in pages or []:
        path = page.get("path") or ""
        if not path or path.startswith("source_files/"):
            continue
        result.append({"path": path, "title": page.get("title") or path, "type": page.get("type") or path.split("/", 1)[0], "kbType": page.get("kbType") or page.get("kb_type") or "wiki", "keywords": page.get("keywords") or [], "sourceIds": page.get("sourceIds") or [], "projectIds": page.get("projectIds") or [], "relatedConcepts": page.get("relatedConcepts") or [], "relatedResources": page.get("relatedResources") or [], "relatedCodePages": page.get("relatedCodePages") or [], "relatedPages": page.get("relatedPages") or [], "sourceStatus": page.get("sourceStatus") or "active"})
    return result


def work_root_for(payload):
    shared = payload.get("sharedDir") or os.getenv("OPENCLAW_SHARED_DIR") or str(Path.home() / ".research-kb")
    task_id = slugify(payload.get("taskId") or sha256_text(str(payload))[:16])
    return Path(shared).expanduser().resolve() / "feishu_ingest" / task_id


def reset_work_root(path):
    resolved = Path(path).resolve()
    if not resolved.name or resolved.anchor == str(resolved):
        raise ValueError(f"Refusing to clean unsafe path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True, exist_ok=True)


def safe_platform(platform):
    return {"giteaUrl": platform.get("giteaUrl") or "", "giteaOwner": platform.get("giteaOwner") or "", "sharedDir": platform.get("sharedDir") or ""}


def safe_source_config(config):
    result = dict(config or {})
    result.pop("appSecret", None)
    result.pop("app_secret", None)
    result.pop("feishuAppSecret", None)
    return result


def classify_download_error(exc):
    text = str(exc)
    if "234037" in text or "100MB" in text or "too large" in text.lower() or "folder_not_downloadable" in text:
        return "unsupported"
    if any(code in text for code in ["230027", "234004", "234038", "234040", "999916", "permission", "forbidden", "权限"]):
        return "need_authorization"
    return "fetch_failed"


def skip_record(reason, kind, title, exc, extra=None):
    data = {"reason": reason, "kind": kind, "sourceKind": kind, "title": title, "message": str(exc)[:1000]}
    if extra:
        data.update(extra)
    return data


def sender_label(sender):
    if not isinstance(sender, dict):
        return str(sender or "")
    sender_id = sender.get("sender_id") or {}
    if isinstance(sender_id, dict):
        return first_text(sender_id.get("open_id"), sender_id.get("user_id"), sender_id.get("union_id"), sender.get("sender_type"))
    return first_text(sender_id, sender.get("sender_type"))


def as_list(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
        return [part.strip() for part in re.split(r"[\n,;]+", text) if part.strip()]
    return [value]


def safe_filename(name):
    value = str(name or "file").replace("\\", "/").rsplit("/", 1)[-1].strip()
    value = re.sub(r"[\x00-\x1f]+", "", value)
    return value[:180] or "file"


def strip_machine_block(text):
    return re.sub(r"## 机器可读定位[\s\S]*$", "", text or "").strip()


def clip(text, limit):
    value = str(text or "")
    return value if len(value) <= limit else value[:limit] + "\n...[truncated]"


def compact(value, max_chars=4000):
    try:
        text = json.dumps(value, ensure_ascii=False, indent=2)
    except Exception:
        text = str(value)
    return clip(text, max_chars)


def iso_time(seconds):
    if not seconds:
        return ""
    return datetime.fromtimestamp(int(seconds), tz=timezone.utc).replace(microsecond=0).isoformat()


def first_text(*values):
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def int_value(value, fallback):
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str) and value.strip():
        try:
            return int(float(value))
        except ValueError:
            return fallback
    return fallback


def bool_value(value, fallback):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "1", "yes", "y", "on"}:
            return True
        if text in {"false", "0", "no", "n", "off"}:
            return False
    return fallback
