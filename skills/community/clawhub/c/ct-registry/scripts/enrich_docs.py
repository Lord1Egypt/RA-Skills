#!/usr/bin/env python3
"""enrich_docs.py - 通用试验文档链接富集入口 / Unified trial-document link enricher.

Why (ct-registry 2026-07-30, v0.3.13)
-------------------------------------
`download_docs.py` 只消费记录里**已存在**的 `documents` 字段；但 `normalize.py` 输出的
WHO / CT.gov / CDE 等记录默认 `documents=[]` —— 这些源**不提供方案 PDF 的公开 API**
（download_docs.py 注释已说明：CT.gov / WHO generally expose no protocol-PDF API；
CDE 受 SafeDog WAF 限制，workflow 详情返回 0 个附件 URL）。

唯一能稳定自动拿到可下载文档链接的是 **EU-CTR**：EU CTIS 公开检索 API 暴露带签名的
文档 URL（protocol / IB / CSR synopsis 等）。本脚本作为统一富集入口：

  * 读 normalized 产物（支持顶层 list 或 dict 包裹 records）；
  * 按 `url` host 分流；EU-CTR 来源复用 `fetch_eu_ctr_docs.fetch_docs` 填充 documents；
  * CT.gov / ChiCTR / JPRN / CTRI / ISRCTN / DRKS 等无公开 PDF API 的源，documents 留空，
    但**保留 `url`** 供人工跳转源平台手动下载；
  * `--run` 才真正向 CTIS API 发请求；默认 PREVIEW 仅统计源 host 分布与可抓取数。

重要（避免误判）：WHO ICTRP 镜像的 CT.gov / ChiCTR / JPRN / CTRI 等记录即便 enrich 后
documents 仍为空 —— 这是**数据源限制，不是 bug**。只有 EU-CTR 来源会产生自动文档链接。
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_eu_ctr_docs import fetch_docs as eu_fetch_docs  # noqa: E402

EU_HOST = "euclinicaltrials.eu"


def _load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data, None
    if isinstance(data, dict):
        return data.get("records") or data.get("records_all") or [], data
    return [], None


def _ct_number(rec):
    url = rec.get("url") or ""
    if EU_HOST in url:
        m = re.search(r"retrieve/([^/?#]+)", url)
        if m:
            return m.group(1)
    return rec.get("ctNumber") or rec.get("ct_number")


def enrich_record(rec, do_fetch):
    url = rec.get("url") or ""
    docs = []
    if EU_HOST in url:
        ct = _ct_number(rec)
        if ct and do_fetch:
            docs, err = eu_fetch_docs(ct)
            if err:
                print("  [enrich] %s EU-CTR: %s" % (rec.get("registry_id"), err))
        # preview (do_fetch=False): leave empty, no network
    # 其余源（CT.gov/ChiCTR/JPRN/CTRI/ISRCTN/DRKS）无公开 PDF API -> 留空
    rec["documents"] = docs
    return rec


def main():
    ap = argparse.ArgumentParser(
        description="通用试验文档链接富集（EU-CTR 自动抓；其余源保留 url 手动下）。")
    ap.add_argument("--in", dest="inp", required=True, help="normalized.json (list 或 dict)")
    ap.add_argument("--out", default=None, help="输出文件（默认 <in>_enriched.json；仅 --run 时写）")
    ap.add_argument("--run", action="store_true",
                    help="真正向 CTIS API 抓取 EU-CTR 文档（默认仅预览统计，不写文件、不发请求）")
    args = ap.parse_args()

    recs, wrapper = _load(args.inp)
    host_counter = Counter()
    for r in recs:
        u = r.get("url") or ""
        m = re.match(r"https?://([^/]+)/?", u)
        host_counter[m.group(1) if m else "(none)"] += 1

    print("[enrich_docs] 读入 %d 条记录" % len(recs))
    print("[enrich_docs] 源 host 分布:")
    for h, c in host_counter.most_common():
        tag = "  <- EU-CTR：可自动抓文档" if EU_HOST in h else ""
        print("    %s: %d%s" % (h, c, tag))

    if not args.run:
        print("[enrich_docs][PREVIEW] 默认仅统计，不抓取、不写文件。"
              "加 --run 才向 CTIS 发请求（仅 EU-CTR 来源）。")
        return

    for r in recs:
        enrich_record(r, do_fetch=True)

    total = sum(len(r.get("documents") or []) for r in recs)
    print("[enrich_docs] 富集后文档链接总数: %d" % total)

    out = args.out or (os.path.splitext(args.inp)[0] + "_enriched.json")
    payload = wrapper if wrapper is not None else recs
    if wrapper is not None:
        wrapper["records"] = recs
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("[enrich_docs] 写出 -> %s" % out)


if __name__ == "__main__":
    main()
