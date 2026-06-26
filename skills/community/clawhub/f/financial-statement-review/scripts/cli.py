#!/usr/bin/env python3
"""
命令行入口

提供简单的命令行接口使用财务报表审查工具
"""
import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from parsers import parse_file, FileParserManager
from strategies import StrategyManager


def review_file(file_path: str, output: str = None):
    """审查单个文件"""
    print(f"正在解析文件: {file_path}")
    
    # 解析文件
    result = parse_file(file_path)
    
    if not result.success:
        print(f"❌ 文件解析失败:")
        for error in result.errors:
            print(f"   - {error}")
        return 1
    
    print(f"✓ 文件解析成功")
    print(f"  公司: {result.data.company_name or '未知'}")
    print(f"  报表期间: {result.data.report_period or '未知'}")
    print(f"  数据来源: {result.data.source_software or '通用'}")
    
    # 提取财务数据
    data = result.data
    review_data = {
        'financial_statements': {
            'revenue': data.income_statement.get('营业收入', 0),
            'cost': data.income_statement.get('营业成本', 0),
            'profit': data.income_statement.get('净利润', 0),
            'total_assets': data.balance_sheet.get('资产总计', 0),
            'owners_equity': data.balance_sheet.get('所有者权益合计', 0),
        },
        'company_info': {
            'name': data.company_name,
        }
    }
    
    # 执行审查策略
    print("\n执行审查策略...")
    manager = StrategyManager()
    manager.load_all_strategies()
    
    results = manager.execute_all(review_data)
    
    # 生成报告
    summary = manager.generate_summary_report(results)
    print("\n" + summary)
    
    # 保存报告（如果指定输出文件）
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"\n报告已保存至: {output}")
    
    return 0


def scan_directory(directory: str, recursive: bool = False):
    """扫描目录"""
    print(f"扫描目录: {directory}")
    
    manager = FileParserManager()
    results = manager.scan_and_parse(directory, recursive=recursive)
    
    summary = manager.get_parsing_summary(results)
    
    print(f"\n扫描结果:")
    print(f"  总文件数: {summary['total_files']}")
    print(f"  解析成功: {summary['successful']}")
    print(f"  解析失败: {summary['failed']}")
    print(f"  成功率: {summary['success_rate']}")
    
    if summary['file_types']:
        print(f"\n文件类型分布:")
        for file_type, count in summary['file_types'].items():
            print(f"  {file_type}: {count}")
    
    if summary['software_types']:
        print(f"\n软件类型分布:")
        for software_type, count in summary['software_types'].items():
            print(f"  {software_type}: {count}")
    
    return 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='财务报表审查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s review report.xlsx                    # 审查单个文件
  %(prog)s review report.xlsx -o report.txt      # 审查并保存报告
  %(prog)s scan /data/reports                    # 扫描目录
  %(prog)s scan /data/reports -r                 # 递归扫描目录
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # review 命令
    review_parser = subparsers.add_parser('review', help='审查财务文件')
    review_parser.add_argument('file', help='要审查的文件路径')
    review_parser.add_argument('-o', '--output', help='输出报告文件路径')
    
    # scan 命令
    scan_parser = subparsers.add_parser('scan', help='扫描目录')
    scan_parser.add_argument('directory', help='要扫描的目录')
    scan_parser.add_argument('-r', '--recursive', action='store_true', 
                             help='递归扫描子目录')
    
    # version 命令
    version_parser = subparsers.add_parser('version', help='显示版本信息')
    
    args = parser.parse_args()
    
    if args.command == 'review':
        return review_file(args.file, args.output)
    elif args.command == 'scan':
        return scan_directory(args.directory, args.recursive)
    elif args.command == 'version':
        print("财务报表审查工具 v1.0.0")
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
