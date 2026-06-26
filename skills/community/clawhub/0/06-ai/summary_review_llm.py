#!/usr/bin/env python3
"""
AI总结复盘技能 v2.0 - 增强版
支持多个大模型API（智谱AI、OpenAI、Anthropic等）
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import re
import sys

# 导入通用LLM客户端
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_client import UniversalLLMClient


class AIContentSummarizer:
    """AI驱动的内容总结器（使用LLM）"""

    def __init__(self, provider: str = "zhipu", api_key: str = None):
        """
        初始化总结器

        Args:
            provider: 大模型提供商
            api_key: API密钥
        """
        self.client = UniversalLLMClient(provider, api_key)
        self.provider = provider

    def summarize(self, content: str, content_type: str = 'general') -> Dict:
        """
        使用AI总结内容

        Args:
            content: 要总结的内容
            content_type: 内容类型

        Returns:
            总结结果
        """
        if not content or not content.strip():
            return {'error': '内容不能为空'}

        if not self.client.is_available():
            # 降级到基础总结
            return self._basic_summarize(content, content_type)

        # 使用AI总结
        result = self.client.summarize(content, content_type)

        if result:
            return {
                'type': content_type,
                'provider': self.client.config.config['name'],
                'model': self.client.config.get_model('summary'),
                'summary': result,
                'created_at': datetime.now().isoformat(),
                'word_count': len(content),
                'method': 'ai'
            }
        else:
            return {'error': 'AI总结失败'}

    def _basic_summarize(self, content: str, content_type: str) -> Dict:
        """基础总结（无AI时使用）"""
        key_points = self._extract_key_points(content)
        summary = '\n'.join([f"• {p}" for p in key_points[:5]])

        return {
            'type': content_type,
            'summary': summary,
            'key_points': key_points,
            'word_count': len(content),
            'created_at': datetime.now().isoformat(),
            'method': 'basic'
        }

    def _extract_key_points(self, content: str) -> List[str]:
        """提取关键点"""
        points = []

        # 分段
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        # 每段提取第一句话
        for para in paragraphs[:5]:
            sentences = para.split('。')
            if sentences:
                first_sentence = sentences[0].strip()
                if len(first_sentence) > 10:
                    points.append(first_sentence + '。')

        if not points:
            sentences = re.split(r'[。！？]', content)
            points = [s.strip() + '。' for s in sentences if len(s.strip()) > 20][:5]

        return points


class ProjectReviewerAI:
    """AI驱动的项目复盘器"""

    def __init__(self, provider: str = "zhipu", api_key: str = None):
        """
        初始化复盘器

        Args:
            provider: 大模型提供商
            api_key: API密钥
        """
        self.client = UniversalLLMClient(provider, api_key)
        self.provider = provider

    def review(self, project_data: Dict) -> Dict:
        """
        项目复盘（AI增强版）

        Args:
            project_data: 项目数据

        Returns:
            复盘报告
        """
        name = project_data.get('name', '未命名项目')
        goals = project_data.get('goals', [])
        results = project_data.get('results', [])
        metrics = project_data.get('metrics', {})

        # 构建复盘Prompt
        review_prompt = f"""
请对以下项目进行复盘分析：

项目名称：{name}

项目目标：
{chr(10).join([f'{i+1}. {g}' for i, g in enumerate(goals)])}

实际结果：
{chr(10).join([f'{i+1}. {r}' for i, r in enumerate(results)])}

关键指标：
{json.dumps(metrics, ensure_ascii=False, indent=2)}

请从以下维度进行分析：
1. 目标达成情况（计算达成率）
2. 成功经验（列出3-5点）
3. 存在问题（列出2-3点）
4. 改进建议（具体可行的建议）
5. 下一步行动计划

请以JSON格式返回，包含以下字段：
{{
    "goal_achievement_rate": 百分比数字,
    "successes": ["成功经验1", "成功经验2"],
    "issues": ["问题1", "问题2"],
    "recommendations": ["建议1", "建议2"],
    "next_steps": ["行动1", "行动2"]
}}
"""

        if self.client.is_available():
            try:
                response = self.client.chat(
                    [{"role": "user", "content": review_prompt}],
                    temperature=0.5
                )

                # 尝试解析JSON响应
                try:
                    ai_result = json.loads(response)
                except:
                    # 如果AI返回的不是纯JSON，提取JSON部分
                    json_match = re.search(r'\{[\s\S]*\}', response)
                    if json_match:
                        ai_result = json.loads(json_match.group())
                    else:
                        raise ValueError("无法解析AI响应")

                return {
                    'project_name': name,
                    'review_date': datetime.now().strftime('%Y-%m-%d'),
                    'provider': self.client.config.config['name'],
                    'method': 'ai',
                    **ai_result
                }

            except Exception as e:
                print(f"AI复盘失败: {e}，使用基础复盘")
                return self._basic_review(project_data)
        else:
            return self._basic_review(project_data)

    def _basic_review(self, project_data: Dict) -> Dict:
        """基础复盘（无AI时使用）"""
        goals = project_data.get('goals', [])
        results = project_data.get('results', [])

        # 计算达成率
        goal_achievement = 0.0
        if goals:
            achieved = sum(1 for g in goals if any(str(g) in str(r) for r in results))
            goal_achievement = round(achieved / len(goals) * 100, 2)

        # 提取成功经验
        successes = []
        for goal in goals:
            for result in results:
                if str(goal) in str(result):
                    successes.append(f"✓ {goal} - 已达成")
                    break

        # 识别问题
        issues = []
        for goal in goals:
            if not any(str(goal) in str(r) for r in results):
                issues.append(f"✗ 目标未完全达成: {goal}")

        # 生成建议
        recommendations = [
            "针对问题制定改进计划" if issues else "保持当前良好状态",
            "将成功经验应用到后续项目" if successes else "总结经验教训",
            "建立更完善的监控机制",
            "加强团队沟通协作"
        ][:3]

        # 下一步计划
        next_steps = [
            "整理项目文档",
            "进行团队复盘会议",
            "制定下一期计划"
        ]

        return {
            'project_name': project_data.get('name', '未命名项目'),
            'review_date': datetime.now().strftime('%Y-%m-%d'),
            'method': 'basic',
            'goal_achievement_rate': goal_achievement,
            'successes': successes,
            'issues': issues,
            'recommendations': recommendations,
            'next_steps': next_steps
        }


class SummaryStorage:
    """总结存储（保持不变）"""

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
                provider TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON summaries(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON summaries(created_at)')

        conn.commit()
        conn.close()

    def save(self, title: str, content: str, summary_data: Dict, provider: str = None) -> int:
        """保存总结"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        summary_data['provider'] = provider or summary_data.get('provider', 'unknown')

        cursor.execute('''
            INSERT INTO summaries (title, type, content, summary_data, provider)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            title,
            summary_data.get('type', 'general'),
            content,
            json.dumps(summary_data, ensure_ascii=False),
            summary_data.get('provider', 'unknown')
        ))

        summary_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return summary_id

    def get_recent(self, limit: int = 10) -> List[Dict]:
        """获取最近的总结"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, type, summary_data, provider, created_at
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
                'provider': row[4],
                'created_at': row[5]
            })

        conn.close()
        return results

    def search(self, keyword: str) -> List[Dict]:
        """搜索总结"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, type, summary_data, provider, created_at
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
                'provider': row[4],
                'created_at': row[5]
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
        if data.get('provider'):
            md += f"**提供商**: {data['provider']}\n"
        md += f"**日期**: {data.get('created_at', '')}\n\n"

        if 'summary' in data:
            md += "## 总结\n\n"
            md += data['summary'] + "\n\n"

        if data.get('method') == 'ai' and data.get('key_points'):
            md += "## 关键要点\n\n"
            for point in data['key_points']:
                md += f"- {point}\n"
            md += "\n"

        return md


class AISummaryReview:
    """AI总结复盘系统（增强版）"""

    def __init__(self, provider: str = "zhipu", api_key: str = None):
        """
        初始化系统

        Args:
            provider: 大模型提供商
            api_key: API密钥
        """
        self.provider = provider
        self.summarizer = AIContentSummarizer(provider, api_key)
        self.reviewer = ProjectReviewerAI(provider, api_key)
        self.storage = SummaryStorage()

    def summarize_content(self, content: str, content_type: str = 'general', title: str = None) -> Dict:
        """
        总结内容

        Args:
            content: 内容文本
            content_type: 内容类型
            title: 标题

        Returns:
            总结结果
        """
        summary = self.summarizer.summarize(content, content_type)

        # 保存到数据库
        if title:
            self.storage.save(title, content, summary, self.summarizer.provider)

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

    def get_info(self) -> Dict:
        """获取系统信息"""
        return {
            'provider': self.provider,
            'summarizer_available': self.summarizer.client.is_available(),
            'reviewer_available': self.reviewer.client.is_available(),
            'models': self.summarizer.client.config.config['models'] if self.summarizer.client else {}
        }


def main():
    """命令行界面"""
    print("=" * 50)
    print("AI总结复盘系统 v2.0 - 增强版")
    print("=" * 50)

    print("\n支持的提供商:")
    providers = ['zhipu', 'openai', 'anthropic', 'deepseek', 'qwen']
    for p in providers:
        print(f"  - {p}")

    provider = input("\n请选择提供商 (默认zhipu): ").strip() or "zhipu"

    system = AISummaryReview(provider=provider)

    # 显示系统信息
    info = system.get_info()
    print(f"\n系统信息:")
    print(f"  提供商: {provider}")
    print(f"  总结器: {'就绪' if info['summarizer_available'] else '未配置'}")
    print(f"  复盘器: {'就绪' if info['reviewer_available'] else '未配置'}")

    if not info['summarizer_available']:
        print(f"\n提示: 将使用基础总结功能")
        print(f"如需AI增强，请设置环境变量: ZHIPU_API_KEY (或其他提供商的密钥)")

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

            print("\n请输入内容 (空行结束):")
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
            if 'error' in result:
                print(f"  错误: {result['error']}")
            else:
                print(f"  方法: {result.get('method', 'unknown').upper()}")
                print(f"  提供商: {result.get('provider', 'unknown')}")
                print(f"\n{result.get('summary', '')}")

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
            print(f"  项目: {review['project_name']}")
            print(f"  方法: {review.get('method', 'unknown').upper()}")
            print(f"  达成率: {review['goal_achievement_rate']}%")
            print(f"\n成功经验:")
            for s in review.get('successes', [])[:3]:
                print(f"  ✓ {s}")
            print(f"\n改进建议:")
            for r in review.get('recommendations', [])[:3]:
                print(f"  • {r}")

        elif choice == "3":
            history = system.get_history(20)

            if history:
                print(f"\n最近 {len(history)} 条记录:")
                for item in history:
                    print(f"\n{item['id']}. {item['title']}")
                    print(f"   类型: {item['type']} | 提供商: {item['provider']}")
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
