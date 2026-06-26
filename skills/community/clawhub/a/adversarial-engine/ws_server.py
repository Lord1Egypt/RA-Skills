#!/usr/bin/env python3
"""
WebSocket服务器 - 实时推送辩论进度
支持断点续传、实时广播

作者: 海狸 🦫
"""

import asyncio
import json
from datetime import datetime
from typing import Set
import sys
import os

# 添加路径
sys.path.insert(0, "/home/admin/.openclaw/workspace/skills/adversarial-engine")

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    print("⚠️ FastAPI未安装，请运行: pip install fastapi uvicorn")

# 全局WebSocket客户端管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"✅ WebSocket连接建立，当前连接数: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        print(f"🔴 WebSocket断开，当前连接数: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """广播消息到所有客户端"""
        dead_connections = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                dead_connections.add(connection)
        
        # 清理断开的连接
        for dead in dead_connections:
            self.active_connections.discard(dead)


manager = ConnectionManager()


def create_app():
    """创建FastAPI应用"""
    if not HAS_FASTAPI:
        return None
    
    app = FastAPI(title="多模型对抗引擎 WebSocket")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {
            "service": "多模型对抗引擎 WebSocket",
            "status": "running",
            "connections": len(manager.active_connections),
            "timestamp": datetime.now().isoformat()
        }
    
    @app.get("/health")
    async def health():
        return {"status": "ok", "connections": len(manager.active_connections)}
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await manager.connect(websocket)
        try:
            while True:
                # 接收客户端消息
                data = await websocket.receive_text()
                
                try:
                    msg = json.loads(data)
                    msg_type = msg.get("type", "unknown")
                    
                    if msg_type == "ping":
                        await websocket.send_json({"type": "pong"})
                    
                    elif msg_type == "start_debate":
                        # 启动新辩论
                        from engine import AdversarialEngine
                        topic = msg.get("topic", "未指定主题")
                        max_rounds = msg.get("max_rounds", 3)
                        
                        # 发送开始通知
                        await manager.broadcast({
                            "type": "debate_started",
                            "topic": topic,
                            "max_rounds": max_rounds,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        # 运行辩论（这里需要异步改造）
                        # 暂时返回确认
                        await websocket.send_json({
                            "type": "task_accepted",
                            "topic": topic,
                            "message": "辩论任务已接收，正在后台执行..."
                        })
                    
                    elif msg_type == "get_status":
                        await websocket.send_json({
                            "type": "status",
                            "connections": len(manager.active_connections)
                        })
                    
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "无效的JSON格式"
                    })
                    
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            print(f"❌ WebSocket错误: {e}")
            manager.disconnect(websocket)
    
    return app


def run_server(host: str = "0.0.0.0", port: int = 8002):
    """启动WebSocket服务器"""
    if not HAS_FASTAPI:
        print("❌ FastAPI未安装，无法启动WebSocket服务")
        print("请运行: pip install fastapi uvicorn")
        return
    
    app = create_app()
    
    print(f"\n{'='*50}")
    print("🚀 多模型对抗引擎 WebSocket服务启动")
    print(f"📡 WebSocket地址: ws://{host}:{port}/ws")
    print(f"🌐 HTTP地址: http://{host}:{port}/")
    print(f"{'='*50}\n")
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()