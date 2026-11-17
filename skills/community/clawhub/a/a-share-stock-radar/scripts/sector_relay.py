#!/usr/bin/env python3
"""
板块资金「接力」（今天的主线，明天还有没有钱进？）

看板：今日主力净额(f62) + 5日(f164) + 10日(f174) 是否同向为正。
  - 今日+5日+10日 全正 → 🟢接力（资金持续）
  - 今日正、5/10日负 → 🟡单日脉冲（可能一日游）
  - 今日正、5日正、10日负 → 🔵刚启动

用法:
  python3 .../sector_relay.py [industry|concept] [N]
数据源：东财 push2 clist（镜像轮换）→ 失败落 akshare。
"""
import argparse
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from radar_common import em_json  # noqa: E402

FIELDS = "f12,f14,f62,f184,f66,f72,f78,f84,f164,f174,f165,f175"


def _pct(v):
    try:
        return float(v)
    except Exception:
        return 0.0


def _fetch(kind):
    fs = "m:90+t:2" if kind == "industry" else "m:90+t:3"
    q = ("api/qt/clist/get?pn=1&pz=100&po=1&np=1&fltt=2&invt=2&fid=f62&fs={fs}&fields={f}"
         .format(fs=fs.replace("+", "%2B"), f=FIELDS))
    obj = em_json(q)
    return (obj.get("data") or {}).get("diff") or []


def _fetch_ak(kind):
    import akshare as ak
    st = "行业资金流" if kind == "industry" else "概念资金流"
    df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type=st)
    out = []
    for _, r in df.iterrows():
        out.append({"f14": r.get("名称"), "f62": r.get("今日主力净流入-净额"),
                    "f164": None, "f174": None, "f184": r.get("今日主力净流入-净占比")})
    return out


def main():
    ap = argparse.ArgumentParser(description="板块资金接力")
    ap.add_argument("kind", nargs="?", default="industry", choices=["industry", "concept"])
    ap.add_argument("n", nargs="?", type=int, default=15)
    a = ap.parse_args()

    rows = []
    try:
        rows = _fetch(a.kind)
    except Exception:
        pass
    if not rows:
        try:
            rows = _fetch_ak(a.kind)
        except Exception as e:
            print("❌ 东财与 akshare 均取不到：{}".format(e)); return 1

    def tag(r):
        t, f5, f10 = _pct(r.get("f62")), _pct(r.get("f164")), _pct(r.get("f174"))
        if f5 is None or f10 is None:
            return "?"
        if t > 0 and f5 > 0 and f10 > 0:
            return "🟢接力"
        if t > 0 and f5 > 0:
            return "🔵启动"
        if t > 0:
            return "🟡脉冲"
        return "🔴流出"

    rows = [r for r in rows if _pct(r.get("f62")) != 0]
    rows.sort(key=lambda r: _pct(r.get("f62")), reverse=True)
    label = "行业" if a.kind == "industry" else "概念"
    print("==== {}板块·资金接力 ====".format(label))
    print("{:<12} {:>12} {:>12} {:>12} {:<8}".format("板块", "今日(万)", "5日(万)", "10日(万)", "判定"))
    for r in rows[:a.n]:
        def fmt(v):
            return "{:>12.0f}".format(float(v) / 1e4) if v is not None else "{:>12}".format("-")
        print("{:<12} {:>12} {:>12} {:>12} {:<8}".format(
            (r.get("f14") or "")[:11], fmt(r.get("f62")), fmt(r.get("f164")), fmt(r.get("f174")), tag(r)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
