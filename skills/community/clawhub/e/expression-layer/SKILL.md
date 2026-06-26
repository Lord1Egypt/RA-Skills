---
name: expression-layer
version: 1.0.0
description: "［何时使用］当需要内容生成、格式转换或多形式输出时触发。支持直接输入问题/素材/链接，无需前置思考层。统一路由至 ljg-skills 及发布工具。"
author: 燃冰 & ant
created: 2026-04-24
skill_type: 通用🟡
allowed-tools: [Bash, Read, Write, Exec, WebSearch]
related_skills: [investor-education-workflow, investment-workflow, investment-advisory-workflow, ljg-skills]
tags: [内容生成, 格式转换, 技能编排, 路由, 多形式输出]
---

# expression-layer: 表达层 🎨

## 📋 功能描述

帮助用户**统一调度内容生成与可视化输出**。不依赖前置思考层，直接接收问题/素材/链接，按意图路由至对应 skill，支持单步/串联/并行/发布编排。

**适用场景：**
- 直接问概念/问题 → 口语化解释/深度文章
- 提供素材/草稿 → 写作 + 人性化 + 多形式输出
- 论文/单词/城市 → 解读 + 可视化卡片
- 完整文章 → 公众号发布

**边界条件：**
- 不负责深度分析/数据查询（由上游工作流或思考层提供）
- 输出格式依赖上游指定或意图自动识别
- 新增 skill 需更新路由矩阵

---

## 🔄 路由编排矩阵

| 输入类型 | 触发意图 | 编排路径 | 输出形式 | 典型场景 |
|---------|---------|---------|---------|---------|
| 专业概念/问题 | `plain` | `ljg-plain` | 大白话文本（≤200字） | “什么是PE？说人话” |
| 观点/素材/草稿 | `writes` | `ljg-writes` → `humanizer-zh` | 深度文章（1000-1500字） | “把这段写成公众号文章” |
| 任何文本/数据 | `card` | `ljg-card`（-l/-i/-c/-w/-b） | PNG 卡片 | “做个信息图/漫画/大字” |
| 文本/大纲 | `present` | `ljg-present` | HTML 高桥流 | “做成演讲PPT” |
| 论文链接/PDF | `paper_flow` | `ljg-paper` → `ljg-card` | 解读Markdown + PNG | “读论文并做漫画卡片” |
| 英文单词 | `word_flow` | `ljg-word` → `ljg-card` | 解析Markdown + PNG | “解词并做信息图” |
| 城市/主题 | `travel` | `ljg-travel` | 研究报告 + PNG卡片 | “做西安旅行功课” |
| 完整文章/解读 | `wechat` | `wechat-publisher` | 公众号推文（HTML+封面） | “发到公众号” |

**编排模式**：
- `单步`：直接路由到 1 个 skill
- `串联`：A 输出 → B 输入（如 `ljg-paper → ljg-card`）
- `并行`：同时生成多个形式（如 大白话 + 卡片 + 文章）
- `发布`：内容 → `wechat-publisher` → 公众号

---

## ⚠️ 常见错误

**错误 1：强行附加思考层**
```
问题：
• 用户只问“什么是定投”，却先跑降秩/追本分析
• 输出冗长，偏离直接表达需求

解决：
✓ 表达层是独立入口，不依赖思考层
✓ 直接按意图路由到 ljg-plain / ljg-writes
✓ 如需深度分析，由上游工作流调用，非表达层职责
```

**错误 2：忽略输出格式指定**
```
问题：
• 只给内容，不指定输出形式
• 路由歧义（该出文章还是卡片？）

解决：
✓ 优先按关键词自动识别意图（如“说人话”→plain，“做卡片”→card）
✓ 歧义时主动询问：“需要大白话解释、深度文章，还是可视化卡片？”
✓ 支持并行输出：plain + card + writes
```

**错误 3：新增 skill 未更新路由**
```
问题：
• 安装了新 skill，但路由矩阵未更新
• 表达层无法调度新能力

解决：
✓ 新增 skill 后，同步更新 SKILL.md 路由矩阵
✓ 在 references/orchestration-matrix.md 维护完整映射
✓ 提交版本升级（patch version）
```

---

## 🧪 使用示例

**输入：**
```
什么是定投？说人话，顺便做个卡片。
```

**预期输出：**
- 识别意图：`multi` (plain + card)
- 编排：并行执行 `ljg-plain` + `ljg-card -i`
- 输出：大白话文本 + PNG 信息图

**输入：**
```
读这篇论文 https://arxiv.org/abs/xxx，做成漫画卡片。
```

**预期输出：**
- 识别意图：`paper_flow`
- 编排：串联执行 `ljg-paper` → `ljg-card -c`
- 输出：论文解读 Markdown + 漫画风格 PNG

**输入：**
```
把刚才的消费分析写成公众号文章发出去。
```

**预期输出：**
- 识别意图：`wechat`
- 编排：`ljg-writes` → `humanizer-zh` → `wechat-publisher`
- 输出：公众号草稿（已排版+封面+合规检查）

---

## 🔧 故障排查

| 问题 | 检查项 |
|------|--------|
| 不触发 | description 是否包含触发词？用户输入是否匹配意图？ |
| 路由错误 | 意图识别是否准确？是否歧义未询问？ |
| 输出为空 | 上游 skill 是否安装？（ljg-plain/ljg-card/wechat-publisher） |
| 新增 skill 不调用 | 路由矩阵是否更新？references 是否同步？ |
| 格式错误 | 输出格式是否指定？并行输出是否超出上下文限制？ |

---

## 🔗 相关资源

- 路由编排矩阵：`references/orchestration-matrix.md`
- 投教工作流编排分析：`references/ie-orchestration.md`
- 输出模板：`templates/output-template.md`
- 标准参考：`docs/SKILL-STANDARD-v3.md`
