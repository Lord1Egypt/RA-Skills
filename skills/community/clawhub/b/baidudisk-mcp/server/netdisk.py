#!/usr/bin/env python3
"""
Baidu Netdisk MCP Server (stdio)

2.0 tools（官方同名 + 历史别名）：
- 官方同名：
  - file_list
  - file_doc_list
  - file_image_list
  - file_video_list_api
  - file_video_list
  - category_info
  - category_info_multi
  - image_gettags
  - image_gettags_summary
  - image_search
  - recent_list
  - file_meta
  - make_dir
  - file_copy
  - file_copy_batch
  - file_del
  - file_move
  - file_move_batch
  - file_rename
  - file_rename_batch
  - file_upload_stdio
  - file_upload_by_url
  - file_upload_by_text
  - file_keyword_search
  - file_semantics_search
  - file_sharelink_set
  - user_info
  - get_quota
- 历史别名（兼容）：
  - list, search, mkdir, move, rename, delete, upload, download

Credential strategy (hot-reload friendly):
- Read BAIDU_NETDISK_TOKEN_FILE JSON on EVERY tool call.
- If BAIDU_NETDISK_TOKEN_FILE is not set, fallback to
  ~/.openclaw/credentials/baidudisk.json when present.
- Fallback to BAIDU_NETDISK_ACCESS_TOKEN / BAIDU_NETDISK_DEFAULT_DIR env vars.
"""

from __future__ import annotations

import builtins
import hashlib
import io
import ipaddress
import json
import os
import random
import re
import socket
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from mcp.server.fastmcp import FastMCP

import openapi_client
from openapi_client.api import (
    fileinfo_api,
    filemanager_api,
    fileupload_api,
    multimediafile_api,
    userinfo_api,
)

mcp = FastMCP("baidu-netdisk-stdio")

# Upload tuning
CHUNK_SIZE = 4 * 1024 * 1024
MAX_RETRIES = 3
RETRY_BACKOFF = 2

# Readonly HTTP retry tuning（urllib 直连）
READONLY_HTTP_MAX_ATTEMPTS = 3
READONLY_HTTP_BACKOFF_BASE_S = 0.5
READONLY_HTTP_BACKOFF_JITTER_S = 0.5
RATE_LIMIT_HTTP_STATUS_CODES = {429}
RATE_LIMIT_ERRNOS = {31034}

# Credentials
TOKEN_FILE_ENV = "BAIDU_NETDISK_TOKEN_FILE"
DEFAULT_TOKEN_FILE_FALLBACK = "~/.openclaw/credentials/baidudisk.json"
ACCESS_TOKEN_ENV = "BAIDU_NETDISK_ACCESS_TOKEN"
DEFAULT_DIR_ENV = "BAIDU_NETDISK_DEFAULT_DIR"

DELETE_CONFIRM_WORD = "DELETE"

# P2 limits
UPLOAD_BY_TEXT_MAX_CHARS = 200_000
UPLOAD_BY_TEXT_MAX_BYTES = 2 * 1024 * 1024
UPLOAD_BY_URL_MAX_BYTES = 200 * 1024 * 1024
UPLOAD_BY_URL_MAX_TIMEOUT_S = 300
UPLOAD_BY_URL_MAX_REDIRECTS = 3

CATEGORY_INFO_ENDPOINT = "https://pan.baidu.com/api/categoryinfo"
IMAGEPROC_ENDPOINT = "https://pan.baidu.com/rest/2.0/xpan/imageproc"
IMAGE_GETTAGS_ENDPOINT = IMAGEPROC_ENDPOINT
MULTIMEDIA_ENDPOINT = "https://pan.baidu.com/rest/2.0/xpan/multimedia"
XPAN_FILE_ENDPOINT = "https://pan.baidu.com/rest/2.0/xpan/file"
READONLY_HTTP_USER_AGENT = "pan.baidu.com"
CATEGORY_RANGE = (1, 7)

VIDEO_EXTENSIONS = {
    "mp4",
    "mkv",
    "mov",
    "avi",
    "flv",
    "wmv",
    "m4v",
    "rm",
    "rmvb",
    "ts",
    "mpeg",
    "mpg",
    "3gp",
    "webm",
}

BATCH_MIN_CHUNK_SIZE = 10
BATCH_DEFAULT_ALLOW_DEST_PREFIXES = ("/Openclaw",)
BATCH_ALLOWED_ONDUP = {"fail", "newcopy", "overwrite", "skip"}
# 不可重试：参数/路径/权限/token 等 fail-fast 场景
BATCH_FAILFAST_ERRNOS = {
    -30,
    -12,
    -10,
    -9,
    -8,
    -7,
    -6,
    2,
    3,
    10,
    111,
    31066,
    31079,
    31326,
}
BATCH_FAILFAST_HINTS = (
    "参数",
    "param",
    "invalid",
    "illegal",
    "permission",
    "权限",
    "denied",
    "auth",
    "token",
    "expired",
    "access denied",
    "鉴权",
    "未登录",
)


@dataclass
class RuntimeCredential:
    access_token: str
    default_dir: str
    default_device_id: Optional[str] = None
    token_file: Optional[str] = None


class CredentialError(RuntimeError):
    pass


def _sanitize_message(message: str, token: str = "") -> str:
    if not message:
        return message

    masked = message
    if token:
        masked = masked.replace(token, "***")

    # Mask URL query tokens: access_token=xxxx
    masked = re.sub(r"(access_token=)[^&\s]+", r"\1***", masked)
    # Mask JSON token fields
    masked = re.sub(r'("access_token"\s*:\s*")[^"]+(")', r"\1***\2", masked)
    return masked


def _coerce_int_or_none(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _coerce_positive_float_or_none(value: Any) -> Optional[float]:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if parsed <= 0:
        return None
    return parsed


def _is_rate_limit_errno(errno: Any) -> bool:
    errno_int = _coerce_int_or_none(errno)
    return errno_int in RATE_LIMIT_ERRNOS if errno_int is not None else False


def _calc_backoff_with_jitter(attempt_index: int) -> float:
    base = READONLY_HTTP_BACKOFF_BASE_S * (2**max(0, int(attempt_index)))
    jitter = random.uniform(0, READONLY_HTTP_BACKOFF_JITTER_S)
    return round(base + jitter, 3)


def _extract_suggested_backoff_s(resp: Optional[Dict[str, Any]], attempt_index: int = 0) -> float:
    if isinstance(resp, dict):
        for key in (
            "suggested_backoff_s",
            "retry_after",
            "retry_after_s",
            "backoff",
            "backoff_s",
        ):
            hinted = _coerce_positive_float_or_none(resp.get(key))
            if hinted is not None:
                return hinted
    return _calc_backoff_with_jitter(attempt_index)


def _error(
    message: str,
    token: str = "",
    retryable: Optional[bool] = None,
    suggested_backoff_s: Optional[Union[int, float]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "status": "error",
        "message": _sanitize_message(message, token),
    }
    if retryable is not None:
        payload["retryable"] = bool(retryable)
    if suggested_backoff_s is not None:
        payload["suggested_backoff_s"] = float(suggested_backoff_s)
    return payload


def _unsupported(message: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "status": "unsupported",
        "message": message,
    }
    if extra:
        payload.update(extra)
    return payload


def _todo(message: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "status": "todo",
        "message": message,
    }
    if extra:
        payload.update(extra)
    return payload


def _success(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = {"status": "success"}
    data.update(payload)
    return data


def _expand_path(path: str) -> str:
    return os.path.abspath(os.path.expandvars(os.path.expanduser(path)))


def _reject_parent_dir_segments(path: str, field_name: str = "path") -> None:
    normalized = str(path).replace("\\", "/")
    if any(segment == ".." for segment in normalized.split("/")):
        raise ValueError(f"{field_name} 不允许包含 '..' 路径段")


def _normalize_dir(path: Optional[str]) -> str:
    if not path:
        return "/"

    p = str(path).strip()
    if not p:
        return "/"

    if not p.startswith("/"):
        p = "/" + p

    p = re.sub(r"/{2,}", "/", p)
    _reject_parent_dir_segments(p)

    if len(p) > 1 and p.endswith("/"):
        p = p[:-1]
    return p


def _join_path(base_dir: str, child: str) -> str:
    if not child:
        return _normalize_dir(base_dir)
    if child.startswith("/"):
        return _normalize_dir(child)
    return _normalize_dir(f"{_normalize_dir(base_dir).rstrip('/')}/{child.lstrip('/')}")


def _load_runtime_credential() -> RuntimeCredential:
    token_file_raw = os.getenv(TOKEN_FILE_ENV, "").strip()
    env_access_token = os.getenv(ACCESS_TOKEN_ENV, "").strip()
    env_default_dir = os.getenv(DEFAULT_DIR_ENV, "").strip()

    if not token_file_raw:
        fallback_token_file = _expand_path(DEFAULT_TOKEN_FILE_FALLBACK)
        if os.path.exists(fallback_token_file):
            token_file_raw = fallback_token_file

    file_data: Dict[str, Any] = {}
    token_file: Optional[str] = None

    if token_file_raw:
        token_file = _expand_path(token_file_raw)
        if not os.path.exists(token_file):
            raise CredentialError(
                f"token 文件不存在: {token_file}. "
                f"请设置 {TOKEN_FILE_ENV} 或 {ACCESS_TOKEN_ENV}。"
            )
        try:
            with open(token_file, "r", encoding="utf-8") as f:
                file_data = json.load(f)
            if not isinstance(file_data, dict):
                raise CredentialError(f"token 文件格式错误（必须是 JSON 对象）: {token_file}")
        except json.JSONDecodeError as exc:
            raise CredentialError(f"token 文件 JSON 解析失败: {token_file}, {exc}") from exc
        except OSError as exc:
            raise CredentialError(f"读取 token 文件失败: {token_file}, {exc}") from exc

    access_token = str(file_data.get("access_token", "") or "").strip()
    if not access_token:
        access_token = env_access_token

    if not access_token:
        raise CredentialError(
            "未找到 access_token。请在 token 文件中写入 access_token，"
            f"或设置环境变量 {ACCESS_TOKEN_ENV}。"
        )

    default_dir = str(file_data.get("default_dir", "") or "").strip()
    if not default_dir:
        default_dir = env_default_dir or "/"

    default_device_id = str(file_data.get("default_device_id", "") or "").strip() or None

    return RuntimeCredential(
        access_token=access_token,
        default_dir=_normalize_dir(default_dir),
        default_device_id=default_device_id,
        token_file=token_file,
    )


def _new_configuration() -> openapi_client.Configuration:
    cfg = openapi_client.Configuration()
    cfg.connection_pool_maxsize = 10
    cfg.retries = MAX_RETRIES
    cfg.socket_options = None
    return cfg


def _check_api_errno(resp: Dict[str, Any], token: str = "") -> Optional[Dict[str, Any]]:
    if not isinstance(resp, dict):
        return _error("API 响应格式异常（非 JSON 对象）", token, retryable=False)

    errno = resp.get("errno", 0)
    if errno in (0, "0", None):
        return None

    errmsg = resp.get("errmsg")
    if errmsg is None:
        errmsg = resp.get("error_msg")
    if errmsg is None:
        errmsg = resp.get("msg")

    detail = f", errmsg={errmsg}" if errmsg not in (None, "") else ""
    errno_int = _coerce_int_or_none(errno)
    retryable = bool(
        _is_rate_limit_errno(errno)
        or (errno_int is not None and errno_int in RATE_LIMIT_HTTP_STATUS_CODES)
    )
    suggested_backoff_s = _extract_suggested_backoff_s(resp, attempt_index=0) if retryable else None

    return _error(
        f"百度网盘 API 返回错误 errno={errno}{detail}",
        token,
        retryable=retryable,
        suggested_backoff_s=suggested_backoff_s,
    )


def _format_entry(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": item.get("server_filename") or item.get("filename"),
        "path": item.get("path"),
        "isdir": bool(item.get("isdir", 0)),
        "size": item.get("size"),
        "fs_id": item.get("fs_id"),
        "md5": item.get("md5"),
        "server_mtime": item.get("server_mtime"),
        "local_mtime": item.get("local_mtime"),
        "category": item.get("category"),
    }


def _normalize_imagelist_item(item: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(item)

    if not normalized.get("server_filename"):
        normalized["server_filename"] = (
            normalized.get("filename")
            or normalized.get("name")
            or normalized.get("title")
        )

    if not normalized.get("path"):
        normalized["path"] = normalized.get("server_path") or normalized.get("file_path")

    if normalized.get("server_mtime") is None:
        normalized["server_mtime"] = normalized.get("mtime") or normalized.get("time")

    if normalized.get("local_mtime") is None:
        normalized["local_mtime"] = normalized.get("local_ctime")

    if normalized.get("fs_id") is None:
        normalized["fs_id"] = normalized.get("fsid")

    return normalized


def _resolve_dir(path: Optional[str], cred: RuntimeCredential) -> str:
    if not path:
        return cred.default_dir
    return _join_path(cred.default_dir, path)


def _resolve_path(path: str, cred: RuntimeCredential, parent_dir: Optional[str] = None) -> str:
    p = (path or "").strip()
    if not p:
        raise ValueError("path 不能为空")
    base = _resolve_dir(parent_dir, cred) if parent_dir else cred.default_dir
    return _join_path(base, p)


def _upload_small_file(
    local_file_path: str,
    remote_path: str,
    file_size: int,
    access_token: str,
    configuration: openapi_client.Configuration,
) -> Dict[str, Any]:
    with open(local_file_path, "rb") as f:
        file_content = f.read()

    file_md5 = hashlib.md5(file_content).hexdigest()
    block_list = f'["{file_md5}"]'

    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = fileupload_api.FileuploadApi(api_client)

        try:
            precreate_response = api_instance.xpanfileprecreate(
                access_token=access_token,
                path=remote_path,
                isdir=0,
                size=file_size,
                autoinit=1,
                block_list=block_list,
                rtype=3,
            )
            err = _check_api_errno(precreate_response, access_token)
            if err:
                return err
            uploadid = precreate_response.get("uploadid")
            if not uploadid:
                return _error(f"预创建成功但缺少 uploadid: {precreate_response}", access_token)
        except Exception as exc:
            return _error(f"预创建文件失败: {exc}", access_token)

        for attempt in range(MAX_RETRIES):
            try:
                with open(local_file_path, "rb") as f:
                    upload_response = api_instance.pcssuperfile2(
                        access_token=access_token,
                        partseq="0",
                        path=remote_path,
                        uploadid=uploadid,
                        type="tmpfile",
                        file=f,
                    )
                if not upload_response.get("md5"):
                    if attempt < MAX_RETRIES - 1:
                        sleep_time = RETRY_BACKOFF * (2**attempt) + random.uniform(0, 1)
                        time.sleep(sleep_time)
                        continue
                    return _error("文件上传失败：未返回分片 MD5", access_token)
                break
            except Exception as exc:
                if attempt < MAX_RETRIES - 1:
                    sleep_time = RETRY_BACKOFF * (2**attempt) + random.uniform(0, 1)
                    time.sleep(sleep_time)
                    continue
                return _error(f"文件上传失败: {exc}", access_token)

        try:
            create_response = api_instance.xpanfilecreate(
                access_token=access_token,
                path=remote_path,
                isdir=0,
                size=file_size,
                uploadid=uploadid,
                block_list=block_list,
                rtype=3,
            )
            err = _check_api_errno(create_response, access_token)
            if err:
                return err
            return _success(
                {
                    "message": "文件上传成功",
                    "remote_path": remote_path,
                    "filename": os.path.basename(remote_path),
                    "size": file_size,
                    "fs_id": create_response.get("fs_id"),
                }
            )
        except Exception as exc:
            return _error(f"创建文件失败: {exc}", access_token)


def _upload_large_file(
    local_file_path: str,
    remote_path: str,
    file_size: int,
    access_token: str,
    configuration: openapi_client.Configuration,
) -> Dict[str, Any]:
    chunk_count = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE
    md5_list = []

    with open(local_file_path, "rb") as f:
        for _ in range(chunk_count):
            chunk_data = f.read(CHUNK_SIZE)
            md5_list.append(hashlib.md5(chunk_data).hexdigest())

    block_list = json.dumps(md5_list)

    with openapi_client.ApiClient(configuration) as api_client:
        api_instance = fileupload_api.FileuploadApi(api_client)

        try:
            precreate_response = api_instance.xpanfileprecreate(
                access_token=access_token,
                path=remote_path,
                isdir=0,
                size=file_size,
                autoinit=1,
                block_list=block_list,
                rtype=3,
            )
            err = _check_api_errno(precreate_response, access_token)
            if err:
                return err
            uploadid = precreate_response.get("uploadid")
            if not uploadid:
                return _error(f"预创建成功但缺少 uploadid: {precreate_response}", access_token)
        except Exception as exc:
            return _error(f"预创建文件失败: {exc}", access_token)

        with open(local_file_path, "rb") as f:
            for idx in range(chunk_count):
                chunk_data = f.read(CHUNK_SIZE)
                for attempt in range(MAX_RETRIES):
                    try:
                        file_obj = io.BytesIO(chunk_data)
                        file_obj.name = os.path.basename(local_file_path)
                        upload_response = api_instance.pcssuperfile2(
                            access_token=access_token,
                            partseq=str(idx),
                            path=remote_path,
                            uploadid=uploadid,
                            type="tmpfile",
                            file=file_obj,
                        )
                        if not upload_response.get("md5"):
                            if attempt < MAX_RETRIES - 1:
                                sleep_time = RETRY_BACKOFF * (2**attempt) + random.uniform(0, 1)
                                time.sleep(sleep_time)
                                continue
                            return _error(f"分片 {idx} 上传失败：未返回 MD5", access_token)
                        break
                    except Exception as exc:
                        if attempt < MAX_RETRIES - 1:
                            sleep_time = RETRY_BACKOFF * (2**attempt) + random.uniform(0, 1)
                            time.sleep(sleep_time)
                            continue
                        return _error(f"分片 {idx} 上传失败: {exc}", access_token)

        try:
            create_response = api_instance.xpanfilecreate(
                access_token=access_token,
                path=remote_path,
                isdir=0,
                size=file_size,
                uploadid=uploadid,
                block_list=block_list,
                rtype=3,
            )
            err = _check_api_errno(create_response, access_token)
            if err:
                return err
            return _success(
                {
                    "message": "文件分片上传成功",
                    "remote_path": remote_path,
                    "filename": os.path.basename(remote_path),
                    "size": file_size,
                    "chunks": chunk_count,
                    "fs_id": create_response.get("fs_id"),
                }
            )
        except Exception as exc:
            return _error(f"创建文件失败: {exc}", access_token)


def _upload_local_file(
    local_file_path: str,
    remote_dir: Optional[str],
    remote_name: Optional[str],
    cred: RuntimeCredential,
) -> Dict[str, Any]:
    local_file = _expand_path(local_file_path)
    if not os.path.isfile(local_file):
        return _error(f"本地文件不存在: {local_file}")

    target_dir = _resolve_dir(remote_dir, cred)
    filename = (remote_name or "").strip() or os.path.basename(local_file)
    remote_path = _join_path(target_dir, filename)

    file_size = os.path.getsize(local_file)
    cfg = _new_configuration()

    if file_size <= CHUNK_SIZE:
        return _upload_small_file(local_file, remote_path, file_size, cred.access_token, cfg)
    return _upload_large_file(local_file, remote_path, file_size, cred.access_token, cfg)


def _normalize_int_bool(value: Union[int, str, bool]) -> int:
    return 1 if int(value) else 0


def _normalize_category(category: Union[int, str]) -> int:
    try:
        value = int(category)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"category 非法: {category}") from exc

    min_category, max_category = CATEGORY_RANGE
    if value < min_category or value > max_category:
        raise ValueError(f"category 仅支持 {min_category}..{max_category}")
    return value


def _normalize_categories(categories: Any) -> List[int]:
    parsed: Any = categories

    if isinstance(categories, str):
        raw = categories.strip()
        if not raw:
            raise ValueError("categories 不能为空")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("categories 必须是 JSON array 字符串") from exc

    if isinstance(parsed, bool):
        raise ValueError("categories 不能是布尔值")

    if isinstance(parsed, int):
        parsed = [parsed]

    if not isinstance(parsed, (builtins.list, tuple)):
        raise ValueError("categories 必须是数组")

    if not parsed:
        raise ValueError("categories 不能为空")

    normalized: List[int] = []
    seen = set()
    for item in parsed:
        category = _normalize_category(item)
        if category in seen:
            continue
        seen.add(category)
        normalized.append(category)
    return normalized


def _normalize_gettags_type(tag_type: Union[int, str]) -> int:
    try:
        value = int(tag_type)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"type 非法: {tag_type}") from exc

    if value not in (1, 2):
        raise ValueError("type 仅支持 1/2")
    return value


def _http_get_json(
    url: str,
    params: Dict[str, Any],
    token: str,
    timeout_s: int = 30,
    max_attempts: int = READONLY_HTTP_MAX_ATTEMPTS,
) -> Dict[str, Any]:
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    request_url = f"{url}?{query}" if query else url
    req = urllib.request.Request(
        request_url,
        headers={"User-Agent": READONLY_HTTP_USER_AGENT},
        method="GET",
    )

    total_attempts = max(1, int(max_attempts))

    for attempt_index in range(total_attempts):
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                payload_raw = resp.read()
        except urllib.error.HTTPError as exc:
            status_code = _coerce_int_or_none(exc.code)
            if status_code in RATE_LIMIT_HTTP_STATUS_CODES:
                retry_after = None
                if getattr(exc, "headers", None):
                    retry_after = exc.headers.get("Retry-After")

                if attempt_index < total_attempts - 1:
                    time.sleep(
                        _extract_suggested_backoff_s(
                            {"retry_after": retry_after},
                            attempt_index=attempt_index,
                        )
                    )
                    continue

                return {
                    "errno": status_code,
                    "errmsg": f"HTTP {status_code} Too Many Requests",
                    "retry_after": retry_after,
                }

            body = ""
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            raise RuntimeError(
                _sanitize_message(f"HTTP 请求失败(code={exc.code}): {body}", token)
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(_sanitize_message(f"HTTP 请求失败: {exc.reason}", token)) from exc
        except TimeoutError as exc:
            raise RuntimeError(
                _sanitize_message(f"HTTP 请求超时(timeout={timeout_s}s)", token)
            ) from exc

        try:
            data = json.loads(payload_raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(_sanitize_message(f"响应 JSON 解析失败: {exc}", token)) from exc

        if not isinstance(data, dict):
            raise RuntimeError(_sanitize_message("API 响应格式异常（非 JSON 对象）", token))

        if _is_rate_limit_errno(data.get("errno")):
            if attempt_index < total_attempts - 1:
                time.sleep(_extract_suggested_backoff_s(data, attempt_index=attempt_index))
                continue

            data = dict(data)
            data.setdefault("retryable", True)
            data.setdefault(
                "suggested_backoff_s",
                _extract_suggested_backoff_s(data, attempt_index=attempt_index),
            )

        # 避免上层误把 access_token 透出
        if "access_token" in data:
            data = dict(data)
            data["access_token"] = "***"

        return data

    raise RuntimeError(_sanitize_message("HTTP 请求失败: 达到最大重试次数", token))


def _extract_category_info_payload(
    resp: Dict[str, Any],
    category: int,
    parent_path: str,
    recursion: int,
) -> Dict[str, Any]:
    raw_info = resp.get("info")
    info_obj = raw_info if isinstance(raw_info, dict) else {}
    picked_info = info_obj
    category_key = str(category)

    # 兼容两种返回形态：
    # 1) info={count,size,total}
    # 2) info={"3": {count,size,total}, ...}
    if "count" not in info_obj:
        nested_obj = info_obj.get(category_key)
        if isinstance(nested_obj, dict):
            picked_info = nested_obj

    count = picked_info.get("count", resp.get("count"))
    size = picked_info.get("size", resp.get("size"))
    total = picked_info.get("total", resp.get("total"))
    if total is None:
        total = count

    if raw_info is None:
        raw_info = {
            k: v
            for k, v in resp.items()
            if k not in {"errno", "request_id"}
        }

    return {
        "category": category,
        "parent_path": parent_path,
        "recursion": recursion,
        "count": count,
        "size": size,
        "total": total,
        "raw_info": raw_info,
    }


def _format_image_tag_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tag_id": item.get("tag_id", item.get("tagid")),
        "tag_name": item.get("tag_name", item.get("tag")),
        "count": item.get("count"),
        "is_show": item.get("is_show"),
        "is_search": item.get("is_search"),
        "cover_fid": item.get("cover_fid"),
        "thumb": item.get("thumb"),
        "ctime": item.get("ctime"),
        "mtime": item.get("mtime"),
        "status": item.get("status"),
    }


def _normalize_search_type(search_type: Union[int, str]) -> int:
    try:
        value = int(search_type)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"search_type 非法: {search_type}") from exc

    if value not in (1, 2):
        raise ValueError("search_type 仅支持 1(tag_id) / 2(汉字)")
    return value


def _normalize_non_negative_int(value: Union[int, str], name: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} 非法: {value}") from exc

    if parsed < 0:
        raise ValueError(f"{name} 必须 >= 0")
    return parsed


def _normalize_positive_int(value: Union[int, str], name: str, max_value: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} 非法: {value}") from exc

    if parsed <= 0:
        raise ValueError(f"{name} 必须 > 0")
    return min(parsed, max_value)


def _normalize_on_off(value: Union[str, int, bool], name: str) -> str:
    if isinstance(value, bool):
        return "on" if value else "off"

    if isinstance(value, int):
        if value in (0, 1):
            return "on" if value else "off"
        raise ValueError(f"{name} 仅支持 on/off 或 0/1")

    text = str(value or "").strip().lower()
    if text in ("on", "off"):
        return text
    if text in ("1", "true", "yes"):
        return "on"
    if text in ("0", "false", "no"):
        return "off"
    raise ValueError(f"{name} 仅支持 on/off 或 0/1")


def _normalize_optional_csv(value: Optional[Union[str, Sequence[Any]]], name: str) -> Optional[str]:
    if value is None:
        return None

    parts: List[str] = []
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return None
        parts = [part.strip() for part in raw.split(",") if part.strip()]
    elif isinstance(value, (builtins.list, tuple)):
        parts = [str(part).strip() for part in value if str(part).strip()]
    else:
        raise ValueError(f"{name} 必须是逗号分隔字符串")

    if not parts:
        raise ValueError(f"{name} 不能为空")
    return ",".join(parts)


def _normalize_optional_int(value: Optional[Union[int, str]], name: str) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None

    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} 非法: {value}") from exc

    if parsed < 0:
        raise ValueError(f"{name} 必须 >= 0")
    return parsed


def _normalize_optional_text(value: Optional[Union[str, int]], name: str) -> Optional[str]:
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None
    return text


def _as_bool_flag(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, ""):
        return False
    try:
        return int(value) != 0
    except (TypeError, ValueError):
        return bool(value)


def _format_image_search_item(item: Dict[str, Any]) -> Dict[str, Any]:
    thumb = item.get("thumb")
    if thumb is None:
        thumb = item.get("thumbnail")
    if thumb is None:
        thumb = item.get("thumbnails")
    if thumb is None:
        thumb = item.get("thumbs")

    return {
        "category": item.get("category"),
        "fs_id": item.get("fs_id"),
        "path": item.get("path"),
        "parent_path": item.get("parent_path"),
        "date_taken": item.get("date_taken"),
        "year": item.get("year"),
        "month": item.get("month"),
        "day": item.get("day"),
        "md5": item.get("md5"),
        "size": item.get("size"),
        "server_ctime": item.get("server_ctime"),
        "server_mtime": item.get("server_mtime"),
        "server_filename": item.get("server_filename"),
        "resolution": item.get("resolution"),
        "orientation": item.get("orientation"),
        "thumb": thumb,
    }


def _is_video_item(item: Dict[str, Any]) -> bool:
    category = item.get("category")
    if str(category) == "1":
        return True

    name = item.get("server_filename") or item.get("filename") or ""
    ext = os.path.splitext(str(name).lower())[1].lstrip(".")
    return ext in VIDEO_EXTENSIONS


def _normalize_fsids(fsids: Any) -> List[int]:
    def _to_int(v: Any) -> int:
        if isinstance(v, bool):
            raise ValueError("fsid 不能是布尔值")
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            s = v.strip()
            if not s:
                raise ValueError("fsid 不能为空字符串")
            return int(s)
        raise ValueError(f"不支持的 fsid 类型: {type(v).__name__}")

    if isinstance(fsids, (builtins.list, tuple)):
        if not fsids:
            raise ValueError("fsids 列表不能为空")
        return [_to_int(v) for v in fsids]

    if isinstance(fsids, bool):
        raise ValueError("fsids 不能是布尔值")

    if isinstance(fsids, int):
        return [fsids]

    if isinstance(fsids, str):
        s = fsids.strip()
        if not s:
            raise ValueError("fsids 不能为空")

        if s.startswith("["):
            parsed = json.loads(s)
            if not isinstance(parsed, builtins.list):
                raise ValueError("fsids JSON 字符串必须是数组")
            if not parsed:
                raise ValueError("fsids JSON 数组不能为空")
            return [_to_int(v) for v in parsed]

        if "," in s:
            parts = [part.strip() for part in s.split(",") if part.strip()]
            if not parts:
                raise ValueError("fsids 逗号分隔字符串不能为空")
            return [_to_int(v) for v in parts]

        return [_to_int(s)]

    raise ValueError(f"不支持的 fsids 类型: {type(fsids).__name__}")


def _is_forbidden_ip(ip: ipaddress._BaseAddress) -> bool:
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def _validate_public_http_url(url: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("仅支持 http(s) URL")

    if not parsed.hostname:
        raise ValueError("URL 缺少 hostname")

    host = parsed.hostname.strip().lower()
    if host == "localhost" or host.endswith(".localhost"):
        raise ValueError("禁止访问 localhost 地址")

    resolved_ips: List[ipaddress._BaseAddress] = []

    try:
        resolved_ips.append(ipaddress.ip_address(host))
    except ValueError:
        try:
            infos = socket.getaddrinfo(host, parsed.port or 80, type=socket.SOCK_STREAM)
        except socket.gaierror as exc:
            raise ValueError(f"域名解析失败: {host}, {exc}") from exc

        seen = set()
        for info in infos:
            ip_str = info[4][0]
            if ip_str in seen:
                continue
            seen.add(ip_str)
            resolved_ips.append(ipaddress.ip_address(ip_str))

    for ip in resolved_ips:
        if _is_forbidden_ip(ip):
            raise ValueError(f"禁止访问内网或保留地址: {host} -> {ip}")

    return parsed


def _guess_filename_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = os.path.basename(path)
    return name or f"url-upload-{int(time.time())}.bin"


def _download_url_to_temp_file(
    url: str,
    timeout_s: int,
    max_bytes: int,
) -> Dict[str, Any]:
    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(_NoRedirect)
    current_url = url
    tmp_path = ""

    try:
        for _ in range(UPLOAD_BY_URL_MAX_REDIRECTS + 1):
            _validate_public_http_url(current_url)
            req = urllib.request.Request(
                current_url,
                headers={"User-Agent": "openclaw-baidudisk-mcp/2.0"},
                method="GET",
            )

            try:
                with opener.open(req, timeout=timeout_s) as resp:
                    status = getattr(resp, "status", resp.getcode())
                    if status and 300 <= status < 400:
                        location = resp.headers.get("Location")
                        if not location:
                            raise ValueError(f"URL 重定向缺少 Location（status={status}）")
                        current_url = urllib.parse.urljoin(current_url, location)
                        continue

                    if status and status >= 400:
                        raise ValueError(f"下载失败，HTTP 状态码: {status}")

                    content_length = resp.headers.get("Content-Length")
                    if content_length:
                        try:
                            if int(content_length) > max_bytes:
                                raise ValueError(
                                    f"下载内容过大，Content-Length={content_length} 超出限制 {max_bytes}"
                                )
                        except ValueError as exc:
                            # int 解析失败也统一走实际流式限制
                            if "超出限制" in str(exc):
                                raise

                    suffix = os.path.splitext(_guess_filename_from_url(current_url))[1]
                    with tempfile.NamedTemporaryFile(
                        prefix="baidudisk_url_", suffix=suffix, delete=False
                    ) as tmp_file:
                        tmp_path = tmp_file.name
                        total = 0
                        while True:
                            chunk = resp.read(1024 * 1024)
                            if not chunk:
                                break
                            total += len(chunk)
                            if total > max_bytes:
                                raise ValueError(f"下载内容超过最大限制 {max_bytes} bytes")
                            tmp_file.write(chunk)

                    return {
                        "temp_path": tmp_path,
                        "downloaded_bytes": total,
                        "final_url": current_url,
                    }

            except urllib.error.HTTPError as exc:
                if 300 <= exc.code < 400:
                    location = exc.headers.get("Location") if exc.headers else None
                    if not location:
                        raise ValueError(f"URL 重定向缺少 Location（status={exc.code}）") from exc
                    current_url = urllib.parse.urljoin(current_url, location)
                    continue
                raise ValueError(f"下载失败，HTTP 状态码: {exc.code}") from exc
            except urllib.error.URLError as exc:
                raise ValueError(f"下载失败: {exc.reason}") from exc
            except TimeoutError as exc:
                raise ValueError(f"下载超时（timeout_s={timeout_s}）") from exc

        raise ValueError(f"重定向次数超过限制（>{UPLOAD_BY_URL_MAX_REDIRECTS}）")
    except Exception:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def _normalize_async_mode(async_mode: Union[int, str, bool]) -> int:
    try:
        value = int(async_mode)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"async_mode 非法: {async_mode}") from exc

    if value not in (0, 1, 2):
        raise ValueError("async_mode 仅支持 0/1/2")
    return value


def _normalize_batch_chunk_size(chunk_size: Union[int, str]) -> int:
    try:
        value = int(chunk_size)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"chunk_size 非法: {chunk_size}") from exc

    if value <= 0:
        raise ValueError("chunk_size 必须 > 0")
    return min(value, 1000)


def _iter_chunks(items: Sequence[Any], chunk_size: int) -> List[List[Any]]:
    return [builtins.list(items[i : i + chunk_size]) for i in range(0, len(items), chunk_size)]


def _next_retry_chunk_size(current_chunk_size: int) -> int:
    if current_chunk_size <= BATCH_MIN_CHUNK_SIZE:
        return BATCH_MIN_CHUNK_SIZE
    if current_chunk_size <= 25:
        return BATCH_MIN_CHUNK_SIZE
    return max(BATCH_MIN_CHUNK_SIZE, current_chunk_size // 2)


def _normalize_allow_dest_prefixes(allow_dest_prefixes: Optional[Sequence[str]]) -> List[str]:
    raw = allow_dest_prefixes
    if raw is None:
        raw = BATCH_DEFAULT_ALLOW_DEST_PREFIXES

    if not isinstance(raw, (builtins.list, tuple)):
        raise ValueError("allow_dest_prefixes 必须是字符串数组")

    prefixes: List[str] = []
    for idx, item in enumerate(raw):
        if not isinstance(item, str):
            raise ValueError(f"allow_dest_prefixes[{idx}] 必须是字符串")
        p = _normalize_dir(item)
        if not p:
            raise ValueError(f"allow_dest_prefixes[{idx}] 不能为空")
        prefixes.append(p)

    if not prefixes:
        raise ValueError("allow_dest_prefixes 不能为空")
    return prefixes


def _path_has_prefix(path: str, prefix: str) -> bool:
    if prefix == "/":
        return True
    return path == prefix or path.startswith(prefix + "/")


def _validate_dest_prefix(dest_full: str, allow_dest_prefixes: Sequence[str]) -> None:
    if any(_path_has_prefix(dest_full, p) for p in allow_dest_prefixes):
        return
    raise ValueError(
        "dest_dir 超出允许范围: "
        f"{dest_full}. allow_dest_prefixes={builtins.list(allow_dest_prefixes)}"
    )


def _normalize_batch_items(items: Any) -> List[Dict[str, Any]]:
    if not isinstance(items, builtins.list):
        raise ValueError("items 必须是 list[dict]")
    if not items:
        raise ValueError("items 不能为空")

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"items[{idx}] 必须是对象")
        normalized.append(item)
    return normalized


def _prepare_move_copy_batch_items(
    items: Any,
    cred: RuntimeCredential,
    allow_dest_prefixes: Optional[Sequence[str]],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    allow_prefixes = _normalize_allow_dest_prefixes(allow_dest_prefixes)
    raw_items = _normalize_batch_items(items)

    prepared: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_items):
        src_path = str(item.get("src_path", "") or "").strip()
        dest_dir = str(item.get("dest_dir", "") or "").strip()
        if not src_path:
            raise ValueError(f"items[{idx}].src_path 不能为空")
        if not dest_dir:
            raise ValueError(f"items[{idx}].dest_dir 不能为空")

        src_full = _resolve_path(src_path, cred)
        dest_full = _resolve_dir(dest_dir, cred)
        _validate_dest_prefix(dest_full, allow_prefixes)

        filemanager_item: Dict[str, Any] = {
            "path": src_full,
            "dest": dest_full,
        }

        normalized_item: Dict[str, Any] = {
            "src_full": src_full,
            "dest_full": dest_full,
        }

        if "new_name" in item and item.get("new_name") is not None:
            new_name = str(item.get("new_name") or "").strip()
            if not new_name:
                raise ValueError(f"items[{idx}].new_name 不能为空字符串")
            filemanager_item["newname"] = new_name
            normalized_item["new_name"] = new_name

        prepared.append(
            {
                "filemanager_item": filemanager_item,
                "normalized_item": normalized_item,
            }
        )

    return prepared, allow_prefixes


def _prepare_rename_batch_items(items: Any, cred: RuntimeCredential) -> List[Dict[str, Any]]:
    raw_items = _normalize_batch_items(items)

    prepared: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_items):
        path = str(item.get("path", "") or "").strip()
        new_name = str(item.get("new_name", "") or "").strip()
        if not path:
            raise ValueError(f"items[{idx}].path 不能为空")
        if not new_name:
            raise ValueError(f"items[{idx}].new_name 不能为空")

        path_full = _resolve_path(path, cred)
        prepared.append(
            {
                "filemanager_item": {
                    "path": path_full,
                    "newname": new_name,
                },
                "normalized_item": {
                    "path_full": path_full,
                    "new_name": new_name,
                },
            }
        )

    return prepared


def _extract_errno(resp: Dict[str, Any]) -> Optional[int]:
    errno = resp.get("errno")
    if errno is None:
        return None
    try:
        return int(errno)
    except (TypeError, ValueError):
        return None


def _extract_resp_core(resp: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "errno": resp.get("errno"),
        "taskid": resp.get("taskid"),
        "info": resp.get("info"),
    }


def _is_fail_fast_error(
    *,
    errno: Optional[int],
    message: str,
    response: Optional[Dict[str, Any]] = None,
) -> bool:
    if errno is not None and errno in BATCH_FAILFAST_ERRNOS:
        return True

    corpus = message
    if response is not None:
        try:
            corpus += " " + json.dumps(response, ensure_ascii=False)
        except Exception:
            corpus += f" {response}"

    lower_corpus = corpus.lower()
    return any(hint.lower() in lower_corpus for hint in BATCH_FAILFAST_HINTS)


def _build_batch_envelope(
    *,
    tool: str,
    dry_run: bool,
    async_mode: int,
    ondup: Optional[str],
    chunk_size: int,
    total_items: int,
) -> Dict[str, Any]:
    return {
        "status": "success",
        "tool": tool,
        "dry_run": dry_run,
        "async_mode": async_mode,
        "ondup": ondup,
        "chunk_size": chunk_size,
        "total_items": total_items,
        "chunks": 0,
        "summary": {
            "ok_chunks": 0,
            "failed_chunks": 0,
            "ok_items_est": 0,
            "failed_items_est": 0,
        },
        "results": [],
        "errors": [],
    }


def _build_batch_error_envelope(
    *,
    tool: str,
    message: str,
    dry_run: bool,
    async_mode: int,
    ondup: Optional[str],
    chunk_size: int,
    total_items: int,
    items_preview: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    envelope = _build_batch_envelope(
        tool=tool,
        dry_run=dry_run,
        async_mode=async_mode,
        ondup=ondup,
        chunk_size=chunk_size,
        total_items=total_items,
    )
    envelope["status"] = "error"
    envelope["chunks"] = 1 if total_items else 0
    envelope["summary"]["failed_chunks"] = 1 if total_items else 0
    envelope["summary"]["failed_items_est"] = total_items
    envelope["errors"].append(
        {
            "chunk_index": "0",
            "message": message,
            "items_preview": (items_preview or [])[:3],
        }
    )
    return envelope


def _build_batch_result_entry(
    *,
    chunk_index: str,
    items: List[Dict[str, Any]],
    filelist_items: List[Dict[str, Any]],
    response: Dict[str, Any],
    status: str,
    current_chunk_size: int,
    dry_run: bool,
    async_mode: int,
    message: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    entry: Dict[str, Any] = {
        "chunk_index": chunk_index,
        "status": status,
        "items": items,
        "request_preview": {
            "chunk_items": len(items),
            "chunk_size_used": current_chunk_size,
            "items_preview": items[:3],
            "filelist_preview": filelist_items[:3],
        },
        "response": _extract_resp_core(response),
    }

    if dry_run:
        entry["request_preview"]["dry_run"] = True

    if async_mode == 2 and response.get("taskid") and not response.get("info"):
        entry["notes"] = "async_mode=2 返回了 taskid 但 info 为空，建议后续抽样核验或补 task 查询接口。"

    if notes:
        entry["notes"] = notes

    if message:
        entry["message"] = message

    return entry


def _call_filemanager_batch_api(
    *,
    operation: str,
    api: filemanager_api.FilemanagerApi,
    access_token: str,
    async_mode: int,
    filelist_json: str,
    ondup: Optional[str],
) -> Dict[str, Any]:
    if operation == "move":
        return api.filemanagermove(
            access_token=access_token,
            _async=async_mode,
            filelist=filelist_json,
            ondup=ondup,
        )
    if operation == "copy":
        return api.filemanagercopy(
            access_token=access_token,
            _async=async_mode,
            filelist=filelist_json,
            ondup=ondup,
        )
    if operation == "rename":
        return api.filemanagerrename(
            access_token=access_token,
            _async=async_mode,
            filelist=filelist_json,
        )
    raise ValueError(f"未知 operation: {operation}")


def _run_filemanager_batch_chunk(
    *,
    tool: str,
    operation: str,
    chunk_entries: List[Dict[str, Any]],
    chunk_index: str,
    current_chunk_size: int,
    min_chunk_size: int,
    envelope: Dict[str, Any],
    access_token: str,
    api: Optional[filemanager_api.FilemanagerApi],
    async_mode: int,
    ondup: Optional[str],
    dry_run: bool,
) -> bool:
    filelist_items = [entry["filemanager_item"] for entry in chunk_entries]
    normalized_items = [entry["normalized_item"] for entry in chunk_entries]

    if dry_run:
        dry_resp = {"errno": 0, "taskid": None, "info": [{"dry_run": True}]}
        envelope["results"].append(
            _build_batch_result_entry(
                chunk_index=chunk_index,
                items=normalized_items,
                filelist_items=filelist_items,
                response=dry_resp,
                status="ok",
                current_chunk_size=current_chunk_size,
                dry_run=True,
                async_mode=async_mode,
                notes="dry_run=true，仅做参数与路径校验，未调用百度 filemanager 接口。",
            )
        )
        envelope["summary"]["ok_chunks"] += 1
        envelope["summary"]["ok_items_est"] += len(chunk_entries)
        return False

    if api is None:
        raise RuntimeError("internal error: api is required when dry_run=false")

    response: Dict[str, Any] = {}
    errno: Optional[int] = None
    failed_message = ""
    try:
        filelist_json = json.dumps(filelist_items, ensure_ascii=False)
        response = _call_filemanager_batch_api(
            operation=operation,
            api=api,
            access_token=access_token,
            async_mode=async_mode,
            filelist_json=filelist_json,
            ondup=ondup,
        )
        errno = _extract_errno(response)
        if errno in (None, 0):
            envelope["results"].append(
                _build_batch_result_entry(
                    chunk_index=chunk_index,
                    items=normalized_items,
                    filelist_items=filelist_items,
                    response=response,
                    status="ok",
                    current_chunk_size=current_chunk_size,
                    dry_run=False,
                    async_mode=async_mode,
                )
            )
            envelope["summary"]["ok_chunks"] += 1
            envelope["summary"]["ok_items_est"] += len(chunk_entries)
            return False

        failed_message = f"{tool} chunk 失败 errno={errno}"
    except Exception as exc:
        failed_message = f"{tool} chunk 调用异常: {exc}"

    fail_fast = _is_fail_fast_error(errno=errno, message=failed_message, response=response)

    can_split = len(chunk_entries) > 1 and current_chunk_size > min_chunk_size and not fail_fast
    if can_split:
        next_chunk_size = _next_retry_chunk_size(current_chunk_size)
        if next_chunk_size < current_chunk_size:
            envelope["results"].append(
                _build_batch_result_entry(
                    chunk_index=chunk_index,
                    items=normalized_items,
                    filelist_items=filelist_items,
                    response=response,
                    status="retry_split",
                    current_chunk_size=current_chunk_size,
                    dry_run=False,
                    async_mode=async_mode,
                    message=failed_message,
                    notes=f"chunk 失败后降级重试：{current_chunk_size}->{next_chunk_size}",
                )
            )
            for idx, sub_chunk in enumerate(_iter_chunks(chunk_entries, next_chunk_size), start=1):
                stop_all = _run_filemanager_batch_chunk(
                    tool=tool,
                    operation=operation,
                    chunk_entries=sub_chunk,
                    chunk_index=f"{chunk_index}.{idx}",
                    current_chunk_size=next_chunk_size,
                    min_chunk_size=min_chunk_size,
                    envelope=envelope,
                    access_token=access_token,
                    api=api,
                    async_mode=async_mode,
                    ondup=ondup,
                    dry_run=dry_run,
                )
                if stop_all:
                    return True
            return False

    envelope["results"].append(
        _build_batch_result_entry(
            chunk_index=chunk_index,
            items=normalized_items,
            filelist_items=filelist_items,
            response=response,
            status="failed",
            current_chunk_size=current_chunk_size,
            dry_run=False,
            async_mode=async_mode,
            message=failed_message,
            notes=("参数/权限/token 类错误，已 fail-fast 停止后续批次。" if fail_fast else None),
        )
    )
    envelope["summary"]["failed_chunks"] += 1
    envelope["summary"]["failed_items_est"] += len(chunk_entries)
    envelope["errors"].append(
        {
            "chunk_index": chunk_index,
            "message": _sanitize_message(failed_message, access_token),
            "items_preview": normalized_items[:3],
        }
    )
    return fail_fast


def _execute_filemanager_batch(
    *,
    tool: str,
    operation: str,
    prepared_items: List[Dict[str, Any]],
    cred: RuntimeCredential,
    async_mode: int,
    ondup: Optional[str],
    chunk_size: int,
    dry_run: bool,
) -> Dict[str, Any]:
    envelope = _build_batch_envelope(
        tool=tool,
        dry_run=dry_run,
        async_mode=async_mode,
        ondup=ondup,
        chunk_size=chunk_size,
        total_items=len(prepared_items),
    )

    top_chunks = _iter_chunks(prepared_items, chunk_size)

    if dry_run:
        for idx, chunk in enumerate(top_chunks, start=1):
            stop_all = _run_filemanager_batch_chunk(
                tool=tool,
                operation=operation,
                chunk_entries=chunk,
                chunk_index=str(idx),
                current_chunk_size=chunk_size,
                min_chunk_size=BATCH_MIN_CHUNK_SIZE,
                envelope=envelope,
                access_token=cred.access_token,
                api=None,
                async_mode=async_mode,
                ondup=ondup,
                dry_run=True,
            )
            if stop_all:
                break
    else:
        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            for idx, chunk in enumerate(top_chunks, start=1):
                stop_all = _run_filemanager_batch_chunk(
                    tool=tool,
                    operation=operation,
                    chunk_entries=chunk,
                    chunk_index=str(idx),
                    current_chunk_size=chunk_size,
                    min_chunk_size=BATCH_MIN_CHUNK_SIZE,
                    envelope=envelope,
                    access_token=cred.access_token,
                    api=api,
                    async_mode=async_mode,
                    ondup=ondup,
                    dry_run=False,
                )
                if stop_all:
                    break

    envelope["chunks"] = envelope["summary"]["ok_chunks"] + envelope["summary"]["failed_chunks"]
    if envelope["errors"]:
        envelope["status"] = "error"

    return envelope




@mcp.tool()
def list(
    dir: Optional[str] = None,
    limit: int = 100,
    order: str = "name",
    desc: int = 0,
    start: int = 0,
) -> Dict[str, Any]:
    """列出目录。dir 为空时默认使用 token 文件中的 default_dir。"""
    try:
        cred = _load_runtime_credential()
        target_dir = _resolve_dir(dir, cred)
        limit = max(1, min(int(limit), 1000))
        start = max(0, int(start))

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            resp = api.xpanfilelist(
                access_token=cred.access_token,
                dir=target_dir,
                folder="0",
                start=str(start),
                limit=limit,
                order=order,
                desc=desc,
                web="1",
                showempty=1,
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_items = resp.get("list", []) or []
        items = [_format_entry(item) for item in raw_items]

        return _success(
            {
                "dir": target_dir,
                "default_dir": cred.default_dir,
                "start": start,
                "limit": limit,
                "order": order,
                "desc": int(desc),
                "count": len(items),
                "has_more": bool(resp.get("has_more", 0)),
                "items": items,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"list 执行失败: {exc}")


@mcp.tool()
def file_list(
    dir: Optional[str] = None,
    limit: int = 100,
    order: str = "name",
    desc: int = 0,
    start: int = 0,
) -> Dict[str, Any]:
    """官方同名工具：等价于 list。"""
    return list(dir=dir, limit=limit, order=order, desc=desc, start=start)


@mcp.tool()
def search(
    keyword: str,
    dir: Optional[str] = None,
    recursion: int = 1,
    num: int = 100,
    page: int = 1,
) -> Dict[str, Any]:
    """搜索文件。dir 为空时默认使用 token 文件中的 default_dir。"""
    try:
        kw = (keyword or "").strip()
        if not kw:
            return _error("keyword 不能为空")

        cred = _load_runtime_credential()
        target_dir = _resolve_dir(dir, cred)
        num = max(1, min(int(num), 1000))
        page = max(1, int(page))
        recursion_flag = _normalize_int_bool(recursion)

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            resp = api.xpanfilesearch(
                access_token=cred.access_token,
                key=kw,
                web="1",
                num=str(num),
                page=str(page),
                dir=target_dir,
                recursion=str(recursion_flag),
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_items = resp.get("list", []) or []
        items = [_format_entry(item) for item in raw_items]

        return _success(
            {
                "keyword": kw,
                "dir": target_dir,
                "default_dir": cred.default_dir,
                "count": len(items),
                "items": items,
                "page": page,
                "num": num,
                "recursion": recursion_flag,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"search 执行失败: {exc}")


@mcp.tool()
def file_keyword_search(
    keyword: str,
    dir: Optional[str] = None,
    recursion: int = 1,
    num: int = 100,
    page: int = 1,
) -> Dict[str, Any]:
    """官方同名工具：等价于 search。"""
    return search(keyword=keyword, dir=dir, recursion=recursion, num=num, page=page)


@mcp.tool()
def mkdir(path: str, parent_dir: Optional[str] = None) -> Dict[str, Any]:
    """创建目录。path 为相对路径时，基于 parent_dir（若为空则 default_dir）拼接。"""
    try:
        cred = _load_runtime_credential()
        full_path = _resolve_path(path, cred, parent_dir=parent_dir)

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = fileupload_api.FileuploadApi(api_client)
            resp = api.xpanfilecreate(
                access_token=cred.access_token,
                path=full_path,
                isdir=1,
                size=0,
                uploadid="",
                block_list="[]",
                rtype=3,
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success(
            {
                "message": "目录创建成功",
                "path": full_path,
                "fs_id": resp.get("fs_id"),
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"mkdir 执行失败: {exc}")


@mcp.tool()
def make_dir(path: str, parent_dir: Optional[str] = None) -> Dict[str, Any]:
    """官方同名工具：等价于 mkdir。"""
    return mkdir(path=path, parent_dir=parent_dir)


@mcp.tool()
def move(
    src_path: str,
    dest_dir: str,
    new_name: Optional[str] = None,
    ondup: str = "fail",
) -> Dict[str, Any]:
    """移动文件/目录，可选同时重命名。"""
    try:
        cred = _load_runtime_credential()
        src_full = _resolve_path(src_path, cred)
        dest_full = _resolve_dir(dest_dir, cred)

        item: Dict[str, Any] = {
            "path": src_full,
            "dest": dest_full,
        }
        if new_name:
            item["newname"] = new_name

        filelist = json.dumps([item], ensure_ascii=False)

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            resp = api.filemanagermove(
                access_token=cred.access_token,
                _async=0,
                filelist=filelist,
                ondup=ondup,
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success(
            {
                "message": "移动请求已提交",
                "src_path": src_full,
                "dest_dir": dest_full,
                "new_name": new_name,
                "taskid": resp.get("taskid"),
                "info": resp.get("info"),
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"move 执行失败: {exc}")


@mcp.tool()
def file_move(
    src_path: str,
    dest_dir: str,
    new_name: Optional[str] = None,
    ondup: str = "fail",
) -> Dict[str, Any]:
    """官方同名工具：等价于 move。"""
    return move(src_path=src_path, dest_dir=dest_dir, new_name=new_name, ondup=ondup)


@mcp.tool()
def file_move_batch(
    items: List[Dict[str, Any]],
    ondup: str = "fail",
    async_mode: int = 1,
    chunk_size: int = 100,
    dry_run: bool = False,
    allow_dest_prefixes: List[str] = ["/Openclaw"],
) -> Dict[str, Any]:
    """批量移动（带分片与二分降级重试）。默认 ondup=fail，避免覆盖。"""
    raw_total_items = len(items) if isinstance(items, builtins.list) else 0
    resolved_async_mode = 1
    resolved_chunk_size = 100
    resolved_dry_run = bool(dry_run)

    try:
        if ondup not in BATCH_ALLOWED_ONDUP:
            raise ValueError(f"ondup 不支持: {ondup}，可选: {sorted(BATCH_ALLOWED_ONDUP)}")

        resolved_async_mode = _normalize_async_mode(async_mode)
        resolved_chunk_size = _normalize_batch_chunk_size(chunk_size)

        cred = _load_runtime_credential()
        prepared_items, allow_prefixes = _prepare_move_copy_batch_items(
            items=items,
            cred=cred,
            allow_dest_prefixes=allow_dest_prefixes,
        )

        result = _execute_filemanager_batch(
            tool="file_move_batch",
            operation="move",
            prepared_items=prepared_items,
            cred=cred,
            async_mode=resolved_async_mode,
            ondup=ondup,
            chunk_size=resolved_chunk_size,
            dry_run=resolved_dry_run,
        )
        result["allow_dest_prefixes"] = allow_prefixes
        return result
    except (CredentialError, ValueError) as exc:
        return _build_batch_error_envelope(
            tool="file_move_batch",
            message=f"file_move_batch 参数错误: {exc}",
            dry_run=resolved_dry_run,
            async_mode=resolved_async_mode,
            ondup=ondup,
            chunk_size=resolved_chunk_size,
            total_items=raw_total_items,
            items_preview=(items[:3] if isinstance(items, builtins.list) else None),
        )
    except Exception as exc:
        return _build_batch_error_envelope(
            tool="file_move_batch",
            message=f"file_move_batch 执行失败: {exc}",
            dry_run=resolved_dry_run,
            async_mode=resolved_async_mode,
            ondup=ondup,
            chunk_size=resolved_chunk_size,
            total_items=raw_total_items,
            items_preview=(items[:3] if isinstance(items, builtins.list) else None),
        )


@mcp.tool()
def file_copy(
    src_path: str,
    dest_dir: str,
    new_name: Optional[str] = None,
    ondup: str = "fail",
) -> Dict[str, Any]:
    """复制文件/目录。"""
    try:
        cred = _load_runtime_credential()
        src_full = _resolve_path(src_path, cred)
        dest_full = _resolve_dir(dest_dir, cred)

        item: Dict[str, Any] = {
            "path": src_full,
            "dest": dest_full,
        }
        if new_name:
            item["newname"] = new_name

        filelist = json.dumps([item], ensure_ascii=False)

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            resp = api.filemanagercopy(
                access_token=cred.access_token,
                _async=0,
                filelist=filelist,
                ondup=ondup,
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success(
            {
                "message": "复制请求已提交",
                "src_path": src_full,
                "dest_dir": dest_full,
                "new_name": new_name,
                "taskid": resp.get("taskid"),
                "info": resp.get("info"),
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_copy 执行失败: {exc}")


@mcp.tool()
def file_copy_batch(
    items: List[Dict[str, Any]],
    ondup: str = "newcopy",
    async_mode: int = 1,
    chunk_size: int = 100,
    dry_run: bool = False,
    allow_dest_prefixes: List[str] = ["/Openclaw"],
) -> Dict[str, Any]:
    """批量复制（带分片与二分降级重试）。默认 ondup=newcopy。"""
    raw_total_items = len(items) if isinstance(items, builtins.list) else 0
    resolved_async_mode = 1
    resolved_chunk_size = 100
    resolved_dry_run = bool(dry_run)

    try:
        if ondup not in BATCH_ALLOWED_ONDUP:
            raise ValueError(f"ondup 不支持: {ondup}，可选: {sorted(BATCH_ALLOWED_ONDUP)}")

        resolved_async_mode = _normalize_async_mode(async_mode)
        resolved_chunk_size = _normalize_batch_chunk_size(chunk_size)

        cred = _load_runtime_credential()
        prepared_items, allow_prefixes = _prepare_move_copy_batch_items(
            items=items,
            cred=cred,
            allow_dest_prefixes=allow_dest_prefixes,
        )

        result = _execute_filemanager_batch(
            tool="file_copy_batch",
            operation="copy",
            prepared_items=prepared_items,
            cred=cred,
            async_mode=resolved_async_mode,
            ondup=ondup,
            chunk_size=resolved_chunk_size,
            dry_run=resolved_dry_run,
        )
        result["allow_dest_prefixes"] = allow_prefixes
        return result
    except (CredentialError, ValueError) as exc:
        return _build_batch_error_envelope(
            tool="file_copy_batch",
            message=f"file_copy_batch 参数错误: {exc}",
            dry_run=resolved_dry_run,
            async_mode=resolved_async_mode,
            ondup=ondup,
            chunk_size=resolved_chunk_size,
            total_items=raw_total_items,
            items_preview=(items[:3] if isinstance(items, builtins.list) else None),
        )
    except Exception as exc:
        return _build_batch_error_envelope(
            tool="file_copy_batch",
            message=f"file_copy_batch 执行失败: {exc}",
            dry_run=resolved_dry_run,
            async_mode=resolved_async_mode,
            ondup=ondup,
            chunk_size=resolved_chunk_size,
            total_items=raw_total_items,
            items_preview=(items[:3] if isinstance(items, builtins.list) else None),
        )


@mcp.tool()
def rename(path: str, new_name: str) -> Dict[str, Any]:
    """重命名文件/目录。"""
    try:
        nn = (new_name or "").strip()
        if not nn:
            return _error("new_name 不能为空")

        cred = _load_runtime_credential()
        src_full = _resolve_path(path, cred)

        filelist = json.dumps([{"path": src_full, "newname": nn}], ensure_ascii=False)

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            resp = api.filemanagerrename(
                access_token=cred.access_token,
                _async=0,
                filelist=filelist,
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success(
            {
                "message": "重命名请求已提交",
                "path": src_full,
                "new_name": nn,
                "taskid": resp.get("taskid"),
                "info": resp.get("info"),
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"rename 执行失败: {exc}")


@mcp.tool()
def file_rename(path: str, new_name: str) -> Dict[str, Any]:
    """官方同名工具：等价于 rename。"""
    return rename(path=path, new_name=new_name)


@mcp.tool()
def file_rename_batch(
    items: List[Dict[str, Any]],
    async_mode: int = 1,
    chunk_size: int = 100,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """批量重命名（带分片与二分降级重试）。"""
    raw_total_items = len(items) if isinstance(items, builtins.list) else 0
    resolved_async_mode = 1
    resolved_chunk_size = 100
    resolved_dry_run = bool(dry_run)

    try:
        resolved_async_mode = _normalize_async_mode(async_mode)
        resolved_chunk_size = _normalize_batch_chunk_size(chunk_size)

        cred = _load_runtime_credential()
        prepared_items = _prepare_rename_batch_items(items=items, cred=cred)

        return _execute_filemanager_batch(
            tool="file_rename_batch",
            operation="rename",
            prepared_items=prepared_items,
            cred=cred,
            async_mode=resolved_async_mode,
            ondup=None,
            chunk_size=resolved_chunk_size,
            dry_run=resolved_dry_run,
        )
    except (CredentialError, ValueError) as exc:
        return _build_batch_error_envelope(
            tool="file_rename_batch",
            message=f"file_rename_batch 参数错误: {exc}",
            dry_run=resolved_dry_run,
            async_mode=resolved_async_mode,
            ondup=None,
            chunk_size=resolved_chunk_size,
            total_items=raw_total_items,
            items_preview=(items[:3] if isinstance(items, builtins.list) else None),
        )
    except Exception as exc:
        return _build_batch_error_envelope(
            tool="file_rename_batch",
            message=f"file_rename_batch 执行失败: {exc}",
            dry_run=resolved_dry_run,
            async_mode=resolved_async_mode,
            ondup=None,
            chunk_size=resolved_chunk_size,
            total_items=raw_total_items,
            items_preview=(items[:3] if isinstance(items, builtins.list) else None),
        )


@mcp.tool()
def delete(path: str, confirm: str = "") -> Dict[str, Any]:
    """删除文件/目录。默认拒绝，只有 confirm=\"DELETE\" 才执行。"""
    try:
        if confirm != DELETE_CONFIRM_WORD:
            return _error(
                f"安全保护：删除已拒绝。请显式传入 confirm=\"{DELETE_CONFIRM_WORD}\" 后重试。"
            )

        cred = _load_runtime_credential()
        full_path = _resolve_path(path, cred)
        filelist = json.dumps([full_path], ensure_ascii=False)

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            resp = api.filemanagerdelete(
                access_token=cred.access_token,
                _async=0,
                filelist=filelist,
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success(
            {
                "message": "删除请求已提交",
                "path": full_path,
                "taskid": resp.get("taskid"),
                "info": resp.get("info"),
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"delete 执行失败: {exc}")


@mcp.tool()
def file_del(path: str, confirm: str = "") -> Dict[str, Any]:
    """官方同名工具：等价于 delete（保留 confirm=DELETE 安全保护）。"""
    return delete(path=path, confirm=confirm)


@mcp.tool()
def upload(
    local_file_path: str,
    remote_dir: Optional[str] = None,
    remote_name: Optional[str] = None,
) -> Dict[str, Any]:
    """上传本地文件到网盘。remote_dir 为空时默认使用 token 文件中的 default_dir。"""
    try:
        cred = _load_runtime_credential()
        return _upload_local_file(local_file_path, remote_dir, remote_name, cred)
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"upload 执行失败: {exc}")


@mcp.tool()
def file_upload_stdio(
    local_file_path: str,
    remote_dir: Optional[str] = None,
    remote_name: Optional[str] = None,
) -> Dict[str, Any]:
    """官方同名工具：等价于 upload。"""
    return upload(local_file_path=local_file_path, remote_dir=remote_dir, remote_name=remote_name)


@mcp.tool()
def file_doc_list(
    parent_path: Optional[str] = None,
    recursion: int = 1,
    page: int = 1,
    num: int = 100,
    order: str = "name",
    desc: int = 0,
) -> Dict[str, Any]:
    """按文档类型列出文件。"""
    try:
        cred = _load_runtime_credential()
        target_dir = _resolve_dir(parent_path, cred)
        page = max(1, int(page))
        num = max(1, min(int(num), 1000))

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            resp = api.xpanfiledoclist(
                access_token=cred.access_token,
                parent_path=target_dir,
                recursion=str(_normalize_int_bool(recursion)),
                page=page,
                num=num,
                order=order,
                desc=str(_normalize_int_bool(desc)),
                web="1",
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_items = resp.get("info") or resp.get("list") or []
        source_field = "info" if resp.get("info") else "list"
        if not isinstance(raw_items, builtins.list):
            return _error(f"file_doc_list 响应 {source_field} 字段类型错误: {type(raw_items).__name__}")

        items = [_format_entry(item) for item in raw_items if isinstance(item, dict)]
        return _success(
            {
                "dir": target_dir,
                "count": len(items),
                "items": items,
                "page": page,
                "num": num,
                "has_more": _as_bool_flag(resp.get("has_more", 0)),
                "source_field": source_field,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_doc_list 执行失败: {exc}")


@mcp.tool()
def file_image_list(
    parent_path: Optional[str] = None,
    recursion: int = 1,
    page: int = 1,
    num: int = 100,
    order: str = "name",
    desc: int = 0,
    web: int = 1,
) -> Dict[str, Any]:
    """按图片类型列出文件（imagelist，优先解析 info[]，兼容 list[]）。"""
    try:
        cred = _load_runtime_credential()
        target_dir = _resolve_dir(parent_path, cred)
        page = max(1, int(page))
        num = max(1, min(int(num), 1000))
        web_flag = _normalize_int_bool(web)

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            resp = api.xpanfileimagelist(
                access_token=cred.access_token,
                parent_path=target_dir,
                recursion=str(_normalize_int_bool(recursion)),
                page=page,
                num=num,
                order=order,
                desc=str(_normalize_int_bool(desc)),
                web=str(web_flag),
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_items = resp.get("info") or resp.get("list") or []
        source_field = "info" if resp.get("info") else "list"

        if not isinstance(raw_items, builtins.list):
            return _error(
                f"file_image_list 响应 {source_field} 字段类型错误: {type(raw_items).__name__}"
            )

        items = [
            _format_entry(_normalize_imagelist_item(item))
            for item in raw_items
            if isinstance(item, dict)
        ]

        return _success(
            {
                "dir": target_dir,
                "count": len(items),
                "items": items,
                "page": page,
                "num": num,
                "has_more": _as_bool_flag(resp.get("has_more", 0)),
                "source_field": source_field,
                "web": web_flag,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_image_list 执行失败: {exc}")


@mcp.tool()
def file_video_list_api(
    parent_path: Optional[str] = None,
    recursion: int = 1,
    page: int = 1,
    num: int = 100,
    order: str = "name",
    desc: int = 0,
    web: int = 1,
) -> Dict[str, Any]:
    """官方 videolist：GET /rest/2.0/xpan/file?method=videolist。"""
    token = ""
    try:
        cred = _load_runtime_credential()
        token = cred.access_token

        target_dir = _resolve_dir(parent_path, cred)
        page = max(1, int(page))
        num = max(1, min(int(num), 1000))
        recursion_flag = _normalize_int_bool(recursion)
        desc_flag = _normalize_int_bool(desc)
        web_flag = _normalize_int_bool(web)

        resp = _http_get_json(
            XPAN_FILE_ENDPOINT,
            {
                "method": "videolist",
                "access_token": cred.access_token,
                "parent_path": target_dir,
                "page": page,
                "num": num,
                "order": order,
                "desc": desc_flag,
                "recursion": recursion_flag,
                "web": web_flag,
            },
            token=cred.access_token,
        )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_items = resp.get("info") or resp.get("list") or []
        source_field = "info" if resp.get("info") else "list"
        if not isinstance(raw_items, builtins.list):
            return _error(
                f"file_video_list_api 响应 {source_field} 字段类型错误: {type(raw_items).__name__}",
                token,
            )

        items = [
            _format_entry(_normalize_imagelist_item(item))
            for item in raw_items
            if isinstance(item, dict)
        ]

        return _success(
            {
                "dir": target_dir,
                "count": len(items),
                "items": items,
                "page": page,
                "num": num,
                "order": order,
                "desc": desc_flag,
                "recursion": recursion_flag,
                "web": web_flag,
                "has_more": _as_bool_flag(resp.get("has_more", 0)),
                "source_field": source_field,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_video_list_api 执行失败: {exc}", token)


@mcp.tool()
def file_video_list(
    dir: Optional[str] = None,
    recursion: int = 1,
    start: int = 0,
    limit: int = 100,
    order: str = "name",
    desc: int = 0,
) -> Dict[str, Any]:
    """视频列表：调用 xpanfilelistall 后按 category/扩展名过滤。"""
    try:
        cred = _load_runtime_credential()
        target_dir = _resolve_dir(dir, cred)
        start = max(0, int(start))
        limit = max(1, min(int(limit), 1000))

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            resp = api.xpanfilelistall(
                access_token=cred.access_token,
                path=target_dir,
                recursion=_normalize_int_bool(recursion),
                web="1",
                start=start,
                limit=limit,
                order=order,
                desc=_normalize_int_bool(desc),
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_items = resp.get("list", []) or []
        filtered = [item for item in raw_items if _is_video_item(item)]
        items = [_format_entry(item) for item in filtered]

        return _success(
            {
                "dir": target_dir,
                "count": len(items),
                "source_count": len(raw_items),
                "items": items,
                "start": start,
                "limit": limit,
                "recursion": _normalize_int_bool(recursion),
                "pagination_note": (
                    "分页发生在源列表（xpanfilelistall）后再按视频过滤；"
                    "如需凑满视频数量，请继续增加 start 拉取后续页。"
                ),
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_video_list 执行失败: {exc}")


@mcp.tool()
def file_meta(
    fsids: Union[int, str, Sequence[Union[int, str]]],
    dlink: int = 0,
    thumb: int = 0,
    extra: int = 0,
    needmedia: int = 0,
    path: Optional[str] = None,
) -> Dict[str, Any]:
    """获取文件元信息。fsids 支持 list/int/str，内部转为 JSON 字符串。"""
    try:
        cred = _load_runtime_credential()

        try:
            fsid_list = _normalize_fsids(fsids)
        except Exception as exc:
            return _error(f"fsids 参数非法: {exc}")

        fsids_json = json.dumps(fsid_list, ensure_ascii=False)
        req_path = _resolve_dir(path, cred) if path else None

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            kwargs: Dict[str, Any] = {
                "access_token": cred.access_token,
                "fsids": fsids_json,
                "dlink": str(_normalize_int_bool(dlink)),
                "thumb": str(_normalize_int_bool(thumb)),
                "extra": str(_normalize_int_bool(extra)),
                "needmedia": _normalize_int_bool(needmedia),
            }
            if req_path:
                kwargs["path"] = req_path

            resp = api.xpanmultimediafilemetas(**kwargs)

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success(
            {
                "fsids": fsid_list,
                "count": len(resp.get("list", []) or []),
                "metas": resp.get("list", []) or [],
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_meta 执行失败: {exc}")


@mcp.tool()
def category_info(
    category: int,
    parent_path: str = "/",
    recursion: int = 1,
) -> Dict[str, Any]:
    """统计某个分类在目录下的文件数量/体积。"""
    token = ""
    try:
        cred = _load_runtime_credential()
        token = cred.access_token

        resolved_category = _normalize_category(category)
        resolved_parent_path = _resolve_dir(parent_path, cred)
        resolved_recursion = _normalize_int_bool(recursion)

        resp = _http_get_json(
            CATEGORY_INFO_ENDPOINT,
            {
                "access_token": cred.access_token,
                "category": resolved_category,
                "parent_path": resolved_parent_path,
                "recursion": resolved_recursion,
            },
            token=cred.access_token,
        )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success(
            _extract_category_info_payload(
                resp=resp,
                category=resolved_category,
                parent_path=resolved_parent_path,
                recursion=resolved_recursion,
            )
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"category_info 执行失败: {exc}", token)


@mcp.tool()
def category_info_multi(
    categories: Union[str, Sequence[Union[int, str]], int],
    parent_path: str = "/",
    recursion: int = 1,
) -> Dict[str, Any]:
    """批量统计多个分类，返回按 category 聚合结果。"""
    token = ""
    try:
        cred = _load_runtime_credential()
        token = cred.access_token

        resolved_categories = _normalize_categories(categories)
        resolved_parent_path = _resolve_dir(parent_path, cred)
        resolved_recursion = _normalize_int_bool(recursion)

        results: List[Dict[str, Any]] = []
        by_category: Dict[str, Dict[str, Any]] = {}

        for category in resolved_categories:
            resp = _http_get_json(
                CATEGORY_INFO_ENDPOINT,
                {
                    "access_token": cred.access_token,
                    "category": category,
                    "parent_path": resolved_parent_path,
                    "recursion": resolved_recursion,
                },
                token=cred.access_token,
            )

            err = _check_api_errno(resp, cred.access_token)
            if err:
                return _error(
                    f"category_info_multi category={category} 调用失败: {err.get('message')}",
                    cred.access_token,
                )

            payload = _extract_category_info_payload(
                resp=resp,
                category=category,
                parent_path=resolved_parent_path,
                recursion=resolved_recursion,
            )
            results.append(payload)
            by_category[str(category)] = payload

        return _success(
            {
                "categories": resolved_categories,
                "parent_path": resolved_parent_path,
                "recursion": resolved_recursion,
                "results": results,
                "by_category": by_category,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"category_info_multi 执行失败: {exc}", token)


@mcp.tool()
def image_gettags(type: int = 1) -> Dict[str, Any]:
    """获取图片智能分类标签（imageproc/gettags）。"""
    token = ""
    try:
        cred = _load_runtime_credential()
        token = cred.access_token

        resolved_type = _normalize_gettags_type(type)

        resp = _http_get_json(
            IMAGE_GETTAGS_ENDPOINT,
            {
                "method": "gettags",
                "key": "tag",
                "type": resolved_type,
                "access_token": cred.access_token,
            },
            token=cred.access_token,
        )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_list = resp.get("list")
        if raw_list is None:
            raw_list = resp.get("tags", [])
        if not isinstance(raw_list, builtins.list):
            return _error(f"image_gettags 响应 list 字段类型错误: {type(raw_list).__name__}", token)

        tags = [_format_image_tag_item(item) for item in raw_list if isinstance(item, dict)]

        return _success(
            {
                "type": resolved_type,
                "count": len(tags),
                "list": tags,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"image_gettags 执行失败: {exc}", token)


@mcp.tool()
def image_gettags_summary(type: int = 1, top: int = 50) -> Dict[str, Any]:
    """图片标签摘要：按 count 排序后返回 top N。"""
    try:
        top_n = max(1, min(int(top), 500))
    except (TypeError, ValueError) as exc:
        return _error(f"top 参数非法: {exc}")

    result = image_gettags(type=type)
    if result.get("status") != "success":
        return result

    tags = result.get("list", [])

    def _as_int(value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    ordered = sorted(tags, key=lambda item: _as_int(item.get("count")), reverse=True)
    top_tags = ordered[:top_n]

    return _success(
        {
            "type": result.get("type"),
            "top": top_n,
            "total_tags": len(tags),
            "total_count": sum(_as_int(item.get("count")) for item in tags),
            "list": top_tags,
        }
    )


@mcp.tool()
def image_search(
    search_type: int,
    keyword: str,
    start: int = 0,
    limit: int = 100,
    size: Optional[str] = None,
) -> Dict[str, Any]:
    """根据关键字检索图片（imageproc/search）。"""
    token = ""
    try:
        kw = (keyword or "").strip()
        if not kw:
            return _error("keyword 不能为空")

        cred = _load_runtime_credential()
        token = cred.access_token

        resolved_search_type = _normalize_search_type(search_type)
        resolved_start = _normalize_non_negative_int(start, "start")
        resolved_limit = _normalize_positive_int(limit, "limit", 100)
        resolved_size = _normalize_optional_csv(size, "size")

        resp = _http_get_json(
            IMAGEPROC_ENDPOINT,
            {
                "method": "search",
                "access_token": cred.access_token,
                "search_type": resolved_search_type,
                "keyword": kw,
                "start": resolved_start,
                "limit": resolved_limit,
                "size": resolved_size,
            },
            token=cred.access_token,
        )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_list = resp.get("list", [])
        if not isinstance(raw_list, builtins.list):
            return _error(f"image_search 响应 list 字段类型错误: {type(raw_list).__name__}", token)

        items = [_format_image_search_item(item) for item in raw_list if isinstance(item, dict)]

        return _success(
            {
                "search_type": resolved_search_type,
                "keyword": kw,
                "start": resolved_start,
                "limit": resolved_limit,
                "size": resolved_size,
                "has_more": _as_bool_flag(resp.get("has_more", 0)),
                "count": len(items),
                "list": items,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except ValueError as exc:
        return _error(f"image_search 参数错误: {exc}", token)
    except Exception as exc:
        return _error(f"image_search 执行失败: {exc}", token)



@mcp.tool()
def recent_list(
    category: int = 3,
    start: int = 0,
    limit: int = 100,
    sortby: Optional[str] = None,
    order: Optional[str] = None,
    stime: Optional[Union[int, str]] = None,
    etime: Optional[Union[int, str]] = None,
    resolution: str = "off",
) -> Dict[str, Any]:
    """按上传时间获取文件列表（multimedia/recentlist）。"""
    token = ""
    try:
        cred = _load_runtime_credential()
        token = cred.access_token

        resolved_category = _normalize_category(category)
        resolved_start = _normalize_non_negative_int(start, "start")
        resolved_resolution = _normalize_on_off(resolution, "resolution")

        max_limit = 100 if resolved_resolution == "on" else 1000
        resolved_limit = _normalize_positive_int(limit, "limit", max_limit)

        resolved_sortby = _normalize_optional_text(sortby, "sortby")
        resolved_order = _normalize_optional_text(order, "order")
        resolved_stime = _normalize_optional_int(stime, "stime")
        resolved_etime = _normalize_optional_int(etime, "etime")

        if (
            resolved_stime is not None
            and resolved_etime is not None
            and resolved_stime > resolved_etime
        ):
            raise ValueError("stime 不能大于 etime")

        resp = _http_get_json(
            MULTIMEDIA_ENDPOINT,
            {
                "method": "recentlist",
                "access_token": cred.access_token,
                "category": resolved_category,
                "start": resolved_start,
                "limit": resolved_limit,
                "sortby": resolved_sortby,
                "order": resolved_order,
                "stime": resolved_stime,
                "etime": resolved_etime,
                "resolution": resolved_resolution,
            },
            token=cred.access_token,
        )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        raw_list = resp.get("list", [])
        if not isinstance(raw_list, builtins.list):
            return _error(f"recent_list 响应 list 字段类型错误: {type(raw_list).__name__}", token)

        return _success(
            {
                "category": resolved_category,
                "start": resolved_start,
                "limit": resolved_limit,
                "sortby": resolved_sortby,
                "order": resolved_order,
                "stime": resolved_stime,
                "etime": resolved_etime,
                "resolution": resolved_resolution,
                "cursor": resp.get("cursor"),
                "has_more": _as_bool_flag(resp.get("has_more", 0)),
                "count": len(raw_list),
                "list": raw_list,
            }
        )
    except CredentialError as exc:
        return _error(str(exc))
    except ValueError as exc:
        return _error(f"recent_list 参数错误: {exc}", token)
    except Exception as exc:
        return _error(f"recent_list 执行失败: {exc}", token)


@mcp.tool()
def user_info() -> Dict[str, Any]:
    """获取用户信息（xpannasuinfo）。"""
    try:
        cred = _load_runtime_credential()

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = userinfo_api.UserinfoApi(api_client)
            resp = api.xpannasuinfo(access_token=cred.access_token)

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success({"user": resp})
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"user_info 执行失败: {exc}")


@mcp.tool()
def get_quota(checkexpire: int = 1, checkfree: int = 1) -> Dict[str, Any]:
    """获取网盘配额（apiquota）。"""
    try:
        cred = _load_runtime_credential()

        with openapi_client.ApiClient(_new_configuration()) as api_client:
            api = userinfo_api.UserinfoApi(api_client)
            resp = api.apiquota(
                access_token=cred.access_token,
                checkexpire=_normalize_int_bool(checkexpire),
                checkfree=_normalize_int_bool(checkfree),
            )

        err = _check_api_errno(resp, cred.access_token)
        if err:
            return err

        return _success({"quota": resp})
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"get_quota 执行失败: {exc}")


@mcp.tool()
def file_upload_by_text(
    text: str,
    remote_dir: Optional[str] = None,
    remote_name: Optional[str] = None,
    max_chars: int = UPLOAD_BY_TEXT_MAX_CHARS,
    max_bytes: int = UPLOAD_BY_TEXT_MAX_BYTES,
) -> Dict[str, Any]:
    """将文本写入临时文件后上传。"""
    try:
        content = text if isinstance(text, str) else str(text)
        max_chars = max(1, min(int(max_chars), 2_000_000))
        max_bytes = max(1, min(int(max_bytes), 20 * 1024 * 1024))

        char_count = len(content)
        if char_count > max_chars:
            return _error(f"文本长度超限：{char_count} chars > max_chars={max_chars}")

        raw = content.encode("utf-8")
        byte_count = len(raw)
        if byte_count > max_bytes:
            return _error(f"文本字节超限：{byte_count} bytes > max_bytes={max_bytes}")

        with tempfile.NamedTemporaryFile(prefix="baidudisk_text_", suffix=".txt", delete=False) as f:
            tmp_path = f.name
            f.write(raw)

        try:
            cred = _load_runtime_credential()
            target_name = (remote_name or "").strip() or f"text-{int(time.time())}.txt"
            result = _upload_local_file(
                local_file_path=tmp_path,
                remote_dir=remote_dir,
                remote_name=target_name,
                cred=cred,
            )
            if result.get("status") == "success":
                result["source"] = {
                    "kind": "text",
                    "chars": char_count,
                    "bytes": byte_count,
                }
            return result
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_upload_by_text 执行失败: {exc}")


@mcp.tool()
def file_upload_by_url(
    url: str,
    remote_dir: Optional[str] = None,
    remote_name: Optional[str] = None,
    timeout_s: int = 60,
    max_bytes: int = UPLOAD_BY_URL_MAX_BYTES,
) -> Dict[str, Any]:
    """下载 HTTP(S) URL 到临时文件后上传（带基础 SSRF 防护）。"""
    temp_path = ""
    try:
        target_url = (url or "").strip()
        if not target_url:
            return _error("url 不能为空")

        timeout_s = max(1, min(int(timeout_s), UPLOAD_BY_URL_MAX_TIMEOUT_S))
        max_bytes = max(1024, min(int(max_bytes), 1024 * 1024 * 1024))

        try:
            download_info = _download_url_to_temp_file(
                url=target_url,
                timeout_s=timeout_s,
                max_bytes=max_bytes,
            )
        except Exception as exc:
            return _error(f"URL 下载失败: {exc}")

        temp_path = download_info["temp_path"]
        final_url = download_info["final_url"]
        downloaded_bytes = download_info["downloaded_bytes"]

        cred = _load_runtime_credential()
        name = (remote_name or "").strip() or _guess_filename_from_url(final_url)
        result = _upload_local_file(
            local_file_path=temp_path,
            remote_dir=remote_dir,
            remote_name=name,
            cred=cred,
        )

        if result.get("status") == "success":
            result["source"] = {
                "kind": "url",
                "url": target_url,
                "final_url": final_url,
                "downloaded_bytes": downloaded_bytes,
            }
        return result
    except CredentialError as exc:
        return _error(str(exc))
    except Exception as exc:
        return _error(f"file_upload_by_url 执行失败: {exc}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@mcp.tool()
def file_semantics_search(
    keyword: str,
    dir: Optional[str] = None,
    limit: int = 20,
) -> Dict[str, Any]:
    """语义搜索占位：当前 openapi_client 未提供对应 endpoint。"""
    return _unsupported(
        "当前 openapi_client 未提供语义搜索 endpoint，暂不支持 file_semantics_search。",
        {
            "keyword": keyword,
            "dir": dir,
            "limit": limit,
        },
    )


@mcp.tool()
def file_sharelink_set(
    path: str,
    period: int = 0,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """分享链接设置占位：当前 openapi_client 未提供对应 endpoint。"""
    return _unsupported(
        "当前 openapi_client 未提供分享链接设置 endpoint，暂不支持 file_sharelink_set。",
        {
            "path": path,
            "period": period,
            "password": password,
        },
    )


@mcp.tool()
def download(path: str, local_path: str) -> Dict[str, Any]:
    """下载能力占位说明。当前版本不实现下载。"""
    return _todo(
        (
            "当前 skill 未实现 download。百度网盘下载通常需走 d.pcs.baidu.com/pcs/file?method=download "
            "等接口（与本 SDK 工具集不同）。请先在主会话确认下载方案后再补齐。"
        ),
        {
            "path": path,
            "local_path": local_path,
        },
    )


@mcp.resource("netdisk://help")
def help_text() -> str:
    return """
Baidu Netdisk MCP Server (stdio)

Official-aligned tools (2.0):
- file_list(dir?, limit?, order?, desc?, start?)
- file_doc_list(parent_path?, recursion?, page?, num?, order?, desc?)
- file_image_list(parent_path?, recursion?, page?, num?, order?, desc?, web?)
- file_video_list_api(parent_path?, recursion?, page?, num?, order?, desc?, web?)  # /xpan/file?method=videolist
- file_video_list(dir?, recursion?, start?, limit?, order?, desc?)  # custom fallback(filter listall)
- category_info(category, parent_path?, recursion?)
- category_info_multi(categories, parent_path?, recursion?)
- image_gettags(type?)
- image_gettags_summary(type?, top?)
- image_search(search_type, keyword, start?, limit?, size?)
- recent_list(category?, start?, limit?, sortby?, order?, stime?, etime?, resolution?)
- file_meta(fsids, dlink?, thumb?, extra?, needmedia?, path?)
- make_dir(path, parent_dir?)
- file_copy(src_path, dest_dir, new_name?, ondup?)
- file_copy_batch(items, ondup?, async_mode?, chunk_size?, dry_run?, allow_dest_prefixes?)
- file_del(path, confirm)  # confirm 必须是 DELETE
- file_move(src_path, dest_dir, new_name?, ondup?)
- file_move_batch(items, ondup?, async_mode?, chunk_size?, dry_run?, allow_dest_prefixes?)
- file_rename(path, new_name)
- file_rename_batch(items, async_mode?, chunk_size?, dry_run?)
- file_upload_stdio(local_file_path, remote_dir?, remote_name?)
- file_upload_by_url(url, remote_dir?, remote_name?, timeout_s?, max_bytes?)
- file_upload_by_text(text, remote_dir?, remote_name?, max_chars?, max_bytes?)
- file_keyword_search(keyword, dir?, recursion?, num?, page?)
- file_semantics_search(...)  # unsupported stub
- file_sharelink_set(...)     # unsupported stub
- user_info()
- get_quota(checkexpire?, checkfree?)

Legacy aliases (kept for compatibility):
- list, search, mkdir, move, rename, delete, upload, download

Credential loading (hot reload):
- 每次工具调用都会重新读取 BAIDU_NETDISK_TOKEN_FILE。
- 若未设置 BAIDU_NETDISK_TOKEN_FILE 且 ~/.openclaw/credentials/baidudisk.json 存在，则自动读取该默认文件。
- token 文件结构示例：{"access_token":"...","default_dir":"/Openclaw/baidudisk"}
- 若文件未配置，回退到 BAIDU_NETDISK_ACCESS_TOKEN 和 BAIDU_NETDISK_DEFAULT_DIR。
""".strip()


if __name__ == "__main__":
    mcp.run(transport="stdio")
