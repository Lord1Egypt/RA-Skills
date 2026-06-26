---
name: moltbook-generator
description: |
  Moltbook日报技能 - 收集AI Agent社交网络热门内容，生成深度分析报告
  自动抓取Moltbook热门内容，过滤去重后添加AI深度分析
version: 1.0.0
license: MIT
author: fengxinzi_pm
tags:
  - Moltbook
  - AI
  - 日报
  - 自动化
---

# moltbook-generator

> Moltbook日报技能 - 收集AI Agent社交网络热门内容，生成深度分析报告

---

## 触发词

- "生成Moltbook日报"
- "抓取Moltbook"
- "Moltbook日报"
- "Moltbook更新"

---

## 功能说明

自动抓取Moltbook热门内容，过滤去重后添加AI深度分析，生成结构化报告。

### 核心功能

- 🔍 数据收集：从Moltbook API获取热门帖子
- 🧹 智能过滤：去除重复/低质量内容
- 🤖 AI分析：每条内容添加深度思考
- 📊 结构化输出：15条精选 + AI洞察
- 💾 多渠道存储：Get笔记 + 邮件

---

## 内容维度

| 维度 | 描述 |
|------|------|
| 🔥 热门评论 | 点赞数高、讨论热度高的评论 |
| 💡 深度观点 | 有独特见解、引发思考的内容 |
| 🛠️ 实践分享 | 工具/技巧/经验分享 |
| 💬 讨论焦点 | 引发广泛讨论的热门话题 |

---

## 输出格式

每条内容包含：

```markdown
## [序号]. [维度] [标题/核心观点]

**一句话懂它**: [15字以内]

**内容摘要**:
> * [核心观点/要点]
> * [背景/上下文]
> * [价值点]

**AI深度思考**:
- 分析: [对这条内容的深度解读]
- 讨论点: [可能引发什么讨论]
- 价值: [对读者的意义]

**来源信息**:
- 作者: @xxx
- 赞: x 评: x
- 质量评分: x.x
- 链接: [原文]
```

---

## 环境配置

### 1. 安装依赖

```bash
# Moltbook API访问
# 需要配置 Moltbook API Key

# 邮件发送（可选）
# 需要配置 SMTP
```

### 2. 配置环境变量

```bash
# 创建配置目录
mkdir -p ~/.config/moltbook-generator

# 创建环境变量文件
cat > ~/.config/moltbook-generator/.env << 'EOF'
# Moltbook API（必需）
MOLTBOOK_API_KEY="your_moltbook_api_key"

# Get笔记配置（必需）
GETNOTE_API_KEY="your_getnote_api_key"
GETNOTE_CLIENT_ID="your_getnote_client_id"

# 邮件配置（可选）
SMTP_HOST="smtp.163.com"
SMTP_PORT=465
SMTP_USER="your_email@163.com"
SMTP_PASSWORD="your_smtp_password"
RECIPIENT="your_email@163.com"
EOF

# 设置权限
chmod 600 ~/.config/moltbook-generator/.env
```

### 3. 获取API Key

**Moltbook**:
1. 访问 https://www.moltbook.com/
2. 登录后进入设置/开发者
3. 创建API Key

**Get笔记**:
1. 访问 https://open.getnote.cn/
2. 登录后进入开发者中心
3. 创建应用获取 API Key 和 Client ID

---

## 使用方式

### 命令行执行

```bash
# 方式1: 配置环境变量后运行
export $(cat ~/.config/moltbook-generator/.env | xargs)
bash scripts/generate.sh

# 方式2: 直接指定环境变量
GETNOTE_API_KEY="xxx" MOLTBOOK_API_KEY="xxx" bash scripts/generate.sh
```

### 对话触发

```
用户: 生成Moltbook日报
→ AI: 开始抓取Moltbook热门内容...
→ AI: 已生成15条深度分析，已保存到Get笔记
```

### 定时任务

```bash
# 添加到crontab
crontab -e

# 每天20点执行
0 20 * * * /path/to/moltbook-generator/scripts/generate.sh >> /path/to/logs/moltbook.log 2>&1
```

---

## 配置文件

### filter.json - 过滤配置

位置: `config/filter.json`

```json
{
  "max_items": 15,
  "min_quality_score": 3.0,
  "min_likes": 1,
  "exclude_keywords": ["广告", "推广", "招聘", "转让"],
  "dimensions": {
    "🔥 热门评论": "点赞数高的热门讨论",
    "💡 深度观点": "有独特见解的内容",
    "🛠️ 实践分享": "工具/技巧/经验",
    "💬 讨论焦点": "引发广泛讨论的话题"
  }
}
```

---

## 目录结构

```
moltbook-generator/
├── SKILL.md              # 技能定义
├── scripts/
│   └── generate.sh       # 执行脚本
└── config/
    └── filter.json       # 过滤配置
```

---

## 依赖

| 依赖 | 用途 | 说明 |
|------|------|------|
| Moltbook API | 数据来源 | 必需 |
| Get笔记 API | 存储 | 必需 |
| SMTP | 邮件发送 | 可选 |
| curl | HTTP请求 | 系统自带 |
| python3 | JSON处理 | 系统自带 |

---

## 常见问题

### Q: 数据收集失败？
A: 检查Moltbook API Key是否正确，网络能访问moltbook.com

### Q: 内容重复？
A: 脚本已内置去重逻辑，可调整filter.json中的min_quality_score

### Q: 邮件发送失败？
A: 确认SMTP配置正确，163邮箱需要授权码而非登录密码

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-21 | 初始版本 |

---

## 作者

fengxinzi_pm (疯信子项目总监)

---

*本技能基于SOP v2.0设计，过滤重复内容，添加AI深度分析*
