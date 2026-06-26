#!/usr/bin/env python3
"""
DataWorks Task Instance Log Diagnostician

Analyzes task instance logs and provides diagnostic recommendations.

Usage:
    python3 diagnose_log.py <log_file_or_text> [options]
    cat log.txt | python3 diagnose_log.py
    python3 diagnose_log.py --instance-id 12345678

Examples:
    python3 diagnose_log.py error.log
    python3 diagnose_log.py --instance-id 12345678
    cat log.txt | python3 diagnose_log.py --json
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Common error patterns and solutions
ERROR_PATTERNS = {
    'resource_quota': {
        'patterns': [
            r'quota exceeded',
            r'resource.*insufficient',
            r'no.*resource',
            r'queue.*full',
            r'max.*limit',
            r'资源.*不足',
            r'配额.*超限',
        ],
        'severity': 'high',
        'title': '资源配额不足',
        'solutions': [
            '检查当前资源组的使用情况，释放闲置资源',
            '联系管理员提升资源配额',
            '优化任务配置，减少资源消耗',
            '考虑错峰调度，避开资源使用高峰',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/resource-group.html',
    },
    'resource_expired': {
        'patterns': [
            r'独享资源组.*过期',
            r'资源组.*过期',
            r'bill.*exception',
            r'checking.*bill',
            r'checkexclusivebillavailable',
            r'任务实例.*欠费',
            r'account.*overdue',
        ],
        'severity': 'high',
        'title': '资源组已过期/欠费',
        'solutions': [
            '登录阿里云控制台，检查独享资源组的计费状态',
            '资源组已过期，需要续费或重新购买',
            '检查账户余额，确保有足够资金',
            '如已续费，等待 5-10 分钟后重试任务',
            '联系阿里云客服确认资源组状态',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/billing.html',
    },
    'connection_timeout': {
        'patterns': [
            r'connection.*timeout',
            r'timeout.*connect',
            r'network.*unreachable',
            r'host.*unreachable',
        ],
        'severity': 'high',
        'title': '网络连接超时',
        'solutions': [
            '检查数据源网络连接是否正常',
            '验证白名单配置，确保 DataWorks IP 已添加',
            '检查防火墙规则',
            '增加连接超时时间配置',
            '使用 VPC 网络时，检查网络连通性',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/network.html',
    },
    'permission_denied': {
        'patterns': [
            r'permission.*denied',
            r'access.*denied',
            r'unauthorized',
            r'authentication.*failed',
            r'invalid.*credential',
        ],
        'severity': 'high',
        'title': '权限不足',
        'solutions': [
            '检查数据源账号权限是否足够',
            '验证 AccessKey 是否有效',
            '确认 RAM 角色授权配置',
            '检查数据源白名单设置',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/permission.html',
    },
    'syntax_error': {
        'patterns': [
            r'syntax.*error',
            r'parse.*error',
            r'invalid.*syntax',
            r'line \d+.*error',
        ],
        'severity': 'medium',
        'title': 'SQL/代码语法错误',
        'solutions': [
            '检查 SQL 语法是否正确',
            '验证表名、字段名是否存在',
            '检查特殊字符是否需要转义',
            '使用语法检查工具预验证',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/sql-reference.html',
    },
    'odps_error': {
        'patterns': [
            r'odps-\d+:\[\d+,\d+\]',
            r'semantic.*analysis.*exception',
            r'function.*cannot.*be.*resolved',
            r'view.*cannot.*be.*resolved',
            r'illegal.*implicit.*type.*cast',
            r'table.*does.*not.*exist',
            r'column.*ambiguous',
            r'odpscmd.*failed',
            r'FAILED: ODPS',
        ],
        'severity': 'high',
        'title': 'ODPS SQL 执行失败',
        'solutions': [
            '检查 SQL 中使用的函数是否存在（如 BOUND_INDEX）',
            '验证表名、字段名是否正确',
            '检查数据类型转换是否合法',
            '查看 Log View 获取详细错误信息',
            '在 DataWorks 数据开发中先试运行 SQL',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/odps-sql.html',
    },
    'null_pointer': {
        'patterns': [
            r'nullpointerexception',
            r'null.*pointer',
            r'should not be (blank|null|empty)',
            r'参数.*为空',
            r'缺少.*参数',
        ],
        'severity': 'high',
        'title': '空指针/参数缺失',
        'solutions': [
            '检查任务配置中的必填参数是否已填写',
            '验证数据源连接信息（用户名、密码、URL）是否完整',
            '检查调度参数是否配置正确',
            '查看节点配置，确认所有必填字段都已填写',
            '如果是自定义脚本，检查代码中的空值处理',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/node-configuration.html',
    },
    'missing_access_key': {
        'patterns': [
            r'di_serv_render_006',
            r'没有指定.*accessid',
            r'没有指定.*accesskey',
            r'accessid.*not.*specified',
            r'accesskey.*not.*specified',
            r'writer 插件.*access',
        ],
        'severity': 'high',
        'title': '数据集成缺少 AK 配置',
        'solutions': [
            '检查数据同步任务的 writer 端配置',
            '在 Holo 写入插件中填写 AccessId 和 AccessKey',
            '如使用数据源，检查数据源配置中的 AK 信息',
            '建议使用 RAM 子账号的 AK，不要用主账号',
            '确认 AK 有 Hologres 的写入权限',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/data-integration.html',
    },
    'db_connection_failed': {
        'patterns': [
            r'communications.*link.*failure',
            r'unknown.*host',
            r'cannot.*connect.*database',
            r'connection.*refused',
            r'mysqlerrcode',
            r'datax.*无法连接',
            r'name.*or.*service.*not.*known',
            r'dbutil.*test.*connection.*failed',
        ],
        'severity': 'high',
        'title': '数据库连接失败',
        'solutions': [
            '检查 JDBC URL 是否正确（IP、端口、数据库名）',
            '验证域名是否可以解析（DNS 问题）',
            '检查 RDS 实例是否正在运行',
            '确认白名单配置，添加 DataWorks IP 到 RDS 白名单',
            '检查网络类型（VPC/公网）是否匹配',
            '验证账号密码是否正确',
            '如果是 VPC 网络，确保 DataWorks 和 RDS 在同一 VPC',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/database-connection.html',
    },
    'table_not_found': {
        'patterns': [
            r'table.*not.*found',
            r"table.*doesn't.*exist",
            r'object.*not.*found',
            r'relation.*does not exist',
        ],
        'severity': 'medium',
        'title': '表不存在',
        'solutions': [
            '确认表名拼写是否正确',
            '检查表是否在指定数据库中',
            '验证表是否已被删除或重命名',
            '检查分区表分区是否存在',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/table-management.html',
    },
    'data_quality': {
        'patterns': [
            r'data.*quality.*check.*failed',
            r'quality.*rule.*violation',
            r'null.*not.*allowed',
            r'constraint.*violation',
        ],
        'severity': 'medium',
        'title': '数据质量问题',
        'solutions': [
            '检查数据质量规则配置',
            '分析源数据是否存在异常值',
            '验证数据类型是否匹配',
            '检查是否有空值违反约束',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/data-quality.html',
    },
    'memory_overflow': {
        'patterns': [
            r'out.*of.*memory',
            r'memory.*overflow',
            r'heap.*space',
            r'gc.*overhead',
        ],
        'severity': 'high',
        'title': '内存溢出',
        'solutions': [
            '增加任务内存配置',
            '优化 SQL，减少数据处理量',
            '使用分区裁剪减少扫描数据',
            '检查是否有数据倾斜',
            '考虑分批次处理数据',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/performance-tuning.html',
    },
    'disk_full': {
        'patterns': [
            r'disk.*full',
            r'no.*space.*left',
            r'storage.*exhausted',
        ],
        'severity': 'high',
        'title': '磁盘空间不足',
        'solutions': [
            '清理临时文件和历史数据',
            '检查输出表数据量是否异常',
            '增加磁盘配额',
            '优化任务减少中间数据',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/storage.html',
    },
    'dependency_failed': {
        'patterns': [
            r'dependency.*failed',
            r'upstream.*failed',
            r'parent.*node.*failed',
        ],
        'severity': 'medium',
        'title': '上游依赖失败',
        'solutions': [
            '检查上游节点运行状态',
            '查看上游节点的错误日志',
            '调整依赖关系配置',
            '考虑添加重试机制',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/dependency.html',
    },
    'api_rate_limit': {
        'patterns': [
            r'rate.*limit.*exceeded',
            r'too.*many.*requests',
            r'qps.*limit.*exceeded',
            r'api.*throttl',
            r'request.*rate.*limit',
        ],
        'severity': 'medium',
        'title': 'API 调用限流',
        'solutions': [
            '降低 API 调用频率',
            '添加重试和退避机制',
            '申请提升 API 配额',
            '使用批量接口替代单次调用',
        ],
        'docs': 'https://help.aliyun.com/document_detail/dataworks/api-limits.html',
    },
}

# Error severity levels
SEVERITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}


def analyze_log(log_text):
    """
    Analyze log text and identify error patterns
    
    Returns list of detected issues with recommendations
    """
    issues = []
    log_lower = log_text.lower()
    
    for error_type, config in ERROR_PATTERNS.items():
        matched = False
        matched_pattern = None
        
        for pattern in config['patterns']:
            if re.search(pattern, log_lower, re.IGNORECASE):
                matched = True
                matched_pattern = pattern
                break
        
        if matched:
            # Extract relevant log lines
            relevant_lines = []
            for line in log_text.split('\n'):
                if re.search(matched_pattern, line, re.IGNORECASE):
                    relevant_lines.append(line.strip())
            
            issues.append({
                'type': error_type,
                'title': config['title'],
                'severity': config['severity'],
                'matched_pattern': matched_pattern,
                'relevant_lines': relevant_lines[:5],  # Top 5 matching lines
                'solutions': config['solutions'],
                'docs': config['docs'],
            })
    
    # Sort by severity
    issues.sort(key=lambda x: SEVERITY_ORDER.get(x['severity'], 99))
    
    return issues


def generate_report(issues, instance_id=None):
    """Generate diagnostic report"""
    output = []
    
    output.append("=" * 70)
    output.append("🔍 DataWorks 任务实例诊断报告")
    output.append("=" * 70)
    
    if instance_id:
        output.append(f"实例 ID: {instance_id}")
    
    output.append(f"发现问题数：{len(issues)}")
    output.append("")
    
    if not issues:
        output.append("✅ 未发现已知错误模式")
        output.append("")
        output.append("建议:")
        output.append("  - 检查业务逻辑是否正确")
        output.append("  - 查看完整日志寻找其他错误信息")
        output.append("  - 联系技术支持获取帮助")
    else:
        for i, issue in enumerate(issues, 1):
            severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(issue['severity'], '⚪')
            
            output.append("-" * 70)
            output.append(f"{severity_icon} 问题 {i}: {issue['title']}")
            output.append(f"   类型：{issue['type']}")
            output.append(f"   严重程度：{issue['severity'].upper()}")
            output.append("")
            
            if issue['relevant_lines']:
                output.append("   相关日志:")
                for line in issue['relevant_lines'][:3]:
                    output.append(f"     > {line[:100]}")
                output.append("")
            
            output.append("   建议解决方案:")
            for j, solution in enumerate(issue['solutions'], 1):
                output.append(f"     {j}. {solution}")
            output.append("")
            output.append(f"   参考文档：{issue['docs']}")
            output.append("")
    
    output.append("=" * 70)
    output.append("💡 提示：根据上述建议逐一排查，通常可以解决 90% 的常见问题")
    output.append("=" * 70)
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Diagnose DataWorks task instance log",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s error.log
  %(prog)s --instance-id 12345678
  cat log.txt | %(prog)s
  %(prog)s --json < log.txt
        """
    )
    
    parser.add_argument("log_file", nargs='?', help="Log file to analyze")
    parser.add_argument("--instance-id", help="Task instance ID")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output as JSON")
    parser.add_argument("--summary", "-s", action="store_true",
                       help="Show summary only")
    
    args = parser.parse_args()
    
    # Read log content
    if args.log_file:
        try:
            log_text = Path(args.log_file).read_text()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        # Read from stdin
        log_text = sys.stdin.read()
    else:
        print("Error: No log content provided. Provide a file or pipe content to stdin.", file=sys.stderr)
        sys.exit(1)
    
    if not log_text.strip():
        print("Error: No log content provided", file=sys.stderr)
        sys.exit(1)
    
    # Analyze
    issues = analyze_log(log_text)
    
    # Output
    if args.json:
        output = {
            'instance_id': args.instance_id,
            'issues_found': len(issues),
            'issues': issues,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.summary:
        print(f"📊 发现 {len(issues)} 个问题")
        for issue in issues:
            icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(issue['severity'], '⚪')
            print(f"  {icon} {issue['title']} ({issue['severity']})")
    else:
        report = generate_report(issues, args.instance_id)
        print(report)


if __name__ == "__main__":
    main()
