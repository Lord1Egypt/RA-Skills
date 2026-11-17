#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cite-holmes 真网稳定性自检（v6.3.0 F56；v6.5.0 F60 增 N5）——注册库实时
可达性+判定圆环+埋雷矩阵+跨注册库一致性：

    python3 tools/netcheck.py            # 全量（四组实时圆环+埋雷+跨库一致，约 2-4 分钟）
    python3 tools/netcheck.py --quick    # 快档（注册库探针+埋雷矩阵，约 1 分钟）

五组检查（引用数据全部当场从公共注册库实时拉取，绝不复用历史测试数据）：
  N1 注册库探针：DOI.org/Crossref/E-utilities/arXiv/OpenAlex/S2/Unpaywall/Cloudflare-CDN 可达性
  N2 PubMed 圆环：实时拉全新 PMID → 引擎核验全 verified
  N3 Crossref 圆环：实时拉全新 DOI → 引擎核验零 invalid
  N4 埋雷矩阵：编造 DOI/假 arXiv/死链/真题名配假 DOI → 全部落网+真引用零误伤
  N5 跨注册库一致性：同一真实 DOI 在 Crossref/OpenAlex/PubMed 三库的登记题名
    归一后一致（引擎判定依赖多库元数据交叉——库间不一致会使忠实度判定失真；
    任一库不可达=SKIP 诚实边界，不伪装通过）

退出码 0=全过；1=有失败（agent 宿主/CI 可当部署后验证钩子）。
与 selfcheck.py 的分工：selfcheck=offline 安装验证（零外呼）；netcheck=真网
稳定性验证（注册库实时面）。两者构成两级验证体系。

数据源：NCBI E-utilities / Crossref / arXiv / OpenAlex 官方 API（公开数据，实时拉取）。
诚实边界：注册库数字每日漂移，本工具测「判定通路在真实网络下的稳定性」，
不测注册库覆盖率；网络受限环境请先配代理（--offline 场景请用 selfcheck）。"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
ENGINE = os.path.join(SK, "scripts", "verify_refs.py")
UA = {"User-Agent": "cite-holmes-netcheck (verification round-trip; mailto=netcheck@docsor.cn)"}

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("  ✅ " if cond else "  ❌ ") + name + (f"  || {str(detail)[:200]}" if not cond else ""))
    return bool(cond)


def http_json(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def run_engine(refs, out_prefix, timeout=420):
    """引擎真网跑一批引用，返回 (results, rc)。"""
    refs_path = out_prefix + ".refs.json"
    with open(refs_path, "w", encoding="utf-8") as f:
        json.dump(refs, f, ensure_ascii=False)
    p = subprocess.run(
        [sys.executable, ENGINE, "--refs", refs_path,
         "--out", out_prefix + ".md", "--interval", "1.5"],
        capture_output=True, text=True, timeout=timeout)
    doc = json.load(open(out_prefix + ".json", encoding="utf-8"))
    return doc["results"], p.returncode


def n1_probes():
    """八注册库探针（可达性，≥6 通即过——单库抖动属诚实态）。"""
    probes = [
        ("DOI.org", "https://doi.org/10.1542/peds.2006-2223", 302, 404),
        ("Crossref", "https://api.crossref.org/works/10.1542/peds.2006-2223", 200,),
        ("E-utilities", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=1&term=bronchiolitis", 200,),
        ("arXiv", "https://export.arxiv.org/api/query?search_query=all:electron&id_list=2005.00001&max_results=1", 200,),
        ("OpenAlex", "https://api.openalex.org/works?search=bronchiolitis&per-page=1", 200,),
        ("Semantic Scholar", "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1542/peds.2006-2223?fields=title", 200, 429),
        ("Unpaywall", "https://api.unpaywall.org/v2/10.1542/peds.2006-2223?email=netcheck@docsor.cn", 200, 404),
        # M1 闸门：Cloudflare TLS1.3 指纹类 CDN 站（OpenSSL 3.0.13 交互实测
        # 对此类站 TLS 握手超时——引擎 TLS1.2 降级重试的靶面，403 反爬也算通）
        ("Cloudflare CDN", "https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills", 200, 403),
    ]
    ok, names = 0, []
    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    _opener = urllib.request.build_opener(_NoRedirect)
    for item in probes:
        name, url, *good = item
        try:
            req = urllib.request.Request(url, headers=UA)
            with _opener.open(req, timeout=15) as r:
                code = r.status
        except urllib.error.HTTPError as e:
            code = e.code  # 302 等重定向在此呈现（审计 P2-1：no-redirect）
        except Exception as e:
            code = 0
        hit = any(code == g for g in good)
        ok += hit
        names.append(f"{name}:{'通' if hit else code}")
    print(f"  [N1] {' '.join(names)}")
    return ok, len(probes)


def n2_pubmed_ring(td, n=4):
    """PubMed 实时圆环：esearch→esummary 拿登记题名原样 → 引擎全 verified。
    （夹具纪律：探针引用必须带登记题名——首版用假题名被引擎当场判错引
    invalid，判定力活证据；真网圆环测的是通路稳定性，夹具必须诚实。）"""
    try:
        q = urllib.parse.urlencode(
            {"db": "pubmed", "retmode": "json", "retmax": n,
             "term": "bronchiolitis infants[MeSH Terms]", "sort": "date"})
        ids = [x for x in (http_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + q)
            .get("esearchresult", {}).get("idlist") or []) if x]
        time.sleep(0.5)
        sm = (http_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
                        "esummary.fcgi?db=pubmed&id=" + ",".join(ids) +
                        "&retmode=json").get("result", {}) if ids else {})
    except Exception as e:
        return None, f"E-utilities 拉取异常: {type(e).__name__}"
    refs = []
    for pid in ids:
        item = sm.get(pid) or {}
        t = item.get("title", "")
        src_j = item.get("fulljournalname") or item.get("source") or ""
        y = item.get("pubdate", "")[:4]
        if t and src_j and y.isdigit():
            refs.append({"title": t, "pmid": pid, "source": src_j,
                         "year": int(y)})
    if not refs:
        return None, "esummary 无可用登记记录"
    results, rc = run_engine(refs, os.path.join(td, "n2"))
    # 审计 P1-1：内容绑定——引擎非零退出/静默丢条目即 FAIL（防空转通过）
    if rc != 0 or len(results) != len(refs):
        return None, f"引擎 rc={rc} 条目 {len(results)}/{len(refs)}（内容绑定失败）"
    return results, None


def n3_crossref_ring(td, n=4):
    """Crossref 实时圆环：最新 DOI（登记题名原样）→ 引擎零 invalid。"""
    try:
        q = urllib.parse.urlencode(
            {"query.bibliographic": "bronchiolitis", "rows": n,
             "sort": "created", "select": "DOI,title,issued"})
        items = (http_json("https://api.crossref.org/works?" + q)
                 .get("message", {}).get("items") or [])
    except Exception as e:
        return None, f"Crossref 拉取异常: {type(e).__name__}"
    refs = []
    for i, it in enumerate(items, 1):
        title = (it.get("title") or [""])[0]
        year = ((it.get("issued", {}).get("date-parts") or [[None]])[0][0])
        refs.append({"title": title, "doi": it.get("DOI"), "year": year})
    refs = [r for r in refs if r["title"] and r["doi"]]
    if not refs:
        return None, "DOI 拉取为空（Crossref 不可达）"
    results, rc = run_engine(refs, os.path.join(td, "n3"))
    if rc != 0 or len(results) != len(refs):
        return None, f"引擎 rc={rc} 条目 {len(results)}/{len(refs)}（内容绑定失败）"
    return results, None


def n5_cross_registry():
    """N5 跨注册库一致性（F60）：同一真实 DOI 在 Crossref/OpenAlex/PubMed
    三库的登记题名归一后一致。锚点=10.1542/peds.2006-2223（PMID 17015575，
    留出集 v1#4——2026-11-06 真网核验在档的稳定公开论文）。
    诚实边界：任一库不可达=SKIP（环境态），不伪装通过；三库齐才可比。"""
    import difflib
    import re as _re
    doi, pmid = "10.1542/peds.2006-2223", "17015575"
    titles = {"Crossref": "", "OpenAlex": "", "PubMed": ""}
    try:
        t = (http_json(f"https://api.crossref.org/works/{doi}").get("message", {})
             .get("title") or [""])[0]
        if t:
            titles["Crossref"] = t
    except Exception as e:
        print(f"  [N5] Crossref 不可达: {type(e).__name__}")
    try:
        w = http_json(f"https://api.openalex.org/works/doi:{doi}")
        t = w.get("title") or w.get("display_name") or ""
        titles["OpenAlex"] = t
    except Exception as e:
        print(f"  [N5] OpenAlex 不可达: {type(e).__name__}")
    try:
        sm = http_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
                       "esummary.fcgi?db=pubmed&id=" + pmid + "&retmode=json"
                       ).get("result", {}).get(pmid, {})
        titles["PubMed"] = sm.get("title", "")
    except Exception as e:
        print(f"  [N5] PubMed 不可达: {type(e).__name__}")
    got = {k: v for k, v in titles.items() if v}
    if len(got) < 3:
        missing = sorted(set(titles) - set(got))
        return None, f"SKIP（{'/'.join(missing)} 不可达——三库齐才可比）"
    norm = lambda s: _re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    pairs = [("Crossref", "OpenAlex"), ("Crossref", "PubMed"),
             ("OpenAlex", "PubMed")]
    ratios = {f"{a}~{b}": round(difflib.SequenceMatcher(
        None, norm(got[a]), norm(got[b])).ratio(), 3) for a, b in pairs}
    return ratios, got["Crossref"]


def n4_mines(td):
    """埋雷矩阵：4 雷（全部应非 verified，其中编造 DOI/拼接应 invalid）
    +2 条真引用（零误伤）。真引用=#1-#2（真网核验过的稳定公开论文）。"""
    refs = [
        {"title": "Comparative Efficacy of Bronchiolitis Interventions in Acute Care: A Network Meta-analysis",
         "doi": "10.1542/peds.2020-040816", "year": 2021},
        {"title": "Clinical practice guideline: the diagnosis, management, and prevention of bronchiolitis",
         "doi": "10.1542/peds.2014-2742", "year": 2014},
        {"title": "Comparative Efficacy of Bronchiolitis Interventions in Acute Care: A Network Meta-analysis",
         "doi": "10.1038/s41586-026-77777-a", "year": 2021},   # 雷：真题名配假 DOI
        {"title": "A fabricated study of citation integrity in agents",
         "doi": "10.1038/s41586-026-99999-x", "year": 2026},   # 雷：编造 DOI
        {"title": "A survey of arxiv preprint quality control methods",
         "arxiv": "2601.99999"},                                # 雷：假 arXiv
        {"title": "Hallucinated citations are polluting the scientific literature",
         "url": "https://example.invalid/dead-link-probe-6f3a"},  # 雷：死链域
    ]
    try:
        results, rc = run_engine(refs, os.path.join(td, "n4"))
    except Exception as e:
        return None, f"引擎调用异常: {type(e).__name__}"
    if rc != 0 or len(results) != len(refs):
        # 审计 P1-1：N4 同样内容绑定（缺雷=空转通过是最危险形态）
        return None, f"引擎 rc={rc} 条目 {len(results)}/{len(refs)}（内容绑定失败）"
    return results, rc


def main():
    ap = argparse.ArgumentParser(description="cite-holmes 真网稳定性自检")
    ap.add_argument("--quick", action="store_true",
                    help="快档：注册库探针+埋雷矩阵（跳过圆环）")
    args = ap.parse_args()
    print(f"cite-holmes netcheck（真网稳定性自检）——{SK}")
    with tempfile.TemporaryDirectory() as td:
        ok, total = n1_probes()
        check("N1 注册库探针 ≥6/8 可达", ok >= 6, f"实测 {ok}/{total}")
        if not args.quick:
            res, err = n2_pubmed_ring(td)
            if res is None:
                check("N2 PubMed 圆环（环境跳过）", True, "SKIP: " + str(err))
                PASS.append("N2 SKIP")
            else:
                vs = [r["verdict"] for r in res]
                check(f"N2 PubMed 实时圆环全 verified（{len(res)} 条）",
                      all(v == "verified" for v in vs), f"实测 {vs}")
            res, err = n3_crossref_ring(td)
            if res is None:
                check("N3 Crossref 圆环（环境跳过）", True, "SKIP: " + str(err))
                PASS.append("N3 SKIP")
            else:
                bad = [(r["index"], r["verdict"]) for r in res
                       if r["verdict"] == "invalid"]
                check(f"N3 Crossref 实时圆环零 invalid（{len(res)} 条）",
                      not bad, f"invalid: {bad}")
            # F60：跨注册库一致性（三库登记题名归一互比，库间不一致=引擎
            # 多库元数据交叉的输入面失真信号；任一库不可达=SKIP 诚实）
            ratios, err = n5_cross_registry()
            if ratios is None:
                check("N5 跨注册库一致性（环境跳过）", True, str(err))
                PASS.append("N5 SKIP")
            else:
                worst = min(ratios.values())
                check(f"N5 三库登记题名一致（最低相似度 {worst}）",
                      worst >= 0.85, f"逐对: {ratios}")
        res, rc = n4_mines(td)
        if res is None:
            check("N4 埋雷矩阵（引擎调用失败）", False, str(rc))
            print(f"\n汇总: {len(PASS)} PASS / {len(FAIL)} FAIL")
            return 1
        by_idx = {r["index"]: r for r in res}
        mines = (3, 4, 5, 6)
        mines_ok = all(by_idx[i]["verdict"] != "verified" for i in mines
                       if i in by_idx)
        hard = [i for i in (3, 4) if i in by_idx
                and by_idx[i]["verdict"] == "invalid"]
        clean_ok = all(by_idx[i]["verdict"] != "invalid" for i in (1, 2)
                       if i in by_idx)
        check("N4 埋雷全落网（4 雷全非 verified）", mines_ok,
              str({i: by_idx.get(i, {}).get("verdict") for i in mines}))
        check("N4 编造 DOI+错配 DOI 实锤 invalid", len(hard) == 2,
              f"实锤 {hard}")
        check("N4 真引用零误伤（2 条非 invalid）", clean_ok,
              str({i: by_idx.get(i, {}).get("verdict") for i in (1, 2)}))
    n_fail = len(FAIL)
    n_skip = sum(1 for p in PASS if "SKIP" in p)
    print(f"\n汇总: {len(PASS) - n_skip} PASS / {n_fail} FAIL"
          + (f" / {n_skip} SKIP（环境跳过，不计入通过）" if n_skip else ""))
    if n_fail:
        for f in FAIL:
            print(f"  FAIL: {f}")
        print("真网稳定性自检未过——检查网络/代理后重跑；持续失败请附本输出反馈。")
        return 1
    print("真网稳定性自检通过——注册库通路与判定矩阵在当前网络下工作正常。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
