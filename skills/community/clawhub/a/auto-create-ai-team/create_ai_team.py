#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Create AI Team - Enhanced Version
Creates AI team directory structures for projects with template support.
No external dependencies, completely offline.
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import error handler
from error_handler import (
    AITeamError, ProjectPathError, ConfigurationError,
    validate_project_path, safe_create_directory, setup_logging, handle_error
)

# =============================================================================
# Internationalization
# =============================================================================

I18N = {
    'zh': {
        'creating': '正在创建 AI 团队结构...',
        'project_path': '项目路径',
        'team_type': '团队类型',
        'project_type': '项目类型',
        'language': '语言',
        'success': 'AI 团队结构创建成功！',
        'location': '位置',
        'error_project_not_found': '错误：项目路径不存在',
        'error_config_invalid': '错误：配置文件格式无效',
        'internal_team': '内部AI团队',
        'internet_team': '互联网团队',
        'single_team': '单一AI团队',
        'dual_mode': '双团队模式 (内部 + 互联网)',
        'single_mode': '单团队模式 (仅内部)',
        'custom_mode': '自定义团队模式',
        # Progress template - keys match template variable names
        'project_info': '项目基本信息',
        'project_name_label': '项目名称',
        'creation_time': '创建时间',
        'project_type_label': '项目类型',
        'team_type_label': '团队类型',
        'team_structure': '团队结构',
        'internal_team_section': '内部AI团队（产品开发）',
        'internet_team_section': '互联网团队（产品运营）',
        'single_team_section': '单一AI团队',
        'team_size_label': '团队规模',
        'main_roles': '主要角色',
        'core_responsibilities': '核心职责',
        'product_dev': '产品开发、技术实现、质量保证',
        'marketing_growth': '市场推广、用户增长、商业化运营',
        'full_process': '全流程产品开发和运营',
        'current_status': '当前状态',
        'team_created': '团队创建',
        'config_files': '配置文件',
        'automation_scripts': '自动化脚本',
        'runtime_logs': '运行日志',
        'completed': '已完成',
        'generated': '已生成',
        'deployed': '已部署',
        'enabled': '已启用',
        'next_steps': '下一步计划',
        'next_step_1': 'AI团队开始自动运行',
        'next_step_2': '监控团队工作进展',
        'next_step_3': '定期生成进展报告',
        'next_step_4': '根据需要调整团队配置',
        'directory_structure': '目录结构',
        'team_info_dir': '团队信息和配置',
        'internal_team_dir': '内部AI团队',
        'internet_team_dir': '互联网团队',
        'single_team_dir': '单一团队',
        'original_dirs': '项目原有目录',
        'auto_generated': '此文件由 Auto Create AI Team Skill v2.0 自动生成',
        # Workflow template
        'workflow_title': 'AI团队工作流程',
        'dual_workflow': '双团队协作流程',
        'single_workflow': '单团队工作流程',
        'custom_workflow': '自定义团队工作流程',
        'collaboration_mechanism': '协作机制',
        'weekly_sync': '每周同步会议',
        'shared_docs': '共享文档库',
        'cross_review': '交叉评审',
        'data_sharing': '数据共享',
        'multi_model_support': '多模型支持',
        'free_first': '免费模型优先',
        'paid_precision': '付费模型精准',
        'auto_fallback': '自动降级',
        'result_aggregation': '结果聚合',
        'automation': '自动化运行',
        'scheduled_tasks': '定时任务',
        'event_triggered': '事件触发',
        'progress_monitoring': '进度监控',
        'exception_handling': '异常处理',
        'product_dev_label': '产品开发',
        'marketing_growth_label': '产品运营',
    },
    'en': {
        'creating': 'Creating AI team structure...',
        'project_path': 'Project path',
        'team_type': 'Team type',
        'project_type': 'Project type',
        'language': 'Language',
        'success': 'AI team structure created successfully!',
        'location': 'Location',
        'error_project_not_found': 'Error: Project path does not exist',
        'error_config_invalid': 'Error: Invalid configuration file format',
        'internal_team': 'Internal AI Team',
        'internet_team': 'Internet Team',
        'single_team': 'Single AI Team',
        'dual_mode': 'Dual team mode (Internal + Internet)',
        'single_mode': 'Single team mode (Internal only)',
        'custom_mode': 'Custom team mode',
        # Progress template - keys match template variable names
        'project_info': 'Project Information',
        'project_name_label': 'Project Name',
        'creation_time': 'Creation Time',
        'project_type_label': 'Project Type',
        'team_type_label': 'Team Type',
        'team_structure': 'Team Structure',
        'internal_team_section': 'Internal AI Team (Product Development)',
        'internet_team_section': 'Internet Team (Product Operations)',
        'single_team_section': 'Single AI Team',
        'team_size_label': 'Team Size',
        'main_roles': 'Main Roles',
        'core_responsibilities': 'Core Responsibilities',
        'product_dev': 'Product development, technical implementation, quality assurance',
        'marketing_growth': 'Marketing, user growth, commercial operations',
        'full_process': 'Full-cycle product development and operations',
        'current_status': 'Current Status',
        'team_created': 'Team Created',
        'config_files': 'Configuration Files',
        'automation_scripts': 'Automation Scripts',
        'runtime_logs': 'Runtime Logs',
        'completed': 'Completed',
        'generated': 'Generated',
        'deployed': 'Deployed',
        'enabled': 'Enabled',
        'next_steps': 'Next Steps',
        'next_step_1': 'AI team starts running automatically',
        'next_step_2': 'Monitor team progress',
        'next_step_3': 'Generate regular progress reports',
        'next_step_4': 'Adjust team configuration as needed',
        'directory_structure': 'Directory Structure',
        'team_info_dir': 'Team info and configuration',
        'internal_team_dir': 'Internal AI Team',
        'internet_team_dir': 'Internet Team',
        'single_team_dir': 'Single Team',
        'original_dirs': 'Original project directories',
        'auto_generated': 'Auto-generated by Auto Create AI Team Skill v2.0',
        # Workflow template
        'workflow_title': 'AI Team Workflow',
        'dual_workflow': 'Dual Team Collaboration',
        'single_workflow': 'Single Team Workflow',
        'custom_workflow': 'Custom Team Workflow',
        'collaboration_mechanism': 'Collaboration Mechanism',
        'weekly_sync': 'Weekly sync meetings',
        'shared_docs': 'Shared document library',
        'cross_review': 'Cross-team review',
        'data_sharing': 'Data sharing',
        'multi_model_support': 'Multi-model Support',
        'free_first': 'Free models first',
        'paid_precision': 'Paid models for precision',
        'auto_fallback': 'Automatic fallback',
        'result_aggregation': 'Result aggregation',
        'automation': 'Automation',
        'scheduled_tasks': 'Scheduled tasks',
        'event_triggered': 'Event-triggered',
        'progress_monitoring': 'Progress monitoring',
        'exception_handling': 'Exception handling',
        'product_dev_label': 'Product Development',
        'marketing_growth_label': 'Product Operations',
    }
}

def t(key: str, lang: str = 'zh') -> str:
    """Translate key to specified language"""
    return I18N.get(lang, I18N['zh']).get(key, key)

# =============================================================================
# Template Engine (Simple Implementation)
# =============================================================================

class SimpleTemplateEngine:
    """Simple template engine using regex, no external dependencies"""
    
    def __init__(self, template_dir: str):
        self.template_dir = Path(template_dir)
    
    def load_template(self, template_name: str) -> str:
        """Load template file content"""
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render(self, template_content: str, context: Dict[str, Any]) -> str:
        """Render template with context variables"""
        result = template_content
        
        # Handle simple variable replacement: {{variable}}
        for key, value in context.items():
            pattern = r'\{\{\s*' + re.escape(key) + r'\s*\}\}'
            result = re.sub(pattern, str(value) if value else '', result)
        
        # Handle conditional blocks: {% if condition %}...{% endif %}
        result = self._process_conditionals(result, context)
        
        # Handle for loops: {% for item in items %}...{% endfor %}
        result = self._process_loops(result, context)
        
        return result
    
    def _process_conditionals(self, content: str, context: Dict[str, Any]) -> str:
        """Process {% if ... %}...{% elif ... %}...{% else %}...{% endif %} blocks"""
        
        def evaluate_condition(condition: str, ctx: Dict[str, Any]) -> bool:
            """Evaluate a condition expression"""
            condition = condition.strip()
            
            # Handle: variable == "value" or variable == 'value'
            eq_match = re.match(r"(\w+)\s*==\s*['\"](.+?)['\"]", condition)
            if eq_match:
                var_name = eq_match.group(1)
                expected = eq_match.group(2)
                actual = str(ctx.get(var_name, ''))
                return actual == expected
            
            # Handle: variable in ['value1', 'value2']
            in_match = re.match(r"(\w+)\s+in\s+\[(.+?)\]", condition)
            if in_match:
                var_name = in_match.group(1)
                values_str = in_match.group(2)
                values = re.findall(r"['\"](.+?)['\"]", values_str)
                actual = str(ctx.get(var_name, ''))
                return actual in values
            
            # Handle: variable != "value"
            neq_match = re.match(r"(\w+)\s*!=\s*['\"](.+?)['\"]", condition)
            if neq_match:
                var_name = neq_match.group(1)
                expected = neq_match.group(2)
                actual = str(ctx.get(var_name, ''))
                return actual != expected
            
            # Simple variable truthy check
            value = ctx.get(condition)
            if value is None:
                return False
            if isinstance(value, bool):
                return value
            if isinstance(value, (list, dict)):
                return len(value) > 0
            return bool(value)
        
        def find_endif(text: str, start: int) -> int:
            """Find matching {% endif %}, accounting for nested ifs"""
            depth = 1
            pos = start
            while depth > 0 and pos < len(text):
                # Find next {% ... %}
                tag_start = text.find('{%', pos)
                if tag_start == -1:
                    return -1
                tag_end = text.find('%}', tag_start)
                if tag_end == -1:
                    return -1
                
                tag_content = text[tag_start+2:tag_end].strip()
                
                if tag_content.startswith('if '):
                    depth += 1
                elif tag_content == 'endif':
                    depth -= 1
                
                pos = tag_end + 2
                
                if depth == 0:
                    return tag_start
            return -1
        
        result = content
        
        # Process if blocks iteratively
        max_iterations = 100  # Safety limit
        for _ in range(max_iterations):
            # Find {% if ... %}
            if_match = re.search(r'\{%\s*if\s+(.+?)\s*%\}', result)
            if not if_match:
                break
            
            if_pos = if_match.start()
            if_cond = if_match.group(1)
            content_start = if_match.end()
            
            # Find matching endif
            endif_pos = find_endif(result, content_start)
            if endif_pos == -1:
                # Malformed template, remove if tag and continue
                result = result[:if_pos] + result[content_start:]
                break
            
            endif_end = result.find('%}', endif_pos) + 2
            block_text = result[content_start:endif_pos]
            
            # Parse branches: collect (condition, content) pairs
            branches = []
            
            # Use regex to find all elif/else positions
            tag_positions = []
            for m in re.finditer(r'\{%\s*(elif\s+.+?|else)\s*%\}', block_text):
                tag_positions.append((m.start(), m.end(), m.group(1).strip()))
            
            # Build branches
            if tag_positions:
                # First branch: content from start to first elif/else
                branches.append((if_cond, block_text[:tag_positions[0][0]]))
                
                # Middle branches
                for i, (start, end, tag) in enumerate(tag_positions):
                    if i + 1 < len(tag_positions):
                        branch_content = block_text[end:tag_positions[i+1][0]]
                    else:
                        branch_content = block_text[end:]
                    
                    if tag.startswith('elif '):
                        cond = tag[5:].strip()
                    else:  # else
                        cond = 'else'
                    branches.append((cond, branch_content))
            else:
                # No elif/else, just the if content
                branches.append((if_cond, block_text))
            
            # Evaluate conditions
            selected_content = ''
            for cond, branch_content in branches:
                if cond == 'else':
                    selected_content = branch_content
                    break
                if evaluate_condition(cond, context):
                    selected_content = branch_content
                    break
            
            # Replace entire if block with selected content
            result = result[:if_pos] + selected_content + result[endif_end:]
        
        return result
    
    def _process_loops(self, content: str, context: Dict[str, Any]) -> str:
        """Process {% for item in items %}...{% endfor %} blocks"""
        for_pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'
        
        def replace_for(match):
            item_name = match.group(1)
            list_name = match.group(2)
            template_block = match.group(3)
            
            items = context.get(list_name, [])
            if not isinstance(items, (list, tuple)):
                return ''
            
            result_parts = []
            for i, item in enumerate(items):
                # Create context for this iteration
                item_context = context.copy()
                item_context[item_name] = item
                item_context['index'] = i
                item_context['index1'] = i + 1
                result_parts.append(self.render(template_block, item_context))
            
            return ''.join(result_parts)
        
        return re.sub(for_pattern, replace_for, content, flags=re.DOTALL)
    
    def render_file(self, template_name: str, context: Dict[str, Any]) -> str:
        """Load and render a template file"""
        template_content = self.load_template(template_name)
        return self.render(template_content, context)

# =============================================================================
# Default Configurations
# =============================================================================

DEFAULT_TEAM_MEMBERS = {
    'zh': {
        'web_app': {
            'internal': ['产品经理', '前端开发工程师', '后端开发工程师', 'QA测试工程师', 'UI/UX设计师'],
            'internet': ['产品运营', '市场推广专员', '数据分析师', '用户增长专家']
        },
        'ecommerce': {
            'internal': ['技术架构师', '全栈开发工程师', 'UI设计师', '支付集成专家', 'QA工程师'],
            'internet': ['电商运营', '营销策划', '客服主管', '数据分析专家']
        },
        'mobile_app': {
            'internal': ['移动端开发工程师', '后端工程师', 'UI/UX设计师', 'QA工程师', 'DevOps工程师'],
            'internet': ['App运营', 'ASO优化专家', '用户运营', '数据分析师']
        },
        'generic': {
            'internal': ['AI助手', '数据处理专员', '内容创作者', '质量审核员', '项目协调员'],
            'internet': ['产品经理', '市场营销专家', '社媒运营', '数据分析专家']
        }
    },
    'en': {
        'web_app': {
            'internal': ['Product Manager', 'Frontend Developer', 'Backend Developer', 'QA Engineer', 'UI/UX Designer'],
            'internet': ['Product Operations', 'Marketing Specialist', 'Data Analyst', 'User Growth Expert']
        },
        'ecommerce': {
            'internal': ['Technical Architect', 'Full-stack Developer', 'UI Designer', 'Payment Integration Specialist', 'QA Engineer'],
            'internet': ['E-commerce Operations', 'Marketing Planner', 'Customer Service Lead', 'Data Analysis Expert']
        },
        'mobile_app': {
            'internal': ['Mobile Developer', 'Backend Engineer', 'UI/UX Designer', 'QA Engineer', 'DevOps Engineer'],
            'internet': ['App Operations', 'ASO Specialist', 'User Operations', 'Data Analyst']
        },
        'generic': {
            'internal': ['AI Assistant', 'Data Processor', 'Content Creator', 'Quality Checker', 'Project Coordinator'],
            'internet': ['Product Manager', 'Marketing Expert', 'Social Media Operator', 'Data Analyst']
        }
    }
}

PROJECT_TYPE_NAMES = {
    'zh': {
        'web_app': 'Web应用',
        'ecommerce': '电商平台',
        'mobile_app': '移动应用',
        'generic': '通用项目'
    },
    'en': {
        'web_app': 'Web Application',
        'ecommerce': 'E-commerce Platform',
        'mobile_app': 'Mobile Application',
        'generic': 'Generic Project'
    }
}

# =============================================================================
# Main Logic
# =============================================================================

class AITeamCreator:
    """Main class for creating AI team structures"""
    
    def __init__(self, project_path: str, config: Dict[str, Any], lang: str = 'zh'):
        self.project_path = Path(project_path)
        self.config = config
        self.lang = lang
        self.team_type = config.get('team_type', 'single')
        self.project_type = config.get('project_type', 'generic')
        self.project_name = self.project_path.name
        
        # Get template directory
        script_dir = Path(__file__).parent
        self.template_dir = script_dir / 'templates'
        self.template_engine = SimpleTemplateEngine(self.template_dir)
        
        # Initialize team members with language support
        lang_teams = DEFAULT_TEAM_MEMBERS.get(lang, DEFAULT_TEAM_MEMBERS['zh'])
        project_teams = lang_teams.get(self.project_type, lang_teams['generic'])
        
        self.internal_members = config.get('internal_members') or project_teams['internal']
        self.internet_members = config.get('internet_members') or project_teams['internet']
    
    def create(self) -> None:
        """Create the complete AI team structure"""
        # Validate project path
        validate_project_path(self.project_path)
        
        # Create main ai-team directory
        ai_team_dir = self.project_path / 'ai-team'
        safe_create_directory(ai_team_dir)
        
        # Create team structures based on team type
        if self.team_type == 'dual':
            self._create_dual_team_structure(ai_team_dir)
        elif self.team_type == 'single':
            self._create_single_team_structure(ai_team_dir)
        else:
            self._create_custom_team_structure(ai_team_dir)
        
        # Create project progress file
        self._create_progress_file(ai_team_dir)
        
        # Create workflow file
        self._create_workflow_file(ai_team_dir)
    
    def _create_dual_team_structure(self, ai_team_dir: Path) -> None:
        """Create dual team structure (internal + internet)"""
        # Internal team
        internal_dir = ai_team_dir / 'internal-team' / 'team-info'
        safe_create_directory(internal_dir)
        self._create_team_config(internal_dir / 'AI_TEAM_CONFIG.md', 'internal')
        self._create_members_file(internal_dir / 'TEAM_MEMBERS.md', 'internal')
        
        # Internet team
        internet_dir = ai_team_dir / 'internet-team' / 'team-info'
        safe_create_directory(internet_dir)
        self._create_team_config(internet_dir / 'INTERNET_TEAM_CONFIG.md', 'internet')
        self._create_members_file(internet_dir / 'TEAM_MEMBERS.md', 'internet')
    
    def _create_single_team_structure(self, ai_team_dir: Path) -> None:
        """Create single team structure"""
        team_dir = ai_team_dir / 'team-info'
        safe_create_directory(team_dir)
        self._create_team_config(team_dir / 'AI_TEAM_CONFIG.md', 'single')
        self._create_members_file(team_dir / 'TEAM_MEMBERS.md', 'single')
    
    def _create_custom_team_structure(self, ai_team_dir: Path) -> None:
        """Create custom team structure from config"""
        team_dir = ai_team_dir / 'team-info'
        safe_create_directory(team_dir)
        self._create_team_config(team_dir / 'AI_TEAM_CONFIG.md', 'custom')
        
        # Save custom config if provided
        if 'custom_config' in self.config:
            with open(team_dir / 'custom_team_config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config['custom_config'], f, indent=2, ensure_ascii=False)
    
    def _create_team_config(self, file_path: Path, team_category: str) -> None:
        """Create team configuration file using template"""
        creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Build context for template
        context = {
            'project_name': self.project_name,
            'project_type': PROJECT_TYPE_NAMES.get(self.lang, {}).get(self.project_type, self.project_type),
            'creation_time': creation_time,
            'team_mode': self.team_type,
            'has_internal_team': self.team_type in ['single', 'dual'],
            'has_internet_team': self.team_type == 'dual',
            'internal_team_roles': ', '.join(self.internal_members),
            'internet_team_roles': ', '.join(self.internet_members) if self.team_type == 'dual' else '',
            'primary_model': self.config.get('primary_model', 'GPT-4'),
            'fallback_models': self.config.get('fallback_models', 'GPT-3.5, Claude'),
            'cost_strategy': self.config.get('cost_strategy', 'free_first'),
            'collaboration_method': self.config.get('collaboration_method', 'async_parallel'),
            'reporting_frequency': self.config.get('reporting_frequency', 'weekly'),
            'quality_standards': self.config.get('quality_standards', 'standard'),
        }
        
        try:
            content = self.template_engine.render_file('team_config_template.md', context)
        except FileNotFoundError:
            # Fallback to simple format if template not found
            content = self._generate_simple_config(team_category, creation_time)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_simple_config(self, team_category: str, creation_time: str) -> str:
        """Generate simple config as fallback"""
        if team_category == 'internal':
            members = self.internal_members
            team_name = t('internal_team', self.lang)
        elif team_category == 'internet':
            members = self.internet_members
            team_name = t('internet_team', self.lang)
        else:
            members = self.internal_members
            team_name = t('single_team', self.lang)
        
        return f"""# {team_name} Configuration

## Project Information
- **Project Name**: {self.project_name}
- **Project Type**: {PROJECT_TYPE_NAMES.get(self.lang, {}).get(self.project_type, self.project_type)}
- **Creation Time**: {creation_time}
- **Team Type**: {team_category}

## Team Members
{chr(10).join(f'- {m}' for m in members)}

## Model Configuration
- **Primary Model**: {self.config.get('primary_model', 'GPT-4')}
- **Fallback Models**: {self.config.get('fallback_models', 'GPT-3.5, Claude')}
"""
    
    def _create_members_file(self, file_path: Path, team_category: str) -> None:
        """Create detailed team members file"""
        if team_category == 'internal':
            members = self.internal_members
            team_name = t('internal_team', self.lang)
        elif team_category == 'internet':
            members = self.internet_members
            team_name = t('internet_team', self.lang)
        else:
            members = self.internal_members
            team_name = t('single_team', self.lang)
        
        context = {
            'TEAM_MODE': self.team_type.upper(),
            'INTERNAL_TEAM_LEAD': members[0] if members else 'Team Lead',
            'TECHNICAL_SPECIALIST': members[1] if len(members) > 1 else 'Technical Specialist',
            'CONTENT_CREATOR': members[2] if len(members) > 2 else 'Content Creator',
            'QUALITY_ASSURANCE': members[3] if len(members) > 3 else 'QA Specialist',
            'PRIMARY_MODEL': self.config.get('primary_model', 'GPT-4'),
            'FALLBACK_MODELS': self.config.get('fallback_models', 'GPT-3.5, Claude'),
            'PRODUCT_MANAGER': self.internet_members[0] if self.internet_members else 'Product Manager',
            'MARKETING_EXPERT': self.internet_members[1] if len(self.internet_members) > 1 else 'Marketing Expert',
            'SOCIAL_MEDIA_MANAGER': self.internet_members[2] if len(self.internet_members) > 2 else 'Social Media Manager',
            'DATA_ANALYST': self.internet_members[3] if len(self.internet_members) > 3 else 'Data Analyst',
            'INTERNET_PRIMARY_MODEL': self.config.get('internet_primary_model', 'Claude'),
            'INTERNET_FALLBACK_MODELS': self.config.get('internet_fallback_models', 'GPT-3.5'),
            'team_name': team_name,
            'members': members,
        }
        
        try:
            content = self.template_engine.render_file('team_members_template.md', context)
        except FileNotFoundError:
            content = self._generate_simple_members(team_name, members)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_simple_members(self, team_name: str, members: List[str]) -> str:
        """Generate simple members file as fallback"""
        return f"""# {team_name} Members

## Team Members
{chr(10).join(f'- **{m}**' for m in members)}

## Responsibilities
Each team member is responsible for their domain expertise and collaborates with others to achieve project goals.
"""
    
    def _create_progress_file(self, ai_team_dir: Path) -> None:
        """Create project progress tracking file"""
        creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get all translations for this language
        translations = I18N.get(self.lang, I18N['zh'])
        
        # Build context - translations first, then specific values (to override)
        context = {
            # Add all translation strings
            **{k.upper(): v for k, v in translations.items()},
        }
        
        # Add specific values (these override translations with same keys)
        context.update({
            'PROJECT_NAME': self.project_name,
            'CREATION_DATE': creation_time,
            'PROJECT_TYPE': PROJECT_TYPE_NAMES.get(self.lang, {}).get(self.project_type, self.project_type),
            'TEAM_MODE': self.team_type,
            'TEAM_MODE_DESC': t(f'{self.team_type}_mode', self.lang),
            'INTERNAL_TEAM_SIZE': len(self.internal_members),
            'INTERNAL_TEAM_ROLES': ', '.join(self.internal_members),
            'INTERNET_TEAM_SIZE': len(self.internet_members),
            'INTERNET_TEAM_ROLES': ', '.join(self.internet_members),
            'TEAM_SIZE': len(self.internal_members),
            'TEAM_ROLES': ', '.join(self.internal_members),
            'PROJECT_PATH': str(self.project_path),
        })
        
        try:
            content = self.template_engine.render_file('progress_template.md', context)
        except FileNotFoundError:
            content = self._generate_simple_progress(creation_time)
        
        with open(ai_team_dir / 'PROJECT_PROGRESS.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_simple_progress(self, creation_time: str) -> str:
        """Generate simple progress file as fallback"""
        mode_desc = t(f'{self.team_type}_mode', self.lang)
        project_type_name = PROJECT_TYPE_NAMES.get(self.lang, {}).get(self.project_type, self.project_type)
        
        # Build internal team section
        internal_section = chr(10).join(f'- {m}' for m in self.internal_members)
        
        # Build internet team section conditionally
        internet_section = ""
        if self.team_type == 'dual':
            internet_team = t('internet_team', self.lang)
            internet_section = f"""
### {internet_team}
{chr(10).join(f'- {m}' for m in self.internet_members)}"""
        
        internal_team = t('internal_team', self.lang)
        project_info = t('project_info', self.lang)
        project_name = t('project_name', self.lang)
        creation_time_label = t('creation_time', self.lang)
        project_type_label = t('project_type', self.lang)
        team_type_label = t('team_type', self.lang)
        team_structure = t('team_structure', self.lang)
        
        return f"""# {self.project_name} - {project_info}

## {project_info}
- **{project_name}**: {self.project_name}
- **{project_type_label}**: {project_type_name}
- **{team_type_label}**: {mode_desc}
- **{creation_time_label}**: {creation_time}

## {team_structure}
### {internal_team}
{internal_section}
{internet_section}

## {t('current_status', self.lang)}
- {t('team_created', self.lang)}: ✅ {t('completed', self.lang)}
- {t('config_files', self.lang)}: ✅ {t('generated', self.lang)}
- {t('automation_scripts', self.lang)}: ✅ {t('deployed', self.lang)}
- {t('runtime_logs', self.lang)}: ✅ {t('enabled', self.lang)}
"""
    
    def _create_workflow_file(self, ai_team_dir: Path) -> None:
        """Create workflow configuration file"""
        # Get all translations
        translations = I18N.get(self.lang, I18N['zh'])
        
        context = {
            'project_type': PROJECT_TYPE_NAMES.get(self.lang, {}).get(self.project_type, self.project_type),
            'team_mode': self.team_type,
            **{k.upper(): v for k, v in translations.items()},
        }
        
        try:
            content = self.template_engine.render_file('workflow_template.md', context)
        except FileNotFoundError:
            content = self._generate_simple_workflow()
        
        with open(ai_team_dir / 'WORKFLOW.md', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_simple_workflow(self) -> str:
        """Generate simple workflow file as fallback"""
        project_type_name = PROJECT_TYPE_NAMES.get(self.lang, {}).get(self.project_type, self.project_type)
        workflow_title = t('workflow_title', self.lang)
        
        return f"""# {workflow_title}

## {t('project_type', self.lang)}: {project_type_name}
## {t('team_type', self.lang)}: {self.team_type}

### {t('collaboration_mechanism', self.lang)}
1. {t('weekly_sync', self.lang)}
2. {t('shared_docs', self.lang)}
3. {t('cross_review', self.lang)}
4. {t('data_sharing', self.lang)}

### {t('multi_model_support', self.lang)}
- {t('free_first', self.lang)}
- {t('paid_precision', self.lang)}
- {t('auto_fallback', self.lang)}
- {t('result_aggregation', self.lang)}

### {t('automation', self.lang)}
- {t('scheduled_tasks', self.lang)}
- {t('event_triggered', self.lang)}
- {t('progress_monitoring', self.lang)}
- {t('exception_handling', self.lang)}
"""

# =============================================================================
# Configuration Loading
# =============================================================================

def load_default_config(script_dir: Path) -> Dict[str, Any]:
    """Load default configuration from JSON file"""
    config_path = script_dir / 'templates' / 'default_config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file: {e}")
    return {}

def merge_configs(default_config: Dict[str, Any], cli_args: argparse.Namespace) -> Dict[str, Any]:
    """Merge CLI arguments with default configuration"""
    config = default_config.copy()
    
    # CLI arguments override defaults
    config['team_type'] = cli_args.team_type or config.get('default_team_mode', 'single')
    config['project_type'] = cli_args.project_type or 'generic'
    config['lang'] = cli_args.lang or 'zh'
    
    # Custom members if provided
    if cli_args.internal_members:
        config['internal_members'] = [m.strip() for m in cli_args.internal_members.split(',')]
    if cli_args.internet_members:
        config['internet_members'] = [m.strip() for m in cli_args.internet_members.split(',')]
    
    # Model configuration
    if cli_args.primary_model:
        config['primary_model'] = cli_args.primary_model
    if cli_args.fallback_models:
        config['fallback_models'] = cli_args.fallback_models
    
    return config

# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Create AI team directory structure for projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --project-path ./my-project
  %(prog)s --project-path ./my-project --team-type dual --project-type web_app
  %(prog)s --project-path ./my-project --internal-members "Dev1,Dev2,Dev3" --lang en
        '''
    )
    
    # Required arguments
    parser.add_argument('--project-path', required=True, 
                        help='Path to the project directory')
    
    # Optional arguments
    parser.add_argument('--team-type', choices=['single', 'dual', 'custom'], 
                        default=None, help='Team type (default: single)')
    parser.add_argument('--project-type', choices=['web_app', 'ecommerce', 'mobile_app', 'generic'], 
                        default=None, help='Project type (default: generic)')
    parser.add_argument('--lang', '--language', choices=['zh', 'en'], 
                        default='zh', help='Output language (default: zh)')
    
    # Custom members
    parser.add_argument('--internal-members', 
                        help='Comma-separated list of internal team members')
    parser.add_argument('--internet-members', 
                        help='Comma-separated list of internet team members')
    
    # Model configuration
    parser.add_argument('--primary-model', 
                        help='Primary AI model to use')
    parser.add_argument('--fallback-models', 
                        help='Comma-separated list of fallback models')
    
    # Logging
    parser.add_argument('--log-file', 
                        help='Path to log file')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_file)
    
    # Load and merge configuration
    script_dir = Path(__file__).parent
    default_config = load_default_config(script_dir)
    config = merge_configs(default_config, args)
    lang = config.get('lang', 'zh')
    
    # Print configuration
    print(t('creating', lang))
    print(f"  {t('project_path', lang)}: {args.project_path}")
    print(f"  {t('team_type', lang)}: {config['team_type']}")
    print(f"  {t('project_type', lang)}: {config['project_type']}")
    print(f"  {t('language', lang)}: {lang}")
    
    try:
        # Create AI team
        creator = AITeamCreator(args.project_path, config, lang)
        creator.create()
        
        print(f"\n✅ {t('success', lang)}")
        print(f"  {t('location', lang)}: {os.path.join(args.project_path, 'ai-team')}")
        
    except ProjectPathError as e:
        print(f"\n❌ {t('error_project_not_found', lang)}: {args.project_path}", file=sys.stderr)
        sys.exit(1)
    except ConfigurationError as e:
        print(f"\n❌ {t('error_config_invalid', lang)}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
