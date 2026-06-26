#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: LOCAL-ONLY. No network requests, no credential access, no remote code execution.

"""
PPT布局模板库 - 提供多种专业布局参考

此文件包含 12+ 种常用的PPT布局模式，用于指导LLM生成更丰富多样的幻灯片设计。
"""

# 布局库提示词 - 用于注入到 DESIGN_PLAN_PROMPT 中
LAYOUT_LIBRARY_PROMPT = """
## 📚 布局模板库（请根据内容类型选择最合适的布局）

### 1️⃣ 仪表盘布局 (Dashboard)
**适用场景**: KPI展示、数据监控、绩效报告
**布局特点**:
- 多区块分区，每个区块展示不同指标
- 使用环形进度条、数字指标卡片
- 可包含折线图、柱状图（用SVG绘制）
**HTML结构示例**:
```
┌─────────────────────────────────────────┐
│  标题区域                                │
├─────────┬─────────┬─────────┬─────────┤
│ 指标卡1 │ 指标卡2 │ 指标卡3 │ 指标卡4 │
│ ●95%   │ $12.5M │ +23%   │ 500+   │
├─────────┴─────────┼─────────┴─────────┤
│ 图表区域（折线图） │ 数据列表/详情     │
└───────────────────┴───────────────────┘
```
**关键CSS**: `display: grid; grid-template-columns: repeat(4, 1fr);`
**SVG进度环示例**:
```html
<svg width="80" height="80" viewBox="0 0 80 80">
  <circle cx="40" cy="40" r="35" fill="none" stroke="#e2e8f0" stroke-width="6"/>
  <circle cx="40" cy="40" r="35" fill="none" stroke="#0022AB" stroke-width="6" 
          stroke-dasharray="220" stroke-dashoffset="22" transform="rotate(-90 40 40)"/>
  <text x="40" y="45" text-anchor="middle" font-size="18" fill="#0022AB" font-weight="bold">95%</text>
</svg>
```

---

### 2️⃣ 时间轴布局 (Timeline)
**适用场景**: 项目规划、发展历程、里程碑展示
**布局特点**:
- 水平或垂直时间线
- 带编号节点（01, 02, 03...）
- 每个节点下方有标题和描述
**HTML结构示例**:
```
水平时间轴:
     ●━━━━━━━━━●━━━━━━━━━●━━━━━━━━━●
    [01]      [02]      [03]      [04]
   准备期     试点期     扩张期     成熟期
   3-9月     9-21月    21-45月      ...
```
**关键CSS**: 使用贯穿线 + flex布局均匀分布节点
**节点样式**: `width: 50px; height: 50px; border-radius: 50%; background: #0022AB;`

---

### 3️⃣ 流程图布局 (Flow Chart / Hub & Spoke)
**适用场景**: 供应链、业务流程、系统架构
**布局特点**:
- 带箭头/连接线的流程节点
- 中心+辐射或线性流程
- 可使用图标代表不同步骤
**HTML结构示例**:
```
Hub & Spoke:
              ┌─────┐
              │中心仓│
              └──┬──┘
         ┌──────┼──────┐
         ▼      ▼      ▼
      [门店A] [门店B] [门店C]

线性流程:
[采购] ─────► [仓储] ─────► [配送] ─────► [门店]
```
**连接箭头SVG**:
```html
<svg width="40" height="24" viewBox="0 0 40 24">
  <path d="M0 12 L30 12 M24 6 L30 12 L24 18" stroke="#0022AB" stroke-width="2" fill="none"/>
</svg>
```

---

### 4️⃣ 对比分析布局 (Comparison / VS)
**适用场景**: 竞品分析、方案对比、优劣对照
**布局特点**:
- 左右两栏明确对比
- 中间可有VS标记或对比指标
- 使用不同颜色区分两侧
**HTML结构示例**:
```
┌─────────────────┬─────────────────┐
│  方案A (蓝色)   │  方案B (金色)   │
├─────────────────┼─────────────────┤
│ ✓ 优势1        │ ✓ 优势1        │
│ ✓ 优势2        │ ✓ 优势2        │
│ ✗ 劣势1        │ ✗ 劣势1        │
└─────────────────┴─────────────────┘
```
**配色建议**: 左侧用品牌主色，右侧用辅助色

---

### 5️⃣ SWOT/四象限布局 (Quadrant)
**适用场景**: SWOT分析、矩阵图、分类展示
**布局特点**:
- 2x2网格，每个象限独立
- 每个象限有自己的标题和颜色
- 中心可有分隔线或总结
**HTML结构示例**:
```
┌─────────────────┬─────────────────┐
│ S (优势)        │ W (劣势)        │
│ 绿色背景        │ 红色背景        │
├─────────────────┼─────────────────┤
│ O (机遇)        │ T (威胁)        │
│ 蓝色背景        │ 橙色背景        │
└─────────────────┴─────────────────┘
```
**关键CSS**: `display: grid; grid-template-columns: 1fr 1fr; gap: 20px;`

---

### 6️⃣ 数据卡片布局 (Stat Cards)
**适用场景**: 关键数据展示、业绩概览
**布局特点**:
- 3-4个独立卡片横向排列
- 每个卡片突出一个核心数字
- 卡片内有图标、数值、描述
**HTML结构示例**:
```
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ 🏪 200  │  │ 💰 13亿 │  │ 📈 18%  │  │ 👥 100万│
│ 门店总数 │  │ 年营收  │  │ 增长率  │  │ 用户数  │
└─────────┘  └─────────┘  └─────────┘  └─────────┘
```
**卡片样式**: 圆角、阴影、左侧装饰条

---

### 7️⃣ 分步流程布局 (Stepped Process)
**适用场景**: 操作指南、实施步骤、方法论
**布局特点**:
- 编号步骤（Step 1, Step 2...）
- 垂直或水平排列
- 每一步有标题+详情
**HTML结构示例**:
```
[ 01 ]────────────────────────────────
  第一步标题
  详细描述内容...

[ 02 ]────────────────────────────────
  第二步标题
  详细描述内容...
```

---

### 8️⃣ 图文混排布局 (Image + Text)
**适用场景**: 产品介绍、案例展示
**布局特点**:
- 左图右文或右图左文
- 图片区域约40%，文字区域约60%
- 文字区有标题+要点列表
**HTML结构示例**:
```
┌───────────────┬─────────────────────┐
│               │ 产品标题            │
│   [产品图]    │ ────────            │
│               │ • 特点1             │
│               │ • 特点2             │
│               │ • 特点3             │
└───────────────┴─────────────────────┘
```

---

### 9️⃣ 金字塔/层级布局 (Pyramid / Hierarchy)
**适用场景**: 组织架构、优先级展示、分层概念
**布局特点**:
- 上窄下宽或反向
- 每层有不同颜色
- 层级关系清晰
**HTML结构示例**:
```
           ┌─────────┐
           │  战略   │
         ┌─┴─────────┴─┐
         │   战术      │
       ┌─┴─────────────┴─┐
       │     执行        │
     ┌─┴─────────────────┴─┐
     │       运营          │
```

---

### 🔟 Action Plan / 行动计划布局
**适用场景**: 下一步行动、待办事项、优先级任务
**布局特点**:
- 深色背景突出"行动"
- 3-4个并列的行动卡片
- 可带时间/负责人标签
**HTML结构示例**:
```
┌──────────────────────────────────────┐ 深色通栏
│ 🎯 下一步行动 (Next 30 Days)         │
├──────────┬──────────┬──────────────┤
│ 1.任务A  │ 2.任务B  │ 3.任务C     │
│ 描述...  │ 描述...  │ 描述...     │
│ 时间:X   │ 时间:Y  │ 时间:Z      │
└──────────┴──────────┴──────────────┘
```

---

### 1️⃣1️⃣ 摘要总结布局 (Executive Summary)
**适用场景**: 核心结论、执行摘要、一页纸汇报
**布局特点**:
- 左侧大标题"核心结论"
- 右侧2-3个要点模块
- 使用图标+高亮关键词
**HTML结构示例**:
```
┌─────────────────┬─────────────────────────┐
│                 │ 📈 要点一               │
│  核心结论       │ 关键数据高亮...         │
│  EXECUTIVE      ├─────────────────────────┤
│  SUMMARY        │ 🎯 要点二               │
│                 │ 关键结论高亮...         │
└─────────────────┴─────────────────────────┘
```

---

### 1️⃣2️⃣ 列表+详情布局 (List + Detail)
**适用场景**: 产品功能、服务清单、技术规格
**布局特点**:
- 左侧带图标的列表项
- 右侧每项的详细说明
- 或垂直堆叠的列表卡片
**HTML结构示例**:
```
┌─────────────────────────────────────────┐
│ ⚙️ 功能一                               │
│    详细描述内容...                       │
├─────────────────────────────────────────┤
│ 🔧 功能二                               │
│    详细描述内容...                       │
├─────────────────────────────────────────┤
│ 📊 功能三                               │
│    详细描述内容...                       │
└─────────────────────────────────────────┘
```

---

### 1️⃣3️⃣ 环形/辐射布局 (Radial / Circular)
**适用场景**: 核心概念+周边元素、生态系统
**布局特点**:
- 中心一个核心概念
- 周围环绕相关元素
- 使用SVG绘制连接线
**HTML结构示例**:
```
           [元素1]
              │
    [元素4]───●───[元素2]
              │
           [元素3]
```

---

### 1️⃣4️⃣ 报价/定价卡片布局 (Pricing Cards)
**适用场景**: 产品定价、套餐对比、服务等级
**布局特点**:
- 3-4个并列卡片
- 中间卡片可突出显示（推荐）
- 每个卡片有价格+功能列表

---

### 1️⃣5️⃣ 封面布局变体 (Cover Variants)
**适用场景**: PPT首页、章节分隔页
**布局变体**:
- A. 全屏图片+居中大标题
- B. 左半图片+右半文字
- C. 上部图片+下部标题卡片
- D. 纯色背景+几何装饰+标题

### 1️⃣6️⃣ 大数字/金句布局 (Big Number / Quote)
**适用场景**: **核心数据强调**、震撼结论、名言引用
**布局特点**:
- 页面中心只有一个巨大的数字（如 "99%"）或一句引言
- 字体极大（80px+），字重极粗
- 极简背景，无干扰元素
**HTML结构**: Flex center，超大 font-size

---

### 1️⃣7️⃣ 数据图表布局 (Chart)
**适用场景**: **市场份额、增长趋势、统计数据**
**布局特点**:
- 使用 CSS/HTML 模拟的条形图或进度条
- 或者左侧数据列表，右侧可视化图形
- **必须用于展示 Markdown 中的表格数据**
**HTML结构**:
- 柱状图：底部对齐的 Flex 容器，不同高度的 div
- 进度条：带背景色的圆角 div

---

### 1️⃣8️⃣ 表格布局 (Table)
**适用场景**: 详细参数对比、财务报表
**布局特点**:
- 专业的表格样式
- 斑马纹背景
- 突出的表头
**HTML结构**: 标准 HTML `<table>`，带 border-collapse

---

## 💡 布局选择指南

| 内容特征 | 推荐 Content Mode | 推荐 Layout |
| :--- | :--- | :--- |
| **封面/章节起始** | `title` | `15. Cover Variants` |
| **仅仅是罗列几个点/功能** | `list` | `12. List + Detail`, `6. Stat Cards` |
| **讲一个完整的故事/产品/案例** | `paragraph` | `8. Image + Text`, `13. Radial` |
| **只有一个震撼的数据/金句** | `data` | `16. Big Number` |
| **多个关键指标监控 (KPI)** | `data` / `mixed` | `1. Dashboard`, `6. Stat Cards` |
| **数据趋势/占比/统计** | `data` | `17. Chart` |
| **详细数据/财务报表** | `data` | `18. Table` |
| **时间/历史/里程碑** | `list` | `2. Timeline` |
| **步骤/操作流程** | `list` | `7. Stepped Process`, `3. Flow Chart` |
| **A vs B / 优劣对比** | `list` | `4. Comparison` |
| **四象限分析 (SWOT)** | `list` | `5. SWOT / Quadrant` |
| **层级/组织架构** | `list` | `9. Pyramid` |
| **下一步行动/计划** | `list` | `10. Action Plan` |
| **核心结论/摘要** | `mixed` | `11. Executive Summary` |
| **产品定价/套餐** | `list` | `14. Pricing Cards` |
| **趋势/体量感** | `data` | `19. Area Chart` (面积图) |
| **排名/分类对比** | `data` | `20. Horizontal Bar Chart` (水平条形图) |
| **转化率/漏斗** | `data` | `21. Funnel Chart` (漏斗图) |
| **多维占比拆分** | `data` | `22. Stacked Bar Chart` (堆叠柱状图) |
| **双Y轴/组合指标** | `data` | `23. Combo Chart` (组合图) |
| **KPI+图表混合** | `mixed` | `24. Card + Chart Mix` |
| **章节过渡** | `title` | `25. Banner Transition` |
"""

# 布局去重逻辑
ALL_LAYOUTS = [
    "COVER", "DASHBOARD", "BIG_NUMBER", "COMPARISON", "PYRAMID",
    "CARD", "ACTION_PLAN", "CONTENT", "SUMMARY", "PIE_CHART",
    "RADAR_CHART", "TABLE", "GAUGE", "AREA_CHART", "H_BAR_CHART",
    "FUNNEL", "STACKED_BAR", "COMBO_CHART", "CARD_CHART_MIX", "BANNER_TRANSITION"
]

# 每种布局的视觉差异类别（用于智能去重 - 连续页面选择不同类别）
LAYOUT_CATEGORIES = {
    "COVER": "title",
    "DASHBOARD": "data_dense",
    "BIG_NUMBER": "data_highlight",
    "COMPARISON": "split",
    "PYRAMID": "visual",
    "CARD": "list",
    "ACTION_PLAN": "process",
    "CONTENT": "text",
    "SUMMARY": "text",
    "PIE_CHART": "chart",
    "RADAR_CHART": "chart",
    "TABLE": "data_dense",
    "GAUGE": "chart",
    "AREA_CHART": "chart",
    "H_BAR_CHART": "chart",
    "FUNNEL": "visual",
    "STACKED_BAR": "chart",
    "COMBO_CHART": "chart",
    "CARD_CHART_MIX": "mixed",
    "BANNER_TRANSITION": "title",
}


def dedup_layout(suggested: str, prev_layouts: list, max_history: int = 3) -> str:
    """确保布局与最近几页不重复。
    
    Args:
        suggested: 原始建议布局
        prev_layouts: 之前页面使用的布局列表（从旧到新）
        max_history: 检查最近几页
    
    Returns:
        去重后的布局名
    """
    if not prev_layouts:
        return suggested
    
    recent = prev_layouts[-max_history:]
    prev_categories = [LAYOUT_CATEGORIES.get(l, "unknown") for l in recent]
    
    # 如果建议的布局与最近页面重复或同类，找一个不同类别的
    suggested_cat = LAYOUT_CATEGORIES.get(suggested, "unknown")
    
    if suggested in recent:
        # 完全重复 → 找一个视觉差异最大的
        candidates = []
        for layout in ALL_LAYOUTS:
            if layout in recent:
                continue
            cat = LAYOUT_CATEGORIES.get(layout, "unknown")
            if cat != suggested_cat:
                candidates.append((layout, cat))
        
        if candidates:
            # 优先选不同类别
            return candidates[0][0]
        else:
            # 所有类别都用过了，选不在最近3页的
            for layout in ALL_LAYOUTS:
                if layout not in recent:
                    return layout
            return suggested
    
    if suggested_cat in prev_categories:
        # 同类别重复 → 找不同类别的
        candidates = []
        for layout in ALL_LAYOUTS:
            cat = LAYOUT_CATEGORIES.get(layout, "unknown")
            if cat not in prev_categories and layout not in recent:
                candidates.append(layout)
        
        if candidates:
            return candidates[0]
        # 没有完全不同类别的，接受建议
    
    return suggested


def get_layout_suggestion_map() -> dict:
    """获取内容类型到推荐布局的映射。
    
    Returns:
        dict: content_type -> [layout_list]
    """
    return {
        "title": ["COVER", "BANNER_TRANSITION", "BIG_NUMBER"],
        "data": ["DASHBOARD", "CARD_CHART_MIX", "BIG_NUMBER", "H_BAR_CHART", "AREA_CHART", "FUNNEL", "TABLE", "COMBO_CHART", "PIE_CHART", "RADAR_CHART", "GAUGE", "STACKED_BAR"],
        "data_dense": ["TABLE", "DASHBOARD", "H_BAR_CHART"],
        "list": ["CARD", "ACTION_PLAN", "COMPARISON", "PYRAMID", "CONTENT"],
        "text": ["CONTENT", "SUMMARY", "CARD"],
        "mixed": ["CARD_CHART_MIX", "DASHBOARD", "COMPARISON"],
        "process": ["ACTION_PLAN", "FUNNEL"],
        "chart": ["AREA_CHART", "H_BAR_CHART", "PIE_CHART", "RADAR_CHART", "GAUGE", "STACKED_BAR", "COMBO_CHART"],
        "visual": ["PYRAMID", "FUNNEL", "RADAR_CHART", "BIG_NUMBER"],
        "split": ["COMPARISON", "CARD_CHART_MIX"],
        "data_highlight": ["BIG_NUMBER", "GAUGE", "DASHBOARD"],
        "title": ["COVER", "BANNER_TRANSITION"],
    }

# SVG组件库 - 常用的可视化元素
SVG_COMPONENTS = """
## 🎨 SVG可视化组件库

### 环形进度条
```html
<svg width="100" height="100" viewBox="0 0 100 100">
  <!-- 背景圆环 -->
  <circle cx="50" cy="50" r="40" fill="none" stroke="#e2e8f0" stroke-width="8"/>
  <!-- 进度圆环 (stroke-dasharray=2πr≈251, stroke-dashoffset控制进度) -->
  <circle cx="50" cy="50" r="40" fill="none" stroke="#0022AB" stroke-width="8" 
          stroke-dasharray="251" stroke-dashoffset="25" transform="rotate(-90 50 50)"
          stroke-linecap="round"/>
  <!-- 中心文字 -->
  <text x="50" y="55" text-anchor="middle" font-size="24" fill="#0022AB" font-weight="bold">90%</text>
</svg>
```

### 半圆仪表盘
```html
<svg width="160" height="90" viewBox="0 0 160 90">
  <!-- 背景弧 -->
  <path d="M 10 80 A 70 70 0 0 1 150 80" fill="none" stroke="#e2e8f0" stroke-width="12" stroke-linecap="round"/>
  <!-- 进度弧 (根据百分比调整终点坐标) -->
  <path d="M 10 80 A 70 70 0 0 1 130 30" fill="none" stroke="#22c55e" stroke-width="12" stroke-linecap="round"/>
  <!-- 数值 -->
  <text x="80" y="75" text-anchor="middle" font-size="28" fill="#1e293b" font-weight="bold">85%</text>
</svg>
```

### 简易柱状图
```html
<svg width="200" height="120" viewBox="0 0 200 120">
  <!-- Y轴参考线 -->
  <line x1="30" y1="10" x2="30" y2="100" stroke="#e2e8f0" stroke-width="1"/>
  <line x1="30" y1="100" x2="190" y2="100" stroke="#e2e8f0" stroke-width="1"/>
  <!-- 柱子 -->
  <rect x="50" y="60" width="25" height="40" fill="#0022AB" rx="2"/>
  <rect x="90" y="40" width="25" height="60" fill="#0022AB" rx="2"/>
  <rect x="130" y="20" width="25" height="80" fill="#0022AB" rx="2"/>
  <!-- 标签 -->
  <text x="62" y="115" text-anchor="middle" font-size="10" fill="#64748b">Q1</text>
  <text x="102" y="115" text-anchor="middle" font-size="10" fill="#64748b">Q2</text>
  <text x="142" y="115" text-anchor="middle" font-size="10" fill="#64748b">Q3</text>
</svg>
```

### 简易折线图
```html
<svg width="200" height="100" viewBox="0 0 200 100">
  <!-- 网格线 -->
  <line x1="20" y1="80" x2="180" y2="80" stroke="#e2e8f0" stroke-width="1"/>
  <!-- 折线 -->
  <polyline points="30,70 70,50 110,60 150,30 180,20" fill="none" stroke="#0022AB" stroke-width="2"/>
  <!-- 数据点 -->
  <circle cx="30" cy="70" r="4" fill="#0022AB"/>
  <circle cx="70" cy="50" r="4" fill="#0022AB"/>
  <circle cx="110" cy="60" r="4" fill="#0022AB"/>
  <circle cx="150" cy="30" r="4" fill="#0022AB"/>
  <circle cx="180" cy="20" r="4" fill="#0022AB"/>
</svg>
```

### 连接箭头（水平）
```html
<svg width="60" height="24" viewBox="0 0 60 24">
  <line x1="0" y1="12" x2="50" y2="12" stroke="#0022AB" stroke-width="2"/>
  <polygon points="50,6 60,12 50,18" fill="#0022AB"/>
</svg>
```

### 连接箭头（垂直）
```html
<svg width="24" height="60" viewBox="0 0 24 60">
  <line x1="12" y1="0" x2="12" y2="50" stroke="#0022AB" stroke-width="2"/>
  <polygon points="6,50 12,60 18,50" fill="#0022AB"/>
</svg>
```

### 时间轴节点
```html
<div style="display: flex; align-items: center; width: 100%;">
  <!-- 节点 -->
  <div style="width: 50px; height: 50px; border-radius: 50%; background: #0022AB; 
              display: flex; align-items: center; justify-content: center;
              color: white; font-weight: bold; font-size: 18px; flex-shrink: 0;">01</div>
  <!-- 连接线 -->
  <div style="flex: 1; height: 3px; background: #0022AB;"></div>
</div>
```
"""
