from __future__ import annotations

import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from skill_runtime.feishu_auth import (
    AuthRequiredError,
    TokenRefreshError,
    clean_text,
    ensure_user_access_token,
    feishu_request,
    require_env,
    token_cache_path,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def mask_value(value: str) -> str:
    cleaned = clean_text(value)
    if len(cleaned) <= 8:
        return cleaned
    return f"{cleaned[:4]}...{cleaned[-4:]}"


def truncate_text(value: Any, limit: int) -> str:
    cleaned = clean_text(value)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(limit - 1, 0)].rstrip() + "…"


def resolve_raw_payload_path(input_path: Path) -> Path:
    if input_path.suffix.lower() == ".json":
        return input_path

    text = read_text(input_path)
    match = re.search(r"Raw JSON：(.+)", text)
    if not match:
        raise ValueError("未能从 wechat-report Markdown 中解析 Raw JSON 路径。")

    candidate = Path(match.group(1).strip())
    if candidate.is_absolute():
        return candidate
    return input_path.parent / candidate


def load_raw_payload(input_path: Path) -> tuple[Path, dict[str, Any]]:
    raw_path = resolve_raw_payload_path(input_path)
    payload = json.loads(read_text(raw_path))
    if not isinstance(payload, dict):
        raise ValueError("wechat-report raw payload must be a JSON object.")
    return raw_path, payload


def get_tenant_access_token() -> str:
    response = feishu_request(
        "POST",
        "/auth/v3/tenant_access_token/internal",
        payload={
            "app_id": require_env("FEISHU_APP_ID"),
            "app_secret": require_env("FEISHU_APP_SECRET"),
        },
    )
    token = clean_text(response.get("tenant_access_token") or (response.get("data") or {}).get("tenant_access_token"))
    if not token:
        raise RuntimeError("飞书 tenant_access_token 获取失败。")
    return token


def extract_source_url(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        for item in value:
            extracted = extract_source_url(item)
            if extracted:
                return extracted
        return ""
    if isinstance(value, dict):
        for key in ["link", "url", "text", "name"]:
            extracted = extract_source_url(value.get(key))
            if extracted:
                return extracted
        return ""
    return clean_text(value)


def list_record_slots(token: str, *, app_token: str, table_id: str) -> list[dict[str, Any]]:
    page_token = ""
    slots: list[dict[str, Any]] = []
    while True:
        query = {"page_size": 500}
        if page_token:
            query["page_token"] = page_token
        response = feishu_request(
            "GET",
            f"/bitable/v1/apps/{app_token}/tables/{table_id}/records",
            token=token,
            query=query,
        )
        data = response.get("data") or {}
        for item in data.get("items", []):
            fields = item.get("fields") or {}
            source_url = extract_source_url(fields.get("source_url"))
            record_id = clean_text(item.get("record_id"))
            nonempty = any(value not in ("", None, [], {}) for value in fields.values())
            if record_id:
                slots.append(
                    {
                        "record_id": record_id,
                        "source_url": source_url,
                        "is_empty": not nonempty,
                    }
                )
        if not data.get("has_more"):
            break
        page_token = clean_text(data.get("page_token"))
        if not page_token:
            break
    return slots


def build_source_url_index(slots: list[dict[str, Any]]) -> dict[str, str]:
    records: dict[str, str] = {}
    for slot in slots:
        source_url = clean_text(slot.get("source_url"))
        record_id = clean_text(slot.get("record_id"))
        if source_url and record_id:
            records[source_url] = record_id
    return records


def first_empty_record_id(slots: list[dict[str, Any]]) -> str | None:
    for slot in slots:
        if slot.get("is_empty"):
            return clean_text(slot.get("record_id"))
    return None


def list_table_field_types(token: str, *, app_token: str, table_id: str) -> dict[str, int]:
    page_token = ""
    field_types: dict[str, int] = {}
    while True:
        query = {"page_size": 500}
        if page_token:
            query["page_token"] = page_token
        response = feishu_request(
            "GET",
            f"/bitable/v1/apps/{app_token}/tables/{table_id}/fields",
            token=token,
            query=query,
        )
        data = response.get("data") or {}
        for item in data.get("items", []):
            name = clean_text(item.get("field_name"))
            field_type = item.get("type")
            if name and isinstance(field_type, int):
                field_types[name] = field_type
        if not data.get("has_more"):
            break
        page_token = clean_text(data.get("page_token"))
        if not page_token:
            break
    return field_types


def maybe_number(value: Any) -> int | None:
    if value in {None, ""}:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def build_fields(article: dict[str, Any], *, topic: str, report_slug: str, sync_status: str, synced_at: str) -> dict[str, Any]:
    engagement = article.get("engagement") or {}
    fields: dict[str, Any] = {
        "topic": topic,
        "report_slug": report_slug,
        "source_url": article.get("source_url") or "",
        "公众号": article.get("account_name") or "",
        "作者": article.get("author") or "",
        "标题": article.get("title") or "",
        "发布时间": article.get("published_at") or "",
        "是否原创": "是" if article.get("is_original") else "否",
        "摘要": article.get("summary") or "",
        "comment_id": engagement.get("comment_id") or "",
        "互动采集状态": engagement.get("status") or "unavailable",
        "封面图": article.get("cover_image") or "",
        "采集时间": synced_at,
        "同步状态": sync_status,
    }
    optional_numbers = {
        "阅读数": maybe_number(engagement.get("read_count")),
        "点赞数": maybe_number(engagement.get("like_count")),
        "评论数": maybe_number(engagement.get("comment_count")),
        "打赏数": maybe_number(engagement.get("reward_total_count")),
        "正文纯文本长度": maybe_number(article.get("plain_text_length")),
        "段落数": maybe_number(article.get("paragraph_count")),
        "图片数": maybe_number(article.get("image_count")),
        "外链数": maybe_number(article.get("external_link_count")),
        "公众号内链数": maybe_number(article.get("mp_link_count")),
    }
    for key, value in optional_numbers.items():
        if value is not None:
            fields[key] = value
    return fields


def upsert_record(token: str, *, app_token: str, table_id: str, record_id: str | None, fields: dict[str, Any]) -> str:
    if record_id:
        response = feishu_request(
            "PUT",
            f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}",
            token=token,
            payload={"fields": fields},
        )
        return clean_text((response.get("data") or {}).get("record", {}).get("record_id") or record_id)

    response = feishu_request(
        "POST",
        f"/bitable/v1/apps/{app_token}/tables/{table_id}/records",
        token=token,
        payload={"fields": fields},
    )
    created_id = clean_text((response.get("data") or {}).get("record", {}).get("record_id"))
    if not created_id:
        raise RuntimeError("飞书新增记录后未返回 record_id。")
    return created_id


def empty_field_value(field_type: int | None) -> Any:
    if field_type == 1:
        return ""
    return None


def clear_record(
    token: str,
    *,
    app_token: str,
    table_id: str,
    record_id: str,
    field_types: dict[str, int],
    field_names: list[str],
) -> None:
    clear_fields = {name: empty_field_value(field_types.get(name)) for name in field_names}
    feishu_request(
        "PUT",
        f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}",
        token=token,
        payload={"fields": clear_fields},
    )


def csv_headers() -> list[str]:
    return [
        "topic",
        "report_slug",
        "source_url",
        "公众号",
        "作者",
        "标题",
        "发布时间",
        "是否原创",
        "摘要",
        "阅读数",
        "点赞数",
        "评论数",
        "打赏数",
        "comment_id",
        "互动采集状态",
        "正文纯文本长度",
        "段落数",
        "图片数",
        "外链数",
        "公众号内链数",
        "封面图",
        "采集时间",
        "同步状态",
    ]


def build_csv_row(article: dict[str, Any], *, topic: str, report_slug: str, exported_at: str) -> dict[str, Any]:
    fields = build_fields(article, topic=topic, report_slug=report_slug, sync_status="csv_exported", synced_at=exported_at)
    row = {header: fields.get(header, "") for header in csv_headers()}
    return row


def normalize_fields_for_table(fields: dict[str, Any], field_types: dict[str, int]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in fields.items():
        field_type = field_types.get(key)
        if field_type == 1:
            normalized[key] = clean_text(value)
            continue
        normalized[key] = value
    return normalized


def export_csv_fallback(
    *,
    workspace_root: Path,
    report_slug: str,
    topic: str,
    articles: list[dict[str, Any]],
) -> Path:
    csv_path = workspace_root / "content-production" / "published" / f"{datetime.now().strftime('%Y%m%d')}-{report_slug}-feishu-import.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    exported_at = datetime.now().isoformat(timespec="seconds")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_headers())
        writer.writeheader()
        for article in articles:
            source_url = clean_text(article.get("source_url"))
            if not source_url:
                continue
            writer.writerow(build_csv_row(article, topic=topic, report_slug=report_slug, exported_at=exported_at))
    return csv_path


def build_manifest(
    *,
    topic: str,
    report_slug: str,
    source_input: Path,
    raw_path: Path,
    published_path: Path,
    status: str,
    auth_mode: str,
    app_token_label: str,
    table_id_label: str,
    summary_rows: list[dict[str, str]] | None = None,
    auth_cache_path: str = "",
    csv_path: str = "",
    error_message: str = "",
) -> str:
    summary_rows = summary_rows or []
    created_count = sum(1 for item in summary_rows if item.get("action") == "created")
    updated_count = sum(1 for item in summary_rows if item.get("action") == "updated")
    lines = [
        f"# 飞书同步结果：{topic}",
        "",
        "## 基础信息",
        "",
        f"- `status`：{status}",
        f"- `auth_mode`：{auth_mode}",
        f"- `report_slug`：{report_slug}",
        f"- `source_input`：{source_input}",
        f"- `raw_path`：{raw_path}",
        f"- `published_path`：{published_path}",
        f"- `app_token`：{app_token_label}",
        f"- `table_id`：{table_id_label}",
        f"- `generated_at`：{datetime.now().isoformat(timespec='seconds')}",
        "",
    ]
    if auth_cache_path:
        lines.append(f"- `user_auth_cache`：{auth_cache_path}")
    if csv_path:
        lines.append(f"- `csv_fallback`：{csv_path}")
    if error_message:
        lines.extend(
            [
                "",
                "## 错误信息",
                "",
                f"- {error_message}",
            ]
        )

    if status == "auth_required":
        lines.extend(
            [
                "",
                "## 下一步",
                "",
                "- 先运行 `feishu-user-auth` 完成一次浏览器授权。",
                "- 授权成功后，再重新运行 `feishu-bitable-sync`。",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    if status == "csv_exported":
        lines.extend(
            [
                "",
                "## 下一步",
                "",
                "- 当前没有直接写入飞书，已额外导出 CSV 兜底文件。",
                "- 可在飞书多维表中使用“导入 Excel/CSV”继续入库。",
            ]
        )

    lines.extend(
        [
            "",
            "## 执行摘要",
            "",
            f"- 共同步 {len(summary_rows)} 篇文章。",
            f"- 新增 {created_count} 行，更新 {updated_count} 行。",
            "",
            "## 同步结果",
            "",
        ]
    )

    if summary_rows:
        lines.extend(
            [
                "| 标题 | 公众号 | source_url | 动作 | record_id |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in summary_rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        truncate_text(item.get("title"), 60).replace("|", "\\|"),
                        truncate_text(item.get("account_name"), 32).replace("|", "\\|"),
                        truncate_text(item.get("source_url"), 80).replace("|", "\\|"),
                        clean_text(item.get("action")),
                        clean_text(item.get("record_id")),
                    ]
                )
                + " |"
            )
    else:
        lines.append("- 本次没有可同步的文章。")
    return "\n".join(lines).rstrip() + "\n"


def update_payload_status(
    *,
    raw_path: Path,
    payload: dict[str, Any],
    status: str,
    auth_mode: str,
    manifest_path: Path,
    app_token: str,
    table_id: str,
    records: list[dict[str, str]] | None = None,
    csv_path: Path | None = None,
    error_message: str = "",
    synced_at: str = "",
) -> None:
    payload.setdefault("feishu_sync", {})
    payload["feishu_sync"].update(
        {
            "status": status,
            "auth_mode": auth_mode,
            "synced_at": synced_at,
            "manifest_path": str(manifest_path),
            "csv_path": str(csv_path) if csv_path else "",
            "error": error_message,
            "user_auth_cache_path": str(token_cache_path()) if auth_mode == "user" else "",
            "table": {
                "app_token": mask_value(app_token),
                "table_id": mask_value(table_id),
            },
            "records": records or [],
        }
    )
    write_text(raw_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def resolve_auth_mode() -> str:
    auth_mode = clean_text(os.environ.get("FEISHU_SYNC_AUTH_MODE") or "user").lower()
    if auth_mode not in {"user", "tenant"}:
        raise ValueError("`FEISHU_SYNC_AUTH_MODE` 只支持 `user` 或 `tenant`。")
    return auth_mode


def run_feishu_bitable_sync(input_path: Path, *, workspace_root: Path) -> dict[str, Any]:
    raw_path, payload = load_raw_payload(input_path)
    request = payload.get("request") or {}
    articles = payload.get("articles") or []
    topic = clean_text(request.get("topic") or raw_path.stem)
    report_slug = clean_text(request.get("slug") or raw_path.stem)

    app_token = require_env("FEISHU_BITABLE_APP_TOKEN")
    table_id = require_env("FEISHU_BITABLE_TABLE_ID")
    auth_mode = resolve_auth_mode()
    manifest_path = workspace_root / "content-production" / "published" / f"{datetime.now().strftime('%Y%m%d')}-{report_slug}-feishu-sync.md"
    app_token_label = mask_value(app_token)
    table_id_label = mask_value(table_id)

    try:
        schema_token = get_tenant_access_token()
        field_types = list_table_field_types(schema_token, app_token=app_token, table_id=table_id)
        if auth_mode == "tenant":
            access_token = get_tenant_access_token()
        else:
            access_token, _ = ensure_user_access_token()
    except AuthRequiredError as error:
        write_text(
            manifest_path,
            build_manifest(
                topic=topic,
                report_slug=report_slug,
                source_input=input_path,
                raw_path=raw_path,
                published_path=manifest_path,
                status="auth_required",
                auth_mode=auth_mode,
                app_token_label=app_token_label,
                table_id_label=table_id_label,
                auth_cache_path=str(token_cache_path()),
                error_message=clean_text(error),
            ),
        )
        update_payload_status(
            raw_path=raw_path,
            payload=payload,
            status="auth_required",
            auth_mode=auth_mode,
            manifest_path=manifest_path,
            app_token=app_token,
            table_id=table_id,
            error_message=clean_text(error),
        )
        return {
            "topic": topic,
            "slug": report_slug,
            "status": "auth_required",
            "raw_path": raw_path,
            "manifest_path": manifest_path,
            "created_count": 0,
            "updated_count": 0,
        }
    except TokenRefreshError as error:
        csv_path = export_csv_fallback(
            workspace_root=workspace_root,
            report_slug=report_slug,
            topic=topic,
            articles=articles,
        )
        write_text(
            manifest_path,
            build_manifest(
                topic=topic,
                report_slug=report_slug,
                source_input=input_path,
                raw_path=raw_path,
                published_path=manifest_path,
                status="csv_exported",
                auth_mode=auth_mode,
                app_token_label=app_token_label,
                table_id_label=table_id_label,
                auth_cache_path=str(token_cache_path()),
                csv_path=str(csv_path),
                error_message=clean_text(error),
            ),
        )
        update_payload_status(
            raw_path=raw_path,
            payload=payload,
            status="csv_exported",
            auth_mode=auth_mode,
            manifest_path=manifest_path,
            app_token=app_token,
            table_id=table_id,
            csv_path=csv_path,
            error_message=clean_text(error),
        )
        return {
            "topic": topic,
            "slug": report_slug,
            "status": "csv_exported",
            "raw_path": raw_path,
            "manifest_path": manifest_path,
            "csv_path": csv_path,
            "created_count": 0,
            "updated_count": 0,
        }

    try:
        slots = list_record_slots(access_token, app_token=app_token, table_id=table_id)
        existing_records = build_source_url_index(slots)
        synced_at = datetime.now().isoformat(timespec="seconds")

        summary_rows: list[dict[str, str]] = []
        for article in articles:
            source_url = clean_text(article.get("source_url"))
            if not source_url:
                continue
            existing_id = existing_records.get(source_url)
            target_record_id = existing_id
            record_to_delete = ""
            action = "updated" if existing_id else "created"

            if existing_id:
                empty_id = first_empty_record_id(slots)
                if empty_id and empty_id != existing_id:
                    existing_index = next((index for index, slot in enumerate(slots) if slot.get("record_id") == existing_id), -1)
                    empty_index = next((index for index, slot in enumerate(slots) if slot.get("record_id") == empty_id), -1)
                    if empty_index != -1 and existing_index != -1 and empty_index < existing_index:
                        target_record_id = empty_id
                        record_to_delete = existing_id
                        action = "updated"
            else:
                empty_id = first_empty_record_id(slots)
                if empty_id:
                    target_record_id = empty_id

            fields = build_fields(article, topic=topic, report_slug=report_slug, sync_status=action, synced_at=synced_at)
            fields = normalize_fields_for_table(fields, field_types)
            record_id = upsert_record(
                access_token,
                app_token=app_token,
                table_id=table_id,
                record_id=target_record_id,
                fields=fields,
            )
            if record_to_delete:
                clear_record(
                    access_token,
                    app_token=app_token,
                    table_id=table_id,
                    record_id=record_to_delete,
                    field_types=field_types,
                    field_names=list(fields.keys()),
                )
            existing_records[source_url] = record_id
            for slot in slots:
                if slot.get("record_id") == record_id:
                    slot["source_url"] = source_url
                    slot["is_empty"] = False
                if record_to_delete and slot.get("record_id") == record_to_delete:
                    slot["source_url"] = ""
                    slot["is_empty"] = True
            summary_rows.append(
                {
                    "title": clean_text(article.get("title")),
                    "account_name": clean_text(article.get("account_name")),
                    "source_url": source_url,
                    "action": action,
                    "record_id": record_id,
                }
            )

        write_text(
            manifest_path,
            build_manifest(
                topic=topic,
                report_slug=report_slug,
                source_input=input_path,
                raw_path=raw_path,
                published_path=manifest_path,
                status="synced",
                auth_mode=auth_mode,
                app_token_label=app_token_label,
                table_id_label=table_id_label,
                summary_rows=summary_rows,
                auth_cache_path=str(token_cache_path()) if auth_mode == "user" else "",
            ),
        )
        update_payload_status(
            raw_path=raw_path,
            payload=payload,
            status="synced",
            auth_mode=auth_mode,
            manifest_path=manifest_path,
            app_token=app_token,
            table_id=table_id,
            records=summary_rows,
            synced_at=synced_at,
        )
        return {
            "topic": topic,
            "slug": report_slug,
            "status": "synced",
            "raw_path": raw_path,
            "manifest_path": manifest_path,
            "created_count": sum(1 for item in summary_rows if item["action"] == "created"),
            "updated_count": sum(1 for item in summary_rows if item["action"] == "updated"),
        }
    except Exception as error:  # noqa: BLE001
        error_message = clean_text(error) or str(error)
        try:
            csv_path = export_csv_fallback(
                workspace_root=workspace_root,
                report_slug=report_slug,
                topic=topic,
                articles=articles,
            )
            status = "csv_exported"
        except Exception as csv_error:  # noqa: BLE001
            csv_path = None
            status = "sync_failed"
            error_message = f"{error_message}；CSV 导出也失败：{clean_text(csv_error) or csv_error}"

        write_text(
            manifest_path,
            build_manifest(
                topic=topic,
                report_slug=report_slug,
                source_input=input_path,
                raw_path=raw_path,
                published_path=manifest_path,
                status=status,
                auth_mode=auth_mode,
                app_token_label=app_token_label,
                table_id_label=table_id_label,
                auth_cache_path=str(token_cache_path()) if auth_mode == "user" else "",
                csv_path=str(csv_path) if csv_path else "",
                error_message=error_message,
            ),
        )
        update_payload_status(
            raw_path=raw_path,
            payload=payload,
            status=status,
            auth_mode=auth_mode,
            manifest_path=manifest_path,
            app_token=app_token,
            table_id=table_id,
            csv_path=csv_path,
            error_message=error_message,
        )
        return {
            "topic": topic,
            "slug": report_slug,
            "status": status,
            "raw_path": raw_path,
            "manifest_path": manifest_path,
            "csv_path": csv_path,
            "created_count": 0,
            "updated_count": 0,
        }
