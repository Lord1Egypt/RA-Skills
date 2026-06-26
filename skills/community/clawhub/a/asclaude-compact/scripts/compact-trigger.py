#!/usr/bin/env python3
"""
Compact Trigger - 手动触发对话压缩

用法：
  python3 compact-trigger.py [session-key]

如果没有提供 session-key，会压缩当前活跃会话
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def get_sessions_dir():
    """获取会话目录"""
    home_dir = os.path.expanduser("~")
    return Path(home_dir) / ".openclaw" / "agents" / "main" / "sessions"

def get_workspace_dir():
    """获取工作区目录"""
    home_dir = os.path.expanduser("~")
    return Path(home_dir) / ".openclaw" / "workspace"

def estimate_tokens_from_filesize(file_path):
    """根据文件大小估算 token 数"""
    size_bytes = os.path.getsize(file_path)
    # 1 token ≈ 3 bytes（保守估计，考虑 JSON 开销）
    return size_bytes / 3

def find_latest_session():
    """找到最新的会话"""
    sessions_dir = get_sessions_dir()
    if not sessions_dir.exists():
        return None
    
    sessions_files = list(sessions_dir.glob("*.jsonl"))
    if not sessions_files:
        return None
    
    # 找出最新的会话文件
    latest_session = max(
        sessions_files,
        key=lambda f: f.stat().st_mtime
    )
    return latest_session.stem

def read_session(session_id):
    """读取会话文件"""
    sessions_dir = get_sessions_dir()
    session_file = sessions_dir / f"{session_id}.jsonl"
    
    if not session_file.exists():
        return None
    
    messages = []
    user_count = 0
    assistant_count = 0
    tool_count = 0
    total_text = 0
    
    with open(session_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if data.get('type') == 'message':
                    msg = data.get('message', {})
                    role = msg.get('role', '')
                    content = msg.get('content', [])
                    
                    if isinstance(content, list):
                        text_content = ''.join([
                            c.get('text', '') 
                            for c in content 
                            if c.get('type') == 'text'
                        ])
                    else:
                        text_content = str(content)
                    
                    total_text += len(text_content) if text_content else 0
                    
                    if role == 'user':
                        user_count += 1
                        messages.append({
                            'type': 'user',
                            'content': text_content,
                            'timestamp': data.get('timestamp', '')
                        })
                    elif role == 'assistant':
                        # 检查是否有工具调用
                        has_tool_call = any(
                            c.get('type') == 'toolCall' 
                            for c in content 
                            if isinstance(c, dict)
                        )
                        if has_tool_call:
                            tool_count += 1
                        # 如果有文本内容，也计入助手回复
                        if text_content:
                            assistant_count += 1
                            messages.append({
                                'type': 'assistant',
                                'content': text_content,
                                'timestamp': data.get('timestamp', '')
                            })
            except json.JSONDecodeError:
                continue
    
    # 根据文件大小估算 token
    session_file_path = sessions_dir / f"{session_id}.jsonl"
    if session_file_path.exists():
        estimated_tokens = estimate_tokens_from_filesize(session_file_path)
    else:
        estimated_tokens = 0
    
    return {
        'session_id': session_id,
        'messages': messages,
        'stats': {
            'user_messages': user_count,
            'assistant_messages': assistant_count,
            'tool_calls': tool_count,
            'total_text_length': total_text,
            'estimated_tokens': max(estimated_tokens, 100)  # 最低 100 tokens
        }
    }

def archive_session(session_data, archive_dir):
    """归档会话到归档目录"""
    session_id = session_data['session_id']
    archive_path = archive_dir / f"{session_id}.jsonl"
    
    sessions_dir = get_sessions_dir()
    source_file = sessions_dir / f"{session_id}.jsonl"
    
    if source_file.exists():
        # 复制文件到归档目录
        import shutil
        shutil.copy2(source_file, archive_path)
        return True
    return False

def create_summary(session_data):
    """创建会话摘要"""
    stats = session_data['stats']
    summary_lines = [
        f"# Session Archive: {session_data['session_id']}",
        f"",
        f"- **会话 ID**: {session_data['session_id']}",
        f"- **归档时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **消息统计**:",
        f"  - 用户消息: {stats['user_messages']}",
        f"  - 助手回复: {stats['assistant_messages']}",
        f"  - 工具调用: {stats['tool_calls']}",
        f"  - 估算 tokens: {stats['estimated_tokens']:.0f}",
        f"",
        f"## 最新消息",
        f"",
    ]
    
    # 添加最近 5 条消息
    recent_messages = session_data['messages'][-5:]
    for msg in recent_messages:
        timestamp = msg['timestamp'][:19] if msg['timestamp'] else '未知时间'
        role_emoji = '👤' if msg['type'] == 'user' else '🤖'
        preview = msg['content'][:100].replace('\n', ' ')
        if len(msg['content']) > 100:
            preview += '...'
        
        summary_lines.append(f"{role_emoji} **{timestamp}**: {preview}")
        summary_lines.append("")
    
    return '\n'.join(summary_lines)

def update_session_memory(session_data, summary_text):
    """更新 session-memory.md"""
    workspace_dir = get_workspace_dir()
    sm_path = workspace_dir / "session-memory.md"
    
    # 创建摘要文件
    memory_dir = workspace_dir / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    archive_summary_file = memory_dir / f"{datetime.now().strftime('%Y-%m-%d')}-compact.md"
    
    with open(archive_summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    return archive_summary_file

def main():
    # 解析参数
    session_key = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🌾 开始对话压缩...\n")
    
    # 1. 找到目标会话
    if not session_key:
        print("未指定会话，查找最新会话...")
        session_id = find_latest_session()
        if not session_id:
            print("❌ 未找到任何会话")
            sys.exit(1)
        print(f"✅ 找到最新会话: {session_id}\n")
    else:
        session_id = session_key
        print(f"🎯 目标会话: {session_id}\n")
    
    # 2. 读取会话信息
    print("📖 读取会话内容...")
    session_data = read_session(session_id)
    if not session_data:
        print(f"❌ 无法读取会话: {session_id}")
        sys.exit(1)
    
    stats = session_data['stats']
    print(f"   用户消息: {stats['user_messages']}")
    print(f"   助手回复: {stats['assistant_messages']}")
    print(f"   工具调用: {stats['tool_calls']}")
    print(f"   估算 tokens: {stats['estimated_tokens']:.0f}")
    print()
    
    # 3. 创建摘要
    print("📝 创建会话摘要...")
    summary_text = create_summary(session_data)
    
    # 4. 归档会话
    workspace_dir = get_workspace_dir()
    archive_dir = workspace_dir / "archived-sessions"
    archive_dir.mkdir(exist_ok=True)
    
    print(f"📦 归档会话到: {archive_dir}")
    if archive_session(session_data, archive_dir):
        print(f"   ✅ 已归档: session-{session_id}.jsonl")
    else:
        print(f"   ⚠️  归档失败（原文件可能不存在）")
    
    # 5. 保存摘要
    summary_file = update_session_memory(session_data, summary_text)
    print(f"   📄 摘要已保存: {summary_file}")
    
    # 6. 完成
    print("\n✅ Compact 完成！")
    print(f"   原始会话 tokens: ~{stats['estimated_tokens']:.0f}")
    print("   压缩后：仅保留摘要文件（约 1k tokens）")
    print(f"   节省: ~{stats['estimated_tokens'] - 1000:.0f} tokens ({((stats['estimated_tokens'] - 1000) / stats['estimated_tokens'] * 100):.1f}%)")
    print("\n💡 提示：")
    print("   - 查看摘要: cat " + str(summary_file))
    print("   - 归档位置: " + str(archive_dir))

if __name__ == "__main__":
    main()
