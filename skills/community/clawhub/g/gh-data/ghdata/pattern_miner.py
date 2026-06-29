"""
规律挖掘 — 从历史K线中自动发现大涨/大跌后的走势规律
====================================================
"""


def up_pullback(klines, lookback=90):
    """
    大涨后回调特征分析。
    找到过去 lookback 天中涨幅>3%的交易日，统计随后3日的平均涨跌幅。

    Returns
    -------
    dict or None
        {"samples": [...], "conclusion": "...", "hitRate": "..."}
    """
    if len(klines) < lookback:
        return None

    samples = []
    n = len(klines)
    for i in range(1, lookback - 5):
        idx = n - i
        prev_idx = idx - 1
        chg = (klines[idx]["close"] - klines[prev_idx]["close"]) / klines[prev_idx]["close"] * 100

        if chg > 3:
            d3_idx = n - i + 2
            if d3_idx < n:
                d3 = (klines[d3_idx]["close"] - klines[idx]["close"]) / klines[idx]["close"] * 100
                samples.append({
                    "date": klines[idx]["date"],
                    "chg": f"+{chg:.1f}%",
                    "d3": f"{d3:+.1f}%",
                    "result": "回调" if d3 < 0 else "续涨"
                })

    if not samples:
        return None

    d3s = [float(s["d3"].replace("%", "")) for s in samples]
    avg = sum(d3s) / len(d3s)
    hit = sum(1 for c in d3s if c < 0)

    return {
        "samples": samples[:3],
        "conclusion": f"3日平均{avg:+.1f}%",
        "hitRate": f"{hit}/{len(d3s)}={hit * 100 // len(d3s)}%回调"
    }


def down_rebound(klines, lookback=90):
    """
    大跌后反弹特征分析。
    找到过去 lookback 天中跌幅>3%的交易日，统计随后3日的平均涨跌幅。

    Returns
    -------
    dict or None
    """
    if len(klines) < lookback:
        return None

    samples = []
    n = len(klines)
    for i in range(1, lookback - 5):
        idx = n - i
        prev_idx = idx - 1
        chg = (klines[idx]["close"] - klines[prev_idx]["close"]) / klines[prev_idx]["close"] * 100

        if chg < -3:
            d3_idx = n - i + 2
            if d3_idx < n:
                d3 = (klines[d3_idx]["close"] - klines[idx]["close"]) / klines[idx]["close"] * 100
                samples.append({
                    "date": klines[idx]["date"],
                    "chg": f"{chg:+.1f}%",
                    "d3": f"{d3:+.1f}%",
                    "result": "反弹" if d3 > 0 else "续跌"
                })

    if not samples:
        return None

    d3s = [float(s["d3"].replace("%", "")) for s in samples]
    avg = sum(d3s) / len(d3s)
    hit = sum(1 for c in d3s if c > 0)

    conc_text = f"3日平均反弹{avg:+.1f}%" if avg > 0 else f"3日平均{avg:+.1f}%（反弹失败）"
    return {
        "samples": samples[:3],
        "conclusion": conc_text,
        "hitRate": f"{hit}/{len(d3s)}={hit * 100 // len(d3s)}%反弹"
    }


def resistance(klines, lookback=60):
    """阻力位识别 — 通过价格密度聚类"""
    if len(klines) < 20:
        return None
    pts = {}
    for item in klines[-lookback:]:
        b = round(item["high"] * 2) / 2
        pts[b] = pts.get(b, 0) + 1

    if not pts:
        return None

    sorted_pts = sorted(pts.items(), key=lambda x: -x[1])
    rh = max(item["high"] for item in klines[-lookback:])

    mr = None
    for p, c in sorted_pts:
        if p >= 0.8 * rh and p <= rh * 1.05 and c >= 2:
            mr = (p, c)
            break

    if mr is None and sorted_pts:
        mr = sorted_pts[0]

    if mr:
        return {
            "r1": f"阻力位① {mr[0]:.2f}元(触及{mr[1]}次)",
            "r2": f"阻力位② {rh:.2f}元(近期高点)"
        }
    return None


def support(klines, lookback=60):
    """支撑位识别 — 通过价格密度聚类"""
    if len(klines) < 20:
        return None
    pts = {}
    for item in klines[-lookback:]:
        b = round(item["low"] * 2) / 2
        pts[b] = pts.get(b, 0) + 1

    if not pts:
        return None

    sorted_pts = sorted(pts.items(), key=lambda x: -x[1])
    rl = min(item["low"] for item in klines[-lookback:])

    ms = None
    for p, c in sorted_pts:
        if p <= rl * 1.2 and p >= rl * 0.95 and c >= 2:
            ms = (p, c)
            break

    if ms is None and sorted_pts:
        ms = sorted_pts[0]

    if ms:
        return {
            "s1": f"支撑位① {ms[0]:.2f}元(触及{ms[1]}次)",
            "s2": f"支撑位② {rl:.2f}元(近期低点)"
        }
    return None


def nature(klines, lookback=60):
    """回调性质判断 — 当前走势属于上涨中继还是下跌中继"""
    if len(klines) < 30:
        return None

    closes = [k["close"] for k in klines[-lookback:]]
    highs = [k["high"] for k in klines[-lookback:]]
    lows = [k["low"] for k in klines[-lookback:]]

    pct = (closes[-1] - closes[0]) / closes[0] * 100
    vol = sum(k["volume"] for k in klines[-5:]) / max(sum(k["volume"] for k in klines[-20:-5]), 1)

    if pct > 10 and closes[-1] > sum(closes[-5:]) / 5:
        return {"status": "上涨中继", "conclusion": f"涨幅{pct:.1f}%，缩量{vol:.2f}倍，回调可视为洗盘"}
    elif pct < -10 and closes[-1] < sum(closes[-5:]) / 5:
        return {"status": "下跌中继", "conclusion": f"跌幅{pct:.1f}%，建议观望"}
    else:
        return {"status": "震荡整理", "conclusion": f"区间{pct:.1f}%，等待方向选择"}


def mine_all(klines):
    """
    一键挖掘全部5种规律。

    Parameters
    ----------
    klines : list[dict]
        需包含 date, close, high, low, volume，按日期升序

    Returns
    -------
    dict
        {"大涨后回调特征": ..., "大跌后反弹特征": ..., ...}
    """
    result = {}
    for name, func in [
        ("大涨后回调特征", up_pullback),
        ("大跌后反弹特征", down_rebound),
        ("阻力位识别", resistance),
        ("支撑位识别", support),
        ("回调性质判断", nature),
    ]:
        r = func(klines)
        if r:
            result[name] = r
    return result


# 兼容别名
mine = mine_all
