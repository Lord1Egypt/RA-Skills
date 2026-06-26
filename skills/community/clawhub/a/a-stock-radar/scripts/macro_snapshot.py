"""
A股宏观快照
优先展示 SHIBOR、LPR、中美10Y利差、北向资金和新增人民币贷款。
"""
try:
    import akshare as ak
except ImportError:
    ak = None
import contextlib
import io


MACRO_NOTES = {
    "SHIBOR": {"desc": "银行间借贷成本，衡量流动性松紧", "us_equivalent": "≈ SOFR"},
    "LPR": {"desc": "贷款市场报价利率，影响房贷与企业融资", "us_equivalent": "≈ Fed Rate"},
    "CN_US_10Y_SPREAD": {"desc": "中美10Y国债利差，影响汇率与外资预期", "us_equivalent": "≈ 10Y-2Y利差"},
    "NORTHBOUND": {"desc": "北向资金净流入，反映外资配置A股情绪", "us_equivalent": "—"},
    "BANK_FINANCING": {"desc": "新增人民币贷款，反映实体融资需求", "us_equivalent": "—"},
}


def extract_shibor_snapshot(df):
    row = df.iloc[-1]
    return {
        "date": str(row["日期"]),
        "on": float(row["O/N-定价"]),
        "1w": float(row["1W-定价"]),
        "1m": float(row["1M-定价"]),
        "3m": float(row["3M-定价"]),
    }


def extract_lpr_snapshot(df):
    row = df.iloc[-1]
    return {
        "date": str(row["TRADE_DATE"]),
        "1y": float(row["LPR1Y"]),
        "5y": float(row["LPR5Y"]),
    }


def extract_cn_us_spread(df):
    row = df.iloc[-1]
    china_10y = float(row["中国国债收益率10年"])
    us_10y = float(row["美国国债收益率10年"])
    return {
        "date": str(row["日期"]),
        "china_10y": china_10y,
        "us_10y": us_10y,
        "spread": china_10y - us_10y,
        "spread_bp": (china_10y - us_10y) * 100,
    }


def extract_northbound_flow(df):
    latest_date = df["交易日"].max()
    latest = df[(df["交易日"] == latest_date) & (df["资金方向"] == "北向")]
    net_buy = float(latest["成交净买额"].sum())
    return {
        "date": str(latest_date),
        "net_buy": net_buy,
    }


def extract_bank_financing(df):
    row = df.iloc[-1]
    return {
        "date": str(row["日期"]),
        "value": float(row["最新值"]),
        "pct": float(row["涨跌幅"]),
    }


def get_macro_snapshot():
    if ak is None:
        return {}

    snapshot = {}
    try:
        snapshot["SHIBOR"] = extract_shibor_snapshot(_quiet_call(ak.macro_china_shibor_all))
    except Exception:
        pass

    try:
        snapshot["LPR"] = extract_lpr_snapshot(_quiet_call(ak.macro_china_lpr))
    except Exception:
        pass

    try:
        snapshot["CN_US_10Y_SPREAD"] = extract_cn_us_spread(_quiet_call(ak.bond_zh_us_rate))
    except Exception:
        pass

    try:
        snapshot["NORTHBOUND"] = extract_northbound_flow(_quiet_call(ak.stock_hsgt_fund_flow_summary_em))
    except Exception:
        pass

    try:
        snapshot["BANK_FINANCING"] = extract_bank_financing(_quiet_call(ak.macro_china_bank_financing))
    except Exception:
        pass

    return snapshot


def _quiet_call(func):
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        return func()


def format_macro_snapshot(snapshot):
    lines = []

    shibor = snapshot.get("SHIBOR")
    if shibor:
        lines.append(
            f"🔹 SHIBOR ({shibor['date']}): O/N {shibor['on']:.3f}% | 1W {shibor['1w']:.3f}% | "
            f"1M {shibor['1m']:.3f}% | 3M {shibor['3m']:.3f}%"
        )

    lpr = snapshot.get("LPR")
    if lpr:
        lines.append(f"🔹 LPR ({lpr['date']}): 1Y {lpr['1y']:.2f}% | 5Y {lpr['5y']:.2f}%")

    spread = snapshot.get("CN_US_10Y_SPREAD")
    if spread:
        lines.append(
            f"🔹 中美10Y利差 ({spread['date']}): 中国 {spread['china_10y']:.2f}% | 美国 {spread['us_10y']:.2f}% | "
            f"利差 {spread['spread_bp']:+.0f}bp"
        )

    northbound = snapshot.get("NORTHBOUND")
    if northbound:
        arrow = "🔴" if northbound["net_buy"] > 0 else "🟢" if northbound["net_buy"] < 0 else "⚪"
        lines.append(f"{arrow} 北向资金 ({northbound['date']}): 净买额 {northbound['net_buy']:+.2f} 亿")

    financing = snapshot.get("BANK_FINANCING")
    if financing:
        lines.append(
            f"🔹 新增人民币贷款 ({financing['date']}): {financing['value']:.0f} 亿元 | "
            f"涨跌幅 {financing['pct']:+.2f}%"
        )

    return lines


if __name__ == "__main__":
    print("\n=== 🌏 A股宏观快照 ===")
    snapshot = get_macro_snapshot()
    if not snapshot:
        print("宏观数据暂不可用")
    else:
        for line in format_macro_snapshot(snapshot):
            print(line)
        print("\n说明:")
        print(f"- SHIBOR: {MACRO_NOTES['SHIBOR']['desc']} {MACRO_NOTES['SHIBOR']['us_equivalent']}")
        print(f"- LPR: {MACRO_NOTES['LPR']['desc']} {MACRO_NOTES['LPR']['us_equivalent']}")
        print(
            f"- 中美10Y利差: {MACRO_NOTES['CN_US_10Y_SPREAD']['desc']} "
            f"{MACRO_NOTES['CN_US_10Y_SPREAD']['us_equivalent']}"
        )
