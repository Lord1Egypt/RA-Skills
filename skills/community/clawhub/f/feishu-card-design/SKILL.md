---
name: feishu-card-design
slug: feishu-card-design
displayName: Feishu Card Design 飞书卡片消息设计规范
version: 1.0.5
summary: 适用于所有 Agent 平台的飞书 IM 卡片消息渲染规范——Card 2.0 Schema + 邻近色环 + 5 语义色块 + 11 种报告类型配色映射 + Python 验证器/构建器/转换器。
description: 飞书卡片消息设计规范技能——一套适用于所有 Agent 平台（TRAE 定时任务、Coze、Dify、自建 Agent）的飞书 IM 卡片消息渲染规范。基于 Card 2.0 Schema，定义邻近色环配色规则、标题命名规则、布局模式、客户端兼容性、可访问性。本技能是纯规范 Skill，不直接发送飞书消息。Do NOT use for 飞书云文档编辑/多维表格操作/IM 群管理/只发文本消息。
trigger_words:
  - 飞书卡片
  - 飞书卡片消息
  - Card 2.0
  - feishu card
  - lark card
  - 飞书卡片设计
  - 飞书卡片样式
  - 飞书卡片配色
  - 飞书卡片模板
  - IM 提醒样式
  - 推送飞书卡片
author: EdwardWason
license: MIT
homepage: https://github.com/EdwardWason/feishu-card-design
tags:
  - feishu
  - lark
  - card-design
  - agent
  - notification
  - im
  - template
language: zh-CN
---

# feishu-card-design · 飞书卡片消息设计规范

> 版本 1.0.5 | Card 2.0 Schema | 让任何 Agent 平台生成的飞书卡片消息都视觉一致、信息密度合理、行动闭环完整。

## 何时使用

**触发场景**（任一即触发）：
- Agent 需要发送飞书 IM 卡片消息（cron 定时任务、监控告警、报告推送、状态更新）
- 用户说"飞书卡片"、"飞书卡片消息"、"Card 2.0"、"飞书卡片设计/配色/模板"、"IM 提醒样式"、"推送飞书卡片"
- 已有卡片渲染不理想（Markdown 不渲染、配色混乱、标题无区分度、客户端兼容差）

**Do NOT use for**：
- 只发文本消息（不需要卡片）
- 飞书云文档编辑（用 lark-doc skill）
- 飞书多维表格操作（用 lark-base skill）
- 飞书 IM 群管理（用 lark-im skill，本 skill 只管卡片样式）

## 5 大铁律

### 铁律 1：Card 2.0 Schema
```json
{
  "schema": "2.0",
  "config": {"wide_screen_mode": true, "update_multi": true},
  "header": {
    "title": {"tag": "plain_text", "content": "卡片标题"},
    "subtitle": {"tag": "plain_text", "content": "副标题（可选）"},
    "template": "blue"
  },
  "body": {"elements": [...]}
}
```
**关键字段**：
- `header.title` / `header.subtitle`：必须是 `{"tag": "plain_text", "content": "..."}` 结构
- `header.template`：起始色枚举（turquoise/blue/green/indigo/violet/red/yellow/wheat）
- `body.elements`：直接挂载数组，**不要**用 `action` 包装

**禁止**：旧版 `config.wide_screen_mode` / 顶层 `elements` / `lark_md` 元素（必须用 `markdown` 元素支持 `#`/`##`/`>`）/ `button` 用 `action` 包装（必须用 `behaviors`）

### 铁律 2：邻近色环配色（≤3 主色系）
- 由 `header.template` 决定起始色，整张卡片最多 3 种主色系
- 背景色块用 `*-50` 系列（light mode）
- `yellow-50` / `grey-50` 是**语义中性色**，不计入 3 主色系限制

| header.template | 邻近色环可选背景色 |
|-----------------|-------------------|
| turquoise | turquoise-50 / wathet-50 / blue-50 |
| blue | blue-50 / violet-50 / purple-50 |
| green | green-50 / turquoise-50 |
| indigo | indigo-50 / blue-50 / violet-50 |
| violet | violet-50 / purple-50 / indigo-50 |
| red | red-50（仅告警，不与其他色搭配）|
| yellow | yellow-50（仅亮点，不作为主色）|

### 铁律 3：5 语义色块
| 背景色 | Hex（light mode） | 语义 | 使用场景 |
|--------|------------------|------|---------|
| `blue-50` | `#F0F4FF` | 主推 | 核心信息、主要内容块 |
| `turquoise-50` | `#E2F8F5` | 主推 | 核心信息、主要内容块（turquoise 系） |
| `yellow-50` | `#FBF4DF` | 亮点 | 金句、关键发现、反常识、可复制提示词 |
| `grey-50` | `#f5f6f7` | 统计 | 数据统计、表格摘要、耗时、计数 |
| `green-50` | `#E4FAE1` | 成功 | 通过的检查、完成的任务、正向行动 |
| `red-50` | `#FEF0F0` | 告警 | 失败、Critical 修复、风险警告 |

**色值来源**：飞书官方文档 [颜色枚举值](https://open.feishu.cn/document/uAjLw4CM/ukzMukzMukzM/feishu-cards/enumerations-for-fields-related-to-color)，light mode 模式取 `*-50` 系列。

### 铁律 4：标题命名 `YYYYMMDD-类型-关键信息`
格式：`<8位日期>-<报告类型>-<关键信息1>-<关键信息2>-...`
- 报告类型：存量日报 / 增量日报 / 行动清单 / 健康报告 / 周报 / 月报 / 发芽日报 / 综合日报 / 反思报告 / 告警通知 / 成功通知
- 关键信息：AI 从标题和内容提取 2-4 个关键词，用 `-` 分隔
- ✅ `20260719-存量日报-归档30篇-Atoms18条-主种1个`
- ❌ `20260719-报告-report_id`（无关键信息）

### 铁律 5：column + column_set 双重保险
兼容性问题：`column.background_style` V7.4+ 支持，`column_set.background_style` V7.9+ 才支持。**同时设置两者**双重保险。`default` 是「无背景色」，不触发双重保险。

## 11 种报告类型 × 配色映射

| 报告类型 | header.template | 主推块 | 亮点块 | 统计块 | 告警块（条件触发） |
|---------|----------------|--------|--------|--------|------------------|
| 存量日报 | turquoise | turquoise-50 | yellow-50 | grey-50 | red-50（健康度章节有 ⚠️ 时） |
| 增量日报 | blue | blue-50 | yellow-50 | grey-50 | — |
| 行动清单 | green | green-50 | yellow-50 | grey-50 | — |
| 健康报告 | red | red-50 | yellow-50 | grey-50 | red-50（评分<60 或有 Critical） |
| 周报 | indigo | blue-50 | yellow-50 | grey-50 | — |
| 月报 | violet | blue-50 | yellow-50 | grey-50 | — |
| 发芽日报 | turquoise | turquoise-50 | yellow-50 | grey-50 | — |
| 综合日报 | blue | blue-50 | yellow-50 | grey-50 | — |
| 反思报告 | indigo | blue-50 | yellow-50 | grey-50 | — |
| 告警通知 | red | red-50 | yellow-50 | grey-50 | red-50（强制） |
| 成功通知 | green | green-50 | yellow-50 | grey-50 | — |

**告警块条件触发规则**：
- 扫描章节内容是否含告警关键词：`⚠️` / `异常` / `待补` / `Critical` / `失败` / `风险`
- 含告警关键词 → 该章节背景色块切换为 `red-50`
- 不含告警关键词 → 用默认色（主推块或 `green-50` 表示通过）
- 告警通知类型强制全部告警块用 `red-50`

## 4 段式标准结构
```
Header（title + subtitle + 色）→ 主推块（blue-50/turquoise-50）
→ 亮点块（yellow-50）→ 统计块（grey-50）→ 行动按钮 + Footer note
```
**永远不要省略**：Header + 主推块 + Footer note。简单通知可省略亮点/统计块。

## 3 种使用方式

**方式 1：Agent 读 SKILL.md + templates/**
Agent 收到"发飞书卡片"指令时，Read SKILL.md → 从 `templates/` 复制模板 → 替换内容 → 用 `scripts/card_validator.py` 验证 → 调用飞书 OpenAPI `POST /im/v1/messages?receive_id_type=open_id` 发送。

**方式 2：Python 构建器**（推荐 Python Agent）
```python
from scripts.card_builder import stock_card, flow_card, action_card, health_card, weekly_card
card = flow_card(title="20260719-增量日报-...", subtitle="...", doc_url="https://...",
                 main_content="...", highlight="...", stats="...")
```

**方式 3：Markdown → Card 转换器**
```bash
python scripts/markdown_to_card.py --input report.md --type flow-report \
  --title "20260719-增量日报-..." --output card.json
```

## 验证 11 项铁律
```bash
python scripts/card_validator.py --input card.json
```
检查：schema=2.0 / header.template 合法色 / `*-50` 背景 / ≤3 主色系 / 邻近色环 / column+column_set 双重保险 / button.behaviors / 禁 lark_md / 禁 action 包装 / 标题格式 / 主推块+note footer

## 权限声明

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ❌ | 本 Skill 是纯规范，不直接发请求；示例代码 `send_feishu_card()` 演示如何调用飞书 OpenAPI，由调用方负责 |
| 文件读写 | ✅ | `scripts/card_validator.py` 读卡片 JSON 文件；`markdown_to_card.py` 读 MD 写 JSON |
| 环境变量 | ❌ | 不读取任何环境变量（飞书 OpenAPI 凭证由调用方管理）|
| subprocess | ❌ | 不调用任何外部命令 |
| 外部 API | ❌ | 不调用任何外部 API（飞书 OpenAPI 由调用方集成）|

## 用户警告

⚠️ **本 Skill 是纯规范 Skill，不直接发送飞书消息**。所有网络请求由调用方代码（示例中的 `send_feishu_card()` 函数）发起，调用方需自行管理飞书 App 凭证（`app_id` / `app_secret`）和用户授权。本 Skill 不存储、不传输任何凭证。

调用方发送卡片消息时需注意：
- 推荐用 `open_id` 直接推送给用户本人，不要用 `chat_id` 推送到 AIbot 自聊会话（用户可能看不到）
- 飞书 App 需开通 `im:message:send_as_bot` 权限

## 文件结构

| 路径 | 内容 |
|------|------|
| `SKILL.md` | 本文件，主入口 |
| `README.md` / `README.en.md` | 21 章产品页（中英双语）|
| `references/` | 6 份规范文档：card-2.0-schema / color-system / title-naming / layout-patterns / compatibility / accessibility |
| `templates/` | 5 份 JSON 模板：report / stat / action / alert / success |
| `examples/` | 5 份真实样例：stock / flow / action / health / weekly（全部通过 11 项铁律验证）|
| `scripts/` | 3 份工具：card_validator.py / card_builder.py / markdown_to_card.py |

## 详细规范
- Card 2.0 Schema 完整字段：[references/card-2.0-schema.md](references/card-2.0-schema.md)
- 邻近色环配色规则详解：[references/color-system.md](references/color-system.md)
- 标题命名规则 + 关键信息提取：[references/title-naming.md](references/title-naming.md)
- 4 段式布局 + 多列布局：[references/layout-patterns.md](references/layout-patterns.md)
- 客户端版本兼容性：[references/compatibility.md](references/compatibility.md)
- 可访问性 + 国际化：[references/accessibility.md](references/accessibility.md)
- 21 章产品页：[README.md](README.md) / [README.en.md](README.en.md)

## License
MIT License — 详见 [LICENSE](LICENSE)
