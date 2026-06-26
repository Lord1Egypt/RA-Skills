#!/usr/bin/env python3
"""
每日进化脚本 v2.0
每天22:00执行，自动总结当天讨论内容并更新记忆
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
DATA_DIR = WORKSPACE / "data"
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = DATA_DIR / "evolution-reports"

def get_freshchat_history():
    """获取飞书今日消息"""
    try:
        # 使用 OpenClaw CLI 获取今日会话消息
        result = subprocess.run(
            ["openclaw", "chat", "history", "--today", "--limit", "100", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WORKSPACE)
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"  ⚠️ 获取飞书消息失败: {e}")
    return []

def get_session_history():
    """获取当前session的历史消息"""
    try:
        # 尝试从 sessions 获取历史
        result = subprocess.run(
            ["openclaw", "sessions", "list", "--active", "--message-limit", "50"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            # 解析会话列表
            return []
    except Exception as e:
        print(f"  ⚠️ 获取session历史失败: {e}")
    return []

def load_today_memory():
    """加载今日记忆"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{today}.md"
    
    if memory_file.exists():
        with open(memory_file, encoding='utf-8') as f:
            return f.read()
    return ""

def save_today_memory(content):
    """保存今日记忆"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{today}.md"
    
    with open(memory_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✅ 已更新: {memory_file.name}")

def extract_topics(memory_text):
    """从记忆文件中提取话题"""
    topics = []
    lines = memory_text.split('\n')
    current_topic = None
    current_items = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            if current_topic:
                topics.append({"title": current_topic, "items": current_items})
            current_topic = line.replace('## ', '')
            current_items = []
        elif line.startswith('### '):
            if current_topic:
                topics.append({"title": current_topic, "items": current_items})
            current_topic = line.replace('### ', '')
            current_items = []
        elif line.startswith('- '):
            current_items.append(line[2:])
    
    if current_topic:
        topics.append({"title": current_topic, "items": current_items})
    
    return topics

def summarize_topics(topics):
    """生成话题总结"""
    if not topics:
        return "今日暂无讨论记录"
    
    summary_parts = []
    for topic in topics:
        if topic['items']:
            summary_parts.append(f"### {topic['title']}")
            for item in topic['items'][:3]:  # 限制每话题3条
                summary_parts.append(f"- {item}")
            summary_parts.append("")
    
    return "\n".join(summary_parts)

def load_longterm_memory():
    """加载长期记忆"""
    memory_file = WORKSPACE / "MEMORY.md"
    if memory_file.exists():
        with open(memory_file, encoding='utf-8') as f:
            return f.read()
    return ""

def update_longterm_memory(today_summary):
    """更新长期记忆"""
    memory_file = WORKSPACE / "MEMORY.md"
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 读取现有内容
    existing = load_longterm_memory()
    
    # 添加今日总结
    new_section = f"\n## {today} 讨论要点\n\n{today_summary}\n"
    
    if "## 讨论要点" in existing:
        # 插入到"讨论要点"部分后面
        existing = existing.replace("## 讨论要点\n", "## 讨论要点" + new_section)
    else:
        existing += new_section
    
    with open(memory_file, 'w', encoding='utf-8') as f:
        f.write(existing)
    
    print(f"  ✅ 已更新 MEMORY.md")

def generate_report():
    """生成进化报告"""
    print(f"\n🧬 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] 每日进化")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 加载今日记忆
    print("[1/4] 加载今日记忆...")
    today_memory = load_today_memory()
    topics = extract_topics(today_memory)
    print(f"  - 发现 {len(topics)} 个话题")
    
    # 2. 生成总结
    print("[2/4] 生成话题总结...")
    summary = summarize_topics(topics)
    if summary == "今日暂无讨论记录":
        print("  - 今日暂无讨论记录")
    else:
        # 保存到记忆文件
        if not today_memory.strip():
            # 首次写入
            save_today_memory(f"# {today} 讨论记录\n\n{summary}")
        else:
            # 已存在则追加
            save_today_memory(today_memory + f"\n\n---\n{summary}")
    
    # 3. 更新长期记忆
    print("[3/4] 更新长期记忆...")
    update_longterm_memory(summary)
    
    # 4. 生成报告文件
    print("[4/4] 生成进化报告...")
    report = {
        "date": today,
        "topics_count": len(topics),
        "summary": summary[:500],  # 截取前500字符
        "generated_at": datetime.now().isoformat()
    }
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / f"evolution-{today}.json"
    with open(report_file, "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 进化完成!")
    print(f"   - 话题: {len(topics)}个")
    print(f"   - 报告: {report_file.name}")
    
    return report

if __name__ == "__main__":
    generate_report()
