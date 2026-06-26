#!/usr/bin/env python3
"""
Memory Keeper - 每日记忆管家 v1.0.0
自动提取会话内容并更新每日记忆文件
"""

import os
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from difflib import SequenceMatcher

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CONFIG_FILE = Path(__file__).parent / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "memory_dir": str(MEMORY_DIR),
    "interval_hours": 1,
    "active_minutes": 60,
    "categories": ["决策", "事项", "进展", "问题", "结论"],
    "skip_patterns": [
        r"^你好", r"^hi", r"^hey", r"^hello",
        r"^谢谢", r"^感谢", r"^感激",
        r"^好的", r"^收到", r"^ok", r"^sure", r"^是$", r"^是的",
        r"^？", r"^\?",
        r"^ HEARTBEAT_OK"
    ],
    "dedup_threshold": 0.8
}


def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            pass
    return DEFAULT_CONFIG


def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_today():
    """获取今天的日期字符串"""
    return datetime.now().strftime("%Y-%m-%d")


def get_now_time():
    """获取当前时间字符串"""
    return datetime.now().strftime("%H:%M")


def get_memory_file_path():
    """获取今天记忆文件的路径"""
    config = load_config()
    memory_dir = Path(config["memory_dir"]).expanduser()
    today = get_today()
    return memory_dir / f"{today}.md"


def ensure_memory_dir():
    """确保 memory 目录存在"""
    config = load_config()
    memory_dir = Path(config["memory_dir"]).expanduser()
    memory_dir.mkdir(parents=True, exist_ok=True)


def create_empty_memory_file():
    """创建空的记忆文件模板"""
    file_path = get_memory_file_path()
    if not file_path.exists():
        content = f"""# {get_today()} 日志

## 今日事项

- 

---
*由 memory-keeper 自动创建*
"""
        file_path.write_text(content, encoding="utf-8")
        print(f"✓ 已创建记忆文件: {file_path}")
    return file_path


def read_today_memory():
    """读取今天的记忆文件内容"""
    file_path = get_memory_file_path()
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return None


def is_noise(message, config):
    """判断消息是否为噪音"""
    if not message or len(message.strip()) < 2:
        return True
    
    msg = message.strip()
    
    # 检查跳过模式
    for pattern in config.get("skip_patterns", []):
        if re.match(pattern, msg, re.IGNORECASE):
            return True
    
    # 跳过太短的消息
    if len(msg) < 4:
        return True
    
    return False


def extract_key_info(message):
    """从消息中提取关键信息"""
    # 简单规则：提取动词+关键内容
    patterns = [
        (r'(安装|创建|添加|配置|设置|完成|修复|更新|修改|删除).*', '进展'),
        (r'(决定|选择|采用|使用|不要|拒绝).*', '决策'),
        (r'(问题|报错|错误|失败|bug).*', '问题'),
        (r'(总结|结论|发现|原来|其实).*', '结论'),
    ]
    
    for pattern, category in patterns:
        if re.search(pattern, message):
            return category, message
    
    return '事项', message


def is_duplicate(new_item, existing_items, threshold=0.8):
    """检查是否重复"""
    new_lower = new_item.lower()
    for item in existing_items:
        if SequenceMatcher(None, new_lower, item.lower()).ratio() > threshold:
            return True
    return False


def get_recent_sessions(config):
    """获取最近的会话"""
    try:
        # 调用 sessions_list 获取活跃会话
        result = subprocess.run(
            ["openclaw", "sessions", "list", "--active-minutes", str(config.get("active_minutes", 60)), "--limit", "5"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # 解析输出（简化版）
            return result.stdout
    except Exception as e:
        print(f"获取会话失败: {e}")
    
    return None


def format_memory_entry(time_str, category, content):
    """格式化记忆条目"""
    # 简化内容，去除多余空白
    content = ' '.join(content.split())
    return f"- {time_str} {content}"


def update_memory(new_entries):
    """更新记忆文件"""
    if not new_entries:
        print("没有新内容需要记录")
        return
    
    file_path = get_memory_file_path()
    content = read_today_memory()
    
    if content is None:
        create_empty_memory_file()
        content = read_today_memory()
    
    # 提取现有条目
    existing_items = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- ') and not line.startswith('---'):
            existing_items.append(line[2:])
    
    # 过滤重复
    unique_entries = []
    for entry in new_entries:
        if not is_duplicate(entry, existing_items):
            unique_entries.append(entry)
            existing_items.append(entry)
    
    if not unique_entries:
        print("没有新内容（已重复）")
        return
    
    # 追加新内容
    new_content = content.rstrip()
    if not new_content.endswith('\n'):
        new_content += '\n'
    
    for entry in unique_entries:
        new_content += '\n' + entry
    
    file_path.write_text(new_content, encoding='utf-8')
    print(f"✓ 已更新记忆文件，添加 {len(unique_entries)} 条记录")


def main():
    """主函数"""
    print("🧠 Memory Keeper v1.0.0 开始执行...")
    
    config = load_config()
    
    # 确保目录存在
    ensure_memory_dir()
    
    # 创建或检查今天的记忆文件
    create_empty_memory_file()
    
    # 获取最近会话（这里需要通过 agent 调用来获取）
    # 当前版本：返回提示信息
    print("📡 会话获取需要在 agent 上下文中执行")
    print(f"📁 记忆文件位置: {get_memory_file_path()}")
    print("✅ Memory Keeper 执行完成")


if __name__ == "__main__":
    main()
