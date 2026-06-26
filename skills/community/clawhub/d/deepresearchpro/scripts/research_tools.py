#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepResearchPro - 辅助调研工具
提供搜索查询生成、结果解析、引用格式化等功能

重要说明：
- 本脚本仅用于生成搜索查询和格式化输出
- 实际搜索执行必须使用 browser 工具，禁止使用 web_search 工具
- 搜索查询生成后，需通过 browser 工具访问目标页面获取内容
"""

import re
from datetime import datetime
from typing import List, Dict, Tuple


class SearchQueryGenerator:
    """搜索查询生成器"""
    
    @staticmethod
    def generate_queries(topic: str, platforms: List[str] = None) -> Dict[str, List[str]]:
        """
        为不同平台生成搜索查询
        
        Args:
            topic: 调研主题
            platforms: 目标平台列表，默认所有平台
            
        Returns:
            字典，key 为平台名，value 为搜索查询列表
        """
        if platforms is None:
            platforms = ['google', 'bilibili', 'xiaohongshu', 'douyin', 'scholar']
        
        queries = {}
        
        # 通用搜索查询
        if 'google' in platforms:
            queries['google'] = [
                topic,
                f"{topic} 2024",
                f"{topic} 2025",
                f"{topic} latest",
                f"{topic} analysis",
                f"{topic} trends",
            ]
        
        # B 站搜索查询
        if 'bilibili' in platforms:
            queries['bilibili'] = [
                f"site:bilibili.com {topic}",
                f"site:bilibili.com {topic} 解析",
                f"site:bilibili.com {topic} 深度",
                f"site:bilibili.com {topic} 解读",
            ]
        
        # 小红书搜索查询
        if 'xiaohongshu' in platforms:
            queries['xiaohongshu'] = [
                f"site:xiaohongshu.com {topic}",
                f"site:xiaohongshu.com {topic} 体验",
                f"site:xiaohongshu.com {topic} 测评",
                f"site:xiaohongshu.com {topic} 真实",
            ]
        
        # 抖音搜索查询
        if 'douyin' in platforms:
            queries['douyin'] = [
                f"site:douyin.com {topic}",
                f"site:douyin.com #{topic}",
                f"site:douyin.com {topic} 热点",
            ]
        
        # 学术搜索查询
        if 'scholar' in platforms:
            queries['scholar'] = [
                f'"{topic}"',
                f"{topic} research",
                f"{topic} study",
                f"{topic} analysis",
            ]
        
        return queries


class CitationFormatter:
    """引用格式化器"""
    
    @staticmethod
    def format_citation(source_name: str, title: str, url: str, index: int) -> str:
        """
        格式化引用条目
        
        Args:
            source_name: 来源名称
            title: 文章/视频标题
            url: 完整 URL
            index: 引用编号
            
        Returns:
            格式化后的引用字符串
        """
        return f"- [{index}] **{source_name}** - *{title}* ({url})"
    
    @staticmethod
    def mark_citation(text: str, index: int) -> str:
        """
        在文本中标注引用
        
        Args:
            text: 原文本
            index: 引用编号
            
        Returns:
            带引用标记的文本
        """
        return f"{text} [{index}]"


class SearchResultParser:
    """搜索结果解析器"""
    
    @staticmethod
    def extract_title(html_content: str) -> str:
        """从 HTML 中提取标题"""
        pattern = r'<title>(.*?)</title>'
        match = re.search(pattern, html_content, re.IGNORECASE)
        return match.group(1).strip() if match else "Unknown Title"
    
    @staticmethod
    def extract_date(html_content: str) -> str:
        """从 HTML 中提取发布日期"""
        # 尝试多种日期格式
        patterns = [
            r'<meta property="article:published_time" content="(.*?)">',
            r'<meta name="date" content="(.*?)">',
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content)
            if match:
                return match.group(1)
        
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def is_quality_source(url: str, title: str) -> Tuple[bool, str]:
        """
        评估来源质量
        
        Args:
            url: URL
            title: 标题
            
        Returns:
            (是否高质量，质量等级)
        """
        quality_indicators = {
            'academic': ['.edu', '.ac.uk', 'nature.com', 'science.org', 'scholar.google.com'],
            'authoritative': ['.gov', 'reuters.com', 'bbc.com', 'xinhuanet.com', 'people.com.cn'],
            'media': ['caixin.com', 'thepaper.cn', '36kr.com', 'techcrunch.com'],
            'social': ['bilibili.com', 'xiaohongshu.com', 'douyin.com'],
        }
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        for quality, indicators in quality_indicators.items():
            if any(indicator in url_lower for indicator in indicators):
                return True, quality
        
        # 检查标题质量
        spam_keywords = ['广告', '点击这里', '免费领取', '震惊', '必看']
        if any(keyword in title_lower for keyword in spam_keywords):
            return False, 'spam'
        
        return True, 'general'


class ReportGenerator:
    """报告生成器"""
    
    @staticmethod
    def generate_metadata(topic: str, sources_count: int, duration_minutes: int) -> str:
        """生成报告元数据"""
        return f"""
## 元数据信息
- **调研主题**: {topic}
- **调研时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
- **调研时长**: {duration_minutes}分钟
- **信息源数量**: {sources_count}个
"""
    
    @staticmethod
    def generate_reference_list(citations: List[Dict]) -> str:
        """
        生成参考资料列表
        
        Args:
            citations: 引用列表，每个元素为{'source_name': str, 'title': str, 'url': str}
            
        Returns:
            格式化后的参考资料列表
        """
        formatted = []
        for i, citation in enumerate(citations, 1):
            formatted.append(
                CitationFormatter.format_citation(
                    citation['source_name'],
                    citation['title'],
                    citation['url'],
                    i
                )
            )
        return '\n'.join(formatted)


if __name__ == "__main__":
    # 测试示例
    generator = SearchQueryGenerator()
    queries = generator.generate_queries("电动汽车电池技术")
    
    print("搜索查询生成示例:")
    for platform, query_list in queries.items():
        print(f"\n{platform}:")
        for query in query_list:
            print(f"  - {query}")
    
    # 测试引用格式化
    formatter = CitationFormatter()
    citation = formatter.format_citation(
        "Reuters",
        "Global EV Battery Market Analysis",
        "https://reuters.com/business/autos-transportation/ev-battery-2024",
        1
    )
    print(f"\n格式化引用:\n{citation}")
    
    # 测试来源质量评估
    parser = SearchResultParser()
    is_quality, quality = parser.is_quality_source(
        "https://reuters.com/business/autos-transportation",
        "Global EV Battery Market Reaches 250GWh in 2024"
    )
    print(f"\n来源质量评估: {is_quality}, 等级: {quality}")
