# 飞书 Card 2.0 Schema 完整规范

> **版本**：1.0.4 | **Schema 来源**：[飞书官方文档](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/feishu-cards/card-components/overview)
> **本文件作用**：定义 Card 2.0 的完整 JSON Schema，所有 Agent 生成的卡片必须符合此 Schema

---

## 1. 顶层结构

```json
{
  "schema": "2.0",
  "config": {
    "wide_screen_mode": true,
    "update_multi": true,
    "enable_forward": true
  },
  "header": {
    "title": {...},
    "subtitle": {...},
    "template": "turquoise|blue|green|indigo|violet|red|yellow|wheat|grey",
    "icon": {...},
    "text_align": "left|center",
    "ud_icon": {...}
  },
  "body": {
    "direction": "vertical|horizontal",
    "padding": "16px 16px 16px 16px",
    "elements": [...]
  }
}
```

### 1.1 必填字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `schema` | string | ✅ | 必须为 `"2.0"` |
| `header` | object | ✅ | 卡片头部 |
| `header.title` | object | ✅ | 标题对象 |
| `header.title.tag` | string | ✅ | 必须为 `"plain_text"` |
| `header.title.content` | string | ✅ | 标题文本 |
| `body` | object | ✅ | 卡片正文 |
| `body.elements` | array | ✅ | 正文元素数组 |

### 1.2 可选字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `config.wide_screen_mode` | bool | true | 宽屏模式（已废弃但仍兼容） |
| `config.update_multi` | bool | true | 多端同步更新 |
| `config.enable_forward` | bool | true | 允许转发 |
| `header.subtitle` | object | null | 副标题 |
| `header.template` | string | "blue" | 头部配色模板 |
| `header.icon` | object | null | 头部图标 |
| `header.text_align` | string | "left" | 标题对齐 |
| `body.direction` | string | "vertical" | 排列方向 |
| `body.padding` | string | "12px 12px 12px 12px" | 内边距 |

---

## 2. Header 详细规范

### 2.1 基础 Header

```json
{
  "title": {
    "tag": "plain_text",
    "content": "20260719-增量日报-SaaS卖软件AgentSaaS卖工作"
  },
  "subtitle": {
    "tag": "plain_text",
    "content": "2026-07-19 · 发现 + 洞察 + 反思"
  },
  "template": "blue"
}
```

### 2.2 带图标的 Header

```json
{
  "title": {
    "tag": "plain_text",
    "content": "🚀 obsidian-loop v2.1 增量日报"
  },
  "subtitle": {
    "tag": "plain_text",
    "content": "2026-07-19 · 4 反常识 / 1 融合 / 3 行动"
  },
  "template": "turquoise",
  "icon": {
    "tag": "standard_icon",
    "token": "myai_colorful"
  },
  "text_align": "left"
}
```

### 2.3 template 取值表

| template | 色相 | 推荐用途 |
|----------|------|---------|
| `turquoise` | 青绿 | 存量日报、发芽日报 |
| `blue` | 蓝色 | 增量日报、综合日报 |
| `green` | 绿色 | 行动清单、成功通知 |
| `indigo` | 靛青 | 周报、反思报告 |
| `violet` | 紫色 | 月报、趋势分析 |
| `red` | 红色 | 告警、健康报告 |
| `yellow` | 黄色 | ⚠️ 不推荐做 header（太亮） |
| `wheat` | 米黄 | 中性通知（不强调类型） |
| `grey` | 灰色 | ⚠️ 不推荐做 header（无色彩） |

---

## 3. Body 元素清单

### 3.1 markdown 元素（推荐）

```json
{
  "tag": "markdown",
  "content": "**加粗** / # 标题 / > 引用 / `代码`"
}
```

**完整 Markdown 语法支持**：

| 语法 | 效果 |
|------|------|
| `**bold**` | **加粗** |
| `# H1` | 一级标题 |
| `## H2` | 二级标题 |
| `### H3` | 三级标题 |
| `> quote` | 引用块 |
| `` `code` `` | 行内代码 |
| ` ```code block``` ` | 代码块 |
| `- item` | 无序列表 |
| `1. item` | 有序列表 |
| `[text](url)` | 链接 |
| `---` | 分隔线 |
| `\n` | 换行 |

### 3.2 column_set + column 元素（结构化布局 + 配色）

> ⚠️ **重要**：`column_set` 和 `column` 元素**不支持 `padding` 属性**（飞书 API 报 230099 错误）。
> 只有 `body` 支持 `padding`。内边距通过 `body.padding` 统一控制。
> `column` 必须设置 `background_style`（与 `column_set` 同色），满足 R4 双重保险规则。

#### 单列布局（最常用）

```json
{
  "tag": "column_set",
  "flex_mode": "none",
  "background_style": "blue-50",
  "columns": [
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "vertical_align": "top",
      "background_style": "blue-50",
      "elements": [
        {"tag": "markdown", "content": "### 🌟 核心洞察\n\n..."}
      ]
    }
  ]
}
```

#### 双列布局（对比展示）

```json
{
  "tag": "column_set",
  "flex_mode": "bisect",
  "background_style": "grey-50",
  "columns": [
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "elements": [{"tag": "markdown", "content": "**左侧**"}]
    },
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "elements": [{"tag": "markdown", "content": "**右侧**"}]
    }
  ]
}
```

#### 三列布局（统计数据）

```json
{
  "tag": "column_set",
  "flex_mode": "trisect",
  "background_style": "grey-50",
  "columns": [
    {"tag": "column", "width": "weighted", "weight": 1, "elements": [{"tag": "markdown", "content": "**30**\n篇归档"}]},
    {"tag": "column", "width": "weighted", "weight": 1, "elements": [{"tag": "markdown", "content": "**18**\nAtoms"}]},
    {"tag": "column", "width": "weighted", "weight": 1, "elements": [{"tag": "markdown", "content": "**1**\n主种子"}]}
  ]
}
```

### 3.3 hr 元素（分隔线）

```json
{"tag": "hr"}
```

### 3.4 button 元素（Card 2.0 必须用 behaviors）

#### 主按钮（查看文档）

```json
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "📄 查看完整云文档"},
  "type": "primary",
  "width": "fill",
  "behaviors": [{"type": "open_url", "default_url": "https://..."}]
}
```

#### 默认按钮（次要操作）

```json
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "📋 复制提示词"},
  "type": "default",
  "width": "fill",
  "behaviors": [{"type": "open_url", "default_url": "https://example.com/action"}]
}
```

#### 危险按钮（删除/撤销）

```json
{
  "tag": "button",
  "text": {"tag": "plain_text", "content": "🗑️ 撤销操作"},
  "type": "danger",
  "width": "fill",
  "behaviors": [{"type": "open_url", "default_url": "..."}]
}
```

### 3.5 footer 来源标识（note 元素已废弃）

> ⚠️ **重要**：`note` 元素在 Card 2.0 V2 已废弃，不要再使用。
> 改用 `markdown` 元素 + `>` 引用样式作为 footer 来源标识。

#### 推荐写法（markdown + > 引用样式）

```json
{
  "tag": "markdown",
  "content": "> 🤖 自动生成 · 触发时间 2026-07-19 07:30"
}
```

#### 已废弃写法（note 元素，不要再使用）

```json
{
  "tag": "note",
  "elements": [
    {"tag": "plain_text", "content": "🤖 自动生成 · 触发时间 2026-07-19 07:30"}
  ]
}
```

> 验证器 R12 会对 note 元素发出废弃警告，R11 会检查 footer 来源标识是否存在（建议用 markdown > 引用样式）。

---

## 4. behaviors 完整规范

### 4.1 open_url（打开链接）

```json
{
  "type": "open_url",
  "default_url": "https://feishu.cn/docx/xxx",
  "pc_url": "https://pc-url.com",     // PC 端跳转（可选）
  "ios_url": "https://example.com/ios",       // iOS 端跳转（可选）
  "android_url": "https://example.com/android" // Android 端跳转（可选）
}
```

### 4.2 callback（回调服务端）

```json
{
  "type": "callback",
  "value": {"key": "action_id", "data": "xxx"}
}
```

### 4.3 open_app（打开飞书小程序）

```json
{
  "type": "open_app",
  "app_id": "cli_xxx",
  "page_path": "pages/index/index"
}
```

---

## 5. 完整最小可用卡片

```json
{
  "schema": "2.0",
  "config": {"wide_screen_mode": true, "update_multi": true},
  "header": {
    "title": {"tag": "plain_text", "content": "20260719-通知-示例"},
    "subtitle": {"tag": "plain_text", "content": "2026-07-19 · 示例通知"},
    "template": "blue"
  },
  "body": {
    "direction": "vertical",
    "padding": "16px 16px 16px 16px",
    "elements": [
      {
        "tag": "column_set",
        "flex_mode": "none",
        "background_style": "blue-50",
        "columns": [{
          "tag": "column",
          "width": "weighted",
          "weight": 1,
          "vertical_align": "top",
          "background_style": "blue-50",
          "elements": [
            {"tag": "markdown", "content": "### 📌 通知\n\n这是一条示例通知。"}
          ]
        }]
      },
      {"tag": "hr"},
      {
        "tag": "button",
        "text": {"tag": "plain_text", "content": "📄 查看详情"},
        "type": "primary",
        "width": "fill",
        "behaviors": [{"type": "open_url", "default_url": "https://example.com"}]
      },
      {
        "tag": "markdown",
        "content": "> 🤖 自动生成"
      }
    ]
  }
}
```

---

## 6. 禁止用法清单

### 6.1 已废弃字段

| 字段 | 状态 | 替代方案 |
|------|------|---------|
| `config.wide_screen_mode` | ⚠️ 已废弃但仍兼容 | 用 `schema: "2.0"` 标识 |
| `elements`（顶层） | ❌ Card 1.0 风格 | 用 `body.elements` |
| `lark_md` 元素 | ⚠️ 不支持 `#`/`##`/`>` | 用 `markdown` 元素 |
| `action` 包装 button | ❌ Card 2.0 报错 | 直接用 button + behaviors |
| button.url | ❌ 已废弃 | 用 button.behaviors[].default_url |
| `div` 元素 | ⚠️ 已过时 | 用 column_set + column |
| `note` 元素 | ❌ Card 2.0 V2 不支持 | 用 `markdown` + `>` 引用样式 |
| `column_set.padding` | ❌ API 报 230099 | 用 `body.padding` 统一控制 |
| `column.padding` | ❌ API 报 230099 | 用 `body.padding` 统一控制 |

### 6.2 常见 Schema 错误

| 错误 | 正确 |
|------|------|
| `"schema": 2` | `"schema": "2.0"`（字符串） |
| `"template": "#FF0000"` | `"template": "red"`（枚举值） |
| `"background_style": "#F0F4FF"` | `"background_style": "blue-50"`（枚举值） |
| `"weight": "1"` | `"weight": 1`（数字） |
| `"width": "100%"` | `"width": "weighted"` + `"weight": 1` |
| `column_set` 含 `padding` | 删除 `padding`，用 `body.padding` |
| `note` 元素 | 改用 `markdown` + `>` 引用 |
