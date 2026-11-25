"""cite-holmes v6.0.0 模块层：ch_registry（由手术脚本从单文件引擎分层，
判定语义与 API 见壳 verify_refs.py 与 ADR-0010）。一切跨层符号与被
测试 patch 的函数一律经 _ROOT（由壳注入主壳命名空间）——patch 语义
与 trunk/mcp 双壳隔离（目录前缀加载）共同由该机制保证。"""

import argparse
import csv
import difflib
import hashlib
import ipaddress
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape as html_escape
from urllib.parse import urlparse, urlunparse, quote

_ROOT = None  # 由 verify_refs 壳注入


def _bind(root):
    global _ROOT
    _ROOT = root


def _cross_lingual_bridge(doi: str, claimed: str, meta: dict, timeout: float) -> str:
    """v3.10 跨语言标题桥接核验（只补证据、只升不降）：中文期刊常在 Crossref
    登记英文题名而用户引用中文原题，跨语言相似度天然低——v3.0 守卫此时一律
    转 partial 人工核对。本函数依次尝试三级桥接，任一命中即返回一致注记
    （调用方升级 verified），全部未命中返回空串（维持 partial 转人工）。
      T1 零网络：Crossref 双语记录的 original-title 字段（常存原语言题名）
      T2 落地页：DOI 资源页的 citation_title/og:title，或页面全文命中中文原题
      T3 OpenAlex：display_name 常为原语言题名（无 key 403 静默跳过）
    设计铁律：网络失败一律静默——「桥接不通」绝不能变成「编造依据」；
    阈值 0.75 为归一化后中文题名比对的保守下限（全半角/标点已归一）。"""
    cn = _ROOT._cjk_norm(claimed)
    if len(cn) < 6:
        return ""
    ot = meta.get("original-title")
    ot = (ot[0] if isinstance(ot, list) and ot else ot) or ""
    if ot:
        r = difflib.SequenceMatcher(None, cn, _ROOT._cjk_norm(ot)).ratio()
        if r >= 0.75:
            return f"双语记录 original-title 核验一致（相似度 {r:.2f}）"
    res_url = (
        ((meta.get("resource") or {}).get("primary") or {}).get("URL")
    ) or f"https://doi.org/{doi}"

    # 安全门（审计 A1/A2 修复）：注册库/出版商自控 URL——
    # ① scheme 白名单（file: 等 hostname 为空的方案在 ssrf_blocked 放行，须显式拦）；
    # ② 禁自动重定向，手动逐跳跟随并对每一跳重查 SSRF 字面量——
    #    否则落地页 302 到内网地址会被默认 opener 照常跟随（盲 SSRF）。
    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    html = _ROOT._fetch_landing_html(res_url, timeout)
    if html:
        m = (
            re.search(r'<meta[^>]+name="citation_title"[^>]+content="([^"]+)"', html, re.I)
            or re.search(r'<meta[^>]+content="([^"]+)"[^>]+name="citation_title"', html, re.I)
            or re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', html, re.I)
        )
        if m:
            r = difflib.SequenceMatcher(None, cn, _ROOT._cjk_norm(m.group(1))).ratio()
            if r >= 0.75:
                return f"DOI 落地页题名核验一致（相似度 {r:.2f}）"
        # 审计 A6 收紧：整页子串命中只认 <head> 区（<title>+meta）——正文区
        # （如攻击者自己论文的参考文献表）出现该题名不构成「同载」证据。
        head_m = re.search(r"<head[^>]*>(.*?)</head>", html, re.I | re.S)
        ttl_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        head_zone = _ROOT._cjk_norm(
            (head_m.group(1) if head_m else "") + (ttl_m.group(1) if ttl_m else "")
        )
        if cn in head_zone:
            return "DOI 落地页同载声称中文原题（双语页命中）"
    if len(cn) >= 12 and (_ROOT._OPTS.get("openalex_key") or ""):
        try:
            q = quote(claimed.strip(), safe="")
            url = (
                f"https://api.openalex.org/works?search={q}&per-page=1"
                f"&select=display_name&api_key={quote(_ROOT._OPTS['openalex_key'], safe='')}"
            )
            if _ROOT._cb_open(url):
                return ""
            req = urllib.request.Request(
                url, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                _ROOT._cb_record(url, False)
                hits = (json.loads(resp.read().decode("utf-8", "ignore")) or {}).get(
                    "results"
                ) or []
            if hits:
                r = difflib.SequenceMatcher(
                    None, cn, _ROOT._cjk_norm(hits[0].get("display_name"))
                ).ratio()
                if r >= 0.75:
                    return f"OpenAlex 原语言题名核验一致（相似度 {r:.2f}）"
        except Exception:
            pass
    return ""


def doi_metadata_match(
    doi: str, title: str, year, timeout: float, source: str = "", authors: str = ""
) -> tuple:
    """DOI 元数据交叉验证（v1.4）：doi.org 内容协商取官方登记的 CSL 元数据，
    与引用声称的标题/年份比对——专抓「真 DOI 假论文」这类最像真引用的伪造。
    v1.6 新增：期刊名一致性核查（复用已取回的 container-title，零网络成本；
    不符降 partial——期刊改名常见，不判 invalid），抓「真 DOI 真论文假期刊」。
    v1.7 新增：作者名一致性核查（复用 CSL author 列表；声称姓氏至少一个命中
    登记列表即视为一致——拼写/变体从宽；全部不命中才降 partial）。
    瞬态网络错误自动重试一次。主机断路器生效。
    返回 (adjust, note, matched, csl)：adjust ∈ {"", "partial", "invalid"}；
    matched=True 表示元数据成功取得且与声称标题一致。csl=注册库权威元数据摘要
    (v3.6 新增，供 GB/T 7714 导出使用；获取失败为 None)。
    v3.6 --cn 模式：doi.org 三试全败时回源 api.crossref.org/works/{doi}
    （独立主机，CN 出口常与 doi.org 不同命运），同 CSL 格式无缝续用。"""
    import difflib

    cb_url = f"https://doi.org/{doi}"
    if _ROOT._cb_open(cb_url):
        return "", _ROOT._cb_skip_note(cb_url) + "，未做 DOI 元数据核验", False, None
    mailto = _ROOT._OPTS.get("mailto") or ""
    # doi.org 走 UA 联系方式（不加 query 参数——避免干扰个别 DOI 的解析行为）；
    # api.crossref.org 才用 ?mailto= polite pool 约定
    ua_contact = (
        f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research "
        "(https://skillhub.cn/skills/cite-holmes)"
    )
    if mailto:
        ua_contact += f" mailto:{mailto}"
    req_url = cb_url
    ua_rot = [
        ua_contact,
        f"Mozilla/5.0 (compatible; cite-holmes/{_ROOT.VERSION}; +verified-deep-research)",
    ]
    meta, fetch_err = None, ""
    retry_after = 0.0
    for attempt in range(3):
        req = urllib.request.Request(
            req_url,
            headers={
                "Accept": "application/vnd.citationstyles.csl+json",
                "User-Agent": ua_rot[min(attempt, 1)],
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                meta = json.loads(resp.read().decode("utf-8", "ignore"))
            fetch_err = ""
            _ROOT._cb_record(cb_url, False)
            break
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(cb_url, False)
            if e.code == 404:
                return "invalid", "DOI 在 DOI.org 不存在（404）→ 疑似编造引用", False, None
            fetch_err = f"HTTP {e.code}"
            if e.code == 429:
                # v1.9：限速分层后的礼貌退避——尊重 Retry-After（封顶 5 秒）
                retry_after = 2.0
                try:
                    if e.headers and e.headers.get("Retry-After"):
                        retry_after = min(5.0, max(1.0, float(e.headers["Retry-After"])))
                except (TypeError, ValueError):
                    pass
        except Exception as e:
            fetch_err = type(e).__name__
        if attempt < 2:
            # T3a 家族第 5 变体修复(09-30 ④b 实证):慢窗下 2 连发全灭→3 连发递增退避
            time.sleep(retry_after if retry_after else (1.2 if attempt == 0 else 3.5))
    if meta is None and _ROOT._OPTS.get("cn_mode"):
        # v3.6 --cn 回源：api.crossref.org/works/{doi} 返回同构 CSL(message 字段)。
        # 独立主机不计入 doi.org 断路器；失败静默回原路径。
        try:
            cr_url = f"https://api.crossref.org/works/{quote(doi, safe='()/')}"
            cr_req = urllib.request.Request(
                cr_url, headers={"User-Agent": ua_contact, "Accept": "application/json"}
            )
            with urllib.request.urlopen(cr_req, timeout=timeout) as resp:
                meta = json.loads(resp.read().decode("utf-8", "ignore")).get("message") or {}
            fetch_err = f"doi.org 失败({fetch_err})→Crossref 回源成功"
        except Exception as e2:
            fetch_err += f";Crossref 回源失败({type(e2).__name__})"
    if meta is None:
        _ROOT._cb_record(cb_url, True)  # 整次调用只记 1 次传输失败（重试是同一逻辑失败）
        return "", f"DOI 元数据获取失败（{fetch_err}），跳过内容核验", False, None
    mt = meta.get("title")
    meta_title = (mt[0] if isinstance(mt, list) else mt) or ""
    sim = difflib.SequenceMatcher(None, (title or "").lower(), str(meta_title).lower()).ratio()
    meta_year = None
    parts = (meta.get("issued") or {}).get("date-parts") or []
    if parts and parts[0]:
        meta_year = parts[0][0]
    # v3.6:注册库权威元数据摘要(GB/T 7714 导出原料)——作者按 GB/T 缩写惯例
    # 预格式化(拉丁:姓全大写+名首字母;CJK:全名),container/year/vol/issue/page 原样
    prov = "；DOI 元数据经 Crossref 回源（CN 模式）" if "Crossref 回源成功" in fetch_err else ""

    def _gbt_author(a):
        fam = (a.get("family") or "").strip()
        giv = (a.get("given") or "").strip()
        whole = fam + giv
        if any("\u4e00" <= c <= "\u9fff" for c in whole):
            return whole
        ini = " ".join(t[0].upper() for t in re.split(r"[\s\-]+", giv) if t)
        return (fam.upper() + (" " + ini if ini else "")).strip()

    _ct = meta.get("container-title")
    _container = (_ct[0] if isinstance(_ct, list) and _ct else _ct) or ""
    csl = {
        "title": str(meta_title)[:300],
        "authors": [
            x
            for x in (_gbt_author(a) for a in (meta.get("author") or []) if isinstance(a, dict))
            if x
        ],
        "container": str(_container)[:200],
        "year": meta_year,
        "volume": str(meta.get("volume") or "")[:32],
        "issue": str(meta.get("issue") or "")[:32],
        "page": str(meta.get("page") or "")[:64],
    }
    # v1.6 期刊名一致性核查（零网络成本）：规范化后互不包含视为不符，
    # 降 partial（期刊改名常见，不判 invalid）。
    # 二轮评审 P1 修正：NLM 式缩写（N Engl J Med vs New England Journal of
    # Medicine）不算不符——短名各词按序匹配长名词首（可跳过虚词）即视为同一
    # 期刊；跨语言（拉丁 vs CJK）不具可比性，跳过判定。
    ct = meta.get("container-title")
    reg_journal = (ct[0] if isinstance(ct, list) and ct else ct) or ""
    jadj, jnote = "", ""
    src = (source or "").strip()
    if reg_journal and src:

        def _nj(s):
            return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", str(s).lower())

        def _tokens(s):
            return re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", str(s).lower())

        def _is_abbrev(short_toks, long_toks):
            j = 0
            for st in short_toks:
                while j < len(long_toks) and not (
                    long_toks[j].startswith(st) or st[0] == long_toks[j][0]
                ):
                    j += 1
                if j >= len(long_toks):
                    return False
                j += 1
            return True

        def _journal_same(x, y):
            a, b = _nj(x), _nj(y)
            if not a or not b:
                return True
            # v3.15 跨族守卫（原 CJK-only）：主导文字系统不同（如俄文刊名 vs
            # 英文登记名、混合文字刊名）→ 不判不符
            if _ROOT._script_family(a) not in ("none", _ROOT._script_family(b)):
                return True
            if a in b or b in a:
                return True
            ta, tb = _tokens(x), _tokens(y)
            return _is_abbrev(ta, tb) or _is_abbrev(tb, ta)

        if not _journal_same(src, reg_journal):
            jadj = "partial"
            jnote = (
                f"；期刊名不符（声称 {str(src)[:40]} / DOI 登记 "
                f"{str(reg_journal)[:40]}）→ 建议核对是否引错论文"
            )
    # v1.7 作者名一致性核查（复用 CSL author，零网络成本）：任一声称姓氏命中
    # 登记列表即视为一致（拼写/变体从宽）；全部不命中才降 partial。
    aadj, anote = "", ""
    claimed = _ROOT._claimed_surnames(authors)
    if claimed and not _ROOT._author_consistent(claimed, meta.get("author")):
        aadj = "partial"
        more = " 等" if len([c for c in (_ROOT._norm_name(x) for x in claimed) if c]) > 1 else ""
        anote = (
            f"；作者不符（声称 {claimed[0]}{more} 未见于 DOI 登记作者列表）"
            f"→ 建议核对是否引错论文"
        )
    if not title:
        return (
            (jadj or aadj),
            (
                f"DOI 元数据核验完成（引用未提供标题，无法比对；"
                f"登记年份 {meta_year or '未知'}）{jnote}{anote}"
            ),
            True,
            csl,
        )
    # v3.15 文字系统守卫（原 v3.0 仅 CJK）：声称与登记的主导文字系统不同
    # （中俄/希/日/韩 vs 拉丁等任意跨族组合）即视为跨语言——不判 invalid。
    # v3.10 三级桥接核验对各族同样适用（original-title/落地页/OpenAlex）。
    _sf_claim, _sf_reg = _ROOT._script_family(title), _ROOT._script_family(meta_title)
    if title and sim < 0.50 and _sf_claim != "none" and _sf_reg != "none" and _sf_claim != _sf_reg:
        bridge = _ROOT._cross_lingual_bridge(doi, title, meta, timeout)
        if bridge:
            # 审计 B1 修复：桥接只解决「标题跨语言不可比」，期刊/作者不符信号
            # 必须原样透出——桥接命中≠整条引用干净，jadj/aadj 参与最终 adjust，
            # jnote/anote 拼回 note（与下方常规路径同款拼接）。
            # 契约:adjust ∈ {"", "partial", "invalid"}——一致=空串(verify_one 视为无调整)
            return (
                (jadj or aadj),
                (
                    f"DOI 元数据核验一致（跨语言桥接：{bridge}；"
                    f"登记题名《{str(meta_title)[:60]}》）{jnote}{anote}"
                ),
                True,
                csl,
            )
        return (
            "partial",
            (
                f"跨语言标题无法机器比对（声称 {_sf_claim} 文 vs 登记 "
                f"{_sf_reg} 文,相似度 {sim:.2f}；桥接核验未命中）{jnote}{anote}"
                f"→ 建议人工核对"
            ),
            True,
            csl,
        )
    if title and sim < 0.50:
        return (
            "invalid",
            (
                f"DOI 元数据标题相似度仅 {sim:.2f} → DOI 指向的不是这篇论文，"
                f"疑似编造或错引（DOI 实际为《{str(meta_title)[:60]}》）"
            ),
            True,
            csl,
        )
    year_note = ""
    if meta_year and year:
        try:
            if abs(int(year) - int(meta_year)) >= 2:
                year_note = f"；年份不符（声称 {year} vs DOI 登记 {meta_year}）"
        except (TypeError, ValueError):
            pass
    if title and sim < 0.82:
        # v6.4.0 M5 忠实度分级（判定零改动——纯标签透出）：partial 内区分
        # 元数据漂移幅度（minor=接近登记[0.68-0.82]，多为年份/拼写/更名级；
        # major=题名明显偏差[0.50-0.68]仍非编造），对齐 CITECHECK 行业前沿
        # 的 Exact/Minor/Major 分层；"完全编造"仍由 invalid 独占。
        _fid = "minor" if sim >= 0.68 else "major"
        return (
            "partial",
            (
                f"[元数据漂移:{_fid}] DOI 元数据标题相似度 {sim:.2f}，"
                f"建议人工复核{year_note}{jnote}{anote}{prov}"
            ),
            True,
            csl,
        )
    if jadj or aadj:
        # 期刊更名/作者变体级偏差=minor（题名一致，字段级漂移）
        return (
            (jadj or aadj),
            (
                f"[元数据漂移:minor] DOI 元数据核验一致（相似度 "
                f"{sim:.2f}）{year_note}{jnote}{anote}{prov}"
            ),
            True,
            csl,
        )
    return (
        (jadj or aadj),
        f"DOI 元数据核验一致（相似度 {sim:.2f}）{year_note}{jnote}{anote}{prov}",
        True,
        csl,
    )


def pubmed_title_reverse_lookup(title: str, source: str, year, timeout: float) -> tuple:
    """v4.0.0 Vancouver 医学引用的 PubMed 题名反查（无标识符引用的官方核验通道）。

    医学文档参考文献的主流形态是 Vancouver 纯文本（作者. 题名. 期刊. 年;卷(期):页.），
    无 DOI/PMID/URL——此前只能走 OpenAlex/S2 标题确认（只确认不升级，unverified 转人工）。
    本通道用 E-utilities esearch 题名实词组合 → 候选 PMID → esummary 官方元数据 →
    标题相似度+年份+期刊三重比对，命中即给「官方注册库核验一致」判定并回填 PMID 锚。

    v4.1.0：
      - 短题名支持：实词 ≥2 即检索（原 <3 静默跳过——"Scleroderma in children"
        类规范短题名漏检；[Title] 限定+相似度阈值守精度）；
      - 传输失败可观测：esearch/esummary 传输异常走 _urlopen_retry（3 次退避），
        仍失败返回 net_err=True——「网络没搜成」绝不伪装成「搜了没有」（2026-10-16
        实测事故：代理抖动致 12+ 条真文献被报 unverified 且无任何痕迹）。

    返回 (adjust, note, matched, pmid, net_err)：
      adjust=""  且 matched=True      → 反查一致（调用方可升 verified）
      adjust="partial"                → 近似命中（转人工）
      adjust=""   且 matched=False    → 未命中（静默：查无≠编造，调用方继续现有
                                        通道——PubMed 收录面为生物医学/生命科学，
                                        中文文献/非生物医学引用未命中属预期）
      net_err=True                    → 传输失败（检索未完成），note 已带说明；
                                        查无与失败必须可区分
    判定语义遵循家族铁律：查无永不判死；只升不降。"""
    q = (title or "").strip()
    if len(q) < 20:  # 题名过短，检索噪声过大
        return "", "", False, "", False
    # 检索构造（实测定标 2026-10-14）：整题名短语 [Title] 对含标点长题名零命中
    # （PubMed phrase 索引 tokenize 问题）——改用区分性实词 AND 组合：
    # 题名实词按长度降序取 5 个，逐词 [Title] AND（真身命中验证：
    # ACR/EULAR SSc 分类标准 → PMID 24122180 ✓）
    stop = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "of",
        "in",
        "on",
        "a",
        "an",
        "to",
        "by",
        "at",
        "is",
        "are",
        "via",
        "after",
        "before",
        "during",
        "into",
        "over",
        "under",
        "between",
        "among",
        "against",
        "without",
        "within",
        "upon",
        "than",
        "that",
        "this",
        "these",
        "those",
        "its",
        "their",
    }
    words = [w for w in re.findall(r"[A-Za-z\u4e00-\u9fff0-9]{2,}", q) if w.lower() not in stop]
    words.sort(key=len, reverse=True)
    if len(words) < 2:  # v4.1.0：<3 → ≥2（短题名规范文献反查，如 "Scleroderma in children"）
        return "", "", False, "", False
    # 词数递减收集全轮候选（5→4→3→2）：不因某轮有命中而停——4 词轮可能只命中
    # 高频词杂讯而真身在 3 词轮（实测 #5 短题名场景）；esummary 统一比对
    ids_all = []
    net_err = False
    for nwords in (5, 4, 3, 2):
        if len(words) < nwords:
            continue
        term = " AND ".join(f"{w}[Title]" for w in words[:nwords])
        u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" + _ROOT._ncbi_qs(
            f"?db=pubmed&retmode=json&retmax=8&sort=relevance&term={quote(term)}"
        )
        if _ROOT._cb_open(u):
            return "", "", False, "", False
        _ROOT._ncbi_rate_wait()
        try:
            req = urllib.request.Request(
                u, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
            )
            with _ROOT._urlopen_retry(req, timeout) as resp:
                j = json.loads(resp.read().decode("utf-8", "ignore"))
            _ROOT._cb_record(u, False)
            got = [str(x) for x in ((j.get("esearchresult") or {}).get("idlist") or [])]
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(u, False)
            # 限流可观测：429/403 让调用方知道「没搜成」而非「搜了没命中」
            return (
                "",
                (
                    f"PubMed 反查限流（HTTP {e.code}）——建议 NCBI_API_KEY 或分批"
                    if e.code in (429, 403)
                    else ""
                ),
                False,
                "",
                False,
            )
        except Exception:
            _ROOT._cb_record(u, True)
            # v4.1.0：传输失败（重试后仍不通）可观测——绝不与「查无」混淆
            net_err = True
            break
        ids_all.extend(got)
        if len(got) >= 8:  # 满额命中：该轮已是最优粒度，停
            break
    ids = list(dict.fromkeys(ids_all))
    if not ids:
        if net_err:
            return (
                "",
                ("PubMed 反查未完成（网络传输失败，已重试）——非查无；" "网络恢复后复跑可完成核验"),
                False,
                "",
                True,
            )
        return "", "", False, "", False
    ids = ids[:24]
    u2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" + _ROOT._ncbi_qs(
        f"?db=pubmed&retmode=json&id={','.join(ids)}"
    )
    if _ROOT._cb_open(u2):
        return "", "", False, "", False
    _ROOT._ncbi_rate_wait()
    try:
        req = urllib.request.Request(
            u2, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
        )
        with _ROOT._urlopen_retry(req, timeout) as resp:
            _ROOT._cb_record(u2, False)
            j2 = json.loads(resp.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        _ROOT._cb_record(u2, False)
        # 审计 P3:esummary 限流与 esearch 同款可观测
        return (
            "",
            (f"PubMed 反查限流（HTTP {e.code}）" if e.code in (429, 403) else ""),
            False,
            "",
            False,
        )
    except Exception:
        _ROOT._cb_record(u2, True)
        return (
            "",
            ("PubMed 反查未完成（网络传输失败，已重试）——非查无；" "网络恢复后复跑可完成核验"),
            False,
            "",
            True,
        )
    best = None  # (sim, pmid, meta_title, meta_source, meta_year)
    for pid in ids:
        doc = (j2.get("result") or {}).get(pid) or {}
        mt = str(doc.get("title") or "").strip()
        if not mt:
            continue
        sim = _ROOT._title_sim(title, mt)
        my = None
        m = re.search(r"(19|20)\d{2}", str(doc.get("pubdate") or ""))
        if m:
            my = int(m.group(0))
        ms = str(doc.get("source") or "").strip()
        try:
            year_i = int(year) if year else None
        except (TypeError, ValueError):
            year_i = None  # 审计 P2:坏 year 字符串（如 "2020 (Epub)"）不过滤，
            #               绝不因元数据解析异常走判死路径
        year_ok = (not year_i) or (not my) or abs(year_i - int(my)) <= 1
        # 收集全部 year_ok 候选取 sim 最大——阈值分档放在收集之后
        # （原实现在收集处就筛 0.82，导致 0.50-0.82 近似命中分支永不触发）
        if year_ok and (best is None or sim > best[0]):
            best = (sim, pid, mt, ms, my)
    if best and best[0] >= 0.82:
        sim, pid, mt, ms, my = best
        note = (
            f"PubMed 题名反查核验一致（PMID:{pid}；登记题名《{mt[:60]}》"
            f"{'·' + ms if ms else ''}{'·' + str(my) if my else ''}）"
        )
        return "", note, True, pid, False
    if best and best[0] >= 0.50:
        sim, pid, mt, ms, my = best
        return (
            "partial",
            f"PubMed 题名反查近似命中（PMID:{pid}，相似度 {sim:.2f}，"
            f"登记题名《{mt[:60]}》）→ 人工核对是否同一篇",
            True,
            pid,
            False,
        )
    return "", "", False, "", False


# v4.2.0 中文医学期刊 → NLM TA（题名缩写）映射。数据源=NLM 目录静态快照（中华医学会
# 系列命名规律 "Zhonghua X Za Zhi"）。收录错误的代价=锚定零命中静默放行（绝不误判）。
# v4.3.0 数据治理：2026-10-18 PubMed 在线抽验——21 条候选映射属「目录登记但 MEDLINE
# 零收录」（定位器永哑火）已剔除，现存 17 条全部实测有收录（中华儿科杂志 6254 条等；2026-10-18 复验
# 中华创伤杂志亦零收录同剔——「18 条全部实测」初版声明经二次抽验纠正为 17）；
# 抽验工具=tools/check_ta_table.py。未收录期刊由 OpenAlex 通道（v4.3.0）覆盖。
def unpaywall_lookup(doi: str, mailto: str, timeout: float) -> dict:
    """v5.6.0 开放获取查询（Unpaywall 官方 API，mailto 礼貌标识必配）。
    返回 {}（失败/未收录——静默，绝不参与判定）或
    {"is_oa": bool, "license": str, "oa_url": str}。纯数据富集：只回答
    「这篇有没有免费全文、什么许可」，是综述工作流的选读信号。"""
    url = (
        "https://api.unpaywall.org/v2/"
        + quote(doi, safe="")
        + "?email="
        + quote(mailto or "", safe="")
    )
    if _ROOT._cb_open(url):
        return {}
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            _ROOT._cb_record(url, False)
            j = json.loads(resp.read().decode("utf-8", "ignore")) or {}
    except urllib.error.HTTPError:
        _ROOT._cb_record(url, False, degrade=False)  # 404=未收录，站点有响应
        return {}
    except Exception:
        _ROOT._cb_record(url, True)
        return {}
    if not j.get("is_oa"):
        return {"is_oa": False}
    best = j.get("best_oa_location") or {}
    return {
        "is_oa": True,
        "license": str(best.get("license") or "")[:24],
        "oa_url": str(best.get("url") or "")[:160],
    }


def _open_access_enrich(out: dict, timeout: float) -> None:
    """v5.6.0 OA 接线 helper：verified+DOI+mailto 三门齐全才查 Unpaywall，
    结果写 checks.open_access（纯数据富集，判定永不改——ADR-0005）。"""
    if (
        not _ROOT._OPTS.get("mailto")
        or not out.get("doi")
        or not _ROOT.DOI_RE.match(out["doi"])
        or out["verdict"] != "verified"
    ):
        return
    oa = _ROOT.unpaywall_lookup(out["doi"], _ROOT._OPTS["mailto"], timeout)
    if oa:
        out["checks"]["open_access"] = dict(oa, ran=True)


def pubmed_locator_lookup(
    source: str, year, volume, issue, pages, timeout: float, claimed_title: str = ""
) -> tuple:
    """v4.2.0 卷期页锚定核验（PubMed Single Citation Matcher 的 E-utilities 形态）。

    GB/T 7714 中文医学引用的第二个无标识符通道：期刊+年+卷(期):页 是 PubMed
    官方引文定位器——语言无关（声称中文题名 vs 登记英文/罗马化题名不影响定位），
    恰好覆盖题名反查的盲区（非 MEDLINE 题名形态、翻译题名相似度不足）。
    期刊映射：中文刊名走 _CN_JOURNAL_TA → NLM TA；英文刊名直接作 TA。

    判定（保守）：TA+年+卷+期+页 **唯一命中**（count==1）→ matched，调用方升
    verified 并回填 PMID 锚；count>=2 → 歧义注记转人工；count==0 → 静默（查无≠编造）。
    年份必须精确（定位器语义，无 ±1 宽限）。返回 (adjust, note, matched, pmid, net_err)，
    契约与题名反查一致。"""
    ta = _ROOT._ta_for_journal(source)
    vol = str(volume or "").strip()
    if not ta or not vol:
        return "", "", False, "", False
    try:
        y = int(str(year)) if year else None
    except (TypeError, ValueError):
        y = None
    if not y:
        return "", "", False, "", False
    parts = [f"{ta}[TA]", f"{y}[DP]", f"{vol}[VI]"]
    iss = str(issue or "").strip()
    pg = str(pages or "").strip()
    if iss:
        parts.append(f"{iss}[IP]")
    if pg:
        parts.append(f"{pg}[PG]")
    term = " AND ".join(parts)
    u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" + _ROOT._ncbi_qs(
        f"?db=pubmed&retmode=json&retmax=4&sort=relevance&term={quote(term)}"
    )
    if _ROOT._cb_open(u):
        return "", "", False, "", False
    _ROOT._ncbi_rate_wait()
    try:
        req = urllib.request.Request(
            u, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
        )
        with _ROOT._urlopen_retry(req, timeout) as resp:
            j = json.loads(resp.read().decode("utf-8", "ignore"))
        _ROOT._cb_record(u, False)
        er = j.get("esearchresult") or {}
        count = int(er.get("count") or 0)
        ids = [str(x) for x in (er.get("idlist") or [])]
    except urllib.error.HTTPError as e:
        _ROOT._cb_record(u, False)
        return (
            "",
            (
                f"PubMed 卷期页锚定限流（HTTP {e.code}）——建议 NCBI_API_KEY 或分批"
                if e.code in (429, 403)
                else ""
            ),
            False,
            "",
            False,
        )
    except Exception:
        _ROOT._cb_record(u, True)
        return "", ("PubMed 卷期页锚定未完成（网络传输失败，已重试）——非查无"), False, "", True
    if count == 1 and ids:
        pid = ids[0]
        # 取登记题名进注记（透明底稿；中文声称 vs 登记题名语言差异如实展示）
        mt = ""
        u2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" + _ROOT._ncbi_qs(
            f"?db=pubmed&retmode=json&id={pid}"
        )
        if not _ROOT._cb_open(u2):
            _ROOT._ncbi_rate_wait()
            try:
                req2 = urllib.request.Request(
                    u2,
                    headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"},
                )
                with _ROOT._urlopen_retry(req2, timeout) as resp2:
                    j2 = json.loads(resp2.read().decode("utf-8", "ignore"))
                _ROOT._cb_record(u2, False)
                doc = (j2.get("result") or {}).get(pid) or {}
                mt = str(doc.get("title") or "").strip()
            except Exception:
                _ROOT._cb_record(u2, True)  # 注记增强失败不影响判定
        # 审计 A2 修复：定位器只证「卷期页↔PMID」，不证「题名↔PMID」——同文字
        # 系统时登记题名必须过 sim 0.50（编造同语言题名+真实卷期页不得机器
        # verified）；跨文字系统（中文声称 vs 登记英文）维持语言无关语义
        if claimed_title and mt:
            import difflib

            _sim = difflib.SequenceMatcher(
                None, str(claimed_title).strip().lower(), re.sub(r"\s+", " ", mt).strip().lower()
            ).ratio()
            _sf_c, _sf_r = _ROOT._script_family(str(claimed_title)), _ROOT._script_family(mt)
            if _sf_c != "none" and _sf_r != "none" and _sf_c == _sf_r and _sim < 0.50:
                return (
                    "partial",
                    (
                        f"卷期页唯一定位到 PMID:{pid}，但同语言登记题名"
                        f"《{mt[:60]}》与声称题名相似度仅 {_sim:.2f}"
                        "——疑似错引或拼接，转人工"
                    ),
                    False,
                    "",
                    False,
                )
        return (
            "",
            (
                f"PubMed 卷期页锚定核验一致（PMID:{pid}；TA:{ta}"
                + (f"；登记题名《{mt[:60]}》" if mt else "")
                + "）"
            ),
            True,
            pid,
            False,
        )
    if count >= 2:
        return "", (f"卷期页定位到 {count} 条（歧义）——转人工判定"), False, "", False
    return "", "", False, "", False


def pubmed_pmid_exists(pmid: str, timeout: float) -> tuple:
    """经 NCBI E-utilities 核实 PMID 真实存在。

    PubMed 网页对不存在的 PMID 也返回 2xx/203（且带反爬壳页），HTTP 状态码
    无法区分真假——AI 编造的 PMID 必须靠 API 核实才能抓住。
    返回 (exists, note)。
    """
    u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" + _ROOT._ncbi_qs(
        f"?db=pubmed&id={pmid}&retmode=json"
    )
    if _ROOT._cb_open(u):
        return True, _ROOT._cb_skip_note(u) + "，按可达处理"
    _ROOT._ncbi_rate_wait()
    try:
        req = urllib.request.Request(
            u, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            j = json.loads(resp.read().decode("utf-8", "ignore"))
        _ROOT._cb_record(u, False)
        res = j.get("result") or {}
        item = res.get(str(pmid)) or {}
        if item.get("error") or str(pmid) not in (res.get("uids") or []):
            return False, "PMID 在 PubMed 不存在（E-utilities 核实）→ 疑似编造引用"
        return True, "PMID 经 E-utilities 核实存在"
    except urllib.error.HTTPError as e:
        _ROOT._cb_record(u, False)
        return True, f"E-utilities 校验失败（HTTP {e.code}），按可达处理"
    except Exception as e:
        _ROOT._cb_record(u, True)
        return True, f"E-utilities 校验失败（{type(e).__name__}），按可达处理"


def pmid_doi_crosscheck(pmid: str, doi: str, timeout: float) -> tuple:
    """v1.6 DOI↔PMID 交叉一致性：两键各自真实也可能「拼接造假」（PMID 是 A 论文的、
    DOI 是 B 论文的）。取 PMID 在 PubMed 登记的 DOI 与声称 DOI 比对：
    不一致 → invalid「拼接伪造特征」；一致 → 加一致备注；登记无 DOI → 跳过。
    返回 (adjust, note)，adjust ∈ {"", "invalid"}。断路器生效。"""
    u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" + _ROOT._ncbi_qs(
        f"?db=pubmed&id={pmid}&retmode=json"
    )
    if _ROOT._cb_open(u):
        return "", _ROOT._cb_skip_note(u) + "，DOI↔PMID 交叉未做"
    _ROOT._ncbi_rate_wait()
    # v3.3.0 评审修复(09-29 ④b 实证):URLError/超时无重试会被网络抖动一击必杀
    # → 3 次递增退避重试(与 T3a DOI 探测同标准);HTTPError 服务器已应答不重试
    j = None
    last_exc = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                u, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                j = json.loads(resp.read().decode("utf-8", "ignore"))
            break
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(u, False)
            return "", f"E-utilities 交叉查询失败（HTTP {e.code}），跳过 DOI↔PMID 交叉"
        except Exception as e:
            _ROOT._cb_record(u, True)
            last_exc = e
            time.sleep(1.5 * (attempt + 1))
    if j is None:
        return "", (
            f"E-utilities 交叉查询失败（{type(last_exc).__name__}×3 重试后仍失败），"
            "跳过 DOI↔PMID 交叉"
        )
    _ROOT._cb_record(u, False)
    res = j.get("result") or {}
    item = res.get(str(pmid)) or {}
    reg = ""
    for a in item.get("articleids") or []:
        if a.get("idtype") == "doi":
            reg = (a.get("value") or "").strip()
            break
    if not reg:
        return "", "PMID 未登记 DOI，跳过 DOI↔PMID 交叉"
    if reg.lower().rstrip(".").rstrip("/") == doi.lower().strip().rstrip(".").rstrip("/"):
        return "", "DOI↔PMID 交叉一致（两键指向同一论文）"
    return "invalid", (
        f"DOI 与 PMID 指向不同论文（PMID {pmid} 登记为 {reg}，"
        f"引用声称 {doi}）→ 拼接伪造特征，疑似编造引用"
    )


def _pmid_reg_doi(item: dict) -> str:
    """v4.3.0 从 esummary item 提取登记 DOI（articleids），供桥接拯救复用。"""
    for a in item.get("articleids") or []:
        if (a.get("idtype") or "") == "doi":
            return a.get("value") or ""
    return ""


def pmid_metadata_match(pmid: str, title: str, source: str, year, timeout: float) -> tuple:
    """v3.4 池开发:PMID 元数据核验——堵「真 PMID+假标题/假期刊」拼接洞。
    此前 PMID-only 引用仅查存在性(pubmed_pmid_exists),esummary 拉回的
    标题/期刊/年份字段被丢弃:攻击者拿真 PMID 配编造标题即可过 verified。
    本函数复用同源数据(一次 esummary):标题相似度三档(与 DOI 路径同阈值)
    +期刊一致性(不透明缩写展开,不符降 partial——期刊改名常见不判 invalid)。
    返回 (adjust, note, matched),adjust ∈ {"", "partial", "invalid"}。"""
    import difflib

    u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" + _ROOT._ncbi_qs(
        f"?db=pubmed&id={pmid}&retmode=json"
    )
    if _ROOT._cb_open(u):
        return "", _ROOT._cb_skip_note(u) + "，PMID 元数据核验未做", False
    _ROOT._ncbi_rate_wait()
    j = None
    last_exc = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                u, headers={"User-Agent": f"cite-holmes/{'3.4'}; +verified-deep-research"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                j = json.loads(resp.read().decode("utf-8", "ignore"))
            break
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(u, False)
            return "", f"E-utilities 元数据获取失败（HTTP {e.code}），跳过 PMID 内容核验", False
        except Exception as e:
            _ROOT._cb_record(u, True)
            last_exc = e
            time.sleep(1.5 * (attempt + 1))
    if j is None:
        return (
            "",
            (f"E-utilities 元数据获取失败（{type(last_exc).__name__}×3），" "跳过 PMID 内容核验"),
            False,
        )
    _ROOT._cb_record(u, False)
    res = j.get("result") or {}
    item = res.get(str(pmid)) or {}
    if item.get("error") or str(pmid) not in (res.get("uids") or []):
        return "invalid", "PMID 在 PubMed 不存在（E-utilities 核实）→ 疑似编造引用", False
    mt = item.get("title") or ""
    matched = False
    if title:
        sim = difflib.SequenceMatcher(
            None, str(title).strip().lower(), re.sub(r"\s+", " ", mt).strip().lower()
        ).ratio()
        if sim < 0.50:
            # v4.2.0 文字系统守卫（与 DOI 通路同语义；家族铁律：语言差异绝不作
            # 编造依据）——真网实锤：中文指南 39429074 声称中文题名 vs 登记英文
            # 题名 sim 0.10 被误判「拼接伪造」。跨族时低相似度不得判死；桥接原料
            # =登记 DOI（articleids），桥接命中给一致，否则 partial 转人工。
            _sf_c, _sf_r = _ROOT._script_family(str(title)), _ROOT._script_family(mt)
            if _sf_c != "none" and _sf_r != "none" and _sf_c != _sf_r:
                reg_doi = _pmid_reg_doi(item)
                bridge = (
                    _ROOT._cross_lingual_bridge(reg_doi, str(title), {"title": mt}, timeout)
                    if reg_doi and _ROOT.DOI_RE.match(reg_doi)
                    else ""
                )
                if bridge:
                    return (
                        "",
                        (f"PMID 元数据核验一致（跨语言桥接：{bridge}；" f"登记题名《{mt[:60]}》）"),
                        True,
                    )
                return (
                    "partial",
                    (
                        f"跨语言标题无法机器比对（声称 {_sf_c} 文 vs 登记 "
                        f"{_sf_r} 文,相似度 {sim:.2f}）→ 建议人工核对"
                    ),
                    False,
                )
            # v4.3.0 判死前桥接拯救（audit P2：罗马化/翻译题名形态——声称与登记
            # 同属拉丁族但一个是拼音/译名时 sim 天然低）；桥接原料=登记 DOI。
            # 桥接未命中仍判死——同语言假标题的拼接防护不弱化。
            reg_doi = _pmid_reg_doi(item)
            if reg_doi and _ROOT.DOI_RE.match(reg_doi):
                bridge = _ROOT._cross_lingual_bridge(reg_doi, str(title), {"title": mt}, timeout)
                if bridge:
                    return (
                        "",
                        (f"PMID 元数据核验一致（跨语言桥接：{bridge}；" f"登记题名《{mt[:60]}》）"),
                        True,
                    )
            return (
                "invalid",
                (
                    f"PMID 登记标题相似度仅 {sim:.2f}（登记为《{mt[:60]}》）"
                    "→ 真 PMID 假标题，疑似拼接伪造"
                ),
                False,
            )
        if sim < 0.82:
            _fid = "minor" if sim >= 0.68 else "major"  # M5 同规
            return (
                "partial",
                (
                    f"[元数据漂移:{_fid}] PMID 登记标题相似度 {sim:.2f}："
                    f"《{mt[:60]}》，建议人工复核"
                ),
                False,
            )
        matched = True
    if source:
        reg_j = item.get("fulljournalname") or item.get("source") or ""
        if reg_j and not _ROOT._journal_consistent(source, reg_j):
            return (
                "partial",
                (
                    f"期刊名与 PubMed 登记不符（登记为 {reg_j}，"
                    "引用声称 " + str(source).strip() + "）——真 PMID 假期刊或改名，"
                    "降 partial 人工复核"
                ),
                matched,
            )
    return "", "PMID 元数据核验一致" + (f"：《{mt[:50]}》" if mt else ""), matched


def _alias_subset(claimed: str, actual: str) -> bool:
    """v6.3.1 title-alias-false-invalid 第3形态修复（探针 2026-11-13 抓包）：
    fallback 路径的字符级 difflib 相似度对截短/别名题名系统性低估（声称题名是登记
    题名的前缀/缩写/重排，如 "STOP: Self-Taught Optimizer" vs 登记
    "Self-Taught Optimizer (STOP): Recursively Self-Improving Code"）。
    声称题名有效 token 是登记题名 token 的子集（或反之）=「非编造」的充分条件
    → 判 partial 转人工，不再误判 invalid。主 API 路径自 v4.0.1 起已有别名
    容忍，本函数将同一保护对齐到着陆页 fallback 路径（arXiv API 超时触发率不低）。
    至少 2 个有效 token 才认定，防单词偶然命中。"""
    STOP = {
        "a",
        "an",
        "the",
        "of",
        "for",
        "and",
        "or",
        "on",
        "in",
        "to",
        "with",
        "via",
        "using",
        "towards",
        "toward",
    }

    def toks(s):
        return {
            t
            for t in re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", (s or "").lower()).split()
            if t not in STOP and len(t) >= 2
        }

    ct, at = toks(claimed), toks(actual)
    if len(ct) < 2 or not at:
        return False
    return ct.issubset(at) or at.issubset(ct)


def _arxiv_landing_fallback(arxiv_id: str, title: str, timeout: float, api_err: str) -> tuple:
    """v1.11 arXiv 第二源 fallback（判定确定性保卫）：export.arxiv.org API 偶发
    406/403——批内多条 arXiv 引用时即便有 3 秒全局控频仍可撞上其反机器人窗口
    （实测单发全 200、批内稳定 406）。此前 API 失败即静默跳过内容核验，导致同一
    引用两次运行判定漂移（verified↔partial，GESIS 立场论文 arXiv:2607.22693
    批评的「inconsistent results across repeated runs of the same tool」）。
    fallback 拉官方着陆页 arxiv.org/abs/<id>（权威层）做标题比对，恢复确定性，
    并补齐与 DOI 路径（S2 第二源）的对称性。着陆页也不可达（全网降级特征）→
    维持可达性路径判定，但 note 明示「元数据核验未完成」，不静默。
    返回 (adjust, note, matched)，语义同 arxiv_metadata_match。"""
    landing = "https://arxiv.org/abs/" + quote(arxiv_id, safe="")
    if _ROOT.ssrf_blocked(landing):  # 与 wayback 同款守卫（域名固定，防御性一致）
        return (
            "",
            (
                f"arXiv 元数据获取失败（{api_err}），着陆页核验跳过（SSRF 防护），"
                "元数据核验未完成"
            ),
            False,
        )
    if _ROOT._cb_open(landing):
        return (
            "",
            (
                f"arXiv 元数据获取失败（{api_err}），着陆页核验跳过（断路器/降级），"
                "元数据核验未完成"
            ),
            False,
        )
    req = urllib.request.Request(
        landing,
        headers={
            "User-Agent": f"Mozilla/5.0 (compatible; cite-holmes/{_ROOT.VERSION};"
            " +verified-deep-research)",
            "Accept": "text/html",
        },
    )
    html_text, err = None, ""
    try:
        # v6.3.1 改走 _urlopen_retry：继承代理自愈（代理在场且传输失败→无代理
        # 直连一试），HTTPError 语义不变（仍即时上抛由本函数分类记账）
        with _ROOT._urlopen_retry(req, timeout=timeout, attempts=2, backoff=1.0) as resp:
            html_text = resp.read().decode("utf-8", "ignore")
        _ROOT._cb_record(landing, False)
    except urllib.error.HTTPError as e:
        # 站点有响应（HTTP 层失败）——走熔断清零记账，不计全局传输失败（与
        # _cb_record 的 degrade 语义一致：arxiv.org 可达≠全网通，不能误判降级）
        _ROOT._cb_record(landing, False)
        if e.code == 404:
            # 官方着陆页 404 = 官方库查无该 ID（与 verify_one 的 abs 域 404 判定一致）
            return (
                "invalid",
                (
                    f"arXiv 元数据 API 失败（{api_err}）后官方着陆页亦 404 → "
                    "官方库查无该 ID，疑似编造引用"
                ),
                False,
            )
        err = f"HTTP {e.code}"
    except Exception as e:  # 传输层失败（超时/DNS/拒连）——如实记账
        _ROOT._cb_record(landing, True)
        err = type(e).__name__
    if html_text is None:
        return (
            "",
            (
                f"arXiv 元数据获取失败（{api_err}）且官方着陆页不可达（{err}），"
                "元数据核验未完成——本条仅按可达性/结构判定"
            ),
            False,
        )
    m = re.search(r"<title>(.*?)</title>", html_text, re.S | re.IGNORECASE)
    if not m:
        return (
            "",
            (f"arXiv 元数据获取失败（{api_err}），着陆页无标题可比对，" "元数据核验未完成"),
            False,
        )
    page_title = re.sub(r"\s+", " ", m.group(1)).strip()
    # arXiv abs 页 <title> 形如 "[2607.22693] 标题"——剥掉 ID 前缀再比对
    page_title = re.sub(r"^\[" + re.escape(arxiv_id) + r"\]\s*", "", page_title, count=1)
    sim = difflib.SequenceMatcher(None, (title or "").lower(), page_title.lower()).ratio()
    if title and sim < 0.50:
        if _alias_subset(title, page_title):
            return (
                "partial",
                (
                    f"arXiv 元数据 API 失败（{api_err}），官方着陆页标题相似度"
                    f"{sim:.2f} 但声称题名是登记题名的截短/别名（token 子集"
                    "关系）→ 非编造，降级人工复核"
                    f"（arXiv 实际为《{page_title[:60]}》）"
                ),
                True,
            )
        return (
            "invalid",
            (
                f"arXiv 元数据 API 失败（{api_err}），官方着陆页标题相似度"
                f"仅 {sim:.2f} → ID 指向的不是这篇论文，疑似错引"
                f"（arXiv 实际为《{page_title[:60]}》）"
            ),
            True,
        )
    if title and sim < 0.82:
        return (
            "partial",
            (
                f"arXiv 元数据 API 失败（{api_err}），官方着陆页标题相似度 "
                f"{sim:.2f}，建议人工复核"
            ),
            True,
        )
    note = f"arXiv 元数据 API 不稳（{api_err}），经官方着陆页标题比对确认" + (
        f"（相似度 {sim:.2f}）" if title else "（引用未提供标题，仅确认存在）"
    )
    return "", note, True


def arxiv_metadata_match(arxiv_id: str, title: str, year, timeout: float) -> tuple:
    """arXiv ID 元数据交叉验证（v1.5）：export.arxiv.org 官方 API 取登记的 Atom 元数据，
    与引用声称的标题/年份比对——复用 DOI 的 0.50/0.82 相似度阈值体系。
    查无记录/格式错误的 ID 直接判 invalid（疑似编造），调用方（verify_one）保证
    该判定先于可达性检查，假 ID 不会被误判为 unreachable。
    返回 (adjust, note, matched)：adjust ∈ {"", "partial", "invalid"}；
    matched=True 表示元数据成功取得且与声称标题一致。"""
    import xml.etree.ElementTree as ET

    ns = {"a": "http://www.w3.org/2005/Atom", "ax": "http://arxiv.org/schemas/atom"}
    api_url = (
        "https://export.arxiv.org/api/query?id_list=" + quote(arxiv_id, safe="") + "&max_results=1"
    )
    if _ROOT._cb_open(api_url):
        return "", _ROOT._cb_skip_note(api_url) + "，未做 arXiv 元数据核验", False
    _ROOT._arxiv_rate_wait()
    ua_rot = [
        f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research",
        f"Mozilla/5.0 (compatible; cite-holmes/{_ROOT.VERSION}; +verified-deep-research)",
    ]
    xml_text, fetch_err = None, ""
    for attempt in range(2):
        req = urllib.request.Request(api_url, headers={"User-Agent": ua_rot[min(attempt, 1)]})
        try:
            # v6.3.1 同着陆页：走 _urlopen_retry 拿代理自愈（HTTPError 仍即时上抛）
            with _ROOT._urlopen_retry(req, timeout=timeout, attempts=2, backoff=1.0) as resp:
                xml_text = resp.read().decode("utf-8", "ignore")
            fetch_err = ""
            _ROOT._cb_record(api_url, False)
            break
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(api_url, False)
            fetch_err = f"HTTP {e.code}"
        except Exception as e:
            fetch_err = type(e).__name__
        if attempt == 0:
            # v1.11 指数退避：406 反爬窗口对短间隔敏感（3s 仍撞），首败后多等 5s
            # 再守 3s 礼貌时隙；sleep 在锁外，不占其他 worker 的限速时隙
            time.sleep(5)
            _ROOT._arxiv_rate_wait()  # 重试同样守 3 秒礼貌上限（v1.5 评审修正）
    if xml_text is None:
        _ROOT._cb_record(api_url, True)  # 整次调用只记 1 次传输失败
        # v1.11：不再静默跳过——fallback 官方着陆页恢复判定确定性
        return _arxiv_landing_fallback(arxiv_id, title, timeout, fetch_err)
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        # API 返回了非 XML（典型=反爬 HTML 页）——同样走着陆页 fallback
        return _arxiv_landing_fallback(arxiv_id, title, timeout, f"返回非预期格式（{e}）")
    entries = root.findall("a:entry", ns)
    # v1.11 评审修正：反爬/错误页常是格式良好的 HTML（合法 XML、可解析成功），
    # 但它不是 Atom feed——绝不能据此判「查无记录 → invalid」误杀真论文。
    # feed 根元素校验失败 → 着陆页 fallback 恢复确定性。
    if not (root.tag == "feed" or root.tag.endswith("}feed")):
        return _arxiv_landing_fallback(arxiv_id, title, timeout, "返回非 Atom 格式")
    if not entries:
        return "invalid", "arXiv ID 在官方 API 查无记录 → 疑似编造引用", False
    entry = entries[0]
    t = entry.find("a:title", ns)
    meta_title = re.sub(r"\s+", " ", (t.text or "")).strip() if t is not None else ""
    # 错误判据以官方 ax:error 元素为准；标题恰为 "Error" 的真实论文不误杀，
    # 仅当 summary 明确含格式错误文案时才作辅助判据（v1.5 评审修正）
    err = entry.find("ax:error", ns)
    summ = entry.find("a:summary", ns)
    err_text = ""
    if err is not None and err.text:
        err_text = err.text.strip()
    elif summ is not None and summ.text and "incorrect id format" in summ.text:
        err_text = summ.text.strip()
    if err_text:
        return "invalid", f"arXiv 官方 API 拒绝该 ID（{err_text[:60]}）→ 疑似编造引用", False
    pub = entry.find("a:published", ns)
    meta_year = None
    if pub is not None and pub.text:
        m = re.match(r"(\d{4})", pub.text.strip())
        if m:
            meta_year = int(m.group(1))
    sim = difflib.SequenceMatcher(None, (title or "").lower(), meta_title.lower()).ratio()
    # v2.0.0 arXiv 版本二级核验(零额外请求):entry id 自带版本号,与声称版本比对。
    # 引用未指定版本且最新版>1 → 提示「该论文存在多个修订版,引用未指定」;
    # 引用指定了旧版且最新版更高 → 提示可能有修订(同一响应内取数,零网络成本)。
    ver_note = ""
    eid = entry.find("a:id", ns)
    latest_v = None
    if eid is not None and eid.text:
        vm = re.search(r"v(\d+)$", eid.text.strip())
        if vm:
            latest_v = int(vm.group(1))
    claimed_v = None
    cm = re.search(r"v(\d+)$", arxiv_id.strip())
    if cm:
        claimed_v = int(cm.group(1))
    if latest_v and latest_v > 1:
        if claimed_v is None:
            ver_note = (
                f"；注意：该论文已有 {latest_v} 个修订版本，引用未指定版本（arXiv 默认解析最新版）"
            )
            if _ROOT._OPTS.get("require_version"):
                # v6.4.0 M3 严格档（默认 off 零行为变化）：多版本文且未指定版本
                # → partial 封顶（引用语义漂移——Attention 7 版实测提示）。判定
                # 走既有 partial 通路（sim 已一致时仅降级注记），绝不判 invalid
                # （未指定版本≠编造）。
                ver_note += (
                    "；--require-version 严格档：引用语义随版本漂移，降 partial 人工确认版本"
                )
                return "partial", (f"arXiv 元数据核验一致{ver_note}"), True
        elif claimed_v < latest_v:
            ver_note = (
                f"；注意：引用指向 v{claimed_v}，最新版为 v{latest_v}"
                "——请确认引用的是预期版本（旧版可能含未修正内容）"
            )
    if not title:
        return (
            "",
            (
                f"arXiv 元数据核验完成（引用未提供标题，无法比对；登记年份 "
                f"{meta_year or '未知'}）{ver_note}"
            ),
            True,
        )
    # v3.15 文字系统守卫（与 DOI 路径同规）
    if sim < 0.50 and _ROOT._script_family(title) not in ("none", _ROOT._script_family(meta_title)):
        return (
            "partial",
            (f"跨语言标题无法机器比对（相似度 {sim:.2f} 不作编造依据）" "→ 建议人工核对"),
            True,
        )
    if sim < 0.50:
        # v5.5.0 标题别名守卫（整合并行会话 2026-10-26 补丁并经门审：截短/异序题名
        # 累计 4 次误判 invalid——STOP(0.42)、Neutropenia、Transaminitis、两篇综述同型。
        # 用户题名实词若全部出现在登记题名中，判「别名/截短」→ partial + 登记全称
        # 建议，而非 invalid。编造引用（ID 指向完全无关论文）词集不相交，仍走
        # invalid，不放开伪造口子。评审修订：CJK 无分隔符不能按词切——改字符级
        # 子集（去 CJK 停用字；≥2 词/字联合门不变）。
        def _lat(s):
            return {
                t
                for t in re.sub(r"[^0-9a-z]+", " ", (s or "").lower()).split()
                if t not in ("a", "an", "the", "of", "for", "and", "on", "in", "to", "with")
            }

        def _cjk(s):
            return {c for c in (s or "") if "\u4e00" <= c <= "\u9fff" and c not in "的与和及对在中"}

        _u_lat, _u_cjk = _lat(title), _cjk(title)
        _r_lat, _r_cjk = _lat(meta_title), _cjk(meta_title)
        if len(_u_lat) + len(_u_cjk) >= 2 and _u_lat <= _r_lat and _u_cjk <= _r_cjk:
            return (
                "partial",
                (
                    f"arXiv 标题疑似截短/异序（相似度 {sim:.2f}，但用户题名"
                    f"实词全部包含于登记题名）→ 建议引用登记全称："
                    f"《{meta_title[:80]}》"
                ),
                True,
            )
        return (
            "invalid",
            (
                f"arXiv 元数据标题相似度仅 {sim:.2f} → ID 指向的不是这篇论文，"
                f"疑似编造或错引（arXiv 实际为《{meta_title[:60]}》）"
            ),
            True,
        )
    year_note = ""
    if meta_year and year:
        try:
            if abs(int(year) - int(meta_year)) >= 2:
                year_note = f"；年份不符（声称 {year} vs arXiv 登记 {meta_year}）"
        except (TypeError, ValueError):
            pass
    if sim < 0.82:
        return (
            "partial",
            f"arXiv 元数据标题相似度 {sim:.2f}，建议人工复核{year_note}{ver_note}",
            True,
        )
    return "", f"arXiv 元数据核验一致（相似度 {sim:.2f}）{year_note}{ver_note}", True


def wayback_available(url: str, timeout: float) -> str:
    """v1.5 unreachable 存档兜底：查 Wayback Machine 是否有历史存档。
    有 → 返回「Wayback 存档可用（YYYY-MM-DD）：<存档URL>（人工复核可对照）」；
    无存档/查询失败 → 返回 ""（静默跳过，不加额外文案）。SSRF 字面量防护同样
    适用——内网/保留地址不外发到 archive.org。"""
    if _ROOT.ssrf_blocked(url):
        return ""
    # 实测教训：archive.org 对全量百分号编码的 url 参数不匹配（原样 200+快照，
    # %3A%2F 编码形式 200 但快照集为空）——必须原文直传，仅编码破坏外层查询的字符
    q = quote(url, safe=":/?&=#%@+!$,;'~()*[]-._")
    wb_url = "https://archive.org/wayback/available?url=" + q
    # 断路器看真正的外呼对象 archive.org（v1.6 二轮评审 P1 修正）——
    # 目标主机熔断不影响存档查询（死站查存档正是本函数的主用例）
    if _ROOT._cb_open(wb_url):
        return ""
    req = urllib.request.Request(
        wb_url, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
    )
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                j = json.loads(resp.read().decode("utf-8", "ignore"))
            _ROOT._cb_record(wb_url, False)
            closest = (j.get("archived_snapshots") or {}).get("closest") or {}
            if closest.get("available") and closest.get("url"):
                ts = str(closest.get("timestamp") or "")
                nice = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]}" if len(ts) >= 8 else ts
                return f"Wayback 存档可用（{nice}）：{closest['url']}（人工复核可对照）"
            return ""  # 有明确响应但无存档：确定性结果，不重试
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(wb_url, False)
            if e.code == 429 and attempt == 0:
                time.sleep(3.0)  # archive.org 对公共 IP 常见限流：退避一次
                continue
            return ""
        except Exception:
            _ROOT._cb_record(wb_url, True)
            return ""
    return ""


def _fetch_landing_html(url: str, timeout: float):
    """手动逐跳抓取落地页（≤3 跳），每跳过 scheme+SSRF 双门，返回 HTML 或 None。
    断路器接线（审计 A3）：主机连续传输失败时本批跳过，与全局外呼同规。
    v4.8.0 自桥接内嵌提取到模块级——EB/OL 落地页对照（landing_title_check）复用。"""

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    for _hop in range(4):
        if not str(url).lower().startswith(("http://", "https://")):
            return None
        if _ROOT.ssrf_blocked(url) or _ROOT._cb_open(url):
            return None
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": f"Mozilla/5.0 (compatible; cite-holmes/{_ROOT.VERSION})"},
            )
            opener = urllib.request.build_opener(_NoRedirect)
            with opener.open(req, timeout=timeout) as resp:
                html = resp.read(262144).decode("utf-8", "ignore")
            _ROOT._cb_record(url, False)
            return html
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(url, False)  # 站点有响应：不计传输失败
            loc = e.headers.get("Location") if e.headers else None
            if e.code in (301, 302, 303, 307, 308) and loc:
                url = urllib.request.urljoin(url, loc)
                continue
            return None
        except Exception:
            _ROOT._cb_record(url, True)
            return None
    return None


def landing_title_check(url: str, title: str, timeout: float) -> tuple:
    """v4.8.0 EB/OL/URL 引用落地页题名对照：页面 <title>/citation_title/og:title
    与声称题名 _title_sim 对照——≥0.75 确认存在（调用方封顶 partial 转人工：
    落地页只证「这条 URL 讲的就是这篇」的存在性，语义支撑归语义层）。
    页面无题名/低相似/抓取失败一律静默（查无永不判死）。返回 (note, confirmed)。"""
    html = _ROOT._fetch_landing_html(url, timeout)
    if not html:
        return "", False
    cands = []
    for pat in (
        r'<meta[^>]+name="citation_title"[^>]+content="([^"]+)"',
        r'<meta[^>]+content="([^"]+)"[^>]+name="citation_title"',
        r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"',
        r"<title[^>]*>(.*?)</title>",
    ):
        m = re.search(pat, html, re.I | re.S)
        if m and m.group(1).strip():
            cands.append(re.sub(r"\s+", " ", m.group(1)).strip())
    # 站点品牌后缀剥离（" - DailyMed" / " | Journal Home" 类——真网探针实证
    # 后缀稀释相似度 0.78→0.70）。分隔符两侧必须有空白：词内连字符（COVID-19/
    # anti-TNF/State-of-the-Art 生物医学高频形态）绝不自削——审计 P1 实证任意
    # 位置开削使连字符题名 perfect match 也 confirmed=False 且静默；确认线 0.75
    # 对齐桥接落地页先例（citation_title 同款阈值）。partial 封顶转人工，
    # 误确认的代价=多一条人工复核不是错判
    cands = [re.sub(r"\s+[-|–—]\s+.*$", "", c).strip() for c in cands]
    cands = [c for c in cands if c]
    best = max((_ROOT._title_sim(title, c) for c in cands), default=0.0)
    # 方向性包含通道：页面题名较短且词汇全部出现在声称题名中（说明书/标签页
    # 题名=声称题名的前缀子集是常态——"USP prescribing information" 尾缀稀释
    # 双通道相似度到 0.74 的真网探针实证）；≥3 词防单词页误伤
    tw = set(re.findall(r"[a-z0-9\u4e00-\u9fff]+", str(title).lower()))
    subset_hit = any(
        (cw := set(re.findall(r"[a-z0-9\u4e00-\u9fff]+", c.lower())))
        and len(cw) >= 3
        and cw.issubset(tw)
        for c in cands
    )
    if best >= 0.75 or subset_hit:
        return (f"落地页题名对照一致（相似度 {best:.2f}）", True)
    if best >= 0.60:
        return (f"落地页题名近似（相似度 {best:.2f}），建议人工复核", False)
    return "", False


def check_url(url: str, timeout: float, retries: int = 1) -> tuple:
    """返回 (reachable, status, note)。reachable 以 2xx/3xx/429(反爬) 计。
    瞬态网络错误（超时/连接重置）自动重试一次——国内网络偶发抖动不误判。
    内网/环回地址直接拒绝（SSRF 防护），不发起请求。
    v1.6：主机断路器生效；传输失败按成因给可操作话术（超时给 --timeout 建议）。
    v6.6.0 F62：重定向逐跳 SSRF 复核（GuardedRedirectHandler）——入口字面量
    防护之外的「公网 URL 经 302 跳内网」绕过面封死。"""
    if _ROOT.ssrf_blocked(url):
        return False, None, "内网/保留地址，验证请求已拒绝（SSRF 防护）"
    if _ROOT._cb_open(url):
        return False, None, _ROOT._cb_skip_note(url)
    note = ""
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={
                "User-Agent": f"Mozilla/5.0 (compatible; cite-holmes/{_ROOT.VERSION}; +verified-deep-research)",
                "Accept": "*/*",
            },
        )
        opener = urllib.request.build_opener(_ROOT.GuardedRedirectHandler())
        transient = False
        use_direct = False
        for method in ("HEAD", "GET"):
            try:
                req.method = method
                with opener.open(req, timeout=timeout) as resp:
                    _ROOT._cb_record(url, False)
                    return True, resp.status, f"{method} {resp.status}"
            except urllib.error.HTTPError as e:
                _ROOT._cb_record(url, False)  # 站点有响应：不算传输失败
                if method == "HEAD" and e.code in (403, 405, 501):
                    continue  # 站点拒绝 HEAD，降级 GET 重试
                if e.code == 429:
                    return True, 429, "HTTP 429（反爬限流，站点实际存在）"
                return False, e.code, f"HTTP {e.code}（站点拒绝或页面不存在）"
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                if method == "HEAD":
                    continue
                # v6.6.0 F62：SSRF 逐跳拒绝是主动防护动作，不是传输失败——
                # 如实透出且不记断路器（不拖累同主机其他条目）；话术常量
                # 单一来源（ch_netio._SSRF_REFUSAL_NOTE）
                if _ROOT._SSRF_REFUSAL_NOTE in str(e):
                    return False, None, str(e)
                # v6.3.1 代理自愈：环境有代理且 GET 传输失败 → 无代理直连重试一次。
                # 必须重建 Request——代理路径已把代理地址烘焙进原 req.host
                # （单变量实验实证：复用污染对象时换无代理 opener 仍连死代理）。
                if (not use_direct) and urllib.request.getproxies():
                    use_direct = True
                    direct_req = urllib.request.Request(
                        url,
                        method="GET",
                        headers={
                            "User-Agent": f"Mozilla/5.0 (compatible; cite-holmes/{_ROOT.VERSION};"
                            " +verified-deep-research)",
                            "Accept": "*/*",
                        },
                    )
                    direct_opener = urllib.request.build_opener(
                        _ROOT.GuardedRedirectHandler(),
                        urllib.request.ProxyHandler({}),
                    )
                    try:
                        with direct_opener.open(direct_req, timeout=timeout) as resp:
                            _ROOT._cb_record(url, False)
                            return (
                                True,
                                resp.status,
                                (f"GET {resp.status}（代理栈故障，无代理直连自愈）"),
                            )
                    except urllib.error.HTTPError as e2:
                        _ROOT._cb_record(url, False)  # 站点有响应≠传输失败
                        if e2.code == 429:
                            return True, 429, "HTTP 429（反爬限流，站点实际存在）"
                        return False, e2.code, f"HTTP {e2.code}（站点拒绝或页面不存在）"
                    except Exception:
                        pass  # 直连也失败 → 落回原 transient 流程如实报错
                transient = True
                msg = str(e)
                if isinstance(e, TimeoutError) or "timed out" in msg or "timeout" in msg.lower():
                    note = "连接超时（站点慢或网络受限），建议 --timeout 20 重试"
                elif (
                    "getaddrinfo" in msg
                    or "name or service" in msg.lower()
                    or "no address" in msg.lower()
                ):
                    note = "域名无法解析，连接失败（站点可能已下线或被网络拦截）"
                elif "refused" in msg or "reset" in msg.lower():
                    note = "连接被拒/重置（站点或网络问题）"
                else:
                    note = f"网络异常：{e}"[:120]
            except ValueError as e:
                return False, None, f"URL 格式无效：{e}"[:120]
        if transient and attempt < retries:
            time.sleep(1.5)  # 瞬态抖动稍候重试
    # 重试耗尽仍失败：每次 check_url 调用只记 1 次传输失败（重试是同一逻辑失败，
    # 逐次记录会导致一次调用即熔断）
    _ROOT._cb_record(url, True)
    return False, None, note or "连接失败（站点不可达、域名不存在或网络受限）"


def _retraction_local(doi: str):
    """v3.2.0 本地撤稿缓存命中查询(零网络)。未配置/未命中返回 None。"""
    path = _ROOT._OPTS.get("retraction_cache") or ""
    if not path:
        return None
    if _ROOT._RETRACTION_CACHE[0] is None:
        try:
            with open(os.path.expanduser(path), encoding="utf-8") as f:
                _ROOT._RETRACTION_CACHE[0] = json.load(f) or {}
        except Exception:
            _ROOT._RETRACTION_CACHE[0] = {}  # 坏文件=视为空缓存,不炸主流程
    return _ROOT._RETRACTION_CACHE[0].get(doi.strip().lower())


def _retraction_classify(raw_type: str) -> str:
    """v4.1.0 撤稿通告类型归一化（Crossref updated-by type 与 RWDB dump 字符串
    两种来源统一到六类）。返回 ∈ {"retraction", "partial_retraction", "withdrawal",
    "expression_of_concern", "correction", ""}（未识别返回小写原文，调用方按
    未分档处理——查无永不判死同样适用于「不认识的通告类型」）。"""
    t = (raw_type or "").strip().lower().replace("-", "_").replace(" ", "_")
    if t in (
        "retraction",
        "retraction_notice",
        "retract_and_republish",
        "retraction_of_publication",
    ):
        return "retraction"
    if t in ("partial_retraction", "partial_retraction_notice"):
        return "partial_retraction"
    if t in ("withdraw", "withdrawal", "remove", "removal"):
        return "withdrawal"
    if t in ("expression_of_concern", "expressions_of_concern"):
        return "expression_of_concern"
    if t in ("correction", "erratum", "corrigendum", "amendment"):
        return "correction"
    return t


def _retraction_nature_note(nature: str, when: str, notice: str, source_label: str) -> str:
    """v4.1.0 按通告分档生成中文注记（降级语义由调用方统一接线）。"""
    when_note = f"（{when}）" if when else ""
    extra = f"，通告 {notice}" if notice else ""
    if nature == "retraction":
        return f"论文已撤稿（{source_label}{when_note}{extra}）" "→ 不得作为有效证据引用"
    if nature == "partial_retraction":
        return (
            f"论文部分撤稿（{source_label}{when_note}{extra}）——撤稿部分"
            "不得作为证据，请人工核对结论边界"
        )
    if nature == "withdrawal":
        return f"论文已被出版方撤回（{source_label}{when_note}{extra}）" "→ 不得作为有效证据引用"
    if nature == "expression_of_concern":
        return (
            f"该文存在编辑关注通告 Expression of Concern"
            f"（{source_label}{when_note}{extra}）——证据效力存疑，转人工复核"
        )
    if nature == "correction":
        return (
            f"该文存在更正/勘误通告（{source_label}{when_note}{extra}）"
            "——仅提示引用时留意勘误内容，不影响有效性判定"
        )
    return f"存在出版方通告（{nature}，{source_label}{when_note}{extra}）"


def crossref_retraction_check(doi: str, timeout: float) -> dict:
    """v1.8 撤稿检测：Crossref REST API（Retraction Watch 数据，免费/每日更新）。
    v3.2.0：--retraction-cache 配置本地索引(GitLab 官方 dump 构建)时先查本地
    (零网络/离线可用),未命中再走网络拿最新状态。
    v4.1.0 通告分档：updated-by/type 细分（撤稿/部分撤稿/撤回/EoC/更正）——
    原二元判定对「编辑关注通告」完全漏抓（医学场景 EoC 论文不应继续当作
    干净证据引用；JMIR 2026 实证 AI 工具单靠自身抓不全撤稿文献）。
    查询失败一律静默跳过（绝不因检查失败惩罚引用）——但 v4.1.0 起
    check_failed=True 可观测（传输失败≠「干净」，报告层注明检查未完成）。

    返回 dict：{"retracted": bool,            # 撤稿族（retraction/partial/withdrawal）
                "nature": str,                # 六类分档（_retraction_classify）
                "notice_doi": str, "when": str,
                "source": "local"|"crossref"|"",
                "check_failed": bool}         # 传输失败（重试耗尽）——非「未撤稿」"""
    failed = {
        "retracted": False,
        "nature": "",
        "notice_doi": "",
        "when": "",
        "source": "",
        "check_failed": True,
    }
    clean = {
        "retracted": False,
        "nature": "",
        "notice_doi": "",
        "when": "",
        "source": "",
        "check_failed": False,
    }
    hit = _retraction_local(doi)
    if hit is not None:
        raw_date = (hit.get("date") or "").split(" 0:00")[0]  # CSV 时间残渣剥除
        nature = _retraction_classify(hit.get("type") or "Retraction")
        family = nature in ("retraction", "partial_retraction", "withdrawal")
        return {
            "retracted": family,
            "nature": nature,
            "notice_doi": "",
            "when": raw_date,
            "source": "local",
            "check_failed": False,
        }
    mailto = _ROOT._OPTS.get("mailto") or ""
    url = f"https://api.crossref.org/works/{quote(doi, safe='()/')}"
    if mailto:
        url += f"?mailto={quote(mailto, safe='@')}"
    if _ROOT._cb_open(url):
        return dict(clean)
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research "
                "(https://skillhub.cn/skills/cite-holmes)"
            },
        )
        with _ROOT._urlopen_retry(req, timeout) as resp:
            m = (json.loads(resp.read().decode("utf-8", "ignore")) or {}).get("message") or {}
        _ROOT._cb_record(url, False)
        for item in m.get("updated-by") or []:
            if not isinstance(item, dict):
                continue
            nature = _retraction_classify(item.get("type") or "")
            if not nature:
                continue
            notice = item.get("DOI") or ""
            when = ((item.get("updated") or {}).get("date-time") or "")[:10]
            if nature in ("retraction", "partial_retraction", "withdrawal"):
                return {
                    "retracted": True,
                    "nature": nature,
                    "notice_doi": notice,
                    "when": when,
                    "source": "crossref",
                    "check_failed": False,
                }
            # EoC/更正：不升级为 retracted，但分档记录（EoC 由调用方降级转人工）
            clean.update(nature=nature, notice_doi=notice, when=when, source="crossref")
        return dict(clean)
    except urllib.error.HTTPError:
        _ROOT._cb_record(url, False, degrade=False)  # 站点有响应（含 429 限流）：不计入全局降级
        return dict(clean)
    except Exception:
        _ROOT._cb_record(url, True)
        return dict(failed)


def _openalex_fetch(url: str, timeout: float, ua: str):
    """v6.4.0 M2：OpenAlex 拉取（429 单次退避重试）。无 key 每日 100 credits
    限流实测高频（doctor 已提示 key 制）——遇 429 尊重 Retry-After（封顶 5s）
    退避重试一次，避免把限流抖动当「未收录」降级；仍 429 则原样抛给调用方
    既有诚实路径。断路器由调用方负责（本助手不触碰 _cb_*）。"""
    last = None
    for attempt in (0, 1):
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", "ignore"))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                ra = 2.0
                try:
                    if e.headers and e.headers.get("Retry-After"):
                        ra = min(5.0, max(1.0, float(e.headers["Retry-After"])))
                except (TypeError, ValueError):
                    pass
                time.sleep(ra)
                last = e
                continue
            raise
        except Exception as e:
            last = e
            break
    raise last


def openalex_works_lookup(title: str, year, timeout: float) -> tuple:
    """v4.3.0 OpenAlex 书目检索升级版：确认存在性 + 候选 DOI 锚。

    背景（TA 表在线甄别实锤）：39 条候选中文医学期刊映射仅 18 条有 PubMed 收录——
    非 MEDLINE 期刊（中华神经科杂志等 21 条）与万方系期刊的引用此前无任何官方
    核验通路。本函数把 v1.8 的「只确认」升级为「找锚→验锚」链的前半程：
    OpenAlex 检索命中（_title_sim ≥0.82 且年份相容）即提取该记录的 DOI，
    交给 DOI.org 权威核验（verify_one 接线）——OpenAlex 只当索引用，
    判定证据全部来自注册库，聚合库质量参差不影响判定权威性。
    无 DOI 候选或相似度不足时维持 v1.8 语义（确认→partial；查无永不判死）。

    返回 (note, confirmed, doi_candidate)。"""
    if len((title or "").strip()) < 18:
        return "", False, ""
    q = quote(title.strip(), safe="")
    url = (
        f"https://api.openalex.org/works?search={q}&per-page=3"
        "&select=display_name,publication_year,doi"
    )
    key = _ROOT._OPTS.get("openalex_key") or ""
    if key:
        url += f"&api_key={quote(key, safe='')}"
    try:
        if _ROOT._cb_open(url):
            return "", False, ""
        results = (
            _ROOT._openalex_fetch(
                url, timeout, f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"
            )
            or {}
        ).get("results") or []
        _ROOT._cb_record(url, False)
        if not results:
            return "OpenAlex 未检索到明显匹配条目（可能未被收录，不作为编造依据）", False, ""
        try:
            year_i = int(str(year)) if year else None
        except (TypeError, ValueError):
            year_i = None
        best = None  # (sim, w)
        for w in results:
            mt = re.sub(r"\s+", " ", str(w.get("display_name") or "")).strip()
            if not mt:
                continue
            sim = _ROOT._title_sim(title, mt)
            my = w.get("publication_year")
            year_ok = (not year_i) or (not my) or abs(year_i - int(my)) <= 1
            if year_ok and (best is None or sim > best[0]):
                best = (sim, w)
        if best is None:
            return ("OpenAlex 未检索到明显匹配条目（可能未被收录，不作为编造依据）", False, "")
        sim, w = best
        mt = re.sub(r"\s+", " ", str(w.get("display_name") or "")).strip()
        my = w.get("publication_year")
        year_note = f"（{my}）" if my else ""
        doi_c = str(w.get("doi") or "").replace("https://doi.org/", "").strip()
        if sim >= 0.82:
            return (f"OpenAlex 书目确认存在：{mt[:60]}{year_note}", True, doi_c)
        if sim >= 0.60:
            return (
                f"OpenAlex 近似条目（标题相似度 {sim:.2f}）：{mt[:60]}{year_note}，" "建议人工复核",
                False,
                "",
            )
        return (
            f"OpenAlex 未检索到明显匹配（最高相似度 {sim:.2f}）；"
            "可能未被收录或较新，不作为编造依据",
            False,
            "",
        )
    except urllib.error.HTTPError as e:
        _ROOT._cb_record(url, True, degrade=False)  # 站点有响应：不计入全局网络降级
        if e.code == 403:
            return (
                "OpenAlex 拒绝访问（403）——2026 年起生产调用需 API key（无 key 每日仅 "
                "100 credits 测试额度），可用 --openalex-key 或环境变量 OPENALEX_API_KEY 配置后重试",
                False,
                "",
            )
        if e.code == 429:
            return (
                "OpenAlex 限流（429）——生产调用建议 --openalex-key 或环境变量 "
                "OPENALEX_API_KEY，稍后自动重试即可",
                False,
                "",
            )
        return "", False, ""
    except Exception:
        _ROOT._cb_record(url, True)
        return "", False, ""


def openalex_title_check(title: str, timeout: float) -> str:
    """v1.8 OpenAlex 书目级存在性核查（v4.3.0 起为 openalex_works_lookup 的
    兼容薄包装——丢弃 DOI 候选只返回注记，消除双实现漂移：同一题名两条路径
    必须给同一 confirmed 判定）。"""
    note, _confirmed, _doi = openalex_works_lookup(title, None, timeout)
    return note


def s2_citation_contexts(doi: str, timeout: float, max_samples: int = 3) -> dict:
    """v3.0.0 L3 引文语境层（Scite 平替的数据面）：对已 verified 的 DOI 引文拉取
    Semantic Scholar citations 端点(fields=contexts,intents,isInfluential)。
    产出「学界评价」素材：被引次数、引用语境摘录（后续文献如何提及本文）、
    intents 分类（background/methodology/result）、influential 标记。
    诚实边界：S2 contexts 覆盖率不均（实测部分空）——返回 coverage 字段如实标注，
    绝不装作全知。失败静默跳过（语境是增强信号,非判定依据）。CC BY 4.0 数据源。
    返回 {}（无数据）或 {"cited_by": int, "samples": [{"context","intents","influential","citing_title"}],
    "coverage": float}；v6.7.0 F67 增 {"skipped": "cn_mode"}（--cn 短路诚实降级，
    显式 --s2-key 放行）。"""
    url = (
        "https://api.semanticscholar.org/graph/v1/paper/DOI:"
        + quote(doi, safe="")
        + "/citations?fields=contexts,intents,isInfluential,title&limit=30"
    )
    if _ROOT._OPTS.get("cn_mode") and not _ROOT._OPTS.get("s2_key"):
        # v6.7.0 F67：--cn 下 S2 短路（诚实降级）。api.semanticscholar.org 在
        # 国内网络高频超时（断路器实测主力源）；语境是增强信号非判定依据，
        # 每条 25s×2 重试的白耗不划算。显式配 --s2-key = 用户声明可达，放行。
        return {"skipped": "cn_mode"}
    key = _ROOT._OPTS.get("s2_key") or ""
    if key:
        url += "&api_key=" + quote(key, safe="")
    if _ROOT._cb_open(url):
        return {}
    for attempt in range(2):
        _ROOT._s2_rate_wait()
        try:
            headers = {"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
            if key:
                headers["x-api-key"] = key
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                _ROOT._cb_record(url, False)
                data = json.loads(resp.read().decode("utf-8", "ignore")) or {}
            break
        except urllib.error.HTTPError as e:
            _ROOT._cb_record(url, False)
            if e.code == 429 and attempt == 0:
                time.sleep(6)  # S2 共享池限流常态：单次退避
                continue
            return {}
        except Exception:
            # 传输层错误（SSL EOF 等，弱网出口实测常见）：单次快速重试，仍败才记熔断
            if attempt == 0:
                time.sleep(2)
                continue
            _ROOT._cb_record(url, True)
            return {}
    else:
        return {}
    items = data.get("data") or []
    if not items:
        return {"cited_by": 0, "samples": [], "coverage": 0.0}
    with_ctx = [it for it in items if (it.get("contexts") or [])]
    samples = []
    for it in with_ctx[:max_samples]:
        cp = it.get("citingPaper") or {}
        samples.append(
            {
                "context": (it.get("contexts") or [""])[0][:220],
                "intents": it.get("intents") or [],
                "influential": bool(it.get("isInfluential")),
                "citing_title": (cp.get("title") or "")[:80],
            }
        )
    return {
        "cited_by": len(items),
        "samples": samples,
        "coverage": round(len(with_ctx) / len(items), 2),
    }


def s2_doi_confirm(doi: str, title: str, timeout: float) -> tuple:
    """v1.9 Semantic Scholar 第三源交叉确认——定位是「第二路正面信号」：
    仅在 DOI.org 元数据未能取得时（网络受限/瞬时 5xx）由 S2 再给一次存在性确认，
    着陆页反爬救回时与 DOI/arXiv 元数据同门槛（仍走层级/字段门控）。
    实测 S2 记录质量参差（存在把正式论文登记成期刊目录页的情况）——因此
    ①只确认不降级：标题不一致一律静默，绝不下调判定；
    ②查无/限流/失败一律静默跳过（S2 收录不全，查无 ≠ 编造）。
    返回 (matched, note)。key 只走 x-api-key 头（query 参数会进代理日志）。"""
    if not (title or "").strip():
        return False, ""  # 无标题无从比对，不浪费限速调用
    url = (
        "https://api.semanticscholar.org/graph/v1/paper/DOI:"
        + quote(doi, safe="")
        + "?fields=title,year"
    )
    key = _ROOT._OPTS.get("s2_key") or ""
    if _ROOT._cb_open(url):
        return False, ""
    _ROOT._s2_rate_wait()
    try:
        headers = {"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
        if key:
            headers["x-api-key"] = key
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            _ROOT._cb_record(url, False)
            j = json.loads(resp.read().decode("utf-8", "ignore")) or {}
    except urllib.error.HTTPError:
        _ROOT._cb_record(url, False)  # 站点有响应（404/429 等）：不算传输失败
        return False, ""
    except Exception:
        _ROOT._cb_record(url, True)
        return False, ""
    mt = re.sub(r"\s+", " ", str(j.get("title") or "")).strip()
    my = j.get("year")
    if not mt or not (title or "").strip():
        return False, ""
    t = title.strip().lower()
    mt_l = mt.lower()
    sim = difflib.SequenceMatcher(None, t, mt_l).ratio()
    pfx = difflib.SequenceMatcher(None, t, mt_l[: len(t)]).ratio() if len(mt_l) >= len(t) else 0.0
    if max(sim, pfx) < 0.82:
        return False, ""  # 不一致静默：绝不以 S2 的不一致作负面判据
    year_note = f"（{my}）" if my else ""
    return True, f"Semantic Scholar 交叉确认存在：{mt[:60]}{year_note}（DOI.org 之外的第二路确认）"


def s2_title_confirm(title: str, timeout: float) -> tuple:
    """v1.10 Semantic Scholar 标题检索确认——无 DOI/PMID/arXiv 引用（.bib 导入常见）
    的第三路正面信号（与 OpenAlex 书目核查并列，互为备份：两库收录面不同）。
    与 s2_doi_confirm 同纪律：只确认不降级——查无/限流/失败一律静默跳过，
    绝不以下调判定（S2 收录不全 + 记录质量参差）。
    实现细节（S2 官方文档确认）：/paper/search 的 query 为纯文本，连字符词
    （如 state-of-the-art）查询无结果——先把连字符归一为空格再编码。
    返回 (matched, note)。key 只走 x-api-key 头。"""
    t = (title or "").strip()
    if len(t) < 18:
        return False, ""  # 过短标题检索噪声大，不浪费限速调用
    q = quote(re.sub(r"[-\u2010-\u2015]+", " ", t), safe="")
    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/search"
        f"?query={q}&fields=title,year&limit=1"
    )
    key = _ROOT._OPTS.get("s2_key") or ""
    if _ROOT._cb_open(url):
        return False, ""
    _ROOT._s2_rate_wait()
    try:
        headers = {"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
        if key:
            headers["x-api-key"] = key
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            _ROOT._cb_record(url, False)
            j = json.loads(resp.read().decode("utf-8", "ignore")) or {}
    except urllib.error.HTTPError:
        _ROOT._cb_record(url, False)  # 站点有响应（404/429 等）：不算传输失败
        return False, ""
    except Exception:
        _ROOT._cb_record(url, True)
        return False, ""
    data = j.get("data")
    if not isinstance(data, list) or not data:
        return False, ""  # 查无 ≠ 编造（收录滞后），静默
    w = data[0] or {}
    mt = re.sub(r"\s+", " ", str(w.get("title") or "")).strip()
    my = w.get("year")
    if not mt:
        return False, ""
    t_l = t.lower()
    mt_l = mt.lower()
    sim = difflib.SequenceMatcher(None, t_l, mt_l).ratio()
    pfx = (
        difflib.SequenceMatcher(None, t_l, mt_l[: len(t_l)]).ratio()
        if len(mt_l) >= len(t_l)
        else 0.0
    )
    if max(sim, pfx) < 0.82:
        return False, ""  # 不一致静默：绝不以 S2 的不一致作负面判据
    year_note = f"（{my}）" if my else ""
    return True, f"Semantic Scholar 标题检索确认存在：{mt[:60]}{year_note}"
