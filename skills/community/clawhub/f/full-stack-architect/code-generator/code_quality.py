#!/usr/bin/env python3
"""
代码质量检查模块
负责检查生成代码的质量
"""

import os
import json
import logging
import re
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeQualityChecker:
    def __init__(self):
        self.rules = {
            'python': {
                'naming_convention': {
                    'function': r'^[a-z_][a-z0-9_]*$',
                    'class': r'^[A-Z][a-zA-Z0-9]*$',
                    'variable': r'^[a-z_][a-z0-9_]*$',
                    'constant': r'^[A-Z_][A-Z0-9_]*$'
                },
                'code_structure': {
                    'max_line_length': 79,
                    'indentation': 4,
                    'blank_lines': {
                        'between_functions': 2,
                        'between_classes': 2,
                        'between_methods': 1
                    }
                },
                'best_practices': {
                    'docstrings': True,
                    'type_hints': True,
                    'error_handling': True,
                    'imports_order': True
                }
            },
            'javascript': {
                'naming_convention': {
                    'function': r'^[a-z][a-zA-Z0-9]*$',
                    'class': r'^[A-Z][a-zA-Z0-9]*$',
                    'variable': r'^[a-z][a-zA-Z0-9]*$',
                    'constant': r'^[A-Z_][A-Z0-9_]*$'
                },
                'code_structure': {
                    'max_line_length': 80,
                    'indentation': 2,
                    'blank_lines': {
                        'between_functions': 2,
                        'between_classes': 2,
                        'between_methods': 1
                    }
                },
                'best_practices': {
                    'comments': True,
                    'error_handling': True,
                    'const_let': True,
                    'arrow_functions': True
                }
            },
            'go': {
                'naming_convention': {
                    'function': r'^[A-Z][a-zA-Z0-9]*$',
                    'struct': r'^[A-Z][a-zA-Z0-9]*$',
                    'variable': r'^[a-z][a-zA-Z0-9]*$',
                    'constant': r'^[A-Z_][A-Z0-9_]*$'
                },
                'code_structure': {
                    'max_line_length': 80,
                    'indentation': 4,
                    'blank_lines': {
                        'between_functions': 1,
                        'between_structs': 1,
                        'between_methods': 1
                    }
                },
                'best_practices': {
                    'error_handling': True,
                    'doc_comments': True,
                    'imports_order': True,
                    'short_variable_names': True
                }
            },
            'java': {
                'naming_convention': {
                    'class': r'^[A-Z][a-zA-Z0-9]*$',
                    'method': r'^[a-z][a-zA-Z0-9]*$',
                    'variable': r'^[a-z][a-zA-Z0-9]*$',
                    'constant': r'^[A-Z_][A-Z0-9_]*$'
                },
                'code_structure': {
                    'max_line_length': 80,
                    'indentation': 4,
                    'blank_lines': {
                        'between_classes': 2,
                        'between_methods': 1,
                        'between_blocks': 1
                    }
                },
                'best_practices': {
                    'javadoc': True,
                    'error_handling': True,
                    'modifiers_order': True,
                    'imports_order': True
                }
            }
        }
        self.config_path = os.path.join(os.path.dirname(__file__), 'quality_config.json')
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if 'rules' in config:
                    self.rules = config['rules']
                logger.info("加载配置成功")
            except Exception as e:
                logger.error(f"加载配置失败: {str(e)}")
        else:
            self._save_config()

    def _save_config(self):
        try:
            config = {
                'rules': self.rules
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            logger.info("配置保存成功")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
    
    def check_code_quality(self, code, language):
        """检查代码质量
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            result: 检查结果
        """
        if language not in self.rules:
            logger.warning(f"不支持的语言: {language}")
            return {
                'success': False,
                'message': f"不支持的语言: {language}",
                'issues': []
            }
        
        rules = self.rules[language]
        issues = []
        
        # 检查命名规范
        naming_issues = self._check_naming_convention(code, language, rules['naming_convention'])
        issues.extend(naming_issues)
        
        # 检查代码结构
        structure_issues = self._check_code_structure(code, language, rules['code_structure'])
        issues.extend(structure_issues)
        
        # 检查最佳实践
        best_practices_issues = self._check_best_practices(code, language, rules['best_practices'])
        issues.extend(best_practices_issues)
        
        # 生成结果
        result = {
            'success': len(issues) == 0,
            'message': f'发现 {len(issues)} 个问题' if issues else '代码质量检查通过',
            'issues': issues
        }
        
        return result
    
    def _check_naming_convention(self, code, language, naming_rules):
        """检查命名规范
        
        Args:
            code: 代码内容
            language: 编程语言
            naming_rules: 命名规则
            
        Returns:
            issues: 问题列表
        """
        issues = []
        
        # 检查函数命名
        if 'function' in naming_rules:
            if language == 'python':
                function_pattern = r'def\s+(\w+)\s*\('
            elif language == 'javascript':
                function_pattern = r'function\s+(\w+)\s*\(' 
            elif language == 'go':
                function_pattern = r'func\s+(\w+)\s*\('
            elif language == 'java':
                function_pattern = r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\('
            else:
                function_pattern = r'function\s+(\w+)\s*\('
            
            functions = re.findall(function_pattern, code)
            for func in functions:
                if not re.match(naming_rules['function'], func):
                    issues.append(f"函数命名不符合规范: {func}")
        
        # 检查类命名
        if 'class' in naming_rules:
            if language == 'python' or language == 'javascript':
                class_pattern = r'class\s+(\w+)\s*\('
            elif language == 'go':
                class_pattern = r'type\s+(\w+)\s+struct'
            elif language == 'java':
                class_pattern = r'class\s+(\w+)'
            else:
                class_pattern = r'class\s+(\w+)'
            
            classes = re.findall(class_pattern, code)
            for cls in classes:
                if not re.match(naming_rules['class'], cls):
                    issues.append(f"类命名不符合规范: {cls}")
        
        return issues
    
    def _check_code_structure(self, code, language, structure_rules):
        """检查代码结构
        
        Args:
            code: 代码内容
            language: 编程语言
            structure_rules: 结构规则
            
        Returns:
            issues: 问题列表
        """
        issues = []
        lines = code.split('\n')
        
        # 检查行长度
        max_line_length = structure_rules.get('max_line_length', 80)
        for i, line in enumerate(lines, 1):
            if len(line) > max_line_length:
                issues.append(f"第 {i} 行长度超过 {max_line_length} 字符")
        
        # 检查缩进
        indentation = structure_rules.get('indentation', 4)
        for i, line in enumerate(lines, 1):
            if line.strip():
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces % indentation != 0:
                    issues.append(f"第 {i} 行缩进不符合规范")
        
        return issues
    
    def _check_best_practices(self, code, language, best_practices_rules):
        """检查最佳实践
        
        Args:
            code: 代码内容
            language: 编程语言
            best_practices_rules: 最佳实践规则
            
        Returns:
            issues: 问题列表
        """
        issues = []
        
        # 检查注释
        if best_practices_rules.get('docstrings', False) or best_practices_rules.get('comments', False):
            if '"""' not in code and '\'\'' not in code and '//' not in code and '/*' not in code:
                issues.append("缺少注释或文档字符串")
        
        # 检查错误处理
        if best_practices_rules.get('error_handling', False):
            if language == 'python':
                if 'try' not in code and 'except' not in code:
                    issues.append("缺少错误处理")
            elif language == 'javascript':
                if 'try' not in code and 'catch' not in code:
                    issues.append("缺少错误处理")
            elif language == 'go':
                if 'err' not in code:
                    issues.append("缺少错误处理")
            elif language == 'java':
                if 'try' not in code and 'catch' not in code:
                    issues.append("缺少错误处理")
        
        return issues
    
    def generate_report(self, quality_result, code, language):
        """生成质量报告
        
        Args:
            quality_result: 质量检查结果
            code: 代码内容
            language: 编程语言
            
        Returns:
            report: 质量报告
        """
        report = {
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'success': quality_result['success'],
            'message': quality_result['message'],
            'issues': quality_result['issues'],
            'code_length': len(code),
            'line_count': len(code.split('\n'))
        }
        
        return report
    
    def add_rule(self, language, rule_type, rule_config):
        """添加规则
        
        Args:
            language: 编程语言
            rule_type: 规则类型
            rule_config: 规则配置
        """
        if language not in self.rules:
            self.rules[language] = {}
        
        self.rules[language][rule_type] = rule_config
        self._save_config()
        logger.info(f"添加规则成功: {language}/{rule_type}")
    
    def update_rule(self, language, rule_type, rule_updates):
        """更新规则
        
        Args:
            language: 编程语言
            rule_type: 规则类型
            rule_updates: 规则更新
        """
        if language in self.rules and rule_type in self.rules[language]:
            self.rules[language][rule_type].update(rule_updates)
            self._save_config()
            logger.info(f"更新规则成功: {language}/{rule_type}")
        else:
            logger.warning(f"规则不存在: {language}/{rule_type}")
    
    def list_rules(self, language=None):
        """列出规则
        
        Args:
            language: 编程语言
            
        Returns:
            rules: 规则列表
        """
        if language:
            return self.rules.get(language, {})
        else:
            return self.rules

if __name__ == "__main__":
    # 测试代码质量检查器
    checker = CodeQualityChecker()
    
    # 测试Python代码
    print("测试Python代码:")
    python_code = '''
def factorial(n):
    """计算阶乘"""
    if n <= 1:
        return n
    else:
        return factorial(n-1) + factorial(n-2)
'''
    result = checker.check_code_quality(python_code, 'python')
    print(f"结果: {result['success']}")
    print(f"消息: {result['message']}")
    print("问题:")
    for issue in result['issues']:
        print(f"  - {issue}")
    print()
    
    # 测试JavaScript代码
    print("测试JavaScript代码:")
    js_code = '''
function factorial(n) {
    if (n <= 1) {
        return n;
    } else {
        return factorial(n-1) + factorial(n-2);
    }
}
'''
    result = checker.check_code_quality(js_code, 'javascript')
    print(f"结果: {result['success']}")
    print(f"消息: {result['message']}")
    print("问题:")
    for issue in result['issues']:
        print(f"  - {issue}")
    print()
    
    # 测试Go代码
    print("测试Go代码:")
    go_code = '''
package main

func Factorial(n int) int {
    if n <= 1 {
        return n
    } else {
        return Factorial(n-1) + Factorial(n-2)
    }
}
'''
    result = checker.check_code_quality(go_code, 'go')
    print(f"结果: {result['success']}")
    print(f"消息: {result['message']}")
    print("问题:")
    for issue in result['issues']:
        print(f"  - {issue}")
