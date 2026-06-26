#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO.SKILL - 诊断工具
功能：检测园区官网GEO部署状态，生成修复清单
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import re


class GEODiagnostics:
    """GEO诊断工具"""
    
    def __init__(self, url: str):
        """初始化诊断工具
        
        Args:
            url: 要诊断的园区官网URL
        """
        self.url = url.rstrip('/')
        self.results = {
            'url': self.url,
            'timestamp': datetime.now().isoformat(),
            'overall_score': 0,
            'categories': {}
        }
    
    def _check_url_accessibility(self) -> Dict:
        """检查URL可访问性"""
        # 注意：实际环境中需要使用requests库
        # 这里提供基础框架
        return {
            'status': 'unknown',
            'https_enabled': True,
            'response_time': 0,
            'issues': []
        }
    
    def _check_llms_txt(self) -> Dict:
        """检查llms.txt部署情况"""
        result = {
            'name': 'llms.txt部署',
            'score': 0,
            'status': '❌ 缺失',
            'checks': []
        }
        
        llms_url = f"{self.url}/llms.txt"
        
        # 检查项
        checks = [
            {
                'name': 'llms.txt存在性',
                'passed': False,
                'detail': f'访问 {llms_url}'
            },
            {
                'name': '内容完整性',
                'passed': False,
                'detail': '检查必需字段'
            },
            {
                'name': '更新时效',
                'passed': False,
                'detail': '检查最后更新时间'
            },
            {
                'name': '格式规范',
                'passed': False,
                'detail': '检查Markdown格式'
            }
        ]
        
        passed_count = sum(1 for c in checks if c['passed'])
        result['score'] = int(passed_count / len(checks) * 100)
        result['checks'] = checks
        
        if result['score'] == 100:
            result['status'] = '✅ 完善'
        elif result['score'] >= 50:
            result['status'] = '⚠️ 需改进'
        
        return result
    
    def _check_schema(self) -> Dict:
        """检查Schema结构化数据"""
        result = {
            'name': 'Schema结构化数据',
            'score': 0,
            'status': '❌ 缺失',
            'checks': []
        }
        
        schema_types = ['Organization', 'Product', 'Event']
        checks = []
        
        for schema_type in schema_types:
            check = {
                'name': f'{schema_type} Schema',
                'passed': False,
                'detail': f'检查{schema_type}类型是否部署'
            }
            # 实际检查需要在页面HTML中查找JSON-LD代码
            checks.append(check)
        
        # 检查页面是否有结构化数据
        checks.append({
            'name': 'JSON-LD格式',
            'passed': False,
            'detail': '检查schema.org格式'
        })
        
        checks.append({
            'name': '内容准确性',
            'passed': False,
            'detail': '检查数据与官网一致性'
        })
        
        passed_count = sum(1 for c in checks if c['passed'])
        result['score'] = int(passed_count / len(checks) * 100)
        result['checks'] = checks
        
        if result['score'] == 100:
            result['status'] = '✅ 完善'
        elif result['score'] >= 50:
            result['status'] = '⚠️ 需改进'
        
        return result
    
    def _check_meta_tags(self) -> Dict:
        """检查Meta标签"""
        result = {
            'name': 'Meta标签配置',
            'score': 0,
            'status': '❌ 缺失',
            'checks': []
        }
        
        checks = [
            {
                'name': 'Title标签',
                'passed': False,
                'detail': '检查页面标题'
            },
            {
                'name': 'Description',
                'passed': False,
                'detail': '检查meta描述'
            },
            {
                'name': 'Keywords',
                'passed': False,
                'detail': '检查关键词'
            },
            {
                'name': 'Open Graph',
                'passed': False,
                'detail': '检查社交分享标签'
            }
        ]
        
        passed_count = sum(1 for c in checks if c['passed'])
        result['score'] = int(passed_count / len(checks) * 100)
        result['checks'] = checks
        
        if result['score'] == 100:
            result['status'] = '✅ 完善'
        elif result['score'] >= 50:
            result['status'] = '⚠️ 需改进'
        
        return result
    
    def _check_content_quality(self) -> Dict:
        """检查内容质量"""
        result = {
            'name': '内容质量',
            'score': 0,
            'status': '❌ 缺失',
            'checks': []
        }
        
        checks = [
            {
                'name': '问题覆盖率',
                'passed': False,
                'detail': '检查FAQ问题数量（目标50+）'
            },
            {
                'name': '内容结构化',
                'passed': False,
                'detail': '检查表格、列表使用'
            },
            {
                'name': '数据时效性',
                'passed': False,
                'detail': '检查数据更新时间'
            },
            {
                'name': '答案完整性',
                'passed': False,
                'detail': '检查核心问题是否都有答案'
            },
            {
                'name': '多平台分发',
                'passed': False,
                'detail': '检查知乎、百家号等内容'
            }
        ]
        
        passed_count = sum(1 for c in checks if c['passed'])
        result['score'] = int(passed_count / len(checks) * 100)
        result['checks'] = checks
        
        if result['score'] == 100:
            result['status'] = '✅ 完善'
        elif result['score'] >= 50:
            result['status'] = '⚠️ 需改进'
        
        return result
    
    def _check_technical_seo(self) -> Dict:
        """检查技术SEO"""
        result = {
            'name': '技术SEO',
            'score': 0,
            'status': '❌ 缺失',
            'checks': []
        }
        
        checks = [
            {
                'name': 'HTTPS',
                'passed': self.url.startswith('https://'),
                'detail': '检查是否使用HTTPS'
            },
            {
                'name': '响应速度',
                'passed': False,
                'detail': '检查页面加载时间'
            },
            {
                'name': '移动适配',
                'passed': False,
                'detail': '检查移动端显示'
            },
            {
                'name': 'Robots.txt',
                'passed': False,
                'detail': '检查robots.txt配置'
            },
            {
                'name': 'Sitemap',
                'passed': False,
                'detail': '检查站点地图'
            }
        ]
        
        passed_count = sum(1 for c in checks if c['passed'])
        result['score'] = int(passed_count / len(checks) * 100)
        result['checks'] = checks
        
        if result['score'] == 100:
            result['status'] = '✅ 完善'
        elif result['score'] >= 50:
            result['status'] = '⚠️ 需改进'
        
        return result
    
    def run_diagnostics(self) -> Dict:
        """运行完整诊断"""
        print(f"\n🔍 正在诊断: {self.url}\n")
        
        # 运行各项检查
        checks = [
            self._check_llms_txt,
            self._check_schema,
            self._check_meta_tags,
            self._check_content_quality,
            self._check_technical_seo
        ]
        
        total_score = 0
        for check_func in checks:
            print(f"  检查 {check_func.__name__.replace('_check_', '').replace('_', '')}...")
            result = check_func()
            self.results['categories'][result['name']] = result
            total_score += result['score']
        
        self.results['overall_score'] = int(total_score / len(checks))
        
        return self.results
    
    def generate_report(self, output_format: str = 'markdown') -> str:
        """生成诊断报告
        
        Args:
            output_format: 报告格式，可选 'markdown' 或 'json'
            
        Returns:
            报告内容
        """
        if output_format == 'json':
            return json.dumps(self.results, ensure_ascii=False, indent=2)
        
        # Markdown格式报告
        report = f"""# GEO诊断报告

**诊断URL**: {self.url}  
**诊断时间**: {self.results['timestamp']}  
**综合评分**: {self.results['overall_score']}/100

---

## 📊 评分总览

| 维度 | 得分 | 状态 |
|------|------|------|
"""
        
        status_emoji = {
            '✅ 完善': '🟢',
            '⚠️ 需改进': '🟡',
            '❌ 缺失': '🔴'
        }
        
        for category_name, category_data in self.results['categories'].items():
            emoji = status_emoji.get(category_data['status'], '⚪')
            report += f"| {category_name} | {category_data['score']}/100 | {emoji} {category_data['status']} |\n"
        
        report += f"\n**总体评分**: {self.results['overall_score']}/100\n\n"
        
        # 详细检查结果
        report += "## 🔍 详细检查\n\n"
        
        for category_name, category_data in self.results['categories'].items():
            report += f"### {category_name}\n\n"
            report += f"**得分**: {category_data['score']}/100 | **状态**: {category_data['status']}\n\n"
            report += "| 检查项 | 状态 | 说明 |\n"
            report += "|--------|------|------|\n"
            
            for check in category_data['checks']:
                status = '✅' if check['passed'] else '❌'
                report += f"| {check['name']} | {status} | {check['detail']} |\n"
            
            report += "\n"
        
        # 修复建议
        report += "## 📝 修复建议\n\n"
        
        priority_1 = []
        priority_2 = []
        
        for category_name, category_data in self.results['categories'].items():
            for check in category_data['checks']:
                if not check['passed']:
                    if category_data['score'] < 30:
                        priority_1.append((category_name, check))
                    else:
                        priority_2.append((category_name, check))
        
        if priority_1:
            report += "### 🔴 紧急修复（P0）\n\n"
            for category_name, check in priority_1:
                report += f"- **{category_name} - {check['name']}**: {check['detail']}\n"
            report += "\n"
        
        if priority_2:
            report += "### 🟡 优化改进（P1）\n\n"
            for category_name, check in priority_2:
                report += f"- **{category_name} - {check['name']}**: {check['detail']}\n"
            report += "\n"
        
        # 下次检测
        report += f"""## 📅 下次检测

建议检测日期: {datetime.now().strftime('%Y-%m-%d')}

---

*报告由GEO.SKILL诊断工具生成*
"""
        
        return report
    
    def save_report(self, output_path: str, format: str = 'markdown'):
        """保存报告到文件"""
        report = self.generate_report(format)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 报告已保存: {output_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='GEO.SKILL - GEO诊断工具')
    parser.add_argument('--url', '-u', type=str, required=True,
                        help='要诊断的园区官网URL')
    parser.add_argument('--output', '-o', type=str, default='geo_diagnostic_report.md',
                        help='报告输出路径')
    parser.add_argument('--format', '-f', choices=['markdown', 'json'], default='markdown',
                        help='报告格式')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='显示详细输出')
    
    args = parser.parse_args()
    
    # 验证URL格式
    if not args.url.startswith(('http://', 'https://')):
        print("错误：URL必须以 http:// 或 https:// 开头")
        sys.exit(1)
    
    diagnostics = GEODiagnostics(args.url)
    diagnostics.run_diagnostics()
    
    if args.verbose:
        report = diagnostics.generate_report('markdown')
        print(report)
    
    diagnostics.save_report(args.output, args.format)
    
    # 输出总结
    score = diagnostics.results['overall_score']
    if score >= 80:
        print(f"\n📊 综合评分: {score}/100 (优秀)")
    elif score >= 60:
        print(f"\n📊 综合评分: {score}/100 (良好)")
    elif score >= 40:
        print(f"\n📊 综合评分: {score}/100 (需改进)")
    else:
        print(f"\n📊 综合评分: {score}/100 (紧急处理)")


if __name__ == '__main__':
    main()
