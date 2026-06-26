#!/usr/bin/env python3
"""
基金分析入口脚本
支持公募基金净值分析

数据来源：腾讯财经API (qt.gtimg.cn)
注意：基金净值数据为估算，仅供参考
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from config import REPORTS_DIR
import requests


def get_fund_quote(fund_code: str) -> dict:
    """
    获取基金行情（腾讯财经）
    
    白名单域名：qt.gtimg.cn
    """
    try:
        # 腾讯基金接口
        market = 'of'  # 开放式基金
        url = f"https://qt.gtimg.cn/q={market}{fund_code}"
        
        resp = requests.get(url, timeout=10)
        text = resp.content.decode('gbk')
        
        if '=' in text and '~' in text:
            data_str = text.split('=')[1].strip().strip('"')
            fields = data_str.split('~')
            
            if len(fields) >= 10:
                return {
                    'code': fund_code,
                    'name': fields[1] if len(fields) > 1 else '未知',
                    'nav': float(fields[3]) if fields[3] else 0,  # 单位净值
                    'total_nav': float(fields[4]) if fields[4] else 0,  # 累计净值
                    'date': fields[5] if len(fields) > 5 else '',  # 净值日期
                }
    except Exception as e:
        return {'error': f'获取基金信息失败: {str(e)}'}
    
    return {'error': '无法解析基金数据'}


def analyze_fund(fund_code: str, fund_name: str = '') -> dict:
    """分析基金"""
    print(f"📊 开始分析基金 {fund_code}")
    print("=" * 60)
    print("⚠️ 注意：基金数据为估算值，仅供参考")
    print()
    
    # 获取基金信息
    print("📈 正在获取基金信息...")
    info = get_fund_quote(fund_code)
    
    if 'error' in info:
        print(f"❌ {info['error']}")
        return info
    
    fund_name = fund_name or info.get('name', '未知')
    print(f"✅ {fund_code} {fund_name}")
    print(f"   单位净值：¥{info['nav']:.4f}")
    print(f"   累计净值：¥{info['total_nav']:.4f}")
    print(f"   净值日期：{info['date']}")
    
    # 分析结果
    result = {
        'fund_code': fund_code,
        'fund_name': fund_name,
        'nav': info['nav'],
        'total_nav': info['total_nav'],
        'nav_date': info['date'],
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # 生成报告
    print("\n" + "=" * 60)
    print("        基金分析报告")
    print("=" * 60)
    print(f"\n【基金代码】：{fund_code}")
    print(f"【基金名称】：{fund_name}")
    print(f"【单位净值】：¥{result['nav']:.4f}")
    print(f"【累计净值】：¥{result['total_nav']:.4f}")
    print(f"【净值日期】：{result['nav_date']}")
    
    # 投资建议（简化）
    print("\n" + "=" * 60)
    print("        投资建议")
    print("=" * 60)
    
    suggestion = "⚠️ 谨慎投资"
    reason = "基金数据为估算值，建议查阅基金公司官方公告"
    
    print(f"\n最终建议：{suggestion}")
    print(f"理由：{reason}")
    
    # 保存报告
    report_file = os.path.join(REPORTS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_{fund_code}_{fund_name}.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"基金分析报告 - {fund_code} {fund_name}\n")
        f.write(f"分析时间：{result['analysis_time']}\n")
        f.write(f"单位净值：¥{result['nav']:.4f}\n")
        f.write(f"建议：{suggestion}\n")
    
    print(f"\n📄 报告已保存至：{report_file}")
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyze_fund.py <基金代码> [基金名称]")
        print("示例: python3 analyze_fund.py 110022 易方达消费行业")
        sys.exit(1)
    
    fund_code = sys.argv[1]
    fund_name = sys.argv[2] if len(sys.argv) > 2 else ''
    
    analyze_fund(fund_code, fund_name)