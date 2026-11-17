#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_cn_refs v1.0 — 中文文献引用五态验证器（cn-med-oa 的验证层）。

验证哲学与判定语义移植 pubmed-verifier v2.1.5（同一作者生态，agent 零学习成本）；
模糊匹配使用 cn_med_oa.zh_similarity（中文 bigram 自适应改造版）。

五态判定：
  ✅ correct      id/标题真实存在，且元数据交叉匹配
  ⚠️ mismatch     文献存在，但指向不同的论文（下错/引用错——AI幻觉最常见形态）
  🔶 partial      部分匹配（如 作者+期刊 对但标题不同）
  ❌ invalid      维普平台查无此文献（编造的 id/标题）
  ❓ unconfirmed  缺少足够元数据交叉比对 / 卷期页存在缺口(--strict 时降级)

验证链：
  1. id 回查维普详情（或按标题检索解析 id）
  2. 标题双重模糊匹配（claimed vs actual，词级Jaccard≥0.5 或 字级≥0.90）
  3. 作者姓氏/期刊名/年份交叉比对
  4. PDF 内容验证（可选）：首页标题窗口匹配 + 卷期三方一致性(API vs PDF vs DOI正则)
  5. 输出 report.html / report.json

用法：
  python verify_cn_refs.py --manifest cn_refs.json --output report.html
  python verify_cn_refs.py --claims '[{"id":"7203426125","title":"...","journal":"浙江医学","year":"2026"}]'
  python verify_cn_refs.py --manifest cn_refs.json --strict   # 卷期页缺口也算不通过
"""
import os, sys, json, re, argparse, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cn_med_oa import (weipu_detail, weipu_search, zh_similarity, zh_title_match,
                       zh_clean, extract_vol_issue, pdf_first_pages_text, SKILL_VER)

VER = "1.0.0"
VERDICT_ZH = {"correct": "✅ 正确", "mismatch": "⚠️ 不匹配", "partial": "🔶 部分匹配",
              "invalid": "❌ 无效", "unconfirmed": "❓ 待确认"}


# ── PDF 标题窗口匹配（PDF 标题常被换行/空格切断，做滑窗最大相似度）──
def pdf_title_ratio(title, pdf_text):
    t = zh_clean(title).replace(" ", "")
    if not t:
        return 0.0
    txt = zh_clean(pdf_text).replace(" ", "")
    n = len(t)
    win = int(n * 1.3) + 8
    step = max(1, n // 4)
    best = 0.0
    for i in range(0, max(1, len(txt) - n + 1), step):
        r = _seq_ratio(t, txt[i:i + win])
        if r > best:
            best = r
        if best >= 0.96:
            break
    return round(best, 3)


def _seq_ratio(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()


# ── 作者匹配（中文姓名 2-4 字，用包含式比对）──
def _author_match(claimed, actual):
    if not claimed or not actual:
        return False
    hits = 0
    for c in claimed:
        c = zh_clean(c).replace(" ", "")
        if not c:
            continue
        for a in actual:
            a = zh_clean(str(a)).replace(" ", "")
            if not a:
                continue
            # 姓或全名包含（处理"陈勇" vs "陈勇" / "郑凤钰" vs "郑凤钰" / 缩写）
            if c in a or a in c:
                hits += 1
                break
    return hits >= (2 if len(claimed) >= 2 else 1)


# ── 期刊匹配（包含式 + 词重叠）──
def _journal_match(cj, aj):
    if not cj or not aj:
        return False
    cj, aj = zh_clean(cj), zh_clean(aj)
    if cj in aj or aj in cj:
        return True
    tc, ta = set(cj.split()), set(aj.split())
    if tc and ta:
        return len(tc & ta) / min(len(tc), len(ta)) >= 0.5
    return False


# ── 五态判定核心（判定规则镜像 pubmed-verifier cross_check_citation）──
def cross_check_cn(claimed, actual):
    """claimed: manifest/claims 条目; actual: 维普详情 dict。返回判定结果。"""
    r = {"verdict": "unconfirmed", "title_match": False, "author_match": False,
         "journal_match": False, "year_match": False, "confidence": 0.0,
         "title_word": 0.0, "title_seq": 0.0, "details": "", "gaps": []}
    checks = 0
    # 标题
    if claimed.get("title") and actual.get("title"):
        m, w, s = zh_title_match(claimed["title"], actual["title"])
        r["title_match"], r["title_word"], r["title_seq"] = m, w, s
        checks += 1
    # 作者
    ca = claimed.get("authors") or ([claimed["first_author"]] if claimed.get("first_author") else [])
    aa = [x.get("name", "") for x in (actual.get("authorInfo") or [])]
    if ca and aa:
        r["author_match"] = _author_match(ca, aa)
        checks += 1
    # 期刊
    aj = ((actual.get("objectInfo") or {}).get("name") or "")
    if claimed.get("journal") and aj:
        r["journal_match"] = _journal_match(claimed["journal"], aj)
        checks += 1
    # 年份
    if claimed.get("year") and actual.get("year"):
        r["year_match"] = str(claimed["year"]) == str(actual["year"])
        checks += 1

    r["confidence"] = round(sum([r["title_match"], r["author_match"], r["journal_match"],
                                 r["year_match"]]) / max(checks, 1), 2)

    if not claimed.get("title") and not ca:
        r["details"] = "声称元数据不足（无标题且无作者），无法交叉比对"
        return r
    parts = []
    if r["title_match"] and (r["author_match"] or r["journal_match"]):
        r["verdict"] = "correct"
        if not r["author_match"]:
            parts.append("作者略有出入")
        if not r["journal_match"]:
            parts.append("期刊名变体")
    elif r["author_match"] and r["journal_match"] and not r["title_match"]:
        r["verdict"] = "partial"
        parts.append("作者+期刊匹配但标题不同")
    elif r["title_match"] and not r["author_match"] and not r["journal_match"]:
        r["verdict"] = "partial"
        parts.append("标题匹配但作者/期刊不符")
    else:
        r["verdict"] = "mismatch"
        if not r["title_match"]:
            parts.append("标题不符")
        if not r["author_match"]:
            parts.append("作者不符")
        if not r["journal_match"]:
            parts.append("期刊不符")
        if not r["year_match"]:
            parts.append("年份不符")
    r["details"] = "; ".join(parts) if parts else "元数据全部匹配"
    return r


# ── 卷期页缺口检查 ──
def check_gaps(entry, actual, pdf_text=""):
    gaps = []
    vi = extract_vol_issue(actual, pdf_text)
    if not vi["volume"]:
        gaps.append("卷号缺失")
    if not vi["issue"]:
        gaps.append("期号缺失")
    if vi["vol_source"] == "doi_guess":
        gaps.append("卷期来自DOI猜测(需人工核对)")
    if not vi["vol_consistent"]:
        gaps.append("API与PDF卷期不一致")
    if not entry.get("pages"):
        gaps.append("页码缺失")
    return gaps, vi


# ── 单条验证 ──
def _yiigle_actual_by_title(title):
    """yiigle 按标题检索，命中则构造与维普详情同构的 actual dict（双源验证回退）。

    返回 actual dict 或 None。中华医学会系期刊维普不收录，靠此回退覆盖。
    """
    try:
        from cn_med_oa import yiigle_search
    except ImportError:
        return None
    rows, _err = yiigle_search(title, field="title", size=5)
    for rw in rows:
        m, _, _ = zh_title_match(title, rw.get("title") or "")
        if m:
            return {"id": str(rw.get("id") or ""),
                    "title": rw.get("title") or "",
                    "objectInfo": {"name": rw.get("journal") or ""},
                    "year": str(rw.get("year") or ""),
                    "doi": rw.get("artDoi") or "",
                    "authorInfo": [{"name": n} for n in (rw.get("authors") or [])][:8],
                    "_source": "Yiigle"}
    return None


def verify_entry(entry, check_pdf=True):
    out = {"input": {k: entry.get(k) for k in
                     ("id", "title", "authors", "journal", "year", "doi", "path",
                      "volume", "issue", "pages")},
           "resolved_via": "id", "actual": {}, "pdf": {}, "gaps": []}
    pid = str(entry.get("id") or entry.get("lngid") or "")
    actual = None
    if pid:
        actual = weipu_detail(pid)
    if actual is None and entry.get("title"):
        # 无 id 或 id 查无 → 按标题检索解析。
        # 期刊感知优先级：期刊匹配的维普行 > yiigle（中华系期刊维普不收录）> 任意标题匹配维普行。
        # 防止维普捞回同名解读文章顶掉声称期刊的真文（如《XX指南》vs《〈XX指南〉解读》）。
        rows, _ = weipu_search(entry["title"], field="title", size=5)
        cj = entry.get("journal") or ""

        def _row_journal(rw):
            return ((rw.get("objectInfo") or {}).get("name") or rw.get("journal") or "")

        def _title_ok(rw):
            m, _, _ = zh_title_match(entry["title"], rw.get("name") or rw.get("title") or "")
            return m

        rw = None
        if cj:
            rw = next((x for x in rows if _journal_match(cj, _row_journal(x)) and _title_ok(x)), None)
        if rw is None:
            y_actual = _yiigle_actual_by_title(entry["title"])
            if y_actual is not None and (not cj or _journal_match(cj, y_actual["objectInfo"]["name"])):
                actual = y_actual
                out["resolved_via"] = "yiigle_title_search"
        if actual is None:
            rw = rw or next((x for x in rows if _title_ok(x)), None)
            if rw is not None:
                pid = str(rw.get("id") or "")
                actual = weipu_detail(pid)
                out["resolved_via"] = "title_search"
    if actual is None and entry.get("title"):
        # 双源回退：维普未命中（中华医学会系期刊维普不收录）→ yiigle 按标题回查
        actual = _yiigle_actual_by_title(entry["title"])
        if actual is not None:
            out["resolved_via"] = "yiigle_title_search"
    if actual is None:
        out["verdict"] = "invalid"
        out["reason"] = "维普OA与yiigle均查无此文献（id 与标题检索未命中）"
        return out

    out["actual"] = {"id": str(actual.get("id") or pid),
                     "title": actual.get("title") or "",
                     "journal": ((actual.get("objectInfo") or {}).get("name") or ""),
                     "year": str(actual.get("year") or ""),
                     "doi": actual.get("doi") or "",
                     "authors": [x.get("name", "") for x in (actual.get("authorInfo") or [])][:8]}

    cc = cross_check_cn(entry, actual)
    out.update(cc)

    # PDF 内容验证（有文件且可解析时）
    if check_pdf and entry.get("path") and os.path.exists(entry["path"]):
        ptxt = pdf_first_pages_text(entry["path"], n=2)
        if ptxt:
            ratio = pdf_title_ratio(entry.get("title") or "", ptxt)
            vi_pdf = extract_vol_issue(actual, ptxt)
            out["pdf"] = {"title_ratio": ratio,
                          "title_match": ratio >= 0.70,
                          "vol_consistent": vi_pdf["vol_consistent"]}
            if not out["pdf"]["title_match"]:
                if out.get("verdict") in ("correct", "partial"):
                    out["verdict"] = "mismatch"
                out["details"] = (out.get("details", "") + "; PDF首页标题不匹配(%.2f)" % ratio).strip("; ")
            if not vi_pdf["vol_consistent"]:
                out["gaps"].append("API与PDF卷期不一致")

    gaps, vi = check_gaps(entry, actual, pdf_first_pages_text(entry["path"]) if
                          (entry.get("path") and os.path.exists(entry.get("path", ""))) else "")
    for g in gaps:
        if g not in out["gaps"]:
            out["gaps"].append(g)
    out["vol_issue"] = {k: vi[k] for k in ("volume", "issue", "vol_source", "vol_consistent")}
    return out


# ── 报告 ──
_HTML_HEAD = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>中文文献引用验证报告</title><style>
body{font-family:"Microsoft YaHei",sans-serif;max-width:1100px;margin:24px auto;color:#222}
h1{font-size:20px} .sum{display:flex;gap:12px;margin:16px 0;flex-wrap:wrap}
.b{padding:10px 18px;border-radius:8px;font-size:14px}
table{border-collapse:collapse;width:100%;font-size:13px}
td,th{border:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}
th{background:#f5f6f8}.c1{background:#e6f7e9}.c2{background:#fdecea}.c3{background:#fff6e0}
.c4{background:#eee}.c5{background:#f0f0f0}
</style></head><body>"""
_HTML_FOOT = """<p style="color:#888;font-size:12px">验证链(双源): 维普详情回查 → (未命中时 yiigle 按标题回查，覆盖中华医学会系期刊) → 标题双重模糊匹配(词级Jaccard/字级Sequence) → 作者/期刊/年份交叉 → PDF首页窗口匹配+卷期三方一致性。判定语义与 pubmed-verifier 一致。</p>
</body></html>"""


def gen_html(results, src):
    n = {k: sum(1 for r in results if r.get("verdict") == k)
         for k in ("correct", "mismatch", "partial", "invalid", "unconfirmed")}
    total = len(results)
    rows_html = []
    for r in results:
        v = r.get("verdict", "unconfirmed")
        i = r.get("input", {})
        a = r.get("actual", {})
        gaps = "；".join(r.get("gaps", [])) or "-"
        pdf = r.get("pdf", {})
        pdfs = ("标题匹配%.2f" % pdf["title_ratio"]) if pdf else "未验证"
        rows_html.append(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                VERDICT_ZH.get(v, v), (i.get("title") or "")[:44],
                (a.get("title") or "")[:44], "%.2f" % r.get("confidence", 0),
                "、".join((i.get("authors") or [])[:3]) or "-", pdfs, gaps))
    cls = {"correct": "c1", "mismatch": "c2", "partial": "c3", "invalid": "c4", "unconfirmed": "c5"}
    cards = "".join('<div class="b %s">%s %d</div>' % (cls[k], VERDICT_ZH[k], n[k])
                    for k in ("correct", "mismatch", "partial", "invalid", "unconfirmed"))
    return (_HTML_HEAD +
            "<h1>中文文献引用验证报告 <small style='color:#888'>verify_cn_refs v" + VER +
            " · 来源: " + str(src) + "</small></h1>" +
            '<div class="sum">' + cards + '<div class="b">合计 ' + str(total) + "</div></div>" +
            "<table><tr><th>判定</th><th>声称标题</th><th>实际标题(维普)</th><th>置信度</th><th>声称作者</th><th>PDF</th><th>缺口</th></tr>" +
            "\n".join(rows_html) + "</table>" +
            _HTML_FOOT)


def main():
    ap = argparse.ArgumentParser(description="中文文献引用五态验证器 v" + VER)
    ap.add_argument("--manifest", default=None, help="cn_med_oa 生成的 cn_refs.json")
    ap.add_argument("--claims", default=None, help="JSON 数组/单条引用(可无id,按标题解析)")
    ap.add_argument("--claims-file", default=None, help="JSON 文件形式的上述数组")
    ap.add_argument("--no-pdf", action="store_true", help="跳过 PDF 内容验证")
    ap.add_argument("--strict", action="store_true", help="卷期页缺口也判为待确认")
    ap.add_argument("--output", default=None, help="报告输出路径(.html/.json)")
    args = ap.parse_args()

    entries, src = [], ""
    if args.manifest:
        data = json.load(open(args.manifest, encoding="utf-8"))
        entries = data.get("files", data if isinstance(data, list) else [])
        src = args.manifest
    elif args.claims or args.claims_file:
        raw = args.claims if args.claims else open(args.claims_file, encoding="utf-8").read()
        data = json.loads(raw)
        entries = data if isinstance(data, list) else [data]
        src = args.claims_file or "--claims"
    else:
        ap.print_help()
        sys.exit(2)
    if not entries:
        print("无待验证条目")
        sys.exit(0)

    results = []
    for e in entries:
        r = verify_entry(e, check_pdf=not args.no_pdf)
        if args.strict and r.get("verdict") == "correct" and r.get("gaps"):
            r["verdict"] = "unconfirmed"
            r["details"] = (r.get("details", "") + "; strict模式:卷期页缺口").strip("; ")
        results.append(r)
        v = r.get("verdict", "unconfirmed")
        print("%s [%s] %s" % (VERDICT_ZH.get(v, v), r.get("resolved_via", "?"),
                              (r.get("input", {}).get("title") or "")[:46]))
        if v not in ("correct",):
            print("      -> %s %s" % (r.get("reason", ""), r.get("details", "")))
        if r.get("gaps"):
            print("      缺口: %s" % "；".join(r["gaps"]))

    n_bad = sum(1 for r in results if r.get("verdict") in ("mismatch", "invalid"))
    n_unc = sum(1 for r in results if r.get("verdict") == "unconfirmed")
    print("\n汇总: %d 条 | ✅%d ⚠️%d 🔶%d ❌%d ❓%d" % (
        len(results),
        sum(1 for r in results if r.get("verdict") == "correct"), n_bad and 0 or
        sum(1 for r in results if r.get("verdict") == "mismatch"),
        sum(1 for r in results if r.get("verdict") == "partial"),
        sum(1 for r in results if r.get("verdict") == "invalid"), n_unc))

    if args.output:
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".json":
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump({"ver": VER, "source": src, "results": results}, f, ensure_ascii=False, indent=2)
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(gen_html(results, src))
        print("报告已写入: %s" % args.output)
    sys.exit(1 if (n_bad or (args.strict and n_unc)) else 0)


if __name__ == "__main__":
    main()
