#!/usr/bin/env python3
"""
ACP 子会话内容回写主会话脚本
读取 ACP 子会话的 transcript，以主会话格式追加到主会话 jsonl
这样 AIMA 平台拉取主会话时就能看到 ACP 子会话的内容

用法:
  python3 sync-acp-to-main.py <acp_session_id> <acp_agent> [main_session_id] [main_agent]

参数:
  acp_session_id  ACP 子会话的 UUID
  acp_agent       ACP agent 的 ID（如 cfuse, claude, codex 等），用于显示名称
  main_session_id 主会话的 UUID（可选，不传则自动找最新的主会话）
  main_agent      主会话 agent 的 ID（可选，默认从环境变量 AGENT_ID 或目录名推断）
"""
import sys
import json
import uuid
import os
from datetime import datetime, timezone

def gen_id():
    return uuid.uuid4().hex[:16]

def detect_main_agent():
    """自动检测主 agent ID"""
    # 1. 环境变量
    env_id = os.environ.get('AGENT_ID') or os.environ.get('OPENCLAW_AGENT_ID')
    if env_id:
        return env_id
    # 2. 从 workspace 路径推断
    cwd = os.getcwd()
    # 路径格式: ~/.openclaw/workspace-<agentId> 或 ~/.openclaw/workspace/<agentId>
    parts = cwd.split('/')
    for p in parts:
        if p.startswith('workspace-'):
            return p.replace('workspace-', '')
    # 3. 从 agents 目录找（有 sessions 子目录的）
    agents_dir = os.path.expanduser('~/.openclaw/agents/')
    if os.path.exists(agents_dir):
        for d in os.listdir(agents_dir):
            sessions_dir = os.path.join(agents_dir, d, 'sessions')
            if os.path.isdir(sessions_dir):
                # 排除 ACP agent（通常名字较短或特定）
                if d not in ('cfuse', 'claude', 'codex', 'gemini', 'opencode', 'droid', 'kilo'):
                    return d
    return 'xiaoling-qinfang'  # 最终兜底

def get_last_message_id(main_jsonl_path):
    """获取主会话最后一条消息的 id"""
    last_id = None
    with open(main_jsonl_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get('type') == 'message':
                    last_id = obj.get('id')
            except:
                continue
    return last_id

def extract_acp_messages(acp_jsonl_path):
    """提取 ACP 子会话中的 user + assistant 消息"""
    messages = []
    with open(acp_jsonl_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except:
                continue
            if obj.get('type') != 'message':
                continue
            msg = obj.get('message', {})
            role = msg.get('role')
            if role not in ('user', 'assistant'):
                continue
            content = msg.get('content', '')
            # 提取文本内容
            text_parts = []
            if isinstance(content, list):
                for c in content:
                    if c.get('type') == 'text':
                        text_parts.append(c.get('text', ''))
                    elif c.get('type') == 'toolCall':
                        text_parts.append(f"[调用工具: {c.get('name', 'unknown')}]")
                    elif c.get('type') == 'toolResult':
                        text_parts.append(f"[工具结果: {str(c.get('content', ''))[:200]}]")
            elif isinstance(content, str):
                text_parts.append(content)
            
            text = '\n'.join(text_parts)
            if text.strip():
                messages.append({'role': role, 'text': text})
    return messages

def build_main_message(role, text, parent_id, timestamp_iso, acp_agent='cfuse'):
    """构建主会话格式的消息"""
    msg_id = gen_id()
    content = [{'type': 'text', 'text': text}]
    
    entry = {
        'type': 'message',
        'id': msg_id,
        'parentId': parent_id,
        'timestamp': timestamp_iso,
        'message': {
            'id': '',
            'role': role,
            'content': content,
        }
    }
    
    if role == 'assistant':
        entry['message']['model'] = f'ACP-{acp_agent}'
        entry['message']['usage'] = {
            'input': 0, 'output': 0,
            'cacheRead': 0, 'cacheWrite': 0,
            'totalTokens': 0,
            'cost': {'input': 0, 'output': 0, 'cacheRead': 0, 'cacheWrite': 0, 'total': 0}
        }
    
    return entry, msg_id

def sync_acp_to_main(acp_session_id, acp_agent='cfuse', main_agent=None, main_session_id=None):
    """主函数：将 ACP 子会话内容回写到主会话"""
    
    if main_agent is None:
        main_agent = detect_main_agent()
    
    # 路径
    acp_jsonl = os.path.expanduser(f'~/.openclaw/agents/{acp_agent}/sessions/{acp_session_id}.jsonl')
    
    if main_session_id:
        main_jsonl = os.path.expanduser(f'~/.openclaw/agents/{main_agent}/sessions/{main_session_id}.jsonl')
    else:
        # 自动找主会话（最新的活跃会话）
        sessions_dir = os.path.expanduser(f'~/.openclaw/agents/{main_agent}/sessions/')
        sessions = []
        for f in os.listdir(sessions_dir):
            if f.endswith('.jsonl'):
                path = os.path.join(sessions_dir, f)
                sessions.append((os.path.getmtime(path), f))
        if not sessions:
            print("ERROR: 没有找到主会话", file=sys.stderr)
            return False
        sessions.sort(reverse=True)
        main_session_id = sessions[0][1].replace('.jsonl', '')
        main_jsonl = os.path.join(sessions_dir, sessions[0][1])
    
    if not os.path.exists(acp_jsonl):
        print(f"ERROR: ACP 子会话不存在: {acp_jsonl}", file=sys.stderr)
        return False
    if not os.path.exists(main_jsonl):
        print(f"ERROR: 主会话不存在: {main_jsonl}", file=sys.stderr)
        return False
    
    # 1. 获取主会话最后一条消息 id
    last_id = get_last_message_id(main_jsonl)
    if not last_id:
        print("ERROR: 主会话为空", file=sys.stderr)
        return False
    
    # 2. 提取 ACP 子会话消息
    acp_messages = extract_acp_messages(acp_jsonl)
    if not acp_messages:
        print("ACP 子会话没有有效消息", file=sys.stderr)
        return False
    
    # 3. 构建回写消息
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    entries = []
    current_parent = last_id
    
    # 先加一条标记消息
    marker_text = f"📋 **{acp_agent}推理过程** (session: {acp_session_id[:8]}...)"
    marker_entry, marker_id = build_main_message('assistant', marker_text, current_parent, now, acp_agent=acp_agent)
    entries.append(marker_entry)
    current_parent = marker_id
    
    # 逐条追加 ACP 消息
    for msg in acp_messages:
        role = msg['role']
        # 用 [xxx推理过程] 前缀区分，xxx 是具体 agent 名称
        prefix = f'[{acp_agent}推理过程]'
        text = f"**{prefix} {role}**\n\n{msg['text']}"
        entry, entry_id = build_main_message('assistant', text, current_parent, now, acp_agent=acp_agent)
        entries.append(entry)
        current_parent = entry_id
    
    # 4. 追加到主会话 jsonl
    with open(main_jsonl, 'a') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"✅ 回写完成: {len(entries)} 条消息已追加到主会话")
    print(f"   ACP 子会话: {acp_session_id[:12]}...")
    print(f"   主会话: {main_session_id[:12]}...")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: sync-acp-to-main.py <acp_session_id> <acp_agent> [main_session_id] [main_agent]")
        print("示例: sync-acp-to-main.py f935963c-b8dd-431c-9d85-85e0e5a41341 cfuse 44c3f987-f9ad-4a02-b107-768ae9f517d3")
        sys.exit(1)
    
    acp_sid = sys.argv[1]
    acp_agent = sys.argv[2]
    main_sid = sys.argv[3] if len(sys.argv) > 3 else None
    main_agent = sys.argv[4] if len(sys.argv) > 4 else None
    success = sync_acp_to_main(acp_sid, acp_agent=acp_agent, main_agent=main_agent, main_session_id=main_sid)
    sys.exit(0 if success else 1)
