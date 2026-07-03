# 🤖 AI Email Agent — 电商客服智能邮件自动回复系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

基于 LLM 的电商客服邮件全自动处理系统。日处理 200+ 封客户邮件，自动分类、情感检测、智能回复、紧急升级。

## ✨ 核心能力

| 模块 | 功能 |
|------|------|
| 📂 **智能分类** | LLM 驱动五分类：咨询/投诉/退换货/合作/垃圾，规则增强校验 |
| 💬 **情感检测** | 五级情感分析 (S0-S4) + 紧急度 1-5 综合评分 |
| 📝 **自动回复** | 多模板 + 个性化变量渲染 + LLM 润色 + 文化适配 |
| 🚨 **升级机制** | 10 条触发规则 + 企微/飞书即时通知 + SLA 倒计时 |
| 🌍 **多语言** | P0-P3 分层策略，覆盖 en/zh/ja/ko/es/fr/de/ar |
| 📚 **知识库** | 关键词 RAG 检索增强咨询类回复 |
| 📊 **监控看板** | Web Dashboard + REST API，实时统计/趋势/升级列表 |

## 🏗 架构

```
IMAP 拉取 → 预处理(去重/过滤) → LLM 分类 → 紧急度评分 → 决策路由
                                              ↓
                              ┌────────────────┼────────────────┐
                              ↓                ↓                ↓
                          自动回复          半自动审核        人工升级
                         (SMTP 发送)       (草稿队列)      (企微通知)
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

```bash
cp .env.example .env
# 编辑 .env，填入 LLM_API_KEY (OpenAI 兼容)
# 编辑 config.yaml，填入 IMAP/SMTP 服务器信息
```

### 3. 运行

```bash
# 演示模式 (模拟 5 封样本邮件，无需真实邮箱)
python main.py demo

# 持续运行 Agent (需配置 IMAP/SMTP)
python main.py run

# 启动 Web 监控看板
python main.py dashboard
# 浏览器打开 http://localhost:8080
```

### 4. 命令列表

| 命令 | 说明 |
|------|------|
| `python main.py demo` | 演示模式，模拟处理 5 封样本邮件 |
| `python main.py run` | 持续运行 Agent 循环 |
| `python main.py once` | 单次拉取处理 |
| `python main.py dashboard` | 启动监控看板 (:8080) |
| `python main.py stats` | 查看工单统计 |
| `python main.py test-send <邮箱>` | 测试 SMTP 配置 |

## 📁 项目结构

```
ai-email-agent/
├── main.py                    # CLI 入口
├── config.yaml                # 主配置文件
├── dashboard.html             # Web 监控看板
├── requirements.txt           # Python 依赖
├── agent/
│   ├── agent_loop.py          # 主 Agent 循环（编排器）
│   ├── email_fetcher.py       # IMAP 邮件获取
│   ├── preprocessor.py        # 预处理（去重/过滤）
│   ├── classifier.py          # LLM 分类器（意图/情感/实体）
│   ├── urgency.py             # 紧急度评分引擎
│   ├── template_engine.py      # 多语言模板渲染
│   ├── sender.py              # SMTP 发送器
│   ├── escalation.py          # 升级引擎 + 通知
│   ├── ticket_db.py           # SQLite 工单数据库
│   ├── knowledge_base.py      # RAG 知识库检索
│   └── config_loader.py       # 配置加载器
├── templates/
│   └── replies.yaml           # 邮件回复模板
└── data/
    ├── faq_zh.md              # 中文 FAQ
    └── faq_en.md              # 英文 FAQ
```

## ⚙️ 分类决策矩阵

```
                紧急度 →
              1(低)    2(一般)   3(中等)   4(高)    5(紧急)
情感↓
S0 积极 │ 自动回复   自动回复   自动回复   自动+抄送  自动+抄送
S1 中性 │ 自动回复   自动回复   自动回复   半自动     半自动
S2 消极 │ 自动+安抚  自动+安抚  半自动     人工       人工
S3 愤怒 │ 半自动     半自动     人工       人工       人工+法务
```

## 📊 升级触发条件

| 条件 | 级别 | 通知 | SLA |
|------|------|------|-----|
| 情感 S3/S4 (愤怒) | P0 | 企微 @值班 + 短信 | 30min |
| 法律威胁关键词 | P0 | 企微 @法务 + 电话 | 15min |
| 安全隐患 | P0 | 企微 @品质总监 + 短信 | 15min |
| 社交媒体扩散威胁 | P1 | 企微 @PR | 1h |
| 24h 内第 3+ 封未解决 | P1 | 企微 @原处理人 | 2h |
| 大额订单 >$1000 + 投诉 | P1 | 企微 @VIP 客服 | 2h |
| 分类置信度 < 0.7 | P2 | 企微群消息 | 4h |
| 合作类 | P2 | 邮件抄送商务 | 24h |

## 🔧 技术栈

- **LLM**: GPT-4o-mini / DeepSeek-V3 (OpenAI 兼容 API)
- **邮件**: IMAP (接收) + SMTP (发送)
- **存储**: SQLite (工单) + YAML (模板/配置)
- **通知**: 企业微信 Webhook / 飞书 Webhook
- **看板**: Chart.js + 原生 HTML/CSS

## 📄 License

MIT
