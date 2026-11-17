#!/usr/bin/env python3
"""自动报表生成器 - 主入口脚本"""

import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import parser, charts, ai_analyzer, report_builder, templates, quota


def main():
    parser_cli = argparse.ArgumentParser(
        description='自动报表生成器 - 从数据文件生成分析报表',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_cli.add_argument('--input', '-i', required=True, help='输入数据文件路径 (CSV/Excel)')
    parser_cli.add_argument('--output', '-o', default='report.xlsx', help='输出报表路径 (默认: report.xlsx)')
    parser_cli.add_argument('--template', '-t', default='custom',
                            choices=['monthly_operation', 'financial', 'sales', 'data_comparison', 'custom'],
                            help='报表模板 (默认: custom)')
    parser_cli.add_argument('--tier', default='free',
                            choices=['free', 'std', 'pro', 'max'],
                            help='用户等级，决定AI分析额度 (默认: free)')
    parser_cli.add_argument('--api-key', help='AI API密钥 (可选，不提供则跳过AI分析)')
    parser_cli.add_argument('--api-base', default='https://api.openai.com/v1',
                            help='AI API基础URL (默认: https://api.openai.com/v1)')
    parser_cli.add_argument('--no-ai', action='store_true', help='跳过AI分析')
    parser_cli.add_argument('--sheet', default=None, help='Excel工作表名称 (仅Excel文件)')

    args = parser_cli.parse_args()

    # 验证输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    # 加载数据
    print(f"正在加载数据: {args.input}")
    if input_path.suffix.lower() == '.csv':
        df = parser.load_csv(str(input_path))
    elif input_path.suffix.lower() in ('.xlsx', '.xls'):
        df = parser.load_excel(str(input_path), sheet=args.sheet)
    else:
        print(f"错误: 不支持的文件格式: {input_path.suffix}", file=sys.stderr)
        sys.exit(1)

    print(f"数据加载完成: {len(df)} 行, {len(df.columns)} 列")

    # 获取统计数据
    stats = parser.get_stats(df)
    print(f"数据统计完成")

    # 生成图表
    chart_paths = []
    if not df.select_dtypes(include=['number']).columns.empty:
        numeric_col = df.select_dtypes(include=['number']).columns[0]
        try:
            chart_path = charts.generate_chart(df, numeric_col, 'line')
            chart_paths.append(chart_path)
            print(f"图表生成完成: {chart_path}")
        except Exception as e:
            print(f"图表生成跳过: {e}")

    # AI 分析
    ai_analysis = ""
    if not args.no_ai and args.api_key:
        quota_result = quota.check_quota(args.tier, 1)
        if quota_result['allowed']:
            print(f"正在进行AI分析 (剩余额度: {quota_result['remaining']})...")
            ai_analysis = ai_analyzer.analyze_data(df, args.api_key, args.api_base)
            quota.increment(args.tier)
        else:
            print(f"AI分析跳过: {quota_result['message']}")
    else:
        print("AI分析已跳过")

    # 获取模板
    template = templates.get_template(args.template)

    # 构建报表
    report_data = {
        'title': f'{template["name"]} - {input_path.stem}',
        'stats': stats,
        'charts': chart_paths,
        'ai_analysis': ai_analysis,
        'raw_data': df,
        'template': template['name'],
    }

    print(f"正在生成报表: {args.output}")
    output_path = report_builder.build_excel_report(report_data, args.output)
    print(f"报表生成完成: {output_path}")


if __name__ == '__main__':
    main()
