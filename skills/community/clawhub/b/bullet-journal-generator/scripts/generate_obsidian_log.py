#!/usr/bin/env python3
"""
生成Obsidian规范日志
支持标签、双链和规范化格式
"""

import re
from datetime import datetime
from typing import List, Dict

class ObsidianLogGenerator:
    """Obsidian日志生成器"""

    # 标签系统
    TAG_CATEGORIES = {
        'work': ['项目', '会议', '文档', '汇报', '立项', '分析'],
        'study': ['研究', '阅读', '技能', '课程', '学习', '方法'],
        'plan': ['计划', '目标', '待办', '安排'],
        'observe': ['观察', '数据', '市场', '波动'],
        'think': ['思考', '想法', '灵感', '思路', '逻辑']
    }

    def __init__(self):
        pass

    def extract_tags(self, text: str) -> List[str]:
        """从文本中提取标签"""
        tags = []

        # 根据关键词匹配标签
        for category, keywords in self.TAG_CATEGORIES.items():
            if any(keyword in text for keyword in keywords):
                tags.append(category)

        return tags

    def generate_wikilink(self, content: str) -> str:
        """
        生成双链

        规则：
        - 提取关键名词/项目名
        - 使用 [[名称/子标题]] 格式
        - 相同主题使用统一格式
        """
        # 项目/任务类
        if '有机逆合成' in content:
            return '[[有机逆合成/自动化]]'
        elif '立项书' in content:
            return '[[立项书/政府项目]]'
        elif '股票' in content or '市场' in content:
            return '[[股票分析/市场波动]]'
        elif '分析' in content:
            return '[[分析/研究]]'
        elif '方法' in content:
            return '[[方法/研究]]'
        else:
            # 提取第一个关键词作为链接
            words = re.findall(r'[\u4e00-\u9fa5]+', content)
            if words:
                return f'[[{words[0]}]]'
            return ''

    def categorize_notes(self, notes: List[Dict]) -> Dict[str, List[Dict]]:
        """按类别组织笔记"""
        categories = {
            'task': [],
            'event': [],
            'note': [],
            'priority': []
        }

        for note in notes:
            categories[note['type']].append(note)

        return categories

    def generate_obsidian_log(
        self,
        date: str,
        notes: List[Dict]
    ) -> str:
        """
        生成Obsidian日志

        Args:
            date: 日期（YYYY-MM-DD）
            notes: 笔记数据列表

        Returns:
            Obsidian格式的Markdown日志
        """
        # 提取所有标签
        all_tags = set()
        for note in notes:
            tags = self.extract_tags(note['content'])
            all_tags.update(tags)

        # 添加日期标签
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        month_tag = f"{date_obj.year}-{date_obj.month:02d}"
        all_tags.add(month_tag)

        # 按类别组织
        categories = self.categorize_notes(notes)

        # 生成头部
        frontmatter = f"""---
date: {date}
tags: {sorted(all_tags)}
type: daily_log
---

"""

        # 生成标题
        title = f"# {date} 日志\n\n"

        # 生成任务部分
        content = ""
        if categories['priority']:
            content += "## 优先任务\n\n"
            for note in categories['priority']:
                wikilink = self.generate_wikilink(note['content'])
                content += f"- {wikilink} {note['content']} ⭐\n"
            content += "\n"

        if categories['task']:
            content += "## 任务\n\n"
            for note in categories['task']:
                wikilink = self.generate_wikilink(note['content'])
                time_str = f"{note['time']} " if note['time'] else ""
                content += f"- {wikilink} {time_str}{note['content']}\n"
            content += "\n"

        # 生成事件部分
        if categories['event']:
            content += "## 事件\n\n"
            for note in categories['event']:
                time_str = f"{note['time']} " if note['time'] else ""
                content += f"- {time_str}{note['content']}\n"
            content += "\n"

        # 生成思考与观察部分
        if categories['note']:
            content += "## 思考与观察\n\n"
            for note in categories['note']:
                wikilink = self.generate_wikilink(note['content'])
                content += f"{wikilink} {note['content']}\n"
            content += "\n"

        # 生成下一步行动
        content += "## 下一步行动\n\n"
        # 提取未完成任务
        pending_tasks = categories['task'] + categories['priority']
        for note in pending_tasks:
            content += f"- [ ] {note['content']}\n"
        content += "\n"

        # 组合完整日志
        obsidian_log = frontmatter + title + content

        return obsidian_log

    def save_to_file(self, log_content: str, output_path: str):
        """保存到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(log_content)
        print(f"Obsidian日志已保存至：{output_path}")


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

    # 筛选工作学习相关内容
    work_study_notes = processor.get_work_study_notes()

    # 生成Obsidian日志
    generator = ObsidianLogGenerator()
    obsidian_log = generator.generate_obsidian_log(
        date='2025-03-16',
        notes=work_study_notes
    )

    print("=" * 60)
    print("Obsidian日志:")
    print("=" * 60)
    print(obsidian_log)


if __name__ == '__main__':
    main()
