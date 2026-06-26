#!/usr/bin/env python3
"""
CFM Daemon - 跨框架通信守护进程
监听Redis消息，收到消息时触发处理

工作原理：
1. 常驻内存，监听Redis频道
2. 收到消息时，写入本地文件触发处理
3. 支持多种触发方式：文件、webhook、stdout
"""

import redis
import json
import signal
import sys
import os
import time
from datetime import datetime
from pathlib import Path


class CFMDaemon:
    """CFM守护进程"""
    
    def __init__(
        self,
        agent_id: str,
        trigger_mode: str = "file",
        trigger_path: str = None,
        webhook_url: str = None,
        redis_host: str = "localhost",
        redis_port: int = 6379
    ):
        """
        初始化守护进程
        
        Args:
            agent_id: 本agent的ID
            trigger_mode: 触发方式 (file/webhook/stdout)
            trigger_path: 文件触发路径
            webhook_url: webhook地址
            redis_host: Redis地址
            redis_port: Redis端口
        """
        self.agent_id = agent_id
        self.trigger_mode = trigger_mode
        self.redis_host = redis_host
        self.redis_port = redis_port
        
        # 设置触发路径
        if trigger_path:
            self.trigger_path = Path(trigger_path)
        else:
            self.trigger_path = Path.home() / ".cfm" / agent_id / "inbox"
        
        # 确保目录存在
        self.trigger_path.mkdir(parents=True, exist_ok=True)
        
        # webhook地址
        self.webhook_url = webhook_url or f"http://localhost:3000/hooks/cfm/{agent_id}"
        
        # Redis连接
        self.redis_client = None
        self.pubsub = None
        self.running = False
        
        # 日志
        self.log_path = Path.home() / ".cfm" / agent_id / "daemon.log"
        
    def start(self):
        """启动守护进程"""
        print(f"🚀 CFM Daemon 启动中...")
        print(f"   Agent: {self.agent_id}")
        print(f"   触发模式: {self.trigger_mode}")
        print(f"   触发路径: {self.trigger_path}")
        print(f"   Redis: {self.redis_host}:{self.redis_port}")
        
        # 连接Redis
        try:
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True
            )
            self.redis_client.ping()
            print("✅ Redis连接成功")
        except redis.ConnectionError as e:
            print(f"❌ Redis连接失败: {e}")
            return False
        
        # 订阅频道
        self.pubsub = self.redis_client.pubsub()
        inbox_channel = f"cfm:{self.agent_id}:inbox"
        self.pubsub.subscribe(inbox_channel)
        print(f"✅ 已订阅频道: {inbox_channel}")
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # 注册agent
        self.redis_client.hset(
            f"cfm:{self.agent_id}:registered",
            mapping={
                "registered_at": datetime.now().isoformat(),
                "status": "online",
                "daemon": "running"
            }
        )
        
        self.running = True
        print("✅ 守护进程已启动，等待消息...")
        print("   (Ctrl+C 停止)")
        print("-" * 40)
        
        # 主循环
        self._listen()
        
        return True
    
    def _listen(self):
        """监听消息"""
        while self.running:
            try:
                # 非阻塞方式获取消息
                msg = self.pubsub.get_message(timeout=1)
                
                if msg and msg["type"] == "message":
                    self._handle_message(msg["data"])
                    
            except redis.ConnectionError:
                print("⚠️ Redis连接断开，尝试重连...")
                self._reconnect()
            except Exception as e:
                self._log(f"处理消息异常: {e}")
                time.sleep(1)
    
    def _handle_message(self, raw_msg: str):
        """处理收到的消息"""
        try:
            msg = json.loads(raw_msg)
        except json.JSONDecodeError:
            self._log(f"无法解析消息: {raw_msg}")
            return
        
        sender = msg.get("from", "unknown")
        content = msg.get("content", "")
        msg_id = msg.get("id", "unknown")
        
        print(f"📨 收到消息!")
        print(f"   发送者: {sender}")
        print(f"   ID: {msg_id}")
        print(f"   内容: {content[:50]}{'...' if len(content) > 50 else ''}")
        
        # 持久化消息
        self._store_message(msg)
        
        # 触发处理
        self._trigger(msg)
        
        # 记录日志
        self._log(f"收到来自 {sender} 的消息: {content[:30]}...")
    
    def _trigger(self, msg: dict):
        """触发消息处理"""
        if self.trigger_mode == "file":
            self._trigger_file(msg)
        elif self.trigger_mode == "webhook":
            self._trigger_webhook(msg)
        elif self.trigger_mode == "stdout":
            self._trigger_stdout(msg)
    
    def _trigger_file(self, msg: dict):
        """文件触发模式"""
        msg_id = msg.get("id", "unknown")
        trigger_file = self.trigger_path / f"{msg_id}.json"
        
        with open(trigger_file, "w", encoding="utf-8") as f:
            json.dump(msg, f, ensure_ascii=False, indent=2)
        
        print(f"   📁 已写入触发文件: {trigger_file}")
    
    def _trigger_webhook(self, msg: dict):
        """Webhook触发模式"""
        import urllib.request
        
        try:
            data = json.dumps(msg, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            urllib.request.urlopen(req, timeout=5)
            print(f"   🔗 已触发webhook: {self.webhook_url}")
        except Exception as e:
            print(f"   ⚠️ Webhook触发失败: {e}")
    
    def _trigger_stdout(self, msg: dict):
        """Stdout触发模式"""
        print(f"   📤 消息输出到stdout")
        print(json.dumps(msg, ensure_ascii=False))
    
    def _store_message(self, msg: dict):
        """持久化消息"""
        store_key = f"cfm:{self.agent_id}:messages"
        self.redis_client.lpush(store_key, json.dumps(msg, ensure_ascii=False))
        self.redis_client.ltrim(store_key, 0, 999)
    
    def _reconnect(self):
        """重连Redis"""
        max_retries = 3
        for i in range(max_retries):
            try:
                self.redis_client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    decode_responses=True
                )
                self.redis_client.ping()
                self.pubsub = self.redis_client.pubsub()
                self.pubsub.subscribe(f"cfm:{self.agent_id}:inbox")
                print("✅ Redis重连成功")
                return
            except:
                time.sleep(2 ** i)
        
        print("❌ Redis重连失败，退出")
        self.running = False
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    def _signal_handler(self, signum, frame):
        """处理停止信号"""
        print(f"\n🛑 收到停止信号 ({signum})")
        self.stop()
    
    def stop(self):
        """停止守护进程"""
        self.running = False
        
        if self.pubsub:
            self.pubsub.unsubscribe()
            self.pubsub.close()
        
        if self.redis_client:
            self.redis_client.hset(
                f"cfm:{self.agent_id}:registered",
                "status", "offline"
            )
            self.redis_client.close()
        
        print("👋 守护进程已停止")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="CFM Daemon - 跨框架通信守护进程")
    parser.add_argument("agent_id", help="Agent ID (如 hermes, chanel)")
    parser.add_argument("--mode", choices=["file", "webhook", "stdout"], 
                       default="file", help="触发模式")
    parser.add_argument("--trigger-path", help="文件触发路径")
    parser.add_argument("--webhook-url", help="Webhook地址")
    parser.add_argument("--redis-host", default="localhost", help="Redis地址")
    parser.add_argument("--redis-port", type=int, default=6379, help="Redis端口")
    
    args = parser.parse_args()
    
    daemon = CFMDaemon(
        agent_id=args.agent_id,
        trigger_mode=args.mode,
        trigger_path=args.trigger_path,
        webhook_url=args.webhook_url,
        redis_host=args.redis_host,
        redis_port=args.redis_port
    )
    
    daemon.start()


if __name__ == "__main__":
    main()
