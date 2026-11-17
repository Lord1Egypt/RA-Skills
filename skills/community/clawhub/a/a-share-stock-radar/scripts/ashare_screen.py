#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股短线选股筛选器（多数据源：东方财富 → 新浪 自动兜底）
用法：
  python3 ashare_screen.py scan     [N]   # ★真·全市场扫描（涨幅3~9.5% + 换手4~25% + 主力净流入>0）
  python3 ashare_screen.py inflow   [N]   # 主力净流入榜
  python3 ashare_screen.py gainers  [N]   # 涨幅榜
  python3 ashare_screen.py turnover [N]   # 换手率榜
  python3 ashare_screen.py amount   [N]   # 成交额榜
环境变量：SOURCE=em|sina 可强制数据源（默认 em 优先、失败自动切 sina）
"""
import sys, os, json, urllib.request, time

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}

# ---------------- 东方财富（主力源，一次带主力净额） ----------------
EM_HOSTS = ["push2delay.eastmoney.com", "1.push2delay.eastmoney.com",
            "7.push2delay.eastmoney.com", "82.push2delay.eastmoney.com"]
EM_UT = "ut=bd1d9ddb04089700cf9c27f6f7426281"
EM_FS = "fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23"   # 深主板+创业板+沪主板+科创板
EM_FIELDS = "fields=f12,f14,f2,f3,f8,f62,f6"      # 代码,名称,价,涨跌%,换手%,主力净额,成交额

def _num(x):
    try:
        return float(x)
    except Exception:
        return None

def _em_page(pn, pz=100, retries=4):
    last = None
    for k in range(retries):
        host = EM_HOSTS[(pn + k) % len(EM_HOSTS)]  # 按页轮换镜像，分摊压力
        url = (f"https://{host}/api/qt/clist/get?{EM_UT}&pn={pn}&pz={pz}&po=1&np=1"
               f"&fltt=2&invt=2&fid=f3&{EM_FS}&{EM_FIELDS}")
        try:
            req = urllib.request.Request(url, headers={**UA, "Referer": "https://quote.eastmoney.com/"})
            raw = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "replace")
            d = json.loads(raw).get("data") or {}
            return d, host
        except Exception as e:
            last = e
            time.sleep(0.8 * (k + 1))
    raise last

def em_all(max_pages=60):
    rows, pn, used = [], 1, set()
    while pn <= max_pages:
        d, host = _em_page(pn)
        used.add(host)
        diff = d.get("diff") or []
        if not diff:
            break
        rows += diff
        if len(diff) < 100:
            break
        pn += 1
        time.sleep(0.25)
    out = []
    for x in rows:
        code = str(x.get("f12", ""))
        name = str(x.get("f14", ""))
        price = _num(x.get("f2")); pct = _num(x.get("f3"))
        turn = _num(x.get("f8")); r0 = _num(x.get("f62")); amt = _num(x.get("f6"))
        if price is None or pct is None:
            continue
        out.append(dict(code=code, name=name, price=price, pct=pct,
                        turnover=turn if turn is not None else 0.0,
                        amount=(amt or 0) / 1e8, r0=(r0 or 0) / 1e8))
    return out, used

# ---------------- 新浪（兜底：排行 + 资金流） ----------------
RANK_URL = ("https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/"
            "Market_Center.getHQNodeData?page={page}&num={num}&sort={sort}&asc=0&node=hs_a&symbol=&_s_r_a=page")
FLOW_URL = ("https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/"
            "MoneyFlow.ssl_bkzj_ssggzj?page={page}&num={num}&sort=netamount&asc=0&bankuai=&shichang=")

def _sina_get(url, retries=6, backoff=12):
    last = None
    for k in range(retries):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read().decode("utf-8", "replace")
            return json.loads(raw)
        except Exception as e:
            last = e
            time.sleep(backoff * (k + 1))
    raise last

def _sina_page_all(tmpl, num=80, max_pages=120):
    rows, page = [], 1
    while page <= max_pages:
        d = _sina_get(tmpl.format(page=page, num=num))
        if not d:
            break
        rows += d
        if len(d) < num:
            break
        page += 1
        time.sleep(1.2)
    return rows

def sina_all():
    rk = _sina_page_all(RANK_URL.replace("{sort}", "changepercent"))
    fl = {}
    for x in _sina_page_all(FLOW_URL):
        fl[x["symbol"][2:]] = _num(x.get("r0_net")) or 0.0
    out = []
    for x in rk:
        code = x["code"]
        out.append(dict(code=code, name=x["name"], price=_num(x["trade"]),
                        pct=_num(x["changepercent"]), turnover=_num(x["turnoverratio"]) or 0.0,
                        amount=(_num(x["amount"]) or 0) / 1e8, r0=(fl.get(code, 0.0)) / 1e8))
    return out, {"sina"}

# ---------------- 过滤 / 输出 ----------------
def bad(nm):
    return "ST" in str(nm) or str(nm)[:1] in ("N", "C") or str(nm).endswith("退")

def _line(i, r):
    return (f"{i:>2}. {r['code']:<6} {r['name']:<6} {r['price']:>9.2f}  {r['pct']:+6.2f}%  "
            f"换手 {r['turnover']:>5.1f}%  主力净额 {r['r0']:+7.2f}亿  成交 {r['amount']:>6.2f}亿")

def fetch_all(src=None):
    src = src or os.environ.get("SOURCE", "").lower()
    order = ["em", "sina"] if src != "sina" else ["sina", "em"]
    err = []
    for s in order:
        try:
            return (em_all() if s == "em" else sina_all()) + (s,)
        except Exception as e:
            err.append(f"{s}:{e}")
    raise RuntimeError("; ".join(err))

def scan(n):
    print("正在全市场扫描...", flush=True)
    rows, used, src = fetch_all()
    print(f"[源:{src} 域名:{','.join(sorted(used))}] 样本 {len(rows)} 只")
    cand = []
    for r in rows:
        if bad(r["name"]):
            continue
        if not (3.0 <= r["pct"] <= 9.5):
            continue
        if not (4.0 <= r["turnover"] <= 25.0):
            continue
        if r["r0"] <= 0:
            continue
        cand.append(r)
    cand.sort(key=lambda r: r["r0"], reverse=True)
    print(f"== 全市场扫描命中（涨幅3~9.5% + 换手4~25% + 主力净流入>0）共 {len(cand)} 只 ==")
    for i, r in enumerate(cand[:n], 1):
        print(_line(i, r))
    print()

def top(mode, n):
    rows, used, src = fetch_all()
    print(f"[源:{src}] ")
    if mode == "inflow":
        rows = sorted([r for r in rows if not bad(r["name"])], key=lambda r: r["r0"], reverse=True)
    elif mode == "gainers":
        rows = sorted([r for r in rows if not bad(r["name"])], key=lambda r: r["pct"], reverse=True)
    elif mode == "turnover":
        rows = sorted([r for r in rows if not bad(r["name"])], key=lambda r: r["turnover"], reverse=True)
    else:
        rows = sorted([r for r in rows if not bad(r["name"])], key=lambda r: r["amount"], reverse=True)
    for i, r in enumerate(rows[:n], 1):
        print(_line(i, r))
    print()

def main():
    argv = sys.argv[1:] or ["scan", "20"]
    mode = argv[0]
    n = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 20
    try:
        if mode == "scan":
            scan(n)
        else:
            top(mode, n)
    except Exception as e:
        print("❌ 取数失败:", e)

if __name__ == "__main__":
    main()
