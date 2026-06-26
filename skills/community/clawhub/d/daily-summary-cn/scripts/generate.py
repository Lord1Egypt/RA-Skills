#!/usr/bin/env python3
"""生成每日工作总结"""

import os
import sys
import sqlite3
import datetime
import shutil
from pathlib import Path

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")

def get_chrome_history(days=1):
    """读取 Chrome 历史"""
    history_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\History")
    return read_browser_history(history_path, days)

def get_edge_history(days=1):
    """读取 Edge 历史"""
    history_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History")
    return read_browser_history(history_path, days)

def read_browser_history(history_path, days=1):
    """读取浏览器历史记录"""
    if not os.path.exists(history_path):
        return []
    
    temp_path = history_path + f".tmp_{os.getpid()}"
    try:
        shutil.copy2(history_path, temp_path)
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        
        since = datetime.datetime.now() - datetime.timedelta(days=days)
        timestamp = int(since.timestamp())
        
        cursor.execute("""
            SELECT urls.url, urls.title, visits.visit_time 
            FROM urls 
            JOIN visits ON urls.id = visits.url
            WHERE visits.visit_time > ?
            ORDER BY visits.visit_time DESC
            LIMIT 50
        """, (timestamp * 1000000,))
        
        results = []
        for url, title, visit_time in cursor.fetchall():
            visit_dt = datetime.datetime.fromtimestamp(visit_time / 1000000)
            results.append({
                'url': url,
                'title': title or '',
                'time': visit_dt.strftime('%H:%M')
            })
        
        conn.close()
    except Exception as e:
        results = []
    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass
    
    return results

def get_today_memory():
    """读取今日 memory 文件"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    memory_file = os.path.join(MEMORY_DIR, f"{today}.md")
    
    if os.path.exists(memory_file):
        with open(memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def summarize_tasks(memory_content, browser_history):
    """生成一句话总结"""
    tasks = []
    
    # 从 memory 提取任务
    if memory_content:
        lines = memory_content.split('\n')
        for line in lines:
            if '###' in line and any(kw in line for kw in ['完成', '创建', '设置', '安装', '配置', '部署']):
                task = line.replace('###', '').strip()
                if task:
                    tasks.append(task)
    
    # 从浏览器历史提取关键访问
    key_sites = []
    seen = set()
    for item in browser_history[:10]:
        title = item.get('title', '')
        if title and title not in seen:
            # 过滤掉 OpenClaw 本地链接
            if '127.0.0.1' not in item.get('url', ''):
                seen.add(title)
                key_sites.append(title[:30])
    
    # 生成一句话
    if tasks:
        summary = "今日完成：" + " + ".join(tasks[:4])
    else:
        summary = "今日工作：处理日常任务"
    
    return summary

def main():
    print("=== 生成每日工作总结 ===\n")
    
    # 读取数据
    memory = get_today_memory()
    chrome_history = get_chrome_history()
    edge_history = get_edge_history()
    
    all_history = chrome_history + edge_history
    
    # 生成总结
    summary = summarize_tasks(memory, all_history)
    
    print(summary)
    print()
    
    # 写入 memory
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    memory_file = os.path.join(MEMORY_DIR, f"{today}.md")
    
    with open(memory_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## 工作总结\n{summary}\n")
    
    print(f"已保存到 {memory_file}")
    
    return summary

if __name__ == "__main__":
    main()
