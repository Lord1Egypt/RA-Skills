#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场情绪温度计（A股短线）—— 给"先判环境，再选股"用。

数据源：东方财富涨停/跌停/炸板池（push2ex.eastmoney.com）
用法：
  python3 skills/trading-desk/scripts/emotion.py            # 今日
  python3 skills/trading-desk/scripts/emotion.py 20260923   # 指定交易日

输出：
  1) 涨停/跌停/炸板家数 + 封板率
  2) 连板梯队（最高板、2板以上各级家数）
  3) 昨日涨停今日溢价 + 晋级率（赚钱效应）
  4) 情绪阶段判定（冰点/修复/启动/发酵/高潮/退潮）+ 建议仓位
  5) 涨停最集中的行业（主线线索）
"""
import sys, json, time, urllib.request, datetime

UT = "7eea3edcaed734bea9cbfc24409ed989"
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://quote.eastmoney.com/"}


def _get(url, tries=3):
    for i in range(tries):
        try:
            return json.loads(urllib.request.urlopen(
                urllib.request.Request(url, headers=HDR), timeout=12).read().decode("utf-8", "replace"))
        except Exception:
            time.sleep(1.2)
    return None


def pool(kind, date, pagesize=600):
    """kind: ZT=涨停 ZB=炸板 DT=跌停"""
    url = (f"https://push2ex.eastmoney.com/getTopic{kind}Pool?ut={UT}&dpt=wz.ztzt"
           f"&Pageindex=0&pagesize={pagesize}&sort=fbt:asc&date={date}")
    d = _get(url)
    if not d or not d.get("data"):
        return []
    return d["data"].get("pool") or []


def pool_count(kind, date):
    url = (f"https://push2ex.eastmoney.com/getTopic{kind}Pool?ut={UT}&dpt=wz.ztzt"
           f"&Pageindex=0&pagesize=1&sort=fbt:asc&date={date}")
    d = _get(url)
    if not d or not d.get("data"):
        return 0
    return d["data"].get("tc") or 0


def prev_trading_day(date):
    d = datetime.datetime.strptime(str(date), "%Y%m%d")
    for _ in range(10):
        d -= datetime.timedelta(days=1)
        if d.weekday() < 5:
            if pool_count("ZT", d.strftime("%Y%m%d")) > 0:
                return d.strftime("%Y%m%d")
    return None


def sina_quotes(codes):
    """codes: 6位代码列表 -> {code: (name, pct)}"""
    pre = lambda c: ("sh" if c[0] in "56" or c.startswith("688") else
                     "bj" if c[0] in "489" else "sz")
    out = {}
    for i in range(0, len(codes), 60):
        chunk = codes[i:i+60]
        url = "https://hq.sinajs.cn/list=" + ",".join(pre(c)+c for c in chunk)
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"}), timeout=10).read().decode("gbk", "replace")
        except Exception:
            continue
        for line in raw.splitlines():
            if '="' not in line:
                continue
            body = line.split('="', 1)[1].rstrip('";')
            parts = body.split(",")
            if len(parts) < 4:
                continue
            code = line.split("hq_str_")[1].split("=")[0][2:]
            try:
                prev = float(parts[2]); cur = float(parts[3])
                out[code] = (parts[0], (cur/prev-1)*100 if prev else 0.0)
            except Exception:
                pass
        time.sleep(0.4)
    return out


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().strftime("%Y%m%d")
    zt = pool("ZT", date); zb = pool("ZB", date)
    ztc = pool_count("ZT", date); zbc = pool_count("ZB", date); dtc = pool_count("DT", date)

    print(f"===== 市场情绪温度计  {date} =====")
    print(f"涨停 {ztc}  |  跌停 {dtc}  |  炸板 {zbc}  |  封板率 {(ztc/(ztc+zbc)*100 if ztc+zbc else 0):.1f}%")

    # 连板梯队
    maxlb = 0; tiers = {}
    for r in zt:
        lb = int(r.get("lbc") or 1)
        maxlb = max(maxlb, lb)
        if lb >= 2:
            tiers[lb] = tiers.get(lb, 0) + 1
    tl = " | ".join(f"{k}板×{tiers[k]}" for k in sorted(tiers, reverse=True)) or "无2板以上"
    print(f"最高板 {maxlb} 板  |  {tl}")

    # 昨日涨停 → 今日溢价/晋级率
    pd = prev_trading_day(date)
    prem = None; promote = None
    if pd:
        yzt = pool("ZT", pd)
        ycodes = [r["c"] for r in yzt]
        q = sina_quotes(ycodes)
        pcts = [q[c][1] for c in ycodes if c in q]
        if pcts:
            prem = sum(pcts)/len(pcts)
        today_zt = set(r["c"] for r in zt)
        if ycodes:
            promote = len([c for c in ycodes if c in today_zt])/len(ycodes)*100
        print(f"昨日({pd})涨停 {len(ycodes)} 只 → 今日平均溢价 {prem:+.2f}%  |  晋级率 {promote:.1f}%")

    # 行业集中度
    from collections import Counter
    hy = Counter(r.get("hybk") or "-" for r in zt)
    print("涨停最多行业: " + "  ".join(f"{k}({v})" for k, v in hy.most_common(6)))

    # 阶段判定 & 仓位建议
    stage, pos = judge(ztc, dtc, zbc, maxlb, prem, promote)
    print(f"\n>>> 情绪阶段: {stage}   |   建议仓位: {pos}")
    print(">>> " + advice(stage))


def judge(ztc, dtc, zbc, maxlb, prem, promote):
    seal = ztc/(ztc+zbc)*100 if ztc+zbc else 0
    prem = prem if prem is not None else 0
    promote = promote if promote is not None else 0
    if ztc < 20 and maxlb <= 2:
        return "冰点期", "0~2 成（空仓/极低仓观望）"
    if dtc > ztc:
        return "退潮期", "≤2 成（降仓、高低切、只做低位先手）"
    if maxlb >= 6 and ztc >= 80 and prem > 3:
        return "高潮期", "5~6 成（开始兑现、去掉后排、只抱核心）"
    if maxlb >= 4 and prem > 1.5 and promote >= 20:
        return "发酵期", "5~7 成（做主线龙头/强分化低吸）"
    if prem > 0 and promote >= 15 and maxlb >= 3:
        return "启动/回暖期", "3~5 成（低位核心先手、主线龙一低吸）"
    if prem < -1 or (ztc < 40 and seal < 65):
        return "退潮/分歧期", "≤3 成（试错为主、不追高）"
    return "混沌期", "3~4 成（轻仓、只做最强/低吸）"


def advice(stage):
    m = {
        "冰点期": "多看少动，等『涨停家数回升+最高板打开+昨日涨停开始有溢价』三重拐点再进场。",
        "启动/回暖期": "情绪修复，买低位核心股先手（首板/二板），仓位随回暖逐步加。",
        "发酵期": "做主线龙头与强分歧低吸，去弱留强，别买后排跟风。",
        "高潮期": "赚钱效应最猛也是最危险：边涨边减，拥抱核心、抛弃后排。",
        "退潮期": "禁止高位接力；只做低位套利或龙头反抽，快进快出。",
        "退潮/分歧期": "不做高位板接力，低吸为主，仓位压到 3 成内。",
        "混沌期": "大盘股低吸半路，只做最强，宁可错过不可做错。",
    }
    return m.get(stage, "顺势而为，控制仓位，严守止损。")


if __name__ == "__main__":
    main()
