#!/usr/bin/env python3
"""
collectors/cli.py - 统一CLI入口

支持多种采集命令:
- collect: 通用采集
- batch: 批量采集
- eastmoney: 东方财富数据
- xueqiu: 雪球数据
- proxy: 代理池测试
- test: 快速测试

Usage:
    python3 collectors/cli.py collect --url https://example.com
    python3 collectors/cli.py batch --file urls.txt --workers 3
    python3 collectors/cli.py eastmoney --stock 600519 --type basic
"""

import sys
import argparse
import json
from pathlib import Path

# 确保 collectors 模块可导入
sys.path.insert(0, str(Path(__file__).parent.parent))

from collectors.base import StructuredItem
from collectors.registry import get_registry


def cmd_collect(args):
    """通用采集命令"""
    from collectors.builtin.browser_collector import BrowserCollector
    from collectors.adapters.extraction.structure import DocumentItem

    collector = BrowserCollector(headless=True)

    # 支持适配器
    adapter = None
    if args.adapter:
        adapter = args.adapter

    item = collector.collect(
        args.url,
        adapter=adapter,
        wait_selector=args.wait_selector,
        wait_time=args.wait_time,
    )

    print(f"✅ 采集成功!")
    print(f"标题: {item.title}")
    print(f"质量: {item.quality_score:.2f}")
    print(f"URL: {item.url}")

    # 根据返回类型显示不同字段
    if isinstance(item, DocumentItem):
        print(f"字数: {item.word_count}")
        print(f"代码块: {item.code_block_count}")
        if item.author:
            print(f"作者: {item.author}")
    else:
        # StructuredItem 兼容
        if hasattr(item, 'platform'):
            print(f"平台: {item.platform}")

    if item.content:
        preview = item.content[:300].replace('\n', ' ')
        print(f"\n内容预览:\n{preview}...")

    collector.close()
    return 0


def cmd_batch(args):
    """批量采集命令"""
    from collectors.builtin.browser_collector import BrowserCollector

    # 加载URL列表
    urls = []
    if args.file:
        with open(args.file, 'r') as f:
            urls = [line.strip() for line in f
                    if line.strip() and not line.startswith('#')]
    elif args.urls:
        urls = args.urls.split(',')
    else:
        print("错误: 必须指定 --file 或 --urls")
        return 1

    print(f"📋 加载了 {len(urls)} 个URL")

    collector = BrowserCollector(headless=True)

    with collector.batch(max_workers=args.workers) as batch:
        def progress(done, total):
            pct = done / total * 100 if total else 0
            print(f"\r进度: {done}/{total} ({pct:.1f}%)", end='', flush=True)

        items = batch.collect_urls(urls, progress_callback=progress)
        print(f"\n\n✅ 完成! 采集了 {len(items)} 个结果")

    collector.close()
    return 0


def cmd_eastmoney(args):
    """东方财富数据命令"""
    try:
        from collectors.builtin.eastmoney import EastMoneyCollector
    except ImportError:
        print("错误: eastmoney 模块不可用")
        return 1

    collector = EastMoneyCollector()

    if args.type == 'basic':
        data = collector.get_stock_basic(args.stock)
        print(f"股票 {args.stock} 基本信息:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.type == 'realtime':
        data = collector.get_realtime_quote([args.stock])
        print(f"股票 {args.stock} 实时行情:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"不支持的类型: {args.type}")
        return 1

    return 0


def cmd_xueqiu(args):
    """雪球数据命令"""
    try:
        from collectors.builtin.xueqiu import XueqiuCollector
    except ImportError:
        print("错误: xueqiu 模块不可用")
        return 1

    collector = XueqiuCollector()

    if args.type == 'discussion':
        data = collector.get_discussions(args.symbol, limit=args.limit)
        print(f"雪球 {args.symbol} 最新讨论:")
        for item in data[:5]:
            print(f"  - {item.get('title', item.get('content', '')[:50])}")
    elif args.type == 'quote':
        data = collector.get_stock_quote(args.symbol)
        print(f"雪球 {args.symbol} 股票行情:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"不支持的类型: {args.type}")
        return 1

    return 0


def cmd_proxy(args):
    """代理池测试命令"""
    from collectors.proxy_pool import ProxyPool, SyncProxyPool

    if args.test:
        pool = ProxyPool()
        print("🌐 测试代理池...")

        proxy = pool.get_proxy()
        if proxy:
            print(f"✅ 获取到代理: {proxy}")
        else:
            print("⚠️ 代理池为空")

        # 显示统计
        stats = pool.get_statistics()
        print(f"\n代理池统计: {json.dumps(stats, indent=2)}")
        return 0

    print("代理池CLI")
    print("  --test: 测试代理池")
    return 0


def cmd_test(args):
    """快速测试命令"""
    print("🧪 运行快速测试...")

    # 测试 base.py 导入
    try:
        from collectors.base import StructuredItem, StockQuote, Discussion
        print("✅ collectors.base 导入成功")
    except Exception as e:
        print(f"❌ collectors.base 导入失败: {e}")
        return 1

    # 测试 StructuredItem
    try:
        item = StructuredItem(
            title="测试标题",
            url="https://example.com",
            platform="test",
            content="测试内容",
            quality_score=0.9,
        )
        print(f"✅ StructuredItem 创建成功: {item}")
    except Exception as e:
        print(f"❌ StructuredItem 创建失败: {e}")
        return 1

    # 测试 Registry
    try:
        from collectors.registry import CollectorRegistry, get_registry
        registry = get_registry()
        print(f"✅ Registry 初始化成功，共 {len(registry.list_all())} 个采集器")
    except Exception as e:
        print(f"❌ Registry 初始化失败: {e}")
        return 1

    # 测试 BrowserCollector 导入
    try:
        from collectors.builtin.browser_collector import BrowserCollector
        print("✅ BrowserCollector 导入成功")
    except Exception as e:
        print(f"⚠️ BrowserCollector 导入失败: {e}")

    print("\n✅ 所有测试通过!")
    return 0


def cmd_registry_list(args):
    """列出所有注册适配器"""
    # 触发所有内置适配器的导入和注册
    from collectors.adapters.builtin import AliyunDocAdapter
    from collectors.adapters.builtin.cloud_docs.coze import CozeDocAdapter
    try:
        from collectors.adapters.builtin.api_docs import KimiApiAdapter
    except ImportError:
        pass
    try:
        from collectors.adapters.builtin.api_docs import MiniMaxApiAdapter
    except ImportError:
        pass
    from collectors.adapters.builtin.social.github import GitHubAdapter
    from collectors.adapters.builtin.social.zhihu import ZhihuAdapter
    from collectors.adapters.builtin.social.juejin import JuejinAdapter
    from collectors.adapters.builtin.social.csdn import CsdnAdapter

    from collectors.adapters.base import get_registry
    registry = get_registry()

    adapters = registry.list_all()
    print(f"📦 注册的适配器 ({len(adapters)} 个):")
    for name in adapters:
        adapter = registry.get(name)
        print(f"  - {name} ({adapter.__class__.__name__})")

    print(f"\n域名映射 ({len(registry._domains)} 个):")
    for domain, adapter_name in registry._domains.items():
        print(f"  {domain} → {adapter_name}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Browser Collector CLI - 统一的采集器命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # collect 命令
    collect_parser = subparsers.add_parser('collect', help='通用采集')
    collect_parser.add_argument('--url', required=True, help='目标URL')
    collect_parser.add_argument('--adapter', help='适配器名称')
    collect_parser.add_argument('--wait-selector', help='等待元素选择器')
    collect_parser.add_argument('--wait-time', type=float, default=2.0, help='等待时间(秒)')

    # batch 命令
    batch_parser = subparsers.add_parser('batch', help='批量采集')
    batch_parser.add_argument('--file', help='URL文件路径')
    batch_parser.add_argument('--urls', help='URL列表(逗号分隔)')
    batch_parser.add_argument('--workers', type=int, default=3, help='并发数')

    # eastmoney 命令
    eastmoney_parser = subparsers.add_parser('eastmoney', help='东方财富数据')
    eastmoney_parser.add_argument('--stock', required=True, help='股票代码')
    eastmoney_parser.add_argument('--type', choices=['basic', 'realtime'], default='basic', help='数据类型')

    # xueqiu 命令
    xueqiu_parser = subparsers.add_parser('xueqiu', help='雪球数据')
    xueqiu_parser.add_argument('--symbol', required=True, help='股票代码')
    xueqiu_parser.add_argument('--type', choices=['discussion', 'quote'], default='discussion', help='数据类型')
    xueqiu_parser.add_argument('--limit', type=int, default=10, help='返回数量')

    # proxy 命令
    proxy_parser = subparsers.add_parser('proxy', help='代理池管理')
    proxy_parser.add_argument('--test', action='store_true', help='测试代理池')

    # test 命令
    test_parser = subparsers.add_parser('test', help='快速测试')

    # registry 命令
    registry_parser = subparsers.add_parser('registry', help='采集器注册表')
    registry_parser.add_argument('--list', action='store_true', help='列出所有采集器')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # 命令分发
    if args.command == 'collect':
        return cmd_collect(args)
    elif args.command == 'batch':
        return cmd_batch(args)
    elif args.command == 'eastmoney':
        return cmd_eastmoney(args)
    elif args.command == 'xueqiu':
        return cmd_xueqiu(args)
    elif args.command == 'proxy':
        return cmd_proxy(args)
    elif args.command == 'test':
        return cmd_test(args)
    elif args.command == 'registry':
        return cmd_registry_list(args)
    else:
        print(f"未知命令: {args.command}")
        return 1


if __name__ == '__main__':
    sys.exit(main())