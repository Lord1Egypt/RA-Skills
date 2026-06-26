# AI Daily Skill

获取 **AI 洞察日报** 最新内容，从官方 RSS 源抓取，支持获取最新 N 条，支持推送到多个 webhook 渠道。

## 触发词
ai daily、ai日报、ai daily、每日ai、人工智能日报、ai洞察

## 环境变量配置

```bash
# 多个推送渠道，空格分隔。支持：Bark / 企业微信机器人 / 飞书机器人 / 钉钉机器人 / 通用 webhook
export AI_DAILY_WEBHOOKS="https://api.day.app/your-token https://other-webhook"

# 默认获取最新条数
export AI_DAILY_DEFAULT_COUNT=1

# RSS 源（默认已配置官方源，一般不需要修改）
# export AI_DAILY_RSS_URL="https://justlovemaki.github.io/CloudFlare-AI-Insight-Daily/rss.xml"
```

---

## 使用方式

```bash
# 加载配置
source ~/.openclaw/skills/ai-daily/config.sh

# 获取默认条数（默认 1 条，当日日报）
~/.openclaw/skills/ai-daily/scripts/fetch.sh

# 获取最新 N 条
~/.openclaw/skills/ai-daily/scripts/fetch.sh 5
```

---

## 输出格式

**获取最新 1 条（当日日报）：**
```
**AI 洞察日报 - 2026-03-18**

### 产品与功能更新
- OpenAI 发布推理速度更快的轻量模型
- Midjourney 开启 V8 模型社区测试
- 谷歌 上线 NotebookLM 电影级视频功能
- Gamma 发布 AI 原生设计工具套件
- Lightricks 发布物理级写实视频模型

### 前沿研究
- DeepMind 扩容蛋白质复合物数据库
- AI 通过新框架自主进化出社会规则
- Tether 发布手机端大模型离线训练框架
- Schmidt 悬赏百万美元研究 AI 欺骗行为

### 行业展望与社会影响
- Hugging Face 发布开源趋势研究报告
- 英伟达 发布太空级 AI 基础设施蓝图
- 甲骨文 因 AI 基建成本飙升裁员三万人

```

---

## 说明

- 数据来源：[AI 洞察日报](https://justlovemaki.github.io/CloudFlare-AI-Insight-Daily/rss.xml) by [justlovemaki](https://github.com/justlovemaki)
- RSS 目前为摘要模式，完整内容请点击原文链接查看
- 支持多个推送渠道，自动适配格式

## 更新记录
- 2026-03-18: 初始版本，支持 RSS 抓取、多 webhook 推送
