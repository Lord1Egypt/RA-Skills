"""
自动缝纫师 - 生成知识连接笔记

这个脚本根据发现的关系，生成"知识连接笔记"，
帮助用户理解碎片之间的关联。
"""

import json
from typing import Dict, List
from datetime import datetime


class FragmentStitcher:
    """碎片缝纫师"""

    def __init__(self, knowledge_base: List[Dict]):
        """
        初始化缝纫师

        Args:
            knowledge_base: 碎片知识库
        """
        self.knowledge_base = knowledge_base

    def generate_stitch_note(self, new_fragment: Dict,
                           relationships: List[Dict]) -> str:
        """
        生成知识连接笔记

        Args:
            new_fragment: 新碎片
            relationships: 关系列表

        Returns:
            格式化的连接笔记
        """
        if not relationships:
            return "未发现明显的知识连接。这是新的知识领域。"

        notes = []
        notes.append("📌 连接发现")
        notes.append(f"来源: {new_fragment.get('source', '未知')}")
        notes.append(f"时间: {self._format_time(new_fragment['created_at'])}")
        notes.append("")

        # 按关系类型分组
        for rel in relationships:
            target = rel['target_fragment']
            rel_types = rel['relationship_type']

            for rel_type in rel_types:
                note = self._generate_type_specific_note(
                    new_fragment, target, rel, rel_type
                )
                notes.append(note)
                notes.append("")

        return '\n'.join(notes)

    def _generate_type_specific_note(self, frag1: Dict,
                                   frag2: Dict,
                                   relationship: Dict,
                                   rel_type: str) -> str:
        """
        根据关系类型生成特定说明

        Args:
            frag1: 碎片 1（新碎片）
            frag2: 碎片 2（相关碎片）
            relationship: 关系信息
            rel_type: 关系类型

        Returns:
            格式化的说明
        """
        details = relationship['details']

        if rel_type == 'concept_similarity':
            return self._generate_concept_note(frag1, frag2, details['concepts'])

        elif rel_type == 'topic_relevance':
            return self._generate_topic_note(frag1, frag2, details['topic'])

        elif rel_type == 'logical_flow':
            return self._generate_flow_note(frag1, frag2, details['flow'])

        elif rel_type == 'complementary':
            return self._generate_complement_note(frag1, frag2, details['complement'])

        else:
            return f"🔗 与碎片 {frag2['id']} 有关联"

    def _generate_concept_note(self, frag1: Dict, frag2: Dict,
                              concept_details: Dict) -> str:
        """生成概念相似说明"""
        shared = concept_details['shared_concepts']

        if shared:
            concepts_str = '、'.join(shared[:3])  # 最多显示 3 个
            note = (f"💡 概念关联\n"
                    f"与「{frag2['id'][:20]}...」共享概念: {concepts_str}\n"
                    f"这两篇内容都涉及到 {concepts_str} 相关的话题")
        else:
            note = f"💡 概念关联\n与「{frag2['id'][:20]}...」概念相近"

        return note

    def _generate_topic_note(self, frag1: Dict, frag2: Dict,
                          topic_details: Dict) -> str:
        """生成话题相关说明"""
        shared_tags = topic_details['shared_tags']

        if shared_tags:
            tags_str = '、'.join(shared_tags)
            note = (f"📚 话题相关\n"
                    f"与「{frag2['id'][:20]}...」同属 {tags_str} 话题\n"
                    f"可以将这些碎片归类到 {tags_str} 的知识体系下")
        else:
            note = f"📚 话题相关\n与「{frag2['id'][:20]}...」主题域相似"

        return note

    def _generate_flow_note(self, frag1: Dict, frag2: Dict,
                         flow_details: Dict) -> str:
        """生成逻辑延续说明"""
        flow_type = flow_details['flow_type']

        flow_explanations = {
            'requirement_to_solution': "需求→方案",
            'requirement_to_solution_reverse': "方案→需求",
            'problem_to_cause': "问题→原因",
            'problem_to_cause_reverse': "原因→问题",
            'hypothesis_to_validation': "假设→验证",
            'hypothesis_to_validation_reverse': "验证→假设",
            'concept_to_application': "概念→应用",
            'concept_to_application_reverse': "应用→概念"
        }

        if flow_type in flow_explanations:
            flow_name = flow_explanations[flow_type]
            note = (f"🔄 逻辑延续\n"
                    f"与「{frag2['id'][:20]}...」形成 {flow_name} 的关系\n"
                    f"可以将这两篇内容串联，形成完整的逻辑链")
        else:
            note = (f"🔄 逻辑延续\n"
                    f"与「{frag2['id'][:20]}...」存在逻辑关联")

        return note

    def _generate_complement_note(self, frag1: Dict, frag2: Dict,
                                complement_details: Dict) -> str:
        """生成补充增强说明"""
        comp_type = complement_details['complement_type']

        comp_explanations = {
            'positive_negative': "优势+劣势",
            'theory_practice': "理论+实践",
            'overview_detail': "概述+详细",
            'before_after': "改进前后"
        }

        if comp_type in comp_explanations:
            comp_name = comp_explanations[comp_type]
            note = (f"⚖️ 互补增强\n"
                    f"与「{frag2['id'][:20]}...」形成 {comp_name} 的互补关系\n"
                    f"结合这两篇内容，可以获得更全面的认识")
        else:
            note = (f"⚖️ 互补增强\n"
                    f"与「{frag2['id'][:20]}...」内容互补")

        return note

    def generate_batch_stitch_notes(self, fragments: List[Dict],
                                  relationship_finder) -> Dict[str, str]:
        """
        批量生成缝合笔记

        Args:
            fragments: 碎片列表
            relationship_finder: 关系发现器实例

        Returns:
            碎片 ID 到缝合笔记的映射
        """
        stitch_notes = {}

        for fragment in fragments:
            # 发现关系
            relationships = relationship_finder.find_relationships(
                fragment, top_k=3
            )

            # 生成缝合笔记
            note = self.generate_stitch_note(fragment, relationships)

            stitch_notes[fragment['id']] = note

            # 更新碎片的缝合笔记字段
            fragment['stitch_notes'].append(note)

        return stitch_notes

    def generate_prd_supplement_note(self, fragment: Dict,
                                    related_fragments: List[Dict]) -> str:
        """
        生成 PRD 文档补充说明

        Args:
            fragment: 当前碎片
            related_fragments: 相关碎片列表

        Returns:
            PRD 补充说明
        """
        note_parts = []
        note_parts.append("📋 PRD 补充建议")
        note_parts.append("")

        # 分析可以补充到 PRD 的内容
        for rel_frag in related_fragments:
            # 检查是否是需求或风险相关
            content = rel_frag['content'].lower()

            if any(kw in content for kw in ['需求', '功能', '用户场景', '痛点']):
                note_parts.append(f"✅ 需求相关:")
                note_parts.append(f"   来自: {rel_frag.get('source', '未知')}")
                note_parts.append(f"   内容: {rel_frag['content'][:100]}...")
                note_parts.append("")

            elif any(kw in content for kw in ['风险', '挑战', '问题', '难点']):
                note_parts.append(f"⚠️  风险相关:")
                note_parts.append(f"   来自: {rel_frag.get('source', '未知')}")
                note_parts.append(f"   内容: {rel_frag['content'][:100]}...")
                note_parts.append("")

            elif any(kw in content for kw in ['方案', '解决', '实现']):
                note_parts.append(f"🔧 技术方案参考:")
                note_parts.append(f"   来自: {rel_frag.get('source', '未知')}")
                note_parts.append(f"   内容: {rel_frag['content'][:100]}...")
                note_parts.append("")

        if len(note_parts) == 2:  # 只有标题，没有内容
            note_parts.append("暂未发现可以补充到 PRD 的内容")

        return '\n'.join(note_parts)

    def generate_weekly_digest(self, fragments: List[Dict],
                             relationship_finder) -> str:
        """
        生成每周知识摘要

        Args:
            fragments: 本周收集的碎片
            relationship_finder: 关系发现器

        Returns:
            摘要文本
        """
        digest = []
        digest.append("=" * 50)
        digest.append(f"每周知识摘要 - {self._get_week_range()}")
        digest.append("=" * 50)
        digest.append("")

        # 统计信息
        digest.append(f"📊 本周收集: {len(fragments)} 个碎片")

        # 话题统计
        topic_count = {}
        for frag in fragments:
            for tag in frag.get('tags', []):
                topic_count[tag] = topic_count.get(tag, 0) + 1

        if topic_count:
            digest.append("🏷️  热门话题:")
            for topic, count in sorted(topic_count.items(),
                                    key=lambda x: x[1],
                                    reverse=True)[:5]:
                digest.append(f"   {topic}: {count} 个碎片")
        digest.append("")

        # 生成缝合笔记
        for i, fragment in enumerate(fragments[:3], 1):  # 最多展示 3 个
            relationships = relationship_finder.find_relationships(
                fragment, top_k=2
            )

            if relationships:
                digest.append(f"{i}. {fragment['content'][:50]}...")
                for rel in relationships[:2]:  # 最多展示 2 个关联
                    target = rel['target_fragment']
                    digest.append(f"   → 关联: {target['content'][:40]}...")
                digest.append("")

        return '\n'.join(digest)

    def _format_time(self, time_str: str) -> str:
        """格式化时间"""
        try:
            dt = datetime.fromisoformat(time_str)
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return time_str

    def _get_week_range(self) -> str:
        """获取本周日期范围"""
        today = datetime.now()
        week_start = today - datetime.timedelta(days=today.weekday())
        week_end = week_start + datetime.timedelta(days=6)

        return f"{week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')}"


def generate_stitch_notes(fragments: List[Dict],
                         knowledge_base: List[Dict],
                         relationship_finder) -> Dict[str, str]:
    """
    批量生成知识连接笔记

    Args:
        fragments: 碎片列表
        knowledge_base: 碎片知识库
        relationship_finder: 关系发现器实例

    Returns:
        碎片 ID 到缝合笔记的映射
    """
    stitcher = FragmentStitcher(knowledge_base)
    return stitcher.generate_batch_stitch_notes(fragments, relationship_finder)


if __name__ == '__main__':
    # 示例：生成缝合笔记
    knowledge_base = [
        {
            'id': 'frag_001',
            'content': '大模型的安全性是一个重要议题，需要对齐模型价值观。',
            'source': '微信文章',
            'tags': ['AI', '安全'],
            'created_at': '2026-03-15T10:30:00',
            'core_insights': {
                'key_concepts': ['大模型', '安全性', '模型对齐']
            }
        },
        {
            'id': 'frag_002',
            'content': '模型对齐技术包括RLHF、Constitutional AI等方法。',
            'source': '论文阅读',
            'tags': ['AI', '对齐'],
            'created_at': '2026-03-12T14:20:00',
            'core_insights': {
                'key_concepts': ['模型对齐', 'RLHF', 'Constitutional AI']
            }
        }
    ]

    new_fragment = {
        'id': 'frag_003',
        'content': 'AI安全领域的技术手段包括内容过滤、对抗攻击防御等。',
        'source': '网页阅读',
        'tags': ['AI', '安全'],
        'created_at': '2026-03-20T17:00:00',
        'core_insights': {
            'key_concepts': ['AI安全', '内容过滤', '对抗攻击']
        }
    }

    from scripts_new.relationship_finder import RelationshipFinder

    finder = RelationshipFinder(knowledge_base)
    relationships = finder.find_relationships(new_fragment, top_k=2)

    stitcher = FragmentStitcher(knowledge_base)
    note = stitcher.generate_stitch_note(new_fragment, relationships)

    print("知识连接笔记:")
    print(note)
