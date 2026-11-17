import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
INVALID_TOKEN_CODES = {99991663, 99991664, 99991661, 99991668}
DOC_URL_RE = re.compile(r"/(wiki|docx|doc|sheets|base|bitable)/([A-Za-z0-9_-]+)")


def first(mapping, *keys):
    if not isinstance(mapping, dict):
        return ""
    for key in keys:
        value = mapping.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def http_json(method, url, headers=None, body=None, timeout=60):
    headers = dict(headers or {})
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers.setdefault("Content-Type", "application/json; charset=utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {url}: {detail[:1600]}")


def http_bytes(method, url, headers=None, timeout=180):
    request = urllib.request.Request(url, headers=dict(headers or {}), method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {url}: {detail[:1600]}")


def cache_file(payload):
    base = os.getenv("OPENCLAW_SHARED_DIR") or str((payload or {}).get("sharedDir") or "") or str(Path.home() / ".research-kb")
    path = Path(base, "cache", "feishu_token.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def credentials(payload):
    config = ((payload or {}).get("source") or {}).get("config") or {}
    app_id = os.getenv("FEISHU_APP_ID") or first(config, "appId", "app_id", "feishuAppId")
    app_secret = os.getenv("FEISHU_APP_SECRET") or first(config, "appSecret", "app_secret", "feishuAppSecret")
    return app_id, app_secret


def get_token(payload, force_refresh=False):
    app_id, app_secret = credentials(payload)
    if not app_id or not app_secret:
        raise RuntimeError("缺少飞书应用凭据：请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
    token_cache = cache_file(payload)
    now_ts = int(time.time())
    if not force_refresh and token_cache.exists():
        try:
            cached = json.loads(token_cache.read_text(encoding="utf-8"))
            token = cached.get("token") or cached.get("tenant_access_token")
            expiry = int(cached.get("expire") or cached.get("expireTime") or 0)
            if token and expiry > now_ts + 60:
                return token
        except Exception:
            pass
    data = http_json(
        "POST",
        f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal",
        body={"app_id": app_id, "app_secret": app_secret},
        timeout=30,
    )
    if data.get("code") != 0:
        raise RuntimeError(f"获取飞书 tenant_access_token 失败：{data.get('msg') or data}")
    token = data.get("tenant_access_token")
    token_cache.write_text(
        json.dumps({"token": token, "expire": now_ts + int(data.get("expire") or 7200)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return token


def with_query(endpoint, query=None):
    request_endpoint = endpoint
    if query:
        request_endpoint += ("&" if "?" in request_endpoint else "?") + urllib.parse.urlencode(query)
    return request_endpoint


def api(payload, method, endpoint, query=None, body=None, force_refresh=False):
    token = get_token(payload, force_refresh)
    request_endpoint = with_query(endpoint, query)
    url = request_endpoint if request_endpoint.startswith("http") else FEISHU_API_BASE + request_endpoint
    data = http_json(method, url, headers={"Authorization": f"Bearer {token}"}, body=body)
    if data.get("code") in INVALID_TOKEN_CODES and not force_refresh:
        return api(payload, method, endpoint, query=query, body=body, force_refresh=True)
    return data


def api_bytes(payload, method, endpoint, query=None, force_refresh=False):
    token = get_token(payload, force_refresh)
    request_endpoint = with_query(endpoint, query)
    url = request_endpoint if request_endpoint.startswith("http") else FEISHU_API_BASE + request_endpoint
    try:
        return http_bytes(method, url, headers={"Authorization": f"Bearer {token}"})
    except RuntimeError as exc:
        text = str(exc)
        if not force_refresh and ("HTTP 401" in text or any(str(code) in text for code in INVALID_TOKEN_CODES)):
            return api_bytes(payload, method, endpoint, query=query, force_refresh=True)
        raise


def message_id(message):
    return first(message or {}, "message_id", "msg_id", "messageId", "open_message_id")


def message_create_seconds(message):
    value = first(message or {}, "create_time", "created_at", "createTime")
    if not value:
        return 0
    try:
        number = int(float(value))
    except Exception:
        return 0
    if number > 10_000_000_000:
        number = number // 1000
    return number


def fetch_messages(payload, chat_id, start_ts, end_ts, max_messages=100):
    if not chat_id:
        return []
    page_token = ""
    items = []
    max_messages = max(1, int(max_messages or 100))
    while len(items) < max_messages:
        query = {
            "container_id_type": "chat",
            "container_id": chat_id,
            "start_time": str(max(0, int(start_ts or 0))),
            "end_time": str(max(0, int(end_ts or time.time()))),
            "sort_type": "ByCreateTimeAsc",
            "page_size": min(50, max_messages - len(items)),
        }
        if page_token:
            query["page_token"] = page_token
        data = api(payload, "GET", "/im/v1/messages", query=query)
        if data.get("code") != 0:
            raise RuntimeError(f"读取飞书群消息失败：{data.get('msg') or data}")
        inner = data.get("data") or {}
        items.extend(inner.get("items") or [])
        if not inner.get("has_more"):
            break
        page_token = inner.get("page_token") or inner.get("next_page_token") or ""
        if not page_token:
            break
    return items[:max_messages]


def get_message(payload, message_id_value):
    data = api(payload, "GET", f"/im/v1/messages/{urllib.parse.quote(str(message_id_value), safe='')}")
    if data.get("code") != 0:
        raise RuntimeError(f"读取飞书消息失败：{data.get('msg') or data}")
    return (data.get("data") or {}).get("items") or data.get("data") or {}


def get_chat(payload, chat_id):
    data = api(payload, "GET", f"/im/v1/chats/{urllib.parse.quote(str(chat_id), safe='')}")
    if data.get("code") != 0:
        raise RuntimeError(f"读取飞书群信息失败：{data.get('msg') or data}")
    return data.get("data") or {}


def download_message_resource(payload, message_id_value, file_key, resource_type, output_path):
    if not message_id_value or not file_key:
        raise RuntimeError("缺少 message_id 或 file_key，无法下载飞书消息资源")
    resource_type = "image" if resource_type == "image" else "file"
    endpoint = f"/im/v1/messages/{urllib.parse.quote(str(message_id_value), safe='')}/resources/{urllib.parse.quote(str(file_key), safe='')}"
    data = api_bytes(payload, "GET", endpoint, query={"type": resource_type})
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return str(target)


def extract_refs(text):
    refs = []
    if not text:
        return refs
    value = str(text)
    for url in re.findall(r"https?://[^\s)>'\"]+", value):
        parsed = url.rstrip(".,;，。；")
        match = DOC_URL_RE.search(parsed)
        ref = {"url": parsed}
        if match:
            ref["type"] = match.group(1)
            ref["token"] = match.group(2)
        refs.append(ref)
    for match in DOC_URL_RE.finditer(value):
        refs.append({"type": match.group(1), "token": match.group(2)})
    clean = value.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{12,}", clean):
        refs.append({"token": clean})
    seen = set()
    result = []
    for ref in refs:
        key = ref.get("url") or f"{ref.get('type', '')}:{ref.get('token', '')}"
        if key and key not in seen:
            result.append(ref)
            seen.add(key)
    return result


def ref_token(ref):
    token = first(ref, "token", "docToken", "doc_token", "documentId", "document_id", "wikiToken", "wiki_token", "spreadsheetToken", "appToken")
    ref_type = first(ref, "type", "objType", "obj_type", "kind")
    url = first(ref, "url", "href", "link")
    if url and not token:
        match = DOC_URL_RE.search(url)
        if match:
            ref_type = ref_type or match.group(1)
            token = match.group(2)
    return token, ref_type.lower(), url


def resolve_wiki(payload, token):
    data = api(payload, "GET", "/wiki/v2/spaces/get_node", query={"token": token})
    if data.get("code") != 0:
        raise RuntimeError(f"飞书 wiki 解析失败：{data.get('msg') or data}")
    node = ((data.get("data") or {}).get("node") or {})
    return {
        "token": node.get("obj_token") or token,
        "type": node.get("obj_type") or "wiki",
        "title": node.get("title") or "飞书 Wiki 页面",
        "url": node.get("url") or "",
    }


def read_docx(payload, token):
    raw = api(payload, "GET", f"/docx/v1/documents/{urllib.parse.quote(token)}/raw_content")
    if raw.get("code") != 0:
        raise RuntimeError(f"读取飞书文档正文失败：{raw.get('msg') or raw}")
    info = api(payload, "GET", f"/docx/v1/documents/{urllib.parse.quote(token)}")
    title = "飞书文档"
    if info.get("code") == 0:
        title = (((info.get("data") or {}).get("document") or {}).get("title") or title)
    return {"title": title, "content": ((raw.get("data") or {}).get("content") or ""), "type": "docx", "externalId": token}


def column_name(num):
    result = ""
    while num > 0:
        num -= 1
        result = chr(65 + (num % 26)) + result
        num //= 26
    return result or "A"


def markdown_table(rows):
    if not rows:
        return ""
    width = max(len(row or []) for row in rows)
    if width <= 0:
        return ""
    clean = []
    for row in rows:
        row = row or []
        current = []
        for index in range(width):
            value = row[index] if index < len(row) else ""
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            current.append(str(value).replace("\n", "<br>").replace("|", "\\|"))
        clean.append(current)
    lines = ["| " + " | ".join(clean[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for row in clean[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def read_sheet(payload, token):
    meta = api(payload, "GET", f"/sheets/v3/spreadsheets/{urllib.parse.quote(token)}/sheets/query")
    if meta.get("code") != 0:
        raise RuntimeError(f"读取飞书表格元数据失败：{meta.get('msg') or meta}")
    sections = []
    for sheet in sorted(((meta.get("data") or {}).get("sheets") or []), key=lambda item: item.get("index") or 0)[:3]:
        if sheet.get("hidden"):
            continue
        sheet_id = sheet.get("sheet_id")
        title = sheet.get("title") or sheet_id or "Sheet"
        row_count = min(int(((sheet.get("grid_properties") or {}).get("row_count") or 100)), 100)
        col_count = min(int(((sheet.get("grid_properties") or {}).get("column_count") or 20)), 20)
        if not sheet_id or row_count <= 0 or col_count <= 0:
            continue
        ref = f"{sheet_id}!A1:{column_name(col_count)}{row_count}"
        values = api(payload, "GET", f"/sheets/v2/spreadsheets/{urllib.parse.quote(token)}/values/{urllib.parse.quote(ref, safe='!')}")
        rows = (((values.get("data") or {}).get("valueRange") or {}).get("values") or []) if values.get("code") == 0 else []
        sections.append(f"## 表格：{title}\n\n{markdown_table(rows) if rows else '未读取到可展示单元格。'}")
    return {"title": "飞书表格", "content": "\n\n".join(sections), "type": "sheet", "externalId": token}


def read_bitable(payload, token):
    tables_data = api(payload, "GET", f"/bitable/v1/apps/{urllib.parse.quote(token)}/tables")
    if tables_data.get("code") != 0:
        raise RuntimeError(f"读取飞书多维表格表列表失败：{tables_data.get('msg') or tables_data}")
    sections = []
    for table in (((tables_data.get("data") or {}).get("items") or [])[:3]):
        table_id = table.get("table_id")
        name = table.get("name") or table_id or "Table"
        if not table_id:
            continue
        records_data = api(payload, "GET", f"/bitable/v1/apps/{urllib.parse.quote(token)}/tables/{urllib.parse.quote(table_id)}/records", query={"page_size": 20})
        records = ((records_data.get("data") or {}).get("items") or []) if records_data.get("code") == 0 else []
        fields = []
        for record in records:
            for key in (record.get("fields") or {}).keys():
                if key not in fields:
                    fields.append(key)
        rows = [fields] + [[(record.get("fields") or {}).get(field, "") for field in fields] for record in records]
        sections.append(f"## 多维表：{name}\n\n{markdown_table(rows) if fields else '未读取到记录。'}")
    return {"title": "飞书多维表格", "content": "\n\n".join(sections), "type": "bitable", "externalId": token}


def read_reference(payload, ref):
    token, ref_type, url = ref_token(ref)
    if not token:
        return None
    if ref_type == "wiki":
        resolved = resolve_wiki(payload, token)
        resolved["url"] = url or resolved.get("url") or f"https://feishu.cn/wiki/{token}"
        return read_reference(payload, resolved)
    if ref_type in {"sheet", "sheets", "spreadsheet"}:
        result = read_sheet(payload, token)
    elif ref_type in {"base", "bitable"}:
        result = read_bitable(payload, token)
    else:
        result = read_docx(payload, token)
    result["url"] = url or result.get("url") or ""
    return result