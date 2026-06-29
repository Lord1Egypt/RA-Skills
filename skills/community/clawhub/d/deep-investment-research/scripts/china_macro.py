"""china_macro.py — 中国宏观数据采集模块

采集 PMI/CPI/PPI/M2/社融/LPR/南北向资金，输出结构化 JSON + 信号检测。
"""
import os
import json
import sys
import argparse
from datetime import date, datetime
from pathlib import Path

RESEARCH_DATA_ROOT = os.path.expanduser(os.environ.get("RESEARCH_DATA_ROOT", "~/research-data"))


def fetch_china_macro(target_date: str = None) -> dict:
    """Fetch all China macro data, return structured dict."""
    import akshare as ak
    import pandas as pd

    if target_date is None:
        target_date = date.today().isoformat()

    result = {
        "date": target_date,
        "fetch_time": datetime.now().astimezone().isoformat(),
        "monthly_data": {},
        "previous_month": {},
        "mom_changes": {},
        "hsgt_flows": {},
        "signals": [],
        "_errors": [],
    }

    # --- PMI ---
    try:
        df = ak.macro_china_pmi()
        if df is not None and len(df) > 0:
            # Data is sorted newest-first (iloc[0] = latest)
            latest = df.iloc[0]
            prev = df.iloc[1] if len(df) > 1 else None

            result["monthly_data"]["latest_month"] = str(latest.get("月份", ""))
            mfg_col = [c for c in df.columns if "制造业" in c and "指数" in c]
            non_mfg_col = [c for c in df.columns if "非制造业" in c and "指数" in c]

            if mfg_col:
                val = float(latest[mfg_col[0]])
                result["monthly_data"]["pmi_manufacturing"] = val
                if prev is not None:
                    prev_val = float(prev[mfg_col[0]])
                    result["previous_month"]["pmi_manufacturing"] = prev_val
                    result["mom_changes"]["pmi_delta"] = round(val - prev_val, 2)
                # Signals
                if val < 49:
                    result["signals"].append({
                        "type": "pmi_critical",
                        "detail": f"制造业PMI {val} 严重低于荣枯线",
                        "policy_implication": "强刺激预期"
                    })
                elif val < 50:
                    result["signals"].append({
                        "type": "pmi_below_50",
                        "detail": f"制造业PMI {val} 跌破荣枯线",
                        "policy_implication": "宽松预期加强"
                    })

            if non_mfg_col:
                result["monthly_data"]["pmi_non_manufacturing"] = float(latest[non_mfg_col[0]])
    except Exception as e:
        result["_errors"].append(f"PMI: {str(e)[:100]}")

    # --- CPI ---
    try:
        df = ak.macro_china_cpi()
        if df is not None and len(df) > 0:
            latest = df.iloc[0]
            prev = df.iloc[1] if len(df) > 1 else None

            yoy_col = [c for c in df.columns if "同比" in c and "全国" in c]
            mom_col = [c for c in df.columns if "环比" in c and "全国" in c]

            if yoy_col:
                val = float(latest[yoy_col[0]])
                result["monthly_data"]["cpi_yoy"] = val
                if prev is not None:
                    prev_val = float(prev[yoy_col[0]])
                    result["previous_month"]["cpi_yoy"] = prev_val
                    result["mom_changes"]["cpi_delta"] = round(val - prev_val, 2)
                # Signals
                if val < 0:
                    result["signals"].append({
                        "type": "deflation_risk",
                        "detail": f"CPI同比 {val}% 进入通缩",
                        "policy_implication": "降息/降准预期"
                    })
                elif val > 3:
                    result["signals"].append({
                        "type": "inflation_pressure",
                        "detail": f"CPI同比 {val}% 通胀压力",
                        "policy_implication": "收紧预期"
                    })
            if mom_col:
                result["monthly_data"]["cpi_mom"] = float(latest[mom_col[0]])
    except Exception as e:
        result["_errors"].append(f"CPI: {str(e)[:100]}")

    # --- PPI ---
    try:
        df = ak.macro_china_ppi()
        if df is not None and len(df) > 0:
            latest = df.iloc[0]
            prev = df.iloc[1] if len(df) > 1 else None

            yoy_col = [c for c in df.columns if "同比" in c]
            if yoy_col:
                val = float(latest[yoy_col[0]])
                result["monthly_data"]["ppi_yoy"] = val
                if prev is not None:
                    prev_val = float(prev[yoy_col[0]])
                    result["previous_month"]["ppi_yoy"] = prev_val
                    result["mom_changes"]["ppi_delta"] = round(val - prev_val, 2)
    except Exception as e:
        result["_errors"].append(f"PPI: {str(e)[:100]}")

    # --- M2 Money Supply ---
    try:
        df = ak.macro_china_money_supply()
        if df is not None and len(df) > 0:
            latest = df.iloc[0]
            prev = df.iloc[1] if len(df) > 1 else None

            m2_col = [c for c in df.columns if "M2" in c and "同比增长" in c]
            m1_col = [c for c in df.columns if "M1" in c and "同比增长" in c]

            if m2_col:
                m2_val = float(latest[m2_col[0]])
                result["monthly_data"]["m2_yoy"] = m2_val
                if prev is not None:
                    prev_val = float(prev[m2_col[0]])
                    result["previous_month"]["m2_yoy"] = prev_val
                    result["mom_changes"]["m2_delta"] = round(m2_val - prev_val, 2)
            if m1_col:
                m1_val = float(latest[m1_col[0]])
                result["monthly_data"]["m1_yoy"] = m1_val

            # M2-M1 scissors signal
            if m2_col and m1_col:
                m2_v = result["monthly_data"].get("m2_yoy", 0)
                m1_v = result["monthly_data"].get("m1_yoy", 0)
                scissors = m2_v - m1_v
                if scissors > 5:
                    result["signals"].append({
                        "type": "liquidity_trap_risk",
                        "detail": f"M2-M1剪刀差 {scissors:.1f}% (M2={m2_v}%, M1={m1_v}%)",
                        "policy_implication": "宽货币未转化为宽信用，结构性问题"
                    })
    except Exception as e:
        result["_errors"].append(f"M2: {str(e)[:100]}")

    # --- Social Financing (社融, sorted oldest-first) ---
    try:
        df = ak.macro_china_shrzgm()
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            sf_col = [c for c in df.columns if "社会融资规模" in c or "增量" in c]
            if sf_col:
                result["monthly_data"]["social_financing"] = float(latest[sf_col[0]])
            elif len(df.columns) > 1:
                # Fallback: use second column
                result["monthly_data"]["social_financing"] = float(latest.iloc[1])
    except Exception as e:
        result["_errors"].append(f"社融: {str(e)[:100]}")

    # --- LPR (sorted oldest-first) ---
    try:
        df = ak.macro_china_lpr()
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else None

            lpr1y_col = [c for c in df.columns if "1Y" in c.upper() or "1年" in c]
            lpr5y_col = [c for c in df.columns if "5Y" in c.upper() or "5年" in c]
            date_col = [c for c in df.columns if "DATE" in c.upper() or "日期" in c]

            if lpr1y_col:
                lpr1y = float(latest[lpr1y_col[0]])
                result["monthly_data"]["lpr_1y"] = lpr1y
            if lpr5y_col:
                lpr5y = float(latest[lpr5y_col[0]])
                result["monthly_data"]["lpr_5y"] = lpr5y
            if date_col:
                result["monthly_data"]["lpr_date"] = str(latest[date_col[0]])

            # LPR change signal
            if prev is not None and lpr1y_col:
                prev_lpr1y = float(prev[lpr1y_col[0]])
                curr_lpr1y = float(latest[lpr1y_col[0]])
                if curr_lpr1y < prev_lpr1y:
                    result["signals"].append({
                        "type": "lpr_cut",
                        "detail": f"LPR1Y降息 {prev_lpr1y}% → {curr_lpr1y}%",
                        "policy_implication": "货币宽松确认，利好地产/消费"
                    })
                elif curr_lpr1y > prev_lpr1y:
                    result["signals"].append({
                        "type": "lpr_hike",
                        "detail": f"LPR1Y加息 {prev_lpr1y}% → {curr_lpr1y}%",
                        "policy_implication": "收紧信号"
                    })
    except Exception as e:
        result["_errors"].append(f"LPR: {str(e)[:100]}")

    # --- HSGT Flows (南北向资金) ---
    try:
        df = ak.stock_hsgt_fund_flow_summary_em()
        if df is not None and len(df) > 0:
            # Filter for latest date (data is newest-first)
            df['交易日'] = df['交易日'].astype(str)
            latest_date = df['交易日'].iloc[0]
            day_df = df[df['交易日'] == latest_date]

            flows = {"date": str(latest_date)}
            nb_total = 0.0
            sb_sh = 0.0
            sb_sz = 0.0

            for _, row in day_df.iterrows():
                board = str(row.get('板块', ''))
                # 成交净买额 is in 亿元
                net_buy = float(row['成交净买额']) if pd.notna(row.get('成交净买额')) else 0

                if board == '沪股通':  # Northbound via Shanghai
                    nb_total += net_buy
                elif board == '深股通':  # Northbound via Shenzhen
                    nb_total += net_buy
                elif board == '港股通(沪)':  # Southbound via Shanghai
                    sb_sh = net_buy
                elif board == '港股通(深)':  # Southbound via Shenzhen
                    sb_sz = net_buy

            flows["northbound_net_buy"] = round(nb_total, 2)
            flows["southbound_sh_net"] = round(sb_sh, 2)
            flows["southbound_sz_net"] = round(sb_sz, 2)
            flows["southbound_net_buy"] = round(sb_sh + sb_sz, 2)

            # Signals (unit: 亿)
            sb_total = flows["southbound_net_buy"]
            if sb_total > 100:
                result["signals"].append({
                    "type": "southbound_surge",
                    "detail": f"南向资金大幅净买入 {sb_total:.1f}亿",
                    "policy_implication": "港股看多情绪强烈"
                })
            elif sb_total < -100:
                result["signals"].append({
                    "type": "southbound_exodus",
                    "detail": f"南向资金大幅净卖出 {sb_total:.1f}亿",
                    "policy_implication": "港股避险情绪"
                })

            result["hsgt_flows"] = flows
    except Exception as e:
        result["_errors"].append(f"HSGT: {str(e)[:100]}")

    # Fill previous_month.month if we have it
    if result["monthly_data"].get("latest_month") and result["previous_month"]:
        # Derive previous month label from data
        result["previous_month"]["month"] = "上月"

    # Clean up empty _errors
    if not result["_errors"]:
        del result["_errors"]

    return result


def save_output(data: dict, target_date: str = None):
    """Save to daily directory."""
    if target_date is None:
        target_date = date.today().isoformat()

    daily_dir = os.path.join(RESEARCH_DATA_ROOT, "data", "daily", target_date)
    os.makedirs(daily_dir, exist_ok=True)

    output_path = os.path.join(daily_dir, "china_macro.json")
    with open(output_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


def print_summary(data: dict):
    """Print human-readable summary."""
    md = data.get("monthly_data", {})
    flows = data.get("hsgt_flows", {})
    signals = data.get("signals", [])
    changes = data.get("mom_changes", {})

    print(f"\n{'='*50}")
    print(f"  中国宏观数据快照 — {data['date']}")
    print(f"{'='*50}")

    print(f"\n📊 月度经济指标 (最新: {md.get('latest_month', 'N/A')})")
    print(f"  制造业PMI:    {md.get('pmi_manufacturing', 'N/A')}", end="")
    if changes.get("pmi_delta"):
        print(f"  (环比 {changes['pmi_delta']:+.1f})")
    else:
        print()
    print(f"  非制造业PMI:  {md.get('pmi_non_manufacturing', 'N/A')}")
    print(f"  CPI同比:      {md.get('cpi_yoy', 'N/A')}%", end="")
    if changes.get("cpi_delta"):
        print(f"  (环比 {changes['cpi_delta']:+.1f})")
    else:
        print()
    print(f"  CPI环比:      {md.get('cpi_mom', 'N/A')}%")
    print(f"  PPI同比:      {md.get('ppi_yoy', 'N/A')}%", end="")
    if changes.get("ppi_delta"):
        print(f"  (环比 {changes['ppi_delta']:+.1f})")
    else:
        print()
    print(f"  M2同比:       {md.get('m2_yoy', 'N/A')}%")
    print(f"  M1同比:       {md.get('m1_yoy', 'N/A')}%")
    print(f"  社融增量:     {md.get('social_financing', 'N/A')}亿")
    print(f"  LPR(1Y/5Y):  {md.get('lpr_1y', 'N/A')}% / {md.get('lpr_5y', 'N/A')}%  ({md.get('lpr_date', '')})")

    print(f"\n💰 南北向资金 ({flows.get('date', 'N/A')})")
    print(f"  北向净买入:   {flows.get('northbound_net_buy', 'N/A')}亿")
    print(f"  南向净买入:   {flows.get('southbound_net_buy', 'N/A')}亿")
    print(f"    沪港通南向: {flows.get('southbound_sh_net', 'N/A')}亿")
    print(f"    深港通南向: {flows.get('southbound_sz_net', 'N/A')}亿")

    if signals:
        print(f"\n🚨 信号 ({len(signals)})")
        for s in signals:
            print(f"  [{s['type']}] {s['detail']}")
            print(f"    → {s['policy_implication']}")
    else:
        print(f"\n✅ 无异常信号")

    errors = data.get("_errors", [])
    if errors:
        print(f"\n⚠️ 采集异常 ({len(errors)})")
        for e in errors:
            print(f"  ❌ {e}")

    print()


# --- Fetcher class for data_daily.py integration ---
class FetchResult:
    """Mimics the result pattern used by data_daily.py fetchers."""
    def __init__(self, status: str, records: int = 0, reason: str = ""):
        self.status = status
        self.records = records
        self.reason = reason

    def to_status_dict(self):
        d = {"status": self.status, "records": self.records}
        if self.reason:
            d["reason"] = self.reason
        return d


class Fetcher:
    """Integration class for data_daily.py pipeline."""
    name = "china_macro"

    def __init__(self, today: str = None):
        self.today = today or date.today().isoformat()

    def run(self) -> FetchResult:
        try:
            data = fetch_china_macro(self.today)
            save_output(data, self.today)

            errors = data.get("_errors", [])
            records = len(data.get("monthly_data", {})) + len(data.get("hsgt_flows", {}))

            if errors and records == 0:
                return FetchResult("rejected", 0, "; ".join(errors[:3]))
            elif errors:
                return FetchResult("ok", records, f"partial: {len(errors)} sources failed")
            else:
                return FetchResult("ok", records)
        except Exception as e:
            return FetchResult("rejected", 0, str(e)[:200])


def main():
    parser = argparse.ArgumentParser(description="中国宏观数据采集")
    parser.add_argument("--date", default=None, help="目标日期 (YYYY-MM-DD)")
    parser.add_argument("--summary", action="store_true", help="打印人类可读摘要")
    args = parser.parse_args()

    target = args.date or date.today().isoformat()

    print(f"Fetching China macro data for {target}...")
    data = fetch_china_macro(target)
    path = save_output(data, target)
    print(f"Saved to: {path}")

    if args.summary:
        print_summary(data)
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    from _base import cli_main
    cli_main(Fetcher)
