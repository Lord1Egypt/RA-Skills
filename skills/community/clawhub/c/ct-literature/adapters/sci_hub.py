#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci_hub.py — Sci-Hub 可选兜底连接器（**默认关闭，显式开启，后果自负**）

⚠️⚠️⚠️ 法律与合规声明（用户 2026-10-26 拍板采纳，参考 openags/paper-search-mcp）⚠️⚠️⚠️
  1. Sci-Hub 提供的全文**绝大多数不受版权方授权**，通过它下载论文在多数司法辖区
     存在法律风险，也可能违反你所在机构 / 资助方的合规政策。
  2. 本连接器**默认关闭**。只有当满足以下全部条件时才会被激活：
     - CLI 显式传入 --use-scihub，或 PdfDownloader(use_scihub=True)，或
     - 环境变量 CT_LIT_ALLOW_SCIHUB=1；
     且仅作为整条下载链的**最后兜底**（在 Europe PMC / OpenAlex / Unpaywall /
     预印本 / coze 云端解码全部失败之后）。
  3. **后果自负**：因使用本连接器产生的一切法律、合规、声誉风险由使用者本人
     承担。ct-literature 技能及其作者不承担任何责任。机构环境（GCP/申办方
     项目）**严禁开启**。
  4. 不作为默认路径的理由（与 paper-search-mcp 同口径）：镜像不稳定、法律风险、
     OA / 合法订阅渠道应始终优先。

设计（纯标准库，不依赖第三方包）：
  - 多镜像顺序回退（环境变量 CT_LIT_SCIHUB_MIRRORS 可覆盖，逗号分隔）；
  - 对每个镜像请求 https://{mirror}/{doi}，从返回 HTML 中解析真实 PDF 直链
    （iframe/embed/location.href/downloads 三类常见形态的正则匹配）；
  - 连续失败熔断由调用方（PdfDownloader._SourceCircuitBreaker）负责，本模块
    只做单次解析，保持无状态、可测试。
"""

import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

# ── 激活开关 ────────────────────────────────────────────────────────────────
ENABLE_ENV = "CT_LIT_ALLOW_SCIHUB"

# 每次实际发起解析时打印的显眼声明（用户要求「加一个明确的说明，要求用户后果自负」）
DISCLAIMER = (
    "⚠️ [Sci-Hub] 兜底已启用：Sci-Hub 全文多数未经版权方授权，存在法律与合规风险，"
    "由此产生的一切后果由使用者本人承担。机构环境（GCP/申办方项目）严禁开启。"
    "可通过 --no-scihub / 取消环境变量 %s 关闭。" % ENABLE_ENV
)

# 默认镜像列表（2026-10-26 口径；镜像频繁失效，可用 CT_LIT_SCIHUB_MIRRORS 覆盖）
DEFAULT_MIRRORS = [
    "https://sci-hub.se",
    "https://sci-hub.st",
    "https://sci-hub.ru",
    "https://sci-hub.ee",
]

# 单镜像请求超时（秒）
_TIMEOUT = 25

# HTML 里常见三类真实 PDF 直链形态：
#   ① <iframe src="//sci-hub.xx/downloads/....pdf"> / <embed src="/downloads/...pdf">
#   ② button onclick="location.href='//sci-hub.xx/downloads/....pdf'"
#   ③ <a href="//sci-hub.xx/downloads/....pdf">
_PDF_URL_RES = [
    re.compile(r"""(?:src|href)\s*=\s*["']([^"']+?\.pdf[^"']*)["']""", re.I),
    re.compile(r"""location\.href\s*=\s*["']([^"']+?\.pdf[^"']*)["']""", re.I),
]
# 过滤掉明显不是全文的伪直链（图形 / 注释碎片）
_PDF_URL_NEG = re.compile(r"(smpl|/graphics/|thumb|_150\.|\.jpg\.pdf)", re.I)

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ct-literature-skill/1.5 research"


def enabled(explicit: bool = None) -> bool:
    """Sci-Hub 兜底是否被激活。

    优先级：显式参数 > 环境变量。只有两者之一为真才激活；默认关闭。
    """
    if explicit is not None:
        return bool(explicit)
    return os.environ.get(ENABLE_ENV, "").strip().lower() in ("1", "true", "yes", "on")


def _mirrors() -> list:
    raw = os.environ.get("CT_LIT_SCIHUB_MIRRORS", "").strip()
    if raw:
        return [m.strip().rstrip("/") for m in raw.split(",") if m.strip()]
    return list(DEFAULT_MIRRORS)


def _fetch_html(mirror: str, doi: str) -> str:
    url = "%s/%s" % (mirror.rstrip("/"), urllib.parse.quote(doi))
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as r:
        raw = r.read().decode("utf-8", errors="replace")
    return raw


def _extract_pdf_url(html: str, mirror: str) -> str | None:
    for rx in _PDF_URL_RES:
        for m in rx.finditer(html):
            u = m.group(1).strip()
            if not u or _PDF_URL_NEG.search(u):
                continue
            if u.startswith("//"):
                return "https:" + u
            if u.startswith("http://") or u.startswith("https://"):
                return u
            # 站内相对路径 → 拼到当前镜像（Sci-Hub 页内 iframe 常是相对路径）
            return mirror.rstrip("/") + ("" if u.startswith("/") else "/") + u
    return None


def resolve_pdf_url(doi: str, log=None, politeness: float = 2.0,
                    disclaimer: bool = True) -> "str | None":
    """按 DOI 依次尝试镜像，返回真实 PDF 直链；全部失败返回 None。

    Args:
        doi: 裸 DOI（可为 doi.org 前缀形式，内部归一化）
        log: 进度回调 fn(msg)（可 None，静默）
        politeness: 镜像之间的间隔秒数（对镜像礼貌，避免触发限流）
        disclaimer: 是否在解析前打印免责声明（默认 True；批量调用方在构造时
            已打印过一次可传 False 避免逐篇刷屏）

    每次打印均为「后果自负」级别显式声明（用户 2026-10-26 要求）。
    """
    log = log or (lambda m: None)
    if disclaimer:
        log(DISCLAIMER)
    doi = (doi or "").strip()
    if doi.lower().startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    elif doi.lower().startswith("http://doi.org/"):
        doi = doi[len("http://doi.org/"):]
    if not doi:
        return None
    for i, mirror in enumerate(_mirrors(), 1):
        try:
            log("[scihub] mirror %d/%d: %s ..." % (i, len(_mirrors()), mirror))
            html = _fetch_html(mirror, doi)
            u = _extract_pdf_url(html, mirror)
            if u:
                log("[scihub] resolved via %s" % mirror)
                return u
            log("[scihub] %s 返回页面但未解析到 PDF 直链" % mirror)
        except urllib.error.HTTPError as e:
            log("[scihub] %s HTTP %d" % (mirror, e.code))
        except Exception as e:
            log("[scihub] %s 失败: %s: %s" % (mirror, type(e).__name__, e))
        if politeness > 0 and i < len(_mirrors()):
            time.sleep(politeness)
    return None


if __name__ == "__main__":
    # 自测：python sci_hub.py 10.1038/s41586-021-03819-2
    import sys
    if len(sys.argv) > 1:
        print("pdf_url =", resolve_pdf_url(sys.argv[1], log=print))
