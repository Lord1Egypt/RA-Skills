#!/Users/bot-eva/.openclaw/workspace/venvs/doc-watcher/bin/python3
"""
文档实时监控脚本 - 通用版

核心特性：
- 自动读取 OpenClaw 配置的通道（无需手动配置）
- 支持所有 OpenClaw 通道插件
- 零配置启动（默认监控 workspace/docs/*.md）

使用：
python3 bin/doc-watcher.py
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 工作目录
WORKSPACE = Path.home() / ".openclaw" / "workspace"
DOCS_DIR = WORKSPACE / "docs"
LOG_DIR = WORKSPACE / "logs"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "config" / "openclaw.json"

# 监控范围：workspace/docs/ 下所有 Markdown 文件
WATCH_PATTERN = "*.md"

# 变更历史文件
CHANGE_HISTORY_FILE = LOG_DIR / "doc_change_history.json"


def load_openclaw_channels():
    """
    自动读取 OpenClaw 配置的通道
    
    读取 ~/.openclaw/config/openclaw.json 中的 channels 配置
    返回所有 enabled: true 的通道列表
    
    Returns:
        list: 通道名称列表，如 ["feishu", "imessage"]
    """
    if not OPENCLAW_CONFIG.exists():
        print(f"⚠️ 未找到 OpenClaw 配置文件：{OPENCLAW_CONFIG}")
        print("  将使用默认通道：webchat")
        return ["webchat"]
    
    try:
        with open(OPENCLAW_CONFIG, 'r') as f:
            config = json.load(f)
        
        # 从 channels 字段读取
        channels_config = config.get('channels', {})
        enabled_channels = []
        
        for channel_name, channel_config in channels_config.items():
            if isinstance(channel_config, dict) and channel_config.get('enabled', False):
                enabled_channels.append(channel_name)
        
        # 如果 channels 为空，从 plugins.entries 读取
        if not enabled_channels:
            plugins_config = config.get('plugins', {}).get('entries', {})
            for plugin_name, plugin_config in plugins_config.items():
                if isinstance(plugin_config, dict) and plugin_config.get('enabled', False):
                    enabled_channels.append(plugin_name)
        
        # 如果还是没有，使用 webchat 作为兜底
        if not enabled_channels:
            print("⚠️ 未找到已启用的通道，使用默认通道：webchat")
            enabled_channels = ["webchat"]
        
        print(f"✅ 自动检测到 {len(enabled_channels)} 个通道：{', '.join(enabled_channels)}")
        return enabled_channels
    
    except Exception as e:
        print(f"⚠️ 读取 OpenClaw 配置失败：{e}")
        print("  将使用默认通道：webchat")
        return ["webchat"]


class DocChangeHandler(FileSystemEventHandler):
    """文档变更处理器"""
    
    def __init__(self, channels=None):
        super().__init__()
        self.channels = channels or load_openclaw_channels()
        self.file_hashes = {}
        self._init_hashes()
    
    def _init_hashes(self):
        """初始化文件哈希 - 监控 docs/ 下所有.md 文件"""
        if DOCS_DIR.exists():
            for filepath in DOCS_DIR.glob(WATCH_PATTERN):
                if filepath.is_file():
                    self.file_hashes[str(filepath)] = self._calculate_hash(filepath)
                    print(f"  📄 监控：{filepath.name}")
    
    def _calculate_hash(self, filepath):
        """计算文件哈希"""
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _get_changes(self, filepath):
        """读取变更内容（简化版：返回文件路径和时间）"""
        return {
            "file": str(filepath),
            "time": datetime.now().isoformat(),
            "size": filepath.stat().st_size,
        }
    
    def _notify_channels(self, change_info):
        """
        通知所有已配置的通道
        
        使用 OpenClaw 消息系统发送通知到所有通道
        """
        # 记录变更历史
        self._log_change(change_info)
        
        # 打印通知
        print(f"\n📢 [文档变更通知] {datetime.now().strftime('%H:%M:%S')}")
        print(f"   文件：{change_info['file']}")
        print(f"   时间：{change_info['time']}")
        print(f"   大小：{change_info['size']} bytes")
        print(f"   通道：{', '.join(self.channels)}")
        print(f"   要求：5 分钟内确认，30 分钟内评估\n")
        
        # TODO: 集成 OpenClaw 消息系统
        # for channel in self.channels:
        #     send_to_channel(channel, f"文档变更：{change_info['file']}")
    
    def _log_change(self, change_info):
        """记录变更历史"""
        history = []
        if CHANGE_HISTORY_FILE.exists():
            with open(CHANGE_HISTORY_FILE, 'r') as f:
                history = json.load(f)
        
        history.append(change_info)
        
        # 保留最近 100 条记录
        if len(history) > 100:
            history = history[-100:]
        
        with open(CHANGE_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def on_modified(self, event):
        """文件修改事件 - 监控 docs/ 下所有.md 文件"""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        # 只监控 docs/ 目录下的.md 文件
        if filepath.parent != DOCS_DIR or filepath.suffix != '.md':
            return
        
        # 计算新哈希
        new_hash = self._calculate_hash(filepath)
        old_hash = self.file_hashes.get(str(filepath))
        
        if new_hash == old_hash:
            return  # 文件内容未变
        
        # 检测到变更
        print(f"\n🔍 检测到文档变更：{filepath.name}")
        
        # 更新哈希
        self.file_hashes[str(filepath)] = new_hash
        
        # 发送通知
        change_info = self._get_changes(filepath)
        self._notify_channels(change_info)
    
    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        # 只监控 docs/ 目录下的.md 文件
        if filepath.parent != DOCS_DIR or filepath.suffix != '.md':
            return
        
        print(f"\n📄 新协作文档创建：{filepath.name}")
        self.file_hashes[str(filepath)] = self._calculate_hash(filepath)


def main():
    """主函数"""
    print("=" * 60)
    print("📄 Doc-Collaboration-Watcher v1.5")
    print("=" * 60)
    print(f"工作目录：{WORKSPACE}")
    print(f"监控目录：{DOCS_DIR}")
    print(f"文件模式：{WATCH_PATTERN}")
    print()
    
    # 自动读取通道
    print("🔌 检测通道配置...")
    channels = load_openclaw_channels()
    print()
    
    # 检查监控目录
    if not DOCS_DIR.exists():
        print(f"❌ 监控目录不存在：{DOCS_DIR}")
        print("  请创建目录或修改配置")
        sys.exit(1)
    
    # 启动监控
    print("🚀 启动文档监控...")
    print()
    
    event_handler = DocChangeHandler(channels=channels)
    observer = Observer()
    observer.schedule(event_handler, str(DOCS_DIR), recursive=False)
    observer.start()
    
    print("✅ 监控已启动（按 Ctrl+C 停止）")
    print()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 监控已停止")
    observer.join()


if __name__ == "__main__":
    main()
