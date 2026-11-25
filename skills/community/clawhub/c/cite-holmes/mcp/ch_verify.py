"""cite-holmes v6.0.0 模块层：ch_verify（由手术脚本从单文件引擎分层，
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


def discover_refs(
    topic: str,
    limit: int = 10,
    timeout: float = 15.0,
    since: int = None,
    sort: str = "relevance",
    policy: dict = None,
) -> tuple:
    """v4.5.0 文献发现：主题 → PubMed + OpenAlex 双源检索 → 候选清单。

    把 skill 从「验已有的文献」扩展为「找文献且出生即核验」——检索结果天然
    带官方标识符（PMID/DOI），交回主管道后走全部既有核验栈（含撤稿检测），
    输出一份每条都验过的文献清单（GB/T/BibTeX 一键导出）。
    返回 (refs, notes)：单源失败静默跳过（绝不因单源失败崩批）；
    跨源按 doi/pmid/题名规一化去重；since 过滤出版年（近 N 年检索）。
    v4.6.0：跨源题名合并——同一论文一侧带 DOI 一侧仅题名时合并字段不再重复
    （原三级互斥键只认同键，跨源残余重复）。"""
    refs, notes = [], []
    seen = set()

    def _key(doi, pmid, title):
        return (
            f"doi:{doi.lower()}"
            if doi
            else (
                f"pmid:{pmid}"
                if pmid
                else "t:" + re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (title or "").lower())[:60]
            )
        )

    def _add(doi, pmid, title, source, year, cited_by=None, src_type=None):
        doi = (doi or "").replace("https://doi.org/", "").strip()
        pmid = str(pmid or "").strip()
        title = re.sub(r"\s+", " ", str(title or "")).strip()
        if not title or len(title) < 15:
            return
        k = _key(doi, pmid, title)
        if k in seen or k == "t:":
            return
        seen.add(k)
        ref = {"title": title, "source": str(source or ""), "year": year}
        if doi and _ROOT.DOI_RE.match(doi):
            ref["doi"] = doi
        if pmid and _ROOT.PMID_RE.match(pmid):
            ref["pmid"] = pmid
        if isinstance(cited_by, int) and cited_by >= 0:
            ref["_cited_by"] = cited_by  # v4.9.0 综述工作台展示用（核验期 S2 优先）
        if src_type:
            ref["_src_type"] = str(src_type)  # v5.2.0 信源政策（journal_only 过滤依据）
        refs.append(ref)

    limit = max(1, min(int(limit or 10), 25))
    sort = sort if sort in ("relevance", "cited", "newest") else "relevance"
    # 源一：PubMed 主题检索（官方题录，PMID 天然在握）；newest→pub_date，
    # cited→relevance（PubMed 无被引序，回退并在 notes 声明）
    pm_sort = "pub_date" if sort == "newest" else "relevance"
    if sort == "cited":
        notes.append("PubMed 无被引排序——该源按相关性回退")
    try:
        u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi" + _ROOT._ncbi_qs(
            f"?db=pubmed&retmode=json&retmax={limit}&sort={pm_sort}" f"&term={quote(topic)}"
        )
        if not _ROOT._cb_open(u):
            _ROOT._ncbi_rate_wait()
            req = urllib.request.Request(
                u, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
            )
            with _ROOT._urlopen_retry(req, timeout) as resp:
                j = json.loads(resp.read().decode("utf-8", "ignore"))
            _ROOT._cb_record(u, False)
            ids = [str(x) for x in ((j.get("esearchresult") or {}).get("idlist") or [])]
            if ids:
                u2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi" + _ROOT._ncbi_qs(
                    f"?db=pubmed&retmode=json&id={','.join(ids)}"
                )
                _ROOT._ncbi_rate_wait()
                req2 = urllib.request.Request(
                    u2,
                    headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"},
                )
                try:
                    with _ROOT._urlopen_retry(req2, timeout) as resp2:
                        j2 = json.loads(resp2.read().decode("utf-8", "ignore"))
                    _ROOT._cb_record(u2, False)
                except Exception:
                    _ROOT._cb_record(u2, True)  # 审计 P2：题录拉取失败也要进断路器记账
                    j2 = {}
                res = j2.get("result") or {}
                for pid in ids:
                    doc = res.get(pid) or {}
                    my = re.search(r"(19|20)\d{2}", str(doc.get("pubdate") or ""))
                    _add(
                        _ROOT._pmid_reg_doi(doc),
                        pid,
                        doc.get("title"),
                        doc.get("source") or "",
                        int(my.group(0)) if my else None,
                    )
            else:
                notes.append("PubMed 该主题零命中")
        else:
            notes.append("PubMed 断路器跳过")
    except urllib.error.HTTPError as e:
        _ROOT._cb_record(u, False, degrade=False)  # 审计 P2：服务器应答不熔断，但必须记账
        notes.append(
            f"PubMed HTTP {e.code}——本源跳过"
            + ("（限流，建议 NCBI_API_KEY）" if e.code in (429, 403) else "")
        )
    except Exception:
        _ROOT._cb_record(u, True)  # 审计 P2：传输失败必须进断路器/全局降级
        notes.append("PubMed 检索失败——本源跳过")
    # 源二：OpenAlex 主题检索（覆盖面更广，DOI 候选交回核验）
    ou = None
    try:
        q = quote(topic, safe="")
        ou = (
            f"https://api.openalex.org/works?search={q}&per-page={limit}"
            "&select=display_name,publication_year,doi,primary_location,cited_by_count"
            + (
                "&sort=cited_by_count:desc"
                if sort == "cited"
                else "&sort=publication_date:desc" if sort == "newest" else ""
            )
        )
        okey = _ROOT._OPTS.get("openalex_key") or ""
        if okey:
            ou += f"&api_key={quote(okey, safe='')}"
        if not _ROOT._cb_open(ou):
            oreq = urllib.request.Request(
                ou, headers={"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
            )
            with _ROOT._urlopen_retry(oreq, timeout) as oresp:
                oj = json.loads(oresp.read().decode("utf-8", "ignore"))
            _ROOT._cb_record(ou, False)
            for w in oj.get("results") or []:
                _src_obj = (
                    (w.get("primary_location") or {}).get("source")
                    if isinstance(w.get("primary_location"), dict)
                    else {}
                ) or {}
                _add(
                    w.get("doi"),
                    None,
                    w.get("display_name"),
                    _src_obj.get("display_name"),
                    w.get("publication_year"),
                    cited_by=w.get("cited_by_count"),
                    src_type=_src_obj.get("type"),
                )
        else:
            notes.append("OpenAlex 断路器跳过")
    except urllib.error.HTTPError as e:
        if ou:
            _ROOT._cb_record(ou, False, degrade=False)  # 服务器应答不熔断（自家惯例）
        notes.append(
            f"OpenAlex HTTP {e.code}——本源跳过"
            + (
                "（2026 年起生产调用需 --openalex-key）"
                if e.code == 403
                else "（限流）" if e.code == 429 else ""
            )
        )
    except Exception:
        if ou:
            _ROOT._cb_record(ou, True)
        notes.append("OpenAlex 检索失败——本源跳过")
    # v4.6.0：since 出版年过滤（无年份条目保留——宁多勿错杀）
    if since and int(since) >= 1900:  # 审计 P3：0/负数静默无效→下限门
        refs = [r for r in refs if not r.get("year") or int(r["year"]) >= int(since)]
    # 跨源题名合并：同题不同键（一侧 DOI 一侧仅题名）字段互补
    by_title, merged = {}, []
    for r in refs:
        tk = "t:" + re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", r["title"].lower())[:60]
        hit = by_title.get(tk)
        if hit is None:
            by_title[tk] = r
            merged.append(r)
        else:
            # 审计 P3：60 字符前缀碰撞可能是不同论文（如 part one vs part one
            # extended）——年份不相容不融合，防 crosscheck 假 invalid
            yr_ok = (
                not hit.get("year")
                or not r.get("year")
                or abs(int(hit["year"]) - int(r["year"])) <= 1
            )
            if yr_ok:
                for k, v in r.items():
                    if v and not hit.get(k):
                        hit[k] = v
                # 审计 P2-2：_cited_by=0 是有效测量值，falsy 守卫不得吞掉
                if hit.get("_cited_by") is None and r.get("_cited_by") is not None:
                    hit["_cited_by"] = r["_cited_by"]
    if policy and policy.get("journal_only"):  # v5.2.0 信源策展（discover 期硬过滤）
        _n0 = len(merged)
        merged = [
            r
            for r in merged
            if r.get("pmid") or r.get("_src_type") == "journal"  # PubMed 题录天然期刊
        ]
        if len(merged) < _n0:
            notes.append(
                f"信源政策 journal_only：过滤 {_n0 - len(merged)} 条"
                "非期刊源（预印本/知识库/未知类型）"
            )
    return merged, notes


def _parse_source_policy(spec: str):
    """v5.2.0 F30 信源政策解析：journal_only / allow-domain=a.org|b /
    deny-domain=x.com；逗号分段、竖线分域。非法段返回 None（调用方友好报错）。"""
    pol = {"journal_only": False, "allow": [], "deny": []}
    for seg in (spec or "").split(","):
        seg = seg.strip()
        if not seg:
            continue
        if seg == "journal_only":
            pol["journal_only"] = True
            continue
        for kind in ("allow-domain", "deny-domain"):
            if seg.startswith(kind + "="):
                doms = [d.strip().lower() for d in seg[len(kind) + 1 :].split("|") if d.strip()]
                if not doms:
                    return None
                pol["allow" if kind.startswith("allow") else "deny"].extend(doms)
                break
        else:
            return None
    return pol if (pol["journal_only"] or pol["allow"] or pol["deny"]) else None


def apply_source_policy(results: list, policy: dict, medical: bool = False) -> int:
    """v5.2.0 F30 信源政策（核验期）：违规**只注记+转人工**，绝不改判定
    （ADR-0005 纪律：政策是策展偏好不是真伪证据）。deny 命中/allow 未命中/
    journal_only 下非期刊 web 源 → checks.source_policy + note + needs_human。
    返回注记条数。"""
    if not policy:
        return 0
    n = 0
    for r in results:
        host = _ROOT._host_of(r.get("url") or "")
        viol = ""
        for d in policy.get("deny") or []:
            if host == d or host.endswith("." + d):
                viol = f"deny-domain 命中 {d}（该域已被政策排除）"
                break
        if not viol and policy.get("allow"):
            if host and not any(host == d or host.endswith("." + d) for d in policy["allow"]):
                viol = "allow-domain 未命中（来源不在政策允许域内）"
        if not viol and policy.get("journal_only") and host and r.get("url"):
            try:
                if _ROOT.classify_tier(r.get("url") or "", medical) != "journal":
                    viol = "journal_only：非期刊 web 来源（层级见 tier 列）"
            except Exception:
                pass
        if viol:
            r.setdefault("checks", {})["source_policy"] = {"violation": viol}
            r["note"] = (
                (r.get("note") + "；") if r.get("note") else ""
            ) + f"信源政策：{viol}——引用前请人工确认"
            r["needs_human_check"] = True
            n += 1
    return n


def apply_research_profile(path: str, args):
    """v5.3.0 F33 持久研究档案：JSON 键作**默认值**注入（显式 CLI 优先——
    只填空缺旗标，绝不覆盖用户显式值），返回已应用项清单（空表=档案全被
    显式旗标覆盖/空档案）；硬失败返回 None。未知键注记忽略（不失败）。
    绝不改判定语义——档案是过程偏好，不是真伪证据。"""
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError) as e:
        print(f"❌ 研究档案读取失败：{e}（--research-profile 需要结构化 JSON）", file=sys.stderr)
        return None
    if not isinstance(doc, dict):
        print("❌ 研究档案须为 JSON 对象（preset/source_policy/export 三键）", file=sys.stderr)
        return None
    known = {"preset", "source_policy", "export"}
    unknown = [k for k in doc if k not in known]
    if unknown:
        print(
            f"[profile] 未知键忽略：{', '.join(unknown)}（支持：preset / "
            "source_policy / export）"
        )
    applied = []
    pv = str(doc.get("preset") or "").strip()
    if pv and not getattr(args, "preset", ""):
        if pv not in ("submission", "deep"):
            print(f"❌ 档案 preset 非法：{pv}（支持 submission/deep）", file=sys.stderr)
            return None
        args.preset = pv
        applied.append(f"preset={pv}")
    sv = str(doc.get("source_policy") or "").strip()
    if sv and not getattr(args, "source_policy", ""):
        if _parse_source_policy(sv) is None:
            print(f"❌ 档案 source_policy 非法：{sv}", file=sys.stderr)
            return None
        args.source_policy = sv
        applied.append("source_policy=" + sv)
    ev = str(doc.get("export") or "").strip()
    if ev and not getattr(args, "export", ""):
        ok_fmts = {"bibtex", "gbt7714", "gb", "ris", "csv", "auditjson"}
        bad = [x for x in (t.strip().lower() for t in ev.split(",")) if x and x not in ok_fmts]
        if bad:
            print(f"❌ 档案 export 含未知格式：{bad}", file=sys.stderr)
            return None
        args.export = ev
        applied.append(f"export={ev}")
    return applied


def build_next_round(report: dict, out_path: str):
    """v5.5.0 F41 下一轮种子：从核验 JSON 报告提取未决条目生成重验骨架。
    收录 partial/unreachable/unverified（invalid 是终局判定不回收——死路不再
    撞）；每条带 _retry_reason（原注记截断）与原标识符，判定字段绝不写入
    （骨架是输入不是结论）。返回 (out_path, n)。硬失败 raise ValueError。"""
    results = report.get("results") if isinstance(report, dict) else None
    if not isinstance(results, list):
        raise ValueError("报告缺 results 数组——请提供本工具生成的完整 JSON")
    keep = []
    for r in results:
        if not isinstance(r, dict) or r.get("verdict") not in (
            "partial",
            "unreachable",
            "unverified",
        ):
            continue
        ref = {
            k: r.get(k)
            for k in ("title", "url", "doi", "pmid", "arxiv", "source", "year")
            if r.get(k)
        }
        if not ref:
            continue
        ref["_retry_reason"] = re.sub(r"\s+", " ", str(r.get("note") or ""))[:120]
        keep.append(ref)
    skeleton = {
        "_comment": (
            "cite-holmes 下一轮重验骨架（v%s 生成）：按需修订"
            "字段后作为 --refs 输入重跑；_retry_reason 仅供人读，"
            "引擎忽略未知键" % _ROOT.VERSION
        ),
        "refs": keep,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(skeleton, f, ensure_ascii=False, indent=2)
    return out_path, len(keep)


def _trace_append(path: str, mode: str, fields: dict) -> None:
    """v5.2.0 F31 研究底稿（append-only 审计链）：discover/verify 各轮追加
    轮次记录。只追加绝不改写；写失败静默（底稿是增强产物，绝不阻断主流程）。"""
    try:
        with open(os.path.expanduser(path), "a", encoding="utf-8") as f:
            f.write(f"\n## {time.strftime('%Y-%m-%d %H:%M:%S')} · {mode}\n")
            for k, v in fields.items():
                f.write(f"- {k}: {v}\n")
    except (OSError, ValueError):
        pass


def verify_one(ref: dict, idx: int, offline: bool, timeout: float, medical: bool = False) -> dict:
    """verify_one 对外入口（v5.6.0 拆分：核心 _verify_one_impl + 统一后处理）。
    OA 富集在 wrapper 统一接线——四条提前 return 的 verified 路径
    （PMID 反查/卷期页锚定/OpenAlex 找锚/着陆页救回）与主路径一样被覆盖。"""
    out = _verify_one_impl(ref, idx, offline, timeout, medical)
    if not offline:
        _ROOT._open_access_enrich(out, timeout)
    return out


def _verify_one_impl(
    ref: dict, idx: int, offline: bool, timeout: float, medical: bool = False
) -> dict:
    def _s(v):
        return str(v) if v is not None else ""

    title_in = _s(ref.get("title"))
    out = {
        "index": idx,
        "title": title_in or "(无标题)",
        "url": _s(ref.get("url")).strip(),
        "doi": _s(ref.get("doi")).strip(),
        "pmid": _s(ref.get("pmid")).strip(),
        "arxiv": _ROOT.extract_arxiv_id(ref),
        "source": _s(ref.get("source")).strip(),
        "year": ref.get("year"),
        "tier": ref.get("tier") or "",
        "semantic": ref.get("semantic", ""),
        "verdict": "unverified",
        "http_status": None,
        "note": "",
        "needs_human_check": False,
        "checks": {},  # v1.9 透明工作底稿：逐项检查的结构化明细（随 JSON 报告/auditjson 导出）
        "semantic_audit": _ROOT.build_semantic_audit(ref),
    }  # v1.11 语义层底稿（dict 输入才非空）

    pmid = out["pmid"]
    doi_adj, doi_matched = "", False
    arxiv_adj, arxiv_matched = "", False
    retracted = False
    url = _ROOT.ref_to_url(ref)
    if not url:
        raw_arxiv = str(ref.get("arxiv") or "").strip()
        if raw_arxiv and not out["arxiv"]:
            out.update(
                verdict="invalid",
                note="arxiv 字段格式无法识别（应为 YYMM.NNNNN 或 category/NNNNNNN）",
            )
        else:
            # v3.4 外部独测合并(#2):无标识符引用先走标题检索(与 SKILL.md「查无≠编造」
            # 声明对齐)——确认存在→partial 保留;查无→unverified 转人工(诚实未知),
            # 不得以「缺标识符」判编造。离线模式维持原 invalid。
            t_claim = _ROOT.clean_title(str(ref.get("title") or "")).strip()
            if offline or not t_claim:
                out.update(
                    verdict="invalid",
                    note="缺少 url 且无可解析的 doi/pmid/arxiv"
                    + ("（pmid 须为 6-9 位数字）" if pmid else ""),
                )
                return out
            # v4.0.0 Vancouver 医学引用的官方核验通道（PubMed 题名反查）——
            # 置于 OpenAlex/S2 之前：它是唯一能给出「官方一致→verified」的无
            # 标识符通道；未命中静默，继续现有确认路径（只确认不降级不变）
            pm_adj, pm_note, pm_matched, rev_pmid, pm_net_err = _ROOT.pubmed_title_reverse_lookup(
                t_claim, str(ref.get("source") or ""), ref.get("year"), max(timeout, 20.0)
            )  # 反查=esearch+esummary 两跳，单跳超时给足
            _eutils_open = any(d.get("open") for hk, d in _ROOT._CB.items() if "eutils" in hk)
            out["checks"]["pubmed_reverse"] = {
                "ran": True,
                "matched": pm_matched,
                "pmid": rev_pmid or None,
                "skipped_by_circuit": (not pm_matched and not pm_note and _eutils_open),
                # v4.1.0：传输失败与查无必须可区分（报告层按此注明「核验未完成」）
                "network_error": pm_net_err,
            }
            if pm_note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + pm_note
            if pm_matched and pm_adj == "":
                # 审计 P3 修复:PMID 锚结构化回填——bibtex/CSV 导出与批内去重可获取
                if not out.get("pmid"):
                    out["pmid"] = rev_pmid
                out.update(
                    verdict="verified",
                    needs_human_check=False,
                    note=(out["note"] + "；" if out["note"] else "")
                    + "无标识符引用经 PubMed 官方题名反查核验一致，已回填 PMID 锚",
                )
                return out
            if pm_adj == "partial":
                out.update(verdict="partial", needs_human_check=True)
                return out
            # v4.2.0 卷期页锚定（题名反查未命中后的第二无标识符通道）：
            # 期刊+年+卷(期):页 是 PubMed 官方引文定位器，语言无关——
            # 中文声称题名 vs 登记题名翻译差异不再阻断核验
            loc_adj, loc_note, loc_matched, loc_pmid, loc_err = _ROOT.pubmed_locator_lookup(
                out["source"],
                ref.get("year"),
                ref.get("volume"),
                ref.get("issue"),
                ref.get("pages"),
                max(timeout, 15.0),
                claimed_title=t_claim,
            )
            out["checks"]["pubmed_locator"] = {
                "ran": bool(out["source"] and ref.get("volume") and ref.get("year")),
                "matched": loc_matched,
                "pmid": loc_pmid or None,
                "network_error": loc_err,
            }
            if loc_note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + loc_note
            if loc_matched and loc_adj == "":
                if not out.get("pmid"):
                    out["pmid"] = loc_pmid
                out.update(
                    verdict="verified",
                    needs_human_check=False,
                    note=(out["note"] + "；" if out["note"] else "")
                    + "无标识符引用经 PubMed 卷期页锚定核验一致，已回填 PMID 锚",
                )
                return out
            oa_note, oa_confirmed, oa_doi = _ROOT.openalex_works_lookup(
                t_claim, ref.get("year"), timeout
            )
            out["checks"]["openalex"] = {
                "ran": True,
                "confirmed": oa_confirmed,
                "doi_candidate": oa_doi or None,
            }
            s2_matched, s2_note = _ROOT.s2_title_confirm(t_claim, timeout)
            out["checks"]["s2_title"] = {"matched": s2_matched}
            if oa_note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + oa_note
            if s2_note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + s2_note
            # v4.3.0 找锚→验锚链：OpenAlex 确认且带候选 DOI → DOI.org 权威核验。
            # OpenAlex 只当索引（聚合库记录质量参差，v1.8 既有结论），判定证据
            # 全部来自注册库；标题不符按 DOI 通路语义判（错引不因「存在相似条目」
            # 放行）；撤稿检测照走，锚定通路不绕开安全检查。
            if oa_confirmed and oa_doi and not offline and _ROOT.DOI_RE.match(oa_doi):
                doi_adj2, note2, doi_m2, csl2 = _ROOT.doi_metadata_match(
                    oa_doi,
                    _ROOT.clean_title(str(ref.get("title") or "")),
                    ref.get("year"),
                    timeout,
                    str(ref.get("source") or ""),
                    str(ref.get("authors") or ""),
                )
                out["checks"]["doi_metadata"] = {
                    "matched": doi_m2,
                    "adjust": doi_adj2,
                    "via": "openalex-anchor",
                }
                if csl2:
                    out["checks"]["doi_metadata"]["csl"] = csl2
                if note2:
                    out["note"] = (out["note"] + "；" if out["note"] else "") + note2
                ret2 = _ROOT.crossref_retraction_check(oa_doi, timeout)
                retracted = bool(ret2.get("retracted"))
                out["checks"]["retraction"] = ret2
                if ret2.get("nature"):
                    out["note"] = (
                        out["note"] + "；" if out["note"] else ""
                    ) + _ROOT._retraction_nature_note(
                        ret2["nature"],
                        ret2["when"],
                        ret2["notice_doi"],
                        (
                            "本地 Retraction Watch 索引"
                            if ret2.get("source") == "local"
                            else "Crossref/Retraction Watch"
                        ),
                    )
                elif ret2.get("check_failed"):
                    out["note"] = (
                        out["note"] + "；" if out["note"] else ""
                    ) + "撤稿检查未完成（网络传输失败，重试后仍不通）——非「未撤稿」"
                if doi_adj2 == "invalid":
                    out.update(verdict="invalid", needs_human_check=True)
                    return out
                if doi_adj2 == "":
                    if not doi_m2:
                        # 审计 P0 修复：元数据获取失败/断路器跳过的 adjust="" 不等于
                        # 「核验一致」——CN 网络 doi.org 常态不通，此场景旧逻辑会把
                        # 失败当一致升 verified。诚实封顶 partial 转人工
                        out.update(verdict="partial", needs_human_check=True)
                        return out
                    if retracted or ret2.get("nature") == "expression_of_concern":
                        out.update(verdict="partial", needs_human_check=True)
                    else:
                        if not out.get("doi"):
                            out["doi"] = oa_doi
                        out.update(
                            verdict="verified",
                            needs_human_check=False,
                            note=(out["note"] + "；" if out["note"] else "")
                            + "无标识符引用经 OpenAlex 找锚、DOI.org 权威核验一致，已回填 DOI 锚",
                        )
                    return out
                # doi_adj2 == "partial"（跨语言桥接未命中/相似度居中）→ 封顶 partial
                out.update(verdict="partial", needs_human_check=True)
                return out
            if oa_confirmed:
                out.update(verdict="partial", needs_human_check=True)
                return out
            out.update(
                verdict="unverified",
                needs_human_check=True,
                note=(out["note"] + "；" if out["note"] else "")
                + "无标识符且两库标题检索未确认——未知状态转人工，不作编造判定",
            )
            return out
        return out
    if not re.match(r"^https?://", url, re.IGNORECASE):
        out.update(verdict="invalid", note=f"url 非 http(s) 格式: {url[:60]}")
        return out

    if not out["tier"]:
        out["tier"] = _ROOT.classify_tier(url, medical)
    out["url"] = url
    if medical and out["tier"] in ("community", "social", "blog"):
        out["note"] = "医学模式：社区/社交/博客层来源不得支撑医学结论（仅作线索）"
    elif medical and out["tier"] == "preprint":
        out["note"] = "医学模式：预印本未经同行评审，证据强度受限"

    if offline:
        out["note"] = (out["note"] + "；" if out["note"] else "") + "offline 模式未做可达性检查"
    else:
        # 带 DOI 的引用优先走元数据核验：能同时判定「存在性」与「内容匹配」，
        # 且假 DOI 的 404 在这里直接判 invalid（不会先被可达性检查误判为 unreachable）
        retracted = False
        s2_matched = False
        if out["doi"] and _ROOT.DOI_RE.match(out["doi"]):
            doi_adj, note, doi_matched, doi_csl = _ROOT.doi_metadata_match(
                out["doi"],
                _ROOT.clean_title(str(ref.get("title") or "")),
                ref.get("year"),
                timeout,
                str(ref.get("source") or ""),
                str(ref.get("authors") or ""),
            )
            out["checks"]["doi_metadata"] = {"matched": doi_matched, "adjust": doi_adj}
            # v3.6:注册库权威元数据(GB/T 7714 导出原料)——仅 matched 时可信
            if doi_matched and doi_csl:
                out["checks"]["doi_metadata"]["csl"] = doi_csl
            if note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + note
            if doi_adj == "invalid":
                out.update(verdict="invalid", needs_human_check=True)
                return out
            # v1.9 Semantic Scholar 第三源：DOI.org 元数据没拿到时（网络受限/瞬时故障）
            # 的第二路正面确认——只确认不降级（S2 记录质量参差，不一致静默）
            if not doi_matched:
                s2_matched, s2note = _ROOT.s2_doi_confirm(
                    out["doi"], _ROOT.clean_title(str(ref.get("title") or "")), timeout
                )
                out["checks"]["s2"] = {"matched": s2_matched}
                if s2note:
                    out["note"] = (out["note"] + "；" if out["note"] else "") + s2note
            # v1.8 撤稿检测：真实存在的论文也可能是撤稿状态，不得作为有效证据
            # v4.1.0 分档：撤稿族降级转人工；EoC 同闸转人工；更正仅提示；
            # check_failed=True 可观测（传输失败≠「未撤稿」，报告层注明）
            ret = _ROOT.crossref_retraction_check(out["doi"], timeout)
            retracted = bool(ret.get("retracted"))
            out["checks"]["retraction"] = ret
            if ret.get("nature"):
                retnote = _ROOT._retraction_nature_note(
                    ret["nature"],
                    ret["when"],
                    ret["notice_doi"],
                    (
                        "本地 Retraction Watch 索引"
                        if ret.get("source") == "local"
                        else "Crossref/Retraction Watch"
                    ),
                )
            elif ret.get("check_failed"):
                retnote = (
                    "撤稿检查未完成（网络传输失败，重试后仍不通）——"
                    "本条结果不含撤稿核验，非「未撤稿」"
                )
            else:
                retnote = ""
            if retnote:
                out["note"] = (out["note"] + "；" if out["note"] else "") + retnote
                if retracted:  # EoC 的转人工在统一降级闸处理；更正提示不强制转人工
                    out["needs_human_check"] = True
        # 带 arXiv ID 的引用同层核验（无 DOI 时）：官方 API 查无记录 → 直接 invalid，
        # 同样先于可达性检查，避免假 ID 被误判为 unreachable（v1.5）
        elif out["arxiv"]:
            arxiv_adj, note, arxiv_matched = _ROOT.arxiv_metadata_match(
                out["arxiv"],
                _ROOT.clean_title(str(ref.get("title") or "")),
                ref.get("year"),
                timeout,
            )
            out["checks"]["arxiv_metadata"] = {"matched": arxiv_matched, "adjust": arxiv_adj}
            if note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + note
            if arxiv_adj == "invalid":
                out.update(verdict="invalid", needs_human_check=True)
                return out
        # v1.6：双键引用（doi+pmid）做交叉一致性——两键各自真实也可能拼接造假，
        # 元数据层判定，先于可达性检查
        if (
            out["doi"]
            and _ROOT.DOI_RE.match(out["doi"])
            and out["pmid"]
            and _ROOT.PMID_RE.match(out["pmid"])
        ):
            xadj, xnote = _ROOT.pmid_doi_crosscheck(out["pmid"], out["doi"], timeout)
            out["checks"]["doi_pmid_crosscheck"] = {"done": True}
            if xnote:
                out["note"] = (out["note"] + "；" if out["note"] else "") + xnote
            if xadj == "invalid":
                out.update(verdict="invalid", needs_human_check=True)
                return out
        reachable, status, note = _ROOT.check_url(url, timeout)
        out["http_status"] = status
        out["checks"]["url"] = {"reachable": reachable, "status": status}
        out["note"] = (out["note"] + "；" if out["note"] else "") + note
        if not reachable:
            # DOI/arXiv 注册元数据或 S2 交叉已确认存在 + 着陆页反爬（403/429）→
            # 引用存在性已被官方注册库证实，不能因反爬误判为 unreachable。评审修正：
            # 救回不再无条件盖 verified——层级/字段门控照走，防"真 ID + 403 博客链接"骗过权威层
            if (doi_matched or arxiv_matched or s2_matched) and status in (403, 429):
                label = "DOI" if doi_matched else "arXiv" if arxiv_matched else "Semantic Scholar"
                out["note"] = (
                    out["note"] + "；" if out["note"] else ""
                ) + f"着陆页反爬（HTTP {status}），但 {label} 注册元数据核验一致——存在性已确认"
                # v1.5 二轮评审 P1：元数据本身判 partial（相似度 0.50-0.82）时，
                # 救回同样不得给 verified——与 200 路径末尾的降级不变量保持一致，
                # 防"疑似错引"借反爬救回混进 verified（进而流入 bibtex/strict CI）
                if (
                    out["tier"] in _ROOT.TRUSTED_TIERS
                    and not _ROOT.missing_fields(ref)
                    and doi_adj != "partial"
                    and arxiv_adj != "partial"
                ):
                    out["verdict"] = "verified"
                else:
                    out["verdict"] = "partial"
                # v4.1.0：撤稿族与 EoC 同闸——反爬救回不得把带通告的文献盖成 verified
                if (
                    retracted
                    or (out["checks"].get("retraction") or {}).get("nature")
                    == "expression_of_concern"
                ) and out["verdict"] == "verified":
                    out["verdict"] = "partial"
                    out["needs_human_check"] = True
                return out
            # v1.5：arXiv ID 以 arxiv.org/abs 为官方解析器——官方站可达却对该 ID
            # 返回 404 → 官方库查无此 ID，判 invalid（官方 API 被墙时兜底）。
            # 评审修正（P0）：仅当元数据核验未能确认存在时才允许此判定——
            # 官方 API 刚确认过存在时，脏 URL 的 404 不得反转成 invalid；
            # 此逻辑仅适用于解析器域名，普通网页 404 仍是 unreachable
            elif (
                status == 404
                and not (doi_matched or arxiv_matched)
                and re.match(
                    r"^https?://(?:www\.|export\.)?arxiv\.org/(?:abs|pdf)/", url, re.IGNORECASE
                )
            ):
                out.update(
                    verdict="invalid",
                    needs_human_check=True,
                    note=(out["note"] + "；" if out["note"] else "")
                    + "arXiv 官方站对该 ID 返回 404（官方库查无）→ 疑似编造引用",
                )
                return out
            # v5.6.0 审计修复（T2 实战回归）：PubMed 落地页对不存在 PMID 开始返回
            # 真 404——unreachable 提前 return 不得屏蔽 E-utilities 权威存在性判定
            # （假 PMID 落地页 404 → 仍须判 invalid）。pubmed_pmid_exists 自身契约
            # fail-safe：传输失败按可达处理（True），只有注册库确凿查无才 False。
            m_pm = _ROOT.PUBMED_URL_RE.match(url)
            if m_pm:
                pmid_ok, pmid_note = _ROOT.pubmed_pmid_exists(m_pm.group(1), timeout)
                if not pmid_ok:
                    out.update(
                        verdict="invalid",
                        needs_human_check=True,
                        note=(out["note"] + "；" if out["note"] else "") + pmid_note,
                    )
                    return out
            out.update(
                verdict="unreachable",
                needs_human_check=True,
                note=(out["note"] + "；" if out["note"] else "")
                + "可能反爬/临时故障，不等于不存在",
            )
            # v1.5 存档兜底：不可达 ≠ 不存在，附 Wayback 存档链给人工复核做对照
            wb = _ROOT.wayback_available(url, timeout)
            out["checks"]["wayback"] = {"archive_found": bool(wb)}
            if wb:
                out["note"] = (out["note"] + "；" if out["note"] else "") + wb
            return out
        m = _ROOT.PUBMED_URL_RE.match(url)
        if m:
            pmid_ok, pmid_note = _ROOT.pubmed_pmid_exists(m.group(1), timeout)
            if not pmid_ok:
                out.update(
                    verdict="invalid",
                    needs_human_check=True,
                    note=(out["note"] + "；" if out["note"] else "") + pmid_note,
                )
                return out
            out["note"] = (out["note"] + "；" if out["note"] else "") + pmid_note
            # v3.4 池:PMID 元数据核验(标题+期刊一致性)——此前 PMID-only 引用
            # 仅查存在性,真 PMID+假标题/假期刊拼接可过 verified(评审缺口)
            if not offline and (
                str(ref.get("title") or "").strip() or str(ref.get("source") or "").strip()
            ):
                padj, pnote, pmatched = _ROOT.pmid_metadata_match(
                    m.group(1),
                    _ROOT.clean_title(str(ref.get("title") or "")),
                    str(ref.get("source") or ""),
                    ref.get("year"),
                    timeout,
                )
                out["checks"]["pmid_metadata"] = {"matched": pmatched, "adjust": padj}
                if pnote:
                    out["note"] = (out["note"] + "；" if out["note"] else "") + pnote
                if padj == "invalid":
                    out.update(verdict="invalid", needs_human_check=True)
                    return out
                if padj == "partial":
                    # v4.2.0 跨语言佐证升级：标题不可比（跨文字系统）partial 时，
                    # 卷期页锚定若唯一命中**同一 PMID**——注册库亲自确认了
                    # 「该组卷期页 ↔ 该 PMID」，声称引用恰好给出同组定位器，
                    # 标题差异纯属翻译——证据充分，解除终局 partial 封顶
                    if (
                        "跨语言标题无法机器比对" in pnote
                        and out["source"]
                        and ref.get("volume")
                        and ref.get("year")
                    ):
                        la, ln, lm_, lp, le = _ROOT.pubmed_locator_lookup(
                            out["source"],
                            ref.get("year"),
                            ref.get("volume"),
                            ref.get("issue"),
                            ref.get("pages"),
                            max(timeout, 15.0),
                            claimed_title=str(ref.get("title") or ""),
                        )
                        out["checks"]["pubmed_locator"] = {
                            "ran": True,
                            "matched": lm_,
                            "pmid": lp or None,
                            "network_error": le,
                        }
                        if ln:
                            out["note"] = (out["note"] + "；" if out["note"] else "") + ln
                        if lm_ and str(lp) == str(out["pmid"]):
                            out["checks"]["pmid_metadata"]["cross_lang_corroborated"] = True
                            out["note"] = (
                                out["note"] + "；" if out["note"] else ""
                            ) + "跨语言标题经卷期页锚定佐证（同一 PMID 唯一命中）——语言差异不作为编造依据"
                        else:
                            out.update(verdict="partial", needs_human_check=True)
                    else:
                        out.update(verdict="partial", needs_human_check=True)
        # v1.8 OpenAlex 书目级核查：无 DOI/PMID/arXiv 的引用多一路正面确认信号；
        # v1.10 S2 标题检索为并列第二路（两库收录面不同，互为备份；同样只确认不降级）
        if not out["doi"] and not out["pmid"] and not out["arxiv"]:
            oa_note = _ROOT.openalex_title_check(str(ref.get("title") or ""), timeout)
            out["checks"]["openalex"] = {"ran": True, "confirmed": "确认存在" in oa_note}
            if oa_note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + oa_note
            s2t_matched, s2t_note = _ROOT.s2_title_confirm(
                _ROOT.clean_title(str(ref.get("title") or "")), timeout
            )
            out["checks"]["s2_title"] = {"matched": s2t_matched}
            if s2t_note:
                out["note"] = (out["note"] + "；" if out["note"] else "") + s2t_note

    # v3.0.0 L3 引文语境层：verified 的 DOI 引文追加学界评价（默认开,--no-contexts 关）
    if (
        not offline
        and _ROOT._OPTS.get("contexts", True)
        and out["doi"]
        and _ROOT.DOI_RE.match(out["doi"])
    ):
        ctx = _ROOT.s2_citation_contexts(out["doi"], timeout)
        if ctx.get("skipped") == "cn_mode":
            # v6.7.0 F67：--cn 短路诚实透出（S2 国内高频超时；语境是增强信号）；
            # 先判后赋——skip 分支不先写 ran:True（审计 P2：防条件化陷阱）
            out["checks"]["citation_contexts"] = {
                "ran": False,
                "skipped": "cn_mode",
                "note": "S2 语境在 --cn 模式下跳过（国内可达性差；显式 --s2-key 可放行）",
            }
        elif ctx:
            out["checks"]["citation_contexts"] = {"ran": True, "cited_by": ctx.get("cited_by", 0)}
            out["citation_contexts"] = ctx
            n = ctx["cited_by"]
            cov = ctx.get("coverage", 0)
            note_ctx = f"学界评价：被引 {'≥' if n >= 30 else ''}{n} 次" f"（语境覆盖率 {cov:.0%}）"
            if ctx["samples"]:
                note_ctx += "；后续文献如是以引用：《" + ctx["samples"][0]["citing_title"] + "》"
            out["note"] = (out["note"] + "；" if out["note"] else "") + note_ctx
        else:
            out["checks"]["citation_contexts"] = {"ran": True, "cited_by": 0}

    miss = _ROOT.missing_fields(ref)
    if out["tier"] in _ROOT.TRUSTED_TIERS and not miss:
        out["verdict"] = "verified"
    else:
        why = []
        if out["tier"] not in _ROOT.TRUSTED_TIERS:
            why.append(f"来源层级为 {out['tier']}（非权威层）")
        if miss:
            why.append(f"缺字段 {','.join(miss)}")
        # v4.8.0 落地页题名对照（EB/OL 靶型）：partial 因非权威层/缺字段而
        # URL 可达时，抽页面题名对照——一致=「这条 URL 讲的就是这篇」的存在性
        # 证据，注记补强不改判定（partial 仍转人工；误确认代价=多一次人工复核）
        if (
            out["url"]
            and not offline
            and not retracted
            and (out.get("checks", {}).get("url") or {}).get("reachable")
        ):
            lt_note, lt_confirmed = _ROOT.landing_title_check(out["url"], out["title"], timeout)
            out["checks"]["landing"] = {"ran": True, "confirmed": lt_confirmed}
            if lt_confirmed:
                why.append("落地页题名对照一致（存在性佐证）")
                out["needs_human_check"] = True
            elif lt_note:
                why.append(lt_note)
        out["verdict"] = "partial"
        out["note"] = (out["note"] + "；" if out["note"] else "") + "；".join(why)

    # v1.4：元数据核验判为 partial 时，verified 降级为 partial
    # v5.5.0 审计 P1-1：arXiv partial（含 0.50-0.82 近似与别名守卫道）一律挂
    # 转人工旗——verification-details 承诺「转人工」，旗必须真挂（v4.1.0 P3-1
    # 自立红线：注记说转人工的旗不得缺席），复核漏斗才不漏计
    if (doi_adj == "partial" or arxiv_adj == "partial") and out["verdict"] == "verified":
        out["verdict"] = "partial"
    if arxiv_adj == "partial" and out["verdict"] == "partial":
        out["needs_human_check"] = True

    # v3.4 外部独测合并:PMID 元数据 partial 与 DOI/arXiv 同闸——降级不得被终局覆盖
    if (
        (out.get("checks", {}).get("pmid_metadata", {}) or {}).get("adjust") == "partial"
        and not (out.get("checks", {}).get("pmid_metadata", {}) or {}).get(
            "cross_lang_corroborated"
        )
        and out["verdict"] == "verified"
    ):
        out["verdict"] = "partial"
    # v4.1.0：撤稿族与 EoC 同闸降级（EoC=编辑关注通告，证据效力存疑转人工；
    # 更正/勘误不降级——仅提示注记）
    _ret_chk = out.get("checks", {}).get("retraction") or {}
    if (retracted or _ret_chk.get("nature") == "expression_of_concern") and out[
        "verdict"
    ] == "verified":
        out["verdict"] = "partial"
        out["needs_human_check"] = True
    elif _ret_chk.get("nature") == "expression_of_concern":
        # EoC 落在其他 partial 路径（层级/缺字段）也要挂人工旗——复核计数口径
        # 与撤稿族一致，注记说「转人工」旗标必须真挂（审计 P3-1）
        out["needs_human_check"] = True
    # offline 模式只做结构核验（格式/字段/层级/去重），可达性未验证——
    # 诚实起见 verified 封顶为 partial（避免离线盖章"已验证"）
    if offline and out["verdict"] == "verified":
        out["verdict"] = "partial"
        out["note"] = (
            out["note"] + "；" if out["note"] else ""
        ) + "offline 模式最高判 partial（可达性未验证）"
    return out


# ---------------- 语义层工作底稿（v1.11，semantic_audit） ----------------
# 模型在研究流程中对每条引用做语义判定（该来源是否真的支撑所引论断），v1.11 起
# 支持把判定以结构化对象写进 research_refs.json 的 semantic 字段，机械层负责校验
# 结构、透传进 auditjson/报告，并对否定性判定封顶——落实 GESIS 立场论文
# （arXiv:2607.22693）「disclosing their own uncertainty」的行业呼吁：
# 检测系统的语义不确定性必须可披露、可审计，而不是藏在模型"感觉"里。
# support 取值：supported（支撑）/ partial（部分支撑）/ not_in_source（来源未
# 包含该论断）/ contradicted（来源与论断相矛盾）/ unclear（无法判定）。
def annotate_preprint_upgrades(results: list, timeout: float) -> int:
    """v3.11 预印本→正式版提示（注记级，只增线索不改判定）：arXiv 引用
    verified 且未带 DOI 时，经 Semantic Scholar 同记录 externalIds 查该
    预印本是否已登记正式发表（期刊版 DOI/venue）——投稿场景引用预印本
    常被审稿人挑，此提示帮作者在提交前完成版本升级。失败/限流一律静默
    （S2 共享池限速走 _s2_rate_wait，断路器生效）；引用已带 DOI 则跳过。"""
    n = 0
    for r in results:
        if r.get("verdict") != "verified":
            continue
        ax = str(r.get("arxiv") or "").strip()
        if not ax or (r.get("doi") or "").strip():
            continue
        try:
            url = (
                f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{quote(ax)}"
                f"?fields=externalIds,venue,year"
            )
            if _ROOT._cb_open(url):
                continue
            _ROOT._s2_rate_wait()
            _hdrs = {"User-Agent": f"cite-holmes/{_ROOT.VERSION}; +verified-deep-research"}
            if _ROOT._OPTS.get("s2_key"):
                _hdrs["x-api-key"] = _ROOT._OPTS["s2_key"]  # 与 _ROOT.s2_doi_confirm 同款头
            req = urllib.request.Request(url, headers=_hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                _ROOT._cb_record(url, False)
                d = json.loads(resp.read().decode("utf-8", "ignore"))
            ext = d.get("externalIds") or {}
            jdoi = str(ext.get("DOI") or "").strip()
            venue = str(d.get("venue") or "").strip()
            if jdoi:
                venue = venue[:60]  # 截断外部数据:防超长与下游子串扫描误触发
                r["note"] = ((r.get("note") + "；") if r.get("note") else "") + (
                    f"该预印本已登记正式发表（{venue or '期刊版'}"
                    f"{' ' + str(d.get('year')) if d.get('year') else ''}，"
                    f"DOI:{jdoi}）——建议引用正式版（preprint→published 升级提示）"
                )
                n += 1
        except urllib.error.HTTPError:
            # 审计修复:HTTP 层失败（404 未收录/429 限流）不触发熔断——否则连续
            # 2 条未收录 arXiv ID 会熔断 api.semanticscholar.org,殃及同主机的
            # s2_doi_confirm 第二源确认（断路器契约:仅传输层失败计数）
            _ROOT._cb_record(url, False)
        except Exception:
            _ROOT._cb_record(url, True)
    return n


def check_document(text: str, results: list, anchor_threshold: float = 0.34) -> dict:
    """文档级上下文核验:抽取→绑定→锚词匹配。语义层(句子是否真被支撑)仍归 agent。
    v4.4.0：正文提取截断到「参考文献」节之前——节内 [N] 是清单编号不是引用标记，
    不截断会把每条文献「自引」成已引用，孤儿审计与引用数全部失真（真网实战
    首跑实锤：69 处"引用"含 16 个清单标签、覆盖度假 100%）。"""
    _m = _ROOT._REF_SECTION_RE.search(text)
    if _m:
        text = text[: _m.start()]
    cits = _ROOT.extract_citations(text)
    out = []
    cited_all = set()  # 复合标记（[1-3]/[1,3]）的全部绑定条目——审计 P1：
    # 原实现每标记只记首绑，医学高频的 [2-5] 会让条目 2-4 被误报孤儿
    for c in cits:
        b = _ROOT.bind_citation(c, results)
        for r in b["bound"] or []:
            if r is not None and r.get("index") is not None:
                cited_all.add(r["index"])
        for r in (b["bound"] or [None])[:1]:
            ar = _ROOT.anchor_rate(c["sentence"], r) if r else 0.0
            entry = {
                "marker": c["marker"],
                "sentence": c["sentence"][:300],
                "ref_index": (r or {}).get("index"),
                "ref_verdict": (r or {}).get("verdict"),
                "anchor_rate": round(ar, 3),
                "anchor": "ok" if ar >= anchor_threshold else "low",
                "bound": bool(r),
            }
            if not r:
                entry["note"] = "未绑定:正文中引用了清单外的编号/条目"
                entry["anchor"] = "n/a"
            out.append(entry)
    unbound = [e for e in out if not e["bound"]]
    low = [e for e in out if e["bound"] and e["anchor"] == "low"]
    # v4.4.0 引用完整性审计：孤儿文献（清单里列了、正文从未引用）与覆盖率。
    # 实锤：毛细支气管炎报告 16 条中 5 条（31%）从未被正文引用——列了没引是学术
    # 写作规范问题（漏引或冗列），不是编造——advisory 级，绝不改判定。
    cited_idx = {e["ref_index"] for e in out if e.get("ref_index") is not None}
    cited_idx |= cited_all
    listed_idx = sorted({r.get("index") for r in results if r.get("index") is not None})
    uncited = sorted(i for i in listed_idx if i not in cited_idx)
    coverage = (
        round(len([i for i in listed_idx if i in cited_idx]) / len(listed_idx), 2)
        if listed_idx
        else 0.0
    )
    return {
        "citations": out,
        "n_citations": len(out),
        "n_unbound": len(unbound),
        "n_low_anchor": len(low),
        "anchor_threshold": anchor_threshold,
        "n_listed": len(listed_idx),
        "n_uncited": len(uncited),
        "uncited_refs": uncited,
        "coverage": coverage,
        "note": (
            "锚词率=引文句与被引标题的内容词重叠(阈值 %.2f);low≠错引,"
            "是语义层人工复核候选;未引用条目=写作规范建议(漏引或冗列),"
            "非真伪问题" % anchor_threshold
        ),
    }


# ═══ v3.9.0 结构化错误码(errorHandling):五态之上的机器可读细分 ═══
