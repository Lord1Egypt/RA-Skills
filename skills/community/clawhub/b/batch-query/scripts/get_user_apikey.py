#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_user_apikey.py — 调用小递查查 GetUserApiKey 获取密钥等信息

前置条件：
  必须先拿到网页登录 token（userToken）。获取方式二选一：
    1) 人工：浏览器登录/注册 xdccy.com 后，在 DevTools Console 执行
         localStorage.getItem('userToken')
       复制返回值。
    2) 半自动：用同目录的 guided_register.py（人在环，自动填表 + 过验证码+短信码）。

用法：
  python get_user_apikey.py --token "<userToken>"
  python get_user_apikey.py --token-file token.txt --output out --format json
  python get_user_apikey.py --env   # 从环境变量 XDCC_USER_TOKEN 读取

说明：
  - 接口：POST https://api.xdccy.com/UserInfo/GetUserApiKey
  - 鉴权：请求头 auth = userToken（小写，与前端一致）
  - 零三方依赖，仅标准库
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

API_BASE = "https://api.xdccy.com"
ENDPOINT = "/UserInfo/GetUserApiKey"


def _pick(d, *keys, default=None):
    """从（可能大小写混合的）字典里按候选键名取值。"""
    if not isinstance(d, dict):
        return default
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
        # 大小写不敏感兜底
        lk = k.lower()
        for real_k, v in d.items():
            if str(real_k).lower() == lk and v not in (None, ""):
                return v
    return default


def call_get_user_apikey(token, timeout=20):
    """调用 GetUserApiKey，返回原始 dict。"""
    url = API_BASE + ENDPOINT
    req = urllib.request.Request(url, data=b"{}", method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("auth", token)  # 关键：小写 auth 头，值为 userToken
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return json.loads(raw), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"网络错误: {e.reason}"
    except json.JSONDecodeError as e:
        return None, f"响应非 JSON: {e}"


def parse_result(payload):
    """把接口返回解析成可读的密钥信息 dict。"""
    if not isinstance(payload, dict):
        return {"_raw": payload}
    code = _pick(payload, "code", "Code", "status", "Status")
    msg = _pick(payload, "msg", "message", "Message", "info")
    data = _pick(payload, "data", "Data") or {}

    info = {
        "code": code,
        "msg": msg,
        "apiKey": _pick(data, "apiKey", "ApiKey", "UserApiKey", "userApiKey", "key"),
        "platformId": _pick(data, "platformId", "PlatformId", "platform_id", "PlatformID"),
        "memberId": _pick(data, "memberId", "MemberId", "member_id"),
        "secret": _pick(data, "secret", "Secret", "apiSecret", "signKey"),
        "expireTime": _pick(data, "expireTime", "ExpireTime", "expire", "Expire"),
        "balance": _pick(data, "balance", "Balance", "quota", "Quota"),
    }
    # 任何未识别到的字段，原样保留，避免丢信息
    extra = {k: v for k, v in data.items()
             if k not in ("apiKey", "ApiKey", "UserApiKey", "userApiKey", "key",
                          "platformId", "PlatformId", "platform_id", "PlatformID",
                          "memberId", "MemberId", "member_id",
                          "secret", "Secret", "apiSecret", "signKey",
                          "expireTime", "ExpireTime", "expire", "Expire",
                          "balance", "Balance", "quota", "Quota")}
    if extra:
        info["extra"] = extra
    return info


def render_txt(info):
    lines = ["=== 小递查查 GetUserApiKey 返回 ==="]
    label_map = {
        "code": "状态码", "msg": "消息", "apiKey": "API Key",
        "platformId": "Platform ID", "memberId": "Member ID",
        "secret": "签名密钥/Secret", "expireTime": "过期时间", "balance": "余量/配额",
    }
    for k, label in label_map.items():
        v = info.get(k)
        if v not in (None, ""):
            lines.append(f"{label}：{v}")
    if info.get("extra"):
        lines.append("其他字段：")
        for k, v in info["extra"].items():
            lines.append(f"  · {k}：{v}")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="小递查查 GetUserApiKey 调用工具")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--token", help="userToken 字符串")
    src.add_argument("--token-file", help="含 userToken 的文本文件")
    src.add_argument("--env", action="store_true", help="从环境变量 XDCC_USER_TOKEN 读取")
    p.add_argument("--output", help="输出基名（不含扩展名），可生成 .json/.txt")
    p.add_argument("--format", choices=["json", "txt", "both"], default="both",
                   help="输出格式，默认 both")
    args = p.parse_args(argv)

    if args.token:
        token = args.token.strip()
    elif args.token_file:
        with open(args.token_file, "r", encoding="utf-8") as f:
            token = f.read().strip()
    elif args.env:
        token = os.environ.get("XDCC_USER_TOKEN", "").strip()
    if not token:
        print("错误：未获取到 token", file=sys.stderr)
        return 2

    payload, err = call_get_user_apikey(token)
    if err:
        print(f"调用失败：{err}", file=sys.stderr)
        return 1

    info = parse_result(payload)

    # 控制台输出
    print(render_txt(info))
    print("\n--- 原始 JSON ---")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    # 落盘
    if args.output:
        if args.format in ("json", "both"):
            jp = args.output + ".json"
            with open(jp, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            print(f"\n[已保存] {jp}")
        if args.format in ("txt", "both"):
            tp = args.output + ".txt"
            with open(tp, "w", encoding="utf-8") as f:
                f.write(render_txt(info))
            print(f"[已保存] {tp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
