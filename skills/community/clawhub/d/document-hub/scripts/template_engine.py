"""
PRD 模板渲染引擎
支持 Jinja2 模板渲染，用于生成标准化的产品需求文档
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template


class TemplateEngine:
    """PRD 模板渲染引擎"""
    
    # 模板类型映射
    TEMPLATE_TYPES = {
        'base': 'base.md',
        'ai': 'ai-feature-prd.md',
        'ai-feature': 'ai-feature-prd.md',
        'api': 'api-prd.md',
        'data': 'data-product-prd.md',
        'data-product': 'data-product-prd.md',
        'platform': 'platform-prd.md'
    }
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初始化模板引擎
        
        Args:
            templates_dir: 模板目录路径，默认使用内置模板目录
        """
        if templates_dir is None:
            # 默认模板目录
            self.templates_dir = Path(__file__).parent.parent / 'templates' / 'prd'
        else:
            self.templates_dir = Path(templates_dir)
        
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # 添加自定义过滤器
        self.env.filters['date'] = self._filter_date
        self.env.filters['uppercase'] = lambda x: str(x).upper()
        self.env.filters['lowercase'] = lambda x: str(x).lower()
    
    def _filter_date(self, value: Any, format_str: str = '%Y-%m-%d') -> str:
        """日期格式化过滤器"""
        if isinstance(value, datetime):
            return value.strftime(format_str)
        return str(value)
    
    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        templates = []
        if self.templates_dir.exists():
            for f in self.templates_dir.glob('*.md'):
                templates.append(f.stem)
        return templates
    
    def get_template(self, template_type: str = 'base') -> Template:
        """
        获取指定类型的模板
        
        Args:
            template_type: 模板类型，可选值: base, ai, api, data, platform
            
        Returns:
            Jinja2 Template 对象
        """
        template_file = self.TEMPLATE_TYPES.get(template_type, 'base.md')
        return self.env.get_template(template_file)
    
    def render(self, template_type: str, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template_type: 模板类型
            context: 模板变量上下文
            
        Returns:
            渲染后的 Markdown 字符串
        """
        template = self.get_template(template_type)
        return template.render(**context)
    
    def render_to_file(self, template_type: str, context: Dict[str, Any], 
                       output_path: str) -> str:
        """
        渲染模板并保存到文件
        
        Args:
            template_type: 模板类型
            context: 模板变量上下文
            output_path: 输出文件路径
            
        Returns:
            输出文件的绝对路径
        """
        content = self.render(template_type, context)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        return str(output_path.absolute())
    
    def extract_placeholders(self, template_type: str = 'base') -> List[str]:
        """
        提取模板中的所有占位符变量
        
        Args:
            template_type: 模板类型
            
        Returns:
            占位符变量名列表
        """
        template = self.get_template(template_type)
        source = template.source
        
        # 匹配 Jinja2 变量 {{ variable }}
        pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}'
        matches = re.findall(pattern, source)
        
        return sorted(list(set(matches)))
    
    def generate_context_template(self, template_type: str = 'base') -> Dict[str, str]:
        """
        生成模板上下文示例（带注释）
        
        Args:
            template_type: 模板类型
            
        Returns:
            带示例值的上下文字典
        """
        placeholders = self.extract_placeholders(template_type)
        
        # 基础示例值
        examples = {
            'product_name': '智能客服系统',
            'version': '1.0.0',
            'create_date': datetime.now().strftime('%Y-%m-%d'),
            'update_date': datetime.now().strftime('%Y-%m-%d'),
            'author': '产品经理',
            'status': '草稿',
            'business_background': '当前客服团队面临大量重复性问题，需要AI辅助提升效率',
            'current_pain_points': '人工回复慢、成本高、7x24小时覆盖难',
            'target_user_persona': '客服人员、终端用户',
            'module_1': '智能问答',
            'feature_1_1': '自动回复',
            'desc_1_1': '基于知识库自动回答常见问题',
            'story_1_actor': '客服人员',
            'story_1_want': '系统自动回答常见问题',
            'story_1_benefit': '减少重复工作，专注复杂问题',
            'api_1_endpoint': '/api/v1/chat',
            'api_1_method': 'POST',
            'pm_count': '1',
            'fe_count': '2',
            'be_count': '2',
            'qa_count': '1'
        }
        
        context = {}
        for key in placeholders:
            context[key] = examples.get(key, f'{{请填写 {key}}}')
        
        return context


class PRDGenerator:
    """PRD 文档生成器"""
    
    def __init__(self, template_engine: Optional[TemplateEngine] = None):
        self.engine = template_engine or TemplateEngine()
    
    def create_prd(self, product_info: Dict[str, Any], 
                   template_type: str = 'base',
                   output_path: Optional[str] = None) -> str:
        """
        创建 PRD 文档
        
        Args:
            product_info: 产品信息字典
            template_type: 模板类型
            output_path: 输出路径，为 None 时返回内容字符串
            
        Returns:
            PRD 内容或文件路径
        """
        # 添加默认字段
        context = self._enrich_context(product_info)
        
        if output_path:
            return self.engine.render_to_file(template_type, context, output_path)
        else:
            return self.engine.render(template_type, context)
    
    def _enrich_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """丰富上下文，添加默认字段"""
        enriched = context.copy()
        
        # 添加时间戳
        now = datetime.now()
        if 'create_date' not in enriched:
            enriched['create_date'] = now.strftime('%Y-%m-%d')
        if 'update_date' not in enriched:
            enriched['update_date'] = now.strftime('%Y-%m-%d')
        
        # 添加默认版本
        if 'version' not in enriched:
            enriched['version'] = '1.0.0'
        
        # 添加默认状态
        if 'status' not in enriched:
            enriched['status'] = '草稿'
        
        return enriched
    
    def create_ai_feature_prd(self, ai_info: Dict[str, Any],
                              output_path: Optional[str] = None) -> str:
        """
        创建 AI 功能 PRD
        
        Args:
            ai_info: AI 功能信息
            output_path: 输出路径
            
        Returns:
            PRD 内容或文件路径
        """
        return self.create_prd(ai_info, 'ai-feature', output_path)
    
    def create_api_prd(self, api_info: Dict[str, Any],
                       output_path: Optional[str] = None) -> str:
        """
        创建 API 设计 PRD
        
        Args:
            api_info: API 信息
            output_path: 输出路径
            
        Returns:
            PRD 内容或文件路径
        """
        return self.create_prd(api_info, 'api', output_path)


def get_default_context(template_type: str = 'base') -> Dict[str, Any]:
    """
    获取默认的模板上下文
    
    Args:
        template_type: 模板类型
        
    Returns:
        默认上下文字典
    """
    engine = TemplateEngine()
    return engine.generate_context_template(template_type)


if __name__ == '__main__':
    # 测试代码
    engine = TemplateEngine()
    
    print("可用模板:")
    for t in engine.list_templates():
        print(f"  - {t}")
    
    print("\n基础模板占位符:")
    placeholders = engine.extract_placeholders('base')
    for p in placeholders[:10]:
        print(f"  - {p}")
    print(f"  ... 共 {len(placeholders)} 个")
