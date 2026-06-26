#!/usr/bin/env python3
"""
DesignKit A+详情页工作流执行器（对齐 xiuxiupro 接口语义）。

命令：
- detail_plan_submit  -> POST /v1/hackathon/ai_model/prompt_submit
- detail_plan_poll    -> GET  /v1/mtlab/k2_query
- detail_render_submit-> POST /v1/hackathon/ai_product_detail/task_submit
- detail_render_regen -> POST /v1/hackathon/regen
- detail_render_poll  -> GET  /v1/hackathon/query
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from local_image_guard import describe_local_image, normalize_local_image_path
from security_logging import (
    format_curl_command,
    format_json_log,
    format_multipart_curl,
    request_log_enabled as shared_request_log_enabled,
    sanitize_json_payload,
)

DEFAULT_OPENCLAW_AK_URL = "https://www.designkit.cn/openclaw"
DEFAULT_WEBAPI_BASE = "https://openclaw-designkit-api.meitu.com"
DEFAULT_ASPECT_RATIO = "970:600"
DEFAULT_SELECTED_MODULES = [
    "首屏主视觉",
    "核心卖点图",
    "使用场景图",
    "多角度图",
    "场景氛围图",
    "商品细节图",
]
DEFAULT_OUTPUT_SUBDIR = "designkit-ecommerce-a-plus-detail"
PROJECT_ROOT = SCRIPT_DIR.parent

_webapi_base_raw = os.environ.get("DESIGNKIT_WEBAPI_BASE", DEFAULT_WEBAPI_BASE).strip().rstrip("/")
WEBAPI_BASE = re.sub(r"/v1/?$", "", _webapi_base_raw)


def _build_ssl_context() -> Optional[ssl.SSLContext]:
    cafile = os.environ.get("SSL_CERT_FILE", "").strip()
    if cafile:
        try:
            return ssl.create_default_context(cafile=cafile)
        except Exception:  # pylint: disable=broad-except
            pass

    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # pylint: disable=broad-except
        return None


_SSL_CONTEXT = _build_ssl_context()


def _urlopen(req: urllib.request.Request, timeout: int | float):
    full_url = str(getattr(req, "full_url", "")).lower()
    if _SSL_CONTEXT is not None and full_url.startswith("https://"):
        return urllib.request.urlopen(req, timeout=timeout, context=_SSL_CONTEXT)
    return urllib.request.urlopen(req, timeout=timeout)


def _openclaw_ak_url() -> str:
    return os.environ.get("DESIGNKIT_OPENCLAW_AK_URL", DEFAULT_OPENCLAW_AK_URL).strip() or DEFAULT_OPENCLAW_AK_URL


def _json_error(
    ok: bool,
    error_type: str,
    message: str,
    user_hint: str,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    out: Dict[str, Any] = {
        "ok": ok,
        "error_type": error_type,
        "message": message,
        "user_hint": user_hint,
    }
    if extra:
        out.update(extra)
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(1 if not ok else 0)


def _require_ak() -> str:
    ak = os.environ.get("DESIGNKIT_OPENCLAW_AK", "").strip()
    if not ak:
        _json_error(
            False,
            "CREDENTIALS_MISSING",
            "缺少 DESIGNKIT_OPENCLAW_AK",
            f"请先前往 {_openclaw_ak_url()} 获取 API Key，然后执行: export DESIGNKIT_OPENCLAW_AK=你的AK",
        )
    return ak


def _request_log_enabled() -> bool:
    return shared_request_log_enabled()


def _request_log_as_curl(
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Optional[bytes] = None,
) -> None:
    if not _request_log_enabled():
        return
    print(
        "[REQUEST] "
        + format_curl_command(
            method,
            url,
            headers,
            data,
            max_time=120,
        ),
        file=sys.stderr,
    )


def _request_log_as_curl_multipart(upload_url: str, file_path: str, file_name: str, mime: str) -> None:
    if not _request_log_enabled():
        return
    print(
        "[REQUEST] "
        + format_multipart_curl(
            upload_url,
            file_path=file_path,
            mime=mime,
            form_fields={
                "token": "<redacted>",
                "key": "<redacted>",
                "fname": file_name,
            },
            headers={
                "Origin": "https://www.designkit.cn",
                "Referer": "https://www.designkit.cn/editor/",
            },
            max_time=120,
        ),
        file=sys.stderr,
    )


def _request_log_response_json(label: str, text: str, http_code: Optional[int] = None) -> None:
    if not _request_log_enabled():
        return
    try:
        max_len = int(os.environ.get("OPENCLAW_REQUEST_LOG_BODY_MAX", "20000"))
    except ValueError:
        max_len = 20000
    print(format_json_log(label, text, max_len=max_len, http_code=http_code), file=sys.stderr)


def _headers_json() -> Dict[str, str]:
    ak = _require_ak()
    return {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.designkit.cn",
        "Referer": "https://www.designkit.cn/product-kit/detailpage",
        "X-Openclaw-AK": ak,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }


def _headers_get() -> Dict[str, str]:
    headers = _headers_json()
    headers.pop("Content-Type", None)
    return headers


def _query_params() -> Dict[str, str]:
    return {
        "client_id": os.environ.get("DESIGNKIT_OPENCLAW_CLIENT_ID", "1189857523"),
        "client_language": os.environ.get("DESIGNKIT_CLIENT_LANGUAGE", "zh-Hans"),
        "channel": "",
        "country_code": os.environ.get("DESIGNKIT_COUNTRY_CODE", "CN"),
        "ts_random_id": str(uuid.uuid4()),
        "client_source": "pc",
        "client_timezone": os.environ.get("DESIGNKIT_CLIENT_TIMEZONE", "Asia/Shanghai"),
        "operate_source": "web",
    }


def _url(path: str, extra: Optional[Dict[str, str]] = None) -> str:
    q = _query_params()
    if extra:
        q = {**q, **extra}
    return f"{WEBAPI_BASE}{path}?{urllib.parse.urlencode(q)}"


def _http_request(
    method: str,
    url: str,
    body: Optional[bytes] = None,
    json_mode: bool = True,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Tuple[int, Any]:
    headers = _headers_json() if json_mode and body is not None else _headers_get()
    if extra_headers:
        headers.update(extra_headers)
    if body is not None and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    _request_log_as_curl(method, url, headers, body)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with _urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            code = resp.getcode() or 200
            _request_log_response_json("response_body", raw, code)
            try:
                return code, json.loads(raw)
            except json.JSONDecodeError:
                return code, {"_raw": raw}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        _request_log_response_json("response_body", raw, exc.code)
        try:
            return exc.code, json.loads(raw)
        except json.JSONDecodeError:
            return exc.code, {"_raw": raw, "_http_message": str(exc)}
    except urllib.error.URLError as exc:
        return 503, {"_raw": str(exc), "_error_type": "url_error"}


def _looks_like_skill_internal(path: pathlib.Path) -> bool:
    try:
        path.relative_to(PROJECT_ROOT)
        return True
    except ValueError:
        return False


def _downloads_dir() -> pathlib.Path:
    return pathlib.Path.home() / "Downloads"


def _default_visual_dir() -> pathlib.Path:
    openclaw_home = os.environ.get("OPENCLAW_HOME", "").strip()
    if openclaw_home:
        return pathlib.Path(openclaw_home).expanduser() / "workspace" / "visual"
    return pathlib.Path.home() / ".openclaw" / "workspace" / "visual"


def resolve_output_dir(inp: Dict[str, Any]) -> pathlib.Path:
    explicit = str(inp.get("output_dir", "") or os.environ.get("DESIGNKIT_OUTPUT_DIR", "")).strip()
    if explicit:
        output_dir = pathlib.Path(explicit).expanduser().resolve()
    else:
        cwd = pathlib.Path.cwd().resolve()
        if (cwd / "openclaw.yaml").is_file():
            output_dir = cwd / "output"
        else:
            visual_dir = _default_visual_dir()
            if visual_dir.is_dir():
                output_dir = visual_dir / "output" / DEFAULT_OUTPUT_SUBDIR
            else:
                output_dir = _downloads_dir()

    if _looks_like_skill_internal(output_dir):
        _json_error(
            False,
            "PARAM_ERROR",
            f"输出目录不能位于 skill 目录内部: {output_dir}",
            "请改用项目 output 目录、共享 visual output 目录，或传入其他 output_dir",
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _safe_filename_part(value: str, fallback: str) -> str:
    text = re.sub(r"\s+", "_", (value or "").strip())
    text = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("._-")
    return text or fallback


def _guess_extension(url: str, default_ext: str = ".jpg") -> str:
    path = urllib.parse.urlparse(url).path
    ext = pathlib.Path(path).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp"}:
        return ext
    return default_ext


def _save_result_images(items: List[Dict[str, Any]], output_dir: pathlib.Path, product_name: str) -> List[str]:
    saved_paths: List[str] = []
    product_part = _safe_filename_part(product_name, "product")

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        image_url = str(item.get("res_img", "")).strip()
        if not image_url.startswith("http"):
            continue
        label = _safe_filename_part(str(item.get("label", "")).strip(), f"image_{index}")
        ext = _guess_extension(image_url)
        filename = f"{product_part}_{index:02d}_{label}{ext}"
        target = output_dir / filename

        req = urllib.request.Request(
            image_url,
            headers={
                "User-Agent": _headers_get().get("User-Agent", "Mozilla/5.0"),
                "Accept": "image/*,*/*;q=0.8",
            },
            method="GET",
        )
        try:
            with _urlopen(req, timeout=120) as resp:
                target.write_bytes(resp.read())
        except Exception as exc:  # pylint: disable=broad-except
            _json_error(False, "DOWNLOAD_ERROR", str(exc), f"下载生成结果失败: {image_url}")

        saved_paths.append(str(target))

    return saved_paths


def _normalize_images_input(inp: Dict[str, Any]) -> List[str]:
    raw = inp.get("images")
    if raw is None:
        raw = inp.get("image_urls")
    if raw is None:
        raw = inp.get("image")

    images: List[str] = []
    if isinstance(raw, list):
        images = [str(v).strip() for v in raw if str(v).strip()]
    elif isinstance(raw, str):
        text = raw.strip()
        if text:
            if text.startswith("[") and text.endswith("]"):
                try:
                    arr = json.loads(text)
                    if isinstance(arr, list):
                        images = [str(v).strip() for v in arr if str(v).strip()]
                except json.JSONDecodeError:
                    images = [x.strip() for x in text.split(",") if x.strip()]
            else:
                images = [x.strip() for x in text.split(",") if x.strip()]

    return images


def _validate_image_count(images: List[str]) -> None:
    if len(images) < 1:
        _json_error(False, "PARAM_ERROR", "缺少商品图", "请至少提供 1 张商品图")
    if len(images) > 3:
        _json_error(False, "PARAM_ERROR", "商品图最多支持 3 张", "请将商品图数量控制在 1~3 张后重试")


def upload_local_image(file_path: str) -> str:
    normalized_path = normalize_local_image_path(file_path)
    if not os.path.isfile(normalized_path):
        _json_error(False, "PARAM_ERROR", f"文件不存在: {normalized_path}", "请检查图片路径")

    try:
        _, mime = describe_local_image(normalized_path)
    except ValueError as exc:
        _json_error(False, "PARAM_ERROR", str(exc), "请提供 JPG/JPEG/PNG/WEBP/GIF 图片文件")

    fname = os.path.basename(normalized_path)

    getsign_url = f"{WEBAPI_BASE}/maat/getsign?type=openclaw"
    code, resp = _http_request("GET", getsign_url, json_mode=False)
    if code < 200 or code >= 300 or not isinstance(resp, dict):
        _json_error(False, "UPLOAD_ERROR", "获取上传签名失败", "请检查网络连接或 API Key 后重试")
    if resp.get("code") != 0:
        _json_error(
            False,
            "UPLOAD_ERROR",
            "获取上传签名失败",
            "请检查网络连接或 API Key 后重试",
            {"result": sanitize_json_payload(resp)},
        )

    policy_url_full = str((resp.get("data") or {}).get("upload_url") or "").strip()
    if not policy_url_full:
        _json_error(False, "UPLOAD_ERROR", "获取上传签名失败", "请检查网络连接或 API Key 后重试")

    _request_log_as_curl(
        "GET",
        policy_url_full,
        {
            "Origin": "https://www.designkit.cn",
            "Referer": "https://www.designkit.cn/editor/",
        },
        None,
    )

    policy_req = urllib.request.Request(policy_url_full)
    policy_req.add_header("Origin", "https://www.designkit.cn")
    policy_req.add_header("Referer", "https://www.designkit.cn/editor/")

    try:
        with _urlopen(policy_req, timeout=30) as resp2:
            raw_policy = resp2.read().decode("utf-8", errors="replace")
            http_code = resp2.getcode() or 200
            _request_log_response_json("policy_response_body", raw_policy, http_code)
            if http_code < 200 or http_code >= 300:
                _json_error(False, "UPLOAD_ERROR", "获取上传策略失败", "请检查网络连接后重试")
            arr = json.loads(raw_policy)
    except Exception as exc:  # pylint: disable=broad-except
        _json_error(False, "UPLOAD_ERROR", str(exc), "获取上传策略失败，请检查网络")

    provider = arr[0]["order"][0]
    p = arr[0][provider]
    token = p["token"]
    key = p["key"]
    up_url = p["url"]
    up_data = p.get("data")

    boundary = uuid.uuid4().hex.encode("utf-8")
    with open(normalized_path, "rb") as handle:
        file_bytes = handle.read()

    def part(name: str, value: str) -> bytes:
        return (
            b"--"
            + boundary
            + b'\r\nContent-Disposition: form-data; name="'
            + name.encode("utf-8")
            + b'"\r\n\r\n'
            + value.encode("utf-8")
            + b"\r\n"
        )

    post_body = (
        part("token", token)
        + part("key", key)
        + part("fname", fname)
        + b"--"
        + boundary
        + b'\r\nContent-Disposition: form-data; name="file"; filename="'
        + fname.encode("utf-8")
        + b'"\r\nContent-Type: '
        + mime.encode("utf-8")
        + b"\r\n\r\n"
        + file_bytes
        + b"\r\n--"
        + boundary
        + b"--\r\n"
    )

    upload_target = f"{up_url}/"
    _request_log_as_curl_multipart(upload_target, normalized_path, fname, mime)

    up_req = urllib.request.Request(upload_target, data=post_body, method="POST")
    up_req.add_header("Content-Type", f"multipart/form-data; boundary={boundary.decode('utf-8')}")
    up_req.add_header("Origin", "https://www.designkit.cn")
    up_req.add_header("Referer", "https://www.designkit.cn/editor/")

    try:
        with _urlopen(up_req, timeout=120) as up_resp:
            raw_up = up_resp.read().decode("utf-8", errors="replace")
            http_code = up_resp.getcode() or 200
            _request_log_response_json("upload_response_body", raw_up, http_code)
            up_json = json.loads(raw_up)
    except Exception as exc:  # pylint: disable=broad-except
        _json_error(False, "UPLOAD_ERROR", str(exc), "上传失败，请换图或稍后重试")

    cdn = up_json.get("data") or up_data
    if not cdn:
        _json_error(False, "UPLOAD_ERROR", "无 CDN URL", "上传响应异常")

    return str(cdn)


def resolve_image_urls(images: List[str]) -> List[str]:
    _validate_image_count(images)
    resolved: List[str] = []
    for image in images:
        image = image.strip()
        if re.match(r"^https?://", image, re.I):
            resolved.append(image)
        else:
            resolved.append(upload_local_image(image))
    return resolved


def _extract_json_object_from_text(text: str) -> Optional[Dict[str, Any]]:
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    first = text.find("{")
    if first < 0:
        return None

    for end in range(len(text) - 1, first, -1):
        if text[end] != "}":
            continue
        candidate = text[first : end + 1]
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            continue
    return None


def _parse_selected_modules(raw: Any) -> Tuple[List[str], str]:
    if raw is None:
        modules = DEFAULT_SELECTED_MODULES[:]
    elif isinstance(raw, list):
        modules = [str(v).strip() for v in raw if str(v).strip()]
    elif isinstance(raw, str):
        modules = [x.strip() for x in raw.split(",") if x.strip()]
    else:
        modules = []

    if not modules:
        modules = DEFAULT_SELECTED_MODULES[:]

    return modules, ",".join(modules)


def _build_full_prompt(image_type: str, image_prompt: str, copy_requirements: str, aspect_ratio: str) -> str:
    if "--ar" in copy_requirements:
        final_copy = copy_requirements
    else:
        final_copy = (copy_requirements + "\n" if copy_requirements else "") + f"--ar {aspect_ratio}"

    return json.dumps(
        {
            "image_type": image_type,
            "picture_requirement": image_prompt,
            "copywriting_requirements": final_copy,
        },
        ensure_ascii=False,
    )


def _ensure_prompt_has_aspect(prompt: str, aspect_ratio: str) -> str:
    try:
        data = json.loads(prompt)
        if isinstance(data, dict):
            copy = str(data.get("copywriting_requirements", "")).strip()
            if "--ar" not in copy:
                data["copywriting_requirements"] = (copy + "\n" if copy else "") + f"--ar {aspect_ratio}"
            return json.dumps(data, ensure_ascii=False)
    except json.JSONDecodeError:
        pass

    if "--ar" not in prompt:
        return prompt + "\n" + f"--ar {aspect_ratio}"
    return prompt


def _parse_modules_for_render(inp: Dict[str, Any], aspect_ratio: str) -> List[Dict[str, str]]:
    params = inp.get("params")
    if isinstance(params, list) and params:
        out: List[Dict[str, str]] = []
        for i, item in enumerate(params, start=1):
            if not isinstance(item, dict):
                continue
            label = str(item.get("label") or f"模块{i}").strip()
            prompt = str(item.get("prompt") or "").strip()
            if not label or not prompt:
                continue
            out.append({"label": label, "prompt": _ensure_prompt_has_aspect(prompt, aspect_ratio)})
        if out:
            return out

    modules = inp.get("modules")
    if isinstance(modules, list) and modules:
        out2: List[Dict[str, str]] = []
        for i, item in enumerate(modules, start=1):
            if not isinstance(item, dict):
                continue
            if item.get("prompt"):
                label = str(item.get("label") or item.get("image_type") or f"模块{i}").strip()
                prompt = str(item.get("prompt") or "").strip()
                if label and prompt:
                    out2.append({"label": label, "prompt": _ensure_prompt_has_aspect(prompt, aspect_ratio)})
                continue

            image_type = str(item.get("image_type") or item.get("label") or f"模块{i}").strip()
            image_prompt = str(item.get("image_prompt") or item.get("picture_requirement") or "").strip()
            copy_requirements = str(item.get("copy_requirements") or item.get("copywriting_requirements") or "").strip()
            if not image_type:
                continue
            out2.append(
                {
                    "label": image_type,
                    "prompt": _build_full_prompt(image_type, image_prompt, copy_requirements, aspect_ratio),
                }
            )
        if out2:
            return out2

    _json_error(False, "PARAM_ERROR", "缺少 modules/params", "请先完成 detail_plan_poll 并传入模块结果")
    return []


def _extract_task_id(resp: Any) -> str:
    if not isinstance(resp, dict):
        return ""
    data = resp.get("data") if isinstance(resp.get("data"), dict) else {}
    for key in ("task_id", "id"):
        val = data.get(key)
        if isinstance(val, str) and val:
            return val
    for key in ("task_id", "id"):
        val = resp.get(key)
        if isinstance(val, str) and val:
            return val
    return ""


def _extract_batch_id(resp: Any) -> str:
    if not isinstance(resp, dict):
        return ""
    data = resp.get("data") if isinstance(resp.get("data"), dict) else {}
    for key in ("batch_id", "batchId"):
        val = data.get(key)
        if isinstance(val, str) and val:
            return val
    for key in ("batch_id", "batchId"):
        val = resp.get(key)
        if isinstance(val, str) and val:
            return val
    return ""


def _api_code(resp: Any) -> Optional[int]:
    if not isinstance(resp, dict):
        return None
    code = resp.get("code")
    return int(code) if isinstance(code, int) else (int(code) if isinstance(code, str) and code.isdigit() else None)


def _api_message(resp: Any) -> str:
    if isinstance(resp, dict):
        return str(resp.get("message", "")).strip()
    return ""


def cmd_detail_plan_submit(inp: Dict[str, Any]) -> None:
    images = _normalize_images_input(inp)
    product_info = str(inp.get("product_info", "")).strip()
    if not product_info:
        _json_error(False, "PARAM_ERROR", "缺少 product_info", "请提供商品卖点和要求")

    platform = str(inp.get("platform", "amazon")).strip() or "amazon"
    market = str(inp.get("market", "US")).strip() or "US"
    language = str(inp.get("language", "English")).strip() or "English"
    aspect_ratio = str(inp.get("aspect_ratio", inp.get("ratio", DEFAULT_ASPECT_RATIO))).strip() or DEFAULT_ASPECT_RATIO
    client_language = str(inp.get("client_language", os.environ.get("DESIGNKIT_CLIENT_LANGUAGE", "zh-Hans"))).strip() or "zh-Hans"

    selected_modules, selected_modules_str = _parse_selected_modules(inp.get("selected_modules"))
    resolved = resolve_image_urls(images)

    params_obj = {
        "product_info": product_info,
        "platform": platform,
        "market": market,
        "language": language,
        "selected_modules": selected_modules_str,
        "client_language": client_language,
        "aspect_ratio": aspect_ratio,
        "proportion": aspect_ratio,
    }

    body_obj = {
        "images": ",".join(resolved),
        "params": json.dumps(params_obj, ensure_ascii=False),
        "step": 3,
    }

    code, resp = _http_request("POST", _url("/v1/hackathon/ai_model/prompt_submit"), json.dumps(body_obj, ensure_ascii=False).encode("utf-8"))

    if code != 200:
        _json_error(False, "API_ERROR", f"HTTP {code}", "提交详情策划任务失败", {"http_code": code, "result": resp})

    api_code = _api_code(resp)
    if api_code != 0:
        _json_error(False, "API_ERROR", _api_message(resp) or "提交详情策划任务失败", "请检查输入后重试", {"result": resp})

    task_id = _extract_task_id(resp)
    if not task_id:
        _json_error(False, "API_ERROR", "提交成功但未返回 task_id", "请稍后重试", {"result": resp})

    print(
        json.dumps(
            {
                "ok": True,
                "command": "detail_plan_submit",
                "task_id": task_id,
                "images": resolved,
                "selected_modules": selected_modules,
                "result": resp,
            },
            ensure_ascii=False,
        )
    )


def cmd_detail_plan_poll(inp: Dict[str, Any]) -> None:
    task_id = str(inp.get("task_id", "")).strip()
    if not task_id:
        _json_error(False, "PARAM_ERROR", "缺少 task_id", "请先执行 detail_plan_submit")

    max_wait = float(inp.get("max_wait_sec", 180))
    interval = float(inp.get("interval_sec", 2))
    deadline = time.time() + max_wait

    while time.time() < deadline:
        url = _url("/v1/mtlab/k2_query", {"task_id": task_id})
        code, resp = _http_request("GET", url, json_mode=False)
        if code != 200:
            _json_error(False, "API_ERROR", f"HTTP {code}", "查询详情策划任务失败", {"http_code": code, "result": resp})

        api_code = _api_code(resp)
        if api_code != 0:
            _json_error(False, "API_ERROR", _api_message(resp) or "查询详情策划任务失败", "请稍后重试", {"result": resp})

        data = resp.get("data") if isinstance(resp, dict) else None
        status = (data or {}).get("status") if isinstance(data, dict) else None
        result = (data or {}).get("result") if isinstance(data, dict) else None

        if result:
            message = ""
            if isinstance(result, dict):
                raw_message = result.get("message", "")
                if isinstance(raw_message, str):
                    message = raw_message.strip()
                elif raw_message:
                    message = json.dumps(raw_message, ensure_ascii=False)
            elif isinstance(result, str):
                message = result.strip()

            parsed: Optional[Dict[str, Any]] = None
            if message:
                parsed = _extract_json_object_from_text(message)

            if not isinstance(parsed, dict):
                if status in (4, "4"):
                    _json_error(
                        False,
                        "API_ERROR",
                        "详情策划结果解析失败",
                        "策划结果返回格式异常，请重试",
                        {"task_id": task_id, "status": status, "message_raw": message, "result": resp},
                    )
                time.sleep(interval)
                continue

            modules = parsed.get("modules")
            if not isinstance(modules, list):
                modules = []

            print(
                json.dumps(
                    {
                        "ok": True,
                        "command": "detail_plan_poll",
                        "done": True,
                        "task_id": task_id,
                        "status": status,
                        "plan": parsed,
                        "modules": modules,
                        "message_raw": message,
                        "result": resp,
                    },
                    ensure_ascii=False,
                )
            )
            return

        time.sleep(interval)

    _json_error(
        False,
        "TEMPORARY_UNAVAILABLE",
        "详情策划轮询超时",
        f"在 {max_wait}s 内未完成，可增大 max_wait_sec 后重试",
        {"task_id": task_id},
    )


def _default_name(product_info: str) -> str:
    first_line = product_info.strip().splitlines()[0] if product_info.strip() else ""
    return first_line[:40] if first_line else "A+ Detail Product"


def _build_custom_ext(
    name: str,
    product_info: str,
    platform: str,
    market: str,
    language: str,
    aspect_ratio: str,
    selected_modules_str: str,
) -> str:
    payload = {
        "target_platform": platform,
        "target_market": market,
        "language": language,
        "proportion": aspect_ratio,
        "name": name,
        "sizeMode": "standard",
        "aspectRatios": [aspect_ratio],
        "fileName": _safe_filename_part(name, "product_detail"),
        "productInfo": product_info,
        "core_point_type": "ai_writing",
        "selected_modules": selected_modules_str,
        "is_modify_setting": False,
    }
    return json.dumps(payload, ensure_ascii=False)


def cmd_detail_render_submit(inp: Dict[str, Any]) -> None:
    images = _normalize_images_input(inp)
    resolved = resolve_image_urls(images)

    product_info = str(inp.get("product_info", "")).strip()
    if not product_info:
        _json_error(False, "PARAM_ERROR", "缺少 product_info", "请提供商品卖点和要求")

    aspect_ratio = str(inp.get("aspect_ratio", inp.get("ratio", DEFAULT_ASPECT_RATIO))).strip() or DEFAULT_ASPECT_RATIO
    platform = str(inp.get("platform", "amazon")).strip() or "amazon"
    market = str(inp.get("market", "US")).strip() or "US"
    language = str(inp.get("language", "English")).strip() or "English"

    selected_modules, selected_modules_str = _parse_selected_modules(inp.get("selected_modules"))
    render_params = _parse_modules_for_render(inp, aspect_ratio)

    name = _default_name(product_info)
    custom_ext = _build_custom_ext(name, product_info, platform, market, language, aspect_ratio, selected_modules_str)
    transfer_id = str(uuid.uuid4()).upper()

    body_obj = {
        "name": name,
        "image_urls": resolved,
        "sizes": [],
        "params": render_params,
        "custom_ext": custom_ext,
    }

    code, resp = _http_request(
        "POST",
        _url("/v1/hackathon/ai_product_detail/task_submit", {"transfer_id": transfer_id}),
        json.dumps(body_obj, ensure_ascii=False).encode("utf-8"),
    )

    if code != 200:
        _json_error(False, "API_ERROR", f"HTTP {code}", "提交详情图任务失败", {"http_code": code, "result": resp})

    api_code = _api_code(resp)
    if api_code != 0:
        _json_error(False, "API_ERROR", _api_message(resp) or "提交详情图任务失败", "请检查输入后重试", {"result": resp})

    batch_id = _extract_batch_id(resp)
    if not batch_id:
        _json_error(False, "API_ERROR", "提交成功但未返回 batch_id", "请稍后重试", {"result": resp})

    print(
        json.dumps(
            {
                "ok": True,
                "command": "detail_render_submit",
                "transfer_id": transfer_id,
                "batch_id": batch_id,
                "images": resolved,
                "selected_modules": selected_modules,
                "result": resp,
            },
            ensure_ascii=False,
        )
    )


def cmd_detail_render_regen(inp: Dict[str, Any]) -> None:
    task_id = str(inp.get("task_id", "")).strip()
    if not task_id:
        _json_error(False, "PARAM_ERROR", "缺少 task_id", "请提供要重生成的 task_id")

    body = urllib.parse.urlencode({"task_id": task_id}).encode("utf-8")
    code, resp = _http_request(
        "POST",
        _url("/v1/hackathon/regen"),
        body,
        json_mode=False,
        extra_headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if code != 200:
        _json_error(False, "API_ERROR", f"HTTP {code}", "提交重生成任务失败", {"http_code": code, "result": resp})

    api_code = _api_code(resp)
    if api_code is not None and api_code != 0:
        _json_error(False, "API_ERROR", _api_message(resp) or "提交重生成任务失败", "请稍后重试", {"result": resp})

    batch_id = _extract_batch_id(resp)
    new_task_id = _extract_task_id(resp) or task_id

    print(
        json.dumps(
            {
                "ok": True,
                "command": "detail_render_regen",
                "task_id": new_task_id,
                "batch_id": batch_id,
                "result": resp,
            },
            ensure_ascii=False,
        )
    )


def _collect_render_items(
    resp: Any,
) -> Tuple[int, int, int, List[str], List[Dict[str, Any]], Dict[str, Any]]:
    total = 0
    done = 0
    running = 0
    urls: List[str] = []
    items: List[Dict[str, Any]] = []
    batches: Dict[str, Any] = {}

    if not isinstance(resp, dict):
        return total, done, running, urls, items, batches

    data = resp.get("data")
    if not isinstance(data, dict):
        return total, done, running, urls, items, batches

    items_map = data.get("items")
    if not isinstance(items_map, dict):
        return total, done, running, urls, items, batches

    batches = items_map

    for batch_id, batch_obj in items_map.items():
        if not isinstance(batch_obj, dict):
            continue
        sub_items = batch_obj.get("items")
        if not isinstance(sub_items, list):
            continue

        for item in sub_items:
            if not isinstance(item, dict):
                continue
            task_item = dict(item)
            task_item["batch_id"] = batch_id
            items.append(task_item)
            total += 1

            status = item.get("status")
            if isinstance(status, str) and status.isdigit():
                status = int(status)
            if status is None:
                status = 29901

            res_img = str(item.get("res_img", "")).strip()
            if status == 0 and res_img.startswith("http"):
                done += 1
                urls.append(res_img)
            elif status == 29901:
                running += 1

    return total, done, running, list(dict.fromkeys(urls)), items, batches


def cmd_detail_render_poll(inp: Dict[str, Any]) -> None:
    batch_id = str(inp.get("batch_id", "")).strip()
    if not batch_id:
        _json_error(False, "PARAM_ERROR", "缺少 batch_id", "请先执行 detail_render_submit 或 detail_render_regen")

    output_dir = resolve_output_dir(inp)
    product_name = str(inp.get("name", "")).strip() or str(inp.get("product_name", "")).strip() or "a_plus_product"
    max_wait = float(inp.get("max_wait_sec", 600))
    interval = float(inp.get("interval_sec", 3))
    deadline = time.time() + max_wait

    last_progress: Optional[Tuple[int, int]] = None

    while time.time() < deadline:
        code, resp = _http_request("GET", _url("/v1/hackathon/query", {"batch_id": batch_id}), json_mode=False)
        if code != 200:
            _json_error(False, "API_ERROR", f"HTTP {code}", "查询详情图结果失败", {"http_code": code, "result": resp})

        api_code = _api_code(resp)
        if api_code != 0:
            _json_error(False, "API_ERROR", _api_message(resp) or "查询详情图结果失败", "请稍后重试", {"result": resp})

        total, done, running, media_urls, items, batches = _collect_render_items(resp)

        if total > 0:
            progress = (done, total)
            if progress != last_progress:
                last_progress = progress
                done_labels = [
                    str(it.get("label", "")).strip()
                    for it in items
                    if str(it.get("res_img", "")).strip().startswith("http")
                ]
                hint = f"（{'、'.join(done_labels[-3:])}）" if done_labels else ""
                print(f"[PROGRESS] {done}/{total}{hint}", file=sys.stderr)

        if total > 0 and done >= total:
            local_paths = _save_result_images(items, output_dir, product_name)
            print(
                json.dumps(
                    {
                        "ok": True,
                        "command": "detail_render_poll",
                        "done": True,
                        "batch_id": batch_id,
                        "media_urls": media_urls,
                        "output_dir": str(output_dir),
                        "local_paths": local_paths,
                        "items": items,
                        "batches": batches,
                        "result": resp,
                    },
                    ensure_ascii=False,
                )
            )
            return

        # 终态失败：存在未完成项且已无 running（running 仅认 29901）
        if total > 0 and done < total and running == 0:
            failed_items: List[Dict[str, Any]] = []
            for item in items:
                status = item.get("status")
                if isinstance(status, str) and status.isdigit():
                    status = int(status)
                if status == 0 and str(item.get("res_img", "")).strip().startswith("http"):
                    continue
                failed_items.append(
                    {
                        "task_id": item.get("task_id"),
                        "label": item.get("label"),
                        "status": status,
                        "batch_id": item.get("batch_id"),
                    }
                )

            _json_error(
                False,
                "API_ERROR",
                "详情图任务失败",
                "任务已进入失败终态，请根据失败 status 排查参数或尝试重生成",
                {
                    "batch_id": batch_id,
                    "done": done,
                    "total": total,
                    "failed_items": failed_items,
                    "result": resp,
                },
            )

        time.sleep(interval)

    _json_error(
        False,
        "TEMPORARY_UNAVAILABLE",
        "详情图轮询超时",
        f"在 {max_wait}s 内未拿到全部图片，可增大 max_wait_sec",
        {"batch_id": batch_id},
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="DesignKit A+详情页执行器")
    parser.add_argument(
        "command",
        choices=(
            "detail_plan_submit",
            "detail_plan_poll",
            "detail_render_submit",
            "detail_render_regen",
            "detail_render_poll",
        ),
    )
    parser.add_argument("--input-json", required=True, help="JSON 参数字符串")
    args = parser.parse_args()

    try:
        inp = json.loads(args.input_json)
    except json.JSONDecodeError as exc:
        _json_error(False, "PARAM_ERROR", str(exc), "--input-json 必须是合法 JSON")

    if not isinstance(inp, dict):
        _json_error(False, "PARAM_ERROR", "根节点须为 JSON 对象", "")

    if args.command == "detail_plan_submit":
        cmd_detail_plan_submit(inp)
    elif args.command == "detail_plan_poll":
        cmd_detail_plan_poll(inp)
    elif args.command == "detail_render_submit":
        cmd_detail_render_submit(inp)
    elif args.command == "detail_render_regen":
        cmd_detail_render_regen(inp)
    else:
        cmd_detail_render_poll(inp)


if __name__ == "__main__":
    main()
