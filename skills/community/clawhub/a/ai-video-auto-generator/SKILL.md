---
name: ai-video-auto-generator
version: 2.7.0
description: "AI 短视频全自动流水线：从想法到成片，一键出视频。脚本生成→自动修复→资产生成→视频→音频→字幕，全自动无人值守。| AI video auto pipeline: from idea to final video, one command. Script generation → auto repair → assets → video → audio → subtitles, fully automated."
category: video-generation
platforms:
  - WorkBuddy
  - QClaw
  - ima
  - Claude Code
  - Cursor
tags:
  - video
  - ai-video
  - pipeline
  - automation
  - short-video
  - tts
  - subtitle
  - script-generation
---

> 📖 **README**: `README.md` | **CHANGELOG**: `CHANGELOG.md`

# ai-video-auto-generator

将书面需求转换为结构化视频脚本，用于AI视频生成流水线。

**目录**
- <a href="#agent-mode">🤖 Agent 使用模式（核心工作流）</a>
- <a href="#quick-start">⚡ Quick Start（4 路径出片）</a>
- <a href="#architecture">🏗️ 流水线架构</a>
- <a href="#verification">🔍 验证体系</a>
- <a href="#self-healing">🩹 自愈机制</a>
- <a href="#cli">🛠️ 流水线 CLI</a>
- **参考文档**
  - [端到端案例](references/e2e-walkthrough.md)
  - [脚本生成检查清单](references/script-json-checklist.md)
  - [Provider 配置](references/provider-config.md)
  - [景别设计](references/shot-scales.md)
  - [剪辑与包装](references/editing-specs.md)
  - [节奏与叙事结构](references/pacing-narrative.md)
  - [Prompt 工程规则](references/prompt-rules.md)
  - [视频生成模式](references/video-modes.md)
  - [环境搭建](references/setup-guide.md)
  - [流水线排错](references/troubleshooting.md)
  - [Segment 合并设计](references/segment-design.md) — 仅小云雀 Provider

---

<h2 id="quick-start">⚡ Quick Start（4 路径出片）</h2>

**🔥 尝鲜（30 秒出预览，无需 API Key）：**
```bash
# 在 skill 根目录执行
python skills/project-generate/scripts/pipeline.py --project ./sample --mode demo
```

**💬 一句话生成视频（推荐，通过 AI Agent）：**
```bash
# 1. 在 WorkBuddy 中加载 ai-video-auto-generator skill
# 2. 直接告诉 AI Agent 你的需求，例如：
#    "帮我做一个古代将军在现代城市醒来的短视频，紧张氛围，约30秒"
# 3. Agent 会自动：分析需求 → 生成 script.json → 跑流水线 → 出片
```

> 📌 **脚本生成已由 AI Agent 接管。** 之前的 `--mode generate` / `--prompt` 命令已废弃，保留入口但不再执行脚本生成。所有脚本生成直接在对话中完成。

**📄 从文档生成视频（通过 AI Agent）：**
```bash
# 直接把文件/URL/飞书链接发给 AI Agent
# Agent 会自动读取内容 → 生成 script.json → 跑流水线
```

**📦 从模板创建（手动编辑）：**
```bash
# 在 skill 根目录执行
python scripts/create_project.py --project "$HOME/WorkBuddy/我的视频" --template short_drama
cd "$HOME/WorkBuddy/我的视频" && python skills/project-generate/scripts/pipeline.py --mode auto
```

> 详细说明见 `README.md`。

---

<h2 id="agent-mode">🤖 Agent 使用模式（核心工作流）</h2>

> **你提供需求，AI Agent（当前对话）帮你搞定一切。** 不需要手动调命令，直接说就好。

### 如何与 Agent 配合

| 你的输入 | Agent 自动执行 |
|---------|---------------|
| `"帮我做一个军事短剧，紧张氛围"` | ① 解析需求 → 生成 `script.json` → 写回项目目录<br>② 创建角色卡、场景卡、镜头列表<br>③ 运行 `--mode auto` 启动流水线 |
| `"从这篇文章生成视频"` + 贴 URL | ① WebFetch 读取文章内容<br>② 分析角色/场景/情绪 → 生成 `script.json`<br>③ 运行 `--mode auto` |
| `"从这份文档生成视频"` + 上传文件 | ① Read 读取文档内容<br>② 提取关键信息 → 生成 `script.json`<br>③ 运行 `--mode auto` |
| `"帮我优化这个脚本"` + 贴 JSON | ① 读取当前 `script.json`<br>② 运行 `optimize` 命令（OptimizerV2）做 12 维叙事修复<br>③ 输出修复报告 |
| `"修一下 shot_05 的运镜问题"` | ① 定位问题<br>② 修改 `script.json`<br>③ 通知验证结果 |

### Agent 脚本生成规则（重要）

当 Agent 为你生成 `script.json` 时，遵循以下标准：

```
📋 角色卡要求:
  - 每个角色必须有 name / title / appearance（clothing/physique/face/features）
  - appearance 要细化到发型、脸型、瞳色、肤色、体态、着装
  - 每个角色至少 front + face 两个视图，主角加 side + back
  - asset_background 固定为 "white"

📋 场景卡要求:
  - 每个场景有 name / description / views（广角/中景/特写）
  - description 描述环境氛围（光线/色调/空间感/情绪）

📋 镜头要求（最重要）:
  - 每个镜头有 id / description / duration
  - voice_over（旁白）和 dialogue（对白）根据以下规则填写：

    voice_over 旁白（TTS 音频 + 字幕）:
    ── 谁在说话: 非角色，解说/叙事者/内心独白
    ── 适用 shot_type: 远景/广角/空镜/建立/转场/过渡
    ── 视频是否自带声音: ❌ 不包含，需 TTS 生成
    ── 写作要求: 用人类叙事语言，不能直接照搬 description
        正确: "硝烟弥漫的废墟战场上，周戎站在高处俯视着远方。"
        错误: "周戎在画面远处，突然，废墟战场全景，硝烟弥漫，断壁残垣中周戎站在废墟高处俯视战场，广角远景"
    ── 生成后自检: voice_over 中不能有景别（中景/远景/特写/广角）、拍摄指令（俯拍/仰拍）、角色定位（"在画面远处"）
    ── 标点规则: 用空格代替所有标点符号（逗号/句号/感叹号等），但需保证断句合理，方便 TTS 自然停顿
        断句规则:
        - 每个空格代表一次自然停顿，每段 5~10 个汉字为宜，便于 TTS 一口气读完
        - 在完整语义单位后断句：场景描述后 / 动作完成后 / 人物出现后
        - 禁止在修饰语和中心语之间断开（"硝烟弥漫的"和"废墟战场"之间不能断）
        - 主语和谓语不断开（"周戎站在高处"不能断为"周戎 站在高处"）
        - 动词和宾语不断开（"俯瞰着整片战场"不能断为"俯瞰着 整片战场"）
        正确: "硝烟弥漫的废墟战场上 断壁残垣间 周戎站在高处俯瞰着整片战场"
        错误: "硝烟弥漫的 废墟战场上 断壁残垣间 周戎 站在 高处 俯瞰着 整片战场"

    dialogue 对白（仅字幕，视频已自带声音）:
    ── 谁在说话: 屏幕上的角色在对话/独白/回应
    ── 适用 shot_type: 中景/双人/过肩/反应/独白/近景
    ── 视频是否自带声音: ✅ Agnes 视频已包含角色对话声

    两者可共存: voice_over 放旁白，dialogue 放对白
    两者都无: 纯画面镜头（动作/追逐/环境），无台词

  - 每个镜头生成后必须做三选一检查：是否决定好了 voice_over / dialogue / 两者皆无
  - 不允许出现: 镜头 ≥5 秒且 voice_over/dialogue 都为空，且 description 未描述动作/追逐内容

  - description 包含: 景别 + 运镜 + 人物动作 + 环境 + 情绪
  - ⚠️ **description 中涉及角色的地方必须使用角色卡中的全名或实词（如「君无烬（奶牛猫）」或「君无烬」），禁止使用「猫」「狗」「他」「她」「男子」「女子」「老人」等泛称代词。**
  - 反例: 「猫吃得太急 不小心打了一个响亮的嗝」（「猫」是泛称，optimizer 无法匹配到具体角色）
  - 正例: 「君无烬（奶牛猫）吃得太急 不小心打了一个响亮的嗝」
  - 理由: optimizer 的 `_fix_shots` 靠文本匹配补全 characters 字段，泛称会绕过全部四种匹配规则（全名/实词/括号内容/逐字），导致角色缺失不被发现
  - duration 3-8 秒，总时长控制在 60-120 秒
  - 前 3 个镜头要有钩子（冲突/悬念/意外）
  - 高潮镜头放在总时长的 70-85% 处
  - 收尾镜头要有结局感

📋 叙事结构:
  - 开头抓人 → 展开 → 冲突升级 → 高潮 → 收尾
  - 运镜要变化（不要连续 3+ 镜头同运镜）
  - 情绪要有起伏（不要从欢快跳到悲伤）
  - 对话和动作镜头比例合理（各不超过 70%）

📋 流水线触发:
  - script.json 写完后，自动执行 `pipeline.py --mode auto`
  - 如果项目已有 task_tracker 且部分完成，auto 会自动从断点继续
```

### 快速命令

```bash
# Agent 一键出片（在对话中描述需求即可）
# 上述步骤全部由 AI Agent 自动完成

# 如果你需要手动查状态
tail -f auto.log          # 查看流水线进度
```

---

<h2 id="architecture">🏗️ 流水线架构</h2>

```
AI Agent（你） → script.json → 9 阶段全自动流水线 → final.mp4

阶段 0:   脚本优化（含 12 维叙事结构修复）
阶段 1:   构建资产 prompt 文件
阶段 2:   角色资产生成 + 6 维质量验证（55 分制）
阶段 3:   辅助资产生成 + 质量验证
阶段 4:   场景资产生成 + 人脸检测 + 风格检测
阶段 5:   初始化首帧图
阶段 6:   首帧图生成 + 50 分制验证
阶段 7:   提交视频任务 + 验证 prompt
阶段 8:   轮询完成 + 55 分制视频验证 + 拼接 + 音频 + 字幕

全部阶段支持断点续跑。
```

<h2 id="verification">🔍 验证体系</h2>

| 资产 | 检查项 | 评分 |
|------|--------|------|
| 角色图 | 文件+模糊+人物=1+背景+全身+风格 | 55 分 |
| 场景图 | Haar 人脸检测 + Canny 风格匹配 | pass/fail |
| 首帧图 | 文件+比例+模糊+HOG人数+色彩 | 50 分 |
| 视频 | 时长+比例+黑帧+光流运镜+情绪匹配 | 55 分 |

<h2 id="self-healing">🩹 自愈机制</h2>

```
fail → classify(5 categories) → strategy(soften/switch/backoff/regen) → capped retry(max 10)
```

<h2 id="cli">🛠️ 流水线 CLI</h2>

```bash
python skills/project-generate/scripts/pipeline.py --mode setup       # 环境检测 + 自动装依赖 + 复制 Key 模板
python skills/project-generate/scripts/pipeline.py --mode auto         # 全自动流水线（从中断继续）
python skills/project-generate/scripts/pipeline.py --mode validate     # 预检（只验证不生成）
python skills/project-generate/scripts/pipeline.py --mode demo         # 快速尝鲜（30 秒，无需 API Key）
python skills/project-generate/scripts/pipeline.py --mode poll --detached  # 仅轮询

# 项目级子命令（project_generate.py）
python skills/project-generate/scripts/project_generate.py --project . status        # 结构化状态（默认 JSON，--text 人类可读）
python skills/project-generate/scripts/project_generate.py --project . stitch --tracker local  # 单独跑拼接（不重新提交/轮询）
```

---

## 参考文档

- [端到端案例](references/e2e-walkthrough.md) — 从飞书文档到成片的完整流程
- [脚本生成检查清单](references/script-json-checklist.md)
- [Provider 配置](references/provider-config.md)
- [景别设计](references/shot-scales.md)
- [剪辑与包装](references/editing-specs.md)
- [节奏与叙事结构](references/pacing-narrative.md)
- [Prompt 工程规则](references/prompt-rules.md)
- [视频生成模式](references/video-modes.md)
- [环境搭建](references/setup-guide.md)
- [流水线排错](references/troubleshooting.md)
- [Segment 合并设计](references/segment-design.md) — 仅小云雀(xiaoyunqiao) Provider 需要

---

## English Quick Start

> **AI video auto pipeline: from idea to final video, one command.**

### How it works

Load this skill in WorkBuddy, then tell the AI agent what you want:

```
"Create a short video about an ancient general waking up in a modern city"
"Generate a video from this article" + paste URL
"Turn this document into a video" + upload file
```

The agent will:
1. Read and analyze your input
2. Generate a complete `script.json` (characters, scenes, shots)
3. Run `pipeline.py --mode auto` — fully automated pipeline
4. Notify you when `final.mp4` is ready

### Pipeline stages

| Stage | Description |
|-------|-------------|
| 0 | Script optimization (incl. 12-dim narrative auto repair: hook/pacing/camera/emotion/closure) |
| 1 | Build asset prompt files |
| 2 | Character asset generation + 6-dim quality verification (55pt) |
| 3 | Troop asset generation + verification |
| 4 | Scene asset generation + face detection + style check |
| 5 | Initialize first frames |
| 6 | First frame generation + 50pt verification |
| 7 | Submit video tasks + prompt verification |
| 8 | Poll completion + 55pt video verification (camera motion/mood/black frames) + stitch + audio + subtitles |

All stages support resume from checkpoint (Ctrl+C / crash / shutdown).

### CLI reference

```bash
python skills/project-generate/scripts/pipeline.py --mode setup       # Auto-install dependencies + copy API key template
python skills/project-generate/scripts/pipeline.py --mode auto         # Full pipeline (resume from checkpoint)
python skills/project-generate/scripts/pipeline.py --mode validate     # Pre-flight check (no generation)
python skills/project-generate/scripts/pipeline.py --mode demo         # 30s preview, no API key needed
python skills/project-generate/scripts/pipeline.py --mode poll --detached  # Poll only
```

### Known limitations

- Requires API Key for AI generation (default: Agnes AI, free unlimited tier)
- Windows prioritized (macOS/Linux not fully tested)
- OpenCV ~50MB dependency (auto-installed via `--mode setup`)
- No real-time progress bar (logs written to file in detach mode)

### Reference docs

- [Provider config](references/provider-config.md)
- [Shot scales](references/shot-scales.md) (Chinese)
- [Prompt rules](references/prompt-rules.md) (Chinese)
- [Troubleshooting](references/troubleshooting.md) (Chinese)
