#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 午盘预判跟踪分析报告 - 自动生成
每天上午收盘(11:05)发送，跟踪当前预判的准确率进展

功能：
1. 读取PREDICTION_TRACKER.md中的预判记录
2. 统计已验证/待验证的预判
3. 计算当前准确率
4. 生成Markdown报告
"""

import os
import re
import json
from datetime import datetime, date

WORKSPACE = "/home/sandbox/.openclaw/workspace"
TRACKER_PATH = os.path.join(WORKSPACE, "PREDICTION_TRACKER.md")
WATCHLIST_PATH = os.path.join(WORKSPACE, "skills/ai-xifu-caopan/config/watchlist.json")

def read_tracker():
    with open(TRACKER_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def parse_stats(content):
    """解析预判跟踪文件中的统计数据"""
    stats = {
        'stock': {'total': 0, 'verified': 0, 'correct': 0, 'partial': 0, 'wrong': 0, 'pending': 0},
        'future': {'total': 0, 'verified': 0, 'correct': 0, 'partial': 0, 'wrong': 0, 'pending': 0},
        'fund': {'total': 0, 'verified': 0, 'correct': 0, 'partial': 0, 'wrong': 0, 'pending': 0},
    }
    
    lines = content.split('\n')
    section = None
    
    for i, line in enumerate(lines):
        if '📈 股票预判记录' in line or '个股走势预判' in line:
            section = 'stock'
        elif '📉 期货预判记录' in line:
            section = 'future'
        elif '💰 基金预判记录' in line:
            section = 'fund'
        elif '## 四、预判统计' in line or '# 预判统计' in line:
            break
            
        if section and '|' in line and '—' not in line:
            # Count predictions (rows with | in a table)
            if section == 'stock' and '个股走势预判' in line:
                continue
            if section == 'future' and '期货走势预判' in line:
                continue
            if section == 'fund' and '基金走势预判' in line:
                continue
                
            cells = [c.strip() for c in line.split('|')]
            if len(cells) >= 7:
                # Check if it has a date entry (meaning it's a real prediction row)
                date_pattern = r'\d{4}-\d{2}-\d{2}'
                has_date = False
                for cell in cells:
                    if re.match(date_pattern, cell):
                        has_date = True
                        break
                
                if has_date:
                    stats[section]['total'] += 1
                    if '待验证' in line:
                        stats[section]['pending'] += 1
                    elif '完全准确' in line or '✅' in line:
                        stats[section]['correct'] += 1
                        stats[section]['verified'] += 1
                    elif '部分准确' in line or '⚠️' in line:
                        stats[section]['partial'] += 1
                        stats[section]['verified'] += 1
                    elif '不准确' in line or '❌' in line:
                        stats[section]['wrong'] += 1
                        stats[section]['verified'] += 1
    
    return stats

def calculate_accuracy(stats):
    """计算准确率"""
    all_verified = sum(s['verified'] for s in stats.values())
    all_score = sum(s['correct'] + s['partial'] * 0.5 for s in stats.values())
    all_total = sum(s['total'] for s in stats.values())
    
    return {
        'all_verified': all_verified,
        'all_score': all_score,
        'all_total': all_total,
        'accuracy': round(all_score / all_verified * 100, 2) if all_verified > 0 else 0
    }

def generate_midday_report():
    """生成午盘跟踪报告"""
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    weekday = today.weekday()
    
    # Check if it's a trading day (Mon-Fri)
    if weekday >= 5:
        return None  # Weekend, no report
    
    content = read_tracker()
    stats = parse_stats(content)
    accuracy_data = calculate_accuracy(stats)
    
    # Build report
    report = []
    report.append(f"📊 **午盘预判跟踪分析报告**")
    report.append(f"🕐 生成时间：{today_str} 11:05")
    report.append(f"")
    report.append(f"━━━━━━━━━━━━━━━━━━━━")
    report.append(f"")
    report.append(f"**📈 预判整体概览**")
    report.append(f"")
    report.append(f"| 类别 | 总预判 | 已验证 | 待验证 | 准确 | 部分准确 | 错误 |")
    report.append(f"|------|:-----:|:-----:|:-----:|:---:|:-------:|:---:|")
    
    for key, label in [('stock', '📈股票'), ('future', '📉期货'), ('fund', '💰基金')]:
        s = stats[key]
        report.append(f"| {label} | {s['total']} | {s['verified']} | {s['pending']} | {s['correct']} | {s['partial']} | {s['wrong']} |")
    
    report.append(f"| **合计** | **{accuracy_data['all_total']}** | **{accuracy_data['all_verified']}** | **—** | **—** | **—** | **—** |")
    report.append(f"")
    
    total_correct = sum(s['correct'] + s['partial'] for s in stats.values())
    total_wrong = sum(s['wrong'] for s in stats.values())
    
    if accuracy_data['all_verified'] > 0:
        report.append(f"**✅ 综合准确率：{accuracy_data['accuracy']}%**")
        report.append(f"")
        report.append(f"| 评级 | 说明 |")
        report.append(f"|------|------|")
        
        if accuracy_data['accuracy'] >= 80:
            report.append(f"| 🟢 优秀 | 准确率≥80%，模型表现良好 |")
        elif accuracy_data['accuracy'] >= 60:
            report.append(f"| 🟡 良好 | 准确率60%-80%，有提升空间 |")
        elif accuracy_data['accuracy'] >= 40:
            report.append(f"| 🟠 一般 | 准确率40%-60%，需要优化 |")
        else:
            report.append(f"| 🔴 较差 | 准确率<40%，需要大幅改进 |")
    else:
        report.append(f"⏳ 暂无已验证的预判数据")
    
    report.append(f"")
    report.append(f"**📋 待验证预判**")
    report.append(f"")
    
    # Extract pending predictions
    lines = content.split('\n')
    section = None
    pending_items = []
    
    for line in lines:
        if '📈 股票预判记录' in line or '个股走势预判' in line:
            section = 'stock'
        elif '📉 期货预判记录' in line:
            section = 'future'
        elif '💰 基金预判记录' in line:
            section = 'fund'
        elif '## 四、' in line or '## 五、' in line:
            section = None
            
        if section and '待验证' in line and '|' in line:
            cells = [c.strip() for c in line.split('|')]
            if len(cells) >= 8:
                date_str = cells[1] if len(cells) > 1 else ''
                name = cells[2] if len(cells) > 2 else ''
                code = cells[3] if len(cells) > 3 else ''
                pred_date = cells[4] if len(cells) > 4 else ''
                pred_dir = cells[5] if len(cells) > 5 else ''
                pending_items.append(f"• {date_str} {name}({code}) → 预判：{pred_dir}")
    
    if pending_items:
        for item in pending_items[:10]:  # Show max 10
            report.append(item)
        if len(pending_items) > 10:
            report.append(f"  ...还有{len(pending_items)-10}条待验证")
    else:
        report.append(f"暂无待验证的预判")
    
    report.append(f"")
    report.append(f"**💡 建议**")
    report.append(f"")
    
    if accuracy_data['all_verified'] > 0 and accuracy_data['accuracy'] < 50:
        report.append(f"⚠️ 当前准确率偏低，建议：")
        report.append(f"1. 检查最近错误预判的共同特征")
        report.append(f"2. 关注板块联动和资金流向")
        report.append(f"3. 减少对外盘单一因素的过度依赖")
    elif accuracy_data['all_verified'] > 0 and accuracy_data['accuracy'] >= 70:
        report.append(f"👍 准确率良好，继续保持当前分析框架")
    else:
        report.append(f"📝 积累更多数据后将提供详细建议")
    
    report.append(f"")
    report.append(f"━━━━━━━━━━━━━━━━━━━━")
    report.append(f"**媳妇智投Pro出品，必属精品**")
    
    return '\n'.join(report)

if __name__ == '__main__':
    report = generate_midday_report()
    if report:
        print(report)
    else:
        print("今日非交易日，跳过报告")
