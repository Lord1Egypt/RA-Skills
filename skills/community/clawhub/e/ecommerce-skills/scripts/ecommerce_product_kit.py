#!/usr/bin/env python3
"""
Designkit ecommerce listing kit runner.
Web API base defaults to production, and auth behavior is aligned with run_command.sh.

Environment variables:
- DESIGNKIT_OPENCLAW_AK: required request header X-Openclaw-AK
- DESIGNKIT_OPENCLAW_AK_URL: credits/check page URL, default https://www.designkit.com/openClaw (used in user-facing hints)
- DESIGNKIT_WEBAPI_BASE: base domain only (without version prefix), default https://openclaw-designkit-api.meitu.com
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from openclaw_safety import detect_local_image, summarize_http_request, summarize_json_text

# Can be overridden by DESIGNKIT_WEBAPI_BASE.
# Base domain only; version prefix is not auto-appended.
_webapi_base_raw = os.environ.get(
    "DESIGNKIT_WEBAPI_BASE",
    "https://openclaw-designkit-api.meitu.com",
).rstrip("/")
WEBAPI_BASE = re.sub(r"/v1/?$", "", _webapi_base_raw)

DEFAULT_OPENCLAW_AK_URL = "https://www.designkit.com/openClaw"


def _openclaw_ak_url() -> str:
    return os.environ.get("DESIGNKIT_OPENCLAW_AK_URL", DEFAULT_OPENCLAW_AK_URL).strip() or DEFAULT_OPENCLAW_AK_URL


def _request_log_enabled() -> bool:
    return os.environ.get("OPENCLAW_REQUEST_LOG", "0") != "0"


def _request_log(message: str) -> None:
    if _request_log_enabled():
        print(f"[REQUEST] {message}", file=sys.stderr)


def _request_log_http_summary(
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Optional[bytes] = None,
    *,
    multipart_hint: Optional[str] = None,
    timeout: int = 120,
) -> None:
    if not _request_log_enabled():
        return
    summary = summarize_http_request(
        method,
        url,
        headers,
        data=data,
        multipart_hint=multipart_hint,
        timeout=timeout,
    )
    print("[REQUEST] request (summary):", file=sys.stderr)
    print(json.dumps(summary, ensure_ascii=False, indent=2), file=sys.stderr)


def _request_log_response_json(
    label: str,
    text: str,
    http_code: Optional[int] = None,
) -> None:
    if not _request_log_enabled():
        return
    try:
        max_len = int(os.environ.get("OPENCLAW_REQUEST_LOG_BODY_MAX", "20000"))
    except ValueError:
        max_len = 20000
    envelope = summarize_json_text(
        text,
        ak=os.environ.get("DESIGNKIT_OPENCLAW_AK", "").strip(),
        http_code=http_code,
        max_len=max_len,
    )
    pretty = json.dumps(envelope, ensure_ascii=False, indent=2)
    print(f"[REQUEST] {label} (summary):", file=sys.stderr)
    print(pretty, file=sys.stderr)

# Style generation prompt template.
STYLE_PROMPT_HEAD = (
    "\nYou are an ecommerce visual art director with strong expertise in category-specific visual direction and style consistency.\n\n[Input]\n"
    "- Product: {product_info}\n- Platform: {platform}\n- Target market: {market}\n\n[Market Aesthetic Reference]\n\n"
    "        [Target market: {market_label}]\n"
    "        - **Visual preference**: high contrast, vivid and impactful, strong commercial appeal, direct and clear\n"
    "        - **Environment references**: modern style, industrial elements, open space, abundant natural light\n"
    "        - **Color direction**: bright and saturated, warm palette, commercially trendy look\n"
    "    \n\n[Platform Style]\n"
    "- **China ecommerce** (Taobao/JD/Douyin/Pinduoduo): stronger visual impact, colorful or gradient background allowed, conversion-oriented attraction\n"
    "- **Global ecommerce** (Amazon/Temu/TikTok/Shopee/AliExpress/Alibaba/OZON/Shopify): restrained and premium, emphasizing realism and quality\n\n[Task]\n"
    "Generate **4 clearly differentiated** commercial photography style concepts for this product. Each concept should be reusable across a 7-image listing set.\n\n[Category Style Guidance]\n"
    "Adjust to product category naturally; avoid rigid templates:\n"
    "- Tech products -> even soft lighting, clean negative space, neutral tones\n"
    "- Gaming devices -> side/transmitted light, dark background, cool and powerful mood\n"
    "- Home products -> natural warm light, soft transparency, lifestyle warmth\n"
    "- Sports gear -> natural light, bright and crisp, energetic feeling\n"
    "- Fashion accessories -> soft side light, refined texture, elegant restraint\n"
    "- Beauty/skincare -> even soft light, clean luminosity, polished detail\n\n[Core Rules]\n"
    "1. **Photorealistic style only**: no illustration styles such as oil painting, watercolor, anime, or sketch\n"
    "2. **globalStyleNote format**:\n"
    "   - light + atmosphere keywords only, 15-25 words\n"
    "   - Allowed example: \"natural warm light, 45-degree soft diffusion, airy and gentle atmosphere\"\n"
    "   - Forbidden: scene/object/background/prop descriptions\n"
    "3. **Keep product colors realistic**: avoid extreme color temperatures (<2700K or >6500K) and heavy filters\n"
    "4. **First color in colorPalette**: must be the product's inherent color (for example green sofa -> green)\n"
    "5. **Typography safety line**: no thin script/calligraphy/handwriting styles, and do not output specific font names\n"
    "6. **Global reusability**: each style must serve as a unified base for all 7 listing images with only scene-detail adjustments\n"
    "7. **Conversion-oriented**: style must improve perceived product value and buyer trust\n\n[Output Format]\n"
    "Output a pure JSON array in English only. Each object must include:\n\n"
    "| Field | Description | Example |\n"
    "|------|------|------|\n"
    "| name | Style name (2-4 words, easy to understand) | \"Warm Home Comfort\" \"Clean Pro Minimal\" |\n"
    "| reasoning | Why this style (<=15 words, conversational) | \"Makes the sofa feel cozy and premium\" |\n"
    "| globalStyleNote | Light + atmosphere keywords (15-25 words) | \"natural warm light, 45-degree soft diffusion, airy and clean\" |\n"
    "| fontStyleDescription | Typography visual traits | \"bold sans-serif, medium weight, modern commercial tone\" |\n"
    "| colorPalette | 3 hex values (product + background + accent) | \"#2ECC71, #F8F9FA, #FF6B6B\" |\n"
    "| colorDescription | Color usage explanation | \"forest green (product), mist white (background), coral red (accent)\" |\n"
    "| iconStyle | Icon style description | \"bold linear minimalist icons\" |\n\n[Pre-output Checklist]\n"
    "- [ ] globalStyleNote contains only light/atmosphere keywords, 15-25 words, no scene/object/background description\n"
    "- [ ] Lighting setup will not distort product colors\n"
    "- [ ] fontStyleDescription is descriptive and includes no specific font names\n"
    "- [ ] First color in colorPalette is the product's inherent color\n"
    "- [ ] All 4 style concepts are visually distinct\n"
    "- [ ] name and reasoning are concise and easy to understand\n"
)

MARKET_LABEL = {
    "US": "United States",
    "CN": "China",
    "UK": "United Kingdom",
    "JP": "Japan",
    "DE": "Germany",
    "FR": "France",
    "AU": "Australia",
}


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
            "Missing DESIGNKIT_OPENCLAW_AK",
            f"Please visit {_openclaw_ak_url()} to get credits",
        )
    return ak


def _query_params() -> Dict[str, str]:
    return {
        "client_id": os.environ.get("DESIGNKIT_OPENCLAW_CLIENT_ID", "2288866678"),
        "client_language": os.environ.get("DESIGNKIT_CLIENT_LANGUAGE", "zh-Hans"),
        "channel": "",
        "country_code": os.environ.get("DESIGNKIT_COUNTRY_CODE", "CN"),
        "ts_random_id": str(uuid.uuid4()),
        "client_source": "pc",
        "client_timezone": os.environ.get("DESIGNKIT_CLIENT_TIMEZONE", "Asia/Shanghai"),
        "operate_source": "web",
    }


def _headers_json() -> Dict[str, str]:
    ak = _require_ak()
    return {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.designkit.cn",
        "Referer": "https://www.designkit.cn/product-kit/?from=home",
        "X-Openclaw-AK": ak,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }


def _headers_get() -> Dict[str, str]:
    h = _headers_json()
    del h["Content-Type"]
    return h


def _url(path: str, extra: Optional[Dict[str, str]] = None) -> str:
    from urllib.parse import urlencode

    q = _query_params()
    if extra:
        q = {**q, **extra}
    return f"{WEBAPI_BASE}{path}?{urlencode(q)}"


def _http_request(
    method: str,
    url: str,
    body: Optional[bytes] = None,
    json_mode: bool = True,
) -> Tuple[int, Any]:
    headers = _headers_json() if json_mode and body else _headers_get()
    if body and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
    _request_log_http_summary(method, url, headers, body, timeout=120)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            code = resp.getcode() or 200
            _request_log_response_json("response_body", raw, code)
            try:
                return code, json.loads(raw)
            except json.JSONDecodeError:
                return code, {"_raw": raw}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        _request_log_response_json("response_body", raw, e.code)
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, {"_raw": raw, "_http_message": str(e)}


def _suffix_mime(path: str) -> Tuple[str, str]:
    return detect_local_image(path)


def upload_local_image(file_path: str) -> str:
    if not os.path.isfile(file_path):
        _json_error(False, "PARAM_ERROR", f"File not found: {file_path}", "Please check the image path")

    try:
        _, mime = _suffix_mime(file_path)
    except ValueError as exc:
        _json_error(False, "PARAM_ERROR", str(exc), "Please provide a valid local JPG, PNG, WEBP, or GIF image")
    fname = os.path.basename(file_path)

    getsign_url = f"{WEBAPI_BASE}/maat/getsign?type=openclaw"
    getsign_code, getsign_resp = _http_request("GET", getsign_url, json_mode=False)
    if getsign_code < 200 or getsign_code >= 300 or not isinstance(getsign_resp, dict):
        _json_error(False, "UPLOAD_ERROR", "Failed to get upload signature", "Please check your network or API key and retry")
    if getsign_resp.get("code") != 0:
        _request_log(f"maat getsign rejected: {json.dumps(getsign_resp, ensure_ascii=False)}")
        _json_error(False, "UPLOAD_ERROR", "Failed to get upload signature", "Please check your network or API key and retry")

    policy_url_full = str((getsign_resp.get("data") or {}).get("upload_url") or "").strip()
    if not policy_url_full:
        _request_log(f"maat getsign missing upload_url: {json.dumps(getsign_resp, ensure_ascii=False)}")
        _json_error(False, "UPLOAD_ERROR", "Failed to get upload signature", "Please check your network or API key and retry")

    _request_log_http_summary(
        "GET",
        policy_url_full,
        {
            "Origin": "https://www.designkit.cn",
            "Referer": "https://www.designkit.cn/editor/",
        },
        None,
        timeout=30,
    )
    policy_req = urllib.request.Request(policy_url_full)
    policy_req.add_header("Origin", "https://www.designkit.cn")
    policy_req.add_header("Referer", "https://www.designkit.cn/editor/")
    try:
        with urllib.request.urlopen(policy_req, timeout=30) as resp:
            code = resp.getcode() or 200
            raw_policy = resp.read().decode()
            _request_log_response_json("policy_response_body", raw_policy, code)
            if code < 200 or code >= 300:
                _json_error(False, "UPLOAD_ERROR", "Failed to get upload policy", "Please check your network and retry")
            arr = json.loads(raw_policy)
    except Exception as e:
        _json_error(False, "UPLOAD_ERROR", str(e), "Failed to get upload policy. Please check your network")

    provider = arr[0]["order"][0]
    p = arr[0][provider]
    token, key, up_url, up_data = p["token"], p["key"], p["url"], p["data"]

    boundary = uuid.uuid4().hex.encode()
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    def part(name: str, value: str) -> bytes:
        return (
            b"--"
            + boundary
            + b'\r\nContent-Disposition: form-data; name="'
            + name.encode()
            + b'"\r\n\r\n'
            + value.encode()
            + b"\r\n"
        )

    post_body = (
        part("token", token)
        + part("key", key)
        + part("fname", fname)
        + b"--"
        + boundary
        + b'\r\nContent-Disposition: form-data; name="file"; filename="'
        + fname.encode()
        + b'"\r\nContent-Type: '
        + mime.encode()
        + b"\r\n\r\n"
        + file_bytes
        + b"\r\n--"
        + boundary
        + b"--\r\n"
    )

    upload_target = f"{up_url}/"
    _request_log_http_summary(
        "POST",
        upload_target,
        {
            "Content-Type": f"multipart/form-data; boundary={boundary.decode()}",
            "Origin": "https://www.designkit.cn",
            "Referer": "https://www.designkit.cn/editor/",
        },
        None,
        multipart_hint=f"file=@<local-file>;type={mime}",
        timeout=120,
    )
    up_req = urllib.request.Request(upload_target, data=post_body, method="POST")
    up_req.add_header("Content-Type", f"multipart/form-data; boundary={boundary.decode()}")
    up_req.add_header("Origin", "https://www.designkit.cn")
    up_req.add_header("Referer", "https://www.designkit.cn/editor/")
    try:
        with urllib.request.urlopen(up_req, timeout=120) as resp:
            ucode = resp.getcode() or 200
            raw_up = resp.read().decode()
            _request_log_response_json("upload_response_body", raw_up, ucode)
            up_json = json.loads(raw_up)
    except Exception as e:
        _json_error(False, "UPLOAD_ERROR", str(e), "Upload failed. Please try another image or retry later")

    cdn = up_json.get("data") or up_data
    if not cdn:
        _request_log("upload response: no CDN URL in body")
        _json_error(False, "UPLOAD_ERROR", "No CDN URL returned", "Unexpected upload response")
    _request_log(f"upload ok, cdn_url={cdn}")
    return str(cdn)


def resolve_image_url(image: str) -> str:
    image = (image or "").strip()
    if not image:
        _json_error(False, "PARAM_ERROR", "Missing image", "Please provide a product image URL or local path")
    if re.match(r"^https?://", image, re.I):
        return image
    return upload_local_image(image)


def extract_task_id(resp: Any) -> Optional[str]:
    if not isinstance(resp, dict):
        return None
    for path in (
        ("data", "task_id"),
        ("data", "id"),
        ("task_id",),
        ("id",),
    ):
        cur: Any = resp
        for k in path:
            if isinstance(cur, dict):
                cur = cur.get(k)
            else:
                cur = None
                break
        if isinstance(cur, str) and cur:
            return cur
    return None


def k2_done(resp: Any) -> Tuple[bool, Optional[str]]:
    """Return (is_done, text/result-string for style parsing)."""
    if not isinstance(resp, dict):
        return False, None
    data = resp.get("data")
    if not isinstance(data, dict):
        return False, None
    st = data.get("status")
    st_str = str(st).lower() if st is not None else ""
    if st in (0, 1, "0", "1") or st_str in ("pending", "running", "processing", "queue", "queued"):
        return False, None
    # Try direct text fields in data
    for key in ("result", "content", "text", "output", "message", "answer"):
        v = data.get(key)
        if isinstance(v, str) and v.strip():
            return True, v
    # Try nested text fields under data.result (for example data.result.message)
    result_obj = data.get("result")
    if isinstance(result_obj, dict):
        for key in ("message", "content", "text", "output", "answer"):
            v = result_obj.get(key)
            if isinstance(v, str) and v.strip():
                return True, v
    # If result is None, treat as not ready even when status >= 2
    if result_obj is None:
        return False, None
    # If result exists but no recognized text field, serialize full data as fallback
    is_terminal = (isinstance(st, int) and st >= 2) or st_str in (
        "2", "3", "success", "complete", "done", "finished",
    )
    if is_terminal:
        return True, json.dumps(data, ensure_ascii=False)
    return False, None


def extract_batch_media(resp: Any) -> List[str]:
    urls: List[str] = []
    if not isinstance(resp, dict):
        return urls
    data = resp.get("data") or resp

    def collect(obj: Any) -> None:
        if isinstance(obj, str) and obj.startswith("http"):
            urls.append(obj)
        elif isinstance(obj, dict):
            for k in ("url", "media_url", "image_url", "src"):
                v = obj.get(k)
                if isinstance(v, str) and v.startswith("http"):
                    urls.append(v)
            for v in obj.values():
                collect(v)
        elif isinstance(obj, list):
            for v in obj:
                collect(v)

    collect(data)
    return list(dict.fromkeys(urls))


def cmd_style_create(inp: Dict[str, Any]) -> None:
    image = resolve_image_url(str(inp.get("image", "")))
    product_info = str(inp.get("product_info", inp.get("selling_points", ""))).strip() or "Product"
    platform = str(inp.get("platform", "amazon")).strip()
    market = str(inp.get("market", "US")).strip()
    market_label = str(inp.get("market_label", "") or MARKET_LABEL.get(market.upper(), "United States"))
    api_engine = str(inp.get("api_engine", "doubao-seed-2.0-lite"))

    prompt = STYLE_PROMPT_HEAD.format(
        product_info=product_info,
        platform=platform,
        market=market,
        market_label=market_label,
    )
    body = json.dumps(
        {"api_engine": api_engine, "prompt": prompt, "images": image},
        ensure_ascii=False,
    ).encode()

    url = _url("/v1/mtlab/ai_text")
    code, resp = _http_request("POST", url, body)
    if code != 200:
        _json_error(
            False,
            "API_ERROR",
            f"HTTP {code}",
            f"Failed to create style task. Please visit {_openclaw_ak_url()} and verify DESIGNKIT_OPENCLAW_AK.",
            {"http_code": code, "result": resp},
        )

    task_id = extract_task_id(resp)
    out = {
        "ok": True,
        "command": "ecommerce_style_create",
        "task_id": task_id,
        "result": resp,
        "user_hint": "If task_id is empty, find task id from result and then poll k2_query.",
    }
    print(json.dumps(out, ensure_ascii=False))


def cmd_style_poll(inp: Dict[str, Any]) -> None:
    task_id = str(inp.get("task_id", "")).strip()
    if not task_id:
        _json_error(False, "PARAM_ERROR", "Missing task_id", "Run style_create first, or get task_id from the create response")

    max_wait = float(inp.get("max_wait_sec", 180))
    interval = float(inp.get("interval_sec", 2))
    deadline = time.time() + max_wait

    while time.time() < deadline:
        url = _url("/v1/mtlab/k2_query", {"task_id": task_id})
        code, resp = _http_request("GET", url)
        if code != 200:
            _json_error(
                False,
                "API_ERROR",
                f"HTTP {code}",
                "Failed to query style task",
                {"http_code": code, "result": resp},
            )

        done, text = k2_done(resp)
        if done and text:
            styles: Any = None
            try:
                # Model may output markdown-wrapped JSON.
                m = re.search(r"\[[\s\S]*\]", text)
                if m:
                    styles = json.loads(m.group(0))
            except json.JSONDecodeError:
                styles = None
            out = {
                "ok": True,
                "command": "ecommerce_style_poll",
                "done": True,
                "styles": styles,
                "styles_raw": text,
                "result": resp,
            }
            print(json.dumps(out, ensure_ascii=False))
            return

        time.sleep(interval)

    print(
        json.dumps(
            {
                "ok": False,
                "error_type": "TEMPORARY_UNAVAILABLE",
                "message": "Polling timed out",
                "user_hint": f"Not completed within {max_wait}s. Increase max_wait_sec and retry.",
                "task_id": task_id,
            },
            ensure_ascii=False,
        )
    )
    sys.exit(1)


def cmd_render_submit(inp: Dict[str, Any]) -> None:
    transfer_id = str(inp.get("transfer_id", "") or str(uuid.uuid4()).upper())
    image_urls = inp.get("image_urls")
    if not image_urls:
        one = inp.get("image")
        if one:
            image_urls = [resolve_image_url(str(one))]
    if not isinstance(image_urls, list) or not image_urls:
        _json_error(False, "PARAM_ERROR", "Missing image_urls", "Please provide image_urls array or a single image")

    resolved = [resolve_image_url(str(u)) if not re.match(r"^https?://", str(u), re.I) else str(u) for u in image_urls]

    brand_style = inp.get("brand_style")
    if brand_style is not None and not isinstance(brand_style, dict):
        _json_error(False, "PARAM_ERROR", "brand_style must be an object or omitted", "Provide style JSON or omit this field for server-side auto selection")

    style_name = str(inp.get("style_name", (brand_style or {}).get("name", "")))
    product_info = str(inp.get("product_info", "")).strip() or "Product"
    aspect_ratio = str(inp.get("aspect_ratio", "1:1"))
    language = str(inp.get("language", "English"))
    platform = str(inp.get("platform", "amazon"))
    market = str(inp.get("market", "US"))
    is_pro = bool(inp.get("is_pro", True))

    burial = inp.get("burial_point")
    if burial is None:
        burial = {
            "first_func": "product_kit",
            "page_name": "commerce",
            "target_platform": platform,
            "target_market": market,
            "language": language,
            "proportion": aspect_ratio,
            "fileName": "openclaw",
            "productInfo": product_info,
            "core_point_type": "customize",
            "is_pro": is_pro,
        }
    burial_str = burial if isinstance(burial, str) else json.dumps(burial, ensure_ascii=False)

    body_obj = {
        "image_urls": resolved,
        "style_name": style_name,
        "product_info": product_info,
        "aspect_ratio": aspect_ratio,
        "language": language,
        "platform": platform,
        "market": market,
        "is_pro": is_pro,
        "burial_point": burial_str,
    }
    if brand_style is not None:
        body_obj["brand_style"] = brand_style
    body = json.dumps(body_obj, ensure_ascii=False).encode()
    url = _url("/v1/hackathon/ai_product/task_submit", {"transfer_id": transfer_id})
    code, resp = _http_request("POST", url, body)
    if code != 200:
        _json_error(
            False,
            "API_ERROR",
            f"HTTP {code}",
            "Failed to submit render task",
            {"http_code": code, "result": resp},
        )

    batch_id = None
    if isinstance(resp, dict):
        batch_id = (
            resp.get("data", {}).get("batch_id")
            if isinstance(resp.get("data"), dict)
            else None
        ) or resp.get("batch_id")

    out = {
        "ok": True,
        "command": "ecommerce_render_submit",
        "transfer_id": transfer_id,
        "batch_id": batch_id,
        "result": resp,
        "user_hint": "If batch_id is empty, find it in result.data and then poll render_poll.",
    }
    print(json.dumps(out, ensure_ascii=False))


def _check_render_items(resp: Any) -> Tuple[int, int, List[str], List[Dict[str, Any]]]:
    """Parse per-item completion status in render response.
    Return (total, done_count, res_img_urls, items_list).
    """
    items_list: List[Dict[str, Any]] = []
    res_urls: List[str] = []
    if not isinstance(resp, dict):
        return 0, 0, res_urls, items_list
    data = resp.get("data", {})
    if not isinstance(data, dict):
        return 0, 0, res_urls, items_list
    items_map = data.get("items", {})
    if not isinstance(items_map, dict):
        return 0, 0, res_urls, items_list
    for batch_val in items_map.values():
        if not isinstance(batch_val, dict):
            continue
        sub_items = batch_val.get("items", [])
        if not isinstance(sub_items, list):
            continue
        for item in sub_items:
            if not isinstance(item, dict):
                continue
            items_list.append(item)
            res_img = (item.get("res_img") or "").strip()
            if res_img.startswith("http"):
                res_urls.append(res_img)
    return len(items_list), len(res_urls), res_urls, items_list


def cmd_render_poll(inp: Dict[str, Any]) -> None:
    batch_id = str(inp.get("batch_id", "")).strip()
    if not batch_id:
        _json_error(False, "PARAM_ERROR", "Missing batch_id", "Run render_submit first")

    max_wait = float(inp.get("max_wait_sec", 600))
    interval = float(inp.get("interval_sec", 3))
    deadline = time.time() + max_wait
    last_done = -1
    last_total = 0
    last_done_count = 0

    while time.time() < deadline:
        url = _url("/v1/hackathon/query", {"batch_id": batch_id})
        code, resp = _http_request("GET", url)
        if code != 200:
            _json_error(
                False,
                "API_ERROR",
                f"HTTP {code}",
                "Failed to query render result",
                {"http_code": code, "result": resp},
            )

        total, done_count, res_urls, items_list = _check_render_items(resp)
        last_total, last_done_count = total, done_count

        # Emit render progress.
        if total > 0 and done_count != last_done:
            last_done = done_count
            done_labels = [
                it.get("label", "")
                for it in items_list
                if isinstance(it, dict) and (it.get("res_img") or "").startswith("http")
            ]
            hint = " (" + ", ".join(done_labels[-3:]) + ")" if done_labels else ""
            print(f"[PROGRESS] {done_count}/{total}{hint}", file=sys.stderr)

        if total > 0 and done_count >= total:
            out = {
                "ok": True,
                "command": "ecommerce_render_poll",
                "done": True,
                "media_urls": res_urls,
                "items": items_list,
                "result": resp,
            }
            print(json.dumps(out, ensure_ascii=False))
            return

        time.sleep(interval)

    print(
        json.dumps(
            {
                "ok": False,
                "error_type": "TEMPORARY_UNAVAILABLE",
                "message": "Render polling timed out",
                "user_hint": f"Not all images were ready within {max_wait}s. Increase max_wait_sec and retry.",
                "batch_id": batch_id,
                "progress": f"{last_done_count}/{last_total}",
            },
            ensure_ascii=False,
        )
    )
    sys.exit(1)


def main() -> None:
    p = argparse.ArgumentParser(description="Designkit ecommerce listing kit webapi runner")
    p.add_argument(
        "command",
        choices=("style_create", "style_poll", "render_submit", "render_poll"),
    )
    p.add_argument("--input-json", required=True, help="JSON argument string")
    args = p.parse_args()
    try:
        inp = json.loads(args.input_json)
    except json.JSONDecodeError as e:
        _json_error(False, "PARAM_ERROR", str(e), "--input-json must be valid JSON")

    if not isinstance(inp, dict):
        _json_error(False, "PARAM_ERROR", "Root node must be a JSON object", "")

    if args.command == "style_create":
        cmd_style_create(inp)
    elif args.command == "style_poll":
        cmd_style_poll(inp)
    elif args.command == "render_submit":
        cmd_render_submit(inp)
    else:
        cmd_render_poll(inp)


if __name__ == "__main__":
    main()
