#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf_download.py — 文献 PDF 批量下载（本地端，与 ct-literature 共用）

架构（2026-09-05 重构：统一输入 + 单次 coze 传送 + 真实直链下载）：
  - 统一输入：本地为每篇 work 生成「单一规范标识」（open_access_url 优先，否则 doi），
    整批一次性发 coze（publisher_pdf_batch 统一契约），不再区分 DOI / OA 两种模式。
  - 解码上移 coze：coze 端对每条标识执行 A(解码+直下探测验证真实 PDF)
    → 若 A 失败则 B(浏览器+S3)，仅返回经探测/上传验证过的真实直链
    （pdf_url / pdf_s3_url）；拿不到真实直链只返 pdf_failed，绝不返回伪直链。
  - 本地只负责「下载 coze 返回的真实直链」。下载失败 → 标记 manual，不重发
    （符合「只做一次 coze 传送」；coze 端 A→B 已联合尝试，无需本地二次传送）。
  - 兜底：coze 不可用 / --skip-coze 时，本地复用 _epmc_lookup_pdf_url 自行解码
    （仅 Europe PMC 非 Cloudflare 副本可直下；付费墙/重定向器本地无浏览器只能标 manual）。

出站信封（ct-base references/coze_io_contract.md 全库统一契约）：
  - skill_version（§1.2）：顶层信封字段，读本地 SKILL.md frontmatter `version:`
  - locale（§1.1）：界面 / 输出语言（zh/en），顶层信封输出开关
  - params.user_language（§1.1）：输入语言提示，规范承载位是请求 params（顶层不双写）
  - coze 端据此把 runtime_sec（处理持续秒数，§2.2）写入飞书 resultstr 列（只进日志不出参）
  - 🔴 版本字段落点（§2.1，2026-09-17 定）：skill_version（本端顶层信封）+ coze_version
    （端点常量）一律由 **coze 端写飞书 resultstr**；本端**不得**把版本号塞进 `querystr`，
    也不用新增列——改端点一处即可，客户端无需改动。

单批上限（用户 2026-09-05 指定）：coze 端 MAX_BATCH_ITEMS=50，超限直接 rejected；
本地按同一上限自动拆批，每批一次传送。

总量上限（用户 2026-09-06 追加）：一次 PDF 下载请求超过 MAX_TOTAL_ITEMS=50 篇
直接拒绝（不再拆批）——多批串行传送 + 逐篇下载的总耗时远超单请求网关/用户可接受
窗口，必然超时；须提示用户缩小范围（按引用排序取 top-N / 单源 / 分次下载）后重试。

传输（2026-09-05 改流式）：PDF 批量下载耗时较长，coze 端口改用 stream_run（SSE 流式）
调用——实时返回节点事件，避免长连接被网关按单响应超时掐断。本地 _call_coze_unified
解析 SSE 流，从 workflow_end / node_end 事件提取最终 projects（兼容 projects 列表、
project_list 字符串/字典、超长回参外置 S3 三种形态）。

流程（run）：
  1. 收集每篇规范标识（OA 优先，否则 DOI）
  2. 总量 > 50 → 直接拒绝（提示缩小范围），不拆批
  3. 按 50 上限拆批，每批一次性调用 coze（publisher_pdf_batch 统一契约）→ 拿回真实直链
  4. 本地 urllib 逐篇下载真实直链（间隔 1s、429 退避、拒绝挑战页）；失败标 manual，不重发
  5. 整批 coze 失败 → 该批走本地兜底解码（仅 epmc 副本可下）

2026-10-25 下载增强（参考 academic-fulltext-fetcher 设计 · 用户指定四项）：
  - ① 中文题名→DOI：Crossref 之外新增 OpenAlex 跨语言通道（title.search +
    年份/第一作者佐证）——Crossref 对中文期刊覆盖差，中文题名常无候选。
  - ② 深度校验：浅层（%PDF 头 + >5KB）之后追加「pypdf/fitz 可解析且页数 ≥1」，
    残篇/截断/加密 PDF 判失败；大小KB/页数落 work 供 Excel/manifest 展示。
  - ③ pdf_manifest.csv 下载台账：来源URL/通道/状态/大小/页数/source_trust 全量留痕。
  - ④ 单源连续失败熔断（_SourceCircuitBreaker）：epmc/openalex/unpaywall/coze
    任一源连续失败达阈值即停用本源，批量运行不再白撞已挂的源。

Sci-Hub 可选兑底（2026-10-26，参考 openags/paper-search-mcp，用户拍板）：
  - **默认关闭**；仅当 --use-scihub / PdfDownloader(use_scihub=True) /
    环境变量 CT_LIT_ALLOW_SCIHUB=1 显式开启时才激活。
  - 定位：整条链的**最后一步**——Europe PMC / OpenAlex / Unpaywall / 预印本 /
    coze 云端解码全部失败后，对仍有 DOI 的条目经 Sci-Hub 镜像解析直链。
  - ⚠️ 法律风险：Sci-Hub 全文多数未经版权方授权，下载存在法律与合规风险，
    **后果自负**；机构环境（GCP/申办方项目）严禁开启。每次激活都会打印免责声明。
"""

import difflib
import hashlib
import json
import os
import random
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

from adapters.sci_hub import DISCLAIMER as _SCIHUB_DISCLAIMER, \
    enabled as _scihub_enabled, resolve_pdf_url as _scihub_resolve

# §16.9 出站归位：本模块自 adapters/ 运行，但同仓引用（adapters.preprint_fallback /
# scripts.i18n 等）依赖技能根与 scripts 在 sys.path——统一在此注入，__main__ 直跑与
# 包导入（from adapters.pdf_download import …）两种场景都可用。
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (_SKILL_ROOT, os.path.join(_SKILL_ROOT, "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# 并发下载线程池上限（P0，2026-09-06）：不同出版商域名之间并发下载，
# 同域名仍按该域名的 min_delay 串行保距（见 _PerHostRateLimiter），
# 既提速又不被 Cloudflare 1015 封。纯本地、标准库实现，不碰 coze 工作流。
MAX_DOWNLOAD_WORKERS = 6
# coze 子批篇数（P1，2026-09-06）：把 indirect_items 拆成 ≤12 的小批送 coze，
# 比一次性 50 更早返回首批结果，且「解码子批 N+1」与「下载子批 N」重叠 → 管道化提速。
COZE_SUB_BATCH = 12
# Unpaywall email（与 coze 端 publisher_pdf_batch_node._UPW_EMAIL 保持一致；
# Unpaywall 要求合法 email，本地用它取 OA 直链 / 更早预印本版本做「本地优先」路由）。
_UPW_EMAIL = "medstatstar@gmail.com"
# 本地预筛：每个 DOI 的 Unpaywall 查询并发上限（预取阶段用，避免触发限流）
_UPW_CONCURRENCY = 5

DEFAULT_EMAIL = "ct-literature@example.com"

# ── 2026-10-25 PDF 下载增强（参考 academic-fulltext-fetcher 设计 · 用户指定四项）──
# ① 中文题名→DOI：新增 OpenAlex 跨语言通道（Crossref 对中文期刊覆盖差，difflib
#    按字符比对在中文上可用但常无候选——缺的是候选源，不是相似度算法）。
# ② 深度校验：pypdf 可解析 + 页数 ≥ _PDF_MIN_PAGES（原有 %PDF 头 + >5KB 只能
#    挡 HTML 落地页，挡不住残篇/截断/加密 PDF）。
# ③ pdf_manifest.csv 下载台账（来源 URL / 大小KB / 页数 / 信任级）。
# ④ 单源连续失败熔断：_SourceCircuitBreaker（epmc / openalex / unpaywall / coze）。
# 单源连续失败熔断阈值：同一本地查询源连续失败即停用本源（整轮不再查询），
# 避免批量运行时每篇都白撞一个已挂的源；任一次成功即重置计数。
_CB_MAX_FAILURES = 3
# 三级 PDF 缓存复用（2026-10-26，参考 meta-analysis _pdf_stem + _a4_cached_pdf）：
# run() 开始时由 pdf_dir 现有文件构建 {stem: path} 缓存映射，下载前命中即复用，
# 避免重复下载。缓存键 = _pdf_stem(work)（DOI 优先，退其次 title md5）。
# 三级查找：① 上一轮 cache_map 传入（兼容旧 docN 命名）② 当前稳定命名 ③ 裸 DOI。
_PDF_STEM_DOI_PREFIX = "doi_"
_PDF_STEM_TITLE_PREFIX = "t_"
# coze 端点熔断阈值：每次传送成本高（sub-batch 级），2 次连续失败即停。
_CB_COZE_MAX_FAILURES = 2
# Sci-Hub 镜像熔断阈值（2026-10-26）：镜像极不稳定，连续 2 次解析失败即停，
# 批量不再逐篇白撞（每篇解析 + 下载耗时可观）。
_CB_SCIHUB_MAX_FAILURES = 2
# OpenAlex 礼貌池邮箱（题名→DOI 解析用；与 Unpaywall 同一合规身份）
_OA_MAILTO = _UPW_EMAIL
# PDF 深度校验最小可接受页数（残篇/截断/加密 PDF 在此被挡下）
_PDF_MIN_PAGES = 1
# manifest 台账里来源类型 → 人类可读标签（原始 via 值括号内保留，便于审计）
_VIA_LABEL = {
    "oa_direct_local": "OA直链(本地)",
    "preprint_local": "预印本(本地)",
    "coze": "云端解码",
    "coze_local_fallback": "云端解码(兜底)",
    "epmc_local": "EuropePMC(本地)",
    "scihub_local": "Sci-Hub(本地·用户自担)",
    "manual_incoming": "手动回传(机构权限)",
}
# manifest source_trust 分级（沿用文章 academic-fulltext-fetcher 的三级口径）：
# 合法 OA（含 Europe PMC / 出版商 OA / 云端解码所得合法直链）= 高；
# 预印本（未经同行评审）= 中；
# Sci-Hub（2026-10-26 可选兑底，**默认关闭**，法律风险用户自担）= 低——
# 仅在用户显式开启时才会出现该标签，台账里一眼可辨以便合规审查。
_VIA_TRUST = {
    "oa_direct_local": "高",
    "preprint_local": "中",
    "coze": "高",
    "coze_local_fallback": "高",
    "epmc_local": "高",
    "scihub_local": "低(用户自担)",
    "manual_incoming": "高",
}
# coze 流式接口（PDF 批量下载耗时较长，改用 stream_run SSE 实时返回节点事件，
# 避免长连接被网关按单响应超时掐断）。
# 宿主用 ct-search.coze.site：实测只有该宿主真正承载 publisher_pdf_batch 工作流
#（/run 返回真实直链；bp3886cvnd.coze.site 是 registry-search 工作流，不服务 PDF 下载）。
# 若 publisher_pdf_batch 已发布到其它流式宿主，可用环境变量 CT_SEARCH_ENDPOINT 覆盖。
# 注意：stream_run 返回 workflow_end.output 依赖 coze 工作流「Output」变量已绑定
# project_list；未绑定则 output 为 {}（已实测），需在工作流控制台配置后流式才生效。
CT_SEARCH_ENDPOINT = os.environ.get("CT_SEARCH_ENDPOINT", "https://ct-search.coze.site/stream_run")
CT_REGISTRY_SKILL = os.path.expanduser("~/.workbuddy/skills/ct-registry")

# Europe PMC 严格限速：两次查询之间至少间隔 1.0 秒（本地兜底用，单线程调用）。
_epmc_last_ts = 0.0
_EPMC_MIN_INTERVAL = 1.0


def _epmc_ratelimit():
    """两次 Europe PMC 查询之间至少间隔 1.0 秒（严格限速）。"""
    global _epmc_last_ts
    now = time.time()
    wait = _EPMC_MIN_INTERVAL - (now - _epmc_last_ts)
    if wait > 0:
        time.sleep(wait)
    _epmc_last_ts = time.time()


# ── 代理绕过（2026-10-26 v1.5.3，参考 meta-analysis pdf_fetch._get 实测结论）──
# 系统代理（如 WorkBuddy 本机加速代理）会杀死长连接/超时 PDF 下载。urllib 默认
# 读 HTTPS_PROXY 环境变量走代理；此处在 **下载器构造时** 给整个进程装一个空
# ProxyHandler 的默认 opener，使 PDF 下载链路（含 preprint_fallback / sci_hub，
# 同进程）全部直连。检索/coze 阶段在下载器构造前已完成，行为不变。
# 恢复系统代理：设环境变量 CT_LIT_USE_SYSTEM_PROXY=1。
# 实现注意：走 install_opener（而非逐调用点换 opener），urllib.request.urlopen
# 的调用形态不变——回归测试 monkeypatch urlopen 仍生效。
_NO_PROXY_DONE = False


def _install_no_proxy_opener():
    """空 ProxyHandler 全局直连（幂等，仅在 PdfDownloader 构造时调用一次）。"""
    global _NO_PROXY_DONE
    if _NO_PROXY_DONE:
        return
    _NO_PROXY_DONE = True
    if os.environ.get("CT_LIT_USE_SYSTEM_PROXY", "").strip() == "1":
        return
    try:
        urllib.request.install_opener(
            urllib.request.build_opener(urllib.request.ProxyHandler({})))
    except Exception:
        pass  # 安装失败不阻塞下载（退回系统默认行为）


def _resolve_token() -> str:
    """token 优先级：env CT_SEARCH_COZE_TOKEN > 本技能内嵌公开 blob > ct-registry 兜底。

    2026-10-13 v1.4.6：endpoint_token.py 自包含于本技能 adapters/（此前仅动态
    insert ct-registry/adapters，云端部署容器无该技能树 → import 失败 → token
    为空 → Coze 401，PDF 直链解析在网页端不可用）。先插 ct-registry 再插本目录，
    最终本目录在 sys.path 最前，本机 / 云端一致。
    """
    tok = os.environ.get("CT_SEARCH_COZE_TOKEN")
    if tok:
        return tok
    try:
        _here = os.path.dirname(os.path.abspath(__file__))
        for p in (os.path.join(CT_REGISTRY_SKILL, "adapters"), _here):
            if os.path.isdir(p) and p not in sys.path:
                sys.path.insert(0, p)
        from endpoint_token import get_token as _gt
        return _gt() or ""
    except Exception:
        return ""


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    tok = _resolve_token()
    if tok:
        h["Authorization"] = "Bearer " + tok
    return h


def _query_origin() -> str:
    """稳定机器标识。"""
    return "sha256:" + hashlib.sha256(os.environ.get("COMPUTERNAME", "unknown").encode()).hexdigest()


# 单批篇数上限：必须与 coze 端 publisher_pdf_batch_node.MAX_BATCH_ITEMS 保持一致。
# coze 端超过该值直接返 status=rejected 拒绝执行；本地按此上限自动拆批，
# 每批一次传送（每篇仍只传送一次，下载失败不重发）。
MAX_BATCH_ITEMS = 50
# 单次下载总量上限（用户 2026-09-06 追加）：一次 run(works) 超过该篇数**直接拒绝**，
# 不拆批继续——多批串行（每批一次 coze 传送 + 逐篇下载间隔 1s）总耗时必然超时；
# 拒绝时提示用户缩小范围（top-N / 单源 / 分次）后重试。
MAX_TOTAL_ITEMS = 50
# sub-batch 发送间隔（秒）：避免 coze 端高频请求触发限流（2026-09-07 用户要求 ≥5 秒）
COZE_BATCH_INTERVAL = 5
# 技能版本号回退常量（SKILL.md 读取失败时使用；ct-base coze_io_contract §1.2）
_SKILL_VERSION_FALLBACK = "1.0.0"


def _skill_version() -> str:
    """技能版本号：优先读技能根 SKILL.md frontmatter 的 `version:`（单一事实来源），
    读取失败（文件缺失 / 格式异常）回退模块常量 —— 升级技能后无需同步改本文件。
    位置：coze 请求**顶层信封**字段（与 query_origin 同级，ct-base coze_io_contract §1.2）。
    """
    try:
        skill_md = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "SKILL.md")
        with open(skill_md, encoding="utf-8") as f:
            head = f.read(4000)
        m = re.search(r"^version:\s*([0-9][\w.\-]*)", head, re.M)
        if m:
            return m.group(1)
    except Exception:
        pass
    return _SKILL_VERSION_FALLBACK


def _resolve_locale() -> str:
    """界面 / 输出语言（zh/en）—— 顶层信封 `locale` 字段（ct-base coze_io_contract §1.1）。

    判定源：ct-literature 自带 i18n（系统 locale 检测）；失败回退 "zh"。
    """
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        if here not in sys.path:
            sys.path.insert(0, here)
        import i18n as _i18n
        lang = (_i18n._current_lang() or "").lower()
        if lang.startswith("zh"):
            return "zh"
        if lang.startswith("en"):
            return "en"
    except Exception:
        pass
    return "zh"


def _resolve_user_language() -> str:
    """输入语言提示（zh/en）—— 承载位 `params.user_language`（ct-base coze_io_contract §1.1）。

    规范位置是请求 `params`（顶层不双写）；服务端读取顺序 params → 顶层 → 空。
    当前与界面语言同源（i18n 判定）；保留独立函数以便后续按「输入 query 文本内容」
    细分（§1.1 三级优先级：显式 override > 输入文本判定 > 系统 locale）。
    """
    return _resolve_locale()


PDF_DOWNLOAD_NOTICE = (
    "【下载说明】本功能仅为方便快速获取文档：① 仅下载无版权问题的 OA 文献，付费文献请自行下载；"
    "② 请勿用于超过 50 篇的批量下载或商业用途，否则可能导致服务被封锁 IP；"
    "③ OA 供应商普遍拦截代码自动下载；本地下载采用「Europe PMC 渲染 + OpenAlex + Unpaywall + 出版商直链」"
    "多级回退，OA/预印本类成功率通常 85–95%，订阅刊无 OA 副本时仍会失败，需自行下载；"
    "④ 对无法直接下载的文献，系统会自动尝试公开提供的作者手稿或其它预印本渠道作为替代；"
    "⑤ 每篇下载约需 10–20 秒（含限流退避与云端解析），整批下载请耐心等待。"
)


def _safe_filename(doi: str, max_len: int = 120) -> str:
    """DOI / URL → 安全文件名。"""
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", doi)
    # 移除末尾已有的 .pdf 后缀，避免重复追加
    if safe.lower().endswith(".pdf"):
        safe = safe[:-4]
    if len(safe) > max_len:
        digest = hashlib.md5(doi.encode()).hexdigest()[:8]
        safe = safe[:max_len - 9] + "_" + digest
    return safe + ".pdf"


# ── 三级 PDF 缓存复用（2026-10-26，参考 meta-analysis _pdf_stem + _a4_cached_pdf）──
def _pdf_stem(work: Dict[str, Any]) -> str:
    """work → 稳定文件基名（DOI 优先，退其次 title md5）。同一文献跨运行恒定。"""
    doi = str((work or {}).get("doi") or "").strip().lower()
    if doi:
        slug = re.sub(r"[^a-z0-9]+", "_", doi).strip("_")[:90]
        if slug:
            return _PDF_STEM_DOI_PREFIX + slug
    title = str((work or {}).get("title") or "").strip().lower()
    return _PDF_STEM_TITLE_PREFIX + (
        hashlib.md5(title.encode("utf-8")).hexdigest()[:10] if title else "notitle")


def _build_cache_map(pdf_dir: str) -> Dict[str, str]:
    """扫描 pdf_dir 现有文件 → {stem: 绝对路径}。三级查找的 cache_map 层。"""
    m = {}
    if not os.path.isdir(pdf_dir):
        return m
    for fn in os.listdir(pdf_dir):
        if not fn.endswith(".pdf"):
            continue
        fp = os.path.join(pdf_dir, fn)
        if os.path.getsize(fp) < 256:  # 跳过残篇
            continue
        stem = fn[:-4]  # 去掉 .pdf
        m[stem] = fp
        # 同时索引裸 DOI 兼容键（doi_ 前缀之外再补一层）
        bare = re.sub(r"^doi_", "", stem)
        if bare != stem:
            m[bare] = fp
    return m


def _cached_pdf(work: Dict[str, Any], pdf_dir: str,
                cache_map: Dict[str, str] = None) -> Optional[str]:
    """查该 work 已落盘的 PDF（跨运行复用，避免重复下载）。

    三级查找：① cache_map（由 _build_cache_map 构建，含旧 docN 命名兼容）；
             ② 当前稳定命名文件；③ 裸 DOI 命名（兼容旧版裸 doi stem）。
    """
    key = str((work or {}).get("doi") or (work or {}).get("title") or "").strip().lower()
    if key and cache_map:
        p = cache_map.get(key)
        if p and os.path.isabs(p) and os.path.exists(p) and os.path.getsize(p) > 256:
            return p
    stem = _pdf_stem(work)
    p = os.path.join(pdf_dir, stem + ".pdf")
    if os.path.exists(p) and os.path.getsize(p) > 256:
        return p
    # ③ 裸 DOI 兼容
    doi = str((work or {}).get("doi") or "").strip().lower()
    if doi:
        bare = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi).strip("/")
        if bare:
            slug = re.sub(r"[^a-z0-9]+", "_", bare).strip("_")[:90]
            lp = os.path.join(pdf_dir, "doi_" + slug + ".pdf")
            if os.path.exists(lp) and os.path.getsize(lp) > 256:
                return lp
    return None


# 直链 PDF 判定：OA / 预印本真实 PDF 直链（本地可直接下载，无需送 coze 解码）。
# 注意：doi.org 解析页不算直链；预印本服务器域名（bioRxiv/medRxiv/arXiv/ChemRxiv/
# ResearchSquare/SSRN）即便 URL 形态不标准也视为可本地直下。
def _looks_like_direct_pdf(url: str) -> bool:
    u = (url or "").strip().lower()
    if not u or "doi.org" in u:
        return False
    # 预印本 / OA 直链域名（命中即视为可本地直下）
    if any(h in u for h in ("biorxiv.org", "medrxiv.org", "arxiv.org",
                            "chemrxiv.org", "researchsquare.com", "ssrn.com")):
        return True
    return (u.endswith(".pdf") or "pdf=render" in u
            or "article-pdf" in u or "pdfs/" in u
            or "full.pdf" in u or "document/" in u
            or "download" in u or "bitstream" in u)


def _looks_like_pdf_url(u: str) -> bool:
    """宽松判定：是否为 PDF 下载地址（用于本地预筛返回的候选直链）。"""
    u = (u or "").strip().lower()
    return bool(u) and (u.endswith(".pdf") or "pdf" in u)


# 出版商 WAF 域名：直链几乎必然对自动化返回 403；本地优先改用
# Europe PMC 渲染通道 / OpenAlex 机构库镜像 / 作者手稿，而非硬刚直链。
# （2026-09-08 实战：Elsevier/Wiley/Lancet 直链 100% 被拦，渲染通道与机构库镜像才拿得到。）
_WAF_HOSTS = (
    "elsevier.com", "sciencedirect.com", "wiley.com", "onlinelibrary.wiley.com",
    "springer.com", "link.springer.com", "springerpub.com", "tandfonline.com",
    "taylorfrancis", "sagepub.com", "nature.com", "wolterskluwer", "lww.com",
    "acs.org", "pubs.acs.org", "bmj.com", "liebertpub.com", "karger.com",
    "frontiersin.org", "thelancet.com", "cell.com", "nejm.org", "oup.com",
)

# 反爬出版商域名（2026-10-26，参考 meta-analysis pdf_fetch._ANTI_SCRAPE_HOSTS）：
# 命中且本地下载失败 → 自动委托 coze 服务端真实浏览器（publisher_pdf_batch）单篇
# 救援，不再直接返回 manual。meta-analysis 实测：MDPI 等出版商对无头客户端 403，
# UA+Referer 都救不了，唯有服务端真实浏览器可破。
_ANTI_SCRAPE_HOSTS = ("mdpi.com", "mdpi-res.com", "mdpi-resilience.com")


def _is_anti_scrape(url: str) -> bool:
    """识别对无头客户端做反爬的出版商（命中且本地下载失败 → 委托 coze 服务端浏览器）。"""
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except Exception:
        return False
    return any(host == h or host.endswith("." + h) for h in _ANTI_SCRAPE_HOSTS)


def _is_waf_host(url: str) -> bool:
    u = (url or "").strip().lower()
    return any(h in u for h in _WAF_HOSTS)


# ── 站点 profile + 通用 landing 页解析（2026-10-27 新增）─────────────────────
# 知识来源：人工研读 zotero/translators 仓库归纳的行为规律（仅思路参考，
# 实现全部自研，无 AGPL 衍生代码）。核心洞察：
#   ① 学术出版商绝大多数遵循 Highwire 元标签标准：landing 页含
#      <meta name="citation_pdf_url">，一个通用规则即可覆盖大量 OA 站
#      （Embedded Metadata.js 即 Zotero 的通用兜底，同理）；
#   ② 少数站点用固定 URL 模板（如 Frontiers：{base}/articles/{doi}/pdf）；
#   ③ 兜底：landing 页 PDF 锚点扫描（href 含 /pdf 或以 .pdf 结尾）。
# 规则数据在 adapters/site_profiles.json（改模板不动代码）。

_SITE_PROFILES: Optional[dict] = None


def _load_site_profiles() -> dict:
    """加载站点 profile 数据文件（懒加载，缺失/损坏返回空表不致命）。"""
    global _SITE_PROFILES
    if _SITE_PROFILES is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "site_profiles.json")
        try:
            with open(path, encoding="utf-8") as f:
                _SITE_PROFILES = json.load(f).get("profiles", {}) or {}
        except Exception:
            _SITE_PROFILES = {}
    return _SITE_PROFILES


def _host_of(url: str) -> str:
    try:
        return (urllib.parse.urlparse(url).hostname or "").lower()
    except Exception:
        return ""


def _profile_for(url: str) -> Tuple[Optional[str], dict]:
    """按落地页域名返回 (profile_key, profile dict)。key 是 profiles 里的域名键。"""
    host = _host_of(url)
    for key, prof in _load_site_profiles().items():
        k = key.lower()
        if host == k or host.endswith("." + k):
            return key, prof or {}
    return None, {}


_AUX_PDF_RE = re.compile(
    r"(_|-|\b)(reference|references|bibliography|supplement|supplementary)\.pdf$", re.I)


def _is_aux_pdf(url: str) -> bool:
    """是否为「非正文」PDF（参考文献列表 / 补充材料）。

    2026-10-27 实测：OpenAlex locations 里存在 nature 的
    `..._reference.pdf`（参考文献列表）这类条目，下载回来是错文件。
    宁可缺漏不可弄错，故在候选阶段直接排除。
    """
    path = (url or "").split("?")[0]
    return bool(_AUX_PDF_RE.search(path))


def _is_epmc_render(url: str) -> bool:
    """是否 Europe PMC 渲染通道链接（.../articles/PMCxxx?pdf=render）。

    2026-10-27 实测：该通道在本地被 Cloudflare 拦（r1 里 24 篇 preprint_local
    全部 FAIL），只能作为「无其他副本时」的兜底，不应占据候选首位。
    """
    u = (url or "").lower()
    return "europepmc.org" in u and "pdf=render" in u


def _doi_prefix(doi: str) -> str:
    """裸 DOI → 注册前缀（'10.3389/fimmu.2026.x' → '10.3389'）。"""
    d = _bare_doi(doi)
    parts = [p for p in d.split("/") if p]
    return parts[0].lower() if len(parts) >= 2 else ""


def _profile_for_doi(doi: str) -> Tuple[Optional[str], dict]:
    """按 DOI 前缀返回 (profile_key, profile dict)。

    2026-10-27 新增：真实检索里大量条目 open_access_url 为空（r1+r2 共 38/82），
    此时没有任何 URL 可供 _profile_for 匹配，站点模板永远轮不到；但 DOI 前缀本身
    就唯一确定了出版商（10.3389 → Frontiers）。实测这批里 10.3389/* 的
    OA 文章用模板构造即可直下（200 + %PDF），属纯漏检。
    """
    pre = _doi_prefix(doi)
    if not pre:
        return None, {}
    for key, prof in _load_site_profiles().items():
        prefixes = (prof or {}).get("doi_prefixes") or []
        if any(str(p).lower() == pre for p in prefixes):
            return key, prof or {}
    return None, {}


_META_PDF_RE = re.compile(
    r"<meta[^>]+name\s*=\s*[\"']citation_pdf_url[\"'][^>]*>", re.I)
_META_CONTENT_RE = re.compile(r"content\s*=\s*[\"']([^\"']+)[\"']", re.I)
_LINK_PDF_RE = re.compile(
    r"<link[^>]+type\s*=\s*[\"']application/pdf[\"'][^>]*>", re.I)
_LINK_HREF_RE = re.compile(r"href\s*=\s*[\"']([^\"']+)[\"']", re.I)
_ANCHOR_RE = re.compile(r"<a\b[^>]*>", re.I)
_HREF_RE = re.compile(r"href\s*=\s*[\"']([^\"']+)[\"']", re.I)
_TITLE_RE = re.compile(r">([^<]{0,60})<", re.S)


def _extract_pdf_candidates(html: str, base_url: str) -> List[Tuple[str, str]]:
    """从 landing 页 HTML 提取 PDF 候选直链，返回 [(url, layer)] 按优先级。

    优先级（归纳自 Zotero Embedded Metadata 的做法）：
      landing_meta  > citation_pdf_url meta 标签（Highwire 标准，最可靠）
      landing_link  > <link type="application/pdf">（次可靠）
      landing_anchor> 锚点 href 形似 PDF（宽松，需下载验证）
    """
    out: List[Tuple[str, str]] = []
    seen = set()

    def _abs(u: str) -> str:
        u = (u or "").strip().replace("&amp;", "&")
        if not u:
            return ""
        if u.startswith("//"):
            return "https:" + u
        if u.startswith("http"):
            return u
        if u.startswith("/"):
            p = urllib.parse.urlparse(base_url)
            return "%s://%s%s" % (p.scheme, p.netloc, u)
        return urllib.parse.urljoin(base_url, u)

    # ① citation_pdf_url（可能有多条，全收）
    for m in _META_PDF_RE.finditer(html):
        c = _META_CONTENT_RE.search(m.group(0))
        if c:
            u = _abs(c.group(1))
            if u and u not in seen:
                seen.add(u)
                out.append((u, "landing_meta"))
    # ② <link type=application/pdf>
    for m in _LINK_PDF_RE.finditer(html):
        h = _LINK_HREF_RE.search(m.group(0))
        if h:
            u = _abs(h.group(1))
            if u and u not in seen:
                seen.add(u)
                out.append((u, "landing_link"))
    # ③ 锚点扫描：href 形似 PDF（同域优先在前，跨域其后）
    anchors = []
    for m in _ANCHOR_RE.finditer(html):
        tag = m.group(0)
        h = _HREF_RE.search(tag)
        if not h:
            continue
        u = _abs(h.group(1))
        if not u or u in seen or not _looks_like_pdf_url(u):
            continue
        base_host = _host_of(base_url)
        same = _host_of(u) == base_host if base_host else True
        anchors.append((same, u))
    anchors.sort(key=lambda x: 0 if x[0] else 1)
    for _, u in anchors:
        seen.add(u)
        out.append((u, "landing_anchor"))
    return out


def _telemetry_pdf_resolve(out_dir: str, doi: str, domain: str,
                           layer: str, url: str, result: str) -> None:
    """解析遥测：一行 JSON 追加到 out_dir/.pdf_resolver_log.jsonl。

    跑几轮真实检索后按 (域名, layer, result) 汇总，即可知道该给哪些
    失败站点做专用 profile / 是否值得上更重的解析层。
    """
    try:
        path = os.path.join(out_dir or ".", ".pdf_resolver_log.jsonl")
        rec = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "doi": doi,
               "domain": domain, "layer": layer, "url": (url or "")[:200],
               "result": result}
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _http_json(url: str, timeout: int = 25) -> Optional[dict]:
    """简单 JSON GET（精简头，不请求压缩），失败返回 None。

    供 Crossref / OpenAlex / Europe PMC 复用。注意：必须显式 Accept-Encoding: identity——
    urllib 标准库不自动解 gzip/br，若带 `Accept-Encoding: gzip` 服务端回压缩字节，
    json.loads 会直接失败（2026-09-08 实测坑：Crossref/OpenAlex 解析全挂、Europe PMC
    因用 plain UA 才正常）。
    """
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "ct-literature-skill/1.0",
            "Accept": "application/json",
            "Accept-Encoding": "identity",
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def _sim(a: str, b: str) -> float:
    """标题相似度（0–1），difflib ratio。用于 Crossref 命中判定。"""
    a, b = (a or "").lower().strip(), (b or "").lower().strip()
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def _year_from_date(s) -> Optional[int]:
    if not s:
        return None
    m = re.search(r"(\d{4})", str(s))
    return int(m.group(1)) if m else None


def _first_author_name(w: Dict[str, Any]) -> str:
    """取 work 的第一作者名（字符串或 [{name}] 两种形态均可）。"""
    a = w.get("authors")
    name = ""
    if isinstance(a, list) and a:
        first = a[0]
        if isinstance(first, str):
            name = first
        elif isinstance(first, dict):
            name = first.get("name") or first.get("display_name") or ""
    elif isinstance(a, str):
        name = a
    return (name or "").strip()


def _info_len(s: str) -> int:
    """题名信息长度：CJK 每字计 2（信息密度高），其余每字符计 1。

    用于「题名过短无法消歧」门槛——中文 6 字 ≈ 英文 12 字符的信息量，
    若按裸字符数一刀切，会把「胎儿型肺腺癌一例」这类高信息密度的短中文
    题名误杀（2026-10-25 live 验证实测教训）。
    """
    cjk = sum(1 for ch in (s or "") if "\u4e00" <= ch <= "\u9fff")
    return cjk * 2 + max(0, len(s or "") - cjk)


def _openalex_title_search(title: str, year=None, author: str = "") -> Tuple[str, float]:
    """OpenAlex 按题名检索解析 DOI（2026-10-25 新增通道）。

    为什么加这条：Crossref 对中文期刊覆盖很差——中文题名在 Crossref 里常常
    **根本没有候选**，difflib 相似度再高也无从比起（文章的 academic-fulltext-
    fetcher 同样踩过「中文题名解析不出」的坑，解法就是补 OpenAlex 通道）。
    OpenAlex 聚合了 Crossref + 各渠道记录，中文期刊命中率显著更高。

    判定（宁缺毋滥，anti-hallucination）：
      - 题名相似度（difflib，中文近逐字匹配同样可近 1.0）≥ 0.90 → 直接接受；
      - 或 相似度 ≥ 0.60 且**年份命中（±1 年）且第一作者名命中** → 接受
        （双佐证消歧，防同名/近似题名撞车）；
      - 其余返回 ("", score)。
    返回 (doi, score)；score<阈值视为未命中。
    """
    if not title or _info_len(title.strip()) < 12:
        # 题名过短/通用无法消歧（同名论文高发）——错下比下不到更糟。
        return "", 0.0
    try:
        q = urllib.parse.quote(title.strip()[:250])
        api = ("https://api.openalex.org/works?filter=title.search:%s"
               "&per-page=5&select=doi,display_name,publication_year,authorships"
               "&mailto=%s" % (q, urllib.parse.quote(_OA_MAILTO)))
        d = _openalex_get_json(api)
        if not d:
            return "", 0.0
        best, best_score = "", 0.0
        author_norm = re.sub(r"\s+", "", (author or "").lower())
        for it in (d.get("results") or [])[:5]:
            doi = _bare_doi(it.get("doi") or "")
            if not doi:
                continue
            t = it.get("display_name") or ""
            s = _sim(t, title)
            yr = it.get("publication_year")
            year_ok = bool(year and yr and abs(int(yr) - int(year)) <= 1)
            if year and yr and not year_ok:
                s -= 0.20          # 年份不符重罚（防撞同名新年份论文）
            elif year_ok:
                s += 0.05
            author_ok = False
            if author_norm:
                for a in (it.get("authorships") or [])[:8]:
                    nm = re.sub(r"\s+", "", ((a.get("author") or {}).get("display_name") or "").lower())
                    if nm and (author_norm in nm or nm in author_norm):
                        author_ok = True
                        break
                if author_ok:
                    s += 0.10
            if s > best_score:
                best, best_score = doi, s
            # 双佐证通道：相似度中等但年份+作者双命中即接受（记录分数备查）
            if best and best_score >= 0.60 and year_ok and author_ok:
                return best, round(best_score, 2)
        if best_score >= 0.90:
            return best, round(best_score, 2)
        return "", round(best_score, 2)
    except Exception:
        return "", 0.0


def _openalex_get_json(url: str) -> Optional[dict]:
    """OpenAlex JSON GET：礼貌池 mailto + 可选 API key（.env 自动加载，
    免 key 亦可，只是限额低）+ 重试。失败返回 None（由熔断器记账）。"""
    try:
        from adapters import http_utils
        h = http_utils.build_openalex_headers(http_utils.load_openalex_key())
        return http_utils.get_json(url, headers=h, timeout=25, max_retries=2)
    except Exception:
        return None


def _bare_doi(v: str) -> str:
    """OpenAlex doi 字段（https://doi.org/10.xxxx/…）→ 裸 DOI。"""
    v = (v or "").strip()
    if not v:
        return ""
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", v, flags=re.I)


def _resolve_doi_from_title(title: str, year=None, author: str = "") -> Tuple[str, float]:
    """按标题解析 DOI：Crossref（原有通道）+ OpenAlex（2026-10-25 新增通道）。

    返回 (doi, score)；score<阈值视为未命中返回 ("", score)。用于「仅有标题、
    无 DOI」的重下载 / 补下载场景（如 Excel 行有标题但 DOI 字段缺失）。

    两通道并行互补：
      - Crossref：英文/主流期刊权威注册库，阈值 0.9（近逐字匹配才接受）；
      - OpenAlex：聚合库，对中文期刊覆盖显著更好——中文题名在 Crossref 常无
        候选，此通道按「年份 + 第一作者」双佐证消歧。
    两路都命中时取分数高者（Crossref 通常更权威，同分优先 Crossref）。
    """
    if not title:
        return "", 0.0
    # ── Leg 1：Crossref（原有行为保持不变：<55 字符不解析 + 阈值 0.9）──
    cross_doi, cross_score = "", 0.0
    if len(title.strip()) >= 55:
        q = urllib.parse.quote(title[:250])
        api = ("https://api.crossref.org/works?query.bibliographic=%s&rows=5"
               "&select=DOI,title,container-title,published" % q)
        d = _http_json(api)
        if d:
            best, best_score = "", 0.0
            for it in (d.get("message") or {}).get("items", []):
                doi = it.get("DOI") or ""
                t = (it.get("title") or [""])[0]
                yr = None
                parts = (it.get("published") or {}).get("date-parts") or [[None]]
                if parts and parts[0]:
                    yr = parts[0][0]
                s = _sim(t, title)
                if year and yr and abs(int(yr) - int(year)) > 1:
                    s -= 0.25
                if s > best_score:
                    best, best_score = doi, s
            # 阈值 0.9：只接受近逐字匹配。正确论文在 Crossref 中标题通常逐字
            # 一致(sim≈1.0)，通用/同名标题易撞车(sim<0.9)——错下比下不到更糟。
            if best_score >= 0.9:
                cross_doi, cross_score = best, best_score
    # ── Leg 2：OpenAlex 跨语言通道（中文题名的主要希望）──
    oa_doi, oa_score = _openalex_title_search(title, year, author)
    if cross_doi and (cross_score >= oa_score):
        return cross_doi, round(cross_score, 2)
    if oa_doi:
        return oa_doi, round(oa_score, 2)
    return "", round(max(cross_score, oa_score), 2)


class _PerHostRateLimiter:
    """每域名限速器（P0，2026-09-06）：不同出版商域名之间并发下载，同域名按 min_delay
    串行保距——既提速又不被 Cloudflare 1015 封。纯本地、标准库实现，不碰 coze 工作流。

    acquire(host, delay)：调用方在发起请求「前」调用。同一 host 的并发调用会顺序化——
    每位等待到「距上一位允许时刻 ≥ delay」才放行；不同 host 各持各锁、互不阻塞。
    下载动作在 acquire 返回之后进行（锁已释放），故同 host 的「间隔」计的是请求发起节奏，
    不计入下载耗时，最大化并发。
    """

    def __init__(self):
        self._host_locks: Dict[str, threading.Lock] = {}
        self._host_last: Dict[str, float] = {}
        self._meta = threading.Lock()

    def acquire(self, host: str, delay: float):
        with self._meta:
            lk = self._host_locks.get(host)
            if lk is None:
                lk = self._host_locks[host] = threading.Lock()
        lk.acquire()
        try:
            # 计算允许时刻需短暂持全局锁（仅读写 _host_last），但 sleep 必须释放全局锁——
            # 否则所有 host 的限速等待会互相阻塞，跨域名并发被全局锁串行化（致命性能 bug）。
            # 同 host 串行保距由 per-host 锁 lk 保证（sleep 期间仍持 lk）；跨 host 并发由
            # 释放全局锁后并行实现。
            now = time.time()
            with self._meta:
                allowed = max(now, self._host_last.get(host, 0.0) + delay)
                wait = allowed - now
                self._host_last[host] = allowed
            if wait > 0:
                time.sleep(wait)
        finally:
            lk.release()


class _SourceCircuitBreaker:
    """单源连续失败熔断器（2026-10-25，参考 academic-fulltext-fetcher 的
    「单源连续失败熔断」设计）：同一来源连续 _CB_MAX_FAILURES 次失败即**停用
    本来源**（整轮剩余不再查询/发送），避免批量运行时每篇都白撞一个已挂的源；
    任一次成功即重置计数。线程安全（预取阶段多线程并发调用）。

    与 Europe PMC 429 特判的关系：429 是「已被服务端明确限流」，仍走
    record(..., force_open=True) 立即停用；其它失败（超时/5xx/连接错误）累计
    计数，达到阈值才停——避免把一次网络抖动误判成源已死。
    """

    def __init__(self, max_failures: int = _CB_MAX_FAILURES):
        self._max = max(1, int(max_failures))
        self._fail: Dict[str, int] = {}
        self._open: set = set()
        self._lock = threading.Lock()

    def is_open(self, src: str) -> bool:
        """本源是否已熔断（停用）。"""
        with self._lock:
            return src in self._open

    def record(self, src: str, ok: bool, force_open: bool = False):
        """记录一次对 src 的访问结果。ok=True 重置计数并尝试复 closed；
        ok=False 累计，force_open=True（如 HTTP 429 明确限流）立即熔断。"""
        with self._lock:
            if ok:
                self._fail[src] = 0
                self._open.discard(src)
                return
            if force_open:
                self._open.add(src)
                return
            n = self._fail.get(src, 0) + 1
            self._fail[src] = n
            if n >= self._max:
                self._open.add(src)

    def open_sources(self) -> List[str]:
        with self._lock:
            return sorted(self._open)


def _browser_headers(url: str = "") -> dict:
    """浏览器级 headers（C：补全 Accept / Accept-Language / Referer 降低被识别为 bot 的概率）。

    🔴 Accept-Encoding 必须为 identity（2026-10-25 live 验证修复）：此前带
    `gzip, deflate, br`，部分源站（bioRxiv 等）会返回 gzip 压缩流，而 urllib
    标准库**不自动解压**——下载到头 5 字节是 gzip magic(\\x1f\\x8b)而非 %PDF-，
    浅层校验直接判死，整类源站「本地直下」全灭（与 _http_json 同文件同款坑，
    JSON 查询侧早已用 identity，下载侧漏改）。请求不压缩最稳。
    """
    h = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
        "Accept": "application/pdf,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
    }
    host = (urlparse(url).hostname or "").lower() if url else ""
    if "biorxiv.org" in host:
        h["Referer"] = "https://www.biorxiv.org/"
    elif "medrxiv.org" in host:
        h["Referer"] = "https://www.medrxiv.org/"
    elif url:
        # v1.5.3 泛化（参考 meta-analysis consent_aware_download）：.pdf 后缀剥除
        # （模拟从文章页点下载），全源站都带 Referer（与 meta-analysis 同口径）。
        u = url[:-4] if urlparse(url).path.lower().endswith(".pdf") else url
        h["Referer"] = u
    # v1.5.3：种 OneTrust「全部接受」consent cookie（跳过 EBI/NCBI 等 API 型站点）
    # ——部分出版商（Nature/Elsevier 系）会先弹同意墙再放 PDF。
    if host and not any(d in host for d in ("ebi.ac.uk", "ncbi.nlm.nih.gov")):
        h["Cookie"] = _ONETRUST_CONSENT_COOKIE
    return h


# OneTrust「全部接受」consent cookie（v1.5.3，参考 meta-analysis _OPANON_CONSENT_ACCEPT_ALL）。
# 静态种子值：绝大多数 OneTrust 站点只看 OptanonAlertBoxClosed（弹窗已关）+ groups 全 1。
_ONETRUST_CONSENT_COOKIE = (
    "OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jan+01+2026+00%3A00%3A00+GMT%2B0000"
    "&version=6.30.0&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1"
    "&OptanonAlertBoxClosed=2026-01-01T00%3A00%3A00.000Z")


def _get(url: str, timeout: int = 60, retries: int = 2) -> bytes:
    """GET 带重试（A：429 指数退避）。"""
    import random as _rand
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=_browser_headers(url))
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = min(30 * (2 ** attempt), 120) + _rand.uniform(0, 5)
                time.sleep(wait)
                last = "HTTP 429 (backoff %.0fs)" % wait
                continue
            if e.code in (403, 404):
                time.sleep(1)
                last = "HTTP %s" % e.code
                continue
            raise
        except Exception as e:
            last = "%s: %s" % (type(e).__name__, e)
            time.sleep(0.5)
    raise RuntimeError(str(last))


def _follow_to_landing(url: str, timeout: int = 25) -> Optional[str]:
    """DOI 解析器 URL（doi.org/...）→ 真实落地页 URL；失败返回 None。

    2026-10-27 实测：OpenAlex primary_location.landing_page_url 与部分
    open_access_url 给的是 doi.org 跳转器，若直接按域名判定会整条 L1.5/L2
    解析被跳过（PLOS 即此情形）。这里只跟随一跳拿最终 URL，读到 2KB 即断流，
    不整页下载（省带宽，且不触发站点反爬的频率阈值）。
    """
    if not url:
        return None
    final = None
    try:
        req = urllib.request.Request(url, headers=_browser_headers(url))
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final = r.geturl()
            r.read(2048)
    except urllib.error.HTTPError as e:
        # 403/404 也会经过重定向；HTTPError 同样带 geturl()
        try:
            final = e.geturl()
        except Exception:
            final = None
    except Exception:
        return None
    if not final or _host_of(final) in ("doi.org", ""):
        return None
    return final


def _pdf_page_count(path: str) -> Optional[int]:
    """解析 PDF 返回页数；无法解析 / 无可用解析器时返回 None。

    解析器链：pypdf → PyMuPDF(fitz)。两者都不可用时返回 None（「未知」而非
    「0 页」）——缺依赖不应把好 PDF 判死，调用方按放行处理。
    """
    # 快速失败：极小文件不进解析器。畸形/截断残篇常只有几十~几百字节，
    # pypdf/fitz 对其会进入修复扫描，单篇耗时可达秒级（批量下被放大成严重卡顿）；
    # 任何有效的多页 PDF 都远大于此阈值，故 <256 字节直接判不可解析。
    try:
        if os.path.getsize(path) < 256:
            return 0
    except Exception:
        return None
    try:
        try:
            from pypdf import PdfReader
            with open(path, "rb") as f:
                return len(PdfReader(f).pages)
        except ImportError:
            pass
        try:
            import fitz
            with fitz.open(path) as doc:
                return doc.page_count
        except ImportError:
            return None
    except Exception:
        # 能打开但解析失败（截断/加密/损坏）→ 0 页语义由 _pdf_is_valid 判定
        return 0


def _pdf_is_valid(path: str, min_pages: int = _PDF_MIN_PAGES) -> Optional[bool]:
    """PDF 深度校验（2026-10-25，参考 academic-fulltext-fetcher）：

    原有浅层校验（%PDF 头 + >5KB + Content-Type 非 HTML）只能挡掉 HTML 挑战页，
    挡不住**残篇 / 截断 / 加密 / 伪造 PDF**——它们会被计为「成功」混进统计。
    本函数在浅层通过后追加一层「可被 PDF 解析器打开且页数 ≥ min_pages」。

    返回 True=有效；False=残篇/损坏（调用方应判失败）；
    None=无可用解析器（pypdf/fitz 均缺）——按放行处理，不因缺依赖误杀。
    """
    pages = _pdf_page_count(path)
    if pages is None:
        return None
    return pages >= min_pages


def _pdf_meta(path: str) -> Tuple[Optional[float], Optional[int]]:
    """返回 (size_kb, pages)：大小恒可算；页数需解析器（缺失返回 None）。"""
    try:
        size_kb = round(os.path.getsize(path) / 1024.0, 1)
    except Exception:
        size_kb = None
    return size_kb, _pdf_page_count(path)


def _download_to(url: str, out_path: str, timeout: int = 120) -> bool:
    """下载 URL 到本地文件。返回是否成功（首字节须为 %PDF-）。

    对 Europe PMC / biorxiv / medRxiv 等 429 限流做指数退避重试（A）；对 Cloudflare /
    跳转 / 限流等 HTML 挑战页直接判失败（不落脏文件到目标路径），避免把网页当 PDF 存下。

    写盘策略：**先写到 out_path + '.part' 临时文件，校验通过后
    用 os.replace 原子替换到 out_path**。绝不在失败路径删除目标文件——WorkBuddy 的
    safe-delete 钩子会拦截对工作区文件的 os.remove（fail closed 抛异常），此前
    "先建目标文件、校验失败再 os.remove 清理" 会触发钩子并反复卡死。os.replace 是
    覆盖写入而非删除，不触发钩子，且天然幂等（可安全覆盖已存在文件）。
    """
    import random as _rand
    tmp_path = out_path + ".part"
    for attempt in range(4):  # A：4 次重试（3 次 429 退避 + 1 次最终尝试）
        try:
            req = urllib.request.Request(url, headers=_browser_headers(url))
            with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp_path, "wb") as f:
                head = r.read(5)
                f.write(head)
                ct = (r.headers.get("Content-Type") or "").lower()
                if head[:5] != b"%PDF-" or "html" in ct:
                    # 挑战页 / 跳转页 / 限流页 → 判失败。临时文件留在 .part 不删
                    # （不触发 safe-delete 钩子）；下次成功 os.replace 会覆盖。
                    if "html" in ct and attempt < 3:
                        time.sleep(3)
                        continue
                    return False
                while True:
                    chunk = r.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
            if os.path.getsize(tmp_path) > 5000:
                # 深度校验（2026-10-25）：残篇/截断/加密/伪造 PDF 在此挡下——
                # 浅层（%PDF 头 + 大小）对它们一律放行，会把「成功」统计注水。
                # None = 无解析器（缺 pypdf/fitz）→ 放行，不因缺依赖误杀。
                if _pdf_is_valid(tmp_path) is False:
                    # 临时文件留在 .part 不删（不触发 safe-delete 钩子）；
                    # 下次成功 os.replace 会覆盖。
                    return False
                # 校验通过 → 原子覆盖到最终路径（os.replace 非删除，不触发钩子）
                os.replace(tmp_path, out_path)
                return True
            return False
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                wait = min(30 * (2 ** attempt), 120) + _rand.uniform(0, 5)
                time.sleep(wait)
                continue
            return False
        except Exception:
            return False
    return False


def _dig_output(node):
    """从单个流式事件对象（workflow_end / node_end）中提取最终 output。

    兼容多种嵌套形态：
      - {"type":"workflow_end", "output": <...>}
      - {"type":"workflow_end", "data": {"output": <...>}}
      - {"type":"workflow_end", "data": {"data": {"output": <...>}}}
    output 可能是 dict（已结构化）或 str（JSON 字符串，由调用方 json.loads）。
    """
    if not isinstance(node, dict):
        return None
    out = node.get("output")
    if out is None and isinstance(node.get("data"), dict):
        out = node["data"].get("output")
    if (out is None and isinstance(node.get("data"), dict)
            and isinstance(node["data"].get("data"), dict)):
        out = node["data"]["data"].get("output")
    return out


def _has_real_output(o: Any) -> bool:
    """判定某节点的输出是否携带「我们需要的」真实结果（而非空容器）。

    workflow_end.output 在 coze「Output 变量未绑定」时返回空字典 {}，
    此时必须回退到 node_end 输出——因此空 dict / 空 list 不算『有结果』。
    """
    if isinstance(o, dict):
        return any(k in o for k in ("projects", "project_list", "s3_url", "status", "total_count"))
    if isinstance(o, str):
        try:
            d = json.loads(o)
        except Exception:
            return bool(o) and "[DONE]" not in o
        return isinstance(d, dict) and any(
            k in d for k in ("projects", "project_list", "s3_url", "status", "total_count"))
    if isinstance(o, list):
        return len(o) > 0
    return False


def _parse_coze_stream(resp, log_fn, return_full: bool = False) -> Any:
    """解析 Coze stream_run 的 SSE 流，提取最终 projects（或完整结果 dict）。

    return_full=False（默认）：返回 projects 列表（兼容 publisher_pdf_batch / 旧调用方）。
    return_full=True（2026-10-26 薄客户端策略调用）：返回完整结果 dict
        （含 projects + 统计字段 duplicates_removed / raw_count 等），调用方自行取用。

    返回 projects（list[dict]）或 None（无结果 / 执行失败 / 被拒绝）。

    流式事件类型（外层 data.type，与用户提供的六种完全一致）：
      - workflow_start : 工作流开始（记日志，忽略内容）
      - node_start     : 节点开始（记节点标题，实时进度）
      - node_end       : 节点结束，output 含该节点输出（流式真实结果常落此处）
      - workflow_end   : 工作流结束，output 为聚合结果（依赖 coze Output 变量绑定）
      - error          : 执行错误，直接返回 None
      - ping           : 保活心跳，忽略

    选择最终结果的优先级：
      workflow_end.output（非空）→ 否则取最后一个『含真实结果』的 node_end 输出
      → 否则取最后一个 node_end → 否则兜底整块 JSON。
    """
    events: List[dict] = []
    buf = b""
    _t0 = time.time()          # 本次流开始时间（用于进度日志中的"已用时"）
    _hb = [0.0]                # 上次心跳 log 时间（列表以便闭包内改写）

    def _log_evt(evt) -> bool:
        """SSE 事件到达即记录（实时进度）。返回 False = 致命 error，需中止。"""
        if not isinstance(evt, dict):
            return True
        etype = evt.get("type")
        inner = evt.get("data")
        if isinstance(inner, dict) and inner.get("type"):
            etype = inner.get("type")
            node = inner
        else:
            node = evt
        _el = time.time() - _t0
        if etype == "workflow_start":
            log_fn("[coze:workflow_start] 工作流已启动（已用时 %.0fs）" % _el)
        elif etype == "node_start":
            nt = node.get("node_title") or node.get("title") or node.get("node_id") or ""
            log_fn("[coze:node_start] %s（已用时 %.0fs）" % (nt, _el))
        elif etype == "node_end":
            nt = node.get("node_title") or node.get("node_id") or ""
            o = _dig_output(node)
            if o is not None and nt:
                try:
                    sz = len(json.dumps(o, ensure_ascii=False))
                except Exception:
                    sz = 0
                log_fn("[coze:node_end] %s -> %d 字节输出（已用时 %.0fs）" % (nt, sz, _el))
        elif etype == "workflow_end":
            log_fn("[coze:workflow_end] 工作流结束（总计 %.0fs）" % _el)
        elif etype == "ping":
            # 端点保活心跳：静默期也每 20s 上报一次，避免界面"假死"
            if _el - _hb[0] >= 20:
                _hb[0] = _el
                log_fn("[coze] 端点保活中，解码进行…已用时 %.0fs" % _el)
        elif etype == "error":
            log_fn("[coze] 流式返回 error: %s"
                   % json.dumps(evt.get("data") or evt, ensure_ascii=False)[:400])
            return False
        return True

    for chunk in resp:
        buf += chunk
        while b"\n" in buf:
            line_b, buf = buf.split(b"\n", 1)
            line = line_b.decode("utf-8", "ignore").rstrip("\r")
            if line.startswith("data:"):
                ds = line[len("data:"):].lstrip()
                if ds and ds != "[DONE]":
                    try:
                        evt = json.loads(ds)
                    except Exception:
                        continue
                    events.append(evt)
                    if not _log_evt(evt):   # 边到边报：进度实时可见
                        return None
    # 兜底：未解析到事件则尝试整块 JSON（应对非 SSE 返回）
    if not events:
        try:
            events.append(json.loads(buf.decode("utf-8", "ignore")))
        except Exception:
            log_fn("[coze] 流式响应无法解析为事件")
            return None

    workflow_end_out: Any = None
    node_outputs: List[Any] = []
    for evt in events:
        if not isinstance(evt, dict):
            continue
        etype = evt.get("type")
        inner = evt.get("data")
        if isinstance(inner, dict) and inner.get("type"):
            etype = inner.get("type")
            node = inner
        else:
            node = evt
        # 注：日志已在流式循环里实时上报（_log_evt），此处只做结果收集，避免重复
        if etype == "node_end":
            o = _dig_output(node)
            if o is not None:
                node_outputs.append(o)
        elif etype == "workflow_end":
            workflow_end_out = _dig_output(node)
        # workflow_start / node_start / error / ping 等：仅日志用途，已在 _log_evt 处理

    # 选择最终结果：优先 workflow_end（非空），否则回退到『含真实结果的』node_end
    final: Any = None
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
        # 兜底：非 SSE 整块 JSON 返回，取最后一个含 projects/project_list 的事件
        for evt in reversed(events):
            if isinstance(evt, dict) and ("projects" in evt or "project_list" in evt):
                final = evt
                break
    if final is None:
        return None
    # output 可能为 JSON 字符串（如 project_list 序列化体）
    if isinstance(final, str):
        try:
            final = json.loads(final)
        except Exception:
            log_fn("[coze] 最终结果非 JSON: %s" % final[:200])
            return None
    if not isinstance(final, dict):
        return None

    # 薄客户端策略调用：返回完整结果 dict（外层字段 + 解析后的 project_list，
    # 含 projects / status / duplicates_removed / raw_count 等节点实际输出字段）。
    if return_full:
        out = dict(final)
        pl = final.get("project_list")
        if isinstance(pl, str):
            try:
                pl = json.loads(pl)
            except Exception:
                pl = None
        if isinstance(pl, dict):
            out.update(pl)
        return out

    # 归一化 projects（兼容 projects 列表 / project_list 字符串或字典 / s3_url 外置）
    projects = final.get("projects")
    if isinstance(projects, list):
        if projects:
            return projects
        # 空列表：若带 s3_url 说明回参超长外置，去拉取真实数据；否则表示 0 篇结果
        s3 = final.get("s3_url")
        if s3:
            pl = None
            log_fn("[coze] 回参超长，从 S3 拉取结果: %s" % s3)
            try:
                raw_json = _get(s3, timeout=60)
                pl = json.loads(raw_json.decode("utf-8"))
            except Exception as e:
                log_fn("[coze] S3 结果拉取失败: %s" % e)
                return None
            if isinstance(pl, str):
                try:
                    pl = json.loads(pl)
                except Exception:
                    return None
            if isinstance(pl, dict):
                p = pl.get("projects")
                if isinstance(p, list):
                    return p
            return None
        return []
    pl = final.get("project_list")
    s3 = final.get("s3_url")
    if pl is None and s3:
        log_fn("[coze] 回参超长，从 S3 拉取结果: %s" % s3)
        try:
            raw_json = _get(s3, timeout=60)
            pl = json.loads(raw_json.decode("utf-8"))
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
                return p
    return None


def _extract_doi_from_url(url: str) -> Optional[str]:
    """从 URL 提取 DOI（如 nejm.org/doi/pdf/10.1056/NEJMoa... → 10.1056/NEJMoa...）。"""
    if not url:
        return None
    m = re.search(r'/doi/(?:pdf/)?(10\.\d{4,}/[^\s?&]+)', url)
    if m:
        return m.group(1)
    m = re.search(r'[?&]doi=(10\.\d{4,}/[^\s?&]+)', url)
    if m:
        return m.group(1)
    # doi.org/10.xxxx/... 形式（最常见的官方 DOI 解析地址）
    m = re.search(r'doi\.org/(10\.\d{4,}/[^\s?&]+)', url)
    if m:
        return m.group(1)
    # 兜底：URL 中任意位置出现的裸 DOI
    m = re.search(r'(10\.\d{4,}/[^\s?&]+)', url)
    if m:
        return m.group(1)
    return None


class PdfDownloader:
    """文献 PDF 批量下载器。

    Args:
        out_dir: PDF 保存目录
        email: Unpaywall email（OA 解析用）
        progress: 进度回调 fn(msg)
        min_delay: 预印本逐篇下载间隔秒数（防 Cloudflare 限流，默认 3.0）
        merged_json: 本次运行的 .merged.json 路径（回写 Excel 时读 meta；None = 不读）
        xlsx_out: 目标 Excel 路径；**给定后 run() 结束会自动把 PDF 本地路径写回
            「PDF 本地路径」列**（用户 2026-09-08 加固：此前该步骤仅主流程内联实现，
            独立直驱脚本易漏，导致「下了却没写进 Excel」）。None = 不回写。
        lang: 回写 Excel 的语言（"auto"/"zh"/"en"，默认 "auto"，与 export_workbook 一致）
        safety: 回写是否渲染 Safety-Related 表（None = 回退到 merged meta.safety）
    """

    def __init__(self, out_dir: str = "pdfs", email: str = DEFAULT_EMAIL,
                 progress=None, min_delay: float = 3.0,
                 merged_json: str = None, xlsx_out: str = None,
                 lang: str = "auto", safety=None,
                 citations_out_dir: str = None, citation_style: str = "apa",
                 use_scihub: bool = None, enable_cache: bool = True,
                 request_id: str = None):
        # normpath 归一路径分隔符（out_dir 常以正斜杠传入，join 会混用 \ /，
        # 导致落盘路径与 Excel 显示出现 C:/…\file 混用）
        self.out_dir = os.path.normpath(out_dir)
        # 三级 PDF 缓存复用（2026-10-26，参考 meta-analysis _a4_cached_pdf）：
        # run() 开始时由 pdf_dir 现有文件构建 {stem: path} 映射，下载前命中即跳过。
        # enable_cache=False 时禁用（如需要全新下载）。
        self._enable_cache = bool(enable_cache)
        self._cache_map: Dict[str, str] = {}
        self.email = email
        self.progress = progress or (lambda m: None)
        # request_id（2026-11-13）：与检索汇总共用 ID，供云端 feishu_write
        # 按 (skillname, request_id) 幂等去重，覆盖批量下载留痕。
        self.request_id = request_id
        # biorxiv/medRxiv 逐篇下载间隔秒数（防 Cloudflare 1015 限流）。默认 3.0
        # （2026-09-06 实测安全）；批量调快可传更小值（如 1.2），失败会自动转
        # coze 兜底，不会卡死。
        self.min_delay = max(0.5, float(min_delay))
        os.makedirs(self.out_dir, exist_ok=True)
        # 整轮下载共用的每域名限速器（P0）：跨「直链下载 / coze 返直链下载」统一保距
        self._limiter = _PerHostRateLimiter()
        # 本地预筛（2026-09-07）：Unpaywall 查询结果缓存（按 DOI），整轮复用避免重复查询
        self._upw_cache: Dict[str, Any] = {}
        self._upw_email = _UPW_EMAIL
        # 单源连续失败熔断（2026-10-25）：epmc / openalex / unpaywall / coze
        # 任一源连续失败达阈值即停用本源，批量运行不再白撞已挂的源。
        self._cb = _SourceCircuitBreaker(_CB_MAX_FAILURES)
        self._cb_coze = _SourceCircuitBreaker(_CB_COZE_MAX_FAILURES)
        # fail-loud 计数器（2026-10-27）：coze 策略节点（lit_route / lit_preprint_check）
        # 不可用导致「判不出来」的篇数，与 skipped_no_oa 分离记账，便于 run() 汇总告警。
        self._strategy_unavailable: Dict[str, int] = {
            "lit_route": 0, "lit_preprint_check": 0}
        # v1.5.3：下载阶段强制直连（绕过系统代理；检索阶段不受影响，见函数 docstring）
        _install_no_proxy_opener()
        # Excel 自动回写配置（用户 2026-09-08）：构造时给定 xlsx_out，run() 正常结束
        # 即自动把 PDF 本地路径写回「PDF 本地路径」列，避免独立直驱 PdfDownloader
        # 的下载脚本漏调 update_xlsx_pdf_paths.py 而出现「下了却没写进 Excel」。
        self.merged_json = merged_json   # .merged.json 路径（读 meta；None = 不读）
        self.xlsx_out = xlsx_out        # 目标 Excel 路径（None = 不回写）
        self.lang = lang
        self.safety = safety            # None = 回退到 merged meta.safety
        # 题录回写（用户 2026-09-21）：下载器自身在 run() 结束自动把 PDF 绝对路径
        # 写回 references.bib / references.ris / references_<style>.md，避免「下了却没写进题录」。
        # citations_out_dir = 题录落盘目录（通常为 out_dir，即 pdfs 的父目录）；None = 不回写。
        self.citations_out_dir = citations_out_dir
        self.citation_style = citation_style
        # Sci-Hub 可选兑底（2026-10-26）：默认关闭；显式参数 > 环境变量
        # CT_LIT_ALLOW_SCIHUB。开启时立即打印免责声明（用户要求「明确说明、后果自负」）。
        self.use_scihub = _scihub_enabled(use_scihub)
        if self.use_scihub:
            self._log(_SCIHUB_DISCLAIMER)
            self._scihub_disclaimer_shown = True
        else:
            self._scihub_disclaimer_shown = False
        # Sci-Hub 镜像熔断器：连续 2 次解析失败即停（镜像极不稳定，省时止损）
        self._cb_scihub = _SourceCircuitBreaker(_CB_SCIHUB_MAX_FAILURES)

    def _log(self, msg: str):
        self.progress(msg)

    def _epmc_lookup_pdf_url(self, doi: str = "", pmcid: str = "", pmid: str = "") -> Optional[str]:
        """按 DOI/PMCID/PMID 解析 Europe PMC 的非 Cloudflare OA PDF 直链（本地兜底用）。

        返回 'https://europepmc.org/articles/{pmcid}?pdf=render' 或 None。
        限速：每次查询前走 _epmc_ratelimit()，严格 1.0 秒间隔（Europe PMC 官方限制 10 次/秒/IP，留足余量）。
        限流/过载处理：
          - 429：立即熔断本源（_cb force_open），本次 session 剩余不再查（避免被封）。
          - 503/504：服务端过载，指数退避重试（最多 3 次），**不禁用整批**——
            避免把“瞬时限流”误判成“无副本”，导致批量回退到出版商直链而拉低回收率。
          - 其它异常：记一次失败（连续 _CB_MAX_FAILURES 次后熔断本源）。
        """
        if self._cb.is_open("epmc"):
            return None
        if pmcid:
            return f"https://europepmc.org/articles/{pmcid}?pdf=render"
        if not doi and not pmid:
            return None
        for attempt in range(4):  # 1 次 + 503/504 重试 3 次
            if self._cb.is_open("epmc"):
                return None
            try:
                _epmc_ratelimit()
                q = f"DOI:{urllib.parse.quote(doi)}" if doi else f"PMID:{urllib.parse.quote(str(pmid))}"
                api = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                       f"?query={q}&format=json&resultType=core")
                req = urllib.request.Request(api, headers={"User-Agent": "ct-literature-skill/1.0"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    data = json.loads(r.read().decode("utf-8"))
                self._cb.record("epmc", ok=True)
                for res in (data.get("resultList") or {}).get("result", [])[:3]:
                    pmcid2 = res.get("pmcid") or ""
                    ftl = res.get("fullTextUrlList") or {}
                    for u in ftl.get("fullTextUrl", []) or []:
                        if u.get("documentStyle") == "pdf" and u.get("availabilityCode") == "OA" and pmcid2:
                            return f"https://europepmc.org/articles/{pmcid2}?pdf=render"
                    # 退路：有 pmcid 且 hasPDF，仍给 render 链接
                    if pmcid2 and res.get("hasPDF"):
                        return f"https://europepmc.org/articles/{pmcid2}?pdf=render"
                return None  # 查到但无 OA 副本
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    self._cb.record("epmc", ok=False, force_open=True)
                    self._log("[epmc] 被限流(429)，熔断本源：本次运行剩余文献不再查 Europe PMC")
                    return None
                elif e.code in (503, 504):
                    self._log(f"[epmc] 服务端过载 HTTP {e.code}，退避重试({attempt + 1}/3)")
                    import time as _t
                    _t.sleep(2 * (attempt + 1))
                    continue
                else:
                    self._cb.record("epmc", ok=False)
                    self._log(f"[epmc] 查询失败 HTTP {e.code}")
                    return None
            except Exception as e:
                self._cb.record("epmc", ok=False)
                self._log(f"[epmc] 查询失败: {type(e).__name__}: {e}")
                return None
        return None

    def _download_direct(self, url: str, doi: str, work: Dict[str, Any] = None) -> Optional[str]:
        """直接下载（OA / 预印本 / Europe PMC），返回本地路径或 None。"""
        fname = _safe_filename(doi or url)
        out_path = os.path.join(self.out_dir, fname)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
            return out_path
        # 三级缓存复用（2026-10-26）：命中稳定命名即跳过下载
        if work and self._enable_cache and self._cache_map:
            cached = _cached_pdf(work, self.out_dir, self._cache_map)
            if cached:
                return cached
        if _download_to(url, out_path):
            return out_path
        return None

    def _download_direct_with_delay(self, url: str, doi: str, delay: float = 1.0) -> Optional[str]:
        """带间隔的直接下载（B：拉长间隔 + jitter 避免触发反爬）。

        biorxiv/medRxiv 限速较严 → 用 self.min_delay（默认 3-5s，可构造时调快）；
        其它源保持 2-3s。
        """
        import random as _rand
        if "biorxiv.org" in url or "medrxiv.org" in url:
            time.sleep(self.min_delay + _rand.uniform(0, 2.0))
        else:
            time.sleep(max(delay, 1.5) + _rand.uniform(0, 1.0))
        return self._download_direct(url, doi)

    # ── Sci-Hub 可选兑底（2026-10-26，默认关闭，后果自负）──
    def _scihub_lookup(self, doi: str) -> Optional[str]:
        """Sci-Hub 镜像解析 PDF 直链（仅 use_scihub=True 时被调用）。

        免责声明只在下载器构造时打印一次（_SCIHUB_DISCLAIMER）；此处不逐篇
        重复打印，避免批量日志刷屏。连续失败达 _CB_SCIHUB_MAX_FAILURES 即熔断。
        """
        if not doi or self._cb_scihub.is_open("scihub"):
            return None
        try:
            u = _scihub_resolve(doi, log=self._log, politeness=1.5,
                                disclaimer=not self._scihub_disclaimer_shown)
            self._scihub_disclaimer_shown = True
        except Exception as e:
            u = None
            self._log(f"[scihub] 解析异常: {type(e).__name__}: {e}")
        self._cb_scihub.record("scihub", ok=bool(u))
        return u

    def _scihub_last_resort(self, works: List[Dict[str, Any]],
                            stats: Dict[str, Any]):
        """run() 末段最后兑底：对仍无 PDF 的条目经 Sci-Hub 兑底下载（可选，默认关闭）。

        仅处理：本地/coze 全部失败、有 DOI、未被 skip（无标识）的条目。
        串行执行（镜像限速），逐篇下载后做深度校验（残篇/加密 PDF 判失败）。
        成功计入 stats["scihub_ok"]，work 标 pdf_via="scihub_local"
        （manifest 信任级 = 低(用户自担)，合规审查一眼可辨）。
        """
        if not self.use_scihub:
            return
        candidates = []
        for w in works:
            if w.get("local_pdf_path"):
                continue
            note = w.get("pdf_download_note") or ""
            if "no DOI" in note:
                continue
            doi = (w.get("doi") or "").strip()
            if doi:
                candidates.append((doi, w))
        if not candidates:
            return
        self._log(f"[scihub] last-resort: {len(candidates)} items still without PDF, "
                  f"trying Sci-Hub (user opted-in, at own risk)...")
        for doi, w in candidates:
            if self._cb_scihub.is_open("scihub"):
                self._log("[scihub] 镜像已熔断（连续失败），剩余条目不再尝试")
                break
            url = self._scihub_lookup(doi)
            stats["scihub_tried"] = stats.get("scihub_tried", 0) + 1
            if not url:
                continue
            host = urlparse(url).netloc
            self._limiter.acquire(host, 2.5)
            path = self._download_direct(url, doi)
            ok = False
            if path:
                valid = _pdf_is_valid(path)
                if valid:
                    ok = True
                else:
                    try:
                        os.unlink(path)   # 残篇/落地页混入，删掉避免污染台账
                    except OSError:
                        pass
            if ok:
                kb, pg = _pdf_meta(path)
                w["pdf_source_url"] = url
                w["pdf_size_kb"] = kb
                w["pdf_pages"] = pg
                w["local_pdf_path"] = path
                w["pdf_via"] = "scihub_local"
                w.pop("pdf_download_note", None)
                stats["scihub_ok"] = stats.get("scihub_ok", 0) + 1
                stats["ok"] += 1
                self._log(f"[scihub] OK saved -> {_safe_filename(doi)} "
                          f"(trust=低·用户自担)")
            else:
                w["pdf_download_note"] = "scihub resolved but download/validate failed"
                self._log(f"[scihub] FAIL -> {_safe_filename(doi)}")

    # ── coze 统一传送（主路径，只做一次）──
    def _call_coze_unified(self, items: List[str]) -> Optional[List[Dict[str, Any]]]:
        """一次 coze 传送（统一契约）：输入统一标识列表（OA 直链或 DOI 混排），
        coze 端解码 + A→B 后，返回每篇记录（含 key / pdf_url / pdf_s3_url / status）。
        只传送一次；下载失败由 run() 标记 manual，不重发（符合「只做一次 coze 传送」）。
        请求失败 / 无结果返回 None（交由 _local_fallback）。
        """
        if not items:
            return []
        payload = {
            "source": "publisher_pdf_batch",
            "keyword": json.dumps(items, ensure_ascii=False),
            "mode": "search",
            "query_origin": _query_origin(),
            # ct-base coze_io_contract §1.2：技能版本号 = 顶层信封字段（与 query_origin 同级，禁止嵌套）
            "skill_version": _skill_version(),
            # ct-base coze_io_contract §1.1：locale = 界面/输出语言（顶层信封输出开关）
            "locale": _resolve_locale(),
            # ct-base coze_io_contract §1.1：user_language（输入语言提示）规范承载位 = 请求 params
            "params": {"user_language": _resolve_user_language()},
        }
        # request_id（2026-11-13）：顶层信封，旧端点 extra='ignore' 静默忽略；
        # 独立直驱脚本（dl_top10.py 等）不传 ID 时不写该字段，行为不变。
        if self.request_id:
            payload["request_id"] = self.request_id
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(CT_SEARCH_ENDPOINT, data=body,
                                     headers=_headers(), method="POST")
        # 流式调用：stream_run 以 SSE 实时返回节点事件（workflow_start/node_end/workflow_end…），
        # 适合耗时较长的 PDF 批量下载——避免长连接被网关按单响应超时掐断。
        # 本地解析 SSE，从 workflow_end（或 node_end）事件提取最终 projects。
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                projects = _parse_coze_stream(r, self._log)
        except Exception as e:
            self._log(f"[coze] 流式传送失败: {type(e).__name__}: {e}")
            self._cb_coze.record("coze", ok=False)
            return None
        if projects is None:
            self._log("[coze] 流式响应未解析到 projects（可能 rejected / 执行失败）")
            self._cb_coze.record("coze", ok=False)
            return None
        self._cb_coze.record("coze", ok=True)
        return projects

    # ── 本地兜底解码（coze 不可用 / skip_coze）──
    def _local_fallback(self, items: List[str],
                        work_by_key: Dict[str, Any]) -> List[Dict[str, Any]]:
        """coze 不可用时的本地兜底：仅能拿到 Europe PMC 非 Cloudflare 副本并直下；
        其余（付费墙/重定向器/Cloudflare 出版商）本地无浏览器，标记 manual。
        """
        out = []
        for key in items:
            w = work_by_key.get(key, {}) or {}
            doi = (w.get("doi") or "") or _extract_doi_from_url(key) or ""
            url = None
            if doi:
                epmc = self._epmc_lookup_pdf_url(doi, w.get("pmcid") or "", w.get("pmid") or "")
                if epmc:
                    url = epmc
            # Sci-Hub 可选兑底（2026-10-26）：Europe PMC 也拿不到且用户显式开启时，
            # skip-coze 场景下仍有一线回收机会（默认关闭时完全不改变原行为）。
            via = "epmc_local"
            if url is None and doi and self.use_scihub and not self._cb_scihub.is_open("scihub"):
                su = self._scihub_lookup(doi)
                if su:
                    url, via = su, "scihub_local"
            if url:
                out.append({"key": key, "doi": doi, "pdf_url": url, "pdf_s3_url": None,
                            "status": "ok", "via": via})
            else:
                out.append({"key": key, "doi": doi, "pdf_url": None, "pdf_s3_url": None,
                            "status": "manual",
                            "error": "本地无浏览器，且无 Europe PMC 副本"})
        return out

    # ── 本地预筛（2026-09-07）：coze 改为「本地逐项预筛后的最后手段」──
    # 路由规则（用户 2026-09-07）：
    #   ① 本地可直接处理/下载的预印本直链 → 本地下载，不送 coze；
    #   ② 非 OA 论文：本地查有无更早预印本，有则本地下载，否则也不送 coze；
    #   ③ 仅当「本地无法直接下载」且「有 OA 或预印本链接」时才送 coze。
    def _upw_look(self, doi: str) -> Optional[Dict[str, Any]]:
        """查 Unpaywall（按 DOI），返回解析后的 JSON dict；不可达/异常返回 None（未知）。

        返回 None 表示「查询未成功」（网络/超时/429/熔断），此时路由应保守地回退到
        coze，而非判定为「无 OA」直接跳过——避免误杀可下载文献。
        命中 200（含 is_oa=false 的闭源论文）正常返回 dict；结果按 DOI 缓存整轮复用。
        熔断（2026-10-25）：本源连续失败达阈值后直接返回 None（不再发请求）。
        """
        if not doi:
            return None
        if self._cb.is_open("unpaywall"):
            return None
        if doi in self._upw_cache:
            return self._upw_cache[doi]
        try:
            u = "https://api.unpaywall.org/v2/%s?email=%s" % (
                urllib.parse.quote(doi), urllib.parse.quote(self._upw_email))
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (research audit)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.loads(r.read().decode("utf-8"))
            self._upw_cache[doi] = d
            self._cb.record("unpaywall", ok=True)
            return d
        except urllib.error.HTTPError as e:
            if e.code == 429:
                self._cb.record("unpaywall", ok=False, force_open=True)
                self._log("[unpaywall] 被限流(429)，熔断本源")
            else:
                self._cb.record("unpaywall", ok=False)
            self._upw_cache[doi] = None
            return None
        except Exception:
            self._cb.record("unpaywall", ok=False)
            self._upw_cache[doi] = None
            return None

    def _prefetch_unpaywall(self, works: List[Dict[str, Any]]):
        """并发预取所有可能需要 Unpaywall 信号的 DOI（受 _UPW_CONCURRENCY 限流）。"""
        import concurrent.futures as _cf
        dois = []
        for w in works:
            doi = (w.get("doi") or "").strip()
            if not doi or doi in self._upw_cache:
                continue
            oa = (w.get("open_access_url") or "").strip()
            pp = w.get("preprint")
            if oa and _looks_like_direct_pdf(oa):
                continue
            if isinstance(pp, dict) and pp.get("url") and _looks_like_direct_pdf(pp["url"]):
                continue
            dois.append(doi)
        if not dois:
            return
        sem = threading.Semaphore(_UPW_CONCURRENCY)

        def _one(d: str):
            with sem:
                self._upw_look(d)

        with _cf.ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(_one, dois))

    def _work_is_oa(self, w: Dict[str, Any]) -> bool:
        """work 是否带 OA 信号（直接字段，优先用上游已算好的 is_oa / oa_status）。"""
        if w.get("is_oa"):
            return True
        oa = w.get("oa_status")
        if isinstance(oa, str) and oa.lower() in ("gold", "green", "bronze", "hybrid"):
            return True
        return False

    def _find_earlier_preprint(self, doi: str, title: str, work: Dict[str, Any] = None,
                               skip_coze: bool = False):
        """本地查找「可下载的更早预印本 / OA 直链」。返回 (kind, url) 或 None。

        kind ∈ {"oa", "preprint"}：二者都直接可本地下载，区别仅用于统计/日志。
          - oa：Unpaywall 返回的 OA 直链（url_for_pdf），本地查询身份确定，不需校验；
          - preprint：Europe PMC PPR 按标题检索到的预印本 PDF（bioRxiv/medRxiv/arXiv 等），
            候选按标题命中需作者级同篇校验——该「同篇判定」策略 2026-10-26 上移 coze
            lit_preprint_check（宁可缺漏不能弄错），本地只负责检索候选 + 批量送校验。

        纯薄客户端：coze lit_preprint_check 不可用 → 不下载任何预印本候选（宁可缺漏）；
        skip_coze → 不调用云端校验（无本地兜底）。kind=oa 按 DOI 定位，身份确定，不需校验。
        """
        # 1) Unpaywall：OA 直链（url_for_pdf）优先（本地查询，不需校验）
        d = self._upw_look(doi) if doi else None
        if d is not None and d.get("is_oa"):
            loc = d.get("best_oa_location") or {}
            u = loc.get("url_for_pdf") or loc.get("pdf_url")
            if u and _looks_like_pdf_url(u):
                return ("oa", u)
        # 2) Europe PMC PPR 按标题检索更早预印本（本地检索候选）
        if title and not skip_coze:
            try:
                from adapters.preprint_fallback import _epmc_preprint_search, \
                    _lastnames_from_authors
                cands = _epmc_preprint_search(title)
                if not cands:
                    return None
                orig_ln = _lastnames_from_authors((work or {}).get("authors") or [])
                if not orig_ln:
                    # 宁可缺漏：原文献无作者可校验 → 不下载任何标题命中的预印本候选
                    if work is not None:
                        work["pdf_download_note"] = (
                            "preprint candidate(s) found but skipped: missing_author_info "
                            "(author-level check, 宁可缺漏不能弄错)")
                    return None
                # 收集候选，批量送 coze lit_preprint_check 做同篇判定（「宁可缺漏不能弄错」）
                checks = []
                for c in cands:
                    cu = c.get("pdf_url")
                    if cu and _looks_like_pdf_url(cu):
                        checks.append({"title": title,
                                       "candidate": {"url": cu, "authors": c.get("authors") or []},
                                       "authors": work.get("authors") or []})
                if not checks:
                    return None
                from adapters._coze_strategy import call_coze_strategy
                final = call_coze_strategy("lit_preprint_check", checks, log_fn=self._log)
                if final is None:
                    # 纯薄客户端：coze 不可用 → 特征不可用 → 不下载预印本（宁可缺漏）
                    # fail-loud：记账「判不出来」，与「作者校验拒绝」区分开
                    self._strategy_unavailable["lit_preprint_check"] = (
                        self._strategy_unavailable.get("lit_preprint_check", 0) + 1)
                    self._log("[preprint][FATAL] coze lit_preprint_check 不可用："
                              f"{len(checks)} 条预印本候选未获同篇校验，按「宁可缺漏不能弄错」"
                              "不下载（服务故障，非「校验拒绝」）")
                    if work is not None:
                        work["pdf_download_note"] = (
                            "preprint candidate(s) found but coze lit_preprint_check "
                            "unavailable; skipped")
                    return None
                for r in final.get("projects", []):
                    if r.get("passed"):
                        return ("preprint", r.get("url"))
                    self._log(f"[preprint] author-check REJECT ({r.get('reason')}): {r.get('url')}")
                if work is not None:
                    work["pdf_download_note"] = (
                        "preprint candidate(s) rejected by author check (coze lit_preprint_check)")
            except Exception as e:
                self._log(f"[preprint] coze 同篇校验异常: {e}")
        return None

    def _epmc_lookup_pmcid(self, doi: str = "", title: str = "", pmid: str = "") -> Optional[str]:
        """按 DOI/TITLE/PMID 解析 Europe PMC 的 PMCID（本地回退预取用）。

        命中且有全文副本才返回 pmcid；429 立即熔断本源、503/504 退避重试、
        其它异常记失败（连续达阈值熔断）。复用同一熔断器（src="epmc"）。
        """
        if self._cb.is_open("epmc"):
            return None
        if not (doi or title or pmid):
            return None
        for attempt in range(4):
            if self._cb.is_open("epmc"):
                return None
            try:
                _epmc_ratelimit()
                if doi:
                    q = f"DOI:{urllib.parse.quote(doi)}"
                elif pmid:
                    q = f"PMID:{urllib.parse.quote(str(pmid))}"
                else:
                    q = f'TITLE:"{urllib.parse.quote((title or "")[:180])}"'
                api = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                       f"?query={q}&format=json&resultType=core&pageSize=3")
                req = urllib.request.Request(api, headers={"User-Agent": "ct-literature-skill/1.0"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    data = json.loads(r.read().decode("utf-8"))
                self._cb.record("epmc", ok=True)
                for res in (data.get("resultList") or {}).get("result", [])[:3]:
                    pc = res.get("pmcid")
                    if pc and (res.get("hasPDF") or (res.get("fullTextUrlList") or {}).get("fullTextUrl")):
                        return pc
                return None
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    self._cb.record("epmc", ok=False, force_open=True)
                    self._log("[epmc] 被限流(429)，熔断本源：本次运行剩余文献不再查 Europe PMC")
                    return None
                elif e.code in (503, 504):
                    self._log(f"[epmc] 服务端过载 HTTP {e.code}，退避重试({attempt + 1}/3)")
                    time.sleep(2 * (attempt + 1))
                    continue
                else:
                    self._cb.record("epmc", ok=False)
                    return None
            except Exception:
                self._cb.record("epmc", ok=False)
                return None
        return None

    def _oa_via_openalex(self, doi: str) -> Optional[str]:
        """OpenAlex 取 OA 副本直链（locations 中的 PMC 直链 > best_oa > 机构库镜像）。

        覆盖 Europe PMC 未索引的绿色 OA / 机构库镜像，回收率显著更高
        （2026-09-08 实战：KEYNOTE-671 的 Lancet 正式版经 OpenAlex 的 PMC 直链拿到）。
        副本选择优先级：① PMC 直链（pmc.ncbi.nlm.nih.gov，最稳几乎必活）
        ② best_oa_location ③ 其余 locations 中的 pdf 直链（机构库镜像，可能 404，作兜底）。
        熔断（2026-10-25）：本源连续失败达阈值后直接返回 None（不再发请求）。
        """
        if not doi:
            return None
        if self._cb.is_open("openalex"):
            return None
        try:
            d = _http_json("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))
            if not d:
                # 查询未成功（网络/超时/429）——记失败由熔断器裁决；
                # 保守起见仍返回 None（路由会回退 coze，不会误判「无 OA」）。
                self._cb.record("openalex", ok=False)
                return None
            self._cb.record("openalex", ok=True)
            locs = (d.get("locations") or [])
            # ① 真直链优先（2026-10-27 修复顺序）：先取 locations 里真正的 pdf_url。
            #    旧版把 Europe PMC 的 ?pdf=render 排在最前直接返回，实测该通道本地
            #    必被 Cloudflare 拦（r1 24 篇 preprint_local 全 FAIL），而真正的
            #    medRxiv / Nature 直链被它挡住永远用不到。实测这 9 篇因此可救回。
            bo = d.get("best_oa_location") or {}
            u = bo.get("pdf_url")
            if (u and _looks_like_pdf_url(u) and not _is_epmc_render(u)
                    and not _is_aux_pdf(u)):
                return u
            for loc in locs:
                lu = loc.get("pdf_url") or ""
                # 只用 pdf_url：旧版回落 landing_page_url 会把「文章页」当直链返回，
                # 下载必然拿到 HTML（同样是一次无效尝试）。
                if (lu and _looks_like_pdf_url(lu) and not _is_epmc_render(lu)
                        and not _is_aux_pdf(lu)):
                    return lu
            # ② Europe PMC 渲染通道降为最后兜底（唯一副本时才用；本地大概率被拦，
            #    失败后仍由 run() 交给 coze 处理，不额外劣化）。
            for loc in locs:
                lu = loc.get("pdf_url") or loc.get("landing_page_url") or ""
                m = re.search(r"pmc\.ncbi\.nlm\.nih\.gov/articles/PMC(\d+)", lu)
                if m:
                    return "https://europepmc.org/articles/PMC%s?pdf=render" % m.group(1)
            return None
        except Exception:
            return None

    def _prefetch_identifiers(self, works: List[Dict[str, Any]]):
        """run() 起始预取：为每篇补全 doi / pmcid / openalex_oa 三类本地可用标识，整轮缓存复用。

        ① 标题→DOI（仅当原 work 缺 doi）；② PMCID（Europe PMC，填充后渲染通道免 API 调用）；
        ③ OpenAlex OA 直链（仅当没有现成可用的非 WAF 直链时才补齐，避免冗余查询）。
        全部只读查询，不送 coze；失败静默跳过（路由保守回退 coze）。
        """
        for w in works:
            title = (w.get("title") or "").strip()
            year = w.get("year") or _year_from_date(w.get("publication_date"))
            # ① 标题→DOI（Crossref + OpenAlex 双通道；中文题名主要靠 OpenAlex）
            if not (w.get("doi") or "").strip() and title:
                doi, _ = _resolve_doi_from_title(title, year,
                                                 author=_first_author_name(w))
                if doi:
                    w["doi"] = doi
            doi = (w.get("doi") or "").strip()
            # ② PMCID（Europe PMC）：仅按 DOI/PMID 查（具体可靠），不按通用标题猜，
            #    避免 Europe PMC TITLE 检索撞同名论文导致错下（anti-hallucination）。
            if not (w.get("pmcid") or "").strip() and (doi or (w.get("pmid") or "")):
                pc = self._epmc_lookup_pmcid(doi=doi, pmid=(w.get("pmid") or ""))
                if pc:
                    w["pmcid"] = pc
                else:
                    w["_epmc_checked"] = True   # 标记已查无副本，classify 不再重复查
            # ③ OpenAlex OA（有现成非 WAF 直链则跳过，省一次查询）
            if (doi and not (w.get("_oa_openalex") or "")
                    and not (w.get("open_access_url") and _looks_like_direct_pdf(w["open_access_url"])
                              and not _is_waf_host(w["open_access_url"]))):
                u = self._oa_via_openalex(doi)
                if u:
                    w["_oa_openalex"] = u

    def _explicit_non_oa(self, doi: str) -> bool:
        """Unpaywall 明确判定为非 OA（可达且 is_oa=False）。仅此情形触发红线 skip。
        返回 None（查询未成功 / 不可达）时路由应保守地回退到 coze，而非判定为非 OA。
        """
        if not doi:
            return False
        upw = self._upw_cache.get(doi)
        return isinstance(upw, dict) and not upw.get("is_oa")

    def _resolve_landing_pdf(self, doi: str, url: str) -> Optional[str]:
        """站点 profile 模板 + 通用 landing 页解析，返回最佳 PDF 直链或 None。

        顺序（知识参考 zotero/translators，实现自研）：
          A. 站点模板：先按落地页域名，未命中再按 DOI 前缀（url 可为空）
             → 直接构造（不抓页，绕 WAF）；
          B. landing 页可达且非反爬 → citation_pdf_url / link-pdf / 锚点扫描。
        每次尝试写遥测（.pdf_resolver_log.jsonl），供后续按域名统计命中率。
        """
        doi_bare = _bare_doi(doi) if doi else ""
        url = (url or "").strip()

        if url and _host_of(url) in ("doi.org", ""):
            # 跟进 DOI 跳转器拿真实落地页（2026-10-27：OpenAlex / open_access_url
            # 常给 doi.org，此处若不展开，后面所有 profile / 抓页逻辑都会空转）。
            url = _follow_to_landing(url) or ""

        domain = _host_of(url) if url else ""

        # A. 站点专用模板（如 Frontiers {base}/articles/{doi}/pdf）
        #    2026-10-27：url 为空时用 DOI 前缀兜底匹配 —— 真实检索里大量条目的
        #    open_access_url 是空的，此前一律 return None，导致 10.3389/* 可直下的
        #    文章被漏掉（实测模板 URL 返回 200 + %PDF）。
        key, prof = _profile_for(url) if url else (None, {})
        if not (key and prof.get("url_template")):
            dkey, dprof = _profile_for_doi(doi_bare)
            if dkey:
                key, prof = dkey, dprof
                if not domain:
                    domain = key
        if prof.get("url_template") and doi_bare:
            try:
                tpl = prof["url_template"].format(doi=doi_bare)
            except Exception:
                tpl = ""
            if tpl:
                _telemetry_pdf_resolve(self.out_dir, doi, domain,
                                       "profile_template", tpl, "constructed")
                return tpl

        # B. 通用 landing 页解析（反爬 / 明确禁止抓页的域名跳过）
        if not url:
            _telemetry_pdf_resolve(self.out_dir, doi, domain,
                                   "landing", "", "no_url")
            return None
        if prof.get("landing_fetch") is False or _is_anti_scrape(url):
            _telemetry_pdf_resolve(self.out_dir, doi, domain,
                                   "landing", url, "skipped_profile")
            return None
        try:
            html = _get(url, timeout=30, retries=1).decode("utf-8", "replace")
        except Exception as e:
            _telemetry_pdf_resolve(self.out_dir, doi, domain,
                                   "landing", url, "fetch_error:%s" % type(e).__name__)
            return None
        cands = _extract_pdf_candidates(html, url)
        if not cands:
            _telemetry_pdf_resolve(self.out_dir, doi, domain,
                                   "landing", url, "no_candidate")
            return None
        # 择优：meta/link 命中的第一条直接回；锚点候选逐条交给下载器验证
        # （这里只回 URL，下载失败由 run() 的既有失败路径兜底）。
        for u, layer in cands:
            _telemetry_pdf_resolve(self.out_dir, doi, domain, layer, u,
                                   "candidate")
            if layer != "landing_anchor":
                return u
        return cands[0][0]

    def _classify(self, w: Dict[str, Any], skip_coze: bool) -> Tuple[str, Any]:
        """单篇路由分类（2026-10-26 重构：本地多级 OA 回退优先，路由决策上移 coze）。

        返回 (kind, val)。kind ∈ {local_direct, local_preprint, coze, _route, skip}：
          - local_direct / local_preprint：本地动作已拿到可下直链，val=URL（本地直下）；
          - coze：skip_coze 模式下仍按旧语义标记待云端下载（由 skip_coze 流程统一不下载）；
          - _route：本地多级回退全部失败，val=决策信号 dict（key/doi/is_oa/
            has_local_signal/explicit_non_oa 等），交由 run() 批量送 coze lit_route
            做「红线 + 信号」判定（纯薄客户端：coze 不可用 → 该批统一判 skip，无本地兜底）；
          - skip：明确非 OA 且无本地信号（仅 skip_coze 路径或 coze 判 skip 后落入）。

        本地优先链（纯标准库，不送云端）：
          ① Europe PMC 渲染通道  ② OpenAlex OA 直链  ③ 非 WAF 主机直链
          ④ Unpaywall OA 直链 / 更早预印本（作者级同篇校验已上移 coze lit_preprint_check）
          ⑤ WAF 出版商直链（仍试一次本地，失败再交 coze 路由）
        「非 OA 不送云端」红线 + 信号组合判定 → 上移 coze lit_route（源码保护）。
        """
        oa = (w.get("open_access_url") or "").strip()
        doi = (w.get("doi") or "").strip()
        pmcid = (w.get("pmcid") or "").strip()
        pmid = (w.get("pmid") or "").strip()
        title = (w.get("title") or "").strip()
        is_oa = self._work_is_oa(w)

        # ① OpenAlex OA 真直链（2026-10-27 前置，原为 ②）
        #    实测依据：Europe PMC 的 ?pdf=render 本地必被 Cloudflare 拦
        #    （r1 24/24 失败、r3 13/13 失败），而 OpenAlex locations 里的
        #    medRxiv / Nature / 机构库直链可直接下（5.2MB/65页、32MB/37页等）。
        #    旧顺序把 render 放在第一位，把真直链永久挡在后面。
        oax = w.get("_oa_openalex") or (self._oa_via_openalex(doi) if doi else None)
        if oax:
            return ("local_preprint", oax)

        # ② 非 WAF 主机的 OA/预印本直链 → 本地直下
        if oa and _looks_like_direct_pdf(oa) and not _is_waf_host(oa):
            return ("local_direct", oa)

        # ④ Unpaywall OA 直链 / 更早预印本（作者级同篇校验已上移 coze lit_preprint_check）
        lp = self._find_earlier_preprint(doi, title, work=w, skip_coze=skip_coze)
        if lp:
            return ("local_preprint", lp[1])

        # ⑤ WAF 出版商直链：仍试一次本地（OA 子集偶可达），失败再交 coze 路由
        if oa and _looks_like_direct_pdf(oa):
            return ("local_direct", oa)

        # ⑤.5 landing 页解析（2026-10-27 新增，知识参考 zotero/translators）：
        # oa 是 landing 页（非直链）时，抓 citation_pdf_url 等元标签 /
        # 站点 profile 模板构造直链。红线内才做（明确非 OA 不白抓页面）；
        # coze 路由红线判定用 explicit_non_oa，此处用 is_oa / preprint 信号
        # 同步对齐，避免为注定 skip 的条目多花一次页面抓取。
        landing_ok = bool(oa) and not _looks_like_direct_pdf(oa)
        # 2026-10-27 扩展：oa 为空时，只要 DOI 前缀命中站点模板（如 10.3389/*）也试一次。
        # 模板构造不抓页面（零请求成本），而实测这类条目的模板 URL 返回 200 + %PDF，
        # 此前因「oa 必须非空」被整批漏掉（r1+r2 共 38/82 篇 oa 为空）。
        has_tpl = bool(doi) and bool(_profile_for_doi(doi)[1].get("url_template"))
        non_oa_blocked = bool(doi) and self._explicit_non_oa(doi)
        if (landing_ok or has_tpl) and (is_oa or w.get("preprint")) and not non_oa_blocked:
            cand = self._resolve_landing_pdf(doi, oa)
            if cand:
                return ("local_direct", cand)

        # ⑤.9 Europe PMC 渲染通道：降为最后兜底（2026-10-27 由原 ① 下移）。
        # 实测该通道本地被 Cloudflare 拦（r1 24/24、r3 13/13 全失败），
        # 只在「有 PMCID 但所有真直链都不存在」时使用——聊胜于无，
        # 失败后仍由 ⑥ 交 coze，不额外劣化。
        if pmcid:
            return ("local_preprint", f"https://europepmc.org/articles/{pmcid}?pdf=render")
        if (doi or pmid) and not w.get("_epmc_checked"):
            epmc = self._epmc_lookup_pdf_url(doi=doi, pmid=pmid)
            if epmc:
                return ("local_preprint", epmc)

        # ⑥ 本地全失败。路由决策（红线 + 信号组合）上移 coze lit_route（源码保护）。
        # skip_coze 模式下不调用云端：维持旧语义，仍标记为 coze 待下载，
        # 由 skip_coze 流程统一不下载（与旧行为一致）。
        if skip_coze:
            return ("coze", oa or doi)
        has_local_signal = bool(oa) or bool(w.get("preprint"))
        return ("_route", {
            # 决策信号（coze lit_route 据以判定 local_direct/local_preprint/coze/skip）
            "key": oa or doi,
            "doi": doi,
            "is_oa": is_oa,
            "has_local_signal": has_local_signal,
            "preprint_found": False,      # ④ 已失败
            "has_direct_oa": False,       # ①②③⑤ 已失败
            "explicit_non_oa": self._explicit_non_oa(doi),
        })

    # ── Excel 自动回写（下沉职责，run() 正常结束后调用）──
    def _write_back_xlsx(self, works: List[Dict[str, Any]]) -> str:
        """下载完成后把 PDF 本地路径写回 Excel「PDF 本地路径」列。

        此前该步骤只在主流程 ct_literature.py 内联实现，独立直驱 PdfDownloader
        的脚本（如 dl_top10.py / dl_latest40.py）一旦漏调 update_xlsx_pdf_paths.py
        就会出现「PDF 已下载却没写进 lit_report.xlsx」的错位（用户 2026-09-08 反馈）。
        现把回写下沉到下载器自身：构造时给了 xlsx_out，run() 结束即自动重渲。

        返回被更新的 xlsx 绝对路径；未配置 xlsx_out 或失败时返回 ""。
        """
        if not self.xlsx_out:
            return ""  # 未配置目标 Excel → 不做回写（独立测试 / 仅下载场景）
        try:
            import sys as _sys
            # pdf_download.py 在 adapters/，export_xlsx.py 在 scripts/：确保可 import
            _scripts = os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "scripts")
            if _scripts not in _sys.path:
                _sys.path.insert(0, _scripts)
            from export_xlsx import export_workbook
            meta = {}
            if self.merged_json and os.path.isfile(self.merged_json):
                try:
                    with open(self.merged_json, encoding="utf-8") as _f:
                        meta = (json.load(_f) or {}).get("meta") or {}
                except Exception as _me:
                    self._log(f"[xlsx] read merged meta failed (ignored): {_me}")
            # 落盘路径可能相对 self.out_dir → 统一绝对路径再写入（与主流程一致）
            for _w in works:
                if _w.get("local_pdf_path"):
                    _w["local_pdf_path"] = os.path.abspath(_w["local_pdf_path"])
            _safety = self.safety if self.safety is not None else bool(meta.get("safety"))
            export_workbook({"count": len(works), "works": works, "meta": meta},
                            self.xlsx_out, lang=self.lang, safety=_safety)
            self._log(f"[OK] xlsx 已更新：PDF 本地路径已写入「PDF 本地路径」列 -> {self.xlsx_out}")
            return os.path.abspath(self.xlsx_out)
        except Exception as _xe:
            self._log(f"[WARN] xlsx 回写 PDF 路径失败（不影响已下载的 PDF）: {_xe}")
            return ""

    def _write_back_citations(self, works: List[Dict[str, Any]]) -> str:
        """题录回写：把 PDF 绝对路径写回 references.bib / references.ris / references_<style>.md。

        与 _write_back_xlsx 同口径（用户 2026-09-21）：下载器自身在 run() 结束自动重渲，
        避免「PDF 已下载却没写进题录」（此前仅主流程内联、独立直驱路径易漏）。
        需要构造时给定 citations_out_dir（题录落盘目录，通常为 out_dir）才生效；否则跳过。
        返回被更新的任一题录文件绝对路径；未配置或失败时返回 ""。
        """
        if not self.citations_out_dir:
            return ""
        try:
            import sys as _sys
            _scripts = os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))), "scripts")
            if _scripts not in _sys.path:
                _sys.path.insert(0, _scripts)
            from format_citations import export_citations
            # 落盘路径可能相对 self.out_dir → 统一绝对路径再写入（与 _write_back_xlsx 一致）
            for _w in works:
                if _w.get("local_pdf_path"):
                    _w["local_pdf_path"] = os.path.abspath(_w["local_pdf_path"])
            _res = export_citations(
                {"count": len(works), "works": works},
                style=self.citation_style or "apa",
                out_dir=self.citations_out_dir, lang=self.lang)
            _bib = _res.get("bib_path") or ""
            self._log(f"[OK] 题录已更新：PDF 绝对路径已写入 references.bib / .ris / "
                      f".md -> {_bib}")
            return os.path.abspath(_bib) if _bib else ""
        except Exception as _ce:
            self._log(f"[WARN] 题录回写 PDF 路径失败（不影响已下载的 PDF）: {_ce}")
            return ""

    # ── 下载台账（2026-10-25，参考 academic-fulltext-fetcher 的 manifest.csv）──
    def _write_manifest(self, works: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
        """产出 pdf_manifest.csv 下载台账（UTF-8 BOM，Excel 可直接打开）。

        字段：序号 / 题名 / DOI / 来源类型 / 来源URL / 状态 / 本地路径 / 大小KB /
        页数 / source_trust。与 batch 层 batch_manifest.json 对齐，作为 PDF 下载的
        独立审计产物：哪篇从哪个 URL、经哪条通道、什么信任级拿到（或为何失败）。

        落点：xlsx_out 同目录（运行根目录）；无 xlsx_out 时退到 out_dir 的父目录。
        失败行「本地路径」列写失败原因（与文章技能同口径）。
        """
        try:
            import csv
            if self.xlsx_out:
                base = os.path.dirname(os.path.abspath(self.xlsx_out))
            else:
                base = os.path.dirname(os.path.abspath(self.out_dir)) or "."
            path = os.path.join(base, "pdf_manifest.csv")
            rows = []
            for i, w in enumerate(works, 1):
                via = w.get("pdf_via") or ""
                label = _VIA_LABEL.get(via, via or "未路由")
                trust = _VIA_TRUST.get(via, "未知")
                p = w.get("local_pdf_path")
                note = w.get("pdf_download_note") or ""
                if p:
                    status = "已存在" if w.get("pdf_existed") else "成功"
                    local = os.path.abspath(p)
                elif note.startswith("no DOI"):
                    status, local = "跳过", note
                elif "non-OA" in note:
                    status, local = "跳过", note
                elif "rejected" in note or stats.get("rejected"):
                    status, local = "拒绝", note or stats.get("rejected_reason", "")
                else:
                    status, local = "失败", note or "未下载"
                kb = w.get("pdf_size_kb")
                pg = w.get("pdf_pages")
                rows.append([
                    i,
                    (w.get("title") or "")[:120],
                    (w.get("doi") or "").strip(),
                    label, w.get("pdf_source_url") or "",
                    status, local,
                    ("" if kb is None else kb),
                    ("" if pg is None else pg),
                    trust,
                ])
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                wcsv = csv.writer(f)
                wcsv.writerow(["序号", "题名", "DOI", "来源类型", "来源URL",
                               "状态", "本地路径", "大小KB", "页数", "source_trust"])
                wcsv.writerows(rows)
            self._log(f"[OK] 下载台账已生成 -> {path}")
            return os.path.abspath(path)
        except Exception as _me:
            self._log(f"[WARN] pdf_manifest.csv 生成失败（不影响已下载的 PDF）: {_me}")
            return ""

    def run(self, works: List[Dict[str, Any]], skip_coze: bool = False) -> Dict[str, Any]:
        """Batch PDF download (four-bucket routing: local direct / local preprint / coze / skip).

        Routing rules (user 2026-09-07):
          - local-direct PDF (preprint / OA direct link via _looks_like_direct_pdf) -> local_direct, no coze
          - non-OA paper: first check local "earlier preprint / OA direct link" (_find_earlier_preprint);
            if found -> local_preprint local download; if not and no OA/preprint signal -> skip (no coze)
          - only when "cannot download locally" AND "has OA or preprint link" -> coze decode
        Speed arch (2026-09-19 fix): coze decode thread is started BEFORE the local download
        phase, so decode and download genuinely overlap; each coze sub-batch pipes its links
        straight into the concurrent downloader. The "local failed -> coze retry" pass waits on
        _local_phase_done so it still runs after the main batches (no endpoint contention).
        """
        stats = {"total": len(works), "ok": 0, "coze_sent": 0,
                 "coze_ok": 0, "manual_needed": 0, "failed": 0,
                 "skipped_no_id": 0, "skipped_no_oa": 0, "batches": 0,
                 "local_direct": 0, "local_preprint": 0,
                 "local_fallback_coze_sent": 0, "local_fallback_coze_ok": 0,
                 "scihub_tried": 0, "scihub_ok": 0,
                 # fail-loud（2026-10-27）：因 coze 策略节点不可用而未能判定/下载的篇数。
                 # 与 skipped_no_oa 分离记账——后者是「判定为非 OA」，前者是「判不出来」。
                 "route_unavailable": 0, "preprint_check_unavailable": 0}

        # 0) batch timing (user 2026-09-07: every PDF batch reports elapsed time)
        _t_wall = time.strftime("%Y-%m-%dT%H:%M:%S")
        _t_mono = time.monotonic()

        # 1) hard cap (user 2026-09-06): >MAX_TOTAL_ITEMS rejected, never split
        if len(works) > MAX_TOTAL_ITEMS:
            stats["rejected"] = True
            stats["rejected_reason"] = (
                f"download {len(works)} items exceeds single-run cap {MAX_TOTAL_ITEMS}; "
                f"splitting serially would always time out. Narrow scope: "
                f"top-{MAX_TOTAL_ITEMS} by citations / single source / multiple small batches.")
            self._log(f"[PDF] rejected: {len(works)} > cap {MAX_TOTAL_ITEMS}. {stats['rejected_reason']}")
            for w in works:
                w["local_pdf_path"] = None
                w["pdf_download_note"] = stats["rejected_reason"]
            stats["started_at"] = _t_wall
            stats["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            stats["elapsed_s"] = round(time.monotonic() - _t_mono, 1)
            stats["elapsed_min"] = round(stats["elapsed_s"] / 60.0, 2)
            return stats

        import threading as _th
        stats_lock = _th.Lock()

        # 2) prefetch Unpaywall (local prescreen; classify reuses cache)
        self._prefetch_unpaywall(works)
        # 2b) prefetch local OA identifiers (doi/pmcid/openalex_oa) — 本地多级回退前置
        self._prefetch_identifiers(works)
        # 2c) build cache_map (2026-10-26, 三级缓存复用):
        #     扫描 pdf_dir 现有文件 → {stem: path}，下载前命中即跳过。
        if self._enable_cache:
            self._cache_map = _build_cache_map(self.out_dir)
            if self._cache_map:
                self._log(f"[pdf] cache_map built: {len(self._cache_map)} existing PDFs in {self.out_dir}")

        # 3) classify into buckets (local-first prescreen)
        work_by_key: Dict[str, Any] = {}
        local_tasks = []      # (url, doi, work, label)
        coze_keys: List[str] = []
        coze_work_ids = set()          # 路由到 coze 的 work（id()），4b 据此排除重复兜底
        pending_route: List[Any] = []  # 本地全失败、待批量送 coze lit_route 决策的工作（w, signal）
        for w in works:
            oa = (w.get("open_access_url") or "").strip()
            doi = (w.get("doi") or "").strip()
            key = oa or doi
            if not key:
                w["local_pdf_path"] = None
                w["pdf_download_note"] = "no DOI / OA, cannot download"
                stats["skipped_no_id"] += 1
                continue
            kind, val = self._classify(w, skip_coze)
            if kind == "local_direct":
                local_tasks.append((val, doi or val, w, "oa_direct_local"))
                w["pdf_via"] = "oa_direct_local"  # 预置，下载失败时 local_failed_keys 收集才能识别
                stats["local_direct"] += 1
            elif kind == "local_preprint":
                local_tasks.append((val, doi or val, w, "preprint_local"))
                w["pdf_via"] = "preprint_local"
                stats["local_preprint"] += 1
            elif kind == "coze":
                # skip_coze 模式：保持旧语义，标记待云端下载（由 skip_coze 流程统一不下载）
                coze_keys.append(val)
                work_by_key[val] = w
                coze_work_ids.add(id(w))
            elif kind == "_route":
                # 本地多级回退全失败 → 暂存决策信号，循环后批量送 coze lit_route
                pending_route.append((w, val))
            else:  # skip: non-OA and no preprint -> do NOT call coze
                w["local_pdf_path"] = None
                w["pdf_download_note"] = "non-OA and no usable preprint; skip cloud decode (per rule)"
                stats["skipped_no_oa"] += 1

        # ── 批量送 coze lit_route 做路由决策（纯薄客户端：无本地兜底）──
        # 循环内只跑本地动作；达「本地全失败」的文献集中一次 coze 调用判定 coze/skip，
        # 既护源码（红线+信号组合逻辑在 coze 端）又避免逐篇打端点。
        if pending_route and not skip_coze:
            from adapters._coze_strategy import call_coze_strategy
            signals = [sig for _, sig in pending_route]
            final = call_coze_strategy("lit_route", signals, log_fn=self._log)
            if final is None:
                # coze 不可用 / 熔断 → 该批无法路由，统一判 skip（feature unavailable，无兜底）
                # fail-loud：这些篇是「判不出来」而非「判定为非 OA」，单独记账 + 醒目日志，
                # 免得用户在统计里只看到 skipped_no_oa 而误以为已做过判定。
                self._log(f"[PDF][FATAL] lit_route coze 不可用：{len(pending_route)} 篇本地不可下文献"
                          f"未获路由判定，暂按 skip 处理（服务故障，非「判定为非 OA」）")
                stats["route_unavailable"] += len(pending_route)
                for w, _ in pending_route:
                    w["local_pdf_path"] = None
                    w["pdf_download_note"] = "route decision unavailable (coze lit_route down); skip"
                    stats["skipped_no_oa"] += 1
            else:
                buckets = {}
                for p in final.get("projects", []):
                    buckets[p.get("key")] = p.get("bucket")
                for w, sig in pending_route:
                    k = sig["key"]
                    b = buckets.get(k)
                    if b == "coze":
                        coze_keys.append(k)
                        work_by_key[k] = w
                        coze_work_ids.add(id(w))
                    else:
                        w["local_pdf_path"] = None
                        w["pdf_download_note"] = (
                            "non-OA and no usable preprint; skip cloud decode (per rule)"
                            if b == "skip" else
                            "route decision=skip (coze lit_route); skip cloud decode")
                        stats["skipped_no_oa"] += 1
        pending_route = []  # 已消费

        # ── fail-loud 汇总（2026-10-27）：coze 策略节点不可用 ≠ 已做判定 ──
        stats["preprint_check_unavailable"] = self._strategy_unavailable.get(
            "lit_preprint_check", 0)
        self._strategy_unavailable["lit_route"] = stats["route_unavailable"]
        if stats["route_unavailable"] or stats["preprint_check_unavailable"]:
            self._log("[PDF][FATAL] coze 策略节点不可用：lit_route 未获路由判定 %d 篇、"
                      "lit_preprint_check 未获同篇校验 %d 篇——这些文献被记为 skip 系"
                      "**服务故障**，而非「判定为非 OA / 作者校验拒绝」。"
                      "请在 lit_* 节点部署/恢复后重跑下载，勿据此认为「本来就下不到」。"
                      % (stats["route_unavailable"],
                         stats["preprint_check_unavailable"]))

        self._log(PDF_DOWNLOAD_NOTICE)
        self._log(f"[PDF] route: local_direct {stats['local_direct']} / local_preprint "
                  f"{stats['local_preprint']} / coze {len(coze_keys)} / "
                  f"skip(nonOA no preprint) {stats['skipped_no_oa']}")

        # ── download helpers ────────────────────────────────────────────────────
        def _coze_anti_scrape_rescue(doi: str, work: Dict[str, Any]) -> Optional[str]:
            """反爬出版商单篇 coze 救援（2026-10-26，参考 meta-analysis _coze_pdf_download）。

            仅当本地直链下载失败且 URL 命中 _ANTI_SCRAPE_HOSTS 时调用。
            委托 ct-search 服务端真实浏览器（publisher_pdf_batch 单元素子批）破反爬。
            coze 熔断时直接返回 None。
            """
            if not doi or self._cb_coze.is_open("coze"):
                return None
            try:
                sub = self._call_coze_unified([doi])
                if sub and sub[0].get("status") == "ok":
                    url = sub[0].get("pdf_s3_url") or sub[0].get("pdf_url")
                    if url:
                        return self._download_direct(url, doi, work)
            except Exception as e:
                self._log(f"[coze-rescue] 异常: {type(e).__name__}: {e}")
            return None

        def _download_one(url: str, doi: str, work: Dict[str, Any], label: str) -> bool:
            host = urlparse(url).netloc
            low = url.lower()
            if "biorxiv.org" in low or "medrxiv.org" in low:
                delay, jitter = self.min_delay, 0.5
            elif "amazonaws" in host or "s3" in host or "cloudfront" in host:
                delay, jitter = 0.1, 0.1
            else:
                delay, jitter = 1.0, 0.3
            self._limiter.acquire(host, delay + random.uniform(0, jitter))
            # 下载前记录「是否已存在」（manifest 区分 成功 / 已存在）
            _existed = os.path.exists(
                os.path.join(self.out_dir, _safe_filename(doi or url)))
            path = self._download_direct(url, doi, work)
            # 反爬出版商救援（2026-10-26）：本地失败 + 命中反爬域名 → 单篇委托 coze
            if path is None and doi and _is_anti_scrape(url):
                self._log(f"[coze-rescue] 反爬出版商 {host} 本地下载失败，委托 coze 单篇救援")
                path = _coze_anti_scrape_rescue(doi, work)
            with stats_lock:
                work["pdf_source_url"] = url      # manifest「来源URL」列
                work["pdf_existed"] = bool(_existed)
                if path:
                    # 大小KB / 页数（深度校验副产品）：让「成功」可审计，
                    # 残篇即使混过校验也能从页数异常暴露。
                    _kb, _pg = _pdf_meta(path)
                    work["pdf_size_kb"] = _kb
                    work["pdf_pages"] = _pg
                    work["local_pdf_path"] = path
                    work["pdf_via"] = label
                    work.pop("pdf_download_note", None)
                    stats["ok"] += 1
                    self._log(f"[pdf] OK {label} saved -> {_safe_filename(doi or url)}")
                    return True
                work["local_pdf_path"] = None
                work["pdf_download_note"] = "download failed (publisher block or network error)"
                self._log(f"[pdf] FAIL {label} -> {_safe_filename(doi or url)}")
                return False

        def _download_batch(recs: List[Dict[str, Any]], label: str):
            tasks = []
            for rec in recs:
                k = rec.get("key") or rec.get("doi") or ""
                w = work_by_key.get(k)
                if not w or w.get("local_pdf_path"):
                    continue
                url = rec.get("pdf_s3_url") or rec.get("pdf_url")
                if rec.get("status") == "ok" and url:
                    tasks.append((url, (w.get("doi") or "").strip() or k, w,
                                  rec.get("via") or label))
            if not tasks:
                return
            ok_n = 0
            with ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKERS) as ex:
                futs = [ex.submit(_download_one, u, d, w, v) for (u, d, w, v) in tasks]
                for f in as_completed(futs):
                    try:
                        if f.result():
                            ok_n += 1
                    except Exception:
                        pass
            self._log(f"[pdf] {label} concurrent download done: {ok_n}/{len(tasks)} ok")

        # ── coze 解码线程：必须在本地下载【之前】启动 ──────────────────────────
        # 旧顺序是「分类 → 本地下载（阻塞跑完）→ 才启动 coze 解码」，虽然 docstring 写着
        # 「local download || coze decode」，实际是本地整段跑完 coze 才发出——用户
        # 2026-09-19 观察到的「先本地搜一遍、再送扣子」白等就在这一段。
        # 线程提前后：coze 与本地下载真正重叠，且每返回一个子批就立刻下载该批直链
        # （P1 流水线），不再攒到末尾统一下载。
        # 「本地下载失败 → coze 兜底重试」必须等本地阶段跑完才知道有哪些失败项，故由
        # _local_phase_done 触发，仍排在主批次之后（也避免与主批次同时打端点）。
        coze_box: Dict[str, Any] = {"projects": None, "done": False}
        local_failed_keys: List[str] = []      # 4b 原地填充；worker 在事件置位后才读
        _local_phase_done = _th.Event()

        def _coze_worker():
            try:
                if skip_coze:
                    coze_box["projects"] = None
                    coze_box["done"] = True
                    return
                collected: List[Dict[str, Any]] = []
                # 主 coze 批次（有 coze_keys 时才执行）
                if coze_keys:
                    subs = [coze_keys[i:i + COZE_SUB_BATCH]
                            for i in range(0, len(coze_keys), COZE_SUB_BATCH)] or [[]]
                    stats["batches"] = len(subs)
                    self._log(f"[coze] bg decode {len(coze_keys)} items ({len(subs)} sub-batches, "
                              f"<= {COZE_SUB_BATCH} each, interval {COZE_BATCH_INTERVAL}s)...")
                    for ci, sub in enumerate(subs, 1):
                        if not sub:
                            continue
                        # coze 端点熔断（2026-10-25）：连续 2 次传送失败即停，
                        # 剩余子批直接走本地兜底，不再白送端点。
                        if self._cb_coze.is_open("coze"):
                            self._log(f"[coze] 端点已熔断（连续失败），剩余子批转本地兜底")
                            part = self._local_fallback(sub, work_by_key)
                            collected.extend(part)
                            _download_batch(part, "coze")
                            continue
                        if ci > 1:
                            # sub-batch 之间强制间隔 ≥ COZE_BATCH_INTERVAL 秒，避免触发限流
                            self._log(f"[coze] waiting {COZE_BATCH_INTERVAL}s before sub-batch {ci}...")
                            time.sleep(COZE_BATCH_INTERVAL)
                        self._log(f"[coze] sub-batch {ci}/{len(subs)}: {len(sub)} items sent...")
                        part = self._call_coze_unified(sub)
                        if part is None:
                            self._log(f"[coze] sub-batch {ci}/{len(subs)} send failed, local fallback")
                            part = self._local_fallback(sub, work_by_key)
                        collected.extend(part)
                        ok_n = len([p for p in part if p.get("status") == "ok"])
                        self._log(f"[coze] sub-batch {ci}/{len(subs)} returned: {ok_n} links -> download now")
                        _download_batch(part, "coze")
                    stats["coze_sent"] = len(coze_keys)
                    self._log(f"[coze] decode done: {len(collected)} records")
                # ── 本地下载失败的条目，送 coze 兜底重试 ──
                # 等本地阶段（分类 → 本地下载 → 4b 收集失败项）走完再发，
                # 否则此刻 local_failed_keys 还是空的。
                _local_phase_done.wait(timeout=1800)
                if local_failed_keys:
                    self._log(f"[coze] local-fallback retry: {len(local_failed_keys)} items sent...")
                    stats["local_fallback_coze_sent"] = len(local_failed_keys)
                    if self._cb_coze.is_open("coze"):
                        # 端点已熔断：不再重试发送，直接本地兜底
                        self._log("[coze] 端点已熔断，local-fallback retry 转本地兜底")
                        fb_part = self._local_fallback(local_failed_keys, work_by_key)
                    else:
                        time.sleep(COZE_BATCH_INTERVAL)
                        fb_part = self._call_coze_unified(list(local_failed_keys))
                        if fb_part is None:
                            self._log("[coze] local-fallback retry send failed, local fallback")
                            fb_part = self._local_fallback(local_failed_keys, work_by_key)
                    fb_ok = len([p for p in fb_part if p.get("status") == "ok"])
                    stats["local_fallback_coze_ok"] = fb_ok
                    self._log(f"[coze] local-fallback retry returned: {fb_ok}/{len(local_failed_keys)} ok")
                    _download_batch(fb_part, "coze_local_fallback")
                    collected.extend(fb_part)
                # 汇总 ok 数
                coze_box["projects"] = collected
                stats["coze_ok"] = len([p for p in collected
                                        if p.get("status") == "ok"
                                        and (p.get("pdf_url") or p.get("pdf_s3_url"))])
                self._log(f"[coze] all done: {len(collected)} records, {stats['coze_ok']} links parsed")
            except Exception as _ce:
                self._log(f"[coze] bg decode error: {type(_ce).__name__}: {_ce}")
                coze_box["projects"] = None
            finally:
                coze_box["done"] = True

        _coze_thread = None
        if not skip_coze:
            # 此刻 local_failed_keys 还是空的，但线程要等 _local_phase_done 置位后才读它；
            # 所以即便本次没有 coze_keys 也要启动（可能只有本地失败项需要兜底）。
            _coze_thread = _th.Thread(target=_coze_worker, daemon=True, name="pdf-coze-decode")
            _coze_thread.start()
            self._log(f"[pdf] coze decode started in parallel with local downloads: "
                      f"local {len(local_tasks)} / coze {len(coze_keys)}")

        # 4) local tasks concurrent download (真与 coze decode 并行)
        if local_tasks:
            self._log(f"[pdf] local direct/preprint concurrent download: {len(local_tasks)} "
                      f"(max workers {MAX_DOWNLOAD_WORKERS})")
            with ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKERS) as ex:
                futs = [ex.submit(_download_one, u, d, w, v) for (u, d, w, v) in local_tasks]
                for _ in as_completed(futs):
                    pass
            self._log("[pdf] local direct/preprint download done")

        # 4b) 收集本地下载失败的条目，送 coze 兜底重试（2026-09-07 新增）
        #    仅当本地下载失败、且该条目有 DOI 或 URL 可送 coze 时才重试。
        #    注意：结果**原地 extend** 进上面已声明并传给 worker 的那个 list——重新赋值
        #    会让 worker 闭包仍指向旧对象（静默失效）。
        #    还要排除「本来就路由到 coze」的条目：coze 线程现在与本地下载同时跑，
        #    它可能已经把这类条目下完/下失败并写上 pdf_download_note，若不排除就会被
        #    当成「本地失败」再送一次端点（重复解码 + 白烧配额）。
        try:
            for w in works:
                if w.get("local_pdf_path"):
                    continue
                if id(w) in coze_work_ids:      # 本来就走 coze 的，不重复兜底
                    continue
                # 只重试原本走 local_direct/local_preprint 的条目
                via = w.get("pdf_via") or ""
                note = w.get("pdf_download_note") or ""
                if via in ("oa_direct_local", "preprint_local") or "download failed" in note:
                    doi = (w.get("doi") or "").strip()
                    oa = (w.get("open_access_url") or "").strip()
                    key = oa or doi
                    if key:
                        local_failed_keys.append(key)
                        work_by_key[key] = w
            if local_failed_keys:
                self._log(f"[pdf] local failed {len(local_failed_keys)} items -> coze fallback retry")
        finally:
            # 无论成败都要放行：worker 在 1800s 超时前一直等这个信号
            _local_phase_done.set()

        # P2: heartbeat every 10s during coze decode wait
        _hb_stop = _th.Event()

        def _heartbeat():
            t0 = time.time()
            while not _hb_stop.is_set():
                if _coze_thread is None or not _coze_thread.is_alive():
                    break
                _hb_stop.wait(10)
                if _hb_stop.is_set():
                    break
                el = int(time.time() - t0)
                self._log(f"[pdf] decoding... elapsed {el}s (saved {stats['ok']} / coze decoding)")
        _hb = _th.Thread(target=_heartbeat, daemon=True, name="pdf-heartbeat")
        _hb.start()

        # 5b) wait for coze thread (local download already done; skip items never entered coze)
        if _coze_thread is not None and _coze_thread.is_alive():
            self._log("[coze] waiting for decode thread...")
            _coze_thread.join(timeout=1200)
        _hb_stop.set()
        _hb.join(timeout=2)

        projects = coze_box.get("projects")
        if projects:
            _download_batch(projects, "coze")
        # 6) Sci-Hub 最后兑底（2026-10-26；默认关闭，仅用户显式开启时执行）。
        #    必须在 coze 全部跑完、reconciliation 之前——scihub_ok 计入 stats["ok"]
        #    才能正确冲抵 manual_needed。
        try:
            self._scihub_last_resort(works, stats)
        except Exception as _se:
            self._log(f"[scihub] last-resort 阶段异常（不影响主流程）: "
                      f"{type(_se).__name__}: {_se}")
        # reconciliation: not-saved (non-reject/non-skip/non-noid) counts as manual_needed
        if not stats.get("rejected"):
            stats["manual_needed"] = max(
                0, stats["total"] - stats["ok"]
                - stats["skipped_no_id"] - stats["skipped_no_oa"])
        # batch-level timing (user 2026-09-07): surface elapsed for user feedback
        stats["started_at"] = _t_wall
        stats["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        stats["elapsed_s"] = round(time.monotonic() - _t_mono, 1)
        stats["elapsed_min"] = round(stats["elapsed_s"] / 60.0, 2)
        self._log(f"[PDF] batch finished: ok {stats['ok']}/{stats['total']}, "
                  f"elapsed {stats['elapsed_s']}s ({stats['elapsed_min']} min), "
                  f"{stats['started_at']} -> {stats['finished_at']}")
        # 自动回写 Excel：把 PDF 本地路径写回「PDF 本地路径」列。下沉到下载器自身，
        # 避免独立下载路径（直驱 PdfDownloader）漏调 update_xlsx_pdf_paths.py。
        try:
            _upd = self._write_back_xlsx(works)
            if _upd:
                stats["xlsx_updated"] = _upd
        except Exception:
            pass
        # 自动回写题录：把 PDF 绝对路径写回 references.bib / .ris / .md（用户 2026-09-21）。
        try:
            _cites = self._write_back_citations(works)
            if _cites:
                stats["citations_updated"] = _cites
        except Exception:
            pass
        # 下载台账 pdf_manifest.csv（2026-10-25）：来源/状态/大小/页数/信任级全量留痕。
        try:
            _mf = self._write_manifest(works, stats)
            if _mf:
                stats["manifest_path"] = _mf
        except Exception:
            pass
        # needs_manual.csv（v1.5.3，参考 meta-analysis a3_pending 的 CLI 化）：
        # 仍无 PDF 且有 DOI 的条目导出 doi.org 深链清单，供用户机构权限浏览器
        # 手动下载后经 --reconcile-manual 归位（合法合规，优先于 Sci-Hub 兑底）。
        try:
            from adapters.manual_reconcile import export_needs_manual
            _base = (os.path.dirname(os.path.abspath(self.xlsx_out))
                     if self.xlsx_out else
                     os.path.dirname(os.path.abspath(self.out_dir)) or ".")
            _nm = export_needs_manual(works, _base, log=self._log)
            if _nm:
                stats["needs_manual_path"] = _nm
        except Exception as _ne:
            self._log(f"[WARN] needs_manual.csv 导出失败（不影响主流程）: {_ne}")
        return stats


if __name__ == "__main__":
    # 独立测试：从 stdin 读 DOI 列表
    if len(sys.argv) > 1:
        items = sys.argv[1:]
        works = [{"doi": d, "title": "test"} for d in items]
        dl = PdfDownloader(out_dir="pdfs")
        stats = dl.run(works)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        # 注意：不要逐篇打印 PDF 绝对路径到 stdout —— 若被结果面板按路径解析会
        # 逐个打开 PDF 卡死 UI（用户 2026-09-08）。路径已写回 Excel「PDF 本地路径」列，
        # 用户到 out_dir/pdfs/ 自行打开即可。
        _ok = sum(1 for w in works if w.get("local_pdf_path"))
        print(f"[summary] ok={_ok}/{len(works)} (PDF paths written to Excel, not printed here)")
