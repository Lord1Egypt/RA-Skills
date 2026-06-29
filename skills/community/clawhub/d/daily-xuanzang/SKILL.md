---
name: daily-xuanzang
description: >
  Daily reading of the Great Tang Records on the Western Regions (大唐西域记) — Xuanzang's
  Western Journey across the Silk Road and India, all 12 fascicles (CBETA T51n2087), with
  auto-tracked progress, vernacular/English translation, a bilingual route map, and voice.
  每日讲读《大唐西域记》——玄奘西行丝路与印度全程，逐段推进，自动追踪进度，默认配中英文路线地图、白话翻译与语音。
  Triggers / 触发词: 「大唐西域记」「西域记」「玄奘西行」「daily xuanzang」「今日西域记」「继续读西域记」「xuanzang」「xiyuji」
---

# 每日西域记 Daily Xuanzang

逐段讲读玄奘《大唐西域记》全 12 卷（《大正藏》No.2087），从高昌出发，沿丝绸之路北道穿越中亚，翻越葱岭进入五印度，遍历佛陀生灭四大圣地与那烂陀寺，再原路返回于阗——亲践 110 国、传闻 28 国，共 138 国的地理风土实录。

每讲包含：**原文节录 → 白话/英文翻译 → 背景讲解 → 下期预告**，并默认配一张**中英文路线示意地图**标出"今天西行到哪里"。自动追踪进度，支持配图与语音朗读。

**本 skill 自带原典全文**（`data/volumes/vol01.txt` .. `vol12.txt`），无需联网取经文；翻译与讲解由 AI 基于原文生成。

---

## 默认交付要求（重要）

- 默认不要只给"短摘要版"；应交付一篇**完整讲稿**（原文 / 翻译 / 讲解三部分都要展开）。
- 默认按 **四步交付**：
  1. **文字成稿**（完整讲稿，先产出）
  2. **路线地图**（中英文标签，标出本期涉及的古国 + 今地名）
  3. **配图**（可选：本期最有画面感的圣迹/场景）
  4. **语音**（可选：基于成稿正文或精炼朗读稿）
- **只要用户当前配置或当前任务明确包含文字 / 地图 / 图片 / 语音中的任一项，就必须把对应产物全部生成出来。**
- **地图是本 skill 的核心特色，默认每期都要有**，除非用户明确关闭。
- 如果用户明确只要文字，才可以跳过地图/图/语音；否则默认至少"文字 + 地图"都要有。

---

## 首次使用 / First Run

第一次触发时，询问语言偏好：

> 欢迎来到「每日西域记」！请选择语言 / Welcome! Choose your language:
> - **中文 (zh):** 原文 + 白话翻译 + 中文讲解
> - **English (en):** Original text + English translation + English commentary

用户选择后运行（`SKILL_DIR` 为本 skill 安装目录）：

```bash
python3 SKILL_DIR/scripts/progress.py set-lang --lang zh   # 或 en
```

进度文件保存在 `~/.openclaw/workspace/daily-xuanzang/progress.json`。

---

## 生成每日讲稿 / Generating a Lecture

### Step 1: 取下一段原文

```bash
python3 SKILL_DIR/scripts/progress.py next
```

返回 JSON 字段：
- `vol`：当前卷号（1–12）
- `seg_index`：本卷内第几段
- `consumed`：本段消耗的字符数（**advance 时要用**）
- `text`：本段文言原文
- `remaining_after`：本卷剩余字符
- `done_volume: true`：本卷已讲完（再次 `next` 会自动进入下一卷开头）
- `done_all: true`：全书 12 卷讲完（发祝贺收尾，不再推进）

### Step 2: 识别本段地理

读 `text`，从 `XX國` / `至XX國` 识别本段讲到的古国/圣迹，并查出对应**今地名**（如 阿耆尼=焉耆、屈支=龟兹/库车、缚喝=巴尔赫、那烂陀=Nālandā）。这一步既用于起标题，也用于画地图。

可参考 `SKILL_DIR/references/structure.md` 了解当前卷的时代地理范围。

### Step 3: 生成讲稿

读 `SKILL_DIR/references/style-guide.md` 了解格式与风格，然后据 `text` 与语言偏好生成讲稿。

#### 中文模式输出格式

```markdown
## 📖 每日西域记 · 第 X 期

**卷次：** 卷X（某区域 · 某干国）
**今地：** [古国 = 今地名对照]
**本期路线：** [从哪到哪]

---

### 📜 原文节录
> [精选原文]

### 🗣️ 白话翻译
[逐段翻译]

### 📚 背景讲解
[这段讲哪国/哪圣迹、地理今地、历史与佛教价值、相关典故；3–5 要点]

### 🔮 下期预告
[一句话勾起好奇]

---
📍 进度：卷 X / 12
```

#### English Mode Output Format

```markdown
## 📖 Daily Xuanzang · Episode X

**Fascicle:** Vol. X (Region · key kingdom)
**Today:** [ancient name = modern place]
**Route:** [from → to]

---

### 📜 Original Text
> [Selected classical Chinese]

### 🗣️ Translation
[English translation]

### 📚 Background
[Which kingdom/sacred site, modern geography, historical & Buddhist significance, related lore]

### 🔮 Next Time
[Teaser]

---
📍 Progress: Vol. X / 12
```

### Step 4: 生成中英文路线地图（默认执行 · 本 skill 核心）

- 用图像生成工具，**优先选当前环境里渲染文字标签最清晰的模型**。经验：`google/gemini-3.1-flash-image-preview` 在标签清晰度上表现好；若 `openai/gpt-image-*` 在本环境已正确鉴权，它对密集文字标签通常更强，可优先尝试。
- `aspectRatio 16:9`，分辨率 2K，文件名形如 `xiyuji-map-NNN.png`。
- **prompt 要点：**
  - 古地图 / 古籍插图风，强对比、深色线条、**标签清晰可读、填满画面**
  - 金色虚线标出玄奘西行路线，**从东往西**推进
  - 标出本期涉及的古国，**每个地名同时标 中文古名 + 今地拼音/英文**（如 龟兹 Kucha、焉耆 Yanqi、那烂陀 Nālandā）
  - 附指南针、标题横幅、山脉与沙漠/河流地貌；博物馆级参考地图质感
  - 背景随西行进度切换区域：丝路北道（塔里木盆地）→ 中亚 → 阿富汗 → 北/中/南印度
  - 标签以中文为主、辅以英文
- 若地图生成失败，仍照常交付文字讲稿，并诚实说明地图缺失，不要假装有图。

### Step 5: 配图与语音（按配置可选）

- **配图**：从本期最有画面感的圣迹/场景生成（佛塔、石窟、那烂陀讲堂、雪山垭口、商旅入城等），水墨/工笔/电影分镜感，重氛围不画证件照。
- **语音**：中文默认生成适合朗读的稿（300–800 字），讲史/诵经般庄重；若工作区有"叙事配轻背景音乐（古琴/箫/古筝）"偏好，遵循之。

### Step 6: 写盘 + 推进进度

**顺序：** 先文字 → 地图 →（可选图/语音）→ 最后推进进度。

讲稿建议写入使用方工作区的讲解库（如 `~/clawd/data/xiyuji/讲解/NNN-标题.md` 或使用方自定路径），并在文件内附地图路径引用。

推进进度（`<consumed>` 用 Step 1 拿到的值）：

```bash
python3 SKILL_DIR/scripts/progress.py advance <consumed> --title "本期标题"
```

- 若本期配置为 **文字 + 地图 +（图/语音）**，缺项不算完成（除非用户接受缺项版本）。
- 不允许"先推进进度、地图/语音以后再补"的默认行为。

---

## 投递方式 / Delivery

本 skill 不绑定特定频道或定时任务。使用者可：

- **手动触发：** 对话中说「今日西域记」「继续读西域记」「daily xuanzang」等
- **定时任务：** 通过 cron / heartbeat 定时调用，配置目标频道
- **图片投递：** 在 Telegram 等渠道，地图/配图务必用消息工具的 media 参数发真图，不要只发裸链接文本

示例：每天 19:00 取下一段 → 生成讲稿 + 中英文地图 → 发送到指定频道。

---

## 进度管理 / Progress Management

进度脚本 `SKILL_DIR/scripts/progress.py`，数据存于 `~/.openclaw/workspace/daily-xuanzang/progress.json`。

| 命令 | 说明 |
|------|------|
| `status` | 查看当前游标 + 语言 |
| `next` | 输出下一段原文（JSON） |
| `advance <consumed> [--title "..."]` | 推进游标 N 个字符 |
| `set --volume N --offset M` | 跳到指定卷/偏移 |
| `reset` | 从头开始（保留语言偏好） |
| `set-lang --lang zh\|en` | 切换语言 |

### 进度 JSON 格式

```json
{
  "currentVolume": 1,
  "charOffset": 921,
  "segIndex": 1,
  "segCharsTarget": 900,
  "language": "zh",
  "history": [
    { "volume": 1, "segIndex": 0, "consumed": 921, "title": "阿耆尼国→屈支国", "completedAt": "2026-06-18T..." }
  ]
}
```

> `segCharsTarget` 控制每段目标长度（默认 900 字，在句末标点处收尾，不硬切句子）。可在 progress.json 手动调大/调小。

---

## 全书结构速览 / Structure

| 卷 | 收录 | 地理范围 | 看点 |
|---|---|---|---|
| 1 | 三十四国 | 西域 + 中亚 | 丝路北道：焉耆、龟兹、撒马尔罕 |
| 2 | 三国 + 印度总述 | 北印度入口 | **印度总论**（名称/气候/文字/种姓/法律） |
| 3 | 八国 | 北印度（犍陀罗、克什米尔） | 乌仗那、迦湿弥罗 |
| 4 | 十五国 | 北印→中印过渡 | 秣菟罗（马图拉） |
| 5 | 六国 | 中印度恒河中游 | 曲女城戒日王、钵逻耶伽 |
| 6 | 四国 | 佛陀生灭圣地 | 舍卫城、迦毗罗卫(佛诞)、拘尸那揭罗(涅槃) |
| 7 | 五国 | 恒河下游 | 鹿野苑(初转法轮)、吠舍釐 |
| 8 | 摩揭陀(上) | 中印度 | **菩提伽耶·成道处** |
| 9 | 摩揭陀(下) | 中印度 | **那烂陀寺**（玄奘留学地） |
| 10 | 十七国 | 东 + 南印度 | 迦摩缕波(阿萨姆)、羯陵伽 |
| 11 | 二十三国 | 南 + 西印度 + 锡兰 | 僧伽罗(斯里兰卡) |
| 12 | 二十二国 | 回程：葱岭 → 于阗 | 瞿萨旦那(于阗)收尾 |

完整脉络见 `references/structure.md`。

---

## 注意事项 / Notes

- 每期只讲"今天这一段"，不要一次把整卷讲完。
- 翻译力求信达：中文要像中文、英文要像英文；**不臆造原文没有的内容**；生僻地名保留音译并注今地。
- 地图标签必须**中英文都有**。
- 全书约 39 万字，以每期约 900 字计，约 430+ 期可读完。
- 不要把内部脚本细节 / 路径 / 进度 JSON 输出给用户，用户只看到讲稿 + 地图成品。
