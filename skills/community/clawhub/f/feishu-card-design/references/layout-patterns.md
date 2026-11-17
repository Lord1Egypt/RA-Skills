# 飞书卡片布局模式

> **版本**：1.0.4 | **本文件作用**：定义 4 段式标准布局 + 多列布局 + 特殊场景布局
> **设计目标**：让卡片信息密度合理、视觉层次清晰、行动闭环完整

---

## 1. 4 段式标准布局

### 1.1 标准结构

```
┌────────────────────────────────────┐
│  Header（title + subtitle + 色）  │  ← 1. 类型识别
├────────────────────────────────────┤
│  Body Element 1: 主推块            │  ← 2. 核心信息
│  ─── hr ───                        │
│  Body Element 2: 亮点块            │  ← 3. Aha 时刻
│  ─── hr ───                        │
│  Body Element 3: 统计块            │  ← 4. 数据支撑
│  ─── hr ───                        │
│  Body Element 4: 行动按钮          │  ← 5. 下一步
│  Footer: note 说明                 │  ← 6. 来源/版本
└────────────────────────────────────┘
```

### 1.2 段落省略规则

| 段落 | 必填？ | 省略条件 |
|------|--------|---------|
| Header | ✅ 必填 | 永不省略 |
| 主推块 | ✅ 必填 | 永不省略（至少 1 个） |
| 亮点块 | ⚠️ 可选 | 简单通知可省略 |
| 统计块 | ⚠️ 可选 | 无数据时省略 |
| 行动按钮 | ⚠️ 可选 | 仅展示类卡片可省略 |
| Footer note | ✅ 必填 | 永不省略（来源标识） |

### 1.3 标准布局 JSON

```json
{
  "schema": "2.0",
  "config": {"wide_screen_mode": true, "update_multi": true},
  "header": {
    "title": {"tag": "plain_text", "content": "20260719-增量日报-..."},
    "subtitle": {"tag": "plain_text", "content": "2026-07-19 · 发现 + 洞察 + 反思"},
    "template": "blue"
  },
  "body": {
    "direction": "vertical",
    "padding": "16px 16px 16px 16px",
    "elements": [
      {/* 主推块 - blue-50 */},
      {"tag": "hr"},
      {/* 亮点块 - yellow-50 */},
      {"tag": "hr"},
      {/* 统计块 - grey-50 */},
      {"tag": "hr"},
      {/* 行动按钮 */},
      {/* footer note */}
    ]
  }
}
```

---

## 2. 主推块模式

### 2.1 单列主推块（最常用）

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "blue-50",
  "padding": "10px 12px",
  "columns": [{
    "tag": "column",
    "width": "weighted",
    "weight": 1,
    "vertical_align": "top",
    "background_style": "blue-50",
    "elements": [
      {"tag": "markdown", "content": "### 🌟 核心洞察\n\n本日最重要发现..."}
    ]
  }]
}
```

### 2.2 双列对比主推块

适合"问题 vs 解决方案"、"旧 vs 新"对比：

```json
{
  "tag": "column_set",
  "flex_mode": "bisect",
  "background_style": "blue-50",
  "columns": [
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "background_style": "blue-50",
      "elements": [{"tag": "markdown", "content": "### ❌ 旧方案\n\n问题..."}]
    },
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "background_style": "blue-50",
      "elements": [{"tag": "markdown", "content": "### ✅ 新方案\n\n改进..."}]
    }
  ]
}
```

### 2.3 三列统计主推块

适合展示 3 个关键数字：

```json
{
  "tag": "column_set",
  "flex_mode": "trisect",
  "background_style": "grey-50",
  "columns": [
    {"tag": "column", "width": "weighted", "weight": 1,
     "background_style": "grey-50",
     "elements": [{"tag": "markdown", "content": "**30**\n篇归档"}]},
    {"tag": "column", "width": "weighted", "weight": 1,
     "background_style": "grey-50",
     "elements": [{"tag": "markdown", "content": "**18**\nAtoms"}]},
    {"tag": "column", "width": "weighted", "weight": 1,
     "background_style": "grey-50",
     "elements": [{"tag": "markdown", "content": "**1**\n主种子"}]}
  ]
}
```

---

## 3. 亮点块模式

### 3.1 单金句亮点块

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "yellow-50",
  "columns": [{
    "tag": "column",
    "width": "weighted",
    "weight": 1,
    "background_style": "yellow-50",
    "elements": [
      {"tag": "markdown", "content": "### ⚡ 今日反常识金句\n\n**「SaaS 卖软件，Agent SaaS 卖工作」**\n\n> 制作自动化不解决价值发生 → PMF 在消费/分发/结算"}
    ]
  }]
}
```

### 3.2 多金句亮点块

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "yellow-50",
  "columns": [{
    "tag": "column",
    "background_style": "yellow-50",
    "elements": [
      {"tag": "markdown", "content": "### ⚡ 反常识金句 TOP 3\n\n**1. 「SaaS 卖软件，Agent SaaS 卖工作」**\n\n**2. 「PMF 不在制作环节」**\n\n**3. 「信任一旦崩塌，争论本身就失去了意义」**"}
    ]
  }]
}
```

### 3.3 可复制提示词亮点块

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "yellow-50",
  "columns": [{
    "tag": "column",
    "background_style": "yellow-50",
    "elements": [
      {"tag": "markdown", "content": "### 🚀 一键复制提示词\n\n```\n请修改 xxx 文件，加入 yyy 步骤...\n```\n\n📋 复制上方提示词到 TRAE 新会话即可执行"}
    ]
  }]
}
```

---

## 4. 统计块模式

### 4.1 列表式统计块

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "grey-50",
  "columns": [{
    "tag": "column",
    "background_style": "grey-50",
    "elements": [
      {"tag": "markdown", "content": "### 📊 今日统计\n\n- 素材：6 篇\n- atoms：32 个（4 层 10 类）\n- concepts：5 个\n- 5 星 atoms：8 个（25% 覆盖率）\n- 字典表查表：4 次 / 23 次命中"}
    ]
  }]
}
```

### 4.2 表格式统计块

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "grey-50",
  "columns": [{
    "tag": "column",
    "background_style": "grey-50",
    "elements": [
      {"tag": "markdown", "content": "### 📊 Atoms 质量自检\n\n| 维度 | 当前 | 阈值 | 状态 |\n|------|------|------|------|\n| 条目数/千字 | 12.5 | ≥10 | ✅ |\n| 4 层覆盖率 | 4/4 | ≥2 | ✅ |\n| 关联数/5 atom | 1.4 | ≥1 | ✅ |\n| 5 星覆盖率 | 25% | ≥10% | ✅ |"}
    ]
  }]
}
```

### 4.3 耗时统计块

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "grey-50",
  "columns": [{
    "tag": "column",
    "background_style": "grey-50",
    "elements": [
      {"tag": "markdown", "content": "### ⏱️ 耗时统计\n\n- Action 1（即时）：15 分钟\n- Action 2（中期）：30 分钟\n- Action 3（长期）：4-6 小时\n\n**总计**：5-7 小时"}
    ]
  }]
}
```

---

## 5. 行动按钮模式

### 5.1 单按钮（查看文档）

```json
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "📄 查看完整云文档"},
  "type": "primary",
  "width": "fill",
  "behaviors": [{"type": "open_url", "default_url": "https://..."}]
}
```

### 5.2 双按钮（主+次）

```json
{/* 主按钮 - 跳转文档 */}
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "📄 查看完整云文档"},
  "type": "primary",
  "width": "fill",
  "behaviors": [{"type": "open_url", "default_url": "https://..."}]
},
{/* 次按钮 - 复制提示词 */}
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "📋 复制行动 1 提示词"},
  "type": "default",
  "width": "fill",
  "behaviors": [{"type": "open_url", "default_url": "https://example.com/action"}]
}
```

### 5.3 危险按钮（撤销/删除）

```json
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "🗑️ 撤销操作"},
  "type": "danger",
  "width": "fill",
  "behaviors": [{"type": "callback", "value": {"action": "undo"}}]
}
```

---

## 6. Footer 来源标识模式（note 元素已废弃）

> ⚠️ **重要**：`note` 元素在 Card 2.0 V2 已废弃，不要再使用。
> 改用 `markdown` 元素 + `>` 引用样式作为 footer 来源标识。
> 验证器 R12 会对 note 元素发出废弃警告。

### 6.1 简单 footer（markdown 引用）

```json
{
  "tag": "markdown",
  "content": "> 🤖 自动生成 · 2026-07-19 07:30"
}
```

### 6.2 多段信息 footer（用 markdown 拼接）

```json
{
  "tag": "markdown",
  "content": "> 🤖 obsidian-loop v2.1 · **触发**：cron 2070cc93 · **作者**：AI"
}
```

### 6.3 带 emoji 装饰的 footer

```json
{
  "tag": "markdown",
  "content": "> 🤖 obsidian-loop v2.1 demo · 07:30 自动生成 · schema 2.0 · 邻近色环 turquoise+blue+yellow（3 主色系）"
}
```

---

## 7. 特殊场景布局

### 7.1 告警卡片布局

```
┌────────────────────────────────────┐
│  Header (red)                      │
├────────────────────────────────────┤
│  🚨 告警块 (red-50) - 紧急程度     │
│  ─── hr ───                        │
│  📊 4 维状态 (yellow-50)           │
│  ─── hr ───                        │
│  🔧 Critical 修复清单 (red-50)     │
│  ─── hr ───                        │
│  📊 统计 (grey-50)                 │
│  ─── hr ───                        │
│  🛠️ 立即修复 (primary button)      │
│  Footer note                       │
└────────────────────────────────────┘
```

### 7.2 行动卡片布局

```
┌────────────────────────────────────┐
│  Header (green)                    │
├────────────────────────────────────┤
│  🎯 N 个行动卡片 (green-50)        │
│  ─── hr ───                        │
│  ⏱️ 行动理由+耗时 (grey-50)        │
│  ─── hr ───                        │
│  🚀 一键复制提示词 (yellow-50)     │
│  ─── hr ───                        │
│  📋 复制提示词 (default button)    │
│  📄 查看完整清单 (primary button)  │
│  Footer note                       │
└────────────────────────────────────┘
```

### 7.3 健康报告布局

```
┌────────────────────────────────────┐
│  Header (red)                      │
├────────────────────────────────────┤
│  📊 总评分 (red-50) - 告警         │
│  ─── hr ───                        │
│  📈 四维健康度 (yellow-50)         │
│  ─── hr ───                        │
│  🚨 Critical 修复 Top 3 (red-50)   │
│  ─── hr ───                        │
│  📚 完整健康报告 (primary button)  │
│  Footer note                       │
└────────────────────────────────────┘
```

### 7.4 周报布局

```
┌────────────────────────────────────┐
│  Header (indigo)                   │
├────────────────────────────────────┤
│  📝 5 条干货 (blue-50)             │
│  ─── hr ───                        │
│  ⚡ Aha 金句 TOP 3 (yellow-50)     │
│  ─── hr ───                        │
│  🌐 跨天涌现模式 (grey-50)         │
│  ─── hr ───                        │
│  🧠 元方法论沉淀 (grey-50)         │
│  ─── hr ───                        │
│  📄 查看完整周报 (primary button)  │
│  Footer note                       │
└────────────────────────────────────┘
```

---

## 8. 布局自检清单

生成卡片后，对照以下清单自检：

- [ ] 有 Header（title + subtitle + template）
- [ ] 至少 1 个主推块（blue-50/turquoise-50/green-50）
- [ ] 亮点块不超过 1 个（yellow-50）
- [ ] 统计块用 grey-50
- [ ] 段落之间用 hr 分隔
- [ ] 至少 1 个行动按钮（除非纯展示类）
- [ ] 有 footer note（来源/版本/时间戳）
- [ ] 总元素数 4-8 个（少于 4 信息不足，多于 8 信息过载）
- [ ] column 和 column_set 同时设置 background_style
- [ ] 多列布局用 flex_mode（bisect/trisect）

---

## 9. 布局禁忌

| 禁忌 | 原因 |
|------|------|
| 10 个以上 body elements | 信息过载，用户扫不完 |
| 没有 hr 分隔 | 视觉无层次 |
| 没有 background_style | 视觉无重点 |
| 5 个以上 column_set | 视觉碎片化 |
| 主推块在最后 | 用户可能没看到就关了 |
| 行动按钮在中间 | 用户找不到下一步 |
| 没有 footer note | 来源不明，可信度低 |
