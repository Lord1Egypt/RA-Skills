"""
大纲草案生成器 - 渐进式成文

这个脚本当某个主题的碎片积累到一定量时，
自动生成结构化的大纲草案。
"""

import json
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
import re


class DraftGenerator:
    """大纲草案生成器"""

    def __init__(self, knowledge_base: List[Dict]):
        """
        初始化生成器

        Args:
            knowledge_base: 碎片知识库
        """
        self.knowledge_base = knowledge_base

    def generate_outline(self, topic: str,
                     min_fragments: int = 5) -> Dict:
        """
        生成主题大纲

        Args:
            topic: 主题关键词
            min_fragments: 最小碎片数量

        Returns:
            大纲草案
        """
        # 筛选相关碎片
        relevant_fragments = self._filter_by_topic(topic)

        if len(relevant_fragments) < min_fragments:
            return {
                'status': 'insufficient_fragments',
                'required': min_fragments,
                'found': len(relevant_fragments),
                'message': f"碎片数量不足，需要至少 {min_fragments} 个关于「{topic}」的碎片"
            }

        # 分析碎片内容
        analysis = self._analyze_fragments(relevant_fragments)

        # 生成大纲结构
        outline = self._build_outline(topic, relevant_fragments, analysis)

        return {
            'status': 'success',
            'topic': topic,
            'fragment_count': len(relevant_fragments),
            'outline': outline,
            'fragments': relevant_fragments
        }

    def _filter_by_topic(self, topic: str) -> List[Dict]:
        """
        根据主题筛选碎片

        Args:
            topic: 主题关键词

        Returns:
            相关碎片列表
        """
        topic_lower = topic.lower()
        relevant = []

        for fragment in self.knowledge_base:
            score = 0

            # 检查标签
            if topic_lower in [tag.lower() for tag in fragment.get('tags', [])]:
                score += 10

            # 检查内容
            if topic_lower in fragment['content'].lower():
                score += 5

            # 检查关键概念
            for concept in fragment['core_insights']['key_concepts']:
                if topic_lower in concept.lower():
                    score += 7

            if score > 0:
                fragment['relevance_score'] = score
                relevant.append(fragment)

        # 按相关性排序
        relevant.sort(key=lambda x: x['relevance_score'], reverse=True)

        return relevant

    def _analyze_fragments(self, fragments: List[Dict]) -> Dict:
        """
        分析碎片内容

        Args:
            fragments: 碎片列表

        Returns:
            分析结果
        """
        analysis = {
            'topics': Counter(),
            'concepts': Counter(),
            'points': [],
            'sources': Counter()
        }

        for fragment in fragments:
            # 统计话题标签
            for tag in fragment.get('tags', []):
                analysis['topics'][tag] += 1

            # 统计关键概念
            for concept in fragment['core_insights']['key_concepts']:
                analysis['concepts'][concept] += 1

            # 收集主要观点
            analysis['points'].extend(
                fragment['core_insights']['main_points']
            )

            # 统计来源
            source = fragment.get('source', '未知')
            analysis['sources'][source] += 1

        return analysis

    def _build_outline(self, topic: str, fragments: List[Dict],
                    analysis: Dict) -> Dict:
        """
        构建大纲结构

        Args:
            topic: 主题
            fragments: 碎片列表
            analysis: 分析结果

        Returns:
            大纲结构
        """
        outline = {
            'title': self._generate_title(topic, analysis),
            'abstract': self._generate_abstract(fragments),
            'sections': []
        }

        # 根据碎片类型决定大纲结构
        if self._is_technical_topic(topic, analysis):
            outline['sections'] = self._build_technical_outline(
                fragments, analysis
            )
        elif self._is_business_topic(topic, analysis):
            outline['sections'] = self._build_business_outline(
                fragments, analysis
            )
        else:
            outline['sections'] = self._build_general_outline(
                fragments, analysis
            )

        return outline

    def _generate_title(self, topic: str, analysis: Dict) -> str:
        """生成标题"""
        # 使用最常见的关键概念增强标题
        top_concepts = analysis['concepts'].most_common(3)
        if top_concepts:
            concepts = '、'.join([c[0] for c in top_concepts])
            return f"{topic}：{concepts}相关内容整理"
        return f"{topic}知识体系"

    def _generate_abstract(self, fragments: List[Dict]) -> str:
        """生成摘要"""
        # 合并多个碎片的摘要
        summaries = []
        for frag in fragments[:5]:  # 最多使用前 5 个
            summary = frag['core_insights']['summary']
            if summary:
                summaries.append(summary)

        return ' '.join(summaries) if summaries else "暂无摘要"

    def _is_technical_topic(self, topic: str, analysis: Dict) -> bool:
        """判断是否是技术主题"""
        tech_keywords = ['技术', '算法', '架构', '系统', '代码',
                       '开发', '实现', '模型', '框架']

        for topic, count in analysis['topics'].items():
            if any(kw in topic.lower() for kw in tech_keywords):
                return True

        return False

    def _is_business_topic(self, topic: str, analysis: Dict) -> bool:
        """判断是否是业务主题"""
        business_keywords = ['产品', '需求', '业务', '增长',
                          '市场', '用户', '运营', '策略']

        for topic, count in analysis['topics'].items():
            if any(kw in topic.lower() for kw in business_keywords):
                return True

        return False

    def _build_technical_outline(self, fragments: List[Dict],
                               analysis: Dict) -> List[Dict]:
        """构建技术类大纲"""
        sections = [
            {
                'title': '一、概述',
                'subsections': [
                    {
                        'title': '1.1 背景与动机',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['背景', '动机', '问题']
                        )
                    },
                    {
                        'title': '1.2 核心概念',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['概念', '原理', '定义']
                        )
                    }
                ]
            },
            {
                'title': '二、核心技术',
                'subsections': [
                    {
                        'title': '2.1 技术方案',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['方案', '方法', '技术']
                        )
                    },
                    {
                        'title': '2.2 关键实现',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['实现', '代码', '算法']
                        )
                    }
                ]
            },
            {
                'title': '三、应用与实践',
                'subsections': [
                    {
                        'title': '3.1 应用场景',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['应用', '场景', '案例']
                        )
                    },
                    {
                        'title': '3.2 实践经验',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['经验', '实践', '教训']
                        )
                    }
                ]
            }
        ]

        return sections

    def _build_business_outline(self, fragments: List[Dict],
                               analysis: Dict) -> List[Dict]:
        """构建业务类大纲"""
        sections = [
            {
                'title': '一、需求分析',
                'subsections': [
                    {
                        'title': '1.1 用户痛点',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['痛点', '问题', '需求']
                        )
                    },
                    {
                        'title': '1.2 市场机会',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['市场', '机会', '趋势']
                        )
                    }
                ]
            },
            {
                'title': '二、产品策略',
                'subsections': [
                    {
                        'title': '2.1 功能设计',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['功能', '设计', '特性']
                        )
                    },
                    {
                        'title': '2.2 增长策略',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['增长', '策略', '运营']
                        )
                    }
                ]
            },
            {
                'title': '三、风险管理',
                'subsections': [
                    {
                        'title': '3.1 潜在风险',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['风险', '挑战', '难点']
                        )
                    },
                    {
                        'title': '3.2 应对措施',
                        'fragments': self._find_fragments_by_keywords(
                            fragments, ['措施', '应对', '解决']
                        )
                    }
                ]
            }
        ]

        return sections

    def _build_general_outline(self, fragments: List[Dict],
                              analysis: Dict) -> List[Dict]:
        """构建通用大纲"""
        # 按话题分组
        sections = []

        # 根据最常见的话题标签分组
        top_topics = analysis['topics'].most_common(5)

        for i, (topic, count) in enumerate(top_topics, 1):
            topic_fragments = [
                f for f in fragments
                if topic in f.get('tags', [])
            ]

            sections.append({
                'title': f'{chr(64+i)}、{topic}部分',
                'subsections': [
                    {
                        'title': f'{i}.{j} 核心内容',
                        'fragments': topic_fragments[:3]
                    }
                ]
            })

        return sections

    def _find_fragments_by_keywords(self, fragments: List[Dict],
                                  keywords: List[str]) -> List[str]:
        """
        根据关键词查找碎片

        Args:
            fragments: 碎片列表
            keywords: 关键词列表

        Returns:
            碎片 ID 列表
        """
        found = []

        for fragment in fragments:
            content = fragment['content'].lower()
            if any(kw.lower() in content for kw in keywords):
                found.append(fragment['id'])

        return found

    def generate_markdown(self, outline: Dict) -> str:
        """
        生成 Markdown 格式的大纲

        Args:
            outline: 大纲结构

        Returns:
            Markdown 文本
        """
        lines = []

        # 标题
        lines.append(f"# {outline['title']}")
        lines.append("")

        # 摘要
        lines.append("## 摘要")
        lines.append(outline['abstract'])
        lines.append("")

        # 章节
        for section in outline['sections']:
            lines.append(f"## {section['title']}")

            for subsection in section['subsections']:
                lines.append(f"### {subsection['title']}")
                lines.append("")

                # 列出碎片引用
                for frag_id in subsection['fragments']:
                    # 找到对应的碎片
                    fragment = next(
                        (f for f in self.knowledge_base
                         if f['id'] == frag_id),
                        None
                    )

                    if fragment:
                        lines.append(f"- [{frag_id}]: {fragment['content'][:80]}...")
                        lines.append(f"  来源: {fragment.get('source', '未知')}")
                        lines.append("")

        return '\n'.join(lines)

    def generate_prd_draft(self, topic: str) -> Dict:
        """
        生成 PRD 文档草案

        Args:
            topic: 产品主题

        Returns:
            PRD 草案
        """
        # 筛选相关碎片
        fragments = self._filter_by_topic(topic)

        if len(fragments) < 3:
            return {
                'status': 'insufficient_fragments',
                'message': f"需要至少 3 个关于「{topic}」的碎片才能生成 PRD 草案"
            }

        # 分析碎片
        analysis = self._analyze_fragments(fragments)

        # 生成 PRD 结构
        prd = {
            'title': f'{topic} 产品需求文档',
            'version': '1.0',
            'sections': [
                {
                    'title': '1. 背景与目标',
                    'content': self._find_content_by_keywords(
                        fragments, ['背景', '目标', '动机']
                    )
                },
                {
                    'title': '2. 需求分析',
                    'content': self._find_content_by_keywords(
                        fragments, ['需求', '痛点', '用户场景']
                    )
                },
                {
                    'title': '3. 功能定义',
                    'content': self._find_content_by_keywords(
                        fragments, ['功能', '特性', '能力']
                    )
                },
                {
                    'title': '4. 非功能需求',
                    'content': self._find_content_by_keywords(
                        fragments, ['性能', '安全', '可靠性']
                    )
                },
                {
                    'title': '5. 风险与挑战',
                    'content': self._find_content_by_keywords(
                        fragments, ['风险', '挑战', '难点']
                    )
                }
            ],
            'fragments': [f['id'] for f in fragments]
        }

        return {
            'status': 'success',
            'prd': prd
        }

    def _find_content_by_keywords(self, fragments: List[Dict],
                                keywords: List[str]) -> List[str]:
        """根据关键词查找内容"""
        contents = []

        for fragment in fragments:
            content = fragment['content'].lower()
            if any(kw.lower() in content for kw in keywords):
                contents.append(fragment['content'][:200])

        return contents[:3]  # 最多返回 3 条


def generate_outline(topic: str, knowledge_base: List[Dict],
                  min_fragments: int = 5) -> Dict:
    """
    生成主题大纲

    Args:
        topic: 主题关键词
        knowledge_base: 碎片知识库
        min_fragments: 最小碎片数量

    Returns:
        大纲草案
    """
    generator = DraftGenerator(knowledge_base)
    return generator.generate_outline(topic, min_fragments)


if __name__ == '__main__':
    # 示例：生成大纲
    knowledge_base = [
        {
            'id': 'frag_001',
            'content': '大模型的安全性是一个重要议题，需要对齐模型价值观。',
            'tags': ['AI', '安全'],
            'created_at': '2026-03-15T10:30:00',
            'core_insights': {
                'key_concepts': ['大模型', '安全性', '模型对齐'],
                'main_points': ['需要对齐模型价值观'],
                'summary': '大模型的安全性是一个重要议题'
            }
        },
        {
            'id': 'frag_002',
            'content': '模型对齐技术包括RLHF、Constitutional AI等方法。',
            'tags': ['AI', '对齐'],
            'created_at': '2026-03-12T14:20:00',
            'core_insights': {
                'key_concepts': ['模型对齐', 'RLHF', 'Constitutional AI'],
                'main_points': ['RLHF 和 Constitutional AI 是主要方法'],
                'summary': '模型对齐技术包括多种方法'
            }
        },
        {
            'id': 'frag_003',
            'content': 'AI安全领域的技术手段包括内容过滤、对抗攻击防御等。',
            'tags': ['AI', '安全'],
            'created_at': '2026-03-20T17:00:00',
            'core_insights': {
                'key_concepts': ['AI安全', '内容过滤', '对抗攻击'],
                'main_points': ['内容过滤和对抗攻击防御是技术手段'],
                'summary': 'AI安全有多种技术手段'
            }
        },
        {
            'id': 'frag_004',
            'content': '对齐后的模型需要在实际应用中持续监控和优化。',
            'tags': ['AI', '应用'],
            'created_at': '2026-03-18T09:15:00',
            'core_insights': {
                'key_concepts': ['持续监控', '优化', '实际应用'],
                'main_points': ['需要持续监控和优化'],
                'summary': '模型需要在应用中持续优化'
            }
        },
        {
            'id': 'frag_005',
            'content': '安全测试是确保模型可靠性的关键环节。',
            'tags': ['AI', '测试'],
            'created_at': '2026-03-10T16:45:00',
            'core_insights': {
                'key_concepts': ['安全测试', '可靠性'],
                'main_points': ['安全测试很关键'],
                'summary': '安全测试确保模型可靠性'
            }
        }
    ]

    generator = DraftGenerator(knowledge_base)
    result = generator.generate_outline('AI安全', min_fragments=3)

    if result['status'] == 'success':
        print("生成的大纲:")
        print(f"主题: {result['topic']}")
        print(f"碎片数: {result['fragment_count']}")
        print("\n大纲结构:")
        print(json.dumps(result['outline'], indent=2, ensure_ascii=False))

        print("\nMarkdown 格式:")
        print(generator.generate_markdown(result['outline']))
    else:
        print(f"生成失败: {result['message']}")
