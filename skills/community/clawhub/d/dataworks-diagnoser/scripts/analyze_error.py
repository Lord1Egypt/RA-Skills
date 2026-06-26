#!/usr/bin/env python3
"""
DataWorks Error Analyzer - Clean and focused error analysis

Extracts errors from logs and provides clear, actionable solutions.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def extract_errors(log_text):
    """
    Extract error codes and key error messages from log
    
    Returns list of error info dicts, sorted by severity
    """
    errors = []
    
    # Pattern 1: ODPS error codes (highest priority)
    # e.g., ODPS-0130071:[11,10] Semantic analysis exception
    odps_pattern = r'ODPS-(\d+):\[(\d+),(\d+)\]\s*([^\n]+)'
    for match in re.finditer(odps_pattern, log_text):
        errors.append({
            'type': 'ODPS',
            'code': f'ODPS-{match.group(1)}',
            'position': f'line {match.group(2)}, col {match.group(3)}',
            'message': match.group(4).strip()[:300],
            'severity': 'high',
        })
    
    # Pattern 2: DataX error codes
    # e.g., Code:[MYSQLErrCode-02], Description:[...]
    datax_pattern = r'Code:\[([^\]]+)\],\s*Description:\[([^\]]+)\]'
    for match in re.finditer(datax_pattern, log_text):
        errors.append({
            'type': 'DataX',
            'code': match.group(1),
            'message': match.group(2).strip()[:300],
            'severity': 'high',
        })
    
    # Pattern 3: Java exceptions
    exception_pattern = r'([a-zA-Z0-9_.]+Exception):\s*([^\n]+)'
    for match in re.finditer(exception_pattern, log_text):
        errors.append({
            'type': 'Exception',
            'code': match.group(1).split('.')[-1],
            'message': match.group(2).strip()[:300],
            'severity': 'medium',
        })
    
    # Remove duplicates (same error code)
    seen_codes = set()
    unique_errors = []
    for error in errors:
        key = f"{error['type']}:{error['code']}"
        if key not in seen_codes:
            seen_codes.add(key)
            unique_errors.append(error)
    
    # Sort by severity
    severity_order = {'high': 0, 'medium': 1, 'low': 2}
    unique_errors.sort(key=lambda x: severity_order.get(x['severity'], 2))
    
    return unique_errors


def analyze_error(error):
    """
    Analyze a single error and provide solutions
    
    Returns analysis dict with causes, solutions, and next steps
    """
    code = error['code']
    msg = error['message'].lower()
    
    analysis = {
        'causes': [],
        'solutions': [],
        'next_step': '',
    }
    
    # ODPS Error Analysis
    if error['type'] == 'ODPS':
        if '0130071' in code or 'semantic' in msg or 'function' in msg:
            analysis['causes'] = [
                f'SQL 中使用了不存在的函数或视图',
            ]
            analysis['solutions'] = [
                f'检查 SQL 第 {error["position"]} 处的函数：{error["message"][:100]}',
                '确认函数名称拼写正确（MaxCompute 函数区分大小写）',
                '在 DataWorks 数据开发中创建临时查询，测试该函数',
            ]
            analysis['next_step'] = '在 DataWorks 数据开发面板试运行 SQL，查看具体哪个函数不存在'
        
        elif '0130141' in code or 'cast' in msg or 'type' in msg:
            analysis['causes'] = [
                '数据类型转换失败',
            ]
            analysis['solutions'] = [
                f'检查错误位置 {error["position"]} 的数据类型',
                '使用 CAST 函数显式转换：CAST(column AS STRING)',
                '检查源数据是否包含无法转换的值',
            ]
            analysis['next_step'] = '查看 SQL 中该位置的字段类型定义'
        
        elif 'table' in msg and ('exist' in msg or 'found' in msg):
            analysis['causes'] = [
                '表不存在',
            ]
            analysis['solutions'] = [
                '检查表名拼写（包括项目空间前缀）',
                '在数据地图中搜索该表',
                '确认环境配置（开发/生产）',
            ]
            analysis['next_step'] = '在 DataWorks 数据地图中搜索表名'
        
        else:
            analysis['causes'] = ['ODPS SQL 执行错误']
            analysis['solutions'] = [
                '查看完整错误信息',
                '检查 SQL 语法',
            ]
            analysis['next_step'] = '复制完整错误信息到 DataWorks 数据开发中测试'
    
    # DataX Error Analysis
    elif error['type'] == 'DataX':
        if 'mysql' in code.lower() or 'jdbc' in msg or 'connection' in msg:
            analysis['causes'] = [
                '数据库连接失败',
            ]
            analysis['solutions'] = [
                '检查 JDBC URL 是否正确',
                '确认 RDS 白名单包含 DataWorks IP',
                '验证账号密码',
            ]
            analysis['next_step'] = '在 RDS 控制台检查白名单配置'
        
        else:
            analysis['causes'] = ['数据同步错误']
            analysis['solutions'] = [
                '检查数据源配置',
                '查看字段映射',
            ]
            analysis['next_step'] = '检查数据同步任务的读写端配置'
    
    # Exception Analysis
    elif error['type'] == 'Exception':
        if 'nullpointer' in code.lower() or 'null' in msg:
            analysis['causes'] = [
                '空指针异常 - 必填参数为空',
            ]
            analysis['solutions'] = [
                '检查任务配置中的必填字段',
                '验证上游节点是否有输出',
            ]
            analysis['next_step'] = '检查节点配置和上游依赖'
        
        else:
            analysis['causes'] = ['程序执行异常']
            analysis['solutions'] = [
                '查看完整堆栈信息',
            ]
            analysis['next_step'] = '收集完整日志联系技术支持'
    
    else:
        analysis['causes'] = ['未知错误']
        analysis['solutions'] = ['收集完整日志']
        analysis['next_step'] = '联系阿里云技术支持'
    
    return analysis


def format_report(errors, analyses, instance_id):
    """Format clean, focused report"""
    output = []
    
    output.append("=" * 70)
    output.append(f"DataWorks 任务诊断报告")
    output.append("=" * 70)
    if instance_id:
        output.append(f"实例 ID: {instance_id}")
    output.append(f"发现错误：{len(errors)} 个\n")
    
    if not errors:
        output.append("✅ 未发现明显错误")
        output.append("\n建议:")
        output.append("  - 检查业务逻辑是否正确")
        output.append("  - 查看完整日志")
    else:
        for i, (error, analysis) in enumerate(zip(errors, analyses), 1):
            output.append("-" * 70)
            output.append(f"错误 {i}: {error['type']} - {error['code']}")
            output.append("")
            
            output.append("错误信息:")
            output.append(f"  {error['message']}")
            if error.get('position'):
                output.append(f"  位置：{error['position']}")
            output.append("")
            
            output.append("可能原因:")
            for cause in analysis['causes']:
                output.append(f"  • {cause}")
            output.append("")
            
            output.append("解决方案:")
            for j, sol in enumerate(analysis['solutions'], 1):
                output.append(f"  {j}. {sol}")
            output.append("")
            
            output.append(f"下一步：{analysis['next_step']}")
            output.append("")
    
    output.append("=" * 70)
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description="DataWorks Error Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument("log_file", nargs='?', help="Log file to analyze")
    parser.add_argument("--instance-id", help="Task instance ID")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Read log content
    if args.log_file:
        try:
            log_text = Path(args.log_file).read_text()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        log_text = sys.stdin.read()
    else:
        print("Error: No log content provided", file=sys.stderr)
        sys.exit(1)
    
    # Extract errors
    errors = extract_errors(log_text)
    
    # Analyze each error
    analyses = [analyze_error(error) for error in errors]
    
    # Output
    if args.json:
        output = {
            'instance_id': args.instance_id,
            'errors': errors,
            'analyses': analyses,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        report = format_report(errors, analyses, args.instance_id)
        print(report)


if __name__ == "__main__":
    main()
