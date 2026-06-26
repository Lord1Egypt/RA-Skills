"""
关系发现器 - 分析碎片之间的关联

这个脚本分析新碎片与已有知识库的关联，
识别概念相似、话题相关、逻辑延续等关系。
"""

import json
from typing import Dict, List, Tuple, Set
from collections import Counter
import re


class RelationshipFinder:
    """碎片关系发现器"""

    def __init__(self, knowledge_base: List[Dict]):
        """
        初始化关系发现器

        Args:
            knowledge_base: 碎片知识库
        """
        self.knowledge_base = knowledge_base
        self.relationships = []

    def find_relationships(self, new_fragment: Dict,
                         top_k: int = 5) -> List[Dict]:
        """
        发现新碎片与知识库的关联

        Args:
            new_fragment: 新碎片
            top_k: 返回最相关的碎片数量

        Returns:
            关系列表
        """
        relationships = []

        for existing_fragment in self.knowledge_base:
            # 跳过自己
            if existing_fragment['id'] == new_fragment['id']:
                continue

            # 分析多种关系类型
            relationship = {
                'target_fragment': existing_fragment,
                'relationship_type': [],
                'confidence': 0.0,
                'details': {}
            }

            # 1. 概念相似
            concept_sim = self._check_concept_similarity(
                new_fragment, existing_fragment
            )
            if concept_sim['similarity'] > 0.3:
                relationship['relationship_type'].append('concept_similarity')
                relationship['confidence'] += concept_sim['similarity']
                relationship['details']['concepts'] = concept_sim

            # 2. 话题相关
            topic_rel = self._check_topic_relevance(
                new_fragment, existing_fragment
            )
            if topic_rel['relevance'] > 0.3:
                relationship['relationship_type'].append('topic_relevance')
                relationship['confidence'] += topic_rel['relevance']
                relationship['details']['topic'] = topic_rel

            # 3. 逻辑延续
            logical_flow = self._check_logical_flow(
                new_fragment, existing_fragment
            )
            if logical_flow['flow_score'] > 0.3:
                relationship['relationship_type'].append('logical_flow')
                relationship['confidence'] += logical_flow['flow_score']
                relationship['details']['flow'] = logical_flow

            # 4. 补充增强
            complement = self._check_complementary(
                new_fragment, existing_fragment
            )
            if complement['complement_score'] > 0.3:
                relationship['relationship_type'].append('complementary')
                relationship['confidence'] += complement['complement_score']
                relationship['details']['complement'] = complement

            # 如果有任何关系，添加到结果
            if relationship['relationship_type']:
                # 归一化置信度
                relationship['confidence'] = min(relationship['confidence'], 1.0)
                relationships.append(relationship)

        # 按置信度排序
        relationships.sort(key=lambda x: x['confidence'], reverse=True)

        return relationships[:top_k]

    def _check_concept_similarity(self, frag1: Dict,
                                frag2: Dict) -> Dict:
        """
        检查概念相似度

        Args:
            frag1: 碎片 1
            frag2: 碎片 2

        Returns:
            相似度分析结果
        """
        concepts1 = set(frag1['core_insights']['key_concepts'])
        concepts2 = set(frag2['core_insights']['key_concepts'])

        # 计算交集
        intersection = concepts1 & concepts2
        union = concepts1 | concepts2

        # Jaccard 相似度
        if union:
            similarity = len(intersection) / len(union)
        else:
            similarity = 0.0

        return {
            'similarity': similarity,
            'shared_concepts': list(intersection),
            'unique_to_frag1': list(concepts1 - concepts2),
            'unique_to_frag2': list(concepts2 - concepts1)
        }

    def _check_topic_relevance(self, frag1: Dict,
                             frag2: Dict) -> Dict:
        """
        检查话题相关性

        Args:
            frag1: 碎片 1
            frag2: 碎片 2

        Returns:
            相关性分析结果
        """
        tags1 = set(frag1.get('tags', []))
        tags2 = set(frag2.get('tags', []))

        # 计算标签重叠
        if tags1 and tags2:
            overlap = len(tags1 & tags2)
            relevance = overlap / min(len(tags1), len(tags2))
        else:
            relevance = 0.0

        # 检查来源是否在同一主题域
        source_relevance = self._check_source_topic(frag1, frag2)

        return {
            'relevance': (relevance + source_relevance) / 2,
            'shared_tags': list(tags1 & tags2),
            'topic_alignment': source_relevance
        }

    def _check_source_topic(self, frag1: Dict, frag2: Dict) -> float:
        """
        检查来源是否在同一主题域

        简单实现：基于来源的关键词
        """
        source1 = frag1.get('source', '').lower()
        source2 = frag2.get('source', '').lower()

        # 定义主题域
        topic_domains = {
            'ai': ['ai', '人工智能', '机器学习', '深度学习', 'ml', 'dl'],
            'tech': ['技术', '技术', '编程', '代码', '开发'],
            'product': ['产品', '需求', 'prd', 'feature'],
            'design': ['设计', 'ui', 'ux', '界面'],
            'business': ['业务', '商业', '市场', '增长']
        }

        for domain, keywords in topic_domains.items():
            in_domain1 = any(kw in source1 for kw in keywords)
            in_domain2 = any(kw in source2 for kw in keywords)

            if in_domain1 and in_domain2:
                return 0.8  # 同一主题域，高相关性

        return 0.0  # 不同主题域

    def _check_logical_flow(self, frag1: Dict,
                         frag2: Dict) -> Dict:
        """
        检查逻辑延续关系

        识别需求→方案→实现、问题→解决、观点→论证等逻辑链
        """
        flow_score = 0.0
        flow_type = None

        # 定义逻辑链关键词
        logical_patterns = {
            'requirement_to_solution': (['需求', '问题', '痛点'],
                                      ['方案', '解决', '实现', '优化']),
            'problem_to_cause': (['问题', '故障', '错误'],
                                ['原因', '根因', '根本']),
            'hypothesis_to_validation': (['假设', '推测', '预判'],
                                       ['验证', '证明', '确认', '实验']),
            'concept_to_application': (['概念', '原理', '理论'],
                                   ['应用', '实践', '案例'])
        }

        content1 = frag1['content'].lower()
        content2 = frag2['content'].lower()

        for flow_name, (keywords1, keywords2) in logical_patterns.items():
            # 检查 frag1 是否有第一组关键词
            has_keywords1 = any(kw in content1 for kw in keywords1)
            # 检查 frag2 是否有第二组关键词
            has_keywords2 = any(kw in content2 for kw in keywords2)

            if has_keywords1 and has_keywords2:
                flow_score = 0.7
                flow_type = flow_name
                break

            # 反向检查
            has_keywords1_reverse = any(kw in content1 for kw in keywords2)
            has_keywords2_reverse = any(kw in content2 for kw in keywords1)

            if has_keywords1_reverse and has_keywords2_reverse:
                flow_score = 0.7
                flow_type = f"{flow_name}_reverse"
                break

        return {
            'flow_score': flow_score,
            'flow_type': flow_type
        }

    def _check_complementary(self, frag1: Dict,
                          frag2: Dict) -> Dict:
        """
        检查补充增强关系

        识别正面案例+反面案例、理论+实践、优势+劣势等互补关系
        """
        complement_score = 0.0
        complement_type = None

        content1 = frag1['content'].lower()
        content2 = frag2['content'].lower()

        # 定义互补关键词对
        complementary_patterns = {
            'positive_negative': (['优势', '优点', '好处', '成功'],
                                ['劣势', '缺点', '问题', '失败']),
            'theory_practice': (['理论', '概念', '原理', '模型'],
                               ['实践', '案例', '实验', '实际']),
            'overview_detail': (['概述', '总结', '简介'],
                              ['详细', '深入', '具体']),
            'before_after': (['之前', '原有', '旧'],
                             ['之后', '新', '改进'])
        }

        for comp_name, (keywords1, keywords2) in complementary_patterns.items():
            has_keywords1 = any(kw in content1 for kw in keywords1)
            has_keywords2 = any(kw in content2 for kw in keywords2)

            if has_keywords1 and has_keywords2:
                complement_score = 0.6
                complement_type = comp_name
                break

        return {
            'complement_score': complement_score,
            'complement_type': complement_type
        }

    def build_relationship_graph(self) -> Dict:
        """
        构建完整的关系图谱

        Returns:
            关系图数据结构
        """
        graph = {
            'nodes': [],
            'edges': []
        }

        # 添加所有碎片作为节点
        for fragment in self.knowledge_base:
            graph['nodes'].append({
                'id': fragment['id'],
                'tags': fragment.get('tags', []),
                'created_at': fragment['created_at']
            })

        # 构建边（碎片之间的关系）
        for i, frag1 in enumerate(self.knowledge_base):
            relationships = self.find_relationships(frag1, top_k=3)

            for rel in relationships:
                frag2 = rel['target_fragment']

                # 添加边
                graph['edges'].append({
                    'source': frag1['id'],
                    'target': frag2['id'],
                    'weight': rel['confidence'],
                    'type': rel['relationship_type']
                })

        return graph

    def find_topic_clusters(self, min_cluster_size: int = 3) -> List[List[str]]:
        """
        发现话题聚类

        基于标签和概念相似度聚类碎片

        Args:
            min_cluster_size: 最小聚类大小

        Returns:
            聚类结果，每个聚类包含碎片 ID
        """
        # 使用标签和概念构建特征向量
        feature_vectors = {}
        for fragment in self.knowledge_base:
            features = set(fragment.get('tags', []))
            features.update(fragment['core_insights']['key_concepts'])
            feature_vectors[fragment['id']] = features

        # 简单的聚类算法：基于特征重叠
        clusters = []
        processed = set()

        for frag_id, features in feature_vectors.items():
            if frag_id in processed:
                continue

            # 找到相似的碎片
            cluster = [frag_id]
            processed.add(frag_id)

            for other_id, other_features in feature_vectors.items():
                if other_id not in processed:
                    # 计算特征重叠
                    overlap = len(features & other_features)
                    if overlap >= 2:  # 至少有 2 个共同特征
                        cluster.append(other_id)
                        processed.add(other_id)

            if len(cluster) >= min_cluster_size:
                clusters.append(cluster)

        return clusters


def discover_relationships(new_fragment: Dict, knowledge_base: List[Dict],
                       top_k: int = 5) -> List[Dict]:
    """
    发现新碎片与知识库的关联

    Args:
        new_fragment: 新碎片
        knowledge_base: 碎片知识库
        top_k: 返回最相关的碎片数量

    Returns:
        关系列表
    """
    finder = RelationshipFinder(knowledge_base)
    return finder.find_relationships(new_fragment, top_k)


if __name__ == '__main__':
    # 示例：发现关系
    knowledge_base = [
        {
            'id': 'frag_001',
            'content': '大模型的安全性是一个重要议题，需要对齐模型价值观。',
            'tags': ['AI', '安全'],
            'core_insights': {
                'key_concepts': ['大模型', '安全性', '模型对齐']
            }
        },
        {
            'id': 'frag_002',
            'content': '模型对齐技术包括RLHF、Constitutional AI等方法。',
            'tags': ['AI', '对齐'],
            'core_insights': {
                'key_concepts': ['模型对齐', 'RLHF', 'Constitutional AI']
            }
        },
        {
            'id': 'frag_003',
            'content': '产品增长需要关注用户留存、活跃度和推荐算法优化。',
            'tags': ['产品', '增长'],
            'core_insights': {
                'key_concepts': ['产品增长', '用户留存', '推荐算法']
            }
        }
    ]

    new_fragment = {
        'id': 'frag_004',
        'content': 'AI安全领域的技术手段包括内容过滤、对抗攻击防御等。',
        'tags': ['AI', '安全'],
        'core_insights': {
            'key_concepts': ['AI安全', '内容过滤', '对抗攻击']
        }
    }

    finder = RelationshipFinder(knowledge_base)
    relationships = finder.find_relationships(new_fragment, top_k=3)

    print("发现的关系:")
    for rel in relationships:
        target = rel['target_fragment']
        print(f"\n与碎片 {target['id']} 的关联:")
        print(f"  类型: {rel['relationship_type']}")
        print(f"  置信度: {rel['confidence']:.2f}")
        print(f"  详情: {rel['details']}")

    # 话题聚类
    clusters = finder.find_topic_clusters()
    print(f"\n发现 {len(clusters)} 个话题聚类")
    for i, cluster in enumerate(clusters, 1):
        print(f"聚类 {i}: {cluster}")
