"""
通用每日早报生成核心逻辑
负责：搜索新闻、筛选、格式编排
支持任意领域配置
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class NewsItem:
    """单条新闻"""
    
    def __init__(self, title: str, content: str, source: str, 
                 link: str = None, publish_time: datetime = None, category: str = None):
        self.title = title
        self.content = content
        self.source = source
        self.link = link
        self.publish_time = publish_time
        self.category = category
        
    def is_within_hours(self, hours: int = 24) -> bool:
        """检查是否在指定小时内"""
        if not self.publish_time:
            return True  # 如果没有时间，默认通过
        
        now = datetime.now()
        delta = now - self.publish_time
        return delta <= timedelta(hours=hours)
    
    def get_age_label(self) -> str:
        """获取时效标签"""
        if self.is_within_hours(24):
            return ""
        elif self.is_within_hours(48):
            return "[昨日资讯] "
        else:
            return "[过期] "


class NewsGenerator:
    """通用新闻生成器"""
    
    def __init__(self, config: dict):
        """
        初始化生成器
        
        Args:
            config: 配置对象，包含：
                - NEWS_DOMAIN: 关注领域
                - DOMAIN_NAME: 领域显示名称
                - MAX_NEWS_PER_CATEGORY: 各分类最大条数
                - CATEGORY_NAMES: 分类名称映射
                - SOURCE_PRIORITY: 信息源优先级列表
                - PREFER_PRIORITY_SOURCES: 是否优先保留指定来源
        """
        self.config = config
        self.domain = config.get('NEWS_DOMAIN', 'AI人工智能')
        self.domain_name = config.get('DOMAIN_NAME', 'AI')
        self.category_names = config.get('CATEGORY_NAMES', {
            "headline": "头条",
            "international": "国际动态",
            "domestic": "国内动态",
            "academic": "深度/学术",
            "observation": "今日观察"
        })
        self.source_priority = config.get('SOURCE_PRIORITY', [])
        self.prefer_priority_sources = config.get('PREFER_PRIORITY_SOURCES', True)
    
    def get_source_priority(self) -> list:
        """
        获取信息源优先级列表
        如果用户配置了，就用用户配置的
        如果用户没配置（空列表），就让AI自动根据领域分析判断
        """
        if self.source_priority and len(self.source_priority) > 0:
            return self.source_priority
        else:
            # 返回空列表，表示让AI自动推断
            return []
    
    def should_auto_infer_sources(self) -> bool:
        """是否需要AI自动推断信息源"""
        return self.source_priority is None or len(self.source_priority) == 0
        
        self.headline = None  # 头条
        self.international = []  # 国际动态
        self.domestic = []  # 国内动态
        self.academic = []  # 深度/学术
        self.observation = ""  # 今日观察
        
    def add_news(self, news: NewsItem):
        """添加新闻到对应分类"""
        if news.category == "headline":
            self.headline = news
        elif news.category == "international":
            self.international.append(news)
        elif news.category == "domestic":
            self.domestic.append(news)
        elif news.category == "academic":
            self.academic.append(news)
    
    def set_observation(self, observation: str):
        """设置今日观察"""
        self.observation = observation
    
    def filter_by_age(self):
        """按时间筛选，移除超过48小时的内容"""
        self.international = [n for n in self.international if n.is_within_hours(48)]
        self.domestic = [n for n in self.domestic if n.is_within_hours(48)]
        self.academic = [n for n in self.academic if n.is_within_hours(48)]
        
        # 限制每条分类的数量
        max_config = self.config.get('MAX_NEWS_PER_CATEGORY', {})
        max_intl = max_config.get('international', 3)
        max_dom = max_config.get('domestic', 3)
        max_aca = max_config.get('academic', 2)
        
        self.international = self.international[:max_intl]
        self.domestic = self.domestic[:max_dom]
        self.academic = self.academic[:max_aca]
    
    def format_news_item(self, news: NewsItem, is_headline: bool = False) -> str:
        """格式化单条新闻"""
        age_label = news.get_age_label()
        title = age_label + news.title
        
        if is_headline:
            # 头条格式
            time_str = news.publish_time.strftime("%Y-%m-%d %H:%M") if news.publish_time else ""
            lines = [
                f"{title} | {time_str}",
                news.content,
            ]
            if news.source:
                source_line = f"来源：{news.source}"
                if news.link:
                    source_line += f" | {news.link}"
                lines.append(source_line)
            return "\n".join(lines)
        else:
            # 列表项格式
            line = f"- {title}：{news.content}"
            if news.source:
                line += f" 来源：{news.source}"
                if news.link:
                    line += f" | {news.link}"
            return line
    
    def generate(self) -> str:
        """生成完整早报文本"""
        self.filter_by_age()
        today = datetime.now().strftime("%Y.%m.%d")
        
        parts = [
            f"📰 {self.domain_name}早报 | {today}",
            f"过去24小时{self.domain}最新动态",
            "",
            f"🔝 {self.category_names['headline']}",
        ]
        
        if self.headline:
            parts.append(self.format_news_item(self.headline, is_headline=True))
        else:
            parts.append("（今日无重大头条）")
        
        parts.extend([
            "",
            f"🏢 {self.category_names['international']}",
        ])
        if self.international:
            for news in self.international:
                parts.append(self.format_news_item(news))
        else:
            parts.append("（今日无国际动态）")
        
        parts.extend([
            "",
            f"🇨🇳 {self.category_names['domestic']}",
        ])
        if self.domestic:
            for news in self.domestic:
                parts.append(self.format_news_item(news))
        else:
            parts.append("（今日无国内动态）")
        
        parts.extend([
            "",
            f"📄 {self.category_names['academic']}",
        ])
        if self.academic:
            for news in self.academic:
                parts.append(self.format_news_item(news))
        else:
            parts.append("（今日无深度内容）")
        
        parts.extend([
            "",
            f"📊 {self.category_names['observation']}",
            self.observation or "（今日暂无观察）",
        ])
        
        return "\n".join(parts)
