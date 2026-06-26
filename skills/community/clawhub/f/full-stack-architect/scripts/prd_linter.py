#!/usr/bin/env python3
"""
PRD文档格式校验脚本
检查PRD文档的格式是否符合规范
"""

import os
import re
import sys

class PRDLinter:
    def __init__(self):
        self.errors = []
    
    def lint_file(self, file_path):
        """校验单个PRD文件"""
        print(f"开始校验文件: {file_path}")
        self.errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            self.errors.append(f"文件读取错误: {str(e)}")
            return False
        
        # 检查文件结构
        self._check_structure(content, lines)
        
        # 检查格式问题
        self._check_format(lines)
        
        # 打印结果
        if self.errors:
            print(f"发现 {len(self.errors)} 个问题:")
            for error in self.errors:
                print(f"  - {error}")
            return False
        else:
            print("✅ 校验通过！")
            return True
    
    def _check_structure(self, content, lines):
        """检查PRD文档结构"""
        # 检查标题结构
        if not re.search(r'^# .+产品需求文档', content, re.MULTILINE):
            self.errors.append("缺少主标题: # [项目名称] 产品需求文档")
        
        # 检查项目概述部分
        if not re.search(r'## 1\. 项目概述', content, re.MULTILINE):
            self.errors.append("缺少项目概述部分: ## 1. 项目概述")
        
        # 检查技术栈部分
        if not re.search(r'## 2\. 技术栈', content, re.MULTILINE):
            self.errors.append("缺少技术栈部分: ## 2. 技术栈")
        
        # 检查用户故事部分
        if not re.search(r'## 3\. 用户故事', content, re.MULTILINE):
            self.errors.append("缺少用户故事部分: ## 3. 用户故事")
        
        # 检查非目标部分
        if not re.search(r'## 4\. 非目标', content, re.MULTILINE):
            self.errors.append("缺少非目标部分: ## 4. 非目标")
        
        # 检查成功指标部分
        if not re.search(r'## 5\. 成功指标', content, re.MULTILINE):
            self.errors.append("缺少成功指标部分: ## 5. 成功指标")
        
        # 检查用户故事是否存在
        # 检查是否包含故事相关内容
        if '故事' not in content:
            self.errors.append("缺少用户故事")
        # 检查是否包含验收标准
        if '验收标准' not in content:
            self.errors.append("缺少验收标准")
        
        # 简单检查故事内容
        if '描述' not in content:
            self.errors.append("故事缺少描述")
        if '依赖关系' not in content:
            self.errors.append("故事缺少依赖关系")
        if '优先级' not in content:
            self.errors.append("故事缺少优先级")
        if '类型' not in content:
            self.errors.append("故事缺少类型")
    
    def _check_format(self, lines):
        """检查markdown格式"""
        for i, line in enumerate(lines, 1):
            # 检查行尾空格
            if line.rstrip() != line:
                self.errors.append(f"第 {i} 行: 行尾有多余空格")
            
            # 检查标题格式
            if line.startswith('#'):
                # 跳过空标题
                if len(line.strip()) == 1:
                    continue
                # 检查标题后是否有空格
                title_match = re.match(r'^#+\s', line)
                if not title_match:
                    self.errors.append(f"第 {i} 行: 标题后缺少空格")
            
            # 检查列表格式
            if line.strip().startswith('- '):
                if not line.startswith('  '):
                    # 检查列表缩进
                    pass
            
            # 检查粗体格式
            if '**' in line:
                bold_matches = re.findall(r'\*\*(.*?)\*\*', line)
                for match in bold_matches:
                    if not match:
                        self.errors.append(f"第 {i} 行: 粗体标记内无内容")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python prd_linter.py <prd文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        sys.exit(1)
    
    linter = PRDLinter()
    success = linter.lint_file(file_path)
    sys.exit(0 if success else 1)
