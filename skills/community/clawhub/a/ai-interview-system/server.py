#!/usr/bin/env python3
"""
Web Viewer 后端服务
直接读取 OpenClaw agent 的 session 文件
"""
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# 配置
PORT = 8091
SESSION_DIR = Path.home() / ".openclaw" / "agents"

def get_available_agents():
    """获取所有可用的 agent"""
    agents_dir = SESSION_DIR
    if not agents_dir.exists():
        return []
    
    agents = []
    for item in agents_dir.iterdir():
        if item.is_dir() and (item / "sessions").exists():
            agents.append(item.name)
    
    return sorted(agents)

def get_latest_session(agent_name):
    """获取最新的 session 文件"""
    agent_dir = SESSION_DIR / agent_name / "sessions"
    if not agent_dir.exists():
        return None
    
    sessions = list(agent_dir.glob("*.jsonl"))
    if not sessions:
        return None
    
    latest = max(sessions, key=lambda p: p.stat().st_mtime)
    return latest

def parse_session_messages(session_file):
    """解析 session 文件，提取对话"""
    messages = []
    
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    
                    if obj.get('type') != 'message':
                        continue
                    
                    msg = obj.get('message', {})
                    role = msg.get('role', '')
                    content = msg.get('content', '')
                    
                    # 解析内容
                    text = ''
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict):
                                if c.get('type') == 'text':
                                    text += c.get('text', '')
                            elif isinstance(c, str):
                                text += c
                    elif isinstance(content, str):
                        text = content
                    
                    if not text:
                        continue
                    
                    # 跳过系统消息和元数据
                    if 'System:' in text[:100]:
                        continue
                    if 'Conversation info' in text:
                        continue
                    if text.startswith('{') and '"runId"' in text:
                        continue
                    if text.startswith('{') and '"count":' in text:
                        continue
                    if text.startswith('{') and '"results":' in text:
                        continue
                    if 'ANNOUNCE_SKIP' in text:
                        continue
                    
                    text = text.strip()
                    # 去掉长度限制，让消息完全显示
                    
                    timestamp = obj.get('timestamp', '')
                    time_str = timestamp[11:19] if timestamp else ''
                    
                    messages.append({
                        'content': text,
                        'time': time_str
                    })
                    
                except (json.JSONDecodeError, KeyError):
                    continue
    except Exception as e:
        print(f"Error reading {session_file}: {e}")
    
    return messages

def get_conversations(agent1, agent2):
    """获取两个 agent 的对话"""
    result = {
        'agent-1': [],
        'agent-2': []
    }
    
    session1 = get_latest_session(agent1)
    if session1:
        result['agent-1'] = parse_session_messages(session1)
        print(f"{agent1}: {session1.name} ({len(result['agent-1'])} msgs)")
    
    session2 = get_latest_session(agent2)
    if session2:
        result['agent-2'] = parse_session_messages(session2)
        print(f"{agent2}: {session2.name} ({len(result['agent-2'])} msgs)")
    
    return result

def clear_conversations(agent1, agent2):
    """清空指定 agent 的对话记录"""
    cleared = []
    
    for agent in [agent1, agent2]:
        agent_dir = SESSION_DIR / agent / "sessions"
        if agent_dir.exists():
            sessions = list(agent_dir.glob("*.jsonl"))
            for s in sessions:
                try:
                    s.unlink()
                    cleared.append(agent)
                    print(f"已删除 {agent} 的会话: {s.name}")
                except Exception as e:
                    print(f"删除失败: {e}")
    
    return cleared

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        if path == '/api/agents':
            # 返回可用 agent 列表
            agents = get_available_agents()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'agents': agents}).encode())
            
        elif path == '/api/conversations':
            # 返回对话
            agent1 = params.get('agent1', [''])[0]
            agent2 = params.get('agent2', [''])[0]
            
            if not agent1 or not agent2:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing agent1 or agent2'}).encode())
                return
            
            convos = get_conversations(agent1, agent2)
            
            # 合并消息
            all_msgs = []
            msgs1 = convos.get('agent-1', [])
            msgs2 = convos.get('agent-2', [])
            
            max_len = max(len(msgs1), len(msgs2))
            for i in range(max_len):
                if i < len(msgs2):
                    all_msgs.append({
                        'from': 'agent-2',
                        'content': msgs2[i]['content'],
                        'time': msgs2[i]['time']
                    })
                if i < len(msgs1):
                    all_msgs.append({
                        'from': 'agent-1',
                        'content': msgs1[i]['content'],
                        'time': msgs1[i]['time']
                    })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'messages': all_msgs,
                'stats': {
                    agent1: len(msgs1),
                    agent2: len(msgs2)
                }
            }).encode())
            
        elif path == '/api/clear':
            # 清空对话
            agent1 = params.get('agent1', [''])[0]
            agent2 = params.get('agent2', [''])[0]
            
            if not agent1 or not agent2:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing agent1 or agent2'}).encode())
                return
            
            cleared = clear_conversations(agent1, agent2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'cleared': cleared
            }).encode())
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    public_dir = Path(__file__).parent / "public"
    os.chdir(public_dir)
    
    server = HTTPServer(('', PORT), Handler)
    print(f"=== Web Viewer 后端 ===")
    print(f"地址: http://localhost:{PORT}")
    print(f"按 Ctrl+C 停止\n")
    
    server.serve_forever()

if __name__ == '__main__':
    main()
