---
name: cclaw
version: 1.10.0
description: "Open-source comedy AI + video editing + poster generation. Create standup/sketch/manzai/scripts, edit videos via FFmpeg, and generate comedy posters via canvas-design. Supports Damai/Maoyan/Xiudong platform specs. Keywords: comedy, standup, sketch, video, edit, poster, canvas."
description_zh: "全球首个开源喜剧 AI + 视频剪辑 + 海报生成工具。创作脱口秀/小品/漫才/剧本等喜剧内容，或通过自然语言脚本驱动 FFmpeg 进行视频剪辑，或生成脱口秀/演出/金句海报及大麦/猫眼/秀动等平台标准规格物料。"
category: "data-analysis"
---

# Cclaw — 喜剧龙虾 🦞

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-lightgrey.svg)](https://opensource.org/licenses/MIT-0)
[![ClawHub](https://img.shields.io/badge/ClawHub-cclaw-blue)](https://clawhub.com/skills/cclaw)

> **全球首个开源喜剧 AI** —— 从灵感到成稿，从稿件到视频到海报，全链路喜剧创作工具。

Cclaw（喜剧龙虾）是一款面向 OpenClaw 平台的开源喜剧创作技能。它不只是"写段子"——而是一套**知识驱动的喜剧创作流水线**：内置 8 种喜剧体裁模板、完整的喜剧理论体系、风格分类系统，以及视频剪辑和海报生成能力。

**AI 完成从零到一，人完成从一到无穷。**

---

## ✨ 核心能力

### 🎭 喜剧文本创作

- **8 种体裁**：脱口秀、漫才、Sketch 小品、日式短剧（コント）、剧本、讽刺文、仿讽、荒诞剧
- **风格体系**：每种体裁下有多种风格维度（如脱口秀支持自嘲 / 观察 / 观点输出 / 隐喻讽刺等 8 种风格），同题不同味
- **四问交互**：模糊请求时自动引导确认体裁 → 题材 → 情绪 → 受众
- **知识驱动**：基于喜剧理论体系（柏格森机械化法则）+ 案例库 + 黑话手册，不是随机堆梗
- **去名化原则**：知识库不含具体人名/书名，通用化处理

### 🎬 视频剪辑

- 自然语言 → FFmpeg 命令自动解析执行
- 支持裁剪 / 拼接 / zoom 特写 / 过渡效果 / 音频标准化
- 内置 3 套剪辑配方：基础剪辑、高光集锦、**喜剧节奏剪辑**
- 默认 H.264 输出，Windows 全平台兼容

### 🖼️ 海报生成

- Design Brief 驱动：喜剧语境 → 设计语言 → 专业视觉
- **11 种规格模板**覆盖三大演出平台：
  - 通用：脱口秀个人海报(1080×1920)、演出宣传海报(1920×1080)、社交分享卡(1200×630)
  - 大麦：海报(1020×1360)、详情页(1020px宽)、Banner(999×375 / 1404×320)
  - 猫眼：海报(1800×2400)、详情页(800px宽)、Banner(1053×180)
  - 秀动：Banner(1114×200)
- 集成 canvas-design skill 输出高质量 PNG/PDF

---

## 🚀 安装

```bash
# 方式一：ClawHub（推荐）
clawhub install cclaw

# 方式二：SkillHub
skillhub install cclaw

# 方式三：手动安装
# 将仓库内容放入 ~/.qclaw/skills/cclaw/
```

---

## 💡 使用示例

### 喜剧创作

```
写一段脱口秀，主题是中年程序员失业
帮我写个漫才，题材是大龄程序员面试
写个讽刺文，主题是内卷
用日式短剧的形式写一个偏执狂在便利店
```

### 视频剪辑

```
帮我剪辑视频，删掉第5秒到第20秒
拼接这4个片段，加上fade过渡
给56秒处加一个zoom特写效果
帮我提取高光片段做成集锦
```

### 海报生成

```
生成脱口秀海报，主题是AI打败了程序员
生成大麦演出海报，演出名称51笑翻天
生成金句卡，内容是35岁一个Bug都没修好的人生
```

---

## 📐 架构

```
cclaw/
├── SKILL.md                          # 技能入口 · 四步路由工作流
├── commands.md                       # 用户命令配置（文本 + 视频）
├── README.md                         # 本文件
├── LICENSE                           # MIT-0
│
├── modules/
│   ├── writing/                      # 8种喜剧输出模板
│   │   ├── standup-template.md       # 脱口秀
│   │   ├── sketch-template.md        # Sketch 小品
│   │   ├── manzai-template.md        # 漫才
│   │   ├── japanese-sketch-template.md # 日式短剧（コント）
│   │   ├── script-template.md        # 剧本
│   │   ├── satire-template.md        # 讽刺文
│   │   ├── parody-template.md        # 仿讽
│   │   └── absurdist-template.md     # 荒诞剧
│   └── tools/
│       ├── video/                    # 视频剪辑模块
│       │   ├── README.md             # FFmpeg 工作流
│       │   ├── transitions.md        # 过渡效果库
│       │   └── recipes/              # 3套剪辑配方
│       │       ├── basic-cut.md
│       │       ├── highlight-reel.md
│       │       └── comedy-timing.md
│       └── poster/                   # 海报生成模块
│           ├── README.md             # 海报工作流 + Brief 规范
│           ├── briefs/               # 11种规格模板
│           │   ├── standup-poster.md / comedy-show.md / social-card.md
│           │   ├── damai-poster.md / damai-detail.md
│           │   ├── maoyan-poster.md / maoyan-detail.md
│           │   ├── banner-damai-999.md / banner-damai-1404.md
│           │   ├── banner-maoyan.md / banner-xiudong.md
│           └── recipes/
│               └── quote-card.md
│
├── knowledge/
│   ├── blackbook.md                  # 黑话手册（术语统一解释，⓪优先加载）
│   ├── style-guide.md                # 风格体系总纲（各体裁风格分类索引）
│   ├── theory/                       # 喜剧底层原理（必读）
│   │   ├── eb7cb5ef.md              # 核心原理（机械化法则）
│   │   ├── ac07d434.md              # 包袱结构与铺垫节奏
│   │   ├── 126b44e8.md              # 笑的心理学机制
│   │   ├── 9d01e4da.md              # 喜剧类型速查
│   │   └── japanese-sketch.md        # 日式短剧理论（含七步展开结构）
│   └── cases/                        # 案例库（按体裁分目录）
│       ├── standup/                  # ✅ 充实（成长路径/排毒日记/灵感库/课程笔记）
│       ├── sketch/                   # ✅ 有模板
│       ├── manzai/                   # ⏳ 待填充
│       ├── japanese-sketch/          # ⏳ 待填充
│       ├── parody/                   # ⏳ 待填充
│       └── script/                   # ⏳ 待填充
│
└── references/                       # 索引
    ├── comedy-theory.md
    └── comedy-templates.md
```

---

## 🔧 工作流程

Cclaw 采用**四步路由**架构：

```
用户输入
  │
  ├─ Step 1：识别命令类型
  │    ├─ 文本创作 ──→ Step 2A（知识驱动）
  │    ├─ 视频工具 ──→ Step 2B（FFmpeg 脚本驱动）
  │    └─ 海报工具 ──→ Step 2C（Design Brief 驱动）
  │
  ├─ Step 1B：意图确认（模糊请求时触发四问交互）
  │    体裁 → 题材 → 情绪 → 受众 → 风格（可选）
  │
  └─ Step 2A：文本创作流程（五步加载）
       ⓪ 黑话手册 → ① 模板+风格 → ② 案例库（按style筛选）
       → ③ 理论原理 → ④ 按模板创作 → 输出成品+创作笔记
```

### 关键设计决策

| 特性 | 说明 |
|------|------|
| **意图分支** | 明确话题直接创作；模糊请求走四问交互 |
| **风格系统** | 每种体裁有多维风格，可指定也可自动推断 |
| **黑话优先** | 创作第一步加载 blackbook.md，确保术语一致 |
| **案例筛选** | 按 style 标签匹配案例，空目录跳过不读其他类型 |
| **理论隐身** | 正文人名/书名/术语标签全部隐藏；创作笔记保留手法标注 |

---

## 📚 理论体系

一切喜剧效果的根本来源：**生命中出现机械性、僵硬性**（柏格森）。

**三大铁律：**
1. 角色越不自觉，越可笑
2. 观众越不动情，越能发笑
3. 效果逐级递增

**核心手法：** 弹簧魔鬼 / 雪球效应 / 系列干扰 / 换位 / 反转 / 三番四抖 / 连续否认 / Call Back（遗忘后再炸）

**日式短剧七步展开结构：** 日常世界设定 → 反常点出现 → 直人反应 → 怪人解释 → 怪人逐渐离谱 → 内部压力增大 → 无法升级的包袱

详见 `knowledge/theory/` 各文件。

---

## 👥 适合谁

- 脱口秀演员、喜剧编剧、真心热爱喜剧的普通人
- 抖音 / 快手 / 小红书 / 视频号喜剧内容创作者
- 漫才、Sketch、喜剧短剧团队与个人
- 需要幽默表达、年会文案、喜剧化演讲的企业与机构
- 需要快速剪辑喜剧视频、制作演出物料的内容创作者
- 每一个想把生活讲成喜剧的人

---

## 📋 版本历史

### v1.10.0 (2026-05-10)
- ✅ 模板输出规格修复：正文不含结构标签，结构规划移入创作笔记
- ✅ 知识库文件哈希化：Sketch写作手册→sketch-writing-guide-HWTWC.md，幽默修辞方法→humor-rhetoric-methods-HRC.md
- ✅ 新增理论文件：humor-rhetoric-methods-HRC.md（六大修辞律：岔断/倒置/转移/干涉/降格/升格）
- ✅ Call Back 定义修正：遗忘后再炸（非呼应/回归）
- ✅ 8个输出模板全部更新（standup/sketch/manzai/japanese-sketch/script/satire/parody/absurdist）
- ✅ 案例库去名化：清除所有人名/书名引用

### v1.9.2 (2026-05-03)
- 知识库全面去名化：清除所有人名/书名引用（意辰、三谷幸喜、岩崎う大 等）
- 日式短剧理论新增「七步展开结构（怪人-直人升级模型）」

### v1.9.1 (2026-04-30)
- 日式短剧理论扩展至 9 条核心铁律（原 8 条 + 七步展开结构）
- SKILL.md frontmatter YAML 格式修复

### v1.9.0 (2026-04-30)
- **新增风格体系**（`knowledge/style-guide.md`）：每种喜剧大类下建立风格分类
- 创作流程重构为五步：模板+风格 → 案例（按 style 筛选）→ 理论 → 创作
- 现有案例统一添加 `style:` 标签

### v1.8.0 ~ v1.8.1 (2026-04-28)
- 新增**日式短剧（コント）**创作类型（第 8 种体裁）
- 新增 8 条核心铁律：装傻彻底、吐槽精准、留白停顿（日式喜剧灵魂）
- SKILL.md YAML frontmatter 格式修复

### v1.7.0 (2026-04-27)
- **新增海报生成模块**：3 种基础海报 + 8 种演出平台规格（共 11 个模板）
- Design Brief 工作流：喜剧语境 → 设计语言 → 专业视觉
- 集成 canvas-design skill
- 实测产出：Diego 脱口秀海报、「51笑翻天」大麦全套物料

### v1.6.0 (2026-04-26)
- 海报模块 P0 实现：3 种基础海报类型 + 金句卡配方

### v1.5.0 ~ v1.5.1 (2026-04-26)
- **新增意图确认分支**：明确话题直接创作，模糊请求走四问交互（体裁→题材→情绪→受众）
- Q3 标题优化为"创作者核心情绪"

### v1.4.0 (2026-04-25)
- 新增黑话手册（`knowledge/blackbook.md`）：蒸馏/龙虾/国潮等术语定义
- SKILL.md 新增步骤⓪ 加载黑话（最高优先级）

---

## 📄 许可证

**MIT No Attribution (MIT-0)**

✅ 可自由使用、修改、分发、商用，无需署名。

详见 [LICENSE](./LICENSE)。
