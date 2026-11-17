#!/usr/bin/env python3
"""
TDD Runner — 测试驱动开发流程工具

功能：
- red: 运行测试，期望失败（红灯）
- green: 运行测试，期望通过（绿灯）
- cycle: 完整红绿重构循环
- strict: 强制 TDD 模式（检测代码先于测试）

用法：
    python tdd_runner.py red tests/test_main.py
    python tdd_runner.py green tests/test_main.py
    python tdd_runner.py cycle tests/test_main.py src/main.py
    python tdd_runner.py strict --check src/main.py tests/

strict 模式逻辑：
1. 检查 src/ 中是否有新增/修改的代码
2. 检查 tests/ 中是否有对应的新测试
3. 如果代码先于测试 → 报错，建议删除代码
4. 如果测试先于代码 → 通过

输出格式：
{
  "status": "pass|fail",
  "message": "TDD 流程正确" | "检测到代码先于测试",
  "violations": [
    {"file": "src/main.py", "reason": "新增代码无对应测试"}
  ]
}
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TDDRunner:
    """TDD 流程管理器"""
    
    def __init__(self, project_root: str = None):
        """初始化
        
        Args:
            project_root: 项目根目录，默认当前目录
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        
    def run_command(self, cmd: List[str], cwd: Path = None) -> Tuple[int, str, str]:
        """运行命令
        
        Args:
            cmd: 命令列表
            cwd: 工作目录
            
        Returns:
            (returncode, stdout, stderr)
        """
        result = subprocess.run(
            cmd,
            cwd=cwd or self.project_root,
            capture_output=True,
            text=True,
            timeout=300  # 5 分钟超时
        )
        return result.returncode, result.stdout, result.stderr
    
    def red(self, test_file: str) -> dict:
        """红灯阶段：运行测试，期望失败
        
        Args:
            test_file: 测试文件路径
            
        Returns:
            包含状态的字典
        """
        test_path = self.project_root / test_file
        
        if not test_path.exists():
            return {
                "status": "error",
                "message": f"测试文件不存在: {test_file}",
                "phase": "red"
            }
        
        # 检测语言并运行测试
        if test_file.endswith('.py'):
            returncode, stdout, stderr = self.run_command(
                [sys.executable, "-m", "pytest", test_file, "-v"]
            )
        elif test_file.endswith('.js') or test_file.endswith('.ts'):
            returncode, stdout, stderr = self.run_command(
                ["npm", "test", "--", test_file]
            )
        else:
            return {
                "status": "error",
                "message": f"不支持的测试文件类型: {test_file}",
                "phase": "red"
            }
        
        # 红灯阶段期望测试失败
        if returncode != 0:
            return {
                "status": "pass",
                "message": "红灯 ✓ 测试按预期失败",
                "phase": "red",
                "output": stdout or stderr
            }
        else:
            return {
                "status": "fail",
                "message": "红灯 ✗ 测试通过了，但期望失败。请确认测试是否正确编写。",
                "phase": "red",
                "output": stdout
            }
    
    def green(self, test_file: str) -> dict:
        """绿灯阶段：运行测试，期望通过
        
        Args:
            test_file: 测试文件路径
            
        Returns:
            包含状态的字典
        """
        test_path = self.project_root / test_file
        
        if not test_path.exists():
            return {
                "status": "error",
                "message": f"测试文件不存在: {test_file}",
                "phase": "green"
            }
        
        # 检测语言并运行测试
        if test_file.endswith('.py'):
            returncode, stdout, stderr = self.run_command(
                [sys.executable, "-m", "pytest", test_file, "-v"]
            )
        elif test_file.endswith('.js') or test_file.endswith('.ts'):
            returncode, stdout, stderr = self.run_command(
                ["npm", "test", "--", test_file]
            )
        else:
            return {
                "status": "error",
                "message": f"不支持的测试文件类型: {test_file}",
                "phase": "green"
            }
        
        # 绿灯阶段期望测试通过
        if returncode == 0:
            return {
                "status": "pass",
                "message": "绿灯 ✓ 测试通过",
                "phase": "green",
                "output": stdout
            }
        else:
            return {
                "status": "fail",
                "message": "绿灯 ✗ 测试失败，请修复实现代码",
                "phase": "green",
                "output": stdout or stderr
            }
    
    def cycle(self, test_file: str, src_file: str) -> dict:
        """完整红绿重构循环
        
        Args:
            test_file: 测试文件路径
            src_file: 源代码文件路径
            
        Returns:
            包含循环结果的字典
        """
        results = {
            "status": "pass",
            "phases": [],
            "message": ""
        }
        
        # 阶段 1: 红灯
        red_result = self.red(test_file)
        results["phases"].append(red_result)
        
        if red_result["status"] != "pass":
            results["status"] = "fail"
            results["message"] = "红灯阶段失败，停止循环"
            return results
        
        # 阶段 2: 提示用户编写实现
        results["phases"].append({
            "status": "info",
            "message": f"请编写 {src_file} 中的实现代码，使测试通过",
            "phase": "implement"
        })
        
        # 阶段 3: 绿灯（需要用户手动触发）
        results["phases"].append({
            "status": "info",
            "message": f"实现完成后，运行: python tdd_runner.py green {test_file}",
            "phase": "green-pending"
        })
        
        results["message"] = "红绿循环已启动，请按照提示继续"
        return results
    
    def strict_check(self, src_dir: str, test_dir: str) -> dict:
        """强制 TDD 检查：检测代码是否先于测试
        
        Args:
            src_dir: 源代码目录
            test_dir: 测试目录
            
        Returns:
            包含检查结果的字典
        """
        src_path = self.project_root / src_dir
        test_path = self.project_root / test_dir
        
        violations = []
        
        # 获取 git 变更
        returncode, stdout, stderr = self.run_command(
            ["git", "diff", "--name-status", "HEAD"]
        )
        
        if returncode != 0:
            # 如果没有 HEAD，使用 unstaged changes
            returncode, stdout, stderr = self.run_command(
                ["git", "diff", "--name-status"]
            )
        
        # 解析变更文件
        changed_files = {}
        for line in stdout.splitlines():
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                status = parts[0]
                file_path = parts[1]
                changed_files[file_path] = status
        
        # 检查源代码变更
        src_changes = [f for f in changed_files if f.startswith(src_dir)]
        test_changes = [f for f in changed_files if f.startswith(test_dir)]
        
        # 对每个源代码变更，检查是否有对应的测试
        for src_file in src_changes:
            # 推断对应的测试文件
            test_file = self._infer_test_file(src_file, src_dir, test_dir)
            
            if test_file and test_file not in test_changes:
                # 检查测试文件是否存在
                full_test_path = self.project_root / test_file
                if not full_test_path.exists():
                    violations.append({
                        "file": src_file,
                        "reason": "新增/修改的源代码没有对应的测试文件",
                        "expected_test": test_file,
                        "suggestion": "请先编写测试，再编写实现代码"
                    })
                else:
                    # 测试文件存在但未修改，检查修改时间
                    src_mtime = (self.project_root / src_file).stat().st_mtime
                    test_mtime = full_test_path.stat().st_mtime
                    
                    if src_mtime > test_mtime:
                        violations.append({
                            "file": src_file,
                            "reason": "源代码修改时间晚于测试文件，可能未遵循 TDD",
                            "suggestion": "请确认是否先更新了测试"
                        })
        
        if violations:
            return {
                "status": "fail",
                "message": f"检测到 {len(violations)} 个 TDD 流程违规",
                "violations": violations,
                "suggestion": "请删除违规的源代码，先编写测试，再重新实现"
            }
        else:
            return {
                "status": "pass",
                "message": "TDD 流程正确 ✓",
                "violations": [],
                "summary": {
                    "src_changes": len(src_changes),
                    "test_changes": len(test_changes)
                }
            }
    
    def _infer_test_file(self, src_file: str, src_dir: str, test_dir: str) -> Optional[str]:
        """推断源代码对应的测试文件
        
        Args:
            src_file: 源代码文件路径
            src_dir: 源代码目录
            test_dir: 测试目录
            
        Returns:
            推断的测试文件路径，或 None
        """
        # 移除 src_dir 前缀
        relative_path = src_file[len(src_dir):].lstrip('/')
        
        # 转换文件名
        # src/utils/parser.py → tests/utils/test_parser.py
        # src/main.py → tests/test_main.py
        
        path_parts = Path(relative_path).parts
        if not path_parts:
            return None
        
        # 构建测试文件路径
        test_parts = list(path_parts[:-1])  # 目录部分
        filename = path_parts[-1]
        
        # 添加 test_ 前缀
        if filename.startswith('test_'):
            test_filename = filename
        else:
            name, ext = os.path.splitext(filename)
            test_filename = f"test_{name}{ext}"
        
        test_parts.append(test_filename)
        
        return f"{test_dir}/{'/'.join(test_parts)}"


def main():
    parser = argparse.ArgumentParser(description="TDD Runner — 测试驱动开发流程工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # red 命令
    red_parser = subparsers.add_parser("red", help="红灯阶段：运行测试，期望失败")
    red_parser.add_argument("test_file", help="测试文件路径")
    
    # green 命令
    green_parser = subparsers.add_parser("green", help="绿灯阶段：运行测试，期望通过")
    green_parser.add_argument("test_file", help="测试文件路径")
    
    # cycle 命令
    cycle_parser = subparsers.add_parser("cycle", help="完整红绿重构循环")
    cycle_parser.add_argument("test_file", help="测试文件路径")
    cycle_parser.add_argument("src_file", help="源代码文件路径")
    
    # strict 命令
    strict_parser = subparsers.add_parser("strict", help="强制 TDD 检查")
    strict_parser.add_argument("--check", action="store_true", help="执行检查")
    strict_parser.add_argument("--src-dir", default="src", help="源代码目录")
    strict_parser.add_argument("--test-dir", default="tests", help="测试目录")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    runner = TDDRunner()
    
    if args.command == "red":
        result = runner.red(args.test_file)
    elif args.command == "green":
        result = runner.green(args.test_file)
    elif args.command == "cycle":
        result = runner.cycle(args.test_file, args.src_file)
    elif args.command == "strict":
        if args.check:
            result = runner.strict_check(args.src_dir, args.test_dir)
        else:
            print("请使用 --check 参数执行检查")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("status") in ("fail", "error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
