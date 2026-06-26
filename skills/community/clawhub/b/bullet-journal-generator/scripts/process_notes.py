#!/usr/bin/env python3
"""
语言润色与内容分类脚本
将零散的自然语言输入转换为规范的子弹笔记格式
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Tuple

class NoteProcessor:
    """笔记处理器：润色语言、分类内容"""

    # 符号系统
    SYMBOLS = {
        'task': '●',      # 任务
        'event': '○',     # 事件
        'note': '–',      # 笔记
        'migration': '>', # 迁移
        'scheduled': '<', # 计划
        'priority': '☆'   # 优先
    }

    # 工作学习关键词
    WORK_STUDY_KEYWORDS = [
        '项目', '报告', '分析', '研究', '学习', '会议',
        '文档', '代码', '开发', '设计', '策划', '立项',
        '数据', '实验', '逆合成', '股票', '市场', '技术',
        '方法', '方案', '总结', '优化', '整理'
    ]

    # 口语化转换规则
    SLANG_PATTERNS = [
        (r'要把\b', '整理'),
        (r'要把(.+?)整理', r'整理\1'),
        (r'突然', ''),
        (r'最好', '目标：'),
        (r'想一想', '思考'),
        (r'看一下', '查看'),
        (r'试一下', '尝试'),
        (r'做一下', '处理'),
        (r'写一下', '编写'),
        (r'找一下', '查找'),
        (r'弄一下', '处理'),
        (r'搞定', '完成'),
        (r'搞定(.+?)', r'完成\1'),
    ]

    def __init__(self):
        self.processed_notes = []

    def polish_language(self, text: str) -> str:
        """润色语言，去除口语化表达"""
        polished = text.strip()

        # 应用转换规则
        for pattern, replacement in self.SLANG_PATTERNS:
            polished = re.sub(pattern, replacement, polished)

        # 去除多余空格
        polished = re.sub(r'\s+', ' ', polished)

        # 移除句尾语气词
        polished = re.sub(r'[了啊呢吧嘛]$', '', polished)

        return polished.strip()

    def classify_note(self, text: str, has_time: bool = False) -> Tuple[str, str, bool]:
        """
        分类笔记内容

        Returns:
            (symbol, type, is_work_study)
        """
        text_lower = text.lower()

        # 优先级判断
        if '紧急' in text or '重要' in text or '优先' in text:
            return self.SYMBOLS['priority'], 'priority', False

        # 未来计划
        if text.startswith('明天') or text.startswith('下周') or text.startswith('下月'):
            return self.SYMBOLS['scheduled'], 'scheduled', False

        # 事件判断（有时间标记或活动类动词）
        if has_time or any(keyword in text for keyword in ['会议', '约', '打羽毛球', '健身', '购物']):
            return self.SYMBOLS['event'], 'event', False

        # 任务判断（动作动词开头）
        task_verbs = ['整理', '完成', '购买', '写', '处理', '预约', '准备', '开发', '设计']
        if any(text.startswith(verb) for verb in task_verbs):
            return self.SYMBOLS['task'], 'task', False

        # 笔记判断（观察、思考类）
        note_keywords = ['观察', '思考', '想法', '发现', '波动', '方法', '逻辑', '思路']
        if any(keyword in text for keyword in note_keywords):
            return self.SYMBOLS['note'], 'note', False

        # 默认为任务
        return self.SYMBOLS['task'], 'task', False

    def is_work_study(self, text: str) -> bool:
        """判断是否为工作学习相关内容"""
        return any(keyword in text for keyword in self.WORK_STUDY_KEYWORDS)

    def extract_time(self, text: str) -> Tuple[str, bool]:
        """
        提取时间信息

        Returns:
            (time_str, has_time)
        """
        # 匹配时间格式：HH:MM 或 HH时MM分
        time_patterns = [
            r'(\d{1,2}):(\d{2})',
            r'(\d{1,2})时(\d{2})分',
        ]

        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2))
                time_str = f"{hour:02d}:{minute:02d}"
                # 从原文本中移除时间
                text_without_time = re.sub(pattern, '', text).strip()
                return time_str, True, text_without_time

        return '', False, text

    def parse_input(self, raw_input: str) -> List[Dict]:
        """
        解析用户输入

        Args:
            raw_input: 零散的自然语言输入

        Returns:
            处理后的笔记列表
        """
        # 按行分割
        lines = raw_input.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 提取时间
            time_str, has_time, content = self.extract_time(line)

            # 润色语言
            polished_content = self.polish_language(content)

            # 分类
            symbol, note_type, _ = self.classify_note(polished_content, has_time)

            # 判断是否工作学习相关
            is_work_study = self.is_work_study(polished_content)

            # 组装结果
            note = {
                'symbol': symbol,
                'type': note_type,
                'content': polished_content,
                'time': time_str,
                'has_time': has_time,
                'is_work_study': is_work_study,
                'raw': line
            }

            self.processed_notes.append(note)

        return self.processed_notes

    def format_bullet_line(self, note: Dict) -> str:
        """格式化单条子弹笔记"""
        parts = [note['symbol']]

        if note['time']:
            parts.append(f"{note['time']}")

        parts.append(note['content'])

        return ' '.join(parts)

    def get_formatted_notes(self) -> str:
        """获取格式化后的子弹笔记"""
        lines = []

        for note in self.processed_notes:
            line = self.format_bullet_line(note)
            lines.append(line)

        return '\n'.join(lines)

    def get_work_study_notes(self) -> List[Dict]:
        """获取工作学习相关笔记"""
        return [note for note in self.processed_notes if note['is_work_study']]

    def export_json(self) -> str:
        """导出为JSON格式"""
        return json.dumps(self.processed_notes, ensure_ascii=False, indent=2)


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

    # 输出结果
    print("=" * 60)
    print("处理后的子弹笔记:")
    print("=" * 60)
    print(processor.get_formatted_notes())
    print()

    print("=" * 60)
    print("工作学习相关内容:")
    print("=" * 60)
    for note in processor.get_work_study_notes():
        print(f"{note['symbol']} {note['content']}")
    print()

    print("=" * 60)
    print("结构化数据 (JSON):")
    print("=" * 60)
    print(processor.export_json())


if __name__ == '__main__':
    main()
