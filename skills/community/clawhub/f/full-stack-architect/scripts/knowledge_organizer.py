#!/usr/bin/env python3
"""
知识整理脚本
用于管理和维护全栈架构导师的知识库
"""

import os
import json
import re
from datetime import datetime

class KnowledgeOrganizer:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.references_dir = os.path.join(base_dir, 'references')
        self.code_snippets_dir = os.path.join(base_dir, 'code_snippets')
        self.project_examples_dir = os.path.join(base_dir, 'project_examples')
        self.scripts_dir = os.path.join(base_dir, 'scripts')
        
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保所有必要的目录存在"""
        for directory in [
            self.references_dir,
            self.code_snippets_dir,
            self.project_examples_dir,
            self.scripts_dir
        ]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"创建目录: {directory}")
    
    def scan_knowledge_base(self):
        """扫描知识库并生成索引"""
        index = {
            'timestamp': datetime.now().isoformat(),
            'references': [],
            'code_snippets': [],
            'project_examples': []
        }
        
        # 扫描参考文档
        for filename in os.listdir(self.references_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(self.references_dir, filename)
                index['references'].append({
                    'filename': filename,
                    'path': file_path,
                    'last_modified': os.path.getmtime(file_path)
                })
        
        # 扫描代码片段
        for filename in os.listdir(self.code_snippets_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(self.code_snippets_dir, filename)
                index['code_snippets'].append({
                    'filename': filename,
                    'path': file_path,
                    'last_modified': os.path.getmtime(file_path)
                })
        
        # 扫描项目示例
        for filename in os.listdir(self.project_examples_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(self.project_examples_dir, filename)
                index['project_examples'].append({
                    'filename': filename,
                    'path': file_path,
                    'last_modified': os.path.getmtime(file_path)
                })
        
        # 保存索引
        index_path = os.path.join(self.base_dir, 'knowledge_index.json')
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        
        print(f"知识库索引已更新: {index_path}")
        print(f"参考文档: {len(index['references'])}")
        print(f"代码片段: {len(index['code_snippets'])}")
        print(f"项目示例: {len(index['project_examples'])}")
        
        return index
    
    def analyze_knowledge_gaps(self):
        """分析知识 gaps"""
        index = self.scan_knowledge_base()
        
        # 预期的知识领域
        expected_references = [
            'knowledge_system.md',
            'frontend_best_practices.md',
            'composition_patterns.md',
            'vue_best_practices.md',
            'nodejs_best_practices.md',
            'database_best_practices.md',
            'cloud_native_devops.md',
            'mobile_development.md',
            'game_development.md',
            'security_best_practices.md',
            'frontend_frameworks.md',
            'backend_frameworks.md',
            'ai_machine_learning.md'
        ]
        
        # 检查缺失的参考文档
        existing_references = [item['filename'] for item in index['references']]
        missing_references = [ref for ref in expected_references if ref not in existing_references]
        
        if missing_references:
            print("\n=== 知识缺口 ===")
            print("缺失的参考文档:")
            for ref in missing_references:
                print(f"- {ref}")
        else:
            print("\n=== 知识状态 ===")
            print("所有预期的参考文档都已存在")
        
        return missing_references
    
    def update_skill_file(self):
        """更新SKILL.md文件中的知识图谱"""
        skill_file = os.path.join(self.base_dir, 'SKILL.md')
        if not os.path.exists(skill_file):
            print(f"SKILL.md文件不存在: {skill_file}")
            return
        
        # 读取当前内容
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 扫描知识库
        index = self.scan_knowledge_base()
        
        # 提取现有文档
        references = [item['filename'] for item in index['references']]
        
        # 构建知识图谱
        knowledge_graph = []
        for ref in references:
            if ref == 'knowledge_system.md':
                knowledge_graph.append("- ✅ 知识体系总览")
            elif ref == 'frontend_best_practices.md':
                knowledge_graph.append("- ✅ 前端最佳实践")
            elif ref == 'composition_patterns.md':
                knowledge_graph.append("- ✅ React组合模式")
            elif ref == 'vue_best_practices.md':
                knowledge_graph.append("- ✅ Vue.js最佳实践")
            elif ref == 'nodejs_best_practices.md':
                knowledge_graph.append("- ✅ Node.js后端开发")
            elif ref == 'database_best_practices.md':
                knowledge_graph.append("- ✅ 数据库最佳实践")
            elif ref == 'cloud_native_devops.md':
                knowledge_graph.append("- ✅ 云原生与DevOps")
            elif ref == 'mobile_development.md':
                knowledge_graph.append("- ✅ 移动开发")
            elif ref == 'game_development.md':
                knowledge_graph.append("- ✅ 游戏开发")
            elif ref == 'security_best_practices.md':
                knowledge_graph.append("- ✅ 安全最佳实践")
            elif ref == 'frontend_frameworks.md':
                knowledge_graph.append("- ✅ 前端框架")
            elif ref == 'backend_frameworks.md':
                knowledge_graph.append("- ✅ 后端框架")
            elif ref == 'ai_machine_learning.md':
                knowledge_graph.append("- ✅ 人工智能与机器学习")
            else:
                knowledge_graph.append(f"- ✅ {ref.replace('.md', '')}")
        
        # 替换知识图谱部分
        knowledge_graph_str = '\n'.join(knowledge_graph)
        new_content = re.sub(
            r'## 知识图谱（持续扩展中）\n\n(.+?)\n\n---',
            f'## 知识图谱（持续扩展中）\n\n{knowledge_graph_str}\n\n---',
            content, 
            flags=re.DOTALL
        )
        
        # 写回文件
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"SKILL.md文件已更新")
    
    def run_full_analysis(self):
        """运行完整分析"""
        print("\n=== 全栈架构导师知识库分析 ===")
        print(f"知识库基础目录: {self.base_dir}")
        
        # 扫描知识库
        self.scan_knowledge_base()
        
        # 分析知识缺口
        self.analyze_knowledge_gaps()
        
        # 更新SKILL.md
        self.update_skill_file()
        
        print("\n=== 分析完成 ===")

if __name__ == "__main__":
    # 脚本所在目录的上级目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    organizer = KnowledgeOrganizer(base_dir)
    organizer.run_full_analysis()
