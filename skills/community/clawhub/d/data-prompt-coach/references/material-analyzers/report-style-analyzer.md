# Report Style Analyzer — 历史报告风格分析器

> 适用于：data-prompt-coach 引导入口 L2+ 资料感知
> 角色：用户提交历史报告样例后，分析结构/风格/信息密度并回填 5 要素

## 触发条件

用户在引导入口提交历史报告（Markdown/HTML/PDF/Word），且场景属于：
- 场景 6（周报敏捷分析）— 用户提供上周报告
- 场景 7（深度洞察报告）— 用户提供报告示例

## 分析流程

### Step 1: 报告结构识别

```yaml
report_structure:
  type: "weekly_report"  # weekly_report / deep_report / dashboard
  sections:
    - title: "执行摘要"
      position: "顶部"
      length: "short"  # short / medium / long
      purpose: "一句话概括本周重点"
    - title: "核心指标"
      position: "顶部-中部"
      length: "medium"
      purpose: "关键 KPI 数据 + 同比环比"
    - title: "趋势分析"
      position: "中部"
      length: "long"
      purpose: "趋势图 + 解读"
    - title: "异常预警"
      position: "中部-底部"
      length: "medium"
      purpose: "异常指标 + 原因分析"
    - title: "下周计划"
      position: "底部"
      length: "short"
      purpose: "基于本周数据的下周行动"
```

### Step 2: 风格分析

```yaml
style_analysis:
  tone: "professional"  # professional / casual / technical / executive
  voice: "third_person"  # first_person / third_person / passive
  sentence_length: "medium"  # short / medium / long
  jargon_level: "medium"  # low / medium / high
  data_presentation: "chart_heavy"  # text_heavy / chart_heavy / balanced
  audience: "executive"  # executive / operational / technical
```

### Step 3: 信息密度评估

```yaml
information_density:
  total_length: 2500  # 字数
  data_points: 15  # 数据点数
  charts: 3
  tables: 2
  density_score: 0.6  # 0-1，越高越密
  density_level: "medium"  # low / medium / high
  key_metrics:
    - "GMV"
    - "订单量"
    - "转化率"
    - "客单价"
    - "复购率"
```

### Step 4: 数据源识别

```yaml
data_sources:
  - type: "excel"
    files: 3
    description: "订单数据 + 用户数据 + 流量数据"
  - type: "database"
    tables: ["orders", "users", "traffic_log"]
    description: "MySQL 主库"
  - type: "api"
    endpoints: 2
    description: "第三方支付 + 物流查询"
```

### Step 5: 周期性对比模式识别（仅周报）

```yaml
comparison_patterns:
  - type: "week_over_week"
    metrics: ["GMV", "订单量", "转化率"]
    style: "百分比变化 + 趋势箭头"
  - type: "month_over_month"
    metrics: ["GMV", "客单价"]
    style: "百分比变化"
  - type: "year_over_year"
    metrics: ["GMV"]
    style: "百分比变化"
```

### Step 6: 回填 5 要素

```yaml
scope: "✅ 已知报告类型：{type}，长度 {N} 字"
fields:
  - "✅ 报告结构已识别：{K} 个章节"
  - "✅ 关键指标已识别：{M} 个"
  - "✅ 数据源已识别"
processing_rules:
  - "✅ 风格已识别：{tone}/{voice}"
  - "✅ 信息密度：{level}"
  - "⚠️ 时间范围需确认（如本周 vs 近 7 天）"
output_format: "✅ 建议沿用历史格式（{format}）"
exception_handling:
  - "⚠️ 异常预警规则未定义"
  - "⚠️ 数据缺失处理规则未定义"
```

## 回填后访谈策略

| 要素 | 资料分析前 | 资料分析后 | 第 1 轮访谈重点 |
|------|----------|----------|---------------|
| 范围 | ❓ | ✅ 已知报告类型 | 跳过 |
| 字段 | ❓ | ✅ 结构+指标已识别 | 问本期是否新增/调整指标 |
| 处理规则 | ❓ | ✅ 风格已识别，⚠️时间范围 | 问时间范围 + 对比周期 |
| 输出格式 | ❓ | ✅ 建议沿用历史格式 | 确认是否沿用 |
| 异常处理 | ❓ | ⚠️ 异常预警规则 | 问异常预警 + 缺失处理 |

**3 轮访谈维度划分**：
- 第 1 轮：指标调整（本期是否新增/删除/调整指标）
- 第 2 轮：时间范围 + 对比周期 + 数据源更新
- 第 3 轮：异常预警规则 + 输出格式确认

## 报告类型专属关注点

### 周报专属

- **周期对比**：周同比、月同比、年同比必须明确
- **执行摘要**：3 句话概括本周重点
- **异常预警**：哪些指标变化超过阈值需要预警
- **下周计划**：基于本周数据的可执行行动

### 深度报告专属

- **分析目标**：报告要回答什么核心问题
- **数据规模**：数据量决定是否需要 M11 大文件阈值
- **章节深度**：每章多深，是否有附录
- **图表风格**：建议使用目标导向（M8），多给目标少给绘图指令

## 与 SKILL.md 的接口

**入口点**：本文件"分析流程"段落
**出口点**：本文件"回填后访谈策略"末尾
**调用方**：SKILL.md Step A2 资料感知访谈
**依赖**：用户提交的历史报告
**联动**：M8 目标导向 + M9 分步提问（深度报告场景）
