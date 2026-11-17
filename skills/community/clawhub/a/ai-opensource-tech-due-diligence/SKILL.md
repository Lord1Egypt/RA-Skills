---
name: ai-opensource-tech-due-diligence
description: AI 开源项目技术尽调与公众号内容自动化 — GitHub Trending 监控 + 技术深度分析 + 公众号文章生成与发布
category: AI
triggers: 开源项目分析, GitHub技术尽调, 技术公众号文章, 开源项目解读, 生成技术文章, GitHub Trending分析
---

# AI 开源项目技术尽调与公众号内容自动化

> GitHub Trending → 技术深度分析 → 公众号长文 → 知识库沉淀

## 🎯 解决痛点

- ❌ 每天刷 GitHub Trending 太耗时，不知道哪些项目值得深入
- ❌ 想写技术公众号文章，但研究+写作耗时太长难以坚持
- ❌ 好内容分散在代码、Issue、README 中，难以系统性提取
- ❌ 文章写完没有形成知识积累，下次重新研究费时费力

## 💡 解决方案

```
GitHub Trending（今日热门项目）
        ↓
┌─────────────────────────┐
│  Agent-Reach             │ → 抓取 Trending 列表 + 指定仓库页面
└───────────┬─────────────┘
            │ 项目列表 + 仓库数据
     ┌──────▼──────┐
     │  tech-article-pro │ → AI 技术深度分析，生成结构化技术解析
     └──────┬──────┘
            │ 技术分析报告
     ┌──────▼──────────────┐
     │ wechat-article-pro  │ → 适配公众号风格，生成3000-5000字长文
     └──────┬──────────────┘
            │ 公众号文章
     ┌──────▼──────────┐
     │ feishu-create-doc │ → 同步至飞书知识库，形成知识沉淀
     └──────────────────┘
```

## 📦 编排 Skills

| Skill | 作用 | 调用时机 |
|-------|------|---------|
| Agent-Reach | 抓取 GitHub Trending + 读取仓库详情页 | Step 1 |
| tech-article-pro | 技术深度分析，生成结构化技术报告 | Step 2 |
| wechat-article-pro | 适配公众号风格，生成可发布长文 | Step 3 |
| feishu-create-doc | 同步技术报告至飞书知识库 | Step 4 |

## 🔧 前置要求

1. **Agent-Reach**：已安装并配置 GitHub 频道
2. **tech-article-pro**：联网搜索权限（web_search/web_fetch）
3. **wechat-article-pro**：微信公众号后台 AI 配图功能
4. **feishu-create-doc**：飞书机器人文档创建权限

## 📝 使用方法

### 触发方式

```
/ai-opensource-tech-due-diligence
帮我分析这个GitHub项目
生成这个仓库的技术文章
对 [repo] 做一个技术尽调
```

### 手动执行

```bash
# 方式1：输入 GitHub 仓库 URL，直接生成技术文章
openclaw run ai-opensource-tech-due-diligence --repo owner/repo-name

# 方式2：分析今日 GitHub Trending 热榜
openclaw run ai-opensource-tech-due-diligence --source trending --language python

# 方式3：分析多个仓库并生成对比文章
openclaw run ai-opensource-tech-due-diligence --repos owner/repo1 owner/repo2 --compare
```

## 🔄 工作流详情

### Step 1: Agent-Reach 抓取项目数据

```yaml
步骤: 1
技能: Agent-Reach
输入:
  模式: 仓库分析
  任务:
    - 获取 GitHub Trending 列表（语言: python, 周期: 今日）
    - 获取指定仓库的 README、star 数、贡献者、主要 Issue
  sources:
    - type: github_trending
      params:
        language: ${language: all}
        since: daily
    - type: github_repo
      params:
        owner: ${owner}
        repo: ${repo}
输出:
  trending_repos: ${list.json}
  repo_data: ${readme + issues + contributors}
```

### Step 2: tech-article-pro 技术深度分析

```yaml
步骤: 2
技能: tech-article-pro
输入:
  主题: "${repo_name} 技术深度解析"
  数据源: ${repo_data}
  分析维度:
    - 架构设计：核心模块、代码结构
    - 技术原理：关键技术选型、算法实现
    - 性能评估：基准测试、优化手段
    - 社区生态：star 趋势、活跃度、贡献者质量
    - 竞品对比：同类开源项目横向对比
  写作风格: 机器之心/InfoQ 硬核技术风
  技术标签: ["架构", "代码实现", "技术原理"]
输出:
  tech_report: ${analysis.md}
  key_insights: ${insights.json}
```

### Step 3: wechat-article-pro 生成公众号文章

```yaml
步骤: 3
技能: wechat-article-pro
输入:
  主题: "${repo_name} 技术解析 | ${一句话概括亮点}"
  技术报告: ${tech_report}
  字数: 3000-5000
  风格: 刘润公众号叙事风格（技术故事切入）
  必含要素:
    - 技术原理（代码示例 ≥4处）
    - 使用场景
    - 竞品对比
    - 未来展望
输出:
  article: ${article.md}
  cover_prompt: ${cover_image_prompt}
```

### Step 4: feishu-create-doc 知识库沉淀

```yaml
步骤: 4
技能: feishu-create-doc
输入:
  标题: "【技术尽调】${repo_name} | ${date}"
  内容: ${tech_report}
  格式: markdown
  位置: 我的空间 或 指定知识库节点
输出:
  doc_url: ${feishu_doc_url}
  doc_id: ${doc_id}
```

## 📊 输出示例

### 生成的文章结构

```markdown
# ${repo_name} 深度解析：一个改变 ${场景} 的开源项目

## 开篇：一个真实的技术痛点

[从真实使用场景或 Issue 中提取的故事切入]

## 一、技术架构解析

[核心模块架构图 + 代码实现细节]

### 1.1 核心机制
```python
# 关键代码实现
def core_function():
    ...
```

### 1.2 性能优化手段
[benchmark 数据 + 分析]

## 二、为什么它值得关注

[从 star 趋势、作者背景、技术创新性角度分析]

## 三、同类项目横向对比

| 维度 | ${repo} | 竞品A | 竞品B |
|------|---------|-------|-------|
| 性能 | ... | ... | ... |
| 易用性 | ... | ... | ... |
| 生态 | ... | ... | ... |

## 四、适用场景与局限

[明确适用场景 + 已知局限]

## 五、技术趋势判断

[从架构设计判断未来技术走向]

---
*由 AI 开源技术尽调工作流自动生成 | ${date}*
```

## ⚙️ 自定义配置

### 修改分析维度

编辑 `workflow.json`：

```json
{
  "analysis_dimensions": [
    "架构设计",
    "技术原理",
    "性能评估",
    "社区生态",
    "竞品对比",
    "安全审计"
  ]
}
```

### 修改公众号风格

```json
{
  "wechat_style": "tech",
  "word_count_target": 4500,
  "code_examples_min": 4
}
```

## 🔒 安全说明

- 所有抓取内容仅用于技术学习与分享
- 尊重开源许可证，不要传播受版权保护的内容
- 飞书文档权限默认为创建者可见

## ⚠️ 注意事项

1. **GitHub API 限制**：建议添加 GitHub Token 避免 API 限流
2. **技术深度**：tech-article-pro 强制要求技术内容占比 ≥70%
3. **公众号配图**：wechat-article-pro 会调用公众号 AI 配图功能
4. **知识沉淀**：建议开启 Step 4，将每次分析结果沉淀为组织知识

## 📞 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 抓取仓库为空 | 仓库不存在或 private | 确认 URL 正确性 |
| 技术分析深度不足 | 输入数据太少 | 增加 Issue/PR 数据抓取 |
| 公众号配图失败 | 后台 AI 功能未开通 | 手动上传封面图 |
| 飞书创建失败 | 权限不足 | 确认机器人文档权限 |
