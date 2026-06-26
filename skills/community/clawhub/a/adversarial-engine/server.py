#!/usr/bin/env python3
"""
多模型对抗引擎整合服务器
WebSocket + HTTP API + 静态页面

作者: 海狸 🦫
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Set

# 先导入FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

sys.path.insert(0, "/home/admin/.openclaw/workspace/skills/adversarial-engine")

try:
    from async_engine import AsyncAdversarialEngine, ROLES
    HAS_ENGINE = True
except ImportError as e:
    HAS_ENGINE = False
    print(f"⚠️ 引擎导入失败: {e}")
    ROLES = {
        "architect": {"model": "qwen3.5-plus", "name": "架构师", "emoji": "🏗️"},
        "engineer": {"model": "qwen3-coder-plus", "name": "工程师", "emoji": "🔧"},
        "security": {"model": "kimi-k2.5", "name": "安全官", "emoji": "🔍"},
        "judge": {"model": "MiniMax-M2.5", "name": "仲裁者", "emoji": "✅"}
    }

# WebSocket连接管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"✅ WebSocket连接: {len(self.active_connections)}个")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: dict):
        for conn in list(self.active_connections):
            try:
                await conn.send_json(message)
            except:
                self.active_connections.discard(conn)


manager = ConnectionManager()

# 全局引擎实例
engine = None


def create_app():
    """创建FastAPI应用"""
    global engine
    
    if HAS_ENGINE:
        engine = AsyncAdversarialEngine()
        engine.ws_manager = manager
    else:
        engine = None
    
    app = FastAPI(title="多模型对抗引擎 v2.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 静态文件目录
    STATIC_DIR = "/home/admin/.openclaw/workspace/multi_agent_engine"
    
    @app.get("/")
    async def root():
        """重定向到主页面"""
        return FileResponse(f"{STATIC_DIR}/adversarial_v2_ui.html")
    
    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "connections": len(manager.active_connections),
            "timestamp": datetime.now().isoformat()
        }
    
    @app.get("/models")
    async def list_models():
        """列出可用模型"""
        return {
            "roles": {
                k: {
                    "model": v["model"],
                    "name": v["name"],
                    "emoji": v["emoji"]
                }
                for k, v in ROLES.items()
            }
        }
    
    @app.post("/api/debate")
    async def start_debate(request: dict):
        """启动辩论（HTTP接口）"""
        topic = request.get("topic", "未指定主题")
        max_rounds = request.get("max_rounds", 2)
        
        # 异步启动辩论
        asyncio.create_task(
            engine.run_debate(topic, max_rounds=max_rounds)
        )
        
        return {
            "status": "started",
            "topic": topic,
            "max_rounds": max_rounds,
            "message": "辩论已在后台启动，请通过WebSocket接收实时进度"
        }
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await manager.connect(websocket)
        
        try:
            while True:
                data = await websocket.receive_text()
                
                try:
                    msg = json.loads(data)
                    msg_type = msg.get("type", "unknown")
                    
                    if msg_type == "ping":
                        await websocket.send_json({"type": "pong"})
                    
                    elif msg_type == "start_debate":
                        topic = msg.get("topic", "未指定主题")
                        max_rounds = msg.get("max_rounds", 2)
                        
                        # 启动辩论任务
                        asyncio.create_task(
                            engine.run_debate(topic, max_rounds=max_rounds)
                        )
                        
                        await websocket.send_json({
                            "type": "task_accepted",
                            "topic": topic
                        })
                    
                    elif msg_type == "get_status":
                        await websocket.send_json({
                            "type": "status",
                            "connections": len(manager.active_connections)
                        })
                        
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "无效JSON"
                    })
                    
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            print(f"❌ WebSocket错误: {e}")
            manager.disconnect(websocket)
    
    # 静态文件
    @app.get("/{filename}.html")
    async def serve_html(filename: str):
        filepath = f"{STATIC_DIR}/{filename}.html"
        if os.path.exists(filepath):
            return FileResponse(filepath)
        return {"error": "Not found"}
    
    return app


def run_server(host: str = "0.0.0.0", port: int = 8002):
    """启动服务器"""
    app = create_app()
    
    print(f"\n{'='*60}")
    print("🦫 多模型对抗引擎 v2.0 服务启动")
    print(f"{'='*60}")
    print(f"📡 WebSocket: ws://{host}:{port}/ws")
    print(f"🌐 HTTP API:  http://{host}:{port}/")
    print(f"📊 健康检查:  http://{host}:{port}/health")
    print(f"🤖 模型列表:  http://{host}:{port}/models")
    print(f"{'='*60}\n")
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()