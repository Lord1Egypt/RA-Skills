#!/usr/bin/env python3
"""
API接口验证工具
专门用于验证API接口是否与设计文档一致
"""

import re
import json
import logging
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class APIVerifier:
    """API接口验证器"""
    
    def __init__(self):
        self.design_endpoints = []
        self.code_endpoints = []
        self.issues = []
    
    def load_api_design(self, design_path: str) -> bool:
        """加载API设计文档"""
        try:
            with open(design_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析API设计文档
            self.design_endpoints = self._parse_api_design(content)
            logger.info(f"加载API设计文档成功: {design_path} ({len(self.design_endpoints)}个端点)")
            return True
            
        except Exception as e:
            logger.error(f"加载API设计文档失败: {str(e)}")
            return False
    
    def _parse_api_design(self, content: str) -> List[Dict[str, Any]]:
        """解析API设计文档内容"""
        endpoints = []
        
        # 提取API端点定义
        # 格式：### 1.2.1 上传知识图谱文件
        #      **请求路径**: `POST /api/knowledge-graph/upload`
        endpoint_pattern = r'###\s*(\d+\.\d+\.\d+)\s*([^\n]+)\s*\n.*?\n\*\*请求路径\*\*:\s*`([^`]+)`'
        
        matches = re.findall(endpoint_pattern, content, re.DOTALL)
        
        for endpoint_num, endpoint_name, endpoint_path in matches:
            # 提取HTTP方法
            method_match = re.search(r'\*\*请求方法\*\*:\s*`([^`]+)`', content)
            method = method_match.group(1) if method_match else 'UNKNOWN'
            
            # 提取功能ID
            func_id_match = re.search(r'\*\*功能ID\*\*:\s*`([^`]+)`', content)
            func_id = func_id_match.group(1) if func_id_match else ''
            
            # 提取请求参数
            params_match = re.search(r'\*\*请求参数\*\*:\s*\n```json\n([^`]+)\n```', content, re.DOTALL)
            request_params = json.loads(params_match.group(1)) if params_match else {}
            
            # 提取响应格式
            response_match = re.search(r'\*\*响应格式\*\*:\s*\n```json\n([^`]+)\n```', content, re.DOTALL)
            response_format = json.loads(response_match.group(1)) if response_match else {}
            
            endpoints.append({
                'id': endpoint_num,
                'name': endpoint_name.strip(),
                'path': endpoint_path.strip(),
                'method': method.upper(),
                'function_id': func_id,
                'request_params': request_params,
                'response_format': response_format
            })
        
        return endpoints
    
    def extract_api_endpoints_from_code(self, code_path: str) -> List[Dict[str, Any]]:
        """从代码中提取API端点定义"""
        try:
            with open(code_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            endpoints = []
            
            # FastAPI路由装饰器模式
            patterns = [
                # @router.get("/api/path")
                (r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', 'router'),
                # @app.get("/api/path")
                (r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', 'app'),
                # @APIRouter().get("/api/path")
                (r'@.*?\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', 'generic')
            ]
            
            for pattern, source in patterns:
                matches = re.findall(pattern, content)
                for method, path in matches:
                    # 提取函数名
                    func_name = self._extract_function_name(content, method, path)
                    
                    endpoints.append({
                        'method': method.upper(),
                        'path': path.strip(),
                        'file': code_path,
                        'function_name': func_name,
                        'source': source
                    })
            
            logger.info(f"从代码中提取API端点: {code_path} ({len(endpoints)}个端点)")
            return endpoints
            
        except Exception as e:
            logger.error(f"提取API端点失败 {code_path}: {str(e)}")
            return []
    
    def _extract_function_name(self, content: str, method: str, path: str) -> str:
        """提取路由装饰器对应的函数名"""
        # 查找装饰器后面的函数定义
        pattern = rf'@.*?\.{re.escape(method)}\(.*?{re.escape(path)}.*?\)\s*\n(?:async\s+)?def\s+(\w+)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else 'unknown'
    
    def verify_api_endpoints(self, design_path: str, code_paths: List[str]) -> Dict[str, Any]:
        """验证API端点一致性"""
        # 加载设计文档
        if not self.load_api_design(design_path):
            return {
                'success': False,
                'error': '无法加载API设计文档',
                'issues': []
            }
        
        # 从代码中提取端点
        self.code_endpoints = []
        for code_path in code_paths:
            endpoints = self.extract_api_endpoints_from_code(code_path)
            self.code_endpoints.extend(endpoints)
        
        # 执行验证
        self._verify_endpoint_coverage()
        self._verify_path_consistency()
        self._verify_method_consistency()
        
        # 生成报告
        return self.generate_report()
    
    def _verify_endpoint_coverage(self):
        """验证端点覆盖：设计文档中的端点是否都在代码中实现"""
        for design_endpoint in self.design_endpoints:
            design_path = design_endpoint['path']
            design_method = design_endpoint['method']
            
            # 查找匹配的代码端点
            matched = False
            for code_endpoint in self.code_endpoints:
                code_path = code_endpoint['path']
                code_method = code_endpoint['method']
                
                # 路径匹配逻辑
                if self._paths_match(design_path, code_path) and \
                   design_method.upper() == code_method.upper():
                    matched = True
                    break
            
            if not matched:
                self.issues.append({
                    'type': 'MISSING_ENDPOINT',
                    'severity': 'HIGH',
                    'description': f"设计文档中的API端点未实现: {design_method} {design_path}",
                    'design_endpoint': design_endpoint,
                    'suggestion': f"需要在代码中实现 {design_method} {design_path} 端点"
                })
    
    def _verify_path_consistency(self):
        """验证路径一致性"""
        for code_endpoint in self.code_endpoints:
            code_path = code_endpoint['path']
            code_method = code_endpoint['method']
            
            # 检查路径格式
            if not code_path.startswith('/'):
                self.issues.append({
                    'type': 'INVALID_PATH_FORMAT',
                    'severity': 'MEDIUM',
                    'description': f"API路径格式不正确: {code_path} (应以'/'开头)",
                    'code_endpoint': code_endpoint,
                    'suggestion': f"修正路径格式: /{code_path.lstrip('/')}"
                })
            
            # 检查路径是否与设计文档一致
            matched = False
            for design_endpoint in self.design_endpoints:
                if self._paths_match(design_endpoint['path'], code_path) and \
                   design_endpoint['method'].upper() == code_method.upper():
                    matched = True
                    break
            
            if not matched:
                self.issues.append({
                    'type': 'UNEXPECTED_ENDPOINT',
                    'severity': 'MEDIUM',
                    'description': f"代码中的API端点不在设计文档中: {code_method} {code_path}",
                    'code_endpoint': code_endpoint,
                    'suggestion': "检查是否是多实现的端点，或需要更新设计文档"
                })
    
    def _verify_method_consistency(self):
        """验证HTTP方法一致性"""
        for design_endpoint in self.design_endpoints:
            design_path = design_endpoint['path']
            design_method = design_endpoint['method']
            
            for code_endpoint in self.code_endpoints:
                code_path = code_endpoint['path']
                code_method = code_endpoint['method']
                
                # 如果路径匹配但方法不匹配
                if self._paths_match(design_path, code_path) and \
                   design_method.upper() != code_method.upper():
                    self.issues.append({
                        'type': 'METHOD_MISMATCH',
                        'severity': 'HIGH',
                        'description': f"HTTP方法不匹配: 设计文档要求{design_method}，代码实现为{code_method}",
                        'design_endpoint': design_endpoint,
                        'code_endpoint': code_endpoint,
                        'suggestion': f"将代码中的方法从{code_method}改为{design_method}"
                    })
    
    def _paths_match(self, path1: str, path2: str) -> bool:
        """判断两个API路径是否匹配"""
        # 简单的路径匹配逻辑
        # 可以改进为更复杂的路径参数匹配
        p1 = path1.strip().rstrip('/')
        p2 = path2.strip().rstrip('/')
        
        # 完全匹配
        if p1 == p2:
            return True
        
        # 路径参数匹配
        # 例如：/api/users/{id} 匹配 /api/users/123
        p1_parts = p1.split('/')
        p2_parts = p2.split('/')
        
        if len(p1_parts) != len(p2_parts):
            return False
        
        for part1, part2 in zip(p1_parts, p2_parts):
            if part1.startswith('{') and part1.endswith('}'):
                # part1是路径参数，part2可以是任意值
                continue
            if part1 != part2:
                return False
        
        return True
    
    def generate_report(self) -> Dict[str, Any]:
        """生成验证报告"""
        total_issues = len(self.issues)
        high_severity = sum(1 for issue in self.issues if issue['severity'] == 'HIGH')
        medium_severity = sum(1 for issue in self.issues if issue['severity'] == 'MEDIUM')
        
        # 统计端点数量
        design_endpoint_count = len(self.design_endpoints)
        code_endpoint_count = len(self.code_endpoints)
        
        # 计算覆盖率
        matched_endpoints = 0
        for design_endpoint in self.design_endpoints:
            for code_endpoint in self.code_endpoints:
                if self._paths_match(design_endpoint['path'], code_endpoint['path']) and \
                   design_endpoint['method'].upper() == code_endpoint['method'].upper():
                    matched_endpoints += 1
                    break
        
        coverage = matched_endpoints / design_endpoint_count * 100 if design_endpoint_count > 0 else 0
        
        report = {
            'summary': {
                'design_endpoints': design_endpoint_count,
                'code_endpoints': code_endpoint_count,
                'matched_endpoints': matched_endpoints,
                'coverage_percentage': round(coverage, 2),
                'total_issues': total_issues,
                'high_severity_issues': high_severity,
                'medium_severity_issues': medium_severity
            },
            'design_endpoints': self.design_endpoints,
            'code_endpoints': self.code_endpoints,
            'issues': self.issues,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if self.issues:
            # 根据问题类型生成建议
            missing_endpoints = [i for i in self.issues if i['type'] == 'MISSING_ENDPOINT']
            unexpected_endpoints = [i for i in self.issues if i['type'] == 'UNEXPECTED_ENDPOINT']
            method_mismatches = [i for i in self.issues if i['type'] == 'METHOD_MISMATCH']
            
            if missing_endpoints:
                recommendations.append(f"需要实现 {len(missing_endpoints)} 个缺失的API端点")
            
            if unexpected_endpoints:
                recommendations.append(f"需要审查 {len(unexpected_endpoints)} 个未在设计文档中定义的API端点")
            
            if method_mismatches:
                recommendations.append(f"需要修正 {len(method_mismatches)} 个HTTP方法不匹配的端点")
        else:
            recommendations.append("API接口与设计文档完全一致")
        
        # 覆盖率建议
        coverage = self.generate_report()['summary']['coverage_percentage']
        if coverage < 100:
            recommendations.append(f"API端点覆盖率为 {coverage}%，需要提高覆盖率")
        else:
            recommendations.append("API端点覆盖率100%，优秀！")
        
        return recommendations


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='API接口验证工具')
    parser.add_argument('--design', required=True, help='API设计文档路径')
    parser.add_argument('--code', required=True, nargs='+', help='要检查的代码文件路径')
    parser.add_argument('--report', help='JSON报告输出路径')
    parser.add_argument('--verbose', action='store_true', help='显示详细输出')
    
    args = parser.parse_args()
    
    # 设置日志
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行验证
    verifier = APIVerifier()
    report = verifier.verify_api_endpoints(args.design, args.code)
    
    # 输出报告
    print("=" * 80)
    print("API接口验证报告")
    print("=" * 80)
    
    summary = report['summary']
    print(f"\n📊 API端点统计")
    print(f"   设计文档端点: {summary['design_endpoints']}个")
    print(f"   代码实现端点: {summary['code_endpoints']}个")
    print(f"   匹配的端点: {summary['matched_endpoints']}个")
    print(f"   覆盖率: {summary['coverage_percentage']}%")
    
    print(f"\n🔍 问题统计")
    print(f"   总问题数: {summary['total_issues']}")
    print(f"   高危问题: {summary['high_severity_issues']}")
    print(f"   中危问题: {summary['medium_severity_issues']}")
    
    if report['issues']:
        print(f"\n❌ 发现的问题:")
        for i, issue in enumerate(report['issues'], 1):
            severity_icon = '❌' if issue['severity'] == 'HIGH' else '⚠️'
            print(f"   {severity_icon} [{issue['severity']}] {issue['type']}: {issue['description']}")
    else:
        print(f"\n✅ 未发现问题，API接口与设计文档一致")
    
    print(f"\n💡 改进建议:")
    for rec in report['recommendations']:
        print(f"   • {rec}")
    
    # 保存JSON报告
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 JSON报告已保存到: {args.report}")
    
    return 0 if summary['high_severity_issues'] == 0 else 1


if __name__ == '__main__':
    exit(main())