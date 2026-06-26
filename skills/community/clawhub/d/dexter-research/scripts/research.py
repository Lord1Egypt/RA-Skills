#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dexter Research - A股自主金融研究脚本
输入: 股票代码(如000001)或名称(如贵州茅台)
输出: 结构化JSON研究报告 → 供Mari深度总结
"""
import sys
import json
import time
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# ============ 数据源配置（从环境变量读取）============
import os

FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
USER_OPEN_ID = os.environ.get("FEISHU_USER_OPEN_ID", "ou_805cd822ede55b661fcbcd1eeab2a3dd")
OUTPUT_FILE = os.environ.get("DEXTER_OUTPUT_FILE", "/root/.openclaw/workspace/data/dexter-research.json")
LOG_FILE = os.environ.get("DEXTER_LOG_FILE", "/root/.openclaw/workspace/logs/dexter-research.log")

# 校验必要配置
if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
    print("⚠️ 未配置飞书凭证，请设置环境变量:")
    print("   export FEISHU_APP_ID=your_app_id")
    print("   export FEISHU_APP_SECRET=your_app_secret")
    print("⚠️ 飞书推送功能暂时不可用，数据分析仍可正常运行")

# ============ 日志 ============
def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ============ 飞书Token ============
def get_feishu_token():
    import requests
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    r = requests.post(url, json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}, timeout=10)
    return r.json().get("tenant_access_token", "")

# ============ 数据获取 ============
def get_stock_info(code):
    """获取个股基本信息"""
    import akshare as ak
    try:
        df = ak.stock_individual_info_em(symbol=code)
        info = df.set_index('item')['value'].to_dict()
        return info
    except Exception as e:
        log(f"个股信息获取失败: {e}")
        return {}

def get_financial_abstract(code):
    """获取财务摘要80指标（多季度）"""
    import akshare as ak
    try:
        df = ak.stock_financial_abstract(symbol=code)
        # 转换为 {指标: {日期: 值}} 的格式
        result = {}
        date_cols = sorted([c for c in df.columns if c.startswith('202')], reverse=True)
        if date_cols:
            latest_date = date_cols[0]
            prev_date = date_cols[1] if len(date_cols) > 1 else date_cols[0]
            
            for _, row in df.iterrows():
                indicator = row['指标']
                latest_val = row.get(latest_date)
                prev_val = row.get(prev_date)
                result[indicator] = {
                    'latest': float(latest_val) if latest_val is not None else None,
                    'prev': float(prev_val) if prev_val is not None else None,
                    'unit': '万元' if '净利润' in indicator or '收入' in indicator or '资产' in indicator or '负债' in indicator else ('元' if '每股' in indicator else '%' if '率' in indicator or '比率' in indicator else '倍')
                }
        return result, latest_date
    except Exception as e:
        log(f"财务摘要获取失败: {e}")
        return {}, ""

def get_fund_flow(code):
    """获取资金流向"""
    import akshare as ak
    try:
        df = ak.stock_individual_fund_flow(stock=code)
        if df is not None and len(df) > 0:
            # 取最近几天
            cols = df.columns.tolist()
            rows = df.head(5).to_dict('records')
            return {'columns': cols, 'data': rows}
    except Exception as e:
        log(f"资金流向获取失败: {e}")
    return {}

def get_kline_data(code, num=120):
    """获取K线数据 - 使用Tencent财经API"""
    try:
        import requests
        import json
        import pandas as pd
        
        # 判断交易所前缀
        prefix = 'sz' if code.startswith(('0', '3', '002', '003')) else 'sh'
        symbol = f'{prefix}{code}'
        
        # Tencent财经API
        url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get'
        params = {'_var': 'kline_dayqfq', 'param': f'{symbol},day,,,{num},qfq'}
        
        resp = requests.get(url, params=params, timeout=15)
        text = resp.text
        start = text.find('{')
        if start < 0:
            log(f"K线获取失败: 无法解析响应")
            return {}
        
        data = json.loads(text[start:])
        qfq = data.get('data', {}).get(symbol, {}).get('qfqday', [])
        
        if not qfq or len(qfq) < 5:
            log(f"K线获取失败: 数据不足")
            return {}
        
        # 清洗数据：只保留标准6字段行
        clean_data = [row for row in qfq if isinstance(row, list) and len(row) == 6]
        if not clean_data:
            log(f"K线获取失败: 清洗后无数据")
            return {}
        
        # 构建DataFrame，字段顺序：日期,开盘,收盘,最高,最低,成交量
        df = pd.DataFrame(clean_data, columns=['date', 'open', 'close', 'high', 'low', 'volume'])
        df = df.astype({'open': float, 'close': float, 'high': float, 'low': float, 'volume': float})
        
        # 计算均线
        df['MA5'] = df['close'].rolling(5).mean()
        df['MA10'] = df['close'].rolling(10).mean()
        df['MA20'] = df['close'].rolling(20).mean()
        
        latest = df.iloc[-1].to_dict()
        return {
            'latest': latest,
            'recent_5': df.tail(5).to_dict('records'),
        }
    except Exception as e:
        log(f"K线获取失败: {e}")
    return {}

def get_market_industry(code):
    """获取所属行业板块"""
    import requests
    try:
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={'1' if code.startswith('6') else '0'}.{code}&fields=f57,f58,f107,f108,f162,f163,f164,f165"
        r = requests.get(url, timeout=10)
        d = r.json().get('data', {})
        return {
            'industry': d.get('f58', ''),
            'code': d.get('f57', ''),
        }
    except:
        return {}

def calculate_scores(financial):
    """基于80指标计算评分"""
    scores = {}
    
    def safe(val):
        return val if val is not None else 0
    
    # 盈利能力 (ROE/毛利率/净利率)
    roe = safe(financial.get('净资产收益率(ROE)', {}).get('latest'))
    gross = safe(financial.get('毛利率', {}).get('latest'))
    net_margin = safe(financial.get('销售净利率', {}).get('latest'))
    
    # 满分85分：ROE(30) + 毛利率(30) + 净利率(25)
    roe_score = min(roe / 20 * 30, 30) if roe > 0 else 0
    gross_score = min(gross / 50 * 30, 30) if gross > 0 else 0
    net_score = min(net_margin / 20 * 25, 25) if net_margin > 0 else 0
    raw = roe_score + gross_score + net_score
    # 归一化到100：ROE达标(20%)+毛利率(50%)+净利率(20%) = 满分
    scores['profitability'] = min(raw / 85 * 100, 100)
    
    # 成长性
    revenue_growth = safe(financial.get('营业总收入增长率', {}).get('latest'))
    profit_growth = safe(financial.get('归属母公司净利润增长率', {}).get('latest'))
    scores['growth'] = min(revenue_growth / 30 * 50, 50) + min(profit_growth / 30 * 50, 50)
    scores['growth'] = min(scores['growth'], 100)
    
    # 财务健康
    debt = safe(financial.get('资产负债率', {}).get('latest'))
    current = safe(financial.get('流动比率', {}).get('latest'))
    quick = safe(financial.get('速动比率', {}).get('latest'))
    scores['health'] = 0
    if 0 < debt < 70:
        scores['health'] += (70 - debt) / 70 * 30
    if current > 1.5:
        scores['health'] += min((current - 1.5) / 1 * 35, 35)
    if quick > 1:
        scores['health'] += min((quick - 1) / 1 * 35, 35)
    scores['health'] = min(scores['health'], 100)
    
    # 现金流
    cash_ratio = safe(financial.get('经营现金流量净额', {}).get('latest'))
    scores['cash'] = 80 if cash_ratio > 0 else 20
    
    # 综合评分
    scores['overall'] = round(
        scores['profitability'] * 0.35 +
        scores['growth'] * 0.25 +
        scores['health'] * 0.25 +
        scores['cash'] * 0.15, 1)
    scores['profitability'] = round(scores['profitability'], 1)
    scores['growth'] = round(scores['growth'], 1)
    scores['health'] = round(scores['health'], 1)
    scores['cash'] = round(scores['cash'], 1)
    
    return scores

def generate_summary(code, stock_info, financial, financial_date, fund_flow, kline, industry, scores):
    """生成文本摘要"""
    name = stock_info.get('股票简称', stock_info.get('简称', code))
    
    # 核心指标
    roe = financial.get('净资产收益率(ROE)', {}).get('latest', 0) or 0
    gross = financial.get('毛利率', {}).get('latest', 0) or 0
    net = financial.get('销售净利率', {}).get('latest', 0) or 0
    debt = financial.get('资产负债率', {}).get('latest', 0) or 0
    revenue_growth = financial.get('营业总收入增长率', {}).get('latest', 0) or 0
    profit_growth = financial.get('归属母公司净利润增长率', {}).get('latest', 0) or 0
    
    # K线
    price = kline.get('latest', {}).get('close', 0) if kline else 0
    ma5 = kline.get('latest', {}).get('MA5', 0) if kline else 0
    ma20 = kline.get('latest', {}).get('MA20', 0) if kline else 0
    
    summary = f"""【{name} ({code})】财务研究简报

■ 评分总览 (满分100)
  综合评分: {scores['overall']:.1f}
  ├ 盈利能力: {scores['profitability']:.1f}/100
  ├ 成长性: {scores['growth']:.1f}/100
  ├ 财务健康: {scores['health']:.1f}/100
  └ 现金流: {scores['cash']:.1f}/100

■ 核心财务指标 ({financial_date})
  ROE(净资产收益率): {roe:.2f}% {'✅优秀' if roe > 15 else '⚠️偏低' if roe > 0 else '❌亏损'}
  毛利率: {gross:.2f}%
  净利率: {net:.2f}%
  资产负债率: {debt:.2f}% {'✅安全' if debt < 60 else '⚠️偏高'}
  营收增长率: {revenue_growth:+.2f}%
  净利润增长率: {profit_growth:+.2f}%

■ 技术面
  当前股价: {price:.2f}元
  MA5: {ma5:.2f} | MA20: {ma20:.2f}
  {'✅ 股价位于均线上方' if price > ma20 else '⚠️ 股价位于均线下方'}

■ 行业: {industry.get("industry", "未知")}

■ 资金面"""
    
    if fund_flow and fund_flow.get('data'):
        try:
            latest_flow = fund_flow['data'][0]
            # 尝试找到主力净流入列
            cols = fund_flow['columns']
            summary += f"\n  (近5日资金流向数据)"
        except:
            summary += "\n  资金流向数据获取中"
    else:
        summary += "\n  数据获取中"
    
    return summary

def save_json(code, data):
    """保存JSON"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "code": code,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }, f, ensure_ascii=False, indent=2, default=str)
    log(f"数据已写入: {OUTPUT_FILE}")

def send_feishu(token, msg):
    """推送飞书"""
    import requests
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    r = requests.post(url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"receive_id": USER_OPEN_ID, "msg_type": "text", "content": json.dumps({"text": msg})},
        timeout=10)
    return r.json().get("code") == 0

# ============ 主流程 ============
def main():
    if len(sys.argv) < 2:
        print("用法: python3 research.py <股票代码>")
        print("示例: python3 research.py 000001")
        print("       python3 research.py 600519")
        sys.exit(1)
    
    code = sys.argv[1].strip()
    
    # 标准化代码
    if code.isdigit():
        if len(code) == 6:
            if code.startswith(('0', '3')):
                code = code  # 深交所
            else:
                code = code  # 上交所
        else:
            print("请输入6位股票代码")
            sys.exit(1)
    
    log(f"{'='*50}")
    log(f"Dexter研究开始: {code}")
    start = time.time()
    
    # 1. 获取个股信息
    log("获取个股信息...")
    stock_info = get_stock_info(code)
    name = stock_info.get('股票简称', code)
    log(f"股票简称: {name}")
    
    # 2. 获取财务数据
    log("获取财务数据(80指标)...")
    financial, financial_date = get_financial_abstract(code)
    log(f"获取到 {len(financial)} 个财务指标, 最新日期: {financial_date}")
    
    # 3. 获取资金流向
    log("获取资金流向...")
    fund_flow = get_fund_flow(code)
    
    # 4. 获取K线
    log("获取K线数据...")
    kline = get_kline_data(code)
    
    # 5. 获取行业
    log("获取行业信息...")
    industry = get_market_industry(code)
    
    # 6. 计算评分
    log("计算财务评分...")
    scores = calculate_scores(financial)
    log(f"综合评分: {scores['overall']:.1f}")
    
    # 7. 生成摘要
    summary = generate_summary(code, stock_info, financial, financial_date, fund_flow, kline, industry, scores)
    print("\n" + summary)
    
    # 8. 保存JSON
    report_data = {
        "stock_info": stock_info,
        "financial": financial,
        "financial_date": financial_date,
        "fund_flow": fund_flow,
        "kline": kline,
        "industry": industry,
        "scores": scores,
        "summary": summary
    }
    save_json(code, report_data)
    
    # 9. 推送飞书
    token = get_feishu_token()
    if token:
        ok = send_feishu(token, summary)
        log(f"飞书推送: {'成功' if ok else '失败'}")
    
    elapsed = time.time() - start
    log(f"Dexter研究完成, 耗时{elapsed:.1f}秒")
    log(f"{'='*50}")
    
    print(f"\n✅ 完整JSON数据已保存至: {OUTPUT_FILE}")
    print(f"💡 供Mari后续深度总结使用")

if __name__ == "__main__":
    main()
