#!/usr/bin/env python3
"""
EXWIND 魔兽数据挖掘监控脚本
每10分钟扫描一次，检测更新并推送到飞书
"""

import subprocess
import json
import re
import requests
import time
from datetime import datetime
from pathlib import Path

# 配置
STATE_FILE = Path("/tmp/exwind_state.json")
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
FEISHU_WEBHOOK = None  # 如果配置了 webhook 可用


def run_cmd(cmd: str, timeout: int = 30) -> tuple[bool, str]:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def close_browser():
    run_cmd('agent-browser close', 10)


def open_page(url: str) -> bool:
    run_cmd('agent-browser close', 10)
    time.sleep(1)
    success, _ = run_cmd(f'agent-browser open "{url}" --timeout 30000', 60)
    return success


def get_snapshot() -> str:
    success, output = run_cmd('agent-browser snapshot -c', 30)
    return output if success else ""


def load_state() -> dict:
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except:
        pass
    return {"seen_ids": [], "last_run": None}


def save_state(state: dict):
    state["seen_ids"] = state["seen_ids"][-500:]
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def parse_articles(snapshot: str) -> list:
    articles = []
    current = {}
    
    for line in snapshot.split('\n'):
        line = line.strip()
        
        if line in ['- text: 蓝帖', '- text: 热修', '- text: 新闻']:
            if current.get('title') and current.get('url'):
                articles.append(current)
            current = {'type': line.replace('- text: ', '')}
        
        if '- heading "' in line and '[level=3]' in line and current.get('type'):
            match = re.search(r'heading "([^"]+)"', line)
            if match:
                current['title'] = match.group(1)
        
        if '/url: /post/' in line and current.get('title'):
            match = re.search(r'/url: (/\S+)', line)
            if match:
                current['url'] = f"https://exwind.net{match.group(1)}"
                id_match = re.search(r'/post/(\w+)/(\d+)', current['url'])
                if id_match:
                    current['id'] = f"{id_match.group(1)}_{id_match.group(2)}"
        
        if line.startswith('- paragraph:') and current.get('url') and not current.get('summary'):
            s = line.replace('- paragraph:', '').strip().strip('"')
            current['summary'] = s[:150] + '...' if len(s) > 150 else s
        
        if line.startswith('- text: schedule ') and current.get('url'):
            current['time'] = line.replace('- text: schedule ', '')
    
    if current.get('title') and current.get('url'):
        articles.append(current)
    
    return articles


def filter_new(articles: list, state: dict) -> list:
    seen = set(state.get("seen_ids", []))
    new = []
    for a in articles:
        aid = a.get('id', '')
        if aid and aid not in seen:
            new.append(a)
            seen.add(aid)
    return new


def format_message(articles: list) -> str:
    """格式化飞书消息"""
    lines = [f"## 🔍 EXWIND 更新 ({datetime.now().strftime('%H:%M')})", ""]
    
    icons = {'蓝帖': '📘', '热修': '🔧', '新闻': '📰'}
    
    for i, a in enumerate(articles[:5]):  # 最多5条
        icon = icons.get(a.get('type', ''), '📄')
        lines.extend([
            f"### {icon} {a.get('type', '')}: {a['title'][:40]}",
            f"📅 {a.get('time', '')}",
            f"🔗 {a['url']}",
            "",
            a.get('summary', ''),
            "",
            "---"
        ])
    
    return '\n'.join(lines)


def send_to_feishu(message: str) -> bool:
    """发送到飞书（通过 stdout，让 agent 处理）"""
    # 输出 JSON，包含消息内容
    result = {
        "empty": False,
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "need_send": True
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return True


def main():
    print(f"[{datetime.now()}] EXWIND 监控...")
    
    state = load_state()
    
    if not open_page("https://exwind.net/"):
        print("打开页面失败")
        close_browser()
        return
    
    time.sleep(3)
    snapshot = get_snapshot()
    close_browser()
    
    if not snapshot:
        print("获取快照失败")
        return
    
    print(f"快照: {len(snapshot)} 字符")
    
    articles = parse_articles(snapshot)
    print(f"解析: {len(articles)} 条")
    
    new_articles = filter_new(articles, state)
    print(f"新文章: {len(new_articles)} 条")
    
    # 更新状态
    all_ids = list(set(state.get("seen_ids", []) + [a.get('id') for a in articles if a.get('id')]))
    state["seen_ids"] = all_ids
    state["last_run"] = datetime.now().isoformat()
    save_state(state)
    
    if not new_articles:
        print(json.dumps({"empty": True}))
        return
    
    # 格式化消息
    message = format_message(new_articles)
    
    # 发送
    send_to_feishu(message)


if __name__ == '__main__':
    main()
