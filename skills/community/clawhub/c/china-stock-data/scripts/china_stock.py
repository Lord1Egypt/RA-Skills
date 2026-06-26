#!/usr/bin/env python3
"""
China Stock Data - 综合数据源
集成了5大数据源，自动降级：
1. 通达信(TDX)  — 实时行情、K线、5档盘口、逐笔成交
2. 腾讯财经     — PE/PB/市值/换手率等财务数据
3. 同花顺(iFinD)— 专业行情、公告、股息率、热点题材
4. AKShare     — 研报、公告、资金流向、补充数据
5. iWencai(问财)— 语义搜索选股（需API Key）
"""
import json, sys, os, time, re
from datetime import datetime, timedelta

PY = os.path.realpath(__file__)
DIR = os.path.dirname(os.path.dirname(PY))

try: import requests
except ImportError:
    print(json.dumps({"error":"缺少requests","fix":"pip install requests"},ensure_ascii=False)); sys.exit(1)

# ============================================================
# 1. 通达讯 TDX - pytdx
# ============================================================
TDX_OK = False
TDX_API = None
_LAST_TDX_TIME = 0  # 全局TDX限速时间戳

try:
    from pytdx.hq import TdxHq_API as _TdxAPI
    TDX_OK = True
    # 可用的TDX服务器列表 (name, ip, port)
    TDX_HOSTS = [
        ('上证云成都电信一', '218.6.170.47', 7709),
        ('上证云北京联通一', '123.125.108.14', 7709),
        ('上海电信主站Z1', '180.153.18.170', 7709),
        ('杭州电信主站J1', '60.191.117.167', 7709),
    ]
    _TDX_HOST_IDX = 0
    # 市场代码: 0=深圳, 1=上海
except ImportError:
    pass

def tdx_throttle():
    """全局TDX限速：每次调用至少间隔0.5秒，防止被封IP"""
    global _LAST_TDX_TIME
    elapsed = time.time() - _LAST_TDX_TIME
    if elapsed < 0.5:
        time.sleep(round(0.5 - elapsed + __import__('random').random() * 0.2, 3))
    _LAST_TDX_TIME = time.time()
    pass

def tdx_connect():
    """连接TDX服务器（限速+轮询多IP）"""
    global _TDX_HOST_IDX
    if not TDX_OK: return None
    tdx_throttle()
    for _ in range(len(TDX_HOSTS)):
        name, ip, port = TDX_HOSTS[_TDX_HOST_IDX % len(TDX_HOSTS)]
        _TDX_HOST_IDX += 1
        api = _TdxAPI()
        try:
            api.connect(ip, port, time_out=3)
            return api
        except:
            try: api.disconnect()
            except: pass
    return None

def tdx_market(code):
    """判断市场代码: 0=深圳, 1=上海"""
    code = code.replace('.SH','').replace('.SZ','').replace('sh','').replace('sz','')
    if code.startswith('6') or code.startswith('9'):
        return 1  # 上海
    elif code.startswith('0') or code.startswith('3') or code.startswith('2'):
        return 0  # 深圳
    elif code.startswith('5'):
        return 0
    return 1

def tdx_quote(code):
    """通达讯实时行情"""
    api = tdx_connect()
    if not api: return None
    try:
        m = tdx_market(code)
        code_clean = re.sub(r'[^0-9]','', code)
        data = api.get_security_quotes([(m, code_clean)])
        if not data: return None
        d = data[0]
        change = d['price'] - d['last_close']
        change_pct = (change / d['last_close'] * 100) if d['last_close'] else 0
        return {
            'source': '通达讯',
            'code': code_clean,
            'name': '',
            'price': d['price'],
            'open': d['open'],
            'high': d['high'],
            'low': d['low'],
            'last_close': d['last_close'],
            'change': round(change, 2),
            'change_pct': round(change_pct, 2),
            'volume': d['vol'],
            'amount': d['amount'],
            'bid': [{'p': d[f'bid{i}'], 'v': d[f'bid_vol{i}']} for i in range(1,6)],
            'ask': [{'p': d[f'ask{i}'], 'v': d[f'ask_vol{i}']} for i in range(1,6)],
            'time': d.get('servertime', ''),
        }
    finally:
        api.disconnect()

def tdx_kline(code, period='daily', count=30):
    """通达讯K线"""
    api = tdx_connect()
    if not api: return None
    try:
        m = tdx_market(code)
        code_clean = re.sub(r'[^0-9]','', code)
        cat = {'daily':9, 'weekly':5, 'monthly':6, '60min':3, '30min':2, '15min':1, '5min':0}.get(period, 9)
        bars = api.get_security_bars(cat, m, code_clean, 0, count)
        if not bars: return None
        result = []
        for b in bars:
            result.append({
                'date': str(b.get('datetime','')),
                'open': b.get('open'),
                'high': b.get('high'),
                'low': b.get('low'),
                'close': b.get('close'),
                'volume': b.get('vol'),
                'amount': b.get('amount'),
            })
        return {'source':'通达讯','code':code_clean,'period':period,'bars':result}
    finally:
        api.disconnect()

# ============================================================
# 2. 腾讯财经 - qt.gtimg.cn
# ============================================================
def tencent_quote(code):
    """腾讯财经实时行情（含PE/PB/市值/换手率）"""
    code = code.replace('.SH','').replace('.SZ','').replace('sh','').replace('sz','SZ').replace('sh','SH')
    if code.isdigit():
        # 自动判断前缀
        if code.startswith('6'):
            prefix = 'sh'
        elif code.startswith('0') or code.startswith('3'):
            prefix = 'sz'
        elif code.startswith('5'):
            prefix = 'sh'
        else:
            prefix = 'sz'
        qcode = f"{prefix}{code}"
    else:
        qcode = code

    try:
        resp = requests.get(f'https://qt.gtimg.cn/q={qcode}', timeout=10,
                           headers={'User-Agent': 'Mozilla/5.0'})
        match = re.search(r'\"(.*?)\"', resp.text)
        if not match: return None
        f = match.group(1).split('~')
        if len(f) < 46: return None
        # Fields: 0=market,1=name,2=code,3=price,4=last_close,5=open,
        # 6=volume(手),7=amount,8~19=bids,20~31=asks,
        # 31=change,32=change%,33=high,34=low,
        # 38=turnover%,39=PE,44=流通市值,45=总市值
        change = float(f[31]) if f[31] else 0
        lc = float(f[4]) if f[4] else 0
        change_pct = float(f[32]) if f[32] else (change/lc*100 if lc else 0)
        return {
            'source': '腾讯财经',
            'code': f[2],
            'name': f[1],
            'price': float(f[3]) if f[3] else 0,
            'open': float(f[5]) if f[5] else 0,
            'high': float(f[33]) if f[33] else 0,
            'low': float(f[34]) if f[34] else 0,
            'last_close': lc,
            'change': round(change, 2),
            'change_pct': round(change_pct, 2),
            'volume': int(float(f[6])) if f[6] else 0,
            'amount': float(f[7]) if f[7] else 0,
            'turnover_rate': float(f[38]) if f[38] else 0,
            'pe': float(f[39]) if f[39] else 0,
            'market_cap': float(f[45]) if f[45] else 0,
            'circulating_cap': float(f[44]) if f[44] else 0,
            'time': f[30] if len(f) > 30 else '',
        }
    except Exception as e:
        return {'source':'腾讯财经','error':str(e)}

def tencent_batch_quote(codes):
    """批量查询腾讯财经行情"""
    qcodes = []
    for code in codes:
        c = code.replace('.SH','').replace('.SZ','').replace('sh','').replace('sz','')
        if c.startswith('6'): qcodes.append(f'sh{c}')
        elif c.startswith('0') or c.startswith('3'): qcodes.append(f'sz{c}')
        elif c.startswith('5'): qcodes.append(f'sh{c}')
        else: qcodes.append(f'sz{c}')
    try:
        url = 'https://qt.gtimg.cn/q=' + ','.join(qcodes)
        resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        results = []
        for m in re.finditer(r'\"(.*?)\"', resp.text):
            f = m.group(1).split('~')
            if len(f) >= 46:
                results.append({
                    'code': f[2], 'name': f[1], 'price': float(f[3]) if f[3] else 0,
                    'change_pct': float(f[32]) if f[32] else 0,
                    'pe': float(f[39]) if f[39] else 0,
                })
        return results
    except: return []

# ============================================================
# 3. 同花顺 iFinD HTTP API (复用现有逻辑)
# ============================================================
CFG = os.path.join(os.path.dirname(DIR), 'tonghuashun', 'ifind_config.json')
IF = {}
if os.path.exists(CFG):
    try:
        with open(CFG) as f: IF = json.load(f)
    except: pass
IFIND_URL = "https://quantapi.51ifind.com/api/v1"
IFIND_OK = bool(IF.get("access_token") or IF.get("refresh_token"))

def ifind_api(ep, params, retry=True):
    at = IF.get("access_token","")
    if not at: return {"errorcode":-9999,"errmsg":"未配置iFinD token"}
    try:
        r = requests.post(f"{IFIND_URL}/{ep}", headers={"Content-Type":"application/json","access_token":at}, json=params, timeout=30)
        d = r.json()
        if d.get("errorcode") in (-1010,-1300,-1302) and retry and IF.get("refresh_token"):
            r2 = requests.post(f"{IFIND_URL}/get_access_token", headers={"Content-Type":"application/json","refresh_token":IF["refresh_token"]}, timeout=15)
            d2 = r2.json()
            if d2.get("errorcode")==0:
                IF["access_token"]=d2.get("access_token","")
                with open(CFG,"w") as f: json.dump(IF,f,ensure_ascii=False,indent=2)
                return ifind_api(ep,params,retry=False)
        return d
    except Exception as e: return {"errorcode":-9998,"errmsg":str(e)}

def ifind_quote(codes):
    """同花顺iFinD专业行情（含PE/换手率/市值/股息率）"""
    if isinstance(codes,str): codes=[c.strip() for c in codes.split(",")]
    def to_ic(c):
        r,m = parse_code(c)
        suf={1:'.SH',0:'.SZ',2:'.HK',3:'.US'}.get(m,'')
        return f"{r}{suf}"
    ds = ifind_api("real_time_quotation",{"codes":",".join(to_ic(c) for c in codes),
        "indicators":"open,high,low,close,preClose,change,changeRatio,volume,amount,pe_ttm,turnoverRatio,totalCapital,amplitude,pe_static,pb"})
    if ds.get("errorcode")!=0: return {"error":ds.get("errmsg","查询失败"),"source":"iFinD"}
    res=[]
    for code in codes:
        ic = to_ic(code)
        dd = ds.get(ic,{})
        if dd:
            r = simplify(dd)
            r['code'] = code
            res.append(r)
    return {"source":"iFinD","data":res}

def parse_code(c):
    """解析股票代码, 返回(code, market) market: 0=深, 1=沪, 2=港, 3=美"""
    c = c.strip().upper().replace('SH','').replace('SZ','').replace('HK','').replace('.','')
    if c.startswith('6'): return c, 1
    if c.startswith('0') or c.startswith('3'): return c, 0
    if c.startswith('5'): return c, 1
    return c, 0

def simplify(d):
    """简化iFinD返回字段名"""
    m = {'open':'open','high':'high','low':'low','close':'close','preClose':'last_close',
         'change':'change','changeRatio':'change_pct','volume':'volume','amount':'amount',
         'pe_ttm':'pe','turnoverRatio':'turnover_rate','totalCapital':'market_cap',
         'amplitude':'amplitude','pe_static':'pe_static','pb':'pb'}
    return {m.get(k,k):v for k,v in d.items() if v is not None}

# ============================================================
# 4. AKShare 研报/公告/资金流向
# ============================================================
AK_OK = False
try: import akshare as ak; AK_OK = True
except: pass

def akshare_report(code, count=5):
    """AKShare券商研报"""
    if not AK_OK: return None
    try:
        code_clean = code.replace('.SH','').replace('.SZ','')
        df = ak.stock_jsyjs_anal_em(symbol=code_clean)
        if df is None or df.empty: return None
        df = df.head(count)
        cols = [c for c in ['股票代码','股票名称','研报内容','最新评级','评级','目标价','评级变动','机构名称','报告日期','行业'] if c in df.columns]
        if not cols: cols = list(df.columns[:8])
        return {'source':'AKShare(研报)','code':code_clean,'reports':df[cols].to_dict('records')}
    except Exception as e:
        return {'source':'AKShare(研报)','error':str(e)}

def cninfo_announce(code, count=10):
    """巨潮资讯网公告搜索（全文搜索API）"""
    try:
        code_clean = code.replace('.SH','').replace('.SZ','')
        url = "http://www.cninfo.com.cn/new/fulltextSearch/full"
        payload = {
            "searchkey": code_clean,
            "sdate": "",
            "edate": "",
            "isfulltext": "false",
            "sortName": "pubdate",
            "sortType": "desc",
            "pageNum": 1,
            "pageSize": count,
        }
        resp = requests.post(url, data=payload, timeout=10,
            headers={'User-Agent':'Mozilla/5.0',
                     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                     'Referer':'http://www.cninfo.com.cn/new/index'})
        if resp.status_code != 200: return None
        data = resp.json()
        items = data.get('announcements') or []
        if not items: return None
        announcements = []
        for item in items:
            ts = item.get('announcementTime', 0)
            date_str = ''
            if ts:
                from datetime import datetime
                date_str = datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d')
            title = item.get('shortTitle') or item.get('announcementTitle','')
            # 去掉<em>标签
            title = re.sub(r'<[^>]+>', '', title)
            announcements.append({
                'title': title,
                'date': date_str,
                'code': item.get('secCode',''),
                'name': item.get('secName',''),
                'pdf_url': f"http://www.cninfo.com.cn/{item.get('adjunctUrl','')}" if item.get('adjunctUrl') else '',
            })
        return {'source':'巨潮资讯网(CNINFO)','code':code_clean,'announcements':announcements}
    except Exception as e:
        return None

def akshare_announce(code, count=10):
    """AKShare公告"""
    if not AK_OK: return None
    try:
        code_clean = code.replace('.SH','').replace('.SZ','')
        df = ak.stock_zh_a_notice_report(symbol=code_clean)
        if df is None or df.empty: return None
        df = df.head(count)
        cols = [c for c in ['股票代码','股票名称','公告标题','公告时间','公告类型'] if c in df.columns]
        if not cols: cols = list(df.columns[:6])
        return {'source':'AKShare(公告)','code':code_clean,'announcements':df[cols].to_dict('records')}
    except: return None

def akshare_moneyflow(code, count=5):
    """AKShare资金流向"""
    if not AK_OK: return None
    try:
        code_clean = code.replace('.SH','').replace('.SZ','')
        df = ak.stock_individual_fund_flow(stock=code_clean, market="sh" if code_clean.startswith('6') else "sz")
        if df is None or df.empty: return None
        df = df.tail(count)
        return {'source':'AKShare(资金流向)','code':code_clean,'flows':df.to_dict('records')}
    except: return None

def ths_sector_page(url_name='thshy', label='行业板块'):
    """从同花顺页面抓取板块排行（EastMoney被限流时的备选）"""
    try:
        from bs4 import BeautifulSoup
        url = f'https://q.10jqka.com.cn/{url_name}/'
        resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('table')
        if not table: raise ValueError('no table')
        rows = table.find_all('tr')
        if len(rows) < 2: raise ValueError('no data rows')
        headers = [th.get_text(strip=True) for th in rows[0].find_all(['th','td'])]
        data = []
        for tr in rows[1:21]:
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cells:
                data.append(dict(zip(headers, cells)))
        return {'source':f'同花顺({label})','sectors':data}
    except Exception as e:
        return {'source':f'同花顺({label})','error':str(e)}

def akshare_sector():
    """板块排行（同花顺页面抓取，EastMoney被限流时自动切换）"""
    return ths_sector_page('thshy', '行业板块')

# ============================================================
# 5. iWencai 问财 - 语义搜索（需Token）
# ============================================================
WENCAI_TOKEN = os.environ.get('WENCAI_TOKEN', '')
WENCAI_OK = bool(WENCAI_TOKEN)

def wencai_search(query, count=20):
    """问财语义搜索 - 需要WENCAI_TOKEN环境变量"""
    if not WENCAI_OK:
        return {'source':'iWencai(问财)','error':'未配置WENCAI_TOKEN','fix':'export WENCAI_TOKEN=your_key | 从 SkillHub 获取'}
    try:
        import wencai as wc
        wc.set_token(WENCAI_TOKEN)
        df = wc.search(query)
        if df is None or df.empty:
            return {'source':'iWencai','query':query,'results':[]}
        data = df.head(count).to_dict('records')
        return {'source':'iWencai(问财)','query':query,'results':data,'columns':list(df.columns[:15])}
    except Exception as e:
        return {'source':'iWencai','error':str(e)}

# ============================================================
# 统一查询：智能降级
# ============================================================
def smart_quote(code):
    """智能查询：三层降级 TDX → 腾讯财经 → 错误"""
    # 第一层：通达讯（实时盘口）
    q = tdx_quote(code)
    if q and q.get('price',0) > 0:
        # 补充腾讯财经的财务数据
        tq = tencent_quote(code)
        if tq and 'error' not in tq:
            q['name'] = tq.get('name','')
            q['pe'] = tq.get('pe',0)
            q['turnover_rate'] = tq.get('turnover_rate',0)
            q['market_cap'] = tq.get('market_cap',0)
            q['circulating_cap'] = tq.get('circulating_cap',0)
        return q

    # 第二层：腾讯财经
    tq = tencent_quote(code)
    if tq and 'error' not in tq:
        return tq

    # 第三层：iFinD（如果配置了token）
    if IFIND_OK:
        iq = ifind_quote(code)
        if isinstance(iq, dict) and 'error' not in iq:
            return iq

    return {'error': f'所有数据源均无法获取 {code} 的行情'}

# ============================================================
# 热点题材 & 板块排行
# ============================================================
def ths_hot_themes():
    """同花顺热点题材：行业+概念双榜"""
    industry = ths_sector_page('thshy', '行业板块')
    concept = ths_sector_page('thybk', '概念板块')
    return {'source':'同花顺热点','industry':industry.get('sectors',[])[:10],'concept':concept.get('sectors',[])[:10]}

# ============================================================
# 6. JQData 聚宽 - 量化指标与因子（需账号）
# ============================================================
JQ_OK = False
JQ_AUTH = os.environ.get('JQ_USER', '') and os.environ.get('JQ_PASS', '')
try:
    import jqdatasdk as jq
    JQ_OK = True
except: pass

def jq_auth():
    """登录JQData"""
    if not JQ_OK or not JQ_AUTH: return False
    try:
        jq.auth(os.environ['JQ_USER'], os.environ['JQ_PASS'])
        return jq.is_auth()
    except: return False

def jq_financial(code, fields=None):
    """JQData财报数据"""
    if not jq_auth(): return {'source':'JQData(聚宽)','error':'未配置JQ_USER/JQ_PASS','fix':'export JQ_USER=xxx JQ_PASS=xxx'}
    try:
        from jqdatasdk import get_fundamentals, query, balance, income, cash_flow, indicator
        code_fmt = f"{code}.XSHE" if code.startswith(('0','3')) else f"{code}.XSHG"
        q = query(indicator).filter(indicator.code == code_fmt)
        df = get_fundamentals(q, statDate='2025q4')
        if df is None or df.empty: return {'source':'JQData','error':'无数据'}
        return {'source':'JQData(聚宽)','code':code,'data':df.to_dict('records')[0] if len(df)>0 else {}}
    except Exception as e:
        return {'source':'JQData','error':str(e)}

def jq_macro():
    """JQData宏观经济数据"""
    if not jq_auth(): return {'source':'JQData','error':'未配置JQ账号'}
    try:
        from jqdatasdk import get_macroeconomics
        # 获取GDP、CPI等
        gdp = get_macroeconomics('CHN_GDP_YOY', startDate='2024-01-01')
        cpi = get_macroeconomics('CHN_CPI_YOY', startDate='2024-01-01')
        return {
            'source':'JQData(聚宽)',
            'gdp': gdp.to_dict('records') if gdp is not None else [],
            'cpi': cpi.to_dict('records') if cpi is not None else [],
        }
    except Exception as e:
        return {'source':'JQData','error':str(e)}

# ============================================================
# 7. Tushare Pro - 基础数据（需积分权限）
# ============================================================
TUSHARE_OK = False
TUSHARE_PRO = None
try:
    import tushare as ts
    import tushare.pro.client as client
    client.DataApi._DataApi__http_url = "http://tushare.xyz"
    TUSHARE_PRO = ts.pro_api('c8dbb3833192a3e47991b1975ad02d95a6567988826e519ba76b0ef5')
    TUSHARE_OK = True
except: pass

def tushare_announce(code, count=20):
    """Tushare公告查询（当前可用）"""
    if not TUSHARE_OK: return None
    try:
        if not code.endswith('.SH') and not code.endswith('.SZ'):
            code_clean = code
            code_ts = f"{code_clean}.SH" if code_clean.startswith('6') else f"{code_clean}.SZ"
        else:
            code_ts = code
        df = TUSHARE_PRO.anns_d(ts_code=code_ts, limit=count)
        if df is None or df.empty: return None
        return {'source':'Tushare Pro','code':code,'announcements':df.to_dict('records')}
    except: return None

# ============================================================
# 8. RiceQuant 米筐 - 量化回测（需账号）
# ============================================================
RQ_OK = False
RQ_AUTH = os.environ.get('RQ_USER', '') and os.environ.get('RQ_PASS', '')
try:
    import rqdatac as rq
    RQ_OK = True
except: pass

def rq_init():
    if RQ_OK and RQ_AUTH:
        try:
            rq.init(os.environ['RQ_USER'], os.environ['RQ_PASS'])
            return True
        except: pass
    return False
# ============================================================
def main():
    if len(sys.argv) < 2:
        print(json.dumps({"usage":"""
china-stock-data CLI - 中国股市综合数据源

命令:
  quote <code>              智能行情查询（通达信→腾讯→iFinD自动降级）
  tdx-quote <code>          通达信实时行情+5档盘口
  tdx-kline <code> [period] 通达信K线 (daily/weekly/monthly/60min)
  tencent-quote <code>      腾讯财经行情（含PE/市值/换手率）
  tencent-batch <code1,code2,...> 腾讯财经批量行情
  ifind-quote <code>        同花顺iFinD专业行情（需token）
  report <code> [count]     研报查询（AKShare）
  announce <code> [count]   公告查询（AKShare）
  moneyflow <code> [count]  资金流向（AKShare）
  sector                    板块排行（同花顺）
  themes                    热点题材（行业+概念）
  search <query>            问财语义搜索（需WENCAI_TOKEN）
  tushare-ann <code>        公告查询（Tushare Pro）
  jq-financial <code>       财报数据（JQData，需JQ_USER/JQ_PASS）
  jq-macro                  宏观数据（JQData）
  status                    数据源状态
"""},ensure_ascii=False)); return

    cmd = sys.argv[1]

    if cmd == 'status':
        print(json.dumps({
            '通达信(TDX)': '✅可用' if TDX_OK else '❌未安装(pytdx)',
            '腾讯财经': '✅可用',
            '同花顺(iFinD)': '✅可用(已配置)' if IFIND_OK else '⚠️未配置token',
            'AKShare': '✅可用' if AK_OK else '❌未安装(akshare)',
            'iWencai(问财)': '✅已配置' if WENCAI_OK else '⚠️未配置WENCAI_TOKEN',
            'JQData(聚宽)': '✅已安装' if JQ_OK else '❌未安装',
            'JQData认证': '✅已认证' if JQ_AUTH else '⚠️需JQ_USER/JQ_PASS',
            'Tushare Pro': '✅已安装(anns_d可用)' if TUSHARE_OK else '❌未安装',
            'RiceQuant(米筐)': '✅已安装' if RQ_OK else '❌未安装',
            'RiceQuant认证': '✅已认证' if RQ_AUTH else '⚠️需RQ_USER/RQ_PASS',
        }, ensure_ascii=False, indent=2))

    elif cmd == 'quote':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        if not code: print(json.dumps({"error":"请指定股票代码"})); return
        r = smart_quote(code)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == 'tdx-quote':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        if not code: print(json.dumps({"error":"请指定股票代码"})); return
        r = tdx_quote(code)
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":f"TDX查询失败:{code}"}))

    elif cmd == 'tdx-kline':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        period = sys.argv[3] if len(sys.argv) > 3 else 'daily'
        r = tdx_kline(code, period)
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":f"TDX K线查询失败:{code}"}))

    elif cmd == 'tencent-quote':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        r = tencent_quote(code)
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":f"腾讯财经查询失败:{code}"}))

    elif cmd == 'tencent-batch':
        codes = sys.argv[2].split(',') if len(sys.argv) > 2 else []
        r = tencent_batch_quote(codes)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == 'ifind-quote':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        r = ifind_quote(code)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == 'report':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        r = akshare_report(code, count)
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":f"研报查询失败:{code}"}))

    elif cmd == 'announce':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        r = cninfo_announce(code, count)
        if not r: r = tushare_announce(code, count)
        if not r: r = akshare_announce(code, count)
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":f"公告查询失败:{code}"}))

    elif cmd == 'moneyflow':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        r = akshare_moneyflow(code, count)
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":f"资金流向查询失败:{code}"}))

    elif cmd == 'sector':
        r = akshare_sector()
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":"板块查询失败"}))

    elif cmd == 'themes':
        r = ths_hot_themes()
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":"热点查询失败"}))

    elif cmd == 'search':
        if len(sys.argv) < 3: print(json.dumps({"error":"请输入搜索词，如: search 人形机器人 丝杠"})); return
        query = ' '.join(sys.argv[2:])
        r = wencai_search(query)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == 'tushare-ann':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        r = tushare_announce(code, count)
        if not r: r = cninfo_announce(code, count)
        if not r: r = akshare_announce(code, count)
        print(json.dumps(r, ensure_ascii=False, default=str) if r else json.dumps({"error":f"公告查询失败:{code}"}))

    elif cmd == 'jq-financial':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        r = jq_financial(code)
        print(json.dumps(r, ensure_ascii=False, default=str))

    elif cmd == 'jq-macro':
        r = jq_macro()
        print(json.dumps(r, ensure_ascii=False, default=str))

    else:
        print(json.dumps({"error":f"未知命令:{cmd}"},ensure_ascii=False))

if __name__ == '__main__':
    PYTHON = sys.executable
    main()
