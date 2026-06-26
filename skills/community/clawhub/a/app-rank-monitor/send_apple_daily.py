#!/usr/bin/env python3
"""
发送苹果榜单日报
"""

import asyncio
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from datetime import date, timedelta
from pathlib import Path
from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import Session

from models.apple_rank import AppleChartRecord, AppleOfflineAlert
from notifiers.dingtalk import DingTalkNotifier
from utils.logger import setup_logger

logger = setup_logger()


async def send_apple_daily_report(report_date: date = None):
    """发送苹果榜单日报到钉钉"""
    if report_date is None:
        report_date = date.today()
    
    db_path = Path(__file__).parent / "database" / "apps.db"
    engine = create_engine(f"sqlite:///{db_path}")
    notifier = DingTalkNotifier()
    
    with Session(engine) as session:
        # 统计今日数据
        today_count = session.query(func.count(AppleChartRecord.id)).filter(
            AppleChartRecord.record_date == report_date
        ).scalar()
        
        # 统计昨日数据
        yesterday = report_date - timedelta(days=1)
        yesterday_count = session.query(func.count(AppleChartRecord.id)).filter(
            AppleChartRecord.record_date == yesterday
        ).scalar()
        
        # 统计今日下架
        offline_count = session.query(func.count(AppleOfflineAlert.id)).filter(
            AppleOfflineAlert.offline_date == report_date
        ).scalar()
        
        # 获取 TOP 榜单（总榜前 10）
        top_free = session.query(AppleChartRecord).filter(
            and_(
                AppleChartRecord.record_date == report_date,
                AppleChartRecord.chart_type == "top_free",
                AppleChartRecord.genre == 0
            )
        ).order_by(AppleChartRecord.rank).limit(10).all()
        
        top_paid = session.query(AppleChartRecord).filter(
            and_(
                AppleChartRecord.record_date == report_date,
                AppleChartRecord.chart_type == "top_paid",
                AppleChartRecord.genre == 0
            )
        ).order_by(AppleChartRecord.rank).limit(10).all()
        
        new_free = session.query(AppleChartRecord).filter(
            and_(
                AppleChartRecord.record_date == report_date,
                AppleChartRecord.chart_type == "new_free",
                AppleChartRecord.genre == 0
            )
        ).order_by(AppleChartRecord.rank).limit(10).all()
    
    if today_count == 0:
        logger.warning(f"今日无苹果榜单数据：{report_date}")
        return False
    
    # 构建 Markdown 消息
    markdown_text = f"""## 🍎 iOS 榜单日报 ({report_date.strftime('%Y-%m-%d')})

### 📊 数据概览
- 今日收录：**{today_count:,}** 条记录
- 昨日收录：**{yesterday_count:,}** 条记录
- 下架告警：**{offline_count}** 个应用

### 🔥 免费榜 TOP 10
"""
    
    for i, app in enumerate(top_free, 1):
        markdown_text += f"{i}. **{app.app_name}** ({app.developer})\n"
    
    markdown_text += "\n### 💰 付费榜 TOP 10\n"
    
    for i, app in enumerate(top_paid, 1):
        markdown_text += f"{i}. **{app.app_name}** ({app.developer})\n"
    
    markdown_text += "\n### 🆕 新上架 TOP 10\n"
    
    for i, app in enumerate(new_free, 1):
        markdown_text += f"{i}. **{app.app_name}** ({app.developer})\n"
    
    if offline_count > 0:
        markdown_text += f"\n### ⚠️ 下架应用\n共 {offline_count} 个，请查看附件详情\n"
    
    content = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"🍎 iOS 榜单日报 {report_date.strftime('%Y-%m-%d')}",
            "text": markdown_text
        }
    }
    
    await notifier._send(content)
    logger.info(f"✅ 苹果榜单日报已发送：{report_date}")
    return True


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    result = asyncio.run(send_apple_daily_report())
    print(f"发送结果：{'成功' if result else '失败'}")
