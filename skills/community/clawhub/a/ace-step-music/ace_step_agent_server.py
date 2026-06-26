#!/usr/bin/env python3
"""
ACE-Step Agent API Server
为其他 Agent 提供 HTTP 接口调用 ACE-Step

用法:
    python ace_step_agent_server.py
    
其他 Agent 调用:
    curl -X POST http://localhost:8765/generate \
        -H "Content-Type: application/json" \
        -d '{"prompt": "peaceful piano", "duration": 30}'
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

# 配置
VENV_PATH = os.path.expanduser("~/ace-step-env")
ACE_STEP_HOME = os.path.expanduser("~/workspace/ace-step")
OUTPUT_DIR = os.path.expanduser("~/Music/ACE-Step")
PORT = 8765

class ACEStepHandler(BaseHTTPRequestHandler):
    """ACE-Step Agent API 处理器"""
    
    def log_message(self, format, *args):
        """简化日志"""
        print(f"[API] {args[0]}")
    
    def _send_json(self, data, status=200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/status':
            self._handle_status()
        elif self.path == '/':
            self._handle_root()
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        """处理 POST 请求"""
        if self.path == '/generate':
            self._handle_generate()
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_OPTIONS(self):
        """处理 CORS 预检"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _handle_root(self):
        """根路径 - 显示帮助"""
        self._send_json({
            "service": "ACE-Step Agent API",
            "version": "1.0",
            "endpoints": {
                "GET /status": "Check service status",
                "POST /generate": "Generate music (prompt, duration, output_path)"
            }
        })
    
    def _handle_status(self):
        """状态检查"""
        status = {
            "venv_exists": os.path.exists(VENV_PATH),
            "code_exists": os.path.exists(ACE_STEP_HOME),
            "output_dir": OUTPUT_DIR,
            "ready": os.path.exists(VENV_PATH) and os.path.exists(ACE_STEP_HOME)
        }
        self._send_json(status)
    
    def _handle_generate(self):
        """处理生成请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode()
            params = json.loads(body)
            
            prompt = params.get('prompt')
            duration = params.get('duration', 30)
            output_path = params.get('output_path')
            
            if not prompt:
                self._send_json({"error": "prompt is required"}, 400)
                return
            
            # 生成输出路径
            if not output_path:
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                timestamp = int(time.time())
                output_path = os.path.join(OUTPUT_DIR, f"agent_{timestamp}.wav")
            
            # 执行生成
            result = self._generate_music(prompt, duration, output_path)
            self._send_json(result)
            
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, 400)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)
    
    def _generate_music(self, prompt, duration, output_path):
        """
        调用 ACE-Step 生成音乐
        
        注意: 由于 ACE-Step 安装未完成，这里返回模拟结果
        实际安装完成后，替换为真实调用
        """
        # 检查环境
        if not os.path.exists(VENV_PATH):
            return {
                "success": False,
                "error": "ACE-Step not installed",
                "hint": "Run: bash skills/ace-step/install_ace_step.sh"
            }
        
        # 构建命令
        # 实际使用时替换为真实的 ACE-Step 调用
        cmd = f'''
source {VENV_PATH}/bin/activate && \
cd {ACE_STEP_HOME} && \
python3 -c "
import sys
sys.path.insert(0, '{ACE_STEP_HOME}')
print('Would generate: prompt={prompt}, duration={duration}, output={output_path}')
print('{{\"success\": true, \"file\": \"{output_path}\", \"note\": \"ACE-Step installation pending\"}}')
"
'''
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                executable='/bin/bash',
                timeout=300
            )
            
            # 尝试解析输出
            for line in result.stdout.split('\n'):
                if line.strip().startswith('{'):
                    try:
                        return json.loads(line)
                    except:
                        pass
            
            return {
                "success": True,
                "file": output_path,
                "stdout": result.stdout,
                "note": "Check actual ACE-Step installation"
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Generation timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """启动 API 服务器"""
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 创建服务器
    server = HTTPServer(('localhost', PORT), ACEStepHandler)
    
    print(f"🎵 ACE-Step Agent API Server")
    print(f"==============================")
    print(f"Listening on http://localhost:{PORT}")
    print(f"")
    print(f"Endpoints:")
    print(f"  GET  http://localhost:{PORT}/status")
    print(f"  POST http://localhost:{PORT}/generate")
    print(f"")
    print(f"Press Ctrl+C to stop")
    print(f"")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋  Server stopped")


if __name__ == '__main__':
    main()
