#!/usr/bin/env python3
"""
生成PDF打印版本
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class PDFGenerator:
    """PDF生成器"""

    def __init__(self, template_path: str = None):
        if template_path is None:
            template_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'templates',
                'print_template.html'
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

    def generate_printable_html(
        self,
        date: str,
        weather: str,
        temperature: str,
        notes: List[Dict]
    ) -> str:
        """
        生成可打印的HTML

        Args:
            date: 日期（YYYY-MM-DD）
            weather: 天气
            temperature: 温度
            notes: 笔记数据列表

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
        print_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 替换模板变量
        html_content = template.replace('{{date_display}}', date_display)
        html_content = html_content.replace('{{date}}', date)
        html_content = html_content.replace('{{weather_icon}}', weather_icon)
        html_content = html_content.replace('{{weather}}', weather)
        html_content = html_content.replace('{{temperature}}', temperature)
        html_content = html_content.replace('{{notes_html}}', notes_html)
        html_content = html_content.replace('{{print_date}}', print_date)

        return html_content

    def generate_pdf(
        self,
        date: str,
        weather: str,
        temperature: str,
        notes: List[Dict],
        output_path: str,
        use_wkhtmltopdf: bool = False
    ) -> str:
        """
        生成PDF文件

        Args:
            date: 日期
            weather: 天气
            temperature: 温度
            notes: 笔记数据
            output_path: PDF输出路径
            use_wkhtmltopdf: 是否使用wkhtmltopdf（需要安装）

        Returns:
            PDF文件路径
        """
        # 生成HTML
        html_content = self.generate_printable_html(
            date=date,
            weather=weather,
            temperature=temperature,
            notes=notes
        )

        # 创建输出目录
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        if use_wkhtmltopdf:
            # 使用wkhtmltopdf生成PDF
            html_path = output_path.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            try:
                subprocess.run([
                    'wkhtmltopdf',
                    '--page-size', 'A4',
                    '--margin-top', '0',
                    '--margin-bottom', '0',
                    '--margin-left', '0',
                    '--margin-right', '0',
                    html_path,
                    output_path
                ], check=True)

                # 删除临时HTML文件
                os.remove(html_path)

                print(f"PDF已生成（使用wkhtmltopdf）：{output_path}")

            except subprocess.CalledProcessError as e:
                print(f"wkhtmltopdf执行失败：{e}")
                print("已生成HTML文件，请使用浏览器打印功能保存为PDF")
                print(f"HTML文件：{html_path}")
                output_path = html_path
        else:
            # 直接保存HTML，提示用户使用浏览器打印
            html_path = output_path.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"已生成打印版HTML：{html_path}")
            print(f"提示：请在浏览器中打开该文件，使用打印功能保存为PDF")
            output_path = html_path

        return output_path


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

    # 生成PDF
    generator = PDFGenerator()
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'printable',
        '2025-03-16.pdf'
    )

    result_path = generator.generate_pdf(
        date='2025-03-16',
        weather='晴',
        temperature='15°C',
        notes=notes,
        output_path=output_path,
        use_wkhtmltopdf=False  # 使用HTML方式
    )

    print(f"\n结果文件：{result_path}")


if __name__ == '__main__':
    main()
