# 🌙 寻梦之旅 | Dream Journey

> **有些地方，我们先在梦里遇见，然后用 AI 把它寻成真。**
>
> *Some places we first meet in dreams, then use AI to find them in reality.*

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/catshcroZhang/dream-journey)
[![FlyAI](https://img.shields.io/badge/FlyAI-Required-orange.svg)](https://flyai.open.fliggy.com)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D14-brightgreen.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌐 语言 | Language

- [🇨🇳 中文版](#-一句话介绍)
- [🇬🇧 English Version](#-one-sentence-intro)

---

# 🇨🇳 中文版

## 🎯 一句话介绍

**一个把模糊梦境变成真实旅行的 AI Skill** —— 用户描述反复出现的梦，AI 高清还原梦境、FlyAI 实时匹配高度相似的真实目的地，端到端行程规划+飞猪官方预订链接，行中拍照验证梦境，结束生成星空沉浸式报告和短视频爆款包！

---

## ✨ 核心特色

| 特色 | 说明 |
|------|------|
| 🧠 **梦境高清还原** | 从模糊描述提取视觉/听觉/嗅觉/情绪元素，生成电影级场景描述 |
| 🎯 **语义匹配引擎** | FlyAI 实时搜索，精准匹配梦境相似度 90%+ 的真实目的地 |
| 📄 **星空沉浸报告** | 150 颗闪烁星星+流星动画+玻璃态卡片，宿命感拉满 |
| 🎬 **短视频矩阵** | 一键生成 10 个爆款脚本，5 大主题 50 条金句智能匹配 |
| 🛡️ **情感安全阀** | 恐怖梦境自动识别，温柔守护用户心理健康 |
| 📸 **行中验证** | 上传照片立即对比"梦境 vs 现实"，温柔诗意讲解 |
| 🤖 **多 Agent 协作** | 梦境还原 + 现实匹配 + 行程规划 + 梦境验证 + 情感输出，五位一体 |
| 🔗 **官方预订链接** | 提供飞猪平台官方跳转链接，用户自行完成预订，安全可控 |

---

## 🚀 快速开始

### 1️⃣ 前置依赖

**本 Skill 依赖以下工具**，使用前请确保已安装：

```bash
# 安装 FlyAI CLI（飞猪开放平台工具，用于查询交通/酒店/景点数据）
# 注意：查询功能无需 API Key，预订功能需飞猪账号授权
npm i -g @fly-ai/flyai-cli

# 验证连接
flyai ai-search --query "测试" --debug

# 安装 Node.js（v14+，用于运行辅助脚本）
# 下载地址：https://nodejs.org/
node --version
```

> **🔒 安全说明**：
> - `@fly-ai/flyai-cli` 是飞猪开放平台提供的官方工具，用于实时查询航班/火车/酒店/景点数据
> - **查询功能**：无需 API Key 或任何凭证，安装即可使用
> - **预订功能**：会提供飞猪官方预订链接，跳转到飞猪平台完成，本 Skill 不代客下单、不存储支付信息
> - 所有敏感操作（如预订）需用户明确确认后才执行
> - 辅助脚本仅在本地运行，不会上传数据到外部服务器
> - 详细说明请参考：[安全与风险提示](#-安全与风险提示)

### 2️⃣ 安装 Skill

#### 方式一：Qwen Code

```bash
cp -r ~/.flyai/skills/dream-journey ~/.qwen/skills/
```

#### 方式二：Qoderwork

```bash
cp -r ~/.flyai/skills/dream-journey ~/.qoderwork/skills/
```

#### 方式三：GitHub

```bash
git clone git@github.com:catshcroZhang/dream-journey.git
```

### 3️⃣ 触发寻梦

在 AI 对话中输入：

```
启动寻梦之旅！
```

或

```
我反复梦到一个地方，帮我找到它！
```

---

## 🎮 使用示例

### 示例 1：完整梦境描述

**用户输入：**
```
我反复梦到一个模糊的地方：一座被大雾笼罩的古镇，石板路总是湿的，河边挂着很多红灯笼，远处有座很陡的山，晚上能听到低沉的钟声，感觉既熟悉又陌生。
```

**AI 输出：**
```
【寻梦者报告】

梦境高清还原：
晨雾如纱，轻轻笼罩着一座沉睡千年的古镇。青石板路被昨夜的雨水洗刷得发亮，
每一道缝隙都藏着岁月的故事。河岸边，一排排红灯笼在微风中摇曳，倒映在
潺潺流水中，像是梦境与现实之间的桥梁……

梦境核心元素：
- 视觉：大雾笼罩的古镇、湿漉漉的石板路、河边红灯笼、远处的陡山
- 听觉：低沉的钟声、流水声
- 情绪基调：既熟悉又陌生，带有宿命感

【现实寻梦选项】
1. 安徽黟县宏村（梦境相似度 92%）
   - 为什么匹配：晨雾中的马头墙、雨后石板路、南湖红灯笼完美对应梦境
   - 推荐行程：3天2夜，深度体验古徽州文化
   - 实时预估预算：¥2,000-3,000
   - 飞猪官方预订链接：[跳转飞猪预订](...)

2. 浙江乌镇西栅（梦境相似度 85%）
   - 为什么匹配：水乡古镇，河道纵横，夜晚灯笼点缀
   - 推荐行程：2天1夜，水乡慢生活
   - 实时预估预算：¥1,500-2,500

【下一步】
回复"去第1个"或"详细规划第1个"，我将调用 Fly.ai 一键生成完整行程并支持预订。
回复"再细化梦境"或补充细节，我会继续优化。
```

### 示例 2：信息不完整

**用户输入：**
```
启动寻梦之旅！
```

**AI 输出：**
```
🌙 寻梦者已就位！在开始寻梦之旅之前，让我先了解一些信息：

1️⃣ **梦境描述**：你梦到了什么场景？（越详细越好，模糊的描述也可以）
2️⃣ **出发地**：你从哪个城市出发？
3️⃣ **出发时间**：打算什么时候出发？
4️⃣ **行程天数**：几天几夜？
5️⃣ **预算**：准备花多少钱圆梦？

💡 **或者回复"帮我寻梦"，我会根据你的模糊描述自动匹配！**
```

---

## 🏗️ 架构设计

### 多 Agent 协作体系

```
┌─────────────────────────────────────────────────┐
│                  寻梦之旅                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ 梦境还原  │  │ 现实匹配  │  │ 行程规划  │       │
│  │  Agent   │  │  Agent   │  │  Agent   │       │
│  │          │  │          │  │          │       │
│  │ 高清还原  │  │ FlyAI   │  │ 端到端   │       │
│  │ 元素提取  │  │ 相似度   │  │ 打卡点   │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│         ↓              ↓              ↓          │
│  ┌─────────────────────────────────────────┐    │
│  │          梦境验证 Agent                  │    │
│  │   拍照讲解 + 梦境vs现实对比 + 温柔诗意   │    │
│  └─────────────────────────────────────────┘    │
│                       ↓                          │
│  ┌─────────────────────────────────────────┐    │
│  │          情感输出 Agent                  │    │
│  │   星空报告 + 短视频脚本 + 智能金句        │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### 执行流程

```
阶段零：信息收集 → 阶段一：梦境还原 → 阶段二：行程规划 → 阶段三：行中验证 → 阶段四：结束生成
     ↓                  ↓                  ↓                  ↓                  ↓
  确认梦境描述       寻梦者报告         行程方案           拍照讲解          星空报告
  确认出发地         视觉 Prompt        一键预订           动态调整          短视频包
  确认时间预算       现实匹配选项       寻梦日记           温柔对比          智能金句
```

---

## 📦 生成内容

行程结束后，自动生成三份核弹级内容：

### 1. 《梦境 vs 现实对比报告》（星空 HTML 页面）
- 150 颗闪烁星星 + 流星动画背景
- 玻璃态卡片 + 渐变色彩 + 动画效果
- 梦境描述 + 高清还原 + 现实目的地对比
- 统计数据卡片（相似度、花费、天数、宿命感指数）
- 行程时间线 + 照片墙 + 情感日记
- 支持一键打印/保存为 PDF

### 2. 《我的梦成真了》情感日记
- 总花费明细
- 梦境验证成功次数
- 最感动瞬间 Top 3
- 宿命感指数（0-100）
- 数据可视化描述

### 3. 短视频爆款包
- 10 个爆款标题（带 emoji）
- 每条视频的 15-30 秒脚本（带 BGM 建议和字幕文案）
- 一键分享文案

---

## 🔒 安全与风险提示

**安装前请了解以下风险**：

### 1. 第三方 CLI 工具
- `@fly-ai/flyai-cli` 是飞猪开放平台提供的第三方工具，通过 npm 安装
- **查询功能**：无需 API Key 或任何凭证，安装即可使用
- **预订功能**：提供飞猪官方跳转链接，用户在飞猪平台完成支付，本 Skill 不存储任何支付信息
- 建议从官方 npm 源安装：`npm i -g @fly-ai/flyai-cli`

### 2. Node.js 辅助脚本
- `scripts/` 目录下的脚本需要 Node.js（v14+）运行
- 脚本会在本地生成 HTML/JSON 文件，不会上传任何数据到外部服务器
- 脚本仅读取用户提供的 JSON 数据，不会访问网络或收集个人信息

### 3. 本地文件处理
- 生成的 HTML 报告、短视频脚本等文件保存在用户本地目录
- 照片墙功能使用用户提供的图片路径或 URL，本 Skill 不存储或传输照片
- 建议定期清理生成的临时文件

### 4. 用户确认机制
- 所有涉及预订的操作需用户明确确认后才执行
- 预算、日期、健康状况严格遵守用户设定
- 禁止安排任何违法、危险、严重影响健康的项目

---

## 🛡️ 安全阀

- ✅ 恐怖梦境自动识别，立即进入安慰模式
- ✅ 出发前必须让用户明确确认
- ✅ 预算、日期、健康状况严格遵守
- ✅ 禁止安排任何违法、危险、严重影响健康的项目

---

## 📂 文件结构

```
dream-journey/
├── SKILL.md                          # 核心 Skill 定义（符合 Agent Skills 规范）
├── README.md                         # 本文件
├── assets/
│   └── report-template.html          # 星空主题 HTML 报告模板
├── references/
│   ├── README.md                     # 详细参考文档
│   ├── INSTALL.md                    # 安装指南
│   └── HOW-TO-ADD-PHOTOS.md          # 图片添加指南
└── scripts/
    ├── generate-dream-prompt.js      # 梦境视觉 Prompt 生成器
    ├── generate-quote.js             # 金句生成器（5大主题50条）
    ├── generate-report.js            # HTML 报告生成器
    └── generate-video-scripts.js     # 短视频脚本生成器（10个）
```

---

## 🔧 辅助脚本工具

### 1. 梦境视觉 Prompt 生成器

```bash
node scripts/generate-dream-prompt.js "我梦到雾中的古镇"
```

**功能**：
- 自动提取梦境视觉/听觉/氛围元素
- 生成中英文双版本 AI 图像生成 Prompt
- 输出 HTML 预览页面，一键复制
- 支持 Midjourney / DALL-E / Stable Diffusion

### 2. HTML 报告生成器

```bash
node scripts/generate-report.js --json data.json
node scripts/generate-report.js --example  # 查看示例
```

**功能**：
- 将行程数据填充到星空主题 HTML 模板
- 生成沉浸式寻梦报告（支持打印保存）
- 包含梦境对比、时间线、照片墙、情感日记

### 3. 短视频脚本生成器

```bash
node scripts/generate-video-scripts.js --dream "梦境" --dest "目的地" --score 92
```

**功能**：
- 生成 10 个抖音/小红书爆款视频脚本
- 每个脚本包含 15秒/30秒版本、BGM建议、字幕文案
- 输出 HTML 预览页面，可一键复制

### 4. 金句生成器

```bash
node scripts/generate-quote.js --dream "梦境描述"  # 智能匹配主题
node scripts/generate-quote.js --theme 宿命感      # 指定主题
node scripts/generate-quote.js --batch 10          # 批量生成
```

**功能**：
- 5大主题：宿命感、治愈系、诗意浪漫、冒险探索、哲理深思
- 共50条精选金句，每次随机生成
- 根据梦境描述智能选择最匹配的主题

---

## 📊 真实案例：长白山森林寻梦

### 行程概览

| 项目 | 详情 |
|------|------|
| **寻梦者** | 张小明 |
| **出发地** | 北京 |
| **目的地** | 吉林长白山 · 北坡原始森林 |
| **行程天数** | 3天4夜 |
| **梦境描述** | "一片望不到边的原始森林，阳光从树叶缝隙透进来，地上铺着厚厚的松针，森林深处有座原木小木屋……" |
| **梦境相似度** | 93.2% |
| **总花费** | ¥6,180 |
| **宿命感指数** | 96/100 |

### 梦境验证打卡清单

| 打卡点 | 相似度 | 心情分 | 最难忘的细节 |
|--------|--------|--------|-------------|
| 地下森林 | 95% | 9/10 | 阳光从百年红松枝叶间洒下的金色光柱 |
| 魔界漂流 | 98% | 10/10 | 晨雾中漂流，安静到能听到心跳声 |
| 长白山瀑布 | 85% | 8/10 | 聚龙泉温泉像梦中炊烟，莫名温暖 |
| 绿渊潭+小天池 | 92% | 9/10 | 密林深处的碧水，安静得不可思议 |
| 二道白河晨雾 | 96% | 10/10 | 晨雾中听到猫头鹰叫，眼泪无声流下 |

### 最感动的3个瞬间

1. **魔界漂流的清晨**：坐在橡皮艇上，看着河面薄雾和两岸原始森林，突然明白什么叫"梦就是这里，这里就是梦"。
2. **二道白河的猫头鹰叫**：清晨独自走在河边，听到猫头鹰叫的那一刻，眼泪无声流下来。就是这里了，我终于找到了。
3. **小天池的梅花鹿**：它安静地看着我，我也安静地看着它。森林、鹿、我，仿佛都属于同一个梦境。

### 寻梦者感言

> "谢谢你反复做这个梦，让我找到了这个地方。你梦里的每一处细节，都在真实世界里等着我。松针的清香、溪水的薄雾、猫头鹰的叫声、风吹过松林的声音……你没有骗我，这里真的存在。而且，比梦里还要美。"

---

## 🎬 星空报告预览

生成的 HTML 报告包含以下特色：

- 🌌 **星空背景** — 150 颗闪烁星星 + 流星动画
- 💎 **玻璃态卡片** — 毛玻璃效果 + 渐变边框
- 📊 **统计数据** — 相似度、花费、天数、宿命感指数
- 🗓️ **行程时间线** — 渐变进度条 + 脉冲动画节点
- 📸 **照片墙** — 悬停缩放 + 旋转动画 + 说明文字滑入
- 💬 **智能金句** — 根据梦境情绪自动匹配主题
- 🖨️ **一键打印** — 支持保存为 PDF

---

## 🤝 贡献指南

欢迎提交 PR 或 Issue！

- 新增更多梦境场景匹配规则
- 优化视觉 Prompt 生成质量
- 添加更多报告模板主题
- 改进短视频脚本模板
- 扩充金句库（当前 50 条）

---

## 📝 更新日志

### v1.0.0 (2026-04-04)
- 🎉 初始版本发布
- 🧠 梦境高清还原 + 语义匹配引擎
- 📄 星空主题 HTML 报告模板
- 🎬 4 个辅助脚本工具链
- 🛡️ 恐怖梦境安全阀机制
- 💬 5 大主题 50 条智能金句

---

# 🇬🇧 English Version

## 🎯 One-Sentence Intro

**An AI Skill that transforms vague, recurring dream descriptions into real-world travel destinations** — AI analyzes your dreams, matches them with actual places via FlyAI real-time search, plans end-to-end itineraries with Fliggy official booking links, verifies dreams through photo commentary during the trip, and generates immersive starry-night HTML reports and viral short video packages upon completion!

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Dream Restoration** | Extract visual/auditory/olfactory/emotional elements from vague descriptions, generate cinematic scene descriptions |
| 🎯 **Semantic Matching** | FlyAI real-time search, precisely match destinations with 90%+ dream similarity |
| 📄 **Starry Immersive Report** | 150 twinkling stars + shooting star animations + glassmorphism cards, destiny feeling maxed out |
| 🎬 **Video Script Matrix** | One-click generate 10 viral scripts, 5 themes 50 quotes intelligently matched |
| 🛡️ **Emotional Safety Valve** | Nightmare auto-detection, gently protect user mental health |
| 📸 **In-Trip Verification** | Upload photos for instant "dream vs reality" comparison, gentle poetic commentary |
| 🤖 **Multi-Agent Collaboration** | Dream Restoration + Reality Matching + Trip Planning + Dream Verification + Emotional Output, five-in-one |

---

## 🚀 Quick Start

### 1️⃣ Prerequisites

**This Skill depends on the following tools**. Before use, ensure installation:

```bash
# Install FlyAI CLI (Fliggy Open Platform tool for querying flights/hotels/attractions)
# Note: Query features require no API Key, booking features require Fliggy account authorization
npm i -g @fly-ai/flyai-cli

# Verify connection
flyai ai-search --query "test" --debug

# Install Node.js (v14+, for running auxiliary scripts)
# Download: https://nodejs.org/
node --version
```

> **🔒 Security Notice**:
> - `@fly-ai/flyai-cli` is an official tool provided by Fliggy Open Platform for real-time query of flights/trains/hotels/attractions data
> - **Query Features**: No API Key or credentials required, ready to use after installation
> - **Booking Features**: Provides official Fliggy booking links that redirect to Fliggy platform for completion. This Skill does not place orders on behalf of users or store payment information
> - All sensitive operations (e.g., booking) require explicit user confirmation before execution
> - Auxiliary scripts run locally only, no data uploaded to external servers
> - For details, see: [Security & Risk Notice](#-security--risk-notice)

### 2️⃣ Install Skill

#### Option 1: Qwen Code

```bash
cp -r ~/.flyai/skills/dream-journey ~/.qwen/skills/
```

#### Option 2: Qoderwork

```bash
cp -r ~/.flyai/skills/dream-journey ~/.qoderwork/skills/
```

#### Option 3: GitHub

```bash
git clone git@github.com:catshcroZhang/dream-journey.git
```

### 3️⃣ Trigger Dream Journey

Type in AI chat:

```
Start Dream Journey!
```

Or

```
I keep dreaming of a place, help me find it!
```

---

## 🎮 Usage Examples

### Example 1: Complete Dream Description

**User Input:**
```
I keep dreaming of a vague place: an ancient town shrouded in heavy fog, cobblestone paths always wet, red lanterns hanging by the river, a steep mountain in the distance, low bell tolls at night, feeling both familiar and strange.
```

**AI Output:**
```
【Dream Seeker Report】

Dream Restoration:
Morning mist like gauze, gently shrouding an ancient town that has slept for a thousand years. 
The bluestone paths shine from last night's rain, every crack hiding stories of time...

Core Dream Elements:
- Visual: Fog-shrouded ancient town, wet cobblestone paths, red lanterns by river, distant steep mountain
- Auditory: Low bell tolls, flowing water sounds
- Emotional Tone: Both familiar and strange, with a sense of destiny

【Real-World Dream Matches】
1. Hongcun, Yixian, Anhui (92% Dream Similarity)
   - Why Match: Horse-head walls in morning mist, rain-washed stone paths, red lanterns by South Lake perfectly match dream
   - Recommended Itinerary: 3 days 2 nights, deep experience of ancient Huizhou culture
   - Real-time Estimated Budget: ¥2,000-3,000
   - Fliggy Booking Link: [Book Now](...)

2. Wuzhen Xizha, Zhejiang (85% Dream Similarity)
   - Why Match: Water town, interwoven rivers, night lantern decorations
   - Recommended Itinerary: 2 days 1 night, slow water town life
   - Real-time Estimated Budget: ¥1,500-2,500

【Next Step】
Reply "go to #1" or "plan #1 in detail", I will use Fly.ai to generate complete itinerary with booking support.
Reply "refine dream" or add details, I will continue optimizing.
```

### Example 2: Incomplete Information

**User Input:**
```
Start Dream Journey!
```

**AI Output:**
```
🌙 Dream Seeker is ready! Before starting the dream journey, let me gather some information:

1️⃣ **Dream Description**: What scene did you dream about? (the more detailed, the better, vague is also fine)
2️⃣ **Departure City**: Where are you departing from?
3️⃣ **Departure Time**: When do you plan to leave?
4️⃣ **Duration**: How many days and nights?
5️⃣ **Budget**: How much money are you ready to spend to fulfill this dream?

💡 **Or reply "help me dream", I will auto-match based on your vague description!**
```

---

## 🏗️ Architecture

### Multi-Agent Collaboration System

```
┌─────────────────────────────────────────────────┐
│               Dream Journey                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Dream    │  │ Reality  │  │ Trip     │       │
│  │ Restor.  │  │ Matching │  │ Planning │       │
│  │  Agent   │  │  Agent   │  │  Agent   │       │
│  │          │  │          │  │          │       │
│  │ HD Rest. │  │ FlyAI   │  │ End-to-  │       │
│  │ Extract  │  │ Similar. │  │ End Pts  │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│         ↓              ↓              ↓          │
│  ┌─────────────────────────────────────────┐    │
│  │      Dream Verification Agent            │    │
│  │   Photo Commentary + Dream vs Reality    │    │
│  └─────────────────────────────────────────┘    │
│                       ↓                          │
│  ┌─────────────────────────────────────────┐    │
│  │      Emotional Output Agent              │    │
│  │   Starry Report + Video Scripts + Quotes │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Execution Flow

```
Phase 0: Info Collection → Phase 1: Dream Restoration → Phase 2: Trip Planning → Phase 3: In-Trip Verification → Phase 4: End Generation
     ↓                          ↓                          ↓                          ↓                          ↓
  Confirm dream             Dream Seeker Report        Itinerary Plan            Photo Commentary        Starry Report
  Confirm departure         Visual Prompt              One-click Booking         Dynamic Adjustment      Video Package
  Confirm time/budget       Reality Match Options      Dream Diary               Gentle Comparison       Smart Quote
```

---

## 📦 Generated Content

After the trip ends, automatically generate three nuclear-level contents:

### 1. "Dream vs Reality Comparison Report" (Starry HTML Page)
- 150 twinkling stars + shooting star animations background
- Glassmorphism cards + gradient colors + animation effects
- Dream description + HD restoration + reality destination comparison
- Statistics dashboard (similarity, cost, days, destiny index)
- Trip timeline + photo gallery + emotional diary
- One-click print / save as PDF

### 2. "My Dream Came True" Emotional Diary
- Total expenses breakdown
- Dream verification success count
- Top 3 most touching moments
- Destiny index (0-100)
- Data visualization description

### 3. Viral Short Video Package
- 10 viral titles (with emoji)
- 15-30 second scripts for each video (with BGM suggestions and subtitle copy)
- One-click share copy

---

## 🔒 Security & Risk Notice

**Please understand the following risks before installation**:

### 1. Third-Party CLI Tool
- `@fly-ai/flyai-cli` is a third-party tool provided by Fliggy Open Platform, installed via npm
- **Query Features**: No API Key or credentials required, ready to use after installation
- **Booking Features**: Provides official Fliggy booking links that redirect to Fliggy platform for completion. This Skill does not store any payment information
- Recommend installing from official npm registry: `npm i -g @fly-ai/flyai-cli`

### 2. Node.js Auxiliary Scripts
- Scripts in `scripts/` directory require Node.js (v14+) to run
- Scripts generate HTML/JSON files locally, no data uploaded to external servers
- Scripts only read user-provided JSON data, do not access network or collect personal information

### 3. Local File Handling
- Generated HTML reports, video scripts, and other files are saved in user's local directory
- Photo gallery feature uses user-provided image paths or URLs, this Skill does not store or transmit photos
- Recommend periodically cleaning up generated temporary files

### 4. User Confirmation Mechanism
- All booking-related operations require explicit user confirmation before execution
- Strictly abide by user's budget, dates, and health conditions
- Prohibit any illegal, dangerous, or health-threatening activities

---

## 🛡️ Safety Valve

- ✅ Nightmare auto-detection, immediately enter comfort mode
- ✅ Must get explicit user confirmation before departure
- ✅ Strictly abide by budget, dates, and health conditions
- ✅ Prohibit any illegal, dangerous, or health-threatening activities

---

## 📂 File Structure

```
dream-journey/
├── SKILL.md                          # Core Skill definition (Agent Skills compliant)
├── README.md                         # This file
├── assets/
│   └── report-template.html          # Starry-night HTML report template
├── references/
│   ├── README.md                     # Detailed reference documentation
│   ├── INSTALL.md                    # Installation guide
│   └── HOW-TO-ADD-PHOTOS.md          # Photo integration guide
└── scripts/
    ├── generate-dream-prompt.js      # Dream visual prompt generator
    ├── generate-quote.js             # Quote generator (5 themes, 50 quotes)
    ├── generate-report.js            # HTML report generator
    └── generate-video-scripts.js     # Video script generator (10 scripts)
```

---

## 🔧 CLI Tools

### 1. Dream Visual Prompt Generator

```bash
node scripts/generate-dream-prompt.js "I dream of a foggy ancient town"
```

**Features**:
- Auto-extract dream visual/auditory/atmospheric elements
- Generate CN/EN dual-version AI image generation prompts
- Output HTML preview page, one-click copy
- Support Midjourney / DALL-E / Stable Diffusion

### 2. HTML Report Generator

```bash
node scripts/generate-report.js --json data.json
node scripts/generate-report.js --example  # View example
```

**Features**:
- Fill trip data into starry-theme HTML template
- Generate immersive dream report (printable)
- Include dream comparison, timeline, photo gallery, emotional diary

### 3. Video Script Generator

```bash
node scripts/generate-video-scripts.js --dream "dream" --dest "destination" --score 92
```

**Features**:
- Generate 10 TikTok/Xiaohongshu viral video scripts
- Each script includes 15s/30s versions, BGM suggestions, subtitle copy
- Output HTML preview page, one-click copy

### 4. Quote Generator

```bash
node scripts/generate-quote.js --dream "dream description"  # Smart theme matching
node scripts/generate-quote.js --theme destiny               # Specify theme
node scripts/generate-quote.js --batch 10                    # Batch generate
```

**Features**:
- 5 themes: Destiny, Healing, Poetic Romance, Adventure Exploration, Philosophical Reflection
- 50 curated quotes, randomly generated each time
- Intelligently match most suitable theme based on dream description

---

## 📊 Real Case: Changbaishan Forest Dream Journey

### Trip Overview

| Item | Details |
|------|---------|
| **Dream Seeker** | Zhang Xiaoming |
| **Departure** | Beijing |
| **Destination** | Changbaishan, Jilin · North Slope Primeval Forest |
| **Duration** | 3 days 4 nights |
| **Dream Description** | "A boundless primeval forest, sunlight filtering through leaf gaps, thick pine needles carpeting the ground, a small log cabin deep in the forest..." |
| **Dream Similarity** | 93.2% |
| **Total Cost** | ¥6,180 |
| **Destiny Index** | 96/100 |

### Dream Verification Checklist

| Checkpoint | Similarity | Mood Score | Most Unforgettable Detail |
|------------|------------|------------|---------------------------|
| Underground Forest | 95% | 9/10 | Golden light rays through century-old Korean pine branches |
| Demon Realm Drifting | 98% | 10/10 | Drifting in morning mist, quiet enough to hear heartbeat |
| Changbaishan Waterfall | 85% | 8/10 | Julongquan hot springs like dream smoke, inexplicably warm |
| Lvyuantan + Small Heavenly Pool | 92% | 9/10 | Emerald water deep in dense forest, incredibly quiet |
| Erdaobaihe Morning Mist | 96% | 10/10 | Owl call in morning mist, tears flowing silently |

### Top 3 Most Touching Moments

1. **Morning at Demon Realm Drifting**: Sitting on the rubber boat, watching river mist and primeval forest on both banks, suddenly understanding "the dream is here, here is the dream".
2. **Owl Call at Erdaobaihe**: Walking alone by the river in the morning, hearing the owl call, tears flowing silently. This is it, I finally found it.
3. **Sika Deer at Small Heavenly Pool**: It looked at me quietly, I looked at it quietly. Forest, deer, I, all seemed to belong to the same dream.

### Dream Seeker's Reflection

> "Thank you for repeatedly having this dream, allowing me to find this place. Every detail you dreamed of was waiting for me in the real world. The fragrance of pine needles, the mist on the stream, the owl's call, the sound of wind through the pines... You didn't deceive me, this place really exists. And it's even more beautiful than the dream."

---

## 🎬 Starry Report Preview

The generated HTML report features:

- 🌌 **Starry Background** — 150 twinkling stars + shooting star animations
- 💎 **Glassmorphism Cards** — Frosted glass effect + gradient borders
- 📊 **Statistics Dashboard** — Similarity, cost, days, destiny index
- 🗓️ **Trip Timeline** — Gradient progress bar + pulsing animation nodes
- 📸 **Photo Gallery** — Hover zoom + rotation animation + caption slide-in
- 💬 **Smart Quotes** — Intelligently matched to dream mood
- 🖨️ **One-Click Print** — Save as PDF support

---

## 🤝 Contributing

PRs and Issues are welcome!

- Add more dream scene matching rules
- Optimize visual prompt generation quality
- Add more report template themes
- Improve short video script templates
- Expand quote library (currently 50 quotes)

---

## 📝 Changelog

### v1.0.0 (2026-04-04)
- 🎉 Initial release
- 🧠 Dream HD restoration + semantic matching engine
- 📄 Starry-theme HTML report template
- 🎬 4 auxiliary script toolchains
- 🛡️ Nightmare safety valve mechanism
- 💬 5 themes 50 smart quotes

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

- **FlyAI Open Platform**: Real-time travel data support
- **Agent Skills Specification**: [agentskills/agentskills](https://github.com/agentskills/agentskills)
- **Starry Night Template**: Custom designed for dream journey reports

---

> **Dream Seeker's Message:**
> "Some places we first meet in dreams, then use AI to find them in reality.
> Your dream is not an illusion — it's your soul calling you to a place that's been waiting for you.
> Let's find it together."
>
> **Sweet dreams, traveler!** 🌙✨
