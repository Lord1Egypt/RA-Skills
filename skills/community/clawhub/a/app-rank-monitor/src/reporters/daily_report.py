"""
日报生成器
"""

from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session
from pathlib import Path

from models.app import AppRecord
from notifiers.dingtalk import DingTalkNotifier
from utils.logger import setup_logger

logger = setup_logger()


class DailyReporter:
    """日报生成器"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "database" / "apps.db"
        
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.notifier = DingTalkNotifier()
    
    def generate_report(self, report_date: date = None) -> dict:
        """生成日报数据"""
        if report_date is None:
            report_date = date.today()
        
        with Session(self.engine) as session:
            # 苹果榜单数据
            apple_records = session.query(AppRecord).filter(
                and_(AppRecord.record_date == report_date)
            ).all()
            
            # 按榜单类型分组
            apple_data = {}
            for record in apple_records:
                key = f"{record.chart_type}_g{record.genre}"
                if key not in apple_data:
                    apple_data[key] = []
                apple_data[key].append(record)
            
            # 新上架应用（首次发现）
            new_apps = [r for r in apple_records if r.is_new]
            
            return {
                "report_date": report_date,
                "apple": {
                    "total": len(apple_records),
                    "charts": apple_data,
                    "new_apps": new_apps,
                },
            }
    
    def save_rank_data(self, platform: str, data: Any):
        """保存榜单数据到数据库（由 monitor 调用）"""
        # 数据已由 monitor 保存，这里只负责生成报告
        pass
    
    async def send_daily_report(self, report_date: date = None):
        """发送日报到钉钉"""
        if report_date is None:
            report_date = date.today()
        
        logger.info(f"📊 生成日报 ({report_date.isoformat()})...")
        
        try:
            report_data = self.generate_report(report_date)
            
            # 生成 Markdown 报告
            markdown = self._generate_markdown(report_data)
            
            # 保存到文件
            report_path = self._save_report(markdown, report_date)
            
            # 发送钉钉消息
            await self._send_report(markdown, report_path)
            
            logger.info("✅ 日报发送完成")
            
        except Exception as e:
            logger.error(f"❌ 日报发送失败：{e}")
            raise
    
    def _generate_markdown(self, report_data: dict) -> str:
        """生成 Markdown 格式的日报"""
        lines = []
        report_date = report_data["report_date"]
        
        lines.append(f"# 📊 应用榜单日报 ({report_date.isoformat()})")
        lines.append("")
        
        # 苹果榜单
        apple = report_data["apple"]
        lines.append("## 🍎 苹果榜单")
        lines.append(f"- 总计：**{apple['total']}** 条记录")
        lines.append(f"- 新上架：**{len(apple['new_apps'])}** 个")
        lines.append("")
        
        # 新上架应用 TOP 20
        if apple["new_apps"]:
            lines.append("### 🆕 新上架应用 TOP 20")
            lines.append("")
            lines.append("| 排名 | 应用名称 | 开发者 | 分类 |")
            lines.append("|------|----------|--------|------|")
            
            for i, app in enumerate(apple["new_apps"][:20], 1):
                lines.append(f"| {i} | {app.app_name} | {app.developer or 'N/A'} | {app.category or 'N/A'} |")
            
            lines.append("")
        
        # 榜单详情
        lines.append("### 📈 榜单分类")
        lines.append("")
        for chart_key, records in apple["charts"].items():
            lines.append(f"- **{chart_key}**: {len(records)} 个应用")
        
        lines.append("")
        lines.append("---")
        lines.append(f"_报告生成时间：{datetime.now().isoformat()}_")
        
        return "\n".join(lines)
    
    def _save_report(self, markdown: str, report_date: date) -> Path:
        """保存报告到文件"""
        reports_dir = Path(__file__).parent.parent.parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        filename = f"daily_report_{report_date.strftime('%Y%m%d')}.md"
        report_path = reports_dir / filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        logger.info(f"📄 报告已保存：{report_path}")
        return report_path
    
    async def _send_report(self, markdown: str, report_path: Path):
        """发送报告到钉钉"""
        # 发送文本消息（前 20 行摘要）
        summary_lines = markdown.split("\n")[:20]
        summary = "\n".join(summary_lines) + "\n\n... 完整报告请查看附件"
        
        await self.notifier.send_text_message(summary)
        
        # 上传文件
        await self.notifier.send_file(str(report_path), title="点点数据日报")
