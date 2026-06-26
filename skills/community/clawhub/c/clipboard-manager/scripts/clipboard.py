#!/usr/bin/env python3
"""
Clipboard Manager - 剪贴板历史管理
"""
import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

DATA_FILE = os.path.expanduser("~/.clipboard_history.json")
MAX_ITEMS = int(os.environ.get("CLIPBOARD_MAX", "100"))

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"items": [], "pinned": []}

def save_history(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_clipboard():
    """获取剪贴板内容"""
    try:
        # Linux
        result = subprocess.run(["xclip", "-selection", "clipboard", "-o"], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            return result.stdout
    except:
        pass
    
    try:
        # macOS
        result = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            return result.stdout
    except:
        pass
    
    return None

def set_clipboard(text):
    """设置剪贴板"""
    try:
        # Linux
        subprocess.run(["xclip", "-selection", "clipboard", "-i"], 
                     input=text.encode(), check=True)
        return True
    except:
        pass
    
    try:
        # macOS
        subprocess.run(["pbcopy"], input=text.encode(), check=True)
        return True
    except:
        pass
    
    return False

def monitor_clipboard():
    """监控剪贴板变化"""
    data = load_history()
    last_content = ""
    
    print("🔄 监控剪贴板变化... (Ctrl+C 退出)")
    print("=" * 50)
    
    while True:
        content = get_clipboard()
        
        if content and content != last_content and len(content.strip()) > 0:
            last_content = content
            
            # 添加到历史
            item = {
                "content": content[:500],  # 限制长度
                "time": datetime.now().isoformat(),
                "type": "text"
            }
            
            # 检查是否已存在
            existing = [i for i in data["items"] if i["content"] == content]
            if not existing:
                data["items"].insert(0, item)
                
                # 限制数量
                if len(data["items"]) > MAX_ITEMS:
                    data["items"] = data["items"][:MAX_ITEMS]
                
                save_history(data)
                
                # 显示
                preview = content[:60].replace("\n", " ")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {preview}...")
        
        time.sleep(1)

def cmd_history(args):
    data = load_history()
    items = data.get("items", [])
    
    limit = args.limit or 10
    
    print("📋 剪贴板历史")
    print("=" * 50)
    
    for i, item in enumerate(items[:limit], 1):
        preview = item["content"][:50].replace("\n", " ")
        timestamp = item.get("time", "")[:16]
        
        print(f"{i}. {preview}...")
        print(f"   {timestamp}")

def cmd_search(args):
    data = load_history()
    items = data.get("items", [])
    query = args.query.lower()
    
    results = [item for item in items if query in item["content"].lower()]
    
    print(f"🔍 搜索结果: {len(results)} 条")
    print("=" * 50)
    
    for i, item in enumerate(results[:10], 1):
        preview = item["content"][:50].replace("\n", " ")
        print(f"{i}. {preview}...")

def cmd_pin(args):
    data = load_history()
    index = args.index - 1
    
    items = data.get("items", [])
    
    if index < 0 or index >= len(items):
        print(f"❌ 无效索引")
        return
    
    item = items.pop(index)
    data["pinned"].append(item)
    save_history(data)
    
    print(f"✅ 已固定: {item['content'][:50]}...")

def cmd_paste(args):
    data = load_history()
    index = args.index - 1
    
    # 先查固定，再查历史
    all_items = data.get("pinned", []) + data.get("items", [])
    
    if index < 0 or index >= len(all_items):
        print(f"❌ 无效索引")
        return
    
    item = all_items[index]
    
    if set_clipboard(item["content"]):
        print(f"✅ 已复制到剪贴板")
    else:
        print(f"❌ 复制失败")

def cmd_clear(args):
    data = {"items": [], "pinned": []}
    save_history(data)
    print("✅ 已清空历史记录")

def main():
    parser = argparse.ArgumentParser(description="Clipboard Manager")
    subparsers = parser.add_subparsers()
    
    subparsers.add_parser("history", help="查看历史").set_defaults(func=cmd_history)
    subparsers.add_parser("monitor", help="监控剪贴板").set_defaults(func=lambda args: monitor_clipboard())
    
    p_search = subparsers.add_parser("search", help="搜索")
    p_search.add_argument("query", help="搜索关键词")
    p_search.set_defaults(func=cmd_search)
    
    p_pin = subparsers.add_parser("pin", help="固定")
    p_pin.add_argument("index", type=int, help="索引")
    p_pin.set_defaults(func=cmd_pin)
    
    p_paste = subparsers.add_parser("paste", help="粘贴")
    p_paste.add_argument("index", type=int, help="索引")
    p_paste.set_defaults(func=cmd_paste)
    
    subparsers.add_parser("clear", help="清空").set_defaults(func=cmd_clear)
    
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
