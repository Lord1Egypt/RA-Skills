# 飞书卡片配色系统 · 邻近色环规则详解

> **版本**：1.0.4 | **本文件作用**：定义"邻近色环 + 3 主色系 + 5 语义色块"完整配色规则
> **设计依据**：[颜色字段枚举值](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/feishu-cards/enumerations-for-fields-related-to-color)

---

## 1. 核心规则总览

### 1.1 5 大配色铁律

1. **header.template 决定起始色**：整张卡片的色相基调由 header 决定
2. **最多 3 种主色系**：含 header 色，整张卡片不超过 3 个色相
3. **背景色用 `*-50` 系列**：light mode 浅色（不深色）
4. **邻近色环搭配**：不跨色相，按色相环邻接搭配
5. **5 种语义色块**：blue-50/turquoise-50(主推) / yellow-50(亮点) / grey-50(统计) / green-50(成功) / red-50(告警)

### 1.2 色相环（参考）

```
红 ── 橙 ── 黄
 │           │
紫           绿
 │           │
靛 ── 蓝 ── 青(turquoise)
```

**邻近色定义**：色相环上相邻 2 步以内的颜色。

---

## 2. 邻近色环映射表

### 2.1 完整邻近色环

| 起始色（header.template） | 邻近色 1 | 邻近色 2 | 邻近色 3 | 不可搭配 |
|--------------------------|---------|---------|---------|---------|
| **turquoise**（青绿） | turquoise-50 | wathet-50 | blue-50 | red-50, yellow-50（少量 OK） |
| **blue**（蓝） | blue-50 | violet-50 | purple-50 | red-50, green-50 |
| **green**（绿） | green-50 | turquoise-50 | — | red-50, violet-50 |
| **indigo**（靛青） | indigo-50 | blue-50 | violet-50 | yellow-50, green-50 |
| **violet**（紫） | violet-50 | purple-50 | indigo-50 | green-50, yellow-50 |
| **red**（红，仅告警） | red-50 | — | — | 任何主推色（red 独占） |
| **yellow**（黄，仅亮点） | yellow-50 | — | — | 不做 header |

### 2.2 推荐配色组合

#### 配色 1：turquoise 系（存量/发芽日报）

```
header: turquoise
body blocks:
  - 主推块: turquoise-50
  - 亮点块: yellow-50
  - 统计块: grey-50
  - 底部说明: 透明（无背景）
```

#### 配色 2：blue 系（增量/综合日报）

```
header: blue
body blocks:
  - 主推块: blue-50
  - 亮点块: yellow-50
  - 统计块: grey-50
  - 底部说明: 透明
```

#### 配色 3：green 系（行动/成功通知）

```
header: green
body blocks:
  - 主推块: green-50
  - 亮点块: yellow-50
  - 统计块: grey-50
  - 底部说明: 透明
```

#### 配色 4：red 系（告警/健康报告）

```
header: red
body blocks:
  - 告警块: red-50
  - 亮点块: yellow-50
  - 统计块: grey-50
  - 底部说明: 透明
```

#### 配色 5：indigo 系（周报/反思）

```
header: indigo
body blocks:
  - 主推块: blue-50
  - 亮点块: yellow-50
  - 统计块: grey-50
  - 底部说明: 透明
```

#### 配色 6：violet 系（月报/趋势）

```
header: violet
body blocks:
  - 主推块: blue-50
  - 亮点块: yellow-50
  - 统计块: grey-50
  - 底部说明: 透明
```

---

## 3. 5 种语义色块详解

### 3.1 blue-50 / turquoise-50（主推色）

**用途**：核心信息块、主要内容区
**Light mode 色值**：
- `blue-50` = `#F0F4FF`
- `turquoise-50` = `#E2F8F5`

**使用原则**：
- 每张卡片至少有 1 个主推块
- 主推块用于承载用户最需要看到的信息
- 同一张卡片主推块不超过 2 个

**示例**：
```json
{
  "tag": "column_set",
  "background_style": "blue-50",
  "columns": [{
    "tag": "column",
    "background_style": "blue-50",
    "elements": [{"tag": "markdown", "content": "### 🌟 核心洞察\n\n本日最重要发现..."}]
  }]
}
```

### 3.2 yellow-50（亮点色）

**用途**：金句、反常识、可复制提示词、Aha 时刻
**Light mode 色值**：`yellow-50` = `#FBF4DF`

**使用原则**：
- 每张卡片最多 1 个亮点块（避免视觉疲劳）
- 亮点块用于"用户看完会截图分享"的内容
- 不做主推（黄色饱和度高，大面积使用刺眼）

**示例**：
```json
{
  "tag": "column_set",
  "background_style": "yellow-50",
  "columns": [{
    "tag": "column",
    "background_style": "yellow-50",
    "elements": [{"tag": "markdown", "content": "### ⚡ 今日反常识金句\n\n**「SaaS 卖软件，Agent SaaS 卖工作」**"}]
  }]
}
```

### 3.3 grey-50（统计色）

**用途**：数据统计、表格摘要、耗时、计数
**Light mode 色值**：`grey-50` = `#f5f6f7`

**使用原则**：
- 用于辅助信息，不抢主推块视觉
- 每张卡片可有 1-2 个统计块
- 适合放数字密集的内容

**示例**：
```json
{
  "tag": "column_set",
  "background_style": "grey-50",
  "columns": [{
    "tag": "column",
    "background_style": "grey-50",
    "elements": [{"tag": "markdown", "content": "### 📊 今日统计\n- 素材：6 篇\n- atoms：32 个\n- concepts：5 个"}]
  }]
}
```

### 3.4 green-50（成功色）

**用途**：通过的检查、完成的任务、正向行动
**Light mode 色值**：`green-50` = `#E4FAE1`

**使用原则**：
- 用于肯定性信息
- 不与 red-50 同卡（避免红绿配色违和）
- 行动清单类卡片可作为主推色

**示例**：
```json
{
  "tag": "column_set",
  "background_style": "green-50",
  "columns": [{
    "tag": "column",
    "background_style": "green-50",
    "elements": [{"tag": "markdown", "content": "### ✅ 检查通过\n\n5 重质量门控全过"}]
  }]
}
```

### 3.5 red-50（告警色）

**用途**：失败、Critical 修复、风险警告、健康度低
**Light mode 色值**：`red-50` = `#FEF0F0`

**使用原则**：
- 仅用于真正的告警场景
- 不做主推色（红色会引起用户紧张）
- 与 yellow-50 + grey-50 搭配，形成"告警 + 亮点 + 统计"三段

**示例**：
```json
{
  "tag": "column_set",
  "background_style": "red-50",
  "columns": [{
    "tag": "column",
    "background_style": "red-50",
    "elements": [{"tag": "markdown", "content": "### 🚨 Critical 修复清单\n\n1. MOC 索引缺失\n2. atoms 断裂链接"}]
  }]
}
```

---

## 4. 完整色值速查表

### 4.1 Light Mode（推荐）

| 颜色名 | 色值 | 用途 |
|--------|------|------|
| `blue-50` | `#F0F4FF` | 主推 |
| `turquoise-50` | `#E2F8F5` | 主推（替代） |
| `wathet-50` | `#E6F4FF` | 主推（浅蓝） |
| `green-50` | `#E4FAE1` | 成功 |
| `yellow-50` | `#FBF4DF` | 亮点 |
| `orange-50` | `#FFEFD8` | 警告（次级） |
| `red-50` | `#FEF0F0` | 告警 |
| `purple-50` | `#F3E8FF` | 主推（紫系） |
| `violet-50` | `#EDE7FF` | 主推（靛紫） |
| `indigo-50` | `#E8E9FF` | 主推（靛青） |
| `grey-50` | `#f5f6f7` | 统计 |
| `default` | 透明 | 无背景 |

### 4.2 Dark Mode（暂不推荐）

Dark mode 色值命名规则为 `*-700` 系列（如 `blue-700`），目前飞书客户端 Dark Mode 自动适配，不需要手动指定。

---

## 5. 配色禁忌清单

### 5.1 绝对禁止

| 禁忌 | 原因 |
|------|------|
| 5 种以上背景色 | 视觉花哨失去重点 |
| `red-50` 做主推块 | 引起不必要紧张 |
| `yellow-50` 做主推块 | 黄色饱和度高，刺眼 |
| 跨色相搭配（如 red+green） | 违和，违反邻近色环 |
| header 用 `grey` | 无色彩，失去识别度 |
| header 用 `yellow` | 太亮，标题区不应是黄色 |

### 5.2 不推荐

| 不推荐 | 替代 |
|--------|------|
| 整张卡片同一种背景色 | 主推+亮点+统计三段 |
| 用 `default` 透明做主推 | 主推必须有背景色 |
| 多张卡片用同一 template | 不同类型用不同 template 区分 |

---

## 6. 配色自检清单

生成卡片后，对照以下清单自检：

- [ ] header.template 是合法枚举值（turquoise/blue/green/indigo/violet/red/wheat）
- [ ] 整张卡片主色系不超过 3 种
- [ ] 所有背景色都是 `*-50` 系列（light mode）
- [ ] 配色符合邻近色环（不跨色相）
- [ ] 主推块用 blue-50/turquoise-50/green-50（按 header 系）
- [ ] 亮点块用 yellow-50（最多 1 个）
- [ ] 统计块用 grey-50
- [ ] 告警块用 red-50（仅告警卡片）
- [ ] column 和 column_set 同时设置 background_style
- [ ] 不存在 5 种以上背景色

---

## 7. 与报告类型的固定映射

| 报告类型 | header.template | 主推色 | 亮点色 | 统计色 | 特殊色 |
|---------|----------------|--------|--------|--------|--------|
| 存量日报 | turquoise | turquoise-50 | yellow-50 | grey-50 | — |
| 增量日报 | blue | blue-50 | yellow-50 | grey-50 | — |
| 行动清单 | green | green-50 | yellow-50 | grey-50 | — |
| 健康报告 | red | red-50 | yellow-50 | grey-50 | red-50（告警） |
| 周报 | indigo | blue-50 | yellow-50 | grey-50 | — |
| 月报 | violet | blue-50 | yellow-50 | grey-50 | — |
| 发芽日报 | turquoise | turquoise-50 | yellow-50 | grey-50 | — |
| 综合日报 | blue | blue-50 | yellow-50 | grey-50 | — |
| 反思报告 | indigo | blue-50 | yellow-50 | grey-50 | — |
| 告警通知 | red | red-50 | yellow-50 | grey-50 | red-50（告警） |
| 成功通知 | green | green-50 | yellow-50 | grey-50 | green-50（成功） |

**固定映射的意义**：用户看到 header 颜色就知道卡片类型，跨 Agent 平台保持一致。
