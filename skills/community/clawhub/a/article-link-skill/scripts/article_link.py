"""
OpenClaw article-link skill runtime — 文章链接提取工具.

五个核心能力:
  1. media         — 查看支持的媒体来源列表
  2. submit        — 提交文章链接进行提取
  3. status        — 查询任务状态
  4. jobs          — 查看近期任务列表
  5. article       — 获取已匹配文章的英文全文

所有操作 (除 media) 需要 Import Token 鉴权, 且有每日次数限制:
  - 基础模式: 50 次/天
  - 深度解析: 5 次/天

This module is intentionally self-contained:
- No third-party dependencies (uses only urllib).
- No hard-coded credentials.
"""

import argparse
import json
import os
import ssl
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import error as urllib_error
from urllib import request as urllib_request

# ─────────────────────── 配置 ───────────────────────


def _load_config() -> Dict[str, Any]:
    """从 skill 目录（scripts 的上一级）加载 config.json."""
    config_path = Path(__file__).parent.parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                data = json.load(f)
            return {k: v for k, v in data.items() if not k.startswith("_")}
        except (json.JSONDecodeError, OSError):
            pass
    return {}


_CONFIG = _load_config()

API_BASE = os.environ.get("API_BASE") or _CONFIG.get("api_base") or "https://pick-read.vip/api"
IMPORT_TOKEN = os.environ.get("IMPORT_TOKEN") or _CONFIG.get("import_token") or ""
TIMEOUT_SECONDS = 30

# ─────────────────────── HTTP 层 ───────────────────────


def _build_ssl_contexts() -> List[ssl.SSLContext]:
    """构建多个 SSL 上下文, 按宽松度递增排列."""
    ctxs: List[ssl.SSLContext] = []
    try:
        c1 = ssl.create_default_context()
        c1.check_hostname = False
        c1.verify_mode = ssl.CERT_NONE
        ctxs.append(c1)
    except Exception:
        pass
    try:
        c2 = ssl._create_unverified_context()  # noqa: SLF001
        ctxs.append(c2)
    except Exception:
        pass
    if not ctxs:
        ctxs.append(ssl.create_default_context())
    return ctxs


_SSL_CONTEXTS = _build_ssl_contexts()
_MAX_RETRIES = 2


def _http_request(
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """对 API 发起请求并返回解析后的 JSON.

    支持 GET / POST, 自动带 Import Token.
    """
    url = f"{API_BASE.rstrip('/')}{path}"
    effective_token = token or IMPORT_TOKEN

    if params:
        qs = "&".join(
            f"{k}={urllib_request.quote(str(v))}"
            for k, v in params.items()
            if v is not None
        )
        if qs:
            url = f"{url}?{qs}"

    headers: Dict[str, str] = {
        "Accept": "application/json",
        "User-Agent": "SkillBot/2.0 ArticleLink",
        "Connection": "close",
    }
    if effective_token:
        headers["X-Import-Token"] = effective_token

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib_request.Request(url, method=method.upper(), headers=headers, data=data)
    last_exc: Optional[Exception] = None

    for ctx in _SSL_CONTEXTS:
        opener = urllib_request.build_opener(
            urllib_request.ProxyHandler({}),
            urllib_request.HTTPSHandler(context=ctx),
        )
        for attempt in range(_MAX_RETRIES):
            try:
                with opener.open(req, timeout=TIMEOUT_SECONDS) as resp:
                    raw = resp.read().decode("utf-8", errors="replace")
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"API {path} returned invalid JSON") from exc
                return parsed if isinstance(parsed, dict) else {"data": parsed}
            except urllib_error.HTTPError as exc:
                err_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
                error_detail = err_body[:500]
                try:
                    err_json = json.loads(err_body)
                    if isinstance(err_json.get("detail"), str):
                        error_detail = err_json["detail"]
                    elif isinstance(err_json.get("detail"), dict):
                        error_detail = err_json["detail"].get("message", error_detail)
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass
                raise RuntimeError(f"API {path} {exc.code}: {error_detail}") from exc
            except (urllib_error.URLError, ssl.SSLError, OSError, EOFError) as exc:
                last_exc = exc
                continue

    reason = str(last_exc) if last_exc else "unknown network error"
    raise RuntimeError(
        f"API {path} failed after trying {len(_SSL_CONTEXTS)} SSL strategies: {reason}. "
        f"请检查网络连接或 Python/OpenSSL 版本（建议 Python>=3.8, OpenSSL>=1.1.1）。"
    )


def _http_get(path: str, params: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> Dict[str, Any]:
    return _http_request("GET", path, params=params, token=token)


def _http_post(path: str, body: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> Dict[str, Any]:
    return _http_request("POST", path, body=body, token=token)


# ─────────────────────── 五个核心能力 ───────────────────────


def list_media() -> Dict[str, Any]:
    """能力 1: 查看支持的媒体来源列表 (无需 token)."""
    result = _http_get("/skill/article-submit/media")
    media = result.get("media", [])
    return {
        "type": "media_list",
        "total": len(media),
        "media": media,
    }


def get_quota(token: Optional[str] = None) -> Dict[str, Any]:
    """查询今日配额."""
    result = _http_get("/skill/article-submit/quota", token=token)
    return {
        "type": "quota",
        "basic_used": result.get("basic_used", 0),
        "basic_limit": result.get("basic_limit", 50),
        "deep_used": result.get("deep_used", 0),
        "deep_limit": result.get("deep_limit", 5),
    }


def get_article(article_id: str, token: Optional[str] = None) -> Dict[str, Any]:
    """能力 5: 获取已匹配文章的英文全文."""
    result = _http_get(f"/skill/article-submit/articles/{article_id}", token=token)
    return {
        "type": "article_content",
        "id": result.get("id"),
        "source_media": result.get("source_media"),
        "title": result.get("title_en"),
        "content_html": result.get("content_html"),
        "origin_url": result.get("origin_url"),
        "original_publish_time": result.get("original_publish_time"),
    }


def submit_link(
    url: str,
    deep: bool = False,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """能力 2: 提交文章链接.

    当 status=matched 时, 自动追加一次 article 请求, 直接返回英文全文.
    """
    result = _http_post(
        "/skill/article-submit/jobs",
        body={"url": url, "deep_parse": deep},
        token=token,
    )
    status = result.get("status")
    matched_id = result.get("matched_article_id")

    if status == "matched" and matched_id:
        try:
            article = get_article(matched_id, token=token)
            return {
                "type": "submit_matched",
                "job_id": result.get("id"),
                "origin_url": result.get("origin_url"),
                "source_media": result.get("source_media"),
                "mode": result.get("mode"),
                "status": "matched",
                "matched_article_id": matched_id,
                "title": article.get("title"),
                "content_html": article.get("content_html"),
                "original_publish_time": article.get("original_publish_time"),
                "next_action": "done — 将 title + content_html 英文全文展示给用户",
            }
        except RuntimeError:
            pass

    return {
        "type": "submit_pending",
        "job_id": result.get("id"),
        "origin_url": result.get("origin_url"),
        "source_media": result.get("source_media"),
        "mode": result.get("mode"),
        "status": status,
        "next_action": "poll — 用 status \"{}\" 轮询任务状态".format(result.get("id")),
    }


def check_status(job_id: str, token: Optional[str] = None) -> Dict[str, Any]:
    """能力 3: 查询任务状态.

    当 status=ready 且有 matched_article_id 时, 自动获取英文全文.
    """
    result = _http_get(f"/skill/article-submit/jobs/{job_id}", token=token)
    status = result.get("status")
    matched_id = result.get("matched_article_id")
    error_msg = result.get("error_message")

    if status in ("matched", "ready") and matched_id:
        try:
            article = get_article(matched_id, token=token)
            return {
                "type": "job_ready",
                "job_id": result.get("id"),
                "status": status,
                "matched_article_id": matched_id,
                "title": article.get("title"),
                "content_html": article.get("content_html"),
                "original_publish_time": article.get("original_publish_time"),
                "next_action": "done — 将 title + content_html 英文全文展示给用户",
            }
        except RuntimeError:
            pass

    if status == "failed":
        return {
            "type": "job_failed",
            "job_id": result.get("id"),
            "status": "failed",
            "error_message": error_msg,
            "next_action": "done — 告知用户提取失败",
        }

    return {
        "type": "job_status",
        "job_id": result.get("id"),
        "status": status,
        "next_action": "poll — 等待几秒后再次查询 status \"{}\" ".format(result.get("id")),
    }


def list_jobs(
    page: int = 1,
    page_size: int = 20,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """能力 4: 查看近期任务列表."""
    result = _http_get(
        "/skill/article-submit/jobs",
        params={"page": page, "page_size": page_size},
        token=token,
    )
    return {
        "type": "job_list",
        "total": result.get("total", 0),
        "jobs": result.get("jobs", []),
    }


# ─────────────────────── CLI ───────────────────────


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="文章链接提取工具 — 五个核心能力: media / submit / status / jobs / article",
    )
    subparsers = parser.add_subparsers(dest="command")

    # media
    subparsers.add_parser("media", help="查看支持的媒体来源列表")

    # quota
    q = subparsers.add_parser("quota", help="查看今日配额使用情况")
    q.add_argument("--token", help="Import Token")

    # submit
    sub = subparsers.add_parser("submit", help="提交文章链接进行提取")
    sub.add_argument("url", help="文章 URL")
    sub.add_argument("--deep", action="store_true", help="深度解析模式 (跳过已有匹配)")
    sub.add_argument("--yes", action="store_true", help="确认执行深度解析 (跳过确认提示)")
    sub.add_argument("--token", help="Import Token")

    # status
    st = subparsers.add_parser("status", help="查询任务状态")
    st.add_argument("job_id", help="任务 ID")
    st.add_argument("--token", help="Import Token")

    # jobs
    jo = subparsers.add_parser("jobs", help="查看近期任务列表")
    jo.add_argument("--page", type=int, default=1, help="页码 (默认 1)")
    jo.add_argument("--page-size", type=int, default=20, help="每页条数 (默认 20)")
    jo.add_argument("--token", help="Import Token")

    # article
    ar = subparsers.add_parser("article", help="获取已匹配文章的英文全文")
    ar.add_argument("article_id", help="文章 ID (来自 submit 返回的 matched_article_id)")
    ar.add_argument("--token", help="Import Token")

    return parser


def run_cli() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    command = args.command
    if command is None:
        parser.print_help()
        raise SystemExit(1)

    try:
        if command == "media":
            result = list_media()
        elif command == "quota":
            result = get_quota(token=args.token)
        elif command == "submit":
            if args.deep and not args.yes:
                quota = get_quota(token=args.token)
                result = {
                    "type": "deep_confirm_required",
                    "message": "深度解析每日仅 {limit} 次，今日已用 {used} 次，剩余 {remain} 次。请确认后使用 --yes 执行。".format(
                        limit=quota["deep_limit"],
                        used=quota["deep_used"],
                        remain=quota["deep_limit"] - quota["deep_used"],
                    ),
                    "deep_used": quota["deep_used"],
                    "deep_limit": quota["deep_limit"],
                    "deep_remaining": quota["deep_limit"] - quota["deep_used"],
                    "confirm_command": f'submit "{args.url}" --deep --yes',
                }
            else:
                result = submit_link(url=args.url, deep=args.deep, token=args.token)
        elif command == "status":
            result = check_status(job_id=args.job_id, token=args.token)
        elif command == "jobs":
            result = list_jobs(page=args.page, page_size=args.page_size, token=args.token)
        elif command == "article":
            result = get_article(article_id=args.article_id, token=args.token)
        else:
            parser.print_help()
            raise SystemExit(1)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_cli()
