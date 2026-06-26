#!/usr/bin/env python3
"""
AI总结复盘技能 v1.0
智能内容总结和项目复盘工具
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import re


class ContentSummarizer:
    """内容总结器"""

    def __init__(self):
        """初始化总结器"""
        self.templates = {
            'daily': self._daily_summary_template,
            'meeting': self._meeting_summary_template,
            'project': self._project_summary_template,
            'article': self._article_summary_template,
        }

    def summarize(self, content: str, content_type: str = 'general') -> Dict:
        """
        总结内容

        Args:
            content: 要总结的内容
            content_type: 内容类型

        Returns:
            总结结果
        """
        if not content or not content.strip():
            return {'error': '内容不能为空'}

        # 使用相应的模板
        template_func = self.templates.get(content_type, self._general_summary_template)

        # 提取关键信息
        key_points = self._extract_key_points(content)
        summary = self._generate_summary(content, key_points)

        return template_func(content, key_points, summary)

    def _extract_key_points(self, content: str) -> List[str]:
        """提取关键点"""
        points = []

        # 分段
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        # 每段提取第一句话作为关键点
        for para in paragraphs[:5]:  # 最多5个关键点
            sentences = para.split('。')
            if sentences:
                first_sentence = sentences[0].strip()
                if len(first_sentence) > 10:
                    points.append(first_sentence + '。')

        # 如果没有段落，按句子分割
        if not points:
            sentences = re.split(r'[。！？]', content)
            points = [s.strip() + '。' for s in sentences if len(s.strip()) > 20][:5]

        return points

    def _generate_summary(self, content: str, key_points: List[str]) -> str:
        """生成总结"""
        if len(content) <= 200:
            return content

        # 取前几个关键点
        summary_points = key_points[:3]
        return '\n'.join([f"• {p}" for p in summary_points])

    def _general_summary_template(self, content: str, key_points: List[str], summary: str) -> Dict:
        """通用总结模板"""
        word_count = len(content)

        return {
            'type': 'general',
            'word_count': word_count,
            'key_points': key_points,
            'summary': summary,
            'created_at': datetime.now().isoformat()
        }

    def _daily_summary_template(self, content: str, key_points: List[str], summary: str) -> Dict:
        """日报总结模板"""
        # 提取今日完成
        completed = [p for p in key_points if any(keyword in p for keyword in ['完成', '实现', '解决'])]

        # 提取遇到的问题
        problems = [p for p in key_points if any(keyword in p for keyword in ['问题', '错误', '失败'])]

        return {
            'type': 'daily',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'completed_tasks': completed,
            'issues': problems,
            'summary': summary,
            'key_points': key_points
        }

    def _meeting_summary_template(self, content: str, key_points: List[str], summary: str) -> Dict:
        """会议总结模板"""
        return {
            'type': 'meeting',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'attendees': [],  # 可以手动添加
            'agenda': key_points[:3],
            'decisions': [],  # 可以从内容中提取
            'action_items': key_points[3:],
            'summary': summary
        }

    def _project_summary_template(self, content: str, key_points: List[str], summary: str) -> Dict:
        """项目复盘模板"""
        return {
            'type': 'project',
            'project_name': '',
            'goals': key_points[:2],
            'achievements': key_points[2:4],
            'challenges': [],
            'lessons_learned': [],
            'next_steps': key_points[4:],
            'summary': summary
        }

    def _article_summary_template(self, content: str, key_points: List[str], summary: str) -> Dict:
        """文章总结模板"""
        return {
            'type': 'article',
            'title': '',
            'main_idea': key_points[0] if key_points else '',
            'key_arguments': key_points[1:4],
            'conclusion': key_points[-1] if len(key_points) > 1 else '',
            'summary': summary
        }


class ProjectReviewer:
    """项目复盘器"""

    def __init__(self):
        """初始化复盘器"""
        pass

    def review(self, project_data: Dict) -> Dict:
        """
        项目复盘

        Args:
            project_data: 项目数据，包含 goals, results, metrics 等

        Returns:
            复盘报告
        """
        goals = project_data.get('goals', [])
        results = project_data.get('results', [])
        metrics = project_data.get('metrics', {})

        # 计算目标达成率
        goal_achievement = self._calculate_goal_achievement(goals, results)

        # 提取成功经验
        successes = self._extract_successes(goals, results)

        # 识别问题
        issues = self._identify_issues(goals, results, metrics)

        # 生成建议
        recommendations = self._generate_recommendations(successes, issues)

        return {
            'project_name': project_data.get('name', '未命名项目'),
            'review_date': datetime.now().strftime('%Y-%m-%d'),
            'goal_achievement_rate': goal_achievement,
            'successes': successes,
            'issues': issues,
            'recommendations': recommendations,
            'next_steps': self._generate_next_steps(project_data)
        }

    def _calculate_goal_achievement(self, goals: List, results: List) -> float:
        """计算目标达成率"""
        if not goals:
            return 0.0

        achieved = sum(1 for g in goals if any(r in str(g) for r in results))
        return round(achieved / len(goals) * 100, 2)

    def _extract_successes(self, goals: List, results: List) -> List[str]:
        """提取成功经验"""
        successes = []

        for goal in goals:
            for result in results:
                if str(goal) in str(result):
                    successes.append(f"✓ {goal} - 已达成")
                    break

        return successes

    def _identify_issues(self, goals: List, results: List, metrics: Dict) -> List[str]:
        """识别问题"""
        issues = []

        # 检查未达成目标
        for goal in goals:
            if not any(str(goal) in str(r) for r in results):
                issues.append(f"✗ 目标未完全达成: {goal}")

        # 检查指标异常
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                if value < 50:
                    issues.append(f"⚠ 指标偏低: {key} = {value}")

        return issues

    def _generate_recommendations(self, successes: List, issues: List) -> List[str]:
        """生成建议"""
        recommendations = []

        if issues:
            recommendations.append("针对问题制定改进计划")

        if successes:
            recommendations.append("将成功经验应用到后续项目")

        recommendations.extend([
            "建立更完善的监控机制",
            "加强团队沟通协作",
            "定期进行进度检查"
        ])

        return recommendations[:5]

    def _generate_next_steps(self, project_data: Dict) -> List[str]:
        """生成下一步计划"""
        return [
            "整理项目文档",
            "进行团队复盘会议",
            "制定下一期计划",
            "跟进未解决问题"
        ]


class SummaryStorage:
    """总结存储"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path.home() / ".ai_summary.db"

        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                type TEXT,
                content TEXT NOT NULL,
                summary_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON summaries(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON summaries(created_at)')

        conn.commit()
        conn.close()

    def save(self, title: str, content: str, summary_data: Dict) -> int:
        """保存总结"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO summaries (title, type, content, summary_data)
            VALUES (?, ?, ?, ?)
        ''', (title, summary_data.get('type', 'general'), content, json.dumps(summary_data, ensure_ascii=False)))

        summary_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return summary_id

    def get_recent(self, limit: int = 10) -> List[Dict]:
        """获取最近的总结"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, type, summary_data, created_at
            FROM summaries
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'title': row[1],
                'type': row[2],
                'data': json.loads(row[3]),
                'created_at': row[4]
            })

        conn.close()
        return results

    def search(self, keyword: str) -> List[Dict]:
        """搜索总结"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, type, summary_data, created_at
            FROM summaries
            WHERE content LIKE ? OR title LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{keyword}%', f'%{keyword}%'))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'title': row[1],
                'type': row[2],
                'data': json.loads(row[3]),
                'created_at': row[4]
            })

        conn.close()
        return results

    def export_markdown(self, summary_id: int) -> str:
        """导出为Markdown"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT title, summary_data FROM summaries WHERE id = ?', (summary_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return ""

        title, data_json = row
        data = json.loads(data_json)

        md = f"# {title}\n\n"
        md += f"**类型**: {data.get('type', 'general')}\n"
        md += f"**日期**: {data.get('created_at', '')}\n\n"

        if 'key_points' in data:
            md += "## 关键要点\n\n"
            for point in data['key_points']:
                md += f"- {point}\n"
            md += "\n"

        if 'summary' in data:
            md += "## 总结\n\n"
            md += data['summary'] + "\n\n"

        return md


class AISummaryReview:
    """AI总结复盘系统"""

    def __init__(self):
        """初始化系统"""
        self.summarizer = ContentSummarizer()
        self.reviewer = ProjectReviewer()
        self.storage = SummaryStorage()

    def summarize_content(self, content: str, content_type: str = 'general', title: str = None) -> Dict:
        """
        总结内容

        Args:
            content: 内容文本
            content_type: 内容类型 (daily, meeting, project, article, general)
            title: 标题

        Returns:
            总结结果
        """
        summary = self.summarizer.summarize(content, content_type)

        # 保存到数据库
        if title:
            self.storage.save(title, content, summary)

        return summary

    def review_project(self, project_data: Dict) -> Dict:
        """
        复盘项目

        Args:
            project_data: 项目数据

        Returns:
            复盘报告
        """
        return self.reviewer.review(project_data)

    def get_history(self, limit: int = 10) -> List[Dict]:
        """获取历史记录"""
        return self.storage.get_recent(limit)

    def search_summaries(self, keyword: str) -> List[Dict]:
        """搜索总结"""
        return self.storage.search(keyword)

    def export_to_markdown(self, summary_id: int, output_path: str = None) -> str:
        """导出为Markdown文件"""
        md_content = self.storage.export_markdown(summary_id)

        if not output_path:
            output_path = f"summary_{summary_id}.md"

        Path(output_path).write_text(md_content, encoding='utf-8')
        return output_path


def main():
    """命令行界面"""
    print("=" * 50)
    print("AI总结复盘系统 v1.0")
    print("=" * 50)

    system = AISummaryReview()

    while True:
        print("\n请选择操作:")
        print("1. 内容总结")
        print("2. 项目复盘")
        print("3. 查看历史")
        print("4. 搜索总结")
        print("5. 导出Markdown")
        print("0. 退出")

        choice = input("\n请输入选项: ").strip()

        if choice == "0":
            print("再见！")
            break

        elif choice == "1":
            print("\n内容类型:")
            print("1. 日报 (daily)")
            print("2. 会议 (meeting)")
            print("3. 项目 (project)")
            print("4. 文章 (article)")
            print("5. 通用 (general)")

            type_choice = input("选择类型 (1-5): ").strip()
            type_map = {'1': 'daily', '2': 'meeting', '3': 'project', '4': 'article', '5': 'general'}
            content_type = type_map.get(type_choice, 'general')

            content = input("请输入内容 (支持多行，空行结束):\n")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            content = '\n'.join(lines)

            title = input("标题 (可选): ").strip() or f"{content_type}总结"

            result = system.summarize_content(content, content_type, title)

            print("\n" + "=" * 50)
            print("总结结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "2":
            print("\n项目复盘")

            name = input("项目名称: ").strip()
            goals_input = input("项目目标 (用逗号分隔): ").strip()
            results_input = input("实际结果 (用逗号分隔): ").strip()

            goals = [g.strip() for g in goals_input.split(',') if g.strip()]
            results = [r.strip() for r in results_input.split(',') if r.strip()]

            project_data = {
                'name': name,
                'goals': goals,
                'results': results,
                'metrics': {}
            }

            review = system.review_project(project_data)

            print("\n" + "=" * 50)
            print("复盘报告:")
            print(json.dumps(review, indent=2, ensure_ascii=False))

        elif choice == "3":
            history = system.get_history(20)

            if history:
                print(f"\n最近 {len(history)} 条记录:")
                for item in history:
                    print(f"\n{item['id']}. {item['title']}")
                    print(f"   类型: {item['type']}")
                    print(f"   时间: {item['created_at']}")
            else:
                print("暂无历史记录")

        elif choice == "4":
            keyword = input("请输入搜索关键词: ").strip()
            results = system.search_summaries(keyword)

            if results:
                print(f"\n找到 {len(results)} 条记录:")
                for item in results:
                    print(f"\n{item['id']}. {item['title']}")
                    print(f"   {item['data'].get('summary', '')[:100]}...")
            else:
                print("未找到相关记录")

        elif choice == "5":
            summary_id = input("请输入总结ID: ").strip()
            if summary_id.isdigit():
                output_path = system.export_to_markdown(int(summary_id))
                print(f"✓ 已导出到: {output_path}")
            else:
                print("无效的ID")


if __name__ == "__main__":
    main()
