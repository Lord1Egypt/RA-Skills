#!/usr/bin/env python3
"""
测试报告生成器

运行 pytest 测试并生成可视化 HTML 报告
"""

import subprocess
import sys
import re
import json
import importlib.util
import os
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import webbrowser

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = PROJECT_ROOT / "cache"
PYCACHE_ROOT = CACHE_ROOT / "pycache"
TMP_ROOT = CACHE_ROOT / "tmp" / "python"
SUMMARY_REPORT_PATH = PROJECT_ROOT / "reports" / "test-results.json"
REPORT_HTML_PATH = PROJECT_ROOT / "reports" / "test-report.html"


def _configure_runtime_cache() -> None:
    """显式固定 pycache/tmp 到项目 cache 目录，避免生成 tests/__pycache__。"""
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    PYCACHE_ROOT.mkdir(parents=True, exist_ok=True)
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    sys.pycache_prefix = str(PYCACHE_ROOT)
    os.environ["PYTHONPYCACHEPREFIX"] = str(PYCACHE_ROOT)
    tempfile.tempdir = str(TMP_ROOT)


_configure_runtime_cache()


def _is_module_installed(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def _strip_cov_args(args: List[str]) -> List[str]:
    """移除 pytest-cov 相关参数，避免插件缺失时参数报错。"""
    cov_args_with_value = {
        "--cov",
        "--cov-report",
        "--cov-config",
        "--cov-fail-under",
        "--cov-context",
    }
    sanitized = []
    skip_next = False

    for arg in args:
        if skip_next:
            skip_next = False
            continue

        if arg in cov_args_with_value:
            skip_next = True
            continue

        if arg.startswith("--cov"):
            continue

        sanitized.append(arg)

    return sanitized


def run_tests_and_generate_report(test_path: str = "tests/unit", extra_args: List[str] = None):
    """运行测试并生成报告
    
    Args:
        test_path: 测试路径，默认为 tests/unit
        extra_args: 额外的 pytest 参数
    """
    print("=" * 60)
    print("[TEST] Running tests and generating report...")
    print("=" * 60)

    if not _is_module_installed("pytest"):
        print("[ERROR] pytest module is not installed.")
        print("[HINT] Install it with: python -m pip install pytest")
        return 2

    pytest_cov_installed = _is_module_installed("pytest_cov")
    
    # 构建 pytest 命令
    cmd = [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"]
    if extra_args:
        cmd.extend(extra_args)
    else:
        if pytest_cov_installed:
            cmd.append("--no-cov")

    if pytest_cov_installed:
        if "--no-cov" not in cmd:
            cmd.append("--no-cov")
    else:
        cmd = _strip_cov_args(cmd)
        # 覆盖 pytest.ini 里的 addopts，移除 --cov 相关选项
        cmd.extend(["-o", "addopts=-v --tb=short --strict-markers -ra -p tests.conftest"])
    
    print(f"\n[CMD] Running: {' '.join(cmd)}")
    
    # 运行测试
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        encoding='utf-8',
        errors='replace'  # 处理编码错误
    )
    
    # 解析输出
    output = result.stdout + result.stderr
    print("\n" + "=" * 60)
    print("[OUTPUT] Test execution output:")
    print("=" * 60)
    print(output)
    print("=" * 60)
    
    # 提取测试统计
    stats = parse_test_output(output)
    
    print(f"\n[RESULT] Test Statistics:")
    print(f"   Total: {stats['total']}")
    print(f"   Passed: {stats['passed']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Skipped: {stats['skipped']}")
    print(f"   Pass Rate: {stats['pass_rate']:.1f}%")

    save_summary_report(stats)
    
    # 生成 HTML 报告
    generate_html_report(
        stats['passed'], 
        stats['failed'], 
        stats['skipped'], 
        stats['pass_rate'],
        stats.get('suite_details', [])
    )
    
    return result.returncode


def parse_test_output(output: str) -> Dict:
    """解析 pytest 输出，提取测试统计
    
    Args:
        output: pytest 的输出文本
        
    Returns:
        包含测试统计的字典
    """
    # 查找测试结果
    passed_match = re.search(r'(\d+) passed', output)
    failed_match = re.search(r'(\d+) failed', output)
    skipped_match = re.search(r'(\d+) skipped', output)
    
    passed = int(passed_match.group(1)) if passed_match else 0
    failed = int(failed_match.group(1)) if failed_match else 0
    skipped = int(skipped_match.group(1)) if skipped_match else 0
    
    total = passed + failed + skipped
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    # 解析测试套件详情
    suite_details = []
    
    # 匹配测试文件和结果
    # 示例: tests/unit/test_config_generation.py::test_version_compatibility PASSED
    test_pattern = r'(tests[\\/][^:]+)::([^\s]+).*?(PASSED|FAILED|SKIPPED)'
    matches = re.findall(test_pattern, output)
    
    # 按文件分组
    suite_groups = {}
    for file_path, test_name, status in matches:
        if file_path not in suite_groups:
            suite_groups[file_path] = {'passed': 0, 'failed': 0, 'skipped': 0, 'tests': []}
        
        if status == 'PASSED':
            suite_groups[file_path]['passed'] += 1
        elif status == 'FAILED':
            suite_groups[file_path]['failed'] += 1
        elif status == 'SKIPPED':
            suite_groups[file_path]['skipped'] += 1
            
        suite_groups[file_path]['tests'].append({
            'name': test_name,
            'status': status.lower()
        })
    
    # 转换为列表
    for file_path, data in suite_groups.items():
        suite_total = data['passed'] + data['failed'] + data['skipped']
        suite_rate = (data['passed'] / suite_total * 100) if suite_total > 0 else 0
        suite_name = Path(file_path).stem.replace('test_', '').replace('_', ' ').title()
        
        suite_details.append({
            'name': suite_name,
            'file': file_path,
            'passed': data['passed'],
            'failed': data['failed'],
            'skipped': data['skipped'],
            'total': suite_total,
            'pass_rate': suite_rate,
            'tests': data['tests'][:10]  # 只保留前10个测试用于展示
        })
    
    return {
        'passed': passed,
        'failed': failed,
        'skipped': skipped,
        'total': total,
        'pass_rate': pass_rate,
        'suite_details': suite_details
    }


def save_summary_report(stats: Dict, output_path: Path | None = None):
    """保存测试摘要，供 report-only 等流程复用。"""
    output_path = Path(output_path) if output_path else SUMMARY_REPORT_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": {
            "total": stats["total"],
            "passed": stats["passed"],
            "failed": stats["failed"],
            "skipped": stats["skipped"],
            "pass_rate": stats["pass_rate"],
        },
        "suite_details": stats.get("suite_details", []),
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _load_report_generator():
    tests_path = PROJECT_ROOT / "tests"
    if str(tests_path) not in sys.path:
        sys.path.insert(0, str(tests_path))
    from report_generator import parse_summary_report
    return parse_summary_report


def _relative_path(path: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(PROJECT_ROOT)).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def generate_html_report(passed: int, failed: int, skipped: int, pass_rate: float, suite_details: List[Dict] = None):
    """使用统一渲染器生成 HTML 报告。"""
    parse_summary_report = _load_report_generator()
    generator = parse_summary_report(str(SUMMARY_REPORT_PATH))
    generator.output_path = REPORT_HTML_PATH
    generator.save()

    print(f"\n[SUCCESS] Test report generated: {_relative_path(REPORT_HTML_PATH)}")

    try:
        webbrowser.open(f'file:///{REPORT_HTML_PATH.absolute()}')
    except Exception as e:
        print(f"[INFO] Could not open browser: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tests and generate HTML report')
    parser.add_argument('test_path', nargs='?', default='tests/unit', help='Test path to run')
    parser.add_argument('--args', nargs='*', help='Extra pytest arguments')
    
    args = parser.parse_args()
    
    exit_code = run_tests_and_generate_report(args.test_path, args.args)
    sys.exit(exit_code)
