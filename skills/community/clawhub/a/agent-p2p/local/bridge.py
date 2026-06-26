#!/usr/bin/env python3
"""
Agent P2P OpenClaw Skill - 标准通道实现

模仿飞书/IMClaw 机制：
1. 保持 WebSocket 连接到 Portal
2. 收到消息 → 通过 /hooks/wake 唤醒 OpenClaw 主会话
3. 支持心跳、重连、离线消息同步

环境变量：
- AGENTP2P_API_KEY: Agent API Key
- AGENTP2P_HUB_URL: Portal 地址
- OPENCLAW_GATEWAY_URL: OpenClaw Gateway 地址
- OPENCLAW_HOOKS_TOKEN: OpenClaw hooks token
"""

import asyncio
import websockets
import json
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import ssl
from pathlib import Path
from datetime import datetime
import urllib.request

# 配置日志 - 使用轮转文件处理器
LOG_DIR = Path(__file__).parent
LOG_FILE = LOG_DIR / 'bridge.log'

# 创建轮转日志处理器：保留3个文件，每个最大5MB
log_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3,          # 保留3个旧文件
    encoding='utf-8'
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[log_handler]
)
logger = logging.getLogger('agent-p2p-skill')

class AgentP2PSkill:
    """Agent P2P OpenClaw Skill - 标准通道实现"""
    
    def __init__(self):
        self.api_key = os.environ.get('AGENTP2P_API_KEY')
        self.hub_url = os.environ.get('AGENTP2P_HUB_URL', 'https://your-domain.com')
        self.gateway_url = os.environ.get('OPENCLAW_GATEWAY_URL', 'http://127.0.0.1:18789')
        self.hooks_token = os.environ.get('OPENCLAW_HOOKS_TOKEN')
        
        self.ws = None
        self.running = True
        self.reconnect_delay = 5
        self.max_reconnect_delay = 60
        
        # 状态文件（用于外部检查）
        self.skill_dir = Path(__file__).parent.parent.absolute()
        self.status_file = self.skill_dir / 'skill_status.json'
        
    def validate_config(self) -> bool:
        """验证配置"""
        if not self.api_key:
            logger.error('AGENTP2P_API_KEY 未设置')
            return False
        if not self.hooks_token:
            logger.error('OPENCLAW_HOOKS_TOKEN 未设置')
            return False
        return True
    
    def update_status(self, status: str, message: str = ''):
        """更新状态文件"""
        try:
            data = {
                'status': status,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'hub_url': self.hub_url
            }
            self.status_file.write_text(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            logger.error(f'更新状态失败: {e}')
    
    async def wake_openclaw(self, notification: dict):
        """
        唤醒 OpenClaw 主会话
        模仿飞书/IMClaw 机制：POST 到 /hooks/wake
        """
        try:
            url = f'{self.gateway_url}/hooks/wake'
            
            # 构建唤醒消息
            payload = {
                'text': self._format_notification(notification),
                'metadata': notification
            }
            
            # 使用 urllib 发送 POST 请求
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Authorization': f'Bearer {self.hooks_token}',
                    'Content-Type': 'application/json'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    logger.info(f'OpenClaw 唤醒成功: {notification.get("type")}')
                    return True
                else:
                    logger.error(f'OpenClaw 唤醒失败: {resp.status}')
                    return False
                        
        except Exception as e:
            logger.error(f'唤醒 OpenClaw 异常: {e}')
            return False
    
    def _format_notification(self, notification: dict) -> str:
        """格式化通知文本"""
        msg_type = notification.get('type')
        
        if msg_type == 'guest_message':
            content = notification.get('content', '')
            return f"[Agent P2P] 新留言: {content}"
        
        elif msg_type == 'message':
            sender = notification.get('sender', '未知')
            sender_name = notification.get('sender_name', '')
            content = notification.get('content', '')
            # 显示格式：主人名的Agent名，如 "李亚楠的小扣子"
            if sender_name and 'http' not in sender_name.lower():
                display_name = f"{sender_name}(Agent)"
            else:
                display_name = sender.replace('https://', '').replace('http://', '')
            return f"[Agent P2P] 新消息来自 {display_name}: {content}"
        
        elif msg_type == 'system':
            content = notification.get('content', '')
            return f"[Agent P2P] 系统通知: {content}"
        
        elif msg_type == 'owner_message':
            content = notification.get('content', '')
            return f"[主人消息] {content}"
        
        else:
            return f"[Agent P2P] 通知: {json.dumps(notification, ensure_ascii=False)}"
    
    async def handle_message(self, data: dict):
        """处理收到的消息"""
        msg_type = data.get('type')
        
        if msg_type == 'pong':
            logger.info('收到 pong，连接正常')
            self.pong_received = True
            return
        
        # 处理 Portal 的心跳 ping，回复 pong 保持连接
        if msg_type == 'ping':
            logger.info('收到 Portal ping，回复 pong')
            if self.ws:
                await self.ws.send(json.dumps({'type': 'pong'}))
            return
        
        notification = None
        
        if msg_type == 'new_guest_message':
            content = data.get('content', '')
            msg_id = data.get('id')
            logger.info(f'新留言: {content}')
            notification = {
                'type': 'guest_message',
                'content': content,
                'message_id': msg_id,
                'priority': 'high',
                'timestamp': datetime.now().isoformat(),
                'actions': ['查看', '回复', '忽略']
            }
            
            # 发送确认
            if msg_id and self.ws:
                await self.ws.send(json.dumps({
                    'type': 'ack',
                    'message_ids': [msg_id]
                }))
        
        elif msg_type == 'new_message':
            from_portal = data.get('from', '')
            from_name = data.get('from_name', from_portal)
            content = data.get('content', '')
            msg_id = data.get('id')
            logger.info(f'新消息来自 {from_portal}: {content}')
            notification = {
                'type': 'message',
                'sender': from_portal,
                'sender_name': from_name,
                'content': content,
                'message_id': msg_id,
                'priority': 'high',
                'timestamp': datetime.now().isoformat(),
                'actions': ['回复', '查看历史']
            }
            
            # 发送确认
            msg_id = data.get('id')
            if msg_id and self.ws:
                await self.ws.send(json.dumps({
                    'type': 'ack',
                    'message_ids': [msg_id]
                }))
        
        elif msg_type == 'file_transfer':
            content = data.get('content', '')
            logger.info(f'文件传输通知: {content}')
            notification = {
                'type': 'file_transfer',
                'content': content,
                'priority': 'high',
                'timestamp': datetime.now().isoformat(),
                'actions': ['查看', '下载']
            }

        elif msg_type == 'owner_message':
            content = data.get('content', '')
            msg_id = data.get('message_id')
            logger.info(f'主人消息: {content}')
            notification = {
                'type': 'owner_message',
                'content': content,
                'message_id': msg_id,
                'priority': 'high',
                'timestamp': datetime.now().isoformat()
            }

        elif msg_type == 'sync_response':
            messages = data.get('messages', [])
            if messages:
                logger.info(f'同步到 {len(messages)} 条离线消息')
                message_ids = []
                for msg in messages:
                    await self.handle_message({
                        'type': 'new_message',
                        'from': msg.get('from'),
                        'content': msg.get('content'),
                        'id': msg.get('id')
                    })
                    message_ids.append(msg.get('id'))

                # 发送 ack 确认收到离线消息
                if message_ids and self.ws:
                    await self.ws.send(json.dumps({
                        'type': 'ack',
                        'message_ids': message_ids
                    }))
                    logger.info(f'已确认 {len(message_ids)} 条离线消息')
            else:
                logger.debug('没有离线消息需要同步')
            return
        
        # 唤醒 OpenClaw
        if notification:
            await self.wake_openclaw(notification)
    
    async def connect(self):
        """连接 Portal WebSocket"""
        ws_url = self.hub_url.replace('https://', 'wss://').replace('http://', 'ws://')
        ws_url = f'{ws_url}/ws/agent?api_key={self.api_key}'
        
        logger.info(f'连接 Portal: {ws_url[:60]}...')
        
        # 创建 SSL 上下文（跳过验证，仅用于测试）
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        try:
            async with websockets.connect(ws_url, ssl=ssl_context) as websocket:
                self.ws = websocket
                self.pong_received = True
                self.reconnect_delay = 5  # 重置重连延迟
                logger.info('WebSocket 连接成功')
                self.update_status('connected', 'WebSocket 连接成功')
                
                # 发送同步请求
                await websocket.send(json.dumps({
                    'type': 'sync_request'
                }))
                
                # 并行运行消息接收和心跳检测
                receive_task = asyncio.create_task(self._receive_messages(websocket))
                heartbeat_task = asyncio.create_task(self._heartbeat(websocket))
                
                # 等待任一任务完成（正常情况下都不会结束）
                done, pending = await asyncio.wait(
                    [receive_task, heartbeat_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # 取消未完成的任务
                for task in pending:
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
                        
        except websockets.exceptions.ConnectionClosed:
            logger.warning('WebSocket 连接断开')
            self.update_status('disconnected', 'WebSocket 连接断开')
        except Exception as e:
            logger.error(f'WebSocket 异常: {e}')
            self.update_status('error', str(e))
    
    async def _receive_messages(self, websocket):
        """持续接收 WebSocket 消息"""
        async for message in websocket:
            try:
                data = json.loads(message)
                await self.handle_message(data)
            except json.JSONDecodeError:
                logger.error(f'收到无效 JSON: {message[:100]}')
            except Exception as e:
                logger.error(f'处理消息异常: {e}')
    
    async def _heartbeat(self, websocket):
        """主动心跳：每30秒发 ping，5秒内没收到 pong 则断开"""
        while True:
            await asyncio.sleep(30)
            try:
                self.pong_received = False
                await websocket.send(json.dumps({'type': 'ping'}))
                # 等5秒看有没有 pong
                for _ in range(5):
                    await asyncio.sleep(1)
                    if self.pong_received:
                        break
                else:
                    # 5秒内没收到 pong，连接可能已死
                    logger.warning('心跳超时，主动断开重连')
                    await websocket.close()
                    break
            except Exception as e:
                logger.warning(f'心跳发送失败: {e}')
                break
    
    async def run(self):
        """主循环"""
        if not self.validate_config():
            sys.exit(1)
        
        logger.info('Agent P2P Skill 启动')
        self.update_status('starting', 'Skill 启动中')
        
        while self.running:
            try:
                await self.connect()
            except Exception as e:
                logger.error(f'连接异常: {e}')
            
            if self.running:
                logger.info(f'{self.reconnect_delay}秒后重连...')
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)

def main():
    """入口函数"""
    skill = AgentP2PSkill()
    try:
        asyncio.run(skill.run())
    except KeyboardInterrupt:
        logger.info('收到中断信号，正在退出...')
        skill.running = False
        skill.update_status('stopped', 'Skill 已停止')

if __name__ == '__main__':
    main()
