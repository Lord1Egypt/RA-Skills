#!/usr/bin/env python3
"""
股息率溢价监控脚本
功能：
1. 检查国债收益率是否连续3天上涨
2. 检查股息率溢价是否低于3%
3. 满足条件时发送Telegram通知
"""

import xlrd
import csv
import subprocess
import re
import os
from datetime import datetime, timedelta
from pathlib import Path

# 配置
DATA_DIR = "/Users/liyi/.openclaw/workspace"
CSV_FILE = os.path.join(DATA_DIR, "股息率溢价跟踪.csv")
EXCEL_FILE = os.path.join(DATA_DIR, "股息率溢价跟踪.xlsx")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = "505395883"

def send_telegram(message):
    """发送Telegram消息"""
    if not TELEGRAM_TOKEN:
        print("未配置Telegram Bot Token")
        return False
    
    cmd = f"""curl -s -X POST https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage \
      -d chat_id={TELEGRAM_CHAT_ID} \
      -d text="{message}" \
      -d parse_mode=HTML"""
    
    os.system(cmd)
    return True

def download_dividend_rate(date_str):
    """下载股息率"""
    url = "https://oss-ch.csindex.com.cn/static/html/csindex/public/uploads/file/autofile/indicator/H30269indicator.xls"
    local_file = "/tmp/H30269indicator.xls"
    
    os.system(f"curl -s -o {local_file} '{url}'")
    
    try:
        book = xlrd.open_workbook(local_file)
        sheet = book.sheet_by_index(0)
        for row in range(1, sheet.nrows):
            if str(sheet.cell_value(row, 0)) == date_str:
                return sheet.cell_value(row, 8)
    except:
        pass
    return None

def download_bond_yield():
    """下载国债收益率数据（最近7天）"""
    result = subprocess.run(
        ['curl', '-s', 'https://yield.chinabond.com.cn/cbweb-czb-web/czb/moreInfo?locale=cn_ZH&nameType=1'],
        capture_output=True, text=True
    )
    
    data = {}
    for row in range(1, 8):  # 最近7天
        date = (datetime.now() - timedelta(days=row)).strftime('%Y-%m-%d')
        pattern = rf'{date}.*?10年.*?(\d+\.\d{{2}})'
        match = re.search(pattern, result.stdout, re.DOTALL)
        if match:
            data[date] = float(match.group(1))
    
    return data

def check_bond_yield_rising(data):
    """检查国债收益率是否连续3天上涨"""
    if len(data) < 3:
        return False, None
    
    sorted_dates = sorted(data.keys(), reverse=True)
    
    # 检查最近3天
    d1, d2, d3 = sorted_dates[0], sorted_dates[1], sorted_dates[2]
    
    if data[d1] > data[d2] > data[d3]:
        return True, f"⚠️ 国债收益率连续3天上涨！\n{d3}: {data[d3]}%\n{d2}: {data[d2]}%\n{d1}: {data[d1]}%"
    
    return False, None

def check_premium_low(data):
    """检查股息率溢价是否低于1%"""
    sorted_dates = sorted(data.keys(), reverse=True)
    latest = sorted_dates[0]
    
    if data[latest] < 1.0:
        return True, f"⚠️ 股息率溢价低于1%！\n{latest}: {data[latest]}%\n可能出现布局机会，请密切关注！"
    
    return False, None

def load_existing_data():
    """加载现有数据"""
    data = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row['日期']
                data[date] = {
                    '股息率': float(row['股息率1']),
                    '国债': float(row['10年国债收益率']),
                    '溢价': float(row['股息率溢价'])
                }
    return data

def run_check():
    """运行监控检查"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 股息率溢价监控检查")
    
    # 加载现有数据
    data = load_existing_data()
    
    if len(data) < 3:
        print("  数据不足3天，跳过检查")
        return
    
    # 检查国债收益率连续上涨
    bond_data = {k: v['国债'] for k, v in data.items()}
    rising, msg = check_bond_yield_rising(bond_data)
    if rising:
        print(f"  🚨 {msg}")
        send_telegram(msg)
    
    # 检查溢价低于3%
    premium_data = {k: v['溢价'] for k, v in data.items()}
    low, msg = check_premium_low(premium_data)
    if low:
        print(f"  💡 {msg}")
        send_telegram(msg)
    
    if not rising and not low:
        print(f"  ✅ 无异常")
    
    print(f"  完成!")

def update_today():
    """更新今天的数据"""
    today = datetime.now().strftime('%Y%m%d')
    formatted = datetime.now().strftime('%Y-%m-%d')
    
    # 下载股息率
    div_rate = download_dividend_rate(today)
    
    # 下载国债收益率
    bond_yields = download_bond_yield()
    bond_yield = bond_yields.get(formatted)
    
    if div_rate and bond_yield:
        premium = div_rate - bond_yield
        
        # 更新数据
        data = load_existing_data()
        data[formatted] = {
            '股息率': div_rate,
            '国债': bond_yield,
            '溢价': round(premium, 2)
        }
        
        # 保存CSV
        with open(CSV_FILE, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['日期', '股息率1', '10年国债收益率', '股息率溢价'])
            writer.writeheader()
            for date in sorted(data.keys()):
                writer.writerow({
                    '日期': date,
                    '股息率1': data[date]['股息率'],
                    '10年国债收益率': data[date]['国债'],
                    '股息率溢价': data[date]['溢价']
                })
        
        print(f"已更新: {formatted} - 股息率={div_rate}%, 国债={bond_yield}%, 溢价={premium:.2f}%")
        
        # 运行检查
        run_check()
    else:
        print(f"获取数据失败: 股息率={div_rate}, 国债={bond_yield}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            run_check()
        elif sys.argv[1] == "--update":
            update_today()
    else:
        update_today()
