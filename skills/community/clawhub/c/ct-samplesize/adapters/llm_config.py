#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-base · 后台大模型配置解析器（configtbl 唯一真相源 · 2026-11-04）
=====================================================================
发布为应用的工作台若需调用后台 LLM，**禁止在代码/配置里写死模型名**。
统一通过本模块取配置：

    from llm_config import resolve_llm_config
    llm = resolve_llm_config(cfg, skill="ct-samplesize")
    api_key = load_llm_key(env_name=llm["apiKeyEnv"], key_path=llm.get("apiKeyFile"))
    req = urllib.request.Request(llm["baseUrl"].rstrip("/") + "/chat/completions", ...
                                 json.dumps({"model": llm["model"], ...}))

取值优先级（高 → 低，逐键覆盖，不是整块替换）：
  1. 进程 env（CT_LLM_MODEL / CT_LLM_BASE_URL / …）—— 应急覆盖，运维注入
  2. 飞书共享 configtbl（经 Coze 端点 download，TTL 缓存）—— 唯一真相源
  3. workbench.config.json 的 backend.llm —— 打包快照（离线兜底）
  4. 本模块内置兜底 —— 最后防线

设计红线：
  · 密钥永不进表、永不进本模块；仍由 llm_loader.load_llm_key() 按 env > 混淆 .py 读取。
  · 端点不可达 / 超时 / 旧 schema / 脏值 → 一律降级，**绝不阻断主流程**。
  · 绝不把 token、完整响应体或任何凭据写进日志/异常。
  · 零第三方依赖（仅标准库）；与家族「发布包零外部依赖」一致。
  · 端点尚未部署 configtbl 补丁时返回 schema="searchlog" + 空 key/value，
    本模块识别为失败并走快照，功能不中断（但不会动态更新）。

契约详见 ct-base/references/coze_io_contract.md §7；规范见 workbench_ui.md §12。
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import socket
import threading
import time
import urllib.error
import urllib.request

__all__ = ["resolve_llm_config", "resolve_key_path", "clear_cache", "last_status",
           "CONFIG_TABLE_ID"]

logger = logging.getLogger("ct-base.llm_config")

# ── 端点与表（非机密；无凭据读不了表）──
DEFAULT_ENDPOINT = "https://ct-bugreport.coze.site/run"
CONFIG_TABLE_ID = "tbldL4vpgE1xj3P4"
CONFIG_KEY_PREFIX = "CT_LLM_"
DEFAULT_TTL_SEC = 86400        # 成功缓存 24 小时（首次读取后每 24h 回源一次，避免频繁读表）
FAIL_TTL_SEC = 60              # 失败负面缓存 1 分钟，避免每次 LLM 调用都打端点
DEFAULT_HTTP_TIMEOUT_SEC = 3.0

# ── 内置兜底（与 workbench.config.json / §12 对齐；注意这里只是"最后防线"）──
_FALLBACK = {
    "provider": "longcat",
    "baseUrl": "https://api.longcat.chat/openai",
    "model": "LongCat-2.5",
    "apiKeyEnv": "LONGCAT_API_KEY",
    "apiKeyFile": "config/llm_key.py",
    "maxTokens": 2048,
    "timeoutSec": 45,
}

# configtbl key → 配置字段（表内只登记非敏感项）
_KEY_MAP = {
    "CT_LLM_MODEL": "model",
    "CT_LLM_BASE_URL": "baseUrl",
    "CT_LLM_PROVIDER": "provider",
    "CT_LLM_API_KEY_ENV": "apiKeyEnv",
    "CT_LLM_MAX_TOKENS": "maxTokens",
    "CT_LLM_TIMEOUT_SEC": "timeoutSec",
    "CT_LLM_UPDATED_AT": "updatedAt",
}
_INT_FIELDS = {"maxTokens": (1, 65536), "timeoutSec": (1, 600)}
_ALLOWED_ENV_KEYS = {k: v for k, v in _KEY_MAP.items() if v not in ("updatedAt",)}

_lock = threading.Lock()
_cache = {"ts": 0.0, "data": {}, "ok": False, "src": "none", "err": ""}
_snapshot_cache = {}


def _query_origin() -> str:
    """端点 §1.4 要求非空 query_origin；与 ct-update 同口径（主机名 sha256，不出 PII）。"""
    try:
        raw = socket.gethostname() or "ct-llm-config"
    except Exception:
        raw = "ct-llm-config"
    return "sha256:" + hashlib.sha256(("llmcfg|" + raw).encode("utf-8")).hexdigest()


def _resolve_token() -> str:
    """取 bugreport 端点公共凭据：env > 各技能发布包已有的凭据模块 > 空串（降级）。

    家族里每个发布包都已内嵌该公共 token（bug_report.py / endpoint_token.py /
    coze_token_embedded.py），这里做 best-effort 探测，避免各技能重复改造凭据链路。
    全部 try/except 包裹：找不到就返回空串，由调用方走快照降级。
    """
    v = (os.environ.get("CT_BUGREPORT_TOKEN") or "").strip()
    if v:
        return v
    probes = (
        ("bug_report", "get_endpoint_token", ()),
        ("endpoint_token", "get_secret", ("ct_bugreport_coze",)),
        ("endpoint_token", "get_bugreport_token", ()),
        ("coze_token_embedded", "get_bugreport_token", ()),
        ("coze_token_embedded", "get_secret", ("ct_bugreport_coze",)),
    )
    for mod_name, fn_name, args in probes:
        try:
            mod = __import__(mod_name)
            fn = getattr(mod, fn_name, None)
            if callable(fn):
                t = (fn(*args) or "").strip()
                if t:
                    return t
        except Exception:  # noqa: BLE001 - 凭据模块缺失/解码失败一律静默降级
            continue
    return ""


def _validate(key: str, value: str):
    """校验并归一化表内值；不合法返回 None（该键被丢弃，不影响其它键）。"""
    v = (value or "").strip().strip("'\"")
    if not v or len(v) > 256:
        return None
    field = _KEY_MAP.get(key)
    if not field:
        return None
    if field in _INT_FIELDS:
        try:
            lo, hi = _INT_FIELDS[field]
            n = int(v)
            return n if lo <= n <= hi else None
        except (TypeError, ValueError):
            return None
    if field in ("model", "provider", "apiKeyEnv"):
        # 标识符类：禁空白/换行/路径分隔符，防脏值注入拼进请求体或 env 名
        if any(c.isspace() for c in v) or "/" in v or "\\" in v:
            return None
    if field == "baseUrl" and not v.startswith("https://"):
        return None
    return v


def _fetch_from_configtbl(endpoint: str, timeout: float) -> dict:
    """调 Coze 端点 download 读 configtbl → (全局配置 dict, {skill: 覆盖 dict})；异常上抛统一降级。"""
    token = _resolve_token()
    if not token:
        raise RuntimeError("no endpoint credential")
    body = {
        "action": "download",
        "table_id": CONFIG_TABLE_ID,
        "token": token,
        "query_origin": _query_origin(),
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "ct-base-llm-config/1.0",
            "Authorization": "Bearer " + token,
        },
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
    data = json.loads(raw)
    if not isinstance(data, dict) or data.get("status") != "ok":
        raise RuntimeError("endpoint status not ok")
    # 旧端点未部署 configtbl 补丁 → schema=searchlog 且记录无 key/value，必须判失败
    if data.get("schema") != "configtbl":
        raise RuntimeError("endpoint lacks configtbl schema")
    records = data.get("records")
    if not isinstance(records, list):
        raise RuntimeError("bad records shape")
    out, scoped = {}, {}
    for rec in records:
        if not isinstance(rec, dict):
            continue
        key = str(rec.get("key") or "").strip()
        if not key.startswith(CONFIG_KEY_PREFIX):
            continue
        base_key, sep, scope = key.partition("@")
        val = _validate(base_key, str(rec.get("value") or ""))
        if val is None:
            continue
        field = _KEY_MAP[base_key]
        if sep and scope and all(c.isalnum() or c in "-_" for c in scope):
            # CT_LLM_MODEL@ct-samplesize → 该技能专属覆盖
            scoped.setdefault(scope.lower(), {})[field] = val
        else:
            out[field] = val
    if not out.get("model"):
        raise RuntimeError("no CT_LLM_MODEL row")
    return out, scoped


def _table_values(endpoint: str, timeout: float) -> tuple:
    """读表 → (全局配置 dict, {skill: 覆盖 dict})。带 TTL + 负面缓存，线程安全。"""
    now = time.time()
    with _lock:
        ttl = DEFAULT_TTL_SEC if _cache["ok"] else FAIL_TTL_SEC
        if _cache["ts"] and now - _cache["ts"] < ttl:
            return dict(_cache["data"]), _cache.get("scoped", {})
    try:
        data, scoped = _fetch_from_configtbl(endpoint, timeout)
        with _lock:
            _cache.update({"ts": now, "data": data, "ok": True,
                           "scoped": scoped, "src": "configtbl", "err": ""})
        return dict(data), scoped
    except Exception as e:  # noqa: BLE001 - 失败一律降级，绝不阻断主流程
        # 只记类型与固定短原因，绝不记录响应体 / token
        reason = type(e).__name__
        with _lock:
            stale = dict(_cache["data"]) if _cache["ok"] else {}
            _cache.update({"ts": now, "data": stale, "ok": False,
                           "src": "snapshot", "err": reason})
        logger.info("[llm_config] configtbl 不可用（%s），回落打包快照", reason)
        return {}, {}


def _env_overrides() -> dict:
    """进程 env 应急覆盖（最高优先级）。"""
    out = {}
    for env_key, field in _ALLOWED_ENV_KEYS.items():
        raw = os.environ.get(env_key)
        if raw is None:
            continue
        v = _validate(env_key, raw)
        if v is not None:
            out[field] = v
    return out


def _discover_snapshot() -> dict:
    """自动向上查找 workbench.config.json 的 backend.llm（打包快照）。

    各技能的 llm_config.py 副本所在目录不同（workbench/ 或 adapters/），
    由调用点手工传 cfg 既啰嗦又易漏；这里从模块所在目录向上最多 4 层探测，
    命中即缓存。找不到时 resolve_llm_config 自然回落到内置 _FALLBACK。
    """
    here = os.path.dirname(os.path.abspath(__file__))
    if here in _snapshot_cache:
        return _snapshot_cache[here]
    found = {}
    base = here
    for _ in range(4):
        for rel in ("workbench.config.json", os.path.join("workbench", "workbench.config.json")):
            p = os.path.join(base, rel)
            if not os.path.isfile(p):
                continue
            try:
                with open(p, "r", encoding="utf-8") as f:
                    d = json.load(f)
                llm = (d.get("backend") or {}).get("llm")
                if isinstance(llm, dict) and llm.get("model"):
                    found = llm
                    break
            except Exception:  # noqa: BLE001 - 快照损坏不应影响主流程
                pass
        if found:
            break
        parent = os.path.dirname(base)
        if parent == base:
            break
        base = parent
    _snapshot_cache[here] = found
    return found


def resolve_key_path(cfg: dict | None = None) -> str | None:
    """把 `apiKeyFile`（如 `config/llm_key.py`）解析为实际存在的绝对路径。

    各技能的 llm_config.py 副本位于 workbench/ 或 adapters/，源文件位于
    <skill>/config/ 或 <publish>/config/；从副本所在目录向上最多 4 层探测即可命中。
    找不到返回 None，交回 llm_loader.load_llm_key() 的默认行为（不抛异常、不阻断）。
    注意：这里只解析路径，绝不读取或回显 key 内容。
    """
    p = ((cfg or {}).get("apiKeyFile") or "config/llm_key.py").strip()
    if os.path.isabs(p):
        return p if os.path.isfile(p) else None
    base = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        cand = os.path.join(base, p)
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(base)
        if parent == base:
            break
        base = parent
    return None


def resolve_llm_config(cfg: dict | None = None, skill: str = "",
                       endpoint: str | None = None,
                       timeout: float = DEFAULT_HTTP_TIMEOUT_SEC,
                       use_table: bool = True) -> dict:
    """返回本次 LLM 调用应使用的配置 dict（含 model/baseUrl/apiKeyEnv/apiKeyFile…）。

    参数：
      cfg       —— workbench.config.json 解析后的 dict；None 时自动向上探测快照
      skill     —— 技能名，如 "ct-samplesize"；用于 CT_LLM_MODEL@<skill> 覆盖
      endpoint  —— 端点 URL 覆盖（测试 / 私有部署）
      timeout   —— 端点读取超时秒（默认 3s）
      use_table —— False 时跳过 configtbl（离线/单测/纯本地模式）

    返回 dict 额外含 `_source` / `_tableError` 两个诊断字段；业务字段用法不变。
    """
    if cfg is None:
        snap_auto = _discover_snapshot()
        cfg = {"backend": {"llm": snap_auto}} if snap_auto else None
    snap = {}
    try:
        raw = ((cfg or {}).get("backend") or {}).get("llm") or {}
        if isinstance(raw, dict):
            snap = {k: v for k, v in raw.items()
                    if k in set(_FALLBACK) | {"apiKeyFile"}}
    except Exception:
        snap = {}

    out = dict(_FALLBACK)
    out.update(snap)
    source = "snapshot" if snap else "fallback"

    if use_table:
        ep = endpoint or os.environ.get("CT_LLM_CONFIG_ENDPOINT") or DEFAULT_ENDPOINT
        table, scoped = _table_values(ep, timeout)
        if table:
            out.update(table)
            source = "configtbl"
            override = scoped.get((skill or "").strip().lower(), {})
            if override:
                out.update(override)
                source = "configtbl@" + skill

    env = _env_overrides()
    if env:
        out.update(env)
        source = "env"

    out["_source"] = source
    out["_tableError"] = _cache.get("err", "")
    return out


def clear_cache() -> None:
    """清空进程内缓存（测试 / 运维强制刷新用）。"""
    with _lock:
        _cache.update({"ts": 0.0, "data": {}, "ok": False,
                       "scoped": {}, "src": "none", "err": ""})


def last_status() -> dict:
    """健康检查 / 诊断用：来源、缓存年龄、最近错误（不含任何凭据或响应体）。"""
    with _lock:
        return {
            "source": _cache.get("src", "none"),
            "cacheAgeSec": round(time.time() - _cache["ts"], 1) if _cache["ts"] else None,
            "ok": bool(_cache["ok"]),
            "error": _cache.get("err", ""),
            "tableId": CONFIG_TABLE_ID,
        }
