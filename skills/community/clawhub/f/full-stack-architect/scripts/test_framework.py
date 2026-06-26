#!/usr/bin/env python3
"""
自动化测试框架
用于测试全栈架构导师的各项功能
"""

import os
import sys
import json
import unittest
import tempfile
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入被测试的模块
from prd_generator_enhanced import PRDGenerator
from tech_stack_recommender import TechStackRecommender
from knowledge_graph import KnowledgeGraph
from pattern_manager import PatternManager
from prd_linter import PRDLinter

class TestPRDGenerator(unittest.TestCase):
    """测试PRD生成器"""
    
    def setUp(self):
        """设置测试环境"""
        self.generator = PRDGenerator()
    
    def test_generate_prd(self):
        """测试生成PRD"""
        project_name = "测试项目"
        project_description = "一个简单的测试项目"
        industry = "ecommerce"
        
        # 生成PRD
        prd_file_path = self.generator.generate_prd(project_name, project_description, industry)
        
        # 验证文件存在
        self.assertTrue(os.path.exists(prd_file_path))
        
        # 验证文件内容
        with open(prd_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证包含必要的部分
        self.assertIn("# 测试项目 电商平台产品需求文档", content)
        self.assertIn("## 1. 项目概述", content)
        self.assertIn("## 2. 技术栈", content)
        self.assertIn("## 3. 用户故事", content)
        self.assertIn("## 4. 非目标", content)
        self.assertIn("## 5. 成功指标", content)
    
    def test_generate_json(self):
        """测试生成JSON格式"""
        project_name = "测试项目"
        project_description = "一个简单的测试项目"
        industry = "ecommerce"
        
        # 生成PRD
        prd_file_path = self.generator.generate_prd(project_name, project_description, industry)
        
        # 找到对应的JSON文件
        json_file_path = prd_file_path.replace('.md', '.json')
        
        # 验证文件存在
        self.assertTrue(os.path.exists(json_file_path))
        
        # 验证JSON内容
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 验证包含必要的字段
        self.assertEqual(data['project_name'], project_name)
        self.assertIn('generated_at', data)
        self.assertIn('sections', data)
        self.assertIn('overview', data['sections'])
        self.assertIn('tech_stack', data['sections'])
        self.assertIn('user_stories', data['sections'])
        self.assertIn('non_goals', data['sections'])
        self.assertIn('success_metrics', data['sections'])

class TestTechStackRecommender(unittest.TestCase):
    """测试技术栈推荐器"""
    
    def setUp(self):
        """设置测试环境"""
        self.recommender = TechStackRecommender()
    
    def test_analyze_project(self):
        """测试项目分析"""
        project_description = "一个电商平台，需要高性能和可扩展性"
        analysis = self.recommender.analyze_project(project_description)
        
        # 验证分析结果
        self.assertEqual(analysis['project_type'], 'ecommerce')
        self.assertIn('performance', analysis['requirements'])
        self.assertIn('scalability', analysis['requirements'])
    
    def test_recommend(self):
        """测试技术栈推荐"""
        project_description = "一个电商平台，需要高性能和可扩展性"
        recommendation = self.recommender.recommend(project_description)
        
        # 验证推荐结果
        self.assertIn('analysis', recommendation)
        self.assertIn('recommendations', recommendation)
        self.assertIn('frontend', recommendation['recommendations'])
        self.assertIn('backend', recommendation['recommendations'])
        self.assertIn('database', recommendation['recommendations'])
        self.assertIn('justification', recommendation)
        self.assertIn('timestamp', recommendation)
        
        # 验证推荐列表不为空
        self.assertTrue(len(recommendation['recommendations']['frontend']) > 0)
        self.assertTrue(len(recommendation['recommendations']['backend']) > 0)
        self.assertTrue(len(recommendation['recommendations']['database']) > 0)

class TestKnowledgeGraph(unittest.TestCase):
    """测试知识图谱"""
    
    def setUp(self):
        """设置测试环境"""
        self.graph = KnowledgeGraph()
        # 创建临时文件用于测试
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """清理测试环境"""
        # 清理临时文件
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_add_node(self):
        """测试添加节点"""
        node_id = self.graph.add_node('React', 'tech', 'React 是一个前端库')
        self.assertIsInstance(node_id, int)
        self.assertEqual(node_id, 1)
        
        # 测试重复节点
        node_id2 = self.graph.add_node('React', 'tech')
        self.assertEqual(node_id2, node_id)
    
    def test_add_edge(self):
        """测试添加边"""
        node1_id = self.graph.add_node('React', 'tech')
        node2_id = self.graph.add_node('组件化', 'concept')
        
        edge_id = self.graph.add_edge(node1_id, node2_id, 'supports', weight=0.8)
        self.assertIsInstance(edge_id, int)
        self.assertEqual(edge_id, 1)
        
        # 测试重复边（应该更新权重）
        edge_id2 = self.graph.add_edge(node1_id, node2_id, 'supports', weight=0.2)
        self.assertEqual(edge_id2, edge_id)
    
    def test_build_from_knowledge_base(self):
        """测试从知识库构建图谱"""
        # 创建测试文件
        test_file = os.path.join(self.temp_dir, 'test.md')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('# 测试文件\n\nReact 是一个前端库，支持组件化开发。')
        
        # 构建图谱
        self.graph.build_from_knowledge_base(self.temp_dir)
        
        # 验证节点和边的数量
        self.assertTrue(len(self.graph.graph_data['nodes']) > 0)
        self.assertTrue(len(self.graph.graph_data['edges']) > 0)

class TestPatternManager(unittest.TestCase):
    """测试模式管理器"""
    
    def setUp(self):
        """设置测试环境"""
        self.manager = PatternManager()
    
    def test_add_pattern(self):
        """测试添加模式"""
        pattern_id = self.manager.add_pattern(
            'JWT认证',
            '后端认证',
            '使用JWT进行无状态认证',
            'const token = jwt.sign({ userId: user.id }, secret);',
            ['认证', 'JWT']
        )
        
        self.assertIsInstance(pattern_id, int)
        self.assertGreater(pattern_id, 0)
    
    def test_get_patterns(self):
        """测试获取模式列表"""
        # 添加模式
        self.manager.add_pattern(
            'JWT认证',
            '后端认证',
            '使用JWT进行无状态认证',
            'const token = jwt.sign({ userId: user.id }, secret);'
        )
        
        # 获取模式列表
        patterns = self.manager.get_patterns()
        self.assertTrue(len(patterns) > 0)
        self.assertEqual(patterns[0]['name'], 'JWT认证')
    
    def test_search_patterns(self):
        """测试搜索模式"""
        # 添加模式
        self.manager.add_pattern(
            'JWT认证',
            '后端认证',
            '使用JWT进行无状态认证',
            'const token = jwt.sign({ userId: user.id }, secret);',
            ['认证', 'JWT']
        )
        
        # 搜索模式
        results = self.manager.search_patterns('认证')
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['name'], 'JWT认证')

class TestPRDLinter(unittest.TestCase):
    """测试PRD linter"""
    
    def setUp(self):
        """设置测试环境"""
        self.linter = PRDLinter()
        # 创建测试PRD文件
        self.test_prd = """# 测试项目 产品需求文档

## 1. 项目概述
- 项目背景：测试PRD校验
- 项目目标：验证PRD格式
- 核心功能：测试功能
- 目标用户：测试用户

## 2. 技术栈
- 前端：React
- 后端：Node.js
- 数据库：MongoDB

## 3. 用户故事

### 3.1 故事1：测试功能
- **描述**：测试PRD校验功能
- **验收标准**：
  1. PRD格式正确
  2. 校验通过
- **依赖关系**：无
- **优先级**：高
- **类型**：fullstack

## 4. 非目标
- 生产部署

## 5. 成功指标
- 校验通过率100%
"""
    
    def test_lint_file(self):
        """测试PRD文件校验"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(self.test_prd)
            temp_file = f.name
        
        try:
            # 执行校验
            result = self.linter.lint_file(temp_file)
            self.assertTrue(result)
        finally:
            # 清理临时文件
            os.unlink(temp_file)

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_end_to_end(self):
        """测试端到端流程"""
        # 1. 生成PRD
        generator = PRDGenerator()
        project_name = "集成测试项目"
        project_description = "一个用于集成测试的项目"
        industry = "saas"
        
        prd_file_path = generator.generate_prd(project_name, project_description, industry)
        self.assertTrue(os.path.exists(prd_file_path))
        
        # 2. 校验PRD
        linter = PRDLinter()
        lint_result = linter.lint_file(prd_file_path)
        self.assertTrue(lint_result)
        
        # 3. 推荐技术栈
        recommender = TechStackRecommender()
        recommendation = recommender.recommend(project_description)
        self.assertTrue(len(recommendation['recommendations']['frontend']) > 0)
        
        # 4. 添加模式
        manager = PatternManager()
        pattern_id = manager.add_pattern(
            '集成测试模式',
            '测试',
            '用于集成测试的模式',
            'def test_integration():\n    pass'
        )
        self.assertIsInstance(pattern_id, int)

def run_tests():
    """运行所有测试"""
    print("开始运行测试...")
    
    # 创建测试套件
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestPRDGenerator))
    suite.addTest(loader.loadTestsFromTestCase(TestTechStackRecommender))
    suite.addTest(loader.loadTestsFromTestCase(TestKnowledgeGraph))
    suite.addTest(loader.loadTestsFromTestCase(TestPatternManager))
    suite.addTest(loader.loadTestsFromTestCase(TestPRDLinter))
    suite.addTest(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 生成测试报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'passed': result.testsRun - len(result.failures) - len(result.errors),
        'success': result.wasSuccessful()
    }
    
    # 保存测试报告
    report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试报告已保存到: {report_file}")
    print(f"测试结果: {report['passed']} 个通过, {report['failures']} 个失败, {report['errors']} 个错误")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
