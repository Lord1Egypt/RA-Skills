#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO.SKILL - llms.txt 生成器
功能：根据JSON数据一键生成符合规范的园区llms.txt文件
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path


class LLMsTxtGenerator:
    """llms.txt文件生成器"""
    
    def __init__(self, config_path: str):
        """初始化生成器
        
        Args:
            config_path: 园区配置文件路径(JSON格式)
        """
        self.config = self._load_config(config_path)
        self.template = self._load_template()
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"错误：配置文件 {config_path} 不存在")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"错误：配置文件 {config_path} 格式错误")
            sys.exit(1)
    
    def _load_template(self) -> str:
        """加载llms.txt模板"""
        template_path = Path(__file__).parent.parent / "templates" / "llms.txt"
        if template_path.exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """获取默认模板"""
        return """# {{PARK_NAME}}

## 关于我们
{{PARK_DESCRIPTION}}

## 核心产业
{{CORE_INDUSTRIES}}

## 产品类型
{{PRODUCT_TYPES}}

## 联系方式
- 地址：{{FULL_ADDRESS}}
- 电话：{{CONTACT_PHONE}}
- 邮箱：{{CONTACT_EMAIL}}
- 官网：{{WEBSITE_URL}}

## 最新动态
{{RECENT_NEWS}}

## 数据摘要
- 占地面积：{{TOTAL_LAND_AREA}}亩
- 入驻企业：{{COMPANY_COUNT}}家
- 年产值：{{ANNUAL_OUTPUT}}亿元
"""
    
    def _replace_placeholder(self, text: str, key: str, value) -> str:
        """替换占位符
        
        Args:
            text: 原始文本
            key: 占位符名称
            value: 替换值
        """
        placeholder = f"{{{{{key}}}}}"
        if value is None:
            return text.replace(placeholder, "待补充")
        if isinstance(value, list):
            return text.replace(placeholder, "、".join(str(v) for v in value))
        if isinstance(value, dict):
            result = text
            for k, v in value.items():
                result = self._replace_placeholder(result, k, v)
            return result
        return text.replace(placeholder, str(value))
    
    def _flatten_dict(self, d: dict, parent_key: str = '', sep: '_') -> dict:
        """扁平化字典"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def _process_config(self) -> str:
        """处理配置文件，生成llms.txt内容"""
        flat_config = self._flatten_dict(self.config)
        
        # 添加自动计算的字段
        if 'address' in self.config:
            addr = self.config['address']
            flat_config['FULL_ADDRESS'] = f"{addr.get('province', '')}{addr.get('city', '')}{addr.get('district', '')}{addr.get('street', '')}"
        
        # 添加当前日期
        flat_config['UPDATE_DATE'] = datetime.now().strftime('%Y-%m-%d')
        
        # 处理产品类型
        if 'products' in self.config:
            products = self.config['products']
            flat_config['PRODUCT_TYPES'] = '、'.join(p.get('name', '') for p in products)
        
        # 处理产业类型
        if 'industries' in self.config:
            flat_config['CORE_INDUSTRIES'] = '、'.join(self.config['industries'])
        
        # 生成内容
        content = self.template
        for key, value in flat_config.items():
            content = self._replace_placeholder(content, key, value)
        
        # 清理未替换的占位符
        import re
        content = re.sub(r'\{\{[^}]+\}\}', '', content)
        
        return content
    
    def generate(self, output_path: str = None) -> str:
        """生成llms.txt文件
        
        Args:
            output_path: 输出文件路径，默认为当前目录下的llms.txt
            
        Returns:
            生成的文件路径
        """
        content = self._process_config()
        
        if output_path is None:
            park_name = self.config.get('name', 'park')
            output_path = f"./{park_name}_llms.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ llms.txt 生成成功：{output_path}")
        return output_path
    
    def validate(self, file_path: str = None) -> dict:
        """验证llms.txt内容
        
        Args:
            file_path: 要验证的文件路径
            
        Returns:
            验证结果字典
        """
        if file_path is None:
            park_name = self.config.get('name', 'park')
            file_path = f"./{park_name}_llms.txt"
        
        result = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            result['valid'] = False
            result['issues'].append(f"文件不存在：{file_path}")
            return result
        
        # 检查基本内容
        required_sections = ['联系方式', '关于我们', '核心产业']
        for section in required_sections:
            if section not in content:
                result['warnings'].append(f"缺少推荐章节：{section}")
        
        # 检查关键信息
        key_fields = ['电话', '邮箱', '官网']
        for field in key_fields:
            if field not in content:
                result['issues'].append(f"缺少关键信息：{field}")
        
        # 检查字符数
        if len(content) > 50000:
            result['warnings'].append("内容超过50000字符，建议精简")
        
        # 检查是否有过时占位符
        import re
        if re.search(r'\{\{[^}]+\}\}', content):
            result['issues'].append("存在未替换的占位符")
        
        result['valid'] = len(result['issues']) == 0
        return result


def create_sample_config(output_path: str = "park_config.json"):
    """创建示例配置文件"""
    sample_config = {
        "name": "苏州生物医药创新园",
        "alternate_names": ["苏州生物园", "SZBioMed"],
        "description": "苏州市重点打造的生物医药产业专业园区，位于苏州工业园区，集研发、生产、办公于一体。",
        "positioning": "生物医药、基因技术、医疗器械",
        
        "address": {
            "province": "江苏省",
            "city": "苏州市",
            "district": "苏州工业园区",
            "street": "星湖街328号",
            "postal_code": "215000"
        },
        
        "contact": {
            "phone": "0512-8888-8888",
            "email": "info@example.cn",
            "website": "https://www.example.cn",
            "hotline": "400-888-8888"
        },
        
        "industries": ["生物医药", "基因技术", "医疗器械"],
        
        "products": [
            {"name": "研发办公楼", "area_range": "200-2000㎡", "price_range": "2.8-3.5元/㎡/天"},
            {"name": "标准厂房", "area_range": "500-5000㎡", "price_range": "2.0-2.8元/㎡/天"},
            {"name": "GMP车间", "area_range": "300-3000㎡", "price_range": "面议"}
        ],
        
        "stats": {
            "total_land_area": 200,
            "total_building_area": 500000,
            "company_count": 86,
            "annual_output": 120,
            "concentration_rate": 92
        },
        
        "policies": {
            "tax_incentive": "企业所得税前3年免征，后3年减半",
            "rent_incentive": "初创企业首年租金减免50%",
            "talent_policy": "高层次人才购房补贴最高500万元"
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 示例配置文件已创建：{output_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GEO.SKILL - llms.txt生成器')
    parser.add_argument('--config', '-c', type=str, default='park_config.json',
                        help='园区配置文件路径(JSON格式)')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='输出文件路径')
    parser.add_argument('--validate', '-v', action='store_true',
                        help='验证生成的llms.txt')
    parser.add_argument('--sample', '-s', action='store_true',
                        help='创建示例配置文件')
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_config()
        return
    
    if not Path(args.config).exists():
        print(f"配置文件不存在，正在创建示例...")
        create_sample_config()
        print(f"请编辑 park_config.json 后重新运行")
        return
    
    generator = LLMsTxtGenerator(args.config)
    output_path = generator.generate(args.output)
    
    if args.validate:
        result = generator.validate(output_path)
        print("\n📋 验证结果：")
        print(f"  状态：{'✅ 通过' if result['valid'] else '❌ 失败'}")
        if result['issues']:
            print("  问题：")
            for issue in result['issues']:
                print(f"    - {issue}")
        if result['warnings']:
            print("  警告：")
            for warning in result['warnings']:
                print(f"    - {warning}")


if __name__ == '__main__':
    main()
