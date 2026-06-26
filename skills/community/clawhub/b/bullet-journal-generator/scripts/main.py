#!/usr/bin/env python3
"""
子弹笔记生成器主程序
整合所有功能的主入口
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.process_notes import NoteProcessor
from scripts.generate_bullet_journal import generate_bullet_journal
from scripts.generate_obsidian_log import ObsidianLogGenerator
from scripts.generate_card import CardGenerator
from scripts.generate_interactive_card import InteractiveCardGenerator
from scripts.generate_pdf import PDFGenerator
from scripts.get_weather import WeatherFetcher
from scripts.save_notes import NoteSaver
from scripts.task_manager import TaskManager


class BulletJournalGenerator:
    """子弹笔记生成器主类"""

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))

        self.base_dir = base_dir

        # 初始化各组件
        self.note_processor = NoteProcessor()
        self.obsidian_generator = ObsidianLogGenerator()
        self.card_generator = CardGenerator()
        self.interactive_card_generator = InteractiveCardGenerator()
        self.pdf_generator = PDFGenerator()
        self.weather_fetcher = WeatherFetcher()
        self.note_saver = NoteSaver(base_dir)
        self.task_manager = TaskManager(base_dir)

    def process_input(self, raw_input: str, date: str = None) -> dict:
        """
        处理用户输入

        Args:
            raw_input: 零散的自然语言输入
            date: 日期（YYYY-MM-DD），默认为今天

        Returns:
            处理结果字典
        """
        # 如果未指定日期，使用今天
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        print(f"\n{'=' * 60}")
        print(f"开始处理子弹笔记：{date}")
        print(f"{'=' * 60}\n")

        # Phase 1: 解析和润色输入
        print("Phase 1: 解析和润色输入...")
        notes = self.note_processor.parse_input(raw_input)
        print(f"  已处理 {len(notes)} 条笔记\n")

        # Phase 2: 获取天气信息
        print("Phase 2: 获取天气信息...")
        weather_data = self.weather_fetcher.get_weather(date)
        print(f"  天气：{weather_data['weather']} {weather_data['icon']}")
        print(f"  温度：{weather_data['temperature_with_unit']}\n")

        # Phase 3: 生成子弹笔记文本
        print("Phase 3: 生成子弹笔记文本...")
        bullet_journal = generate_bullet_journal(
            date=date,
            weather=weather_data['weather'],
            temperature=weather_data['temperature_with_unit'],
            notes_data=notes
        )
        print("  ✓ 子弹笔记文本生成完成\n")

        # Phase 4: 生成Obsidian日志（仅工作学习内容）
        print("Phase 4: 生成Obsidian日志...")
        work_study_notes = self.note_processor.get_work_study_notes()
        obsidian_log = self.obsidian_generator.generate_obsidian_log(
            date=date,
            notes=work_study_notes
        )
        print(f"  ✓ Obsidian日志生成完成（{len(work_study_notes)} 条工作学习内容）\n")

        # Phase 5: 生成HTML卡片
        print("Phase 5: 生成HTML卡片...")
        html_card_path = os.path.join(
            self.base_dir,
            'cards',
            f"{date}.html"
        )
        html_content = self.card_generator.generate_card(
            date=date,
            weather=weather_data['weather'],
            temperature=weather_data['temperature_with_unit'],
            notes=notes,
            output_path=html_card_path
        )
        print("  ✓ HTML卡片生成完成\n")

        # Phase 5.5: 生成交互式HTML卡片
        print("Phase 5.5: 生成交互式HTML卡片...")
        interactive_card_path = os.path.join(
            self.base_dir,
            'cards',
            f"{date}-interactive.html"
        )

        # 为任务添加ID和状态
        task_counter = 0
        for note in notes:
            if note['type'] in ['task', 'completed', 'migrated', 'cancelled', 'planned']:
                task_counter += 1
                note['id'] = f"task_{task_counter:03d}"
                note['status'] = note['type']

        interactive_html_content = self.interactive_card_generator.generate_interactive_card(
            date=date,
            weather=weather_data['weather'],
            temperature=weather_data['temperature_with_unit'],
            notes=notes,
            output_path=interactive_card_path
        )
        print("  ✓ 交互式HTML卡片生成完成\n")

        # Phase 6: 生成打印版本
        print("Phase 6: 生成打印版本...")
        printable_path = os.path.join(
            self.base_dir,
            'printable',
            f"{date}.pdf"
        )
        printable_file = self.pdf_generator.generate_pdf(
            date=date,
            weather=weather_data['weather'],
            temperature=weather_data['temperature_with_unit'],
            notes=notes,
            output_path=printable_path,
            use_wkhtmltopdf=False  # 使用HTML方式
        )
        print("  ✓ 打印版本生成完成\n")

        # Phase 7: 保存所有文件
        print("Phase 7: 保存所有文件...")
        saved_paths = self.note_saver.save_all(
            date=date,
            bullet_journal=bullet_journal,
            obsidian_log=obsidian_log,
            html_card=html_content,
            printable_file=printable_file,
            notes_data=notes,
            weather_data=weather_data
        )
        print("  ✓ 所有文件保存完成\n")

        # 组装返回结果
        result = {
            'date': date,
            'notes': notes,
            'weather': weather_data,
            'bullet_journal': bullet_journal,
            'obsidian_log': obsidian_log,
            'html_card': html_card_path,
            'interactive_html_card': interactive_card_path,
            'printable': printable_file,
            'saved_paths': saved_paths
        }

        # 打印摘要
        print(f"{'=' * 60}")
        print(f"处理完成！")
        print(f"{'=' * 60}\n")

        print("📝 子弹笔记预览：")
        print("-" * 60)
        print(bullet_journal[:200] + "..." if len(bullet_journal) > 200 else bullet_journal)
        print("-" * 60)

        print("\n📂 文件路径：")
        for file_type, path in saved_paths.items():
            print(f"  {file_type:15s}: {path}")

        print(f"\n💡 提示：")
        print(f"  - HTML卡片：在浏览器中打开 {saved_paths.get('html_card')}")
        print(f"  - 交互式卡片：在浏览器中打开 {interactive_card_path}（支持任务状态切换）")
        print(f"  - 打印版本：在浏览器中打开 {saved_paths.get('printable')} 并使用打印功能")
        print(f"  - Obsidian日志：{saved_paths.get('obsidian_log')} 可导入到Obsidian")

        return result


def main():
    """主函数"""
    # 示例输入
    example_input = """09:00 今天要把有机逆合成的逻辑和思路整理出来最好自动化。去买卫生纸，预约羽毛球场地
09:17 老板突然紧急需要交给政府的立项书，我先把摘要写出来
明天家家悦有打折的鸡蛋
最近的股票市场波动比较大，要尝试新的分析方法了"""

    # 创建生成器
    generator = BulletJournalGenerator()

    # 处理输入
    result = generator.process_input(example_input, date='2025-03-16')

    # 返回结果
    return result


if __name__ == '__main__':
    main()
