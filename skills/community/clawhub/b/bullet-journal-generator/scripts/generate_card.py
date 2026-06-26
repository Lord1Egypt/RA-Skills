#!/usr/bin/env python3
"""
生成可视化HTML卡片
模拟手写风格的子弹笔记
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class CardGenerator:
    """HTML卡片生成器"""

    def __init__(self, template_path: str = None):
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'templates',
                'card_template.html'
            )
        self.template_path = template_path

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

    def generate_notes_html(self, notes: List[Dict]) -> str:
        """生成笔记内容的HTML"""
        html_lines = []

        for note in notes:
            # 符号类名
            symbol_class = note['type']

            # 时间显示
            time_html = ""
            if note.get('time'):
                time_html = f'<span class="time">{note["time"]}</span>'

            # 生成单条笔记HTML
            note_html = f"""
                <div class="note-item">
                    <span class="symbol {symbol_class}">{note['symbol']}</span>
                    <div class="note-text">
                        {time_html}{note['content']}
                    </div>
                </div>
            """
            html_lines.append(note_html)

        return '\n'.join(html_lines)

    def generate_card(
        self,
        date: str,
        weather: str,
        temperature: str,
        notes: List[Dict],
        output_path: str = None
    ) -> str:
        """
        生成HTML卡片

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
        notes_html = self.generate_notes_html(notes)

        # 替换模板变量
        html_content = template.replace('{{date_display}}', date_display)
        html_content = html_content.replace('{{date}}', date)
        html_content = html_content.replace('{{weather_icon}}', weather_icon)
        html_content = html_content.replace('{{weather}}', weather)
        html_content = html_content.replace('{{temperature}}', temperature)
        html_content = html_content.replace('{{notes_html}}', notes_html)

        # 保存文件
        if output_path:
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"HTML卡片已保存至：{output_path}")

        return html_content


def main():
    """测试用例"""
    from process_notes import NoteProcessor

    # 创建处理器
    processor = NoteProcessor()

    # 示例输入
    example_input = """09:00 今天要把有机逆合成的逻辑和思路整理出来最好自动化。去买卫生纸，预约羽毛球场地
09:17 老板突然紧急需要交给政府的立项书，我先把摘要写出来
明天家家悦有打折的鸡蛋
最近的股票市场波动比较大，要尝试新的分析方法了"""

    # 处理输入
    notes = processor.parse_input(example_input)

    # 生成HTML卡片
    generator = CardGenerator()
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'cards',
        '2025-03-16.html'
    )

    html_content = generator.generate_card(
        date='2025-03-16',
        weather='晴',
        temperature='15°C',
        notes=notes,
        output_path=output_path
    )

    print(f"HTML卡片生成成功！")
    print(f"文件路径：{output_path}")
    print(f"\n预览内容（前200字符）：")
    print(html_content[:200] + "...")


if __name__ == '__main__':
    main()
