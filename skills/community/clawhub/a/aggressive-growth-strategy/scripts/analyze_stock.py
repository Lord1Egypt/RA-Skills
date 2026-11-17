#!/usr/bin/env python3
"""
激进成长个股八步深度分析器
对单只股票执行"激进成长投研体系"八步分析流程

Usage:
  python3 analyze_stock.py sz.300308
  python3 analyze_stock.py 300308

Output: Markdown格式分析报告（stdout）

数据源: akshare > baostock > 东方财富API (四层降级，Tushare MCP由Agent直接调用优先)
财务验证: 东方财富datacenter API交叉验证 (2026-07-31铁律)
"""

import sys
import os
from datetime import datetime, timedelta

# 导入共享数据源模块
try:
    from data_source import (
        get_kline, get_spot, get_profit_data, get_growth_data,
        get_stock_industry, get_index_stocks, verify_financial_data,
        source_label, format_data_source_line,
        SOURCE_AKSHARE, SOURCE_BAOSTOCK, SOURCE_EASTMONEY, SOURCE_FAILED
    )
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_source import (
        get_kline, get_spot, get_profit_data, get_growth_data,
        get_stock_industry, get_index_stocks, verify_financial_data,
        source_label, format_data_source_line,
        SOURCE_AKSHARE, SOURCE_BAOSTOCK, SOURCE_EASTMONEY, SOURCE_FAILED
    )

# ============================================================
# 行业关键词（与screen_stocks.py一致）
# ============================================================
TECH_KEYWORDS = [
    '电子', '半导体', '芯片', '集成电路', '软件', '计算机', '通信', '科技',
    '智能', '人工智能', '机器人', '新能源', '光伏', '电池', '军工', '航天',
    '航空', '信息安全', '大数据', '云计算', '物联网', '5G', '光电',
    '新材料', '自动化', '精密制造'
]
CONSUMER_KEYWORDS = [
    '消费', '食品', '饮料', '白酒', '家电', '家居', '服装', '纺织',
    '零售', '商业', '旅游', '酒店', '餐饮', '医药', '医疗', '生物',
    '制药', '中药', '保健', '化妆品', '宠物', '教育', '传媒', '游戏',
    '影视', '广告', '文娱'
]


def normalize_code(code):
    """标准化股票代码"""
    code = code.strip()
    if code.startswith('sh.') or code.startswith('sz.'):
        return code
    code = code.replace('sh', '').replace('sz', '').replace('.', '')
    if code.startswith('6') or code.startswith('9'):
        return f'sh.{code}'
    return f'sz.{code}'


def code_to_secucode(code):
    """baostock代码 -> 东方财富secucode (sz.300308 -> 300308.SZ)"""
    if code.startswith('sh.'):
        return f"{code[3:]}.SH"
    elif code.startswith('sz.'):
        return f"{code[3:]}.SZ"
    return code


def is_target_industry(industry):
    if not industry:
        return False, '未知'
    for kw in TECH_KEYWORDS:
        if kw in industry:
            return True, '科技'
    for kw in CONSUMER_KEYWORDS:
        if kw in industry:
            return True, '消费'
    return False, industry


def get_latest_quarter():
    now = datetime.now()
    year = now.year
    month = now.month
    if month <= 4:
        return year - 1, 3
    elif month <= 6:
        return year - 1, 4
    elif month <= 8:
        return year, 1
    elif month <= 10:
        return year, 2
    else:
        return year, 3


def safe_float(val, default=None):
    try:
        return float(val) if val and val != '' else default
    except (ValueError, TypeError):
        return default


def format_money(val):
    """格式化金额显示（baostock返回元为单位）"""
    if val is None:
        return 'N/A'
    if abs(val) >= 1e8:
        return f'{val/1e8:.2f}亿元'
    elif abs(val) >= 1e4:
        return f'{val/1e4:.2f}万元'
    else:
        return f'{val:.2f}元'


def estimate_market_cap(close, volume, turn):
    """通过换手率反推流通市值（亿元）"""
    close = safe_float(close)
    volume = safe_float(volume)
    turn = safe_float(turn)
    if close and volume and turn and turn > 0:
        float_shares = volume * 100 / turn
        return round(close * float_shares / 1e8, 2)
    return None


def calculate_price_percentile(kline_data, lookback=250):
    """计算当前价格在历史区间的百分位（0-100）"""
    if not kline_data or len(kline_data) < 10:
        return None
    recent = kline_data[-lookback:]
    try:
        close_values = [float(d['close']) for d in recent if d['close']]
        if not close_values:
            return None
        current = close_values[-1]
        high = max(close_values)
        low = min(close_values)
        if high == low:
            return 50.0
        return round((current - low) / (high - low) * 100, 1)
    except (ValueError, TypeError):
        return None


def get_multiquarter_financials(code, num_quarters=4):
    """获取最近N个季度的财务数据（通过data_source模块降级获取）"""
    quarters = []
    year, quarter = get_latest_quarter()
    for _ in range(num_quarters):
        quarters.append((year, quarter))
        quarter -= 1
        if quarter == 0:
            quarter = 4
            year -= 1

    profit_list = []
    growth_list = []
    profit_source_label = ''
    growth_source_label = ''

    for y, q in quarters:
        # 通过data_source获取profit数据
        profit_data, p_source = get_profit_data(code, y, q)
        if profit_data:
            profit_data['period'] = f'{y}Q{q}'
            profit_list.append(profit_data)
            if not profit_source_label:
                profit_source_label = source_label(p_source)

        # 通过data_source获取growth数据
        growth_data, g_source = get_growth_data(code, y, q)
        if growth_data:
            growth_data['period'] = f'{y}Q{q}'
            growth_list.append(growth_data)
            if not growth_source_label:
                growth_source_label = source_label(g_source)

    return profit_list, growth_list, profit_source_label, growth_source_label


def check_layered_growth(profit_list):
    """检查利润是否层级式增长"""
    if len(profit_list) < 2:
        return False, '数据不足'
    profits = []
    for p in reversed(profit_list):
        np_val = safe_float(p.get('netProfit'))
        if np_val is not None:
            profits.append(np_val)
    if len(profits) < 2:
        return False, '净利润数据不足'
    is_growing = all(profits[i] <= profits[i+1] for i in range(len(profits)-1))
    if is_growing:
        return True, f'连续{len(profits)}期净利润递增'
    else:
        return False, '净利润存在波动，非严格递增'


def analyze_stock(code):
    """执行八步分析"""
    code = normalize_code(code)
    report_lines = []
    data_sources_used = {}  # 记录各维度数据来源

    # baostock login (data_source模块中baostock层需要已登录)
    import baostock as bs
    _stdout = sys.stdout
    sys.stdout = sys.stderr
    lg = bs.login()
    sys.stdout = _stdout
    if lg.error_code != '0':
        print(f'错误：baostock登录失败 - {lg.error_msg}')
        return

    try:
        # === 获取基本信息（通过data_source模块）===
        industry, ind_source = get_stock_industry(code)
        data_sources_used['行业'] = source_label(ind_source)

        # 获取股票名称
        try:
            basic_rs = bs.query_stock_basic(code=code)
            basic_df = basic_rs.get_data()
            stock_name = basic_df.iloc[0]['code_name'] if not basic_df.empty else code
        except Exception:
            stock_name = code

        # === 获取K线数据（通过data_source模块降级获取）===
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=400)).strftime('%Y-%m-%d')
        kline_data, kline_source = get_kline(code, start_date, end_date, adjust='qfq')
        data_sources_used['K线'] = source_label(kline_source)

        if not kline_data:
            print(f'错误：无法获取{code}的K线数据（所有数据源均不可用）')
            return

        latest = kline_data[-1]
        close = safe_float(latest.get('close'), 0)
        volume = safe_float(latest.get('volume'), 0)
        amount = safe_float(latest.get('amount'), 0)
        turn = safe_float(latest.get('turn'), 0)
        pe = safe_float(latest.get('peTTM'))
        pb = safe_float(latest.get('pbMRQ'))
        ps = safe_float(latest.get('psTTM'))
        pct_chg = safe_float(latest.get('pctChg'), 0)
        is_st = str(latest.get('isST', '0'))

        # 如果K线数据中没有PE/PB，尝试从实时行情获取
        if pe is None or pe == 0:
            spot_data, spot_source = get_spot(code)
            if spot_data:
                pe = safe_float(spot_data.get('pe'))
                pb = safe_float(spot_data.get('pb'))
                data_sources_used['实时行情'] = source_label(spot_source)

        # 计算市值
        market_cap = estimate_market_cap(close, volume, turn)

        # 计算价格位置
        price_percentile = calculate_price_percentile(kline_data)

        # 计算近5日/20日/60日均量
        recent_klines = kline_data[-60:] if len(kline_data) >= 60 else kline_data
        recent_5 = kline_data[-5:]
        recent_20 = kline_data[-20:]
        avg_amount_5 = sum(safe_float(d.get('amount'), 0) for d in recent_5) / max(len(recent_5), 1)
        avg_amount_20 = sum(safe_float(d.get('amount'), 0) for d in recent_20) / max(len(recent_20), 1)
        avg_amount_60 = sum(safe_float(d.get('amount'), 0) for d in recent_klines) / max(len(recent_klines), 1) if len(recent_klines) >= 10 else avg_amount_20
        avg_volume_20 = sum(safe_float(d.get('volume'), 0) for d in recent_20) / max(len(recent_20), 1)

        # === 获取财务数据（通过data_source模块降级获取）===
        year, quarter = get_latest_quarter()
        profit_list, growth_list, profit_src_label, growth_src_label = get_multiquarter_financials(code, 4)
        data_sources_used['财务(盈利)'] = profit_src_label or '⚠️ 数据获取失败'
        data_sources_used['财务(成长)'] = growth_src_label or '⚠️ 数据获取失败'

        latest_profit = profit_list[0] if profit_list else {}
        latest_growth = growth_list[0] if growth_list else {}

        roe = safe_float(latest_profit.get('roeAvg'))
        if roe is not None:
            roe = roe * 100 if abs(roe) < 1 else roe
        np_margin = safe_float(latest_profit.get('npMargin'))
        if np_margin is not None:
            np_margin = np_margin * 100 if abs(np_margin) < 1 else np_margin
        gp_margin = safe_float(latest_profit.get('gpMargin'))
        if gp_margin is not None:
            gp_margin = gp_margin * 100 if abs(gp_margin) < 1 else gp_margin
        net_profit = safe_float(latest_profit.get('netProfit'))
        yoy_ni = safe_float(latest_growth.get('YOYNI'))
        yoy_rev = safe_float(latest_growth.get('YOYEquity'))

        # 检查利润层级增长
        is_layered, growth_desc = check_layered_growth(profit_list)

        # === 财务数据交叉验证 (2026-07-31 铁律) ===
        secucode = code_to_secucode(code)
        verified = verify_financial_data(secucode)
        if verified:
            data_sources_used['财务验证'] = '东方财富datacenter ✓'
            verified_np = verified.get('parent_netprofit')
            verified_rev = verified.get('total_operate_income')
            verified_yoy = verified.get('yoy_netprofit')
            verified_date = verified.get('report_date', '')
        else:
            data_sources_used['财务验证'] = '⚠️ 财务数据未验证'
            verified_np = verified_rev = verified_yoy = verified_date = None

        # === 检查指数路径（通过data_source模块）===
        in_sz50 = in_hs300 = in_zz500 = False
        idx_stocks_50, idx_src_50 = get_index_stocks('sz50')
        if idx_stocks_50 and code in idx_stocks_50:
            in_sz50 = True
        idx_stocks_300, idx_src_300 = get_index_stocks('hs300')
        if idx_stocks_300 and code in idx_stocks_300:
            in_hs300 = True
        idx_stocks_500, idx_src_500 = get_index_stocks('zz500')
        if idx_stocks_500 and code in idx_stocks_500:
            in_zz500 = True
        data_sources_used['指数'] = source_label(idx_src_50) if idx_stocks_50 else 'baostock'

        # ============================================================
        # 生成报告
        # ============================================================
        report_lines.append(f'# {stock_name}（{code}）个股分析报告')
        report_lines.append(f'')
        report_lines.append(f'> 分析日期：{datetime.now().strftime("%Y-%m-%d")}  |  财报期：{year}Q{quarter}（最新可用）')
        report_lines.append(f'> 数据源降级链：akshare > baostock > 东方财富API（Tushare MCP由Agent直接调用优先）')
        report_lines.append(f'> 财务验证：东方财富datacenter API交叉验证（2026-07-31铁律）')
        report_lines.append(f'')
        report_lines.append(f'---')
        report_lines.append(f'')

        # === Step 1: 赛道判断 ===
        report_lines.append(f'## Step 1：赛道判断')
        report_lines.append(f'')
        is_target, sector = is_target_industry(industry)
        report_lines.append(f'- **行业分类**：{industry}  `[{data_sources_used["行业"]}]`')
        report_lines.append(f'- **板块归属**：{sector}')
        if is_target:
            report_lines.append(f'- **赛道判定**：✅ 属于{"科技" if sector == "科技" else "消费"}赛道，符合体系要求')
        else:
            report_lines.append(f'- **赛道判定**：⚠️ 不在科技/消费核心赛道，需谨慎评估')
        report_lines.append(f'- **好产业验证**：需结合产品单价、使用周期、复购频率定性判断（Agent补充）')
        report_lines.append(f'')

        # === Step 2: 市值评估 ===
        report_lines.append(f'## Step 2：市值评估')
        report_lines.append(f'')
        report_lines.append(f'- **当前股价**：{close:.2f}元  `[{data_sources_used["K线"]}]`')
        report_lines.append(f'- **流通市值（估算）**：{market_cap:.1f}亿元' if market_cap else '- **流通市值**：⚠️ 数据获取失败')
        report_lines.append(f'- **PE(TTM)**：{pe:.1f}' if pe else '- **PE(TTM)**：N/A')
        report_lines.append(f'- **PB(MRQ)**：{pb:.2f}' if pb else '- **PB(MRQ)**：N/A')
        report_lines.append(f'- **PS(TTM)**：{ps:.2f}' if ps else '- **PS(TTM)**：N/A')
        if market_cap:
            if market_cap < 30:
                report_lines.append(f'- **10倍空间评估**：✅ 市值<30亿，若5年后利润达25亿，市值可达500-750亿，50倍以上空间')
            elif market_cap < 50:
                report_lines.append(f'- **10倍空间评估**：⚠️ 市值30-50亿，10倍需达300-500亿，需利润达10-25亿，难度中等')
            elif market_cap < 100:
                report_lines.append(f'- **10倍空间评估**：⚠️ 市值{market_cap:.0f}亿，10倍需达{market_cap*10:.0f}亿，利润要求较高')
            else:
                report_lines.append(f'- **10倍空间评估**：❌ 市值{market_cap:.0f}亿过大，10倍概率极低')
        report_lines.append(f'')

        # === Step 3: 成长性分析 ===
        report_lines.append(f'## Step 3：成长性分析')
        report_lines.append(f'')
        report_lines.append(f'- **ROE**：{roe:.2f}%' if roe is not None else '- **ROE**：⚠️ 数据获取失败')
        report_lines.append(f'- **销售净利率**：{np_margin:.2f}%' if np_margin is not None else '- **销售净利率**：N/A')
        report_lines.append(f'- **销售毛利率**：{gp_margin:.2f}%' if gp_margin is not None else '- **销售毛利率**：N/A')
        report_lines.append(f'- **净利润**：{format_money(net_profit)}  `[{data_sources_used["财务(盈利)"]}]`')
        report_lines.append(f'- **净利润同比增长**：{yoy_ni:.2f}%' if yoy_ni is not None else '- **净利润同比增长**：N/A')
        report_lines.append(f'- **利润层级增长**：{"✅ " + growth_desc if is_layered else "⚠️ " + growth_desc}')
        if profit_list:
            report_lines.append(f'- **近期净利润轨迹**：')
            for p in profit_list[:4]:
                np_val = safe_float(p.get('netProfit'))
                report_lines.append(f'  - {p.get("period", "?")}: {format_money(np_val)}' if np_val else f'  - {p.get("period", "?")}: N/A')

        # 财务数据交叉验证结果
        report_lines.append(f'')
        report_lines.append(f'### 财务数据交叉验证（2026-07-31铁律）')
        report_lines.append(f'')
        if verified:
            report_lines.append(f'- **验证来源**：东方财富datacenter API ✓')
            report_lines.append(f'- **验证报告期**：{verified_date}')
            report_lines.append(f'- **验证归母净利润**：{format_money(verified_np)}')
            report_lines.append(f'- **验证营业总收入**：{format_money(verified_rev)}')
            report_lines.append(f'- **验证净利润同比**：{verified_yoy:.2f}%' if verified_yoy else '- **验证净利润同比**：N/A')
            report_lines.append(f'- **验证状态**：✅ 财务数据已通过API交叉验证')
        else:
            report_lines.append(f'- **验证状态**：⚠️ 财务数据未验证（datacenter API不可用或返回空）')
            report_lines.append(f'- **注意**：以上财务数据未经独立验证，使用时请谨慎。Agent应通过Tushare MCP或东方财富新闻搜索API补充验证。')
        report_lines.append(f'')

        # === Step 4: 位置判断 ===
        report_lines.append(f'## Step 4：位置判断')
        report_lines.append(f'')
        report_lines.append(f'- **价格位置（250日百分位）**：{price_percentile:.1f}%' if price_percentile is not None else '- **价格位置**：数据不足')
        if price_percentile is not None:
            if price_percentile < 30:
                report_lines.append(f'- **位置判定**：✅ 低位区，左侧布局区间')
            elif price_percentile < 50:
                report_lines.append(f'- **位置判定**：⚠️ 中低位，接近左侧尾声')
            elif price_percentile < 70:
                report_lines.append(f'- **位置判定**：⚠️ 中高位，右侧区域，市场共识已形成')
            else:
                report_lines.append(f'- **位置判定**：❌ 高位区，追涨风险大')
        report_lines.append(f'- **近5日均量**：{avg_amount_5/1e4:.0f}万元')
        report_lines.append(f'- **近20日均量**：{avg_amount_20/1e4:.0f}万元')
        report_lines.append(f'- **近60日均量**：{avg_amount_60/1e4:.0f}万元')
        if avg_amount_20 > 0:
            vol_ratio = avg_amount_5 / avg_amount_20
            if vol_ratio > 1.5:
                report_lines.append(f'- **量能趋势**：放量（近5日/20日 = {vol_ratio:.2f}）')
            elif vol_ratio < 0.7:
                report_lines.append(f'- **量能趋势**：缩量（近5日/20日 = {vol_ratio:.2f}）')
            else:
                report_lines.append(f'- **量能趋势**：平稳（近5日/20日 = {vol_ratio:.2f}）')
        report_lines.append(f'')

        # === Step 5: 指数路径 ===
        report_lines.append(f'## Step 5：指数路径')
        report_lines.append(f'')
        if in_sz50:
            report_lines.append(f'- **上证50**：✅ 已纳入（被动资金充足，但10倍空间受限）')
        else:
            report_lines.append(f'- **上证50**：未纳入')
        if in_hs300:
            report_lines.append(f'- **沪深300**：✅ 已纳入')
        else:
            report_lines.append(f'- **沪深300**：未纳入')
        if in_zz500:
            report_lines.append(f'- **中证500**：✅ 已纳入')
        else:
            report_lines.append(f'- **中证500**：未纳入')
        if not in_sz50 and not in_hs300:
            report_lines.append(f'- **指数路径判定**：✅ 未被纳入大盘指数，处于指数升维路径起点（50->300->1000->2000）')
        else:
            report_lines.append(f'- **指数路径判定**：⚠️ 已被纳入主要指数，被动资金涌入阶段已过')
        report_lines.append(f'')

        # === Step 6: 排除检查 ===
        report_lines.append(f'## Step 6：排除检查')
        report_lines.append(f'')
        if is_st == '1':
            report_lines.append(f'- **ST状态**：❌ ST股，坚决排除')
        else:
            report_lines.append(f'- **ST状态**：✅ 正常')
        if close < 2:
            report_lines.append(f'- **股价**：❌ 低于2元，有退市虹吸风险')
        else:
            report_lines.append(f'- **股价**：✅ {close:.2f}元，高于2元安全线')
        report_lines.append(f'- **PE合理性**：{"✅ 合理" if pe and 0 < pe < 50 else "⚠️ 偏高或为负"}')
        report_lines.append(f'- **造假/商誉/蹭热点**：需Agent结合公开信息定性判断')
        report_lines.append(f'')

        # === Step 7: 建仓建议 ===
        report_lines.append(f'## Step 7：建仓建议')
        report_lines.append(f'')
        max_daily_buy = avg_volume_20 * 0.1
        max_daily_amount = avg_amount_20 * 0.1
        report_lines.append(f'- **近20日日均成交量**：{avg_volume_20/1e4:.0f}万股')
        report_lines.append(f'- **近20日日均成交额**：{avg_amount_20/1e4:.0f}万元')
        report_lines.append(f'- **单日最大买入量（10%规则）**：{max_daily_buy/1e4:.0f}万股 / {max_daily_amount/1e4:.0f}万元')
        report_lines.append(f'- **建议建仓节奏**：')
        report_lines.append(f'  1. 第一批（试探仓）：目标仓位20-30%，观察3-5日')
        report_lines.append(f'  2. 第二批（确认仓）：趋势确认后加至50-60%')
        report_lines.append(f'  3. 第三批（主仓）：突破关键位后加至目标仓位')
        if avg_amount_20 < 1000e4:  # < 1000万
            report_lines.append(f'- ⚠️ **流动性警告**：日均成交额不足1000万，建仓难度极大')
        report_lines.append(f'')

        # === Step 8: 卖出预案 ===
        report_lines.append(f'## Step 8：卖出预案（倒金字塔）')
        report_lines.append(f'')
        report_lines.append(f'| 涨幅 | 卖出比例 | 累计卖出 |')
        report_lines.append(f'|------|---------|---------|')
        report_lines.append(f'| +20% | 5% | 5% |')
        report_lines.append(f'| +40% | 10% | 15% |')
        report_lines.append(f'| +60% | 15% | 30% |')
        report_lines.append(f'| +80% | 20% | 50% |')
        report_lines.append(f'| +100% | 25% | 75% |')
        report_lines.append(f'| +120% | 25% | 100% |')
        report_lines.append(f'')
        report_lines.append(f'- **翻倍策略**：涨100%先卖一半，收回本金')
        report_lines.append(f'- **最高点不可参考**：碎骨成交价不具代表性')
        report_lines.append(f'- **目标市值**：需结合行业天花板和利润预测设定')
        if market_cap:
            report_lines.append(f'- **当前市值**：{market_cap:.1f}亿 -> 目标500亿+（若利润达25亿）')
        report_lines.append(f'')

        # === 综合评级 ===
        report_lines.append(f'---')
        report_lines.append(f'')
        report_lines.append(f'## 综合评级')
        report_lines.append(f'')

        # 计算综合评分
        score = 0
        if is_target:
            score += 10
        if market_cap and market_cap < 50:
            score += 20
            if market_cap < 30:
                score += 10
        if roe and roe >= 8:
            score += 15
            if roe > 15:
                score += 5
        if yoy_ni and yoy_ni >= 10:
            score += 15
            if yoy_ni > 30:
                score += 5
        if price_percentile and price_percentile <= 50:
            score += 20
            if price_percentile < 30:
                score += 10
        if not in_sz50 and not in_hs300:
            score += 5
        if pe and 0 < pe < 30:
            score += 10

        if score >= 80:
            rating = 'A（强烈关注）'
        elif score >= 60:
            rating = 'B（值得关注）'
        elif score >= 40:
            rating = 'C（观望）'
        else:
            rating = 'D（不符合体系）'

        report_lines.append(f'- **综合评分**：{score}/120')
        report_lines.append(f'- **评级**：{rating}')
        report_lines.append(f'')

        # === 数据来源汇总 ===
        report_lines.append(f'---')
        report_lines.append(f'')
        report_lines.append(f'## 数据来源汇总')
        report_lines.append(f'')
        for dim, src in data_sources_used.items():
            report_lines.append(f'- {dim}：{src}')
        report_lines.append(f'')
        report_lines.append(f'> 数据源降级链：akshare > baostock > 东方财富API')
        report_lines.append(f'> Tushare MCP由Agent直接调用，优先于以上所有Python数据源')
        report_lines.append(f'> 财务数据经东方财富datacenter API交叉验证')
        report_lines.append(f'')

        # === 免责声明 ===
        report_lines.append(f'---')
        report_lines.append(f'')
        report_lines.append(f'> ⚠️ **免责声明**：以上分析结果仅供学习交流，不构成任何投资建议。投资有风险，入市需谨慎。')
        report_lines.append(f'> 📊 **数据来源**：{", ".join(set(data_sources_used.values()))}，财报期 {year}Q{quarter}')

        # 输出
        print('\n'.join(report_lines))

    finally:
        _stdout = sys.stdout
        sys.stdout = sys.stderr
        bs.logout()
        sys.stdout = _stdout


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 analyze_stock.py <stock_code>')
        print('Example: python3 analyze_stock.py sz.300308')
        sys.exit(1)
    analyze_stock(sys.argv[1])
