"""copy-brain 脚本共享工具。

提供：
- API Key 读取（从系统环境变量）与缺失提示
- HTTP 请求（含重试与错误处理）
- 结果输出（打印到 stdout，或保存 JSON 到文件）

所有脚本均依赖 requests：pip install -r requirements.txt
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

# 让中文在 Windows(GBK) 控制台也能正常输出，避免 UnicodeEncodeError
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

try:
    import requests
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "缺少依赖 requests。请先运行：pip install -r requirements.txt\n"
    )
    sys.exit(3)

# skill 根目录（scripts 的上一级）
SKILL_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = SKILL_ROOT / "output"

# 退出码约定
EXIT_OK = 0
EXIT_API_ERROR = 1
EXIT_NO_KEY = 2  # 未配置 API Key，agent 据此判断该服务不可用
EXIT_BAD_USAGE = 4


def require_key(env_name: str, service: str, signup_url: str) -> str:
    """从系统环境变量读取 API Key；缺失时打印提示并以 EXIT_NO_KEY 退出。"""
    key = os.environ.get(env_name, "").strip()
    if not key:
        sys.stderr.write(
            f"[未配置] 环境变量 {env_name} 缺失，无法调用 {service}。\n"
            f"请在系统环境变量中设置 {env_name}（设置后需重开终端 / Cursor 使其生效）。\n"
            f"申请地址：{signup_url}\n"
        )
        sys.exit(EXIT_NO_KEY)
    return key


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: int = 40,
    max_retries: int = 3,
) -> dict[str, Any]:
    """带重试的 JSON 请求。429/5xx 指数退避；其他错误直接抛出友好信息。"""
    last_err = ""
    for attempt in range(max_retries):
        try:
            resp = requests.request(
                method.upper(),
                url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=timeout,
            )
        except requests.RequestException as exc:
            last_err = f"网络错误：{exc}"
            time.sleep(1.5 * (attempt + 1))
            continue

        if resp.status_code in (429, 500, 502, 503, 504):
            last_err = f"HTTP {resp.status_code}：{resp.text[:300]}"
            time.sleep(2.0 * (attempt + 1))
            continue

        if not resp.ok:
            sys.stderr.write(
                f"[请求失败] HTTP {resp.status_code}\n{resp.text[:600]}\n"
            )
            sys.exit(EXIT_API_ERROR)

        try:
            return resp.json()
        except ValueError:
            sys.stderr.write(f"[解析失败] 响应非 JSON：\n{resp.text[:600]}\n")
            sys.exit(EXIT_API_ERROR)

    sys.stderr.write(f"[重试耗尽] {last_err}\n")
    sys.exit(EXIT_API_ERROR)


REDFOX_BASE = "https://redfox.hk"
REDFOX_SIGNUP = "https://redfox.hk/dashboard/keys"


def redfox_headers(api_key: str) -> dict[str, str]:
    return {"REDFOX_API_KEY": api_key, "Content-Type": "application/json"}


def redfox_search(api_key: str, endpoint: str, keyword: str, sort: str, pages: int) -> dict:
    """RedFox 通用搜索：按 offset（每页 +20）翻页，合并 list（小红书/公众号通用）。"""
    all_items: list = []
    offset = 0
    total = None
    for _ in range(max(1, pages)):
        body = {"keyword": keyword, "offset": offset, "sortType": sort}
        resp = request_json(
            "POST", REDFOX_BASE + endpoint, headers=redfox_headers(api_key), json_body=body
        )
        data = resp.get("data") or {}
        items = data.get("list") or []
        all_items.extend(items)
        total = data.get("total", total)
        if not data.get("hasMore") or not items:
            break
        offset += 20
    return {"keyword": keyword, "total": total, "count": len(all_items), "list": all_items}


def emit(data: Any, out: str | None) -> None:
    """输出结果：始终打印到 stdout；若指定 --out 则同时写入文件。"""
    text = json.dumps(data, ensure_ascii=False, indent=2)
    print(text)
    if out:
        out_path = Path(out)
        if not out_path.is_absolute():
            out_path = OUTPUT_DIR / out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        sys.stderr.write(f"[已保存] {out_path}\n")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--out",
        default=None,
        help="可选：将原始 JSON 结果保存到该文件（相对路径默认存入 output/）",
    )
