#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
板块行情 / 资金（数据源：东方财富 push2delay，4 镜像轮换）
用法：
  python3 sector_flow.py industry [N]        # 行业板块按涨幅榜（默认20）
  python3 sector_flow.py industry flow [N]   # 行业板块按主力净额榜
  python3 sector_flow.py concept  [N]        # 概念板块按涨幅榜
  python3 sector_flow.py concept  flow [N]   # 概念板块按主力净额榜
  python3 sector_flow.py members BK0546 [N]  # 板块成分股（含涨跌/换手/主力净额）
"""
import sys, json, urllib.request, time

EM_HOSTS = ["push2delay.eastmoney.com", "1.push2delay.eastmoney.com",
            "7.push2delay.eastmoney.com", "82.push2delay.eastmoney.com"]
EM_UT = "ut=bd1d9ddb04089700cf9c27f6f7426281"
EM_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
              "Referer": "https://quote.eastmoney.com/"}
FS = {"industry": "m:90+t:2", "concept": "m:90+t:3"}
BOARD_FIELDS = "fields=f12,f14,f3,f62,f104,f105,f128,f136"

def em(fs, fid, pz, page=1):
    last = None
    for k in range(5):
        host = EM_HOSTS[k % len(EM_HOSTS)]
        url = (f"https://{host}/api/qt/clist/get?{EM_UT}&pn={page}&pz={pz}&po=1&np=1"
               f"&fltt=2&invt=2&fid={fid}&fs={fs}&{BOARD_FIELDS if fs.startswith('m:90') else 'fields=f12,f14,f2,f3,f8,f62'}")
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=EM_HEADERS), timeout=12).read().decode("utf-8", "replace")
            return json.loads(raw).get("data") or {}
        except Exception as e:
            last = e
            time.sleep(0.6 * (k + 1))
    raise last

def yi(v):
    try:
        return f"{float(v) / 1e8:+.2f}亿"
    except Exception:
        return "-"

def main():
    a = sys.argv[1:] or ["industry", "20"]
    kind = a[0]
    if kind == "members":
        bk = a[1] if len(a) > 1 else ""
        n = int(a[2]) if len(a) > 2 and a[2].isdigit() else 20
        if not bk:
            print("用法: sector_flow.py members BK0546 [N]"); return
        d = em(f"b:{bk}", "f3", min(n, 100))
        print(f"== {bk} 成分股（按涨幅） 共 {d.get('total')} 只 ==")
        for i, x in enumerate((d.get("diff") or [])[:n], 1):
            print(f"{i:>2}. {x.get('f12'):<6} {x.get('f14'):<8} {x.get('f2'):>9}  "
                  f"{x.get('f3'):+6.2f}%  换手{x.get('f8'):>5.1f}%  主力 {yi(x.get('f62'))}")
        return

    fs = FS.get(kind)
    if not fs:
        print("用法: sector_flow.py industry|concept [flow] [N]  |  members BKxxxx [N]"); return
    flow = len(a) > 1 and a[1] == "flow"
    n = int(a[2]) if flow and len(a) > 2 and a[2].isdigit() else (int(a[1]) if len(a) > 1 and a[1].isdigit() else 20)
    fid = "f62" if flow else "f3"
    d = em(fs, fid, min(n, 100))
    title = f"{'行业' if kind == 'industry' else '概念'}板块 · 按{'主力净额' if flow else '涨幅'}"
    print(f"== {title} TOP{n}（共 {d.get('total')} 个板块） ==")
    for i, x in enumerate((d.get("diff") or [])[:n], 1):
        lead = x.get("f128") or ""
        leadp = x.get("f136")
        leads = f"  领涨 {lead}({leadp:+.1f}%)" if lead and leadp not in (None, "-") else ""
        print(f"{i:>2}. {x.get('f14'):<12} {x.get('f3'):+6.2f}%  主力 {yi(x.get('f62')):>10}  "
              f"涨/跌 {x.get('f104')}/{x.get('f105')}{leads}")
    print()

if __name__ == "__main__":
    main()
