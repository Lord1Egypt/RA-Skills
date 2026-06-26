---
name: ai-news-brief
version: 1.0.3
description: 自动抓取 AI/算力/大模型/GPU 相关最新资讯简报，使用 Chrome 浏览器自动化绕过反爬，支持多个科技媒体来源，支持PDF生成和邮件推送
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python", "chrome"],
        "python_packages": ["requests", "beautifulsoup4", "websocket-client", "fpdf2"]
      },
      "install": [
        {
          "id": "python_deps",
          "kind": "pip",
          "packages": ["requests", "beautifulsoup4", "websocket-client", "fpdf2"],
          "label": "安装 Python 依赖"
        },
        {
          "id": "chrome",
          "kind": "system",
          "label": "Chrome 浏览器 (系统已有)"
        }
      ],
      "autoInstall": true
    }
  }
---

# AI 资讯简报

> 自动抓取国内外 AI/算力/大模型/GPU/芯片相关最新资讯，生成简报

---

## 📊 网站配置管理

本 Skill 使用配置文件管理各网站的获取方式，文件位于 `scripts/sites_config.json`。

### 获取方式优先级

| 方式 | 说明 | 速度 |
|------|------|------|
| **rss** | RSS订阅，最快最稳定 | ⚡⚡⚡ |
| **http** | HTTP直接请求 | ⚡⚡ |
| **chrome** | Chrome CDP自动化 | ⚡ |

### 状态说明

- **working**: 正常工作
- **failed**: 之前失败，暂不尝试
- **unreachable**: 网站无法访问

### 自动调度逻辑

```
1. 读取 sites_config.json 配置文件
2. 对每个网站，按 priority 顺序尝试：
   - 首选：优先级最高且状态为 working 的方式
   - 备选：如果首选失败，尝试其他可用的方式
3. 抓取完成后，自动更新各方式的状态到配置文件
4. 下次运行时，使用更新后的配置
```

### 手动更新配置

如需手动更新网站配置，可编辑 `scripts/sites_config.json`：

```json
{
  "sites": {
    "网站key": {
      "name": "网站名",
      "url": "主页面URL",
      "rss": "RSS地址",
      "http": "HTTP地址",
      "chrome": "Chrome地址",
      "priority": ["rss", "http", "chrome"],
      "status": {
        "rss": "working/failed/unreachable",
        "http": "working/failed/unreachable", 
        "chrome": "working/failed/unreachable"
      }
    }
  }
}
```

---

## 🎯 用户反馈和关键词优化

本 Skill 支持根据用户反馈调整获取的资讯内容。

### 用户反馈方式

当用户给出以下反馈时，系统会自动调整：

| 用户输入 | 系统行为 |
|----------|----------|
| "我喜欢GPU/显卡相关" | 添加关键词 `gpu`, `显卡`, `nvidia` |
| "不喜欢自动驾驶" | 排除关键词 `自动驾驶`, `智驾` |
| "想看华为昇腾" | 添加关键词 `华为`, `昇腾` |
| "不要抖音字节" | 屏蔽来源 `字节`, `抖音` |

### 配置文件

用户配置保存在 `scripts/user_config.json`：

```json
{
  "user_preferences": {
    "liked_keywords": ["gpu", "华为"],
    "disliked_keywords": ["自动驾驶"],
    "liked_sources": [],
    "disliked_sources": []
  },
  "default_keywords": {
    "AI基础": ["ai", "人工智能", "大模型", "gpt", ...],
    "GPU硬件": ["gpu", "nvidia", "amd", "cuda", ...],
    ...
  }
}
```

### 关键词分类

| 分类 | 关键词示例 |
|------|------------|
| AI基础 | ai, 人工智能, 大模型, gpt, llm, openai |
| GPU硬件 | gpu, nvidia, amd, intel, cuda, h100 |
| 算力芯片 | 算力, 芯片, 半导体, 处理器, cpu, npu |
| 自动驾驶 | 自动驾驶, 智能驾驶, 特斯拉, fsd |
| 大厂动态 | 华为, 昇腾, 阿里, 百度, 字节, 腾讯 |

---

## 🔍 内容可信度验证

每条资讯都会经过可信度评估，帮助用户判断信息质量。

### 可信度等级

| 等级 | 分数 | 说明 | 来源示例 |
|------|------|------|----------|
| **A级** | 90+ | 权威来源，可信度最高 | TechCrunch, The Verge, 政府官网 |
| **B级** | 70-89 | 专业媒体，可信度较高 | 36kr, 量子位, 虎嗅, 爱范儿 |
| **C级** | 50-69 | 一般来源，需核实 | HackerNews, 综合新闻 |
| **D级** | <50 | 较低可信，仅供参考 | 论坛, 自媒体 |

### 验证规则

1. **来源可信度** - 根据来源类型给基础分
2. **内容长度** - 超过200字 +10分
3. **敏感词检测** - 含"谣言""震惊"等词 -15分
4. **时效性** - 有日期标注 +5分

### 使用可信度过滤

```bash
# 至少B级可信度
python fetch_ai_news.py --min-credibility B

# 至少70分
python fetch_ai_news.py --min-score 70
```

### 输出示例

```json
{
  "title": "OpenAI新模型曝光",
  "source": "量子位",
  "credibility": {
    "score": 80,
    "level": "B",
    "reasons": ["权威来源", "内容详细"]
  }
}
```

---

## 🔥 热点排序

资讯按热点程度排序，GPU相关资讯权重最高：

### 关键词热度权重

| 类别 | 关键词 | 权重 |
|------|--------|------|
| 🟢 **GPU/显卡** | gpu, nvidia, amd, h100, 4090, 5090, RTX | 15 (最高) |
| 🔵 **大模型** | 大模型, llm, gpt, openai, claude, deepseek, moE | 12 |
| 🟡 **AI基础** | ai, 人工智能, 模型, 训练, 推理 | 10 |
| 🟠 **芯片/算力** | 算力, 芯片, 半导体, npu, 华为, 昇腾 | 10 |
| 🔴 **自动驾驶** | 自动驾驶, 智驾, 特斯拉, fsd | 8 |

### 排序规则

1. **关键词热度** - 匹配热门关键词越多，分数越高
2. **可信度等级** - A级来源 +10分，B级 +8分
3. **内容详细度** - 摘要超过100字 +3分
4. **关键点数量** - 有2个以上关键点 +2分

---

## 🔄 智能重试机制

当某个获取方式失败时：

| 失败次数 | 处理方式 |
|----------|----------|
| 第1-2次 | 继续重试（最多2次） |
| 3次以上 | 自动降低该方式优先级 |
| 后续 | 跳过该方式，尝试其他方式 |

### 失败记录

失败记录保存在 `scripts/failure_log.json`：
- 记录每个网站每种方式的失败次数
- 每天自动重置
- 影响排序优先级

---

## 🧹 智能去重

使用标题相似度算法去除重复文章：

| 相似度 | 处理 |
|--------|------|
| ≥0.6 | 视为重复，保留可信度高的 |
| <0.6 | 视为不同文章 |

相似度检测基于：
- 共同关键词（中文词组、英文单词）
- 核心词匹配（GPT、RTX、AI等）
- 字符重叠率

---

## 📊 政策资讯

Skill 支持抓取政府官网的政策通知：

### 来源列表

| 来源 | 类别 | 说明 |
|------|------|------|
| 中国政府网 | 中央政策 | 国务院、部委重要政策 |
| 工信部 | 部委政策 | 工业和信息化相关 |
| 科技部 | 部委政策 | 科技创新、项目申报 |
| 网信办 | 部委政策 | 网络安全、AI监管 |
| 发改委 | 部委政策 | 项目批复、产业政策 |
| 教育部 | 部委政策 | AI教育相关 |
| 财政部 | 部委政策 | 补贴、专项资金 |
| 国家数据局 | 新机构 | 数据、AI政策 |

### 使用方式

在获取AI资讯时，可选择是否同时获取政策资讯：
- 自动获取：每天定时任务会同时抓取AI资讯和政策

---

## 📈 增量抓取与数据持久化

### 增量抓取

- 首次运行：获取全部内容
- 后续运行：只获取新增内容
- 自动去重：已抓取的文章不会重复

### 数据保存

| 类型 | 文件 | 位置 |
|------|------|------|
| AI资讯历史 | `news_history.json` | `scripts/data/` |
| 政策资讯历史 | `policy_history.json` | `scripts/data/` |

### 查询历史

```bash
# 查询最近3天的资讯
python scripts/incremental_fetch.py --days 3

# 查看统计
python scripts/incremental_fetch.py --stats
```

---

## 🤖 AI摘要生成（可选）

使用大模型为文章生成更好的摘要：

### 配置

文件：`scripts/llm_config.json`

```json
{
  "config": {
    "enabled": true,
    "provider": "deepseek",  // deepseek / qwen / openai
    "deepseek": {
      "api_key": "your_api_key"
    }
  }
}
```

### 支持的模型

| 服务商 | 模型 | 特点 |
|--------|------|------|
| DeepSeek | deepseek-chat | 便宜量大 |
| 阿里Qwen | qwen-plus | 有免费额度 |
| OpenAI | gpt-3.5-turbo | 稳定性好 |

### 使用

```bash
python scripts/llm_summarizer.py
```

---

## 📄 自动报告生成

每天自动生成资讯报告：

### 支持格式

- **HTML报告** - 可在浏览器查看，包含样式
- **Markdown报告** - 便于分享和编辑
- **PDF报告** - 支持中文，样式整洁（新增）

### 输出位置

```
scripts/reports/
├── ai_news_20260406.html
├── ai_news_20260406.md
└── ai_news_20260406.pdf
```

### PDF 生成

需要安装 fpdf2：
```bash
pip install fpdf2
```

在 `pdf_config.json` 中启用：
```json
{
  "config": {
    "enabled": true,
    "output_dir": "./reports"
  }
}
```

### 生成报告

```bash
python scripts/report_generator.py
```

---

## 🌐 多语言翻译（预留接口）

翻译英文AI资讯为中文：

### 配置

文件：`scripts/translator_config.json`

```json
{
  "config": {
    "enabled": true,
    "provider": "baidu"  // baidu / deep
  }
}
```

### 注意

- 需要配置翻译API才能使用
- 目前是预留接口，需要开发者自行接入

---

## 📧 邮件推送（可选）

Skill 支持将简报发送到邮箱，需要使用者自行配置。

### ⚠️ 重要：配置存放位置

为防止项目更新时覆盖用户配置，请按以下步骤配置：

1. **创建配置目录**（如果不存在）：
   - Windows: `C:\Users\你的用户名\.openclaw\config\`
   - macOS/Linux: `~/.openclaw/config/`

2. **复制配置模板**：将 `scripts/email_config.json.default` 复制到上述目录，并重命名为 `ai-news-email.json`

3. **填写配置**：编辑 `ai-news-email.json`，填写你的邮箱信息

### 配置步骤

1. 创建目录：`~/.openclaw/config/`
2. 复制模板：
   ```bash
   # Windows
   copy scripts\email_config.json.default %USERPROFILE%\.openclaw\config\ai-news-email.json
   
   # macOS/Linux
   cp scripts/email_config.json.default ~/.openclaw/config/ai-news-email.json
   ```
3. 编辑 `ai-news-email.json`，设置 `smtp_config.enabled: true`，填写发件人邮箱和授权码
4. 设置 `recipient_config.enabled: true`，添加收件人邮箱

### 配置示例

```json
{
  "smtp_config": {
    "enabled": true,
    "smtp_server": "smtp.qq.com",
    "smtp_port": 465,
    "use_ssl": true,
    "sender_email": "your_email@qq.com",
    "sender_password": "your_auth_code",
    "sender_name": "AI资讯小助手"
  },
  "recipient_config": {
    "enabled": true,
    "recipients": ["your_email@example.com"]
  }
}
```

### 支持的邮箱

| 邮箱 | SMTP服务器 | 端口 | 授权码获取 |
|------|-----------|------|----------|
| QQ邮箱 | smtp.qq.com | 465 | 邮箱设置→账户→开启IMAP |
| 163邮箱 | smtp.163.com | 465 | 邮箱设置→POP3/SMTP |
| Gmail | smtp.gmail.com | 465 | Google账户→安全→应用密码 |

### 测试邮件

```bash
python scripts/email_sender.py
```

### ⏰ 定时发送（手动添加）

定时任务需要在 OpenClaw 中手动添加，步骤如下：

#### 1. 添加早间任务（每天 7:00）

```bash
openclaw cron add --name "AI资讯简报-早间版" \
  --schedule "0 7 * * *" \
  --agent main \
  --message "请运行 AI 资讯简报技能，获取昨日7点至今日7点的AI/算力/GPU/政策资讯，生成简报，并自动生成 PDF 附件发送到配置好的邮箱" \
  --delivery wechat
```

#### 2. 添加午间任务（每天 14:00）

```bash
openclaw cron add --name "AI资讯简报-午间版" \
  --schedule "0 14 * * *" \
  --agent main \
  --message "请运行 AI 资讯简报技能，获取今日最新的AI/算力/GPU/政策资讯，生成简报，并自动生成 PDF 附件发送到配置好的邮箱" \
  --delivery wechat
```

#### 3. 查看和管理定时任务

```bash
# 查看所有定时任务
openclaw cron list

# 删除定时任务
openclaw cron rm <任务ID>

# 立即运行定时任务（测试）
openclaw cron run <任务ID>
```

> **注意**：定时任务由 OpenClaw 管理，不是 Skill 代码的一部分。如果需要修改或删除定时任务，请使用上述命令。

---

## 📁 项目结构

```
ai-news-brief/
├── SKILL.md                    # Skill 定义文件
├── scripts/                    # 代码文件（更新时会被覆盖）
│   ├── *.py                   # 功能代码
│   └── *.json.default         # 默认配置模板（只读，不要修改）
├── user_config/               # ⚠️ 已弃用，请使用外部配置
│   └── *.json                 # 历史配置（不再使用）
└── data/                      # 数据缓存（不会被覆盖）

# 👇 用户配置存放位置（项目外，更新时不会被覆盖）
~/.openclaw/config/
├── ai-news-email.json         # 邮件配置
├── ai-news-llm.json           # LLM API 配置
├── ai-news-pdf.json           # PDF 配置
├── ai-news-user.json          # 用户偏好
└── ai-news-sites.json         # 网站配置
```

### ⚠️ 重要：为什么配置放项目外？

- 项目更新时会覆盖 `scripts/` 目录下的所有文件
- 如果配置放在项目内，更新后会被覆盖
- 因此，**用户配置必须放在 `~/.openclaw/config/` 目录**

### 配置流程

1. 首次使用：从 `scripts/*.json.default` 复制模板到 `~/.openclaw/config/`
2. 编辑配置：填写自己的邮箱、API密钥等
3. 后续更新：项目代码会更新，但你的配置不会受影响

### 方式一：自动安装（推荐）

首次使用前，可选择自动安装依赖。**AI 会询问你是否安装**：

```
我需要安装一些依赖才能运行：
- requests, beautifulsoup4, websocket-client (Python 包)

是否现在安装？请回复"是"或"安装"
```

### 方式二：手动安装

在终端运行：
```bash
pip install requests beautifulsoup4 websocket-client
```

### 环境要求

- Python 3.8+
- Chrome 浏览器（已安装在系统中）
- Windows/macOS/Linux 均可

---

## 📋 功能说明

### 核心能力

1. **Chrome 自动化抓取** - 使用 Chrome DevTools Protocol (CDP) 绕过反爬
2. **多源资讯聚合** - 同时抓取 20+ 个科技媒体网站
3. **智能关键词过滤** - 仅保留 AI/算力/GPU/大模型 相关内容
4. **自动摘要提取** - 从文章页面提取关键信息
5. **来源多样化** - 国内+国外，确保资讯全面

### 抓取来源

#### 国内
- 36kr、量子位、机器之心、虎嗅、爱范儿、极客公园
- 网易科技、新浪科技、搜狐科技、腾讯科技、凤凰网科技
- 驱动之家、超能网、中关村在线、快科技

#### 国外
- TechCrunch、The Verge、VentureBeat、HackerNews

---

## 🎯 触发方式

当用户说出以下关键词时激活：

- "最新AI资讯"
- "AI新闻"
- "算力新闻"
- "GPU资讯"
- "大模型动态"
- "AI简报"
- "科技资讯"

---

## 📊 输出格式

### 标准简报

```markdown
# 🤖 AI/算力/GPU 资讯简报

**查询日期**: 2026年4月6日
**数据范围**: 2026年4月5日

---

### 🔥 重点新闻

| 来源 | 标题 | 概要 |
|------|------|------|
| 36kr | 标题 | 概要... |
| 量子位 | 标题 | 概要... |

---

### 📊 来源分布

| 来源 | 数量 |
|------|------|
| 36kr | 10条 |
| 搜狐科技 | 8条 |

---

### 💡 趋势总结

1. 趋势1...
2. 趋势2...

---
```

---

## 🔧 工作流程

```
Phase 1: 启动 Chrome
  └─ 检查 Chrome 是否已运行，若无则启动
      ↓
Phase 2: 多源抓取
  └─ 依次访问20+网站，获取文章标题和链接
      ↓
Phase 3: 内容过滤
  └─ 过滤保留 AI/算力/GPU 相关内容
      ↓
Phase 4: 摘要提取
  └─ 打开每篇文章，获取内容摘要（仅处理前15条）
      ↓
Phase 5: 整理输出
  └─ 分类、去重、生成简报
```

---

## ⚡ 使用示例

### 示例1：用户查询

**用户**: "最新AI资讯"

**AI**: \[自动执行以下操作]
1. 启动/连接 Chrome
2. 抓取各网站资讯
3. 提取文章摘要
4. 生成简报输出

---

## ⚠️ 注意事项

1. **首次使用需安装依赖** - AI 会询问是否安装
2. **首次会打开 Chrome** - 首次运行时 Chrome 窗口会打开
3. **运行时间** - 完整抓取约需 2-3 分钟
4. **网络要求** - 需能访问国内科技网站
5. **Chrome 保持打开** - 运行后 Chrome 会保持打开状态，便于后续快速运行

---

## 🔄 更新日志

### 2026-04-06 (v1.0)

- 初始版本
- 支持 Chrome 自动化抓取
- 支持 20+ 科技媒体来源
- 自动提取文章摘要
- 提供来源分布统计

---

## 📞 支持

如遇问题，请检查：
1. Python 3.8+ 已安装
2. Chrome 浏览器已安装
3. 依赖包已安装（requests, beautifulsoup4, websocket-client）
4. 网络可以访问目标网站