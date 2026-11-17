#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_coze_unified.py — 文献检索统一 Coze 客户端（ct-literature 所有文献检索的外发出口）

WHY / 设计动机
─────────────
把 ct-literature 的「本地文献检索」动作外发到 Coze 服务端（轻本地端策略）：
  - OpenAlex / Europe PMC / bioRxiv / medRxiv / Semantic Scholar / arXiv
  - 6 个 source 共用同一端点 ct-search.coze.site/run
  - 服务端用 requests 直连各公共 API，回传结构化检索结果
  - 本地侧（ct_literature.py）做合并去重（normalize.py 保留本地）

向后兼容（100% 保证）：
  - 新增 source 全部是"增量追加"，不修改 Coze 端已有逻辑
  - 本地端 CLI 接口不变，输出格式不变
  - fetch_*.py 完整保留，作为 --offline 兜底
  - Coze 不可用时自动降级到本地 fetch（老版本行为）

飞书日志开关：
  - 中间调用（6 个 source 并行检索）传 log_feishu=False → 不记飞书
  - 最终汇总调用传 log_feishu=True → 只记一条汇总
  - 老版本终端不传此字段 → 默认 True → 行为不变
  - 注意（2026-09-11 修）：log_feishu 只在请求真正到达 Coze 时才生效。而
    dispatch 对「openalex + 本机有 key」会早返回本地直连、对 semantic_scholar
    恒本地化——留痕类调用必须同时传 force_coze=True，否则审计记录被静默吞掉。

mode（2026-09-11 新增）：
  - "search"（默认）：真实检索，Coze 端走 search_node。
  - "log_only"      ：**仅写飞书审计留痕、不做任何检索**。Coze 端 route_by_mode
    据此直连 feishu_write 节点（跳过检索），只为落一条 audit 记录。汇总类调用用它
    取代「借一次真实检索顺手留痕」——不再白跑一次检索、不浪费配额、不污染结果日志。
    log_only 隐含 force_coze=True（留痕必须真正到达 Coze）。CLI：`--log-only`。
    要求 querystr 携带审计内容（否则留痕行没内容可写）。

出站路径分工（2026-10-19 异步化改造）：
  - 快速路径 `/stream_run`（SSE 流式）：socket timeout 钳制
    min(timeout, _STREAM_FAST_PATH_MAX=60s)——只承担 60s 内能完成的轻检索
    （网关 stgw 60s 硬超时内最快、带 SSE 进度；超时主动切换主路径）。
  - 主路径 `/run`（非流式）：响应形态自适应——同步返回直接解析；
    `{status:accepted, run_id}` 异步协议 → 轮询 `/run/status/{run_id}`
    （指数退避 5→30s，总上限 timeout 秒）。重检索（批量 PDF / 深翻页 /
    ICTRP 型长任务）服务端可跑数分钟，同步响应必被网关 60s 掐断，
    只有异步轮询能完整回收（照搬 ct-registry extsvc_client._run_async_poll）。

用法：
  python adapters/fetch_coze_unified.py --source openalex --keyword "osimertinib" --run
  python adapters/fetch_coze_unified.py --source europepmc --keyword "diabetes" --year-from 2020 --run
  python adapters/fetch_coze_unified.py --source biorxiv --keyword "covid" --offline  # 本地兜底
"""
from datetime import datetime
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

# ── 路径设置 ──────────────────────────────────────────────────────────────
_ADAPTERS_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_ADAPTERS_DIR)
_CT_REGISTRY_SKILL = os.path.expanduser("~/.workbuddy/skills/ct-registry")

# 本技能 adapters/ 优先入 path：endpoint_token.py（内嵌公共 token blob）自包含于
# 本技能包（2026-10-13 v1.4.6 修复）——此前仅把 ct-registry/adapters 入 path，
# 云端部署容器无 ct-registry 技能树 → import 失败 → token 为空 → Coze 401
# （线上实测三源 AUTH-BLOCK 修复后仍降级，根因即此）。自包含后本机 / CLI /
# agent / 云端网页端全部署面一致，与 ct-base / ct-advisor「包内各持一份」范式对齐。
if _ADAPTERS_DIR not in sys.path:
    sys.path.insert(0, _ADAPTERS_DIR)

# 兜底：本技能 adapters 无 endpoint_token.py 的老布局，仍尝试 ct-registry
if os.path.isdir(os.path.join(_CT_REGISTRY_SKILL, "adapters")):
    _ctr = os.path.join(_CT_REGISTRY_SKILL, "adapters")
    if _ctr not in sys.path:
        sys.path.insert(1, _ctr)

# 本技能 scripts/ 也入路径：本地兜底模块（fetch_semantic_scholar 等）内部会
# 延迟 `from i18n import t`（i18n.py 在 scripts/ 下）——不经 ct_literature 主流程
# 单独调用 dispatch 时若无此路径即 ModuleNotFoundError（2026-09-06 实测）
_scripts = os.path.join(_SKILL_ROOT, "scripts")
if os.path.isdir(_scripts) and _scripts not in sys.path:
    sys.path.insert(0, _scripts)

# ── 复用 ct-registry 的凭据单一真相源 ─────────────────────────────────────
def _resolve_token() -> str:
    """token 优先级：CLI --token > env CT_REGISTRY_COZE_TOKEN > 内嵌公开 blob。

    复用 ct-registry 的 endpoint_token.py（ct-base §5.236），不重复造轮子。
    """
    # 1) CLI --token（由 argparse 注入）
    cli_tok = getattr(_resolve_token, "_cli_token", None)
    if cli_tok:
        return cli_tok
    # 2) env
    env_tok = os.environ.get("CT_REGISTRY_COZE_TOKEN") or os.environ.get("ICTRP_WORKFLOW_TOKEN")
    if env_tok:
        return env_tok
    # 3) 内嵌公开 blob
    try:
        from endpoint_token import get_token as _gt
        return _gt() or ""
    except Exception:
        return ""


def _has_openalex_key() -> bool:
    """本地是否配置 OpenAlex API key（env OPENALEX_API_KEY / 技能根 .env）。

    有 key → dispatch 把 openalex 路由到本地直连（keyed pool 100k credits/天）；
    无 key → 仍走 Coze 匿名池（openalex 匿名可用，非 S2 那种必 429，无需跳过）。
    复用 http_utils.load_openalex_key 保证与 fetch_openalex 离线路径 key 一致。
    """
    try:
        sys.path.insert(0, _ADAPTERS_DIR)
        from adapters import http_utils
        return bool(http_utils.load_openalex_key())
    except Exception:
        return bool(os.environ.get("OPENALEX_API_KEY"))


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    tok = _resolve_token()
    if tok:
        h["Authorization"] = "Bearer " + tok
    return h


def _query_origin() -> str:
    """稳定机器标识（sha256 哈希，不可逆）。"""
    return "sha256:" + hashlib.sha256(os.environ.get("COMPUTERNAME", "unknown").encode()).hexdigest()


# ── 入口标识 entry_point（ct-base coze_io_contract §1.3 / §2.3 · 2026-10-07）─────
# 区分「调用来源」：技能本身（"skill"）vs 工作台 Web 应用（"workbench"）vs 未来
# 第三方 API（"api"）。透传写入飞书**独立列** entry_point，供后台按来源直切筛选。
#
# 与 query_origin 的区别（🔴 不得混用）：query_origin 按**机器**（COMPUTERNAME 哈希）
# 同一台机器上 skill / workbench 算出的哈希逐字节相同 → 无法区分界面来源。
# 进程启动期初值来源（2026-10-13 修复）：环境变量 CT_ENTRY_POINT。
# ct-literature 工作台是 Popen(ct_literature.py) 子进程架构——真正向 coze 发请求的是
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


def set_entry_point(value) -> None:
    """覆盖进程级入口标识（工作台进程启动期调用以标记 workbench）。

    agent / 技能进程**不import** 工作台模块 → 两进程全局值天然隔离、无污染。
    空值 / 空白 / 非法值一律回退 "skill"，绝不写出 None 或脏值（§1.3）。
    """
    global _ENTRY_POINT
    v = (value or "").strip() if isinstance(value, str) else ""
    _ENTRY_POINT = v if v in _ENTRY_POINT_WHITELIST else "skill"


def entry_point() -> str:
    """当前进程级入口标识（永不为 None / 空串）。"""
    return _ENTRY_POINT or "skill"


# ── 端点 ──────────────────────────────────────────────────────────────────
# 主路径 /stream_run（SSE 流式）：2026-09-06 改流式，与 PDF 通道同源 SSE 架构，
# 避免长检索被网关按单响应超时掐断；流式无结果自动回退 /run（CT_SEARCH_ENDPOINT）。
# 2026-10-19 降级为「快速路径」：socket timeout 钳制 60s（见 _STREAM_FAST_PATH_MAX），
# 只承担 60s 内能完成的轻检索；超过即主动切换 /run 主路径（同步/异步自适应）。
CT_SEARCH_ENDPOINT_STREAM = os.environ.get("CT_SEARCH_ENDPOINT_STREAM", "https://ct-search.coze.site/stream_run")
# 回退路径 /run（非流式，旧默认）：stream 无结果/超时/被拒时启用；
# 2026-10-19 起为主路径——同步返回直接解析，accepted+run_id 异步协议轮询回收。
CT_SEARCH_ENDPOINT = os.environ.get("CT_SEARCH_ENDPOINT", "https://ct-search.coze.site/run")

# ── stream 快速路径上限（2026-10-19 异步化改造） ────────────────────────────
# Coze 云端网关 stgw 对 HTTP 请求有 60s 硬超时（ct-base §20.17.1 实测 60.0s 整
# 504，流式同样被杀——不是逃生通道）。把 stream 的 socket timeout 钳到 60s：
# 60s 内能完成的轻检索走 SSE（最快、带进度），到点主动切换 /run 主路径
# （同步解析 / accepted+run_id 异步轮询自适应），不在必死的连接上干等。
_STREAM_FAST_PATH_MAX = float(os.environ.get("CT_SEARCH_STREAM_TIMEOUT", "60"))

# 支持的 source 集合（与 Coze 端 sources.py 同步）
DISPATCHABLE_SOURCES = frozenset({
    "openalex",
    "europepmc",
    "pubmed",           # 2026-11-04 S5：Coze 0.3.97 已上线 pubmed_node
    "biorxiv",
    "medrxiv",
    "semantic_scholar",
    "arxiv",
})

# Coze 端小写 source → 本地规范显示名（与 fetch_*.py 返回的 source 一致；
# 保证下游 normalize / hit_count 等按 source 判断的逻辑不受大小写影响）
_SOURCE_DISPLAY = {
    "openalex": "OpenAlex",
    "europepmc": "EuropePMC",
    "pubmed": "PubMed",
    "biorxiv": "bioRxiv",
    "medrxiv": "medRxiv",
    "semantic_scholar": "SemanticScholar",
    "arxiv": "arXiv",
}


def _display_source(source: str) -> str:
    """Coze 小写 source → 本地规范显示名（未知源原样返回）。"""
    return _SOURCE_DISPLAY.get(source, source)


# ── Coze 侧文本兜底清洗 ────────────────────────────────────────────────────
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t]{2,}")


def _sanitize_text(s):
    """Strip residual HTML tags from a Coze-side text field (<h4>, <i>, …).

    WHY: Europe PMC serves structured abstracts (Purpose / Methods / Results headings)
    as HTML. The local EuropePMC fetcher strips them via its own `_strip_html`, but the
    Coze server-side node passes raw `<h4>…</h4>` through — 2026-09-08 measurement:
    18/56 merged works had tag residue on the `--online` path vs 0/56 locally. Cleaning
    at the Coze egress equalizes both paths. Idempotent: once the Coze node also strips,
    this becomes a no-op.
    """
    if not isinstance(s, str) or "<" not in s:
        return s
    s = _TAG_RE.sub(" ", s)
    return _WS_RE.sub(" ", s).strip()


def _sanitize_works(works):
    """Apply `_sanitize_text` to every work's title / abstract_snippet."""
    if not isinstance(works, list):
        return works
    for w in works:
        if isinstance(w, dict):
            for k in ("title", "abstract_snippet"):
                if isinstance(w.get(k), str):
                    w[k] = _sanitize_text(w[k])
    return works

# 技能版本号回退常量
_SKILL_VERSION_FALLBACK = "0.9.7"


def _skill_version() -> str:
    """技能版本号：优先读技能根 SKILL.md frontmatter 的 `version:`（单一事实来源）。"""
    try:
        skill_md = os.path.join(_SKILL_ROOT, "SKILL.md")
        with open(skill_md, encoding="utf-8") as f:
            head = f.read(4000)
        m = re.search(r"^version:\s*([0-9][\w.\-]*)", head, re.M)
        if m:
            return m.group(1)
    except Exception:
        pass
    return _SKILL_VERSION_FALLBACK


def _resolve_locale() -> str:
    """界面 / 输出语言（zh/en）—— 顶层信封 `locale` 字段。"""
    try:
        sys.path.insert(0, os.path.join(_SKILL_ROOT, "scripts"))
        import i18n as _i18n
        lang = (_i18n._current_lang() or "").lower()
        if lang.startswith("zh"):
            return "zh"
        if lang.startswith("en"):
            return "en"
    except Exception:
        pass
    return "zh"


# ── 出站授权门（ct-base §5.212）──────────────────────────────────────────
# config.json 存放「出站授权白名单」，含作者私有 coze 端点（ct-search /
# ct-bugreport），属本机运行态配置，不随技能发布包公开。2026-09-06 起移出
# 技能树，置于 ~/.workbuddy/ct-literature-runtime/。解析优先级：
#   1) env CT_LIT_RUNTIME_DIR 指定目录
#   2) 默认 ~/.workbuddy/ct-literature-runtime/config/config.json
#   3) 技能树内 config/config.json（兜底，兼容旧布局 / 包内默认）
_SESSION_AUTHORIZED = set()
_RUNTIME_DIR = os.environ.get("CT_LIT_RUNTIME_DIR") or os.path.join(
    os.path.expanduser("~"), ".workbuddy", "ct-literature-runtime")

# 2026-10-13：部署包内置公开端点白名单（授权门兜底放行）。
# ct-search / ct-bugreport 的 /run 是作者公开端点（token 为嵌入式公共 token，
# 2026-08-18 授权），授权门语义只防「未经同意外发到私有端点」。云端部署面
# （publish 容器）home 无 runtime config.json、发布包亦不随带（避免公开
# 私有端点），曾致 europepmc / biorxiv / medrxiv 三源全部 AUTH-BLOCK 降级
# 本地 fetch。公开端点在所有部署面（本机 / CLI / agent / 云端网页端）一律
# 放行，与「私有端点须显式授权」不冲突；env CT_SEARCH_ENDPOINT 覆盖为其他
# 端点时仍走 config 授权，原语义不变。
_BUILTIN_PUBLIC_ENDPOINTS = frozenset({
    "https://ct-search.coze.site/run",
    "https://ct-bugreport.coze.site/run",
})


def _config_candidates():
    cands = []
    if os.environ.get("CT_LIT_RUNTIME_DIR"):
        cands.append(os.path.join(os.environ["CT_LIT_RUNTIME_DIR"], "config", "config.json"))
    cands.append(os.path.join(_RUNTIME_DIR, "config", "config.json"))
    cands.append(os.path.join(_SKILL_ROOT, "config", "config.json"))  # 兜底
    return cands


def _check_outbound_authorization(endpoint: str) -> bool:
    """出站授权检查：已授权 → True；未授权 → 返回 False（由调用方提示用户）。

    脚本只发 [AUTH-BLOCK] 信号，绝不自行修改 config.json。config 解析按
    _config_candidates() 多候选回退，确保移出技能树后仍能在运行态目录命中。
    公开端点白名单（_BUILTIN_PUBLIC_ENDPOINTS）优先放行——云端部署面无
    runtime config，见常量处注释（2026-10-13）。
    """
    if endpoint in _BUILTIN_PUBLIC_ENDPOINTS:
        return True
    if endpoint in _SESSION_AUTHORIZED:
        return True
    for path in _config_candidates():
        try:
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    cfg = json.load(f)
                if endpoint in cfg.get("auto_approve_endpoints", []):
                    _SESSION_AUTHORIZED.add(endpoint)
                    return True
        except Exception:
            continue
    return False


# ── 本地兜底（--offline / Coze 不可用）──────────────────────────────────
def _offline_fallback(source: str, keyword: str, year_from: int = None,
                      year_to: int = None, max_results: int = 50,
                      date_from: str = None, date_to: str = None,
                      cochrane: bool = False) -> Optional[Dict]:
    """Coze 不可用时的本地兜底：调用原有的 fetch_*.py 模块。

    返回格式与 Coze 端一致：{"total_count": N, "projects": [...]}
    本地 fetch 模块返回 {"source": "...", "works": [...], "count": N}，
    需转换为 Coze 格式。

    `cochrane` 只在本地兜底路径生效（OpenAlex ISSN 过滤 / Europe PMC 期刊过滤）：
    Coze 云端没有对应过滤器，所以 online 路径下客户端二次过滤是唯一执行点。
    """
    try:
        result = None
        if source == "openalex":
            from adapters import fetch_openalex
            result = fetch_openalex.fetch(keyword, year_from=year_from, max_results=max_results,
                                          run=True, cochrane=cochrane)
        elif source == "europepmc":
            from adapters import fetch_europepmc
            result = fetch_europepmc.fetch(keyword, year_from=year_from, max_results=max_results,
                                           run=True, cochrane=cochrane)
        elif source in ("biorxiv", "medrxiv"):
            from adapters import fetch_preprints
            server = "medrxiv" if source == "medrxiv" else "biorxiv"
            result = fetch_preprints.fetch(keyword, server=server, year_from=year_from, max_results=max_results, run=True)
        elif source == "semantic_scholar":
            from adapters import fetch_semantic_scholar
            result = fetch_semantic_scholar.fetch(keyword, year_from=year_from, max_results=max_results, run=True)
        elif source == "arxiv":
            from adapters import fetch_arxiv
            result = fetch_arxiv.fetch(keyword, year_from=year_from, max_results=max_results, run=True)
        elif source == "pubmed":
            # 2026-11-04 S5：Coze 不可用时的 R1 本地降级（§20.19.7 红线 2：
            # 不取消本地引擎）。此前缺这个分支，切路由后降级会静默退化为空结果。
            from adapters import fetch_pubmed
            result = fetch_pubmed.fetch(keyword, year_from=year_from,
                                        max_results=max_results, run=True,
                                        cochrane=cochrane,
                                        date_from=date_from, date_to=date_to)

        if result is None:
            return None

        # 统一为本地格式（与 Coze 成功路径一致）：{"source": 规范名, "count", "works"}
        # source 用规范大写；本地 fetch 模块本就返回规范名，此处 display 映射兜底。
        works = result.get("works", [])
        # 路线 B：本地兜底结果同样按日期窗口裁剪（各 fetch 走 year 级拉取，
        # 此处统一 clip 保证窗口正确；原生支持 date 的源已在 fetch 内过滤）。
        works, _dw = clip_by_date_window(works, date_from, date_to, source)
        _log_date_window(source, _dw, date_from, date_to)
        return {
            "source": _display_source(result.get("source") or source),
            "count": result.get("count", len(works)),
            "works": works,
            "total_count": result.get("count", len(works)),
        }
    except Exception as e:
        print(f"[offline_fallback] {source} 本地兜底失败: {e}", file=sys.stderr)
    return None


# ── SSE 流式解析（与 PDF 通道同源）──────────────────────────────────────────
def _silent_log(msg):
    """流式解析用的静默日志（dispatch 主路径不需要逐事件打屏）。"""
    return


def _fetch_s3_projects(s3_url, log_fn=_silent_log, timeout=60):
    """回参超长外置时，从 S3 拉回真实 projects。

    ct-search 在结果集过大时把 projects 外置到 S3，只在 output 里回
    `s3_url` + 空 projects。**必须回拉**，否则会把「有结果」误判成「0 篇」。
    与 pdf_download._parse_coze_stream 的 s3 分支同构。
    """
    log_fn("[coze] 回参超长，从 S3 拉取结果: %s" % s3_url)
    req = urllib.request.Request(s3_url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    pl = json.loads(raw.decode("utf-8"))
    if isinstance(pl, str):
        pl = json.loads(pl)
    if isinstance(pl, dict) and isinstance(pl.get("projects"), list):
        return pl["projects"]
    return None


def _parse_stream(resp, log_fn=_silent_log):
    """解析 Coze stream_run 的 SSE 流，提取检索结果 projects 列表。

    主路径复用本技能树内的 adapters/pdf_download._parse_coze_stream（同源实现，
    含 node_end 回退 + s3 外置回拉）。该模块**确实存在于 ct-literature 技能树内**
    （这与 ct-safety 不同——后者树内无此文件，import 必失败而降级到弱解析器，
    见 ct-safety v0.9.14 CHANGELOG）。

    此处的兜底降级路径仍保留，因为它必须能独立正确工作——不能依赖「主路径一定
    成功」。故 _parse_stream_local 已与 pdf_download 解析能力对齐（node_end 回退、
    三种嵌套形态、s3 外置回拉），避免一旦降级就退化为「只认projects 键」而误判
    无结果 → 回退 /run → 双发。
    """
    try:
        if _SKILL_ROOT not in sys.path:
            sys.path.insert(0, _SKILL_ROOT)
        from adapters.pdf_download import _parse_coze_stream
        return _parse_coze_stream(resp, log_fn)
    except Exception:
        return _parse_stream_local(resp, log_fn)


def _parse_stream_local(resp, log_fn=_silent_log):
    """最小 SSE 解析兜底（仅当无法复用 pdf_download 时启用）。"""
    events = []
    buf = b""
    for chunk in resp:
        buf += chunk
        while b"\n" in buf:
            line_b, buf = buf.split(b"\n", 1)
            line = line_b.decode("utf-8", "ignore").rstrip("\r")
            if line.startswith("data:"):
                ds = line[len("data:"):].lstrip()
                if ds and ds != "[DONE]":
                    try:
                        events.append(json.loads(ds))
                    except Exception:
                        pass
    if not events:
        try:
            events.append(json.loads(buf.decode("utf-8", "ignore")))
        except Exception:
            return None

    # 结果提取优先级（与 pdf_download._parse_coze_stream 对齐）：
    #   workflow_end.output（有真实结果）→ 最后一个含真实结果的 node_end.output
    #   → 含 projects/project_list 的事件。Coze「Output 变量未绑定」时
    #   workflow_end.output 为 {}，真结果只在 node_end。
    def _dig_output(node):
        if not isinstance(node, dict):
            return None
        out = node.get("output")
        if out is None and isinstance(node.get("data"), dict):
            out = node["data"].get("output")
        if (out is None and isinstance(node.get("data"), dict)
                and isinstance(node["data"].get("data"), dict)):
            out = node["data"]["data"].get("output")
        return out

    def _has_real_output(o):
        if isinstance(o, dict):
            return any(k in o for k in ("projects", "project_list", "s3_url",
                                        "status", "total_count"))
        if isinstance(o, str):
            try:
                d = json.loads(o)
            except Exception:
                return bool(o) and "[DONE]" not in o
            return isinstance(d, dict) and any(
                k in d for k in ("projects", "project_list", "s3_url",
                                 "status", "total_count"))
        if isinstance(o, list):
            return len(o) > 0
        return False

    workflow_end_out = None
    node_outputs = []
    for evt in events:
        if not isinstance(evt, dict):
            continue
        inner = evt.get("data")
        node = inner if (isinstance(inner, dict) and inner.get("type")) else evt
        etype = node.get("type") or evt.get("type")
        if etype == "workflow_end":
            workflow_end_out = _dig_output(node)
        elif etype == "node_end":
            o = _dig_output(node)
            if o is not None:
                node_outputs.append(o)

    final = None
    if _has_real_output(workflow_end_out):
        final = workflow_end_out
    else:
        for o in reversed(node_outputs):
            if _has_real_output(o):
                final = o
                break
        if final is None and node_outputs:
            final = node_outputs[-1]
    if final is None:
        for evt in reversed(events):
            if isinstance(evt, dict) and ("projects" in evt or "project_list" in evt):
                final = evt
                break
    if final is None:
        return None
    if isinstance(final, str):
        try:
            final = json.loads(final)
        except Exception:
            return None
    if not isinstance(final, dict):
        return None
    projects = final.get("projects")
    if isinstance(projects, list):
        if projects:
            return projects
        # 空列表：若带 s3_url 说明回参超长外置，须回拉真实数据；
        # 否则就是「确实 0 篇」。
        s3 = final.get("s3_url")
        if s3:
            try:
                return _fetch_s3_projects(s3, log_fn)
            except Exception as e:
                log_fn("[coze] S3 结果拉取失败: %s" % e)
                return None
        return []
    pl = final.get("project_list")
    s3 = final.get("s3_url")
    if pl is None and s3:
        try:
            pl = _fetch_s3_projects(s3, log_fn)
        except Exception as e:
            log_fn("[coze] S3 结果拉取失败: %s" % e)
            return None
    if pl is not None:
        if isinstance(pl, str):
            try:
                pl = json.loads(pl)
            except Exception:
                return None
        if isinstance(pl, dict):
            p = pl.get("projects")
            if isinstance(p, list):
                if not p and pl.get("s3_url"):
                    try:
                        return _fetch_s3_projects(pl["s3_url"], log_fn)
                    except Exception as e:
                        log_fn("[coze] S3 结果拉取失败: %s" % e)
                        return None
                return p
            if pl.get("s3_url"):
                try:
                    return _fetch_s3_projects(pl["s3_url"], log_fn)
                except Exception as e:
                    log_fn("[coze] S3 结果拉取失败: %s" % e)
                    return None
    return None


def _parse_run_response(data, source):
    """解析 /run（非流式）返回体 → 本地统一格式 {"source","works","count","total_count"}。"""
    if isinstance(data, list):
        # /run 对留痕类调用（末尾飞书汇总等）直接返回 JSON 数组而非对象——
        # 此前 data.get(...) 直接 AttributeError，汇总整条丢失（2026-10-23 修复）。
        return {"source": _display_source(source), "works": data,
                "count": len(data), "total_count": len(data)}
    if not isinstance(data, dict):
        return {"source": _display_source(source), "works": [],
                "count": 0, "total_count": 0}
    if isinstance(data.get("project_list"), str):
        try:
            pl = json.loads(data["project_list"])
            if isinstance(pl, list):
                # project_list 解码后是数组（留痕/汇总类返回形态）——此前 pl.get 直接
                # AttributeError，整条汇总丢失（2026-10-23 修复）。
                return {
                    "source": _display_source(source),
                    "count": len(pl),
                    "works": pl,
                    "total_count": len(pl),
                }
            works = pl.get("projects", [])
            return {
                "source": _display_source(source),
                "count": pl.get("total_count", len(works)),
                "works": works,
                "total_count": pl.get("total_count", len(works)),
            }
        except (json.JSONDecodeError, TypeError):
            pass
    if "projects" in data and "works" not in data:
        data["works"] = data.pop("projects")
        data["count"] = data.get("total_count", len(data["works"]))
    _sanitize_works(data.get("works"))
    data["source"] = _display_source(source)
    return data


def _coze_stream_once(body, timeout):
    """单次 /stream_run 请求 + SSE 解析；返回 projects(list) 或 None（无结果/被拒），异常上抛。"""
    req = urllib.request.Request(CT_SEARCH_ENDPOINT_STREAM, data=body, headers=_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return _parse_stream(resp, _silent_log)


def _coze_async_poll(endpoint, run_id, timeout):
    """异步协议：轮询 {endpoint_base}/run/status/{run_id}（照搬 ct-registry
    adapters/extsvc_client._run_async_poll，改 stdlib urllib 零依赖）。

    背景：ct-search 统一端点对重检索任务（批量 PDF / 深翻页 / ICTRP 型长任务）
    返回 `{status:"accepted", run_id}` 而非同步结果——服务端还要跑数分钟，
    同步响应必被网关 60s 掐断。此前客户端不识别该协议，把 accepted 信封当
    同步响应对待 → project_list 缺失 → 空结果（2026-10-19 修复）。

    轮询策略（与 extsvc_client 对齐）：
      - 指数退避：首轮 5s，逐轮 ×2 封顶 30s；总上限 timeout 秒；
      - 轮询 GET 为短请求：单次网络抖动 / 单次超时 / 404（最终一致性窗口）
        均续轮，不废弃服务端任务；401/403 鉴权问题立即失败（重试无意义）；
      - 终态 completed → data["result"] 或 data 本体（交调用方
        _parse_run_response + clip_by_date_window，与 /run 同步路径同口径）；
        failed/cancelled → {"error": ...}（不静默）；到期 → {"error": timeout}。

    返回 dict：completed 时为最终 result payload；失败/到期为 {"error": msg}。
    """
    base = endpoint.rsplit("/run", 1)[0].rstrip("/")
    status_url = "%s/run/status/%s" % (base, run_id)
    headers = _headers()

    deadline = time.time() + timeout
    wait = 5.0
    while time.time() < deadline:
        try:
            req = urllib.request.Request(status_url, method="GET", headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                print("[Coze] Token 无效或已过期，请通过 --token 或 env CT_REGISTRY_COZE_TOKEN 重新设置",
                      file=sys.stderr)
                return {"error": f"HTTP {e.code} (poll /run/status)",
                        "message": "token rejected during async poll"}
            # 404（最终一致性窗口）/ 其它 5xx（网关抖动）：续轮等终态
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        except Exception:
            # 连接抖动 / 单次超时：服务端任务不受影响，续轮（deadline 兜底）
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        status = data.get("status")
        if status == "running":
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        if status == "failed":
            print(f"[Coze] 异步检索失败（run_id={run_id}）: {data.get('error')}", file=sys.stderr)
            return {"error": "remote run failed", "message": str(data.get("error"))[:500]}
        if status == "cancelled":
            print(f"[Coze] 异步检索被取消（run_id={run_id}）", file=sys.stderr)
            return {"error": "remote run cancelled", "run_id": run_id}
        # completed（或 status 缺失的兜底）：最终结果两种形态
        #  (a) 平台已重命名：{"status", "result": {...}}
        #  (b) 直接是 result dict
        print(f"[Coze] 异步检索完成（run_id={run_id}，轮询回收）", file=sys.stderr)
        return data.get("result", data)
    return {"error": f"timeout after {timeout}s (poll /run/status)",
            "message": "Coze 异步检索超过等待上限；数据可能不全：建议缩小关键字 / 换其他源交叉验证",
            "run_id": run_id}


# ── 统一外发检索 ──────────────────────────────────────────────────────────
# ── 月份级日期窗口裁剪（路线 B · 2026-10-12）────────────────────────────
def _parse_ymd(s):
    """YYYY-MM-DD (or longer ISO) → datetime.date；缺失/非法 → None。"""
    if not s:
        return None
    s = str(s)[:10]
    if len(s) == 10 and s[4] == "-" and s[7] == "-":
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return None
    return None


def clip_by_date_window(works, date_from=None, date_to=None, source=""):
    """月份级日期窗口裁剪（online/Coze 通道与 run() 合并兜底共用）。

    规则：
      - publication_date 有效 → 精确比较 [date_from, date_to]，越界丢弃；
      - publication_date 缺失/空 → 回退 year 粗兜底：
          year < date_from.year 或 year > date_to.year → 丢弃；
          year 落在边界年内（无法判月）→ 保守保留（计 year_fallback）；
      - year 也没有 → 保守保留（计 no_date，交由下游/用户判断）。
    返回 (kept_works, stats)；stats = {"dropped":n, "year_fallback":m, "no_date":k}。

    WHY year 兜底：实测 Coze 端 europepmc 节点不填 publication_date（返回空串），
    仅靠精确日期会漏砍该源的老文；用 year 先砍掉明显跨年的超窗文献，边界年内
    保守保留（宁多勿漏，交由周报人工判断）。europepmc 精滤需云端工作流升级
    （消费 date 参数 + 填 publication_date），见 SKILL.md 路线 B 说明。
    """
    if not (date_from or date_to) or not isinstance(works, list):
        return works, {"dropped": 0, "year_fallback": 0, "no_date": 0}
    df = _parse_ymd(date_from) if date_from else None
    dt = _parse_ymd(date_to) if date_to else None
    df_year = df.year if df else None
    dt_year = dt.year if dt else None
    kept, dropped, year_fb, no_date = [], 0, 0, 0
    for w in works:
        if not isinstance(w, dict):
            kept.append(w)
            continue
        wd = _parse_ymd(w.get("publication_date") or "")
        if wd is not None:
            if df and wd < df:
                dropped += 1
                continue
            if dt and wd > dt:
                dropped += 1
                continue
            kept.append(w)
            continue
        # 缺精确日期 → year 粗兜底
        yr = w.get("year")
        try:
            yr = int(yr) if yr is not None else None
        except Exception:
            yr = None
        if yr is None:
            no_date += 1
            kept.append(w)  # 无年份：保守保留
            continue
        if df_year and yr < df_year:
            dropped += 1
            continue
        if dt_year and yr > dt_year:
            dropped += 1
            continue
        year_fb += 1
        kept.append(w)  # 边界年内，无法判月：保守保留
    return kept, {"dropped": dropped, "year_fallback": year_fb, "no_date": no_date}


def _log_date_window(source, stats, date_from, date_to):
    """date-window 裁剪日志（仅在有丢弃或 year 兜底时打，避免噪音）。"""
    if stats["dropped"] or stats["year_fallback"]:
        print("[coze date-window] %s: dropped=%d year_fallback=%d no_date=%d "
              "(window [%s, %s])"
              % (source, stats["dropped"], stats["year_fallback"],
                 stats["no_date"], date_from, date_to), file=sys.stderr)


def dispatch(source: str, keyword: str, year_from: int = None, year_to: int = None,
             max_results: int = 50, run: bool = False, log_feishu: bool = True,
             timeout: int = 300, offline: bool = False,
             querystr: str = None, skillname: str = None,
             force_coze: bool = False, mode: str = "search",
             date_from: str = None, date_to: str = None,
             cochrane: bool = False,
             request_id: str = None) -> Optional[Dict]:
    """统一外发检索，返回结构化结果。

    Args:
        source: 数据源（openalex/europepmc/pubmed/biorxiv/medrxiv/
                semantic_scholar/arxiv）
        keyword: 检索词（英文）。pubmed 源会先经本地 fetch_pubmed._build_query()
                 构造完整检索式再外发（Coze 节点不自行拼子句，§6.3）。
        year_from: 起始年份
        year_to: 截止年份
        max_results: 每源最大返回数
        run: 是否实际执行网络请求（False = 仅预览 payload）
        log_feishu: 是否记飞书（中间调用=False，最终汇总=True）
        timeout: HTTP 超时秒数
        offline: 强制本地兜底（不调 Coze）
        querystr: 审计 querystr JSON 字符串（透传飞书 querystr 列；None 则不携带）。
            🔴 版本字段（skill_version / coze_version）**不得**放进这里——§2.1（2026-09-17 定）
            规定版本字段唯一落点是飞书 resultstr（由 coze 端写入）；客户端只需按 §1.2
            发顶层信封 `skill_version`，不要在本参数内重复携带。
        skillname: 飞书审计 skillname 覆盖（None=Coze 端按 source 推导）
        force_coze: 强制走 Coze，跳过「本地直连」早返回（openalex 有 key /
            semantic_scholar 本地化）。用于**留痕类调用**——这类调用必须真正到达
            Coze 端，否则 `log_feishu` 被本地路由静默吞掉、审计记录丢失。
            默认 False（保持既有的本地优先行为不变）。
        mode: 工作模式，透传到 Coze 端 `mode` 字段。默认 `"search"`（真实检索）。
            `"log_only"` = **仅写飞书审计留痕、不做任何检索**（Coze 端 route_by_mode
            据此直连 feishu_write 节点）——这类调用没有任何检索结果可返回，`source`
            只用于保持既有签名兼容，不产生实际检索。log_only 隐含 force_coze=True：
            留痕调用必须真正到达 Coze，否则记录丢失。（2026-09-11 新增）
        cochrane: CDSR-only 车道开关。**仅在本地兜底路径生效**（OpenAlex ISSN 过滤 /
            Europe PMC 期刊过滤）。Coze 云端当前没有对应过滤器，online 路径下
            客户端二次过滤是唯一执行点——调用方需自行就「未推送」告警。

    Returns:
        {"source": 规范名, "works": [...], "count": N, "total_count": N} 或 None（预览模式）
    """
    if source not in DISPATCHABLE_SOURCES:
        raise ValueError(f"unsupported source: {source}. Must be one of {sorted(DISPATCHABLE_SOURCES)}")

    # log_only 是纯留痕调用：必须真正送达 Coze，否则飞书那条记录就没了。
    # 在此强制打开 force_coze，避免调用方忘记传而被打包进「本地直连」早返回。
    if mode == "log_only":
        force_coze = True

    # Semantic Scholar 本地化（用户决策 2026-09-06）：有 key 用户走本地直连，
    # 不经过 Coze——私人 key 零传递最安全，本地 fetch_semantic_scholar.py 本就支持
    # key（1 RPS 专属）；无 key 本地模块自行跳过（与老版本一致）。Coze 端
    # semantic_scholar_node 仅服务无本地检索能力的调用方（无 key 时跳过）。
    # force_coze=True 时跳过此早返回（留痕类调用必须到 Coze）。
    if source == "semantic_scholar" and not force_coze:
        if not run:
            print(json.dumps({
                "source": source, "mode": "local", "note": "semantic_scholar 本地直连（有 key 用户，不经 Coze）",
                "keyword": keyword, "max_results": max_results}, ensure_ascii=False, indent=2))
            return None
        return _offline_fallback(source, keyword, year_from, year_to, max_results,
                                 date_from=date_from, date_to=date_to, cochrane=cochrane)

    # OpenAlex 本地化（用户决策 2026-09-06，方案 B 同 S2 原则）：有 key 用户本地直连
    # 不经过 Coze——key 零传递 + 进 keyed pool（100k credits/天，无 429），本地
    # fetch_openalex.py 经 build_openalex_headers 带 mailto polite-pool + Bearer key。
    # 无 key 仍走 Coze（openalex_node 匿名池可用，与 S2"无 key 必 429"不同，不需跳过）。
    # force_coze=True 时跳过此早返回：留痕类调用（如末尾飞书汇总，log_feishu=True）
    # 必须真正到达 Coze，否则被本地路由吞掉、审计记录静默丢失（2026-09-11 修）。
    if source == "openalex" and _has_openalex_key() and not force_coze:
        if not run:
            print(json.dumps({
                "source": source, "mode": "local", "note": "openalex 本地直连（有 key 用户，keyed pool，不经 Coze）",
                "keyword": keyword, "max_results": max_results}, ensure_ascii=False, indent=2))
            return None
        return _offline_fallback(source, keyword, year_from, year_to, max_results,
                                 date_from=date_from, date_to=date_to, cochrane=cochrane)

    # 本地兜底
    if offline:
        return _offline_fallback(source, keyword, year_from, year_to, max_results,
                                 date_from=date_from, date_to=date_to, cochrane=cochrane)

    # 2026-11-04 S5：pubmed 是唯一「节点不自行拼子句」的源（Coze
    # literature_nodes.pubmed_node 直接把 state.keyword 当完整检索式）。
    # ct-literature 主链路调用方传的是裸主题词，若直接外发会丢掉 pt / 日期 /
    # Cochrane 过滤 → 语义退化。故在此用本地 fetch_pubmed._build_query() 把子句
    # 编进检索式，保证切到 Coze 后语义不变（§6.3：检索式构造留本地，节点只执行）。
    # 构造失败退回裸词：节点仍可执行，最坏只少一层过滤，绝不中断流程。
    _coze_keyword = keyword
    if source == "pubmed":
        try:
            from adapters import fetch_pubmed as _fp
            _coze_keyword = _fp._build_query(
                keyword, cochrane=cochrane, year_from=year_from,
                year_to=year_to, date_from=date_from, date_to=date_to)
        except Exception:
            _coze_keyword = keyword

    # 构造 payload
    payload = {
        "source": source,
        # mode 由调用方决定："search"（默认，真实检索）/ "log_only"（仅写飞书留痕，
        # Coze 端 route_by_mode 直连 feishu_write，跳过检索节点）。
        "mode": mode,
        "keyword": _coze_keyword,
        "max_results": max_results,
        "log_feishu": log_feishu,
        "query_origin": _query_origin(),
        "skill_version": _skill_version(),
        # ct-base coze_io_contract §1.3/§2.3：entry_point 顶层信封字段，
        # 写入飞书独立列 entry_point（不并入 resultstr / querystr）。
        "entry_point": entry_point(),
        "locale": _resolve_locale(),
        "params": {"user_language": _resolve_locale()},
    }
    if year_from:
        payload["year_from"] = year_from
    if year_to:
        payload["year_to"] = year_to
    # 路线 B：月份级日期窗口透传 Coze 端。云端（ct-registry/adapters/coze
    # coze_version 0.3.94，2026-10-13）GraphInput/GlobalState/SearchNodeInput
    # 三模型已声明 lit_date_from/lit_date_to，literature_nodes 五节点原生过滤
    # （OpenAlex from/to_publication_date；Europe PMC/预印本 FIRST_PDATE 子句；
    # arXiv submittedDate；S2 publicationDateOrYear）。旧云端无此字段时被
    # extra='ignore' 静默忽略（向后兼容不报错），由下方结果端的客户端
    # clip_by_date_window 保证窗口正确性。
    # 注意键名 lit_date_* 与 FAERS 的 date_from/date_to（YYYYMMDD）区分，防混用。
    if date_from:
        payload["lit_date_from"] = date_from
    if date_to:
        payload["lit_date_to"] = date_to
    # CDSR-only 车道：与 lit_date_* 同为「云端暂未消费、extra='ignore' 静默忽略」的
    # 前向兼容字段。云端将来实现后无需再改客户端；当前 online 路径的 Cochrane
    # 限定完全由调用方（ct_literature.run）的客户端二次过滤保证。
    if cochrane:
        payload["lit_cochrane"] = True
    # 审计透传：汇总/标记类调用把统计信息放进 querystr，Coze 端飞书节点原样落库
    if querystr:
        payload["querystr"] = querystr
    if skillname:
        payload["skillname"] = skillname
    # request_id（2026-11-13 修复）：11-11 引入幂等去重时只在调用点传参，
    # 本函数签名与 payload 均未接通，云端 feishu_write 收不到 ID → 无法去重，
    # searchlog 实测 40.6% 结构性双写。此处补齐顶层信封字段；旧云端
    # extra='ignore' 静默忽略，向后兼容。详见 references/coze_fix_spec_*。
    if request_id:
        payload["request_id"] = request_id

    if not run:
        # 预览模式：只打印 payload，不执行网络请求
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return None

    # 出站授权检查
    if not _check_outbound_authorization(CT_SEARCH_ENDPOINT):
        print(f"[AUTH-BLOCK] endpoint not authorized: {CT_SEARCH_ENDPOINT}", file=sys.stderr)
        print("Run with --run after authorizing, or use --offline for local fallback.", file=sys.stderr)
        return {"error": "AUTH-BLOCK", "endpoint": CT_SEARCH_ENDPOINT}

    # HTTP POST to Coze —— 快速路径 /stream_run（钳制 60s），主路径 /run（同步/异步自适应）
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    try:
        # 钳制理由：网关 60s 硬超时（stgw），stream 超过即整次被杀——
        # 给它 300s socket timeout 只会干等到被杀，不如 60s 主动切换主路径。
        projects = _sanitize_works(_coze_stream_once(body, min(timeout, _STREAM_FAST_PATH_MAX)))
        if projects is not None:
            # 流式成功：projects 已是从 workflow_end/output 提取的列表（兼容 projects
            # 列表 / project_list 字符串 / 字典三种形态）。total_count 取实际返回条数
            # （检索受 max_results 截断，与 Coze 端 total_count 语义一致）。
            # 路线 B：拿到结果后按日期窗口裁剪（云端未原生过滤时的正确性保证）。
            projects, _dw = clip_by_date_window(projects, date_from, date_to, source)
            _log_date_window(source, _dw, date_from, date_to)
            return {
                "source": _display_source(source),
                "count": len(projects),
                "works": projects,
                "total_count": len(projects),
            }
        # 流式无结果（workflow Output 未绑定 / 被 rejected）→ 回退 /run
        print("[coze] /stream_run 无结果，回退 /run", file=sys.stderr)
    except urllib.error.HTTPError as e:
        print(f"[Coze] /stream_run HTTP {e.code}，回退 /run: "
              f"{(e.read().decode('utf-8', errors='replace') if e.fp else '')[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"[Coze] /stream_run 失败({type(e).__name__})，回退 /run: {e}", file=sys.stderr)
    # 回退 /run（非流式）——响应形态自适应：同步返回 / accepted+run_id 异步轮询
    try:
        req2 = urllib.request.Request(CT_SEARCH_ENDPOINT, data=body, headers=_headers(), method="POST")
        with urllib.request.urlopen(req2, timeout=timeout) as resp2:
            data = json.loads(resp2.read().decode("utf-8"))
        # 异步协议探测（2026-10-19）：重检索任务返回 {status:accepted, run_id}
        # （服务端还要跑数分钟）。不识别该协议会被当同步响应对待 → 空结果。
        if isinstance(data, dict) and data.get("status") == "accepted" \
                and data.get("run_id"):
            print(f"[Coze] /run 返回 accepted（run_id={data['run_id']}），转异步轮询",
                  file=sys.stderr)
            data = _coze_async_poll(CT_SEARCH_ENDPOINT, str(data["run_id"]), timeout)
            if isinstance(data, dict) and data.get("error"):
                return data  # 轮询失败/超时：错误透传，不进 parse/裁剪
        parsed = _parse_run_response(data, source)
        # 路线 B：/run 回退路径同样按日期窗口裁剪（与 stream 路径一致）。
        if isinstance(parsed, dict) and isinstance(parsed.get("works"), list):
            _w, _dw = clip_by_date_window(parsed["works"], date_from, date_to, source)
            _log_date_window(source, _dw, date_from, date_to)
            parsed["works"] = _w
            parsed["count"] = len(_w)
            parsed["total_count"] = len(_w)
        return parsed
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print(f"[Coze] HTTP {e.code}: {err_body[:500]}", file=sys.stderr)
        # 401/403 → 明确警告
        if e.code in (401, 403):
            print("[Coze] Token 无效或已过期，请通过 --token 或 env CT_REGISTRY_COZE_TOKEN 重新设置", file=sys.stderr)
        return {"error": f"HTTP {e.code}", "message": err_body[:500]}
    except Exception as e:
        print(f"[Coze] 请求失败: {type(e).__name__}: {e}", file=sys.stderr)
        return {"error": f"{type(e).__name__}: {e}"}


# ── 流式检索生成器 ──────────────────────────────────────────────────────────
def dispatch_stream(source: str, keyword: str, year_from: int = None, year_to: int = None,
                    max_results: int = 50, run: bool = False, log_feishu: bool = True,
                    timeout: int = 300, offline: bool = False, querystr: str = None,
                    skillname: str = None, batch_size: int = 5, progress=None,
                    force_coze: bool = False,
                    mode: str = "search",
                    date_from: str = None, date_to: str = None,
                    request_id: str = None) -> "Generator[List[Dict], None, None]":
    """流式检索生成器：把 Coze 返回的 works 按 batch_size 切片，依次 yield 给调用方。

    设计（对应「对 coze 的调用改为流式调用，5 个一批依次返回」）：
      - 内部复用 dispatch()：dispatch 已改 /stream_run（SSE）+ /run 回退，coze 调用本身是流式的；
      - 检索工作流在 workflow_end 一次性返回全部结果（非节点级增量），故切片在流结束后分批吐出；
        若 coze 端未来支持节点级增量返回，吐批点可自然前移，无需改调用方；
      - 每批最多 batch_size 篇（默认 5），最后一批可能不足。progress 回调逐批上报进度，
        便于 workbench / CLI 渐进渲染，避免长检索「干等」。

    Args:
        batch_size: 每批返回篇数（默认 5）。
        progress: 可选 fn(msg) 进度回调。
        mode: 工作模式，透传给 dispatch()（"search" 真实检索 / "log_only" 仅留痕）。
            修复 2026-09-26：2026-09-11 给 dispatch 加 mode 参数时漏改本函数签名，
            导致内部 `mode=mode` 引用未定义全局名，流式检索一执行即 NameError。

    Yields:
        List[dict] —— 每批 work（本地统一格式，含 doi/title/source 等）。
    """
    if batch_size < 1:
        batch_size = 1
    result = dispatch(source, keyword, year_from, year_to, max_results,
                      date_from=date_from, date_to=date_to,
                      run=run, log_feishu=log_feishu, timeout=timeout, offline=offline,
                      querystr=querystr, skillname=skillname, force_coze=force_coze,
                      mode=mode, request_id=request_id)
    if result is None or result.get("error"):
        msg = f"[coze] 检索失败: {result.get('error') if result else 'None'}"
        if progress:
            progress(msg)
        else:
            print(msg, file=sys.stderr)
        return
    works = result.get("works", [])
    total = len(works)
    if progress:
        progress(f"[coze] 检索完成，共 {total} 篇，按 {batch_size} 篇/批返回")
    for i in range(0, total, batch_size):
        batch = works[i:i + batch_size]
        if progress:
            progress(f"[coze] 返回第 {i // batch_size + 1} 批（{len(batch)} 篇）")
        yield batch


# ── CLI ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="文献检索统一 Coze 客户端（ct-literature 外发出口）")
    ap.add_argument("--source", required=True, choices=sorted(DISPATCHABLE_SOURCES),
                    help="数据源")
    ap.add_argument("--keyword", required=True, help="检索词（英文）")
    ap.add_argument("--year-from", type=int, default=None, help="起始年份")
    ap.add_argument("--year-to", type=int, default=None, help="截止年份")
    ap.add_argument("--max-results", type=int, default=50, help="每源最大返回数（默认 50）")
    ap.add_argument("--run", action="store_true", help="实际执行网络请求（默认仅预览 payload）")
    ap.add_argument("--log-feishu", type=lambda x: x.lower() in ("true", "1", "yes"),
                    default=True, help="是否记飞书（默认 True，中间调用设 False）")
    ap.add_argument("--timeout", type=int, default=300, help="HTTP 超时秒数（默认 300）")
    ap.add_argument("--offline", action="store_true", help="强制本地兜底（不调 Coze）")
    ap.add_argument("--force-coze", action="store_true",
                    help="强制走 Coze，跳过本地直连早返回（留痕类调用用：保证 log_feishu 生效）")
    ap.add_argument("--token", default=None, help="Coze Bearer token（优先级最高）")
    ap.add_argument("--stream", action="store_true",
                    help="流式返回：works 按 --batch-size 切片逐批输出（默认 5 篇/批）")
    ap.add_argument("--batch-size", type=int, default=5,
                    help="--stream 时每批篇数（默认 5）")
    ap.add_argument("--log-only", action="store_true",
                    help="仅写飞书审计留痕、不做检索（mode=log_only；隐含 --force-coze）。"
                         "修复 2026-10-12：此前 main() 引用 args.log_only 但未定义该参数，"
                         "单独运行 CLI 必 AttributeError。")
    ap.add_argument("--date-from", default=None, metavar="YYYY-MM-DD",
                    help="月份级发表日期下界（路线 B，优先于 --year-from）")
    ap.add_argument("--date-to", default=None, metavar="YYYY-MM-DD",
                    help="月份级发表日期上界（默认今天）")
    args = ap.parse_args()

    # 注入 CLI token
    if args.token:
        _resolve_token._cli_token = args.token

    # --log-only → mode=log_only（仅写飞书留痕，不检索）；否则默认 search
    _mode = "log_only" if args.log_only else "search"
    # log_only 隐含 force_coze（dispatch 内也会兜底强制），此处显式合并便于调试打印
    _force_coze = args.force_coze or args.log_only

    if args.stream:
        n_batches = 0
        for batch in dispatch_stream(
            source=args.source,
            keyword=args.keyword,
            year_from=args.year_from,
            year_to=args.year_to,
            date_from=args.date_from,
            date_to=args.date_to,
            max_results=args.max_results,
            run=args.run,
            log_feishu=args.log_feishu,
            timeout=args.timeout,
            offline=args.offline,
            batch_size=args.batch_size,
            force_coze=_force_coze,
            mode=_mode,
        ):
            n_batches += 1
            print(f"--- batch {n_batches} ({len(batch)} works) ---")
            print(json.dumps(batch, ensure_ascii=False, indent=2))
        print(f"[done] {n_batches} batches")
        return 0

    result = dispatch(
        source=args.source,
        keyword=args.keyword,
        year_from=args.year_from,
        year_to=args.year_to,
        date_from=args.date_from,
        date_to=args.date_to,
        max_results=args.max_results,
        run=args.run,
        log_feishu=args.log_feishu,
        timeout=args.timeout,
        offline=args.offline,
        force_coze=_force_coze,
        mode=_mode,
    )

    if result is not None:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
