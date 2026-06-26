#!/usr/bin/env python3
"""
知识图谱构建工具
用于构建和管理技术知识图谱，支持知识关联和智能推荐
"""

import os
import json
import re
from datetime import datetime
from collections import defaultdict

class KnowledgeGraph:
    def __init__(self):
        self.graph_data = {
            'nodes': [],
            'edges': []
        }
        self.node_id_counter = 1
        self.edge_id_counter = 1
        self.known_nodes = {}
    
    def add_node(self, name, type, description=None, attributes=None):
        """添加节点
        
        Args:
            name: 节点名称
            type: 节点类型 (tech, concept, pattern, resource)
            description: 节点描述
            attributes: 节点属性
            
        Returns:
            node_id: 节点ID
        """
        # 检查节点是否已存在
        node_key = f"{type}:{name.lower()}"
        if node_key in self.known_nodes:
            return self.known_nodes[node_key]
        
        # 创建新节点
        node = {
            'id': self.node_id_counter,
            'name': name,
            'type': type,
            'description': description,
            'attributes': attributes or {},
            'created_at': datetime.now().isoformat()
        }
        
        # 添加到图谱
        self.graph_data['nodes'].append(node)
        self.known_nodes[node_key] = self.node_id_counter
        self.node_id_counter += 1
        
        return node['id']
    
    def add_edge(self, source_id, target_id, relationship, weight=1.0, attributes=None):
        """添加边
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            relationship: 关系类型
            weight: 关系权重
            attributes: 边属性
            
        Returns:
            edge_id: 边ID
        """
        # 检查边是否已存在
        for edge in self.graph_data['edges']:
            if (edge['source'] == source_id and 
                edge['target'] == target_id and 
                edge['relationship'] == relationship):
                # 更新权重
                edge['weight'] += weight
                return edge['id']
        
        # 创建新边
        edge = {
            'id': self.edge_id_counter,
            'source': source_id,
            'target': target_id,
            'relationship': relationship,
            'weight': weight,
            'attributes': attributes or {},
            'created_at': datetime.now().isoformat()
        }
        
        # 添加到图谱
        self.graph_data['edges'].append(edge)
        self.edge_id_counter += 1
        
        return edge['id']
    
    def build_from_knowledge_base(self, knowledge_base_path):
        """从知识库构建图谱
        
        Args:
            knowledge_base_path: 知识库路径
        """
        print(f"从知识库构建图谱: {knowledge_base_path}")
        
        # 遍历知识库文件
        for root, dirs, files in os.walk(knowledge_base_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self._process_markdown_file(file_path)
                elif file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self._process_python_file(file_path)
        
        print(f"图谱构建完成: {len(self.graph_data['nodes'])} 个节点, {len(self.graph_data['edges'])} 条边")
    
    def _process_markdown_file(self, file_path):
        """处理Markdown文件
        
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件失败: {file_path}, {str(e)}")
            return
        
        # 提取文件信息
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        
        # 创建文件节点
        file_node_id = self.add_node(
            file_name,
            'resource',
            f"知识库文件: {file_path}",
            {'path': file_path, 'type': 'markdown'}
        )
        
        # 提取技术术语
        tech_terms = self._extract_tech_terms(content)
        for term in tech_terms:
            # 创建技术节点
            tech_node_id = self.add_node(
                term,
                'tech',
                f"技术术语: {term}"
            )
            
            # 添加关联
            self.add_edge(
                file_node_id,
                tech_node_id,
                'mentions',
                weight=0.5
            )
        
        # 提取概念
        concepts = self._extract_concepts(content)
        for concept in concepts:
            # 创建概念节点
            concept_node_id = self.add_node(
                concept,
                'concept',
                f"概念: {concept}"
            )
            
            # 添加关联
            self.add_edge(
                file_node_id,
                concept_node_id,
                'discusses',
                weight=0.5
            )
    
    def _process_python_file(self, file_path):
        """处理Python文件
        
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件失败: {file_path}, {str(e)}")
            return
        
        # 提取文件信息
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        
        # 创建文件节点
        file_node_id = self.add_node(
            file_name,
            'resource',
            f"代码文件: {file_path}",
            {'path': file_path, 'type': 'python'}
        )
        
        # 提取技术术语
        tech_terms = self._extract_tech_terms(content)
        for term in tech_terms:
            # 创建技术节点
            tech_node_id = self.add_node(
                term,
                'tech',
                f"技术术语: {term}"
            )
            
            # 添加关联
            self.add_edge(
                file_node_id,
                tech_node_id,
                'uses',
                weight=0.8
            )
        
        # 提取函数和类
        functions = self._extract_functions(content)
        for func in functions:
            # 创建模式节点
            pattern_node_id = self.add_node(
                func,
                'pattern',
                f"函数: {func}"
            )
            
            # 添加关联
            self.add_edge(
                file_node_id,
                pattern_node_id,
                'defines',
                weight=1.0
            )
    
    def _extract_tech_terms(self, content):
        """提取技术术语
        
        Args:
            content: 文本内容
            
        Returns:
            terms: 技术术语列表
        """
        # 常见技术术语列表
        tech_terms_list = [
            'React', 'Vue', 'Angular', 'Svelte', 'Solid.js',
            'Node.js', 'Express', 'Nest.js', 'Python', 'FastAPI', 'Django', 'Flask',
            'Go', 'Java', 'Spring', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'CI/CD',
            'React Native', 'Flutter', 'Unity', 'Unreal Engine', 'Three.js',
            'JWT', 'OAuth', 'GraphQL', 'REST', 'WebSocket',
            'TensorFlow', 'PyTorch', 'scikit-learn', 'Machine Learning', 'AI',
            'HTML', 'CSS', 'JavaScript', 'TypeScript', 'Python', 'Go', 'Java'
        ]
        
        terms = []
        content_lower = content.lower()
        
        for term in tech_terms_list:
            term_lower = term.lower()
            if term_lower in content_lower:
                terms.append(term)
        
        return list(set(terms))
    
    def _extract_concepts(self, content):
        """提取概念
        
        Args:
            content: 文本内容
            
        Returns:
            concepts: 概念列表
        """
        # 常见概念列表
        concepts_list = [
            '组件化', '状态管理', '路由', '中间件', 'API',
            '微服务', '单体应用', '服务器less', '缓存', '负载均衡',
            '数据库设计', '索引', '事务', '并发', '异步',
            '安全', '认证', '授权', '加密', 'API设计',
            '性能优化', '代码质量', '测试', '部署', '监控',
            '前端', '后端', '全栈', '移动端', '游戏开发'
        ]
        
        concepts = []
        content_lower = content.lower()
        
        for concept in concepts_list:
            concept_lower = concept.lower()
            if concept_lower in content_lower:
                concepts.append(concept)
        
        return list(set(concepts))
    
    def _extract_functions(self, content):
        """提取函数
        
        Args:
            content: 文本内容
            
        Returns:
            functions: 函数列表
        """
        # 提取函数定义
        function_pattern = r'def\s+(\w+)\s*\('
        functions = re.findall(function_pattern, content)
        
        # 提取类定义
        class_pattern = r'class\s+(\w+)\s*\('
        classes = re.findall(class_pattern, content)
        
        return functions + classes
    
    def search_nodes(self, query, type=None):
        """搜索节点
        
        Args:
            query: 搜索关键词
            type: 节点类型
            
        Returns:
            results: 搜索结果
        """
        results = []
        query_lower = query.lower()
        
        for node in self.graph_data['nodes']:
            if (query_lower in node['name'].lower() or 
                (node['description'] and query_lower in node['description'].lower())):
                if type is None or node['type'] == type:
                    results.append(node)
        
        return results
    
    def get_related_nodes(self, node_id, max_depth=2):
        """获取相关节点
        
        Args:
            node_id: 节点ID
            max_depth: 最大深度
            
        Returns:
            related_nodes: 相关节点
        """
        related = {}
        visited = set()
        
        def dfs(current_id, depth):
            if depth > max_depth or current_id in visited:
                return
            
            visited.add(current_id)
            
            # 查找相关边
            for edge in self.graph_data['edges']:
                if edge['source'] == current_id:
                    target_id = edge['target']
                    if target_id not in related:
                        # 查找目标节点
                        for node in self.graph_data['nodes']:
                            if node['id'] == target_id:
                                related[target_id] = {
                                    'node': node,
                                    'relationship': edge['relationship'],
                                    'weight': edge['weight']
                                }
                                break
                    dfs(target_id, depth + 1)
                elif edge['target'] == current_id:
                    source_id = edge['source']
                    if source_id not in related:
                        # 查找源节点
                        for node in self.graph_data['nodes']:
                            if node['id'] == source_id:
                                related[source_id] = {
                                    'node': node,
                                    'relationship': f"reverse_{edge['relationship']}",
                                    'weight': edge['weight']
                                }
                                break
                    dfs(source_id, depth + 1)
        
        dfs(node_id, 0)
        return related
    
    def recommend_tech(self, project_description):
        """推荐技术
        
        Args:
            project_description: 项目描述
            
        Returns:
            recommendations: 推荐结果
        """
        # 提取项目中的技术需求
        terms = self._extract_tech_terms(project_description)
        concepts = self._extract_concepts(project_description)
        
        # 计算技术相关度
        tech_scores = defaultdict(float)
        
        for term in terms:
            # 查找相关技术
            nodes = self.search_nodes(term, 'tech')
            for node in nodes:
                tech_scores[node['id']] += 1.0
                
                # 查找相关节点
                related = self.get_related_nodes(node['id'], max_depth=1)
                for related_id, info in related.items():
                    if info['node']['type'] == 'tech':
                        tech_scores[related_id] += info['weight'] * 0.5
        
        for concept in concepts:
            # 查找相关概念
            nodes = self.search_nodes(concept, 'concept')
            for node in nodes:
                # 查找相关技术
                related = self.get_related_nodes(node['id'], max_depth=2)
                for related_id, info in related.items():
                    if info['node']['type'] == 'tech':
                        tech_scores[related_id] += info['weight'] * 0.3
        
        # 排序技术
        sorted_tech = sorted(tech_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 生成推荐
        recommendations = []
        for tech_id, score in sorted_tech[:10]:
            # 查找技术节点
            for node in self.graph_data['nodes']:
                if node['id'] == tech_id:
                    recommendations.append({
                        'tech': node['name'],
                        'score': score,
                        'description': node['description']
                    })
                    break
        
        return recommendations
    
    def save_graph(self, file_path):
        """保存图谱
        
        Args:
            file_path: 保存路径
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.graph_data, f, ensure_ascii=False, indent=2)
            print(f"图谱保存成功: {file_path}")
        except Exception as e:
            print(f"保存图谱失败: {str(e)}")
    
    def load_graph(self, file_path):
        """加载图谱
        
        Args:
            file_path: 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.graph_data = json.load(f)
            
            # 重建known_nodes映射
            self.known_nodes = {}
            for node in self.graph_data['nodes']:
                node_key = f"{node['type']}:{node['name'].lower()}"
                self.known_nodes[node_key] = node['id']
            
            # 更新ID计数器
            if self.graph_data['nodes']:
                self.node_id_counter = max(node['id'] for node in self.graph_data['nodes']) + 1
            else:
                self.node_id_counter = 1
            
            if self.graph_data['edges']:
                self.edge_id_counter = max(edge['id'] for edge in self.graph_data['edges']) + 1
            else:
                self.edge_id_counter = 1
            
            print(f"图谱加载成功: {file_path}")
        except Exception as e:
            print(f"加载图谱失败: {str(e)}")
    
    def export_graphml(self, file_path):
        """导出为GraphML格式
        
        Args:
            file_path: 保存路径
        """
        try:
            graphml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
         http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
  <key id="name" for="node" attr.name="name" attr.type="string"/>
  <key id="type" for="node" attr.name="type" attr.type="string"/>
  <key id="description" for="node" attr.name="description" attr.type="string"/>
  <key id="relationship" for="edge" attr.name="relationship" attr.type="string"/>
  <key id="weight" for="edge" attr.name="weight" attr.type="float"/>
  <graph id="G" edgedefault="directed">
'''
            
            # 添加节点
            for node in self.graph_data['nodes']:
                graphml_content += f'    <node id="n{node["id"]}">\n'
                graphml_content += f'      <data key="name">{node["name"]}</data>\n'
                graphml_content += f'      <data key="type">{node["type"]}</data>\n'
                if node['description']:
                    graphml_content += f'      <data key="description">{node["description"]}</data>\n'
                graphml_content += '    </node>\n'
            
            # 添加边
            for edge in self.graph_data['edges']:
                graphml_content += f'    <edge id="e{edge["id"]}" source="n{edge["source"]}" target="n{edge["target"]}">\n'
                graphml_content += f'      <data key="relationship">{edge["relationship"]}</data>\n'
                graphml_content += f'      <data key="weight">{edge["weight"]}</data>\n'
                graphml_content += '    </edge>\n'
            
            graphml_content += '''  </graph>
</graphml>
'''
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(graphml_content)
            
            print(f"图谱导出为GraphML成功: {file_path}")
        except Exception as e:
            print(f"导出GraphML失败: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python knowledge_graph.py build <知识库路径> [输出文件]")
        print("  python knowledge_graph.py search <关键词> [类型]")
        print("  python knowledge_graph.py recommend <项目描述>")
        print("  python knowledge_graph.py export <图谱文件> <输出文件>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'build':
        if len(sys.argv) < 3:
            print("参数不足: python knowledge_graph.py build <知识库路径> [输出文件]")
            sys.exit(1)
        
        knowledge_base_path = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else 'knowledge_graph.json'
        
        graph = KnowledgeGraph()
        graph.build_from_knowledge_base(knowledge_base_path)
        graph.save_graph(output_file)
        
        # 导出为GraphML
        graphml_file = output_file.replace('.json', '.graphml')
        graph.export_graphml(graphml_file)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("参数不足: python knowledge_graph.py search <关键词> [类型]")
            sys.exit(1)
        
        query = sys.argv[2]
        type = sys.argv[3] if len(sys.argv) > 3 else None
        
        graph = KnowledgeGraph()
        graph.load_graph('knowledge_graph.json')
        
        results = graph.search_nodes(query, type)
        print(f"搜索 '{query}' 结果: {len(results)} 个节点")
        for node in results:
            print(f"ID: {node['id']}, 名称: {node['name']}, 类型: {node['type']}")
            if node['description']:
                print(f"  描述: {node['description']}")
    
    elif command == 'recommend':
        if len(sys.argv) < 3:
            print("参数不足: python knowledge_graph.py recommend <项目描述>")
            sys.exit(1)
        
        project_description = ' '.join(sys.argv[2:])
        
        graph = KnowledgeGraph()
        graph.load_graph('knowledge_graph.json')
        
        recommendations = graph.recommend_tech(project_description)
        print(f"技术推荐结果: {len(recommendations)} 个技术")
        for rec in recommendations[:5]:
            print(f"{rec['tech']} (得分: {rec['score']:.2f})")
            if rec['description']:
                print(f"  描述: {rec['description']}")
    
    elif command == 'export':
        if len(sys.argv) < 4:
            print("参数不足: python knowledge_graph.py export <图谱文件> <输出文件>")
            sys.exit(1)
        
        graph_file = sys.argv[2]
        output_file = sys.argv[3]
        
        graph = KnowledgeGraph()
        graph.load_graph(graph_file)
        graph.export_graphml(output_file)
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
