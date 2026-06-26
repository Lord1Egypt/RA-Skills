#!/usr/bin/env python3
"""
数据源连通性验证脚本
测试所有真实数据源的可用性和数据质量
"""

import os
import sys
import json
from datetime import datetime, date, timedelta
from pathlib import Path

# 确保从正确的目录导入
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from data_fetcher import DataFetcher
    from utils import get_logger, parse_date
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print(f"   当前脚本目录: {script_dir}")
    print(f"   sys.path: {sys.path[:3]}...")
    sys.exit(1)

logger = get_logger('data_source_verification')

def print_header(title):
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_result(name, success, data=None, source=None, error=None, latency_ms=None):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n[{status}] {name}")
    if success:
        if source:
            print(f"   数据源: {source}")
        if latency_ms is not None:
            print(f"   延迟: {latency_ms:.1f}ms")
        if data:
            # 显示数据摘要
            if isinstance(data, dict):
                print(f"   数据量: {len(data)} 个字段")
                # 显示关键字段
                for key in list(data.keys())[:5]:
                    print(f"   - {key}: {str(data[key])[:100]}")
            elif isinstance(data, list):
                print(f"   数据量: {len(data)} 条记录")
    if error:
        print(f"   错误: {error}")

def test_akshare_index():
    """测试 akshare 指数数据获取"""
    print_header("测试 1: akshare 指数数据源")

    config = {"data_source": "akshare"}
    fetcher = DataFetcher(config)

    test_date = date.today() - timedelta(days=1)  # 昨天（最近交易日）
    result = fetcher.get_index_data('000001.SH', test_date)

    success = result.get('success', False)
    data = result.get('data')
    source = result.get('source')
    error = result.get('error')

    print_result(
        "上证指数 (000001.SH)",
        success,
        data=data,
        source=source,
        error=error
    )

    if success and data:
        # 验证数据完整性
        required_fields = ['ts_code', 'name', 'close', 'change_pct']
        missing = [f for f in required_fields if f not in data]
        if missing:
            print(f"   ⚠️  缺失字段: {missing}")
        else:
            print(f"   ✅ 数据完整性检查通过")
            print(f"   - 指数名称: {data.get('name')}")
            print(f"   - 收盘价: {data.get('close')}")
            print(f"   - 涨跌幅: {data.get('change_pct')*100:.2f}%")

    return success

def test_akshare_sectors():
    """测试 akshare 板块数据获取"""
    print_header("测试 2: akshare 板块数据源")

    config = {"data_source": "akshare"}
    fetcher = DataFetcher(config)

    test_date = date.today() - timedelta(days=1)
    result = fetcher.get_sector_data(test_date)

    success = result.get('success', False)
    data = result.get('data')
    source = result.get('source')
    error = result.get('error')

    print_result(
        "行业/概念板块排行",
        success,
        data=data,
        source=source,
        error=error
    )

    if success and data:
        industry_count = len(data.get('industry', []))
        concept_count = len(data.get('concept', []))
        print(f"   ✅ 行业板块: {industry_count} 个")
        print(f"   ✅ 概念板块: {concept_count} 个")

        if industry_count > 0:
            top_industry = data['industry'][0]
            print(f"   - 领涨行业: {top_industry['sector']} ({top_industry['change_pct']:.2f}%)")

    return success

def test_akshare_lhb():
    """测试 akshare 龙虎榜数据获取"""
    print_header("测试 3: akshare 龙虎榜数据源")

    config = {"data_source": "akshare"}
    fetcher = DataFetcher(config)

    test_date = date.today() - timedelta(days=1)
    result = fetcher.get_lhb_data(test_date)

    success = result.get('success', False)
    data = result.get('data')
    source = result.get('source')
    error = result.get('error')

    print_result(
        "龙虎榜机构席位",
        success,
        data=data,
        source=source,
        error=error
    )

    if success and data:
        print(f"   ✅ 获取到 {len(data)} 条龙虎榜记录")
        for i, item in enumerate(data[:3], 1):
            print(f"   {i}. {item['name']} ({item['code']}) 净买入: {item['net_inflow']/1e8:.2f} 亿元")

    return success

def test_yfinance():
    """测试 yfinance 美股数据获取"""
    print_header("测试 4: yfinance 美股数据源")

    config = {"data_source": "yfinance"}
    fetcher = DataFetcher(config)

    result = fetcher.get_us_market()

    success = result.get('success', False)
    data = result.get('data')
    source = result.get('source')
    error = result.get('error')

    print_result(
        "美股指数 + 中概股",
        success,
        data=data,
        source=source,
        error=error
    )

    if success and data:
        indices = data.get('indices', {})
        chinadotcom = data.get('chinadotcom', {})

        print(f"   ✅ 美股指数: {len(indices)} 个")
        for name, info in indices.items():
            print(f"   - {info['name']}: {info['close']:.2f} ({info['change_pct']*100:+.2f}%)")

        print(f"   ✅ 中概股/港股: {len(chinadotcom)} 个")
        for name, info in chinadotcom.items():
            print(f"   - {info['name']} ({info['code']}): {info['close']:.2f} ({info['change_pct']*100:+.2f}%)")

    return success

def test_mx_search():
    """测试 mx-search 新闻数据获取"""
    print_header("测试 5: mx-search 财经新闻源")

    config = {"data_source": "mx-search", "news_limit": 5}
    fetcher = DataFetcher(config)

    test_date = date.today() - timedelta(days=1)
    result = fetcher.get_news(test_date, limit=5)

    success = result.get('success', False)
    data = result.get('data')
    source = result.get('source')
    error = result.get('error')

    print_result(
        "财经新闻 (mx-search)",
        success,
        data=data,
        source=source,
        error=error
    )

    if success and data:
        news_list = data.get('news', [])
        print(f"   ✅ 获取到 {len(news_list)} 条新闻")
        for i, news in enumerate(news_list[:3], 1):
            title = news.get('title', '')[:80]
            print(f"   {i}. {title}...")
            print(f"      来源: {news.get('source', '未知')}")

    return success

def test_env_config():
    """测试环境配置"""
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent.parent  # workspace-trader/
    print_header("测试 6: 环境配置检查")

    checks = []

    # 检查 .env 文件
    env_path = project_root / '.env'
    env_exists = env_path.exists()
    checks.append(('.env 文件', env_exists))

    if env_exists:
        print("   ✅ .env 文件存在")
        # 检查 MX_APIKEY
        mx_apikey = os.environ.get('MX_APIKEY')
        if mx_apikey:
            print(f"   ✅ MX_APIKEY 已配置 (长度: {len(mx_apikey)})")
        else:
            print("   ⚠️  MX_APIKEY 未设置 (mx-search 新闻源将无法使用)")
    else:
        print("   ⚠️  .env 文件不存在")

    # 检查技能目录
    skill_dir = project_root / 'skills' / 'a-share-daily-report'
    if skill_dir.exists():
        print(f"   ✅ 技能目录存在: {skill_dir}")
    else:
        print(f"   ❌ 技能目录缺失: {skill_dir}")
        return False

    # 检查虚拟环境
    venv_python = project_root / 'venv' / 'bin' / 'python3'
    if venv_python.exists():
        print(f"   ✅ 虚拟环境存在: {venv_python}")
    else:
        print(f"   ⚠️  虚拟环境不存在: {venv_python}")

    return True

def main():
    print("🔍 A股日报生成器 - 数据源连通性验证")
    print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 测试日期基准: {date.today()} (实际使用最近交易日)")

    results = []

    # 环境检查（不中断）
    results.append(("环境配置", test_env_config()))

    # 数据源测试
    results.append(("akshare 指数", test_akshare_index()))
    results.append(("akshare 板块", test_akshare_sectors()))
    results.append(("akshare 龙虎榜", test_akshare_lhb()))
    results.append(("yfinance 美股", test_yfinance()))
    results.append(("mx-search 新闻", test_mx_search()))

    # 总结报告
    print_header("验证总结")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\n📊 总体结果: {passed}/{total} 项测试通过 ({passed/total*100:.0f}%)")

    for name, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {name}")

    # 问题清单
    failures = [name for name, success in results if not success]
    if failures:
        print("\n⚠️  需要关注的问题:")
        for name in failures:
            print(f"   - {name}")

        print("\n💡 建议排查步骤:")
        print("   1. 检查网络连接")
        print("   2. 确认依赖库已安装: pip install -r requirements.txt")
        print("   3. 检查 .env 文件配置 (特别是 MX_APIKEY)")
        print("   4. 查看日志文件获取详细错误信息")
    else:
        print("\n🎉 所有数据源均正常工作！")

    print("\n" + "="*80)
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
