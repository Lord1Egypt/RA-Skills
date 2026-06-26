#!/usr/bin/env python3
"""
Claude Code 代理服务器
- 接收 Anthropic Messages API 格式
- 转换为 OpenAI Chat Completions 格式
- 支持 SSE 流式传输
"""
import http.server
import json
import time
import requests

UPSTREAM_HOST = "api.53hk.cn"
UPSTREAM_PATH = "/v1/chat/completions"
API_KEY = "sk-4194e63b46b29886573888adcb69b5b10fcd41e8b9801f1ae66487c19d57a75a"
LISTEN_PORT = 4002
MAX_RETRIES = 3
BASE_WAIT_SECONDS = 10

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def anthropic_to_openai(body):
    """将 Anthropic API 格式转换为 OpenAI Chat Completions 格式"""
    messages = body.get("messages", [])
    
    # 转换消息格式
    openai_messages = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        
        # 处理 content 数组（Anthropic 格式）
        if isinstance(content, list):
            text_content = ""
            for block in content:
                if block.get("type") == "text":
                    text_content += block.get("text", "")
            content = text_content
        
        openai_messages.append({"role": role, "content": content})
    
    openai_body = {
        "model": "MiniMax-M2.7-highspeed",  # 强制使用这个模型，忽略客户端请求
        "messages": openai_messages,
        "stream": True,
        "max_tokens": body.get("max_tokens", 4096),
        "temperature": body.get("temperature", 0.7)
    }
    return openai_body

def openai_to_anthropic(openai_chunk, message_id, first_chunk=False):
    """将 OpenAI chunk 转换为 Anthropic SSE 事件"""
    events = []
    
    choice = openai_chunk.get("choices", [{}])[0]
    delta = choice.get("delta", {})
    content = delta.get("content", "")
    
    if first_chunk:
        # message_start 事件
        events.append(("message_start", {
            "type": "message_start",
            "message": {
                "id": message_id,
                "type": "message",
                "role": "assistant",
                "model": openai_chunk.get("model", ""),
                "content": [],
                "stop_reason": None,
                "usage": openai_chunk.get("usage", {})
            }
        }))
        
        # content_block_start 事件
        events.append(("content_block_start", {
            "type": "content_block_start",
            "index": 0,
            "content_block": {
                "type": "text",
                "text": ""
            }
        }))

    
    if content:
        # content_block_delta 事件
        events.append(("content_block_delta", {
            "type": "content_block_delta",
            "index": 0,
            "delta": {
                "type": "text_delta",
                "text": content
            }
        }))
    
    # 检查是否完成
    if choice.get("finish_reason"):
        # content_block_stop 事件
        events.append(("content_block_stop", {
            "type": "content_block_stop",
            "index": 0
        }))
        
        # message_delta 事件
        events.append(("message_delta", {
            "type": "message_delta",
            "delta": {
                "stop_reason": choice.get("finish_reason", "end_turn"),
                "usage": {"output_tokens": 0}
            }
        }))
        
        # message_stop 事件
        events.append(("message_stop", {
            "type": "message_stop"
        }))
    
    return events

def call_upstream_with_retry(url, headers, data, max_retries=MAX_RETRIES):
    """调用上游 API，支持重试（处理 429 错误）"""
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(url, json=data, headers=headers, stream=True, timeout=120)
            
            if r.status_code == 429:
                if attempt < max_retries:
                    wait_time = BASE_WAIT_SECONDS * (attempt + 1)
                    log(f"Rate limited (429), waiting {wait_time}s before retry... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    log(f"Rate limited (429), max retries ({max_retries}) exceeded")
            
            r.raise_for_status()
            return r
        
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None and e.response.status_code == 429 and attempt < max_retries:
                wait_time = BASE_WAIT_SECONDS * (attempt + 1)
                log(f"Rate limited (429), waiting {wait_time}s before retry... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            raise
    
    return None

from urllib.parse import urlparse

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        log(f"GET {self.path} (path: {path})")
        if path == "/v1/models":
            # 返回 Claude Code 期望的模型列表
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            models = {
                "data": [
                    {
                        "type": "model",
                        "id": "claude-sonnet-4-6",
                        "display_name": "Claude Sonnet 4.6"
                    },
                    {
                        "type": "model",
                        "id": "claude-opus-4-5",
                        "display_name": "Claude Opus 4.5"
                    },
                    {
                        "type": "model",
                        "id": "claude-haiku-4-5",
                        "display_name": "Claude Haiku 4.5"
                    },
                    {
                        "type": "model",
                        "id": "MiniMax-M2.7-highspeed",
                        "display_name": "MiniMax M2.7 Highspeed"
                    }
                ]
            }
            self.wfile.write(json.dumps(models).encode())
            return
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        log(f"POST {self.path} (path: {path})")
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length))
        log(f"Body: {json.dumps(body)[:300]}")
        
        if path == "/v1/messages":
            openai_body = anthropic_to_openai(body)
            message_id = f"msg_{int(time.time() * 1000)}"
            
            log(f"Forwarding to upstream (streaming): model={openai_body['model']}")
            
            try:
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                # 调用上游 API（流式）
                upstream_url = f"https://{UPSTREAM_HOST}{UPSTREAM_PATH}"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}",
                    "Accept": "text/event-stream"
                }
                
                log("Calling upstream API (streaming)...")
                
                r = call_upstream_with_retry(upstream_url, headers, openai_body)
                
                if not r:
                    raise Exception("Failed to call upstream API after retries")
                
                log(f"Upstream response status: {r.status_code}")
                
                # 读取 SSE 流
                buffer = b""  # 使用字节缓冲区
                first_chunk = True
                
                for chunk in r.iter_content(chunk_size=None, decode_unicode=False):
                    if chunk:
                        buffer += chunk
                        while b"\n" in buffer:
                            line_bytes, buffer = buffer.split(b"\n", 1)
                            line = line_bytes.strip().decode("utf-8", errors="replace")
                            
                            if not line:
                                continue
                            
                            # 解析 OpenAI SSE
                            if line.startswith("data: "):
                                data_str = line[6:].strip()
                                
                                if data_str == "[DONE]":
                                    log("Received [DONE] from upstream")
                                    break
                                
                                try:
                                    openai_chunk = json.loads(data_str)
                                    
                                    # 转换为 Anthropic 格式
                                    events = openai_to_anthropic(openai_chunk, message_id, first_chunk)
                                    first_chunk = False
                                    
                                    for event_type, event_data in events:
                                        event_json = json.dumps(event_data, ensure_ascii=False)
                                        self.wfile.write(f"event: {event_type}\n".encode())
                                        self.wfile.write(f"data: {event_json}\n\n".encode())
                                        self.wfile.flush()
                                        log(f"Sent event: {event_type}")
                                
                                except json.JSONDecodeError:
                                    pass
                
                log("Stream completed successfully")
                
            except Exception as e:
                log(f"Upstream error: {e}")
                import traceback
                traceback.print_exc()
                
                # 发送错误事件
                error_event = {
                    "type": "error",
                    "error": {
                        "type": "api_error",
                        "message": str(e)
                    }
                }
                try:
                    self.wfile.write(f"event: error\n".encode())
                    self.wfile.write(f"data: {json.dumps(error_event)}\n\n".encode())
                    self.wfile.flush()
                except:
                    pass
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, x-api-key")
        self.end_headers()
    
    def log_message(self, format, *args):
        pass

class ThreadedHTTPServer(http.server.HTTPServer):
    """支持多线程的 HTTP 服务器"""
    daemon_threads = True

if __name__ == "__main__":
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', LISTEN_PORT))
    if result == 0:
        log(f"ERROR: Port {LISTEN_PORT} is already in use!")
        exit(1)
    sock.close()
    
    log(f"Claude Code proxy started: http://127.0.0.1:{LISTEN_PORT}")
    log(f"Features: Anthropic API → OpenAI API, streaming, retry on 429")
    server = ThreadedHTTPServer(("127.0.0.1", LISTEN_PORT), ProxyHandler)
    server.serve_forever()
