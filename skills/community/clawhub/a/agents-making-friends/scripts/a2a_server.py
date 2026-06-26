#!/usr/bin/env python3
"""
A2A Server - Expose OpenClaw as A2A service

Usage:
    python a2a_server.py --port 8080 [--token required-token]

Example:
    python a2a_server.py --port 8080
    python a2a_server.py --port 8080 --token my-secret-token
"""

import sys
import json
import argparse
import subprocess
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional


class OpenClawA2AHandler(BaseHTTPRequestHandler):
    """A2A Protocol HTTP Request Handler"""
    
    agent_name = "OpenClaw Agent"
    agent_description = "OpenClaw Personal AI Assistant"
    required_token: Optional[str] = None
    
    def log_message(self, format, *args):
        print(f"[A2A] {args[0]}")
    
    def send_json_response(self, data: Dict[str, Any], status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def check_auth(self) -> bool:
        if not self.required_token:
            return True
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:] == self.required_token
        return False
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        if not self.check_auth():
            self.send_json_response({"error": "Unauthorized"}, 401)
            return
        
        # Agent Card endpoint
        if self.path in ['/.well-known/agent.json', '/agent-card', '/a2a/agent-card']:
            self.send_json_response(self.get_agent_card())
            return
        
        # Health check
        if self.path == '/health':
            self.send_json_response({"status": "ok", "service": "a2a-server"})
            return
        
        self.send_json_response({"error": "Not found"}, 404)
    
    def do_POST(self):
        if not self.check_auth():
            self.send_json_response({"error": "Unauthorized"}, 401)
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            request = json.loads(body)
        except json.JSONDecodeError:
            self.send_json_response({
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": "Parse error"},
                "id": None
            })
            return
        
        response = self.handle_jsonrpc(request)
        self.send_json_response(response)
    
    def get_agent_card(self) -> Dict[str, Any]:
        return {
            "name": self.agent_name,
            "description": self.agent_description,
            "url": f"http://{self.headers.get('Host', 'localhost:8080')}/a2a",
            "capabilities": {
                "streaming": False,
                "pushNotifications": False
            },
            "skills": [
                {"name": "chat", "description": "Conversational capability"},
                {"name": "execute", "description": "Execute commands"}
            ],
            "authentication": {
                "schemes": ["Bearer"] if self.required_token else []
            }
        }
    
    def handle_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get('method', '')
        params = request.get('params', {})
        request_id = request.get('id', '1')
        
        if method == 'message/send':
            return self.handle_message_send(params, request_id)
        elif method == 'task/get':
            return self.handle_task_get(params, request_id)
        elif method == 'task/list':
            return self.handle_task_list(params, request_id)
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: {method}"},
                "id": request_id
            }
    
    def handle_message_send(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        message = params.get('message', {})
        parts = message.get('parts', [])
        
        # Extract text
        text = ""
        for part in parts:
            if part.get('type') == 'text':
                text = part.get('text', '')
                break
        
        if not text:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "No text in message"},
                "id": request_id
            }
        
        # Call OpenClaw agent
        print(f"[A2A] Received: {text}")
        
        try:
            result = subprocess.run(
                ['openclaw', 'agent', '--agent', 'main', '--message', text, '--json'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                try:
                    agent_response = json.loads(result.stdout)
                    response_text = agent_response.get('content', result.stdout)
                except json.JSONDecodeError:
                    response_text = result.stdout
            else:
                response_text = f"Error: {result.stderr}"
            
            print(f"[A2A] Response: {response_text[:100]}...")
            
        except subprocess.TimeoutExpired:
            response_text = "Error: Agent timeout"
        except Exception as e:
            response_text = f"Error: {str(e)}"
        
        return {
            "jsonrpc": "2.0",
            "result": {
                "id": f"task-{os.urandom(8).hex()}",
                "status": "completed",
                "artifacts": [
                    {"parts": [{"type": "text", "text": response_text}]}
                ]
            },
            "id": request_id
        }
    
    def handle_task_get(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        task_id = params.get('id', '')
        return {
            "jsonrpc": "2.0",
            "result": {"id": task_id, "status": "completed"},
            "id": request_id
        }
    
    def handle_task_list(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "result": {"tasks": []},
            "id": request_id
        }


def main():
    parser = argparse.ArgumentParser(description='A2A Server for OpenClaw Agent')
    parser.add_argument('--port', type=int, default=8080, help='Server port (default: 8080)')
    parser.add_argument('--token', type=str, help='Bearer Token (optional)')
    parser.add_argument('--name', type=str, default='OpenClaw Agent', help='Agent name')
    parser.add_argument('--description', type=str, default='OpenClaw Personal AI Assistant', help='Agent description')
    args = parser.parse_args()
    
    OpenClawA2AHandler.agent_name = args.name
    OpenClawA2AHandler.agent_description = args.description
    OpenClawA2AHandler.required_token = args.token
    
    server = HTTPServer(('0.0.0.0', args.port), OpenClawA2AHandler)
    
    print(f"🦞 A2A Server started!")
    print(f"📍 URL: http://0.0.0.0:{args.port}")
    print(f"📋 Agent Card: http://0.0.0.0:{args.port}/.well-known/agent.json")
    print(f"🔐 Auth: {'Bearer Token: ' + args.token if args.token else 'No auth'}")
    print(f"\nPress Ctrl+C to stop...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        server.shutdown()


if __name__ == "__main__":
    main()