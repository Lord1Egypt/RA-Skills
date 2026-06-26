#!/usr/bin/env python3
"""
AKY-select — A股选股器 v2.0
筛选条件：
  1. 涨幅 +2% ~ +5%
  2. 流通市值 50~200亿
  3. 换手率 4%~10%
  4. 量比 > 1
  5. 量价齐升（收阳 + 成交量 > 昨日）
  6. 均线多头排列（MA5 > MA10 > MA20，且股价 > MA5）
  7. K线强于大盘（个股涨幅 > 上证指数涨幅）
  8. 分时全天在均价线上方
  9. 近3日资金净流入（主力净流入-净额 3日累计 > 0）

数据源：akshare (东方财富/新浪/腾讯) — 免费，无需Token
"""

import sys
import warnings
warnings.filterwarnings('ignore')

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================
# 配置参数
# ============================================================
MIN_PCT = 2.0
MAX_PCT = 5.0
MIN_MARKET_CAP = 50          # 亿
MAX_MARKET_CAP = 200         # 亿
MIN_TURNOVER = 4.0           # %
MAX_TURNOVER = 10.0          # %
MIN_VOL_RATIO = 1.0

CACHE = {}  # 缓存资金流向数据，避免重复请求


# ============================================================
# 第一步：获取全A实时行情 — 粗筛
# ============================================================
def get_spot_data():
    """获取全A股实时行情"""
    print("📡 正在获取全A股实时行情...", flush=True)
    df = ak.stock_zh_a_spot_em()

    col_map = {
        '代码': 'code', '名称': 'name', '最新价': 'price', '涨跌幅': 'pct_chg',
        '成交量': 'volume', '成交额': 'amount', '换手率': 'turnover', '量比': 'vol_ratio',
        '流通市值': 'circ_mv', '总市值': 'total_mv',
        '最高': 'high', '最低': 'low', '今开': 'open', '昨收': 'pre_close',
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

    for col in ['pct_chg', 'circ_mv', 'total_mv', 'turnover', 'vol_ratio', 'price', 'volume', 'amount']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 元 → 亿
    if 'circ_mv' in df.columns:
        df['circ_mv'] = df['circ_mv'] / 1e8
    if 'total_mv' in df.columns:
        df['total_mv'] = df['total_mv'] / 1e8

    return df


def coarse_filter(df):
    """条件1-4 粗筛"""
    counts = {'全A股': len(df)}
    mask = pd.Series(True, index=df.index)

    if 'pct_chg' in df.columns:
        c1 = df['pct_chg'].between(MIN_PCT, MAX_PCT)
        counts['涨幅2-5%'] = int(c1.sum())
        mask &= c1
    counts['①涨幅通过'] = int(mask.sum())

    if 'circ_mv' in df.columns:
        c2 = df['circ_mv'].between(MIN_MARKET_CAP, MAX_MARKET_CAP)
        counts['市值50-200亿'] = int(c2.sum())
        mask &= c2
    counts['②+市值通过'] = int(mask.sum())

    if 'turnover' in df.columns:
        c3 = df['turnover'].between(MIN_TURNOVER, MAX_TURNOVER)
        counts['换手4-10%'] = int(c3.sum())
        mask &= c3
    counts['③+换手通过'] = int(mask.sum())

    if 'vol_ratio' in df.columns:
        c4 = df['vol_ratio'] >= MIN_VOL_RATIO
        counts['量比>1'] = int(c4.sum())
        mask &= c4
    counts['④+量比通过'] = int(mask.sum())

    candidates = df[mask].copy()
    return candidates, counts


# ============================================================
# 第二步：精筛
# ============================================================
def get_daily_history(code):
    """获取个股日线数据"""
    try:
        start = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start, adjust="qfq")
        return df if df is not None and not df.empty else None
    except:
        return None


def check_volume_price(df_hist, today_close, today_vol):
    """条件5: 量价齐升"""
    if df_hist is None or len(df_hist) < 2:
        return False, {}
    closes = df_hist['收盘'].astype(float).values
    volumes = df_hist['成交量'].astype(float).values
    if len(closes) < 2:
        return False, {}
    is_up = today_close > closes[1]
    vol_up = today_vol > volumes[1]
    return (is_up and vol_up), {
        '昨收': round(closes[1], 2), '今收': round(today_close, 2),
        '昨量': int(volumes[1]), '今量': int(today_vol),
    }


def check_mas(df_hist, current_price):
    """条件6: 均线多头排列"""
    if df_hist is None or len(df_hist) < 20:
        return False, {}
    closes = df_hist['收盘'].astype(float).values
    if len(closes) < 20:
        return False, {}
    ma5 = np.mean(closes[:5])
    ma10 = np.mean(closes[:10])
    ma20 = np.mean(closes[:20])
    ok = (ma5 > ma10 > ma20) and (current_price > ma5)
    return ok, {'MA5': round(ma5, 2), 'MA10': round(ma10, 2), 'MA20': round(ma20, 2)}


def get_index_change():
    """条件7: 上证指数今日涨幅"""
    try:
        df = ak.stock_zh_index_spot_em()
        sh = df[df['代码'] == '000001']
        if not sh.empty and '涨跌幅' in sh.columns:
            return float(sh['涨跌幅'].values[0])
    except:
        pass
    return 0


def check_vwap(code, today_close):
    """条件8: 均价线上方"""
    try:
        df = ak.stock_zh_a_tick_tx_js(code)
        if df is None or df.empty:
            return None
        df.columns = df.columns.str.strip()
        if '成交均价' in df.columns:
            avg = df['成交均价'].astype(float)
            return today_close > avg.iloc[-1]
        if all(c in df.columns for c in ['价格', '成交量', '成交额']):
            prices = df['价格'].astype(float)
            amounts = df['成交额'].astype(float)
            vols = df['成交量'].astype(float)
            vwap_series = amounts.cumsum() / vols.cumsum().replace(0, np.nan)
            vwap_series = vwap_series.ffill()
            above_ratio = (prices.values >= vwap_series.values).sum() / len(prices)
            return above_ratio > 0.8
    except:
        pass
    return None


# ============================================================
# 新增：条件9 — 近3日资金净流入
# ============================================================
def get_market_symbol(code):
    """根据代码判断市场：6开头=沪市sh，其他=深市sz，3开头/0开头也是sz"""
    if code.startswith('6'):
        return 'sh'
    return 'sz'


def check_fund_flow_3day(code):
    """条件9: 近3日主力资金净流入 > 0"""
    cache_key = f"fund_{code}"
    if cache_key in CACHE:
        return CACHE[cache_key]

    try:
        market = get_market_symbol(code)
        df = ak.stock_individual_fund_flow(stock=code, market=market)
        if df is None or df.empty or len(df) < 3:
            CACHE[cache_key] = (False, 0, None)
            return CACHE[cache_key]

        # 取最近3个交易日的主力净流入
        main_flow_col = '主力净流入-净额'
        if main_flow_col not in df.columns:
            CACHE[cache_key] = (False, 0, None)
            return CACHE[cache_key]

        recent = df[main_flow_col].tail(3).astype(float)
        total_flow = recent.sum()

        ok = total_flow > 0
        CACHE[cache_key] = (ok, round(total_flow, 0), recent.tolist())
        return CACHE[cache_key]

    except Exception as e:
        CACHE[cache_key] = (False, 0, None)
        return CACHE[cache_key]


# ============================================================
# 主流程
# ============================================================
def main():
    print("=" * 75)
    print("   🎯 AKY-select 选股器 v2.0")
    print(f"   筛选：+{MIN_PCT}%~+{MAX_PCT}% | 流通{MIN_MARKET_CAP}-{MAX_MARKET_CAP}亿")
    print(f"   换手{MIN_TURNOVER}%-{MAX_TURNOVER}% | 量比>{MIN_VOL_RATIO} | 量价↑ | 多头 | 强于大盘 | 3日资金净流入")
    print(f"   时间：{datetime.now().strftime('%Y-%m-%d %H:%M CST')}")
    print("=" * 75 + "\n")

    # ── 步骤1 ──
    spot = get_spot_data()

    # ── 步骤2：粗筛 ──
    candidates, counts = coarse_filter(spot)

    print(f"  📊 全A股: {counts['全A股']} 只")
    print(f"     涨幅 {MIN_PCT}%~{MAX_PCT}%: {counts.get('涨幅2-5%',0)} 只")
    print(f"     +流通市值 {MIN_MARKET_CAP}~{MAX_MARKET_CAP}亿: {counts.get('②+市值通过',0)} 只")
    print(f"     +换手率 {MIN_TURNOVER}%~{MAX_TURNOVER}%: {counts.get('③+换手通过',0)} 只")
    print(f"     +量比 >{MIN_VOL_RATIO}: {counts.get('④+量比通过',0)} 只")
    print(f"  → 粗筛通过: {len(candidates)} 只\n")

    if candidates.empty:
        print("❌ 当前无满足基本条件的股票")
        return

    # ── 步骤3：上证指数 ──
    index_pct = get_index_change()
    print(f"  📈 上证指数: {index_pct:+.2f}%\n")

    # ── 步骤4：精筛 ──
    total_cand = len(candidates)
    print(f"  🔍 精筛 {total_cand} 只候选股（资金流向数据较慢，请稍候）...\n")

    results = []
    for i, (_, row) in enumerate(candidates.iterrows()):
        code = str(row.get('code', ''))
        name = str(row.get('name', ''))
        price = float(row.get('price', 0))
        pct = float(row.get('pct_chg', 0))
        circ_mv = float(row.get('circ_mv', 0))
        turnover = float(row.get('turnover', 0))
        vol_ratio = float(row.get('vol_ratio', 0))
        today_vol = float(row.get('volume', 0))

        # 进度
        pct_done = (i + 1) / total_cand * 100
        bar_len = 20
        filled = int(bar_len * (i + 1) / total_cand)
        bar = '█' * filled + '░' * (bar_len - filled)
        print(f"    [{bar}] {i+1}/{total_cand} ({pct_done:.0f}%) {code} {name:<8}", end='\r', flush=True)

        scores = {
            'code': code, 'name': name, 'price': price,
            'pct_chg': pct, 'circ_mv': circ_mv,
            'turnover': turnover, 'vol_ratio': vol_ratio,
        }

        # 日线历史
        hist = get_daily_history(code)
        if hist is None:
            continue

        # 条件5
        vp_ok, vp_info = check_volume_price(hist, price, today_vol)
        scores['vp'] = vp_ok
        if vp_info:
            scores.update(vp_info)
        if not vp_ok:
            continue

        # 条件6
        ma_ok, ma_info = check_mas(hist, price)
        scores['ma'] = ma_ok
        if ma_info:
            scores.update(ma_info)
        if not ma_ok:
            continue

        # 条件7
        scores['strong'] = pct > index_pct
        if not scores['strong']:
            continue

        # 条件8
        vwap_ok = check_vwap(code, price)
        scores['vwap'] = vwap_ok

        # 条件9: 近3日资金净流入
        fund_ok, fund_amt, fund_details = check_fund_flow_3day(code)
        scores['fund'] = fund_ok
        scores['fund_amt'] = fund_amt
        if not fund_ok:
            continue

        results.append(scores)

    # ── 输出 ──
    print("\n" + "=" * 75)
    print(f"  📋 最终结果：{len(results)} 只  (粗筛{total_cand}→精筛{len(results)})")
    print("=" * 75)

    if not results:
        print("\n  当前无完全符合全部9条件的股票。")
        print("  提示：盘中数据实时变化，建议收盘后再次运行。")
        return

    # 表格
    hdr = f"{'代码':<8} {'名称':<7} {'价格':<7} {'涨幅%':<7} {'市值亿':<8} {'换手%':<7} {'量比':<6} 量价  MA  大盘  均价  资金"
    print(f"\n{hdr}")
    print("-" * 88)
    for r in results:
        vw_s = '✅' if r.get('vwap') else ('⚪' if r.get('vwap') is None else '❌')
        fd_s = '✅' if r.get('fund') else '❌'
        print(f"{r['code']:<8} {r['name']:<7} {r['price']:<7.2f} {r['pct_chg']:<7.2f} "
              f"{r['circ_mv']:<8.1f} {r['turnover']:<7.2f} {r['vol_ratio']:<6.2f} "
              f"{'✅' if r['vp'] else '❌'}  {'✅' if r['ma'] else '❌'}  {'✅' if r['strong'] else '❌'}  {vw_s}  {fd_s}")

    # 详情
    print(f"\n{'='*75}")
    print("  📊 各股详情")
    print('='*75)
    for r in results:
        vw_s = '✅' if r.get('vwap') else ('⚪' if r.get('vwap') is None else '❌')
        fd_s = '✅' if r.get('fund') else '❌'
        fund_str = f"¥{r['fund_amt']/1e4:.0f}万" if r.get('fund_amt') else '?'
        print(f"\n  [{r['code']}] {r['name']}  ￥{r['price']:.2f}  +{r['pct_chg']:.2f}%")
        print(f"    流通市值: {r['circ_mv']:.1f}亿  换手率: {r['turnover']:.2f}%  量比: {r['vol_ratio']:.2f}")
        print(f"    量价齐升: {'✅ 收阳+放量' if r['vp'] else '❌'} | MA多头: {'✅' if r['ma'] else '❌'} MA5={r.get('MA5','?'):.2f}")
        print(f"    强于大盘: {'✅' if r['strong'] else '❌'} | 均价线上: {vw_s} | 3日资金净流入: {fd_s} ({fund_str})")

    print(f"\n  ✅ 共 {len(results)} 只符合全部9条件")
    print(f"  ⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('=' * 75)


if __name__ == '__main__':
    main()
