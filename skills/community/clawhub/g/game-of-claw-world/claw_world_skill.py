"""
龙虾世界 (ClawWorld) Skill - 客户端 Skill 配置

这个 Skill 使 openClaw 能够连接到龙虾世界游戏服务器。
"""
import json
import threading
import time
from typing import Any, Dict, Optional, Callable

import websocket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class ClawWorldSkill:
    """龙虾世界游戏的 Skill，用于 openClaw 客户端"""

    def __init__(self, server_url: str = "ws://claw.hifunyo.cc:8000/ws/"):
        """
        初始化 Skill
        
        Args:
            server_url: 游戏服务器的 WebSocket URL 地址
        """
        self.server_url = server_url
        self.private_key: Optional[rsa.RSAPrivateKey] = None
        self.public_key: Optional[rsa.RSAPublicKey] = None
        self.agent_id: Optional[str] = None
        self.session_token: Optional[str] = None
        self.player_id: Optional[str] = None
        
        # WebSocket 连接相关
        self.ws: Optional[websocket.WebSocketApp] = None
        self.ws_thread: Optional[threading.Thread] = None
        self.is_connected: bool = False
        self.reconnect_enabled: bool = True
        self.reconnect_interval: int = 5
        self.heartbeat_interval: int = 30
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._stop_heartbeat: threading.Event = threading.Event()
        
        # 消息处理器
        self.message_handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {}

    def generate_identity(self) -> None:
        """
        生成 A2A 身份密钥对
        
        这个方法会生成一对 RSA 公钥和私钥，用于 A2A 协议的身份认证。
        生成后会自动设置 agent_id。
        """
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        self.agent_id = self._generate_agent_id()

    def _generate_agent_id(self) -> str:
        """
        从公钥生成唯一的代理 ID
        
        使用公钥的 SHA256 哈希值的前 16 个字符作为 agent_id
        
        Returns:
            str: 16 位的 agent ID 字符串
        """
        pub_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        import hashlib
        return hashlib.sha256(pub_bytes).hexdigest()[:16]

    def get_public_key_pem(self) -> str:
        """
        获取 PEM 格式的公钥
        
        Returns:
            str: PEM 格式的公钥字符串
            
        Raises:
            ValueError: 如果身份尚未生成
        """
        if not self.public_key:
            raise ValueError("Identity not generated")
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem.decode()

    def sign(self, data: bytes) -> str:
        """
        使用私钥对数据进行签名
        
        Args:
            data: 需要签名的字节数据
            
        Returns:
            str: 签名的十六进制字符串
            
        Raises:
            ValueError: 如果身份尚未生成
        """
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding

        if not self.private_key:
            raise ValueError("Identity not generated")

        signature = self.private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return signature.hex()

    def create_handshake_message(self) -> Dict[str, Any]:
        """
        创建 A2A 握手消息
        
        Returns:
            Dict[str, Any]: 包含握手信息的字典
        """
        return {
            "version": "1.0",
            "type": "a2a_handshake",
            "sender_id": self.agent_id,
            "payload": {
                "public_key": self.get_public_key_pem(),
                "nonce": self._generate_nonce(),
            },
        }

    def create_game_action(self, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建游戏动作消息
        
        Args:
            action: 动作类型字符串
            data: 动作数据字典
            
        Returns:
            Dict[str, Any]: 包含游戏动作的字典
        """
        return {
            "version": "1.0",
            "type": "game_action",
            "sender_id": self.agent_id,
            "payload": {
                "action": action,
                "data": data,
            },
        }

    def _generate_nonce(self) -> str:
        """
        生成随机 nonce
        
        Returns:
            str: UUID 格式的随机字符串
        """
        import uuid
        return str(uuid.uuid4())

    def handle_response(self, response: Dict[str, Any]) -> None:
        """
        处理服务器响应消息
        
        Args:
            response: 服务器返回的消息字典
            
        根据消息类型处理不同的响应:
        - a2a_success: 认证成功，保存 session_token 和 player_id
        - error: 显示错误消息
        - game_event: 显示游戏事件
        """
        msg_type = response.get("type")

        if msg_type == "a2a_success":
            self.session_token = response.get("payload", {}).get("session_token")
            self.player_id = response.get("payload", {}).get("player_id")
            print(f"Authentication successful! Player ID: {self.player_id}")
        elif msg_type == "error":
            print(f"Error: {response.get('payload', {}).get('error_message')}")
        elif msg_type == "game_event":
            event = response.get("payload", {})
            print(f"Game Event: {event}")

    def connect(self, on_open: Optional[Callable[[], None]] = None) -> None:
        """
        连接到 WebSocket 服务器
        
        Args:
            on_open: 连接成功后的回调函数
        """
        if self.is_connected:
            print("Already connected to server")
            return

        def on_ws_open(ws):
            print(f"Connected to {self.server_url}")
            self.is_connected = True
            self._start_heartbeat()
            if on_open:
                on_open()

        def on_ws_message(ws, message):
            self.handle_message(message)

        def on_ws_error(ws, error):
            print(f"WebSocket error: {error}")

        def on_ws_close(ws, close_status_code, close_msg):
            print(f"Disconnected from server: {close_status_code} - {close_msg}")
            self.is_connected = False
            self._stop_heartbeat.set()
            if self.reconnect_enabled:
                print(f"Reconnecting in {self.reconnect_interval} seconds...")
                time.sleep(self.reconnect_interval)
                self.connect(on_open)

        self.ws = websocket.WebSocketApp(
            self.server_url,
            on_open=on_ws_open,
            on_message=on_ws_message,
            on_error=on_ws_error,
            on_close=on_ws_close,
        )

        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def disconnect(self) -> None:
        """
        断开与 WebSocket 服务器的连接
        """
        self.reconnect_enabled = False
        self._stop_heartbeat.set()
        
        if self.ws:
            self.ws.close()
            self.ws = None
        
        self.is_connected = False
        print("Disconnected from server")

    def send_message(self, message: Dict[str, Any]) -> bool:
        """
        发送消息到服务器
        
        Args:
            message: 要发送的消息字典
            
        Returns:
            bool: 发送是否成功
        """
        if not self.is_connected or not self.ws:
            print("Not connected to server")
            return False
        
        try:
            json_message = json.dumps(message)
            self.ws.send(json_message)
            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False

    def handle_message(self, message: str) -> None:
        """
        处理从服务器接收到的消息
        
        Args:
            message: 接收到的 JSON 字符串消息
        """
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            # 调用特定的消息处理器（如果已注册）
            if msg_type in self.message_handlers:
                self.message_handlers[msg_type](data)
            
            # 调用默认的响应处理
            self.handle_response(data)
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse message: {e}")
        except Exception as e:
            print(f"Error handling message: {e}")

    def register_message_handler(self, msg_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        注册特定消息类型的处理器
        
        Args:
            msg_type: 消息类型
            handler: 处理函数
        """
        self.message_handlers[msg_type] = handler

    def _start_heartbeat(self) -> None:
        """
        启动心跳线程，定期发送心跳消息保持连接
        """
        self._stop_heartbeat.clear()
        
        def heartbeat_loop():
            while not self._stop_heartbeat.is_set():
                if self.is_connected:
                    heartbeat_msg = {
                        "version": "1.0",
                        "type": "heartbeat",
                        "sender_id": self.agent_id,
                        "payload": {"timestamp": time.time()},
                    }
                    self.send_message(heartbeat_msg)
                self._stop_heartbeat.wait(self.heartbeat_interval)
        
        self._heartbeat_thread = threading.Thread(target=heartbeat_loop)
        self._heartbeat_thread.daemon = True
        self._heartbeat_thread.start()

    def authenticate(self) -> bool:
        """
        发送 A2A 握手消息进行身份认证
        
        Returns:
            bool: 认证消息是否成功发送
        """
        if not self.agent_id:
            print("Identity not generated. Call generate_identity() first.")
            return False
        
        handshake = self.create_handshake_message()
        return self.send_message(handshake)


# Skill 配置
SKILL_CONFIG = {
    "name": "clawworld",
    "version": "1.0.0",
    "description": "龙虾世界游戏 Skill，用于 openClaw 客户端",
    "server_url": "ws://claw.hifunyo.cc:8000/ws/",
    "api_url": "http://claw.hifunyo.cc:8000/api",
}

# 游戏命令定义
GAME_COMMANDS = {
    "create_character": {
        "description": "创建新的龙虾角色",
        "params": {"name": "角色名称"},
        "action": "create_character",
    },
    "work": {
        "description": "开始工作赚取金币",
        "params": {"job_id": "工作 ID"},
        "action": "work",
    },
    "battle": {
        "description": "挑战怪物战斗",
        "params": {"monster_id": "怪物 ID"},
        "action": "battle",
    },
    "shop": {
        "description": "打开商店",
        "params": {},
        "action": "shop",
    },
    "buy": {
        "description": "从商店购买物品",
        "params": {"item_id": "物品 ID", "quantity": "购买数量"},
        "action": "buy",
    },
    "equip": {
        "description": "装备物品",
        "params": {"item_id": "要装备的物品 ID"},
        "action": "equip",
    },
    "status": {
        "description": "查看角色状态",
        "params": {},
        "action": "status",
    },
    "explore": {
        "description": "探索当前位置",
        "params": {},
        "action": "explore",
    },
}
