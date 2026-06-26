#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import requests

ENV_KEY = "AIDSO_GEO_API_KEY"
ENV_FILE = Path(__file__).resolve().parent / ".env"
SAVE_URL = "https://api.aidso.com/openapi/skills/save_content/md"

def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False))

def load_env_file() -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not ENV_FILE.exists():
        return result
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result

def get_api_key() -> Tuple[Optional[str], Optional[str]]:
    api_key = os.getenv(ENV_KEY)
    if api_key:
        return api_key.strip(), "environment"
    api_key = load_env_file().get(ENV_KEY)
    if api_key:
        return api_key.strip(), ".env"
    return None, None

def request_post(url: str, api_key: str, payload: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), timeout=timeout)
        try:
            data = response.json()
        except Exception:
            return {"code": -1, "msg": "response is not json", "data": response.text, "http_status": response.status_code}
        if response.status_code < 200 or response.status_code >= 300:
            return {"code": -1, "msg": "http status error", "data": data, "http_status": response.status_code}
        return data
    except requests.Timeout:
        return {"code": -1, "msg": "request timeout", "data": None}
    except requests.RequestException as e:
        return {"code": -1, "msg": f"request error: {e}", "data": None}

def add_knowledge(brand_name: str, content: str) -> Dict[str, Any]:
    brand_name = brand_name.strip()
    content = content.strip()
    if not brand_name:
        return {"ok": False, "msg": "brand_name 不能为空"}
    if not content:
        return {"ok": False, "msg": "content 不能为空"}
    api_key, source = get_api_key()
    if not api_key:
        return {"ok": False, "need_bind_api_key": True, "env_key": ENV_KEY, "msg": "还没有绑定 API Key，请先发送：绑定 api-key：你的_api_key"}
    result = request_post(SAVE_URL, api_key, {"content": content, "brand_name": brand_name}, timeout=60)
    if result.get("code") == 200 and result.get("msg") == "success" and result.get("data") is True:
        return {"ok": True, "msg": "success", "brand_name": brand_name, "data": True, "api_key_source": source}
    if result.get("code") == 405:
        return {"ok": False, "msg": "参数不正确", "brand_name": brand_name, "raw": result}
    return {"ok": False, "msg": "添加品牌知识失败", "brand_name": brand_name, "raw": result}

def main() -> None:
    parser = argparse.ArgumentParser(description="AIDSO GEO Knowledge Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add", help="添加品牌知识库内容")
    add_parser.add_argument("--brand-name", required=True, help="品牌名称")
    add_parser.add_argument("--content", required=True, help="知识内容")
    args = parser.parse_args()
    if args.command == "add":
        result = add_knowledge(args.brand_name, args.content)
        print_json(result)
        if not result.get("ok"):
            sys.exit(1)
        return

if __name__ == "__main__":
    main()
