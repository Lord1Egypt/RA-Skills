#!/usr/bin/env python3
"""
补数据.py - 手动补充成交量数据

用法：
    python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30
    python3 scripts/补数据.py 2026-03-22 -t 1.23 -p 1.30
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 导入 fetch_data 模块
sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import get_manual_path, load_manual_data, save_manual_data


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='手动补充成交量数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/补数据.py 2026-03-22 --today 1.23 --previous 1.30
  python3 scripts/补数据.py 2026-03-22 -t 1.23 -p 1.30
  python3 scripts/补数据.py 2026-03-22 --clear  # 清除手动数据

参数说明:
  --today, -t     今日成交量（单位：万亿）
  --previous, -p  昨日成交量（单位：万亿）
        """
    )
    
    parser.add_argument('date', nargs='?', default=None, help='日期 (YYYY-MM-DD)，默认今天')
    parser.add_argument('--today', '-t', type=float, help='今日成交量（万亿）')
    parser.add_argument('--previous', '-p', type=float, help='昨日成交量（万亿）')
    parser.add_argument('--clear', action='store_true', help='清除手动数据')
    parser.add_argument('--show', action='store_true', help='显示当前手动数据')
    
    args = parser.parse_args()
    
    # 确定日期
    if args.date:
        date = args.date
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    manual_path = get_manual_path(date)
    
    # 清除手动数据
    if args.clear:
        if manual_path.exists():
            manual_path.unlink()
            print(f"✅ 已清除手动数据：{manual_path}")
        else:
            print(f"ℹ️  没有手动数据可清除")
        return
    
    # 显示当前手动数据
    if args.show:
        data = load_manual_data(date)
        if data:
            print(f"📊 {date} 的手动数据:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"ℹ️  {date} 没有手动数据")
        return
    
    # 检查是否提供了数据
    if args.today is None and args.previous is None:
        # 没有提供数据，显示当前状态
        data = load_manual_data(date)
        if data:
            print(f"📊 {date} 的当前手动数据:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"ℹ️  {date} 没有手动数据")
        print(f"\n💡 使用 --today 和 --previous 参数补充数据")
        print(f"   示例：python3 scripts/补数据.py {date} --today 1.23 --previous 1.30")
        return
    
    # 加载现有数据
    existing_data = load_manual_data(date)
    
    # 更新数据
    if 'volume' not in existing_data:
        existing_data['volume'] = {}
    
    if args.today is not None:
        existing_data['volume']['today'] = args.today
        print(f"✅ 今日成交量：{args.today}万亿")
    
    if args.previous is not None:
        existing_data['volume']['previous'] = args.previous
        print(f"✅ 昨日成交量：{args.previous}万亿")
    
    # 保存数据
    save_manual_data(date, existing_data)
    
    # 提示重新生成报告
    print(f"\n💡 提示：重新生成报告以应用更新")
    print(f"   python3 scripts/generate_report.py {date}")


if __name__ == '__main__':
    main()
