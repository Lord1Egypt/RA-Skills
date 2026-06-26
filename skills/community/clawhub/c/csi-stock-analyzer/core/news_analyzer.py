#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻分析模块 - 分析公司新闻舆情，识别利好利空、做空信息、管理层变动等
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime

class NewsAnalyzer:
    def __init__(self):
        # 关键词词典
        self.short_keywords = [
            '做空', '看空', '沽空', '做空报告', '浑水', '香橼', '做空机构',
            '质疑', '财务造假', '欺诈', '虚假陈述', '内幕交易'
        ]
        
        self.positive_keywords = [
            '利好', '盈利增长', '营收增长', '利润大增', '订单大增', '合同签订',
            '新产品发布', '技术突破', '成本下降', '效率提升', '政策支持',
            '产能扩张', '市场拓展', '战略合作', '收购优质资产', '股权激励',
            '回购', '增持', '分红', '高送转', '业绩预增', '超预期'
        ]
        
        self.negative_keywords = [
            '利空', '亏损', '业绩下滑', '利润下降', '营收下降', '订单减少',
            '合同违约', '产品质量问题', '安全事故', '环境污染', '法律诉讼',
            '行政处罚', '监管调查', '立案调查', '股东减持', '高管减持',
            '解禁', '商誉减值', '资产减值', '坏账', '现金流紧张', '债务违约',
            '停产', '停工', '裁员', '高管离职', '管理层动荡'
        ]
        
        self.management_keywords = [
            '离职', '辞职', '卸任', '离任', '接任', '新任', '任命', '空降',
            '人事变动', '管理层变动', '董事会换届', '董事长变更', '总经理变更',
            'CEO变更', 'CFO变更', 'CTO变更'
        ]
        
        self.outlook_keywords = [
            '展望', '预期', '目标', '未来规划', '战略规划', '业绩指引',
            '营收目标', '利润目标', '市场份额目标', '研发投入', '产能规划'
        ]
        
        self.holder_keywords = [
            '减持', '增持', '回购', '股东减持', '高管减持', '机构减持',
            '股东增持', '高管增持', '机构增持', '要约收购', '举牌'
        ]
    
    def analyze_news_sentiment(self, news_list: List[Dict], company_name: str) -> Dict:
        """
        分析新闻情感和关键信息
        :param news_list: 新闻列表
        :param company_name: 公司名称
        :return: 分析结果
        """
        if not news_list:
            return {
                'has_short_report': False,
                'short_reports': [],
                'positive_news': [],
                'negative_news': [],
                'management_news': [],
                'holder_news': [],
                'outlook_news': [],
                'overall_sentiment': 'neutral',
                'news_count': 0,
                'positive_count': 0,
                'negative_count': 0
            }
        
        short_reports = []
        positive_news = []
        negative_news = []
        management_news = []
        holder_news = []
        outlook_news = []
        
        for news in news_list:
            title = news.get('title', '').lower()
            content = news.get('content', '').lower()
            full_text = f"{title} {content}"
            
            # 检查做空信息
            if any(keyword in full_text for keyword in self.short_keywords) and company_name in full_text:
                short_reports.append(news)
            
            # 检查利好消息
            if any(keyword in full_text for keyword in self.positive_keywords):
                positive_news.append(news)
            
            # 检查利空消息
            if any(keyword in full_text for keyword in self.negative_keywords):
                negative_news.append(news)
            
            # 检查管理层变动
            if any(keyword in full_text for keyword in self.management_keywords):
                management_news.append(news)
            
            # 检查股东变动
            if any(keyword in full_text for keyword in self.holder_keywords):
                holder_news.append(news)
            
            # 检查管理层展望
            if any(keyword in full_text for keyword in self.outlook_keywords):
                outlook_news.append(news)
        
        # 整体情感判断
        total = len(positive_news) + len(negative_news)
        overall_sentiment = 'neutral'
        if total > 0:
            positive_ratio = len(positive_news) / total
            if positive_ratio > 0.6:
                overall_sentiment = 'positive'
            elif positive_ratio < 0.4:
                overall_sentiment = 'negative'
        
        return {
            'has_short_report': len(short_reports) > 0,
            'short_reports': short_reports,
            'positive_news': positive_news,
            'negative_news': negative_news,
            'management_news': management_news,
            'holder_news': holder_news,
            'outlook_news': outlook_news,
            'overall_sentiment': overall_sentiment,
            'news_count': len(news_list),
            'positive_count': len(positive_news),
            'negative_count': len(negative_news)
        }
    
    def extract_management_outlook(self, outlook_news: List[Dict]) -> str:
        """
        提取管理层对未来的展望
        :param outlook_news: 展望相关新闻
        :return: 展望摘要
        """
        if not outlook_news:
            return "暂无公开的管理层展望信息"
        
        outlook_points = []
        for news in outlook_news[:3]:  # 取最近3条
            title = news.get('title', '')
            content = news.get('content', '')[:200] + '...' if len(news.get('content', '')) > 200 else news.get('content', '')
            outlook_points.append(f"- {title}: {content}")
        
        return "\n".join(outlook_points)
    
    def analyze_management_stability(self, management_news: List[Dict]) -> Tuple[str, str]:
        """
        分析管理层稳定性
        :param management_news: 管理层相关新闻
        :return: (稳定性评级, 详细说明)
        """
        if not management_news:
            return ("stable", "近期无管理层变动公告，管理层保持稳定")
        
        recent_changes = []
        for news in management_news:
            title = news.get('title', '')
            date = news.get('published_date', '未知日期')
            recent_changes.append(f"- {date}: {title}")
        
        change_count = len(recent_changes)
        if change_count >= 3:
            return ("unstable", f"近期管理层变动频繁，共{change_count}起变动：\n" + "\n".join(recent_changes))
        elif change_count >= 1:
            return ("minor_changes", f"近期有少数管理层变动：\n" + "\n".join(recent_changes))
        else:
            return ("stable", "管理层保持稳定")
    
    def analyze_holder_changes(self, holder_news: List[Dict]) -> Dict:
        """
        分析股东变动情况
        :param holder_news: 股东相关新闻
        :return: 分析结果
        """
        has_institution_reduction = any('机构减持' in news.get('title', '') or '机构减持' in news.get('content', '') for news in holder_news)
        has_management_reduction = any('高管减持' in news.get('title', '') or '高管减持' in news.get('content', '') for news in holder_news)
        has_increase = any('增持' in news.get('title', '') or '增持' in news.get('content', '') for news in holder_news)
        has_repurchase = any('回购' in news.get('title', '') or '回购' in news.get('content', '') for news in holder_news)
        
        recent_changes = []
        for news in holder_news[:5]:
            title = news.get('title', '')
            date = news.get('published_date', '未知日期')
            recent_changes.append(f"- {date}: {title}")
        
        return {
            'has_institution_reduction': has_institution_reduction,
            'has_management_reduction': has_management_reduction,
            'has_increase': has_increase,
            'has_repurchase': has_repurchase,
            'recent_changes': recent_changes
        }
