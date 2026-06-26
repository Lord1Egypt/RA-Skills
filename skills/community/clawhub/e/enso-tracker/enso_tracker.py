#!/usr/bin/env python3
"""
ENSO Tracker - Main entry point.
Track global city temperatures and analyze El Niño/La Niña phenomena.
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Add skill directory to path
SKILL_DIR = Path(__file__).parent.expanduser().absolute()
sys.path.insert(0, str(SKILL_DIR))

import numpy as np

from sources import (
    load_config,
    fetch_oni_data,
    fetch_city_temperatures,
    fetch_berkeley_earth_anomaly,
    get_current_enso_phase,
    DEFAULT_CITIES
)
from viz import (
    plot_heat_records,
    plot_enso_timeline,
    plot_enso_heat_correlation,
    plot_city_ranking,
    COLORS
)


# Default output directory
OUTPUT_DIR = Path.home() / 'Downloads'


def cmd_status(args):
    """
    Fetch current ONI, classify phase, print summary.
    """
    print("\n" + "="*50)
    print("🌊 ENSO 状态查询")
    print("="*50)

    # Fetch ONI data
    oni_df = fetch_oni_data()

    if oni_df.empty:
        print("❌ 无法获取 ONI 数据")
        return 1

    # Get latest reading
    latest = oni_df.iloc[-1]
    oni_value = latest['oni_value']
    year = int(latest['year'])
    season = latest['season']

    # Classify phase
    phase_info = get_current_enso_phase(oni_value)

    # Print summary
    print(f"\n📊 当前 ENSO 状态")
    print("-" * 30)
    print(f"ONI 指数: {oni_value:+.2f}°C")
    print(f"相位: {phase_info['phase']} ({phase_info['phase_en']})")
    print(f"强度: {phase_info['intensity']}")
    print(f"季节: {season} {year}")
    print("-" * 30)

    # Historical context
    if len(oni_df) > 12:
        last_year = oni_df[oni_df['year'] >= year - 1]
        avg_oni = last_year['oni_value'].mean()
        print(f"\n📈 过去一年平均 ONI: {avg_oni:+.2f}°C")

        # Trend
        recent = oni_df.tail(6)['oni_value'].values
        if len(recent) >= 2:
            trend = recent[-1] - recent[0]
            if trend > 0.3:
                print("📉 趋势: 指数上升中")
            elif trend < -0.3:
                print("📉 趋势: 指数下降中")
            else:
                print("📊 趋势: 相对稳定")

    print("="*50 + "\n")
    return 0


def cmd_cities(args):
    """
    Fetch top N hottest cities, generate ranking chart.
    """
    print("\n" + "="*50)
    print("🌍 全球最热城市追踪")
    print("="*50)

    # Load config for API key
    config = load_config()
    if not config:
        print("❌ 未配置 OpenWeatherMap API 密钥，请参见 SKILL.md 中的设置说明")
        return 1

    api_key = config.get('openweather_api_key')
    if not api_key:
        print("❌ API 密钥未设置")
        return 1

    # Determine cities to check
    if args.cities:
        cities = [c.strip() for c in args.cities.split(',')]
    else:
        # Use default major cities
        cities = DEFAULT_CITIES[:args.top]

    print(f"\n📍 查询城市数量: {len(cities)}")
    print(f"📊 显示前 {args.top} 名\n")

    # Fetch temperatures
    cities_data = fetch_city_temperatures(cities, api_key, rate_limit_delay=args.rate_limit)

    if not cities_data:
        print("❌ 未获取到任何城市数据")
        return 1

    # Sort and get top N
    cities_data.sort(key=lambda x: x['temp'], reverse=True)
    top_cities = cities_data[:args.top]

    # Print ranking
    print(f"\n🏆 全球最热城市 Top {args.top}")
    print("-" * 40)
    for i, city in enumerate(top_cities, 1):
        print(f"{i:2d}. {city['city']}, {city['country']:3s} - {city['temp']:.1f}°C "
              f"(体感 {city['feels_like']:.1f}°C, 湿度 {city['humidity']}%)")

    # Generate chart
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = plot_city_ranking(top_cities, str(output_path), lang=args.lang, top_n=args.top)

    if success:
        print(f"\n✅ 排名图表已保存: {output_path}")
        return 0
    else:
        return 1


def cmd_correlate(args):
    """
    Generate ENSO-India heat correlation chart.
    """
    print("\n" + "="*50)
    print("📊 ENSO 与印度高温相关性分析")
    print("="*50)

    # Fetch ONI data
    oni_df = fetch_oni_data()

    if oni_df.empty:
        print("❌ 无法获取 ONI 数据")
        return 1

    # Fetch Berkeley Earth India anomaly data (or generate sample)
    print("\n📊 获取印度温度异常数据...")

    # Try Berkeley Earth first
    berkeley_df = fetch_berkeley_earth_anomaly("India")

    if berkeley_df is not None and not berkeley_df.empty:
        # Convert Berkeley data to heat records format
        # Aggregate by year
        yearly = berkeley_df.groupby('year')['anomaly'].mean().reset_index()
        # Assume base temp around 32°C for India
        heat_records = [
            {'year': int(row['year']), 'temp': 32 + row['anomaly']}
            for _, row in yearly.iterrows()
        ]
    else:
        print("⚠️  Berkeley Earth 数据不可用，使用模拟数据...")
        # Generate sample heat records for demonstration
        years = list(range(int(oni_df['year'].min()), int(oni_df['year'].max()) + 1))
        base_temp = 36

        # Create correlation with ONI
        heat_records = []
        for year in years:
            year_oni = oni_df[oni_df['year'] == year]['oni_value']
            oni_avg = year_oni.mean() if len(year_oni) > 0 else 0

            # Higher ONI (El Niño) correlates with higher temps
            temp = base_temp + np.random.uniform(-2, 2) + oni_avg * 0.8 + (year - 1950) * 0.015
            heat_records.append({'year': year, 'temp': temp})

    # Generate correlation chart
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = plot_enso_heat_correlation(oni_df, heat_records, str(output_path), lang=args.lang)

    if success:
        print(f"\n✅ 相关性图表已保存: {output_path}")
        return 0
    else:
        return 1


def cmd_anomaly(args):
    """
    Generate temperature anomaly chart for a region.
    """
    print("\n" + "="*50)
    print(f"📈 {args.region} 温度异常分析")
    print("="*50)

    # Try to fetch Berkeley Earth data
    berkeley_df = fetch_berkeley_earth_anomaly(args.region)

    if berkeley_df is None or berkeley_df.empty:
        print(f"⚠️  {args.region} 数据不可用，使用模拟数据...")

        # Generate sample data
        years = list(range(args.start_year, args.end_year + 1))
        anomalies = [np.random.uniform(-0.5, 0.5) + (y - 1950) * 0.01 for y in years]

        records = [{'year': y, 'temp': a} for y, a in zip(years, anomalies)]
    else:
        # Filter by year range
        berkeley_df = berkeley_df[
            (berkeley_df['year'] >= args.start_year) &
            (berkeley_df['year'] <= args.end_year)
        ]

        # Aggregate by year
        yearly = berkeley_df.groupby('year')['anomaly'].mean().reset_index()
        records = [
            {'year': int(row['year']), 'temp': row['anomaly']}
            for _, row in yearly.iterrows()
        ]

    # Generate chart
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    title = f"{args.region} 温度异常 ({args.start_year}-{args.end_year})"
    success = plot_heat_records(records, title, str(output_path), lang=args.lang)

    if success:
        print(f"\n✅ 温度异常图表已保存: {output_path}")
        return 0
    else:
        return 1


def cmd_compare(args):
    """
    Compare temperature data between two years.
    """
    print("\n" + "="*50)
    print(f"📊 年份对比: {args.year1} vs {args.year2}")
    print("="*50)

    # Load config for API key
    config = load_config()
    if not config:
        print("❌ 未配置 OpenWeatherMap API 密钥")
        return 1

    api_key = config.get('openweather_api_key')
    if not api_key:
        print("❌ API 密钥未设置")
        return 1

    # For comparison, we need historical data
    # OpenWeatherMap free tier doesn't provide historical data easily
    # We'll use ONI data for comparison instead

    oni_df = fetch_oni_data()

    if oni_df.empty:
        print("❌ 无法获取 ONI 数据")
        return 1

    # Filter for both years
    year1_data = oni_df[oni_df['year'] == args.year1]
    year2_data = oni_df[oni_df['year'] == args.year2]

    if year1_data.empty:
        print(f"⚠️  {args.year1} 年数据不可用")
    if year2_data.empty:
        print(f"⚠️  {args.year2} 年数据不可用")

    if year1_data.empty or year2_data.empty:
        print("请确保两个年份都在数据范围内")
        return 1

    # Compare ONI values
    print(f"\n📈 ONI 指数对比")
    print("-" * 40)

    season_order = ['DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ']

    print(f"{'季节':<6} {args.year1:>8} {args.year2:>8} {'差异':>8}")
    print("-" * 40)

    for season in season_order:
        val1 = year1_data[year1_data['season'] == season]['oni_value'].values
        val2 = year2_data[year2_data['season'] == season]['oni_value'].values

        if len(val1) > 0 and len(val2) > 0:
            diff = val2[0] - val1[0]
            print(f"{season:<6} {val1[0]:+8.2f} {val2[0]:+8.2f} {diff:+8.2f}")

    # Phase comparison
    print(f"\n🌊 ENSO 相位对比")
    print("-" * 40)

    avg1 = year1_data['oni_value'].mean()
    avg2 = year2_data['oni_value'].mean()

    phase1 = get_current_enso_phase(avg1)
    phase2 = get_current_enso_phase(avg2)

    print(f"{args.year1} 平均 ONI: {avg1:+.2f}°C - {phase1['phase']}")
    print(f"{args.year2} 平均 ONI: {avg2:+.2f}°C - {phase2['phase']}")

    print("-" * 40 + "\n")

    # Generate comparison chart
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create two datasets
    records1 = [{'year': i, 'temp': row['oni_value']} for i, row in year1_data.iterrows()]
    records2 = [{'year': i, 'temp': row['oni_value']} for i, row in year2_data.iterrows()]

    # For now, use timeline chart
    success = plot_enso_timeline(oni_df[oni_df['year'].isin([args.year1, args.year2])],
                                  str(output_path), lang=args.lang)

    if success:
        print(f"✅ 对比图表已保存: {output_path}")
        return 0
    else:
        return 1


def cmd_timeline(args):
    """
    Generate ENSO timeline chart.
    """
    print("\n" + "="*50)
    print("📊 ENSO 时间线生成")
    print("="*50)

    oni_df = fetch_oni_data()

    if oni_df.empty:
        print("❌ 无法获取 ONI 数据")
        return 1

    # Filter by year range if specified
    if args.start_year:
        oni_df = oni_df[oni_df['year'] >= args.start_year]
    if args.end_year:
        oni_df = oni_df[oni_df['year'] <= args.end_year]

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = plot_enso_timeline(oni_df, str(output_path), lang=args.lang)

    if success:
        print(f"\n✅ ENSO 时间线已保存: {output_path}")
        return 0
    else:
        return 1


def main():
    """Main entry point with argparse CLI."""
    parser = argparse.ArgumentParser(
        description='ENSO Tracker - 追踪全球温度与厄尔尼诺/拉尼娜现象',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s status                     # 显示当前 ENSO 状态
  %(prog)s cities --top 20            # 追踪前 20 个最热城市
  %(prog)s correlate                  # 生成 ENSO 与印度高温相关性图
  %(prog)s anomaly --region Global    # 全球温度异常图
  %(prog)s compare --year1 2023 --year2 2024  # 年份对比
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # status command
    status_parser = subparsers.add_parser('status', help='显示当前 ENSO 状态')

    # cities command
    cities_parser = subparsers.add_parser('cities', help='追踪全球最热城市')
    cities_parser.add_argument('--top', type=int, default=10,
                              help='显示前 N 个最热城市 (默认 10)')
    cities_parser.add_argument('--cities', type=str,
                              help='自定义城市列表，逗号分隔')
    cities_parser.add_argument('--output', type=str, default='~/Downloads/city_ranking.png',
                              help='输出文件路径')
    cities_parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'en'],
                              help='图表语言 (默认 zh)')
    cities_parser.add_argument('--rate-limit', type=float, default=1.0,
                              help='API 请求间隔秒数 (默认 1.0)')

    # correlate command
    correlate_parser = subparsers.add_parser('correlate', help='分析 ENSO 与印度高温相关性')
    correlate_parser.add_argument('--output', type=str, default='~/Downloads/enso_correlation.png',
                                  help='输出文件路径')
    correlate_parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'en'],
                                  help='图表语言 (默认 zh)')

    # anomaly command
    anomaly_parser = subparsers.add_parser('anomaly', help='生成温度异常图表')
    anomaly_parser.add_argument('--region', type=str, default='India',
                               help='区域名称 (默认 India)')
    anomaly_parser.add_argument('--start-year', type=int, default=1950,
                               help='起始年份 (默认 1950)')
    anomaly_parser.add_argument('--end-year', type=int, default=datetime.now().year,
                               help='结束年份 (默认当前年份)')
    anomaly_parser.add_argument('--output', type=str, default='~/Downloads/temperature_anomaly.png',
                               help='输出文件路径')
    anomaly_parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'en'],
                               help='图表语言 (默认 zh)')

    # compare command
    compare_parser = subparsers.add_parser('compare', help='对比两个年份的温度数据')
    compare_parser.add_argument('--year1', type=int, required=True,
                               help='第一个年份')
    compare_parser.add_argument('--year2', type=int, required=True,
                               help='第二个年份')
    compare_parser.add_argument('--output', type=str, default='~/Downloads/year_comparison.png',
                               help='输出文件路径')
    compare_parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'en'],
                               help='图表语言 (默认 zh)')

    # timeline command
    timeline_parser = subparsers.add_parser('timeline', help='生成 ENSO 时间线')
    timeline_parser.add_argument('--start-year', type=int, help='起始年份')
    timeline_parser.add_argument('--end-year', type=int, help='结束年份')
    timeline_parser.add_argument('--output', type=str, default='~/Downloads/enso_timeline.png',
                                 help='输出文件路径')
    timeline_parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'en'],
                                 help='图表语言 (默认 zh)')

    args = parser.parse_args()

    # Route to command handler
    if args.command == 'status':
        return cmd_status(args)
    elif args.command == 'cities':
        return cmd_cities(args)
    elif args.command == 'correlate':
        return cmd_correlate(args)
    elif args.command == 'anomaly':
        return cmd_anomaly(args)
    elif args.command == 'compare':
        return cmd_compare(args)
    elif args.command == 'timeline':
        return cmd_timeline(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())