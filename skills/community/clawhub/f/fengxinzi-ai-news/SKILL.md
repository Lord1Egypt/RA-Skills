---
name: ai-news-generator
description: |
  AI资讯推送技能 - 根据SOP生成高价值AI资讯报告
  自动抓取过去24小时内的AI热点，生成结构化深度分析
version: 1.0.0
license: MIT
author: fengxinzi_pm
tags:
  - AI
  - 资讯
  - 日报
  - 自动化
---

# ai-news-generator

> AI资讯推送技能 - 根据SOP v2.0生成高价值AI资讯报告

---

## 触发词

- "生成AI资讯"
- "抓取AI资讯"
- "AI资讯推送"
- "每日AI资讯"
- "AI日报"

---

## 功能说明

根据定义的SOP，自动抓取过去24小时内最值得报道的AI资讯，生成结构化报告并保存到Get笔记。

### 核心流程

1. **精准抓取**：使用多种搜索工具抓取热点
2. **深度降噪**：深入阅读原文，过滤PR通稿
3. **格式化输出**：按Markdown模板输出

### 搜索工具优先级

| 优先级 | 工具 | 用途 |
|--------|------|------|
| 1 | ddgs | 全网搜索 |
| 2 | felo-x-search | Twitter/X实时 |
| 3 | web_fetch | 读取原文内容 |

### 内容维度（每类至少1条，共10条）

| 维度 | 关键词示例 | 筛选标准 |
|------|-----------|----------|
| 🔥 行业核弹 | AI GPT Claude 大模型更新 巨头战略 | 有外媒/大佬第一手评价 |
| 💻 硬核开源/神器 | GitHub trending AI tool 霸榜 | 解决技术痛点，有实际效果 |
| 🧠 深度观点/论文 | AI research 顶会 行业领袖推文 | 有核心insight，可延展讨论 |

---

## 输出格式

每条资讯包含：

```markdown
## [序号]. [维度] 标题

**一句话懂它**: [15字以内]

**核心信息提取**:
> * [技术突破/功能亮点]
> * [对比优势/数据]
> * [使用门槛/开源情况]

**博主创作视角**: [解读切入点、值得聊的话题、争议点]

**来源溯源**: [原文链接]
```

### 输出元信息

- 标题: `[AI资讯] YYYY-MM-DD`
- 存储: Get笔记
- 标签: AI, 资讯, 每日汇总

---

## 环境配置

### 1. 安装依赖

```bash
# 安装搜索工具
npm install -g ddgs

# 或使用pnpm
pnpm add -g ddgs
```

### 2. 配置环境变量

```bash
# 创建配置目录
mkdir -p ~/.config/ai-news-generator

# 创建环境变量文件
cat > ~/.config/ai-news-generator/.env << 'EOF'
# Get笔记配置
GETNOTE_API_KEY="your_getnote_api_key"
GETNOTE_CLIENT_ID="your_getnote_client_id"
EOF

# 设置权限
chmod 600 ~/.config/ai-news-generator/.env
```

### 3. 获取API Key

**Get笔记**:
1. 访问 https://open.getnote.cn/
2. 登录后进入开发者中心
3. 创建应用获取 API Key 和 Client ID

---

## 使用示例

### 命令行执行

```bash
# 执行AI资讯生成
bash /path/to/ai-news-generator/scripts/generate.sh
```

### 对话触发

```
Boss: 生成今天的AI资讯
→ AI: 开始抓取...
→ AI: 已生成10条高价值资讯，已保存到Get笔记
```

### 定时任务

```bash
# 添加到crontab
crontab -e

# 每天8点执行
0 8 * * * /path/to/ai-news-generator/scripts/generate.sh >> /path/to/logs/ai-news.log 2>&1
```

---

## 配置文件

### keywords.json - 搜索关键词

位置: `config/keywords.json`

```json
{
  "行业核弹": [
    "AI GPT Claude 大模型 更新",
    "OpenAI Google Anthropic 战略"
  ],
  "硬核开源": [
    "GitHub trending AI 工具",
    "开源 AI 模型 本地部署"
  ],
  "深度观点": [
    "AI 趋势 报告 2026",
    "AI research 顶会"
  ]
}
```

---

## 目录结构

```
ai-news-generator/
├── SKILL.md              # 技能定义
├── scripts/
│   └── generate.sh       # 执行脚本
└── config/
    └── keywords.json     # 搜索关键词
```

---

## 依赖工具

| 工具 | 用途 | 安装 |
|------|------|------|
| ddgs | 全网搜索 | `npm i -g ddgs` |
| felo-x-search | Twitter搜索 | 见对应skill |
| web_fetch | 读取网页 | OpenClaw内置 |
| curl | HTTP请求 | 系统自带 |
| python3 | JSON处理 | 系统自带 |

---

## 常见问题

### Q: 搜索没有结果？
A: 检查ddgs是否正确安装，尝试手动执行 `ddgs text -q "关键词"`

### Q: Get笔记保存失败？
A: 确认API Key和Client ID正确，网络能访问open.getnote.cn

### Q: 内容太少？
A: 调整config/keywords.json中的搜索关键词

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-21 | 初始版本 |

---

## 作者

fengxinzi_pm (疯信子项目总监)

---

*本技能基于SOP v2.0设计*
