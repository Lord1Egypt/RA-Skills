"""
Amazon商品数据采集 - 简化版
使用方法: python amazon_own_product.py <ASIN> [ZIP_CODE]
"""
import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amazon_monitor_core import get_product_data, save_history, generate_trend_chart

if __name__ == '__main__':
    asin = sys.argv[1] if len(sys.argv) > 1 else None
    if not asin:
        print("错误: 请提供ASIN，例如: python amazon_own_product.py B0XXXXXXX 10001")
        sys.exit(1)
    zip_code = sys.argv[2] if len(sys.argv) > 2 else '10001'
    
    print(f"="*50)
    print(f"Amazon商品数据采集")
    print(f"="*50)
    print(f"ASIN: {asin}")
    print(f"邮编: {zip_code}")
    print()
    
    # 获取数据
    data = get_product_data(asin, zip_code)
    
    if not data.get('valid', True):
        print(f"错误: {data.get('error', '链接失效或页面不存在')}")
        sys.exit(1)
    
    print(f"商品名称: {data.get('productName', '')}")
    print(f"价格: {data.get('price')}")
    print(f"星级: {data.get('rating')}")
    print(f"评论数: {data.get('reviewCount')}")
    print(f"配送地址: {data.get('location')}")
    print(f"采集时间: {data.get('parseTime')}")
    
    # 保存历史数据
    history = save_history(asin, data, zip_code)
    print()
    print(f"历史记录已保存，共 {len(history)} 条")
    
    # 生成趋势图
    if len(history) >= 2:
        chart_file = generate_trend_chart(asin, history)
        if chart_file:
            print(f"趋势图已生成: {chart_file}")
    else:
        print("提示: 需要至少2条数据才能生成趋势图")
        print(f"下次运行时将自动生成趋势图")
