#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crossref 元数据取数脚本 —— GB/T 7714 参考文献真实性核验用

职责单一：只负责从 Crossref 取回权威元数据，不做任何真伪判定。
判定与比对由检查流程完成（见 SKILL.md 的 Phase 3）。

依赖：仅 Python 标准库，无需 pip 安装。

用法
----
# 1) 按 DOI 直查（输入每行一个 DOI，可带 https://doi.org/ 前缀）
python crossref_verify.py --file dois.txt --output result.json

# 2) 输入带序号（序号<TAB>DOI 或 序号|DOI），结果会带上序号便于回填
python crossref_verify.py --file dois.txt --output result.json

# 3) 按引文文本匹配（无 DOI 的英文文献尝试找回 DOI）
python crossref_verify.py --text --file refs.txt --output result.json

# 4) 直接从管道读入
echo "10.1038/s41586-021-03819-2" | python crossref_verify.py

# 5) 证书链有问题的内网环境可加 --insecure（不建议作为默认）
python crossref_verify.py --file dois.txt --insecure

输出
----
JSON 数组，每项含 status / doi / title / authors / container / year /
volume / issue / page / type / score / title_in_input / candidates /
url_crossref / update_flags / error

text 模式下，脚本会同时用 query.bibliographic 与 query.title 检索并合并
候选，每项标注 matched_field 以示来源。candidates 保存其余候选记录
（已按"题名落位优先、分数次之"排序）。同一题名在 Crossref 常有多条
记录（原刊版 / 论文集收录版 / 预印本 / 重印版），判定时必须比对
年卷期页，不能只看第一条。

status 取值：
  ok        取到记录（DOI 模式即该 DOI 有效；text 模式即匹配到候选）
  not_found DOI 无法解析（强信号，需人工复核，但不得直接断言文献不存在）
  no_match  text 模式下未匹配到任何候选
  error     网络或解析异常
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.crossref.org/works"
PLACEHOLDER_MAILTO = "reference-checker@example.com"
# Retrieval queries travel in the URL; keep them well under the server/proxy
# limit so an over-long citation cannot turn into an opaque HTTP 414.
MAX_QUERY_CHARS = 1500


def norm_doi(raw: str):
    """从任意文本中提取并规范化 DOI。"""
    if not raw:
        return None
    m = re.search(r"(10\.\d{4,9}/[^\s]+)", raw, re.I)
    if not m:
        return None
    return m.group(1).lower().rstrip(".,;:)]}\u3002\uff0c\uff1b\uff1a")


def split_index(line: str):
    """拆出可选的序号前缀。支持 1<TAB>... / [1] ... / 1|... / 1. ..."""
    m = re.match(r"^\s*(?:\[?(\d{1,4})\]?)\s*[\t|]\s*(.+)$", line)
    if m:
        return m.group(1), m.group(2).strip()
    m = re.match(r"^\s*\[(\d{1,4})\]\s+(.+)$", line)
    if m:
        return m.group(1), m.group(2).strip()
    return "", line.strip()


def fmt_authors(items):
    """Crossref author 列表 -> ['Jumper J', 'Evans R', ...]（姓 名首字母）"""
    out = []
    for a in items or []:
        fam = (a.get("family") or "").strip()
        giv = (a.get("given") or "").strip()
        if fam:
            initials = "".join(p[0].upper() for p in re.split(r"[\s.\-]+", giv) if p)
            out.append((fam + " " + initials).strip())
        elif a.get("name"):
            out.append(a["name"].strip())
    return out


def strip_markup(s):
    """
    清理 Crossref 题名／容器名中的内联排版标记与 HTML 实体。

    Crossref 的题名常带期刊排版标记（`<scp>ChatGPT</scp>`、`<i>…</i>`、
    `<jats:sub>` 等），容器名常带实体（`Communications Earth &amp; Environment`）。
    不清理有两个后果：

    1. **落位检测假阴性**——实测 Hydrological Processes 一条题名
       `<scp>AI</scp> tools such as <scp>ChatGPT</scp> will disrupt hydrology, too`
       因标签词占了词表较大比例，词覆盖率跌破阈值，被判 `title_in_input=false`，
       而它实为完全正确的匹配（DOI 10.1002/hyp.14843）。
    2. **报告被污染**——标签会原样进入报告，用户直接复制就把 `<scp>` 写进参考文献。
    """
    if not s:
        return ""
    s = re.sub(r"<[^>]{1,80}>", " ", s)
    for ent, ch in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                    ("&quot;", '"'), ("&apos;", "'"), ("&#39;", "'"),
                    ("&nbsp;", " ")):
        s = s.replace(ent, ch)
    return re.sub(r"\s+", " ", s).strip()


def norm_text(s):
    """归一化：先去排版标记，再转小写、去标点、压缩空白。中英文均适用。"""
    if not s:
        return ""
    s = strip_markup(s).lower()
    s = re.sub(r"[^\w\u4e00-\u9fff\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def title_in_input(title, raw):
    """
    检测 Crossref 返回的题名是否真的落在原始引文文本里。

    这是 text 模式的关键兜底：Crossref 的 score 只反映检索相关性，
    不反映语义正确性。实测中一条中文图书（《信息计量学》）返回的
    score（108.2）高于一条完全正确的英文文献匹配（69.0），但内容
    毫不相干——因为中文文献在 Crossref 中无对应记录时，检索会退化
    为词面匹配。

    著录规范的条目里题名必然出现，因此"题名是否落在原文中"是比
    score 可靠得多的信号。返回 True / False。
    """
    t = norm_text(title)
    r = norm_text(raw)
    if not t or not r:
        return False
    if t in r:
        return True
    # 容忍分词与标点差异：按词做覆盖率判断（中文按字符滑窗）
    words = [w for w in t.split() if len(w) > 2]
    if words:
        hit = sum(1 for w in words if w in r)
        return hit / len(words) >= 0.8
    return False


def pick_year(msg):
    for key in ("published-print", "published-online", "issued", "published", "created"):
        v = msg.get(key)
        if isinstance(v, dict):
            parts = v.get("date-parts") or []
            if parts and parts[0] and parts[0][0]:
                return parts[0][0]
    return None


def update_flags(msg):
    """标记撤稿/更正等更新关系。"""
    flags = []
    for u in msg.get("update-to") or []:
        if isinstance(u, dict):
            flags.append({"relation": u.get("type", ""), "doi": u.get("DOI", "")})
    for u in msg.get("updated-by") or []:
        if isinstance(u, dict):
            flags.append({"relation": u.get("type", ""), "doi": u.get("DOI", "")})
    return flags


def pick_meta(msg, source, score=None):
    year = pick_year(msg)
    return {
        "status": "ok",
        "doi": (msg.get("DOI") or "").lower(),
        "title": strip_markup((msg.get("title") or [""])[0]),
        "authors": fmt_authors(msg.get("author")),
        "container": strip_markup((msg.get("container-title") or [""])[0]),
        "year": year,
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "page": msg.get("page", "") or msg.get("article-number", ""),
        "type": msg.get("type", ""),
        "publisher": msg.get("publisher", ""),
        "score": score,
        "url_crossref": "https://api.crossref.org/works/" + (msg.get("DOI") or ""),
        "update_flags": update_flags(msg),
        "source": source,
        "title_in_input": None,
        "matched_field": "",
        "error": "",
    }


def http_json(url, mailto, timeout, insecure):
    headers = {
        "User-Agent": "GB7714-ReferenceChecker/4.0.4 (mailto:%s)" % mailto,
        "Accept": "application/json",
    }
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def empty_result(raw, source):
    return {
        "status": "error", "doi": "", "title": "", "authors": [], "container": "",
        "year": None, "volume": "", "issue": "", "page": "", "type": "",
        "publisher": "", "score": None, "url_crossref": "",
        "update_flags": [], "source": source, "title_in_input": None,
        "matched_field": "", "candidates": [], "error": "",
    }


def query_doi(doi, mailto, timeout, insecure):
    url = API + "/" + urllib.parse.quote(doi, safe="")
    try:
        data = http_json(url, mailto, timeout, insecure)
        return pick_meta(data["message"], "doi")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            r = empty_result(doi, "doi")
            r["status"] = "not_found"
            r["doi"] = doi
            return r
        r = empty_result(doi, "doi")
        r["error"] = "HTTP %s" % e.code
        return r
    except Exception as e:  # noqa: BLE001
        r = empty_result(doi, "doi")
        r["error"] = "%s: %s" % (type(e).__name__, e)
        return r


def query_text(text, mailto, timeout, insecure, rows=5):
    """
    引文文本匹配。**同时**发起 query.bibliographic 与 query.title 两次检索并合并候选。

    为什么要两个字段：`query.bibliographic` 会把整串文本按书目字段混合匹配，
    对题名偏长、含冒号副题名、或字段顺序异常的条目会**漏检**。实测反例
    （2026-09-27）：Paolicelli 等的 "Microglia states and nomenclature: A field
    at its crossroads"（Neuron, 2022, 110(21): 3458-3483，真实存在）经
    query.bibliographic 检索，前 5 条候选全部题名落位为否（返回的是同刊
    同期的其他文章），照现行判定规则会被误报为"疑似不存在"；改用
    query.title 检索，该记录以 score 45.6 稳居首位。

    两个字段各有盲区，合并后取并集，再按"题名落位优先、分数次之"排序，
    可显著降低漏检。candidates 中标注 matched_field 便于追溯。
    """
    select = ("DOI,title,author,container-title,issued,published-print,"
              "published-online,volume,issue,page,article-number,type,publisher,score")

    cands = []
    seen = set()
    errors = []
    for field in ("query.bibliographic", "query.title"):
        params = urllib.parse.urlencode(
            {field: text[:MAX_QUERY_CHARS], "rows": rows, "select": select})
        try:
            data = http_json(API + "?" + params, mailto, timeout, insecure)
        except Exception as e:  # noqa: BLE001
            errors.append("%s: %s: %s" % (field, type(e).__name__, e))
            continue
        for it in (data.get("message") or {}).get("items") or []:
            doi = (it.get("DOI") or "").lower()
            if doi and doi in seen:
                continue
            if doi:
                seen.add(doi)
            c = pick_meta(it, "text", score=round(it.get("score") or 0, 1))
            c["title_in_input"] = title_in_input(c["title"], text)
            c["matched_field"] = field
            cands.append(c)

    if not cands:
        r = empty_result(text, "text")
        if errors:
            r["error"] = " | ".join(errors)
        else:
            r["status"] = "no_match"
        return r

    # 排序键：题名落在原文中的优先，其次按检索分数降序。
    # 同一题名在 Crossref 常有多条记录（原刊版 / 论文集收录版 / 重印版），
    # 实测中 LIGO 那篇的收录版记录反而分数更高，只按分数排序会挑中错误版本。
    cands.sort(key=lambda c: (not c["title_in_input"], -(c["score"] or 0)))

    best = dict(cands[0])
    best["candidates"] = cands[1:]
    return best


def read_lines(path):
    if path:
        with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
            return [ln for ln in f.read().splitlines() if ln.strip()]
    return [ln for ln in sys.stdin.read().splitlines() if ln.strip()]


def main():
    ap = argparse.ArgumentParser(description="Crossref metadata fetcher for GB/T 7714 verification")
    ap.add_argument("--file", help="input file, one entry per line")
    ap.add_argument("--output", help="write JSON to this path instead of stdout")
    ap.add_argument("--text", action="store_true", help="treat each line as a citation string")
    ap.add_argument("--mailto", default=PLACEHOLDER_MAILTO,
                    help="contact email for Crossref polite pool (replace with a real one)")
    ap.add_argument("--delay", type=float, default=0.25, help="seconds between requests")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--insecure", action="store_true", help="skip TLS verification")
    ap.add_argument("--force", action="store_true",
                    help="allow --output to overwrite an existing file")
    args = ap.parse_args()

    if args.insecure:
        sys.stderr.write(
            "WARNING: --insecure is on. TLS certificate verification is DISABLED; "
            "responses may be intercepted or tampered with. Use only for debugging.\n")

    lines = read_lines(args.file)
    if not lines:
        print("[]")
        return

    results = []
    if not args.text:
        for line in lines:
            idx, body = split_index(line)
            doi = norm_doi(body)
            if not doi:
                r = empty_result(body, "doi")
                r["error"] = "no DOI found in input"
                results.append({"index": idx, "input": body, **r})
                continue
            r = query_doi(doi, args.mailto, args.timeout, args.insecure)
            results.append({"index": idx, "input": body, **r})
            time.sleep(args.delay)
    else:
        for line in lines:
            idx, body = split_index(line)
            r = query_text(body, args.mailto, args.timeout, args.insecure)
            results.append({"index": idx, "input": body, **r})
            time.sleep(args.delay)

    payload = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output:
        # Guard against silently truncating an existing user file (e.g. a thesis
        # or a hand-written notes file passed by mistake).
        if os.path.exists(args.output) and not args.force:
            sys.stderr.write(
                "ERROR: %s already exists. Refusing to overwrite.\n"
                "       Re-run with --force if this is intended.\n" % args.output)
            sys.exit(2)
        parent = os.path.dirname(os.path.abspath(args.output))
        if parent and not os.path.isdir(parent):
            sys.stderr.write("ERROR: output directory does not exist: %s\n" % parent)
            sys.exit(2)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(payload)
        print("wrote %d records to %s" % (len(results), args.output))
    else:
        print(payload)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    main()
