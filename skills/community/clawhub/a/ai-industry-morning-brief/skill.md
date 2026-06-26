---
name: ai-daily
description: AI 日报 - 自动抓取 LLM/Agent 领域热点信息，生成结构化中文简报。
author: OpenClaw Community
version: 1.0.0
homepage: https://github.com/openclaw/openclaw
triggers:
  - "ai 日报"
  - "ai daily"
  - "生成简报"
  - "大模型日报"
metadata:
  {
    "clawdbot":
      {
        "emoji": "📰",
        "requires": { "bins": ["python3", "curl"] },
        "config":
          {
            "env":
              {
                "TAVILY_API_KEY":
                  {
                    "description": "Tavily API key（用于 X/Twitter 搜索）",
                    "required": false,
                  },
                "GITHUB_TOKEN":
                  { "description": "GitHub Token（可选，提高限流）", "required": false },
              },
          },
      },
  }
---

# AI Daily - AI 大模型日报

自动从多个异构信息源抓取、筛选、提炼大模型（LLM）和智能体（Agent）领域的 Top 级热点信息与核心论文，生成结构化中文简报。

## 命令

### 生成日报
```bash
bash {baseDir}/scripts/generate.sh
bash {baseDir}/scripts/generate.sh --date 2026-02-26
```

### 查看今日简报
```bash
bash {baseDir}/scripts/view.sh today
bash {baseDir}/scripts/view.sh 2026-02-26
```

### 手动触发（通过 OpenClaw）
```
/ai-daily generate
```

## 数据源

### 官方实验室与博客
- OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral AI, Qwen, AWS ML

### 深度技术媒体
- The Batch, Hugging Face, 机器之心，量子位，Distill

### X (Twitter) KOL 追踪
- karpathy, ylecun, _akhaliq 等（通过 Tavily Search）

### 学术论文
- arXiv: cs.CL, cs.AI, cs.LG 分类

## 输出

每日生成 Markdown 格式简报，包含：
1. 📌 核心大事件总结
2. 🏢 官方框架更新
3. 💬 KOL 前沿观点
4. 📚 必读硬核论文

## 配置

编辑 `{baseDir}/config/sources.json` 自定义数据源。

## 定时任务

建议配置每日 08:00 自动执行：
```bash
# crontab -e
0 8 * * * cd /path/to/ai-daily && bash scripts/generate.sh
```

或在 OpenClaw 中使用 cron skill 设置。
