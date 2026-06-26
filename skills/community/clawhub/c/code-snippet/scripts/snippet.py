#!/usr/bin/env python3
"""
Code Snippet - 代码片段收藏夹
"""
import os
import sys
import json
import argparse
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.code_snippets.json")

def load_snippets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_snippets(snippets):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(snippets, f, ensure_ascii=False, indent=2)

def cmd_add(args):
    snippets = load_snippets()
    
    snippet = {
        "id": len(snippets) + 1,
        "title": args.title,
        "code": args.code,
        "language": args.lang or "text",
        "tags": args.tag or [],
        "created_at": datetime.now().isoformat(),
    }
    
    snippets.append(snippet)
    save_snippets(snippets)
    
    print(f"✅ 已添加: {args.title}")

def cmd_search(args):
    snippets = load_snippets()
    query = args.query.lower()
    
    results = [
        s for s in snippets 
        if query in s["title"].lower() or query in s.get("code", "").lower()
    ]
    
    if not results:
        print(f"❌ 未找到匹配")
        return
    
    print(f"🔍 找到 {len(results)} 个结果:")
    for s in results:
        print(f"\n#{s['id']} {s['title']} [{s['language']}]")
        print(f"   {s.get('code', '')[:80]}")

def cmd_list(args):
    snippets = load_snippets()
    
    if not snippets:
        print("📭 暂无代码片段")
        return
    
    tag_filter = args.tag
    
    print("📋 代码片段列表:")
    print("=" * 60)
    
    for s in snippets:
        if tag_filter and tag_filter not in s.get("tags", []):
            continue
        tags = ", ".join(s.get("tags", [])) or "-"
        print(f"#{s['id']} {s['title']} [{s['language']}] 标签: {tags}")

def cmd_get(args):
    snippets = load_snippets()
    snippet = next((s for s in snippets if s["id"] == args.id), None)
    
    if not snippet:
        print(f"❌ 未找到片段 #{args.id}")
        return
    
    print(f"📌 {snippet['title']}")
    print(f"语言: {snippet['language']}")
    print(f"标签: {', '.join(snippet.get('tags', []))}")
    print()
    print(snippet["code"])
    print()
    
    # 复制到剪贴板
    if args.copy:
        try:
            import subprocess
            subprocess.run(["xclip", "-selection", "clipboard"], 
                         input=snippet["code"].encode(), check=True)
            print("✅ 已复制到剪贴板")
        except:
            pass

def cmd_delete(args):
    snippets = load_snippets()
    snippets = [s for s in snippets if s["id"] != args.id]
    save_snippets(snippets)
    print(f"✅ 已删除 #{args.id}")

def main():
    parser = argparse.ArgumentParser(description="Code Snippet")
    subparsers = parser.add_subparsers()
    
    p_add = subparsers.add_parser("add", help="添加片段")
    p_add.add_argument("title", help="标题")
    p_add.add_argument("--code", required=True, help="代码")
    p_add.add_argument("--lang", "-l", help="语言")
    p_add.add_argument("--tag", "-t", action="append", help="标签")
    p_add.set_defaults(func=cmd_add)
    
    p_search = subparsers.add_parser("search", help="搜索")
    p_search.add_argument("query", help="关键词")
    p_search.set_defaults(func=cmd_search)
    
    p_list = subparsers.add_parser("list", help="列出")
    p_list.add_argument("--tag", "-t", help="标签过滤")
    p_list.set_defaults(func=cmd_list)
    
    p_get = subparsers.add_parser("get", help="查看/复制")
    p_get.add_argument("id", type=int, help="片段ID")
    p_get.add_argument("--copy", action="store_true", help="复制到剪贴板")
    p_get.set_defaults(func=cmd_get)
    
    p_del = subparsers.add_parser("delete", help="删除")
    p_del.add_argument("id", type=int, help="片段ID")
    p_del.set_defaults(func=cmd_delete)
    
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
