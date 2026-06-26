#!/usr/bin/env python3
"""
设计文档对照验证工具
用于验证代码是否严格遵循设计文档

功能：
1. 解析设计文档（API设计、系统功能设计、数据库设计）
2. 对照代码文件，检查功能实现完整性
3. 验证API接口、数据库字段与设计文档的一致性
4. 生成验证报告
"""

import os
import re
import json
import logging
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DesignDocumentChecker:
    """设计文档对照检查器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.design_docs = {}
        self.issues = []
        
    def load_design_document(self, doc_type: str, doc_path: str) -> bool:
        """加载设计文档"""
        try:
            full_path = self.project_path / doc_path
            if not full_path.exists():
                logger.error(f"设计文档不存在: {full_path}")
                return False
                
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.design_docs[doc_type] = {
                'path': str(full_path),
                'content': content,
                'parsed': self._parse_design_document(doc_type, content)
            }
            
            logger.info(f"加载设计文档成功: {doc_type} ({doc_path})")
            return True
            
        except Exception as e:
            logger.error(f"加载设计文档失败 {doc_type}: {str(e)}")
            return False
    
    def _parse_design_document(self, doc_type: str, content: str) -> Dict[str, Any]:
        """解析设计文档内容"""
        parsed = {}
        
        if doc_type == 'api_design':
            parsed = self._parse_api_design(content)
        elif doc_type == 'system_function_design':
            parsed = self._parse_system_function_design(content)
        elif doc_type == 'database_design':
            parsed = self._parse_database_design(content)
        elif doc_type == 'prd':
            parsed = self._parse_prd(content)
            
        return parsed
    
    def _parse_api_design(self, content: str) -> Dict[str, Any]:
        """解析API设计文档"""
        parsed = {
            'modules': {},
            'endpoints': [],
            'total_endpoints': 0
        }
        
        # 提取模块信息
        module_pattern = r'##\s*(\d+\.\d+)\s*([^\n]+)'
        modules = re.findall(module_pattern, content)
        
        for module_num, module_name in modules:
            parsed['modules'][module_num] = {
                'name': module_name.strip(),
                'endpoints': []
            }
        
        # 提取API端点
        endpoint_pattern = r'###\s*(\d+\.\d+\.\d+)\s*([^\n]+)\s*\n.*?\n\*\*请求路径\*\*:\s*`([^`]+)`'
        endpoints = re.findall(endpoint_pattern, content, re.DOTALL)
        
        for endpoint_num, endpoint_name, endpoint_path in endpoints:
            # 提取HTTP方法
            method_match = re.search(r'\*\*请求方法\*\*:\s*`([^`]+)`', content)
            method = method_match.group(1) if method_match else 'UNKNOWN'
            
            # 提取功能ID
            func_id_match = re.search(r'\*\*功能ID\*\*:\s*`([^`]+)`', content)
            func_id = func_id_match.group(1) if func_id_match else ''
            
            endpoint_info = {
                'id': endpoint_num,
                'name': endpoint_name.strip(),
                'path': endpoint_path.strip(),
                'method': method,
                'function_id': func_id
            }
            
            parsed['endpoints'].append(endpoint_info)
            
            # 添加到对应模块
            module_num = endpoint_num.rsplit('.', 1)[0]
            if module_num in parsed['modules']:
                parsed['modules'][module_num]['endpoints'].append(endpoint_info)
        
        parsed['total_endpoints'] = len(parsed['endpoints'])
        return parsed
    
    def _parse_system_function_design(self, content: str) -> Dict[str, Any]:
        """解析系统功能设计文档"""
        parsed = {
            'functions': {},
            'total_functions': 0
        }
        
        # 提取功能定义
        # 格式：### F-001: 功能名称
        function_pattern = r'###\s*(F-\d+):\s*([^\n]+)'
        functions = re.findall(function_pattern, content)
        
        for func_id, func_name in functions:
            # 提取功能描述
            desc_pattern = rf'###\s*{re.escape(func_id)}:[^\n]+\n(.*?)(?=###|\Z)'
            desc_match = re.search(desc_pattern, content, re.DOTALL)
            
            func_desc = desc_match.group(1).strip() if desc_match else ''
            
            # 提取功能职责
            responsibilities = []
            resp_pattern = r'-\s*([^\n]+)'
            if desc_match:
                responsibilities = re.findall(resp_pattern, desc_match.group(1))
            
            parsed['functions'][func_id] = {
                'name': func_name.strip(),
                'description': func_desc,
                'responsibilities': responsibilities
            }
        
        parsed['total_functions'] = len(parsed['functions'])
        return parsed
    
    def _parse_database_design(self, content: str) -> Dict[str, Any]:
        """解析数据库设计文档"""
        parsed = {
            'tables': {},
            'total_tables': 0
        }
        
        # 提取表定义
        # 格式：### 表名 (table_name)
        table_pattern = r'###\s*([^\n]+)\s*\(([^)]+)\)'
        tables = re.findall(table_pattern, content)
        
        for table_name, table_code in tables:
            # 提取表描述
            desc_pattern = rf'###\s*{re.escape(table_name)}[^\n]+\n(.*?)(?=###|\Z)'
            desc_match = re.search(desc_pattern, content, re.DOTALL)
            
            table_desc = desc_match.group(1).strip() if desc_match else ''
            
            # 提取字段定义
            fields = []
            field_pattern = r'\|\s*(\w+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
            if desc_match:
                fields = re.findall(field_pattern, desc_match.group(1))
            
            parsed['tables'][table_code] = {
                'name': table_name.strip(),
                'description': table_desc,
                'fields': [
                    {
                        'name': field[0].strip(),
                        'type': field[1].strip(),
                        'constraint': field[2].strip(),
                        'description': field[3].strip()
                    }
                    for field in fields
                ]
            }
        
        parsed['total_tables'] = len(parsed['tables'])
        return parsed
    
    def _parse_prd(self, content: str) -> Dict[str, Any]:
        """解析PRD文档"""
        parsed = {
            'requirements': [],
            'total_requirements': 0
        }
        
        # 提取功能需求
        req_pattern = r'###\s*(\d+\.\d+)\s*([^\n]+)'
        requirements = re.findall(req_pattern, content)
        
        for req_num, req_name in requirements:
            parsed['requirements'].append({
                'id': req_num,
                'name': req_name.strip()
            })
        
        parsed['total_requirements'] = len(parsed['requirements'])
        return parsed
    
    def check_code_against_design(self, code_file_path: str) -> List[Dict[str, Any]]:
        """检查代码文件是否符合设计文档"""
        issues = []
        
        try:
            with open(code_file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # 根据文件类型进行不同的检查
            if 'router' in str(code_file_path).lower() or 'api' in str(code_file_path).lower():
                issues.extend(self._check_api_endpoints(code_file_path, code_content))
            elif 'service' in str(code_file_path).lower():
                issues.extend(self._check_service_functions(code_file_path, code_content))
            elif 'model' in str(code_file_path).lower() or 'schema' in str(code_file_path).lower():
                issues.extend(self._check_data_models(code_file_path, code_content))
            
        except Exception as e:
            logger.error(f"检查代码文件失败 {code_file_path}: {str(e)}")
            issues.append({
                'type': 'ERROR',
                'file': code_file_path,
                'description': f"检查代码文件失败: {str(e)}",
                'severity': 'HIGH'
            })
        
        return issues
    
    def _check_api_endpoints(self, file_path: str, code_content: str) -> List[Dict[str, Any]]:
        """检查API端点是否符合设计文档"""
        issues = []
        
        if 'api_design' not in self.design_docs:
            logger.warning(f"缺少API设计文档，跳过API端点检查: {file_path}")
            return issues
        
        api_design = self.design_docs['api_design']['parsed']
        
        # 从代码中提取API端点
        # FastAPI路由模式：@router.get("/api/path")
        endpoint_patterns = [
            r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
            r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
            r'@APIRouter\(.*?\)[\s\S]*?@.*?\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
        ]
        
        found_endpoints = []
        for pattern in endpoint_patterns:
            matches = re.findall(pattern, code_content, re.DOTALL)
            for method, path in matches:
                found_endpoints.append({
                    'method': method.upper(),
                    'path': path.strip(),
                    'file': str(file_path)
                })
        
        # 检查设计文档中的端点是否都在代码中实现
        for endpoint in api_design['endpoints']:
            design_path = endpoint['path']
            design_method = endpoint['method']
            
            # 查找匹配的端点
            matched = False
            for found in found_endpoints:
                # 简单的路径匹配（可以改进为更复杂的匹配逻辑）
                if (design_path in found['path'] or found['path'] in design_path) and \
                   design_method.upper() == found['method']:
                    matched = True
                    break
            
            if not matched:
                issues.append({
                    'type': 'MISSING_ENDPOINT',
                    'file': str(file_path),
                    'description': f"设计文档中的API端点未实现: {design_method} {design_path} (功能ID: {endpoint.get('function_id', '未知')})",
                    'severity': 'HIGH',
                    'design_endpoint': endpoint
                })
        
        return issues
    
    def _check_service_functions(self, file_path: str, code_content: str) -> List[Dict[str, Any]]:
        """检查服务层功能是否符合设计文档"""
        issues = []
        
        if 'system_function_design' not in self.design_docs:
            logger.warning(f"缺少系统功能设计文档，跳过服务层检查: {file_path}")
            return issues
        
        func_design = self.design_docs['system_function_design']['parsed']
        
        # 从代码中提取函数定义
        # Python函数模式：def function_name 或 async def function_name
        func_pattern = r'(?:async\s+)?def\s+(\w+)\s*\('
        found_functions = re.findall(func_pattern, code_content)
        
        # 检查文件名是否包含功能ID
        file_name = Path(file_path).name.lower()
        
        for func_id, func_info in func_design['functions'].items():
            # 检查功能ID是否在文件名或函数名中体现
            func_id_lower = func_id.lower()
            
            # 检查文件名是否包含功能ID
            if func_id_lower in file_name:
                # 文件名包含功能ID，检查功能职责是否在代码中实现
                func_name = func_info['name']
                responsibilities = func_info['responsibilities']
                
                # 简单的检查：功能名称是否在代码中出现
                if func_name and func_name not in code_content:
                    issues.append({
                        'type': 'FUNCTION_NAME_MISMATCH',
                        'file': str(file_path),
                        'description': f"功能名称不匹配: 设计文档中的功能 '{func_name}' 未在代码中体现",
                        'severity': 'MEDIUM',
                        'design_function': func_info
                    })
        
        return issues
    
    def _check_data_models(self, file_path: str, code_content: str) -> List[Dict[str, Any]]:
        """检查数据模型是否符合数据库设计文档"""
        issues = []
        
        if 'database_design' not in self.design_docs:
            logger.warning(f"缺少数据库设计文档，跳过数据模型检查: {file_path}")
            return issues
        
        db_design = self.design_docs['database_design']['parsed']
        
        # 从文件名推断表名
        file_name = Path(file_path).stem.lower()  # 去掉扩展名
        
        # 尝试匹配表名
        matched_tables = []
        for table_code, table_info in db_design['tables'].items():
            table_name_lower = table_info['name'].lower()
            table_code_lower = table_code.lower()
            
            # 检查文件名是否包含表名或表代码
            if (table_name_lower in file_name or 
                table_code_lower in file_name or
                file_name in table_name_lower):
                matched_tables.append((table_code, table_info))
        
        # 如果没有匹配的表，可能是公共模型文件
        if not matched_tables:
            return issues
        
        # 检查字段定义
        for table_code, table_info in matched_tables:
            for field in table_info['fields']:
                field_name = field['name']
                field_type = field['type']
                
                # 在代码中查找字段定义
                # SQLAlchemy模式：field_name = Column(type, ...)
                # Pydantic模式：field_name: type
                field_patterns = [
                    rf'{field_name}\s*=\s*Column\([^)]*{re.escape(field_type)}[^)]*\)',
                    rf'{field_name}\s*:\s*{re.escape(field_type)}',
                    rf'"{field_name}"\s*:\s*{re.escape(field_type)}'
                ]
                
                field_found = False
                for pattern in field_patterns:
                    if re.search(pattern, code_content, re.IGNORECASE):
                        field_found = True
                        break
                
                if not field_found:
                    issues.append({
                        'type': 'MISSING_FIELD',
                        'file': str(file_path),
                        'description': f"数据库设计中的字段未在代码中定义: {field_name} ({field_type})",
                        'severity': 'HIGH',
                        'design_field': field,
                        'table': table_info['name']
                    })
        
        return issues
    
    def generate_report(self) -> Dict[str, Any]:
        """生成验证报告"""
        total_issues = len(self.issues)
        high_severity = sum(1 for issue in self.issues if issue['severity'] == 'HIGH')
        medium_severity = sum(1 for issue in self.issues if issue['severity'] == 'MEDIUM')
        low_severity = sum(1 for issue in self.issues if issue['severity'] == 'LOW')
        
        report = {
            'summary': {
                'total_issues': total_issues,
                'high_severity': high_severity,
                'medium_severity': medium_severity,
                'low_severity': low_severity,
                'design_docs_loaded': list(self.design_docs.keys())
            },
            'issues': self.issues,
            'design_docs_summary': {
                doc_type: {
                    'path': info['path'],
                    'parsed_summary': {
                        'total_endpoints': info['parsed'].get('total_endpoints', 0),
                        'total_functions': info['parsed'].get('total_functions', 0),
                        'total_tables': info['parsed'].get('total_tables', 0),
                        'total_requirements': info['parsed'].get('total_requirements', 0)
                    }
                }
                for doc_type, info in self.design_docs.items()
            }
        }
        
        return report
    
    def run_checks(self, code_files: List[str], design_docs: Dict[str, str]) -> Dict[str, Any]:
        """运行完整的设计文档对照检查"""
        # 加载设计文档
        for doc_type, doc_path in design_docs.items():
            self.load_design_document(doc_type, doc_path)
        
        # 检查每个代码文件
        for code_file in code_files:
            if not os.path.exists(code_file):
                logger.warning(f"代码文件不存在: {code_file}")
                continue
                
            file_issues = self.check_code_against_design(code_file)
            self.issues.extend(file_issues)
        
        # 生成报告
        return self.generate_report()


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='设计文档对照验证工具')
    parser.add_argument('--project', required=True, help='项目根目录路径')
    parser.add_argument('--code', required=True, nargs='+', help='要检查的代码文件路径')
    parser.add_argument('--api-design', help='API设计文档路径')
    parser.add_argument('--func-design', help='系统功能设计文档路径')
    parser.add_argument('--db-design', help='数据库设计文档路径')
    parser.add_argument('--prd', help='PRD文档路径')
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
    
    if not design_docs:
        print("错误：至少需要指定一个设计文档")
        return 1
    
    # 运行检查
    checker = DesignDocumentChecker(args.project)
    report = checker.run_checks(args.code, design_docs)
    
    # 输出报告
    print("=" * 80)
    print("设计文档对照验证报告")
    print("=" * 80)
    
    summary = report['summary']
    print(f"\n📊 检查摘要")
    print(f"   加载的设计文档: {', '.join(summary['design_docs_loaded'])}")
    print(f"   发现问题总数: {summary['total_issues']}")
    print(f"   高危问题: {summary['high_severity']}")
    print(f"   中危问题: {summary['medium_severity']}")
    print(f"   低危问题: {summary['low_severity']}")
    
    if report['issues']:
        print(f"\n🔍 发现的问题:")
        for i, issue in enumerate(report['issues'], 1):
            severity_icon = '❌' if issue['severity'] == 'HIGH' else '⚠️' if issue['severity'] == 'MEDIUM' else 'ℹ️'
            print(f"   {severity_icon} [{issue['severity']}] {issue['type']}: {issue['description']}")
    else:
        print(f"\n✅ 未发现问题，代码符合设计文档")
    
    # 保存JSON报告
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 JSON报告已保存到: {args.report}")
    
    return 0 if summary['high_severity'] == 0 else 1


if __name__ == '__main__':
    exit(main())