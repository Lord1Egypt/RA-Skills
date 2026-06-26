#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Article Analyzer Core Module
文章分析核心模块 - 从 article-analyzer 迁移

功能：接收文章 URL → 分析总结 → 生成标签 → 归档

注意：
    此模块提供分析逻辑，但需要配合 OpenClaw 工具系统使用：
    - web_fetch/browser: 内容抓取
    - feishu-create-doc: 创建飞书文档
    - feishu-bitable: 写入多维表格
    
    独立运行时仅支持分析和去重功能
"""

import json
from pathlib import Path
from datetime import datetime

# 导入工具模块
from .dedup import check_url_duplicate, add_url_to_cache
from .scorer import evaluate_quality_score

# 模块目录（相对路径）
MODULE_DIR = Path(__file__).parent
SKILL_DIR = MODULE_DIR.parent


class ArticleAnalyzer:
    """文章分析器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化分析器
        
        Args:
            config_path: 配置文件路径，默认为 skills/article-workflow/config.json
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.json"
        
        self.config = self._load_config(config_path)
        self.bitable_token = self.config.get("bitable", {}).get("app_token")
        self.table_id = self.config.get("bitable", {}).get("table_id")
    
    def _load_config(self, config_path: Path) -> dict:
        """加载配置文件"""
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def analyze(self, url: str, title: str = None, content: str = None) -> dict:
        """
        分析文章
        
        Args:
            url: 文章 URL
            title: 文章标题（可选，如不提供则自动提取）
            content: 文章内容（可选，如不提供则自动抓取）
        
        Returns:
            dict: 分析结果
                - title: 标题
                - url: URL
                - source: 来源平台
                - summary: 简短摘要
                - tags: 关键词标签
                - importance: 重要程度
                - quality_score: 质量评分
                - report_content: 详细报告内容
        """
        # 1. URL 去重检查
        dedup_result = check_url_duplicate(url)
        if dedup_result["is_duplicate"]:
            return {
                "success": False,
                "error": "duplicate",
                "message": f"URL 已存在：{url}",
                "existing_record": dedup_result["record"]
            }
        
        # 2. 抓取内容（如果未提供）
        if title is None or content is None:
            fetched = self._fetch_content(url)
            if title is None:
                title = fetched.get("title", "")
            if content is None:
                content = fetched.get("content", "")
        
        # 3. 分析总结
        analysis = self._analyze_content(title, content)
        
        # 4. 质量评分
        quality_score = evaluate_quality_score(
            title=title,
            content=content,
            summary=analysis.get("summary", "")
        )
        
        # 5. 生成详细报告
        report_content = self._generate_report(title, url, analysis, quality_score)
        
        return {
            "success": True,
            "title": title,
            "url": url,
            "source": self._detect_source(url),
            "summary": analysis.get("summary", ""),
            "tags": analysis.get("tags", []),
            "importance": analysis.get("importance", "中"),
            "quality_score": quality_score,
            "report_content": report_content
        }
    
    def _fetch_content(self, url: str) -> dict:
        """
        抓取文章内容
        
        Args:
            url: 文章 URL
        
        Returns:
            dict: {"title": str, "content": str}
        """
        # 这里调用 OpenClaw 的 web_fetch 或 browser 工具
        # 实际实现需要集成到 OpenClaw 工具系统
        return {
            "title": "",
            "content": ""
        }
    
    def _analyze_content(self, title: str, content: str) -> dict:
        """
        分析文章内容
        
        Args:
            title: 文章标题
            content: 文章内容
        
        Returns:
            dict: {"summary": str, "tags": list, "importance": str}
        """
        # 这里调用 LLM 进行分析
        # 实际实现需要集成到 OpenClaw 工具系统
        return {
            "summary": "",
            "tags": [],
            "importance": "中"
        }
    
    def _generate_report(self, title: str, url: str, analysis: dict, quality_score: dict) -> str:
        """
        生成详细报告
        
        Args:
            title: 标题
            url: URL
            analysis: 分析结果
            quality_score: 质量评分
        
        Returns:
            str: Markdown 格式报告
        """
        report = f"""# 📄 {title} 分析报告

---

## 📌 基本信息

- **标题：** {title}
- **来源 URL：** {url}
- **来源平台：** {self._detect_source(url)}
- **阅读日期：** {datetime.now().strftime('%Y-%m-%d')}
- **重要程度：** {analysis.get('importance', '中')}

---

## 📝 简短摘要

{analysis.get('summary', '暂无摘要')}

---

## 🏷️ 关键词标签

{self._format_tags(analysis.get('tags', []))}

---

## 🔍 详细分析

### 背景

[文章发布的背景、解决的问题]

### 核心内容

[文章的主要内容、论点、方法]

### 亮点与价值

1. [亮点 1]
2. [亮点 2]
3. [亮点 3]

### 风险与问题

1. [风险 1]
2. [风险 2]

### 适配建议

[对团队的适配性分析、如何使用]

---

## ✅ 行动项

- [ ] [行动项 1]
- [ ] [行动项 2]
- [ ] [行动项 3]

---

## 📊 质量评分

| 维度 | 分数 |
|------|------|
| 内容价值 | {quality_score.get('content_value', 0)}/40 |
| 技术深度 | {quality_score.get('technical_depth', 0)}/30 |
| 适配性 | {quality_score.get('relevance', 0)}/20 |
| 可读性 | {quality_score.get('readability', 0)}/10 |
| **总分** | **{quality_score.get('total', 0)}/100** |
| **等级** | **{quality_score.get('level', 'N/A')}** |

---

## 🔗 相关链接

- [原文链接]({url})

---

*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*
*分析 Agent：Article Workflow Skill*
"""
        return report
    
    def _detect_source(self, url: str) -> str:
        """
        检测文章来源平台
        
        Args:
            url: 文章 URL
        
        Returns:
            str: 平台名称（微信/知乎/GitHub/新闻/其他）
        """
        if "mp.weixin.qq.com" in url:
            return "微信"
        elif "zhihu.com" in url:
            return "知乎"
        elif "github.com" in url:
            return "GitHub"
        elif "news" in url or "163.com" in url or "sina.com" in url:
            return "新闻"
        else:
            return "其他"
    
    def _format_tags(self, tags: list) -> str:
        """格式化标签输出"""
        if not tags:
            return "暂无标签"
        return "\n".join([f"- {tag}" for tag in tags])
    
    def archive_to_bitable(self, analysis_result: dict, doc_url: str) -> dict:
        """
        归档到 Bitable
        
        Args:
            analysis_result: 分析结果
            doc_url: 详细报告文档链接
        
        Returns:
            dict: {"record_id": str, "success": bool}
        """
        # 这里调用飞书 Bitable API
        # 实际实现需要集成到 OpenClaw 工具系统
        return {
            "record_id": "",
            "success": True
        }
    
    def create_doc(self, report_content: str, title: str) -> str:
        """
        创建飞书文档
        
        Args:
            report_content: 报告内容（Markdown）
            title: 文档标题
        
        Returns:
            str: 文档 URL
        """
        # 这里调用飞书文档 API
        # 实际实现需要集成到 OpenClaw 工具系统
        return ""
    
    def process(self, url: str) -> dict:
        """
        完整处理流程：分析→归档→创建文档
        
        Args:
            url: 文章 URL
        
        Returns:
            dict: 完整处理结果
        """
        # 1. 分析
        analysis = self.analyze(url)
        if not analysis.get("success"):
            return analysis
        
        # 2. 创建文档
        doc_url = self.create_doc(
            analysis.get("report_content", ""),
            analysis.get("title", "")
        )
        
        # 3. 归档到 Bitable
        archive_result = self.archive_to_bitable(analysis, doc_url)
        
        # 4. 添加到 URL 缓存
        add_url_to_cache(
            url=url,
            title=analysis.get("title", ""),
            record_id=archive_result.get("record_id", ""),
            doc_url=doc_url
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "doc_url": doc_url,
            "archive": archive_result
        }


# 便捷函数
def analyze_article(url: str) -> dict:
    """
    便捷函数：分析单篇文章
    
    Args:
        url: 文章 URL
    
    Returns:
        dict: 分析结果
    """
    analyzer = ArticleAnalyzer()
    return analyzer.analyze(url)


def process_article(url: str) -> dict:
    """
    便捷函数：完整处理文章（分析 + 归档）
    
    Args:
        url: 文章 URL
    
    Returns:
        dict: 处理结果
    """
    analyzer = ArticleAnalyzer()
    return analyzer.process(url)
