#!/usr/bin/env python3
"""
七维分析框架 - 深度股票分析
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# 添加脚本目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from analyzers import (
    DataCollector,
    FundamentalAnalyzer,
    ValuationAnalyzer,
    IndustryAnalyzer,
    TechnicalAnalyzer,
    RiskAnalyzer,
    ConclusionGenerator
)

from adapters import (
    EfinanceAdapter,
    AkshareAdapter,
    QverisAdapter
)

from reporters import MarkdownReporter, JSONReporter


# 维度映射
DIMENSIONS = {
    'data': DataCollector,
    'fundamental': FundamentalAnalyzer,
    'valuation': ValuationAnalyzer,
    'industry': IndustryAnalyzer,
    'technical': TechnicalAnalyzer,
    'risk': RiskAnalyzer,
    'conclusion': ConclusionGenerator
}


# 数据源适配器
ADAPTERS = {
    'efinance': EfinanceAdapter,
    'akshare': AkshareAdapter,
    'qveris': QverisAdapter
}


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='七维分析框架 - 深度股票分析',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
可用维度:
  data         数据收集与验证
  fundamental  基本面分析
  valuation    估值分析
  industry     行业与竞争分析
  technical    技术面分析
  risk         风险识别
  conclusion   结论输出

示例:
  %(prog)s 600519                    # 基础分析
  %(prog)s 600519 --full             # 完整分析
  %(prog)s 600519 -d fundamental     # 仅基本面
  %(prog)s 600519 -d fun,val,tech    # 多维度
  %(prog)s 600519 -o json            # JSON 输出
        """
    )

    parser.add_argument('symbol', help='股票代码（如 600519）或名称')

    parser.add_argument(
        '--full', '-f',
        action='store_true',
        help='执行完整七维分析'
    )

    parser.add_argument(
        '--dimensions', '-d',
        help='指定分析维度（逗号分隔）'
    )

    parser.add_argument(
        '--sources', '-s',
        help='指定数据源（逗号分隔），默认：efinance,akshare'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['markdown', 'json', 'brief'],
        default='markdown',
        help='输出格式（默认：markdown）'
    )

    parser.add_argument(
        '--output-file',
        help='输出到文件（不指定则输出到控制台）'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细过程'
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()

    # 确定要执行的维度
    if args.full:
        dimensions = list(DIMENSIONS.keys())
    elif args.dimensions:
        dim_map = {d[0]: d for d in DIMENSIONS.keys()}
        dimensions = []
        for d in args.dimensions.split(','):
            d = d.strip()
            if d in DIMENSIONS:
                dimensions.append(d)
            elif d in dim_map:
                dimensions.append(dim_map[d])
            else:
                print(f"警告: 未知维度 '{d}'，跳过")
    else:
        # 默认维度
        dimensions = ['fundamental', 'valuation', 'risk', 'conclusion']

    # 确定数据源
    if args.sources:
        sources = [s.strip() for s in args.sources.split(',')]
        sources = [s for s in sources if s in ADAPTERS]
    else:
        sources = ['efinance', 'akshare']

    if not sources:
        print("错误: 未指定有效的数据源")
        return 1

    print(f"🔍 开始分析股票: {args.symbol}")
    print(f"📊 分析维度: {', '.join(dimensions)}")
    print(f"🔌 数据源: {', '.join(sources)}")
    print()

    # 初始化数据源适配器
    adapters = {}
    for source in sources:
        try:
            adapter_class = ADAPTERS[source]
            adapters[source] = adapter_class()
            if args.verbose:
                print(f"  ✓ {source} 适配器初始化成功")
        except Exception as e:
            print(f"  ✗ {source} 适配器初始化失败: {e}")

    if not adapters:
        print("错误: 所有数据源初始化失败")
        return 1

    # 执行分析
    results = {}
    for dim in dimensions:
        if dim not in DIMENSIONS:
            continue

        analyzer_class = DIMENSIONS[dim]
        try:
            analyzer = analyzer_class(adapters, verbose=args.verbose)
            print(f"📈 执行 {analyzer.name}...")
            result = analyzer.analyze(args.symbol)
            results[dim] = result
            if args.verbose:
                print(f"  ✓ {analyzer.name} 完成")
        except Exception as e:
            print(f"  ✗ {analyzer.name} 失败: {e}")
            results[dim] = {'error': str(e)}

    # 生成报告
    if args.output == 'json':
        reporter = JSONReporter()
    else:
        reporter = MarkdownReporter()

    report = reporter.generate(args.symbol, results, full=args.full)

    # 输出报告
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ 报告已保存到: {args.output_file}")
    else:
        print("\n" + "=" * 80)
        print(report)

    return 0


if __name__ == '__main__':
    sys.exit(main())
