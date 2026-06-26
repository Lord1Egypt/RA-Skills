# expression-layer: 表达层

统一的内容生成与可视化输出协调器。不依赖思考层，直接按意图路由至 ljg-skills 及发布工具。

## 快速开始

```
/表达层 什么是定投？说人话，顺便做个卡片。
/表达层 读这篇论文 https://arxiv.org/abs/xxx，做成漫画卡片。
/表达层 把刚才的分析写成公众号文章发出去。
```

## 路由矩阵

| 意图 | 编排路径 | 输出 |
|------|---------|------|
| `plain` | ljg-plain | 大白话文本 |
| `writes` | ljg-writes → humanizer-zh | 深度文章 |
| `card` | ljg-card (-l/-i/-c/-w/-b) | PNG 卡片 |
| `present` | ljg-present | HTML 演讲 |
| `paper_flow` | ljg-paper → ljg-card | 解读 + PNG |
| `word_flow` | ljg-word → ljg-card | 解析 + PNG |
| `travel` | ljg-travel | 研究报告 + PNG |
| `wechat` | wechat-publisher | 公众号推文 |

## 编排模式

- **单步**：直接路由到 1 个 skill
- **串联**：A 输出 → B 输入
- **并行**：同时生成多个形式
- **发布**：内容 → 公众号

## 扩展指南

新增 skill 时：
1. 更新 SKILL.md 路由矩阵
2. 更新 references/orchestration-matrix.md
3. 升级版本号（patch）
4. 提交并推送

---

*版本：v1.0.0 | 2026-04-24*
