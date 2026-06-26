#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI技术动向追踪辅助脚本
用于整理和分析AI技术动态数据
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Region(Enum):
    """地区"""
    DOMESTIC = "国内"
    INTERNATIONAL = "国外"


class DynamicType(Enum):
    """动态类型"""
    MODEL_RELEASE = "模型发布"
    FEATURE_UPDATE = "功能更新"
    PERFORMANCE_BOOST = "性能提升"
    PRODUCT_LAUNCH = "产品发布"
    TECH_BREAKTHROUGH = "技术突破"
    OPEN_SOURCE = "开源发布"
    PARTNERSHIP = "合作动态"
    OTHER = "其他"


class ImportanceLevel(Enum):
    """重要级别"""
    GROUNDBREAKING = "🔴 划时代"
    MAJOR = "🟠 重大"
    MODERATE = "🟡 中等"
    MINOR = "🟢 一般"


@dataclass
class BenchmarkData:
    """基准测试数据"""
    mmlu: Optional[float] = None
    humaneval: Optional[float] = None
    gsm8k: Optional[float] = None
    hellaswag: Optional[float] = None
    math: Optional[float] = None
    context_length: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class AIDynamic:
    """AI技术动态"""
    title: str  # 动态标题
    company: str  # 涉及公司
    region: Region  # 地区
    dynamic_type: DynamicType  # 动态类型
    importance: ImportanceLevel  # 重要级别
    heat_rating: int  # 热度评级 (1-5)
    publish_date: str  # 发布日期
    
    description: str = ""  # 详细描述
    key_highlights: List[str] = None  # 技术亮点
    benchmark_before: BenchmarkData = None  # 更新前基准
    benchmark_after: BenchmarkData = None  # 更新后基准
    source_links: Dict[str, str] = None  # 来源链接
    impact_analysis: str = ""  # 影响分析
    related_products: List[str] = None  # 相关产品
    
    def __post_init__(self):
        if self.key_highlights is None:
            self.key_highlights = []
        if self.source_links is None:
            self.source_links = {}
        if self.related_products is None:
            self.related_products = []
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def get_heat_stars(self) -> str:
        """获取热度星星"""
        return "🔥" * self.heat_rating + "░" * (5 - self.heat_rating)


class AITechReport:
    """AI技术报告"""
    
    def __init__(self, start_date: str, end_date: str, report_type: str = "周报"):
        self.start_date = start_date
        self.end_date = end_date
        self.report_type = report_type
        self.dynamics: List[AIDynamic] = []
        self.generated_at = datetime.now().isoformat()
    
    def add_dynamic(self, dynamic: AIDynamic):
        """添加动态"""
        self.dynamics.append(dynamic)
    
    def get_dynamics_by_region(self, region: Region) -> List[AIDynamic]:
        """按地区获取动态"""
        return [d for d in self.dynamics if d.region == region]
    
    def get_dynamics_by_importance(self, importance: ImportanceLevel) -> List[AIDynamic]:
        """按重要级别获取动态"""
        return [d for d in self.dynamics if d.importance == importance]
    
    def get_top_dynamics(self, n: int = 5) -> List[AIDynamic]:
        """获取热度最高的N条动态"""
        return sorted(self.dynamics, key=lambda x: x.heat_rating, reverse=True)[:n]
    
    def get_groundbreaking_dynamics(self) -> List[AIDynamic]:
        """获取划时代级动态"""
        return self.get_dynamics_by_importance(ImportanceLevel.GROUNDBREAKING)
    
    def get_major_dynamics(self) -> List[AIDynamic]:
        """获取重大级动态"""
        return self.get_dynamics_by_importance(ImportanceLevel.MAJOR)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            "total": len(self.dynamics),
            "domestic": len(self.get_dynamics_by_region(Region.DOMESTIC)),
            "international": len(self.get_dynamics_by_region(Region.INTERNATIONAL)),
            "groundbreaking": len(self.get_groundbreaking_dynamics()),
            "major": len(self.get_major_dynamics()),
            "by_type": {},
            "by_company": {}
        }
        
        # 按类型统计
        for dtype in DynamicType:
            count = len([d for d in self.dynamics if d.dynamic_type == dtype])
            if count > 0:
                stats["by_type"][dtype.value] = count
        
        # 按公司统计
        for d in self.dynamics:
            company = d.company
            stats["by_company"][company] = stats["by_company"].get(company, 0) + 1
        
        return stats
    
    def export_to_json(self, filepath: str):
        """导出为JSON"""
        data = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "report_type": self.report_type,
            "generated_at": self.generated_at,
            "statistics": self.get_statistics(),
            "dynamics": [d.to_dict() for d in self.dynamics]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"报告已导出到: {filepath}")
    
    def generate_markdown(self) -> str:
        """生成Markdown格式报告"""
        lines = [
            f"# AI技术动向{self.report_type}",
            "",
            f"> 📅 **统计周期**：{self.start_date} - {self.end_date}",
            f"> 🌍 **覆盖范围**：国内 + 国外",
            f"> 📊 **收录动态**：{len(self.dynamics)}条",
            "",
            "---",
            "",
            "## 📋 执行摘要",
            "",
            "### 本周核心动态",
            ""
        ]
        
        # 添加划时代级动态摘要
        groundbreaking = self.get_groundbreaking_dynamics()
        if groundbreaking:
            lines.append("**划时代级动态**：")
            for d in groundbreaking:
                lines.append(f"- {d.company}：{d.title}")
            lines.append("")
        
        # 添加重大级动态摘要
        major = self.get_major_dynamics()
        if major:
            lines.append("**重大级动态**：")
            for d in major[:3]:
                lines.append(f"- {d.company}：{d.title}")
            lines.append("")
        
        # 统计数据
        stats = self.get_statistics()
        lines.extend([
            "### 关键数据",
            "",
            "| 指标 | 数值 |",
            "|------|------|",
            f"| 国外动态数 | {stats['international']} |",
            f"| 国内动态数 | {stats['domestic']} |",
            f"| 划时代级 | {stats['groundbreaking']} |",
            f"| 重大级 | {stats['major']} |",
            "",
            "---",
            "",
            "## ✨ 本周亮点",
            ""
        ])
        
        # 划时代级动态详情
        if groundbreaking:
            lines.append("### 🔴 划时代级动态")
            lines.append("")
            for d in groundbreaking:
                lines.extend(self._generate_dynamic_detail(d))
        
        # 重大级动态详情
        if major:
            lines.append("### 🟠 重大级动态")
            lines.append("")
            for d in major[:5]:
                lines.extend(self._generate_dynamic_brief(d))
        
        # 国外动态
        lines.extend([
            "---",
            "",
            "## 🌍 国外动态",
            ""
        ])
        international = self.get_dynamics_by_region(Region.INTERNATIONAL)
        for d in international:
            lines.extend(self._generate_dynamic_brief(d))
        
        # 国内动态
        lines.extend([
            "---",
            "",
            "## 🇨🇳 国内动态",
            ""
        ])
        domestic = self.get_dynamics_by_region(Region.DOMESTIC)
        for d in domestic:
            lines.extend(self._generate_dynamic_brief(d))
        
        # 热度排行榜
        lines.extend([
            "---",
            "",
            "## 🔥 热度排行榜",
            "",
            "### 综合热度榜",
            "",
            "| 排名 | 动态 | 公司 | 热度 | 级别 |",
            "|------|------|------|------|------|",
        ])
        
        for i, d in enumerate(self.get_top_dynamics(10), 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}")
            lines.append(f"| {medal} | {d.title} | {d.company} | {d.get_heat_stars()} | {d.importance.value} |")
        
        lines.extend([
            "",
            "---",
            "",
            f"*报告生成时间：{self.generated_at}*",
        ])
        
        return "\n".join(lines)
    
    def _generate_dynamic_detail(self, dynamic: AIDynamic) -> List[str]:
        """生成动态详细内容"""
        lines = [
            f"#### {dynamic.title}",
            "",
            "| 属性 | 内容 |",
            "|------|------|",
            f"| **涉及公司** | {dynamic.company} |",
            f"| **发布时间** | {dynamic.publish_date} |",
            f"| **动态类型** | {dynamic.dynamic_type.value} |",
            f"| **重要级别** | {dynamic.importance.value} |",
            f"| **热度评级** | {dynamic.get_heat_stars()} |",
            "",
        ]
        
        if dynamic.description:
            lines.extend([
                "**详细内容**：",
                f"{dynamic.description}",
                "",
            ])
        
        if dynamic.key_highlights:
            lines.extend([
                "**技术亮点**：",
            ])
            for highlight in dynamic.key_highlights:
                lines.append(f"- 🌟 {highlight}")
            lines.append("")
        
        if dynamic.source_links:
            lines.extend([
                "**来源链接**：",
            ])
            for name, url in dynamic.source_links.items():
                lines.append(f"- [{name}]({url})")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def _generate_dynamic_brief(self, dynamic: AIDynamic) -> List[str]:
        """生成动态简要内容"""
        lines = [
            f"#### {dynamic.title}",
            "",
            f"**公司**：{dynamic.company} | **日期**：{dynamic.publish_date} | **热度**：{dynamic.get_heat_stars()}",
            "",
        ]
        
        if dynamic.description:
            desc = dynamic.description[:100] + "..." if len(dynamic.description) > 100 else dynamic.description
            lines.append(desc)
            lines.append("")
        
        if dynamic.source_links:
            sources = " | ".join([f"[{k}]({v})" for k, v in list(dynamic.source_links.items())[:2]])
            lines.append(f"**来源**：{sources}")
            lines.append("")
        
        return lines


class SearchHelper:
    """搜索辅助"""
    
    # 国外厂商搜索关键词
    INTERNATIONAL_KEYWORDS = {
        "OpenAI": [
            "OpenAI GPT update",
            "OpenAI new model",
            "ChatGPT new features",
            "OpenAI API update",
        ],
        "Google": [
            "Google Gemini update",
            "Google AI new features",
            "Gemini Pro new version",
            "Google Bard update",
        ],
        "Anthropic": [
            "Anthropic Claude update",
            "Claude 3 new features",
            "Anthropic new model",
        ],
        "Meta": [
            "Meta Llama update",
            "Llama 3 new version",
            "Meta AI new features",
        ],
    }
    
    # 国内厂商搜索关键词
    DOMESTIC_KEYWORDS = {
        "百度": [
            "文心一言 更新",
            "文心大模型 新版本",
            "百度AI 发布",
        ],
        "阿里": [
            "通义千问 更新",
            "Qwen 新版本",
            "阿里云 大模型",
        ],
        "字节": [
            "豆包 更新",
            "云雀大模型 新版本",
            "字节AI 发布",
        ],
        "智谱": [
            "ChatGLM 更新",
            "GLM-4 新版本",
            "智谱AI 发布",
        ],
        "月之暗面": [
            "Kimi 更新",
            "Kimi 新版本",
            "月之暗面 发布",
        ],
    }
    
    @classmethod
    def get_keywords(cls, company: str = None, region: str = None) -> List[str]:
        """获取搜索关键词"""
        keywords = []
        
        if company:
            if company in cls.INTERNATIONAL_KEYWORDS:
                keywords.extend(cls.INTERNATIONAL_KEYWORDS[company])
            if company in cls.DOMESTIC_KEYWORDS:
                keywords.extend(cls.DOMESTIC_KEYWORDS[company])
        
        if region == "international":
            for kws in cls.INTERNATIONAL_KEYWORDS.values():
                keywords.extend(kws)
        elif region == "domestic":
            for kws in cls.DOMESTIC_KEYWORDS.values():
                keywords.extend(kws)
        
        return keywords
    
    @classmethod
    def get_general_keywords(cls, time_range: str = "本周") -> List[str]:
        """获取通用搜索关键词"""
        return [
            f"AI技术 {time_range}",
            f"大模型 {time_range}",
            f"LLM update {time_range}",
            "AI breakthrough",
            "大模型 发布",
        ]


class HeatCalculator:
    """热度计算器"""
    
    @staticmethod
    def calculate_heat(
        media_exposure: int = 0,  # 媒体报道数
        community_discussion: int = 0,  # 社区讨论数
        tech_impact: int = 0,  # 技术影响 (1-5)
        business_impact: int = 0,  # 商业影响 (1-5)
        user_attention: int = 0,  # 用户关注度 (1-5)
    ) -> int:
        """
        计算热度评级 (1-5)
        
        权重：
        - 媒体曝光: 25%
        - 社区讨论: 25%
        - 技术影响: 20%
        - 商业影响: 15%
        - 用户关注: 15%
        """
        # 媒体曝光评分 (0-5)
        if media_exposure >= 10:
            media_score = 5
        elif media_exposure >= 5:
            media_score = 4
        elif media_exposure >= 2:
            media_score = 3
        elif media_exposure >= 1:
            media_score = 2
        else:
            media_score = 1
        
        # 社区讨论评分 (0-5)
        if community_discussion >= 5000:
            community_score = 5
        elif community_discussion >= 1000:
            community_score = 4
        elif community_discussion >= 100:
            community_score = 3
        elif community_discussion >= 10:
            community_score = 2
        else:
            community_score = 1
        
        # 计算加权总分
        weighted_score = (
            media_score * 0.25 +
            community_score * 0.25 +
            tech_impact * 0.20 +
            business_impact * 0.15 +
            user_attention * 0.15
        )
        
        return min(max(round(weighted_score), 1), 5)


# 使用示例
if __name__ == "__main__":
    # 创建报告
    report = AITechReport("2024-01-15", "2024-01-21", "周报")
    
    # 添加示例动态
    dynamic = AIDynamic(
        title="GPT-4 Turbo 更新",
        company="OpenAI",
        region=Region.INTERNATIONAL,
        dynamic_type=DynamicType.MODEL_RELEASE,
        importance=ImportanceLevel.MAJOR,
        heat_rating=4,
        publish_date="2024-01-16",
        description="OpenAI发布了GPT-4 Turbo的更新版本，在多个基准测试上有显著提升。",
        key_highlights=[
            "上下文长度扩展到128K",
            "代码能力显著提升",
            "多模态能力增强"
        ],
        source_links={
            "官方公告": "https://openai.com/blog",
            "技术报告": "https://openai.com/research"
        }
    )
    
    report.add_dynamic(dynamic)
    
    # 生成Markdown
    markdown = report.generate_markdown()
    print(markdown)
    
    # 导出JSON
    report.export_to_json("ai_tech_report.json")
    
    # 获取搜索关键词
    keywords = SearchHelper.get_keywords("OpenAI")
    print("\n搜索关键词：")
    for kw in keywords:
        print(f"  - {kw}")
