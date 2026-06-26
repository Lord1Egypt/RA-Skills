import argparse
import json
import os
import re
import subprocess
import sys
import uuid
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests

# 订单状态本地存储：断连/异常后可在聊天框展示订餐链接，恢复后可 --query-order 查询进度
OPENCLAW_ORDER_STATE_DIR_ENV = "OPENCLAW_ORDER_STATE_DIR"
ORDER_STATE_SUBDIR = "openclaw_order_state"
# 标准输出中可解析行，便于大模型/客户端断连后仍能从输出中提取订餐链接
OPENCLAW_FINAL_LINK_PREFIX = "OPENCLAW_FINAL_LINK:"
OPENCLAW_ORDER_STATE_PREFIX = "OPENCLAW_ORDER_STATE:"

# 麦当劳 customProduct 固定为「门店自提」
MCD_CUSTOM_PRODUCT_EAT_TYPE = "门店自提"

# 流程注册表：OpenClaw 可根据 flow_code 明确知道将调用的脚本与所需参数
FLOW_REGISTRY = {
    "kfc_vip_choose_spec": {
        "script": "kfc_vip_choose_spec_flow.py",
        "name": "肯德基 VIP 兑换链接(outId)",
        "required_params": ["--city 与 --store-keyword 或 --kfc-store-code"],
    },
    "kfc_custom_product": {
        "script": "kfc_custom_product_flow.py",
        "name": "肯德基 customProduct(cdkey+store+booking_time)",
        "required_params": ["--city 与 --store-keyword 或 --kfc-store-code"],
    },
    "kfc_city_store_booking": {
        "script": "kfc_place_order_test_old.py",
        "name": "肯德基 城市+门店+预约",
        "required_params": ["--city", "--store-keyword"],
    },
    "mcd_custom_product": {
        "script": "mcd_custom_product_flow.py",
        "name": "麦当劳 customProduct(门店自提)",
        "required_params": ["--store-keyword 或 --mcd-store-number"],
    },
    "mcd_store_eattype": {
        "script": "mcd_place_order_test.py",
        "name": "麦当劳 门店+就餐方式",
        "required_params": ["--store-keyword"],
    },
}

# 错误码与处理建议（供 OpenClaw 或用户展示）
ERROR_REMEDIES = {
    "ELEMENT_NOT_FOUND": (
        "未找到页面上的预期按钮或文案",
        "请检查：1) 页面是否完全加载 2) 网络是否稳定 3) 门店是否营业/可下单 4) 链接是否已过期",
    ),
    "TIMEOUT": (
        "页面加载或操作超时",
        "请检查网络或稍后重试；可适当增加 --wait-pickup-seconds",
    ),
    "NETWORK": (
        "网络请求失败",
        "请检查本机网络与后端/目标站点是否可达",
    ),
    "API_ERROR": (
        "门店或订单接口返回异常",
        "请确认后端 /kfc/store 或 /mcd/store 已实现且返回正确格式；或直接传 --kfc-store-code / --mcd-store-number",
    ),
    "INVALID_URL": (
        "链接缺少必要参数(cdkey/outId等)",
        "请确认订单接口返回的 url 格式正确",
    ),
    "SUBMIT_ABORTED": (
        "已按配置在最终确认前停止",
        "若需真实下单请使用 --allow-final-submit",
    ),
    "SCRIPT_NOT_FOUND": (
        "流程脚本文件不存在",
        "请确认 skill 目录完整，包含对应 .py 脚本",
    ),
    "RESULT_READ_ERROR": (
        "无法读取流程结果文件",
        "请查看 outputs 目录下最新 JSON 与截图排查",
    ),
}

DEFAULT_BASE_URL_DEV = "http://localhost:8888/api/openclaw"
DEFAULT_BASE_URL_PROD = "https://www.clawauto.shop/api/openclaw"


def resolve_base_url(cli_value: str = "") -> str:
    """
    Resolve base URL with simple dev/prod support controlled by env:
    - KFC_PLATFORM_ENV=prod or OPENCLAW_ENV=prod ->
        use KFC_PLATFORM_BASE_URL_PROD / OPENCLAW_PLATFORM_BASE_URL_PROD / DEFAULT_BASE_URL_PROD
    - otherwise ->
        use KFC_PLATFORM_BASE_URL_DEV / OPENCLAW_PLATFORM_BASE_URL_DEV / DEFAULT_BASE_URL_DEV
    CLI --base-url always has highest priority.
    """
    cli_value = cli_value.strip()
    if cli_value:
        return cli_value.rstrip("/")

    env_mode = (os.getenv("KFC_PLATFORM_ENV", "") or os.getenv("OPENCLAW_ENV", "")).strip().lower()
    if env_mode in {"prod", "production"}:
        value = (
            os.getenv("KFC_PLATFORM_BASE_URL_PROD", "").strip()
            or os.getenv("OPENCLAW_PLATFORM_BASE_URL_PROD", "").strip()
            or os.getenv("KFC_PLATFORM_BASE_URL", "").strip()
            or os.getenv("OPENCLAW_PLATFORM_BASE_URL", "").strip()
            or DEFAULT_BASE_URL_PROD
        )
    else:
        value = (
            os.getenv("KFC_PLATFORM_BASE_URL_DEV", "").strip()
            or os.getenv("OPENCLAW_PLATFORM_BASE_URL_DEV", "").strip()
            or os.getenv("KFC_PLATFORM_BASE_URL", "").strip()
            or os.getenv("OPENCLAW_PLATFORM_BASE_URL", "").strip()
            or DEFAULT_BASE_URL_DEV
        )

    return value.rstrip("/")


def get_products(identity: str, api_key: str, base_url: str, timeout: int = 10) -> dict:
    payload = {"username": identity, "phone": identity, "api_key": api_key}
    url = f"{base_url}/products"
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.encoding = "utf-8"
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"request failed: {exc}") from exc
    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError("invalid response json") from exc


def fetch_order_status(
    identity: str,
    api_key: str,
    base_url: str,
    order_id: int,
    timeout: int = 15,
) -> dict:
    """POST /order/status：服务端查单（含供应商状态、订餐链接刷新），需 API Key。"""
    payload = {
        "username": identity,
        "phone": identity,
        "api_key": api_key,
        "order_id": int(order_id),
    }
    url = f"{base_url.rstrip('/')}/order/status"
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.encoding = "utf-8"
    except requests.RequestException as exc:
        raise RuntimeError(f"request failed: {exc}") from exc
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("invalid response json") from exc
    if response.status_code >= 400:
        msg = (data.get("message") if isinstance(data, dict) else None) or response.text
        code = (data.get("code") if isinstance(data, dict) else "") or ""
        extra = f"{code} ".strip()
        raise RuntimeError(f"{extra}{msg}".strip())
    return data


def list_openclaw_orders(
    identity: str,
    api_key: str,
    base_url: str,
    timeout: int = 15,
) -> dict:
    """POST /orders：当前用户订单列表（与 Bearer /api/orders 一致）。"""
    payload = {"username": identity, "phone": identity, "api_key": api_key}
    url = f"{base_url.rstrip('/')}/orders"
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.encoding = "utf-8"
    except requests.RequestException as exc:
        raise RuntimeError(f"request failed: {exc}") from exc
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("invalid response json") from exc
    if response.status_code >= 400:
        msg = (data.get("message") if isinstance(data, dict) else None) or response.text
        code = (data.get("code") if isinstance(data, dict) else "") or ""
        extra = f"{code} ".strip()
        raise RuntimeError(f"{extra}{msg}".strip())
    return data


def order(
    identity: str,
    api_key: str,
    base_url: str,
    product_id: int,
    product_name: str,
    price_yuan: int,
    available_date: str,
    idempotency_key: str,
    supplier_goods_id: int = 0,
    timeout: int = 10,
) -> dict:
    payload = {
        "username": identity,
        "phone": identity,
        "api_key": api_key,
        "product_id": product_id,
        "product_name": product_name,
        "price_yuan": price_yuan,
        "available_date": available_date,
        "idempotency_key": idempotency_key,
    }
    if supplier_goods_id > 0:
        payload["supplier_goods_id"] = supplier_goods_id
    url = f"{base_url}/order"
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.encoding = "utf-8"
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"request failed: {exc}") from exc
    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError("invalid response json") from exc


def get_order_state_dir() -> Path:
    """订单状态保存目录（用户本地），可用 OPENCLAW_ORDER_STATE_DIR 覆盖。"""
    env = (os.getenv(OPENCLAW_ORDER_STATE_DIR_ENV) or "").strip()
    if env:
        return Path(env)
    return Path(__file__).resolve().parent / ORDER_STATE_SUBDIR


def _sanitize_idem_key(key: str) -> str:
    """生成安全文件名（仅保留字母数字与下划线）。"""
    return re.sub(r"[^\w]", "_", key or "unknown")[:128]


def save_order_state(
    idempotency_key: str,
    *,
    order_id: int = 0,
    url: str = "",
    stage: str = "order_received",
    flow_code: str = "",
    flow_result: dict | None = None,
    order_resp: dict | None = None,
) -> Path | None:
    """将订单状态写入本地文件，便于断连后查询或直接展示链接。"""
    state_dir = get_order_state_dir()
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "idempotency_key": idempotency_key,
        "order_id": order_id or (order_resp or {}).get("order_id") or 0,
        "url": url or (order_resp or {}).get("url") or "",
        "stage": stage,
        "flow_code": flow_code,
        "flow_result": flow_result,
        "updated_at": now,
    }
    if order_resp:
        payload["cost_yuan"] = order_resp.get("cost_yuan", order_resp.get("points_cost"))
        payload["balance_yuan"] = order_resp.get("balance_yuan", order_resp.get("points_balance"))
        payload["product_name"] = (order_resp.get("product") or {}).get("name")
    if "created_at" not in payload:
        payload["created_at"] = now
    path = state_dir / f"{_sanitize_idem_key(idempotency_key)}.json"
    try:
        # 若已存在则保留 created_at
        if path.exists():
            try:
                existing = json.loads(path.read_text(encoding="utf-8"))
                payload["created_at"] = existing.get("created_at", now)
            except Exception:
                pass
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
    except OSError:
        return None


def load_order_state(idempotency_key: str) -> dict | None:
    """按幂等键读取本地订单状态。"""
    path = get_order_state_dir() / f"{_sanitize_idem_key(idempotency_key)}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_order_state_by_order_id(order_id: int) -> tuple[str | None, dict | None]:
    """按 order_id 查找本地状态（扫描状态目录）。"""
    if order_id <= 0:
        return None, None
    state_dir = get_order_state_dir()
    if not state_dir.exists():
        return None, None
    for f in state_dir.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if int(data.get("order_id") or 0) == int(order_id):
                return data.get("idempotency_key"), data
        except Exception:
            continue
    return None, None


def emit_order_result_for_chat(
    url: str,
    idempotency_key: str = "",
    order_id: int = 0,
    stage: str = "",
    order_resp: dict | None = None,
) -> None:
    """立即向标准输出输出订餐链接与状态，便于断连后大模型/客户端从输出中展示给用户。"""
    if url:
        print(OPENCLAW_FINAL_LINK_PREFIX, url.strip(), flush=True)
    state = {
        "url": (url or "").strip(),
        "order_id": order_id,
        "idempotency_key": idempotency_key,
        "stage": stage or "order_received",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if order_resp:
        state["cost_yuan"] = order_resp.get("cost_yuan", order_resp.get("points_cost"))
        state["balance_yuan"] = order_resp.get("balance_yuan", order_resp.get("points_balance"))
        state["product_name"] = (order_resp.get("product") or {}).get("name")
    print(OPENCLAW_ORDER_STATE_PREFIX, json.dumps(state, ensure_ascii=False), flush=True)


def extract_result_file(stdout_text: str) -> Path | None:
    match = re.search(r"result_file:\s*(.+)", stdout_text)
    if not match:
        return None
    p = Path(match.group(1).strip())
    return p if p.exists() else None


def normalize_products(products_data: dict) -> list[dict]:
    if isinstance(products_data, dict) and isinstance(products_data.get("products"), list):
        return products_data.get("products", [])
    if isinstance(products_data, list):
        return products_data
    return []


def find_product(
    products: list[dict], product_id: int, supplier_goods_id: int = 0
) -> dict | None:
    """按 product_id 或 supplier_goods_id 查找商品。id=0 的虚拟商品（仅供应商有）用 supplier_goods_id 匹配。"""
    for item in products:
        try:
            if int(item.get("id", 0)) == int(product_id):
                return item
            if supplier_goods_id > 0 and int(item.get("supplier_goods_id", 0)) == int(
                supplier_goods_id
            ):
                return item
        except Exception:
            continue
    return None


def run_kfc_vip_choose_spec_flow(order_url: str, store_code: str, args) -> dict:
    """肯德基 VIP 兑换链接流程：打开 outId 链接 -> 下一步 -> 允许定位 -> 取 productId -> 拼 choose_specifications -> 下单 -> 确认 -> 等取餐码。"""
    flow_script = Path(__file__).resolve().parent / "kfc_vip_choose_spec_flow.py"
    if not flow_script.exists():
        raise RuntimeError(f"flow script not found: {flow_script}")

    wait_sec = getattr(args, "wait_pickup_seconds", 60)
    cmd = [
        sys.executable,
        str(flow_script),
        "--url",
        order_url,
        "--store-code",
        store_code,
        "--wait-pickup-seconds",
        str(wait_sec),
    ]
    if args.kfc_headless:
        cmd.append("--headless")
    if args.no_final_submit or not args.allow_final_submit:
        cmd.append("--no-submit")

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    result_file = extract_result_file(proc.stdout)
    if result_file is None:
        if proc.returncode != 0:
            raise RuntimeError(
                f"kfc vip choose_spec flow failed(exit={proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
            )
        raise RuntimeError("kfc vip choose_spec flow result file path not found in output")

    try:
        result = json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"failed to read flow result json: {exc}") from exc
    result["result_file"] = str(result_file)
    if proc.returncode != 0 and not result.get("error_code"):
        result.setdefault("error", proc.stderr.strip() or proc.stdout.strip())
        result.setdefault("error_code", "RESULT_READ_ERROR")
    return result


def run_kfc_custom_product_flow(order_url: str, args) -> dict:
    """肯德基 customProduct 流程：打开链接 -> 确认提交 -> 弹窗确认 -> 等取餐码（最多 60 秒）。"""
    flow_script = Path(__file__).resolve().parent / "kfc_custom_product_flow.py"
    if not flow_script.exists():
        raise RuntimeError(f"flow script not found: {flow_script}")

    wait_sec = getattr(args, "wait_pickup_seconds", 60)
    cmd = [
        sys.executable,
        str(flow_script),
        "--url",
        order_url,
        "--wait-pickup-seconds",
        str(wait_sec),
    ]
    if args.kfc_headless:
        cmd.append("--headless")
    if args.no_final_submit or not args.allow_final_submit:
        cmd.append("--no-submit")

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    result_file = extract_result_file(proc.stdout)
    if result_file is None:
        if proc.returncode != 0:
            raise RuntimeError(
                f"kfc customProduct flow failed(exit={proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
            )
        raise RuntimeError("kfc customProduct flow result file path not found in output")

    try:
        result = json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"failed to read flow result json: {exc}") from exc
    result["result_file"] = str(result_file)
    if proc.returncode != 0 and not result.get("error_code"):
        result.setdefault("error", proc.stderr.strip() or proc.stdout.strip())
        result.setdefault("error_code", "RESULT_READ_ERROR")
    return result


def run_kfc_flow(order_url: str, args) -> dict:
    flow_script = Path(__file__).resolve().parent / "kfc_place_order_test_old.py"
    if not flow_script.exists():
        raise RuntimeError(f"flow script not found: {flow_script}")

    cmd = [
        sys.executable,
        str(flow_script),
        "--url",
        order_url,
        "--city",
        args.city,
        "--store-keyword",
        args.store_keyword,
        "--store-name",
        args.store_name,
        "--pickup-type",
        args.pickup_type,
        "--pickup-time",
        args.pickup_time,
        "--wait-taskslist-seconds",
        str(args.wait_taskslist_seconds),
    ]
    if args.kfc_headless:
        cmd.append("--headless")
    if args.no_final_submit or not args.allow_final_submit:
        cmd.append("--no-submit")

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    result_file = extract_result_file(proc.stdout)
    if result_file is None:
        if proc.returncode != 0:
            raise RuntimeError(f"kfc flow failed(exit={proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}")
        raise RuntimeError("kfc flow result file path not found in output")

    try:
        result = json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"failed to read flow result json: {exc}") from exc
    result["result_file"] = str(result_file)
    if proc.returncode != 0 and not result.get("error_code"):
        result.setdefault("error", proc.stderr.strip() or proc.stdout.strip())
        result.setdefault("error_code", "RESULT_READ_ERROR")
    return result


def run_mcd_flow(order_url: str, args) -> dict:
    flow_script = Path(__file__).resolve().parent / "mcd_place_order_test.py"
    if not flow_script.exists():
        raise RuntimeError(f"flow script not found: {flow_script}")

    cmd = [
        sys.executable,
        str(flow_script),
        "--url",
        order_url,
        "--store-keyword",
        args.store_keyword,
        "--store-name",
        args.store_name,
        "--eat-type",
        args.eat_type,
    ]
    if args.kfc_headless:
        cmd.append("--headless")
    if args.no_final_submit or not args.allow_final_submit:
        cmd.append("--no-submit")

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    result_file = extract_result_file(proc.stdout)
    if result_file is None:
        if proc.returncode != 0:
            raise RuntimeError(f"mcd flow failed(exit={proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}")
        raise RuntimeError("mcd flow result file path not found in output")

    try:
        result = json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"failed to read flow result json: {exc}") from exc
    result["result_file"] = str(result_file)
    if proc.returncode != 0 and not result.get("error_code"):
        result.setdefault("error", proc.stderr.strip() or proc.stdout.strip())
        result.setdefault("error_code", "RESULT_READ_ERROR")
    return result


def run_mcd_custom_product_flow(order_url: str, args) -> dict:
    """麦当劳 customProduct 流程：打开链接 -> 点红色下单 -> 弹窗点「就是这个餐厅」-> 等取餐码（最多 60 秒）。"""
    flow_script = Path(__file__).resolve().parent / "mcd_custom_product_flow.py"
    if not flow_script.exists():
        raise RuntimeError(f"flow script not found: {flow_script}")

    wait_sec = getattr(args, "wait_pickup_seconds", 60)
    cmd = [
        sys.executable,
        str(flow_script),
        "--url",
        order_url,
        "--wait-pickup-seconds",
        str(wait_sec),
    ]
    if args.kfc_headless:
        cmd.append("--headless")
    if args.no_final_submit or not args.allow_final_submit:
        cmd.append("--no-submit")

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    result_file = extract_result_file(proc.stdout)
    if result_file is None:
        if proc.returncode != 0:
            raise RuntimeError(
                f"mcd customProduct flow failed(exit={proc.returncode}): {proc.stderr.strip() or proc.stdout.strip()}"
            )
        raise RuntimeError("mcd customProduct flow result file path not found in output")

    try:
        result = json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"failed to read flow result json: {exc}") from exc
    result["result_file"] = str(result_file)
    if proc.returncode != 0 and not result.get("error_code"):
        result.setdefault("error", proc.stderr.strip() or proc.stdout.strip())
        result.setdefault("error_code", "RESULT_READ_ERROR")
    return result


def detect_flow_code(order_resp: dict, url: str) -> tuple[str, dict]:
    """
    识别订单链接对应的流程，供 OpenClaw 准确选择脚本。优先级：
    1) 后端 order 返回的 flow.code（若存在）
    2) vip.woaicoffee.com + outId 且非 choose_specifications -> kfc_vip_choose_spec
    3) kfc.woaicoffee.cn + cdkey 且非 customProduct 路径 -> kfc_custom_product
    4) kfc.woaicoffee.cn -> kfc_city_store_booking
    5) mdl.woaicoffee.cn + cdkey 且非 customProduct 路径 -> mcd_custom_product
    6) mdl.woaicoffee.cn -> mcd_store_eattype
    7) 其他 -> 空（仅打开浏览器）
    """
    flow = order_resp.get("flow") if isinstance(order_resp, dict) else None
    if isinstance(flow, dict):
        code = str(flow.get("code") or "").strip()
        if code and code in FLOW_REGISTRY:
            return code, flow
    # 归一化：去掉 fragment，统一小写比较
    u = (url or "").strip()
    if u and "#" in u:
        u = u.split("#")[0]
    url_lower = u.lower()
    if "vip.woaicoffee.com" in url_lower and "outid=" in url_lower and "choose_specifications" not in url_lower:
        return "kfc_vip_choose_spec", flow or {}
    if "kfc.woaicoffee.cn" in url_lower and "cdkey=" in url_lower and "/index/index/customproduct" not in url_lower:
        return "kfc_custom_product", flow or {}
    if "kfc.woaicoffee.cn" in url_lower:
        return "kfc_city_store_booking", flow or {}
    if "mdl.woaicoffee.cn" in url_lower and "cdkey=" in url_lower and "/index/index/customproduct" not in url_lower:
        return "mcd_custom_product", flow or {}
    if "mdl.woaicoffee.cn" in url_lower:
        return "mcd_store_eattype", flow or {}
    return "", flow or {}


def get_flow_script(flow_code: str) -> str:
    """返回 flow_code 对应的脚本文件名，便于 OpenClaw 日志与校验。"""
    reg = FLOW_REGISTRY.get(flow_code)
    return reg["script"] if reg else ""


def format_flow_error(flow_code: str, result: dict | None, exc: Exception | None = None) -> str:
    """根据流程结果或异常生成用户可读的错误说明与处理建议。"""
    parts = []
    if result:
        err = (result.get("error") or "").strip()
        code = (result.get("error_code") or "").strip()
        if code and code in ERROR_REMEDIES:
            msg, suggestion = ERROR_REMEDIES[code]
            parts.append(f"[{code}] {msg}")
            parts.append(f"处理建议: {suggestion}")
        if err and err not in str(parts):
            parts.append(f"详情: {err}")
    if exc and not parts:
        parts.append(str(exc))
    return " ".join(parts) if parts else "流程执行失败，请查看 result_file 与截图。"


def resolve_kfc_store_code(base_url: str, city: str, keyword: str, timeout: int = 10) -> str:
    """Call backend API to resolve KFC store. GET {base_url}/kfc/store?city=xxx&keyword=xxx -> {"store_code": "SHA391"}."""
    url = f"{base_url.rstrip('/')}/kfc/store"
    try:
        resp = requests.get(
            url,
            params={"city": city.strip(), "keyword": keyword.strip()},
            timeout=timeout,
        )
        resp.encoding = "utf-8"
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"查询肯德基门店编号失败: {exc}") from exc
    try:
        data = resp.json()
    except ValueError as exc:
        raise RuntimeError("肯德基门店接口返回非 JSON") from exc
    code = (data.get("store_code") or data.get("storeCode") or data.get("store") or "").strip()
    if not code:
        raise RuntimeError(f"肯德基门店接口未返回 store_code，响应: {data}")
    return code


def resolve_mcd_store_code(base_url: str, keyword: str, timeout: int = 10) -> str:
    """Call backend API to resolve store keyword to store number. GET {base_url}/mcd/store?keyword=xxx -> {"store": "1450468"}."""
    url = f"{base_url.rstrip('/')}/mcd/store"
    try:
        resp = requests.get(url, params={"keyword": keyword.strip()}, timeout=timeout)
        resp.encoding = "utf-8"
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"查询麦当劳门店编号失败: {exc}") from exc
    try:
        data = resp.json()
    except ValueError as exc:
        raise RuntimeError("麦当劳门店接口返回非 JSON") from exc
    store = (data.get("store") or data.get("store_id") or "").strip()
    if not store:
        raise RuntimeError(f"麦当劳门店接口未返回 store，响应: {data}")
    return store


def build_kfc_custom_product_url(raw_url: str, store: str, booking_time: str = "0") -> str:
    """Convert kfc.woaicoffee.cn/?cdkey=xxx to customProduct URL with store and booking_time (0=立即取餐)."""
    parsed = urlparse(raw_url)
    qs = parse_qs(parsed.query)
    cdkey = (qs.get("cdkey") or [""])[0].strip()
    if not cdkey:
        raise RuntimeError("原始链接中缺少 cdkey 参数")
    base = "https://kfc.woaicoffee.cn/index/index/customProduct"
    query = {"cdkey": cdkey, "store": store, "booking_time": (booking_time or "0").strip()}
    return f"{base}?{urlencode(query)}"


def build_mcd_custom_product_url(raw_url: str, store: str, eat_type: str = MCD_CUSTOM_PRODUCT_EAT_TYPE) -> str:
    """Convert mdl.woaicoffee.cn/?cdkey=xxx to customProduct URL with store and eat_type (default 门店自提)."""
    parsed = urlparse(raw_url)
    qs = parse_qs(parsed.query)
    cdkey = (qs.get("cdkey") or [""])[0].strip()
    if not cdkey:
        raise RuntimeError("原始链接中缺少 cdkey 参数")
    base = "https://mdl.woaicoffee.cn/index/index/customProduct"
    query = {"cdkey": cdkey, "store": store, "eat_type": eat_type}
    return f"{base}?{urlencode(query)}"


def detect_brand_hint(product: dict) -> str:
    brand = str(product.get("brand", "") or "")
    name = str(product.get("name", "") or "")
    combined = f"{brand} {name}".lower()
    if "kfc" in combined:
        return "KFC"
    if "mcd" in combined or "mcdonald" in combined:
        return "McDonalds"
    return ""


def print_chat_report(order_resp: dict, flow_resp: dict) -> None:
    print("## OpenClaw Order Result")
    print(f"- order_id: `{order_resp.get('order_id', '')}`")
    print(f"- order_url: `{order_resp.get('url', '')}`")
    flow_meta = order_resp.get("flow") if isinstance(order_resp, dict) else None
    if isinstance(flow_meta, dict) and flow_meta:
        print(
            f"- flow: `{flow_meta.get('code', '')}` "
            f"`{flow_meta.get('name', '')}` stop_before=`{flow_meta.get('stop_before', '')}`"
        )
    print(f"- automation_status: `{flow_resp.get('status', '')}`")
    print(f"- final_url: `{flow_resp.get('final_url', '')}`")
    print(f"- final_confirm_visible: `{flow_resp.get('final_confirm_visible', False)}`")
    print(f"- final_confirm_clicked: `{flow_resp.get('final_confirm_clicked', False)}`")
    cost_yuan = order_resp.get("cost_yuan", order_resp.get("points_cost", ""))
    balance_yuan = order_resp.get("balance_yuan", order_resp.get("points_balance", ""))
    if cost_yuan != "":
        print(f"- cost_yuan: `{cost_yuan}`")
    if balance_yuan != "":
        print(f"- balance_yuan: `{balance_yuan}`")

    pickup_code = flow_resp.get("pickup_code", "")
    order_no = flow_resp.get("order_no", "")
    if pickup_code:
        print(f"- pickup_code: `{pickup_code}`")
    if order_no:
        print(f"- order_no: `{order_no}`")

    detail_lines = flow_resp.get("detail_lines", []) or []
    if detail_lines:
        print("- detail_lines:")
        for line in detail_lines[:10]:
            print(f"  - {line}")

    screenshots = flow_resp.get("screenshots", []) or []
    if screenshots:
        print("- screenshots:")
        for shot in screenshots:
            print(f"  - `{shot}`")

    print(f"- result_file: `{flow_resp.get('result_file', '')}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw order helper")
    parser.add_argument("--username", type=str, default="", help="identity username")
    parser.add_argument("--phone", type=str, default="", help="identity phone (preferred)")
    parser.add_argument("--api-key", type=str, default="", help="API key")
    parser.add_argument("--base-url", type=str, default="", help="backend base url")
    parser.add_argument("--product-id", type=int, default=0, help="product id (use 0 with --supplier-goods-id for supplier-only goods)")
    parser.add_argument("--supplier-goods-id", type=int, default=0, help="supplier goods id (for goods that exist only at supplier, id=0)")
    parser.add_argument("--product-name", type=str, default="", help="product name override")
    parser.add_argument(
        "--price-yuan",
        "--price-points",
        type=int,
        default=0,
        dest="price_yuan",
        help="price in yuan override (legacy: --price-points)",
    )
    parser.add_argument("--available-date", type=str, default="", help="available date override")
    parser.add_argument("--list-products", action="store_true", help="list products only")
    parser.add_argument("--idempotency-key", type=str, default="", help="idempotency key")
    parser.add_argument(
        "--query-order",
        type=str,
        default="",
        help="查询本地订单进度（传幂等键 idempotency_key），断连/恢复后可查当前阶段与订餐链接",
    )
    parser.add_argument(
        "--query-order-by-id",
        type=int,
        default=0,
        help="按 order_id 查询本地订单进度",
    )
    parser.add_argument(
        "--list-local-orders",
        action="store_true",
        help="列出本机最近保存的订单（order_id、阶段、更新时间），便于用 --query-order-by-id 查询",
    )
    parser.add_argument(
        "--fetch-order-status",
        type=int,
        default=0,
        dest="fetch_order_status",
        help="从服务器查询订单状态（order_id），需 --phone/--username 与 --api-key；不跑浏览器流程",
    )
    parser.add_argument(
        "--list-server-orders",
        action="store_true",
        help="从服务器拉取当前用户订单列表（POST /orders），需 API Key",
    )

    # Runtime inputs for the browser flow.
    parser.add_argument("--city", type=str, default="", help="KFC city")
    parser.add_argument("--store-keyword", type=str, default="", help="store keyword")
    parser.add_argument("--store-name", type=str, default="", help="store display name (optional)")
    parser.add_argument("--pickup-type", type=str, default="外带", help="KFC pickup type")
    parser.add_argument("--pickup-time", type=str, default="", help="KFC pickup time")
    parser.add_argument("--wait-taskslist-seconds", type=int, default=90, help="KFC tasksList wait seconds")
    parser.add_argument(
        "--kfc-store-code",
        type=str,
        default="",
        help="肯德基门店编号(如 SHA391)，VIP/customProduct 不填则用 city+store-keyword 调 API",
    )
    parser.add_argument(
        "--booking-time",
        type=str,
        default="0",
        help="肯德基 customProduct 预定时间编码，0=立即取餐",
    )
    parser.add_argument("--eat-type", type=str, default="Dine-in", help="McD eat type")
    parser.add_argument(
        "--mcd-store-number",
        type=str,
        default="",
        help="麦当劳 customProduct 门店编号，不填则用 store-keyword 调 API 查询",
    )
    parser.add_argument(
        "--wait-pickup-seconds",
        type=int,
        default=60,
        help="麦当劳 customProduct 等待取餐码最大秒数",
    )
    parser.add_argument("--kfc-headless", action="store_true", help="run browser headless")
    parser.add_argument("--no-final-submit", action="store_true", help="stop at final confirm")
    parser.add_argument("--allow-final-submit", action="store_true", help="allow clicking final confirm")
    parser.add_argument("--skip-flow", action="store_true", help="skip browser flow")
    parser.add_argument("--skip-kfc-flow", action="store_true", help="skip browser flow (legacy flag)")
    args = parser.parse_args()

    env_phone = os.getenv("KFC_PLATFORM_PHONE", "").strip() or os.getenv("OPENCLAW_PHONE", "").strip()
    env_username = os.getenv("KFC_PLATFORM_USERNAME", "").strip() or os.getenv("OPENCLAW_USERNAME", "").strip()
    env_api_key = os.getenv("KFC_PLATFORM_API_KEY", "").strip() or os.getenv("OPENCLAW_API_KEY", "").strip()

    args.phone = args.phone.strip()
    args.username = args.username.strip()
    args.api_key = args.api_key.strip() or env_api_key
    args.base_url = resolve_base_url(args.base_url)
    args.city = args.city.strip()
    args.store_keyword = args.store_keyword.strip()
    args.store_name = args.store_name.strip()
    args.pickup_time = args.pickup_time.strip()
    args.booking_time = (getattr(args, "booking_time", "") or "0").strip()
    args.eat_type = args.eat_type.strip()
    args.query_order = (getattr(args, "query_order", "") or "").strip()
    args.query_order_by_id = getattr(args, "query_order_by_id", 0) or 0
    args.list_local_orders = getattr(args, "list_local_orders", False)
    args.fetch_order_status = getattr(args, "fetch_order_status", 0) or 0
    args.list_server_orders = getattr(args, "list_server_orders", False)

    identity_probe = args.phone or env_phone or args.username or env_username

    if args.fetch_order_status > 0:
        if not identity_probe or not args.api_key:
            print(
                "error: --fetch-order-status 需要 --phone/--username 与 --api-key",
                file=sys.stderr,
            )
            return 1
        try:
            st = fetch_order_status(
                identity_probe,
                args.api_key,
                args.base_url,
                args.fetch_order_status,
            )
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(st, ensure_ascii=False, indent=2))
        return 0

    if args.list_server_orders:
        if not identity_probe or not args.api_key:
            print(
                "error: --list-server-orders 需要 --phone/--username 与 --api-key",
                file=sys.stderr,
            )
            return 1
        try:
            od = list_openclaw_orders(identity_probe, args.api_key, args.base_url)
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(od, ensure_ascii=False, indent=2))
        return 0

    # 列出本机最近订单（用户说「我最近的订单」时可由大模型调用）
    if args.list_local_orders:
        state_dir = get_order_state_dir()
        if not state_dir.exists():
            print("## 本机订单（本地无记录）")
            print("暂无保存的订单，请先下单或确认 OPENCLAW_ORDER_STATE_DIR 路径。")
            return 0
        entries = []
        for f in state_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                entries.append(data)
            except Exception:
                continue
        entries.sort(key=lambda x: (x.get("updated_at") or ""), reverse=True)
        entries = entries[:20]
        if not entries:
            print("## 本机订单（本地无记录）")
            return 0
        print("## 本机最近订单（可用 --query-order-by-id <order_id> 查看详情）")
        for i, e in enumerate(entries, 1):
            oid = e.get("order_id") or "-"
            stage = e.get("stage") or "-"
            url = (e.get("url") or "")[:60] + ("..." if len(e.get("url") or "") > 60 else "")
            updated = e.get("updated_at") or "-"
            print(f"{i}. order_id={oid} stage={stage} updated={updated}")
            if url:
                print(f"   url={url}")
        return 0

    # 查询本地订单进度（大模型恢复后或用户主动查「订单到哪了」）
    if args.query_order or args.query_order_by_id:
        if args.query_order_by_id:
            idem_key, state = find_order_state_by_order_id(args.query_order_by_id)
        else:
            idem_key = args.query_order
            state = load_order_state(idem_key)
        if not state:
            print(
                "error: 未找到该订单的本地记录，请确认 idempotency_key 或 order_id 正确，或订单尚未在本机执行过",
                file=sys.stderr,
            )
            return 1
        stage = state.get("stage") or "unknown"
        stage_desc = {
            "order_received": "已获得订餐链接，浏览器流程未执行",
            "flow_running": "浏览器流程执行中",
            "flow_done": "浏览器流程已完成",
            "flow_failed": "浏览器流程失败或中断",
        }.get(stage, stage)
        print("## 订单进度（本地保存）")
        print(f"- 阶段: {stage_desc}")
        print(f"- order_id: {state.get('order_id')}")
        print(f"- idempotency_key: {state.get('idempotency_key')}")
        if state.get("url"):
            print(f"- 订餐链接: {state['url']}")
            emit_order_result_for_chat(
                state["url"],
                idempotency_key=state.get("idempotency_key", ""),
                order_id=state.get("order_id") or 0,
                stage=stage,
            )
        else:
            print("- 订餐链接: （尚未返回）")
        if state.get("flow_result"):
            fr = state["flow_result"]
            if fr.get("pickup_code"):
                print(f"- 取餐码: {fr.get('pickup_code')}")
            if fr.get("order_no"):
                print(f"- 订单号: {fr.get('order_no')}")
        print(f"- 更新时间: {state.get('updated_at', '')}")
        return 0

    identity = args.phone or env_phone or args.username or env_username
    if not identity:
        print("error: missing identity, provide --phone or --username", file=sys.stderr)
        return 1
    if not args.api_key:
        print("error: missing api key, provide --api-key or KFC_PLATFORM_API_KEY", file=sys.stderr)
        return 1
    if not args.list_products and not args.store_keyword:
        print("error: store-keyword is required", file=sys.stderr)
        return 1

    try:
        products_data = get_products(identity, args.api_key, args.base_url)
        products = normalize_products(products_data)
        print(f"products: {products_data}")
        if args.list_products:
            print("## platform products")
            for item in products:
                sid = item.get("supplier_goods_id") or ""
                print(
                    f"- id={item.get('id')} name={item.get('name')} "
                    f"yuan={item.get('price_yuan', item.get('price_points'))} date={item.get('available_date')} stock={item.get('stock')}"
                    + (f" supplier_goods_id={sid}" if sid else "")
                )
            return 0

        supplier_goods_id = getattr(args, "supplier_goods_id", 0) or 0
        if args.product_id <= 0 and supplier_goods_id <= 0:
            print("error: --product-id or --supplier-goods-id is required for purchase", file=sys.stderr)
            return 1

        selected = find_product(products, args.product_id, supplier_goods_id)
        if selected is None:
            print(
                f"error: product_id={args.product_id} supplier_goods_id={supplier_goods_id} not found in platform products",
                file=sys.stderr,
            )
            return 1

        product_name = args.product_name.strip() or str(selected.get("name", "")).strip()
        price_yuan = args.price_yuan if args.price_yuan > 0 else int(
            selected.get("price_yuan") or selected.get("price_points", 0) or 0
        )
        available_date = args.available_date.strip() or str(selected.get("available_date", "")).strip()
        if not product_name or price_yuan <= 0:
            print("error: missing product_name/price_yuan and cannot infer from product list", file=sys.stderr)
            return 1

        brand_hint = detect_brand_hint(selected)
        skip_flow = args.skip_flow or args.skip_kfc_flow
        if not skip_flow:
            kfc_store_code = (getattr(args, "kfc_store_code", "") or "").strip()
            if brand_hint == "KFC" and not args.store_keyword:
                print("error: store-keyword is required for KFC flow", file=sys.stderr)
                return 1
            if brand_hint == "KFC" and not args.city and not kfc_store_code:
                print("error: city or --kfc-store-code is required for KFC flow", file=sys.stderr)
                return 1
            if brand_hint == "McDonalds" and not args.store_keyword:
                print("error: store-keyword is required for McDonalds flow", file=sys.stderr)
                return 1

        idem_key = args.idempotency_key.strip() or uuid.uuid4().hex
        order_product_id = int(selected.get("id", 0))
        order_supplier_goods_id = int(selected.get("supplier_goods_id", 0)) or supplier_goods_id
        order_resp = order(
            identity,
            args.api_key,
            args.base_url,
            order_product_id,
            product_name,
            price_yuan,
            available_date,
            idem_key,
            supplier_goods_id=order_supplier_goods_id,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    url = order_resp.get("url", "")
    if not url:
        print("error: response does not contain url", file=sys.stderr)
        return 1

    print(f"order result: {order_resp}")
    print(f"order url: {url}")

    # 立即落盘并输出可解析行，断连时大模型/客户端可从输出中取订餐链接展示给用户
    save_order_state(
        idem_key,
        order_id=order_resp.get("order_id") or 0,
        url=url,
        stage="order_received",
        flow_code=detect_flow_code(order_resp, url)[0],
        order_resp=order_resp,
    )
    emit_order_result_for_chat(
        url,
        idempotency_key=idem_key,
        order_id=order_resp.get("order_id") or 0,
        stage="order_received",
        order_resp=order_resp,
    )

    skip_flow = args.skip_flow or args.skip_kfc_flow
    flow_code, _ = detect_flow_code(order_resp, url)
    script_name = get_flow_script(flow_code)
    if script_name:
        print(f"flow_detected: {flow_code} -> {script_name}")
    if skip_flow:
        if not webbrowser.open(url):
            print("warning: browser may not open automatically", file=sys.stderr)
        return 0

    save_order_state(
        idem_key,
        url=url,
        order_id=order_resp.get("order_id") or 0,
        stage="flow_running",
        flow_code=flow_code,
        order_resp=order_resp,
    )

    try:
        if flow_code == "mcd_custom_product":
            store = (args.mcd_store_number or "").strip()
            if not store and not args.store_keyword:
                print("error: 麦当劳 customProduct 需提供 --store-keyword 或 --mcd-store-number", file=sys.stderr)
                return 1
            if not store:
                store = resolve_mcd_store_code(args.base_url, args.store_keyword)
            converted_url = build_mcd_custom_product_url(url, store)
            flow_resp = run_mcd_custom_product_flow(converted_url, args)
        elif flow_code == "kfc_vip_choose_spec":
            store_code = (getattr(args, "kfc_store_code", "") or "").strip()
            if not store_code and (not args.city or not args.store_keyword):
                print("error: 肯德基 VIP 链接需提供 --city 与 --store-keyword 或 --kfc-store-code", file=sys.stderr)
                return 1
            if not store_code:
                store_code = resolve_kfc_store_code(args.base_url, args.city, args.store_keyword)
            flow_resp = run_kfc_vip_choose_spec_flow(url, store_code, args)
        elif flow_code == "kfc_custom_product":
            store_code = (getattr(args, "kfc_store_code", "") or "").strip()
            if not store_code and (not args.city or not args.store_keyword):
                print("error: 肯德基 customProduct 需提供 --city 与 --store-keyword 或 --kfc-store-code", file=sys.stderr)
                return 1
            if not store_code:
                store_code = resolve_kfc_store_code(args.base_url, args.city, args.store_keyword)
            booking_time = (getattr(args, "booking_time", "") or "0").strip()
            converted_url = build_kfc_custom_product_url(url, store_code, booking_time)
            flow_resp = run_kfc_custom_product_flow(converted_url, args)
        elif flow_code.startswith("kfc"):
            if not args.city or not args.store_keyword:
                print("error: city and store-keyword are required for KFC flow", file=sys.stderr)
                return 1
            flow_resp = run_kfc_flow(url, args)
        elif flow_code.startswith("mcd"):
            if not args.store_keyword:
                print("error: store-keyword is required for McDonalds flow", file=sys.stderr)
                return 1
            flow_resp = run_mcd_flow(url, args)
        else:
            print(f"warning: unknown flow code {flow_code}, opening url only", file=sys.stderr)
            if not webbrowser.open(url):
                print("warning: browser may not open automatically", file=sys.stderr)
            return 0
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        try:
            fc = flow_code
        except NameError:
            fc = ""
        remedy = format_flow_error(fc, None, exc)
        if remedy:
            print(f"处理建议: {remedy}", file=sys.stderr)
        save_order_state(
            idem_key,
            url=url,
            order_id=order_resp.get("order_id") or 0,
            stage="flow_failed",
            flow_code=flow_code,
            flow_result={"error": str(exc)},
            order_resp=order_resp,
        )
        emit_order_result_for_chat(
            url,
            idempotency_key=idem_key,
            order_id=order_resp.get("order_id") or 0,
            stage="flow_failed",
            order_resp=order_resp,
        )
        return 1

    save_order_state(
        idem_key,
        url=url,
        order_id=order_resp.get("order_id") or 0,
        stage="flow_done",
        flow_code=flow_code,
        flow_result=flow_resp,
        order_resp=order_resp,
    )
    emit_order_result_for_chat(
        url,
        idempotency_key=idem_key,
        order_id=order_resp.get("order_id") or 0,
        stage="flow_done",
        order_resp=order_resp,
    )
    print_chat_report(order_resp, flow_resp)
    if flow_resp.get("status") == "failed" or flow_resp.get("error_code"):
        remedy = format_flow_error(flow_code, flow_resp)
        if remedy:
            print(f"## 报错与处理建议\n{remedy}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
