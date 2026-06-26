#!/usr/bin/env python3
"""
generate_report.py - 生成 A 股市场日报

功能：
1. 调用 fetch_data.py 获取数据（自动 + 手动）
2. 生成 Markdown 报告（人类阅读）
3. 生成 JSON 数据（程序调用）
4. 保存到 output/ 目录和 ~/Desktop/A 股每日复盘/
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# 导入 fetch_data 模块
sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_all_data, PLACEHOLDER, PLACEHOLDER_STR

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "output"
DESKTOP_DIR = Path.home() / "Desktop" / "A 股每日复盘"


def format_point(point: Any) -> str:
    """格式化指数点位"""
    if point is None or point == PLACEHOLDER:
        return PLACEHOLDER_STR
    return f"{point:.2f}"


def format_change(change: Any) -> str:
    """格式化涨跌幅"""
    if change is None or change == PLACEHOLDER:
        return PLACEHOLDER_STR
    
    emoji = "📈" if change > 0 else ("📉" if change < 0 else "➖")
    sign = "+" if change > 0 else ""
    return f"{emoji} {sign}{change:.2f}%"


def format_volume(value: Any) -> str:
    """格式化成交金额"""
    if value is None or value == PLACEHOLDER:
        return PLACEHOLDER_STR
    
    # 假设单位是万亿
    return f"{value}万亿"


def calculate_volume_change(today: Any, previous: Any) -> Dict[str, Any]:
    """计算量能变化"""
    if today is None or today == PLACEHOLDER or previous is None or previous == PLACEHOLDER:
        return {
            'change': PLACEHOLDER,
            'changePercent': PLACEHOLDER,
            'type': PLACEHOLDER_STR,
            'description': PLACEHOLDER_STR,
        }
    
    try:
        today_num = float(today)
        previous_num = float(previous)
        change = today_num - previous_num
        change_percent = (change / previous_num * 100) if previous_num != 0 else 0
        
        if change > 0:
            vol_type = "放量"
            emoji = "🔴"
            desc = "放量上涨" if change_percent > 10 else "温和放量"
        elif change < 0:
            vol_type = "缩量"
            emoji = "🟢"
            desc = "缩量调整" if abs(change_percent) < 10 else "大幅缩量"
        else:
            vol_type = "平量"
            emoji = "➖"
            desc = "成交量持平"
        
        return {
            'change': change,
            'changePercent': round(change_percent, 2),
            'type': vol_type,
            'description': f"{emoji} {desc}",
        }
    except (ValueError, TypeError):
        return {
            'change': PLACEHOLDER,
            'changePercent': PLACEHOLDER,
            'type': PLACEHOLDER_STR,
            'description': PLACEHOLDER_STR,
        }


def generate_markdown(data: Dict[str, Any]) -> str:
    """生成 Markdown 报告"""
    date = data.get('date', 'N/A')
    indices = data.get('indices', {})
    volume = data.get('volume', {})
    sentiment = data.get('sentiment', {})
    
    # 计算量能变化
    volume_change = calculate_volume_change(
        volume.get('today'),
        volume.get('previous')
    )
    
    # 构建报告
    md = f"""# 📊 A 股市场日报 | {date}

> 数据来源：同花顺问财（自动）+ 用户补充（手动） | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 三大指数

| 指数 | 点位 | 涨跌幅 |
|------|------|--------|
| 上证指数 | {format_point(indices.get('shanghai', {}).get('point'))} | {format_change(indices.get('shanghai', {}).get('change'))} |
| 深证成指 | {format_point(indices.get('shenzhen', {}).get('point'))} | {format_change(indices.get('shenzhen', {}).get('change'))} |
| 创业板指 | {format_point(indices.get('chinext', {}).get('point'))} | {format_change(indices.get('chinext', {}).get('change'))} |

---

## 成交量

- **今日量能**：{format_volume(volume.get('today'))}
- **量能变化**：{volume_change['type']} {format_volume(abs(volume_change['change']) if volume_change['change'] != PLACEHOLDER else 0)} ({volume_change['changePercent'] if volume_change['changePercent'] != PLACEHOLDER else PLACEHOLDER_STR}%)

> 💡 **提示**：成交量数据需要手动补充。编辑 `manual/{date}.json` 或运行：
> ```bash
> python3 scripts/补数据.py {date} --today 1.23 --previous 1.30
> ```

---

## 涨跌家数

- **上涨**：{sentiment.get('up', PLACEHOLDER_STR)} 家
- **下跌**：{sentiment.get('down', PLACEHOLDER_STR)} 家
- **涨跌比**：≈ {sentiment.get('ratio', PLACEHOLDER_STR)}
- **市场情绪**：{sentiment.get('description', PLACEHOLDER_STR)}

---

## 数据说明

- **缓存状态**：{"✅ 使用缓存" if data.get('_from_cache') else "🔄 实时获取"}
- **数据源**：{data.get('dataSource', 'N/A')}
- **查询日期**：{data.get('query_date', date)}
- **手动补充**：{len(data.get('manualDataRequired', []))} 项待补充
"""
    
    return md


def generate_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """生成 JSON 数据（优化格式）"""
    volume = data.get('volume', {})
    volume_change = calculate_volume_change(
        volume.get('today'),
        volume.get('previous'),
    )
    
    return {
        'date': data.get('date'),
        'query_date': data.get('query_date'),
        'indices': {
            'shanghai': {
                'point': data.get('indices', {}).get('shanghai', {}).get('point'),
                'change': data.get('indices', {}).get('shanghai', {}).get('change'),
            },
            'shenzhen': {
                'point': data.get('indices', {}).get('shenzhen', {}).get('point'),
                'change': data.get('indices', {}).get('shenzhen', {}).get('change'),
            },
            'chinext': {
                'point': data.get('indices', {}).get('chinext', {}).get('point'),
                'change': data.get('indices', {}).get('chinext', {}).get('change'),
            },
        },
        'volume': {
            'today': volume.get('today'),
            'previous': volume.get('previous'),
            'change': volume_change['change'],
            'changePercent': volume_change['changePercent'],
            'type': volume_change['type'],
        },
        'sentiment': {
            'up': data.get('sentiment', {}).get('up'),
            'down': data.get('sentiment', {}).get('down'),
            'ratio': data.get('sentiment', {}).get('ratio'),
            'description': data.get('sentiment', {}).get('description'),
        },
        'meta': {
            'cached': data.get('_from_cache', False),
            'dataSource': data.get('dataSource'),
            'generatedAt': datetime.now().isoformat(),
            'manualDataRequired': data.get('manualDataRequired', []),
        },
    }


def save_reports(data: Dict[str, Any]) -> tuple:
    """保存报告到多个位置"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DESKTOP_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成报告
    md_content = generate_markdown(data)
    json_content = generate_json(data)
    
    # 保存路径
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    md_filename = f"stock-report-{date}.md"
    json_filename = f"data-{date}.json"
    
    # 保存到 output 目录
    output_md_path = OUTPUT_DIR / md_filename
    output_json_path = OUTPUT_DIR / json_filename
    
    output_md_path.write_text(md_content, encoding='utf-8')
    output_json_path.write_text(json.dumps(json_content, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # 保存到 Desktop
    desktop_md_path = DESKTOP_DIR / md_filename
    desktop_json_path = DESKTOP_DIR / json_filename
    
    desktop_md_path.write_text(md_content, encoding='utf-8')
    desktop_json_path.write_text(json.dumps(json_content, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return (output_md_path, output_json_path), (desktop_md_path, desktop_json_path)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='生成 A 股市场日报')
    parser.add_argument('date', nargs='?', default=None, help='日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('--force', action='store_true', help='强制刷新，忽略缓存')
    parser.add_argument('--json', action='store_true', help='仅输出 JSON')
    parser.add_argument('--markdown', action='store_true', help='仅输出 Markdown')
    
    args = parser.parse_args()
    
    # 确定日期
    if args.date:
        date = args.date
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"[INFO] 生成报告：{date}")
    
    # 获取数据
    data = fetch_all_data(date, force_refresh=args.force)
    
    # 输出模式
    if args.json:
        json_content = generate_json(data)
        print(json.dumps(json_content, ensure_ascii=False, indent=2))
    elif args.markdown:
        md_content = generate_markdown(data)
        print(md_content)
    else:
        # 保存报告
        (out_md, out_json), (desk_md, desk_json) = save_reports(data)
        
        print(f"\n✅ 报告生成完成！")
        print(f"\n📁 Workspace 输出:")
        print(f"   Markdown: {out_md}")
        print(f"   JSON: {out_json}")
        print(f"\n📁 Desktop 输出:")
        print(f"   Markdown: {desk_md}")
        print(f"   JSON: {desk_json}")
        print(f"\n💡 提示：补充成交量数据后重新运行即可更新报告")


if __name__ == '__main__':
    main()
