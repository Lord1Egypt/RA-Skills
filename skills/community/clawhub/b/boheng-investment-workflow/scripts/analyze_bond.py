#!/usr/bin/env python3
"""
可转债分析入口脚本
支持可转债转股价值、溢价率分析

数据来源：腾讯财经API (qt.gtimg.cn)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from config import REPORTS_DIR
import requests


def get_bond_quote(bond_code: str) -> dict:
    """
    获取可转债实时行情（腾讯财经）
    
    白名单域名：qt.gtimg.cn
    """
    try:
        # 可转债市场判断
        market = 'sh' if bond_code.startswith('1') else 'sz'
        url = f"https://qt.gtimg.cn/q={market}{bond_code}"
        
        resp = requests.get(url, timeout=10)
        text = resp.content.decode('gbk')
        
        if '=' in text:
            data_str = text.split('=')[1].strip().strip('"')
            fields = data_str.split('~')
            
            if len(fields) >= 40:
                current = float(fields[3])
                prev_close = float(fields[4])
                
                return {
                    'code': bond_code,
                    'name': fields[1],
                    'price': current,
                    'change': current - prev_close,
                    'change_pct': ((current / prev_close) - 1) * 100,
                }
    except Exception as e:
        return {'error': f'获取可转债行情失败: {str(e)}'}
    
    return {'error': '无法解析可转债数据'}


def get_stock_quote(stock_code: str) -> dict:
    """获取正股行情（腾讯财经）"""
    try:
        market = 'sh' if stock_code.startswith('6') else 'sz'
        url = f"https://qt.gtimg.cn/q={market}{stock_code}"
        
        resp = requests.get(url, timeout=10)
        text = resp.content.decode('gbk')
        
        if '=' in text:
            data_str = text.split('=')[1].strip().strip('"')
            fields = data_str.split('~')
            
            if len(fields) >= 40:
                return {
                    'code': stock_code,
                    'name': fields[1],
                    'price': float(fields[3]),
                    'pe': float(fields[39]) if fields[39] else 0,
                    'pb': float(fields[46]) if fields[46] else 0,
                }
    except:
        pass
    
    return {'error': '无法获取正股数据'}


def calculate_conversion_value(bond_price: float, stock_price: float, conversion_price: float) -> dict:
    """
    计算转股价值和溢价率
    
    Args:
        bond_price: 可转债价格
        stock_price: 正股价格
        conversion_price: 转股价
    
    Returns:
        转股价值、溢价率等指标
    """
    # 转股价值 = 100 / 转股价 × 正股价格
    conversion_value = (100 / conversion_price) * stock_price
    
    # 转股溢价率 = (转债价格 - 转股价值) / 转股价值
    conversion_premium = ((bond_price - conversion_value) / conversion_value) * 100
    
    # 纯债价值估算（简化）
    bond_value = 95  # 假设纯债价值约95元
    
    # 纯债溢价率
    bond_premium = ((bond_price - bond_value) / bond_value) * 100
    
    # 双低指标
    double_low = conversion_premium + bond_premium
    
    return {
        'conversion_value': conversion_value,
        'conversion_premium': conversion_premium,
        'bond_value': bond_value,
        'bond_premium': bond_premium,
        'double_low': double_low,
    }


def analyze_bond(bond_code: str, bond_name: str = '', conversion_price: float = 0) -> dict:
    """
    分析可转债
    
    Args:
        bond_code: 可转债代码
        bond_name: 可转债名称
        conversion_price: 转股价（可选，默认估算）
    """
    print(f"📊 开始分析可转债 {bond_code}")
    print("=" * 60)
    print("⚠️ 注意：转股溢价率为估算值，仅供参考")
    print()
    
    # 获取可转债行情
    print("📈 正在获取可转债行情...")
    bond_quote = get_bond_quote(bond_code)
    
    if 'error' in bond_quote:
        print(f"❌ {bond_quote['error']}")
        return bond_quote
    
    bond_name = bond_name or bond_quote.get('name', '未知')
    print(f"✅ {bond_code} {bond_name}: ¥{bond_quote['price']:.2f} ({bond_quote['change_pct']:+.2f}%)")
    
    # 获取正股代码（可转债代码通常对应正股）
    # 常见可转债-正股映射
    bond_stock_map = {
        '113050': '601985',  # 核能转债 -> 中国核电
        '110048': '600019',  # 宝钢转债 -> 宝钢股份
        '113041': '600900',  # 长电转债 -> 长江电力
        '123107': '000921',  # 海信转债 -> 海信家电
    }
    
    stock_code = bond_stock_map.get(bond_code, '')
    
    # 获取正股行情
    stock_quote = {}
    if stock_code:
        print(f"📊 正在获取正股行情 ({stock_code})...")
        stock_quote = get_stock_quote(stock_code)
        
        if 'error' not in stock_quote:
            print(f"✅ 正股 {stock_quote['name']}: ¥{stock_quote['price']:.2f}")
    
    # 转股价估算（默认）
    if not conversion_price:
        # 基于正股价格估算转股价（通常略高于正股价格）
        if 'error' not in stock_quote:
            conversion_price = stock_quote['price'] * 1.05
        else:
            conversion_price = 10.0  # 默认值
    
    # 计算转股价值
    print(f"\n📊 计算转股价值...")
    conversion_metrics = calculate_conversion_value(
        bond_quote['price'],
        stock_quote.get('price', 10),
        conversion_price
    )
    
    # 分析结果
    result = {
        'bond_code': bond_code,
        'bond_name': bond_name,
        'bond_price': bond_quote['price'],
        'change_pct': bond_quote['change_pct'],
        'stock_code': stock_code,
        'stock_name': stock_quote.get('name', '未知'),
        'stock_price': stock_quote.get('price', 0),
        'stock_pe': stock_quote.get('pe', 0),
        'conversion_price': conversion_price,
        'conversion_value': conversion_metrics['conversion_value'],
        'conversion_premium': conversion_metrics['conversion_premium'],
        'bond_value': conversion_metrics['bond_value'],
        'bond_premium': conversion_metrics['bond_premium'],
        'double_low': conversion_metrics['double_low'],
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # 生成报告
    print("\n" + "=" * 60)
    print("        可转债分析报告")
    print("=" * 60)
    print(f"\n【转债代码】：{bond_code}")
    print(f"【转债名称】：{bond_name}")
    print(f"【转债价格】：¥{bond_quote['price']:.2f}")
    print(f"【涨跌幅】：{bond_quote['change_pct']:+.2f}%")
    
    if stock_code and 'error' not in stock_quote:
        print(f"\n📊 正股信息：")
        print(f"   正股代码：{stock_code}")
        print(f"   正股名称：{stock_quote['name']}")
        print(f"   正股价格：¥{stock_quote['price']:.2f}")
        print(f"   正股PE：{stock_quote['pe']:.2f}倍")
    
    print(f"\n💰 转股指标：")
    print(f"   转股价：¥{conversion_price:.2f}")
    print(f"   转股价值：¥{conversion_metrics['conversion_value']:.2f}")
    print(f"   转股溢价率：{conversion_metrics['conversion_premium']:.2f}%")
    print(f"   双低指标：{conversion_metrics['double_low']:.2f}")
    
    # 投资建议
    print("\n" + "=" * 60)
    print("        投资建议")
    print("=" * 60)
    
    # 建议逻辑（基于双低指标）
    double_low = conversion_metrics['double_low']
    
    if double_low < 120:
        suggestion = "✅ 建议关注"
        reason = f"双低指标 {double_low:.1f}，估值偏低"
    elif double_low < 150:
        suggestion = "⚠️ 谨慎投资"
        reason = f"双低指标 {double_low:.1f}，估值合理"
    else:
        suggestion = "⚠️ 谨慎观望"
        reason = f"双低指标 {double_low:.1f}，估值偏高"
    
    print(f"\n最终建议：{suggestion}")
    print(f"理由：{reason}")
    
    # 保存报告
    report_file = os.path.join(REPORTS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_{bond_code}_{bond_name}.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"可转债分析报告 - {bond_code} {bond_name}\n")
        f.write(f"分析时间：{result['analysis_time']}\n")
        f.write(f"转债价格：¥{bond_quote['price']:.2f}\n")
        f.write(f"双低指标：{double_low:.2f}\n")
        f.write(f"建议：{suggestion}\n")
    
    print(f"\n📄 报告已保存至：{report_file}")
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyze_bond.py <可转债代码> [可转债名称] [转股价]")
        print("示例: python3 analyze_bond.py 113050 核能转债")
        print("      python3 analyze_bond.py 113050 核能转债 10.5")
        sys.exit(1)
    
    bond_code = sys.argv[1]
    bond_name = sys.argv[2] if len(sys.argv) > 2 else ''
    conversion_price = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    
    analyze_bond(bond_code, bond_name, conversion_price)