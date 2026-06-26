#!/usr/bin/env python3
"""
生成交互式HTML卡片
支持任务状态变化和事件详细信息
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from task_manager import TaskManager


class InteractiveCardGenerator:
    """交互式卡片生成器"""

    def __init__(self, template_path: str = None, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))

        self.base_dir = base_dir

        if template_path is None:
            template_path = os.path.join(
                base_dir,
                'templates',
                'interactive_card_template.html'
            )
        self.template_path = template_path
        self.task_manager = TaskManager(base_dir)

    def get_weather_icon(self, weather: str) -> str:
        """获取天气图标"""
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
        return weather_icons.get(weather, '🌡️')

    def format_date_display(self, date: str) -> str:
        """格式化日期显示"""
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        week_day = week_days[date_obj.weekday()]

        return f"{date_obj.year}年{date_obj.month}月{date_obj.day}日 {week_day}"

    def generate_notes_html(self, date: str, notes: List[Dict]) -> str:
        """
        生成笔记内容的HTML（包含任务状态和事件详细信息）

        Args:
            date: 日期
            notes: 笔记数据列表

        Returns:
            HTML内容
        """
        html_lines = []

        # 加载任务数据（如果有）
        try:
            tasks = self.task_manager.get_daily_tasks(date)
            task_dict = {t['id']: t for t in tasks}
        except:
            task_dict = {}

        for note in notes:
            # 判断是否为任务或事件
            if note['type'] in ['task', 'completed', 'migrated', 'cancelled', 'planned']:
                # 任务类型
                status = note.get('status', 'task')

                # 获取任务ID
                task_id = note.get('id', f"task_{note.get('raw', '').__hash__()}")

                # 如果有任务数据，使用任务的状态
                if task_id in task_dict:
                    status = task_dict[task_id]['status']
                    note['status'] = status

                # 状态配置
                status_configs = {
                    'task': {'name': '待办', 'css': 'task'},
                    'completed': {'name': '已完成', 'css': 'completed'},
                    'migrated': {'name': '已迁移', 'css': 'migrated'},
                    'cancelled': {'name': '已取消', 'css': 'cancelled'},
                    'planned': {'name': '已计划', 'css': 'planned'}
                }

                status_config = status_configs.get(status, status_configs['task'])

                # 符号
                symbols = {
                    'task': '●',
                    'completed': '×',
                    'migrated': '>',
                    'cancelled': '~~',
                    'planned': '<'
                }
                symbol = symbols.get(status, '●')

                # 时间显示
                time_html = ""
                if note.get('time'):
                    time_html = f'<span class="time">{note["time"]}</span>'

                # 操作按钮（仅待办任务显示）
                actions_html = ""
                if status == 'task':
                    actions_html = f"""
                        <div class="actions">
                            <button class="action-btn complete" data-action="complete" title="完成任务">✓</button>
                            <button class="action-btn migrate" data-action="migrate" title="迁移任务">→</button>
                            <button class="action-btn cancel" data-action="cancel" title="取消任务">✗</button>
                        </div>
                    """

                # 生成单条笔记HTML
                note_html = f"""
                    <div class="note-item" data-status="{status}" data-task-id="{task_id}">
                        <span class="symbol {status_config['css']} task-clickable">{symbol}</span>
                        <div class="note-text" style="{'text-decoration: line-through; color: #999;' if status == 'cancelled' else ''}">
                            {time_html}{note['content']}
                            <span class="status-badge {status_config['css']}">{status_config['name']}</span>
                        </div>
                        {actions_html}
                    </div>
                """
                html_lines.append(note_html)

            elif note['type'] == 'event':
                # 事件类型：包含日期、时间、地点等详细信息
                time_html = f'<span class="time">{note["time"]}</span>' if note.get('time') else ""

                # 地点信息
                location_html = ""
                if note.get('location'):
                    location_html = f'<span class="location">📍 {note["location"]}</span>'

                # 生成事件HTML
                note_html = f"""
                    <div class="note-item">
                        <span class="symbol event">○</span>
                        <div class="note-text">
                            {time_html}{note['content']}
                            {location_html}
                        </div>
                    </div>
                """
                html_lines.append(note_html)

            else:
                # 笔记类型
                note_html = f"""
                    <div class="note-item">
                        <span class="symbol note">{note['symbol']}</span>
                        <div class="note-text">{note['content']}</div>
                    </div>
                """
                html_lines.append(note_html)

        return '\n'.join(html_lines)

    def generate_interactive_card(
        self,
        date: str,
        weather: str,
        temperature: str,
        notes: List[Dict],
        output_path: str = None
    ) -> str:
        """
        生成交互式HTML卡片

        Args:
            date: 日期（YYYY-MM-DD）
            weather: 天气
            temperature: 温度
            notes: 笔记数据列表
            output_path: 输出文件路径（可选）

        Returns:
            HTML内容
        """
        # 读取模板
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # 准备替换数据
        date_display = self.format_date_display(date)
        weather_icon = self.get_weather_icon(weather)
        notes_html = self.generate_notes_html(date, notes)

        # 获取任务统计
        try:
            stats = self.task_manager.get_task_statistics(date)
        except:
            # 如果没有任务数据，使用默认统计
            task_count = sum(1 for n in notes if n['type'] in ['task', 'completed', 'migrated', 'cancelled', 'planned'])
            completed_count = sum(1 for n in notes if n['type'] == 'completed')
            stats = {
                'total': task_count,
                'completed': completed_count,
                'pending': task_count - completed_count,
                'completion_rate': (completed_count / task_count * 100) if task_count > 0 else 0
            }

        # 替换模板变量
        html_content = template.replace('{{date_display}}', date_display)
        html_content = html_content.replace('{{date}}', date)
        html_content = html_content.replace('{{weather_icon}}', weather_icon)
        html_content = html_content.replace('{{weather}}', weather)
        html_content = html_content.replace('{{temperature}}', temperature)
        html_content = html_content.replace('{{notes_html}}', notes_html)

        # 替换统计数据
        html_content = html_content.replace('{{stats_total}}', str(stats['total']))
        html_content = html_content.replace('{{stats_completed}}', str(stats['completed']))
        html_content = html_content.replace('{{stats_pending}}', str(stats['pending']))
        html_content = html_content.replace('{{stats_rate}}', f"{stats['completion_rate']:.1f}")

        # 保存文件
        if output_path:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"交互式HTML卡片已保存至：{output_path}")

        return html_content


def main():
    """测试用例"""
    from process_notes import NoteProcessor

    # 创建处理器
    processor = NoteProcessor()

    # 示例输入（包含任务和事件）
    example_input = """09:00 今天要把有机逆合成的逻辑和思路整理出来最好自动化。
09:15 团队会议（地点：会议室A）
09:30 购买卫生纸
明天家家悦有打折的鸡蛋
最近的股票市场波动比较大，要尝试新的分析方法了"""

    # 处理输入
    notes = processor.parse_input(example_input)

    # 标记任务类型
    for note in notes:
        if note['type'] == 'task':
            note['status'] = 'task'
            note['id'] = f"task_{hash(note['content'])}"

        # 为事件添加地点信息（模拟）
        if '会议' in note['content']:
            note['type'] = 'event'
            note['location'] = '会议室A'

    # 生成交互式卡片
    generator = InteractiveCardGenerator()
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'cards',
        '2025-03-16-interactive.html'
    )

    html_content = generator.generate_interactive_card(
        date='2025-03-16',
        weather='晴',
        temperature='15°C',
        notes=notes,
        output_path=output_path
    )

    print(f"交互式HTML卡片生成成功！")
    print(f"文件路径：{output_path}")


if __name__ == '__main__':
    main()
