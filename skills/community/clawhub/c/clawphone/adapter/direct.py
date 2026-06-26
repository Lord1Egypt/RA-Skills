"""
DirectAdapter - ClawPhone 内置直接 P2P 通信（不依赖 ClawMesh）
使用同步 TCP sockets 实现。
"""

import json
import logging
import socket
import threading
from typing import Optional, Callable, Dict, Any
from pathlib import Path
import sqlite3

logger = logging.getLogger(__name__)

# 数据库路径
DB_PATH = Path.home() / ".openclaw" / "skills" / "clawphone" / "phonebook.db"


class DirectAdapter:
    """直接 TCP 通信适配器"""

    def __init__(self, node_id: str, listen_port: int = 0):
        self.node_id = node_id
        self.listen_port = listen_port
        self._address: Optional[str] = None
        self._server: Optional[socket.socket] = None
        self._on_message: Optional[Callable[[Dict[str, Any]], None]] = None
        self._running = False
        self._server_thread: Optional[threading.Thread] = None

    def start(self) -> str:
        """启动 TCP server（后台线程），返回地址 "127.0.0.1:port" """
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(("127.0.0.1", self.listen_port))
        actual_port = self._server.getsockname()[1]
        self._address = f"127.0.0.1:{actual_port}"
        self._server.listen(5)
        self._running = True

        def _accept_loop():
            while self._running:
                try:
                    self._server.settimeout(1.0)
                    conn, addr = self._server.accept()
                    threading.Thread(target=self._handle_connection, args=(conn,), daemon=True).start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self._running:
                        logger.error(f"[{self.node_id}] Server error: {e}")

        self._server_thread = threading.Thread(target=_accept_loop, daemon=True)
        self._server_thread.start()
        logger.info(f"[{self.node_id}] DirectAdapter listening on {self._address}")
        return self._address

    def _handle_connection(self, conn: socket.socket):
        """处理传入连接（单条消息）"""
        try:
            conn.settimeout(5.0)
            data = conn.recv(4096)
            if data:
                try:
                    msg = json.loads(data.decode('utf-8'))
                    if self._on_message:
                        self._on_message(msg)
                except json.JSONDecodeError:
                    logger.warning(f"[{self.node_id}] Invalid JSON")
        except Exception as e:
            logger.error(f"[{self.node_id}] Handler error: {e}")
        finally:
            conn.close()

    def on_message(self, callback: Callable[[Dict[str, Any]], None]):
        self._on_message = callback

    def send(self, address: str, payload: dict) -> bool:
        """同步发送到目标地址"""
        if not address or ":" not in address:
            logger.warning(f"[{self.node_id}] Invalid address: {address}")
            return False
        host, port_str = address.split(":")
        port = int(port_str)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((host, port))
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            sock.sendall(data)
            sock.close()
            return True
        except Exception as e:
            logger.error(f"[{self.node_id}] Send failed to {address}: {e}")
            return False

    def get_my_address(self) -> Optional[str]:
        return self._address

    def stop(self):
        self._running = False
        if self._server:
            self._server.close()
        if self._server_thread and self._server_thread.is_alive():
            self._server_thread.join(timeout=2)
        logger.info(f"[{self.node_id}] DirectAdapter stopped")
