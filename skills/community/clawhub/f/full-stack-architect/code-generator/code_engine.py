#!/usr/bin/env python3
"""
代码生成引擎
负责生成高质量的代码
"""

import os
import json
import logging
from datetime import datetime
from ..ai_models.code_generation import CodeGenerator

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeEngine:
    def __init__(self):
        self.code_generator = CodeGenerator()
        self.templates_dir = os.path.join(os.path.dirname(__file__), 'language_templates')
        self.config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info("加载配置成功")
            except Exception as e:
                logger.error(f"加载配置失败: {str(e)}")
                self.config = {}
        else:
            # 默认配置
            self.config = {
                'default_language': 'python',
                'code_quality_check': True,
                'template_dir': self.templates_dir
            }
            self._save_config()
    
    def _save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info("配置保存成功")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def generate_code(self, task_description, language=None, model_name='default'):
        """生成代码
        
        Args:
            task_description: 任务描述
            language: 编程语言
            model_name: 模型名称
            
        Returns:
            code: 生成的代码
        """
        if not language:
            language = self.config.get('default_language', 'python')
        
        try:
            # 分析任务类型
            task_type = self._analyze_task_type(task_description)
            
            # 根据任务类型生成代码
            if task_type == 'function':
                code = self.code_generator.generate_function(language, task_description, model_name)
            elif task_type == 'class':
                code = self.code_generator.generate_class(language, task_description, model_name)
            elif task_type == 'module':
                code = self.code_generator.generate_module(language, task_description, model_name)
            elif task_type == 'algorithm':
                code = self.code_generator.generate_algorithm(language, task_description, model_name)
            else:
                # 默认为函数
                code = self.code_generator.generate_function(language, task_description, model_name)
            
            # 代码质量检查
            if self.config.get('code_quality_check', True):
                quality_result = self.check_code_quality(code, language)
                if not quality_result['success']:
                    logger.warning(f"代码质量检查失败: {quality_result['message']}")
            
            logger.info(f"生成代码成功，语言: {language}, 任务类型: {task_type}")
            return code
        except Exception as e:
            logger.error(f"生成代码失败: {str(e)}")
            return f"生成代码失败: {str(e)}"
    
    def _analyze_task_type(self, task_description):
        """分析任务类型
        
        Args:
            task_description: 任务描述
            
        Returns:
            task_type: 任务类型
        """
        task_description_lower = task_description.lower()
        
        if any(keyword in task_description_lower for keyword in ['函数', '方法', 'function', 'method']):
            return 'function'
        elif any(keyword in task_description_lower for keyword in ['类', 'class']):
            return 'class'
        elif any(keyword in task_description_lower for keyword in ['模块', '包', 'module', 'package']):
            return 'module'
        elif any(keyword in task_description_lower for keyword in ['算法', 'algorithm']):
            return 'algorithm'
        else:
            return 'function'
    
    def check_code_quality(self, code, language):
        """检查代码质量
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            result: 检查结果
        """
        # 简单的代码质量检查
        result = {
            'success': True,
            'message': '代码质量检查通过',
            'issues': []
        }
        
        # 检查代码长度
        if len(code) < 10:
            result['success'] = False
            result['message'] = '代码太短'
            result['issues'].append('代码长度不足')
        
        # 检查注释
        if '#' not in code and '//' not in code and '/*' not in code:
            result['issues'].append('缺少注释')
        
        # 检查语法（简单检查）
        if language == 'python':
            if 'def ' not in code and 'class ' not in code:
                result['issues'].append('可能缺少函数或类定义')
        elif language == 'javascript':
            if 'function ' not in code and '=>' not in code:
                result['issues'].append('可能缺少函数定义')
        
        if result['issues']:
            result['message'] = f'发现 {len(result["issues"])} 个问题'
        
        return result
    
    def generate_from_template(self, template_name, language, template_vars):
        """从模板生成代码
        
        Args:
            template_name: 模板名称
            language: 编程语言
            template_vars: 模板变量
            
        Returns:
            code: 生成的代码
        """
        try:
            # 加载模板
            template_path = os.path.join(self.templates_dir, f"{language}_{template_name}.txt")
            if not os.path.exists(template_path):
                # 使用内置模板
                return self.code_generator.generate_from_language_template(language, template_name)
            
            # 读取模板文件
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # 填充模板
            code = template_content.format(**template_vars)
            
            logger.info(f"从模板生成代码成功: {template_name}")
            return code
        except Exception as e:
            logger.error(f"从模板生成代码失败: {str(e)}")
            return f"从模板生成代码失败: {str(e)}"
    
    def save_code(self, code, file_path):
        """保存代码到文件
        
        Args:
            code: 代码内容
            file_path: 文件路径
            
        Returns:
            success: 是否成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            logger.info(f"保存代码成功: {file_path}")
            return True
        except Exception as e:
            logger.error(f"保存代码失败: {str(e)}")
            return False
    
    def list_supported_languages(self):
        """列出支持的语言
        
        Returns:
            languages: 语言列表
        """
        return self.code_generator.list_supported_languages()
    
    def list_templates(self, language=None):
        """列出可用模板
        
        Args:
            language: 编程语言
            
        Returns:
            templates: 模板列表
        """
        return self.code_generator.list_language_templates(language)
    
    def update_config(self, config_updates):
        """更新配置
        
        Args:
            config_updates: 配置更新
        """
        self.config.update(config_updates)
        self._save_config()
        logger.info("更新配置成功")

if __name__ == "__main__":
    # 测试代码生成引擎
    engine = CodeEngine()
    
    # 测试生成函数
    print("测试生成函数:")
    code = engine.generate_code('计算阶乘', 'python')
    print(code)
    print()
    
    # 测试生成类
    print("测试生成类:")
    code = engine.generate_code('学生类，包含姓名、年龄和成绩属性，以及计算平均成绩的方法', 'python')
    print(code)
    print()
    
    # 测试生成模块
    print("测试生成模块:")
    code = engine.generate_code('数学工具模块，包含常用的数学函数如求和、平均值、标准差等', 'python')
    print(code)
    print()
    
    # 测试生成算法
    print("测试生成算法:")
    code = engine.generate_code('二分查找算法，在有序数组中查找目标值', 'python')
    print(code)
    print()
    
    # 测试从模板生成
    print("测试从模板生成:")
    code = engine.generate_from_template('hello_world', 'python', {})
    print(code)
    print()
    
    # 测试保存代码
    print("测试保存代码:")
    success = engine.save_code(code, 'test_hello_world.py')
    print(f"保存成功: {success}")
