#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
京ME 内网认证模块（零配置，独立复刻自 joy-helper/lib/jme-auth.mjs）。

核心：从本机京ME桌面客户端（JDITDesk）自动换取 me_token，再换出 sso_token
（sso.jd.com），供 jcd.jd.com 等内网接口做认证。全程无需扫码、无需手填 token。

链路（5 步）：
  ① desk.agent.auth.encrypt      → {aesKey, content}
  ② 本机 HiOffice 127.0.0.1:{8988..9006 步长2}/hioffice → body + 响应头 X-AES-Key
  ③ desk.agent.auth.getWebToken  → accessToken(=me_token)
  ④ eopen.getCode                → code
  ⑤ autherp.jd.com/sso/tp        → Set-Cookie 里的 sso.jd.com

前提：本机已安装并登录京ME客户端（监听 8988~9006 之一）。
token 缓存在 ~/.jdos-config-fetcher-cache.json（权限 600），过期自动刷新。
仅依赖标准库 + requests。
"""

import hashlib
import json
import os
import platform
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# ── 常量（照搬 joy-helper，已验证）─────────────────────────────────────────
APPID = "JDME_DESKTOP"
COLOR_GATEWAY = "https://api.m.jd.com"
SSO_APP_KEY = "sL5qtKu71X8H25ysaaHB"

# 租户 CN.JD.GROUP → teamId / ddAppId
TENANT_CODE = "CN.JD.GROUP"
TEAM_ID = "00046419"
DD_APP_ID = "ee"

# HiOffice 本地端口：8988 起，步长 2，共 10 个
HIOFFICE_PORTS = [8988 + i * 2 for i in range(10)]

_IS_MAC = sys.platform == "darwin"
HIOFFICE_FROM = "hio_plugin_joydesk_Mac" if _IS_MAC else "hio_plugin_joydesk"

CACHE_FILE = os.path.join(os.path.expanduser("~"), ".ducc-helper-cache.json")
ME_TOKEN_TTL = 12 * 60 * 60      # me_token 缓存 12h
SSO_TOKEN_TTL = 20 * 60 * 60     # sso_token 保守按 20h（实际 24h）

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
)


def log(msg):
    print(f"[jme-auth] {msg}", file=sys.stderr)


def _device_id():
    """稳定的设备标识：ducc-helper-<md5(hostname)[:12]>。"""
    h = hashlib.md5(socket.gethostname().encode("utf-8")).hexdigest()[:12]
    return f"ducc-helper-{h}"


# ── 缓存 ────────────────────────────────────────────────────────────────
def _read_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _write_cache(obj):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        os.chmod(CACHE_FILE, 0o600)
    except Exception as e:  # noqa: BLE001
        log(f"缓存写入失败（忽略）: {e}")


def clear_cache():
    """清除缓存（调试/登出用）。"""
    try:
        os.unlink(CACHE_FILE)
        log("缓存已清除")
    except FileNotFoundError:
        pass
    except Exception as e:  # noqa: BLE001
        log(f"清除缓存失败: {e}")


# ── Color 网关 ─────────────────────────────────────────────────────────
def _call_color(function_id, body, retries=3):
    """POST color 网关（JSON body），返回解析后的 JSON。"""
    url = f"{COLOR_GATEWAY}?functionId={requests.utils.quote(function_id)}&appid={APPID}"
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps({"functionId": function_id, "body": body, "appid": APPID}),
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise last_err or RuntimeError(f"callColorGateway {function_id} failed")


# ── ① encrypt → ② HiOffice → ③ getWebToken 换 me_token ───────────────────
def _post_hioffice(port, aes_key, content):
    """向单个本机 HiOffice 端口发请求，返回 (body, resp_x_aes_key, port)。"""
    r = requests.post(
        f"http://127.0.0.1:{port}/hioffice?from={requests.utils.quote(HIOFFICE_FROM)}",
        headers={"X-AES-Key": aes_key, "Content-Type": "application/json"},
        data=content.encode("utf-8") if isinstance(content, str) else content,
        timeout=5,
    )
    r.raise_for_status()
    key = r.headers.get("X-AES-Key")
    if not key:
        raise RuntimeError(f"port {port}: 缺少 X-AES-Key")
    return r.text, key, port


def _fetch_me_token(device_id, retries=3):
    # Step ①：encrypt
    content = json.dumps({
        "method": "query",
        "param": "appToken",
        "timestamp": str(int(time.time())),
        "from": HIOFFICE_FROM,
        "to": "HiOfficeClient",
    })
    enc = _call_color("desk.agent.auth.encrypt", {"content": content, "jdmeAppId": DD_APP_ID}, retries)
    data = enc.get("data") or {}
    if enc.get("code") != 0 or not data.get("aesKey") or not data.get("content"):
        raise RuntimeError(enc.get("msg") or "encrypt 失败（code != 0）")
    aes_key = data["aesKey"]
    enc_content = data["content"]

    # Step ②：本机 HiOffice 多端口并发，取首个成功
    res_body = res_key = used_port = None
    for _round in range(retries + 1):
        if res_body:
            break
        with ThreadPoolExecutor(max_workers=len(HIOFFICE_PORTS)) as ex:
            futs = {ex.submit(_post_hioffice, p, aes_key, enc_content): p for p in HIOFFICE_PORTS}
            for fut in as_completed(futs):
                try:
                    body, key, port = fut.result()
                    res_body, res_key, used_port = body, key, port
                    break
                except Exception:  # noqa: BLE001
                    continue
    if not res_body:
        raise RuntimeError(
            "无法连接本机京ME客户端（HiOffice 端口 8988~9006 全部失败）。\n"
            "请确认：1) 已安装京ME桌面客户端 2) 客户端处于登录状态 3) 客户端正在运行。"
        )
    log(f"HiOffice 命中端口 {used_port}")

    # Step ③：getWebToken
    tok = _call_color(
        "desk.agent.auth.getWebToken",
        {
            "token": res_body,
            "tenantCode": TENANT_CODE,
            "deviceUuid": device_id,
            "aesKey": res_key,
            "jdmeAppId": DD_APP_ID,
        },
        retries,
    )
    if tok.get("code") != 0:
        raise RuntimeError(tok.get("msg") or "getWebToken 失败（code != 0）")
    access_token = (tok.get("data") or {}).get("accessToken", "").strip()
    if not access_token:
        raise RuntimeError("getWebToken 未返回 accessToken")
    return access_token


# ── ④ eopen.getCode → ⑤ autherp 换 sso.jd.com ────────────────────────────
def _fetch_sso_token(me_token):
    # Step ④：eopen.getCode
    code_body = {
        "appid": APPID,
        "body": json.dumps({"appKey": SSO_APP_KEY, "jdmeAppId": DD_APP_ID}),
        "client": "web",
        "functionId": "eopen.getCode",
        "loginType": "15",
    }
    code_res = requests.post(
        f"{COLOR_GATEWAY}?functionId=eopen.getCode&appid={APPID}",
        headers={
            "x-device-type": "web",
            "x-team-id": TEAM_ID,
            "Cookie": f"me_token={me_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=code_body,
        timeout=30,
    )
    code_data = code_res.json()
    code = (code_data.get("data") or {}).get("code")
    if code_data.get("code") != 0 or not code:
        raise RuntimeError(code_data.get("msg") or "eopen.getCode 失败")

    # Step ⑤：autherp，从 Set-Cookie 提取 sso.jd.com
    return_url = "https://joyspace.jd.com?lang=zh_CN"
    sso_res = requests.get(
        "https://autherp.jd.com/sso/tp",
        params={"name": "joydesk", "token": code, "returnUrl": return_url},
        allow_redirects=False,
        timeout=30,
    )
    sso = sso_res.cookies.get("sso.jd.com")
    if not sso:
        # 兜底：手动扫描 Set-Cookie 头
        raw = sso_res.headers.get("set-cookie", "")
        import re
        m = re.search(r"sso\.jd\.com=([^;]+)", raw)
        if m:
            sso = m.group(1)
    if not sso:
        raise RuntimeError("未能从 autherp 响应中提取 sso.jd.com")
    return sso


# ── 对外主入口 ────────────────────────────────────────────────────────────
def get_sso_token(force_refresh=False):
    """返回 sso_token 原始值（不含 'sso.jd.com=' 前缀）。优先用缓存，过期自动刷新。"""
    device_id = os.environ.get("JMECHAT_DEVICE_ID", "").strip() or _device_id()
    cache = _read_cache()
    entry = cache.get(TENANT_CODE, {})
    now = int(time.time())

    me_token = entry.get("meToken")
    me_valid = (
        me_token
        and entry.get("meTokenAt")
        and now - entry["meTokenAt"] < ME_TOKEN_TTL
        and not force_refresh
    )
    if not me_valid:
        log("获取 me_token（HiOffice 本地链路）...")
        me_token = _fetch_me_token(device_id)
        entry["meToken"] = me_token
        entry["meTokenAt"] = now
        entry["ssoToken"] = None      # me_token 变了，sso 作废
        entry["ssoTokenAt"] = None

    sso_token = entry.get("ssoToken")
    sso_valid = (
        sso_token
        and entry.get("ssoTokenAt")
        and now - entry["ssoTokenAt"] < SSO_TOKEN_TTL
        and not force_refresh
    )
    if not sso_valid:
        log("换取 sso_token ...")
        sso_token = _fetch_sso_token(me_token)
        entry["ssoToken"] = sso_token
        entry["ssoTokenAt"] = now

    cache[TENANT_CODE] = entry
    _write_cache(cache)
    return sso_token


def get_sso_cookie(force_refresh=False):
    """返回可直接用于 Cookie 头的字符串：'sso.jd.com=<token>'。"""
    return f"sso.jd.com={get_sso_token(force_refresh=force_refresh)}"


if __name__ == "__main__":
    # 自测：python jme_auth.py [--clear] [--force]
    args = sys.argv[1:]
    if "--clear" in args:
        clear_cache()
    force = "--force" in args
    cookie = get_sso_cookie(force_refresh=force)
    tok = cookie.split("=", 1)[1]
    log(f"OK: sso.jd.com 长度={len(tok)}")
    print(cookie)
