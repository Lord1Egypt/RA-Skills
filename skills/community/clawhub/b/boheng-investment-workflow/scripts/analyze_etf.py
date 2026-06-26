#!/usr/bin/env python3
"""
ETF分析入口脚本
支持ETF实时行情分析

数据来源：腾讯财经API (qt.gtimg.cn)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from config import REPORTS_DIR
import requests


def get_etf_quote(etf_code: str) -> dict:
    """
    获取ETF实时行情（腾讯财经）
    
    白名单域名：qt.gtimg.cn
    """
    try:
        # 判断市场
        market = 'sh' if etf_code.startswith('5') else 'sz'
        url = f"https://qt.gtimg.cn/q={market}{etf_code}"
        
        resp = requests.get(url, timeout=10)
        text = resp.content.decode('gbk')
        
        if '=' in text:
            data_str = text.split('=')[1].strip().strip('"')
            fields = data_str.split('~')
            
            if len(fields) >= 40:
                current = float(fields[3])
                prev_close = float(fields[4])
                
                return {
                    'code': etf_code,
                    'name': fields[1],
                    'price': current,
                    'change': current - prev_close,
                    'change_pct': ((current / prev_close) - 1) * 100,
                    'open': float(fields[5]) if fields[5] else 0,
                    'high': float(fields[33]) if fields[33] else 0,
                    'low': float(fields[34]) if fields[34] else 0,
                    'volume': float(fields[6]) if fields[6] else 0,
                    'amount': float(fields[37]) if fields[37] else 0,
                }
    except Exception as e:
        return {'error': f'获取ETF行情失败: {str(e)}'}
    
    return {'error': '无法解析ETF数据'}


def analyze_etf(etf_code: str, etf_name: str = '') -> dict:
    """分析ETF"""
    print(f"📊 开始分析ETF {etf_code}")
    print("=" * 60)
    
    # 获取ETF行情
    print("📈 正在获取ETF行情...")
    quote = get_etf_quote(etf_code)
    
    if 'error' in quote:
        print(f"❌ {quote['error']}")
        return quote
    
    etf_name = etf_name or quote.get('name', '未知')
    print(f"✅ {etf_code} {etf_name}: ¥{quote['price']:.3f} ({quote['change_pct']:+.2f}%)")
    
    # 判断ETF类型
    etf_type = "未知"
    if etf_code.startswith('51'):  # 上交所ETF
        if etf_code.startswith('510'):
            etf_type = "宽基ETF"
        elif etf_code.startswith('512'):
            etf_type = "行业ETF"
        elif etf_code.startswith('513'):
            etf_type = "跨境ETF"
        elif etf_code.startswith('511'):
            etf_type = "债券ETF"
    elif etf_code.startswith('15'):  # 深交所ETF
        etf_type = "深市ETF"
    
    # 分析结果
    result = {
        'etf_code': etf_code,
        'etf_name': etf_name,
        'etf_type': etf_type,
        'price': quote['price'],
        'change_pct': quote['change_pct'],
        'volume': quote['volume'],
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # 生成报告
    print("\n" + "=" * 60)
    print("        ETF分析报告")
    print("=" * 60)
    print(f"\n【ETF代码】：{etf_code}")
    print(f"【ETF名称】：{etf_name}")
    print(f"【ETF类型】：{etf_type}")
    print(f"【当前价格】：¥{quote['price']:.3f}")
    print(f"【涨跌幅】：{quote['change_pct']:+.2f}%")
    print(f"【成交量】：{quote['volume']/10000:.2f}万手")
    
    # 投资建议
    print("\n" + "=" * 60)
    print("        投资建议")
    print("=" * 60)
    
    # 简单建议逻辑
    if quote['change_pct'] < -3:
        suggestion = "⚠️ 谨慎观望"
        reason = "今日跌幅较大，建议等待企稳"
    elif quote['change_pct'] > 3:
        suggestion = "⚠️ 谨慎追高"
        reason = "今日涨幅较大，注意回调风险"
    else:
        suggestion = "⚠️ 谨慎投资"
        reason = "建议结合指数估值综合判断"
    
    print(f"\n最终建议：{suggestion}")
    print(f"理由：{reason}")
    
    # 保存报告
    report_file = os.path.join(REPORTS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_{etf_code}_{etf_name}.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"ETF分析报告 - {etf_code} {etf_name}\n")
        f.write(f"分析时间：{result['analysis_time']}\n")
        f.write(f"当前价格：¥{quote['price']:.3f}\n")
        f.write(f"建议：{suggestion}\n")
    
    print(f"\n📄 报告已保存至：{report_file}")
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyze_etf.py <ETF代码> [ETF名称]")
        print("示例: python3 analyze_etf.py 510300 沪深300ETF")
        sys.exit(1)
    
    etf_code = sys.argv[1]
    etf_name = sys.argv[2] if len(sys.argv) > 2 else ''
    
    analyze_etf(etf_code, etf_name)