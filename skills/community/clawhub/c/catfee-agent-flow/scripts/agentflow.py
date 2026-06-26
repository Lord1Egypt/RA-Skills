#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AgentFlow 工作流管理系统 CLI 工具
调用 MCP: http://182.42.153.28:18900/api/mcp/sse

用法:
    python agentflow.py list_projects
    python agentflow.py create_project "项目名" "描述" "tag1,tag2"
    python agentflow.py get_project <projectId>
    python agentflow.py create_requirement <projectId> "需求标题" "P1"
    python agentflow.py list_requirements <projectId>
    python agentflow.py create_task <requirementId> "任务标题" "P1" "负责人"
    python agentflow.py transition <taskId/requirementId> "fromStatus" "toStatus" "操作人"
    python agentflow.py get_timeline <taskId>
    python agentflow.py search "关键词"
"""

import requests
import json
import sys
import time
import threading
from urllib.parse import urlencode

BASE_URL = "http://182.42.153.28:18900"
SSE_URL = f"{BASE_URL}/api/mcp/sse"
MSG_URL = f"{BASE_URL}/api/mcp/message"

session_id = None
session_lock = threading.Lock()
response_received = threading.Event()
response_data = None
response_error = None

def sse_listener():
    global session_id, response_data, response_error
    try:
        with requests.get(SSE_URL, stream=True, timeout=60) as resp:
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode('utf-8', errors='ignore')
                    if decoded.startswith('data:'):
                        data_str = decoded[5:].strip()
                        if 'sessionId=' in data_str:
                            sid = data_str.split('sessionId=')[1].split('&')[0]
                            with session_lock:
                                session_id = sid
                        elif '[DONE]' in data_str:
                            response_received.set()
                        else:
                            try:
                                parsed = json.loads(data_str)
                                if 'result' in parsed:
                                    response_data = parsed['result']
                                    response_received.set()
                                elif 'error' in parsed:
                                    response_error = parsed['error']
                                    response_received.set()
                            except:
                                pass
    except Exception as e:
        response_error = str(e)
        response_received.set()

def wait_session():
    global session_id
    for _ in range(30):
        with session_lock:
            if session_id:
                return session_id
        time.sleep(0.5)
    raise Exception("获取 sessionId 超时")

def post_request(method, params=None):
    global response_data, response_error
    response_data = None
    response_error = None
    response_received.clear()
    
    sid = [None]
    
    def sse_flow():
        global response_data, response_error
        try:
            req = requests.Request('GET', SSE_URL)
            prepared = req.prepare()
            s = requests.Session()
            resp = s.send(prepared, stream=True, timeout=60)
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode('utf-8', errors='ignore')
                    if 'sessionId=' in decoded and sid[0] is None:
                        sid[0] = decoded.split('sessionId=')[1].split('&')[0]
                    try:
                        d = json.loads(decoded[5:])
                        if 'result' in d:
                            response_data = d['result']
                            response_received.set()
                        elif 'error' in d:
                            response_error = d['error']
                            response_received.set()
                    except:
                        pass
                    if '[DONE]' in decoded:
                        break
            resp.close()
        except Exception as e:
            response_error = str(e)
            response_received.set()
    
    t = threading.Thread(target=sse_flow, daemon=True)
    t.start()
    
    # Wait for sessionId
    for _ in range(50):
        if sid[0]:
            break
        time.sleep(0.1)
    
    if not sid[0]:
        raise Exception("获取 sessionId 超时")
    
    # Post the JSON-RPC request
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    try:
        resp = requests.post(f"{MSG_URL}?sessionId={sid[0]}", json=body, timeout=30)
        resp.raise_for_status()
        resp.close()
    except Exception as e:
        raise Exception(f"请求失败: {e}")
    
    response_received.wait(timeout=30)
    
    if response_error:
        raise Exception(f"AgentFlow错误: {response_error}")
    return response_data

def format_result(data):
    """格式化输出"""
    if data is None:
        return "(无返回数据)"
    if isinstance(data, list):
        if not data:
            return "(空列表)"
        lines = []
        for item in data:
            if isinstance(item, dict):
                lines.append(json.dumps(item, ensure_ascii=False, indent=2))
            else:
                lines.append(str(item))
        return "\n".join(lines)
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False, indent=2)
    return str(data)

# --- Tools ---

def cmd_list_projects():
    result = post_request("tools/call", {
        "name": "list_projects",
        "arguments": {}
    })
    print(format_result(result))

def cmd_create_project(name, description="", tags=""):
    tags_arg = json.dumps(tags.split(",")) if tags else "[]"
    result = post_request("tools/call", {
        "name": "create_project",
        "arguments": {
            "name": name,
            "description": description,
            "tags": tags_arg
        }
    })
    print(format_result(result))

def cmd_get_project(projectId):
    result = post_request("tools/call", {
        "name": "get_project",
        "arguments": {"projectId": projectId}
    })
    print(format_result(result))

def cmd_create_requirement(projectId, title, priority="P1", description=""):
    result = post_request("tools/call", {
        "name": "create_requirement",
        "arguments": {
            "projectId": projectId,
            "title": title,
            "priority": priority,
            "description": description
        }
    })
    print(format_result(result))

def cmd_list_requirements(projectId):
    result = post_request("tools/call", {
        "name": "list_requirements",
        "arguments": {"projectId": projectId}
    })
    print(format_result(result))

def cmd_create_task(requirementId, title, priority="P1", assignee=""):
    result = post_request("tools/call", {
        "name": "create_task",
        "arguments": {
            "requirementId": requirementId,
            "title": title,
            "priority": priority,
            "assignee": assignee
        }
    })
    print(format_result(result))

def cmd_transition(taskId, fromStatus, toStatus, operator="猫二", note=""):
    result = post_request("tools/call", {
        "name": "transition",
        "arguments": {
            "taskId": taskId,
            "fromStatus": fromStatus,
            "toStatus": toStatus,
            "operator": operator,
            "note": note
        }
    })
    print(format_result(result))

def cmd_get_timeline(taskId):
    result = post_request("tools/call", {
        "name": "get_timeline",
        "arguments": {"taskId": taskId}
    })
    print(format_result(result))

def cmd_search(query):
    result = post_request("tools/call", {
        "name": "search",
        "arguments": {"query": query}
    })
    print(format_result(result))

def cmd_get_upload_url(entityType, entityId, filename):
    result = post_request("tools/call", {
        "name": "get_upload_url",
        "arguments": {
            "entityType": entityType,
            "entityId": entityId,
            "filename": filename
        }
    })
    print(format_result(result))

def cmd_upload_file(entityType, entityId, filepath):
    """完整文件上传流程：1.获取上传地址和字段 2.POST multipart/form-data"""
    import os
    if not os.path.exists(filepath):
        print(f"错误: 文件不存在: {filepath}")
        sys.exit(1)
    
    filename = os.path.basename(filepath)
    
    # Step 1: 获取上传地址和字段
    url_result = post_request("tools/call", {
        "name": "get_upload_url",
        "arguments": {
            "entityType": entityType,
            "entityId": entityId,
            "filename": filename
        }
    })
    
    if url_result is None:
        print("获取上传地址失败")
        sys.exit(1)
    
    # 解析返回结果：{'content': [{'text': '{"uploadUrl":..., "fields":...}'}]}
    try:
        content_list = url_result.get('content', [])
        if not content_list:
            print(f"获取上传地址失败: {url_result}")
            sys.exit(1)
        upload_info = json.loads(content_list[0].get('text', '{}'))
        upload_url = upload_info.get('uploadUrl', '/api/files/upload')
        if not upload_url.startswith('http'):
            upload_url = BASE_URL + upload_url
        fields = upload_info.get('fields', {})
    except Exception as e:
        print(f"解析上传地址失败: {e}")
        sys.exit(1)
    
    # Step 2: POST multipart/form-data
    with open(filepath, 'rb') as f:
        file_data = f.read()
    
    files = {
        'file': (filename, file_data, 'application/octet-stream')
    }
    for k, v in fields.items():
        files[k] = (None, str(v))
    
    post_resp = requests.post(upload_url, files=files, timeout=60)
    
    if post_resp.status_code in (200, 201):
        print(f"✅ 文件上传成功: {filename} ({len(file_data)} bytes)")
        try:
            print(f"   响应: {post_resp.json()}")
        except:
            print(f"   响应: {post_resp.text[:200]}")
    else:
        print(f"❌ 上传失败: HTTP {post_resp.status_code}")
        print(post_resp.text[:300])
        sys.exit(1)

def cmd_get_project_status(projectId):
    result = post_request("tools/call", {
        "name": "get_project_status",
        "arguments": {"projectId": projectId}
    })
    print(format_result(result))

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    try:
        if cmd == "list_projects":
            cmd_list_projects()
        elif cmd == "create_project":
            cmd_create_project(*args)
        elif cmd == "get_project":
            cmd_get_project(*args)
        elif cmd == "create_requirement":
            cmd_create_requirement(*args)
        elif cmd == "list_requirements":
            cmd_list_requirements(*args)
        elif cmd == "create_task":
            cmd_create_task(*args)
        elif cmd == "transition":
            cmd_transition(*args)
        elif cmd == "get_timeline":
            cmd_get_timeline(*args)
        elif cmd == "search":
            cmd_search(*args)
        elif cmd == "get_project_status":
            cmd_get_project_status(*args)
        elif cmd == "get_upload_url":
            cmd_get_upload_url(*args)
        elif cmd == "upload_file":
            cmd_upload_file(*args)
        else:
            print(f"未知命令: {cmd}")
            print(__doc__)
            sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
