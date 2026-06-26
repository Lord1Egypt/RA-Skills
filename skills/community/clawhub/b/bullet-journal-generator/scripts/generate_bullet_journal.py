#!/usr/bin/env python3
"""
生成标准化子弹笔记文本
"""

import sys
from datetime import datetime
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.process_notes import NoteProcessor


def generate_bullet_journal(
    date: str,
    weather: str,
    temperature: str,
    notes_data: list
) -> str:
    """
    生成标准化子弹笔记

    Args:
        date: 日期（YYYY-MM-DD）
        weather: 天气（晴/多云/雨等）
        temperature: 温度（如 "15°C"）
        notes_data: 笔记数据列表

    Returns:
        格式化后的子弹笔记文本
    """
    # 解析日期
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    week_day = week_days[date_obj.weekday()]

    # 天气图标映射
    weather_icons = {
        '晴': '☀️',
        '多云': '☁️',
        '阴': '☁️',
        '雨': '🌧️',
        '小雨': '🌦️',
        '大雨': '⛈️',
        '雪': '❄️',
        '风': '💨',
        '雾': '🌫️'
    }
    weather_icon = weather_icons.get(weather, '🌡️')

    # 生成标题
    header = f"{date} ({week_day}) | {weather_icon} {weather} | {temperature}"

    # 生成笔记内容
    note_lines = []
    for note in notes_data:
        # 格式化每条笔记
        parts = [note['symbol']]

        if note.get('time'):
            parts.append(note['time'])

        parts.append(note['content'])

        line = ' '.join(parts)
        note_lines.append(line)

    # 组合完整文本
    bullet_journal = f"{header}\n\n" + '\n'.join(note_lines)

    return bullet_journal


def main():
    """测试用例"""
    processor = NoteProcessor()

    # 示例输入
    example_input = """09:00 今天要把有机逆合成的逻辑和思路整理出来最好自动化。去买卫生纸，预约羽毛球场地
09:17 老板突然紧急需要交给政府的立项书，我先把摘要写出来
明天家家悦有打折的鸡蛋
最近的股票市场波动比较大，要尝试新的分析方法了"""

    # 处理输入
    notes = processor.parse_input(example_input)

    # 生成子弹笔记
    bullet_journal = generate_bullet_journal(
        date='2025-03-16',
        weather='晴',
        temperature='15°C',
        notes_data=notes
    )

    print(bullet_journal)


if __name__ == '__main__':
    from datetime import datetime
    main()
