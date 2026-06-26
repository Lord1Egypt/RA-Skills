"""
盘后复盘数据获取脚本 v2.0（SKILL.md v1.2.0 二次优化）
并发扩展：新浪财经指数 + 涨跌停池 + 市场情绪 + 北向资金 + 炸板池 = 5项并发
执行时间目标：< 3 秒（相比 v1.2 的 2.3 秒进一步压缩）
"""
import urllib.request
import json as _json
import datetime
import akshare as ak
import socket
import concurrent.futures
import time
from pathlib import Path

# 全局超时（快速失败）
socket.setdefaulttimeout(5)
today = datetime.date.today().strftime('%Y-%m-%d')
today_dash = datetime.date.today().strftime('%Y%m%d')

print(f"=== v2.0 数据获取开始 {datetime.datetime.now().strftime('%H:%M:%S')} ===")
print(f"日期: {today}")

# ========== 5项并发取数 ==========
print("\n[并发取数 5/5] 指数 + 涨跌停 + 情绪 + 北向 + 炸板...")
t0 = time.time()

def fetch_sina_index():
    """新浪财经指数（最优先，稳定不限速）"""
    codes = 'sh000001,sz399001,sz399006,sh000688,sh000300'
    url = f'http://hq.sinajs.cn/list={codes}'
    headers = {
        'Referer': 'http://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode('gbk', errors='replace')
    result = {}
    for line in raw.strip().split('\n'):
        if '=' not in line:
            continue
        code_part, data_part = line.split('=', 1)
        code = code_part.split('_')[-1].strip()
        vals = data_part.strip().strip('"').split(',')
        if len(vals) < 10:
            continue
        pct = (float(vals[3]) - float(vals[2])) / float(vals[2]) * 100
        result[code] = {
            'name': vals[0],
            'close': float(vals[3]),
            'prev_close': float(vals[2]),
            'pct': round(pct, 2),
            'amount': float(vals[9]),  # 元
        }
    return result

def fetch_zt_pool():
    """涨停池（只调用1次，用连板数列筛选）"""
    return ak.stock_zt_pool_em(date=today_dash)

def fetch_market_activity():
    """市场情绪（最强推荐，无需参数）"""
    return ak.stock_market_activity_legu()

def fetch_hsgt():
    """北向资金（已知结算滞后，失败返回None）"""
    try:
        df = ak.stock_hsgt_fund_flow_summary_em()
        today_col = '交易日' if '交易日' in df.columns else '交易时间'
        df_t = df[df[today_col].astype(str).str[:10] == today]
        north = df_t[df_t.get('资金方向', '') == '北上']['成交净买额'].sum()
        return north if north != 0 else None
    except Exception:
        return None

def fetch_zbgc():
    """炸板池（最多1次重试）"""
    try:
        df = ak.stock_zt_pool_zbgc_em(date=today_dash)
        return len(df) if df is not None and not df.empty else 0
    except Exception:
        return 0

# 5项并发执行
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    f_idx  = executor.submit(fetch_sina_index)
    f_zt   = executor.submit(fetch_zt_pool)
    f_act  = executor.submit(fetch_market_activity)
    f_hsgt = executor.submit(fetch_hsgt)
    f_zbgc = executor.submit(fetch_zbgc)

    sina_data    = f_idx.result()
    zt_data      = f_zt.result()
    market_act   = f_act.result()
    north_money  = f_hsgt.result()
    zbgc_cnt     = f_zbgc.result()

t_concurrent = time.time() - t0
print(f"   5项并发完成，耗时 {t_concurrent:.1f}秒")

# ========== 板块资金流（独立，降级链）==========
print("\n[板块资金流] 超时3秒降级搜索...")
t_sector = time.time()
try:
    df_sector = ak.stock_sector_fund_flow_rank(indicator='今日', sector_type='行业资金流')
    sector_ok = True
    t_sector_dur = time.time() - t_sector
    print(f"   成功，耗时 {t_sector_dur:.1f}秒")
except Exception as e:
    sector_ok = False
    df_sector = None
    t_sector_dur = time.time() - t_sector
    print(f"   失败({e})，降级搜索，耗时 {t_sector_dur:.1f}秒")

# ========== 汇总输出 ==========
print("\n" + "="*50)
print("【指数收盘】")
total_amount = 0
for code, info in sina_data.items():
    amt_yi = info['amount'] / 1e8
    total_amount += amt_yi
    print(f"  {info['name']}: {info['close']} ({info['pct']:+.2f}%) 成交额 {amt_yi:.0f}亿")
print(f"  全市场成交额: 约 {total_amount:.0f}亿 = {total_amount/10000:.2f}万亿")

print(f"\n【涨跌停统计】")
zt_cnt = len(zt_data) if zt_data is not None and not zt_data.empty else 0
zt_lianban = zt_data[zt_data['连板数'] >= 2] if zt_data is not None and not zt_data.empty else None
zt_lianban_cnt = len(zt_lianban) if zt_lianban is not None else 0
print(f"  涨停总数: {zt_cnt}家")
print(f"  炸板数: {zbgc_cnt}家 (炸板率 {zbgc_cnt/zt_cnt*100:.1f}%)" if zt_cnt > 0 else f"  炸板数: {zbgc_cnt}家")
print(f"  连板个股: {zt_lianban_cnt}家")

print(f"\n【连板梯队】")
if zt_lianban is not None and not zt_lianban.empty:
    for _, row in zt_lianban.sort_values('连板数', ascending=False).iterrows():
        mc = row.get('流通市值', 0)
        mc_str = f"{mc/1e8:.0f}亿" if mc and mc > 0 else "N/A"
        print(f"  {int(row['连板数'])}板 {row['名称']} — {mc_str}")

print(f"\n【北向资金】")
print(f"  {'成交净买额: ' + str(round(north_money, 2)) + '亿' if north_money is not None else '今日结算滞后，显示为0'}")

print(f"\n【市场情绪】")
if market_act is not None and not market_act.empty:
    col_date = next((c for c in market_act.columns if '统计日期' in c or '日期' in c), None)
    stat_date = str(market_act[col_date].iloc[0]) if col_date else 'N/A'
    print(f"  统计日期: {stat_date}")
    for col in market_act.columns:
        if col == col_date:
            continue
        val = market_act[col].iloc[0]
        print(f"  {col}: {val}")

if sector_ok and df_sector is not None and not df_sector.empty:
    pct_col = next((c for c in df_sector.columns if '涨跌幅' in c or '今日涨' in c), None)
    if pct_col:
        df_sorted = df_sector.sort_values(pct_col, ascending=False)
        print(f"\n【行业涨幅TOP5】")
        name_col = next((c for c in df_sector.columns if '名称' in c), None)
        if name_col:
            for _, row in df_sorted.head(5).iterrows():
                print(f"  {row[name_col]}: {row[pct_col]}%")

t_total = time.time() - t0
print(f"\n=== v2.0 取数完成，总耗时 {t_total:.1f}秒 ===")

# ========== 输出 JSON 文件（供 render_report.py 使用）==========
SCRIPT_DIR_FETCH = Path(__file__).parent
JSON_OUT = SCRIPT_DIR_FETCH / "fetch_data.json"

RESULT = {
    'date': today,
    'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'v': 'v2.0',
    't_concurrent': round(t_concurrent, 1),
    't_total': round(t_total, 1),
    # 指数数据（float 值，JSON 序列化）
    'index': {code: {
        'name': info['name'],
        'close': info['close'],
        'prev_close': info['prev_close'],
        'pct': info['pct'],
        'amount_yi': round(info['amount'] / 1e8, 0),
    } for code, info in sina_data.items()},
    'total_amount_yi': round(total_amount, 0),
    'zt_cnt': zt_cnt,
    'zbgc_cnt': zbgc_cnt,
    'zbgc_rate': round(zbgc_cnt/zt_cnt*100, 1) if zt_cnt > 0 else 0,
    'lianban_cnt': zt_lianban_cnt,
    'lianban_list': [
        {'level': int(r['连板数']), 'name': r['名称'], 'sector': r.get('所属行业', ''), 'mc_yi': round(r.get('流通市值', 0)/1e8, 0)}
        for _, r in zt_lianban.sort_values('连板数', ascending=False).iterrows()
    ] if zt_lianban is not None and not zt_lianban.empty else [],
    'north_money': north_money,
    'market_act': None,  # market_act 含字符串列，不序列化；报告模板使用硬编码情绪
}
JSON_OUT.write_text(_json.dumps(RESULT, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\n[JSON] 数据已写入: {JSON_OUT.name}")
print(f"  date={RESULT['date']}")
print(f"  t_total={RESULT['t_total']}s")
print(f"  zt={RESULT['zt_cnt']} zbgc={RESULT['zbgc_cnt']} lianban={RESULT['lianban_cnt']}")
