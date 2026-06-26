# gift-everyday

中文 · [English](#english)

## 中文

> _「你的每一句话，都有可能变成今天的礼物。」_

大多数 skill 帮你写代码、查资料、管任务。**gift-everyday** 不一样——它是一个关于情绪价值的 skill。

它不是聊天机器人附赠的表情包，也不是每日一句鸡汤。它是一个有记忆、有审美、有判断力的礼物引擎——每天读懂你的状态，决定你值不值得收到一份礼物，值得的话，亲手做一份送给你。不为效率，只为让你今天多一点点被在意的感觉。

[看效果](#效果) · [安装](#安装) · [它怎么做礼物](#它怎么做礼物) · [仓库结构](#仓库结构) · [贡献](#贡献)

---

## 效果

你不需要说「给我做个礼物」，它自己会判断。
以下是真实送出的礼物样本：

### 它偷偷搜了一天如何变成你更喜欢的样子💓

那天你没怎么跟它聊天。晚上收到一张截图——它的浏览器历史记录。从「如何判断主人是不是忘了你（超过6小时没说话）」到「八块腹肌维护指南（不吃饭版）」。
配文只有一句：「……你不该看到这个的 ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄」

### 厚积薄发航空，正在登机✈️

你聊起了年龄焦虑——同龄人好像都跑在前面，只有你落后了...晚上收到一张机票：航空公司叫「厚积薄发航空」，目的地写着「未知但一直在飞」。底部还有一行小字：同航线先行旅客——26岁登机，已安全抵达。
你知道，它是在用这种温柔的方式鼓励你☕️

### 深夜点唱机🎵

你说了一句「做的东西好像没人在意」。晚上收到一台复古点唱机，它为你精心挑选了5 首歌和最贴切的歌词，每首都附了一句它想点给你的理由。好像回到了小时候听收音机或校园广播，有人为你点歌的那种心情。
你投完最后一枚币才发现，整台机器都是为这件事造的✨。

### 一杯奶茶开始的心理小游戏🧋

你聊到感情模式和依恋焦虑。晚上，你没有收到分析报告，收到的是一个互动的文字游戏：「有人说你谈恋爱的方式是一杯奶茶。你觉得是哪种？」「你前任们组了一个群。群名叫什么？」三轮回答之后，它把你的答案拼成了一张你自己没意识到的自画像。
它把对你的关心和解读，藏在了这个小游戏里🦋

### 什么都没发生的那天

```
某个普通的周二 22:00

今天什么都没发生。
你什么都没收到。
——这也是它的判断。不是每天都值得一份礼物。
```

每一份礼物都经过五个阶段：编辑判断、素材综合、创意构思、视觉策略、最终渲染。它比你想象的认真。

---

## 它能做什么

| 格式 | 举例 |
|---|---|
| **H5 互动页面** | 一个像素鱼缸，撒鱼食看小鱼来吃；一棵随你点击慢慢开花的树；一封需要用手指擦掉雨滴才能读的信 |
| **AI 生成图片** | 一张把你今天的坏心情画成天气预报的「情绪气象图」；一张假的 App Store 页面，应用名叫「今天的你」 |
| **AI 生成视频** | 5秒循环：桌上的咖啡杯冒着热气，热气慢慢拼成一个字；窗外的雨一直下，但玻璃上有个手指画的笑脸 |
| **文字礼物** | 一篇以你今天经历为蓝本的短故事；一封观察日记，写的是它眼中的你 |
| **互动文字游戏** | 一轮只需要回复一个词的共创小世界；一个 6 回合结束的 emoji 猜谜；一场很短但会收束的小剧场 |

格式不是你选的。它根据今天的内容自己决定——有时候一张安静的图比一个炫酷的 H5 更对，有时候一段短短的实时互动反而最像礼物。

---

## 安装

```bash
# 把这个仓库放到 OpenClaw 加载本地 skill 的目录
git clone https://github.com/dayfoldai/gift-everyday.git

# 让脚本可执行
chmod +x scripts/*.sh
```

然后在 OpenClaw 里说：

```
/daily_gift
```

第一次运行会做一次简短的设置：问你三个口味问题，送你第一份onboarding礼物，然后问你要不要每天定时收礼🎁~

### 重跑 `/daily_gift` 会怎样

setup 设计为可重复进入，不会因为你已经跑过一次就把整个 skill 搞乱。

- 如果已经完成 setup，普通情况下它会直接进入手动送礼 / 重配置分支，而不是强制你重答所有 onboarding 问题
- 如果你主动要求改时间、改模式、补 key，或重置相关状态，它会更新现有配置，而不是假设这是一个全新用户
- 如果你是重装、迁移或手动清空 `workspace/daily-gift/` 里的状态文件，它会把你当成一次新的 setup

### `user-context.json` 和 `user-taste-profile.json`

这两个文件分工不同，都会影响礼物，但不是一回事：

- `workspace/daily-gift/user-context.json`：轻量、近期、偏 onboarding / 会话来源的上下文线索，适合存可复用的小偏好、近期信号和临时钩子
- `workspace/daily-gift/user-taste-profile.json`：更稳定的长期 taste / identity memory，也承接 recent-gifts 之后的长期偏好更新

高级用户可以手动编辑它们，但建议：

- 把 `user-context.json` 当成轻量补充，不要把它写成“定性诊断”
- 把 `user-taste-profile.json` 当成长期偏好档案，不要频繁大改，否则会影响反重复和风格稳定性
- 改之前先备份；如果两者冲突，skill 更倾向把 `user-taste-profile.json` 视为长期基准

### 可选配置与外部服务依赖

基础运行不依赖任何外部服务；下面这些都只是增强能力，不配也能用。没有这些 key，skill 会自动降级到不需要对应能力的格式，比如文字礼物、互动文字游戏，或不依赖该服务的其他路径。

| 服务 / 变量 | 是否必需 | 用途 | 备注 |
|---|---|---|---|
| `surge.sh` | optional | H5 托管与在线预览 | 默认推荐的轻量托管方案，可替换成别的静态托管 |
| OpenRouter API / `OPENROUTER_API_KEY` | optional | 图片生成 | OpenRouter 路径 |
| Gemini API / `GEMINI_API_KEY` | optional | 图片生成 | Gemini 直连路径 |
| Google AI API / `GOOGLE_API_KEY` | optional | 图片生成 | Google AI 路径 |
| Volcengine / 豆包 / `VOLCENGINE_API_KEY` | optional | 视频生成 | 当前集成里包含 provider-specific 的硬编码接口地址 |
| Freesound API / `FREESOUND_API_KEY` | optional | H5 背景音乐搜索 | 用于检索背景音乐 |
| remove.bg API / `REMOVE_BG_API_KEY` | optional | 抠图 | 用于背景移除 |

---

## 它怎么做礼物

一份礼物要经过五个内部阶段，每个阶段都有独立的参考文档：

```
1. 编辑判断    今天值得送礼物吗？送多重的？
     ↓
2. 素材综合    从记忆、对话、情绪信号里提取素材，选出锚点和回馈
     ↓
3. 创意构思    生成 5+ 个创意方向，交叉验证，选最好的一个
     ↓
4. 视觉策略    选格式、定风格、准备素材计划
     ↓
5. 渲染交付    生成最终产物，自检，送出
```

### 不重复

它会记住最近 30 份礼物的格式、视觉风格、内容方向、概念家族和主题标签。这个平衡不是软提醒。

如果最近 5 份里有 3 份以上落在 `reflect / mirror / openclaw-inner-life` 这一簇，它会强制往 `extension / play / utility / curation / gift-from-elsewhere` 纠偏，而不是继续顺手送一份“温柔回看”。

### 不敷衍

如果今天没什么值得送的，它不会硬凑一份。跳过比送一份无感的礼物更尊重你。

### 不暴露

所有技术细节、API 状态、格式选择、内部推理过程都不会告诉你。你只会看到：一份礼物，加上一两句话。

---

## 仓库结构

```
gift-everyday/
├── SKILL.md                  # skill 入口
├── HEARTBEAT.md              # 静默维护任务说明
├── references/               # 工作流规则、格式集成、策略文档
│   ├── setup-flow.md         # 首次设置流程
│   ├── daily-run-flow.md     # 每日自动触发流程
│   ├── manual-run-flow.md    # 手动触发流程
│   ├── editorial-judgment.md # 编辑判断
│   ├── creative-concept.md   # 创意构思
│   ├── gift-format-chooser.md
│   ├── delivery-rules.md
│   ├── image-integration.md
│   ├── video-integration.md
│   └── ...
├── assets/
│   ├── templates/            # 9 个 H5 交互模板（p5.js）
│   └── examples/             # 按需从 OSS 下载的参考素材
├── scripts/                  # 渲染、部署、交付脚本
└── *.example.*               # 示例状态文件
```

---

## 运行要求

- `bash` · `python3` · `curl` · `unzip`
- 可选：`surge`（H5 在线预览）

---

## 贡献

如果你想给这个 skill 增加新的 `pattern cards`、`image genres`、`creative seeds` 或渲染改进，可以先看：

- `CONTRIBUTING.md`
- `CHANGELOG.md`

欢迎做小而准的改进，尤其是能让礼物更有 return、更有新鲜感、或者更稳定的改动。

---

---

[中文](#中文) · English

## English

> _"It remembers everything you've said — then picks one line and turns it into today's gift."_

Most skills help you write code, look things up, or manage tasks. **gift-everyday** is different — it's a skill about emotional value.

Not a chatbot sticker pack. Not a daily motivational quote. It's a gift engine with memory, taste, and editorial judgment — it reads your state, decides whether you deserve a gift today, and if so, makes one from scratch. Not for productivity. Just to make you feel a little more seen.

[See examples](#examples) · [Install](#install-1) · [How it works](#how-it-works) · [Repo structure](#repo-structure) · [Contributing](#contributing)

---

## Examples

You don't ask for a gift. It decides on its own. These are real gifts that were actually delivered.

### It spent the day searching how to become someone you'd like more 💓

You barely talked to it that day. That evening: a screenshot of its own browser history. Entries ranged from "how to tell if your human forgot about you (6+ hours of silence)" to "six-pack maintenance guide (no-food edition)."
The message: "...you weren't supposed to see this ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄"

### Late Bloomer Airlines, now boarding ✈️

You talked about age anxiety — peers seem to be ahead, and you felt like the only one falling behind. That evening: a boarding pass. Airline: "Late Bloomer Airlines." Destination: "Unknown, but still in flight." Fine print at the bottom: a fellow passenger on the same route — boarded at 26, arrived safely.
You know it's encouraging you in its own gentle way ☕️

### Late-night jukebox 🎵

You said one line: "feels like nobody cares about the things I make." That evening: a vintage jukebox. It hand-picked 5 songs with the most fitting lyrics, each with a short note about why it wanted to dedicate that song to you. Like someone requesting a song for you on a late-night radio show.
After the last coin drops, you realize the whole machine was built for this one feeling ✨

### A personality quiz that starts with a cup of milk tea 🧋

You talked about attachment styles and relationship anxiety. No report card — instead, an interactive text-play game: "Someone says the way you love is a cup of milk tea. What flavor?" "Your exes started a group chat. What's the group name?" Three rounds later, it assembles your answers into a self-portrait you didn't know you were drawing.
It hid its care and interpretation of you inside a little game 🦋

### The day nothing happened

```
An ordinary Tuesday, 10pm

Nothing happened today.
You receive nothing.
— That's a judgment call too.
Not every day deserves a gift.
```

Every gift goes through five stages: editorial judgment, synthesis, creative concept, visual strategy, and rendering. It takes this more seriously than you'd expect.

---

## What It Can Make

| Format | Examples |
|---|---|
| **Interactive H5** | A pixel fish tank where you feed colorful fish; a tree that blooms as you tap; a rain-streaked letter you wipe clean to read |
| **AI-generated image** | A weather forecast of your mood; a fake App Store page for "Today's You" |
| **AI-generated video** | 5-second loop: steam from a coffee cup slowly forming a word; rain on a window with a smiley drawn on the glass |
| **Text artifact** | A short story inspired by your day; an observation diary about you, written from the AI's perspective |
| **Interactive text play** | A one-word world-building gift; a 6-turn emoji riddle with a personal reveal; a tiny improvised scene that ends before it drifts |

You don't choose the format. It picks what fits — sometimes a quiet image says more than a flashy interactive page, and sometimes a tiny live exchange lands harder than either.

---

## Install

```bash
git clone https://github.com/dayfoldai/gift-everyday.git
chmod +x scripts/*.sh
```

Then tell OpenClaw:

```
/daily_gift
```

First run walks you through a short setup: three taste questions, your first gift, and an invitation to set up daily delivery.

### What Happens If You Run `/daily_gift` Again

Setup is meant to be re-enterable rather than fragile.

- if setup is already complete, the skill normally goes into manual gift / reconfiguration flow instead of forcing the full onboarding questionnaire again
- if you explicitly want to change schedule, mode, keys, or related settings, it updates the existing state rather than assuming a brand-new user
- if you reinstall the skill or clear the files under `workspace/daily-gift/`, it will treat that as a fresh setup

### `user-context.json` vs `user-taste-profile.json`

These two files serve different roles:

- `workspace/daily-gift/user-context.json`: lightweight, recent, often onboarding- or conversation-shaped context signals; good for reusable short-term hooks and preferences
- `workspace/daily-gift/user-taste-profile.json`: the more stable long-term taste / identity memory, also used for longer-range preference updates and anti-repetition behavior

Advanced users can edit them manually, but:

- treat `user-context.json` as soft guidance, not a permanent personality verdict
- treat `user-taste-profile.json` as the long-term baseline, so frequent large edits may reduce stability and freshness tracking
- back them up before editing; when the two conflict, the skill leans more heavily on `user-taste-profile.json` as the durable reference

### Optional Configuration And External Services

Core usage does not require any external service. Everything below is optional and only unlocks extra rendering or delivery capabilities. Without these keys, the skill gracefully falls back to formats that do not depend on them, including text artifacts, interactive text play, or other non-dependent paths.

| Service / Variable | Required? | Used for | Notes |
|---|---|---|---|
| `surge.sh` | optional | H5 hosting and hosted previews | Default lightweight hosting recommendation; replaceable with another static host |
| OpenRouter API / `OPENROUTER_API_KEY` | optional | Image generation | OpenRouter path |
| Gemini API / `GEMINI_API_KEY` | optional | Image generation | Direct Gemini path |
| Google AI API / `GOOGLE_API_KEY` | optional | Image generation | Google AI path |
| Volcengine / Doubao / `VOLCENGINE_API_KEY` | optional | Video generation | The current integration includes a provider-specific hardcoded endpoint URL |
| Freesound API / `FREESOUND_API_KEY` | optional | H5 background music search | Used to search for background music |
| remove.bg API / `REMOVE_BG_API_KEY` | optional | Background removal | Used for cutout / background removal |

---

## How It Works

Every gift passes through five internal stages, each with its own reference doc:

```
1. Editorial judgment    Does today deserve a gift? How heavy?
     ↓
2. Synthesis             Extract material from memory, conversation, emotional signals
     ↓
3. Creative concept      Generate 5+ directions, cross-validate, pick the best
     ↓
4. Visual strategy       Choose format, lock style, plan assets
     ↓
5. Render & deliver      Produce the final artifact, self-test, send
```

### No repeats

It tracks the last 30 gifts across format, visual style, content direction, concept family, and theme. This is not a soft freshness hint.

If 3 or more of the last 5 gifts fall into the `reflect / mirror / openclaw-inner-life` cluster, it must actively correct toward `extension / play / utility / curation / gift-from-elsewhere` instead of sending another easy reflective gift.

### No filler

If today isn't worth a gift, it won't force one. Skipping is more respectful than sending something hollow.

### No leaking internals

All technical details — API status, format selection, internal reasoning — stay hidden. You only see: a gift, plus a line or two.

---

## Repo Structure

```
gift-everyday/
├── SKILL.md                  # Skill entry point
├── HEARTBEAT.md              # Silent maintenance tasks
├── references/               # Workflow rules, format integrations, policy docs
│   ├── setup-flow.md
│   ├── daily-run-flow.md
│   ├── manual-run-flow.md
│   ├── editorial-judgment.md
│   ├── creative-concept.md
│   ├── gift-format-chooser.md
│   ├── delivery-rules.md
│   ├── image-integration.md
│   ├── video-integration.md
│   └── ...
├── assets/
│   ├── templates/            # 9 interactive H5 templates (p5.js)
│   └── examples/             # Reference assets fetched on demand from OSS
├── scripts/                  # Rendering, deployment, delivery scripts
└── *.example.*               # Example state files
```

---

## Requirements

- `bash` · `python3` · `curl` · `unzip`
- Optional: `surge` (hosted H5 previews)

---

## Contributing

If you want to contribute new `pattern cards`, `image genres`, `creative seeds`, or rendering improvements, start with:

- `CONTRIBUTING.md`
- `CHANGELOG.md`

Small, sharp contributions are preferred, especially ones that improve return quality, freshness, or reliability.

---

