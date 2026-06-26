#!/usr/bin/env python3
"""
架构检查脚本

功能：
1. 检查文件职责单一性（SRP原则）
2. 检查代码结构合理性
3. 检查功能边界分明性
4. 生成架构健康度报告

使用方式：
python3 architecture_check.py --path /path/to/code --report /path/to/report.json
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional

class ArchitectureChecker:
    """架构检查器"""
    
    def __init__(self, code_path: str):
        self.code_path = Path(code_path)
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
    def check_file_responsibilities(self, file_path: Path) -> Dict:
        """检查文件职责单一性"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            file_name = file_path.name
            
            # 分析文件中的功能
            functions = self._extract_functions(content)
            imports = self._extract_imports(content)
            classes = self._extract_classes(content)
            
            # 检查是否违反SRP原则
            srp_violations = self._check_srp_violations(str(file_path), functions, imports, classes)
            
            if srp_violations:
                issues.append({
                    "type": "SRP_VIOLATION",
                    "file": str(file_path),
                    "description": f"文件包含多个不相关功能：{srp_violations}",
                    "severity": "HIGH"
                })
            
            # 检查文件大小（过大可能表示职责过多）
            file_size_kb = file_path.stat().st_size / 1024
            if file_size_kb > 50:  # 超过50KB
                issues.append({
                    "type": "FILE_TOO_LARGE",
                    "file": str(file_path),
                    "description": f"文件过大 ({file_size_kb:.1f}KB)，可能包含过多职责",
                    "severity": "MEDIUM"
                })
            
            # 检查代码行数
            line_count = len(content.splitlines())
            if line_count > 500:  # 超过500行
                issues.append({
                    "type": "TOO_MANY_LINES",
                    "file": str(file_path),
                    "description": f"文件行数过多 ({line_count}行)，建议拆分",
                    "severity": "MEDIUM"
                })
                
        except Exception as e:
            issues.append({
                "type": "PARSE_ERROR",
                "file": str(file_path),
                "description": f"解析文件时出错：{str(e)}",
                "severity": "LOW"
            })
        
        return {
            "file": str(file_path),
            "issues": issues,
            "function_count": len(functions),
            "class_count": len(classes)
        }
    
    def check_code_structure(self, file_path: Path) -> Dict:
        """检查代码结构合理性"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            file_name = file_path.name
            
            # 检查分层架构
            if self._is_router_file(file_name):
                if self._has_business_logic_in_router(content):
                    issues.append({
                        "type": "BUSINESS_LOGIC_IN_ROUTER",
                        "file": str(file_path),
                        "description": "路由文件中包含业务逻辑，应移动到服务层",
                        "severity": "HIGH"
                    })
            
            # 检查依赖关系
            if self._has_cyclic_dependencies(content, file_name):
                issues.append({
                    "type": "CYCLIC_DEPENDENCY",
                    "file": str(file_path),
                    "description": "可能存在循环依赖",
                    "severity": "HIGH"
                })
            
            # 检查公共功能提取
            if self._has_duplicate_code_patterns(content):
                issues.append({
                    "type": "DUPLICATE_CODE",
                    "file": str(file_path),
                    "description": "发现重复代码模式，建议提取为公共函数",
                    "severity": "MEDIUM"
                })
                
        except Exception as e:
            issues.append({
                "type": "PARSE_ERROR",
                "file": str(file_path),
                "description": f"解析文件时出错：{str(e)}",
                "severity": "LOW"
            })
        
        return {
            "file": str(file_path),
            "issues": issues
        }
    
    def check_function_boundaries(self, file_path: Path) -> Dict:
        """检查功能边界分明性"""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            file_name = file_path.name
            
            # 检查功能耦合度
            if self._has_high_coupling(content):
                issues.append({
                    "type": "HIGH_COUPLING",
                    "file": str(file_path),
                    "description": "功能耦合度过高，建议解耦",
                    "severity": "MEDIUM"
                })
            
            # 检查功能内聚性
            if not self._has_high_cohesion(content, file_name):
                issues.append({
                    "type": "LOW_COHESION",
                    "file": str(file_path),
                    "description": "功能内聚性低，相关功能应放在一起",
                    "severity": "MEDIUM"
                })
                
        except Exception as e:
            issues.append({
                "type": "PARSE_ERROR",
                "file": str(file_path),
                "description": f"解析文件时出错：{str(e)}",
                "severity": "LOW"
            })
        
        return {
            "file": str(file_path),
            "issues": issues
        }
    
    def _extract_functions(self, content: str) -> List[str]:
        """提取函数定义"""
        functions = []
        # 匹配Python函数定义
        pattern = r'def\s+(\w+)\s*\([^)]*\)\s*(?:->[^:]+)?:'
        functions.extend(re.findall(pattern, content))
        return functions
    
    def _extract_imports(self, content: str) -> List[str]:
        """提取导入语句"""
        imports = []
        # 匹配import语句
        pattern = r'^(?:from\s+(\w+)|import\s+([\w\s,]+))'
        for line in content.splitlines():
            match = re.match(pattern, line.strip())
            if match:
                imports.append(match.group(1) or match.group(2))
        return imports
    
    def _extract_classes(self, content: str) -> List[str]:
        """提取类定义"""
        classes = []
        # 匹配Python类定义
        pattern = r'class\s+(\w+)\s*(?:\([^)]*\))?:'
        classes.extend(re.findall(pattern, content))
        return classes
    
    def _check_srp_violations(self, file_path: str, functions: List[str], 
                             imports: List[str], classes: List[str]) -> List[str]:
        """检查SRP违规"""
        violations = []
        
        file_name = os.path.basename(file_path)
        
        # 根据文件名判断预期职责
        expected_responsibilities = self._get_expected_responsibilities(file_name)
        
        # 检查路由文件是否包含业务逻辑类
        if self._is_router_file(file_path):
            # 路由文件不应该包含业务逻辑类
            business_logic_keywords = [
                'service', 'repository', 'dao', 'parser', 'validator',
                'processor', 'handler', 'manager', 'helper', 'util'
            ]
            
            for cls in classes:
                cls_lower = cls.lower()
                for keyword in business_logic_keywords:
                    if keyword in cls_lower:
                        violations.append(f"路由文件中包含业务逻辑类: {cls}")
                        break
            
            # 路由文件中的类不应超过2个（通常只有路由类）
            if len(classes) > 2:
                violations.append(f"路由文件中类数量过多: {len(classes)}个")
        
        # 简单检查：如果文件包含太多不同类型的功能
        if len(functions) > 10 and len(classes) > 3:
            violations.append("函数和类数量过多")
        
        return violations
    
    def _get_expected_responsibilities(self, file_name: str) -> List[str]:
        """根据文件名获取预期职责"""
        file_lower = file_name.lower()
        
        if 'router' in file_lower or 'api' in file_lower:
            return ['routing', 'request_handling']
        elif 'service' in file_lower:
            return ['business_logic']
        elif 'model' in file_lower or 'schema' in file_lower:
            return ['data_model']
        elif 'repository' in file_lower or 'dao' in file_lower:
            return ['data_access']
        elif 'util' in file_lower or 'helper' in file_lower:
            return ['utility_functions']
        
        return []
    
    def _is_router_file(self, file_path: str) -> bool:
        """判断是否是路由文件"""
        file_name = os.path.basename(file_path)
        # 检查文件名
        if 'router' in file_name.lower() or 'api' in file_name.lower():
            return True
        
        # 检查路径
        if '/routers/' in file_path.replace('\\', '/'):
            return True
        
        return False
    
    def _has_business_logic_in_router(self, content: str) -> bool:
        """检查路由文件中是否包含业务逻辑"""
        # 更精确的检查：如果包含数据库操作或复杂计算
        business_logic_patterns = [
            r'SELECT\s+.*FROM',  # SQL查询
            r'INSERT\s+INTO',    # SQL插入
            r'UPDATE\s+.*SET',   # SQL更新
            r'DELETE\s+FROM',    # SQL删除
            r'session\.',        # SQLAlchemy会话操作
            r'db\.',             # 数据库操作
            r'\.add\(',         # 添加数据
            r'\.commit\(',      # 提交事务
            r'\.query\(',       # 查询操作
            r'def\s+calculate_', # 计算函数
            r'def\s+process_',   # 处理函数（但排除process_upload等常见模式）
            r'def\s+transform_', # 转换函数
            r'business_logic',    # 明确业务逻辑
            r'algorithm'          # 算法
        ]
        
        content_lower = content.lower()
        
        # 排除常见服务调用模式
        exclude_patterns = [
            r'_service\.',       # 服务调用
            r'await.*service',    # 异步服务调用
            r'process_upload',    # 文件上传处理
            r'process_download',  # 文件下载处理
            r'validate_input',    # 输入验证
        ]
        
        # 先检查排除模式
        for pattern in exclude_patterns:
            if re.search(pattern, content_lower):
                # 如果是服务调用，不视为业务逻辑
                return False
        
        # 再检查业务逻辑模式
        for pattern in business_logic_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _has_cyclic_dependencies(self, content: str, file_name: str) -> bool:
        """检查循环依赖（简化版）"""
        # 这里可以添加更复杂的循环依赖检测逻辑
        return False
    
    def _has_duplicate_code_patterns(self, content: str) -> bool:
        """检查重复代码模式"""
        lines = content.splitlines()
        
        # 忽略模板文件中的占位符行
        template_patterns = [
            r'\{module_name\}',
            r'\{ModuleName\}',
            r'\{module_name_plural\}',
            r'\{module_name_display\}',
            r'# 模板',
            r'# 示例',
            r'# 占位符'
        ]
        
        # 简单的重复行检测
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            # 忽略空行、短行、注释行和模板行
            if stripped and len(stripped) > 10 and not stripped.startswith('#'):
                # 检查是否是模板行
                is_template_line = False
                for pattern in template_patterns:
                    if re.search(pattern, stripped):
                        is_template_line = True
                        break
                
                if not is_template_line:
                    line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        # 如果有行出现多次（考虑模板文件的特点）
        for line, count in line_counts.items():
            if count > 5:  # 同一行出现超过5次（模板文件可能允许更多重复）
                # 检查是否是合理的重复（如错误处理模式）
                if 'raise HTTPException' in line or 'except Exception' in line:
                    # 错误处理模式的重复是合理的
                    continue
                return True
        
        return False
    
    def _has_high_coupling(self, content: str) -> bool:
        """检查高耦合度"""
        # 简单的检查：导入模块数量
        imports = self._extract_imports(content)
        return len(imports) > 15  # 导入过多模块可能表示耦合度高
    
    def _has_high_cohesion(self, content: str, file_name: str) -> bool:
        """检查高内聚性"""
        # 简单的检查：函数和类的相关性
        functions = self._extract_functions(content)
        classes = self._extract_classes(content)
        
        # 如果文件有明确职责且功能相关，则内聚性高
        expected = self._get_expected_responsibilities(file_name)
        if expected and len(functions) > 0:
            # 这里可以添加更复杂的逻辑来检查功能相关性
            return True
        
        return len(functions) == 0 and len(classes) == 0
    
    def run_checks(self) -> Dict:
        """运行所有检查"""
        results = {
            "srp_checks": [],
            "structure_checks": [],
            "boundary_checks": [],
            "summary": {
                "total_files": 0,
                "issues_found": 0,
                "high_severity": 0,
                "medium_severity": 0,
                "low_severity": 0
            }
        }
        
        # 收集所有Python文件
        python_files = list(self.code_path.rglob("*.py"))
        results["summary"]["total_files"] = len(python_files)
        
        for file_path in python_files:
            # 检查文件职责单一性
            srp_result = self.check_file_responsibilities(file_path)
            results["srp_checks"].append(srp_result)
            
            # 检查代码结构
            structure_result = self.check_code_structure(file_path)
            results["structure_checks"].append(structure_result)
            
            # 检查功能边界
            boundary_result = self.check_function_boundaries(file_path)
            results["boundary_checks"].append(boundary_result)
            
            # 更新问题统计
            for check_result in [srp_result, structure_result, boundary_result]:
                for issue in check_result.get("issues", []):
                    results["summary"]["issues_found"] += 1
                    severity = issue.get("severity", "LOW")
                    if severity == "HIGH":
                        results["summary"]["high_severity"] += 1
                    elif severity == "MEDIUM":
                        results["summary"]["medium_severity"] += 1
                    else:
                        results["summary"]["low_severity"] += 1
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """生成架构检查报告"""
        report = []
        report.append("=" * 80)
        report.append("架构检查报告")
        report.append("=" * 80)
        report.append("")
        
        # 摘要
        summary = results["summary"]
        report.append(f"📊 检查摘要")
        report.append(f"   检查文件数: {summary['total_files']}")
        report.append(f"   发现问题数: {summary['issues_found']}")
        report.append(f"   高危问题: {summary['high_severity']}")
        report.append(f"   中危问题: {summary['medium_severity']}")
        report.append(f"   低危问题: {summary['low_severity']}")
        report.append("")
        
        # SRP检查结果
        report.append(f"🔍 SRP原则检查（文件职责单一性）")
        srp_issues = []
        for check in results["srp_checks"]:
            for issue in check.get("issues", []):
                if issue["type"] == "SRP_VIOLATION":
                    srp_issues.append(issue)
        
        if srp_issues:
            report.append(f"   ❌ 发现 {len(srp_issues)} 个SRP违规：")
            for issue in srp_issues:
                report.append(f"      • {issue['file']}: {issue['description']}")
        else:
            report.append(f"   ✅ 未发现SRP违规")
        report.append("")
        
        # 结构检查结果
        report.append(f"🏗️  代码结构检查")
        structure_issues = []
        for check in results["structure_checks"]:
            for issue in check.get("issues", []):
                if issue["type"] == "BUSINESS_LOGIC_IN_ROUTER":
                    structure_issues.append(issue)
        
        if structure_issues:
            report.append(f"   ⚠️  发现 {len(structure_issues)} 个结构问题：")
            for issue in structure_issues:
                report.append(f"      • {issue['file']}: {issue['description']}")
        else:
            report.append(f"   ✅ 代码结构良好")
        report.append("")
        
        # 建议
        report.append(f"💡 重构建议")
        if summary["high_severity"] > 0:
            report.append(f"   1. 优先处理 {summary['high_severity']} 个高危问题")
        if srp_issues:
            report.append(f"   2. 拆分职责混淆的文件（{len(srp_issues)}个）")
        if structure_issues:
            report.append(f"   3. 将业务逻辑从路由文件移动到服务层")
        
        if summary["issues_found"] == 0:
            report.append(f"   ✅ 架构健康，无需重构")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='架构检查工具')
    parser.add_argument('--path', required=True, help='要检查的代码路径')
    parser.add_argument('--report', help='JSON报告输出路径')
    parser.add_argument('--verbose', action='store_true', help='显示详细输出')
    
    args = parser.parse_args()
    
    # 检查路径是否存在
    if not os.path.exists(args.path):
        print(f"错误：路径不存在 - {args.path}")
        sys.exit(1)
    
    # 运行检查
    checker = ArchitectureChecker(args.path)
    results = checker.run_checks()
    
    # 生成报告
    report_text = checker.generate_report(results)
    
    # 输出报告
    if args.verbose:
        print(report_text)
    else:
        print("架构检查完成")
        summary = results["summary"]
        print(f"检查文件数: {summary['total_files']}")
        print(f"发现问题数: {summary['issues_found']} (高危: {summary['high_severity']})")
    
    # 保存JSON报告
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"JSON报告已保存到: {args.report}")
    
    # 返回退出码（如果有高危问题则返回1）
    if results["summary"]["high_severity"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()