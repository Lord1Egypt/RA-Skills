#!/usr/bin/env python3
"""
生成独立运行的交互式卡片
将所有必要的数据嵌入HTML中，无需服务器即可运行
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from process_notes import NoteProcessor
from task_manager import TaskManager
from generate_card import CardGenerator
from generate_pdf import PDFGenerator


class StandaloneInteractiveCardGenerator:
    """独立运行的交互式卡片生成器"""

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.task_manager = TaskManager(base_dir)
        self.card_generator = CardGenerator(base_dir)
        self.pdf_generator = PDFGenerator(base_dir)

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

    def generate_notes_html(self, date: str, notes: list) -> str:
        """生成笔记内容的HTML"""
        html_lines = []

        for note in notes:
            if note['type'] in ['task', 'completed', 'migrated', 'cancelled', 'planned']:
                status = note.get('status', 'task')
                task_id = note.get('id', f"task_{hash(note['content'])}")

                status_configs = {
                    'task': {'name': '待办', 'css': 'task', 'symbol': '●'},
                    'completed': {'name': '已完成', 'css': 'completed', 'symbol': '×'},
                    'migrated': {'name': '已迁移', 'css': 'migrated', 'symbol': '>'},
                    'cancelled': {'name': '已取消', 'css': 'cancelled', 'symbol': '~~'},
                    'planned': {'name': '已计划', 'css': 'planned', 'symbol': '<'}
                }

                status_config = status_configs.get(status, status_configs['task'])

                time_html = f'<span class="time">{note.get("time", "")}</span>' if note.get('time') else ""

                note_html = f"""
                    <div class="note-item" data-status="{status}" data-task-id="{task_id}">
                        <span class="symbol {status_config['css']} task-clickable" onclick="toggleTaskStatus('{task_id}')">{status_config['symbol']}</span>
                        <div class="note-text" style="{'text-decoration: line-through; color: #999;' if status == 'cancelled' else ''}">
                            {time_html}{note['content']}
                            <span class="status-badge {status_config['css']}">{status_config['name']}</span>
                        </div>
                        {self.generate_action_buttons(status, task_id)}
                    </div>
                """
                html_lines.append(note_html)
            elif note['type'] == 'event':
                time_html = f'<span class="time">{note.get("time", "")}</span>' if note.get('time') else ""
                location_html = f'<span class="location">📍 {note.get("location", "")}</span>' if note.get('location') else ""

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
                note_html = f"""
                    <div class="note-item">
                        <span class="symbol note">{note.get('symbol', '–')}</span>
                        <div class="note-text">{note['content']}</div>
                    </div>
                """
                html_lines.append(note_html)

        return '\n'.join(html_lines)

    def generate_action_buttons(self, status: str, task_id: str) -> str:
        """生成操作按钮"""
        if status == 'task':
            return f"""
                <div class="actions">
                    <button class="action-btn complete" onclick="completeTask('{task_id}')" title="完成任务">✓ 完成</button>
                    <button class="action-btn migrate" onclick="migrateTask('{task_id}')" title="迁移任务">→ 迁移</button>
                    <button class="action-btn cancel" onclick="cancelTask('{task_id}')" title="取消任务">✗ 取消</button>
                    <button class="action-btn plan" onclick="planTask('{task_id}')" title="计划任务">< 计划</button>
                </div>
            """
        elif status == 'completed':
            return f"""
                <div class="actions">
                    <button class="action-btn restart" onclick="restartTask('{task_id}')" title="重做任务">↺ 重做</button>
                    <button class="action-btn migrate" onclick="migrateTask('{task_id}')" title="迁移任务">→ 迁移</button>
                </div>
            """
        elif status == 'migrated':
            return f"""
                <div class="actions">
                    <button class="action-btn restart" onclick="restartTask('{task_id}')" title="重启任务">↺ 重启</button>
                    <button class="action-btn cancel" onclick="cancelTask('{task_id}')" title="取消任务">✗ 取消</button>
                </div>
            """
        elif status == 'cancelled':
            return f"""
                <div class="actions">
                    <button class="action-btn restart" onclick="restartTask('{task_id}')" title="恢复任务">↺ 恢复</button>
                </div>
            """
        elif status == 'planned':
            return f"""
                <div class="actions">
                    <button class="action-btn restart" onclick="restartTask('{task_id}')" title="开始执行">↺ 开始</button>
                    <button class="action-btn cancel" onclick="cancelTask('{task_id}')" title="取消计划">✗ 取消</button>
                </div>
            """
        return ""

    def generate_standalone_card(self, date: str, weather: str, temperature: str, notes: list, output_path: str = None) -> str:
        """生成独立运行的交互式卡片"""
        date_display = self.format_date_display(date)
        weather_icon = self.get_weather_icon(weather)
        notes_html = self.generate_notes_html(date, notes)

        # 计算统计
        task_count = sum(1 for n in notes if n['type'] in ['task', 'completed', 'migrated', 'cancelled', 'planned'])
        completed_count = sum(1 for n in notes if n['type'] == 'completed')
        pending_count = task_count - completed_count
        completion_rate = (completed_count / task_count * 100) if task_count > 0 else 0

        # 生成完整HTML
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{date} - 子弹笔记（独立交互版）</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .card {{
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 700px;
            padding: 40px;
            position: relative;
            overflow: hidden;
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }}

        .date {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
            letter-spacing: 1px;
        }}

        .weather {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 20px;
            color: #666;
        }}

        .weather-icon {{
            font-size: 32px;
        }}

        .content {{
            font-size: 18px;
            line-height: 2.2;
            color: #555;
        }}

        .note-item {{
            padding: 12px 0;
            border-bottom: 1px dashed #eee;
            display: flex;
            align-items: flex-start;
            gap: 12px;
            transition: all 0.3s ease;
        }}

        .note-item:hover {{
            background-color: #f9f9f9;
            padding-left: 8px;
        }}

        .note-item:last-child {{
            border-bottom: none;
        }}

        .symbol {{
            font-size: 24px;
            width: 40px;
            text-align: center;
            flex-shrink: 0;
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }}

        .symbol:hover {{
            transform: scale(1.2);
        }}

        .symbol.task {{
            color: #3498db;
        }}

        .symbol.completed {{
            color: #27ae60;
        }}

        .symbol.migrated {{
            color: #9b59b6;
        }}

        .symbol.cancelled {{
            color: #95a5a6;
            text-decoration: line-through;
        }}

        .symbol.planned {{
            color: #e67e22;
        }}

        .symbol.event {{
            color: #2ecc71;
        }}

        .symbol.note {{
            color: #f39c12;
        }}

        .note-text {{
            flex: 1;
        }}

        .time {{
            color: #999;
            font-size: 14px;
            margin-right: 8px;
        }}

        .location {{
            color: #e67e22;
            font-size: 14px;
            margin-left: 10px;
        }}

        .status-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            margin-left: 10px;
            font-weight: bold;
        }}

        .status-badge.task {{
            background-color: #e8f4f8;
            color: #3498db;
        }}

        .status-badge.completed {{
            background-color: #e8f8f0;
            color: #27ae60;
        }}

        .status-badge.migrated {{
            background-color: #f4e8f8;
            color: #9b59b6;
        }}

        .status-badge.cancelled {{
            background-color: #f0f0f0;
            color: #95a5a6;
        }}

        .status-badge.planned {{
            background-color: #f8f0e8;
            color: #e67e22;
        }}

        .actions {{
            display: flex;
            gap: 5px;
            opacity: 0;
            transition: opacity 0.2s ease;
        }}

        .note-item:hover .actions {{
            opacity: 1;
        }}

        .action-btn {{
            padding: 4px 8px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s ease;
        }}

        .action-btn:hover {{
            background: #f0f0f0;
        }}

        .action-btn.complete {{
            color: #27ae60;
            border-color: #27ae60;
        }}

        .action-btn.migrate {{
            color: #9b59b6;
            border-color: #9b59b6;
        }}

        .action-btn.cancel {{
            color: #95a5a6;
            border-color: #95a5a6;
        }}

        .action-btn.plan {{
            color: #e67e22;
            border-color: #e67e22;
        }}

        .action-btn.restart {{
            color: #3498db;
            border-color: #3498db;
        }}

        .statistics {{
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 5px;
            font-size: 14px;
        }}

        .statistics-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}

        .statistics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 10px;
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 12px;
            color: #666;
        }}

        .notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #333;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }}

        @keyframes slideIn {{
            from {{
                transform: translateX(100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        @media (max-width: 600px) {{
            .card {{
                padding: 20px;
            }}

            .date {{
                font-size: 22px;
            }}

            .content {{
                font-size: 16px;
            }}

            .actions {{
                opacity: 1;
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="date">
                {date_display}
            </div>
            <div class="weather">
                <span class="weather-icon">{weather_icon}</span>
                <span>{weather}</span>
                <span>{temperature}</span>
            </div>
        </div>

        <div class="content">
            {notes_html}
        </div>

        <div class="statistics">
            <div class="statistics-title">📊 今日任务统计</div>
            <div class="statistics-grid">
                <div class="stat-item">
                    <div class="stat-value" id="stat-total">{task_count}</div>
                    <div class="stat-label">总任务</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="stat-completed">{completed_count}</div>
                    <div class="stat-label">已完成</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="stat-pending">{pending_count}</div>
                    <div class="stat-label">待办</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="stat-rate">{completion_rate:.1f}%</div>
                    <div class="stat-label">完成率</div>
                </div>
            </div>
        </div>

        <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #f0f0f0; font-size: 14px; color: #999; text-align: center;">
            💡 提示：点击符号可切换任务状态 | 悬停查看操作按钮
        </div>
    </div>

    <script>
        // 任务状态定义
        const taskStatuses = {{
            'task': {{ symbol: '●', name: '待办', css: 'task' }},
            'completed': {{ symbol: '×', name: '已完成', css: 'completed' }},
            'migrated': {{ symbol: '>', name: '已迁移', css: 'migrated' }},
            'cancelled': {{ symbol: '~~', name: '已取消', css: 'cancelled' }},
            'planned': {{ symbol: '<', name: '已计划', css: 'planned' }}
        }};

        // 状态循环顺序（点击符号时的切换顺序）
        const statusCycle = ['task', 'completed', 'task'];

        // 状态映射（任意状态之间的转换）
        const statusTransitions = {{
            'task': ['completed', 'migrated', 'cancelled', 'planned'],
            'completed': ['task', 'migrated', 'cancelled'],
            'migrated': ['task', 'completed', 'cancelled'],
            'cancelled': ['task'],
            'planned': ['task', 'completed']
        }};

        // 切换任务状态（点击符号，循环切换）
        function toggleTaskStatus(taskId) {{
            const noteItem = document.querySelector(`[data-task-id="${{taskId}}"]`);
            if (!noteItem) return;

            const currentStatus = noteItem.dataset.status;

            // 查找当前状态在循环中的位置
            const currentIndex = statusCycle.indexOf(currentStatus);
            if (currentIndex === -1) return;

            // 切换到下一个状态
            const nextIndex = (currentIndex + 1) % statusCycle.length;
            const nextStatus = statusCycle[nextIndex];

            updateTaskStatus(taskId, nextStatus);
        }}

        // 完成任务
        function completeTask(taskId) {{
            updateTaskStatus(taskId, 'completed');
        }}

        // 撤销完成
        function undoCompleteTask(taskId) {{
            updateTaskStatus(taskId, 'task');
        }}

        // 迁移任务
        function migrateTask(taskId) {{
            updateTaskStatus(taskId, 'migrated');
        }}

        // 取消任务
        function cancelTask(taskId) {{
            updateTaskStatus(taskId, 'cancelled');
        }}

        // 重启任务（取消/迁移/计划 → 待办）
        function restartTask(taskId) {{
            updateTaskStatus(taskId, 'task');
        }}

        // 计划任务
        function planTask(taskId) {{
            updateTaskStatus(taskId, 'planned');
        }}

        // 更新任务状态（核心函数）
        function updateTaskStatus(taskId, newStatus) {{
            const noteItem = document.querySelector(`[data-task-id="${{taskId}}"]`);
            if (!noteItem) return;

            const oldStatus = noteItem.dataset.status;
            const statusConfig = taskStatuses[newStatus];

            // 更新符号
            const symbol = noteItem.querySelector('.symbol');
            symbol.textContent = statusConfig.symbol;
            symbol.className = `symbol ${{statusConfig.css}} task-clickable`;

            // 更新data属性
            noteItem.dataset.status = newStatus;

            // 更新状态标签
            const badge = noteItem.querySelector('.status-badge');
            if (badge) {{
                badge.textContent = statusConfig.name;
                badge.className = `status-badge ${{newStatus}}`;
            }}

            // 更新文本样式
            const text = noteItem.querySelector('.note-text');
            if (newStatus === 'cancelled') {{
                text.style.textDecoration = 'line-through';
                text.style.color = '#999';
            }} else {{
                text.style.textDecoration = 'none';
                text.style.color = '#555';
            }}

            // 更新操作按钮
            const actionsDiv = noteItem.querySelector('.actions');
            if (actionsDiv) {{
                if (newStatus === 'task') {{
                    actionsDiv.innerHTML = `
                        <button class="action-btn complete" onclick="completeTask('${{taskId}}')" title="完成任务">✓ 完成</button>
                        <button class="action-btn migrate" onclick="migrateTask('${{taskId}}')" title="迁移任务">→ 迁移</button>
                        <button class="action-btn cancel" onclick="cancelTask('${{taskId}}')" title="取消任务">✗ 取消</button>
                        <button class="action-btn plan" onclick="planTask('${{taskId}}')" title="计划任务">< 计划</button>
                    `;
                }} else if (newStatus === 'completed') {{
                    actionsDiv.innerHTML = `
                        <button class="action-btn restart" onclick="restartTask('${{taskId}}')" title="重做任务">↺ 重做</button>
                        <button class="action-btn migrate" onclick="migrateTask('${{taskId}}')" title="迁移任务">→ 迁移</button>
                    `;
                }} else if (newStatus === 'migrated') {{
                    actionsDiv.innerHTML = `
                        <button class="action-btn restart" onclick="restartTask('${{taskId}}')" title="重启任务">↺ 重启</button>
                        <button class="action-btn cancel" onclick="cancelTask('${{taskId}}')" title="取消任务">✗ 取消</button>
                    `;
                }} else if (newStatus === 'cancelled') {{
                    actionsDiv.innerHTML = `
                        <button class="action-btn restart" onclick="restartTask('${{taskId}}')" title="恢复任务">↺ 恢复</button>
                    `;
                }} else if (newStatus === 'planned') {{
                    actionsDiv.innerHTML = `
                        <button class="action-btn restart" onclick="restartTask('${{taskId}}')" title="开始执行">↺ 开始</button>
                        <button class="action-btn cancel" onclick="cancelTask('${{taskId}}')" title="取消计划">✗ 取消</button>
                    `;
                }}
            }}

            // 更新统计
            updateStatistics();

            // 显示通知
            showNotification(`任务状态更新：${{taskStatuses[oldStatus].name}} → ${{statusConfig.name}}`);
        }}

        // 更新统计
        function updateStatistics() {{
            const allTasks = document.querySelectorAll('[data-status]');
            const total = allTasks.length;
            const completed = document.querySelectorAll('[data-status="completed"]').length;
            const pending = total - completed;
            const rate = total > 0 ? (completed / total * 100).toFixed(1) : 0;

            document.getElementById('stat-total').textContent = total;
            document.getElementById('stat-completed').textContent = completed;
            document.getElementById('stat-pending').textContent = pending;
            document.getElementById('stat-rate').textContent = rate + '%';
        }}

        // 显示通知
        function showNotification(message) {{
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.textContent = message;
            document.body.appendChild(notification);

            setTimeout(() => {{
                notification.style.animation = 'slideIn 0.3s ease reverse';
                setTimeout(() => {{
                    document.body.removeChild(notification);
                }}, 300);
            }}, 2000);
        }}

        // 页面加载完成
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('交互式卡片已加载');
        }});
    </script>
</body>
</html>
'''

        # 保存文件
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"独立交互式卡片已保存：{output_path}")

        return html_content


def main():
    """主函数"""
    from pathlib import Path

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    today = datetime.now().strftime('%Y-%m-%d')

    # 创建测试数据
    notes = [
        {'raw': '09:00 整理有机逆合成逻辑', 'content': '整理有机逆合成逻辑', 'time': '09:00', 'type': 'task', 'symbol': '●', 'status': 'task', 'id': 'task_001'},
        {'raw': '09:15 团队会议', 'content': '团队会议', 'time': '09:15', 'type': 'task', 'symbol': '●', 'status': 'task', 'id': 'task_002'},
        {'raw': '09:30 购买卫生纸', 'content': '购买卫生纸', 'time': '09:30', 'type': 'task', 'symbol': '●', 'status': 'task', 'id': 'task_003'},
        {'raw': '10:00 完成立项书摘要', 'content': '完成立项书摘要', 'time': '10:00', 'type': 'completed', 'symbol': '×', 'status': 'completed', 'id': 'task_004'},
        {'raw': '明天家家悦有打折的鸡蛋', 'content': '明天家家悦有打折的鸡蛋', 'type': 'note', 'symbol': '–'},
        {'raw': '最近的股票市场波动比较大', 'content': '最近的股票市场波动比较大', 'type': 'note', 'symbol': '–'}
    ]

    # 生成交互式卡片
    generator = StandaloneInteractiveCardGenerator(base_dir)
    output_path = os.path.join(base_dir, 'cards', f'{today}-standalone.html')

    generator.generate_standalone_card(
        date=today,
        weather='晴',
        temperature='15°C',
        notes=notes,
        output_path=output_path
    )

    print(f"\n✅ 独立交互式卡片生成成功！")
    print(f"📂 文件路径：{output_path}")
    print(f"\n🚀 使用方法：")
    print(f"1. 在浏览器中打开：open {output_path}")
    print(f"2. 点击任务符号（●）切换状态")
    print(f"3. 悬停显示操作按钮")
    print(f"\n💡 特点：")
    print(f"✅ 无需服务器，直接运行")
    print(f"✅ 完全独立，无外部依赖")
    print(f"✅ 点击即响应，状态立即更新")


if __name__ == '__main__':
    main()
