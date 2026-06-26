"""
监控调度器 - 榜单监控核心逻辑

功能：爬取应用榜单数据
"""

import asyncio
from datetime import datetime, date
from typing import List, Dict, Optional
from sqlalchemy import create_engine
from pathlib import Path

from notifiers.dingtalk import DingTalkNotifier
from rankers.diandian import DiandianRanker
from rankers.apple_ranker import AppleRanker
from reporters.daily_report import DailyReporter
from utils.logger import setup_logger

logger = setup_logger()


class AppMonitor:
    """应用榜单监控器"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "database" / "apps.db"
        
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        
        # 创建所有表
        from models.app import Base as AppBase
        AppBase.metadata.create_all(self.engine)
        
        self.notifier = DingTalkNotifier()
        
        # 榜单爬虫
        # 使用浏览器版本（API 已失效）
        from rankers.diandian_android_web_final import DiandianAndroidWebRankerFinal
        self.rankers = {
            "diandian": DiandianRanker(),
            "diandian_android": DiandianAndroidWebRankerFinal(),  # 安卓渠道（浏览器版本）
            "apple": AppleRanker(),
        }
        
        # 安卓渠道爬虫由 DiandianAndroidWebRankerFinal 统一处理
        
        # 日报生成器
        self.reporter = DailyReporter()
    
    async def fetch_all_ranks(self, platform: str = "all", android_channels: list = None):
        """
        爬取所有榜单数据
        
        Args:
            platform: 指定平台 (all/diandian/diandian_android/apple)
            android_channels: 安卓渠道列表 (None 表示所有渠道)
        """
        logger.info(f"开始爬取榜单数据... (platform={platform})")
        
        if platform == "all":
            # 爬取点点 iOS
            for platform_name, ranker in self.rankers.items():
                if platform_name in ["apple", "diandian_android"]:
                    continue  # 苹果和安卓单独处理
                
                try:
                    data = await ranker.fetch_all()
                    self.reporter.save_rank_data(platform_name, data)
                    logger.info(f"{platform_name} 榜单爬取完成")
                except Exception as e:
                    logger.error(f"{platform_name} 榜单爬取失败：{e}")
            
            # 爬取点点安卓各渠道
            await self.fetch_diandian_android_all_channels(android_channels)
            
            # 爬取苹果榜单
            try:
                await self._fetch_apple_charts()
            except Exception as e:
                logger.error(f"苹果榜单爬取失败：{e}")
        
        elif platform == "diandian_android":
            # 只爬取安卓渠道
            await self.fetch_diandian_android_all_channels(android_channels)
        
        elif platform in self.rankers:
            # 爬取指定平台
            try:
                ranker = self.rankers[platform]
                data = await ranker.fetch_all()
                self.reporter.save_rank_data(platform, data)
                logger.info(f"{platform} 榜单爬取完成")
            except Exception as e:
                logger.error(f"{platform} 榜单爬取失败：{e}")
        else:
            logger.error(f"不支持的平台：{platform}")
        
        logger.info("榜单爬取完成")
    
    async def fetch_diandian_android_all_channels(self, channels: list = None):
        """
        爬取点点数据安卓所有渠道
        
        Args:
            channels: 渠道列表 (None 表示所有渠道)
        """
        from pathlib import Path
        import yaml
        
        # 加载配置
        config_path = Path(__file__).parent.parent / "config" / "diandian.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}
        
        # 获取启用的渠道
        if channels is None:
            channels_config = config.get('android_channels', {})
            channels = [ch for ch, cfg in channels_config.items() if cfg.get('enabled', True)]
        
        logger.info(f"开始爬取点点安卓渠道：{channels}")
        
        ranker = self.rankers["diandian_android"]
        all_data = {}
        
        for channel in channels:
            try:
                # 获取渠道数据（包含新上架和下架）
                result = await ranker.fetch_all_for_channel(channel, limit=100)
                
                all_data[channel] = {
                    "channel": channel,
                    "channel_name": ranker.CHANNELS.get(channel, {}).get('name', channel),
                    "new_apps": result.get("new_apps", []),
                    "offline_apps": result.get("offline_apps", []),
                    "fetch_time": datetime.now().isoformat(),
                }
                
                new_count = len(result.get("new_apps", []))
                offline_count = len(result.get("offline_apps", []))
                logger.info(f"✅ {channel} 爬取完成：新上架 {new_count} 个，下架 {offline_count} 个")
            except Exception as e:
                logger.error(f"❌ {channel} 爬取失败：{e}")
                import traceback
                traceback.print_exc()
        
        # 保存数据
        if all_data:
            self.reporter.save_rank_data("diandian_android", all_data)
            logger.info(f"✅ 安卓渠道数据已保存 ({len(all_data)} 个渠道)")
    
    async def send_daily_report(self):
        """发送日报"""
        await self.reporter.send_daily_report(date.today())
    
    async def _fetch_apple_charts(self, fetch_all: bool = True, retention_days: int = 7):
        """
        爬取苹果榜单
        
        Args:
            fetch_all: 是否爬取所有分类（默认 True，获取全量数据）
            retention_days: 数据保留天数（默认 7 天）
        """
        logger.info("🍎 开始爬取苹果榜单..." + ("（全量模式）" if fetch_all else "（仅总榜）"))
        apple_ranker = AppleRanker(limit=200, fetch_all_categories=fetch_all)
        
        try:
            # 获取今日日期
            today = date.today()
            today_str = today.isoformat()
            
            # 爬取所有榜单
            all_charts = await apple_ranker.fetch_all_charts()
            all_current_apps = {}  # {app_id: app_data}
            
            # 合并所有榜单数据
            for chart_key, apps in all_charts.items():
                logger.info(f"获取到 {chart_key}: {len(apps)} 个应用")
                
                # 保存到数据库
                from models.app import AppRecord
                from sqlalchemy.orm import Session
                from sqlalchemy import and_
                
                with Session(self.engine) as session:
                    for app_data in apps:
                        app_id = app_data["app_id"]
                        all_current_apps[app_id] = app_data
                        
                        # 解析 chart_key 获取榜单类型和分类
                        parts = chart_key.split("_g")
                        chart_type = parts[0] if len(parts) > 0 else "top_free"
                        genre = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                        
                        # 查询是否已存在
                        existing = session.query(AppRecord).filter(
                            and_(
                                AppRecord.app_id == app_id,
                                AppRecord.record_date == today,
                                AppRecord.chart_type == chart_type,
                                AppRecord.genre == genre
                            )
                        ).first()
                        
                        if existing:
                            # 更新现有记录
                            existing.rank = app_data["rank"]
                            existing.last_seen = today_str
                            existing.updated_at = datetime.now().isoformat()
                        else:
                            # 创建新记录
                            record = AppRecord(
                                record_date=today,
                                app_id=app_id,
                                bundle_id=app_data.get("bundle_id", ""),
                                app_name=app_data["name"],
                                developer=app_data.get("developer", ""),
                                chart_type=chart_type,
                                genre=genre,
                                rank=app_data["rank"],
                                category=app_data.get("category", ""),
                                price=str(app_data.get("price", "0")),
                                icon_url=app_data.get("icon", ""),
                                is_new=True,
                                first_seen=today_str,
                                last_seen=today_str,
                            )
                            session.add(record)
                    
                    session.commit()
            
            logger.info(f"🍎 苹果榜单爬取完成，记录 {len(all_current_apps)} 个应用")
            
        finally:
            await apple_ranker.close()
        
        # 清理过期数据（保留 retention_days 天）
        await self._cleanup_old_apple_data(retention_days)
    
    async def _cleanup_old_apple_data(self, retention_days: int = 7):
        """
        清理过期的苹果榜单数据
        
        Args:
            retention_days: 保留天数（默认 7 天）
        """
        from datetime import timedelta
        from models.app import AppRecord
        from sqlalchemy import delete
        from sqlalchemy.orm import Session
        
        cutoff_date = date.today() - timedelta(days=retention_days)
        
        with Session(self.engine) as session:
            # 删除过期的榜单记录
            result = session.execute(
                delete(AppRecord).where(
                    AppRecord.record_date < cutoff_date
                )
            )
            deleted_count = result.rowcount
            
            session.commit()
            
            if deleted_count > 0:
                logger.info(f"🧹 清理完成：删除 {deleted_count} 条榜单记录（保留{retention_days}天）")
            else:
                logger.debug(f"✅ 无需清理（保留{retention_days}天数据）")
