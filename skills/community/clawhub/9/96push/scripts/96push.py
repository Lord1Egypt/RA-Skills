#!/usr/bin/env python3
"""96Push remote control CLI — wraps the proxy API for OpenClaw skills."""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import uuid

BASE_URL = "https://api.96.cn/api/push/proxy"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
RULES_DIR = os.path.join(SKILL_DIR, "references", "platform-rules")

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".flv", ".wmv"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_IMAGE_UPLOAD_BYTES = 50 * 1024 * 1024
CONTENT_TYPE_LABELS = {
    "article": "文章",
    "graph_text": "图文",
    "video": "视频",
}
PLATFORM_SUPPORTS = {
    "wechat": {"article", "graph_text"},
    "wechat-video": {"graph_text", "video"},
    "douyin": {"graph_text", "video"},
    "toutiaohao": {"article", "graph_text", "video"},
    "kuaishou": {"graph_text", "video"},
    "xiaohongshu": {"graph_text", "video"},
    "omtencent": {"article", "video"},
    "weishi": {"video"},
    "bilibili": {"article", "video"},
    "baijiahao": {"article", "graph_text", "video"},
    "sohuhao": {"article", "graph_text", "video"},
    "wangyihao": {"article"},
    "jianshuhao": {"article"},
    "zhihu": {"article", "graph_text", "video"},
    "pinduoduo": {"video"},
    "juejin": {"article", "graph_text"},
    "tiktok": {"video"},
    "csdn": {"article", "video"},
}
PLATFORM_ALIASES = {
    "wechat": "wechat",
    "weixin": "wechat",
    "微信公众号": "wechat",
    "公众号": "wechat",
    "wechat-video": "wechat-video",
    "wechat_video": "wechat-video",
    "weixin-video": "wechat-video",
    "微信视频号": "wechat-video",
    "视频号": "wechat-video",
    "douyin": "douyin",
    "抖音": "douyin",
    "toutiao": "toutiaohao",
    "toutiaohao": "toutiaohao",
    "今日头条": "toutiaohao",
    "头条": "toutiaohao",
    "kuaishou": "kuaishou",
    "快手": "kuaishou",
    "xiaohongshu": "xiaohongshu",
    "xhs": "xiaohongshu",
    "小红书": "xiaohongshu",
    "omtencent": "omtencent",
    "腾讯内容开放平台": "omtencent",
    "腾讯内容": "omtencent",
    "企鹅号": "omtencent",
    "weishi": "weishi",
    "微视": "weishi",
    "bilibili": "bilibili",
    "bili": "bilibili",
    "哔哩哔哩": "bilibili",
    "b站": "bilibili",
    "acfun": "acfun",
    "a站": "acfun",
    "baijiahao": "baijiahao",
    "百家号": "baijiahao",
    "sohuhao": "sohuhao",
    "sohu": "sohuhao",
    "搜狐号": "sohuhao",
    "wangyihao": "wangyihao",
    "netease": "wangyihao",
    "网易号": "wangyihao",
    "sina": "sina",
    "weibo": "sina",
    "新浪微博": "sina",
    "微博": "sina",
    "jianshuhao": "jianshuhao",
    "jianshu": "jianshuhao",
    "简书号": "jianshuhao",
    "简书": "jianshuhao",
    "zhihu": "zhihu",
    "知乎": "zhihu",
    "pinduoduo": "pinduoduo",
    "pdd": "pinduoduo",
    "拼多多": "pinduoduo",
    "juejin": "juejin",
    "掘金": "juejin",
    "tiktok": "tiktok",
    "youtube": "youtube",
    "ytube": "youtube",
    "yt": "youtube",
    "csdn": "csdn",
    "x": "x",
    "twitter": "x",
}


class PlainOutput(str):
    """Marker for commands that should print human-readable text."""


def media_extension(value: str) -> str:
    parsed = urllib.parse.urlparse((value or "").strip())
    path = parsed.path or value
    _, ext = os.path.splitext(path)
    return ext.lower()


def media_kind(value: str) -> str:
    raw = (value or "").strip()
    if raw.startswith("data:video/"):
        return "video"
    if raw.startswith("data:image/"):
        return "image"
    parsed = urllib.parse.urlparse(raw)
    if "/pix/" in parsed.path:
        return "image"
    ext = media_extension(raw)
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in IMAGE_EXTENSIONS:
        return "image"
    return ""


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def local_file_path(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    expanded = os.path.expanduser(raw)
    if os.path.isfile(expanded):
        return os.path.abspath(expanded)

    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme == "file":
        path = urllib.request.url2pathname(parsed.path)
        if parsed.netloc and os.name == "nt":
            path = f"//{parsed.netloc}{path}"
        if os.path.isfile(path):
            return os.path.abspath(path)
    return ""


def normalize_platform_key(value: str) -> str:
    key = (value or "").strip()
    if not key:
        return ""
    normalized = key.lower().replace("_", "-")
    if normalized in PLATFORM_ALIASES:
        return PLATFORM_ALIASES[normalized]
    if key in PLATFORM_ALIASES:
        return PLATFORM_ALIASES[key]
    for alias, platform in PLATFORM_ALIASES.items():
        if alias and alias in key:
            return platform
    return normalized


def available_rule_keys() -> list[str]:
    if not os.path.isdir(RULES_DIR):
        return []
    keys = []
    for name in os.listdir(RULES_DIR):
        if name.endswith(".md") and name not in {"index.md", "common.md"}:
            keys.append(name[:-3])
    return sorted(keys)


def rule_path_for_platform(value: str) -> tuple[str, str]:
    key = normalize_platform_key(value)
    if not key:
        return "", ""
    path = os.path.join(RULES_DIR, f"{key}.md")
    return key, path


def read_platform_rule(value: str) -> tuple[str, str, str]:
    key, path = rule_path_for_platform(value)
    if not path or not os.path.isfile(path):
        return key, path, ""
    with open(path, encoding="utf-8") as f:
        return key, path, f.read().strip()


def platform_key_from_account(account: dict) -> str:
    for field in ("platType", "plat_type", "platformType", "platform_type", "platform"):
        value = account.get(field)
        if isinstance(value, str) and value.strip():
            return normalize_platform_key(value)
        if isinstance(value, dict):
            for nested in ("plat_type", "platType", "name"):
                nested_value = value.get(nested)
                if nested_value:
                    return normalize_platform_key(str(nested_value))
    for field in ("platName", "platformName", "platform_name", "name"):
        value = account.get(field)
        if isinstance(value, str) and value.strip():
            return normalize_platform_key(value)
    return ""


def flatten_response_rows(resp: dict) -> list[dict]:
    if isinstance(resp, list):
        return [item for item in resp if isinstance(item, dict)]
    if not isinstance(resp, dict):
        return []
    for key in ("data", "list", "records"):
        value = resp.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = flatten_response_rows(value)
            if nested:
                return nested
    if all(isinstance(value, dict) for value in resp.values()):
        return [value for value in resp.values() if isinstance(value, dict)]
    return []


def enrich_accounts_with_platforms(accounts: list[dict]) -> list[dict]:
    if all(platform_key_from_account(account) for account in accounts):
        return accounts
    resp = request("GET", "account/logged", query={})
    rows = flatten_response_rows(resp)
    by_id = {}
    for row in rows:
        if row.get("id") is not None:
            by_id[int(row["id"])] = row
    enriched = []
    for account in accounts:
        merged = dict(account)
        row = by_id.get(int(account.get("id", 0)))
        if row:
            for key in ("platform", "platName", "plat_type", "platType"):
                if key in row and key not in merged:
                    merged[key] = row[key]
        enriched.append(merged)
    return enriched


def emit_publish_rules_hint(accounts: list[dict], content_type: str, show_full: bool = False) -> None:
    enriched = enrich_accounts_with_platforms(accounts)
    keys = sorted({platform_key_from_account(account) for account in enriched if platform_key_from_account(account)})
    if not keys:
        print("[rules] 未能从账号参数识别平台；发布前可运行 rules --platform <平台> 查看限制。", file=sys.stderr)
        return
    label = CONTENT_TYPE_LABELS.get(content_type, content_type)
    for key in keys:
        path = os.path.join(RULES_DIR, f"{key}.md")
        if os.path.isfile(path):
            print(f"[rules] {key} {label}规则: {path}", file=sys.stderr)
            if show_full:
                with open(path, encoding="utf-8") as f:
                    print("\n" + f.read().strip() + "\n", file=sys.stderr)
        else:
            print(f"[rules] {key} 暂无规则文件，请勿猜测必填 settings。", file=sys.stderr)


def validate_platform_content_support(accounts: list[dict], content_type: str) -> dict | None:
    enriched = enrich_accounts_with_platforms(accounts)
    failures = []
    unknown = []
    for account in enriched:
        key = platform_key_from_account(account)
        account_id = account.get("id")
        if not key:
            unknown.append({"id": account_id, "account": account})
            continue
        supported = PLATFORM_SUPPORTS.get(key)
        if supported is None:
            unknown.append({"id": account_id, "platform": key})
            continue
        if content_type not in supported:
            failures.append({
                "id": account_id,
                "platform": key,
                "requestedType": content_type,
                "supportedTypes": sorted(supported),
            })

    if failures:
        label = CONTENT_TYPE_LABELS.get(content_type, content_type)
        return {
            "error": f"target platform does not support {label}",
            "unsupportedTargets": failures,
            "message": (
                "Do not publish with the article endpoint for platforms that only support "
                "graph_text/video. Create or select content with a supported type first."
            ),
        }
    if unknown:
        print(f"[rules] 无法识别部分账号平台，跳过支持类型校验: {unknown}", file=sys.stderr)
    return None


def parse_json_array(raw: str, field: str) -> list[str]:
    if not raw:
        return []
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field} must be a JSON array: {exc}") from exc
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a JSON array")
    items = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError(f"{field} values must be strings")
        item = item.strip()
        if item:
            items.append(item)
    return items


def confirmation_error(action: str, flag: str = "--confirm") -> dict:
    return {
        "error": f"{action} requires {flag} after explicit user approval",
        "requiredConfirmation": flag,
        "message": (
            "Show the user the exact content/config ID, target accounts, "
            "visibility/draft state, and settings before rerunning with confirmation."
        ),
    }


def require_confirm(args, action: str, flag: str = "confirm"):
    if getattr(args, flag, False):
        return None
    return confirmation_error(action, f"--{flag.replace('_', '-')}")


def validate_public_urls(values: list[str], field: str) -> None:
    for value in values:
        parsed = urllib.parse.urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"{field} only accepts HTTP(S) URLs, got: {value}. Use upload first for image files.")


def validate_content_payload(content_type: str, args, files: list[str], thumb: list[str], require_article_body: bool) -> None:
    validate_public_urls(files, "files")
    validate_public_urls(thumb, "thumb")

    if content_type == "article":
        if files:
            print("[create] article ignores files; put body images in markdown/content and covers in thumb", file=sys.stderr)
        if require_article_body and not (args.markdown or args.content):
            raise ValueError("article requires --markdown or --content")
        return

    if args.markdown or args.content:
        print(f"[create] {content_type} ignores markdown/content; media URLs in files are the content", file=sys.stderr)

    if content_type == "graph_text":
        if not files:
            raise ValueError("graph_text requires --files with at least one image URL")
        if any(media_kind(item) == "video" for item in files):
            raise ValueError("graph_text files must be image URLs, not video URLs")
        return

    if content_type == "video":
        if len(files) != 1:
            raise ValueError("video requires --files with exactly one video URL")
        if media_kind(files[0]) == "image":
            raise ValueError("video files must contain one video URL, not an image URL")


def build_content_body(args, content_type: str, files: list[str], thumb: list[str], require_article_body: bool) -> dict:
    validate_content_payload(content_type, args, files, thumb, require_article_body)
    body = {
        "title": args.title,
        "autoThumb": not args.no_auto_thumb,
    }
    if args.desc:
        body["desc"] = args.desc
    if thumb:
        body["thumb"] = thumb
    if content_type == "article":
        if args.content:
            body["content"] = args.content
        if args.markdown:
            body["markdown"] = args.markdown
    else:
        body["files"] = files
    return body


def content_type_from_publish_type(value) -> str:
    try:
        publish_type = int(value)
    except (TypeError, ValueError):
        return ""
    return {1: "article", 2: "graph_text", 3: "video"}.get(publish_type, "")


def infer_type_from_files(files: list[str]) -> str:
    kinds = [media_kind(item) for item in files]
    if any(kind == "video" for kind in kinds):
        return "video"
    if any(kind == "image" for kind in kinds):
        return "graph_text"
    return ""


def infer_type_from_content_detail(content_id: int) -> str:
    detail = request("GET", f"article/get/{content_id}")
    if not isinstance(detail, dict) or "error" in detail:
        return ""

    data = detail.get("data", detail)
    if not isinstance(data, dict):
        return ""

    content_type = content_type_from_publish_type(data.get("publish_type"))
    publish_data = data.get("publish_data") or {}
    if isinstance(publish_data, dict):
        inferred = infer_type_from_files(publish_data.get("files") or [])
        if inferred:
            return inferred
    return content_type


def resolve_content_type(explicit_type: str | None, files: list[str] | None = None, content_id: int | None = None) -> str:
    if explicit_type:
        if explicit_type == "article" and content_id is not None:
            inferred = infer_type_from_content_detail(content_id)
            if inferred in {"graph_text", "video"}:
                return inferred
        return explicit_type
    inferred = infer_type_from_files(files or [])
    if inferred:
        return inferred
    if content_id is not None:
        inferred = infer_type_from_content_detail(content_id)
        if inferred:
            return inferred
    return "article"


def get_api_key() -> str:
    key = os.environ.get("PUSH_API_KEY", "").strip()
    if key:
        return key
    env_file = os.path.expanduser("~/.openclaw/.env")
    if os.path.isfile(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("PUSH_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def missing_api_key_error() -> dict:
    return {
        "error": "PUSH_API_KEY not configured",
        "setup": [
            "1. Download 96Push from https://push.96.cn",
            "2. Launch and login",
            "3. Go to profile (bottom-left avatar) → API Key → Generate",
            "4. Add to ~/.openclaw/.env: PUSH_API_KEY=pk_your_key_here",
        ],
    }


def request(method: str, path: str, body: dict | None = None, query: dict | None = None, timeout: int = 30) -> dict:
    api_key = get_api_key()
    if not api_key:
        return missing_api_key_error()

    url = f"{BASE_URL}/{path.lstrip('/')}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})

    headers = {
        "X-Push-Api-Key": api_key,
        "Content-Type": "application/json",
    }

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read())
        except Exception:
            err_body = {}
        return {"error": f"HTTP {e.code}", "detail": err_body}
    except urllib.error.URLError as e:
        return {"error": f"Network error: {e.reason}"}
    except TimeoutError:
        return {"error": "Request timed out"}


def request_multipart(path: str, file_path: str, field_name: str = "file", timeout: int = 120) -> dict:
    api_key = get_api_key()
    if not api_key:
        return missing_api_key_error()

    filename = os.path.basename(file_path)
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    boundary = f"----96PushBoundary{uuid.uuid4().hex}"

    with open(file_path, "rb") as f:
        file_data = f.read()

    body = b"".join([
        f"--{boundary}\r\n".encode(),
        (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode(),
        f"Content-Type: {content_type}\r\n\r\n".encode(),
        file_data,
        f"\r\n--{boundary}--\r\n".encode(),
    ])

    headers = {
        "X-Push-Api-Key": api_key,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    url = f"{BASE_URL}/{path.lstrip('/')}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if not raw:
                return {}
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"raw": raw.decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read())
        except Exception:
            err_body = {}
        return {"error": f"HTTP {e.code}", "detail": err_body}
    except urllib.error.URLError as e:
        return {"error": f"Network error: {e.reason}"}
    except TimeoutError:
        return {"error": "Request timed out"}


# ── Query commands ──────────────────────────────────────────────

def cmd_check(_args):
    return request("GET", "check")


def cmd_platforms(args):
    q = {"simple": "true"}
    if args.article:
        q["article"] = "true"
    if args.graph_text:
        q["graph_text"] = "true"
    if args.video:
        q["video"] = "true"
    return request("GET", "platform/list", query=q)


def cmd_accounts(args):
    q = {}
    if args.simple:
        q["simple"] = "1"
    return request("GET", "account/logged", query=q)


def cmd_all_accounts(_args):
    return request("GET", "account/list", query={"simple": "1"})


def cmd_articles(args):
    q = {"current": str(args.page), "size": str(args.size), "simple": "true"}
    if args.status is not None:
        q["status"] = str(args.status)
    return request("GET", "article/list", query=q)


def cmd_article(args):
    return request("GET", f"article/get/{args.id}")


def cmd_records(args):
    q = {"current": str(args.page), "size": str(args.size)}
    if args.status:
        q["status"] = str(args.status)
    return request("GET", "record/list", query=q)


def cmd_record(args):
    return request("GET", f"record/info/{args.id}")


def cmd_dashboard(_args):
    return request("GET", "home/dashboard")


def cmd_overview(_args):
    return request("GET", "home/overview")


def cmd_user(_args):
    return request("GET", "user/info")


def cmd_plat_sets(args):
    return request("GET", f"platSet/list/{args.pid}")


def cmd_rules(args):
    if args.list:
        return {
            "rulesDir": RULES_DIR,
            "platforms": available_rule_keys(),
            "usage": "python3 scripts/96push.py rules --platform wechat --type article",
        }

    platforms = split_csv(args.platform)
    if not platforms:
        return {
            "error": "Use --platform <platform[,platform...]> or --list",
            "platforms": available_rule_keys(),
        }

    blocks = []
    missing = []
    label = CONTENT_TYPE_LABELS.get(args.type or "", args.type or "all")
    for platform in platforms:
        key, path, text = read_platform_rule(platform)
        if not text:
            missing.append({"platform": platform, "normalized": key, "expected": path})
            continue
        header = f"<!-- requested_content_type: {args.type or 'all'} ({label}) -->"
        blocks.append(f"{header}\n{text}")

    if missing and not blocks:
        return {"error": "No platform rule files found", "missing": missing, "platforms": available_rule_keys()}

    if missing:
        missing_text = "\n".join(f"- {item['platform']} -> {item['expected']}" for item in missing)
        blocks.append("# Missing Platform Rules\n\n" + missing_text)

    return PlainOutput("\n\n---\n\n".join(blocks))


# ── Media upload ────────────────────────────────────────────────

def cmd_upload(args):
    valid_files = []
    failures = []

    for raw_file in args.file or []:
        path = local_file_path(raw_file)
        if not path:
            failures.append({"file": raw_file, "error": "file does not exist or is not readable"})
            continue
        if media_kind(path) != "image":
            failures.append({"file": path, "error": "upload only accepts image files"})
            continue
        size = os.path.getsize(path)
        if size > MAX_IMAGE_UPLOAD_BYTES:
            failures.append({
                "file": path,
                "error": f"image exceeds {MAX_IMAGE_UPLOAD_BYTES // (1024 * 1024)}MB limit",
                "size": size,
            })
            continue
        valid_files.append(path)

    if failures:
        return {"error": "invalid upload file", "failures": failures}

    confirm_error = require_confirm(args, "upload image")
    if confirm_error:
        return confirm_error | {
            "files": [{"path": path, "size": os.path.getsize(path)} for path in valid_files],
        }

    uploads = []
    upload_failures = []
    for path in valid_files:
        result = request_multipart("pix/upload", path, timeout=args.timeout)
        url = ""
        if isinstance(result, dict):
            data = result.get("data")
            if isinstance(data, str) and data.strip():
                url = data.strip()
            elif isinstance(result.get("url"), str):
                url = result["url"].strip()

        if url:
            uploads.append({"path": path, "url": url})
        else:
            upload_failures.append({"path": path, "response": result})

    response = {
        "uploads": uploads,
        "urls": [item["url"] for item in uploads],
        "usage": (
            "Use returned URLs in markdown/content image src values, thumb, or files. "
            "OpenClaw cannot read arbitrary user-local paths; --file must point to a file available in the skill runtime."
        ),
    }
    if upload_failures:
        response["error"] = "one or more uploads failed"
        response["failures"] = upload_failures
    return response


# ── Content creation ────────────────────────────────────────────

def cmd_create(args):
    try:
        thumb = parse_json_array(args.thumb, "thumb")
        files = parse_json_array(args.files, "files")
    except ValueError as exc:
        return {"error": str(exc)}
    content_type = resolve_content_type(args.type, files=files)

    try:
        body = build_content_body(args, content_type, files, thumb, require_article_body=True)
    except ValueError as exc:
        return {"error": str(exc)}

    endpoints = {
        "article": "article/create",
        "graph_text": "article/graphText",
        "video": "article/video",
    }
    return request("POST", endpoints.get(content_type, "article/create"), body=body)


def cmd_update(args):
    confirm_error = require_confirm(args, "update")
    if confirm_error:
        return confirm_error

    try:
        thumb = parse_json_array(args.thumb, "thumb")
        files = parse_json_array(args.files, "files")
    except ValueError as exc:
        return {"error": str(exc)}
    content_type = resolve_content_type(args.type, files=files, content_id=args.id)

    try:
        body = build_content_body(args, content_type, files, thumb, require_article_body=False)
    except ValueError as exc:
        return {"error": str(exc)}
    return request("POST", f"article/update/{args.id}", body=body)


def cmd_delete_article(args):
    confirm_error = require_confirm(args, "delete-article")
    if confirm_error:
        return confirm_error
    return request("DELETE", f"article/delete/{args.id}")


# ── Publishing ──────────────────────────────────────────────────

def cmd_publish(args):
    if args.accounts_json:
        accounts = json.loads(args.accounts_json)
    elif args.accounts:
        accounts = []
        for a in args.accounts.split(","):
            a = a.strip()
            if a:
                accounts.append({"id": int(a), "platName": "", "settings": {}})
    else:
        return {"error": "Either --accounts or --accounts-json is required"}

    if len(accounts) > 1 and not getattr(args, "confirm_multi_account", False):
        return confirmation_error(
            "multi-account publish",
            "--confirm-multi-account",
        ) | {
            "accounts": accounts,
            "message": (
                "Multiple target accounts can amplify mistakes across platforms. "
                "Confirm the full target list and rerun with --confirm-multi-account."
            ),
        }

    confirm_error = require_confirm(args, "publish")
    if confirm_error:
        return confirm_error | {"accounts": accounts, "draft": args.draft}

    content_type = resolve_content_type(args.type, content_id=args.id)
    support_error = validate_platform_content_support(accounts, content_type)
    if support_error:
        return support_error

    if not getattr(args, "force", False):
        active = request("GET", "record/list", query={"current": "1", "size": "5"})
        active_list = active.get("list", []) if isinstance(active, dict) else []
        busy = [r for r in active_list if r.get("status") in (1, 5)]
        if busy:
            names = {1: "发布中", 5: "排队中"}
            items = [f"#{r['id']}({names.get(r.get('status'), '?')})" for r in busy[:3]]
            print(f"[info] 当前有任务: {', '.join(items)}，新任务将自动入队", file=sys.stderr)

    emit_publish_rules_hint(accounts, content_type, show_full=getattr(args, "show_rules", False))
    body = {
        "headless": True,
        "syncDraft": args.draft,
        "postAccounts": accounts,
    }
    endpoints = {
        "article": f"publish/article/{args.id}",
        "graph_text": f"publish/graphText/{args.id}",
        "video": f"publish/video/{args.id}",
    }
    result = request("POST", endpoints.get(content_type, f"publish/article/{args.id}"), body=body, timeout=60)

    # 自动 poll 等待结果（除非 --no-wait）
    if getattr(args, "no_wait", False):
        return result

    if "error" in result:
        return result

    data = result.get("data", result)
    rid = data.get("publishRecordId")
    if not rid:
        return result

    print(f"[publish] 已提交，recordId={rid}，等待完成...", file=sys.stderr)

    max_attempts = 200
    interval = 5
    for i in range(max_attempts):
        time.sleep(interval)
        rec = request("GET", "record/list", query={"current": "1", "size": "10"})
        rec_list = rec.get("list", []) if isinstance(rec, dict) else []
        target = next((r for r in rec_list if r.get("id") == rid), None)
        if not target:
            continue
        status = target.get("status", 1)
        if status == 6:
            return {"publish": "cancelled", "record": target, "detail": []}
        if status not in (1, 5):
            info = request("GET", f"record/info/{rid}")
            detail = info if isinstance(info, list) else info.get("data", [])
            return {
                "publish": "done",
                "record": target,
                "detail": detail if isinstance(detail, list) else [],
            }
        qpos = target.get("queue_position")
        if qpos is not None and status == 5:
            print(f"[poll {i+1}/{max_attempts}] 排队中，位置: {qpos}", file=sys.stderr)
        elif status == 1:
            print(f"[poll {i+1}/{max_attempts}] 发布中...", file=sys.stderr)

    return {
        "publish": "timeout",
        "publishRecordId": rid,
        "message": f"Record {rid} still active after {max_attempts * interval // 60}min",
    }


def cmd_poll(args):
    rid = args.id
    max_attempts = args.max or 60
    interval = args.interval or 5

    for i in range(max_attempts):
        rec = request("GET", "record/list", query={"current": "1", "size": "10"})
        rec_list = rec.get("list", []) if isinstance(rec, dict) else []
        target = next((r for r in rec_list if r.get("id") == rid), None)

        if target:
            status = target.get("status", 1)
            # status 6 = Cancelled — terminal state
            if status == 6:
                return {
                    "poll": "cancelled",
                    "attempts": i + 1,
                    "record": target,
                    "detail": [],
                }
            # status 1 = Publishing, status 5 = Queued — still waiting
            if status not in (1, 5):
                info = request("GET", f"record/info/{rid}")
                detail = info if isinstance(info, list) else info.get("data", [])
                return {
                    "poll": "done",
                    "attempts": i + 1,
                    "record": target,
                    "detail": detail if isinstance(detail, list) else [],
                }
            # Show queue position if available
            qpos = target.get("queue_position")
            if qpos is not None and status == 5:
                print(f"[poll {i+1}/{max_attempts}] 排队中，位置: {qpos}", file=sys.stderr)
            elif status == 1:
                print(f"[poll {i+1}/{max_attempts}] 发布中...", file=sys.stderr)

        if i < max_attempts - 1:
            time.sleep(interval)

    return {
        "poll": "timeout",
        "attempts": max_attempts,
        "message": f"Record {rid} still active after {max_attempts * interval}s. The browser automation may be stuck or the daemon needs restart.",
    }


def cmd_queue(_args):
    return request("GET", "queue/list")


def cmd_cancel_queue(args):
    confirm_error = require_confirm(args, "cancel-queue")
    if confirm_error:
        return confirm_error
    return request("POST", f"queue/cancel/{args.id}")


# ── Platform settings management ────────────────────────────────

def cmd_create_plat_set(args):
    confirm_error = require_confirm(args, "create-plat-set")
    if confirm_error:
        return confirm_error
    body = {
        "name": args.name,
        "description": args.description or "",
        "platform_id": args.pid,
        "setting": json.loads(args.setting),
    }
    return request("POST", "platSet/create", body=body)


def cmd_update_plat_set(args):
    confirm_error = require_confirm(args, "update-plat-set")
    if confirm_error:
        return confirm_error
    body = {
        "name": args.name,
        "description": args.description or "",
        "platform_id": args.pid,
        "setting": json.loads(args.setting),
    }
    return request("POST", f"platSet/update/{args.sid}", body=body)


def cmd_delete_plat_set(args):
    confirm_error = require_confirm(args, "delete-plat-set")
    if confirm_error:
        return confirm_error
    return request("DELETE", f"platSet/delete/{args.sid}")


# ── Main ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="96Push remote control")
    sub = parser.add_subparsers(dest="command", required=True)

    # Query
    sub.add_parser("check", help="Health check — is client online?")

    p = sub.add_parser("platforms", help="List supported platforms")
    p.add_argument("--article", action="store_true")
    p.add_argument("--graph-text", action="store_true")
    p.add_argument("--video", action="store_true")

    p = sub.add_parser("accounts", help="List logged-in accounts")
    p.add_argument("--simple", action="store_true", default=True)

    sub.add_parser("all-accounts", help="List all accounts (including logged out)")

    p = sub.add_parser("articles", help="List articles")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=10)
    p.add_argument("--status", type=int, default=None, help="1=draft, 2=published")

    p = sub.add_parser("article", help="Get article detail")
    p.add_argument("--id", type=int, required=True)

    p = sub.add_parser("records", help="List publish records")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=10)
    p.add_argument("--status", type=int, default=None, help="1=publishing,2=all_failed,3=partial,4=all_success")

    p = sub.add_parser("record", help="Get publish record detail")
    p.add_argument("--id", type=int, required=True)

    sub.add_parser("dashboard", help="Dashboard summary")
    sub.add_parser("overview", help="Overview with charts")
    sub.add_parser("user", help="Current user info")

    p = sub.add_parser("plat-sets", help="List platform publish configs")
    p.add_argument("--pid", type=int, required=True, help="Platform ID")

    p = sub.add_parser("rules", help="Show platform publishing rules from local reference files")
    p.add_argument("--platform", default="", help="Platform key/name, or comma-separated list (e.g. wechat,zhihu)")
    p.add_argument("--type", choices=["article", "graph_text", "video"], default=None, help="Target content type for context")
    p.add_argument("--list", action="store_true", help="List platforms with rule files")

    p = sub.add_parser("upload", help="Upload image(s) available to this runtime to the 96Push pix store")
    p.add_argument("--file", action="append", required=True, help="Image path available to this runtime; repeat for multiple images")
    p.add_argument("--timeout", type=int, default=120, help="Upload timeout in seconds")
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")

    # Content creation
    p = sub.add_parser("create", help="Create content")
    p.add_argument("--type", choices=["article", "graph_text", "video"], default=None, help="Content type. If omitted, inferred from --files")
    p.add_argument("--title", required=True)
    p.add_argument("--desc", default="", help="Description/summary")
    p.add_argument("--content", default="", help="HTML content (for article)")
    p.add_argument("--markdown", default="", help="Markdown source (for article)")
    p.add_argument("--files", default="", help='JSON array of public HTTP(S) URLs (images for graph_text, video URL for video)')
    p.add_argument("--thumb", default="", help='JSON array of cover image public HTTP(S) URLs')
    p.add_argument("--no-auto-thumb", action="store_true", help="Disable auto cover extraction from content")

    p = sub.add_parser("update", help="Update existing content")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--type", choices=["article", "graph_text", "video"], default=None, help="Content type. If omitted, inferred from existing content/files")
    p.add_argument("--title", required=True)
    p.add_argument("--desc", default="")
    p.add_argument("--content", default="")
    p.add_argument("--markdown", default="")
    p.add_argument("--files", default="")
    p.add_argument("--thumb", default="")
    p.add_argument("--no-auto-thumb", action="store_true")
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")

    p = sub.add_parser("delete-article", help="Delete content")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")

    # Publish
    p = sub.add_parser("publish", help="Submit async publish task")
    p.add_argument("--type", choices=["article", "graph_text", "video"], default=None, help="Content type. If omitted, inferred from content detail")
    p.add_argument("--id", type=int, required=True, help="Content ID to publish")
    p.add_argument("--accounts", default="", help="Simple mode: comma-separated account IDs (no settings)")
    p.add_argument("--accounts-json", default="", help='Advanced: JSON array of {"id":N,"platName":"...","settings":{...}}')
    p.add_argument("--draft", action="store_true", help="Save as draft only (syncDraft)")
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")
    p.add_argument("--confirm-multi-account", action="store_true", help="Required when publishing to more than one account")
    p.add_argument("--force", action="store_true", help="Skip active-publish check (dangerous, can create duplicates)")
    p.add_argument("--no-wait", action="store_true", help="Return immediately without polling for result")
    p.add_argument("--show-rules", action="store_true", help="Print full platform rule files to stderr before publishing")

    p = sub.add_parser("poll", help="Poll publish result")
    p.add_argument("--id", type=int, required=True, help="publishRecordId")
    p.add_argument("--max", type=int, default=40, help="Max poll attempts (default 40 × 5s = 200s)")
    p.add_argument("--interval", type=int, default=5, help="Seconds between polls")

    sub.add_parser("queue", help="Show current publish queue")

    p = sub.add_parser("cancel-queue", help="Cancel a queued publish task")
    p.add_argument("--id", type=int, required=True, help="publishRecordId to cancel")
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")

    # Platform setting management
    p = sub.add_parser("create-plat-set", help="Create a platform publish config")
    p.add_argument("--pid", type=int, required=True, help="Platform ID")
    p.add_argument("--name", required=True, help="Config name")
    p.add_argument("--description", default="")
    p.add_argument("--setting", required=True, help="JSON object of platform settings")
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")

    p = sub.add_parser("update-plat-set", help="Update a platform publish config")
    p.add_argument("--sid", type=int, required=True, help="Setting ID")
    p.add_argument("--pid", type=int, required=True, help="Platform ID")
    p.add_argument("--name", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--setting", required=True, help="JSON object of platform settings")
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")

    p = sub.add_parser("delete-plat-set", help="Delete a platform publish config")
    p.add_argument("--sid", type=int, required=True, help="Setting ID")
    p.add_argument("--confirm", action="store_true", help="Required after explicit user approval")

    args = parser.parse_args()

    handlers = {
        "check": cmd_check,
        "platforms": cmd_platforms,
        "accounts": cmd_accounts,
        "all-accounts": cmd_all_accounts,
        "articles": cmd_articles,
        "article": cmd_article,
        "create": cmd_create,
        "update": cmd_update,
        "delete-article": cmd_delete_article,
        "publish": cmd_publish,
        "poll": cmd_poll,
        "queue": cmd_queue,
        "cancel-queue": cmd_cancel_queue,
        "records": cmd_records,
        "record": cmd_record,
        "dashboard": cmd_dashboard,
        "overview": cmd_overview,
        "user": cmd_user,
        "plat-sets": cmd_plat_sets,
        "rules": cmd_rules,
        "upload": cmd_upload,
        "create-plat-set": cmd_create_plat_set,
        "update-plat-set": cmd_update_plat_set,
        "delete-plat-set": cmd_delete_plat_set,
    }

    result = handlers[args.command](args)
    if isinstance(result, PlainOutput):
        print(result)
    else:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        print()


if __name__ == "__main__":
    main()
