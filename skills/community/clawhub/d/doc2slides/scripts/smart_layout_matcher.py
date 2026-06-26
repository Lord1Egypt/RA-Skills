#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

#!/usr/bin/env python3
"""
Smart Layout Matcher - LLM-based intelligent layout and chart selection.

Uses LLM to analyze data characteristics and choose the most appropriate
visualization type for each slide.

Usage:
    from smart_layout_matcher import SmartLayoutMatcher
    
    matcher = SmartLayoutMatcher(model="glm-4-flash")
    result = await matcher.match(slide_data)
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Add parent to path
CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))

try:
    from llm_adapter import LLMAdapter
    HAS_LLM = True
except ImportError:
    HAS_LLM = False
    print("Warning: llm_adapter not found")


@dataclass
class LayoutMatch:
    """Result of smart layout matching."""
    layout: str
    chart_type: str
    confidence: float
    reason: str
    visual_elements: List[str]
    color_suggestion: str
    data_preprocessing: Dict[str, Any]


# All available layouts with descriptions
LAYOUT_CATALOG = {
    "DASHBOARD": {
        "name": "仪表盘",
        "best_for": "多指标展示，3-6个数据点",
        "chart_types": ["kpi_cards", "progress_rings", "mini_charts"],
        "data_range": (3, 6),
        "visual_strength": 5
    },
    "BIG_NUMBER": {
        "name": "大数字",
        "best_for": "突出核心指标，1-2个关键数据",
        "chart_types": ["hero_number", "supporting_chart"],
        "data_range": (1, 2),
        "visual_strength": 5
    },
    "COMPARISON": {
        "name": "对比布局",
        "best_for": "A/B对比，前后对比，新旧方案对比",
        "chart_types": ["two_column", "vs_badge", "comparison_bars"],
        "data_range": (2, 4),
        "visual_strength": 5
    },
    "PYRAMID": {
        "name": "金字塔",
        "best_for": "层级结构，优先级递进，从上到下的关系",
        "chart_types": ["svg_pyramid", "numbered_cards"],
        "data_range": (3, 5),
        "visual_strength": 4
    },
    "TIMELINE": {
        "name": "时间线",
        "best_for": "时间序列，发展历程，里程碑",
        "chart_types": ["horizontal_timeline", "vertical_timeline"],
        "data_range": (3, 8),
        "visual_strength": 4
    },
    "PIE_CHART": {
        "name": "饼图/环形图",
        "best_for": "占比关系，百分比数据，整体构成",
        "chart_types": ["donut_chart", "pie_chart", "percentage_bars"],
        "data_range": (2, 6),
        "visual_strength": 5
    },
    "RADAR_CHART": {
        "name": "雷达图",
        "best_for": "多维度能力对比，360度评估",
        "chart_types": ["hexagon_radar", "pentagon_radar"],
        "data_range": (3, 8),
        "visual_strength": 4
    },
    "TABLE": {
        "name": "表格",
        "best_for": "大量结构化数据，详细对比",
        "chart_types": ["data_table", "comparison_table"],
        "data_range": (6, 20),
        "visual_strength": 3
    },
    "GAUGE": {
        "name": "仪表盘",
        "best_for": "单一指标，进度完成率",
        "chart_types": ["gauge_arc", "progress_bar"],
        "data_range": (1, 1),
        "visual_strength": 5
    },
    "ACTION_PLAN": {
        "name": "行动计划",
        "best_for": "步骤流程，实施路径，操作指南",
        "chart_types": ["step_cards", "flow_arrows"],
        "data_range": (3, 6),
        "visual_strength": 4
    },
    "CARD": {
        "name": "卡片列表",
        "best_for": "并列要点，无层级关系",
        "chart_types": ["numbered_cards", "icon_cards"],
        "data_range": (3, 6),
        "visual_strength": 3
    },
    "CONTENT": {
        "name": "内容页",
        "best_for": "纯文字内容，无数据",
        "chart_types": ["bullet_points", "paragraph"],
        "data_range": (0, 2),
        "visual_strength": 1
    }
}


MATCH_PROMPT = """你是专业的数据可视化设计师，擅长为商业PPT选择最佳布局和图表类型。

## 幻灯片数据
```json
{slide_json}
```

## 可用布局类型
{layout_catalog}

## 分析步骤

### 第一步：数据特征分析
- 数据点数量：{data_count}
- 数据类型：{data_types}
- 数值范围：{value_ranges}
- 单位类型：{unit_types}

### 第二步：内容语义分析
检查以下关键词和模式：

**对比关系** (推荐 COMPARISON)
- 关键词：vs、对比、比较、优于、提升、增长、下降、传统vs创新、前后对比
- 特征：两组或多组数据形成对比关系

**时间序列** (推荐 TIMELINE)
- 关键词：年、月、季度、阶段、历程、发展、时间轴、里程碑
- 特征：数据按时间顺序排列，展示演进过程

**层级关系** (推荐 PYRAMID)
- 关键词：战略、目标、优先级、核心、支撑、从上到下、金字塔
- 特征：数据有明确层级，上层依赖下层

**占比关系** (推荐 PIE_CHART)
- 关键词：%、占比、构成、份额、比例、百分比
- 特征：数据总和为100%，展示部分与整体关系

**多维评估** (推荐 RADAR_CHART)
- 关键词：能力、维度、评估、评分、综合、360度
- 特征：多维度数值评估，维度数3-8个

**单一核心指标** (推荐 BIG_NUMBER)
- 关键词：核心、关键、重要、突破、里程碑
- 特征：1-2个数据点，需要强调突出

**多指标展示** (推荐 DASHBOARD)
- 关键词：概览、汇总、数据看板、指标
- 特征：3-6个独立数据点，无明确关系

**流程步骤** (推荐 PROCESS_FLOW 或 ACTION_PLAN)
- 关键词：步骤、流程、路径、实施、阶段、操作
- 特征：数据有先后顺序或依赖关系

### 第三步：视觉需求分析
考虑以下因素：
- 需要突出什么？（核心数字、对比差异、趋势变化、构成比例）
- 信息密度要求？（简洁突出 vs 详细完整）
- 视觉冲击力需求？（强调数据 vs 强调逻辑）

## 选择原则
1. **数据优先**：数据点数量决定基本布局
2. **语义增强**：根据内容关系选择具体图表类型
3. **视觉协调**：考虑与整体PPT风格的一致性
4. **可读性**：避免过度复杂的可视化

## 输出格式
```json
{{
  "layout": "DASHBOARD|BIG_NUMBER|COMPARISON|TIMELINE|PYRAMID|PIE_CHART|RADAR_CHART|TABLE|PROCESS_FLOW|ACTION_PLAN",
  "chart_type": "具体的图表子类型（如 kpi_cards、progress_rings、donut_chart 等）",
  "confidence": 0.85,
  "reason": "选择理由（中文，一句话说明为什么这个布局最适合，不超过20字）",
  "visual_elements": ["建议的视觉元素，如进度环、图标、箭头等"],
  "color_suggestion": "主色调建议（warm橙红色/cool蓝绿色/highlight高亮对比）",
  "data_preprocessing": {{
    "hero_metric": "最核心的指标（如果有）",
    "sort_order": "排序方式（asc/desc/none）"
  }}
}}
```

只输出 JSON，不要其他文字。
"""


class SmartLayoutMatcher:
    """LLM-based intelligent layout and chart matcher."""
    
    def __init__(self, model: str = None):
        """Initialize matcher.
        
        Args:
            model: LLM model name (e.g., "glm-4-flash")
        """
        if not HAS_LLM:
            raise RuntimeError("llm_adapter not available")
        
        self.llm = LLMAdapter(model=model)
        self.cache = {}  # Cache results for identical inputs
    
    def _analyze_data_characteristics(self, data_points: List[Dict]) -> Dict:
        """Analyze data point characteristics."""
        if not data_points:
            return {
                "data_count": 0,
                "data_types": [],
                "value_ranges": [],
                "unit_types": []
            }
        
        data_types = []
        value_ranges = []
        unit_types = []
        
        for dp in data_points:
            value = str(dp.get('value', ''))
            unit = str(dp.get('unit', ''))
            
            # Determine data type
            if '%' in unit:
                data_types.append('percentage')
            elif unit in ['亿', '万', '元']:
                data_types.append('currency')
            elif unit in ['家', '人', '个', '名']:
                data_types.append('count')
            elif unit in ['年', '月', '日']:
                data_types.append('time')
            else:
                data_types.append('other')
            
            # Determine value range
            try:
                num = float(value.replace('+', '').replace(',', ''))
                if num > 100:
                    value_ranges.append('large')
                elif num > 10:
                    value_ranges.append('medium')
                else:
                    value_ranges.append('small')
            except:
                value_ranges.append('text')
            
            unit_types.append(unit)
        
        return {
            "data_count": len(data_points),
            "data_types": list(set(data_types)),
            "value_ranges": list(set(value_ranges)),
            "unit_types": list(set(unit_types))
        }
    
    def _analyze_content_semantics(self, slide_data: Dict) -> Dict:
        """Analyze content semantic relationships with improved accuracy."""
        title = slide_data.get('title', '').lower()
        key_points = slide_data.get('key_points', [])
        content_detail = slide_data.get('content_detail', '').lower()
        data_points = slide_data.get('data_points', [])
        
        all_text = f"{title} {' '.join(key_points)} {content_detail}".lower()
        
        # Detect comparison - need explicit comparison pattern
        has_comparison = False
        comparison_patterns = [
            'vs', '对比', '比较', '优于', '劣于',
            '传统', '创新', '新旧', '前后', '改进后',
            '方案a', '方案b', '选项a', '选项b',
            '之前', '之后', '变革前', '变革后'
        ]
        # Also check if data points suggest comparison (exactly 2 groups)
        if len(data_points) == 2:
            labels = [dp.get('label', '').lower() for dp in data_points]
            # Check if labels suggest comparison
            if any(p in ' '.join(labels) for p in ['vs', '对比', '传统', '旧', '前']):
                has_comparison = True
        if not has_comparison:
            has_comparison = any(p in all_text for p in comparison_patterns)
        
        # Detect timeline - check for year patterns
        has_timeline = False
        import re
        year_pattern = r'(20[0-9]{2}|19[0-9]{2})'
        years = re.findall(year_pattern, all_text)
        timeline_keywords = ['历程', '发展', '时间', '阶段', '里程碑', '演进', '历史']
        if len(years) >= 2 or any(kw in all_text for kw in timeline_keywords):
            has_timeline = True
        
        # Detect hierarchy - priority/level indicators
        has_hierarchy = any(kw in all_text for kw in [
            '层级', '优先', '顶层', '底层', '金字塔',
            '战略', '战术', '执行', '一级', '二级',
            '核心层', '支撑层', '基础层'
        ])
        
        # Detect parallel - non-sequential items
        has_parallel = any(kw in all_text for kw in [
            '并列', '同时', '分别', '各自', '同等', '平行'
        ])
        
        # Detect percentage/constituency
        has_percentage = any(kw in all_text for kw in [
            '占比', '百分比', '构成', '比例', '份额', '分布'
        ])
        
        return {
            "has_comparison": has_comparison,
            "has_timeline": has_timeline,
            "has_hierarchy": has_hierarchy,
            "has_parallel": has_parallel,
            "has_percentage": has_percentage
        }
    
    async def match(self, slide_data: Dict) -> LayoutMatch:
        """Match the best layout for slide data.
        
        Args:
            slide_data: Slide data including title, content, data_points
        
        Returns:
            LayoutMatch with layout, chart_type, reason, etc.
        """
        data_points = slide_data.get('data_points', [])
        
        # Quick return for empty data
        if not data_points:
            return LayoutMatch(
                layout='CONTENT',
                chart_type='bullet_points',
                confidence=1.0,
                reason='无数据点，使用纯内容布局',
                visual_elements=['bullet_points'],
                color_suggestion='neutral',
                data_preprocessing={}
            )
        
        # Analyze characteristics
        data_chars = self._analyze_data_characteristics(data_points)
        content_semantics = self._analyze_content_semantics(slide_data)
        
        # Format layout catalog
        catalog_text = "\n".join([
            f"- **{k}**: {v['name']} - {v['best_for']}"
            for k, v in LAYOUT_CATALOG.items()
        ])
        
        # Build prompt
        prompt = MATCH_PROMPT.format(
            slide_json=json.dumps(slide_data, ensure_ascii=False, indent=2),
            layout_catalog=catalog_text,
            data_count=data_chars['data_count'],
            data_types=', '.join(data_chars['data_types']),
            value_ranges=', '.join(data_chars['value_ranges']),
            unit_types=', '.join(data_chars['unit_types'])
        )
        
        # Add semantic hints
        semantic_hints = []
        if content_semantics['has_comparison']:
            semantic_hints.append("检测到对比关系，考虑 COMPARISON 布局")
        if content_semantics['has_timeline']:
            semantic_hints.append("检测到时间序列，考虑 TIMELINE 布局")
        if content_semantics['has_hierarchy']:
            semantic_hints.append("检测到层级关系，考虑 PYRAMID 布局")
        if content_semantics['has_percentage']:
            semantic_hints.append("检测到占比关系，考虑 PIE_CHART 布局")
        
        if semantic_hints:
            prompt += f"\n\n## 语义提示\n" + "\n".join(semantic_hints)
        
        # Call LLM
        try:
            response = await self.llm.generate(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.3
            )
            
            content = response.get('content', '')
            
            # Extract JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
                
                return LayoutMatch(
                    layout=result.get('layout', 'DASHBOARD'),
                    chart_type=result.get('chart_type', 'kpi_cards'),
                    confidence=result.get('confidence', 0.8),
                    reason=result.get('reason', 'LLM智能匹配'),
                    visual_elements=result.get('visual_elements', []),
                    color_suggestion=result.get('color_suggestion', 'neutral'),
                    data_preprocessing=result.get('data_preprocessing', {})
                )
        
        except Exception as e:
            print(f"LLM match failed: {e}")
            # Return default layout (no rule-based fallback)
            return LayoutMatch(
                layout='CONTENT',
                chart_type='bullet_points',
                confidence=0.5,
                reason=f'LLM调用失败，使用默认布局',
                visual_elements=['bullet_points'],
                color_suggestion='neutral',
                data_preprocessing={}
            )
        
        # Should not reach here, but return default if it does
        return LayoutMatch(
            layout='CONTENT',
            chart_type='bullet_points',
            confidence=0.3,
            reason='未匹配到布局',
            visual_elements=['bullet_points'],
            color_suggestion='neutral',
            data_preprocessing={}
        )


async def main():
    """Test the smart matcher."""
    matcher = SmartLayoutMatcher()
    
    # Test case 1: Dashboard
    slide1 = {
        "title": "业务增长数据",
        "data_points": [
            {"label": "营收", "value": "3", "unit": "亿"},
            {"label": "增长率", "value": "45", "unit": "%"},
            {"label": "客户数", "value": "100", "unit": "家"}
        ]
    }
    
    result1 = await matcher.match(slide1)
    print(f"Test 1: {result1.layout} - {result1.reason}")
    
    # Test case 2: Comparison
    slide2 = {
        "title": "传统方案 vs 创新方案",
        "data_points": [
            {"label": "传统准确率", "value": "60", "unit": "%"},
            {"label": "创新准确率", "value": "95", "unit": "%"}
        ],
        "key_points": ["传统方案准确率低", "创新方案大幅提升"]
    }
    
    result2 = await matcher.match(slide2)
    print(f"Test 2: {result2.layout} - {result2.reason}")
    
    # Test case 3: Timeline
    slide3 = {
        "title": "发展历程",
        "data_points": [
            {"label": "2020年", "value": "成立", "unit": ""},
            {"label": "2022年", "value": "A轮", "unit": ""},
            {"label": "2024年", "value": "B轮", "unit": ""}
        ]
    }
    
    result3 = await matcher.match(slide3)
    print(f"Test 3: {result3.layout} - {result3.reason}")


if __name__ == "__main__":
    asyncio.run(main())
