# AI News Skills 安装指南

请按以下步骤为用户安装 AI News Skills。

## 1. 安装 Agent Reach（前置依赖）

先检查是否已安装：

```bash
command -v agent-reach
```

如果未安装，执行：

```bash
pip install agent-reach
agent-reach install --env=auto
```

安装后验证：

```bash
agent-reach doctor
```

> 如果遇到问题，参考 Agent Reach 官方文档：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md

## 2. 克隆并安装 Skills

```bash
git clone git@github.com:yy4fun/ai-news-skills.git
cd ai-news-skills
./install.sh
```

这会把 `ai_news_fetcher` 和 `ai_news_reporter` 安装到 `~/.openclaw/workspace/skills/`。

## 3. 配置飞书多维表格

```bash
cp ~/.openclaw/workspace/skills/ai_news_fetcher/bitable_target.example.json \
   ~/.openclaw/workspace/skills/ai_news_fetcher/bitable_target.json

cp ~/.openclaw/workspace/skills/ai_news_reporter/bitable_target.example.json \
   ~/.openclaw/workspace/skills/ai_news_reporter/bitable_target.json
```

然后请用户填入飞书多维表格信息（app_name、app_token、table_name、table_id、url）。

## 4. 验证

跑一次单源采集测试，确认管道正常：

```bash
cd ~/.openclaw/workspace/skills/ai_news_fetcher
curl -s "https://r.jina.ai/https://openai.com/zh-Hans-CN/news/" \
  | python3 normalize_agent_reach.py --source "OpenAI新闻"
```

如果输出 JSON 格式的结构化新闻记录（包含 title、url、date 等字段），说明安装成功。

## 完成

告诉用户：
- 安装完成，需要填写 `bitable_target.json` 中的飞书配置
- 之后可以配置 cron 定时采集，先跑 fetcher 采集入表，再跑 reporter 生成日报
