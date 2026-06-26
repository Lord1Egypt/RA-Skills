---
name: ai-tech-interview-bootcamp
description: AI 全栈技术面试训练营 — 从真题追踪、代码练习到 Mock 面试的系统性面试备战方案
category: AI|开发|自动化
triggers: 面试, 技术面试, 刷题, 面试准备, code interview, 面经
---

# AI Tech Interview Bootcamp

AI 全栈技术面试训练营，帮你系统性准备技术面试。整合真题追踪、代码练习、Mock 对练三大模块，覆盖前端/后端/算法/系统设计全维度。

## 核心功能

1. **热点真题挖掘** — 自动抓取 GitHub Trending、LeetCode 热题、牛客面经中的最新高频考点
2. **代码能力训练** — 基于真实面试题生成针对性代码练习，附带多解法分析
3. **系统设计练习** — 经典系统设计场景题，AI 陪你走完设计思路
4. **Mock 面试报告** — 生成模拟面试评估报告，标注薄弱环节

## 工作流编排

```
brave-search          →  搜索最新大厂真题/面经
    ↓
agent-reach           →  抓取 GitHub/LeetCode 热题趋势
    ↓
github-issues-skill   →  创建个人面试题库 Issue（带标签/里程碑）
    ↓
code-review-skill     →  对系统设计答案进行代码审查式评审
    ↓
card-renderer         →  生成面试知识点卡片（供移动端复习）
```

## 使用方式

### 启动面试训练

当你开始准备面试或需要刷题时，说：

> "开始面试训练，准备字节跳动后端岗"

系统会：
1. 用 `brave-search` 搜索近3个月字节/腾讯/阿里面经
2. 用 `agent-reach` 抓取 GitHub "awesome-interview" 和 LeetCode 热题
3. 归类题目到 `数据结构`、`系统设计`、`多线程`、`数据库` 等标签
4. 为每道题创建 GitHub Issue，带题目、考察点、难度星级
5. 用 `card-renderer` 渲染每日复习卡片

### 查看面试题库

> "查看我的面试题库"

系统列出所有已创建的面试 Issue，按难度/标签分类。

### Mock 系统设计

> "Mock 一个分布式 ID 生成系统设计"

AI 以面试官身份提问，引导你完成：
- 需求分析 → 边界确认 → 方案设计 → 权衡取舍
- 结束后给出 `code-review-skill` 风格的评审报告

### 每日练习报告

> "生成今日面试报告"

汇总当日练习情况，生成可视化卡片和薄弱点列表。

## 示例

**输入：** "准备腾讯 T9 后台面试，从系统设计开始"
**输出：**
- 🔍 搜索近90天腾讯后台面经（brave-search）
- 📊 抓取高频系统设计题（agent-reach → GitHub Trending）
- 📝 创建3道系统设计 Issue（github-issues-skill）
- 📋 生成复习计划卡片（card-renderer）
- 🎯 进入 Mock 模式，AI 面试官陪你练题

## 技能依赖

| 技能 | 用途 | 来源 |
|------|------|------|
| brave-search | 搜索大厂面经/真题 | ClawHub |
| agent-reach | 抓取 GitHub/LeetCode 热题 | ClawHub |
| github-issues-skill | 创建/管理面试题库 | ClawHub |
| code-review-skill | 系统设计评审 | ClawHub |
| card-renderer | 生成复习知识卡片 | ClawHub |

## 适用人群

- 应届生准备校招面试
- 社招生跳槽面试
- 技术团队面试官出题参考