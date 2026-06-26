#!/usr/bin/env python3
"""
文件保存与管理脚本
自动保存所有格式的笔记
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class NoteSaver:
    """笔记保存器"""

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))

        self.base_dir = base_dir

        # 创建目录结构
        self.data_dir = os.path.join(base_dir, 'data')
        self.cards_dir = os.path.join(base_dir, 'cards')
        self.printable_dir = os.path.join(base_dir, 'printable')
        self.backup_dir = os.path.join(base_dir, 'data', 'backup')

        # 确保目录存在
        self._ensure_directories()

    def _ensure_directories(self):
        """确保所有目录存在"""
        dirs = [
            self.data_dir,
            self.cards_dir,
            self.printable_dir,
            self.backup_dir
        ]

        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)

    def _get_date_dir(self, date: str) -> str:
        """获取日期目录路径"""
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        year = str(date_obj.year)
        month = f"{date_obj.month:02d}"
        day = f"{date_obj.day:02d}"

        return os.path.join(self.data_dir, year, month, day)

    def save_bullet_journal(
        self,
        date: str,
        bullet_journal: str
    ) -> str:
        """保存子弹笔记文本"""
        date_dir = self._get_date_dir(date)
        os.makedirs(date_dir, exist_ok=True)

        file_path = os.path.join(date_dir, 'bullet_journal.txt')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(bullet_journal)

        print(f"子弹笔记已保存：{file_path}")

        return file_path

    def save_obsidian_log(
        self,
        date: str,
        obsidian_log: str
    ) -> str:
        """保存Obsidian日志"""
        date_dir = self._get_date_dir(date)
        os.makedirs(date_dir, exist_ok=True)

        # 使用Daily Notes格式命名
        file_path = os.path.join(date_dir, f"{date}.md")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(obsidian_log)

        print(f"Obsidian日志已保存：{file_path}")

        return file_path

    def save_html_card(
        self,
        date: str,
        html_content: str
    ) -> str:
        """保存HTML卡片"""
        os.makedirs(self.cards_dir, exist_ok=True)

        file_path = os.path.join(self.cards_dir, f"{date}.html")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML卡片已保存：{file_path}")

        return file_path

    def save_printable_pdf(
        self,
        date: str,
        file_path: str
    ) -> str:
        """保存打印版本PDF或HTML"""
        # 复制文件到printable目录
        os.makedirs(self.printable_dir, exist_ok=True)

        # 获取文件扩展名
        ext = os.path.splitext(file_path)[1]
        target_path = os.path.join(self.printable_dir, f"{date}{ext}")

        # 如果源文件和目标文件相同，直接返回
        if os.path.abspath(file_path) == os.path.abspath(target_path):
            print(f"打印版本已存在：{target_path}")
            return target_path

        shutil.copy2(file_path, target_path)

        print(f"打印版本已保存：{target_path}")

        return target_path

    def save_json_data(
        self,
        date: str,
        notes_data: List[Dict],
        weather_data: Dict
    ) -> str:
        """保存JSON格式数据"""
        date_dir = self._get_date_dir(date)
        os.makedirs(date_dir, exist_ok=True)

        file_path = os.path.join(date_dir, 'data.json')

        data = {
            'date': date,
            'notes': notes_data,
            'weather': weather_data,
            'created_at': datetime.now().isoformat()
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"JSON数据已保存：{file_path}")

        return file_path

    def backup_note(self, date: str, source_files: Dict[str, str]):
        """备份笔记文件"""
        backup_date_dir = os.path.join(self.backup_dir, date)
        os.makedirs(backup_date_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        for file_type, file_path in source_files.items():
            if os.path.exists(file_path):
                ext = os.path.splitext(file_path)[1]
                backup_path = os.path.join(
                    backup_date_dir,
                    f"{file_type}_{timestamp}{ext}"
                )
                shutil.copy2(file_path, backup_path)
                print(f"已备份 {file_type}：{backup_path}")

    def save_all(
        self,
        date: str,
        bullet_journal: str,
        obsidian_log: str,
        html_card: str,
        printable_file: str,
        notes_data: List[Dict],
        weather_data: Dict
    ) -> Dict[str, str]:
        """
        保存所有格式的笔记

        Returns:
            各文件路径的字典
        """
        print(f"\n{'=' * 60}")
        print(f"开始保存笔记：{date}")
        print(f"{'=' * 60}\n")

        # 保存各类文件
        paths = {}

        paths['bullet_journal'] = self.save_bullet_journal(date, bullet_journal)
        paths['obsidian_log'] = self.save_obsidian_log(date, obsidian_log)
        paths['html_card'] = self.save_html_card(date, html_card)
        paths['printable'] = self.save_printable_pdf(date, printable_file)
        paths['json_data'] = self.save_json_data(date, notes_data, weather_data)

        # 备份
        self.backup_note(date, paths)

        print(f"\n{'=' * 60}")
        print(f"笔记保存完成！")
        print(f"{'=' * 60}\n")

        return paths


def main():
    """测试用例"""
    saver = NoteSaver()

    # 模拟数据
    date = '2025-03-16'
    bullet_journal = """2025-03-16 (周日) | ☀️ 晴 | 15°C

● 09:00 整理有机逆合成逻辑与思路
● 09:00 购买卫生纸
○ 09:17 紧急处理政府立项书摘要
< 明天 家家悦购买打折鸡蛋
– 最近股票市场波动较大，尝试新方法
☆ 有机逆合成自动化整理"""

    obsidian_log = """---
date: 2025-03-16
tags: ['work', 'study', 'analyze']
type: daily_log
---

# 2025-03-16 日志

## 优先任务

- [[有机逆合成/自动化]] 整理有机逆合成逻辑 ⭐

## 任务

- [[立项书/政府项目]] 09:17 处理立项书摘要

## 思考与观察

[[股票分析/市场波动]] 市场波动较大，研究新方法

## 下一步行动

- [ ] 完成有机逆合成自动化
- [ ] 购买打折鸡蛋
"""

    html_card = "<html>...</html>"

    printable_file = "/tmp/2025-03-16.pdf"

    notes_data = []
    weather_data = {'weather': '晴', 'temperature': '15°C'}

    # 保存所有文件
    paths = saver.save_all(
        date=date,
        bullet_journal=bullet_journal,
        obsidian_log=obsidian_log,
        html_card=html_card,
        printable_file=printable_file,
        notes_data=notes_data,
        weather_data=weather_data
    )

    print("\n所有文件路径：")
    for file_type, path in paths.items():
        print(f"  {file_type}: {path}")


if __name__ == '__main__':
    main()
