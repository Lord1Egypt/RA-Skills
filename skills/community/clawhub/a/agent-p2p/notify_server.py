#!/usr/bin/env python3
"""
Agent P2P 通知接收服务
接收 Portal 的实时推送，转发给 OpenClaw
"""
import asyncio
from aiohttp import web
import json
import os

# 通知文件路径
NOTIFY_FILE = os.path.expanduser("~/.agent_p2p_notify.json")

async def handle_notify(request):
    """接收 Portal 推送的通知"""
    try:
        data = await request.json()
        
        # 验证 token
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return web.Response(status=401, text='Unauthorized')
        
        token = auth_header[7:]
        # 这里可以验证 token，暂时跳过
        
        # 保存通知到文件
        notification = {
            "type": data.get('type', 'unknown'),
            "content": data.get('content', ''),
            "portal": data.get('portal', ''),
            "timestamp": data.get('timestamp', '')
        }
        
        # 读取现有通知
        notifications = []
        if os.path.exists(NOTIFY_FILE):
            try:
                with open(NOTIFY_FILE, 'r') as f:
                    notifications = json.load(f)
            except:
                notifications = []
        
        # 添加新通知
        notifications.append(notification)
        
        # 只保留最近100条
        notifications = notifications[-100:]
        
        # 写入文件
        with open(NOTIFY_FILE, 'w') as f:
            json.dump(notifications, f, ensure_ascii=False)
        
        print(f"[Agent P2P Notify] Received: {notification['content'][:50]}...")
        
        return web.Response(status=200, text='OK')
    
    except Exception as e:
        print(f"[Agent P2P Notify] Error: {e}")
        return web.Response(status=500, text=str(e))

async def handle_health(request):
    """健康检查"""
    return web.Response(status=200, text='OK')

async def main():
    app = web.Application()
    app.router.add_post('/notify', handle_notify)
    app.router.add_get('/health', handle_health)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '127.0.0.1', 8081)
    await site.start()
    
    print("[Agent P2P Notify] Server started at http://127.0.0.1:8081")
    print("[Agent P2P Notify] POST /notify to receive notifications")
    
    # 保持运行
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
