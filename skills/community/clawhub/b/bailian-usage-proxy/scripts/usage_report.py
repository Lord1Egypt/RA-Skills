#!/usr/bin/env python3
"""
用量报表脚本
"""

import asyncio
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import db


async def generate_report(user_id: str = None, start_date: str = None, end_date: str = None, export: str = None):
    """生成用量报表"""
    await db.init()
    
    # 默认时间范围
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    logs = await db.query_usage_logs(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=10000
    )
    
    # 统计
    total_requests = len(logs)
    total_input = sum(log.input_tokens for log in logs)
    total_output = sum(log.output_tokens for log in logs)
    total_tokens = sum(log.total_tokens for log in logs)
    
    print(f"\n{'='*60}")
    print(f"用量报表: {start_date} 至 {end_date}")
    print(f"{'='*60}")
    print(f"总请求数: {total_requests}")
    print(f"输入Token: {total_input:,}")
    print(f"输出Token: {total_output:,}")
    print(f"总Token:   {total_tokens:,}")
    print(f"{'='*60}\n")
    
    # 按模型分组
    model_stats = {}
    for log in logs:
        model = log.model
        if model not in model_stats:
            model_stats[model] = {"requests": 0, "tokens": 0}
        model_stats[model]["requests"] += 1
        model_stats[model]["tokens"] += log.total_tokens
    
    print("模型分布:")
    for model, stats in sorted(model_stats.items(), key=lambda x: -x[1]["tokens"]):
        print(f"  {model:30} | {stats['requests']:5}次 | {stats['tokens']:10,} tokens")
    
    print()
    
    # 导出CSV
    if export:
        import csv
        with open(export, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['日期', '用户ID', '模型', '输入Token', '输出Token', '总Token', '响应时间(ms)'])
            for log in logs:
                writer.writerow([
                    log.request_date,
                    log.user_id,
                    log.model,
                    log.input_tokens,
                    log.output_tokens,
                    log.total_tokens,
                    log.response_time_ms
                ])
        print(f"报表已导出: {export}")


def main():
    parser = argparse.ArgumentParser(description="生成用量报表")
    parser.add_argument("--user-id", help="指定用户ID")
    parser.add_argument("--start-date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--today", action="store_true", help="今日报表")
    parser.add_argument("--export", help="导出CSV文件路径")
    
    args = parser.parse_args()
    
    if args.today:
        args.end_date = datetime.now().strftime("%Y-%m-%d")
        args.start_date = args.end_date
    
    asyncio.run(generate_report(
        user_id=args.user_id,
        start_date=args.start_date,
        end_date=args.end_date,
        export=args.export
    ))


if __name__ == "__main__":
    main()
