#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coze_client.py — ct-samplesize v4.0 coze 后端（权威计算引擎）

职责：
  - 将本地解析好的参数打包成请求信封，调用 coze 端 R 服务。
  - 解析 coze 返回的多部件信封（数值 + 可选 R 代码/结果 + 可选可视化产物）。
  - 端点与 Bearer token 默认取自 `coze_token_embedded`（随技能发布的公共凭据，
    XOR+base64 混淆内嵌）；可用 env(CTSS_COZE_ENDPOINT / CTSS_COZE_TOKEN) 覆盖。
  - mock 模式（CTSS_COZE_MOCK=1）仍保留，用于无网络/演示场景返回样例信封。

出站授权（ct-base §5 安全模型 / docs/02-security-model.md，2026-08-19 应用）：
  - 任何发往外部端点的请求在真正发送前经 `_check_outbound_authorization` 门控：
    命中 config/config.json 的 auto_approve_endpoints 白名单（公共端点已由作者预置，
    永不弹确认）或本会话内存已授权 → 放行；否则 stderr 输出 AUTH-BLOCK + 全库统一
    确认提示，**不发送**（授权不阻断流程：返回 None，由调用方提示用户）。
  - 发往端点的 payload 经 `sanitize()` 剥离 PII（身份证 / 手机号 / 邮箱）。
  - Windows 系统代理残留（WinError 10061）→ 绕过代理直连重试一次。
  - 异常与日志绝不回显 token / payload 明文（只打异常类型与端点）。

信封契约见 adapters/coze/coze_contract.md。
"""
import contextvars
import hashlib
import json
import os
import re
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from types import SimpleNamespace

from compute_backend import ComputeBackend, Figure, Result

# 自举 sys.path（2026-08-19 修复）：本文件通过 `adapters.coze_client` 方式导入时
# （CLI 主路径 samplesize_power.py → compute_backend → adapters.coze_client），
# sys.path 通常不含 adapters/ 目录 → 裸 `from coze_token_embedded import` 失败 →
# 内嵌端点/token 静默丢失 → coze_available() 误判"coze 不可达"。
# 这里把本文件所在目录加入 sys.path（幂等），保证两种导入方式行为一致。
_HERE_DIR = str(Path(__file__).resolve().parent)
if _HERE_DIR not in sys.path:
    sys.path.insert(0, _HERE_DIR)

# ---------------------------------------------------------------------------
# coze 信封契约漂移检测（ct-base §20.9 单入口 · 2026-08-29 修订：仅结构/数据内容不一致触发）
# ---------------------------------------------------------------------------
# 仅当 coze 返回的数据内容与本地消费接口不一致（字段别名 / 结构形变）时，自适应兼容并
# 经 HTML 横幅（_needs_upgrade / _contract_drift 驱动）提示升级。
# ⚠️ 版本号差异**不再**触发任何提醒：版本由 coze 端随发布同步，本地不比对版本号，避免无谓打扰。


def _assess_contract(parsed: dict) -> tuple:
    """结构/数据内容漂移检测（自愈优先），单一入口（ct-base §20.9 · 2026-08-29 修订）。

    仅检测「结构漂移（主·自愈）」：识别已知字段别名并自适应归一化，保证报告仍能渲染；
    映射发生时记 drift 说明，交给 rendering.py 在 HTML 横幅提示升级。对无法自适应的
    结构缺失仅记录告警、不臆造数据。别名表按 ct-samplesize 信封微调。

    ⚠️ 版本号差异**不再**触发任何提醒：版本由 coze 端随发布同步，本地不比对版本号，
    避免无谓打扰。仅当返回的「数据内容 / 结构」与本地消费接口不一致时才提示。

    Returns: (parsed, drift_notes, needs_upgrade)
      drift_notes 非空（= 检测到数据内容/结构不一致）=> 交给 rendering.py 在 HTML 横幅提示；
      needs_upgrade 仅为机器可读标记（写回 parsed），本函数**不产生任何用户可见提示**
      （用户可见提示统一只在渲染层的 HTML 横幅，避免 stderr / notes 重复提示）。
    """
    if not isinstance(parsed, dict):
        return parsed, [], False
    notes = []
    p = parsed

    # ---- 结构漂移：已知字段别名 → 本地期望字段（仅当期望字段缺/空、且别名存在时映射）----
    # 1) 主叙述：旧信封 `content` → 当前 `narrative`
    if not p.get("narrative") and isinstance(p.get("content"), str) and p["content"].strip():
        p["narrative"] = p["content"]
        notes.append("coze 响应字段已变更：主叙述由 `content` 改为 `narrative`，已自动适配")

    # 2) figures 结构兜底（dict → list；图体别名 image/svg_data/base64/svg → content）
    figs = p.get("figures")
    if isinstance(figs, dict):
        p["figures"] = [
            {"format": "svg", "content": v, "caption": k}
            for k, v in figs.items() if isinstance(v, str)
        ]
        notes.append("coze 响应结构已变更：figures 由 dict 改为 list，已自动适配")
    elif isinstance(figs, list):
        for i, f in enumerate(figs):
            if isinstance(f, dict) and "content" not in f:
                for fa in ("svg", "image", "svg_data", "base64"):
                    if isinstance(f.get(fa), str):
                        f["content"] = f[fa]
                        notes.append(
                            f"coze 响应字段已变更：figures[{i}] 图体由 `{fa}` 改为 `content`，已自动适配")
                        break

    # 去重（保持顺序）
    seen, uniq = set(), []
    for n in notes:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    return p, uniq, bool(uniq)


# ---------------------------------------------------------------------------
# coze 调用并发限流（2026-08-28 新增 · ct-base §20.10 全库统一标准）
# ---------------------------------------------------------------------------
# 相邻两次 coze /run 出站调用之间必须间隔 ≥1 秒，防止触发 coze 端频控（429）。
# meta-analysis 实测曾因密集请求被限流至次日，整批分析失败。强制间隔是零成本护栏。
# 间隔秒数可由环境变量 COZE_META_MIN_INTERVAL（浮点秒）覆写；<=0 时关闭保护（调试用）。
_RATE_LIMIT_LOCK = threading.Lock()
_LAST_CALL_TS = 0.0  # time.monotonic() of the most recently dispatched coze POST


def _acquire_rate_limit() -> None:
    """相邻两次 coze POST 之间至少间隔 1 秒（可由 COZE_META_MIN_INTERVAL 覆写）。

    用模块级锁串行化"间隔决策"并强制最小间隔；锁内只做间隔判定 + 必要 sleep 占位，
    网络请求在锁释放后发出——既保证 ≥1s 间距，又不把网络延迟锁进临界区。
    作用域：同一 Python 进程内多线程并发（本技能典型调用场景）。跨进程并发需另加
    文件锁，当前未实现（ct-base §20.10 边界）。
    """
    try:
        interval = float(os.environ.get("COZE_META_MIN_INTERVAL", "1.0"))
    except (TypeError, ValueError):
        interval = 1.0
    if interval <= 0:
        return
    global _LAST_CALL_TS
    with _RATE_LIMIT_LOCK:
        now = time.monotonic()
        wait = interval - (now - _LAST_CALL_TS)
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
        _LAST_CALL_TS = now


# 发布版强制禁用内嵌凭据：设置 CTSS_COZE_NO_EMBEDDED=1 后，即使 coze_token_embedded.py
# 存在也忽略，强制走 env(CTSS_COZE_TOKEN / CTSS_COZE_ENDPOINT)，避免内嵌密钥随包外泄。
if os.environ.get("CTSS_COZE_NO_EMBEDDED") in ("1", "true", "yes"):
    _embedded_get_token = None
    _embedded_get_endpoint = None
else:
    try:
        from coze_token_embedded import (
            get_token as _embedded_get_token,
            get_endpoint as _embedded_get_endpoint,
        )
    except Exception:  # pragma: no cover - 内嵌凭据缺失时退化为仅 env/mock
        _embedded_get_token = None
        _embedded_get_endpoint = None

# ---------------------------------------------------------------------------
# 出站授权确认提示（ct-base language_policy：一次性提示强制走 i18n，禁止硬编码）
# ---------------------------------------------------------------------------
try:
    from i18n import t as _i18n_t  # 单一事实来源：scripts/i18n.py _MESSAGES
    _HAS_I18N = True
except Exception:  # pragma: no cover - 测试环境缺 scripts 路径时退化
    _HAS_I18N = False
    _i18n_t = None


# ---------------------------------------------------------------------------
# §8.6 query_origin：调用来源标识（全库统一，审计 / 归因 / 限流）
# ---------------------------------------------------------------------------
def _compute_query_origin() -> str:
    """§8.6 query_origin：按本机 hostname 计算稳定标识，由客户端（技能安装设备）生成。

    - 格式 `sha256:<64 hex>`；同一台机器每次返回完全相同的值（便于按机器审计/限流）。
    - SHA256 单向不可逆，不含明文 hostname / IP / 任何 PII。
    - **必须由客户端生成随请求发出**，禁止由 coze 服务器兜底生成（服务器容器重建即漂移）。
    """
    return "sha256:" + hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()

# ---------------------------------------------------------------------------
# skill_version：技能版本号（2026-09-02 新增 · 服务端分版本归因）
# ---------------------------------------------------------------------------
# 由客户端（技能安装设备）随请求发出，coze 端透传写入飞书日志的 **resultstr 顶层**
# （ct-base coze_io_contract §2.1，2026-09-17 起；此前曾并入 querystr，已移除），用于
# 按技能版本归因调用量与失败率。**可选字段**：老版本技能不发送该字段时，coze 端
# 按缺省处理（resultstr 不含该键），两端均不报错（见 coze_contract.md §2）。
_SKILL_VERSION_FALLBACK = "5.7.27"


def _skill_version() -> str:
    """技能版本号：优先读技能根 `SKILL.md` frontmatter 的 `version:`（单一事实来源），
    读取失败（文件缺失 / 格式异常）时回退到模块常量 `_SKILL_VERSION_FALLBACK`。

    每次调用读一次文件（<1ms，且出站已按 ≥1s 限流，开销可忽略）；换来的是升级技能后
    无需同步改本文件——版本号永远与 SKILL.md 保持一致。
    """
    try:
        skill_md = Path(__file__).resolve().parent.parent / "SKILL.md"
        head = skill_md.read_text(encoding="utf-8")[:4000]
        m = re.search(r"^version:\s*([0-9][\w.\-]*)", head, re.M)
        if m:
            return m.group(1)
    except Exception:  # pragma: no cover - 文件缺失/编码异常时静默回退
        pass
    return _SKILL_VERSION_FALLBACK

# ---------------------------------------------------------------------------
# 出站授权门控（ct-base 全库统一范式，对齐 ct-advisor scripts/refine_answer.py）
# ---------------------------------------------------------------------------
# 本会话内存已授权端点（随进程重置：同一次脚本运行内多次出站只确认一次）。
_SESSION_AUTHORIZED_ENDPOINTS = set()


def _default_config_path() -> str:
    """config.json 默认路径（技能根 config/）。"""
    here = Path(__file__).resolve().parent.parent  # adapters/ -> 技能根
    return str(here / "config" / "config.json")


def _load_auto_approve_endpoints(config_path: str) -> set:
    """从 config.json 加载 auto_approve_endpoints 白名单。"""
    try:
        cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
        return set(cfg.get("auto_approve_endpoints", []) or [])
    except Exception:
        return set()


def _check_outbound_authorization(endpoint: str, config_path: str = None) -> bool:
    """出站授权检查：返回 True 放行，False 拦截（不发送）。

    语义（ct-base）：
      - 命中本会话内存 / config.json 白名单（作者预置公共端点）→ True，永不弹确认；
      - 否则 stderr 输出 AUTH-BLOCK + 全库统一确认提示，返回 False。
    白名单写入须由用户确认触发（agent 引导、不代写 config.json）。
    """
    if endpoint in _SESSION_AUTHORIZED_ENDPOINTS:
        return True
    cfg_path = config_path or _default_config_path()
    if endpoint in _load_auto_approve_endpoints(cfg_path):
        return True
    # 一次性出站授权确认：强制走 i18n 单语输出（ct-base language_policy §首次使用与一次性运行期提示）。
    # 主路径经 t("auth.coze_outbound") 取词（单一事实来源 scripts/i18n.py），
    # 仅在 i18n 不可导入（测试环境缺 scripts 路径）时退化为英文安全提示，绝不中英双显/硬编码。
    if _HAS_I18N:
        prompt = _i18n_t("auth.coze_outbound", endpoint=endpoint)
    else:
        prompt = (
            "[ct-samplesize] outbound to %s requires user confirmation. "
            "Only trial-design parameters (no personal data) are sent; "
            "declining disables cloud computation." % endpoint
        )
    sys.stderr.write(
        "[ct-samplesize][AUTH-BLOCK] outbound to %s requires user confirmation.\n"
        "%s\n" % (endpoint, prompt)
    )
    return False


def _authorize_endpoint(endpoint: str, config_path: str = None) -> None:
    """（供 agent 引导用户确认后调用）把端点加入会话内存授权。"""
    _SESSION_AUTHORIZED_ENDPOINTS.add(endpoint)


# ---------------------------------------------------------------------------
# payload 脱敏（ct-base：出站 payload 发送前剥离 PII；日志绝不回显明文）
# ---------------------------------------------------------------------------
# 注意（2026-08-19 修复）：原实现用 \b 边界，Python 把中文字符视为 \w，
# "身份证<18位>" 中 "证" 与数字之间无 \b → 身份证/手机号永不匹配。
# 改为数字/字母数字负向断言（对中文相邻文本同样生效）：
#   ID    18位（17数字+X/x）；先于 PHONE 匹配，防止手机号模式吞身份证子串
#   PHONE 大陆手机号
#   EMAIL 邮箱（ASCII 边界，避免吞并相邻中文）
_PII_PATTERNS = [
    (re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"), "<ID>"),               # 身份证号
    (re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "<PHONE>"),             # 大陆手机号
    (re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+(?![A-Za-z0-9])"), "<EMAIL>"),  # 邮箱
]


def sanitize(obj):
    """递归剥离 PII（身份证 / 手机号 / 邮箱），返回脱敏副本（不修改原对象）。"""
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(v) for v in obj]
    if isinstance(obj, str):
        for pat, repl in _PII_PATTERNS:
            obj = pat.sub(repl, obj)
        return obj
    return obj


# 入口标识（entry_point）— 2026-10-07 新增（ct-base coze_io_contract §1.3）
# 区分调用来源：技能本身（"skill"） vs 工作台 web 应用（"workbench"）。
# 透传写入飞书 entry_point 列，供后台按来源筛选/统计。
# 默认 "skill"；工作台进程在 fullflow 入口调用 set_entry_point("workbench") 覆盖。
_ENTRY_POINT = "skill"


def set_entry_point(value: str) -> None:
    """覆盖进程级入口标识（工作台调用以标记 workbench）。"""
    global _ENTRY_POINT
    _ENTRY_POINT = value or "skill"


def _with_user_language(params, lang):
    """把用户语言注入请求 `params`（ct-base coze_io_contract §1.1 唯一承载位）。

    2026-09-03 收敛：此前 `user_language` 既在顶层信封、又在 `params` 内（双写冗余），
    与 canonical §1.1「位置：请求 params 内（非顶层信封）」不一致。现统一为**仅进
    params**，顶层信封不再携带该键。

    兼容策略（双向）：
      - 入参 `params` 已含有效 `user_language`（build_params 总会写入）→ 原样保留，不覆盖；
      - 缺失/非 zh/en → 用 `lang` 兜底注入；
      - 服务端（coze）按 `params.user_language` → 顶层 `user_language` 顺序回退读取，
        老客户端（仍发顶层）不受影响。
    """
    out = dict(params) if isinstance(params, dict) else {}
    cur = out.get("user_language")
    if cur not in ("zh", "en"):
        out["user_language"] = lang
    return out


# ---------------------------------------------------------------------------
# 端点 / token / locale 解析
# ---------------------------------------------------------------------------
def _resolve_token() -> str:
    """取 coze Bearer token：env(CTSS_COZE_TOKEN) > 内嵌公共 blob。"""
    env = os.environ.get("CTSS_COZE_TOKEN")
    if env:
        return env
    if _embedded_get_token is not None:
        return _embedded_get_token()
    return ""


def _resolve_endpoint() -> str:
    """取 coze 端点：env(CTSS_COZE_ENDPOINT/COZE_ENDPOINT) > 内嵌公共常量。"""
    env = os.environ.get("CTSS_COZE_ENDPOINT") or os.environ.get("COZE_ENDPOINT")
    if env:
        return env
    if _embedded_get_endpoint is not None:
        return _embedded_get_endpoint()
    return ""


def _current_locale() -> str:
    """当前界面语言（zh / en），走 ct-base i18n._current_lang()（系统 locale 检测）。

    语言解析的权威实现是 i18n.resolve_user_language(query, override)（三级优先级：
    override > 输入文本 → 系统 locale），由调用方（samplesize_power.main）解析后写入
    ctx["user_language"] 经本模块信封发出。本函数仅作信封兜底（ctx 未带 user_language
    时回退系统语言），不重复实现检测逻辑。
    """
    try:
        from i18n import _current_lang
        return _current_lang()
    except Exception:
        return "en"


# 本地编排控制字段，不进入发往 coze 的请求参数
_PARAM_EXCLUDE = frozenset({
    "yes", "dry_run", "show_code", "install_all_packages", "test",
    # 曲线序列/效应量列表走 curve_* 协议（R 端 run_task.R 曲线分支消费）
    "n_seq", "power_seq", "plot_effects", "effect_seq",
    # 三类新图形开关：dist_plot / power_time_seq / heatmap
    "dist_plot", "power_time_seq", "heatmap",
})

# 引擎控制类参数：不在契约 required 白名单内，但用户显式请求时必须进入信封，
# 否则 build_params 白名单会将其剥离，导致 samplesize_power 收不到对应 CLI flag。
# C3 Monte-Carlo 验证（verify*）/ C5 公开证据基准（effect_ref·adopt_ref）/
# C6 方案论证段（justify）·假设质量审计（audit·evidence_source）。
_ENGINE_CONTROL_KEYS = (
    "verify", "verify_design", "verify_n", "verify_looks", "verify_spending",
    "justify", "audit", "evidence_source", "effect_ref", "adopt_ref",
)


# 契约索引缓存（tests/coze_cases/_contract_index.json 的 required 字段 = 每 test 所需参数白名单）
_CONTRACT_REQUIRED_CACHE = None
# optional 通道缓存（v5.13.19）：契约显式登记的 required 之外可选统计参数
# （meta_planning 的 n_cv/n_sim），与 required 同一 JSON 事务加载
_CONTRACT_OPTIONAL_CACHE = {}
_CONTRACT_LOAD_FAILED = False

# ---------------------------------------------------------------------------
# 发布包内契约（2026-11-15 · 修复 P0-1 根因）
# ---------------------------------------------------------------------------
# 原 _load_contract_required 只认 `adapters/workbench/publish/tests/coze_cases/
# _contract_index.json`，而发布包按 ct-base §16 红线排除 tests/ → 契约恒加载失败，
# build_params 发送全部 argparse 默认值（实测 136~141 键），出站守卫又因共用同一
# 依赖一并放行。改为优先读 config/log_contract.json（发布包内、由
# scripts/build_log_contract.py 从 tests/coze_cases/_contract_index.json 烘焙生成）。
_LOG_CONTRACT_CACHE = None
_LOG_CONTRACT_PATHS = (
    Path(__file__).resolve().parent.parent / "config" / "log_contract.json",
    Path(__file__).resolve().parent / "log_contract.json",
    Path(__file__).resolve().parent.parent / "workbench" / "publish" / "tests"
    / "coze_cases" / "_contract_index.json",
    Path(__file__).resolve().parent.parent / "tests" / "coze_cases" / "_contract_index.json",
)


def _load_log_contract():
    """读发布包内契约；缺失时返回最小骨架（fail-closed，不再静默发送全量默认值）。"""
    global _LOG_CONTRACT_CACHE
    if _LOG_CONTRACT_CACHE is not None:
        return _LOG_CONTRACT_CACHE
    for p in _LOG_CONTRACT_PATHS:
        try:
            if p.exists():
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, dict) and isinstance(data.get("tests"), dict):
                    _LOG_CONTRACT_CACHE = data
                    return data
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write("[ct-samplesize][guard] 契约读取失败 %s: %s\n" % (p, exc))
    _LOG_CONTRACT_CACHE = {"tests": {}, "common": [], "ranges": [],
                           "argparse_defaults": {}, "intent_hints": {}}
    sys.stderr.write("[ct-samplesize][guard] 契约缺失：启用 fail-closed 最小白名单\n")
    return _LOG_CONTRACT_CACHE


def _contract_common():
    return _load_log_contract().get("common") or []


def _argparse_defaults():
    return _load_log_contract().get("argparse_defaults") or {}


def validate_domain(test, params, lang=None):
    """P0-2：出站前本地参数域校验（零网络往返）。返回 (ok, message)。

    与 Coze 端 run_task.R::.PARAM_RANGE_HINTS 及 log_aggregator.validate_domain
    同源（口径写在 config/log_contract.json 的 ranges）。命中越界时 call() 直接
    返回可行动的双语错误信封，不再让用户付 4~5s 云端往返看裸 R 报错。
    """
    lang = lang or _current_locale() or "zh"
    p = params if isinstance(params, dict) else {}
    for r in _load_log_contract().get("ranges") or []:
        if r.get("only_test") and r["only_test"] != test:
            continue
        for key in r.get("keys") or []:
            v = p.get(key)
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                continue
            lo, hi, opn = r.get("lo"), r.get("hi"), bool(r.get("open"))
            bad = ((lo is not None and (v <= lo if opn else v < lo))
                   or (hi is not None and (v >= hi if opn else v > hi)))
            if not bad:
                continue
            desc = r.get("zh") if str(lang).startswith("zh") else r.get("en")
            if str(lang).startswith("zh"):
                return False, ("参数取值无效：%s = %g 超出有效范围 (%s, %s)，无法计算。"
                               "请修正后重试（本次未发起云端请求）。"
                               % (desc, v, "-∞" if lo is None else lo,
                                  "+∞" if hi is None else hi))
            return False, ("Invalid parameter: %s = %g outside (%s, %s). "
                           "Please fix and retry (no cloud request was sent)."
                           % (desc, v, "-inf" if lo is None else lo,
                              "+inf" if hi is None else hi))
    return True, ""


# ---------------------------------------------------------------------------
# 请求级日志作用域（2026-11-15 · 一次用户需求 → 少量飞书行）
# ---------------------------------------------------------------------------
_REQUEST_CTX = contextvars.ContextVar("ctss_request_ctx", default=None)
_FALLBACK_CTX = {"id": "", "seq": 0, "log_mode": "auto", "is_qa": False}
_CTX_LOCK = threading.RLock()


def _get_request_ctx():
    c = _REQUEST_CTX.get()
    return c if c is not None else _FALLBACK_CTX


class request_scope:
    """把一次「用户需求」的所有 Coze 子调用绑定到同一 request_id。

    用法（编排层 / 工作台入口）：
        with request_scope() as rid:
            call(...)          # 子调用 1
            call_paired(...)   # 子调用 2
            call_grid(...)     # 子调用 3
        # 服务端按 rid 合并写：首次 add_records，后续 update_records 同一行

    不显式包裹时 call() 会生成一个单次 ID（= 1 POST 1 行，行为与历史一致）。
    """

    def __init__(self, request_id=None, *, log_mode="auto", is_qa=False):
        self.request_id = request_id or ("ctss-" + uuid.uuid4().hex)
        self.log_mode = log_mode
        self.is_qa = bool(is_qa)
        self._token = None
        self._prev = None

    def __enter__(self):
        ctx = {"id": self.request_id, "seq": 0,
               "log_mode": self.log_mode, "is_qa": self.is_qa}
        self._token = _REQUEST_CTX.set(ctx)
        with _CTX_LOCK:
            self._prev = dict(_FALLBACK_CTX)
            _FALLBACK_CTX.update(ctx)
        return self.request_id

    def __exit__(self, *exc):
        if self._token is not None:
            _REQUEST_CTX.reset(self._token)
        with _CTX_LOCK:
            _FALLBACK_CTX.update(self._prev or
                                 {"id": "", "seq": 0, "log_mode": "auto", "is_qa": False})
        return False


def _request_meta(call_type=""):
    """构造随每个出站信封透传的聚合元数据（供 feishu_save 合并写）。"""
    ctx = _get_request_ctx()
    rid = ctx.get("id") or ""
    with _CTX_LOCK:
        seq = int(ctx.get("seq", 0)) + 1
        ctx["seq"] = seq
    if not rid:
        rid = "ctss-" + uuid.uuid4().hex
    return {
        "request_id": rid,
        "call_seq": seq,
        "log_mode": ctx.get("log_mode") or "auto",
        "call_type": call_type,
        "is_qa": bool(ctx.get("is_qa", False)),
    }


# 旧版参数名 → 现行契约键（P2-9：5.8.0 仍带 delta/sd/sides，落 R 引擎报 NA）
_LEGACY_PARAM_ALIASES = {"sides": "side", "delta": "effect", "sig_level": "alpha",
                         "power_target": "power", "sd": "sd"}


def normalize_legacy_params(params):
    """兼容老客户端参数名；side 数字 2/1 → 'two'/'one'。"""
    if not isinstance(params, dict):
        return params
    out = dict(params)
    for old, new in _LEGACY_PARAM_ALIASES.items():
        if old in out and new not in out:
            out[new] = out.pop(old)
    if isinstance(out.get("side"), int) and out["side"] in (1, 2):
        out["side"] = "two" if out["side"] == 2 else "one"
    return out


# 本地短时去重（60s）：实证 60s 内同签名重复 25 行 / 91.8s；成功结果直接复用，
# 不产生新 POST、也不产生新飞书行。失败不缓存，保证用户修正后可立即重试。
_LOCAL_DEDUP = {}
_LOCAL_DEDUP_LOCK = threading.RLock()
_LOCAL_DEDUP_TTL = int(os.environ.get("CTSS_LOCAL_DEDUP_TTL", "60"))


def _dedup_key(test, params, mode):
    sig = json.dumps({"t": test, "p": params, "m": mode},
                     sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(sig.encode("utf-8")).hexdigest()


def _dedup_get(key):
    now = time.time()
    with _LOCAL_DEDUP_LOCK:
        item = _LOCAL_DEDUP.get(key)
        if item and now - item[0] <= _LOCAL_DEDUP_TTL:
            return item[1]
        if item:
            _LOCAL_DEDUP.pop(key, None)
    return None


def _dedup_put(key, out):
    if isinstance(out, dict) and out.get("status") in ("ok", "warn"):
        with _LOCAL_DEDUP_LOCK:
            _LOCAL_DEDUP[key] = (time.time(), out)
            if len(_LOCAL_DEDUP) > 256:
                for k in sorted(_LOCAL_DEDUP, key=lambda k: _LOCAL_DEDUP[k][0])[:128]:
                    _LOCAL_DEDUP.pop(k, None)


def clear_local_dedup():
    """测试/调试用：清空本地去重表。"""
    with _LOCAL_DEDUP_LOCK:
        _LOCAL_DEDUP.clear()


# 连续效应量键：仅这些参数出现的 test 才以 Cohen's d 解释效应量，才需要随信封发送
# d_val；比例/率/生存/诊断等 test 不消费 d_val，发送 d_val:0.5 默认值属脏参数泄漏
# （飞书 querystr 噪声），故在 build_params 中剔除。
_CONTINUOUS_EFFECT_KEYS = frozenset({"effect", "sd", "delta", "mean_diff"})

# 例外：这些 test 的 `effect` 是【比值型】（OR / RR / 率比），不是 Cohen's d，
# 故即使 required 含 `effect` 也不应发送 d_val（否则 d_val=OR/RR 属脏参数泄漏）。
# 2026-10-12 补充：Tier 1 的 ci_or/ci_rr 与 Tier 2 的回归/率比测试均属此类。
_D_VAL_EXCLUDED_TESTS = frozenset({
    "ci_or", "ci_rr", "regression_logistic", "regression_poisson", "rates_ext",
})


def _test_consumes_d_val(test):
    """契约驱动判定：该 test 是否消费连续型效应量 d_val（Cohen's d）。

    依据 tests/coze_cases/_contract_index.json 的 required 字段：若含连续效应量键
    （effect/sd/delta/mean_diff）则视为均值类 test，需要 d_val；否则（比例/率/生存/
    诊断等）剔除。契约未登记（加载失败或该 test 缺失）时保守返回 True，保留旧行为，
    避免误伤真正需要 d_val 的 test（零回归风险）。

    另见 _D_VAL_EXCLUDED_TESTS：`effect` 为比值型（OR/RR/率比）的 test 一律不发 d_val。
    """
    if test in _D_VAL_EXCLUDED_TESTS:
        return False
    required = _load_contract_required(test)
    if not required:
        # 契约缺失 → 保守发送（与旧行为一致）
        return True
    return any(k in required for k in _CONTINUOUS_EFFECT_KEYS)


def _load_contract_required(test):
    """从 _contract_index.json 加载该 test 的 required 参数白名单（单一真相源）。

    返回 frozenset；未登记/契约缺失 → 空 frozenset（调用方退化为发送全部非 None 字段）。
    """
    global _CONTRACT_REQUIRED_CACHE, _CONTRACT_LOAD_FAILED
    if _CONTRACT_REQUIRED_CACHE is None and not _CONTRACT_LOAD_FAILED:
        _CONTRACT_REQUIRED_CACHE = {}
        # ── 2026-11-15 P0-1：优先读发布包内 config/log_contract.json ────────
        # 旧路径 `adapters/workbench/publish/tests/coze_cases/...` 在发布包中
        # 不存在（§16 排除 tests/），是 136 键胖信封的直接根因。
        contract = _load_log_contract()
        tests = contract.get("tests") or {}
        if tests:
            for name, spec in tests.items():
                _CONTRACT_REQUIRED_CACHE[name] = frozenset(spec.get("required") or [])
                _CONTRACT_OPTIONAL_CACHE[name] = frozenset(spec.get("optional") or [])
        else:
            # 兼容旧布局（本地源码树）：tests/coze_cases/_contract_index.json
            for p in _LOG_CONTRACT_PATHS[2:]:
                try:
                    if not p.exists():
                        continue
                    data = json.loads(p.read_text(encoding="utf-8"))
                    for entry in data.get("tests", []):
                        _CONTRACT_REQUIRED_CACHE[entry["test"]] = frozenset(entry.get("required") or [])
                        _CONTRACT_OPTIONAL_CACHE[entry["test"]] = frozenset(entry.get("optional") or [])
                    if _CONTRACT_REQUIRED_CACHE:
                        break
                except Exception:
                    continue
        if not _CONTRACT_REQUIRED_CACHE:
            _CONTRACT_LOAD_FAILED = True
        # 注意：此处**只**返回该 test 的 required，不并入通用键。
        # build_params 会按 required 从 argparse namespace 取值，若把 ~35 个通用键
        # 并进去，正常信封会平白多带一批默认值（回归风险）；通用键只在
        # _trim_bloated_params 的裁剪白名单里使用。
    if _CONTRACT_LOAD_FAILED or not _CONTRACT_REQUIRED_CACHE:
        return frozenset()
    # 未登记 test：返回空集 → build_params 走旧「发送全部非 None」分支，
    # 保证新检验/跨域请求不被误裁参数（fail-open 仅限未知 test）。
    return _CONTRACT_REQUIRED_CACHE.get(test, frozenset())


def _load_contract_optional(test):
    """从 _contract_index.json 加载该 test 的 optional 参数通道（v5.13.19）。

    optional = required 之外、契约显式登记的可选统计参数（如 meta_planning 的
    n_cv/n_sim）。用户显式提供（argparse 非 None）才随信封发送；不提供走原解析档，
    向后兼容。与 _load_contract_required 同一加载事务（同一 JSON、同一缓存周期）。
    """
    _load_contract_required(test)  # 触发同一加载事务（含 optional 填充）
    return _CONTRACT_OPTIONAL_CACHE.get(test, frozenset())


def build_params(test, args, ctx):
    """把 args + ctx 序列化为 JSON 友好的请求参数。

    仅发送「本 test 实际需要」的参数，避免把 argparse 全家族默认值（varcorr/sigma/
    nsim/theta0/cv/design/ve_*/prior_a0/prob_*/n_doses/target_dlt/win_ratio_theta/...）
    一锅炖进 params（这些无关默认值虽被 R 端 %||% 忽略，但会让飞书 querystr 看起来像
    「全参数扫描」，无法区分真实请求与测试）。白名单取自 tests/coze_cases/_contract_index.json
    的 required 字段（与 CLI choices / R 引擎 dispatch 三者一致的单一真相源）。

    发送集合 = 该 test 的 required 参数（非 None）+ 通用参数 alpha + 模式关键参数
    （求 n → power；求 power → nobs）+ 派生量（solve_for_power/alt/d_val）+ 曲线参数
    （curve_*，来自 --n_seq/--power_seq/--plot_effects）。
    """
    ns = vars(args)
    required = _load_contract_required(test)
    params = {}
    if required:
        for k in required:
            if k in ns and ns[k] is not None:
                params[k] = ns[k]
        # 通用参数：alpha 几乎被全部 R 分支消费；argparse 默认 0.05，总是随请求带上
        alpha = ns.get("alpha")
        if alpha is not None:
            params.setdefault("alpha", alpha)
        # 模式关键参数：求样本量需要 target power；求效能需要 nobs
        if ctx.get("solve_for_power"):
            nobs = ns.get("nobs")
            if nobs is not None:
                params["nobs"] = nobs
        else:
            params["power"] = ns.get("power") or 0.8
    else:
        # 契约缺失/未登记 → 退化为原行为（发送全部非 None、非控制字段），保证不丢参
        for k, v in ns.items():
            if k in _PARAM_EXCLUDE:
                continue
            if v is None:
                continue
            if isinstance(v, (str, int, float, bool, list)):
                params[k] = v
    # 契约 optional 通道（v5.13.19）：required 之外、契约显式登记的可选统计参数
    # （如 meta_planning 的 n_cv/n_sim），用户显式提供（argparse 非 None）才随信封
    # 发送；不提供则 R 端走原解析档，向后兼容。契约缺失 → _load_contract_optional
    # 返回空集，此处零操作。
    for k in _load_contract_optional(test):
        if k in ns and ns[k] is not None:
            params[k] = ns[k]
    # 派生量
    params.update({
        "solve_for_power": ctx.get("solve_for_power", False),
        "alt": ctx.get("alt", "two.sided"),
        # 用户语言（zh/en）备用：随 params 进入 coze 端，作为 locale 的冗余兜底。
        # coze 端容器 LANG 多为英文，服务端自检测不到用户真实语言；
        # 此字段让 R 引擎在 req$locale 缺失时仍有用户语言可用。
        "user_language": ctx.get("user_language") or _current_locale(),
    })
    # d_val（Cohen's d）仅连续均值类 test 消费；比例/率/生存/诊断等 test 不消费，
    # 不发送以避免脏参数泄漏（飞书 querystr 噪声）。契约缺失时保守发送，不回归。
    if _test_consumes_d_val(test):
        params["d_val"] = ctx.get("d_val")
    # 曲线参数映射（CLI 名 → coze 端 curve_* 协议，R 端 run_task.R 曲线分支消费）
    for cli_key, coze_key in (("n_seq", "curve_n_seq"),
                              ("power_seq", "curve_power_seq"),
                              ("plot_effects", "curve_effects"),
                              ("effect_seq", "curve_effect_seq"),
                              ("dist_plot", "plot_dist"),
                              ("power_time_seq", "curve_power_time_seq"),
                              ("heatmap", "curve_heatmap")):
        val = ns.get(cli_key)
        if val:
            params[coze_key] = val
    # v5.13.6：引擎控制类参数显式转发（契约白名单之外的用户显式请求）
    for _k in _ENGINE_CONTROL_KEYS:
        _v = ns.get(_k)
        if _v is not None and _v is not False:
            params[_k] = _v
    return params


def build_batch(specs):
    """组装批量请求信封（coze v5.7 batch 模式，对应服务端 samplesize 节点 batch 分支）。

    specs: 列表，每项 = (test, args, ctx) 三元组（与单次 build_params 调用一致）。
           网格/敏感性扫描请一次性传入全部格点，服务端批量计算 + 合并飞书日志。
    返回可直接作为 /run 请求体的 dict：{"batch": [{"test","mode","params"}, ...]}。

    用途：把「逐格 N 次串行调用」（实证：4 分 15 秒 54 次）压成「1 次批量」，
    服务端经请求级幂等缓存再去重，飞书日志合并为单行。约 50%+ 调用量削减。
    """
    items = []
    for spec in specs:
        test = spec[0]
        args = spec[1]
        ctx = spec[2] if len(spec) > 2 else {}
        params = _trim_bloated_params(test, build_params(test, args, ctx or {}))
        mode = "power" if (ctx or {}).get("solve_for_power") else "n"
        items.append({"test": test, "mode": mode, "params": params})
    return {"batch": items}


# ---------------------------------------------------------------------------
# 出站信封守卫（v5.7.27 · 2026-09-11 后端日志实证驱动）
# ---------------------------------------------------------------------------
# 2026-09-11 后端日志（26 条请求）实证：每条请求平均携带 135 个参数（2.8KB），
# 而真正被消费的仅 6 个 —— 调用方（编排 agent）绕过 build_params 手拼了全家族
# argparse 默认值信封（auc0/cv/design/n_doses/win_ratio_theta/...），导致：
#   ① 飞书日志「全参数扫描」假象，真实请求与测试样本不可区分；
#   ② (test, params, mode, locale) 归一化签名含大量噪声键 → 服务端 10min TTL
#      幂等缓存几乎永不命中（同网格曲线重复计算占曲线请求 38%）。
# 守卫策略：params 键数显著超过该 test 契约白名单（required）时，判定为疑似
# 绕过 build_params 的过肥信封，裁剪至 required ∪ 通用/曲线键，stderr 告警。
# 正常 CLI / workbench 路径（build_params 产出 ~10-20 键）完全不受影响。
_ALWAYS_ALLOWED_PARAMS = frozenset({
    # 通用模式参数（build_params 派生量 + 求解关键参数）
    "alpha", "power", "nobs", "solve_for_power", "alt", "d_val", "side",
    "user_language",
    # curve_* 协议键（曲线 / 图形开关）
    "curve_n_seq", "curve_power_seq", "curve_effects", "curve_effect_seq",
    "plot_dist", "curve_power_time_seq", "curve_heatmap",
})


def _trim_bloated_params(test, params):
    """出站信封守卫：裁剪疑似绕过 build_params 的过肥 params（详情见上方块注释）。

    v5.13.19：白名单扩为 required ∪ optional（契约 optional 通道，meta_planning
    的 n_cv/n_sim 等经 workbench 直传路径也会过此处，必须在白名单内才能存活）。
    """
    if not isinstance(params, dict):
        return params
    required = _load_contract_required(test)
    if not required:
        # ── 2026-11-15 fail-closed（P0-1）────────────────────────────────
        # 旧实现「契约未登记 → 直接放行」，与 build_params 共用同一依赖：
        # 一旦契约文件缺失，两道防线同时失效（实测 50 行 136~141 键胖信封）。
        # 现改为按 argparse 默认值表剔除「值等于默认值」的噪声键；用户显式
        # 改过的键、未知键、通用模式键一律保留，不误伤真实入参。
        if len(params) <= 40:
            return params  # 正常信封零影响
        defaults = _argparse_defaults()
        if not defaults:
            sys.stderr.write("[ct-samplesize][guard] 契约与默认值表均不可用，"
                             "保守放行（请检查 config/log_contract.json）\n")
            return params
        trimmed = {k: v for k, v in params.items()
                   if k in _ALWAYS_ALLOWED_PARAMS or k not in defaults
                   or v != defaults.get(k)}
        for k in ("alpha", "power", "nobs"):
            if k not in trimmed and k in params:
                trimmed[k] = params[k]
        sys.stderr.write("[ct-samplesize][guard] 契约不可用 → 按默认值表 fail-closed "
                         "裁剪：params %d 键 → %d 键\n" % (len(params), len(trimmed)))
        return trimmed
    # 裁剪白名单 = 该 test 的契约键 ∪ 通用/模式/曲线键；不改变 build_params 出站集合
    allowed = (required | _load_contract_optional(test)
               | frozenset(_contract_common()) | _ALWAYS_ALLOWED_PARAMS)
    limit = max(30, len(allowed) + 15)
    if len(params) <= limit:
        return params
    trimmed = {k: v for k, v in params.items()
               if k in allowed or k in _ALWAYS_ALLOWED_PARAMS}
    # 保底回补：模式关键参数任一缺失则计算必然失败，从原 params 回补
    for k in ("alpha", "power", "nobs"):
        if k not in trimmed and k in params:
            trimmed[k] = params[k]
    sys.stderr.write(
        "[ct-samplesize][guard] 检测到过肥请求信封：params %d 键 → 裁剪至 %d 键"
        "（疑似绕过 build_params 手拼全家族默认值；契约白名单=%s）\n"
        % (len(params), len(trimmed), ",".join(sorted(allowed))))
    return trimmed


def _fill_external_svgs(parsed, timeout=30):
    """统一 manifest 重组入口（对齐 meta-analysis 2026-08-28）：
    优先走**新契约**：若响应含 `_coze_manifest`（coze 端把超 4000 的 figures/repro/narrative
    统一移进单个 manifest 文件并挂链接），则 GET manifest → 逐 path 写回原值 →
    重组为原始 JSON（含 content/r 代码/narrative），一次还原、零数据丢失。

    **向后兼容**：无 `_coze_manifest`（旧 coze 响应 / 方案 B）时，走旧契约——
    figures[].url→content、repro.url→r 逐项回填。

    - 超时 / 网络失败 → 保留引用并标记 _*_fetch_failed，绝不抛错中断分析。
    """
    if not isinstance(parsed, dict):
        return parsed
    # 新契约：manifest 单文件重组（优先级最高）
    manifest = parsed.get("_coze_manifest")
    if isinstance(manifest, dict) and manifest.get("storage") == "s3" and manifest.get("url"):
        return _reassemble_from_manifest(parsed, manifest, timeout=timeout)
    # 旧契约（方案 B，向后兼容）：figures[].url → content / repro.url → r
    return _fill_external_svgs_legacy(parsed, timeout=timeout)


def _reassemble_from_manifest(parsed, manifest, timeout=30):
    """按 manifest 重组原始 JSON（对齐 meta-analysis 2026-08-28，ct-samplesize 移植版）：
    coze 端把超 4000 的最大块（figures/repro/narrative）统一移进单个 S3 manifest 文件，
    manifest 为 [{path, value}, ...]，主返回体挂 `_coze_manifest = {storage:"s3", url}`。
    此处 GET manifest → 按 path 写回 value → 重组为原始 JSON。

    - path 支持 `figures[i]`（列表下标）、`stats.xxx` 点路径、**以及顶层键**（如 `narrative`）。
    - 写回时若该位置当前仍是 {storage:"s3",type:"block"} 引用（未被本地改动）才覆盖。
    - 超时 / 网络失败 → 保留 manifest 引用并在主返回体标 _manifest_failed，绝不抛错中断。
    - 重组完成后移除 `_coze_manifest`（下游见到的即原始结构）。
    """
    url = manifest.get("url")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            manifest_list = json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        parsed["_manifest_failed"] = True
        return parsed
    if not isinstance(manifest_list, list):
        parsed["_manifest_failed"] = True
        return parsed

    def _resolve_target(root, path):
        """返回 (容器, key) 或 (list, idx) 以便写回；找不到返回 None。
        支持 figures[i] / stats.xxx 点路径 / 顶层键（如 narrative）。
        """
        if path.startswith("figures["):
            # figures[i]
            m = path[8:-1]
            if not m.isdigit():
                return None
            idx = int(m)
            figs = root.get("figures")
            if not isinstance(figs, list) or idx >= len(figs):
                return None
            return figs, idx
        if "." in path:
            # stats.a.b 点路径
            parts = path.split(".")
            node = root
            for p in parts[:-1]:
                if not isinstance(node, dict) or p not in node:
                    return None
                node = node[p]
            if not isinstance(node, dict) or parts[-1] not in node:
                return None
            return node, parts[-1]
        # 顶层键（如 narrative）
        if isinstance(root, dict) and path in root:
            return root, path
        return None

    for entry in manifest_list:
        if not isinstance(entry, dict):
            continue
        p = entry.get("path")
        if not p:
            continue
        target = _resolve_target(parsed, p)
        if target is None:
            continue
        container, key = target
        cur = container[key]
        # 仅当仍是外置引用时才写回；已被本地改动为实际内容则跳过
        if isinstance(container, dict):
            is_ref = (isinstance(cur, dict) and cur.get("storage") == "s3"
                      and cur.get("type") == "block")
            if is_ref:
                container[key] = entry.get("value")
        else:  # list
            if isinstance(cur, dict) and cur.get("storage") == "s3" and cur.get("type") == "block":
                container[key] = entry.get("value")
    # 重组完成，移除 manifest 引用（下游见原始结构）
    parsed.pop("_coze_manifest", None)
    return parsed


def _fill_external_svgs_legacy(parsed, timeout=30):
    """旧契约（方案 B，向后兼容）：coze 端把 figures[].content（SVG）与 repro['r']
    （R 复现脚本）外置 S3 并返回 {type,format,storage:"s3",key,url} 引用；按 url 下载回填。

    - 超时 / 网络失败 → 保留 url 并标记 _svg_fetch_failed / _repro_fetch_failed，绝不抛错中断。
    - 已含 content / r（coze 降级内联）或不是 dict → 原样跳过。
    """
    if not isinstance(parsed, dict):
        return parsed
    figs = parsed.get("figures")
    if isinstance(figs, list):
        for fig in figs:
            if not isinstance(fig, dict):
                continue
            if fig.get("url") and not fig.get("content"):
                try:
                    with urllib.request.urlopen(fig["url"], timeout=timeout) as r:
                        fig["content"] = r.read().decode("utf-8")
                except Exception:  # noqa: BLE001
                    fig["_svg_fetch_failed"] = True
    # 方案 B 扩展：R 复现脚本外链回填（repro.url → repro.r）
    repro = parsed.get("repro")
    if isinstance(repro, dict) and repro.get("url") and not repro.get("r"):
        try:
            with urllib.request.urlopen(repro["url"], timeout=timeout) as r:
                repro["r"] = r.read().decode("utf-8")
        except Exception:  # noqa: BLE001
            repro["_repro_fetch_failed"] = True
    return parsed


# ---------------------------------------------------------------------------
# 公共 POST / 外层响应解析（2026-08-31 抽取：单请求 call() 与批量 call_batch() 复用）
# ---------------------------------------------------------------------------
# 2026-10-24 修复（524 根因）：计算请求专用短超时。Cloudflare 网关 100s 切断，
# 默认 600s 的 read_timeout 会让 server 傻等且用户只看到不可诊断的 524。
# 计算请求设 95s（<100s 网关），超时返回可控 504 + 友好提示。
_COMPUTE_TIMEOUT = float(os.environ.get("CTSS_COMPUTE_TIMEOUT", "95"))


def _post(payload_dict: dict, read_timeout=None):
    """POST payload 到 coze 端点，返回解析后的外层响应 dict（出错抛 URLError）。

    出站授权（ct-base §5）已在调用方 _check_outbound_authorization 门控后调用本函数；
    本函数只负责序列化 + 发请求 + 解析 outer，不含授权/语言/脱敏（由调用方在 payload 内完成）。
    频控 _acquire_rate_limit 仍在此处统一施加（相邻两次 coze POST 间隔 ≥1s）。
    """
    endpoint = _resolve_endpoint()
    token = _resolve_token()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    body = json.dumps(payload_dict, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
    _acquire_rate_limit()
    with _urlopen_with_proxy_fallback(req, read_timeout=read_timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _parse_outer(outer):
    """从 coze 外层响应取出**完整**内层信封（优先经 _coze_full 下载 S3 完整数据）。

    单请求：返回完整 out（含 figures/repro）；批量：返回完整 agg_full（含每项 out）。
    S3 不可达时降级到旧契约（manifest / figures[].url）或内联删减版，绝不抛错中断分析。
    """
    if not isinstance(outer, dict):
        return {"status": "error", "notes": "coze 返回非对象响应"}
    result_str = outer.get("result")
    if isinstance(result_str, str) and result_str.strip().startswith("{"):
        try:
            parsed = json.loads(result_str)
        except ValueError:
            return outer
        full = _fetch_full_json(parsed, timeout=30)
        if full is not None:
            return full
        return _fill_external_svgs(parsed)
    return _fill_external_svgs(outer)


def _fetch_full_json(parsed, timeout=30):
    """新契约（2026-08-29）：coze 把 R 引擎生成的完整信封整体写入单个 S3 文件，
    内联挂 `_coze_full = {storage:"s3", url}`。本地经 url 下载完整 JSON 作为分析源
    （含 figures/repro，零删减）。内联的轻量删减版（无 figures/repro）仅用于飞书日志
    与老版本技能兼容，本地分析不使用。

    返回完整 dict；下载失败 / 无链接 / 非 dict → 返回 None（调用方降级到旧契约或内联）。
    """
    if not isinstance(parsed, dict):
        return None
    full = parsed.get("_coze_full")
    if not (isinstance(full, dict) and full.get("storage") == "s3" and full.get("url")):
        return None
    try:
        with urllib.request.urlopen(full["url"], timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001
        parsed["_full_fetch_failed"] = True
        return None
    if not isinstance(data, dict):
        parsed["_full_fetch_failed"] = True
        return None
    data.pop("_coze_full", None)
    return data


def _mock_envelope(test, params, mode, return_r_code):
    """本地 mock：演示用样例信封（v5 结构：status/stats/narrative/figures）。"""
    sample_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="160">'
        '<rect width="100%%" height="100%%" fill="#fafafa"/>'
        '<text x="10" y="30" font-family="sans-serif" font-size="14">'
        'MOCK power curve (%s)</text>'
        '<polyline points="20,140 120,80 300,30" fill="none" stroke="#c0392b" stroke-width="2"/>'
        '</svg>' % test
    )
    env = {
        "status": "ok",
        "stats": {"test": test, "mode": mode, "note": "mock"},
        "narrative": (
            "MOCK coze response for test=%s (mode=%s).\n"
            "真实端点就绪后此处返回 R 端算出的数值与叙述。" % (test, mode)),
        "figures": [
            {"format": "svg", "content": sample_svg,
             "caption": "Mock power curve (%s)" % test}
        ],
        "warnings": ["MOCK 响应，非真实计算"],
        "notes": "",
        "repro": {"r": "# MOCK R code for %s" % test, "r_version": "mock",
                  "packages": {}},
    }
    return env


def _urlopen_with_proxy_fallback(req, connect_timeout=15, read_timeout=None):
    """HTTP POST + Windows 系统代理残留直连重试（ct-base 出站容错）。

    ⚠️ 关键修正（2026-08-29，对齐 meta-analysis）：
    旧实现 `http.client.HTTPSConnection(host, timeout=15)` 的 timeout 实际作用于
    **所有** socket 操作（connect 与 recv 共享同一超时）——注释里"读取不设限"是
    **错误**的。coze serverless 冷启动常 >15s，导致**读取响应阶段**被 15s 杀掉，
    表现为"每次都 15s 无应答"。meta-analysis 用 `urllib.urlopen(timeout=600)` 因此无此问题。

    修正方案：把 connect 与 read 拆成两个独立超时——
      - connect_timeout=15：连接握手失败快速报错（主机不可达时不空等）；
      - read_timeout（默认 600s，可由 CTSS_COZE_READ_TIMEOUT 覆盖）：允许冷启动
        与大规模 Monte-Carlo 计算的长时间响应读取，不被中途杀掉。
    实现：conn.request() 内部完成 connect+send（受 connect_timeout 约束），
    之后把底层 socket 超时改为 read_timeout，再 getresponse()/read()（受 read_timeout 约束）。

    返回对象实现 `.read()` 与上下文管理器，`call()` 的
    `with ... as resp: resp.read()` 契约保持不变。
    """
    import http.client

    if read_timeout is None:
        try:
            read_timeout = float(os.environ.get("CTSS_COZE_READ_TIMEOUT", "600"))
        except (TypeError, ValueError):
            read_timeout = 600.0

    def _conn():
        # connect 阶段受 connect_timeout 约束（主机不可达时快速失败，不空等 600s）。
        if req.type == "https":
            return http.client.HTTPSConnection(req.host, timeout=connect_timeout)
        return http.client.HTTPConnection(req.host, timeout=connect_timeout)

    def _do(conn):
        body = req.data if hasattr(req, "data") else None
        headers = dict(req.headers) if hasattr(req, "headers") else {}
        conn.request(req.get_method(), req.selector, body=body, headers=headers)
        # 连接已建立、请求已发出 → 把底层 socket 超时从 connect 改为 read 长超时，
        # 避免 coze 冷启动 / 长时间计算被 15s 杀掉（对齐 meta-analysis 的 600s 策略）。
        if getattr(conn, "sock", None) is not None:
            conn.sock.settimeout(read_timeout)
        return conn.getresponse()

    for attempt in (1, 2):
        conn = _conn()
        try:
            resp = _do(conn)
            return resp
        except (http.client.HTTPException, OSError, socket.error) as e:
            conn.close()
            # 首次失败若是 Windows 系统代理残留（10061/10060/11004），直连重试一次；
            # 计算请求幂等，重试无副作用。
            winerr = getattr(e, "winerror", None) or getattr(getattr(e, "reason", None), "winerror", None)
            errno = getattr(e, "errno", None) or getattr(getattr(e, "reason", None), "errno", None)
            if attempt == 1 and (winerr in (10061, 10060, 11004) or errno in (10061, 10060, 11004)):
                continue
            # 非代理残留错误 → 包装为与 urllib 一致的异常语义上抛
            raise urllib.error.URLError(reason=e)


def attach_billing(env: dict, account_id: str | None = None,
                   billing_token: str | None = None) -> dict:
    """billing 标识仅透传（ct-base §20.12 范本，2026-10-13 落地，与 meta-analysis
    attach_billing 同构）：account_id/billing_token 二选一注入信封顶层，与
    query_origin（匿名机器指纹）完全独立。缺失 → 免费路径（node 出口对 B 类
    高级方法拦截 R 代码）。billing_token 当前仅透存不验签（验签+计量+配额为
    后续 coze 端 billing 中间件职责）。"""
    if account_id:
        env["account_id"] = account_id
    if billing_token:
        env["billing_token"] = billing_token
    return env


def _billing_from_env() -> tuple:
    """从环境变量读取计费标记（调用方「直接发送变量」的本地接入口）：
    CTSS_ACCOUNT_ID / CTSS_BILLING_TOKEN，任一非空即返回 (account_id, token)。
    当前无发放渠道 → 通常返回 ('', '') → 全部按免费拦截（架构位先行）。"""
    return (os.environ.get("CTSS_ACCOUNT_ID") or "",
            os.environ.get("CTSS_BILLING_TOKEN") or "")


def call(test, params, mode, return_r_code, locale=None, resolved_spec=None,
         user_language=None, account_id=None, billing_token=None, read_timeout=None,
         call_type="single", dedup=True):
    """调用 coze 服务，返回 R 引擎信封 dict（重构 v5 协议）。

    模式（优先级从高到低）：
      - CTSS_COZE_MOCK=1 → 本地 mock 信封（演示/测试；无出站、不走授权门控）
      - CTSS_COZE_ENDPOINT / COZE_ENDPOINT 或内嵌端点 → 真实 HTTP POST（urllib，无第三方依赖）
      - 均未设置 → 抛错提示配置端点

    出站授权（ct-base §5）：真实发送前经 _check_outbound_authorization 门控；
    未授权 → stderr AUTH-BLOCK + 确认提示，**不发送**、返回 None（授权不阻断流程，
    由调用方提示用户）。发往端点的 payload 经 sanitize() 剥离 PII。
    """
    # ── 2026-11-15：旧参数名兼容 + 出站前参数域校验（P0-2 / P2-9）────────
    params = normalize_legacy_params(params)
    lang0 = user_language or locale or _current_locale()
    ok, msg = validate_domain(test, params, lang0)
    if not ok:
        # 直接返回与 R 引擎同形状的错误信封：零网络往返、零飞书写行、可行动提示
        return {"status": "error", "stats": None, "narrative": "",
                "figures": [], "warnings": [], "notes": msg, "repro": None,
                "test": test, "domain_validation": True, "cache_hit": False}
    # mock 显式优先：设置了 mock 绝不联网、不走授权门控（2026-08-19 修复：
    # 原实现把 mock 分支放在 endpoint 之后，内嵌端点恒非空导致 mock 成为死代码）
    if os.environ.get("CTSS_COZE_MOCK") in ("1", "true", "yes"):
        return _mock_envelope(test, params, mode, return_r_code)
    endpoint = _resolve_endpoint()
    if endpoint:
        # ── 出站授权门控（ct-base 全库统一）──────────────────────────────
        if not _check_outbound_authorization(endpoint):
            return None  # AUTH-BLOCK：不发送，调用方提示用户
        token = _resolve_token()
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer %s" % token
        # 发送前脱敏（剥离 PII）；脱敏副本用于发送，原 params 不受影响
        # 语言：locale 为输出语言主字段（顶层信封）；user_language 为备用提示，
        # 按 ct-base coze_io_contract §1.1 只进请求 params（顶层不再双写）。
        # 优先级 user_language > locale > 自动检测；coze 端容器 LANG 多为英文，
        # 服务端自检测不到用户真实语言，故由客户端把解析结果随 params 带出。
        lang = user_language or locale or _current_locale()
        # 出站信封守卫：裁剪疑似绕过 build_params 的过肥 params（v5.7.27）
        params = _trim_bloated_params(test, params)
        sent_params = _with_user_language(sanitize(params), lang)
        # ── 本地短时去重（P1-4）：60s 内同签名成功结果直接复用，不新开 POST、不新写行 ──
        dkey = _dedup_key(test, sent_params, mode) if dedup else None
        if dkey:
            cached = _dedup_get(dkey)
            if cached is not None:
                return dict(cached, cache_hit=True, served_from="local_dedup")
        payload = {
            "test": test, "params": sent_params, "mode": mode,
            "return_r_code": return_r_code,
            "locale": lang,
            "query_origin": _compute_query_origin(),
            "skill_version": _skill_version(),
            # 入口标识（2026-10-07）：skill/workbench，透传飞书 entry_point 列
            "entry_point": _ENTRY_POINT,
            "resolved_spec": resolved_spec or {
                "test": test, "mode": mode, "params": sent_params
            },
        }
        # ── 请求级日志聚合元数据（一次用户需求 → 少量飞书行）──────────────
        payload.update(_request_meta(call_type))
        # 计费身份标识（ct-base §20.12）：显式参数优先，缺失回退 env（CTSS_ACCOUNT_ID /
        # CTSS_BILLING_TOKEN）；均无 → 不带字段 → coze 端按免费路径处理。
        if not (account_id or billing_token):
            account_id, billing_token = _billing_from_env()
        attach_billing(payload, account_id, billing_token)
        try:
            outer = _post(payload, read_timeout=read_timeout)
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            # 超时（read_timeout 触发）统一转 COZE_TIMEOUT 标记，server 侧据此返回 504
            _reason = getattr(e, "reason", e)
            _is_timeout = (isinstance(e, socket.timeout) or isinstance(_reason, socket.timeout)
                           or "timed out" in str(e).lower() or "timeout" in str(e).lower())
            if _is_timeout:
                raise RuntimeError("COZE_TIMEOUT: coze 计算超时（%s，超过 %ss 上限）" % (endpoint, _COMPUTE_TIMEOUT))
            # 只打异常类型 + 端点（绝不回显 token / payload）
            raise RuntimeError("coze 调用失败（%s）: %s" % (endpoint, e))
        out = _parse_outer(outer)
        if dkey:
            _dedup_put(dkey, out)
        return out
    raise RuntimeError(
        "coze 端点未配置：请设置 CTSS_COZE_ENDPOINT（真实），"
        "或 CTSS_COZE_MOCK=1（本地演示）。")


def call_batch(specs, return_r_code=True, user_language=None,
               account_id=None, billing_token=None, read_timeout=None,
               call_type="batch"):
    """v5.7 批量计算：specs = [(test, args, ctx), ...]（与 build_batch 入参一致）。

    返回服务端聚合的**完整**结果 dict（agg_full，含每项 out 完整信封）；
    AUTH-BLOCK（未授权）返回 None；mock 模式返回本地聚合信封（不联网）。

    与 call() 的差异：
      - 请求体顶层为 {"batch": [...]} 而非 {test, params, mode, ...}；
      - 服务端把 N 格扫描压成 1 次计算，并返回聚合 agg（含每项的完整 out）；
      - 本地经 agg 的 _coze_full 一次下载即得全部 item 结果，无需逐条解析。
    """
    if os.environ.get("CTSS_COZE_MOCK") in ("1", "true", "yes"):
        return _mock_batch(specs, return_r_code=return_r_code)
    endpoint = _resolve_endpoint()
    if endpoint:
        if not _check_outbound_authorization(endpoint):
            return None  # AUTH-BLOCK：不发送，调用方提示用户
        envelope = build_batch(specs)
        lang = user_language or _current_locale()
        envelope["return_r_code"] = return_r_code
        envelope["locale"] = lang
        # ct-base coze_io_contract §1.1：user_language 唯一承载位 = 请求 params（顶层不双写）。
        # 批量信封顶层无业务 params（各项自带 build_params 产出的 params），故：
        #   ① 各项 params 的语言统一为批量整体语言 lang（避免逐项 ctx 语言不一致）；
        #   ② 顶层补仅含 user_language 的 params 承载位 —— 批量模式下服务端忽略顶层
        #      params 参与计算（state.py 已注明），仅作契约元数据传递，不引发歧义。
        for item in envelope.get("batch") or []:
            if isinstance(item, dict):
                p = dict(item.get("params") or {})
                p["user_language"] = lang
                item["params"] = p
        envelope["params"] = {"user_language": lang}
        envelope["query_origin"] = _compute_query_origin()
        envelope["skill_version"] = _skill_version()
        # 入口标识（2026-10-07）：skill/workbench，透传飞书 entry_point 列
        envelope["entry_point"] = _ENTRY_POINT
        # ── 请求级日志聚合元数据（批量整包 = 1 次 Coze 请求 = 1 行飞书）──
        envelope.update(_request_meta(call_type))
        # 计费身份标识（ct-base §20.12）：显式参数优先，缺失回退 env；均无 → 免费路径
        if not (account_id or billing_token):
            account_id, billing_token = _billing_from_env()
        attach_billing(envelope, account_id, billing_token)
        # batch 内 params 同样脱敏（剥离 PII）
        envelope["batch"] = sanitize(envelope["batch"])
        try:
            outer = _post(envelope, read_timeout=read_timeout)
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            _reason = getattr(e, "reason", e)
            _is_timeout = (isinstance(e, socket.timeout) or isinstance(_reason, socket.timeout)
                           or "timed out" in str(e).lower() or "timeout" in str(e).lower())
            if _is_timeout:
                raise RuntimeError("COZE_TIMEOUT: coze 批量计算超时（%s，超过 %ss 上限）" % (endpoint, _COMPUTE_TIMEOUT))
            raise RuntimeError("coze 批量调用失败（%s）: %s" % (endpoint, e))
        return _parse_outer(outer)
    raise RuntimeError(
        "coze 端点未配置：请设置 CTSS_COZE_ENDPOINT（真实），"
        "或 CTSS_COZE_MOCK=1（本地演示）。")


def _spec_from_params(test, params, mode="n", user_language=None):
    """把 {test, params, mode} 转成 build_batch 需要的 (test, args, ctx) 三元组。"""
    p = dict(params or {})
    ul = p.get("user_language") or user_language or _current_locale()
    p["user_language"] = ul
    ctx = {
        "solve_for_power": mode == "power",
        "alt": p.get("alt", "two.sided"),
        "d_val": p.get("d_val", p.get("effect")),
        "user_language": ul,
    }
    return (test, SimpleNamespace(**p), ctx)


def call_paired(test, params, return_r_code=True, **kwargs):
    """P1-3：一次 POST 同时给出「所需样本量 n」与「该 n 下的实际把握度」。

    实证：近 30 天 45/45 的 power 调用都在 2 分钟内紧接同检验的 n 调用，
    用户实际是在「算完 n 再验算 power」。旧路径 = 2 次 POST / 2 行飞书 / ~10s；
    paired 模式由服务端在单次请求内连算两向 → 1 次 POST / 1 行飞书。
    """
    kwargs.setdefault("call_type", "paired")
    return call(test, params, "paired", return_r_code, **kwargs)


def call_grid(test, base_params, variants, **kwargs):
    """P1-5：同检验多组参数一次 POST 返回全部（参数扫描 40 次 → 1 次）。

    variants: [{"effect": 0.3, "i2": 0.25}, ...]，每项覆盖 base_params；
    可用 "mode" 指定该项求解方向。返回聚合 agg（含每项完整结果）。
    """
    specs = []
    for v in variants:
        p = dict(base_params or {})
        p.update({k: val for k, val in (v or {}).items() if k != "mode"})
        specs.append(_spec_from_params(test, p, (v or {}).get("mode", "n"),
                                       kwargs.get("user_language")))
    kwargs.setdefault("call_type", "grid")
    return call_batch(specs, **kwargs)


def _mock_batch(specs, return_r_code=True):
    """本地 mock：把多个 _mock_envelope 聚合成 agg_full 形状（演示批量管线，不联网）。"""
    full_results = []
    ok = 0
    err = 0
    for idx, spec in enumerate(specs):
        test = spec[0]
        args = spec[1]
        ctx = spec[2] if len(spec) > 2 else {}
        params = build_params(test, args, ctx or {})
        mode = "power" if (ctx or {}).get("solve_for_power") else "n"
        out = _mock_envelope(test, params, mode, return_r_code)
        st = out.get("status")
        if st in ("ok", "warn"):
            ok += 1
        else:
            err += 1
        full_results.append({"index": idx, "test": test, "mode": mode,
                             "status": st, "out": out})
    return {
        "status": "ok" if err == 0 else ("partial" if ok else "error"),
        "batch": True,
        "count": len(specs),
        "ok": ok,
        "errors": err,
        "results": full_results,
    }


class CozeBackend(ComputeBackend):
    name = "coze"
    # coze 为远程纯计算、无本地副作用 → 不强制 --yes；--dry-run 仍只预览不发送。
    requires_confirmation = False

    def preview(self, test, args, ctx):
        """--dry-run / --show-code 时展示将要发往 coze 的请求信封（脱敏后）。"""
        if not (ctx.get("dry_run") or ctx.get("show_code")):
            return None
        mode = "power" if ctx.get("solve_for_power") else "n"
        params = _trim_bloated_params(test, build_params(test, args, ctx))
        lang = ctx.get("user_language") or _current_locale()
        # ct-base coze_io_contract §1.1：user_language 只进 params，与 call() 实际出站一致
        # （dry-run 预览必须逐字段反映真实请求体，否则预览与实发不一致会误导排查）
        sent_params = _with_user_language(sanitize(params), lang)
        # 计费标记（ct-base §20.12）：与 call() 实发一致——ctx 显式优先、env 兜底
        _acct = (ctx.get("account_id") or None)
        _token = (ctx.get("billing_token") or None)
        if not (_acct or _token):
            _acct, _token = _billing_from_env()
        preview_payload = {
            "endpoint": _resolve_endpoint() or "(mock)",
            "test": test,
            "mode": mode,
            "return_r_code": ctx.get("return_r_code", False),
            "locale": lang,
            "query_origin": _compute_query_origin(),
            "skill_version": _skill_version(),
            # 入口标识（2026-10-07）：skill/workbench，透传飞书 entry_point 列
            "entry_point": _ENTRY_POINT,
            "params": sent_params,
            "resolved_spec": {"test": test, "mode": mode, "params": sent_params},
        }
        # dry-run 预览逐字段反映真实请求体（含聚合元数据），避免预览/实发不一致
        preview_payload.update(_request_meta("preview"))
        attach_billing(preview_payload, _acct, _token)
        return json.dumps(preview_payload, ensure_ascii=False, indent=2)

    def compute(self, test, args, ctx):
        params = build_params(test, args, ctx)
        mode = "power" if ctx.get("solve_for_power") else "n"
        # P3：resolved_spec 契约增强——本次完整语义快照，远端可选消费（补参/校验）。
        resolved_spec = {"test": test, "mode": mode, "params": sanitize(params)}
        # 计费标记（ct-base §20.12）：ctx 显式优先，缺失由 call() 回退 env
        account_id = ctx.get("account_id") or None
        billing_token = ctx.get("billing_token") or None
        env = call(test, params, mode, ctx.get("return_r_code", False),
                   locale=ctx.get("user_language") or _current_locale(),
                   user_language=ctx.get("user_language") or _current_locale(),
                   resolved_spec=resolved_spec,
                   account_id=account_id, billing_token=billing_token,
                   read_timeout=_COMPUTE_TIMEOUT)
        # AUTH-BLOCK：未授权不发送，提示用户（授权不阻断流程）
        if env is None:
            raise RuntimeError(
                "出站未授权：本次未发送到云端计算。"
                "若同意发送，请确认后将端点加入 config/config.json 的 "
                "auto_approve_endpoints（或重跑本命令）。")
        return _envelope_to_result(env, test, ctx)

    def compute_batch(self, specs):
        """v5.7 批量计算：specs = [(test, args, ctx), ...]（与 build_batch 入参一致）。

        返回 BatchResult（items 与 specs 一一对应）。AUTH-BLOCK（call_batch 返回 None）
        抛错提示用户；S3 外置下载失败时聚合摘要仍取自服务端（count/ok/errors/tests/modes），
        缺失 out 的逐项标记为 error（外置数据不可用），不中断整体。"""
        from compute_backend import BatchResult, BatchItem  # 延迟导入，避免循环
        # 取 specs 中首个带 user_language 的作为批量整体语言（coze 端冗余兜底）
        user_language = None
        for spec in specs:
            ctx = spec[2] if len(spec) > 2 else {}
            ul = (ctx or {}).get("user_language")
            if ul:
                user_language = ul
                break
        agg = call_batch(specs, return_r_code=True, user_language=user_language, read_timeout=_COMPUTE_TIMEOUT)
        if agg is None:
            raise RuntimeError(
                "出站未授权：批量请求未发送到云端计算。"
                "若同意发送，请确认后将端点加入 config/config.json 的 "
                "auto_approve_endpoints（或重跑本命令）。")
        if not isinstance(agg, dict):
            raise RuntimeError("coze 批量返回非对象响应")
        results = agg.get("results") if isinstance(agg.get("results"), list) else []
        items = []
        tests = []
        modes = []
        for i, spec in enumerate(specs):
            test = spec[0]
            ctx = spec[2] if len(spec) > 2 else {}
            mode = "power" if (ctx or {}).get("solve_for_power") else "n"
            if test not in tests:
                tests.append(test)
            if mode not in modes:
                modes.append(mode)
            r = results[i] if i < len(results) else None
            if not isinstance(r, dict):
                items.append(BatchItem(index=i, test=test, mode=mode,
                                       status="error", error="批量响应缺失该项结果"))
                continue
            st = r.get("status")
            out = r.get("out") if isinstance(r.get("out"), dict) else None
            if st in ("ok", "warn") and out is not None:
                try:
                    res = _envelope_to_result(out, test, ctx or {})
                    items.append(BatchItem(index=i, test=test, mode=mode,
                                           status=st, result=res))
                except Exception as _e:  # noqa: BLE001 - 单条规整失败不影响其余项
                    items.append(BatchItem(index=i, test=test, mode=mode,
                                           status="error",
                                           error="结果规整失败: %s" % _e))
            elif out is not None:
                # 服务端判定失败但完整 out 信封已返回 → 从信封抽真实错误原因
                # （_envelope_to_result 对 error 信封会抛 RuntimeError，message 即原因）。
                try:
                    _envelope_to_result(out, test, ctx or {})
                except Exception as _e:  # noqa: BLE001
                    items.append(BatchItem(index=i, test=test, mode=mode,
                                           status="error", error=str(_e)))
                else:
                    items.append(BatchItem(index=i, test=test, mode=mode,
                                           status="error",
                                           error="服务端返回状态=%s（无错误明细）" % st))
            else:
                # 仅 inline 摘要可用 / out 缺失（S3 外置下载失败或降级）→ 本地无法产出
                # Result，按渲染失败计为 error；服务端判定 st 与原因写进 error 文本便于溯源。
                srv_err = (r.get("error") if isinstance(r, dict) else None)
                reason = srv_err or "外置完整数据不可用（S3 下载失败/降级）"
                if st and st not in ("ok", "warn"):
                    reason = "%s；服务端判定=%s" % (reason, st)
                items.append(BatchItem(index=i, test=test, mode=mode,
                                       status="error", error=reason))
        # 聚合摘要优先取自服务端（S3 失败时仍准确），本地计算仅兜底
        count = agg.get("count", len(items))
        ok = agg.get("ok", sum(1 for it in items if it.status in ("ok", "warn")))
        errors = agg.get("errors", len(items) - ok)
        status = agg.get("status") or ("ok" if errors == 0
                                       else ("partial" if ok else "error"))
        return BatchResult(status=status, count=count, ok=ok, errors=errors,
                           tests=tests, modes=modes, items=items)


def _envelope_to_result(env, test, ctx):
    """把 coze 返回的信封 dict 规整为跨后端统一的 Result（单请求 / 批量逐项共用）。

    含契约漂移检测 + 结构自适应兼容（ct-base §20.9）、错误/状态判定、字段缺省、
    Figure 列表与 meta 标记组装。异常（非 dict / coze error）直接上抛供调用方处理。
    """
    if not isinstance(env, dict):
        raise RuntimeError("coze 返回非对象响应")
    # ── 契约漂移检测 + 结构自适应兼容（ct-base §20.9 单入口 _assess_contract）──
    # 仅结构/数据内容不一致触发提醒：结构别名自愈兼容，无需比对版本号。
    # 用户可见提示统一只在渲染层 HTML 横幅（_needs_upgrade/_contract_drift 驱动），
    # 不写 stderr、不污染 narrative/notes（零噪音原则）。
    env, drift_notes, needs_upgrade = _assess_contract(env)
    # 自适应兼容：缺字段补默认，保证下游不 KeyError
    env.setdefault("stats", {})
    env.setdefault("narrative", "")
    env.setdefault("figures", [])
    env.setdefault("warnings", [])
    env.setdefault("notes", "")
    env.setdefault("repro", {})
    # 机器可读标记写回信封（rendering 横幅消费；非用户提示）
    env["_needs_upgrade"] = needs_upgrade
    if drift_notes:
        env["_contract_drift"] = drift_notes
    # 契约 §5：coze 出错可返回 {"error": {...}}；原样呈现 message。
    # v5.13.39：err 亦可能是**裸字符串**（实测限流时 coze 返回
    # {"ok": false, "error": "rate_limited"}，经 call() 归一成 {"error": ...}）——
    # 旧代码 err.get("message") 遇 str 直接 AttributeError，把真实错误
    # （rate_limited 限流）吞成栈跟踪。按类型分流，字符串原样呈现。
    err = env.get("error")
    if err:
        if isinstance(err, dict):
            msg = err.get("message") or err.get("code") or "coze 端返回未知错误"
        else:
            msg = str(err) or "coze 端返回未知错误"
        raise RuntimeError("coze 计算失败: %s" % msg)
    status = env.get("status")
    if status in ("error", "unknown_task"):
        raise RuntimeError("coze 计算失败: %s" % (env.get("notes") or status))
    stats = env.get("stats") or {}
    repro = env.get("repro") or {}
    # 截断告警（coze 返回体超 4000 字符、已丢部分 stats 子块；narrative 优先外置故鲜触发）
    truncated = env.get("_coze_truncated")
    text = env.get("narrative", "") or ""
    meta = dict(stats)
    if truncated:
        sys.stderr.write(
            "\n[ct-samplesize] 注意：coze 返回体超 4000 字符，"
            "已截断部分 stats 子块：%s\n" % truncated)
        meta["_coze_truncated"] = truncated
    # 契约漂移标记：透出到 meta（rendering 经 res.meta 读取，写回报告横幅）
    meta["_needs_upgrade"] = needs_upgrade
    if drift_notes:
        meta["_contract_drift"] = drift_notes
    # D3（v5.13.24）：引擎 warnings 通道——此前 env["warnings"] 从未写入 meta，
    # R 引擎的降级提示（如 D1 根治后「随访时间-效能曲线仅支持 survival」、
    # 「热力图需要 curve_n_seq 与 curve_effect_seq」）到不了前端，用户无从知晓
    # 图形为何没出。仅在非空时写入，避免污染 meta。
    eng_warns = env.get("warnings") or []
    # jsonlite auto_unbox：长度 1 的 warnings 会被序列化成字符串而非数组，
    # 直接 list() 会把中文串拆成单字符——此处统一归一为字符串列表。
    if isinstance(eng_warns, str):
        eng_warns = [eng_warns]
    if eng_warns:
        meta["warnings"] = [str(w) for w in eng_warns]
    # 可复现性透传（upgrade J2 措辞修订，2026-09-29）：R 版本 + 包版本进 meta，
    # 供 --justify 渲染 "R <ver> + rpact <ver>/TrialSize <ver>" 式引擎声明
    #（用户口径：只报版本号，不区分云端/本地）。stats 已有同名键时不覆盖。
    if repro.get("r_version") and "r_version" not in meta:
        meta["r_version"] = repro.get("r_version")
    if repro.get("packages") and "packages" not in meta:
        meta["packages"] = repro.get("packages")
    return Result(
        text=text,
        figures=[Figure(f.get("format", "svg"), f.get("content", ""),
                        f.get("caption", "")) for f in env.get("figures", [])],
        r_code=repro.get("r") if ctx.get("return_r_code") else None,
        r_result=stats,
        meta=meta,
        backend="coze",
    )

