#!/usr/bin/env python3
"""
文本生成模块
负责处理自然语言生成任务
"""

import os
import json
import logging
from datetime import datetime
from .model_manager import ModelManager

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TextGenerator:
    def __init__(self):
        self.model_manager = ModelManager()
        self.templates = {
            'prd_summary': '''
请对以下PRD文档进行总结，提取关键信息：

{prd_content}

总结应该包括：
1. 项目概述
2. 核心功能
3. 技术栈
4. 目标用户
5. 成功指标
''',
            'tech_recommendation': '''
请根据以下项目需求，推荐合适的技术栈：

项目需求：{project_requirements}

推荐应该包括：
1. 前端技术
2. 后端技术
3. 数据库
4. 部署方案
5. 推荐理由
''',
            'code_explanation': '''
请解释以下代码的功能和实现原理：

{code}

解释应该包括：
1. 代码的整体功能
2. 关键部分的详细说明
3. 可能的优化建议
''',
            'bug_analysis': '''
请分析以下代码中可能存在的bug：

{code}

分析应该包括：
1. 可能的bug
2. 问题原因
3. 修复建议
''',
            'documentation': '''
请为以下功能编写文档：

功能描述：{feature_description}

文档应该包括：
1. 功能概述
2. 使用方法
3. 参数说明
4. 示例代码
5. 注意事项
'''
        }
    
    def generate(self, prompt, model_name='default', max_tokens=1000):
        """生成文本
        
        Args:
            prompt: 提示词
            model_name: 模型名称
            max_tokens: 最大 token 数
            
        Returns:
            result: 生成结果
        """
        return self.model_manager.generate(prompt, model_name, max_tokens)
    
    def generate_from_template(self, template_name, template_vars, model_name='default', max_tokens=1000):
        """使用模板生成文本
        
        Args:
            template_name: 模板名称
            template_vars: 模板变量
            model_name: 模型名称
            max_tokens: 最大 token 数
            
        Returns:
            result: 生成结果
        """
        if template_name not in self.templates:
            logger.error(f"模板不存在: {template_name}")
            return "模板不存在"
        
        try:
            # 填充模板
            prompt = self.templates[template_name].format(**template_vars)
            # 生成文本
            result = self.generate(prompt, model_name, max_tokens)
            return result
        except Exception as e:
            logger.error(f"生成失败: {str(e)}")
            return f"生成失败: {str(e)}"
    
    def summarize_prd(self, prd_content, model_name='default'):
        """总结PRD文档
        
        Args:
            prd_content: PRD内容
            model_name: 模型名称
            
        Returns:
            summary: PRD总结
        """
        return self.generate_from_template(
            'prd_summary',
            {'prd_content': prd_content},
            model_name
        )
    
    def recommend_tech(self, project_requirements, model_name='default'):
        """推荐技术栈
        
        Args:
            project_requirements: 项目需求
            model_name: 模型名称
            
        Returns:
            recommendation: 技术栈推荐
        """
        return self.generate_from_template(
            'tech_recommendation',
            {'project_requirements': project_requirements},
            model_name
        )
    
    def explain_code(self, code, model_name='default'):
        """解释代码
        
        Args:
            code: 代码内容
            model_name: 模型名称
            
        Returns:
            explanation: 代码解释
        """
        return self.generate_from_template(
            'code_explanation',
            {'code': code},
            model_name
        )
    
    def analyze_bug(self, code, model_name='default'):
        """分析代码中的bug
        
        Args:
            code: 代码内容
            model_name: 模型名称
            
        Returns:
            analysis: bug分析
        """
        return self.generate_from_template(
            'bug_analysis',
            {'code': code},
            model_name
        )
    
    def generate_documentation(self, feature_description, model_name='default'):
        """生成文档
        
        Args:
            feature_description: 功能描述
            model_name: 模型名称
            
        Returns:
            documentation: 生成的文档
        """
        return self.generate_from_template(
            'documentation',
            {'feature_description': feature_description},
            model_name
        )
    
    def add_template(self, template_name, template_content):
        """添加模板
        
        Args:
            template_name: 模板名称
            template_content: 模板内容
        """
        self.templates[template_name] = template_content
        logger.info(f"添加模板成功: {template_name}")
    
    def remove_template(self, template_name):
        """删除模板
        
        Args:
            template_name: 模板名称
        """
        if template_name in self.templates:
            del self.templates[template_name]
            logger.info(f"删除模板成功: {template_name}")
        else:
            logger.warning(f"模板不存在: {template_name}")
    
    def list_templates(self):
        """列出所有模板
        
        Returns:
            template_list: 模板列表
        """
        return list(self.templates.keys())
    
    def get_template(self, template_name):
        """获取模板
        
        Args:
            template_name: 模板名称
            
        Returns:
            template: 模板内容
        """
        return self.templates.get(template_name, None)

if __name__ == "__main__":
    # 测试文本生成器
    generator = TextGenerator()
    
    # 测试基本生成
    print("测试基本生成:")
    result = generator.generate("写一个Hello World程序")
    print(result)
    print()
    
    # 测试模板生成
    print("测试PRD总结:")
    test_prd = "# 测试项目 PRD\n\n## 1. 项目概述\n这是一个测试项目，用于演示PRD总结功能。\n\n## 2. 核心功能\n- 功能1: 测试功能\n- 功能2: 演示功能\n\n## 3. 技术栈\n- 前端: React\n- 后端: Node.js\n- 数据库: MongoDB\n\n## 4. 目标用户\n开发人员和测试人员\n\n## 5. 成功指标\n- 功能完整性\n- 用户满意度\n"
    result = generator.summarize_prd(test_prd)
    print(result)
    print()
    
    # 测试技术推荐
    print("测试技术推荐:")
    test_requirements = "一个电商平台，需要高性能、可扩展性和安全性"
    result = generator.recommend_tech(test_requirements)
    print(result)
    print()
    
    # 测试代码解释
    print("测试代码解释:")
    test_code = "def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)"
    result = generator.explain_code(test_code)
    print(result)
