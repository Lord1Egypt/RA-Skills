#!/usr/bin/env python3
"""
cn-todo-today - 今日待办管理器
"""
import argparse
import json
import os
from datetime import datetime

TODO_FILE = os.path.expanduser('~/.cn_todo_today.json')

def load_todos():
    """加载待办"""
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'todos': [], 'completed': []}
    return {'todos': [], 'completed': []}

def save_todos(data):
    """保存待办"""
    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_todo(text):
    """添加待办"""
    data = load_todos()
    todo_id = len(data['todos']) + 1
    todo = {
        'id': todo_id,
        'text': text,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    data['todos'].append(todo)
    save_todos(data)
    print(f"✓ 已添加: {text}")

def list_todos():
    """列出待办"""
    data = load_todos()
    
    print(f"\n📋 今日待办 ({datetime.now().strftime('%Y-%m-%d')})")
    print("=" * 40)
    
    if not data['todos']:
        print("暂无待办")
        return
    
    for todo in data['todos']:
        print(f"{todo['id']}. ☐ {todo['text']}")
    
    # 显示已完成
    if data['completed']:
        print("\n✓ 已完成:")
        for todo in data['completed'][-5:]:
            print(f"   ✓ {todo['text']}")

def mark_done(todo_id):
    """标记完成"""
    data = load_todos()
    todo_id = int(todo_id)
    
    for i, todo in enumerate(data['todos']):
        if todo['id'] == todo_id:
            completed = data['todos'].pop(i)
            completed['completed'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            data['completed'].append(completed)
            save_todos(data)
            print(f"✓ 已完成: {completed['text']}")
            return
    
    print(f"未找到ID {todo_id}")

def delete_todo(todo_id):
    """删除待办"""
    data = load_todos()
    todo_id = int(todo_id)
    
    for i, todo in enumerate(data['todos']):
        if todo['id'] == todo_id:
            deleted = data['todos'].pop(i)
            save_todos(data)
            print(f"✗ 已删除: {deleted['text']}")
            return
    
    print(f"未找到ID {todo_id}")

def show_stats():
    """统计"""
    data = load_todos()
    total = len(data['todos']) + len(data['completed'])
    completed = len(data['completed'])
    
    print(f"\n📊 今日统计")
    print("=" * 40)
    print(f"总待办: {total}")
    print(f"已完成: {completed}")
    if total > 0:
        print(f"完成率: {completed/total*100:.1f}%")
    
    if data['completed']:
        print("\n✓ 已完成项目:")
        for todo in data['completed'][-5:]:
            print(f"   {todo['text']}")

def main():
    parser = argparse.ArgumentParser(description='今日待办管理器')
    parser.add_argument('action', choices=['add', 'list', 'done', 'delete', 'stats'], help='操作')
    parser.add_argument('--text', help='待办文本')
    parser.add_argument('--id', help='待办ID')
    
    args = parser.parse_args()
    
    if args.action == 'add':
        if not args.text:
            print("请输入待办内容: --text '内容'")
            return
        add_todo(args.text)
    
    elif args.action == 'list':
        list_todos()
    
    elif args.action == 'done':
        if not args.id:
            print("请指定ID: --id 1")
            return
        mark_done(args.id)
    
    elif args.action == 'delete':
        if not args.id:
            print("请指定ID: --id 1")
            return
        delete_todo(args.id)
    
    elif args.action == 'stats':
        show_stats()

if __name__ == '__main__':
    main()