# 组件选择决策表

**核心原则**：组件服务于阅读友好，不追求密度。能用纯 md 表达清楚的不上组件。

## 速查表

| 内容信号 | 首选 | 降级 |
|---|---|---|
| 补充说明/提示/警告/结论强调 | `Callout`（按语义选 type） | `>` 引用 |
| 分步骤/时间顺序 **≥3 步** | `Timeline` | 有序列表 |
| 多语言/多平台同等代码 | `CodeTabs` | 多个独立 code block |
| FAQ/长附录/次要但不删 | `Collapse`（默认折叠） | 纯 md 小节 |
| A vs B 两列等长要点 | `CompareCard` | 两列表格 |
| 同主题系列截图 **≥3 张** | `ImageCarousel` | 纯 md 多图 |
| 可运行代码 + 输出 | `Playground` | 代码块 + `> 输出：...` |
| YouTube/Bilibili/本地视频 | `Video`（v1.3 新增） | 直接放视频链接 |
| 普通段落/列表/引用 | **纯 md，不用组件** | — |

## 硬规则

1. **一段话能直接用 md 表达清楚的，不要包组件**
2. Timeline 至少 3 步才用
3. ImageCarousel 至少 3 张图才用
4. Collapse 只藏次要信息，不藏主要内容
5. **无数量上限**：组件数量由内容需要决定，不设硬性比例

## 典型场景

### 教程型长文

- 概述段：纯 md
- 准备工作（3 个前置）：Timeline
- 代码示例（Python + JS）：CodeTabs
- 注意事项：Callout warning
- 效果对比（6 张截图）：ImageCarousel
- 常见问题（5 个 Q&A）：5 个 Collapse

### 评测/对比型文章

- 引言：纯 md
- 方案对比（A vs B）：CompareCard
- 详细测试数据：markdown 表格
- 结论：Callout info

### 资讯/速记型短文

- 全程纯 md，顶多一个 Callout tip 点出重点
