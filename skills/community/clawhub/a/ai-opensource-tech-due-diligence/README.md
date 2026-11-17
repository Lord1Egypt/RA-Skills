# AI 开源项目技术尽调与公众号内容自动化

> GitHub Trending 热门项目监控 → 技术深度分析 → 公众号文章生成与发布 → 飞书知识库沉淀

## 📌 业务场景

**目标用户**：技术博主、开发者布道师、创业公司 CTO、技术自媒体从业者

**核心痛点**：
- 想写技术公众号文章，但研究+写作耗时太长，难以坚持更新
- GitHub Trending 太多，看不完，不知道哪些项目值得深入分析
- 好内容分散在代码、Issue、README 中，难以系统性提取
- 文章发布后没有形成知识积累，下次重新研究同样费时费力

## 🎯 Combo 目标

一条完整流水线：**发现值得分析的项目 → 深度技术研究 → 生成高质量公众号文章 → 沉淀为组织知识**

## 🔧 Skill 编排图谱

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Trending / 指定仓库               │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │     Agent-Reach          │
              │  抓取 Trending 列表       │
              │  读取仓库 README/Issue   │
              │  收集 star/贡献者数据     │
              └────────────┬────────────┘
                           │ 原始项目数据
              ┌────────────▼────────────┐
              │   tech-article-pro      │
              │  技术深度分析            │
              │  架构解析+代码实现+       │
              │  竞品对比+趋势判断       │
              └────────────┬────────────┘
                           │ 技术分析报告
              ┌────────────▼────────────┐
              │  wechat-article-pro    │
              │  公众号长文生成          │
              │  3000-5000字            │
              │  机器之心/InfoQ 风格     │
              └────────────┬────────────┘
                           │ 可发布文章
         ┌────────────────┴────────────────┐
         │                                     │
  ┌──────▼──────┐                  ┌─────────▼────────┐
  │飞书知识库沉淀 │                  │   公众号发布      │
  │feishu-create │                  │ (wechat后台)     │
  │  -doc        │                  └──────────────────┘
  └──────────────┘
```

## 📦 包含 Skills

| Skill | 来源 | 作用 |
|-------|------|------|
| Agent-Reach | workspace skills | GitHub Trending 抓取 + 仓库页面读取 |
| tech-article-pro | workspace skills | 技术深度分析，机器之心/InfoQ 风格 |
| wechat-article-pro | workspace skills | 公众号长文生成与发布 |
| feishu-create-doc | plugin-skills | 飞书知识库文档创建与同步 |

## 💡 使用示例

### 场景一：分析今日 GitHub Trending Python 热门项目

```
用户：帮我分析今天 GitHub Trending 上 Python 项目的热门项目，写一篇技术公众号文章

执行流程：
1. Agent-Reach 抓取今日 Python Trending 列表
2. 选取排名第一的项目进行深度分析
3. tech-article-pro 生成技术深度报告
4. wechat-article-pro 生成 3000-5000 字公众号长文
5. feishu-create-doc 同步至飞书知识库
```

### 场景二：指定仓库技术尽调

```
用户：对 https://github.com/xxx/yyy 做一次完整技术尽调

执行流程：
1. Agent-Reach 读取仓库 README、Issue、Star 趋势
2. tech-article-pro 从架构、技术原理、性能、社区生态多维度分析
3. 生成结构化技术报告
4. wechat-article-pro 生成公众号风格文章
5. feishu-create-doc 沉淀至知识库
```

### 场景三：多仓库横向对比

```
用户：帮我对比分析 langchain 和 langgraph 两个项目的技术架构

执行流程：
1. Agent-Reach 同时抓取两个仓库的完整数据
2. tech-article-pro 生成对比分析报告
3. wechat-article-pro 生成竞品对比文章
4. feishu-create-doc 沉淀至知识库
```

## 📋 前置配置

### 1. Agent-Reach 配置
```bash
agent-reach doctor  # 检查 GitHub 频道状态
```

### 2. 飞书机器人权限
- 云文档创建权限
- 知识库节点访问权限（可选）

### 3. 微信公众号后台
- AI 配图功能已开通（用于自动生成封面）

## 🔄 工作流参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `repo` | 目标仓库（owner/repo 格式） | - |
| `source` | 数据来源：`trending` 或 `repo` | `repo` |
| `language` | GitHub Trending 语言筛选 | `all` |
| `since` | Trending 周期：`daily` / `weekly` / `monthly` | `daily` |
| `word_count` | 公众号文章目标字数 | 4000 |
| `compare` | 是否开启多仓库对比模式 | `false` |

## 📁 生成文件说明

每次执行会生成以下文件（保存在工作目录）：

- `tech-report-{repo}-{date}.md` — 技术深度分析报告
- `wechat-article-{repo}-{date}.md` — 公众号可发布文章
- `feishu-doc-{repo}-{date}.md` — 飞书文档内容备份

## 🚀 扩展用法

### 定时监控模式

通过 cron 设置每日自动执行：

```
# 每天早上 9:00 分析昨日 GitHub Trending Python 热门项目
openclaw cron add \
  --name "每日 GitHub Trending Python 技术分析" \
  --schedule "0 9 * * *" \
  --skill ai-opensource-tech-due-diligence \
  --params '{"source": "trending", "language": "python", "publish": true}'
```

### 系列文章模式

针对某一技术领域（如 AI Agent、大模型推理优化），连续多周追踪分析多个相关项目，形成系列技术文章。

## ⚠️ 注意事项

1. GitHub API 有速率限制，建议配置 GitHub Token 以提高抓取稳定性
2. 技术分析深度取决于输入数据丰富度，建议开启 Issue 和 Star 历史抓取
3. 公众号 AI 配图功能需在微信公众号后台开通
4. 飞书文档默认在「我的空间」创建，可在 workflow.json 中指定知识库节点

## 📞 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| Agent-Reach 无法抓取 GitHub | 未配置 GitHub Token | 运行 `agent-reach configure github` |
| 技术分析内容太少 | 仓库数据量不足 | 增加 `--include-issues --include-stars` 参数 |
| 公众号配图失败 | AI 配图功能未开通 | 手动上传封面图，跳过自动配图步骤 |
| 飞书文档创建失败 | 机器人权限不足 | 在飞书管理后台确认机器人文档权限 |
