#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nmpa_coze.py — NMPA《药品不良反应信息通报》检索的 Coze 浏览器通道客户端

WHY THIS EXISTS:
  NMPA 主站 (nmpa.gov.cn，含《药品不良反应信息通报》) 对本机直连返回 HTTP 412
  (CDN/WAF 拦截)。与 ct-registry 的 Tier2 统一检索（WHO ICTRP / CDE / ChiCTR 等
  无公开 API 源走 Coze 服务器端浏览器抓取）同一架构：把检索委派给 Coze 统一
  工作流端点 ct-search.coze.site/run，由服务端浏览器通道抓取并返回结构化结果，
  本地零 Playwright、零浏览器依赖。

PROTOCOL (consistent with the live ct-search.coze.site/run unified endpoint):
  - POST JSON (sync) to https://ct-search.coze.site/run with `Authorization: Bearer <token>`.
    The endpoint runs the LangGraph synchronously and returns the full state dict
    (no async run_id / polling in practice; a minimal poll fallback is kept defensively).
  - Payload: {"source": "nmpa_pv", "mode": "search", "keyword": <drug>,
              "multi_keywords": "<event terms, space-separated>",
              "max_pages": N, "query_origin": <sha256(hostname)>}
  - Response: {"project_list": "<json {total_count, projects:[{title,url,date,
              source_column,snippet,matched_keywords,tier}]}>", "total_count": N,
              "run_id": "..."}  (project_list is a JSON STRING — parse it).
  - Token resolution (ct-base §5): --token > env CT_REGISTRY_COZE_TOKEN >
    embedded public blob (XOR+base64, same shared credential as ct-registry).
  - SAFE PREVIEW by default: no network I/O unless --run.
  - Outbound authorization gate (ct-base §5.212): endpoint must be present in
    adapters/config.json auto_approve_endpoints, else [AUTH-BLOCK] and exit.

DEPLOYMENT STATUS (re-probed 2026-09-01, verified live — NOT an assumption):
  The unified endpoint **now serves source "nmpa_pv"** and returns genuine
  NMPA/CDR-ADR ADR bulletins. Live probe with drug=甲氨蝶呤 returned
  hit_count=1 (通报专文: "药品不良反应信息通报（第75期）关注甲氨蝶呤片的误用风险"),
  with the `tier` field present — i.e. the response-shape guard PASSED, no
  contamination. The browser channel (Playwright on the Coze server) is exactly
  what bypasses the NMPA-main-site WAF (HTTP 412) that blocks local direct fetch.
  (Background, kept for context: before the workflow was uploaded, the endpoint
  silently FELL BACK to the default chinadrugtrials source for unknown sources —
  which is why `_reject_foreign_records` exists. That guard is STILL enforced;
  it must never be relaxed, because a regressed/unknown source could re-introduce
  the clinical-trial-into-safety-report contamination.)

EGRESS: only PUBLIC query terms (drug / event keywords) are sent. No
confidential data; PII patterns are stripped from the payload (ct-base §5.50).
"""
import argparse
import hashlib
import json
import os
import re
import socket
import sys
import time

import base64

# ── ct-base coze_io_contract §1.1：user_language 备用提示（注入 params）────
# 复用本技能 scripts/i18n.py（与 coze_dispatch 同源单一实现）。
try:
    _HERE0 = os.path.dirname(os.path.abspath(__file__))
    _SCRIPTS_DIR0 = os.path.join(os.path.dirname(_HERE0), "scripts")
    if _SCRIPTS_DIR0 not in sys.path:
        sys.path.insert(0, _SCRIPTS_DIR0)
    from i18n import resolve_user_language as _i18n_resolve_user_language, \
        _current_lang as _i18n_current_lang
except Exception:  # pragma: no cover — i18n 缺失时降级为系统 locale
    _i18n_resolve_user_language = None
    _i18n_current_lang = None

# ── ct-base §5 公用凭据：与 ct-registry 同一份统一端点 token ──────────────
# XOR key 与 ct-registry adapters/endpoint_token.py 保持一致以兼容同一 blob。
OBFUSCATION_KEY = b"ct-registry-extsvc-obf-v1-9c4d2a"

_EMBEDDED_COZE_UNIFIED = (
    "Bg1nGgcgCho7GzN-MAI9QjgKZBwrC1kGa25wVX0Jfxk5Hk5HKyM_HjgmM0UoPDUHOCdKGDsPHB5oR1IbeDBnVSwwRkc8VTgKOTYRRigBPkpYBlQlEgUeO1hiUClbAHozFBdXHRMrWzUDEyoYDxpHAxovQCEXL0QBWHRhNV8tWBEBPUE4MQYCQjYgPWBWGkclIDdDCBsrHhJod30tZikAGRM5RxYSBQMbRStKfBwxGEMFKkA5VgVuPwdifSpMKXYoUTpHFVYpAxBBPSpaDBkjNUYqRwAaKFcRAGBtNgYrdjhXOG44HwM-Oh09EGcfGzMfGzlAOlQqVE9ZTn4IQT0AWFUufkcPBQBKRxBKZxcaM0oeOWtWEjxqIERJfg8EAWFYEy5pHVYpAypFPS1KVzcgIkYuaQQYKXkzS2BtJgQtWxYKFx44Dy4DHB0TLhgMGkclAzlrVgoCdSRedQslXj0ANxkXHEtVBVsHGBAVFBUiMBxFLUc2USt5HUZgQzoHKXYoUDt5FVcpLSIMOxcdSzVEEEA8WjUAKF0YAkp2M1M3UwIKHwAdCAk6PhAxPmYsPx8aACp9PiQNSkZoTHc2TR58BS0HFCgCViMEEhhMXUhARitAElkXGgh4FEtlVVNkVn84BC0cFCEoOio6Mw18DykDMiUzFSsNUlwYUHdrCW0AZlQvPGUFXRIRNBU9C2scQEUJOQdbXCAnXiFub35VR1BKAycZfCJdDCM-Bj4qfy0qGTIfCX0ZLSF6E2IVFFEHVQEUEzpUATVUIhYlPE58MRYbQx0pQSoLF3QdYXVRMAI1XhNRDHsKUz0NQDELL3sJKTE3BAlvPRNWawxgRwkvUyBEEBc3HydVXz1DTQdIVxVOK0U7FRo1Ug5XAkBkCzVZVVZWWyRVChM0ExkiPAxaNDIXERoGSSVbV10uQGZWE30gBikXMmMlFlczHgImIX8sQUAXEA19GDc8GU9oRHUJeQhEIlIsWg=="
)

DEFAULT_ENDPOINT = "https://ct-search.coze.site/run"
SOURCE = "nmpa_pv"
DEFAULT_TOKEN_ENV = "CT_REGISTRY_COZE_TOKEN"

# 出站授权闸门（ct-base §5.212）：端点须在 adapters/config.json auto_approve_endpoints
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def _obf_decode(blob: str) -> str:
    data = base64.urlsafe_b64decode(blob.strip())
    plain = bytes(b ^ OBFUSCATION_KEY[i % len(OBFUSCATION_KEY)]
                  for i, b in enumerate(data))
    return plain.decode("utf-8")


def get_token(cli_token=None, token_env=None):
    """token 解析优先级：CLI > env(CT_REGISTRY_COZE_TOKEN) > 内嵌公用 blob。"""
    if cli_token:
        return cli_token
    env = token_env or DEFAULT_TOKEN_ENV
    v = os.environ.get(env)
    if v:
        return v
    return _obf_decode(_EMBEDDED_COZE_UNIFIED)


def check_outbound_authorization(endpoint):
    """端点在 config.json auto_approve_endpoints 即放行；否则 [AUTH-BLOCK] 返回 False。"""
    try:
        with open(_CONFIG_PATH, encoding="utf-8") as f:
            cfg = json.load(f)
        if endpoint in cfg.get("auto_approve_endpoints", []):
            return True
    except Exception:
        pass
    sys.stderr.write(
        "[AUTH-BLOCK] outbound to %s requires user confirmation.\n"
        "Add it to adapters/config.json auto_approve_endpoints after user approval.\n" % endpoint)
    return False


# ── ct-base §5.50: 出站 payload 剥离 PII ────────────────────────────────
_PII_PATTERNS = [
    (re.compile(r"\b1[3-9]\d{9}\b"), "<phone>"),
    (re.compile(r"\b\d{17}[\dXx]\b"), "<id-card>"),
    (re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"), "<email>"),
]


def _sanitize(obj):
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, str):
        for pat, repl in _PII_PATTERNS:
            obj = pat.sub(repl, obj)
        return obj
    return obj


# ── §8.6 硬件绑定机器标识：统一从本技能 scripts/hardware_id.py 导入（ct-base 共享件 vendored 副本）──
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "scripts"))
try:
    from hardware_id import hardware_id as _hardware_id
except Exception:  # pragma: no cover
    _hardware_id = None


def _query_origin():
    """§8.6 调用来源标识：硬件绑定的 sha256，跨 Windows 账号 / 改主机名 / 重装系统稳定。"""
    if _hardware_id is not None:
        return _hardware_id()
    import socket as _s
    try:
        return "sha256:" + hashlib.sha256(_s.gethostname().encode("utf-8")).hexdigest()
    except Exception:  # pragma: no cover
        return "sha256:" + hashlib.sha256(b"unknown-host").hexdigest()


# ── 入口标识 entry_point（ct-base coze_io_contract §1.3 / §2.3 · 2026-10-07）─────
# 区分「调用来源」：技能本身（"skill"）vs 工作台 Web 应用（"workbench"）vs 未来
# 第三方 API（"api"）。透传写入飞书**独立列** entry_point，供后台按来源直切筛选。
#
# 与 query_origin 的区别（🔴 不得混用）：query_origin 按**机器**（hostname SHA-256）
# 且被 _assert_query_origin 硬守卫；同一台机器上 skill / workbench 算出的哈希逐字节
# 相同 → 无法区分界面来源，故须独立字段。
# 进程启动期初值来源（2026-10-13 修复）：环境变量 CT_ENTRY_POINT。
# ct-safety 工作台是 Popen(scripts/ct_safety.py) 子进程架构——真正向 coze 发请求的是
# 子进程，父进程（server.py）里调用 set_entry_point() 无法跨进程传递，历史上因此
# 全树零调用点、entry_point 恒为默认 "skill"（应用页面调用也落 "skill"）。
# 现由 server.py 在 Popen env 写 CT_ENTRY_POINT=workbench，本模块加载时读取作初值；
# agent / 技能进程不设该变量 → 恒为 "skill"。非法值 / 空白一律回退 "skill"（§1.3）。
_ENTRY_POINT_WHITELIST = frozenset({"skill", "workbench", "api"})
_ENTRY_POINT_ENV = "CT_ENTRY_POINT"


def _entry_point_from_env():
    """进程启动期从环境变量解析 entry_point 初值（白名单外一律回退 "skill"）。"""
    v = (os.environ.get(_ENTRY_POINT_ENV) or "").strip()
    return v if v in _ENTRY_POINT_WHITELIST else "skill"


_ENTRY_POINT = _entry_point_from_env()


def set_entry_point(value):
    """覆盖进程级入口标识（工作台进程启动期调用以标记 workbench）。

    agent / 技能进程**不import** 工作台模块 → 两进程全局值天然隔离、无污染。
    空值 / 空白 / 非法值一律回退 "skill"，绝不写出 None 或脏值（§1.3）。
    """
    global _ENTRY_POINT
    v = (value or "").strip() if isinstance(value, str) else ""
    _ENTRY_POINT = v if v in _ENTRY_POINT_WHITELIST else "skill"


def entry_point():
    """当前进程级入口标识（永不为 None / 空串）。"""
    return _ENTRY_POINT or "skill"


def _billing_fields(account_id, billing_token):
    """ct-base §20.12：计费身份标识透传（可选）。

    仅当调用方显式提供才进入出站 payload；服务端未部署计费中间件时由
    `extra='ignore'` 安全忽略（向后兼容、不阻断）。与 `query_origin` 匿名机器
    指纹完全独立，不复用其字段。返回 {} 表示 legacy 未计量路径。
    """
    out = {}
    if account_id and account_id.strip():
        out["account_id"] = account_id.strip()
    if billing_token and billing_token.strip():
        out["billing_token"] = billing_token.strip()
    return out


# ── ct-base §20.13 / coze_io_contract：统一 coze 信封字段 ─────────────────
# 所有 ct-* 调用 coze 端点（不分计算/检索）一律遵守 ct-base 契约：
#   §1.2 `skill_version` → 顶层信封字段（与 query_origin 同级）
#   §1.1 `user_language` → 进 params（非顶层，备用提示）
# 飞书 searchlog（§2.1/§2.2）由 coze 服务端工作流负责，此处只发字段。

# §1.2 单一事实来源 = SKILL.md frontmatter `version:`；读取失败回退内置常量。
_SKILL_VERSION_FALLBACK = "0.9.8"


def _skill_version() -> str:
    """读本地 SKILL.md frontmatter 的 `version:`（契约 §1.2 单一事实来源）。

    失败（文件缺失 / 无 version 键 / 解析异常）回退 _SKILL_VERSION_FALLBACK。
    升版本只改 SKILL.md，无需动此函数。
    """
    try:
        _here = os.path.dirname(os.path.abspath(__file__))
        _skill_md = os.path.join(os.path.dirname(_here), "SKILL.md")  # adapters/../SKILL.md
        with open(_skill_md, encoding="utf-8") as _f:
            _text = _f.read()
        _m = re.match(r"^---\s*\n(.*?)\n---", _text, re.DOTALL)
        if _m:
            for _line in _m.group(1).splitlines():
                _kv = re.match(r"^version:\s*(\S+)\s*$", _line)
                if _kv:
                    return _kv.group(1).strip().strip('"').strip("'")
    except Exception:
        pass
    return _SKILL_VERSION_FALLBACK


def _user_language_hint(query: str = "", override=None) -> str:
    """契约 §1.1 三级判定：override > 输入内容检测 > 系统 locale 回退。

    返回 'zh' / 'en'；i18n 完全缺失时返回 ''（调用方据此不注入 params）。
    """
    if _i18n_resolve_user_language is not None:
        try:
            return _i18n_resolve_user_language(query or "", override)
        except Exception:
            pass
    if _i18n_current_lang is not None:
        try:
            return _i18n_current_lang()
        except Exception:
            pass
    return ""


def attach_coze_contract(payload: dict, query: str = "", override=None) -> dict:
    """ct-base coze_io_contract §1：统一注入信封字段（就地修改并返回，幂等）。

    - §1.2 `skill_version`：顶层信封字段（与 query_origin 同级）。
    - §1.1 `user_language`：进 params（非顶层）；仅非空才注入。
    - §2.1 `querystr`：请求参数 JSON（审计列）。统一端点的飞书 querystr 列是
      调用方传入（state.querystr 透传），不传则走服务端 _fallback_querystr
      兜底白名单——该白名单不含 skill_version / user_language / 日期范围，
      客户端必须自带 querystr，版本号才能落进飞书（2026-09-06 修复）。
      幂等：调用方已带 querystr 时不覆盖。
    调用方在 _sanitize 之前调用即可；多余字段由服务端 extra='ignore' 安全忽略。
    """
    payload["skill_version"] = _skill_version()
    # ct-base coze_io_contract §1.3：entry_point 顶层信封字段（与 query_origin /
    # skill_version 同级），标记调用来源；透传写入飞书**独立列** entry_point（§2.3）。
    # 幂等：调用方已显式带 entry_point 时不覆盖（显式传参优先）。
    payload.setdefault("entry_point", entry_point())
    _ul = _user_language_hint(query, override)
    if _ul:
        payload.setdefault("params", {})["user_language"] = _ul
    if not payload.get("querystr"):
        _qs = {k: payload[k] for k in (
            "source", "mode", "keyword", "multi_keywords", "date_from",
            "date_to", "max_pages", "reg_no", "indication", "case_no",
            "skill_version") if payload.get(k) is not None}
        if _ul:
            _qs["user_language"] = _ul
        if _qs:
            payload["querystr"] = json.dumps(_qs, ensure_ascii=False, sort_keys=True)
    return payload


# ── 错源污染守卫 / response-shape guard ────────────────────────────────────
# 背景：统一端点对未知 source 不报错，而是静默 fallback 到默认源（实测 2026-09-01：
# nmpa_pv / chinadrugtrials / 乱码源名返回完全一致的临床试验登记记录）。若不加守卫，
# 临床试验登记会被当成 NMPA 不良反应通报灌进安全报告——数据污染级假阳性，比硬失败更危险。
#
# NMPA 节点（nmpa_search_node._filter_and_grade）保证输出的记录键集合：
#     {title, url, date, source_column, snippet, matched_keywords, tier}
# 临床试验源（chinadrugtrials / chictr 等）的记录键含：登记号 / 试验状态 / project_id …
# 两者互斥，可据此确定性判定。
_FOREIGN_KEYS = ("登记号", "试验状态", "project_id", "试验通俗题目", "适应症",
                 "申办单位", "伦理委员会")


def _reject_foreign_records(records):
    """校验记录是否为 NMPA 通报形状。返回 (ok, reason)；ok=False 时必须拒绝合并。

    判定规则（确定性、零网络、纯函数，符合 ct-base 反幻觉护栏原则）：
      1. 任一条记录含临床试验特征键 → 错源污染；
      2. 非空记录集里 tier 全缺 → 不是 nmpa_pv 节点的产物，同样视为污染。
    """
    if not records:
        return True, ""
    sample = records[:20]
    for r in sample:
        if not isinstance(r, dict):
            return False, "record is not an object"
        for k in _FOREIGN_KEYS:
            if k in r:
                return False, (
                    "endpoint fell back to a non-NMPA source: records carry "
                    "clinical-trial field %r (source nmpa_pv not deployed on the "
                    "unified endpoint yet)" % k)
    if not any(isinstance(r, dict) and r.get("tier") for r in sample):
        return False, (
            "endpoint returned records without the 'tier' field that the NMPA "
            "node always emits — refusing to merge (unknown/degraded source)")
    return True, ""


def search_nmpa(drug_keywords, event_keywords=None, terms=None, max_pages=3,
                run=False, out=None, timeout=300, token=None, endpoint=None,
                account_id=None, billing_token=None):
    """检索 NMPA 通报（经 Coze 统一端点浏览器通道）。返回 result dict 或 None(preview)。

    契约（与 ct-registry 统一端点一致）：服务端同步返回全局状态 dict，
    project_list 为 JSON 字符串，内含 projects 列表（公报记录）。
    """
    endpoint = endpoint or DEFAULT_ENDPOINT
    drug_list = [d for d in (drug_keywords or []) if d]
    event_list = [e for e in (event_keywords or []) if e]
    terms_list = [t for t in (terms or []) if t]
    primary_drug = drug_list[0] if drug_list else (event_list[0] if event_list else "")
    # 事件词 + 额外词作为本地 AND 过滤条件（服务端 multi_keywords）
    multi_kw = " ".join(event_list + terms_list)

    payload = {
        "source": SOURCE,
        "mode": "search",
        "keyword": primary_drug,
        "multi_keywords": multi_kw,
        "max_pages": max(1, int(max_pages)),
        "query_origin": _query_origin(),
    }
    billing = _billing_fields(account_id, billing_token)
    if billing:
        payload.update(billing)

    # ct-base coze_io_contract §1：统一注入 skill_version(顶层) + user_language(params)
    # query 用原始输入（药名+事件+术语）做内容级语言检测。
    attach_coze_contract(payload, query=" ".join([primary_drug] + event_list + terms_list))
    if not run:
        print("[PREVIEW] nmpa-coze: no network request will be made. Add --run to execute.")
        print("[PREVIEW] Endpoint : %s" % endpoint)
        print("[PREVIEW] Payload  : %s" % json.dumps(payload, ensure_ascii=False))
        return None

    if not check_outbound_authorization(endpoint):
        return {"source": "NMPA via coze", "hit_count": 0, "hits": [],
                "error": "AUTH-BLOCK: endpoint not in auto_approve_endpoints"}

    import requests
    tok = get_token(token)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer %s" % tok}

    safe_payload = _sanitize(payload)
    try:
        resp = requests.post(endpoint, headers=headers, json=safe_payload, timeout=timeout)
    except requests.exceptions.ProxyError:
        # ct-base §5.49：系统代理残留 → 绕代理直连重试
        resp = requests.post(endpoint, headers=headers, json=safe_payload, timeout=timeout,
                             proxies={"http": None, "https": None})
    except requests.RequestException as e:
        return {"source": "NMPA via coze", "hit_count": 0, "hits": [],
                "error": "request failed: %s" % e}

    try:
        data = resp.json()
    except Exception:
        data = {}

    if resp.status_code != 200:
        return {"source": "NMPA via coze", "hit_count": 0, "hits": [],
                "error": "HTTP %s: %s" % (resp.status_code, resp.text[:300])}

    # 极小概率异步分支（本端点实际同步返回，防御性保留）
    run_id = data.get("run_id")
    if data.get("status") == "accepted" and run_id and not data.get("project_list"):
        base = endpoint.rsplit("/run", 1)[0]
        status_url = "%s/run/status/%s" % (base.rstrip("/"), run_id)
        deadline = time.time() + timeout
        wait = 5.0
        while time.time() < deadline:
            try:
                r = requests.get(status_url, headers=headers, timeout=15)
                sd = r.json()
            except Exception:
                time.sleep(min(wait, max(1, deadline - time.time())))
                wait = min(wait * 2, 30)
                continue
            st = sd.get("status")
            if st == "running":
                time.sleep(min(wait, max(1, deadline - time.time())))
                wait = min(wait * 2, 30)
                continue
            if st in ("failed", "cancelled"):
                return {"source": "NMPA via coze", "hit_count": 0, "hits": [],
                        "error": "remote run %s: %s" % (st, sd.get("error")),
                        "run_id": run_id}
            data = sd.get("result", sd)
            break
        else:
            return {"source": "NMPA via coze", "hit_count": 0, "hits": [],
                    "error": "timeout after %ss polling run_id=%s" % (timeout, run_id),
                    "run_id": run_id}

    # 解析 project_list（JSON 字符串）
    projects = []
    if data.get("project_list"):
        try:
            pl = json.loads(data["project_list"])
            projects = pl.get("projects", []) if isinstance(pl, dict) else []
        except Exception as e:
            return {"source": "NMPA via coze", "hit_count": 0, "hits": [],
                    "error": "project_list parse failed: %s" % e}

    # 错源污染守卫：形状不符一律 fail-closed，绝不把临床试验登记并入安全报告
    ok, reason = _reject_foreign_records(projects)
    if not ok:
        return {"source": "NMPA via coze", "hit_count": 0, "hits": [],
                "tier_counts": {}, "query": payload,
                "run_id": data.get("run_id"),
                "error": "NMPA_SOURCE_NOT_DEPLOYED: %s" % reason}

    hits = []
    tier_counts = {}
    for p in projects:
        tier = p.get("tier") or "NMPA通报"
        hit = {
            "title": p.get("title", ""),
            "url": p.get("url", ""),
            "date": p.get("date"),
            "source_column": p.get("source_column", "NMPA通报"),
            "snippet": p.get("snippet", ""),
            "matched_keywords": p.get("matched_keywords", []),
            "tier": tier,
        }
        hits.append(hit)
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

    result = {
        "source": "NMPA via coze (nmpa.gov.cn browser channel)",
        "note": ("NMPA《药品不良反应信息通报》定性叙事检索；非个案计数，不可做 "
                 "disproportionality 分析。仅作 FAERS 信号定性佐证。"),
        "query": payload,
        "run_id": data.get("run_id"),
        "hit_count": len(hits),
        "tier_counts": tier_counts,
        "hits": hits,
    }
    if isinstance(data, dict) and data.get("error"):
        result["error"] = data["error"]
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", out, "(hits=%d)" % len(hits))
    return result


def main():
    ap = argparse.ArgumentParser(
        description="Search NMPA adverse-reaction bulletins via Coze browser channel.")
    ap.add_argument("--drug", required=True,
                    help="drug keyword(s), comma-separated Chinese/English aliases")
    ap.add_argument("--event", help="event keyword")
    ap.add_argument("--terms", nargs="*", help="extra AND keywords")
    ap.add_argument("--max-pages", type=int, default=3)
    ap.add_argument("--run", action="store_true", help="execute network call")
    ap.add_argument("--out", help="output JSON path")
    ap.add_argument("--timeout", type=int, default=300, help="poll timeout seconds")
    ap.add_argument("--token", help="override Bearer token (ct-base §5 resolution otherwise)")
    ap.add_argument("--endpoint", help="override endpoint URL")
    ap.add_argument("--account-id", help="（可选）付费账户标识，透传至统一端点（ct-base §20.12 计费预留）")
    ap.add_argument("--billing-token", help="（可选）服务端签发的计费令牌，透传至统一端点")
    args = ap.parse_args()

    # 计费标识：CLI 优先，env (CT_BILLING_ACCOUNT_ID / CT_BILLING_TOKEN) 兜底
    account_id = args.account_id or os.environ.get("CT_BILLING_ACCOUNT_ID")
    billing_token = args.billing_token or os.environ.get("CT_BILLING_TOKEN")

    drug_kw = [k.strip() for k in args.drug.split(",") if k.strip()]
    res = search_nmpa(drug_kw, [args.event] if args.event else [], args.terms,
                      args.max_pages, args.run, args.out, args.timeout,
                      args.token, args.endpoint, account_id, billing_token)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
