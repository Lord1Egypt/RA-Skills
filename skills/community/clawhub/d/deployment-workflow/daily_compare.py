#!/usr/bin/env python3
"""
内容组数据对比分析脚本
自动对比前日数据和上周同期数据
"""

import os
import re
from datetime import datetime, timedelta

WORKSPACE = "/root/.openclaw/workspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")

# 北京时间
tz_offset = 8
now = datetime.utcnow() + timedelta(hours=tz_offset)
today = now.strftime("%Y-%m-%d")
yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
last_week = (now - timedelta(days=7)).strftime("%Y-%m-%d")

def parse_daily_report(date_str):
    """解析日报文件，提取数据"""
    file_path = os.path.join(MEMORY_DIR, f"{date_str}.md")
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {'date': date_str}
    
    # 提取视频总产出
    match = re.search(r'视频输出[：:]\s*(\d+)部', content)
    if match:
        data['video_total'] = int(match.group(1))
    
    # 提取社区总产出
    match = re.search(r'社区输出[：:]\s*(\d+)贴', content)
    if match:
        data['community_total'] = int(match.group(1))
    
    # 提取个人产出（支持冒号格式：李易：16部 或 李易16部）
    people = ['李易', '淼淼', '王汪', '秋刀鱼', '秋千', '阔落', '熙门']
    for person in people:
        match = re.search(rf'{person}[：:]?\s*(\d+)部', content)
        if match:
            data[person] = int(match.group(1))
    
    # 提取社区个人产出
    for person in ['虾虾', '锐安']:
        match = re.search(rf'{person}[：:]?\s*(\d+)贴', content)
        if match:
            data[person] = int(match.group(1))
    
    # 提取内容分级
    match = re.search(r'视频[：:]\s*S级(\d+)部.*?A级(\d+)部.*?B级(\d+)部', content)
    if match:
        data['video_S'] = int(match.group(1))
        data['video_A'] = int(match.group(2))
        data['video_B'] = int(match.group(3))
    
    match = re.search(r'社区[：:]\s*S级(\d+)部.*?A级(\d+)部.*?B级(\d+)部', content)
    if match:
        data['community_S'] = int(match.group(1))
        data['community_A'] = int(match.group(2))
        data['community_B'] = int(match.group(3))
    
    return data

def compare_data(today_data, yesterday_data, last_week_data):
    """生成对比报告"""
    report = []
    report.append(f"📊 {today} 数据对比分析")
    report.append("")
    
    # 视频产出对比
    report.append("【视频产出对比】")
    if yesterday_data and 'video_total' in yesterday_data:
        diff = today_data.get('video_total', 0) - yesterday_data['video_total']
        sign = "+" if diff > 0 else ""
        report.append(f"  昨日（{yesterday_data['video_total']}部）→ 今日（{today_data.get('video_total', 'N/A')}部），{sign}{diff}")
    else:
        report.append(f"  昨日数据暂无")
    
    if last_week_data and 'video_total' in last_week_data:
        diff = today_data.get('video_total', 0) - last_week_data['video_total']
        sign = "+" if diff > 0 else ""
        report.append(f"  上周同期（{last_week_data.get('video_total', 'N/A')}部）→ 今日（{today_data.get('video_total', 'N/A')}部），{sign}{diff}")
    else:
        report.append(f"  上周同期数据暂无")
    
    report.append("")
    
    # 社区产出对比
    report.append("【社区产出对比】")
    if yesterday_data and 'community_total' in yesterday_data:
        diff = today_data.get('community_total', 0) - yesterday_data['community_total']
        sign = "+" if diff > 0 else ""
        report.append(f"  昨日（{yesterday_data.get('community_total', 'N/A')}贴）→ 今日（{today_data.get('community_total', 'N/A')}贴），{sign}{diff}")
    else:
        report.append(f"  昨日数据暂无")
    
    if last_week_data and 'community_total' in last_week_data:
        diff = today_data.get('community_total', 0) - last_week_data['community_total']
        sign = "+" if diff > 0 else ""
        report.append(f"  上周同期（{last_week_data.get('community_total', 'N/A')}贴）→ 今日（{today_data.get('community_total', 'N/A')}贴），{sign}{diff}")
    else:
        report.append(f"  上周同期数据暂无")
    
    report.append("")
    
    # 个人产出对比
    report.append("【个人产出对比（视频）】")
    people = ['李易', '淼淼', '王汪', '秋刀鱼', '秋千', '阔落', '熙门']
    for person in people:
        today_val = today_data.get(person, 0)
        yesterday_val = yesterday_data.get(person, 0) if yesterday_data else 0
        last_week_val = last_week_data.get(person, 0) if last_week_data else 0
        
        diff_yesterday = today_val - yesterday_val
        diff_week = today_val - last_week_val
        
        sign_y = "+" if diff_yesterday > 0 else ""
        sign_w = "+" if diff_week > 0 else ""
        
        report.append(f"  {person}: 今日{today_val}部, 昨日{sign_y}{diff_yesterday}, 上周同期{sign_w}{diff_week}")
    
    return "\n".join(report)

def main():
    print("开始数据对比分析...")
    
    today_data = parse_daily_report(today)
    yesterday_data = parse_daily_report(yesterday)
    last_week_data = parse_daily_report(last_week)
    
    if not today_data:
        print(f"今日（{today}）数据未找到")
        return
    
    print(f"今日数据: 视频{today_data.get('video_total', 'N/A')}部, 社区{today_data.get('community_total', 'N/A')}贴")
    
    if yesterday_data:
        print(f"昨日数据: 视频{yesterday_data.get('video_total', 'N/A')}部, 社区{yesterday_data.get('community_total', 'N/A')}贴")
    
    if last_week_data:
        print(f"上周同期: 视频{last_week_data.get('video_total', 'N/A')}部, 社区{last_week_data.get('community_total', 'N/A')}贴")
    
    # 生成对比报告
    report = compare_data(today_data, yesterday_data, last_week_data)
    print("")
    print(report)
    
    # 保存报告
    report_file = os.path.join(MEMORY_DIR, f"对比报告-{today}.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# {today} 数据对比分析报告\n\n")
        f.write(report)
    print(f"\n报告已保存至: {report_file}")

if __name__ == "__main__":
    main()
