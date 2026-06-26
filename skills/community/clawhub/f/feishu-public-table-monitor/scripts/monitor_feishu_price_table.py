#!/usr/bin/env python3
"""Monitor a public Feishu/Lark wiki/doc table for changes.

This helper intentionally avoids assuming the old Feishu HTML shape. Feishu has
changed public pages from embedding a full `clientVars: Object({...})` payload to
sometimes returning `Object()` and loading real block data later. When the old
HTML payload is unavailable, this script now fails with a clear actionable error
instead of a misleading JSONDecodeError.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

DEFAULT_SECTION_TITLE = "三、模型列表与倍率价格表（所有模型可用）"
DOCX_MODE_SPECIFIC = 4
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


def fetch_html(url: str, session: Any | None = None) -> str:
    try:
        import requests  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"缺少 requests 依赖: {e}") from e

    http = session or requests
    resp = http.get(
        url,
        timeout=30,
        headers={"User-Agent": USER_AGENT},
        allow_redirects=True,
    )
    resp.raise_for_status()
    resp.encoding = resp.encoding or "utf-8"
    return resp.text


def _skip_ws(source: str, index: int) -> int:
    while index < len(source) and source[index].isspace():
        index += 1
    return index


def _read_js_string(source: str, start: int) -> tuple[str, int]:
    start = _skip_ws(source, start)
    if start >= len(source) or source[start] not in {'"', "'"}:
        raise RuntimeError("飞书数据块不是字符串包装格式")

    if source[start] == '"':
        value, end = json.JSONDecoder().raw_decode(source[start:])
        return value, start + end

    i = start + 1
    out: list[str] = []
    escaped = False
    while i < len(source):
        ch = source[i]
        if escaped:
            try:
                out.append(json.loads('"\\' + ch + '"'))
            except Exception:
                out.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == "'":
            return "".join(out), i + 1
        else:
            out.append(ch)
        i += 1
    raise RuntimeError("飞书数据块字符串未闭合")


def _find_matching_paren(source: str, open_index: int) -> int:
    depth = 0
    in_string: str | None = None
    escaped = False
    for i in range(open_index, len(source)):
        ch = source[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            continue
        if ch in {'"', "'"}:
            in_string = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    raise RuntimeError("飞书 Object(...) 数据块括号未闭合")


def _extract_balanced_json_object(source: str, start: int) -> str:
    start = _skip_ws(source, start)
    if start >= len(source):
        raise RuntimeError("飞书数据块为空")
    if source[start] != "{":
        object_start = source.find("{", start)
        if object_start == -1:
            raise RuntimeError("飞书数据块中找不到 JSON 对象")
        prefix = source[start:object_start].strip()
        if prefix:
            raise RuntimeError(f"不支持的飞书数据包装格式：{prefix[:80]}")
    else:
        object_start = start

    brace = 0
    in_string: str | None = None
    escaped = False
    for i in range(object_start, len(source)):
        ch = source[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == in_string:
                in_string = None
            continue
        if ch in {'"', "'"}:
            in_string = ch
        elif ch == "{":
            brace += 1
        elif ch == "}":
            brace -= 1
            if brace == 0:
                return source[object_start : i + 1]
    raise RuntimeError("飞书 JSON 对象未闭合")


def _parse_object_arg(source: str, arg_start: int) -> dict[str, Any]:
    arg_start = _skip_ws(source, arg_start)
    if arg_start >= len(source) or source[arg_start] == ")":
        raise RuntimeError(
            "飞书未在 HTML 的 clientVars 中下发页面数据；该公开页已切换为新版异步读取，"
            "请改用浏览器自动化或飞书实际接口抓取加载后的表格。"
        )

    wrappers = (
        ("JSON.parse(", lambda s: s),
        ("decodeURIComponent(", unquote),
    )
    for prefix, transform in wrappers:
        if source.startswith(prefix, arg_start):
            encoded, string_end = _read_js_string(source, arg_start + len(prefix))
            close = _skip_ws(source, string_end)
            if close >= len(source) or source[close] != ")":
                raise RuntimeError(f"飞书 {prefix[:-1]} 包装未闭合")
            return json.loads(transform(encoded))

    if source[arg_start] in {'"', "'"}:
        encoded, _ = _read_js_string(source, arg_start)
        return json.loads(encoded)

    return json.loads(_extract_balanced_json_object(source, arg_start))


def extract_client_vars_json(html: str) -> dict[str, Any]:
    marker = "clientVars: Object("
    marker_index = html.find(marker)
    if marker_index == -1:
        raise RuntimeError("找不到飞书页面数据块 clientVars")

    object_call = html.rfind("Object(", 0, marker_index + len(marker))
    if object_call == -1:
        raise RuntimeError("找不到 Object( 起点")

    arg_start = object_call + len("Object(")
    close = _find_matching_paren(html, object_call + len("Object"))
    return _parse_object_arg(html[: close + 1], arg_start)


def client_vars_api_url(page_url: str) -> str:
    parsed = urlparse(page_url)
    if not parsed.scheme or not parsed.netloc:
        raise RuntimeError("飞书链接格式不正确，无法构造分页接口")
    return f"{parsed.scheme}://{parsed.netloc}/space/api/docx/pages/client_vars"


def fetch_client_vars_slice(session: Any, page_url: str, doc_id: str, params: dict[str, Any]) -> dict[str, Any]:
    query = {"id": doc_id, "limit": 239, **params}
    resp = session.get(
        client_vars_api_url(page_url),
        params=query,
        timeout=30,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Referer": page_url,
        },
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("code", 0) != 0:
        raise RuntimeError(f"飞书分页接口返回错误：{payload.get('msg') or payload.get('message') or payload.get('code')}")
    return payload.get("data") or {}


def merge_client_vars_data(base_data: dict[str, Any], patch_data: dict[str, Any]) -> None:
    for key in ("block_map", "meta_map", "user_map", "editor_map", "mention_page_title"):
        value = patch_data.get(key)
        if isinstance(value, dict):
            base_data.setdefault(key, {}).update(value)
    for key in ("block_sequence", "skip_blocks"):
        value = patch_data.get(key)
        if isinstance(value, list):
            existing = base_data.setdefault(key, [])
            seen = set(existing)
            existing.extend(item for item in value if item not in seen)


def complete_table_block_map(session: Any, page_url: str, client_vars: dict[str, Any], table_id: str) -> None:
    """Fetch missing public table slices Feishu omits from initial clientVars.

    Current Feishu public pages often preload only part of a large table. The
    front-end fills table blocks via `/space/api/docx/pages/client_vars` using
    `mode=SPECIFIC` and cursors. Replicating that flow keeps this skill usable
    for customers who only monitor a public Feishu link and do not have API auth.
    """
    data = client_vars.get("data") or {}
    doc_id = data.get("id")
    first_cursor = data.get("cursor")
    if not doc_id or not first_cursor:
        return

    queue: list[dict[str, Any]] = [
        {"mode": DOCX_MODE_SPECIFIC, "block_id": table_id, "cursor": first_cursor}
    ]
    seen: set[str] = set()
    for _ in range(20):
        if not queue:
            break
        params = queue.pop(0)
        key = json.dumps(params, ensure_ascii=False, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        patch_data = fetch_client_vars_slice(session, page_url, doc_id, params)
        merge_client_vars_data(data, patch_data)
        next_cursors = patch_data.get("next_cursors") or (
            [patch_data.get("cursor")] if patch_data.get("has_more") and patch_data.get("cursor") else []
        )
        for cursor in next_cursors:
            if cursor:
                queue.append({"mode": DOCX_MODE_SPECIFIC, "cursor": cursor})


def block_plain_text(block_map: dict[str, Any], block_id: str) -> str:
    block = block_map.get(block_id)
    if not block:
        return ""
    data = block.get("data", {})
    parts: list[str] = []
    text_obj = data.get("text", {})
    initial = text_obj.get("initialAttributedTexts", {})
    text_map = initial.get("text", {})
    if isinstance(text_map, dict):
        for _, value in sorted(text_map.items(), key=lambda kv: kv[0]):
            if isinstance(value, str):
                parts.append(value)
    for child_id in data.get("children", []) or []:
        child_text = block_plain_text(block_map, child_id)
        if child_text:
            parts.append(child_text)
    return " ".join(p.strip() for p in parts if p and p.strip()).strip()


def find_target_table(block_map: dict[str, Any], sequence: list[str], section_title: str) -> tuple[str, str | None]:
    section_index = None
    effective_date = None
    for i, bid in enumerate(sequence):
        data = block_map[bid]["data"]
        if data.get("type") == "heading2" and block_plain_text(block_map, bid) == section_title:
            section_index = i
            break
    if section_index is None:
        raise RuntimeError(f"找不到目标章节：{section_title}")

    for bid in sequence[section_index + 1 :]:
        data = block_map[bid]["data"]
        btype = data.get("type")
        text = block_plain_text(block_map, bid)
        if btype == "heading2":
            break
        if btype == "heading1" and re.fullmatch(r"\d{4}-\d{2}-\d{2}\s*调整", text):
            effective_date = text.replace(" 调整", "")
        if btype == "table":
            rows = table_to_rows(block_map, bid)
            if not is_target_price_table(rows):
                continue
            return bid, effective_date
    raise RuntimeError("目标章节下找不到价格表")


def table_to_rows(block_map: dict[str, Any], table_id: str) -> list[list[str]]:
    table = block_map[table_id]["data"]
    rows: list[list[str]] = []
    for row_id in table.get("rows_id", []):
        row: list[str] = []
        for col_id in table.get("columns_id", []):
            cell_key = f"{row_id}{col_id}"
            cell_info = table.get("cell_set", {}).get(cell_key)
            if not cell_info:
                row.append("")
                continue
            row.append(block_plain_text(block_map, cell_info.get("block_id")))
        rows.append(row)
    return rows


def normalize_rows(rows: list[list[str]]) -> dict[str, Any]:
    if not rows:
        return {"headers": [], "items": []}
    headers = rows[0]
    items = []
    for row in rows[1:]:
        row = row + [""] * (len(headers) - len(row))
        item = {headers[i]: row[i].strip() for i in range(len(headers))}
        item["_model_key"] = canonical_model_name(get_first(item, MODEL_KEYS))
        item["_price"] = get_first(item, PRICE_KEYS)
        items.append(item)
    return {"headers": headers, "items": items}


MODEL_KEYS = ("模型名称", "模型名称（模型 ID）", "模型名称（模型ID）", "模型名")
PRICE_KEYS = (
    "100 万 Tokens 价格",
    "100 万 Tokens 价格（换算价格）",
    "100 万 Tokens 价格 （换算价格）",
    "1 亿 Tokens 价格（换算价格）",
    "1 亿 Tokens 价格 （换算价格）",
    "价格",
)


def get_first(item: dict[str, str], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = item.get(key, "")
        if value:
            return value.strip()
    for key, value in item.items():
        compact = re.sub(r"\s+", "", key)
        if any(re.sub(r"\s+", "", candidate) == compact for candidate in keys) and value:
            return value.strip()
    return ""


def canonical_model_name(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    value = re.split(r"\s*说明\s*[:：]", value, maxsplit=1)[0].strip()
    return value


def is_target_price_table(rows: list[list[str]]) -> bool:
    if not rows:
        return False
    headers = [re.sub(r"\s+", "", header) for header in rows[0]]
    joined = "|".join(headers)
    has_model = any("模型" in header for header in headers)
    has_rate = any("倍率" in header for header in headers)
    has_price = "价格" in joined or "Tokens" in joined
    return has_model and has_rate and has_price


def snapshot_from_url(url: str, section_title: str) -> dict[str, Any]:
    try:
        import requests  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(f"缺少 requests 依赖: {e}") from e

    session = requests.Session()
    html = fetch_html(url, session=session)
    client_vars = extract_client_vars_json(html)
    data = client_vars["data"]
    block_map = data["block_map"]
    sequence = data["block_sequence"]
    table_id, effective_date = find_target_table(block_map, sequence, section_title)
    complete_table_block_map(session, url, client_vars, table_id)
    rows = table_to_rows(block_map, table_id)
    normalized = normalize_rows(rows)
    snapshot = {
        "url": url,
        "section_title": section_title,
        "effective_date": effective_date,
        "headers": normalized["headers"],
        "items": normalized["items"],
    }
    snapshot["hash"] = hashlib.sha256(json.dumps(snapshot, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return snapshot


def summarize_item(item: dict[str, str]) -> str:
    vendor = item.get("厂家", "").strip()
    model = item.get("_model_key", "") or canonical_model_name(get_first(item, MODEL_KEYS))
    ratio = item.get("倍率", "").strip()
    price = item.get("_price", "") or get_first(item, PRICE_KEYS)
    left = " / ".join([p for p in [vendor, model] if p])
    right = " · ".join([p for p in [ratio, price] if p])
    return f"{left} -> {right}".strip(" -> ")


def diff_snapshots(old: dict[str, Any], new: dict[str, Any]) -> str:
    old_items = {json.dumps(item, ensure_ascii=False, sort_keys=True): item for item in old.get("items", [])}
    new_items = {json.dumps(item, ensure_ascii=False, sort_keys=True): item for item in new.get("items", [])}
    old_by_model = {item.get("_model_key", "") or canonical_model_name(get_first(item, MODEL_KEYS)): item for item in old.get("items", [])}
    new_by_model = {item.get("_model_key", "") or canonical_model_name(get_first(item, MODEL_KEYS)): item for item in new.get("items", [])}

    added_models = [m for m in new_by_model if m and m not in old_by_model]
    removed_models = [m for m in old_by_model if m and m not in new_by_model]
    common_models = [m for m in new_by_model if m in old_by_model]

    price_lines: list[str] = []
    for model in common_models:
        old_item = old_by_model[model]
        new_item = new_by_model[model]
        parts = []
        comparisons = [
            ("厂家", "厂家", old_item.get("厂家", ""), new_item.get("厂家", "")),
            ("倍率", "倍率", old_item.get("倍率", ""), new_item.get("倍率", "")),
            ("价格", "价格", old_item.get("_price", "") or get_first(old_item, PRICE_KEYS), new_item.get("_price", "") or get_first(new_item, PRICE_KEYS)),
        ]
        for _, label, old_value, new_value in comparisons:
            if (old_value or "") != (new_value or ""):
                parts.append(f"{label} {old_value or '空'} → {new_value or '空'}")
        if parts:
            price_lines.append(f"- **{model}**：" + "；".join(parts))

    extra_lines: list[str] = []
    if not added_models and not removed_models and not price_lines and old.get("hash") != new.get("hash"):
        old_extra = set(old_items) - set(new_items)
        new_extra = set(new_items) - set(old_items)
        if new_extra:
            extra_lines.extend(f"- {summarize_item(new_items[k])}" for k in sorted(new_extra))
        if old_extra:
            extra_lines.extend(f"- {summarize_item(old_items[k])}" for k in sorted(old_extra))

    has_effective_date_change = old.get("effective_date") != new.get("effective_date")
    if not (has_effective_date_change or added_models or removed_models or price_lines or extra_lines):
        return "NO_REPLY"

    summary_parts = []
    if added_models:
        summary_parts.append(f"新增 {len(added_models)}")
    if removed_models:
        summary_parts.append(f"移除 {len(removed_models)}")
    if price_lines:
        summary_parts.append(f"调价 {len(price_lines)}")
    if has_effective_date_change:
        summary_parts.append("版本更新")
    if not summary_parts:
        summary_parts.append("表格变化")

    lines = [
        "# 贵州大模型算力倍率更新啦",
        "",
        f"- **文档**：{new['section_title']}",
        f"- **摘要**：{' · '.join(summary_parts)}",
    ]
    if has_effective_date_change:
        lines.append(f"- **版本**：{old.get('effective_date') or '无'} → {new.get('effective_date') or '无'}")
    elif new.get("effective_date"):
        lines.append(f"- **版本**：{new['effective_date']}")
    lines.append("")

    if price_lines:
        lines.append("## 💸 调价模型")
        lines.extend(price_lines)
        lines.append("")
    if added_models:
        lines.append("## 🆕 新增模型")
        lines.extend(f"- {summarize_item(new_by_model[m])}" for m in added_models)
        lines.append("")
    if removed_models:
        lines.append("## 🗑️ 移除模型")
        lines.extend(f"- {summarize_item(old_by_model[m])}" for m in removed_models)
        lines.append("")
    if extra_lines:
        lines.append("## 📝 其他表格变化")
        lines.extend(extra_lines)
        lines.append("")
    lines.append(f"- **链接**：{new['url']}")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor public Feishu wiki price table")
    parser.add_argument("url")
    parser.add_argument("--section-title", default=DEFAULT_SECTION_TITLE)
    parser.add_argument("--state-dir", default=str(Path.home() / ".openclaw" / "workspace" / "data" / "feishu-monitors"))
    parser.add_argument("--print-snapshot", action="store_true")
    args = parser.parse_args()

    state_dir = Path(args.state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256((args.url + "\0" + args.section_title).encode("utf-8")).hexdigest()[:16]
    state_path = state_dir / f"{key}.json"

    snapshot = snapshot_from_url(args.url, args.section_title)
    if args.print_snapshot:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        return 0

    if not state_path.exists():
        state_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        print("INIT_ONLY")
        return 0

    old = json.loads(state_path.read_text(encoding="utf-8"))
    message = diff_snapshots(old, snapshot)
    if message != "NO_REPLY":
        state_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(message)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"飞书价格表监控出错喵：{e}")
        raise
