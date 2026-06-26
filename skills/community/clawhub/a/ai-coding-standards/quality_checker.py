#!/usr/bin/env python3
"""
AI Coding Standards - Quality Checker
基于 Claude Code 最佳实践的代码质量检查
"""
import os
import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class QualityIssue:
    """质量问题"""
    line: int
    issue_type: str
    message: str
    severity: str = "error"


@dataclass
class QualityResult:
    """检查结果"""
    passed: bool
    issues: List[QualityIssue]
    file_path: str


class QualityChecker:
    """代码质量检查器"""
    
    # 质量红线配置
    MAX_FUNCTION_LINES = 30
    MAX_FILE_LINES = 800
    MAX_NESTING = 3
    MAX_BRANCHES = 3
    
    def __init__(self, config: Optional[dict] = None):
        if config:
            self.MAX_FUNCTION_LINES = config.get('max_function_lines', 30)
            self.MAX_FILE_LINES = config.get('max_file_lines', 800)
            self.MAX_NESTING = config.get('max_nesting', 3)
            self.MAX_BRANCHES = config.get('max_branches', 3)
    
    def check_file(self, file_path: str) -> QualityResult:
        """检查单个文件"""
        if not os.path.exists(file_path):
            return QualityResult(
                passed=False,
                issues=[QualityIssue(0, "file_not_found", f"文件不存在: {file_path}")],
                file_path=file_path
            )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        issues = []
        
        # 1. 检查文件行数
        if len(lines) > self.MAX_FILE_LINES:
            issues.append(QualityIssue(
                len(lines),
                "file_too_long",
                f"文件超过 {self.MAX_FILE_LINES} 行 (当前 {len(lines)} 行)",
                "warning"
            ))
        
        # 2. 检查函数长度
        issues.extend(self._check_functions(lines, file_path))
        
        # 3. 检查嵌套深度
        issues.extend(self._check_nesting(lines, file_path))
        
        return QualityResult(
            passed=len([i for i in issues if i.severity == "error"]) == 0,
            issues=issues,
            file_path=file_path
        )
    
    def _check_functions(self, lines: List[str], file_path: str) -> List[QualityIssue]:
        """检查函数长度"""
        issues = []
        in_function = False
        function_start = 0
        function_lines = 0
        function_name = ""
        
        for i, line in enumerate(lines):
            # 检测函数定义
            if re.match(r'^\s*(def |function |fn |async def )', line):
                if in_function and function_lines > self.MAX_FUNCTION_LINES:
                    issues.append(QualityIssue(
                        function_start + 1,
                        "function_too_long",
                        f"函数 {function_name} 超过 {self.MAX_FUNCTION_LINES} 行 (当前 {function_lines} 行)"
                    ))
                in_function = True
                function_start = i
                function_lines = 0
                match = re.search(r'(def |function |fn |async def )(\w+)', line)
                function_name = match.group(2) if match else "anonymous"
            
            if in_function:
                # 跳过空行和注释
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('//'):
                    function_lines += 1
        
        return issues
    
    def _check_nesting(self, lines: List[str], file_path: str) -> List[QualityIssue]:
        """检查嵌套深度"""
        issues = []
        max_depth = 0
        
        for i, line in enumerate(lines):
            # 计算缩进
            indent = len(line) - len(line.lstrip())
            depth = indent // 4  # 假设 4 空格 = 1 层
            
            if depth > self.MAX_NESTING and line.strip():
                issues.append(QualityIssue(
                    i + 1,
                    "nesting_too_deep",
                    f"嵌套深度 {depth} 超过限制 {self.MAX_NESTING}"
                ))
        
        return issues
    
    def check_directory(self, dir_path: str, extensions: List[str] = None) -> List[QualityResult]:
        """检查整个目录"""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.go', '.rs']
        
        results = []
        for root, _, files in os.walk(dir_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    results.append(self.check_file(file_path))
        
        return results


def main():
    """CLI 入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python quality_checker.py <file_or_directory>")
        sys.exit(1)
    
    path = sys.argv[1]
    checker = QualityChecker()
    
    if os.path.isfile(path):
        result = checker.check_file(path)
        print(f"\n{'✅' if result.passed else '❌'} {result.file_path}")
        for issue in result.issues:
            print(f"  L{issue.line}: {issue.issue_type} - {issue.message}")
    else:
        results = checker.check_directory(path)
        failed = [r for r in results if not r.passed]
        print(f"\n检查 {len(results)} 个文件, {len(failed)} 个有问题")
        for result in failed[:10]:
            print(f"  ❌ {result.file_path}: {len(result.issues)} issues")


if __name__ == "__main__":
    main()
