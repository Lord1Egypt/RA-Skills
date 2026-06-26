#!/usr/bin/env python3
"""
清理过期的苹果榜单数据
默认保留 7 天数据
"""

import sys
import asyncio
from pathlib import Path

# 添加 src 到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from monitor import AppMonitor


async def cleanup(retention_days: int = 7, dry_run: bool = False):
    """
    清理过期数据
    
    Args:
        retention_days: 保留天数（默认 7 天）
        dry_run: 只显示不删除（默认 False）
    """
    monitor = AppMonitor()
    
    print(f"\n🧹 开始清理过期数据...")
    print(f"   保留策略：{retention_days} 天")
    print(f"   模式：{'预览' if dry_run else '执行'}\n")
    
    if dry_run:
        # 预览模式
        from sqlalchemy.orm import Session
        from models.apple_rank import AppleChartRecord, AppleOfflineAlert
        from datetime import date, timedelta
        
        cutoff_date = date.today() - timedelta(days=retention_days)
        
        with Session(monitor.engine) as session:
            # 统计要删除的数据
            old_records = session.query(AppleChartRecord).filter(
                AppleChartRecord.record_date < cutoff_date
            ).count()
            
            old_alerts = session.query(AppleOfflineAlert).filter(
                AppleOfflineAlert.offline_date < cutoff_date,
                AppleOfflineAlert.notified == True
            ).count()
            
            print(f"📊 预览结果:")
            print(f"   将删除榜单记录：{old_records} 条")
            print(f"   将删除下架告警：{old_alerts} 条")
            print(f"\n💡 提示：使用 --execute 参数执行实际删除")
    else:
        # 执行清理
        await monitor._cleanup_old_apple_data(retention_days)
        print(f"\n✅ 清理完成!\n")
    
    # 显示当前数据量
    from sqlalchemy.orm import Session
    from models.apple_rank import AppleChartRecord, AppleOfflineAlert
    from sqlalchemy import func
    
    with Session(monitor.engine) as session:
        current_records = session.query(AppleChartRecord).count()
        current_alerts = session.query(AppleOfflineAlert).count()
        
        # 查询数据库文件大小
        import os
        db_path = monitor.db_path
        db_size = os.path.getsize(db_path) / 1024 / 1024 if os.path.exists(db_path) else 0
        
        print(f"📊 当前数据库状态:")
        print(f"   榜单记录：{current_records} 条")
        print(f"   下架告警：{current_alerts} 条")
        print(f"   数据库大小：{db_size:.2f} MB")
        print()


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="清理过期的苹果榜单数据")
    parser.add_argument("--retention-days", type=int, default=7, help="保留天数（默认 7 天）")
    parser.add_argument("--dry-run", action="store_true", help="预览模式（只统计不删除）")
    parser.add_argument("--execute", action="store_true", help="执行清理（默认模式）")
    
    args = parser.parse_args()
    
    if args.dry_run:
        await cleanup(retention_days=args.retention_days, dry_run=True)
    else:
        await cleanup(retention_days=args.retention_days, dry_run=False)


if __name__ == "__main__":
    asyncio.run(main())
