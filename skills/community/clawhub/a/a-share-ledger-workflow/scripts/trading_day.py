"""A股交易日判定（新增，流程规定「买卖时要确认当天是否交易日」）

## 为什么要正式日历

`profit_guard.py` 原先的 `is_trading_day()` 只判「周一至周五 = 交易日」——**这是错的**。
实测反例（某大盘股前复权日K，国庆休市期间）：

    2026-09-25  ← 周五，K线里不存在（国庆休市）
    ...
    2026-10-07  ← 周三，K线里不存在（国庆休市）
    2026-10-08  ← 周四，节后首个交易日

按「工作日=交易日」判断，10-01~10-07 会被误判成交易日。这直接影响：
  · 台账《交易记录》日期写错 → 峰值起点错 → 盈利保护整条线算错
  · 用户报告「我今天买了」，若当天休市则可能是场外成交或记错日期

## 三层判定（可靠性递增，成本递增）

| 层 | 判据 | 说明 |
|---|---|---|
| 1 | 周末 | 必休市，最便宜 |
| 2 | 腾讯日K 列表 | **权威**：休市日不会出现在 K 线里 |
| 3 | 腾讯实时接口时间字段 | 盘中更新到当天；休市日停在最近收盘 |

🔴 **不使用「周一至周五=交易日」这种粗判** —— 节假日 + 调休工作日会让它错得很离谱
（调休的周六其实是交易日，而春节所在的周五其实是休市）。

🔴 **日历不可硬编码**：节假日安排每年由国务院公布，硬编码会过期且无人记得更新。
    本模块不内置假期表，一律现查数据源。
"""

import json
import ssl
import urllib.request

TZ_OFFSET = "+08:00"


def _get(url, timeout=20):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://gu.qq.com/",
    })
    return urllib.request.urlopen(req, timeout=timeout, context=ctx).read()


def kline_dates(pre_code, n=400):
    """返回日K 里的**全部交易日日期**列表（升序）。

    🔴 取 n 根是有意为之，不是性能妥协：
       休市日根本不会出现在 K 线里，所以「日期在列表里」是唯一可靠判据。
       只取 5 根时，「2026-10-01 早于末根 2026-10-09」会被判成交易日 ——
       而它实际是国庆休市。窗口太短 = 把整个长假都变成交易日。
    """
    url = (f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
           f"?param={pre_code},day,,,{n},qfq")
    k = json.loads(_get(url).decode())
    node = k["data"][pre_code]
    kl = node.get("qfqday") or node.get("day") or []
    return [r[0] for r in kl if r and isinstance(r[0], str)]


def realtime_stamp(pre_code):
    """实时接口的报价时间戳，形如 20261009161441。"""
    txt = _get(f"https://qt.gtimg.cn/q={pre_code}").decode("gbk", errors="ignore")
    seg = txt.split('"')
    if len(seg) < 2:
        return None, None
    f = seg[1].split("~")
    if len(f) < 31:
        return None, None
    return f[30], float(f[3] or 0)


def is_trading_day(date_str, pre_code="sh600000"):  # 默认探针：高流动性大盘股；调用方应传实际持仓代码
    """🔴 主入口。date_str = 'YYYY-MM-DD'。

    返回 (是否交易日, 说明, 判定依据)。**查不到一律按「不是交易日」处理**
    —— 宁可在该记账时让用户确认，也不要在休市日默默写入一笔成交。
    """
    # ── 层1：周末
    import datetime
    try:
        d = datetime.date.fromisoformat(date_str)
    except ValueError:
        return False, f"日期格式非法：{date_str}", "本地解析"
    if d.weekday() >= 5:
        return False, f"{date_str} 是{'周六' if d.weekday()==5 else '周日'}，必休市", "周末规则"

    # ── 层2：日K 列表（权威）—— 休市日不在列表里
    try:
        days = kline_dates(pre_code)
        if days:
            if date_str in days:
                return True, f"{date_str} 在日K 交易日列表中，确为交易日", "日K列表"
            if date_str < days[0]:
                return False, (f"日K 数据最早只到 {days[0]}，{date_str} 更早，"
                               f"超出可核验范围"), "日K列表（超范围）"
            if date_str > days[-1]:
                return False, (f"日K 末根是 {days[-1]}，{date_str} 尚无数据 —— "
                               f"休市日不产生K线。若你确定当天成交了，"
                               f"多半是场外交易或日期记错"), "日K列表"
            # 🔴 落在 [首, 末] 区间内但不在列表 → 只可能是休市日（最确定的否定）
            gap_before = max(x for x in days if x < date_str)
            gap_after = min(x for x in days if x > date_str)
            return False, (f"{date_str} 不在日K 列表中，且夹在 {gap_before} 与 "
                           f"{gap_after} 两个交易日之间 → **休市日**"), "日K列表"
    except Exception:
        pass

    # ── 层3：实时接口时间戳
    try:
        stamp, _ = realtime_stamp(pre_code)
        if stamp and len(stamp) >= 8:
            sdate = f"{stamp[0:4]}-{stamp[4:6]}-{stamp[6:8]}"
            if date_str == sdate:
                return True, f"{date_str} 与实时报价时间戳一致", "实时时间戳"
            return False, (f"实时报价停在 {sdate}，{date_str} 无报价 —— "
                           f"休市日不会更新报价"), "实时时间戳"
    except Exception:
        pass

    return False, (f"🔴 无法确认 {date_str} 是否交易日（数据源均失败）"
                   f"→ 按「不是交易日」处理，请人工核实"), "判定失败"


if __name__ == "__main__":
    import sys
    ds = sys.argv[1:] or ["2026-10-09"]
    for x in ds:
        ok, note, src = is_trading_day(x)
        print(f"{x}: {'✅ 交易日' if ok else '❌ 非交易日'}｜{note}｜依据={src}")