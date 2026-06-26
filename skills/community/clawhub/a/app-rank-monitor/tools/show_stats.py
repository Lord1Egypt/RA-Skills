#!/usr/bin/env python3
"""显示苹果榜单数据统计"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from monitor import AppMonitor
from sqlalchemy.orm import Session
from models.apple_rank import AppleChartRecord, AppleOfflineAlert
from sqlalchemy import func
from datetime import date, timedelta

monitor = AppMonitor()

with Session(monitor.engine) as session:
    # 总记录数
    total = session.query(AppleChartRecord).count()
    
    # 今日记录
    today = session.query(AppleChartRecord).filter(
        AppleChartRecord.record_date == date.today()
    ).count()
    
    # 昨日记录
    yesterday = date.today() - timedelta(days=1)
    yesterday_count = session.query(AppleChartRecord).filter(
        AppleChartRecord.record_date == yesterday
    ).count()
    
    # 日期范围
    oldest = session.query(func.min(AppleChartRecord.record_date)).scalar()
    newest = session.query(func.max(AppleChartRecord.record_date)).scalar()
    
    # 各分类统计
    category_stats = session.query(
        AppleChartRecord.genre,
        AppleChartRecord.category,
        func.count(AppleChartRecord.id)
    ).filter(
        AppleChartRecord.record_date == date.today()
    ).group_by(
        AppleChartRecord.genre,
        AppleChartRecord.category
    ).order_by(
        func.count(AppleChartRecord.id).desc()
    ).all()
    
    # 下架告警
    total_alerts = session.query(AppleOfflineAlert).count()
    pending_alerts = session.query(AppleOfflineAlert).filter(
        AppleOfflineAlert.notified == False
    ).count()
    today_alerts = session.query(AppleOfflineAlert).filter(
        AppleOfflineAlert.offline_date == date.today()
    ).count()
    
    # 数据库大小
    import os
    db_path = monitor.db_path
    db_size = os.path.getsize(db_path) / 1024 / 1024 if os.path.exists(db_path) else 0
    
    print("\n📊 苹果榜单数据统计")
    print("=" * 60)
    print(f"总记录数：       {total:,}")
    print(f"今日记录：       {today:,}")
    print(f"昨日记录：       {yesterday_count:,}")
    print(f"最早日期：       {oldest or '无'}")
    print(f"最新日期：       {newest or '无'}")
    print()
    print(f"下架告警：       {total_alerts} (未通知：{pending_alerts}, 今日：{today_alerts})")
    print()
    print(f"数据库大小：     {db_size:.2f} MB")
    print("=" * 60)
    
    if category_stats:
        print(f"\n📋 今日各分类应用数 (Top 10)")
        print("-" * 60)
        for genre, category, count in category_stats[:10]:
            print(f"  {category:25} (ID:{genre:5}): {count:4} 个应用")
        print()
