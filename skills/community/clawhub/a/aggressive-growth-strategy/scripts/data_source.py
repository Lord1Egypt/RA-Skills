"""
aggressive_growth_strategy 共享数据源模块
==========================================
四层降级架构: akshare > baostock > 东方财富API
(Tushare MCP 由 Agent 直接调用，不在此模块中)

数据校验铁律:
  - 严禁编造任何具体数值
  - 数据获取失败时必须如实标注"数据获取失败"
  - 所有输出必须标注实际数据来源
  - 财务数据必须通过东方财富datacenter API交叉验证
"""

import json
import subprocess
import sys
import time
import os

# ============================================================
# 数据源优先级常量
# ============================================================
SOURCE_AKSHARE = 'akshare'
SOURCE_BAOSTOCK = 'baostock'
SOURCE_EASTMONEY = 'eastmoney_api'
SOURCE_FAILED = 'failed'

# venv python 路径
VENV_PYTHON = '/home/ubuntu/.hermes/hermes-agent/venv/bin/python3'

# ============================================================
# 工具函数
# ============================================================

def _code_to_akshare(code):
    """baostock代码 -> akshare代码 (sz.300308 -> 300308)"""
    return code.replace('sh.', '').replace('sz.', '')

def _code_to_eastmoney_secid(code):
    """baostock代码 -> 东方财富secid (sz.300308 -> 0.300308, sh.600000 -> 1.600000)"""
    if code.startswith('sh.'):
        return f"1.{code[3:]}"
    elif code.startswith('sz.'):
        return f"0.{code[3:]}"
    return f"0.{code}"

def _curl_json(url, timeout=15, retries=3):
    """通过curl获取JSON，带重试"""
    for attempt in range(retries):
        try:
            result = subprocess.run(
                ['curl', '-sL', '--connect-timeout', '10', '--max-time', str(timeout), url],
                capture_output=True, text=True, timeout=timeout + 5
            )
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
        except (json.JSONDecodeError, subprocess.TimeoutExpired, Exception) as e:
            if attempt < retries - 1:
                time.sleep(0.5 * (attempt + 1))
    return None

# ============================================================
# 日K线数据获取
# ============================================================

def get_kline(code, start_date, end_date, adjust='qfq'):
    """
    获取日K线数据，多源降级
    
    参数:
        code: baostock格式代码 (如 sz.300308)
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        adjust: qfq前复权/hfq后复权/不复权
    
    返回: (data_list, source)
        data_list: [{'date': ..., 'open': ..., 'high': ..., 'low': ..., 'close': ..., 'volume': ..., 'turn': ...}, ...]
        source: 'akshare' / 'baostock' / 'eastmoney_api' / 'failed'
    """
    # ---- 第1层: akshare ----
    try:
        import akshare as ak
        ak_code = _code_to_akshare(code)
        adjust_map = {'qfq': 'qfq', 'hfq': 'hfq', '不复权': ''}
        adj = adjust_map.get(adjust, 'qfq')
        df = ak.stock_zh_a_hist(
            symbol=ak_code,
            period='daily',
            start_date=start_date.replace('-', ''),
            end_date=end_date.replace('-', ''),
            adjust=adj
        )
        if df is not None and len(df) > 0:
            data_list = []
            for _, row in df.iterrows():
                data_list.append({
                    'date': str(row.get('日期', '')),
                    'open': float(row.get('开盘', 0)),
                    'high': float(row.get('最高', 0)),
                    'low': float(row.get('最低', 0)),
                    'close': float(row.get('收盘', 0)),
                    'volume': float(row.get('成交量', 0)),
                    'amount': float(row.get('成交额', 0)),
                    'turn': float(row.get('换手率', 0)) if '换手率' in row else 0.0,
                    'pctChg': float(row.get('涨跌幅', 0)) if '涨跌幅' in row else 0.0,
                    'isST': 0
                })
            return data_list, SOURCE_AKSHARE
    except Exception as e:
        print(f"[数据源降级] akshare K线获取失败({code}): {e}", file=sys.stderr)
    
    # ---- 第2层: baostock ----
    try:
        import baostock as bs
        # 调用方负责login/logout，这里假设已登录或自行登录
        need_logout = False
        try:
            # 尝试查询，如果未登录会抛异常
            bs_query = bs.query_history_k_data_plus(
                code,
                "date,open,high,low,close,volume,amount,turn,pctChg,isST,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="2" if adjust == 'qfq' else ("1" if adjust == 'hfq' else "3")
            )
            data_list = []
            while (bs_query.error_code == '0') and bs_query.next():
                row = bs_query.get_row_data()
                data_list.append({
                    'date': row[0],
                    'open': float(row[1]) if row[1] else 0.0,
                    'high': float(row[2]) if row[2] else 0.0,
                    'low': float(row[3]) if row[3] else 0.0,
                    'close': float(row[4]) if row[4] else 0.0,
                    'volume': float(row[5]) if row[5] else 0.0,
                    'amount': float(row[6]) if row[6] else 0.0,
                    'turn': float(row[7]) if row[7] else 0.0,
                    'pctChg': float(row[8]) if row[8] else 0.0,
                    'isST': int(float(row[9])) if row[9] else 0,
                    'peTTM': float(row[10]) if row[10] else 0.0,
                    'pbMRQ': float(row[11]) if row[11] else 0.0,
                    'psTTM': float(row[12]) if row[12] else 0.0
                })
            if data_list:
                return data_list, SOURCE_BAOSTOCK
        except Exception:
            pass
    except Exception as e:
        print(f"[数据源降级] baostock K线获取失败({code}): {e}", file=sys.stderr)
    
    # ---- 第3层: 东方财富历史K线API ----
    try:
        secid = _code_to_eastmoney_secid(code)
        beg = start_date.replace('-', '')
        end = end_date.replace('-', '')
        url = (f"https://push2his.eastmoney.com/api/qt/stock/kline/get?"
               f"secid={secid}&fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56,f57"
               f"&klt=101&fqt={'1' if adjust == 'qfq' else '2' if adjust == 'hfq' else '0'}"
               f"&beg={beg}&end={end}")
        data = _curl_json(url)
        if data and data.get('data') and data['data'].get('klines'):
            data_list = []
            for kline in data['data']['klines']:
                parts = kline.split(',')
                if len(parts) >= 6:
                    data_list.append({
                        'date': parts[0],
                        'open': float(parts[1]) if parts[1] else 0.0,
                        'close': float(parts[2]) if parts[2] else 0.0,
                        'high': float(parts[3]) if parts[3] else 0.0,
                        'low': float(parts[4]) if parts[4] else 0.0,
                        'volume': float(parts[5]) if parts[5] else 0.0,
                        'amount': float(parts[6]) if len(parts) > 6 and parts[6] else 0.0,
                        'turn': 0.0,
                        'pctChg': 0.0,
                        'isST': 0
                    })
            if data_list:
                return data_list, SOURCE_EASTMONEY
    except Exception as e:
        print(f"[数据源降级] 东方财富API K线获取失败({code}): {e}", file=sys.stderr)
    
    # ---- 全部失败 ----
    return [], SOURCE_FAILED

# ============================================================
# 实时行情获取
# ============================================================

def get_spot(code):
    """
    获取实时行情快照
    
    返回: (spot_dict, source)
        spot_dict: {'close': ..., 'open': ..., 'high': ..., 'low': ..., 'pre_close': ...,
                    'volume': ..., 'amount': ..., 'pe': ..., 'pb': ..., 'total_mv': ..., 'turnover': ...}
        source: 'akshare' / 'eastmoney_api' / 'failed'
    """
    # ---- 第1层: akshare ----
    try:
        import akshare as ak
        ak_code = _code_to_akshare(code)
        df = ak.stock_zh_a_spot_em(symbol=ak_code)
        if df is not None and len(df) > 0:
            row = df.iloc[0]
            return {
                'close': float(row.get('最新价', 0)),
                'open': float(row.get('今开', 0)),
                'high': float(row.get('最高', 0)),
                'low': float(row.get('最低', 0)),
                'pre_close': float(row.get('昨收', 0)),
                'volume': float(row.get('成交量', 0)),
                'amount': float(row.get('成交额', 0)),
                'pe': float(row.get('市盈率-动态', 0)),
                'pb': float(row.get('市净率', 0)),
                'total_mv': float(row.get('总市值', 0)),
                'circ_mv': float(row.get('流通市值', 0)),
                'turnover': float(row.get('换手率', 0)),
                'pctChg': float(row.get('涨跌幅', 0)),
                'name': str(row.get('名称', ''))
            }, SOURCE_AKSHARE
    except Exception as e:
        print(f"[数据源降级] akshare实时行情获取失败({code}): {e}", file=sys.stderr)
    
    # ---- 第2层: 东方财富Push API ----
    try:
        secid = _code_to_eastmoney_secid(code)
        url = (f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}"
               f"&fields=f43,f44,f45,f46,f47,f48,f50,f57,f58,f60,f116,f117,f162,f167,f170,f171")
        data = _curl_json(url)
        if data and data.get('data'):
            d = data['data']
            return {
                'close': d.get('f43', 0),
                'high': d.get('f44', 0),
                'low': d.get('f45', 0),
                'open': d.get('f46', 0),
                'volume': d.get('f47', 0),
                'amount': d.get('f48', 0),
                'volume_ratio': d.get('f50', 0),
                'code': d.get('f57', ''),
                'name': d.get('f58', ''),
                'pre_close': d.get('f60', 0),
                'total_mv': d.get('f116', 0),
                'circ_mv': d.get('f117', 0),
                'pe': d.get('f162', 0),
                'pb': d.get('f167', 0),
                'turnover': d.get('f170', 0),
                'pctChg': d.get('f171', 0)
            }, SOURCE_EASTMONEY
    except Exception as e:
        print(f"[数据源降级] 东方财富API实时行情获取失败({code}): {e}", file=sys.stderr)
    
    return {}, SOURCE_FAILED

# ============================================================
# 财务数据获取
# ============================================================

def get_profit_data(code, year, quarter):
    """
    获取盈利能力数据，多源降级
    
    参数:
        code: baostock格式 (如 sz.300308)
        year: 年份 (如 2025)
        quarter: 季度 (1-4)
    
    返回: (profit_dict, source)
    """
    # ---- 第1层: akshare (同花顺财务摘要) ----
    try:
        import akshare as ak
        ak_code = _code_to_akshare(code)
        df = ak.stock_financial_abstract_ths(symbol=ak_code, indicator="按报告期")
        if df is not None and len(df) > 0:
            # 取最近的报告期
            latest = df.iloc[-1] if len(df) > 0 else None
            if latest is not None:
                return {
                    'roeAvg': float(latest.get('加权净资产收益率', 0)) if latest.get('加权净资产收益率') else 0.0,
                    'npMargin': float(latest.get('销售净利率', 0)) if latest.get('销售净利率') else 0.0,
                    'gpMargin': float(latest.get('销售毛利率', 0)) if latest.get('销售毛利率') else 0.0,
                    'netProfit': float(latest.get('净利润', 0)) if latest.get('净利润') else 0.0,
                    'yaoyNit': float(latest.get('净利润同比增长率', 0)) if latest.get('净利润同比增长率') else 0.0,
                }, SOURCE_AKSHARE
    except Exception as e:
        print(f"[数据源降级] akshare财务数据获取失败({code}): {e}", file=sys.stderr)
    
    # ---- 第2层: baostock ----
    try:
        import baostock as bs
        rs = bs.query_profit_data(code=code, year=year, quarter=quarter)
        data_list = []
        while (rs.error_code == '0') and rs.next():
            data_list.append(rs.get_row_data())
        if data_list:
            row = data_list[0]
            return {
                'roeAvg': float(row[0]) if row[0] else 0.0,
                'npMargin': float(row[1]) if row[1] else 0.0,
                'gpMargin': float(row[2]) if row[2] else 0.0,
                'netProfit': float(row[3]) if row[3] else 0.0,
                'epsTTM': float(row[4]) if len(row) > 4 and row[4] else 0.0,
                'MBRevenue': float(row[5]) if len(row) > 5 and row[5] else 0.0,
                'totalShare': float(row[6]) if len(row) > 6 and row[6] else 0.0,
                'liqaShare': float(row[7]) if len(row) > 7 and row[7] else 0.0,
            }, SOURCE_BAOSTOCK
    except Exception as e:
        print(f"[数据源降级] baostock财务数据获取失败({code}): {e}", file=sys.stderr)
    
    return {}, SOURCE_FAILED

def get_growth_data(code, year, quarter):
    """
    获取成长能力数据，多源降级
    
    返回: (growth_dict, source)
    """
    # ---- 第1层: baostock (成长能力接口稳定) ----
    try:
        import baostock as bs
        rs = bs.query_growth_data(code=code, year=year, quarter=quarter)
        data_list = []
        while (rs.error_code == '0') and rs.next():
            data_list.append(rs.get_row_data())
        if data_list:
            row = data_list[0]
            return {
                'YOYEquity': float(row[0]) if row[0] else 0.0,
                'YOYAsset': float(row[1]) if row[1] else 0.0,
                'YOYNI': float(row[2]) if row[2] else 0.0,
                'YOYEPSBasic': float(row[3]) if row[3] else 0.0,
                'YOYPNI': float(row[4]) if len(row) > 4 and row[4] else 0.0,
            }, SOURCE_BAOSTOCK
    except Exception as e:
        print(f"[数据源降级] baostock成长数据获取失败({code}): {e}", file=sys.stderr)
    
    return {}, SOURCE_FAILED

# ============================================================
# 财务数据交叉验证（铁律要求）
# ============================================================

def verify_financial_data(secucode):
    """
    通过东方财富datacenter API交叉验证财务数据
    （2026-07-31 财务数据验证铁律要求）
    
    参数:
        secucode: 证券代码，格式如 "300769.SZ" 或 "600000.SH"
    
    返回: dict 或 None
        {
            'report_date': 'YYYY-MM-DD',
            'parent_netprofit': float,  # 归母净利润
            'total_operate_income': float,  # 营业总收入
            'operate_profit': float,  # 营业利润
            'yoy_netprofit': float,  # 净利润同比
            'yoy_sales': float,  # 营收同比
            'source': 'eastmoney_datacenter'
        }
    """
    try:
        url = (
            f"https://datacenter-web.eastmoney.com/api/data/v1/get?"
            f"sortColumns=REPORTDATE&sortTypes=-1&pageSize=10&pageNumber=1"
            f"&reportName=RPT_LICO_FN_CPD&columns=ALL"
            f"&filter=(SECUCODE%3D%22{secucode}%22)"
        )
        data = _curl_json(url, timeout=15)
        if data and data.get('result') and data['result'].get('data'):
            records = data['result']['data']
            if records:
                latest = records[0]
                return {
                    'report_date': str(latest.get('REPORTDATE', ''))[:10],
                    'parent_netprofit': float(latest.get('PARENT_NETPROFIT', 0) or 0),
                    'total_operate_income': float(latest.get('TOTAL_OPERATE_INCOME', 0) or 0),
                    'operate_profit': float(latest.get('OPERATE_PROFIT', 0) or 0),
                    'yoy_netprofit': float(latest.get('PARENT_NETPROFIT_YOY', 0) or 0),
                    'yoy_sales': float(latest.get('TOTAL_OPERATE_INCOME_YOY', 0) or 0),
                    'source': 'eastmoney_datacenter'
                }
    except Exception as e:
        print(f"[财务验证] 东方财富datacenter验证失败({secucode}): {e}", file=sys.stderr)
    
    return None

# ============================================================
# 股票列表获取
# ============================================================

def get_stock_list():
    """
    获取全A股股票列表，多源降级
    
    返回: (stock_list, source)
        stock_list: [{'code': 'sz.300308', 'code_name': '中际旭创'}, ...]
    """
    # ---- 第1层: baostock ----
    try:
        import baostock as bs
        rs = bs.query_stock_basic()
        stocks = []
        while (rs.error_code == '0') and rs.next():
            row = rs.get_row_data()
            # code, code_name, ipoDate, outDate, type, status
            if row[4] == '1' and row[5] == '1':  # 股票且在市
                stocks.append({
                    'code': row[0],
                    'code_name': row[1],
                    'ipoDate': row[2],
                })
        if stocks:
            return stocks, SOURCE_BAOSTOCK
    except Exception as e:
        print(f"[数据源降级] baostock股票列表获取失败: {e}", file=sys.stderr)
    
    # ---- 第2层: akshare ----
    try:
        import akshare as ak
        df = ak.stock_info_a_code_name()
        if df is not None and len(df) > 0:
            stocks = []
            for _, row in df.iterrows():
                code = str(row.get('code', ''))
                # 推断baostock格式
                if code.startswith('6'):
                    bs_code = f'sh.{code}'
                else:
                    bs_code = f'sz.{code}'
                stocks.append({
                    'code': bs_code,
                    'code_name': str(row.get('name', '')),
                })
            return stocks, SOURCE_AKSHARE
    except Exception as e:
        print(f"[数据源降级] akshare股票列表获取失败: {e}", file=sys.stderr)
    
    return [], SOURCE_FAILED

# ============================================================
# 指数数据获取
# ============================================================

def get_index_kline(code, start_date, end_date):
    """
    获取指数K线数据，多源降级
    
    参数:
        code: 指数代码 (如 sh.000001 上证综指)
    
    返回: (data_list, source)
    """
    # ---- 第1层: baostock ----
    try:
        import baostock as bs
        rs = bs.query_history_k_data_plus(
            code,
            "date,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency="d"
        )
        data_list = []
        while (rs.error_code == '0') and rs.next():
            row = rs.get_row_data()
            data_list.append({
                'date': row[0],
                'open': float(row[1]) if row[1] else 0.0,
                'high': float(row[2]) if row[2] else 0.0,
                'low': float(row[3]) if row[3] else 0.0,
                'close': float(row[4]) if row[4] else 0.0,
                'volume': float(row[5]) if row[5] else 0.0,
                'amount': float(row[6]) if row[6] else 0.0,
            })
        if data_list:
            return data_list, SOURCE_BAOSTOCK
    except Exception as e:
        print(f"[数据源降级] baostock指数K线获取失败({code}): {e}", file=sys.stderr)
    
    return [], SOURCE_FAILED

# ============================================================
# 行业分类获取
# ============================================================

def get_stock_industry(code):
    """
    获取股票行业分类
    
    返回: (industry_str, source)
    """
    # ---- 第1层: baostock ----
    try:
        import baostock as bs
        rs = bs.query_stock_industry(code=code)
        while (rs.error_code == '0') and rs.next():
            row = rs.get_row_data()
            # updateDate, code, code_name, industry, industryClassification
            return row[3], SOURCE_BAOSTOCK  # industry
    except Exception as e:
        print(f"[数据源降级] baostock行业获取失败({code}): {e}", file=sys.stderr)
    
    return '未知', SOURCE_FAILED

# ============================================================
# 指数成分股获取
# ============================================================

def get_index_stocks(index_code):
    """
    获取指数成分股列表
    
    参数:
        index_code: 'sz50' / 'hs300' / 'zz500'
    
    返回: (stock_codes_list, source)
    """
    # ---- 第1层: baostock ----
    try:
        import baostock as bs
        if index_code == 'sz50':
            rs = bs.query_sz50_stocks()
        elif index_code == 'hs300':
            rs = bs.query_hs300_stocks()
        elif index_code == 'zz500':
            rs = bs.query_zz500_stocks()
        else:
            return [], SOURCE_FAILED
        
        stocks = []
        while (rs.error_code == '0') and rs.next():
            row = rs.get_row_data()
            stocks.append(row[1])  # code
        if stocks:
            return stocks, SOURCE_BAOSTOCK
    except Exception as e:
        print(f"[数据源降级] baostock指数成分股获取失败({index_code}): {e}", file=sys.stderr)
    
    return [], SOURCE_FAILED

# ============================================================
# 数据源标签输出
# ============================================================

def source_label(source):
    """返回数据源的中文标签"""
    labels = {
        SOURCE_AKSHARE: 'akshare',
        SOURCE_BAOSTOCK: 'baostock',
        SOURCE_EASTMONEY: '东方财富API',
        SOURCE_FAILED: '⚠️ 数据获取失败'
    }
    return labels.get(source, source)

def format_data_source_line(source, extra=''):
    """格式化数据来源标注行"""
    label = source_label(source)
    if source == SOURCE_FAILED:
        return f"> ⚠️ **数据来源**：{label}。{extra}" if extra else f"> ⚠️ **数据来源**：{label}"
    else:
        return f"> 📊 **数据来源**：{label}。{extra}" if extra else f"> 📊 **数据来源**：{label}"

# ============================================================
# 自检
# ============================================================

if __name__ == '__main__':
    print("data_source.py 模块自检")
    print(f"VENV_PYTHON: {VENV_PYTHON}")
    print(f"可用数据源: akshare > baostock > 东方财富API")
    
    # 测试东方财富API可达性
    test_code = 'sz.300308'
    secid = _code_to_eastmoney_secid(test_code)
    print(f"代码映射测试: {test_code} -> secid={secid}")
    
    # 测试财务数据验证API
    print("\n测试财务数据验证API (300769.SZ):")
    result = verify_financial_data('300769.SZ')
    if result:
        print(f"  报告期: {result['report_date']}")
        print(f"  归母净利润: {result['parent_netprofit']}")
        print(f"  营业总收入: {result['total_operate_income']}")
        print(f"  净利润同比: {result['yoy_netprofit']}%")
        print(f"  来源: {result['source']}")
    else:
        print("  ⚠️ 验证API不可用或返回空")
    
    print("\n模块加载成功 ✓")
