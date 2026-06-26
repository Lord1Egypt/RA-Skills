# Awesome Design Skill

UI 设计风格选择器，为 Claude Code 提供设计系统选择能力。

## 简介

> 💡 **灵感来源**: 本项目受 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 启发而创建，感谢他们的开源贡献。

Awesome Design Skill 是一个 Claude Code 技能插件，帮助开发者使用指定的设计风格进行 UI 开发。包含 **54+ 知名品牌设计规范**，覆盖 AI 产品、开发者工具、金融科技、协作平台等多种场景。

## 特性

- **54+ 精选设计风格** - 涵盖 Linear、Apple、Stripe、Vercel、Notion 等知名品牌
- **完整设计规范** - 每个风格包含颜色、字体、间距、组件等完整设计系统
- **一键应用** - 快速复制 DESIGN.md 到项目目录
- **可自定义** - 轻松添加或替换设计风格

## 安装

将本仓库克隆到 Claude Code 的 skills 目录：

```bash
cd ~/.claude/skills
git clone https://github.com/zhouchang1988/awesome-design-skill.git
```

## 使用方法

### 在 Claude Code 中使用

**此技能仅在用户明确指定设计风格时触发。** 例如：

```
用 Linear 风格设计一个登录页面
```

```
使用 Stripe 风格创建支付界面
```

```
按 Apple 风格重构这个页面
```

**以下请求不会触发此技能**（未指定风格）：

```
设计一个项目管理 dashboard        # 未指定风格，不触发
制作一个音乐播放器界面            # 未指定风格，不触发
创建一个登录页面                  # 未指定风格，不触发
```

### 查看可用风格

```
列出所有设计风格
有哪些风格可用
```

### 查看特定风格详情

```
看看 Linear 风格的设计规范
查看 Vercel 风格
```

## 自定义设计风格

**design-md 目录中的内容可以自由添加或替换。** 你可以：

- 添加自己喜欢的设计风格（在 `design-md/` 目录下创建新的风格文件夹和 DESIGN.md）
- 替换现有风格的 DESIGN.md 内容
- 删除不需要的风格

这样你可以构建属于自己的设计风格库，让 Claude 使用你熟悉和偏好的设计系统。

### 添加新风格示例

```bash
# 创建新风格目录
mkdir -p design-md/my-brand

# 创建 DESIGN.md 文件
cat > design-md/my-brand/DESIGN.md << 'EOF'
# My Brand Design System

## Overview
我的自定义设计风格描述...

## Colors
- Primary: #3B82F6
- Background: #FFFFFF
...
EOF
```

## 命令行使用

### 查看可用风格

```bash
./scripts/list-styles.sh
```

### 获取指定风格

```bash
./scripts/get-design.sh linear.app
./scripts/copy-design.sh linear.app
```

### 智能选择风格

```bash
./scripts/smart-select.sh "项目管理"
```

### 随机选择风格

```bash
./scripts/random-style.sh
```

## 支持的设计风格

### AI 产品

| 风格 | 适用场景 |
|------|----------|
| [Claude](design-md/claude) | AI 助手、对话产品 |
| [Cursor](design-md/cursor) | AI 编辑器、开发者工具 |
| [Cohere](design-md/cohere) | 企业 AI、NLP 产品 |
| [Mistral AI](design-md/mistral.ai) | 开源 AI 大模型 |
| [xAI](design-md/x.ai) | 前沿科技 AI |
| [Together AI](design-md/together.ai) | 云端 AI 推理 |
| [MiniMax](design-md/minimax) | 多模态 AI |
| [OpenCode](design-md/opencode.ai) | AI 编程助手 |
| [Ollama](design-md/ollama) | 本地 AI 运行 |
| [Runway](design-md/runwayml) | AI 视频、创意 |
| [Replicate](design-md/replicate) | AI 模型 API |
| [ElevenLabs](design-md/elevenlabs) | AI 语音合成 |
| [Lovable](design-md/lovable) | AI 应用构建 |
| [Composio](design-md/composio) | AI 代理集成 |
| [VoltAgent](design-md/voltagent) | AI 代理框架 |

### 开发者工具

| 风格 | 适用场景 |
|------|----------|
| [Linear](design-md/linear.app) | 项目管理、开发者工具 |
| [Vercel](design-md/vercel) | 部署、前端、云服务 |
| [Figma](design-md/figma) | 设计工具、协作平台 |
| [Framer](design-md/framer) | 设计工具、创意平台 |
| [Raycast](design-md/raycast) | 效率工具、Mac 应用 |
| [Warp](design-md/warp) | 终端、命令行 |
| [Sentry](design-md/sentry) | 错误监控、调试 |
| [Expo](design-md/expo) | React Native、移动开发 |
| [Mintlify](design-md/mintlify) | 文档、知识库 |

### 金融科技

| 风格 | 适用场景 |
|------|----------|
| [Stripe](design-md/stripe) | 支付、金融科技、API |
| [Coinbase](design-md/coinbase) | 加密货币、交易 |
| [Wise](design-md/wise) | 国际转账、支付 |
| [Revolut](design-md/revolut) | 金融科技、银行 |
| [Kraken](design-md/kraken) | 加密货币交易所 |

### 协作与生产力

| 风格 | 适用场景 |
|------|----------|
| [Notion](design-md/notion) | 笔记、文档、协作 |
| [Airtable](design-md/airtable) | 数据库、表格、协作 |
| [Miro](design-md/miro) | 白板、协作、创意 |
| [Intercom](design-md/intercom) | 客服、沟通、SaaS |
| [Cal.com](design-md/cal) | 日程、预约 |
| [Zapier](design-md/zapier) | 自动化、工作流 |
| [Superhuman](design-md/superhuman) | 邮件、效率工具 |

### 数据与后端

| 风格 | 适用场景 |
|------|----------|
| [Supabase](design-md/supabase) | 数据库、后端服务 |
| [MongoDB](design-md/mongodb) | 数据库、NoSQL |
| [ClickHouse](design-md/clickhouse) | 分析数据库、大数据 |
| [PostHog](design-md/posthog) | 数据分析、开源 |
| [HashiCorp](design-md/hashicorp) | 基础设施、云服务 |

### 消费产品

| 风格 | 适用场景 |
|------|----------|
| [Apple](design-md/apple) | 产品展示、高端品牌 |
| [Airbnb](design-md/airbnb) | 旅行、预订、社区 |
| [Spotify](design-md/spotify) | 音乐、媒体播放 |
| [Uber](design-md/uber) | 出行、服务 |
| [Pinterest](design-md/pinterest) | 图片、社交、发现 |

### 企业与品牌

| 风格 | 适用场景 |
|------|----------|
| [IBM](design-md/ibm) | 企业级、B2B |
| [NVIDIA](design-md/nvidia) | 硬件、AI、游戏 |
| [BMW](design-md/bmw) | 汽车、高端品牌 |
| [SpaceX](design-md/spacex) | 航天、科技、探索 |

### 其他

| 风格 | 适用场景 |
|------|----------|
| [Webflow](design-md/webflow) | 网站构建、无代码 |
| [Sanity](design-md/sanity) | CMS、内容管理 |
| [Clay](design-md/clay) | B2B、销售、数据 |

## DESIGN.md 结构

每个设计规范文件包含以下内容：

- **视觉主题与氛围** - 整体设计理念和风格描述
- **色彩调色板** - 完整的颜色系统和角色定义
- **字体规则** - 字体族、字号、字重、行高、字间距
- **组件样式** - 按钮、卡片、输入框、徽章等组件规范
- **布局原则** - 间距系统、网格、留白哲学
- **深度与层级** - 阴影、层级关系
- **响应式行为** - 断点、触控目标、折叠策略
- **宜与忌** - 设计最佳实践

## 脚本说明

| 脚本 | 用途 |
|-----|------|
| `list-styles.sh` | 列出所有可用的设计风格 |
| `smart-select.sh` | 智能选择设计风格（根据需求关键词匹配） |
| `random-style.sh` | 随机选择一个设计风格 |
| `get-design.sh` | 获取指定风格的 DESIGN.md 路径 |
| `copy-design.sh` | 复制 DESIGN.md 到指定目录 |

## 贡献

欢迎贡献新的设计风格或改进现有规范。

## 致谢

本项目灵感来自 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)，感谢他们为社区提供的优秀设计资源。

## 许可证

MIT License

## 作者

[@zhouchang1988](https://github.com/zhouchang1988)
