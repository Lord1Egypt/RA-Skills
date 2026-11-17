#!/usr/bin/env python3
"""
同业存单查询脚本（通用版本）
用法: python3 query_cd.py [银行简称]
示例: python3 query_cd.py 民生
"""
from playwright.sync_api import sync_playwright
import time
import sys
import re
import os
import tempfile

BANK_MAPPING = {
    "工商": "中国工商银行", "工行": "中国工商银行",
    "农业": "中国农业银行", "农行": "中国农业银行",
    "中国": "中国银行", "中行": "中国银行",
    "建设": "中国建设银行", "建行": "中国建设银行",
    "交通": "交通银行", "交行": "交通银行",
    "邮储": "中国邮政储蓄银行", "邮政": "中国邮政储蓄银行",
    "招商": "招商银行", "招行": "招商银行",
    "民生": "中国民生银行",
    "光大": "中国光大银行",
    "中信": "中信银行",
    "兴业": "兴业银行",
    "浦发": "上海浦东发展银行", "浦东": "上海浦东发展银行",
    "平安": "平安银行",
    "华夏": "华夏银行",
    "广发": "广发银行",
    "浙商": "浙商银行",
    "渤海": "渤海银行",
    "恒丰": "恒丰银行",
    "北京": "北京银行", "上海": "上海银行", "江苏": "江苏银行",
    "南京": "南京银行", "杭州": "杭州银行", "宁波": "宁波银行",
    "苏州": "苏州银行",
    "国开": "国家开发银行", "国开行": "国家开发银行",
    "进出口": "中国进出口银行", "进出口行": "中国进出口银行",
    "农发": "中国农业发展银行", "农发行": "中国农业发展银行",
}

def get_bank_full_name(bank_input):
    if bank_input in BANK_MAPPING:
        return BANK_MAPPING[bank_input]
    for key, value in BANK_MAPPING.items():
        if key in bank_input or bank_input in key:
            return value
    return bank_input

def query_cd(bank_input="民生"):
    bank_full_name = get_bank_full_name(bank_input)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 2560, "height": 1080})

        page.goto("https://www.chinamoney.com.cn/chinese/tycdfxxx/?issueStType=1")
        time.sleep(5)

        page.fill("#ENTY", bank_full_name)
        time.sleep(1)
        page.click("#queryInterbankInfo")
        time.sleep(5)

        # 跨平台临时目录（Windows 兼容）
        safe_name = re.sub(r'[\\/:*?"<>|]', '_', bank_input)
        screenshot_path = os.path.join(tempfile.gettempdir(), f"cd_result_{safe_name}.png")
        page.screenshot(path=screenshot_path, full_page=True)

        result_text = page.inner_text("body")
        match = re.search(r'共\s*(\d+)\s*条', result_text)

        records = []
        if match:
            count = int(match.group(1))
            print(f"查询结果: 共 {count} 条记录")

            if count > 0:
                tables = page.query_selector_all("table")
                for table in tables:
                    rows = table.query_selector_all("tbody tr")
                    if len(rows) > 0:
                        for row in rows:
                            cells = row.query_selector_all("td")
                            if len(cells) >= 5:
                                data = [cell.inner_text().strip() for cell in cells]
                                if data[0]:
                                    if bank_full_name in data[1] or bank_input in data[1]:
                                        # 根据实际表格结构映射（从截图确认）
                                        # [0]存单代码 [1]存单简称 [2]发行日期 [3]发行方式 [4]期限
                                        # [5]息票类型 [6]票面利率(%) [7]参考收益率(%) [8]计划发行量(亿元) [9]主体评级
                                        record = {
                                            "code": data[0] if len(data) > 0 else "",
                                            "name": data[1] if len(data) > 1 else "",
                                            "date": data[2] if len(data) > 2 else "",
                                            "method": data[3] if len(data) > 3 else "",
                                            "term": data[4] if len(data) > 4 else "",
                                            "coupon": data[5] if len(data) > 5 else "",  # 息票类型（不播报）
                                            "face_rate": data[6] if len(data) > 6 else "",  # 票面利率(%)
                                            "ref_rate": data[7] if len(data) > 7 else "",   # 参考收益率(%)
                                            "amount": data[8] if len(data) > 8 else "",     # 计划发行量(亿元)
                                            "rating": data[9] if len(data) > 9 else "",     # 主体评级
                                        }
                                        records.append(record)
                        break
        else:
            print("未能获取结果数量")

        browser.close()
        return screenshot_path, records, bank_full_name

if __name__ == "__main__":
    bank_input = sys.argv[1] if len(sys.argv) > 1 else "民生"

    print(f"正在查询 [{bank_input}] 的同业存单信息...")
    screenshot_path, records, bank_full_name = query_cd(bank_input)

    print(f"\n截图已保存: {screenshot_path}")

    if records:
        print(f"\n{bank_full_name}同业存单发行计划:")
        print(f"\n找到 {len(records)} 条记录:")
        for i, record in enumerate(records, 1):
            print(f"\n[{i}] {record['name']}")
            print(f"    代码: {record['code']}")
            print(f"    发行日期: {record['date']}")
            print(f"    发行方式: {record['method']}")
            print(f"    期限: {record['term']}")

            # 只播报关键字段（不包含息票类型）
            if record['amount'] and record['amount'] not in ['', '--']:
                print(f"    计划发行量(亿元): {record['amount']}")
            if record['ref_rate'] and record['ref_rate'] not in ['', '--']:
                print(f"    参考收益率(%): {record['ref_rate']}")
            if record['rating'] and record['rating'] not in ['', '--']:
                print(f"    主体评级: {record['rating']}")
    else:
        print(f"\n今日{bank_full_name}无存单发行计划")
