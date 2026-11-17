#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TA 映射表在线抽验工具（v4.3.0 数据治理固化——上版审计 P3「TA 表未经在线验证」根治）。

对 verify_refs._CN_JOURNAL_TA 每条映射查 PubMed esearch（TA[TA]）：
- count>0  → 活映射（MEDLINE 有收录）
- count=0  → 目录登记但零收录（定位器永哑火）——从表中剔除或改 TA

用法：python3 tools/check_ta_table.py [--verbose]
退网环境跳过（exit 3=无法验证，非失败）。改动 _CN_JOURNAL_TA 后必跑本工具。"""
import json
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, __file__.rsplit("/", 2)[0] + "/scripts")
import verify_refs as vr  # noqa: E402


def main():
    verbose = "--verbose" in sys.argv
    ok, dead, err = [], [], []
    for cn, ta in vr._CN_JOURNAL_TA.items():
        term = f'"{ta}"[TA]'
        u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
             + f"?db=pubmed&retmode=json&retmax=1&term={urllib.parse.quote(term)}")
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    u, headers={"User-Agent": f"cite-holmes/{vr.VERSION}; ta-table-check"}),
                    timeout=12) as r:
                count = int((json.loads(r.read().decode()).get("esearchresult")
                             or {}).get("count") or 0)
        except Exception as e:
            err.append((cn, ta, str(e)))
            continue
        (ok if count > 0 else dead).append((cn, ta, count))
        vr._ncbi_rate_wait()
        if verbose:
            print(f"  {'✓' if count else '✗'} {cn} → {ta} ({count})")
    print(f"== TA 表抽验 == 活 {len(ok)} / 零收录 {len(dead)} / 错误 {len(err)}（共 {len(vr._CN_JOURNAL_TA)} 条）")
    for cn, ta, count in dead:
        print(f"  零收录（应剔除或改 TA）: {cn} → {ta}")
    for cn, ta, e in err:
        print(f"  查询失败: {cn} → {ta}: {e[:60]}")
    sys.exit(0 if not err else 3)


if __name__ == "__main__":
    main()
