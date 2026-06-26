#!/usr/bin/env python3
"""
通过乐享 OpenAPI 上传视频/音频到知识库，产生可播放的 entry_type=video 条目。

✅ 已验证可行（2026-05-03）：视频上传后立即可播放，且挂在指定目录下。

正确的 3 步流程（腾讯内部乐享 lexiang.tencent.com 文档）：
  1. POST /cgi-bin/v1/kb/files/upload-params    → 获取 VOD 上传签名 + state
     body: {"name": "xxx.mp4", "media_type": "video"}
  2. PUT  <bucket>.cos.<region>.myqcloud.com/<key>   → 上传文件到 VOD COS
  3. POST /cgi-bin/v1/kb/entries?space_id=xxx&state=xxx  → 创建 entry_type=video 节点
     body: {"data": {"attributes": {"name": "xxx.mp4",  "entry_type": "video"},
                     "relationships": {"parent_entry": {...}}}}

🚨 关键细节（踩坑后总结，不改）：
  - 签名接口必须用 /cgi-bin/v1/kb/files/upload-params（**不是** /cgi-bin/v1/docs/cos-param）
  - media_type 有三种：video / audio / file（docs/cos-param 只支持 attachment/file）
  - 签名接口的 name 和创建 entry 的 name **必须带文件后缀**（否则报"name需指定文件后缀"）
  - kb/entries 接口用 **x-staff-id**（小写，带连字符），不是 StaffID
  - parent_entry 指向目标 page/folder 的 entry_id，不写则挂到 space 根目录

凭证存放（不进 git）：
  ~/.lexiang/openapi.json    （AppKey / AppSecret / StaffID）
  ~/.lexiang/token_cache.json （access_token 缓存，2h 有效）

用法：
  python3 upload_video_via_openapi.py <本地视频> \\
      --space-id <知识库 space_id> \\
      --parent-entry-id <父节点 entry_id> \\
      [--name "视频标题.mp4"]       # 必须带扩展名；不填则用本地文件名
      [--media-type video|audio|file]  # 默认 video

返回：
  entry_id（乐享知识节点 id）
  entry_type（应为 video）
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from typing import Any


CONFIG_PATH = os.path.expanduser("~/.lexiang/openapi.json")
TOKEN_CACHE_PATH = os.path.expanduser("~/.lexiang/token_cache.json")

# api_base 默认值：外部乐享 OpenAPI 域名（lxapi.lexiangla.com）。
# 文档：https://lexiang.tencent.com/wiki/api/ → "获取 access_token" 一节
# 腾讯内部乐享用户可在 openapi.json 中覆盖为 "https://lexiang.tencent.com"。
DEFAULT_API_BASE = "https://lxapi.lexiangla.com"


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"凭证文件不存在: {CONFIG_PATH}\n"
            f"需要字段: app_key, app_secret, staff_id\n"
            f"api_base 可选（默认 {DEFAULT_API_BASE}；腾讯内部乐享填 https://lexiang.tencent.com）"
        )
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    cfg.setdefault("api_base", DEFAULT_API_BASE)
    return cfg


def http_json(
    url: str,
    *,
    method: str = "POST",
    headers: dict | None = None,
    json_body: Any = None,
    form_body: dict | None = None,
    timeout: int = 120,
) -> dict:
    data = None
    hdrs = dict(headers or {})
    if json_body is not None:
        data = json.dumps(json_body).encode()
        hdrs.setdefault("Content-Type", "application/json; charset=utf-8")
    elif form_body is not None:
        data = urllib.parse.urlencode(form_body).encode()
        hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")

    req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode()
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        raise RuntimeError(f"HTTP {e.code} {url}\n响应: {err_body[:500]}") from e
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"_raw": body}


def get_access_token(cfg: dict, *, force_refresh: bool = False) -> str:
    if not force_refresh and os.path.exists(TOKEN_CACHE_PATH):
        try:
            with open(TOKEN_CACHE_PATH) as f:
                cache = json.load(f)
            if cache.get("expires_at", 0) > int(time.time()):
                return cache["access_token"]
        except Exception:
            pass

    url = f"{cfg['api_base']}/cgi-bin/token"
    result = http_json(
        url,
        json_body={
            "grant_type": "client_credentials",
            "app_key": cfg["app_key"],
            "app_secret": cfg["app_secret"],
        },
    )
    if "access_token" not in result:
        raise RuntimeError(f"换取 access_token 失败: {result}")

    cache = {
        "access_token": result["access_token"],
        "expires_at": int(time.time()) + result["expires_in"] - 300,
    }
    os.makedirs(os.path.dirname(TOKEN_CACHE_PATH), exist_ok=True)
    with open(TOKEN_CACHE_PATH, "w") as f:
        json.dump(cache, f)
    os.chmod(TOKEN_CACHE_PATH, 0o600)
    return result["access_token"]


def apply_upload_params(
    *,
    api_base: str,
    access_token: str,
    staff_id: str,
    filename: str,
    media_type: str,
) -> dict:
    """Step 1: 获取 kb/files 的上传签名。"""
    url = f"{api_base}/cgi-bin/v1/kb/files/upload-params"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-staff-id": staff_id,
    }
    result = http_json(
        url,
        headers=headers,
        json_body={"name": filename, "media_type": media_type},
    )
    if "object" not in result or "state" not in result["object"]:
        raise RuntimeError(f"upload-params 失败: {result}")
    return result


def put_to_cos(*, local_file: str, params: dict) -> None:
    """Step 2: PUT 文件到腾讯云 COS。"""
    bucket = params["options"]["Bucket"]
    region = params["options"]["Region"]
    key = params["object"]["key"]
    auth = params["object"]["auth"]
    file_headers = params["object"].get("headers", {}) or {}

    url = f"https://{bucket}.cos.{region}.myqcloud.com/{key}"
    with open(local_file, "rb") as f:
        data = f.read()

    req_headers = {
        "Authorization": auth["Authorization"],
        "x-cos-security-token": auth["XCosSecurityToken"],
    }
    for k, v in file_headers.items():
        req_headers[k] = v

    print(f"      bucket: {bucket}")
    print(f"      region: {region}")
    print(f"      key: {key[:70]}...")
    print(f"      size: {len(data) / 1024 / 1024:.1f} MB")

    req = urllib.request.Request(url, data=data, method="PUT", headers=req_headers)
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            etag = resp.headers.get("ETag", "(none)")
            print(f"      ✓ HTTP {resp.status}, ETag {etag}, 耗时 {time.time()-start:.1f}s")
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"COS PUT 失败 HTTP {e.code}: {e.read().decode()[:500]}"
        ) from e


def create_kb_entry(
    *,
    api_base: str,
    access_token: str,
    staff_id: str,
    space_id: str,
    state: str,
    name: str,
    entry_type: str,
    parent_entry_id: str | None = None,
) -> dict:
    """Step 3: 创建知识节点（entry_type=video/audio/file）。"""
    url = (
        f"{api_base}/cgi-bin/v1/kb/entries"
        f"?space_id={urllib.parse.quote(space_id)}"
        f"&state={urllib.parse.quote(state)}"
    )
    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-staff-id": staff_id,
    }
    body: dict = {
        "data": {
            "attributes": {"name": name, "entry_type": entry_type}
        }
    }
    if parent_entry_id:
        body["data"]["relationships"] = {
            "parent_entry": {"data": {"type": "entry", "id": parent_entry_id}}
        }
    result = http_json(url, headers=headers, json_body=body)
    if "data" not in result or not result["data"].get("id"):
        raise RuntimeError(f"创建知识节点失败: {result}")
    return result["data"]


def upload_media(
    *,
    local_file: str,
    space_id: str,
    parent_entry_id: str | None,
    name: str | None = None,
    media_type: str = "video",
) -> dict:
    """端到端上传入口。"""
    if not os.path.exists(local_file):
        raise FileNotFoundError(f"文件不存在: {local_file}")

    cfg = load_config()
    filename = os.path.basename(local_file)  # 带扩展名
    if not name:
        name = filename  # 默认用文件名（带后缀）
    elif "." not in name:
        # 确保 name 有文件后缀（API 强制要求）
        ext = os.path.splitext(filename)[1]
        name = name + ext

    print(f"文件: {local_file}")
    print(f"  上传名: {filename}")
    print(f"  条目名: {name}")
    print(f"  media_type: {media_type}")
    print(f"  space: {space_id}")
    print(f"  parent: {parent_entry_id or '(space 根目录)'}")
    print()

    print("[0/3] 获取 access_token ...")
    access_token = get_access_token(cfg)
    print(f"      ✓ token: {access_token[:30]}...")

    print("[1/3] kb/files/upload-params (获取 VOD 上传签名) ...")
    params = apply_upload_params(
        api_base=cfg["api_base"],
        access_token=access_token,
        staff_id=cfg["staff_id"],
        filename=filename,
        media_type=media_type,
    )
    state = params["object"]["state"]
    print(f"      ✓ state: {state}")

    print("[2/3] PUT 文件到腾讯云 COS ...")
    put_to_cos(local_file=local_file, params=params)

    entry_type = media_type  # video/audio/file
    print(f"[3/3] 创建 kb/entry (entry_type={entry_type}) ...")
    entry = create_kb_entry(
        api_base=cfg["api_base"],
        access_token=access_token,
        staff_id=cfg["staff_id"],
        space_id=space_id,
        state=state,
        name=name,
        entry_type=entry_type,
        parent_entry_id=parent_entry_id,
    )
    entry_id = entry["id"]
    actual_type = entry.get("attributes", {}).get("entry_type", "?")
    print(f"      ✓ entry_id: {entry_id}")
    print(f"      ✓ entry_type: {actual_type}")

    return {
        "entry_id": entry_id,
        "entry_type": actual_type,
        "name": entry.get("attributes", {}).get("name", name),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="通过乐享 OpenAPI 上传视频/音频到知识库（产生 entry_type=video 条目，可播放）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("local_file", help="本地文件路径")
    parser.add_argument("--space-id", required=True, help="目标知识库 space_id")
    parser.add_argument(
        "--parent-entry-id",
        default=None,
        help="父节点 entry_id；不填则挂到 space 根目录",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="条目名称（须带文件后缀；缺省用本地文件名）",
    )
    parser.add_argument(
        "--media-type",
        default="video",
        choices=["video", "audio", "file"],
        help="媒体类型，决定 kb_entry 的 entry_type（默认 video）",
    )
    parser.add_argument(
        "--json-output", action="store_true", help="以 JSON 输出结果"
    )
    args = parser.parse_args()

    try:
        result = upload_media(
            local_file=args.local_file,
            space_id=args.space_id,
            parent_entry_id=args.parent_entry_id,
            name=args.name,
            media_type=args.media_type,
        )
    except Exception as exc:
        sys.stderr.write(f"\n❌ 上传失败: {exc}\n")
        sys.exit(1)

    print()
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("✅ 上传完成！")
        print(f"   entry_id: {result['entry_id']}")
        print(f"   entry_type: {result['entry_type']}")
        print(f"   链接: https://lexiangla.com/pages/{result['entry_id']}")
        print()
        print("   说明：视频已上传且挂到目标目录。乐享会做 VOD 转码，")
        print("   通常几秒到几分钟内可在 Web 端播放。")


if __name__ == "__main__":
    main()
