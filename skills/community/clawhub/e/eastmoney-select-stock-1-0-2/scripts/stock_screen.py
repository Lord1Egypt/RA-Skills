#!/usr/bin/env python3
"""
东方财富智能选股脚本
使用方式: python stock_screen.py <选股条件> [页码] [每页数量]
示例: python stock_screen.py "今日涨幅2%的股票" 1 20
"""

import os
import sys
import csv
import json
import requests

def main():
    if len(sys.argv) < 2:
        print("使用方式: python stock_screen.py <选股条件> [页码] [每页数量]")
        print("示例: python stock_screen.py \"今日涨幅2%的股票\" 1 20")
        sys.exit(1)
    
    keyword = sys.argv[1]
    page_no = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    page_size = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    
    api_key = os.getenv("EASTMONEY_APIKEY")
    
    if not api_key:
        print("错误: 请先设置EASTMONEY_APIKEY环境变量")
        print("你可以在东方财富Skills页面获取apikey，然后执行: export EASTMONEY_APIKEY='你的apikey'")
        sys.exit(1)
    
    url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen"
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key
    }
    data = {
        "keyword": keyword,
        "pageNo": page_no,
        "pageSize": page_size
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # 检查接口状态
        if result.get("status") != 0:
            print(f"接口请求失败: {result.get('message', '未知错误')}")
            sys.exit(1)
        
        if not result.get("data") or result["data"].get("code") != "100":
            print("选股查询失败，建议到东方财富妙想AI进行选股。")
            print(f"错误信息: {result['data'].get('msg', '未知错误')}")
            sys.exit(1)
        
        result_data = result["data"]["data"]["result"]
        if not result_data.get("dataList"):
            print("没有找到符合条件的股票，建议调整筛选条件或到东方财富妙想AI查询。")
            sys.exit(0)
        
        # 打印统计信息
        total = result_data["total"]
        print(f"✅ 找到 {total} 只符合条件的股票\n")
        
        # 打印筛选条件
        total_condition = result["data"]["data"].get("totalCondition", {})
        if total_condition.get("describe"):
            print(f"🔍 筛选条件: {total_condition['describe']}\n")
        
        # 打印列名映射
        columns = result_data["columns"]
        column_map = {col["key"]: col["title"] for col in columns}
        
        # 打印前10条结果
        data_list = result_data["dataList"]
        print("📋 部分结果预览:")
        print("-" * 100)
        
        # 打印表头
        headers = [column_map[key] for key in data_list[0].keys() if key in column_map]
        print("\t".join(headers[:5]))  # 只显示前5列
        print("-" * 100)
        
        # 打印前10行
        for row in data_list[:10]:
            row_data = [str(row[key]) for key in data_list[0].keys() if key in column_map]
            print("\t".join(row_data[:5]))
        
        # 导出为CSV
        csv_filename = f"选股结果_{keyword[:20]}.csv".replace("/", "_").replace("\\", "_")
        with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in data_list:
                csv_row = {column_map[key]: value for key, value in row.items() if key in column_map}
                writer.writerow(csv_row)
        
        print(f"\n💾 完整结果已保存到: {csv_filename}")
        print(f"📊 共 {len(data_list)} 条数据，总共有 {total} 条符合条件的记录")
        
        if total > len(data_list):
            print(f"ℹ️  当前显示第 {page_no} 页，可通过调整页码参数查看更多结果")
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
