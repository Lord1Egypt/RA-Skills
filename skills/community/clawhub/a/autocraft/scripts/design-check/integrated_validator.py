#!/usr/bin/env python3
"""
集成验证器：结合架构检查 + 设计文档对照
用于验证子代理的完整验证流程
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# 添加父目录到路径，以便导入其他模块
sys.path.append(str(Path(__file__).parent.parent))

from architecture_check.architecture_check import ArchitectureChecker
from design_document_check import DesignDocumentChecker
from api_verification import APIVerifier
from database_mapping import DatabaseMappingVerifier

logger = logging.getLogger(__name__)

class IntegratedValidator:
    """集成验证器：架构检查 + 设计文档对照"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.architecture_checker = ArchitectureChecker(project_path)
        self.design_checker = DesignDocumentChecker(project_path)
        self.api_verifier = APIVerifier()
        self.db_verifier = DatabaseMappingVerifier()
        
        self.issues = []
        self.design_docs_loaded = False
    
    def load_design_documents(self, design_docs: Dict[str, str]) -> bool:
        """加载设计文档"""
        try:
            for doc_type, doc_path in design_docs.items():
                if doc_type == 'api_design':
                    self.api_verifier.load_api_design(str(self.project_path / doc_path))
                elif doc_type == 'database_design':
                    self.db_verifier.load_database_design(str(self.project_path / doc_path))
                else:
                    self.design_checker.load_design_document(doc_type, doc_path)
            
            self.design_docs_loaded = True
            logger.info(f"设计文档加载成功: {list(design_docs.keys())}")
            return True
            
        except Exception as e:
            logger.error(f"加载设计文档失败: {str(e)}")
            return False
    
    def run_architecture_check(self, code_files: List[str]) -> Dict[str, Any]:
        """运行架构检查"""
        logger.info(f"运行架构检查: {len(code_files)}个文件")
        
        # 运行架构检查
        architecture_results = self.architecture_checker.run_checks()
        
        # 提取架构问题
        architecture_issues = []
        for file_result in architecture_results.get('srp_checks', []):
            for issue in file_result.get('issues', []):
                if issue.get('severity') == 'HIGH':
                    architecture_issues.append({
                        'type': 'ARCHITECTURE_' + issue['type'],
                        'file': issue['file'],
                        'description': issue['description'],
                        'severity': issue['severity']
                    })
        
        return {
            'success': architecture_results['summary']['high_severity'] == 0,
            'issues': architecture_issues,
            'summary': architecture_results['summary']
        }
    
    def run_design_check(self, code_files: List[str], design_docs: Dict[str, str]) -> Dict[str, Any]:
        """运行设计文档对照检查"""
        if not self.design_docs_loaded:
            if not self.load_design_documents(design_docs):
                return {
                    'success': False,
                    'error': '设计文档加载失败',
                    'issues': []
                }
        
        logger.info(f"运行设计文档对照检查: {len(code_files)}个文件")
        
        # 运行设计文档检查
        design_results = self.design_checker.run_checks(
            code_files=[str(self.project_path / f) if not os.path.isabs(f) else f for f in code_files],
            design_docs=design_docs
        )
        
        # 提取设计文档问题
        design_issues = []
        for issue in design_results.get('issues', []):
            design_issues.append({
                'type': 'DESIGN_' + issue['type'],
                'file': issue['file'],
                'description': issue['description'],
                'severity': issue['severity']
            })
        
        return {
            'success': design_results['summary']['high_severity'] == 0,
            'issues': design_issues,
            'summary': design_results['summary']
        }
    
    def run_api_verification(self, api_code_files: List[str], api_design_path: str) -> Dict[str, Any]:
        """运行API接口验证"""
        logger.info(f"运行API接口验证: {len(api_code_files)}个文件")
        
        # 运行API验证
        api_results = self.api_verifier.verify_api_endpoints(
            design_path=str(self.project_path / api_design_path),
            code_paths=[str(self.project_path / f) if not os.path.isabs(f) else f for f in api_code_files]
        )
        
        # 提取API问题
        api_issues = []
        for issue in api_results.get('issues', []):
            api_issues.append({
                'type': 'API_' + issue['type'],
                'description': issue['description'],
                'severity': issue['severity']
            })
        
        return {
            'success': api_results['summary']['high_severity_issues'] == 0,
            'issues': api_issues,
            'summary': api_results['summary']
        }
    
    def run_database_verification(self, model_files: List[str], db_design_path: str) -> Dict[str, Any]:
        """运行数据库映射验证"""
        logger.info(f"运行数据库映射验证: {len(model_files)}个文件")
        
        # 运行数据库验证
        db_results = self.db_verifier.verify_database_mapping(
            design_path=str(self.project_path / db_design_path),
            code_paths=[str(self.project_path / f) if not os.path.isabs(f) else f for f in model_files]
        )
        
        # 提取数据库问题
        db_issues = []
        for issue in db_results.get('issues', []):
            db_issues.append({
                'type': 'DATABASE_' + issue['type'],
                'description': issue['description'],
                'severity': issue['severity']
            })
        
        return {
            'success': db_results['summary']['high_severity_issues'] == 0,
            'issues': db_issues,
            'summary': db_results['summary']
        }
    
    def run_comprehensive_validation(self, 
                                   code_files: List[str], 
                                   design_docs: Dict[str, str],
                                   api_code_files: Optional[List[str]] = None,
                                   model_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """运行全面的验证"""
        logger.info("开始全面验证...")
        
        all_issues = []
        dimension_results = {}
        
        # 1. 架构检查
        logger.info("1. 运行架构检查...")
        arch_results = self.run_architecture_check(code_files)
        dimension_results['架构合理性'] = 'PASS' if arch_results['success'] else 'FAIL'
        all_issues.extend(arch_results['issues'])
        
        # 2. 设计文档对照检查
        logger.info("2. 运行设计文档对照检查...")
        design_results = self.run_design_check(code_files, design_docs)
        dimension_results['设计一致性'] = 'PASS' if design_results['success'] else 'FAIL'
        all_issues.extend(design_results['issues'])
        
        # 3. API接口验证（如果提供了API设计文档和API代码文件）
        if 'api_design' in design_docs and api_code_files:
            logger.info("3. 运行API接口验证...")
            api_results = self.run_api_verification(api_code_files, design_docs['api_design'])
            dimension_results['API一致性'] = 'PASS' if api_results['success'] else 'FAIL'
            all_issues.extend(api_results['issues'])
        else:
            dimension_results['API一致性'] = 'SKIP'
        
        # 4. 数据库映射验证（如果提供了数据库设计文档和模型文件）
        if 'database_design' in design_docs and model_files:
            logger.info("4. 运行数据库映射验证...")
            db_results = self.run_database_verification(model_files, design_docs['database_design'])
            dimension_results['数据库一致性'] = 'PASS' if db_results['success'] else 'FAIL'
            all_issues.extend(db_results['issues'])
        else:
            dimension_results['数据库一致性'] = 'SKIP'
        
        # 计算总体结果
        high_severity_issues = [issue for issue in all_issues if issue['severity'] == 'HIGH']
        verification_success = len(high_severity_issues) == 0
        
        # 生成验证报告
        verification_report = self._generate_report(
            dimension_results, 
            all_issues,
            arch_results.get('summary', {}),
            design_results.get('summary', {}),
            api_results.get('summary', {}) if 'api_results' in locals() else {},
            db_results.get('summary', {}) if 'db_results' in locals() else {}
        )
        
        # 生成改进建议
        improvements_suggested = self._generate_improvements(all_issues)
        
        return {
            'verification_success': verification_success,
            'verification_report': verification_report,
            'dimension_results': dimension_results,
            'issues_found': [issue['description'] for issue in high_severity_issues],
            'improvements_suggested': improvements_suggested,
            'detailed_issues': all_issues,
            'summary': {
                'total_issues': len(all_issues),
                'high_severity_issues': len(high_severity_issues),
                'architecture_issues': len(arch_results['issues']),
                'design_issues': len(design_results['issues']),
                'api_issues': len(api_results.get('issues', [])) if 'api_results' in locals() else 0,
                'database_issues': len(db_results.get('issues', [])) if 'db_results' in locals() else 0
            }
        }
    
    def _generate_report(self, dimension_results: Dict[str, str], 
                        issues: List[Dict[str, Any]],
                        arch_summary: Dict[str, Any],
                        design_summary: Dict[str, Any],
                        api_summary: Dict[str, Any],
                        db_summary: Dict[str, Any]) -> str:
        """生成验证报告"""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("集成验证报告")
        report_lines.append("=" * 80)
        
        # 维度检查结果
        report_lines.append("\n📊 维度检查结果:")
        for dimension, result in dimension_results.items():
            status_icon = "✅" if result == 'PASS' else "❌" if result == 'FAIL' else "⚠️"
            report_lines.append(f"   {status_icon} {dimension}: {result}")
        
        # 问题汇总
        if issues:
            report_lines.append("\n🔍 发现问题汇总:")
            
            # 按类型分组
            issue_types = {}
            for issue in issues:
                issue_type = issue['type']
                if issue_type not in issue_types:
                    issue_types[issue_type] = []
                issue_types[issue_type].append(issue)
            
            for issue_type, type_issues in issue_types.items():
                severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
                for issue in type_issues:
                    severity_counts[issue['severity']] += 1
                
                report_lines.append(f"\n   {issue_type}:")
                for severity, count in severity_counts.items():
                    if count > 0:
                        severity_icon = '❌' if severity == 'HIGH' else '⚠️' if severity == 'MEDIUM' else 'ℹ️'
                        report_lines.append(f"     {severity_icon} {severity}: {count}个")
        
        # 详细统计
        report_lines.append("\n📈 详细统计:")
        report_lines.append(f"   架构检查: {arch_summary.get('issues_found', 0)}个问题 ({arch_summary.get('high_severity', 0)}高危)")
        report_lines.append(f"   设计文档对照: {design_summary.get('total_issues', 0)}个问题 ({design_summary.get('high_severity', 0)}高危)")
        
        if api_summary:
            report_lines.append(f"   API接口验证: {api_summary.get('total_issues', 0)}个问题 ({api_summary.get('high_severity_issues', 0)}高危)")
            report_lines.append(f"   API覆盖率: {api_summary.get('coverage_percentage', 0)}%")
        
        if db_summary:
            report_lines.append(f"   数据库映射: {db_summary.get('total_issues', 0)}个问题 ({db_summary.get('high_severity_issues', 0)}高危)")
            report_lines.append(f"   表覆盖率: {db_summary.get('table_coverage_percentage', 0)}%")
        
        # 总体结论
        report_lines.append("\n🎯 总体结论:")
        high_severity_count = sum(1 for issue in issues if issue['severity'] == 'HIGH')
        if high_severity_count == 0:
            report_lines.append("   ✅ 验证通过：未发现高危问题")
        else:
            report_lines.append(f"   ❌ 验证失败：发现{high_severity_count}个高危问题")
        
        return "\n".join(report_lines)
    
    def _generate_improvements(self, issues: List[Dict[str, Any]]) -> List[str]:
        """生成改进建议"""
        improvements = []
        
        # 按问题类型统计
        issue_categories = {}
        for issue in issues:
            category = issue['type'].split('_')[0]  # ARCHITECTURE, DESIGN, API, DATABASE
            if category not in issue_categories:
                issue_categories[category] = []
            issue_categories[category].append(issue)
        
        # 生成分类建议
        if 'ARCHITECTURE' in issue_categories:
            improvements.append("1. 重构代码架构，遵循单一职责原则")
            improvements.append("2. 拆分职责混淆的文件，分离路由、服务、数据访问层")
        
        if 'DESIGN' in issue_categories:
            improvements.append("3. 对照设计文档，确保功能实现完整")
            improvements.append("4. 检查设计文档中的功能是否全部实现")
        
        if 'API' in issue_categories:
            improvements.append("5. 修正API接口，确保与设计文档一致")
            improvements.append("6. 检查HTTP方法、路径、参数是否符合设计")
        
        if 'DATABASE' in issue_categories:
            improvements.append("7. 修正数据模型，确保与数据库设计一致")
            improvements.append("8. 检查字段类型、约束、关系是否正确")
        
        # 如果没有问题，给出肯定
        if not issues:
            improvements.append("代码质量优秀，继续保持！")
        
        return improvements


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='集成验证器：架构检查 + 设计文档对照')
    parser.add_argument('--project', required=True, help='项目根目录路径')
    parser.add_argument('--code', required=True, nargs='+', help='要检查的代码文件路径')
    parser.add_argument('--api-design', help='API设计文档路径（相对于项目根目录）')
    parser.add_argument('--func-design', help='系统功能设计文档路径（相对于项目根目录）')
    parser.add_argument('--db-design', help='数据库设计文档路径（相对于项目根目录）')
    parser.add_argument('--prd', help='PRD文档路径（相对于项目根目录）')
    parser.add_argument('--api-code', nargs='+', help='API代码文件路径（相对于项目根目录）')
    parser.add_argument('--model-code', nargs='+', help='数据模型代码文件路径（相对于项目根目录）')
    parser.add_argument('--report', help='JSON报告输出路径')
    parser.add_argument('--verbose', action='store_true', help='显示详细输出')
    
    args = parser.parse_args()
    
    # 设置日志
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 准备设计文档映射
    design_docs = {}
    if args.api_design:
        design_docs['api_design'] = args.api_design
    if args.func_design:
        design_docs['system_function_design'] = args.func_design
    if args.db_design:
        design_docs['database_design'] = args.db_design
    if args.prd:
        design_docs['prd'] = args.prd
    
    # 运行集成验证
    validator = IntegratedValidator(args.project)
    result = validator.run_comprehensive_validation(
        code_files=args.code,
        design_docs=design_docs,
        api_code_files=args.api_code,
        model_files=args.model_code
    )
    
    # 输出报告
    print(result['verification_report'])
    
    # 输出JSON结果（验证子代理格式）
    print("\n" + "=" * 80)
    print("验证结果JSON:")
    print(json.dumps({
        'verification_success': result['verification_success'],
        'verification_report': result['verification_report'],
        'dimension_results': result['dimension_results'],
        'issues_found': result['issues_found'],
        'improvements_suggested': result['improvements_suggested']
    }, ensure_ascii=False, indent=2))
    
    # 保存JSON报告
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n📄 JSON报告已保存到: {args.report}")
    
    return 0 if result['verification_success'] else 1


if __name__ == '__main__':
    exit(main())