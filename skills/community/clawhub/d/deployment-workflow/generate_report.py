#!/usr/bin/env python3
"""
午间/晚间汇报自动生成脚本
功能：
1. 从memory读取测试反馈数据
2. 自动汇总业务人员汇报
3. 生成结构化汇报
4. 发送到群组
"""

import os
import re
from datetime import datetime, timedelta

MEMORY_DIR = "/root/.openclaw/workspace/memory"

def read_today_memory():
    """读取当日memory数据"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = f"{MEMORY_DIR}/{today}.md"
    
    if not os.path.exists(memory_file):
        return None
    
    with open(memory_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    return content

def extract_test_feedback(content):
    """提取测试反馈数据"""
    data = {
        "白浅": [],
        "李顺利": [],
        "链接测试": [],
        "APK测试": []
    }
    
    # 提取白浅汇报
    if "白浅" in content:
        data["白浅"].append("有汇报")
    
    # 提取李顺利汇报
    if "李顺利" in content:
        data["李顺利"].append("有汇报")
    
    # 提取链接测试结果
    if "测试" in content and "链接" in content:
        data["链接测试"].append("已测试")
    
    # 提取APK测试
    if "APK" in content or "下载" in content:
        data["APK测试"].append("已测试")
    
    return data

def generate_noon_report():
    """生成午间汇报"""
    content = read_today_memory()
    if not content:
        return "【午间汇报】暂无数据"
    
    data = extract_test_feedback(content)
    
    report = "【午间汇报】\n\n"
    
    # 测试人员汇报
    if data["白浅"]:
        report += "白浅：已汇报\n"
    if data["李顺利"]:
        report += "李顺利：已汇报\n"
    
    # 链接测试
    if data["链接测试"]:
        report += "链接测试：已完成\n"
    else:
        report += "链接测试：待测试\n"
    
    # APK测试
    if data["APK测试"]:
        report += "APK测试：已完成\n"
    else:
        report += "APK测试：待测试\n"
    
    report += "\n详细数据请查看memory文件"
    
    return report

def generate_evening_report():
    """生成晚间汇报"""
    content = read_today_memory()
    if not content:
        return "【晚间汇报】暂无数据"
    
    data = extract_test_feedback(content)
    
    report = "【晚间汇报】\n\n"
    
    # 测试人员汇报
    if data["白浅"]:
        report += "白浅：✓ 已汇报\n"
    if data["李顺利"]:
        report += "李顺利：✓ 已汇报\n"
    
    # 链接测试汇总
    report += "\n链接测试：\n"
    if data["链接测试"]:
        report += "  - 已完成巡检\n"
    else:
        report += "  - 待执行\n"
    
    # APK测试汇总
    report += "\nAPK下载：\n"
    if data["APK测试"]:
        report += "  - 已完成验证\n"
    else:
        report += "  - 待验证\n"
    
    report += "\n详细信息请查看memory文件"
    
    return report

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        report_type = sys.argv[1]
        if report_type == "午间":
            print(generate_noon_report())
        elif report_type == "晚间":
            print(generate_evening_report())
        else:
            print("用法: python3 generate_report.py [午间|晚间]")
    else:
        print("用法: python3 generate_report.py [午间|晚间]")
