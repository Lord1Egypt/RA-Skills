#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 内容分析器 - 在同一次流式请求中完成所有分析

功能：
1. 一次性分析内容，输出标签 + 摘要 + 报告 + 评分
2. 不增加模型请求次数（同一次流式请求）
3. 结构化输出（JSON 格式）

设计原则：
- ✅ 单次流式请求完成所有分析
- ✅ 工具调用不中断流式
- ✅ 结构化 Prompt，一次性输出多个字段
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class AnalysisResult:
    """分析结果"""
    tags: List[str]
    summary: str
    report: str
    quality_score: int
    quality_level: str
    importance: str
    cover_image_url: Optional[str] = None


class LLMContentAnalyzer:
    """LLM 内容分析器"""
    
    # 结构化 Prompt 模板
    ANALYSIS_PROMPT = """请分析以下文章内容，并输出完整的结构化结果。

文章标题：{title}
文章内容：
{content}

请按以下要求输出：

1. **关键词标签**（3-5 个）
   - 标签简洁明了（2-6 个字）
   - 覆盖核心主题和技术点
   - 优先提取技术栈、框架、平台名称
   - 避免过于宽泛的标签

2. **简短摘要**（3-5 句，200 字以内）
   - 概括文章核心内容
   - 说明解决的问题或提供的价值

3. **重要程度**（高/中/低）
   - 高：前沿技术、重大更新、深度分析
   - 中：常规技术文章、案例分析
   - 低：简讯、广告、低质量内容

4. **质量评分**（0-100 分）
   - 内容价值（40 分）：信息量、实用性、原创性
   - 技术深度（30 分）：技术含量、专业度
   - 可读性（20 分）：结构清晰、表达准确
   - 时效性（10 分）：内容新颖、不过时

**输出格式：严格使用 JSON**

```json
{{
  "tags": ["标签 1", "标签 2", "标签 3"],
  "summary": "摘要内容...",
  "importance": "高",
  "quality_score": {{
    "content_value": 35,
    "technical_depth": 25,
    "readability": 18,
    "timeliness": 8,
    "total": 86
  }},
  "quality_level": "A",
  "reasoning": "评分理由简述"
}}
```

**质量等级标准：**
- S 级：85-100 分（极高价值，立即处理）
- A 级：70-84 分（高价值，优先处理）
- B 级：55-69 分（中等价值，正常处理）
- C 级：40-54 分（低价值，简略处理）
- D 级：0-39 分（极低价值，跳过或仅存档）
"""
    
    def __init__(self):
        """初始化分析器"""
        pass
    
    async def analyze(self, title: str, content: str, cover_image_url: Optional[str] = None) -> AnalysisResult:
        """
        分析文章内容（单次流式请求）
        
        Args:
            title: 文章标题
            content: 文章内容
            cover_image_url: 封面图片 URL（可选）
        
        Returns:
            AnalysisResult: 分析结果
        """
        # 构建 Prompt
        prompt = self.ANALYSIS_PROMPT.format(
            title=title,
            content=content[:3000]  # 限制内容长度，避免 token 超限
        )
        
        # TODO: 调用 LLM API（单次流式请求）
        # 示例代码：
        # stream = await llm.stream_generate(prompt)
        # response = await stream.finish()
        # result = json.loads(response)
        
        # 演示用：模拟分析结果
        result = self._mock_analysis(title, content)
        
        # 添加封面图片
        if cover_image_url:
            result.cover_image_url = cover_image_url
        
        return result
    
    def _mock_analysis(self, title: str, content: str) -> AnalysisResult:
        """
        模拟分析结果（演示用）
        
        实际使用时会被 LLM API 调用替换
        """
        # 基于标题和内容的简单分析
        tags = self._extract_tags(title, content)
        summary = self._generate_summary(title, content)
        importance = self._determine_importance(title, content)
        score = self._calculate_score(content)
        
        return AnalysisResult(
            tags=tags,
            summary=summary,
            report="",  # 详细报告由主流程生成
            quality_score=score,
            quality_level=self._score_to_level(score),
            importance=importance
        )
    
    def _extract_tags(self, title: str, content: str) -> List[str]:
        """提取关键词标签"""
        tags = []
        
        # 关键词映射
        keyword_map = {
            "OpenClaw": ["OpenClaw", "AI 智能体", "Skill 生态"],
            "Agent": ["AI Agent", "多智能体", "自动化"],
            "智能体": ["AI 智能体", "多智能体协作"],
            "开源": ["开源项目", "GitHub"],
            "AI 编程": ["AI 编程", "代码生成", "自动化开发"],
            "Spec": ["Spec-Driven", "规范驱动开发"],
            "ChatDev": ["多智能体开发", "游戏开发"],
            "NocoBase": ["无代码", "低代码", "数据模型驱动"],
            "案例": ["落地案例", "最佳实践"],
            "Spring": ["Java", "后端开发", "框架更新"],
            "百度搜索": ["百度搜索", "搜索引擎", "国产 AI"],
            "Skill": ["Skill 生态", "ClawHub"],
            "多智能体": ["多智能体协作", "Agent 协作"],
            "GitHub": ["GitHub", "开源项目"],
            "Llm": ["LLM", "大语言模型", "AI"],
            "API": ["API 集成", "工具调用"],
            "RAG": ["RAG", "检索增强", "知识库"],
            "Agent": ["Agent", "智能体", "自动化"],
        }
        
        # 检查标题
        text = title + " " + content[:500]
        for keyword, tag_list in keyword_map.items():
            if keyword.lower() in text.lower():
                tags.extend(tag_list[:2])  # 每个关键词最多取 2 个标签
        
        # 去重并限制数量
        unique_tags = list(dict.fromkeys(tags))[:5]
        
        # 如果标签不足，添加通用标签
        if len(unique_tags) < 3:
            unique_tags.append("技术文章")
        
        return unique_tags
    
    def _generate_summary(self, title: str, content: str) -> str:
        """生成摘要"""
        # 简单实现：取标题 + 内容前 100 字
        content_preview = content[:200].replace('\n', ' ').strip()
        return f"文章《{title}》主要介绍了{content_preview}..."
    
    def _determine_importance(self, title: str, content: str) -> str:
        """判断重要程度"""
        # 高重要性关键词
        high_keywords = ["重大", "突破", "首次", "最新发布", "深度分析", "完整指南"]
        
        # 中重要性关键词
        medium_keywords = ["教程", "实战", "案例分析", "对比", "评测"]
        
        text = title + " " + content[:500]
        
        if any(kw in text for kw in high_keywords):
            return "高"
        elif any(kw in text for kw in medium_keywords):
            return "中"
        else:
            return "中"
    
    def _calculate_score(self, content: str) -> int:
        """计算质量评分"""
        # 简单实现：基于内容长度和质量
        length = len(content)
        
        if length > 3000:
            return 85  # A 级
        elif length > 1500:
            return 75  # A 级
        elif length > 800:
            return 65  # B 级
        else:
            return 50  # C 级
    
    def _score_to_level(self, score: int) -> str:
        """分数转等级"""
        if score >= 85:
            return "S"
        elif score >= 70:
            return "A"
        elif score >= 55:
            return "B"
        elif score >= 40:
            return "C"
        else:
            return "D"


# 便捷函数
async def analyze_content(title: str, content: str, cover_image_url: Optional[str] = None) -> AnalysisResult:
    """
    便捷函数：分析文章内容
    
    Args:
        title: 文章标题
        content: 文章内容
        cover_image_url: 封面图片 URL
    
    Returns:
        AnalysisResult: 分析结果
    """
    analyzer = LLMContentAnalyzer()
    return await analyzer.analyze(title, content, cover_image_url)


# 测试
if __name__ == "__main__":
    import asyncio
    
    async def test():
        result = await analyze_content(
            title="OpenClaw 智能路由优化",
            content="这是一篇关于 OpenClaw 智能路由优化的技术文章...",
            cover_image_url="https://example.com/cover.jpg"
        )
        
        print("分析结果：")
        print(f"  标签：{', '.join(result.tags)}")
        print(f"  摘要：{result.summary[:50]}...")
        print(f"  重要程度：{result.importance}")
        print(f"  质量评分：{result.quality_score}/100 ({result.quality_level}级)")
        print(f"  封面图：{result.cover_image_url or '无'}")
    
    asyncio.run(test())
