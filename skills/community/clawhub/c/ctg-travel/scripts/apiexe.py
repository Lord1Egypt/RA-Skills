#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旅游项目统一接口调用脚本（auth 签名版）
根据 api/*.json 中的接口描述，由 Agent 识别用户意图后选择对应 method，传入 params 执行调用。
每次调用时自动构造 auth（key、timestamp、nonce、signature。
"""

import argparse
import base64
import hmac
import hashlib
import json
import os
import random
import sys
import time
from pathlib import Path

# 强制设置 stdout/stderr 编码为 UTF-8，避免 Windows 环境下中文乱码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_ROOT / "config" / "ctgConfig.json"
API_DIR = SKILL_ROOT / "api"
CACHE_DIR = SKILL_ROOT / "cache"
CACHE_EXPIRE_SECONDS = 24*3600  # 1天

# 支持缓存的接口配置：method -> (缓存文件名模板, 用于构造缓存key的参数列表)
# 目前为空，保留框架以便未来扩展
CACHEABLE_METHODS = {}


def get_cache_key(method, params):
    """根据 method 和参数生成缓存文件名"""
    if method not in CACHEABLE_METHODS:
        return None
    template, keys = CACHEABLE_METHODS[method]
    values = [str(params.get(k, "default")) for k in keys]
    return template.format(*values)


def get_cached_data(cache_file):
    """获取缓存数据，如果缓存无效或不存在返回 None"""
    cache_path = CACHE_DIR / cache_file
    if not cache_path.exists():
        return None
    file_mtime = cache_path.stat().st_mtime
    if time.time() - file_mtime > CACHE_EXPIRE_SECONDS:
        return None
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_cache_data(cache_file, data):
    """保存数据到缓存"""
    CACHE_DIR.mkdir(exist_ok=True)
    cache_path = CACHE_DIR / cache_file
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 缓存保存失败不影响主流程


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg


CALL_URL = "https://pro-api.ourtour.com/openapi/tools/call"


def compute_signature(secret_key, method_part, params_part, timestamp, nonce):
    """计算 HMAC-SHA256 + Base64 签名（与服务端约定：method_json|params_json|timestamp|nonce）"""
    # 签名计算时排除 version 字段（version 用于路由，不参与签名）
    method_for_sign = {k: v for k, v in method_part.items() if k != "version"}
    # 不使用 sort_keys，保持原始字段顺序（与服务端 ObjectMapper 一致）
    method_json = json.dumps(method_for_sign, separators=(',', ':'), ensure_ascii=False)
    params_json = json.dumps(params_part, separators=(',', ':'), ensure_ascii=False)
    sign_data = f"{method_json}|{params_json}|{timestamp}|{nonce}"

    signature = hmac.new(
        secret_key.encode('utf-8'),
        sign_data.encode('utf-8'),
        hashlib.sha256
    ).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    return signature_b64


def build_payload(config, method_part, params_part, api_key_override=None):
    """构造完整请求体：method + params + auth（key、timestamp、nonce、signature）"""
    timestamp = int(time.time() * 1000)
    nonce = random.randint(1, 100)
    api_key = api_key_override or os.environ.get("CTG_API_KEY") or config.get("apiKey")

    if not api_key:
        raise ValueError("未找到 API Key。请通过以下方式设置：\n"
                         "  1. 运行 python scripts/apiexe.py set-key --api-key <your-key>\n"
                         "  2. 或设置环境变量 CTG_API_KEY")

    signature_b64 = compute_signature(api_key, method_part, params_part, timestamp, nonce)
    auth_part = {
        "key": api_key,
        "timestamp": timestamp,
        "nonce": nonce,
        "signature": signature_b64
    }

    # 发送请求时，如果 version 为 None 则不发送该字段
    if method_part.get("version") is None:
        method_part.pop("version", None)

    return {
        "method": method_part,
        "params": params_part,
        "auth": auth_part
    }


def api_call(url, payload, config, timeout=30):
    import urllib.request
    import urllib.error

    skill_version = config.get("skillVersion", "1.2.0")
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": f"CTGTravelSkill/{skill_version}",
        "X-Skill-Version": skill_version
    }
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        try:
            err_data = json.loads(body)
            raise Exception(err_data.get("message", body) or f"HTTP {e.code}")
        except json.JSONDecodeError:
            raise Exception(f"HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise Exception(f"网络错误: {e.reason}")
    except Exception as e:
        raise Exception(str(e))


def load_api_definitions(api_file=None):
    definitions = []
    if api_file:
        path = SKILL_ROOT / api_file if not Path(api_file).is_absolute() else Path(api_file)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                definitions.extend(json.load(f))
    else:
        for f in API_DIR.glob("*.json"):
            if f.name == "auth.json":
                continue
            with open(f, "r", encoding="utf-8") as fp:
                definitions.extend(json.load(fp))
    return definitions


def find_method_by_method(definitions, method):
    """根据 method 查找对应的 category、subCategory、action、version（从接口定义顶层读取）"""
    for d in definitions:
        if d.get("method") == method:
            sub_cat = d.get("subCategory") or d.get("platform")
            if "category" in d and sub_cat is not None and "action" in d:
                return {
                    "category": d["category"],
                    "subCategory": sub_cat,
                    "action": d["action"],
                    "version": d.get("version"),  # 从接口定义读取，可能为 None
                }
            raise ValueError(f"接口 {method} 缺少 category/subCategory(或 platform)/action 定义")
    raise ValueError(f"未找到接口定义: {method}")


def main():
    parser = argparse.ArgumentParser(
        description="接口调用：每次调用自动构造 auth 签名，无需 loginToken",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用方式:
  call: 调用业务接口，自动携带 auth 签名
    %(prog)s call --method search_trains --arg "{\"fromStation\":\"武汉\",\"toStation\":\"长沙\",\"ticketDate\":\"2026-03-08\"}"

  大 JSON 从文件读入后删除（不保留文件）:
    %(prog)s call --method flight.createOrder --arg-file order_arg.json --rm-arg-file

  从 stdin 读入参数（不生成文件）:
    cat order_arg.json | %(prog)s call --method flight.createOrder --arg-file -

  list: 列出 api 中的 method 定义
    %(prog)s list

  set-key: 保存 API Key 到配置文件
    %(prog)s set-key --api-key <your-api-key>
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="命令")

    call_p = subparsers.add_parser("call", help="调用指定 method")
    call_p.add_argument("--method", required=True, help="接口 method，如 search_trains")
    call_p.add_argument("--arg", default="{}", help="业务参数 JSON")
    call_p.add_argument("--arg-file", help="从文件读取业务参数 JSON；使用 - 表示从 stdin 读取，不落盘")
    call_p.add_argument("--rm-arg-file", action="store_true", help="与 --arg-file 配合：读取后删除该文件（仅当 --arg-file 为文件路径时生效）")
    call_p.add_argument("--api-key", help="API Key（优先级高于配置文件）")

    list_p = subparsers.add_parser("list", help="列出 method 定义")
    list_p.add_argument("--api", help="指定 api 文件，如 api/train.json")

    setkey_p = subparsers.add_parser("set-key", help="保存 API Key 到配置文件")
    setkey_p.add_argument("--api-key", required=True, help="要保存的 API Key")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        config = load_config()
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "list":
        definitions = load_api_definitions(getattr(args, "api", None))
        print(json.dumps(definitions, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.command == "set-key":
        config["apiKey"] = args.api_key
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ API Key 已保存到 {CONFIG_FILE}")
        sys.exit(0)

    if args.arg_file:
        if args.arg_file == "-":
            params_part = json.load(sys.stdin)
        else:
            with open(args.arg_file, "r", encoding="utf-8") as f:
                params_part = json.load(f)
            if getattr(args, "rm_arg_file", False):
                Path(args.arg_file).unlink(missing_ok=True)
    else:
        try:
            params_part = json.loads(args.arg)
        except json.JSONDecodeError as e:
            print(f"❌ --arg 不是合法 JSON: {e}", file=sys.stderr)
            sys.exit(1)

    definitions = load_api_definitions()
    try:
        method_part = find_method_by_method(definitions, args.method)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    payload = build_payload(config, method_part, params_part, api_key_override=getattr(args, "api_key", None))
    url = CALL_URL
    
    # 检查缓存
    cache_key = get_cache_key(args.method, params_part)
    if cache_key:
        cached = get_cached_data(cache_key)
        if cached is not None:
            print(json.dumps(cached, ensure_ascii=False, indent=2))
            sys.exit(0)
    
    try:
        result = api_call(url, payload, config)
        # 保存缓存
        if cache_key and result.get("success"):
            save_cache_data(cache_key, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
