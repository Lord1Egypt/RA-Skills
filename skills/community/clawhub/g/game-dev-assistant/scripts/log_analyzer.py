#!/usr/bin/env python3
"""游戏日志分析器 - 异常检测/崩溃分析/统计"""
import argparse
import re
import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime


# 异常模式定义
ERROR_PATTERNS = [
    (re.compile(r'(Exception|Error|FATAL|CRASH):(.+)', re.I), 'error'),
    (re.compile(r'\[ERROR\](.+)'), 'error'),
    (re.compile(r'Traceback \(most recent call last\):'), 'traceback'),
    (re.compile(r'NullReferenceException'), 'null_ref'),
    (re.compile(r'OutOfMemoryException'), 'oom'),
    (re.compile(r'SteamAPI_Init\(\) failed'), 'steam_init'),
    (re.compile(r'connection.*timeout', re.I), 'timeout'),
    (re.compile(r'Cheat.*detected|anti-cheat', re.I), 'anticheat'),
]

INFO_PATTERNS = [
    re.compile(r'\[INFO\](.+)'),
    re.compile(r'\[DEBUG\](.+)'),
]

WARN_PATTERNS = [
    re.compile(r'\[WARN\](.+)'),
    re.compile(r'\[WARNING\](.+)'),
]


def parse_log_line(line):
    """解析日志行，返回类型和内容"""
    for pattern, etype in ERROR_PATTERNS:
        m = pattern.search(line)
        if m:
            return etype, m.group(0)
    if re.search(r'\[ERROR\]|Exception|FATAL', line, re.I):
        return 'error', line.strip()
    if re.search(r'\[WARN\]', line, re.I):
        return 'warn', line.strip()
    return None, None


def analyze_single_log(file_path):
    """分析单个日志文件"""
    errors = []
    warnings = []
    line_count = 0
    error_lines = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            line_count += 1
            etype, content = parse_log_line(line)
            if etype == 'error':
                errors.append({'line': i, 'content': content[:200]})
                error_lines.append(i)
            elif etype == 'warn':
                warnings.append({'line': i, 'content': content[:200]})

    return {
        'file': str(file_path),
        'lines': line_count,
        'errors': errors,
        'error_count': len(errors),
        'warnings': warnings[:50],  # 只保留前50条
        'warning_count': len(warnings),
        'error_lines': error_lines
    }


def analyze_multi_logs(log_dir, pattern='*.log'):
    """批量分析多个日志"""
    logs = list(Path(log_dir).glob(pattern))
    results = []
    all_errors = []
    for log in logs:
        r = analyze_single_log(log)
        results.append(r)
        all_errors.extend([(log.name, e['line'], e['content']) for e in r['errors']])
    return results, all_errors


def group_similar_errors(all_errors, similarity_threshold=0.7):
    """将相似错误分组"""
    groups = Counter()
    for log_name, line_no, content in all_errors:
        # 简化：取前50字符作为分组键
        key = content[:50] if content else 'unknown'
        groups[key] += 1
    return groups.most_common(20)


def detect_crash(log_path):
    """检测崩溃"""
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    crash_indicators = [
        'FATAL ERROR',
        'Stack trace:',
        'Segmentation fault',
        'Access violation',
        'crashed',
        'Assertion failed',
    ]
    found = [ind for ind in crash_indicators if ind in content]
    if found:
        print(f"[CRASH DETECTED] 崩溃指标: {found}")
        return True
    return False


def generate_report(results, output_path=None):
    """生成分析报告"""
    total_errors = sum(r['error_count'] for r in results)
    total_warnings = sum(r['warning_count'] for r in results)
    total_lines = sum(r['lines'] for r in results)

    report = {
        'summary': {
            'total_files': len(results),
            'total_lines': total_lines,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'error_rate': f"{total_errors/total_lines*100:.2f}%" if total_lines > 0 else '0%'
        },
        'top_errors': [],
        'files': []
    }

    # 收集所有错误并分组
    all_errors = []
    for r in results:
        for e in r['errors']:
            all_errors.append((r['file'], e['line'], e['content']))
        r.pop('error_lines', None)
        r.pop('warnings', None)

    grouped = group_similar_errors(all_errors)
    for key, count in grouped:
        report['top_errors'].append({'pattern': key, 'count': count})

    report['files'] = results

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[OK] 报告已生成: {output_path}")

    # 打印摘要
    print(f"\n=== 日志分析摘要 ===")
    print(f"文件数: {len(results)}")
    print(f"总行数: {total_lines:,}")
    print(f"错误数: {total_errors}")
    print(f"警告数: {total_warnings}")
    print(f"\nTop 错误模式:")
    for key, count in grouped[:5]:
        print(f"  [{count}x] {key[:80]}")

    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='游戏日志分析')
    sub = parser.add_subparsers(dest='cmd')
    p = sub.add_parser('analyze', help='分析日志文件')
    p.add_argument('file')
    p.add_argument('--output', '-o', help='输出报告 JSON')
    p = sub.add_parser('batch', help='批量分析')
    p.add_argument('directory')
    p.add_argument('--pattern', default='*.log')
    p.add_argument('--output', '-o', help='输出报告 JSON')
    sub.add_parser('crash', help='检测崩溃').add_argument('file')
    args = parser.parse_args()
    if args.cmd == 'analyze':
        result = analyze_single_log(args.file)
        generate_report([result], args.output)
    elif args.cmd == 'batch':
        results, _ = analyze_multi_logs(args.directory, args.pattern)
        generate_report(results, args.output)
    elif args.cmd == 'crash':
        detected = detect_crash(args.file)
        if not detected:
            print("未检测到崩溃迹象")
