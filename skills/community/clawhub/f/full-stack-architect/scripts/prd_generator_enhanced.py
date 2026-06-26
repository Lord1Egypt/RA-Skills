#!/usr/bin/env python3
"""
增强的PRD生成器
模拟LangChain的链式调用功能，实现PRD生成的智能化
"""

import os
import re
import json
from datetime import datetime

class PRDGenerator:
    def __init__(self):
        self.templates_dir = os.path.join(os.path.dirname(__file__), '../prd-modules/templates')
        self.prd_context_dir = os.path.join(os.path.dirname(__file__), '../../prd-context')
        self.prd_files_dir = os.path.join(self.prd_context_dir, 'prd-files')
        self.execution_logs_dir = os.path.join(self.prd_context_dir, 'execution-logs')
        self.conventions_dir = os.path.join(self.prd_context_dir, 'conventions')
        
        # 创建必要的目录
        for directory in [self.prd_context_dir, self.prd_files_dir, self.execution_logs_dir, self.conventions_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def generate_prd(self, project_name, project_description, industry='general'):
        """生成PRD文档
        
        Args:
            project_name: 项目名称
            project_description: 项目描述
            industry: 行业类型 (general, ecommerce, saas)
            
        Returns:
            prd_file_path: 生成的PRD文件路径
        """
        # 记录执行开始
        self._log_execution(f"开始生成PRD: {project_name}")
        
        try:
            # 步骤1: 分析项目需求
            requirements = self._analyze_requirements(project_description)
            
            # 步骤2: 选择合适的模板
            template = self._select_template(industry)
            
            # 步骤3: 填充模板
            prd_content = self._fill_template(template, project_name, requirements)
            
            # 步骤4: 生成PRD文件
            prd_file_path = self._save_prd(prd_content, project_name)
            
            # 步骤5: 生成JSON格式
            self._generate_json(prd_content, project_name)
            
            # 记录执行完成
            self._log_execution(f"PRD生成完成: {prd_file_path}")
            
            return prd_file_path
        except Exception as e:
            error_message = f"PRD生成失败: {str(e)}"
            self._log_execution(error_message)
            raise
    
    def _analyze_requirements(self, project_description):
        """分析项目需求
        
        Args:
            project_description: 项目描述
            
        Returns:
            requirements: 分析后的需求
        """
        # 简单的需求分析逻辑
        requirements = {
            'background': project_description,
            'goals': [],
            'features': [],
            'target_users': [],
            'tech_stack': {
                'frontend': ['React', 'Next.js', 'TypeScript'],
                'backend': ['Node.js', 'Express', 'TypeScript'],
                'database': ['MongoDB']
            }
        }
        
        # 提取关键信息
        if '电商' in project_description or 'ecommerce' in project_description.lower():
            requirements['goals'].append('建立在线销售渠道')
            requirements['goals'].append('提升用户购物体验')
            requirements['features'].append('商品管理')
            requirements['features'].append('订单处理')
            requirements['features'].append('支付集成')
            requirements['target_users'].append('普通消费者')
            requirements['target_users'].append('商家')
            requirements['tech_stack']['payment'] = ['Stripe', '支付宝', '微信支付']
        
        elif 'SaaS' in project_description or 'saas' in project_description.lower():
            requirements['goals'].append('提供企业级服务')
            requirements['goals'].append('简化业务流程')
            requirements['features'].append('用户管理')
            requirements['features'].append('订阅管理')
            requirements['features'].append('数据分析')
            requirements['target_users'].append('企业客户')
            requirements['target_users'].append('团队')
            requirements['tech_stack']['authentication'] = ['OAuth 2.0', 'JWT']
        
        else:
            requirements['goals'].append('实现项目功能')
            requirements['goals'].append('提供良好的用户体验')
            requirements['features'].append('核心功能')
            requirements['target_users'].append('目标用户')
        
        return requirements
    
    def _select_template(self, industry):
        """选择合适的PRD模板
        
        Args:
            industry: 行业类型
            
        Returns:
            template_content: 模板内容
        """
        template_file = os.path.join(self.templates_dir, f"{industry}.md")
        
        # 如果指定行业的模板不存在，使用通用模板
        if not os.path.exists(template_file):
            template_file = os.path.join(self.templates_dir, "ecommerce.md")  # 使用电商模板作为默认
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        return template_content
    
    def _fill_template(self, template, project_name, requirements):
        """填充模板
        
        Args:
            template: 模板内容
            project_name: 项目名称
            requirements: 分析后的需求
            
        Returns:
            prd_content: 填充后的PRD内容
        """
        # 替换项目名称
        prd_content = template.replace('[项目名称]', project_name)
        
        # 替换项目概述
        prd_content = prd_content.replace('[描述电商平台的背景和市场需求]', requirements['background'])
        prd_content = prd_content.replace('[描述项目的核心目标，如建立在线销售渠道、提升用户体验等]', '、'.join(requirements['goals']))
        prd_content = prd_content.replace('[列出核心功能，如商品管理、订单处理、支付集成等]', '、'.join(requirements['features']))
        prd_content = prd_content.replace('[描述目标用户群体，如普通消费者、商家等]', '、'.join(requirements['target_users']))
        
        # 替换技术栈
        frontend_stack = '、'.join(requirements['tech_stack'].get('frontend', []))
        backend_stack = '、'.join(requirements['tech_stack'].get('backend', []))
        database_stack = '、'.join(requirements['tech_stack'].get('database', []))
        
        prd_content = prd_content.replace('[推荐：React、Next.js、TypeScript、Tailwind CSS]', frontend_stack)
        prd_content = prd_content.replace('[推荐：Node.js、Express/Nest.js、TypeScript]', backend_stack)
        prd_content = prd_content.replace('[推荐：MongoDB/PostgreSQL]', database_stack)
        
        # 替换支付集成（如果有）
        if 'payment' in requirements['tech_stack']:
            payment_stack = '、'.join(requirements['tech_stack']['payment'])
            prd_content = prd_content.replace('[推荐：Stripe/PayPal/支付宝/微信支付]', payment_stack)
        
        # 替换认证（如果有）
        if 'authentication' in requirements['tech_stack']:
            auth_stack = '、'.join(requirements['tech_stack']['authentication'])
            prd_content = prd_content.replace('[推荐：OAuth 2.0、JWT]', auth_stack)
        
        return prd_content
    
    def _save_prd(self, prd_content, project_name):
        """保存PRD文件
        
        Args:
            prd_content: PRD内容
            project_name: 项目名称
            
        Returns:
            prd_file_path: 保存的PRD文件路径
        """
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 处理中文项目名称
        if not project_name.strip():
            safe_project_name = 'unnamed'
        else:
            # 保留中文和字母数字，其他替换为下划线
            safe_project_name = re.sub(r'[^\w\u4e00-\u9fa5]', '_', project_name)
            # 确保文件名不为空
            if not safe_project_name.strip():
                safe_project_name = 'unnamed'
        prd_filename = f"prd-{safe_project_name}_{timestamp}.md"
        prd_file_path = os.path.join(self.prd_files_dir, prd_filename)
        
        # 保存文件
        with open(prd_file_path, 'w', encoding='utf-8') as f:
            f.write(prd_content)
        
        return prd_file_path
    
    def _generate_json(self, prd_content, project_name):
        """生成JSON格式的PRD
        
        Args:
            prd_content: PRD内容
            project_name: 项目名称
        """
        # 简单的PRD解析逻辑
        prd_json = {
            'project_name': project_name,
            'generated_at': datetime.now().isoformat(),
            'sections': {}
        }
        
        # 提取项目概述
        overview_match = re.search(r'## 1\. 项目概述(.*?)## 2\. 技术栈', prd_content, re.DOTALL)
        if overview_match:
            overview_text = overview_match.group(1)
            prd_json['sections']['overview'] = overview_text.strip()
        
        # 提取技术栈
        tech_stack_match = re.search(r'## 2\. 技术栈(.*?)## 3\. 用户故事', prd_content, re.DOTALL)
        if tech_stack_match:
            tech_stack_text = tech_stack_match.group(1)
            prd_json['sections']['tech_stack'] = tech_stack_text.strip()
        
        # 提取用户故事
        user_stories_match = re.search(r'## 3\. 用户故事(.*?)## 4\. 非目标', prd_content, re.DOTALL)
        if user_stories_match:
            user_stories_text = user_stories_match.group(1)
            prd_json['sections']['user_stories'] = user_stories_text.strip()
        
        # 提取非目标
        non_goals_match = re.search(r'## 4\. 非目标(.*?)## 5\. 成功指标', prd_content, re.DOTALL)
        if non_goals_match:
            non_goals_text = non_goals_match.group(1)
            prd_json['sections']['non_goals'] = non_goals_text.strip()
        
        # 提取成功指标
        success_metrics_match = re.search(r'## 5\. 成功指标(.*?)$', prd_content, re.DOTALL)
        if success_metrics_match:
            success_metrics_text = success_metrics_match.group(1)
            prd_json['sections']['success_metrics'] = success_metrics_text.strip()
        
        # 保存JSON文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # 处理中文项目名称
        if not project_name.strip():
            safe_project_name = 'unnamed'
        else:
            # 保留中文和字母数字，其他替换为下划线
            safe_project_name = re.sub(r'[^\w\u4e00-\u9fa5]', '_', project_name)
            # 确保文件名不为空
            if not safe_project_name.strip():
                safe_project_name = 'unnamed'
        json_filename = f"prd-{safe_project_name}_{timestamp}.json"
        json_file_path = os.path.join(self.prd_files_dir, json_filename)
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(prd_json, f, ensure_ascii=False, indent=2)
    
    def _log_execution(self, message):
        """记录执行日志
        
        Args:
            message: 日志消息
        """
        log_file = os.path.join(self.execution_logs_dir, 'development-log.txt')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(log_entry.strip())

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python prd_generator_enhanced.py <项目名称> <项目描述> [行业类型]")
        print("行业类型: general, ecommerce, saas")
        sys.exit(1)
    
    project_name = sys.argv[1]
    project_description = sys.argv[2]
    industry = sys.argv[3] if len(sys.argv) > 3 else 'general'
    
    generator = PRDGenerator()
    prd_file = generator.generate_prd(project_name, project_description, industry)
    print(f"\nPRD生成成功！文件路径: {prd_file}")
