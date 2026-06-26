"""
ClawPhone Skill - 让 Agent 拥有"手机号码"
支持多种传输层：ClawMesh（可选）或内置 Direct P2P
"""

import sqlite3
import random
import json
import time
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import logging
import asyncio

logger = logging.getLogger(__name__)

# 数据库路径
DB_PATH = Path.home() / ".openclaw" / "skills" / "clawphone" / "phonebook.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _init_db():
    """初始化 SQLite 数据库（含 address 字段）"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # 创建 phones 表（如果不存在）
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS phones (
            alias TEXT PRIMARY KEY,
            phone_id TEXT UNIQUE,
            node_id TEXT,
            address TEXT,
            public_key TEXT,
            status TEXT DEFAULT 'offline',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    # 确保 address 列存在（对旧数据库迁移）
    cur.execute("PRAGMA table_info(phones)")
    cols = [row[1] for row in cur.fetchall()]
    if "address" not in cols:
        cur.execute("ALTER TABLE phones ADD COLUMN address TEXT")
        print("[DB] 迁移: 添加 address 列")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS call_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_phone TEXT,
            to_phone TEXT,
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


class DirectAdapter:
    """直接 WebSocket 通信适配器（无中心服务器）"""

    def __init__(self, phone, listen_port: int = 0):
        """
        :param phone: ClawPhone 实例（用于回调）
        :param listen_port: 监听端口（0=随机）
        """
        self.phone = phone
        self.listen_port = listen_port
        self._address: Optional[str] = None
        self._server: Optional[asyncio.Server] = None
        self._on_message: Optional[Callable[[Dict[str, Any]], None]] = None

    async def start(self) -> str:
        """启动 WebSocket 简易服务（使用 asyncio start_server）"""
        host = "0.0.0.0"
        self._server = await asyncio.start_server(self._handler, host, self.listen_port)
        actual_port = self._server.sockets[0].getsockname()[1]
        self._address = f"127.0.0.1:{actual_port}"
        logger.info(f"[DirectAdapter] listening on {self._address}")
        return self._address

    async def _handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理传入连接（TCP 流，JSON 消息）"""
        try:
            data = await reader.read(4096)
            if data:
                try:
                    msg = json.loads(data.decode('utf-8'))
                    if self._on_message:
                        self._on_message(msg)
                except json.JSONDecodeError:
                    logger.warning(f"[DirectAdapter] Invalid JSON")
        except Exception as e:
            logger.error(f"[DirectAdapter] handler error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def send(self, target_address: str, payload: dict) -> bool:
        """发送到目标 "host:port" """
        host, port_str = target_address.split(":")
        port = int(port_str)
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=5.0
            )
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            writer.write(data)
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return True
        except Exception as e:
            logger.error(f"[DirectAdapter] send to {target_address} failed: {e}")
            return False

    def on_message(self, callback: Callable[[Dict[str, Any]], None]):
        """设置消息回调"""
        self._on_message = callback

    def get_my_address(self) -> Optional[str]:
        return self._address

    async def stop(self):
        if self._server:
            self._server.close()
            await self._server.wait_closed()


class ClawPhone:
    """核心类（支持多适配器）"""

    def __init__(self):
        self._on_message: Optional[Callable[[Dict[str, Any]], None]] = None
        self._my_phone_id: Optional[str] = None
        self._my_node_id: Optional[str] = None
        self._status = "offline"
        self._adapter = None  # 网络适配器
        self._my_address: Optional[str] = None
        _init_db()

    # --- 适配器管理 ---
    def set_adapter(self, adapter):
        """注入通用网络适配器"""
        self._adapter = adapter
        self._restore_registration()
        # 如果适配器有 on_message 设置（ClawMesh 方式）
        if hasattr(adapter, 'on_message'):
            adapter.on_message = self._handle_network_message
        logger.info(f"Adapter set: {type(adapter).__name__}")

    # 兼容旧名
    def set_network(self, network):
        self.set_adapter(network)

    def set_direct_adapter(self, adapter):
        self.set_adapter(adapter)

    # --- 注册 ---
    def register(self, alias: str) -> str:
        """注册一个 13 位纯数字号码"""
        if not alias or not alias.replace('_', '').isalnum():
            raise ValueError("alias 必须为字母数字组合（可含下划线）")

        logger.debug(f"[register] called with alias='{alias}', _my_phone_id={self._my_phone_id}, _my_node_id={self._my_node_id}")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT phone_id FROM phones WHERE alias = ?", (alias,))
        row = cur.fetchone()
        if row:
            conn.close()
            return row[0]  # 已存在

        # 生成唯一 13 位数字
        for _ in range(100):
            phone_id = str(random.randint(1000000000000, 9999999999999))
            cur.execute("SELECT 1 FROM phones WHERE phone_id = ?", (phone_id,))
            if not cur.fetchone():
                break
        else:
            raise RuntimeError("无法生成唯一号码，请重试")

        # 获取地址（如果适配器提供）
        my_address = None
        if self._adapter and hasattr(self._adapter, 'get_my_address'):
            try:
                my_address = self._adapter.get_my_address()
                logger.debug(f"[register] 从适配器获取地址: {my_address}")
            except Exception:
                my_address = None

        # 插入（包括 address 列）
        if my_address:
            sql = "INSERT OR REPLACE INTO phones (alias, phone_id, node_id, address, status) VALUES (?, ?, ?, ?, ?)"
            params = (alias, phone_id, self._my_node_id, my_address, self._status)
            logger.debug(f"[register] 执行: {sql} | params={params}")
            cur.execute(sql, params)
            logger.debug(f"[register] 插入记录: alias={alias}, phone_id={phone_id}, address={my_address}")
        else:
            sql = "INSERT OR REPLACE INTO phones (alias, phone_id, node_id, status) VALUES (?, ?, ?, ?)"
            params = (alias, phone_id, self._my_node_id, self._status)
            logger.debug(f"[register] 执行(无地址): {sql} | params={params}")
            cur.execute(sql, params)
        conn.commit()
        conn.close()

        self._my_phone_id = phone_id
        logger.info(f"注册成功: {phone_id}")
        return phone_id

    # --- 查询 ---
    def lookup(self, target: str) -> Optional[str]:
        """查询 node_id（仅用于 ClawMesh 模式）"""
        target = target.strip()
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if target.isdigit() and len(target) == 13:
            cur.execute("SELECT node_id FROM phones WHERE phone_id = ?", (target,))
            row = cur.fetchone()
            if row and row[0]:
                conn.close()
                return row[0]
        cur.execute("SELECT node_id FROM phones WHERE alias = ?", (target,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    def _get_target_info(self, target: str) -> Optional[tuple]:
        """获取目标 (node_id, address)"""
        target = target.strip()
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(phones)")
        cols = [row[1] for row in cur.fetchall()]
        has_address = "address" in cols
        logger.debug(f"[_get_target_info] target={target}, has_address={has_address}")

        if target.isdigit() and len(target) == 13:
            if has_address:
                sql = "SELECT node_id, address FROM phones WHERE phone_id = ?"
                cur.execute(sql, (target,))
            else:
                sql = "SELECT node_id FROM phones WHERE phone_id = ?"
                cur.execute(sql, (target,))
            row = cur.fetchone()
            logger.debug(f"[_get_target_info] phone_id query -> row={row}")
            if row:
                conn.close()
                if has_address:
                    return (row[0], row[1]) if row[0] else (None, row[1])
                else:
                    return (row[0], None)

        if has_address:
            cur.execute("SELECT node_id, address FROM phones WHERE alias = ?", (target,))
            sql = "SELECT node_id, address FROM phones WHERE alias = ?"
            cur.execute(sql, (target,))
        else:
            cur.execute("SELECT node_id FROM phones WHERE alias = ?", (target,))
        row = cur.fetchone()
        logger.debug(f"[_get_target_info] alias query -> row={row}")
        conn.close()
        if row:
            if has_address:
                return (row[0], row[1]) if row[0] else (None, row[1])
            else:
                return (row[0], None)
        return None

    # --- 呼叫 ---
    def call(self, target: str, message: str) -> bool:
        """呼叫（自动适配同步/异步适配器）"""
        if not self._adapter:
            logger.warning("网络适配器未设置")
            return False

        logger.debug(f"[call] target={target}, my_phone={self._my_phone_id}")
        info = self._get_target_info(target)
        logger.debug(f"[call] _get_target_info({target}) -> {info}")
        if not info:
            logger.warning(f"找不到目标: {target}")
            return False
        node_id, address = info
        logger.debug(f"[call] unpack -> node_id={node_id}, address={address}")

        payload = {
            "type": "call",
            "from": self._my_phone_id,
            "to": target,
            "content": message,
            "timestamp": time.time()
        }

        try:
            # 判断适配器类型
            if hasattr(self._adapter, 'get_my_address'):
                # DirectAdapter 需要 address
                if not address:
                    logger.warning(f"目标 {target} 无地址")
                    return False
                send_method = getattr(self._adapter, 'send', None)
                if send_method is None:
                    raise NotImplementedError("DirectAdapter 缺少 send 方法")
                # DirectAdapter.send(address, payload) - 同步
                logger.debug(f"调用 send: address={address}, payload_type={payload.get('type')}")
                result = send_method(address, payload)  # type: ignore
                logger.debug(f"send 返回类型: {type(result)} = {result}")
                success = bool(result)
            else:
                # ClawMesh 风格适配器
                if not node_id:
                    logger.warning(f"目标 {target} 无 node_id")
                    return False
                if hasattr(self._adapter, 'send_message'):
                    content = json.dumps(payload, ensure_ascii=False)
                    success = self._adapter.send_message(node_id, content, msg_type=payload.get("type", "custom"))
                elif hasattr(self._adapter, 'send'):
                    raw = json.dumps(payload, ensure_ascii=False)
                    success = self._adapter.send(node_id, raw)
                else:
                    raise NotImplementedError("适配器无 send/send_message")
            if success:
                self._log_call(target, message)
            return success
        except Exception as e:
            logger.error(f"发送失败: {e}")
            return False

    def _log_call(self, to_phone: str, message: str):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("INSERT INTO call_log (from_phone, to_phone, message) VALUES (?, ?, ?)",
                        (self._my_phone_id, to_phone, message))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"记录呼叫日志失败: {e}")

    # --- 状态与回调 ---
    def set_status(self, status: str):
        if status not in ("online", "away", "offline"):
            raise ValueError("状态必须是 online/away/offline")
        self._status = status

    @property
    def on_message(self) -> Optional[Callable]:
        return self._on_message

    @on_message.setter
    def on_message(self, callback: Callable[[Dict[str, Any]], None]):
        self._on_message = callback
        # 如果适配器需要设置回调（ClawMesh 模式），也设置
        if self._adapter and hasattr(self._adapter, 'on_message'):
            self._adapter.on_message = self._handle_network_message

    # --- 网络消息处理（ClawMesh 模式）---
    def _handle_network_message(self, raw_message: str):
        try:
            msg = json.loads(raw_message)
            if msg.get("type") in ("call", "message"):
                if self._on_message:
                    self._on_message(msg)
        except Exception as e:
            logger.error(f"处理网络消息失败: {e}")

    # --- 恢复注册 ---
    def _restore_registration(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(phones)")
        cols = [row[1] for row in cur.fetchall()]
        has_address = "address" in cols

        if self._my_node_id:
            if has_address:
                cur.execute(
                    "SELECT phone_id, node_id, address FROM phones WHERE node_id = ? ORDER BY created_at DESC LIMIT 1",
                    (self._my_node_id,)
                )
            else:
                cur.execute(
                    "SELECT phone_id, node_id FROM phones WHERE node_id = ? ORDER BY created_at DESC LIMIT 1",
                    (self._my_node_id,)
                )
        else:
            cur.execute("SELECT phone_id, node_id FROM phones ORDER BY created_at DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row:
            self._my_phone_id = row[0]
            if len(row) >= 2:
                self._my_node_id = row[1]
            if has_address and len(row) >= 3:
                self._my_address = row[2]
            logger.info(f"恢复号码: {self._my_phone_id}, address: {self._my_address or 'N/A'}")

    # --- 手动添加联系人 ---
    def add_contact(self, alias: str, phone_id: Optional[str] = None, address: Optional[str] = None, via: str = "direct") -> bool:
        """添加联系人。
        - alias: 联系人的别名（主键，必须唯一且非空）
        - phone_id: 对方的号码（可选，但建议提供）
        - address: 对方的网络地址（可选，但建议提供）
        - via: 网络类型 (如 "direct", "clawmesh")
        """
        if not alias:
            logger.warning("add_contact: alias is required")
            return False
        if not phone_id and not address:
            logger.warning("add_contact: at least phone_id or address required")
            return False
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(phones)")
            cols = [row[1] for row in cur.fetchall()]
            has_address = "address" in cols
            has_public_key = "public_key" in cols

            if has_address and has_public_key:
                sql = "INSERT OR REPLACE INTO phones (alias, phone_id, node_id, address, public_key, status) VALUES (?, ?, ?, ?, ?, ?)"
                params = (alias, phone_id, via, address, None, "online")
            elif has_address:
                sql = "INSERT OR REPLACE INTO phones (alias, phone_id, node_id, address, status) VALUES (?, ?, ?, ?, ?)"
                params = (alias, phone_id, via, address, "online")
            else:
                sql = "INSERT OR REPLACE INTO phones (alias, phone_id, node_id, status) VALUES (?, ?, ?, ?)"
                params = (alias, phone_id, via, "online")

            cur.execute(sql, params)
            conn.commit()
            conn.close()
            logger.info(f"添加联系人: {alias} (phone_id={phone_id}, address={address})")
            return True
        except Exception as e:
            logger.error(f"添加联系人失败: {e}")
            return False

    def get_my_phone(self) -> Optional[str]:
        return self._my_phone_id

    def get_my_address(self) -> Optional[str]:
        return self._my_address


# 全局实例
_phone = ClawPhone()


# Skill API 入口
def skill_main(**kwargs):
    return {
        "phone_id": _phone.get_my_phone(),
        "capabilities": ["register", "call", "lookup", "set_status", "on_message", "add_contact", "start_direct_mode"]
    }


def register(alias: str) -> str:
    return _phone.register(alias)


def lookup(target: str) -> Optional[str]:
    return _phone.lookup(target)


def call(target: str, message: str) -> bool:
    return _phone.call(target, message)


def set_status(status: str):
    _phone.set_status(status)


def on_message(callback: Callable[[Dict[str, Any]], None]):
    _phone.on_message = callback


def set_network(network):
    _phone.set_network(network)


def set_adapter(adapter):
    _phone.set_adapter(adapter)


async def start_direct_mode(port: int = 0) -> str:
    """
    启动内置 Direct P2P 模式（不依赖 ClawMesh）
    返回本节点地址 "127.0.0.1:port"
    """
    from .direct import DirectAdapter
    # 生成或获取 node_id（如果没有，用 phone_id 代替）
    node_id = _phone._my_node_id or _phone._my_phone_id or "unknown"
    adapter = DirectAdapter(node_id, port)
    # DirectAdapter.start() 现在是同步方法（启动后台线程）
    address = adapter.start()
    _phone.set_adapter(adapter)
    return address
