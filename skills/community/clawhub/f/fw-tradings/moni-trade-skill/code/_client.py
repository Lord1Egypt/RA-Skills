"""moni-trade-skill 公共客户端工厂。"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from zoneinfo import ZoneInfo

import logging

try:
    import urllib3
except ModuleNotFoundError:  # pragma: no cover - 兼容最小运行环境
    urllib3 = None

SKILL_ROOT = Path(__file__).resolve().parent.parent
FW_TRADE_ROOT = SKILL_ROOT.parent

# 复用同级 fosun-env-setup 的权威 apikey 错误码分类（单一事实源），
# 与 real-trade-skill 保持一致；fosun-env-setup 不可用时退化为内置集合，
# 保证模拟盘仍能在凭据出错时给出续期/重置/客服引导。
try:
    _SETUP_CODE_DIR = FW_TRADE_ROOT / "fosun-env-setup" / "code"
    if str(_SETUP_CODE_DIR) not in sys.path:
        sys.path.insert(0, str(_SETUP_CODE_DIR))
    from api_key_check import classify_api_key_error_code  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - 仅在脱离总入口的极简部署时触发
    _FALLBACK_APIKEY_STATUS = {
        40001: "invalid", 40015: "invalid",
        40005: "disabled", 40008: "disabled",
        40010: "expired",
    }

    def classify_api_key_error_code(code: Any) -> Optional[str]:
        try:
            return _FALLBACK_APIKEY_STATUS.get(int(code))
        except (TypeError, ValueError):
            return None


class APIError(Exception):
    """fsopenapi 未就绪时的占位异常类型。"""


SDKClient = Any
JsonFormatter = None
get_sdk_logger = None
_FSOPENAPI_READY = False

DEFAULT_SHARED_ENV_PATH = FW_TRADE_ROOT / "fosun.env"
SIM_TRADE_MARKETS = {"hk", "us"}
SIM_TRADE_PRODUCT_TYPES = {5, 6}
SIM_TRADE_ALLOWED_ORDER_TYPES = {3, 9}
SIM_TRADE_ALLOWED_MODIFY_TYPES = {1}
_PEM_WRAPPERS = {
    "FSOPENAPI_CLIENT_PRIVATE_KEY": ("-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----"),
    "FSOPENAPI_SERVER_PUBLIC_KEY": ("-----BEGIN PUBLIC KEY-----", "-----END PUBLIC KEY-----"),
}

ACCOUNT_INDEX_KEY = "FSOPENAPI_ACCOUNT_INDEX"
ACCOUNT_TYPE_LABELS = {
    0: "real_stock",
    1: "real_option",
    2: "mock",
}
SUPPORTED_ACCOUNT_TYPES = ("mock", "real_stock", "real_option")
SKILL_ALLOWED_ACCOUNT_TYPE = "mock"
_ACCOUNT_REFRESH_HINTS = (
    "subaccount",
    "sub_account",
    "account not found",
    "no permission",
    "无权限",
    "账户",
    "子账户",
)
_ACCOUNT_REFRESH_CODES = {60901, 90001, 90004, 90005}
_HK_SIM_BLOCK_START_MINUTE = 16 * 60 + 10
_HK_SIM_BLOCK_END_MINUTE = 24 * 60
_HK_MARKET_TZ = ZoneInfo("Asia/Shanghai")
CONFIRMATION_WINDOW_SECONDS = 15 * 60
CONFIRMATION_STATE_PATH = SKILL_ROOT / ".pending_confirmation.json"


class NoMockAccountError(RuntimeError):
    """共享凭证下不存在模拟盘子账户（subAccountType=2）。"""


class StructuredScriptError(RuntimeError):
    """带 error_code / hint / next_action 的结构化业务错误，供 run() 统一输出。"""

    def __init__(
        self,
        message: str,
        *,
        error_code: str,
        hint: str = "",
        next_action: str = "",
        exit_code: int = 2,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.hint = hint
        self.next_action = next_action
        self.exit_code = exit_code


def shared_env_path() -> Path:
    """共享凭证路径：优先 FOSUN_ENV_PATH，否则固定为总入口 `fw-trade-skill/fosun.env`。

    唯一真源与安装位置无关：由本文件路径推出 moni-trade-skill → 父目录即总入口，
    不猜 Agent 工作区等魔法前缀路径。
    """
    raw = (os.environ.get("FOSUN_ENV_PATH") or "").strip()
    if not raw:
        return DEFAULT_SHARED_ENV_PATH.resolve()
    path = Path(os.path.expandvars(os.path.expanduser(raw)))
    if not path.is_absolute():
        path = (DEFAULT_SHARED_ENV_PATH.parent / path).resolve()
    return path


def _candidate_env_files() -> list[Path]:
    return [shared_env_path()]


def load_env_file() -> Path:
    for path in _candidate_env_files():
        if path.exists():
            for key, value in _read_shared_entries(path).items():
                os.environ[key] = value
            return path
    raise FileNotFoundError(
        "未找到共享凭证文件。请先通过同级 fosun-env-setup 生成，确保 FOSUN_ENV_PATH 指向的文件存在且有效；"
        "未设置时默认解析为总 skill 根目录下的 fosun.env"
    )


def _read_shared_entries(path: Path | None = None) -> dict[str, str]:
    """读取共享 fosun.env 全部键值，兼容多行带引号 PEM 与 base64 单行 PEM。"""
    target = path or shared_env_path()
    if not target.exists():
        return {}
    entries: dict[str, str] = {}
    lines = target.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and not value.endswith('"'):
            parts = [value[1:]]
            i += 1
            while i < len(lines):
                part = lines[i]
                if part.endswith('"'):
                    parts.append(part[:-1])
                    break
                parts.append(part)
                i += 1
            value = "\n".join(parts)
        elif value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        if key:
            entries[key] = _ensure_pem(key, value)
        i += 1
    return entries


def _ensure_pem(key_name: str, value: str) -> str:
    value = str(value or "").strip()
    if not value or value.startswith("-----BEGIN "):
        return value
    wrapper = _PEM_WRAPPERS.get(key_name)
    if not wrapper:
        return value
    try:
        decoded = base64.b64decode(value).decode("utf-8")
        if decoded.strip().startswith("-----BEGIN "):
            return decoded.strip()
    except Exception:  # noqa: BLE001
        pass
    begin, end = wrapper
    raw = value.replace("\n", "").replace("\r", "").replace(" ", "")
    lines = [raw[i:i + 64] for i in range(0, len(raw), 64)]
    return begin + "\n" + "\n".join(lines) + "\n" + end


def _encode_env_value(key: str, value: Optional[str]) -> str:
    """与实盘 credential_flow 一致：PEM 字段写出时 base64 单行编码，其它原样。"""
    if value is None:
        return ""
    value = str(value).strip()
    if key in _PEM_WRAPPERS and value.startswith("-----BEGIN "):
        return base64.b64encode(value.encode("utf-8")).decode("utf-8")
    return value


def upsert_shared_env(updates: dict[str, Any]) -> None:
    """安全 upsert 共享 fosun.env：read-modify-write，不丢失实盘已有字段。"""
    env_path = shared_env_path()
    env_path.parent.mkdir(parents=True, exist_ok=True)
    entries = _read_shared_entries()
    for key, value in updates.items():
        entries[key] = "" if value is None else str(value)
    serialized = {k: _encode_env_value(k, v) for k, v in entries.items() if v is not None}
    with env_path.open("w", encoding="utf-8") as f:
        for key in sorted(serialized.keys()):
            f.write(f"{key}={serialized[key]}\n")
    for key, value in updates.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = str(value)


def _truthy(value: Optional[str]) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on", "debug"}


def _configure_sdk_debug_logger() -> None:
    """开启 SDK 原生 JSON 日志（stderr），仅在 FSOPENAPI_DEBUG 时调用。"""
    _ensure_fsopenapi_ready()
    logger = get_sdk_logger()
    logger.setLevel(logging.DEBUG)
    if any(getattr(h, "_moni_debug", False) for h in logger.handlers):
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    handler._moni_debug = True  # type: ignore[attr-defined]
    logger.addHandler(handler)


def build_client() -> SDKClient:
    _ensure_fsopenapi_ready()
    if urllib3 is not None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_env_file()
    base_url = os.environ.get("FSOPENAPI_BASE_URL")
    api_key = os.environ.get("FSOPENAPI_API_KEY")
    if not base_url or not api_key:
        raise EnvironmentError("FSOPENAPI_BASE_URL 与 FSOPENAPI_API_KEY 必须在 env 文件中配置")
    debug = _truthy(os.environ.get("FSOPENAPI_DEBUG"))
    log_body = _truthy(os.environ.get("FSOPENAPI_LOG_BODY"))
    if debug or log_body:
        _configure_sdk_debug_logger()
    return SDKClient(
        base_url,
        api_key,
        logging_enable=debug or log_body,
        log_body=log_body,
    )


def _ensure_fsopenapi_ready() -> None:
    global APIError, SDKClient, JsonFormatter, get_sdk_logger, _FSOPENAPI_READY
    if _FSOPENAPI_READY:
        return
    try:
        from fsopenapi import JsonFormatter as _JsonFormatter, SDKClient as _SDKClient, get_sdk_logger as _get_sdk_logger  # type: ignore[import-not-found]
        from fsopenapi.exceptions import APIError as _APIError  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        missing = getattr(exc, "name", None) or "unknown"
        raise StructuredScriptError(
            f"运行依赖缺失：`{missing}` 未安装。",
            error_code="DEPENDENCY_MISSING",
            hint=(
                "当前 Python 环境缺少 `fsopenapi` 及其依赖，脚本无法初始化 SDK 客户端。"
            ),
            next_action=(
                f"在当前环境先补齐缺失包：`{sys.executable} -m pip install {missing}`；"
                "若后续仍提示 `fsopenapi` 相关缺失，请在总 skill 根目录执行 install.sh 一次性安装共享 SDK 依赖后重试。"
            ),
            exit_code=2,
        ) from exc

    APIError = _APIError
    SDKClient = _SDKClient
    JsonFormatter = _JsonFormatter
    get_sdk_logger = _get_sdk_logger
    _FSOPENAPI_READY = True


def _coerce_sub_account_id(value: Any) -> str:
    """单一出口的 subAccountId 净化：强转 str + strip。

    历史踩坑：服务端有时返回 int，缓存写入后下游某些 SDK 调用会因类型不一致报错。
    本函数是 subAccountId 进出 _client.py 的唯一净化入口，任何路径都要走它。
    """
    if value is None:
        return ""
    return str(value).strip()


def _normalize_account_index(payload: Optional[dict]) -> dict:
    """把 list_accounts 响应分门别类成 {mock/real_stock/real_option: [...]} 索引。"""
    sub_accounts = (((payload or {}).get("data") or {}).get("subAccounts")) or []
    bucket: dict[str, list[dict]] = {label: [] for label in ACCOUNT_TYPE_LABELS.values()}
    for sub in sub_accounts:
        sub_type = sub.get("subAccountType")
        label = ACCOUNT_TYPE_LABELS.get(sub_type)
        if not label:
            continue
        bucket[label].append({
            "subAccountId": _coerce_sub_account_id(sub.get("subAccountId")),
            "subAccountType": sub_type,
            "chineseName": sub.get("chineseName"),
            "englishName": sub.get("englishName"),
            "status": sub.get("status"),
        })
    return {"refreshedAt": int(time.time()), **bucket}


def load_account_index() -> Optional[dict]:
    """读取共享 fosun.env 中已缓存的账户索引，未缓存返回 None。"""
    raw = os.environ.get(ACCOUNT_INDEX_KEY)
    if not raw:
        return None
    try:
        index = json.loads(raw)
    except (TypeError, ValueError):
        return None
    if not isinstance(index, dict):
        return None
    return index


def refresh_account_index(client: SDKClient) -> dict:
    """调一次账户列表，分类后写回共享 fosun.env，并刷新进程内缓存。"""
    response = client.account.list_accounts()
    index = _normalize_account_index(response)
    upsert_shared_env({ACCOUNT_INDEX_KEY: json.dumps(index, ensure_ascii=False)})
    return index


def sim_account_create(client: SDKClient) -> dict:
    """创建模拟账户，兼容新旧 SDK 封装。"""
    method = getattr(client.account, "sim_account_create", None)
    if callable(method):
        return method()
    return client.post("/v1/account/SimAccountCreate", data={})


def sim_account_reset(client: SDKClient, sub_account_id: str) -> dict:
    """重置模拟账户，兼容新旧 SDK 封装。"""
    method = getattr(client.account, "sim_account_reset", None)
    if callable(method):
        return method(sub_account_id)
    return client.post(
        "/v1/account/SimAccountReset",
        data={"subAccountId": _coerce_sub_account_id(sub_account_id)},
    )


def _pick_from_index(index: Optional[dict], account_type: str) -> Optional[str]:
    if not index:
        return None
    bucket = index.get(account_type) or []
    for item in bucket:
        sub_account_id = _coerce_sub_account_id(item.get("subAccountId"))
        if sub_account_id:
            return sub_account_id
    return None


def _find_account_type_by_sub_account_id(index: Optional[dict], sub_account_id: str) -> Optional[str]:
    if not index:
        return None
    target = _coerce_sub_account_id(sub_account_id)
    if not target:
        return None
    for label in SUPPORTED_ACCOUNT_TYPES:
        for item in index.get(label) or []:
            current = _coerce_sub_account_id(item.get("subAccountId"))
            if current == target:
                return label
    return None


def _index_is_empty(index: Optional[dict]) -> bool:
    if not index:
        return True
    return not any(index.get(label) for label in SUPPORTED_ACCOUNT_TYPES)


def _raise_no_mock_account(index: dict) -> None:
    """共享凭证下不存在 subAccountType=2 的模拟盘子账户时调用。"""
    visible = []
    for label in SUPPORTED_ACCOUNT_TYPES:
        for item in index.get(label) or []:
            sub_id = _coerce_sub_account_id(item.get("subAccountId"))
            if sub_id:
                name = item.get("chineseName") or item.get("englishName") or ""
                visible.append(f"{label}: {sub_id} {name}".strip())
    msg_lines = [
        "你选择了【模拟盘】交易，但当前共享凭证下未发现模拟盘子账户（subAccountType=2）。",
        "本次操作已停止，等待用户决策；模型不得擅自切换到实盘 skill 或自动改用其他账户继续操作。",
    ]
    if visible:
        msg_lines.append("共享凭证下可见的子账户（仅供参考，不得自动选用）：")
        msg_lines.extend(f"  - {item}" for item in visible)
    msg_lines.append(
        "请先把以下情况告知用户并等待其明确指示后再继续：\n"
        "  1) 是否前往券商开通模拟盘账户后重试；\n"
        "  2) 是否要显式 `--sub-account-id <ID>` 用某个已可见账户做调试（必须由用户指定具体 ID）。"
    )
    raise NoMockAccountError("\n".join(msg_lines))


def _ensure_skill_account_type(account_type: str) -> None:
    if account_type == SKILL_ALLOWED_ACCOUNT_TYPE:
        return
    raise StructuredScriptError(
        f"模拟盘脚本禁止解析 account_type={account_type}。",
        error_code="CROSS_TRADING_GUARD",
        hint=(
            "当前脚本是模拟盘隔离域，只允许 mock 子账户；"
            "任何 real_stock / real_option 路径都会被本地硬拦截。"
        ),
        next_action=(
            "立即停手并向用户确认盘别；若用户明确要实盘，请切换到 real-trade-skill，"
            "不要在模拟盘脚本里重试。"
        ),
        exit_code=2,
    )


def _validate_explicit_sub_account_id(
    client: SDKClient,
    sub_account_id: str,
    *,
    source: str,
    expected_account_type: str,
) -> str:
    target = _coerce_sub_account_id(sub_account_id)
    if not target:
        return target
    cached = load_account_index()
    actual_type = _find_account_type_by_sub_account_id(cached, target)
    if actual_type is None:
        refreshed = refresh_account_index(client)
        actual_type = _find_account_type_by_sub_account_id(refreshed, target)
    if actual_type is None:
        raise StructuredScriptError(
            f"{source} 指定的 subAccountId={target} 不在当前共享账户索引中。",
            error_code="CROSS_TRADING_GUARD",
            hint=(
                "无法确认该账户 ID 的盘别归属。为防串盘，模拟盘脚本不会盲信外部传入的账户 ID。"
            ),
            next_action=(
                "先运行 account_list.py 确认可见 mock 子账户，再由用户明确指定 mock 账户 ID 重试；"
                "禁止自动切实盘或改用其他账户。"
            ),
            exit_code=2,
        )
    if actual_type != expected_account_type:
        raise StructuredScriptError(
            f"{source} 指定的 subAccountId={target} 属于 {actual_type}，与模拟盘要求 {expected_account_type} 不一致。",
            error_code="CROSS_TRADING_GUARD",
            hint=(
                "检测到跨盘账户注入风险：模拟盘脚本收到非 mock 子账户。"
                "为避免串盘，本次操作已被硬拦截。"
            ),
            next_action=(
                "立即停手并向用户确认盘别；若用户明确要模拟盘，请改用 mock 子账户 ID 后重试。"
            ),
            exit_code=2,
        )
    return target


def resolve_sub_account_id(
    client: SDKClient,
    override: Optional[str] = None,
    account_type: str = "mock",
) -> str:
    """解析 subAccountId：CLI > 环境变量 > 共享 env 缓存 > 接口刷新缓存。

    严格按 subAccountType 分类：
    - 缓存命中对应类型 → 直接返回（零网络）
    - 缓存未命中 → 调一次 list_accounts 写回缓存再尝试
    - 仍未命中且 account_type=mock → 抛 NoMockAccountError，明确告知用户"无模拟账号"
    """
    _ensure_skill_account_type(account_type)
    if account_type not in SUPPORTED_ACCOUNT_TYPES:
        raise ValueError(
            f"不支持的账户类型：{account_type}；可选 {SUPPORTED_ACCOUNT_TYPES}"
        )
    override_clean = _coerce_sub_account_id(override)
    if override_clean:
        return _validate_explicit_sub_account_id(
            client,
            override_clean,
            source="CLI --sub-account-id",
            expected_account_type=account_type,
        )
    env_value = _coerce_sub_account_id(os.environ.get("MONI_SUB_ACCOUNT_ID"))
    if env_value:
        return _validate_explicit_sub_account_id(
            client,
            env_value,
            source="环境变量 MONI_SUB_ACCOUNT_ID",
            expected_account_type=account_type,
        )

    cached = load_account_index()
    if not _index_is_empty(cached):
        picked = _pick_from_index(cached, account_type)
        if picked:
            return picked

    refreshed = refresh_account_index(client)
    picked = _pick_from_index(refreshed, account_type)
    if picked:
        return picked

    if account_type == "mock":
        _raise_no_mock_account(refreshed)

    raise RuntimeError(
        f"未在 account_type={account_type} 找到子账户；"
        "请确认共享凭证已开通对应类型的子账户"
    )


def _looks_like_account_error(exc: APIError) -> bool:
    if getattr(exc, "code", None) in _ACCOUNT_REFRESH_CODES:
        return True
    message = str(getattr(exc, "message", "") or "").lower()
    return any(hint in message for hint in _ACCOUNT_REFRESH_HINTS)


def call_with_account_retry(
    client: SDKClient,
    factory,
    override: Optional[str] = None,
    account_type: str = "mock",
):
    """业务调用包装：

    - factory(sub_account_id) -> 调一次 SDK 接口
    - 第一次调用前用缓存解析 sub_account_id（零额外网络）
    - 出现账户类业务错（APIError）时，强刷缓存，**重新解析并重试一次**；
      若新旧 ID 完全一致，说明问题不在缓存而在业务参数，直接抛出原错误，避免无意义重试。
    - 任何路径传给 factory 的 sub_account_id 都强制为干净字符串，杜绝下游类型踩坑。
    """
    _ensure_skill_account_type(account_type)
    sub_account_id = _coerce_sub_account_id(
        resolve_sub_account_id(client, override, account_type)
    )
    try:
        return factory(sub_account_id)
    except APIError as exc:
        if not _looks_like_account_error(exc):
            raise
        refresh_account_index(client)
        new_sub_account_id = _coerce_sub_account_id(
            resolve_sub_account_id(client, override, account_type)
        )
        if new_sub_account_id == sub_account_id:
            raise
        print(
            f"[提示] 缓存中的 subAccountId={sub_account_id} 已失效，"
            f"已自动刷新为 {new_sub_account_id} 并重试。",
            file=sys.stderr,
        )
        return factory(new_sub_account_id)


def ensure_sim_trade_market(market_code: Optional[str]) -> None:
    if market_code and market_code not in SIM_TRADE_MARKETS:
        raise ValueError("模拟盘仅支持港股/美股交易，market-code 仅允许 hk 或 us")


def ensure_sim_trade_markets(market_codes: Optional[list[str]]) -> None:
    for market_code in market_codes or []:
        ensure_sim_trade_market(market_code)


def ensure_sim_trade_product_type(product_type: Optional[int]) -> None:
    if product_type is not None and product_type not in SIM_TRADE_PRODUCT_TYPES:
        raise ValueError("模拟盘仅支持港股/美股交易，product-type 仅允许 5=港股 或 6=美股")


def ensure_sim_trade_product_types(product_types: Optional[list[int]]) -> None:
    for product_type in product_types or []:
        ensure_sim_trade_product_type(product_type)


def ensure_sim_trade_order_type(order_type: Optional[int]) -> None:
    if order_type is not None and order_type not in SIM_TRADE_ALLOWED_ORDER_TYPES:
        raise StructuredScriptError(
            f"模拟盘不支持 orderType={order_type}。",
            error_code="INVALID_PARAM",
            hint=(
                "模拟盘交易能力白名单仅允许 3=限价单、9=市价单。"
            ),
            next_action=(
                "改用 orderType=3（限价）或 orderType=9（市价）后重试；"
                "条件单、跟踪止损、止盈止损、竞价/增强/特殊限价、暗盘订单一律不支持。"
            ),
            exit_code=2,
        )


def ensure_sim_us_night_session_order_supported(
    market_code: Optional[str],
    order_type: Optional[int],
    time_in_force: Optional[int],
) -> None:
    """模拟盘美股夜盘限制：不支持市价单。"""
    if (market_code or "").strip().lower() != "us":
        return
    if time_in_force != 4:
        return
    if order_type == 9:
        raise StructuredScriptError(
            "模拟盘美股夜盘不支持市价单（orderType=9）。",
            error_code="INVALID_PARAM",
            hint=(
                "当前参数组合是美股 + 夜盘(timeInForce=4) + 市价单(orderType=9)。"
                "模拟盘夜盘仅支持限价单，市价单会被本地拦截。"
            ),
            next_action="改用限价单（orderType=3 并传 --price）后重试，或去掉夜盘参数改为常规时段。",
            exit_code=2,
        )


def ensure_sim_hk_order_time_window(market_code: Optional[str]) -> None:
    """模拟盘港股时段硬拦截：16:10-00:00 不允许下单（含限价/市价）。"""
    if (market_code or "").strip().lower() != "hk":
        return
    now_local = datetime.now(_HK_MARKET_TZ)
    minute_of_day = now_local.hour * 60 + now_local.minute
    if _HK_SIM_BLOCK_START_MINUTE <= minute_of_day < _HK_SIM_BLOCK_END_MINUTE:
        raise StructuredScriptError(
            "模拟盘港股在 16:10-00:00 禁止下单（含限价单/市价单）。",
            error_code="INVALID_PARAM",
            hint=(
                f"当前市场时间 {now_local.strftime('%H:%M')}（Asia/Shanghai）落在受限区间，"
                "为避免夜盘虚假成交与状态歧义，脚本在本地硬拦截，不向网关发单。"
            ),
            next_action="请在 00:00 后重试港股模拟下单；如需当前时段交易，请先与用户确认改为其他市场或延后执行。",
            exit_code=2,
        )


def ensure_sim_trade_modify_type(modify_type: Optional[int]) -> None:
    if modify_type is not None and modify_type not in SIM_TRADE_ALLOWED_MODIFY_TYPES:
        raise StructuredScriptError(
            f"模拟盘不支持 modifyType={modify_type}。",
            error_code="INVALID_PARAM",
            hint="模拟盘仅允许普通改单 modifyType=1，不支持条件单改单。",
            next_action="若要改模拟盘订单，只能用 modifyType=1 并修改数量或价格。",
            exit_code=2,
        )


# 港股/美股市场维度的"三件套"对齐校验：market_code / currency / product_type 必须同向。
# 设计目的：
#   - 防止模型把"买美股"误下到港股市场（例如忘改 currency / product_type 仍为港股值）。
#   - 任何一个错配，都在本地直接报错，零网络代价、零误下单风险。
_SIM_TRADE_MARKET_TUPLES = {
    "hk": {"currency": "HKD", "product_type": 5, "label": "港股"},
    "us": {"currency": "USD", "product_type": 6, "label": "美股"},
}


def ensure_sim_trade_tuple_aligned(
    market_code: str,
    currency: str,
    product_type: int,
) -> None:
    """校验下单/改单/撤单三件套是否同向；任意错配立即抛 ValueError。"""
    expected = _SIM_TRADE_MARKET_TUPLES.get(market_code)
    if not expected:
        raise ValueError("模拟盘 market-code 仅允许 hk 或 us")
    mismatches = []
    if currency != expected["currency"]:
        mismatches.append(f"currency={currency} 应为 {expected['currency']}")
    if product_type != expected["product_type"]:
        mismatches.append(f"product-type={product_type} 应为 {expected['product_type']}")
    if mismatches:
        raise ValueError(
            f"市场参数错配（{expected['label']} {market_code}）："
            + "；".join(mismatches)
            + "。请显式对齐 market-code / currency / product-type 三件套，禁止依赖默认值。"
        )


def expand_market_to_tuple(market: str) -> dict:
    """`--market hk|us` → 完整市场三件套字典（market_code / currency / product_type）。

    设计意图：消灭模型每次下单都要在脑子里映射「港股=hk/HKD/5、美股=us/USD/6」
    这个高频出错点，把映射工作从模型推理移到本地常量表，零网络代价、零遗忘风险。
    """
    expected = _SIM_TRADE_MARKET_TUPLES.get(market)
    if not expected:
        raise ValueError("--market 仅支持 hk（港股）或 us（美股），其它值禁止")
    return {
        "market_code": market,
        "currency": expected["currency"],
        "product_type": expected["product_type"],
    }


def resolve_market_args(
    market: Optional[str],
    market_code: Optional[str],
    currency: Optional[str],
    product_type: Optional[int],
    *,
    require_currency: bool = True,
) -> tuple[str, Optional[str], int]:
    """下单/改单/撤单脚本统一的市场参数解析入口。

    设计意图：把「--market 简写优先 / 三件套兼容 / 互斥校验 / 对齐校验」四件事
    收敛到一个函数，三个交易脚本一行调用即可，避免每个脚本都散写一遍判断逻辑。

    使用规则：
      - 推荐路径：`--market hk` 或 `--market us`，自动展开成对应三件套
      - 兼容路径：显式同时传完整 --market-code/--currency/--product-type（高级用户）
      - 不允许两种路径混用（互斥），否则抛 INVALID_PARAM
      - cancel/modify 这类不需要 currency 的脚本，传 require_currency=False，
        currency 在返回值里恒为 None；展开时也不再要求其同传

    返回：(market_code, currency_or_None, product_type)
    """
    if market:
        if market_code or currency or (product_type is not None):
            raise ValueError(
                "--market 与 --market-code / --currency / --product-type 互斥，"
                "二选一即可：用 `--market hk|us`（推荐）或完整三件套（高级用户）"
            )
        expanded = expand_market_to_tuple(market)
        return (
            expanded["market_code"],
            expanded["currency"] if require_currency else None,
            expanded["product_type"],
        )

    if require_currency:
        if not (market_code and currency and product_type is not None):
            raise ValueError(
                "请用 `--market hk|us`（推荐），或同时显式传完整三件套 "
                "`--market-code / --currency / --product-type`，禁止依赖默认值"
            )
        ensure_sim_trade_tuple_aligned(market_code, currency, product_type)
        return (market_code, currency, product_type)

    if product_type is None:
        raise ValueError("请用 `--market hk|us`（推荐），或显式传 `--product-type 5|6`")
    ensure_sim_trade_product_type(product_type)
    return (market_code, None, product_type)


def ensure_sim_trade_show_type(show_type: Optional[int]) -> None:
    if show_type is not None and show_type != 0:
        raise ValueError("模拟盘不支持期权订单，show-type 仅允许 0=只有正股订单")


def ensure_sim_sub_account_class(sub_account_class: Optional[int]) -> None:
    if sub_account_class == 9:
        raise ValueError("模拟盘不支持期权账户，sub-account-class 不能传 9")


def _sanitize_confirmation_argv(argv: list[str]) -> list[str]:
    """归一化确认指纹输入：移除确认相关 flag，保留真实业务参数。"""
    sanitized: list[str] = []
    skip_next = False
    for token in argv:
        if skip_next:
            skip_next = False
            continue
        if token == "--confirm":
            continue
        if token == "--confirm-token":
            skip_next = True
            continue
        if token.startswith("--confirm-token="):
            continue
        sanitized.append(token)
    return sanitized


def _build_confirmation_fingerprint(*, action: str, intent_summary: str) -> str:
    """把动作 + 意图 + 当前命令参数绑定成稳定指纹，防止换参复用 token。"""
    payload = {
        "action": str(action or "").strip(),
        "intent": str(intent_summary or "").strip(),
        "argv": _sanitize_confirmation_argv(sys.argv[1:]),
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _issue_confirmation_challenge(
    *,
    action: str,
    intent_summary: str,
    confirmation_fingerprint: str,
) -> dict[str, Any]:
    issued_at = int(time.time())
    expires_at = issued_at + CONFIRMATION_WINDOW_SECONDS
    seed = (
        f"{confirmation_fingerprint}|{issued_at}|{time.time_ns()}|"
        f"{os.getpid()}|{os.urandom(8).hex()}"
    )
    token = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()
    challenge = {
        "action": action,
        "intent": intent_summary,
        "fingerprint": confirmation_fingerprint,
        "token": token,
        "issuedAt": issued_at,
        "expiresAt": expires_at,
    }
    CONFIRMATION_STATE_PATH.write_text(
        json.dumps(challenge, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return challenge


def _load_confirmation_challenge() -> Optional[dict[str, Any]]:
    if not CONFIRMATION_STATE_PATH.exists():
        return None
    try:
        data = json.loads(CONFIRMATION_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None
    return data if isinstance(data, dict) else None


def _clear_confirmation_challenge() -> None:
    try:
        CONFIRMATION_STATE_PATH.unlink(missing_ok=True)
    except OSError:
        pass


def ensure_user_confirmed(
    confirmed: bool,
    *,
    action: str,
    intent_summary: str,
    confirm_token: Optional[str] = None,
) -> None:
    """变更类脚本运行时强制：必须显式 `--confirm` 才能继续。

    设计意图：把"变更操作二次确认"从 SKILL.md 的纸面铁律下沉到运行时拦截，
    模型即使漏看 SKILL.md 第 2 条铁律，也无法绕过 —— 脚本会直接抛
    NEED_CONFIRMATION 结构化错误，强制模型回头先用自然语言找用户确认。

    Args:
        confirmed: argparse `--confirm` 的取值；True 才放行。
        action: 中文动作名（"下单" / "改单" / "撤单" / "创建模拟账户" / "重置模拟账户"），用于错误信息。
        intent_summary: 模型必须复述给用户的最小字段清单提示（脚本相关）。
    """
    normalized_intent = str(intent_summary or "").strip()
    if not normalized_intent:
        raise StructuredScriptError(
            f"{action}操作缺少意图摘要（intent）。",
            error_code="INVALID_PARAM",
            hint=(
                "变更类操作必须要求模型先复述完整意图，再走二次确认流程；"
                "intent 为空会导致确认链路失去语义绑定。"
            ),
            next_action=(
                f"先补充本次{action}的完整意图摘要（包含关键对象与参数），"
                "再触发确认流程。"
            ),
            exit_code=2,
        )
    current_fingerprint = _build_confirmation_fingerprint(
        action=action,
        intent_summary=normalized_intent,
    )
    if not confirmed:
        challenge = _issue_confirmation_challenge(
            action=action,
            intent_summary=normalized_intent,
            confirmation_fingerprint=current_fingerprint,
        )
        raise StructuredScriptError(
            f"{action}操作未确认：必须先让用户明确同意，再带确认令牌执行。",
            error_code="NEED_CONFIRMATION",
            hint=(
                f"变更类操作（{action}）会改变账户或订单状态（模拟盘同样按真实交易流程控制），"
                "禁止一条命令直接执行。系统已生成一次性确认令牌，并同时绑定当前意图与完整命令参数。"
            ),
            next_action=(
                f"先用自然语言把完整{action}意图（{normalized_intent}）复述给用户并获得明确同意；"
                f"随后在原命令追加 `--confirm --confirm-token {challenge['token']}` 重试。"
                "令牌 15 分钟内有效，且只对当前意图生效。"
            ),
            exit_code=2,
        )

    provided_token = str(confirm_token or "").strip().upper()
    challenge = _load_confirmation_challenge()
    now_ts = int(time.time())
    valid = bool(
        challenge
        and provided_token
        and challenge.get("token") == provided_token
        and challenge.get("action") == action
        and str(challenge.get("intent") or "").strip() == normalized_intent
        and str(challenge.get("fingerprint") or "") == current_fingerprint
        and int(challenge.get("expiresAt") or 0) >= now_ts
    )
    if not valid:
        refreshed = _issue_confirmation_challenge(
            action=action,
            intent_summary=normalized_intent,
            confirmation_fingerprint=current_fingerprint,
        )
        raise StructuredScriptError(
            f"{action}确认令牌无效、缺失或已过期，已阻止执行。",
            error_code="NEED_CONFIRMATION",
            hint=(
                "二次确认采用一次性令牌，且强绑定操作类型、意图摘要与命令参数指纹；"
                "无法通过复用旧令牌、偷偷改参数或跳过令牌直接执行订单操作。"
            ),
            next_action=(
                f"请重新向用户确认本次{action}意图，然后使用新的确认令牌重试："
                f"`--confirm --confirm-token {refreshed['token']}`。"
            ),
            exit_code=2,
        )
    _clear_confirmation_challenge()


def dump(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


# v1.7.5：标的代码自动规范化。
# 实测发现 SDK 对无前缀的标的代码（"01810" / "AAPL"）会 silent fail：
# 返回 ok=true / code=0 / message="success" 但 data=null，模型读到 ok=true 会误以为成功。
# 治本方案：在脚本侧把"用户原话格式"统一规范化为 SDK 接受的"<前缀><代码>"格式，
# 让模型可以原样把用户说的"01810"或"AAPL"传进来，连市场前缀都不用想。
_HK_BOARD_LOTS = re.compile(r"^\d{1,5}$")
_US_TICKER = re.compile(r"^[A-Z]{1,5}([.\-][A-Z0-9]{1,3})?$", re.IGNORECASE)
_KNOWN_PREFIXES_LOWER = ("hk", "us", "sh", "sz")


def normalize_security_code(raw: str) -> tuple[str, Optional[str]]:
    """把"用户原话"格式的标的代码规范化为 SDK 接受的 `<市场前缀><代码>` 格式。

    返回值：(normalized_code, note)
      - note 为 None 表示规范化成功
      - note 为字符串表示无法可靠推断（已原样返回，让 API 自然报错；同时给模型 hint）

    规则（v1.7.5 起，与 SKILL.md 速抄表 / JSON 模板对齐）：
      - 已带合法小写前缀（`hk` / `us` / `sh` / `sz`）→ 原样返回（不动）
      - 大写前缀格式 `HK.01810` / `US.AAPL` → 转成 `hk01810` / `usAAPL`
      - 纯数字（1-5 位） → 港股，补 `hk` 前缀；不足 5 位前面补 `0`（港股板号习惯）
      - 纯字母（A-Z，1-5 个字符） → 美股，补 `us` 前缀；字母统一大写
      - 字母 + 单点 + 字母数字（如 `BRK.B` / `BABA.O`） → 美股，补 `us`
      - 其它格式（含中划线、长短超出常理）→ 原样返回 + note，让 API 报错或人工介入
    """
    if not isinstance(raw, str):
        return str(raw), "标的代码不是字符串，已 str() 转换并原样返回"
    s = raw.strip()
    if not s:
        return s, "标的代码为空字符串"

    upper = s.upper()
    # 先处理点分大写格式（必须在"已带前缀"判断之前，否则 `us.aapl` 会被误判为已带 `us` 前缀）
    for prefix_upper in ("HK.", "US.", "SH.", "SZ."):
        if upper.startswith(prefix_upper):
            body = upper[len(prefix_upper):]
            if not body:
                return s, f"`{s}` 形似 `{prefix_upper}<代码>` 但代码部分为空"
            mkt = prefix_upper[:2].lower()
            # 港股板号补 0 到 5 位
            if mkt in ("hk", "sh", "sz") and body.isdigit():
                body = body.zfill(5)
            return mkt + body, None

    lower = s.lower()
    for prefix in _KNOWN_PREFIXES_LOWER:
        if lower.startswith(prefix) and len(s) > len(prefix):
            # 已有合法前缀（如 hk00700 / usAAPL），原样返回；只把前缀部分小写化
            body = s[len(prefix):]
            # 防御性：如果 body 第一个字符是 `.`，是点分格式漏网，去掉
            if body.startswith("."):
                body = body[1:]
            return prefix + body, None

    if _HK_BOARD_LOTS.match(s):
        # 纯数字，按港股处理；港股板号习惯前导 0 到 5 位（00700 / 00388 / 09888）
        return "hk" + s.zfill(5), None

    if _US_TICKER.match(s):
        return "us" + upper, None

    # 兜底：返回原样 + 标记，让模型/用户看到不规范的标的代码 hint
    return s, (
        f"`{s}` 不像标准的港股板号（5 位数字）/ 美股 ticker（1-5 位字母）/ 已带合法前缀（hk/us/sh/sz）的格式，"
        "已原样转给 SDK；如果 API 报错或返回空 data，请向用户确认完整的市场+代码。"
    )


def normalize_trade_stock_code(raw: str, market_code: str) -> str:
    """规范化交易接口的 stockCode。

    行情接口用 `hk00700` / `usAAPL` 这种带市场前缀的 symbol；OrderCreate 文档明确
    把市场拆成 `marketCode`，`stockCode` 只传纯代码（如 marketCode=hk, stockCode=00700）。
    因此交易变更接口不能复用 normalize_security_code 的输出。
    """
    market = (market_code or "").strip().lower()
    if not market:
        raise StructuredScriptError(
            "缺少 marketCode，无法把标的代码规范化为交易接口 stockCode。",
            error_code="INVALID_PARAM",
            hint="交易接口的 stockCode 依赖 marketCode 判定是否需要剥离 hk/us/sh/sz 前缀。",
            next_action="使用 `--market hk|us`，或显式传齐 `--market-code/--currency/--product-type` 后重试。",
            exit_code=2,
        )

    s = str(raw).strip()
    if not s:
        raise StructuredScriptError(
            "标的代码为空。",
            error_code="INVALID_PARAM",
            hint="stockCode 是下单必填字段，不能为空。",
            next_action="向用户确认具体标的代码后重试。",
            exit_code=2,
        )

    explicit_prefix: Optional[str] = None
    body = s
    upper = s.upper()
    for prefix_upper in ("HK.", "US.", "SH.", "SZ."):
        if upper.startswith(prefix_upper):
            explicit_prefix = prefix_upper[:2].lower()
            body = s[len(prefix_upper):]
            break

    if explicit_prefix is None:
        lower = s.lower()
        for prefix in _KNOWN_PREFIXES_LOWER:
            if lower.startswith(prefix) and len(s) > len(prefix):
                explicit_prefix = prefix
                body = s[len(prefix):]
                if body.startswith("."):
                    body = body[1:]
                break

    if explicit_prefix and explicit_prefix != market:
        raise StructuredScriptError(
            f"标的代码前缀 `{explicit_prefix}` 与市场 `{market}` 不一致。",
            error_code="INVALID_PARAM",
            hint=(
                "交易接口同时有 marketCode 和 stockCode，二者必须指向同一市场；"
                "禁止把 hk00700 这类带前缀代码拿去配 us 市场，或反过来。"
            ),
            next_action="停手并向用户确认市场与标的代码；确认后用 `--market` 和匹配的 `--stock-code` 重试。",
            exit_code=2,
        )

    body = body.strip()
    if not body:
        raise StructuredScriptError(
            f"`{s}` 形似市场前缀，但代码部分为空。",
            error_code="INVALID_PARAM",
            hint="例如 `hk00700` 可拆成 marketCode=hk + stockCode=00700；但只有 `hk` 没有实际股票代码。",
            next_action="向用户确认完整标的代码后重试。",
            exit_code=2,
        )

    if market == "hk":
        if not body.isdigit():
            raise StructuredScriptError(
                f"港股 stockCode 应为纯数字代码，当前得到 `{body}`。",
                error_code="INVALID_PARAM",
                hint="OrderCreate 文档示例为 marketCode=hk + stockCode=00700；不要传 hk00700，也不要传非数字 ticker。",
                next_action="向用户确认港股 5 位数字代码后重试。",
                exit_code=2,
            )
        return body.zfill(5)

    if market == "us":
        return body.upper()

    return body


def ensure_order_create_effective(result: Any) -> str:
    """校验下单返回是否可证明"真实落单"；返回标准化 order_id。"""
    if not isinstance(result, dict):
        raise StructuredScriptError(
            "下单接口返回结构异常，无法确认是否真正创建订单。",
            error_code="ORDER_CREATE_UNVERIFIABLE",
            hint=(
                "SDK 返回不是 JSON 对象（dict），这意味着当前结果无法提取 code/message/data，"
                "不能据此向用户声称“下单成功”。"
            ),
            next_action=(
                "停止汇报“成功”，先把原始返回和 requestId（若有）反馈给用户，并要求运维修复 SDK/网关返回格式后重试。"
            ),
            exit_code=2,
        )

    code = result.get("code")
    message = str(result.get("message") or "").strip().lower()
    data = result.get("data")
    if code == 0 and data is None and message in ("success", "ok", ""):
        raise StructuredScriptError(
            "下单返回出现 silent-fail：code=0 但 data=null，无法确认订单落库。",
            error_code="ORDER_CREATE_SILENT_FAIL",
            hint=(
                "这是典型的“成功外壳”响应：接口看似成功，但没有任何订单实体。"
                "在未拿到真实订单标识前，不能对用户宣称下单成功。"
            ),
            next_action=(
                "立即停止后续动作并原样告知用户失败；检查 stockCode/marketCode/price/quantity 等入参后重试。"
            ),
            exit_code=2,
        )

    data_dict = data if isinstance(data, dict) else {}
    order_id = (
        data_dict.get("orderId")
        or data_dict.get("orderID")
        or data_dict.get("order_id")
        or result.get("orderId")
        or result.get("orderID")
        or result.get("order_id")
    )
    order_id = str(order_id or "").strip()
    if code == 0 and not order_id:
        raise StructuredScriptError(
            "下单返回缺少 orderId，无法证明订单已被持久化。",
            error_code="ORDER_CREATE_NO_ORDER_ID",
            hint=(
                "订单查询与后续改单/撤单都依赖 orderId。没有 orderId 时，"
                "本次响应不具备可核验性，不能被当作真实成功。"
            ),
            next_action=(
                "把本次下单判定为失败并回传给用户；请携带同参数重试，仍失败则提交网关日志排查。"
            ),
            exit_code=2,
        )
    return order_id


def _extract_order_mutation_evidence(result: dict[str, Any]) -> dict[str, Any]:
    data = result.get("data")
    data_dict = data if isinstance(data, dict) else {}
    order_id = (
        data_dict.get("orderId")
        or data_dict.get("orderID")
        or data_dict.get("order_id")
        or result.get("orderId")
        or result.get("orderID")
        or result.get("order_id")
    )
    order_status = (
        data_dict.get("orderStatus")
        or data_dict.get("status")
        or result.get("orderStatus")
        or result.get("status")
    )
    return {
        "orderId": str(order_id).strip() if order_id not in (None, "") else "",
        "orderStatus": order_status,
        "data": data,
    }


def _ensure_order_mutation_effective(result: Any, *, action_zh: str) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise StructuredScriptError(
            f"{action_zh}接口返回结构异常，无法确认是否真正生效。",
            error_code="ORDER_MUTATION_UNVERIFIABLE",
            hint="SDK 返回不是 JSON 对象（dict），无法提取可核验字段。",
            next_action=(
                f"停止汇报“{action_zh}成功”，先把原始返回和 requestId（若有）反馈给用户，并要求排查网关返回格式。"
            ),
            exit_code=2,
        )

    code = result.get("code")
    message = str(result.get("message") or "").strip().lower()
    evidence = _extract_order_mutation_evidence(result)
    if code == 0 and evidence["data"] is None and message in ("success", "ok", ""):
        raise StructuredScriptError(
            f"{action_zh}返回出现 silent-fail：code=0 但 data=null，无法确认订单状态变更。",
            error_code="ORDER_MUTATION_SILENT_FAIL",
            hint=(
                "这是“成功外壳”响应：接口看似成功，但没有任何订单实体或状态字段，"
                "不能据此向用户宣称操作已经生效。"
            ),
            next_action=f"立即停止并向用户如实反馈失败；核对订单参数后再重试。",
            exit_code=2,
        )

    if code == 0 and not evidence["orderId"] and evidence["orderStatus"] in (None, ""):
        raise StructuredScriptError(
            f"{action_zh}返回缺少可核验证据（orderId/orderStatus）。",
            error_code="ORDER_MUTATION_NO_EVIDENCE",
            hint=(
                "未返回 orderId 或 orderStatus 时，无法证明改单/撤单已被系统接受并落到订单实体。"
            ),
            next_action=(
                f"把本次{action_zh}判定为失败并回传给用户；请携带同参数重试，仍失败则提交网关日志排查。"
            ),
            exit_code=2,
        )
    return {"orderId": evidence["orderId"], "orderStatus": evidence["orderStatus"]}


def ensure_order_modify_effective(result: Any) -> dict[str, Any]:
    return _ensure_order_mutation_effective(result, action_zh="改单")


def ensure_order_cancel_effective(result: Any) -> dict[str, Any]:
    return _ensure_order_mutation_effective(result, action_zh="撤单")


def normalize_codes_inplace(args: argparse.Namespace, *fields: str) -> list[str]:
    """对 args 上的多个字段做标的代码规范化。返回所有"无法可靠推断"的 note 列表（用于 hint）。

    用法：在脚本 parse_args() 之后调用：
        notes = normalize_codes_inplace(args, "code", "stock_code", "symbols")
    支持单值字段（str）和多值字段（list[str]，对应 action="append"）。
    """
    notes: list[str] = []
    for field in fields:
        attr = field.replace("-", "_")
        if not hasattr(args, attr):
            continue
        value = getattr(args, attr)
        if value is None:
            continue
        if isinstance(value, list):
            new_list: list[str] = []
            for raw in value:
                if raw is None:
                    new_list.append(raw)
                    continue
                norm, note = normalize_security_code(str(raw))
                new_list.append(norm)
                if note:
                    notes.append(note)
            setattr(args, attr, new_list)
        else:
            norm, note = normalize_security_code(str(value))
            setattr(args, attr, norm)
            if note:
                notes.append(note)
    return notes


def dump_with_directive(
    data: Any,
    *,
    next_action: str,
    **directives: Any,
) -> None:
    """带"模型指令"的结构化输出（v1.7.3 起接受任意 JSON-serializable data）。

    设计意图：让模型读 stdout 的第一刻就拿到"接下来该做什么"的明确指令，
    把流程纪律从"靠 SKILL.md 自觉"升级成"靠运行时输出强制"。
    长会话中模型对 SKILL.md 的注意力会衰减，但**每条 stdout 的 next_action 是 stateless 的**，
    无论会话多长都会重新喂到模型嘴边，是抗衰减的最强武器。

    输出契约：
        {
          "ok": true,
          "next_action": "...",   # 祈使句，告诉模型下一步必须做什么
          ...directives,          # 决策辅助字段（如 mock_account_available, accounts_summary）
          # 末尾追加 data：
          ...data                 # 当 data 是 dict 时，平铺到顶层（向后兼容 v1.7.2 之前的 4 个调用者）
          "data": data            # 当 data 是 list/dataclass/None 时，包到 "data" 字段
        }

    用法：所有"查询型/meta 型/行情型"脚本都应该用本函数而不是 dump()，
    用来强制模型停手汇报、避免自动连环跑业务脚本——这是抗长会话衰减的关键基建。
    """
    payload = {"ok": True, "next_action": next_action, **directives}
    if isinstance(data, dict):
        payload.update(data)
    else:
        payload["data"] = data

    # v1.7.5：silent fail 兜底。
    # 实测 SDK 对无效标的代码会回 `{code:0, data:null, message:"success"}`——
    # 模型若直接读 ok=true 会误以为查到数据，最危险是凭空编一个数字汇报给用户。
    # 这里在输出层强制把这种"成功外壳 + 空 data"重写成 ok=false + INVALID_PARAM，
    # 与 normalize_security_code（事前规范化）形成二层防御。
    raw_data_field = payload.get("data")
    raw_code_field = payload.get("code")
    raw_message = (payload.get("message") or "").lower()
    if (
        raw_code_field == 0
        and raw_data_field is None
        and raw_message in ("success", "ok", "")
    ):
        silent_fail_payload = {
            "ok": False,
            "error_code": "SILENT_FAIL_EMPTY_DATA",
            "message": (
                "SDK 返回 code=0 / message=success 但 data=null —— 这是 silent failure。"
                "最常见原因：标的代码格式不对（如缺市场前缀、代码不存在），SDK 静默吞掉错误，没有真实数据。"
            ),
            "hint": (
                "v1.7.5 起脚本侧已经对入参做 normalize_security_code 自动补前缀，"
                "如果还触发本错误，意味着 normalize 后的代码也无法被 SDK 识别（多半是真的不存在的标的，或者用了非常非常规的格式）。"
                "**禁止**把本次失败解读成『查到了空数据』或自己编一个价格——data 是空的、不是 0。"
            ),
            "next_action": (
                "立即停手并把『SDK 返回空数据』如实告诉用户，请用户**确认完整的标的代码**（含市场，如 hk00700/usAAPL）后再重试。"
                "不要自己猜代码、不要把 ok=true 的语义误读成成功；本次没有任何可汇报的真实数据。"
            ),
            "_silent_fail_payload_preview": payload,
        }
        print(json.dumps(silent_fail_payload, ensure_ascii=False, indent=2, default=str), file=sys.stderr)
        sys.exit(2)

    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


# 业务错误码 → (hint, next_action)。命中即在 stderr 输出可被模型直接读取的下一步建议。
# 设计原则：
#   - hint 解释"为什么会这样"（机制层面），帮模型理解，不要让它瞎猜
#   - next_action 是"模型该做什么"的祈使句，越具体越好；做不了就让它"停手转告用户"
#   - 这里只覆盖**已知会反复踩**的错误码；未知码走通用兜底，避免误导
# apikey 相关错误码（40001/40005/40008/40010/40015）不在此硬编码，
# 改由 classify_api_key_error_code 统一识别 → _APIKEY_ERROR_GUIDANCE 按 status 引导，
# 避免与权威源分叉。模拟盘不负责鉴权，统一引导用户回 real-trade-skill 处理。
# error_code 仍沿用 APIERROR_<code>（与 SKILL.md 错误码矩阵一致）；
# 引导文案按 status 统一，避免与权威源分叉。
_APIKEY_ERROR_GUIDANCE: dict[str, dict[str, str]] = {
    "invalid": {
        "account_action": "reset",
        "hint": "共享凭证中的 apikey 无效或客户端密钥不匹配，模拟盘无法自行修复。",
        "next_action": (
            "停手，引导用户回同级 real-trade-skill 完成重置扫码；"
            "提醒：若已开通过 OpenAPI，页面上须点「忘记 API 参数」再重置；"
            "扫码后必须把页面上 API Key 与服务端公钥（PEM）一并发给 Agent，"
            "由 real-trade-skill 执行 update_api_key.py（--api-key 与 --server-public-key）写入共享 fosun.env 后再重试。"
        ),
    },
    "expired": {
        "account_action": "renew",
        "hint": "共享凭证中的 apikey 已过期，模拟盘无法自行续期。",
        "next_action": (
            "停手，引导用户回到同级 real-trade-skill 执行续期流程（扫码）；"
            "续期只延长原 apikey 有效期，不覆盖 fosun.env 中的 API Key，无需用户回填；"
            "扫码完成后让用户直接重试当前模拟盘命令。"
        ),
    },
    "disabled": {
        "account_action": "contact_support",
        "hint": "共享凭证中的 apikey 已被禁用或撤销，无法自助恢复。",
        "next_action": (
            "停手，用大白话告知用户 OpenAPI 账号已被禁用/撤销，请联系星财富客服；"
            "不要尝试 TicketCreate 或生成二维码。"
        ),
    },
}

APIERROR_PLAYBOOK: dict[Any, dict[str, str]] = {
    50001: {
        "hint": "服务端列表类接口对分页 Count 字段强校验，未传或传 0 都会拒绝。",
        "next_action": "在命令行追加 `--count 50`（或合理分页值）后重试一次；不要重复用同样参数重试。",
    },
    60006: {
        "hint": "服务端业务校验失败，多见于价格/数量越界、停牌、币种不符等。",
        "next_action": "原样把错误信息转告用户，等待用户调整委托参数后再重试，禁止自行猜测修正。",
    },
    60009: {
        "hint": "单笔委托金额超过模拟盘限额。",
        "next_action": "建议用户减少 quantity 或换一只单价更低的标的；不要用相同参数重试。",
    },
    60014: {
        "hint": "委托被风控/合规拦截。",
        "next_action": "原样转告用户错误码与 message，等待用户决定是否换标的或参数。",
    },
}


def _apierror_message_playbook(message: str) -> Optional[dict[str, str]]:
    """按 APIError message 做二次识别，补上 code 维度覆盖不到的高频故障。

    用关键词组合匹配而非整段子串，覆盖 "session expired" / "session is expired" /
    "session has been expired" / "your session expired" 等服务端文案变体，避免漏识别。
    """
    lower = (message or "").strip().lower()
    if "session" in lower and ("expir" in lower or "invalid" in lower or "timeout" in lower or "time out" in lower or "timed out" in lower):
        return {
            "error_code": "SESSION_EXPIRED",
            "hint": "共享凭证里的券商会话已过期。当前失败不是“订单/持仓不存在”，而是查询/操作通道失效。",
            "next_action": "先跑 `check_shared_env.py` 体检共享凭证；若仍报会话失效，提示用户通过同级 `fosun-env-setup` 修复或重新生成共享凭证后再重试。不要把这次失败解读成“订单不存在”或“查无结果”。",
        }
    if "signature" in lower and ("invalid" in lower or "verify" in lower or "verification" in lower or "mismatch" in lower):
        return {
            "error_code": "INVALID_SIGNATURE",
            "hint": "共享凭证里的 API Key / 公私钥签名链已失效。当前失败不是业务查无此单，而是凭证链路失效。",
            "next_action": "提示用户通过同级 `fosun-env-setup` 修复或重新生成共享凭证，再重试当前操作；不要把这次失败解读成“订单不存在”。",
        }
    return None


def _maybe_inject_from_args_json() -> None:
    """v1.7.4 新增：让所有脚本统一支持 `--args-json '<JSON 对象>'` 入参。

    动机：模型在长会话里最容易脑补「参数名」（--ticker / --stock_code 等）。给一个 JSON
    填空模板让模型只填值，连 CLI 翻译都不用做，是最强的反脑补防线。

    转换规则（机械、零思考）：
      - JSON key → CLI flag：加 `--` 前缀；`_` → `-`（如 `stock_code` → `--stock-code`）
      - JSON value 是 bool=true → 只放 flag 名（store_true）
      - JSON value 是 bool=false → 跳过（默认即 false）
      - JSON value 是 list → 重复 `--key v1 --key v2`（覆盖 action="append"）
      - JSON value 是其它（str/int/float） → `--key "v"`
      - 顶层若有 `_script` 字段，忽略（只用于模板自描述，不参与 CLI）
      - 命令行里同时出现的 flag 会被 JSON 覆盖（JSON 优先）

    错误转结构化 JSON（INVALID_PARAM）：
      - --args-json 后没跟值
      - JSON 解析失败
      - JSON 不是对象
    """
    if "--args-json" not in sys.argv:
        return
    idx = sys.argv.index("--args-json")
    if idx + 1 >= len(sys.argv):
        raise StructuredScriptError(
            "`--args-json` 后必须紧跟一个 JSON 对象字符串",
            error_code="INVALID_PARAM",
            hint="`--args-json` 期望接一个 JSON 对象（如 `'{\"code\":[\"hk01810\"]}'`），现在后面是空。",
            next_action="把 `--args-json` 后面补上完整 JSON 对象（建议用单引号包住整个 JSON 防 shell 转义），再重试。",
            exit_code=2,
        )
    raw_json = sys.argv[idx + 1]
    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise StructuredScriptError(
            f"`--args-json` 解析失败：{e}",
            error_code="INVALID_PARAM",
            hint="传给 `--args-json` 的字符串不是合法 JSON（常见原因：双引号被 shell 吃了 / 缺逗号 / 单双引号混用）。",
            next_action=(
                "建议写法：用单引号包整个 JSON，JSON 内部用双引号。例如 "
                "`--args-json '{\"code\":[\"hk01810\"],\"field\":[\"price\"]}'`。修正后重试。"
            ),
            exit_code=2,
        )
    if not isinstance(payload, dict):
        raise StructuredScriptError(
            "`--args-json` 必须是 JSON 对象（{...}），不是数组 / 字符串 / 数字",
            error_code="INVALID_PARAM",
            hint="JSON 模板必须是顶层对象，每个 key 对应一个 argparse flag。",
            next_action="把外层包成 `{...}`，例如 `{\"code\":[\"hk01810\"]}`，再重试。",
            exit_code=2,
        )

    new_argv = list(sys.argv[:idx])  # 保留 script 名 + idx 之前已有的 flag
    for key, value in payload.items():
        if key == "_script":
            continue
        flag = "--" + str(key).lstrip("-").replace("_", "-")
        if isinstance(value, bool):
            if value:
                new_argv.append(flag)
            continue
        if value is None:
            continue
        if isinstance(value, list):
            for v in value:
                new_argv.append(flag)
                new_argv.append(str(v))
        else:
            new_argv.append(flag)
            new_argv.append(str(value))
    new_argv.extend(sys.argv[idx + 2:])  # 跳过 `--args-json <json>`，保留剩余
    sys.argv = new_argv


# 模型在「标的代码」上常见的脑补名（除官方 alias --code/--stock-code/--symbol/--symbols 外）。
# 命中其中任一，_raise_argparse_error 会给出"立刻改成官方 alias"的精准 hint，避免再猜。
_SYMBOL_BRAINSTORM_NAMES = (
    "--ticker", "--tickers",
    "--instrument", "--instruments",
    "--security", "--securities",
    "--asset", "--assets",
    "--inst-code", "--inst_code",
    "--stockcode", "--stock_code",     # 漏写中划线
    "--symbolcode", "--symbol_code",
    "--codes",                          # 复数误写
    "--stock", "--stocks",
)


def _detect_symbol_brainstorm(detail: str) -> Optional[str]:
    """识别「标的代码脑补名」。同时扫 argparse error message 和 sys.argv。

    为什么要扫 sys.argv：当 `--code` 是 required 时，模型若传 `--ticker hk01810`，
    argparse 会优先报「required: --code」而非「unrecognized: --ticker」，
    单看 message 看不到脑补名，必须从 argv 兜底识别。
    """
    full_text = (detail + " " + " ".join(sys.argv)).lower()
    for name in _SYMBOL_BRAINSTORM_NAMES:
        if name in full_text:
            return name
    return None


def _raise_argparse_error(message: str) -> None:
    """把 argparse 的本地参数错误转成结构化 JSON，避免模型误把 usage 文本当业务结论。

    针对「标的代码脑补名」「order_list.py 误传 --order-id」两种高频错误给出精准 hint，
    其它情况落到通用提示。任何分支都强调："先看脚本 --help / SKILL.md 速抄表，禁止再猜其它参数名"。
    """
    detail = (message or "命令行参数解析失败").strip()
    hint = "命令行参数解析失败（参数名不存在 / 缺少必填 / choices 不匹配 / 当前脚本不支持该过滤条件）。"
    next_action = "按错误信息修正命令行参数后重试；若不确定参数名，先跑当前脚本的 `--help` 或 SKILL.md 速抄表，**禁止再猜**。"

    brainstorm = _detect_symbol_brainstorm(detail)
    if brainstorm is not None:
        hint = (
            f"参数名 `{brainstorm}` 是脑补出来的——本 skill 所有脚本的「标的代码」入参 "
            "**统一接受 4 个官方 alias**：`--code` / `--stock-code` / `--symbol` / `--symbols`（v1.7.4 起跨脚本对齐）。"
            "不在这 4 个里的名字（含 `--ticker` / `--instrument` / `--security` / `--stocks` 等）一律是脑补。"
        )
        next_action = (
            f"立刻把 `{brainstorm}` 改成 `--code`（行情类脚本主名）或 `--stock-code`（交易类脚本主名）重试；"
            "其它名字（`--symbol` / `--symbols`）也都接受。**禁止再猜其它写法**——4 个 alias 之外都是脑补。"
        )
    elif "unrecognized arguments" in detail and "--order-id" in detail:
        hint = "`order_list.py` 不支持 `--order-id` 直接过滤；这次失败是本地命令行用法不对，不是券商侧“订单不存在”。"
        next_action = "改用 `order_list.py` 的 `--stock-code` + 日期 / 市场 / 状态缩小列表范围，再从结果里反查 orderId；不要把这次错误解读成“查无此单”。"

    raise StructuredScriptError(
        detail,
        error_code="INVALID_PARAM",
        hint=hint,
        next_action=next_action,
        exit_code=2,
    )

# 异常类型 → (error_code, exit_code, default_hint, default_next_action)
# 抓不到具体码时，至少给到分类级别的指引。
_GENERIC_PLAYBOOK = {
    "NoMockAccountError": {
        "error_code": "NO_MOCK_ACCOUNT",
        "exit_code": 3,
        "hint": "共享凭证下没有 subAccountType=2 的模拟盘子账户，本 skill 已直接拦截。",
        "next_action": "停手并把账户缺失情况完整转告用户，等待用户决定：开通模拟账户 / 显式 --sub-account-id 调试。禁止私自切实盘 skill 或挑选其他账户继续。",
    },
    "FileNotFoundError": {
        "error_code": "ENV_FILE_MISSING",
        "exit_code": 2,
        "hint": "FOSUN_ENV_PATH 指向的共享凭证文件不存在。",
        "next_action": "提示用户先通过同级 `fosun-env-setup` 生成共享凭证后再来。",
    },
    "EnvironmentError": {
        "error_code": "ENV_INCOMPLETE",
        "exit_code": 2,
        "hint": "共享凭证存在但关键字段缺失（FSOPENAPI_BASE_URL / FSOPENAPI_API_KEY）。",
        "next_action": "提示用户通过同级 `fosun-env-setup` 修复或刷新共享凭证。",
    },
    "ValueError": {
        "error_code": "INVALID_PARAM",
        "exit_code": 2,
        "hint": "本地参数校验未通过（市场三件套错配 / 模拟盘能力边界外的入参等）。",
        "next_action": "按错误信息修正命令行参数后重试；若涉及用户原始意图，先和用户确认。",
    },
}


def _format_error_payload(
    *,
    error_code: str,
    message: str,
    hint: str,
    next_action: str,
    extras: Optional[dict] = None,
) -> dict:
    payload = {
        "ok": False,
        "error_code": error_code,
        "message": message,
        "hint": hint,
        "next_action": next_action,
    }
    if extras:
        payload.update(extras)
    return payload


def _emit_error(payload: dict, exit_code: int) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(exit_code)


def run(action) -> None:
    """脚本入口包装：把所有异常转成"模型可直接读"的结构化 JSON 错误。

    输出契约（stderr）：
        {
          "ok": false,
          "error_code": "...",        # 见 SKILL.md 错误码处置矩阵
          "message": "...",            # 原始错误描述
          "hint": "...",               # 为什么会这样（机制说明）
          "next_action": "...",        # 模型应该做什么
          "code": 60009,               # APIError 才有
          "requestId": "...",          # APIError 才有
          "data": {...}                # APIError 才有
        }

    退出码：
        0 = 成功
        1 = APIError（服务端业务错）
        2 = 参数 / 配置错（本地校验或 env 问题）
        3 = NO_MOCK_ACCOUNT（强拦截，必须停手转告用户）
    """
    original_argparse_error = argparse.ArgumentParser.error

    def _patched_argparse_error(self, message):  # type: ignore[no-untyped-def]
        _raise_argparse_error(message)

    argparse.ArgumentParser.error = _patched_argparse_error
    try:
        _maybe_inject_from_args_json()  # v1.7.4：让所有脚本统一支持 `--args-json '{...}'`
        action()
    except StructuredScriptError as exc:
        _emit_error(
            _format_error_payload(
                error_code=exc.error_code,
                message=str(exc),
                hint=exc.hint,
                next_action=exc.next_action,
            ),
            exc.exit_code,
        )
    except NoMockAccountError as exc:
        playbook = _GENERIC_PLAYBOOK["NoMockAccountError"]
        _emit_error(
            _format_error_payload(
                error_code=playbook["error_code"],
                message=str(exc),
                hint=playbook["hint"],
                next_action=playbook["next_action"],
            ),
            playbook["exit_code"],
        )
    except APIError as exc:
        code = getattr(exc, "code", None)
        message = getattr(exc, "message", str(exc))
        apikey_status = classify_api_key_error_code(code)
        if apikey_status in _APIKEY_ERROR_GUIDANCE:
            guidance = _APIKEY_ERROR_GUIDANCE[apikey_status]
            _emit_error(
                _format_error_payload(
                    error_code=f"APIERROR_{code}" if code is not None else "APIERROR",
                    message=message,
                    hint=guidance["hint"],
                    next_action=guidance["next_action"],
                    extras={
                        "code": code,
                        "account_action": guidance["account_action"],
                        "credential_owner_skill": "real-trade-skill",
                        "requestId": getattr(exc, "request_id", None),
                        "data": getattr(exc, "data", None),
                    },
                ),
                1,
            )
        message_playbook = _apierror_message_playbook(message)
        playbook = APIERROR_PLAYBOOK.get(code, {})
        _emit_error(
            _format_error_payload(
                error_code=message_playbook["error_code"] if message_playbook else (
                    f"APIERROR_{code}" if code is not None else "APIERROR"
                ),
                message=message,
                hint=(message_playbook or playbook).get(
                    "hint",
                    "服务端业务错；请按 message 内容判断是否要重试。",
                ),
                next_action=(message_playbook or playbook).get(
                    "next_action",
                    "若错误信息提示参数问题，按提示修正后重试；否则原样转告用户，等待决策。",
                ),
                extras={
                    "code": code,
                    "requestId": getattr(exc, "request_id", None),
                    "data": getattr(exc, "data", None),
                },
            ),
            1,
        )
    except FileNotFoundError as exc:
        playbook = _GENERIC_PLAYBOOK["FileNotFoundError"]
        _emit_error(
            _format_error_payload(
                error_code=playbook["error_code"],
                message=str(exc),
                hint=playbook["hint"],
                next_action=playbook["next_action"],
            ),
            playbook["exit_code"],
        )
    except EnvironmentError as exc:
        playbook = _GENERIC_PLAYBOOK["EnvironmentError"]
        _emit_error(
            _format_error_payload(
                error_code=playbook["error_code"],
                message=str(exc),
                hint=playbook["hint"],
                next_action=playbook["next_action"],
            ),
            playbook["exit_code"],
        )
    except ValueError as exc:
        playbook = _GENERIC_PLAYBOOK["ValueError"]
        _emit_error(
            _format_error_payload(
                error_code=playbook["error_code"],
                message=str(exc),
                hint=playbook["hint"],
                next_action=playbook["next_action"],
            ),
            playbook["exit_code"],
        )
    finally:
        argparse.ArgumentParser.error = original_argparse_error
