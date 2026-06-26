#!/usr/bin/env python3
"""
Cross-Framework Messenger (CFM) - 跨框架Agent通信库
基于Redis Pub/Sub实现Hermes ↔ OpenClaw双向通信

设计原则：
- 事件驱动，零轮询
- 消息持久化（可选）
- 简单易用
"""

import redis
import json
import time
import threading
import uuid
from datetime import datetime
from typing import Callable, Optional, Dict, Any


class CFMMessenger:
    """跨框架通信器 - 基于Redis Pub/Sub"""
    
    def __init__(
        self,
        agent_id: str,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0
    ):
        """
        初始化通信器
        
        Args:
            agent_id: 本agent的唯一标识（如 "hermes" 或 "chanel"）
            redis_host: Redis服务器地址
            redis_port: Redis服务器端口
            redis_db: Redis数据库编号
        """
        self.agent_id = agent_id
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        
        # 检查连接
        try:
            self.redis_client.ping()
        except redis.ConnectionError:
            raise ConnectionError(f"无法连接Redis: {redis_host}:{redis_port}")
        
        # 频道命名
        self.inbox_channel = f"cfm:{agent_id}:inbox"
        self.outbox_channel = f"cfm:{agent_id}:outbox"
        
        # 消息存储（用于持久化）
        self.message_store_key = f"cfm:{agent_id}:messages"
        
        # 订阅者
        self.pubsub = None
        self.listener_thread = None
        self.running = False
        
        # 回调函数
        self.on_message_callback: Optional[Callable] = None
        
    def send(self, to_agent: str, message: str, msg_type: str = "text") -> str:
        """
        发送消息给另一个agent
        
        Args:
            to_agent: 目标agent的ID
            message: 消息内容
            msg_type: 消息类型（text/command/response）
            
        Returns:
            消息ID
        """
        msg_id = str(uuid.uuid4())[:8]
        
        payload = {
            "id": msg_id,
            "from": self.agent_id,
            "to": to_agent,
            "type": msg_type,
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # 发布到目标agent的收件箱频道
        target_channel = f"cfm:{to_agent}:inbox"
        self.redis_client.publish(target_channel, json.dumps(payload, ensure_ascii=False))
        
        # 持久化消息（同时存到双方的messages存储）
        # 发送者的存储
        self._store_message(payload, self.agent_id)
        # 接收者的存储（这样接收者监听自己的频道就能收到）
        self._store_message(payload, to_agent)
        
        return msg_id
    
    def get_messages(self, limit: int = 50) -> list:
        """
        获取持久化的消息历史
        
        Args:
            limit: 最大返回条数
            
        Returns:
            消息列表
        """
        messages = self.redis_client.lrange(self.message_store_key, 0, limit - 1)
        return [json.loads(msg) for msg in messages]
    
    def _store_message(self, msg: Dict[str, Any], agent_id: str = None):
        """持久化消息到Redis"""
        store_key = f"cfm:{agent_id or self.agent_id}:messages"
        self.redis_client.lpush(
            store_key,
            json.dumps(msg, ensure_ascii=False)
        )
        # 保留最近1000条
        self.redis_client.ltrim(store_key, 0, 999)
        self.pubsub.subscribe(self.inbox_channel)
        
        def listener():
            for raw_msg in self.pubsub.listen():
                if not self.running:
                    break
                
                if raw_msg["type"] == "message":
                    try:
                        msg = json.loads(raw_msg["data"])
                        # 持久化收到的消息
                        self._store_message(msg)
                        # 调用回调
                        if self.on_message_callback:
                            self.on_message_callback(msg)
                    except json.JSONDecodeError:
                        pass
        
        self.listener_thread = threading.Thread(target=listener, daemon=True)
        self.listener_thread.start()
        
        return True
    
    def stop_listening(self):
        """停止消息监听"""
        self.running = False
        if self.pubsub:
            self.pubsub.unsubscribe()
            self.pubsub.close()
        if self.listener_thread:
            self.listener_thread.join(timeout=2)
    
    def discover_agents(self) -> list:
        """
        发现网络中注册的其他agents
        
        Returns:
            agent列表
        """
        keys = self.redis_client.keys("cfm:*:registered")
        agents = []
        for key in keys:
            agent_id = key.split(":")[1]
            if agent_id != self.agent_id:
                info = self.redis_client.hgetall(key)
                agents.append({"id": agent_id, **info})
        return agents
    
    def register(self):
        """注册本agent到网络"""
        self.redis_client.hset(
            f"cfm:{self.agent_id}:registered",
            mapping={
                "registered_at": datetime.now().isoformat(),
                "status": "online"
            }
        )
    
    def unregister(self):
        """注销本agent"""
        self.redis_client.delete(f"cfm:{self.agent_id}:registered")
    
    def __enter__(self):
        self.register()
        self.start_listening()
        return self
    
    def __exit__(self, *args):
        self.stop_listening()
        self.unregister()


# 便捷函数
def quick_send(to_agent: str, message: str, from_agent: str = "cli") -> str:
    """
    快速发送消息（不保持连接，不触发监听线程）
    
    Args:
        to_agent: 目标agent
        message: 消息内容
        from_agent: 发送者ID
        
    Returns:
        消息ID
    """
    r = redis.Redis(decode_responses=True)
    msg_id = str(uuid.uuid4())[:8]
    
    payload = {
        "id": msg_id,
        "from": from_agent,
        "to": to_agent,
        "type": "text",
        "content": message,
        "timestamp": datetime.now().isoformat()
    }
    
    # 直接发布，不启动监听线程
    target_channel = f"cfm:{to_agent}:inbox"
    r.publish(target_channel, json.dumps(payload, ensure_ascii=False))
    
    # 持久化（同时存到双方）
    # 发送者的存储
    sender_store_key = f"cfm:{from_agent}:messages"
    r.lpush(sender_store_key, json.dumps(payload, ensure_ascii=False))
    r.ltrim(sender_store_key, 0, 999)
    # 接收者的存储
    receiver_store_key = f"cfm:{to_agent}:messages"
    r.lpush(receiver_store_key, json.dumps(payload, ensure_ascii=False))
    r.ltrim(receiver_store_key, 0, 999)
    
    r.close()
    return msg_id


def quick_receive(agent_id: str, timeout: int = 10) -> Optional[Dict]:
    """
    快速接收一条消息（阻塞等待，超时自动退出）
    
    Args:
        agent_id: 本agent的ID
        timeout: 超时秒数
        
    Returns:
        消息字典或None
    """
    r = redis.Redis(decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe(f"cfm:{agent_id}:inbox")
    
    start = time.time()
    result = None
    
    try:
        # 用get_message代替listen循环，避免阻塞
        while time.time() - start < timeout:
            msg = pubsub.get_message(timeout=1)
            if msg and msg["type"] == "message":
                result = json.loads(msg["data"])
                break
    finally:
        pubsub.unsubscribe()
        pubsub.close()
        r.close()
    
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CFM Messenger")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # send command
    send_parser = subparsers.add_parser("send", help="Send a message")
    send_parser.add_argument("to", help="Target agent ID")
    send_parser.add_argument("message", help="Message content")
    send_parser.add_argument("--from", dest="from_agent", default="cli", help="Sender agent ID")
    
    # listen command
    listen_parser = subparsers.add_parser("listen", help="Listen for messages")
    listen_parser.add_argument("agent_id", help="Agent ID to listen for")
    
    # discover command
    discover_parser = subparsers.add_parser("discover", help="Discover agents")
    
    args = parser.parse_args()
    
    if args.command == "send":
        quick_send(args.to, args.message, args.from_agent)
        print(f"✅ Message sent to {args.to}")
    elif args.command == "listen":
        print(f"Listening for messages to {args.agent_id}...")
        msg = quick_receive(args.agent_id)
        if msg:
            print(f"📨 Received: {msg}")
        else:
            print("📭 No messages")
    elif args.command == "discover":
        r = redis.Redis(decode_responses=True)
        keys = r.keys("cfm:*:registered")
        agents = []
        for key in keys:
            agent_id = key.split(":")[1]
            info = r.hgetall(key)
            agents.append({"id": agent_id, **info})
        print(f"Found {len(agents)} agents:")
        for agent in agents:
            print(f"  - {agent['id']} (registered at {agent.get('registered_at', 'unknown')})")
    else:
        parser.print_help()
