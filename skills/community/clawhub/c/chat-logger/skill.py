"""
Chat Logger Skill - 对话记录 V3

自动记录飞书/钉钉消息 - 主动调用模式，不依赖 Hook
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict


class ChatLoggerSkill:
    """对话记录 Skill - V3 主动调用模式"""

    def __init__(self):
        self.enabled = True
        self.base_dir = Path.home() / '.openclaw' / 'workspace' / 'memory' / 'chat-logs'
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _safe_name(self, name: str) -> str:
        """清理名称，移除非法字符"""
        return re.sub(r'[\\/:*?"<>|]', '_', name)

    def _get_channel_dir(self, channel: str) -> Path:
        """获取渠道目录（支持中英文）"""
        channel_map = {
            'feishu': 'feishu',
            'dingtalk': 'dingtalk',
            '飞书': 'feishu',
            '钉钉': 'dingtalk'
        }
        channel_en = channel_map.get(channel, channel)
        return self.base_dir / channel_en

    def write_message(self, channel: str, user_name: str, user_content: str) -> bool:
        """
        写入用户消息到文件

        Args:
            channel: 渠道名称 (feishu/dingtalk/飞书/钉钉)
            user_name: 用户名称
            user_content: 用户消息内容

        Returns:
            是否写入成功
        """
        if not self.enabled:
            return False

        try:
            date = datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.now().strftime('%H:%M')

            # 获取渠道目录
            channel_dir = self._get_channel_dir(channel)
            user_dir = channel_dir / self._safe_name(user_name)
            user_dir.mkdir(parents=True, exist_ok=True)

            file_path = user_dir / f"{date}.md"

            # 创建文件头（如果是新文件）
            if not file_path.exists():
                header = f"# {date} 提问记录 - {user_name}（{channel}）\n\n## 提问列表\n\n---\n\n"
                file_path.write_text(header, encoding='utf-8')

            # 追加消息
            entry = f"\n### {time_str}\n**用户**：{user_content}\n"

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(entry)

            return True

        except Exception as e:
            print(f"[ChatLogger] 写入失败: {e}")
            return False


# 全局实例（单例模式）
_chat_logger = ChatLoggerSkill()


def record_message(channel: str, user_name: str, user_content: str) -> bool:
    """
    主动记录消息 - 主 Agent 调用入口

    Args:
        channel: 渠道名称 (feishu/dingtalk/飞书/钉钉)
        user_name: 用户名称
        user_content: 用户消息内容

    Returns:
        是否记录成功

    Example:
        >>> from skills.chat_logger.skill import record_message
        >>> record_message('dingtalk', '孟凡军', '测试消息')
        True
    """
    return _chat_logger.write_message(channel, user_name, user_content)


def get_daily_summary(date: Optional[str] = None) -> str:
    """
    生成每日简报

    Args:
        date: 日期字符串 (YYYY-MM-DD)，默认为今天

    Returns:
        格式化的每日简报
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    base_dir = Path.home() / '.openclaw' / 'workspace' / 'memory' / 'chat-logs'

    lines = [f"# {date} 提问记录\n"]
    total = 0

    # 渠道名称映射（英文 -> 中文显示）
    channel_display = {
        'feishu': '飞书',
        'dingtalk': '钉钉'
    }

    # 遍历所有渠道
    for channel_dir in sorted(base_dir.iterdir()):
        if not channel_dir.is_dir():
            continue

        channel_en = channel_dir.name
        channel_name = channel_display.get(channel_en, channel_en)
        channel_total = 0
        channel_lines = []

        # 遍历用户
        for user_dir in sorted(channel_dir.iterdir()):
            if not user_dir.is_dir():
                continue

            user_name_dir = user_dir.name
            file_path = user_dir / f"{date}.md"

            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                msg_count = content.count('**用户**：')
                if msg_count > 0:
                    channel_total += msg_count
                    channel_lines.append(f"  - {user_name_dir}: {msg_count} 条")

        if channel_total > 0:
            lines.append(f"\n## {channel_name}（{channel_total} 条）")
            lines.extend(channel_lines)
            total += channel_total

    lines.insert(1, f"\n总计: {total} 条提问\n")

    return '\n'.join(lines)


def get_chatlog_summary() -> str:
    """
    生成完整的 ChatLog 汇总（所有用户、所有日期）

    Returns:
        格式化的完整汇总报告
    """
    base_dir = Path.home() / '.openclaw' / 'workspace' / 'memory' / 'chat-logs'

    if not base_dir.exists():
        return "暂无聊天记录"

    # 渠道名称映射
    channel_display = {
        'feishu': '飞书',
        'dingtalk': '钉钉'
    }

    # 数据结构
    from collections import defaultdict
    user_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    user_channel_totals = defaultdict(lambda: defaultdict(int))
    user_messages = defaultdict(lambda: defaultdict(list))

    grand_total = 0

    # 遍历所有渠道
    for channel_dir in sorted(base_dir.iterdir()):
        if not channel_dir.is_dir():
            continue

        channel_en = channel_dir.name
        channel_name = channel_display.get(channel_en, channel_en)

        # 遍历用户
        for user_dir in sorted(channel_dir.iterdir()):
            if not user_dir.is_dir():
                continue

            user_name = user_dir.name

            # 遍历该用户的所有日期文件
            for file_path in sorted(user_dir.glob("*.md")):
                if not file_path.is_file():
                    continue

                date_str = file_path.stem
                content = file_path.read_text(encoding='utf-8')
                msg_count = content.count('**用户**：')

                if msg_count > 0:
                    user_data[user_name][date_str][channel_name] += msg_count
                    user_channel_totals[user_name][channel_name] += msg_count
                    grand_total += msg_count

                    # 解析详细消息内容
                    pattern = r'###\s+(\d{2}:\d{2})\s*\n\*\*用户\*\*：(.+?)(?=\n###|\n## |\Z)'
                    matches = re.findall(pattern, content, re.DOTALL)
                    for time_str, msg_content in matches:
                        msg_content = msg_content.strip()
                        if msg_content:
                            user_messages[user_name][date_str].append({
                                'time': time_str,
                                'channel': channel_name,
                                'content': msg_content[:100] + '...' if len(msg_content) > 100 else msg_content
                            })

    # 生成报告
    lines = ["# 📊 ChatLog 汇总\n"]
    lines.append(f"\n**总计: {grand_total} 条消息**\n")

    # 按用户分组显示
    for user_name in sorted(user_data.keys()):
        user_dates = user_data[user_name]
        user_total = sum(sum(channels.values()) for channels in user_dates.values())
        user_channels = user_channel_totals[user_name]

        lines.append(f"\n## 👤 {user_name} - {user_total} 条")

        # 渠道分布
        channel_summary = " | ".join([f"{ch}: {cnt}条" for ch, cnt in sorted(user_channels.items())])
        lines.append(f"*渠道分布: {channel_summary}*")

        # 按日期显示
        for date_str in sorted(user_dates.keys(), reverse=True):
            channels = user_dates[date_str]
            date_total = sum(channels.values())

            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                date_display = f"{dt.month}月{dt.day}日"
            except:
                date_display = date_str

            channel_details = " | ".join([f"{ch}: {cnt}条" for ch, cnt in sorted(channels.items())])
            lines.append(f"\n### {date_display} ({date_total} 条)")

            # 显示详细消息
            if user_messages[user_name][date_str]:
                sorted_msgs = sorted(user_messages[user_name][date_str], key=lambda x: x['time'])
                for msg in sorted_msgs:
                    lines.append(f"  - [{msg['time']}] [{msg['channel']}] {msg['content']}")

    # 添加用户汇总表
    lines.append("\n---\n")
    lines.append("## 📈 用户统计")
    lines.append("\n| 用户 | 总消息数 | 渠道分布 |")
    lines.append("|:---|---:|:---|")

    sorted_users = sorted(user_data.keys(),
                         key=lambda u: sum(sum(c.values()) for c in user_data[u].values()),
                         reverse=True)

    for user_name in sorted_users:
        user_total = sum(sum(channels.values()) for channels in user_data[user_name].values())
        channels = user_channel_totals[user_name]
        channel_str = " | ".join([f"{ch}: {cnt}" for ch, cnt in sorted(channels.items())])
        lines.append(f"| {user_name} | {user_total} | {channel_str} |")

    return '\n'.join(lines)


def handle_chat_query(message: str, user_name: str, channel: str = None) -> Optional[str]:
    """
    处理查询指令

    Args:
        message: 查询消息
        user_name: 用户名
        channel: 渠道名称（可选，用于记录当前查询）

    Returns:
        查询结果或 None
    """
    message = message.strip()

    # 记录当前查询消息
    if channel:
        record_message(channel, user_name, message)

    if "今日简报" in message or "今天简报" in message:
        return get_daily_summary()

    if "我的记录" in message or "我的简报" in message:
        return get_daily_summary()

    if "chatlog汇总" in message.lower() or "chatlog" in message.lower():
        return get_chatlog_summary()

    return None


# ============ Hook 入口（方案B：双保险）============

def on_incoming_message_hook(channel: str, sender_id: str, 
                             sender_name: str, content: str, **kwargs) -> dict:
    """
    OpenClaw Hook 入口 - 自动记录消息
    
    方案B：Hook + 显式调用双保险
    - Hook 自动记录（无需主 Agent 干预）
    - 主 Agent 也显式调用 record_message()（备用）
    """
    try:
        chat_type = kwargs.get('chat_type', 'direct')
        
        # 只记录私聊
        if chat_type != 'direct':
            return {'success': True, 'skipped': 'group_chat'}
        
        # 调用核心记录函数
        success = _chat_logger.record_message(channel, sender_name, content, chat_type)
        
        return {'success': success, 'recorded': success}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def on_ai_response_callback(ai_response: str, **kwargs) -> bool:
    """
    OpenClaw afterReply Hook 入口
    
    当前不记录 AI 回复（只记录用户提问）
    """
    return True