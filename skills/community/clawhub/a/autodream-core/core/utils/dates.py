"""
日期处理工具

相对日期转换。
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Union


def parse_relative_dates(text: str, reference_date: datetime = None) -> str:
    """
    将相对日期转换为绝对日期
    
    示例:
    - "昨天我们决定使用 Redis" → "2026-04-01 我们决定使用 Redis"
    - "上周修复了这个 bug" → "2026-03-26 修复了这个 bug"
    
    参数:
        text: 包含相对日期的文本
        reference_date: 参考日期（默认当前 UTC 时间）
        
    返回:
        替换后的文本
    """
    if reference_date is None:
        reference_date = datetime.now(timezone.utc)
    
    today = reference_date.date()
    
    # 常见相对日期模式（中文不使用\b，因为中文没有单词边界）
    patterns = [
        (r'昨天', (today - timedelta(days=1)).isoformat()),
        (r'前天', (today - timedelta(days=2)).isoformat()),
        (r'今天', today.isoformat()),
        (r'明天', (today + timedelta(days=1)).isoformat()),
        (r'上周', (today - timedelta(days=7)).isoformat()),
        (r'本周', today.isoformat()),
        (r'下周', (today + timedelta(days=7)).isoformat()),
        (r'上个月', (today.replace(day=1) - timedelta(days=1)).strftime('%Y-%m')),
        (r'这个月', today.strftime('%Y-%m')),
        (r'前几天', (today - timedelta(days=3)).isoformat()),
        (r'最近', (today - timedelta(days=7)).isoformat()),
        # 英文相对日期（使用\b 单词边界）
        (r'\byesterday\b', (today - timedelta(days=1)).isoformat()),
        (r'\blast week\b', (today - timedelta(days=7)).isoformat()),
        (r'\btoday\b', today.isoformat()),
        (r'\bthis week\b', today.isoformat()),
    ]
    
    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result


def is_stale(entry: dict, workspace_path) -> bool:
    """
    检测条目是否过时
    
    过时场景:
    - 引用的文件不存在
    - 引用的路径已删除
    
    参数:
        entry: 条目 {"text": "..."}
        workspace_path: 工作区路径
        
    返回:
        是否过时
    """
    text = entry.get("text", "")
    
    # 检测文件路径引用
    path_patterns = [
        r'[/\\][\w./-]+\.\w+',  # 绝对路径
        r'[\w./-]+\.(py|js|ts|md|json|yaml|yml|txt|cfg|conf)',  # 相对路径
    ]
    
    for pattern in path_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # 检查文件是否存在
            if match.startswith('/'):
                path = workspace_path / match[1:]  # 去掉开头的/
            else:
                path = workspace_path / match
            
            if not path.exists():
                # 文件不存在且文本包含"存在"关键词
                if any(kw in text for kw in ["存在", "位于", "path", "file"]):
                    return True
    
    return False
