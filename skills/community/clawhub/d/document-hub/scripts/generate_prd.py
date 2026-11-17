#!/usr/bin/env python3
"""
PRD 生成工作流
集成飞书文档创建功能，实现从模板到飞书文档的完整流程
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from template_engine import TemplateEngine, PRDGenerator


class FeishuDocIntegration:
    """飞书文档集成"""
    
    def __init__(self):
        self.enabled = self._check_feishu_available()
    
    def _check_feishu_available(self) -> bool:
        """检查飞书工具是否可用"""
        try:
            # 尝试导入飞书工具
            import importlib.util
            spec = importlib.util.find_spec('feishu_create_doc')
            return spec is not None
        except Exception:
            return False
    
    def create_doc(self, title: str, markdown: str, 
                   folder_token: Optional[str] = None,
                   wiki_node: Optional[str] = None) -> Dict[str, Any]:
        """
        创建飞书文档
        
        Args:
            title: 文档标题
            markdown: Markdown 内容
            folder_token: 文件夹 token（可选）
            wiki_node: 知识库节点 token（可选）
            
        Returns:
            创建结果，包含文档 URL
        """
        if not self.enabled:
            return {
                'success': False,
                'error': '飞书工具不可用，请检查配置'
            }
        
        try:
            # 这里调用实际的 feishu_create_doc 工具
            # 由于是在 OpenClaw 环境中，实际调用由主 Agent 处理
            return {
                'success': True,
                'message': '请使用 feishu_create_doc 工具创建文档',
                'title': title,
                'content_length': len(markdown)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


class PRDWorkflow:
    """PRD 生成工作流"""
    
    def __init__(self):
        self.generator = PRDGenerator()
        self.feishu = FeishuDocIntegration()
    
    def generate(self, 
                 product_info: Dict[str, Any],
                 template_type: str = 'base',
                 output_format: str = 'markdown',
                 output_path: Optional[str] = None,
                 feishu_title: Optional[str] = None,
                 feishu_folder: Optional[str] = None) -> Dict[str, Any]:
        """
        生成 PRD 文档
        
        Args:
            product_info: 产品信息字典
            template_type: 模板类型 (base/ai-feature/api/data/platform)
            output_format: 输出格式 (markdown/feishu/both)
            output_path: 本地输出路径
            feishu_title: 飞书文档标题
            feishu_folder: 飞书文件夹 token
            
        Returns:
            生成结果字典
        """
        result = {
            'success': True,
            'template_type': template_type,
            'timestamp': datetime.now().isoformat(),
            'outputs': {}
        }
        
        # 1. 生成 PRD 内容
        try:
            prd_content = self.generator.create_prd(product_info, template_type)
            result['outputs']['content'] = {
                'length': len(prd_content),
                'preview': prd_content[:500] + '...' if len(prd_content) > 500 else prd_content
            }
        except Exception as e:
            result['success'] = False
            result['error'] = f'生成 PRD 失败: {str(e)}'
            return result
        
        # 2. 保存到本地文件
        if output_path or output_format in ('markdown', 'both'):
            if not output_path:
                # 生成默认文件名
                product_name = product_info.get('product_name', 'untitled')
                output_path = f"{product_name}_PRD.md"
            
            try:
                file_path = self.generator.engine.render_to_file(
                    template_type, 
                    self.generator._enrich_context(product_info),
                    output_path
                )
                result['outputs']['file'] = {
                    'path': file_path,
                    'size': os.path.getsize(file_path)
                }
            except Exception as e:
                result['outputs']['file_error'] = str(e)
        
        # 3. 创建飞书文档
        if output_format in ('feishu', 'both'):
            title = feishu_title or product_info.get('product_name', 'PRD') + ' - 产品需求文档'
            feishu_result = self.feishu.create_doc(
                title=title,
                markdown=prd_content,
                folder_token=feishu_folder
            )
            result['outputs']['feishu'] = feishu_result
        
        return result
    
    def interactive_generate(self):
        """交互式生成 PRD"""
        print("=" * 60)
        print("PRD 文档生成器")
        print("=" * 60)
        
        # 选择模板类型
        print("\n请选择 PRD 类型:")
        templates = {
            '1': ('base', '基础 PRD'),
            '2': ('ai-feature', 'AI 功能 PRD'),
            '3': ('api', 'API 设计 PRD'),
            '4': ('data', '数据产品 PRD'),
            '5': ('platform', '平台产品 PRD')
        }
        
        for key, (value, name) in templates.items():
            print(f"  {key}. {name}")
        
        choice = input("\n选择 (1-5): ").strip() or '1'
        template_type = templates.get(choice, ('base', '基础 PRD'))[0]
        
        # 获取模板占位符
        placeholders = self.generator.engine.extract_placeholders(template_type)
        
        print(f"\n已选择: {templates.get(choice, ('base', '基础 PRD'))[1]}")
        print(f"需要填写 {len(placeholders)} 个字段")
        print("-" * 60)
        
        # 收集必要信息
        context = {}
        
        # 必填字段
        print("\n【基础信息】")
        context['product_name'] = input("产品名称: ").strip()
        context['version'] = input("版本号 (默认 1.0.0): ").strip() or '1.0.0'
        context['author'] = input("作者: ").strip() or '产品经理'
        
        # 根据模板类型收集特定信息
        if template_type == 'ai-feature':
            print("\n【AI 功能信息】")
            context['ai_capability_type'] = input("AI 能力类型 (LLM/VLM/Agent): ").strip() or 'LLM'
            context['core_function'] = input("核心功能描述: ").strip()
            context['selected_model'] = input("选定模型: ").strip() or 'GPT-4'
        
        elif template_type == 'api':
            print("\n【API 信息】")
            context['api_name'] = input("API 名称: ").strip()
            context['base_url'] = input("Base URL: ").strip() or 'https://api.example.com'
        
        # 生成 PRD
        print("\n" + "=" * 60)
        print("正在生成 PRD...")
        
        output_path = f"{context['product_name']}_PRD.md"
        result = self.generate(
            product_info=context,
            template_type=template_type,
            output_format='markdown',
            output_path=output_path
        )
        
        if result['success']:
            print(f"✅ PRD 生成成功!")
            if 'file' in result['outputs']:
                print(f"📄 文件路径: {result['outputs']['file']['path']}")
            print(f"📊 内容长度: {result['outputs']['content']['length']} 字符")
        else:
            print(f"❌ 生成失败: {result.get('error', '未知错误')}")
        
        return result


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='PRD 文档生成工具')
    parser.add_argument('--template', '-t', default='base',
                        choices=['base', 'ai-feature', 'api', 'data', 'platform'],
                        help='模板类型')
    parser.add_argument('--input', '-i', help='输入 JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--feishu', '-f', action='store_true',
                        help='同时创建飞书文档')
    parser.add_argument('--interactive', '-I', action='store_true',
                        help='交互式模式')
    
    args = parser.parse_args()
    
    workflow = PRDWorkflow()
    
    if args.interactive:
        workflow.interactive_generate()
        return
    
    # 从文件或命令行读取输入
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            product_info = json.load(f)
    else:
        # 使用默认示例
        product_info = {
            'product_name': '示例产品',
            'version': '1.0.0',
            'author': '产品经理'
        }
    
    # 生成 PRD
    result = workflow.generate(
        product_info=product_info,
        template_type=args.template,
        output_format='both' if args.feishu else 'markdown',
        output_path=args.output
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
