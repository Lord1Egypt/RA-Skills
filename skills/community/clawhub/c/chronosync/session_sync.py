#!/usr/bin/env python3
"""
Session Sync - 跨会话记忆同步与知识沉淀系统

核心功能：
- 30分钟静默同步
- 增量写入，零冗余
- JSON + Markdown 双格式输出
- 插件化扩展
"""

import json
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

# Windows 控制台 UTF-8 编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


# ========== 插件基类 ==========
from plugin_base import Plugin

# 配置 - 优先从环境变量读取
def get_openclaw_dir() -> Path:
    """获取 OpenClaw 目录，支持多种方式"""
    # 1. 环境变量
    if "OPENCLAW_STATE_DIR" in os.environ:
        return Path(os.environ["OPENCLAW_STATE_DIR"])
    
    # 2. 默认位置（跨平台）
    home = Path.home()
    
    # Windows
    if os.name == 'nt':
        default = home / ".openclaw"
    else:
        # Linux/Mac
        default = home / ".openclaw"
    
    return default

OPENCLAW_DIR = get_openclaw_dir()
OUTPUT_DIR = Path(os.environ.get("SESSION_SYNC_OUTPUT", OPENCLAW_DIR / "workspace" / "memory" / "sync"))

# 尝试多种可能的 sessions 目录
SESSIONS_DIR_CANDIDATES = [
    OPENCLAW_DIR / "agents" / "main" / "sessions",  # OpenClaw 2026.3.x 新路径
    OPENCLAW_DIR / "sessions",
    OPENCLAW_DIR / "workspace" / "sessions",
    Path.home() / ".openclaw" / "sessions",
]

def get_sessions_dir() -> Optional[Path]:
    """查找有效的 sessions 目录"""
    for candidate in SESSIONS_DIR_CANDIDATES:
        if candidate.exists():
            return candidate
    # 返回第一个作为默认值（即使不存在）
    return SESSIONS_DIR_CANDIDATES[0]

SESSIONS_DIR = get_sessions_dir()
HASH_FILE = OUTPUT_DIR / ".last_hash"

# 敏感信息脱敏模式
SENSITIVE_PATTERNS = [
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),  # 邮箱
    (r'\b\d{11}\b', '[PHONE]'),  # 手机号
    (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[CARD]'),  # 银行卡
    (r'\b[A-Za-z0-9]{32,}\b', '[TOKEN]'),  # API Token
]


def sanitize_content(content: str) -> str:
    """脱敏处理"""
    for pattern, replacement in SENSITIVE_PATTERNS:
        content = re.sub(pattern, replacement, content)
    return content


class ChangeDetector:
    """变化检测器 - 使用 SHA256 计算内容 hash"""

    @staticmethod
    def calculate_hash(content: str) -> str:
        """计算内容的 SHA256 hash"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

    @staticmethod
    def has_changed(session_id: str, new_content: str) -> bool:
        """检查内容是否变化"""
        if not HASH_FILE.exists():
            return True

        try:
            with open(HASH_FILE, 'r', encoding='utf-8') as f:
                hashes = json.load(f)
            last_hash = hashes.get(session_id, "")
            current_hash = ChangeDetector.calculate_hash(new_content)
            return last_hash != current_hash
        except (json.JSONDecodeError, IOError):
            return True

    @staticmethod
    def save_hash(session_id: str, content: str):
        """保存当前 hash"""
        hashes = {}
        if HASH_FILE.exists():
            try:
                with open(HASH_FILE, 'r', encoding='utf-8') as f:
                    hashes = json.load(f)
            except (json.JSONDecodeError, IOError):
                hashes = {}

        hashes[session_id] = ChangeDetector.calculate_hash(content)
        HASH_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HASH_FILE, 'w', encoding='utf-8') as f:
            json.dump(hashes, f, indent=2)


class FileManager:
    """文件管理器 - 负责 JSON 和 Markdown 输出"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.json_file = output_dir / "shared_chat.json"
        self.md_file = output_dir / "shared_chat.md"
        self.ensure_dirs()

    def ensure_dirs(self):
        """确保目录存在"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            (self.output_dir / "decisions").mkdir(exist_ok=True)
            (self.output_dir / "todos").mkdir(exist_ok=True)
        except OSError as e:
            print(f"[Session Sync] 创建目录失败: {e}")
            raise

    def read_existing_json(self) -> Dict:
        """读取现有 JSON 文件"""
        if self.json_file.exists():
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"last_sync": "", "sessions": []}

    def append_json(self, session_data: Dict):
        """追加到 JSON 文件"""
        data = self.read_existing_json()

        # 更新或添加会话
        existing = [s for s in data["sessions"] if s["id"] != session_data["id"]]
        existing.append(session_data)
        data["sessions"] = existing[-100:]  # 只保留最近100个会话
        data["last_sync"] = datetime.now().isoformat()

        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"[Session Sync] 写入 JSON 失败: {e}")

    def append_markdown(self, session_data: Dict):
        """追加到 Markdown 文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        md_content = f"\n\n## {timestamp}\n\n"

        for msg in session_data.get("messages", []):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # 脱敏处理
            content = sanitize_content(content)

            if role == "user":
                md_content += f"**用户:** {content}\n\n"
            elif role == "assistant":
                md_content += f"**AI:** {content}\n\n"

        # 追加写入
        try:
            with open(self.md_file, 'a', encoding='utf-8') as f:
                f.write(md_content)
        except IOError as e:
            print(f"[Session Sync] 写入 Markdown 失败: {e}")


class PluginManager:
    """插件管理器"""

    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        """加载插件"""
        plugins_dir = Path(__file__).parent / "plugins"
        if not plugins_dir.exists():
            return

        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            try:
                # 动态导入插件
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    plugin_file.stem, plugin_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 查找插件实例
                if hasattr(module, 'plugin'):
                    self.plugins.append(module.plugin)
                    print(f"[Session Sync] 插件已加载: {module.plugin.name}")
            except Exception as e:
                print(f"[Session Sync] 加载插件 {plugin_file.name} 失败: {e}")

    def process(self, messages: List[Dict]):
        """处理消息"""
        for plugin in self.plugins:
            try:
                plugin.on_sync(messages)
            except Exception as e:
                print(f"[Session Sync] 插件 {plugin.name} 处理失败: {e}")


class SyncEngine:
    """同步引擎 - 核心逻辑"""

    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.file_manager = FileManager(self.output_dir)
        self.detector = ChangeDetector()
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

    def get_session_content(self, session_id: str) -> Optional[str]:
        """获取会话内容"""
        session_file = SESSIONS_DIR / f"{session_id}.jsonl"
        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            return None

    def parse_messages(self, content: str) -> List[Dict]:
        """解析消息内容"""
        messages = []
        for line in content.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                # 脱敏处理
                msg_content = msg.get("content", "")
                msg_content = sanitize_content(msg_content)

                messages.append({
                    "role": msg.get("role", "unknown"),
                    "content": msg_content,
                    "timestamp": msg.get("timestamp", "")
                })
            except json.JSONDecodeError:
                continue
        return messages
    
    def sync_session(self, session_id: str) -> bool:
        """同步单个会话"""
        content = self.get_session_content(session_id)
        if not content:
            return False
        
        # 检查是否变化
        if not self.detector.has_changed(session_id, content):
            return False
        
        # 解析消息
        messages = self.parse_messages(content)
        if not messages:
            return False
        
        # 构建会话数据
        session_data = {
            "id": session_id,
            "timestamp": datetime.now().isoformat(),
            "hash": self.detector.calculate_hash(content),
            "message_count": len(messages),
            "messages": messages[-50:]  # 只保留最近50条
        }
        
        # 写入文件
        self.file_manager.append_json(session_data)
        self.file_manager.append_markdown(session_data)
        self.detector.save_hash(session_id, content)
        
        # 触发插件
        self.plugin_manager.process(messages)
        
        return True
    
    def sync_all(self):
        """同步所有会话"""
        if not SESSIONS_DIR.exists():
            return
        
        synced_count = 0
        for session_file in SESSIONS_DIR.glob("*.jsonl"):
            session_id = session_file.stem
            if self.sync_session(session_id):
                synced_count += 1
        
        return synced_count


def main():
    """主入口"""
    engine = SyncEngine()
    
    # 显示找到的会话文件
    if SESSIONS_DIR.exists():
        session_files = list(SESSIONS_DIR.glob("*.jsonl"))
        print(f"[Session Sync] 找到 {len(session_files)} 个会话文件")
    
    count = engine.sync_all()
    print(f"[Session Sync] 完成: {count} 个会话已同步")


if __name__ == "__main__":
    main()