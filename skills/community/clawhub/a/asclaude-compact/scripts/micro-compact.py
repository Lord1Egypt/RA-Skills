#!/usr/bin/env python3
"""
Micro Compact - 基于时间的微压缩

原理：
当距离最后一条助手消息超过阈值（默认 30 分钟），
清理旧的工具结果内容，只保留最近 N 个。

收益：
- 节省 20-40% token
- 零 API 成本
- 保持工具调用历史（模型知道"做过什么"）

用法：
  python3 micro-compact.py [session-id]
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# ============ 配置 ============

CONFIG = {
    'enabled': True,
    'gap_threshold_minutes': 30,  # 时间阈值（分钟）
    'keep_recent': 2,             # 保留最近 N 个工具结果
    'workspace_dir': os.path.expanduser('~/.openclaw/workspace'),
    'sessions_dir': os.path.expanduser('~/.openclaw/agents/main/sessions'),
}

# 可压缩的工具列表
COMPACTABLE_TOOLS = {
    'read', 'write', 'edit', 'exec', 'grep', 'glob',
    'web_fetch', 'web_search', 'image',
}

CLEARED_MESSAGE = '[Old tool result content cleared]'


# ============ 核心逻辑 ============

def find_latest_session():
    """找到最新的会话"""
    sessions_dir = Path(CONFIG['sessions_dir'])
    if not sessions_dir.exists():
        return None
    
    sessions_files = list(sessions_dir.glob("*.jsonl"))
    if not sessions_files:
        return None
    
    latest_session = max(sessions_files, key=lambda f: f.stat().st_mtime)
    return latest_session.stem


def read_session(session_id):
    """读取会话文件"""
    sessions_dir = Path(CONFIG['sessions_dir'])
    session_file = sessions_dir / f"{session_id}.jsonl"
    
    if not session_file.exists():
        return None
    
    messages = []
    with open(session_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if data.get('type') == 'message':
                    msg = data.get('message', {})
                    if msg:
                        messages.append({
                            'data': data,
                            'message': msg,
                        })
            except json.JSONDecodeError:
                continue
    
    return {
        'session_id': session_id,
        'messages': messages,
        'file_path': session_file,
    }


def estimate_token_count(text):
    """粗略估算 token 数"""
    if not text:
        return 0
    # 1 token ≈ 2.5 chars（中英文混合）
    return len(str(text)) / 2.5


def collect_compactable_tool_ids(messages):
    """收集所有可压缩工具的 tool_use IDs（按出现顺序）"""
    ids = []
    
    for item in messages:
        msg = item.get('message', {})
        if msg.get('role') == 'assistant':
            content = msg.get('content', [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'tool_use':
                        if block.get('name') in COMPACTABLE_TOOLS:
                            ids.append(block.get('id'))
    
    return ids


def execute_micro_compact(session_data):
    """执行时间触发 micro compact"""
    if not CONFIG['enabled']:
        print("⚠️  Micro Compact 已禁用")
        return None
    
    messages = session_data['messages']
    
    # 1. 找到最后一条助手消息
    last_assistant = None
    for item in reversed(messages):
        if item['message'].get('role') == 'assistant':
            last_assistant = item
            break
    
    if not last_assistant:
        print("⚠️  未找到助手消息")
        return None
    
    # 2. 计算时间差
    timestamp_str = last_assistant['data'].get('timestamp', '')
    if not timestamp_str:
        print("⚠️  未找到时间戳")
        return None
    
    try:
        last_timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(last_timestamp.tzinfo)
        gap_minutes = (now - last_timestamp).total_seconds() / 60
    except Exception as e:
        print(f"⚠️  时间解析失败: {e}")
        return None
    
    if gap_minutes < CONFIG['gap_threshold_minutes']:
        print(f"⚠️  时间间隔不足（{gap_minutes:.1f}min < {CONFIG['gap_threshold_minutes']}min）")
        return None
    
    print(f"✅ 触发条件满足：间隔 {gap_minutes:.1f} 分钟 > {CONFIG['gap_threshold_minutes']} 分钟")
    
    # 3. 收集可压缩工具 IDs
    compactable_ids = collect_compactable_tool_ids(messages)
    print(f"   找到 {len(compactable_ids)} 个可压缩工具调用")
    
    # 4. 确定保留和清理的工具
    keep_recent = max(1, CONFIG['keep_recent'])
    keep_set = set(compactable_ids[-keep_recent:]) if len(compactable_ids) >= keep_recent else set(compactable_ids)
    clear_set = set([id for id in compactable_ids if id not in keep_set])
    
    if not clear_set:
        print("ℹ️  没有需要清理的工具结果")
        return {
            'messages': messages,
            'was_compacted': False,
            'tokens_saved': 0,
            'cleared_count': 0,
        }
    
    print(f"   保留最近 {len(keep_set)} 个，清理 {len(clear_set)} 个")
    
    # 5. 清理旧工具结果
    tokens_saved = 0
    cleared_count = 0
    modified_messages = []
    
    for item in messages:
        msg = item['message']
        data = item['data']
        
        if msg.get('role') != 'user':
            modified_messages.append(item)
            continue
        
        content = msg.get('content', [])
        if not isinstance(content, list):
            modified_messages.append(item)
            continue
        
        touched = False
        new_content = []
        
        for block in content:
            if (block.get('type') == 'tool_result' and
                block.get('tool_use_id') in clear_set and
                block.get('content') != CLEARED_MESSAGE):
                
                # 估算节省的 token
                old_content = block.get('content', '')
                saved = estimate_token_count(old_content)
                tokens_saved += saved
                
                # 替换内容
                new_block = {**block, 'content': CLEARED_MESSAGE}
                new_content.append(new_block)
                touched = True
                cleared_count += 1
            else:
                new_content.append(block)
        
        if touched:
            # 更新消息
            new_data = {**data, 'message': {**msg, 'content': new_content}}
            modified_messages.append({
                'data': new_data,
                'message': new_data['message'],
            })
        else:
            modified_messages.append(item)
    
    if tokens_saved == 0:
        print("ℹ️  没有实际清理任何内容")
        return {
            'messages': messages,
            'was_compacted': False,
            'tokens_saved': 0,
            'cleared_count': 0,
        }
    
    print(f"✅ Micro Compact 完成！")
    print(f"   清理 {cleared_count} 个工具结果")
    print(f"   节省 ~{tokens_saved:.0f} tokens ({tokens_saved / estimate_token_count(str(len(messages) * 1000)) * 100:.1f}% 估算)")
    
    return {
        'messages': modified_messages,
        'was_compacted': True,
        'tokens_saved': tokens_saved,
        'cleared_count': cleared_count,
    }


def save_session(session_data, modified_messages):
    """保存修改后的会话"""
    session_file = session_data['file_path']
    
    # 备份原文件
    backup_file = session_file.with_suffix('.jsonl.backup')
    if session_file.exists():
        import shutil
        shutil.copy2(session_file, backup_file)
        print(f"   📦 备份原文件: {backup_file}")
    
    # 写入新文件
    with open(session_file, 'w', encoding='utf-8') as f:
        for item in modified_messages:
            f.write(json.dumps(item['data'], ensure_ascii=False) + '\n')
    
    print(f"   💾 会话已更新: {session_file}")


def main():
    # 解析参数
    session_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🌾 Micro Compact - 基于时间的微压缩\n")
    
    # 1. 找到目标会话
    if not session_id:
        print("未指定会话，查找最新会话...")
        session_id = find_latest_session()
        if not session_id:
            print("❌ 未找到任何会话")
            sys.exit(1)
        print(f"✅ 找到最新会话: {session_id}\n")
    else:
        print(f"🎯 目标会话: {session_id}\n")
    
    # 2. 读取会话
    print("📖 读取会话内容...")
    session_data = read_session(session_id)
    if not session_data:
        print(f"❌ 无法读取会话: {session_id}")
        sys.exit(1)
    
    print(f"   消息数: {len(session_data['messages'])}")
    print()
    
    # 3. 执行 micro compact
    print("⚙️  执行微压缩...")
    result = execute_micro_compact(session_data)
    
    if not result or not result['was_compacted']:
        print("\nℹ️  Micro Compact 未触发或无需清理")
        return
    
    # 4. 保存修改
    print("\n💾 保存修改后的会话...")
    save_session(session_data, result['messages'])
    
    # 5. 完成
    print("\n✅ Micro Compact 全部完成！")
    print(f"   清理 {result['cleared_count']} 个工具结果")
    print(f"   节省 ~{result['tokens_saved']:.0f} tokens")


if __name__ == "__main__":
    main()
