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

## 🛡️ 弹性优先交付（Resilience First · 重要）

本 skill 默认要稳定交付【文字 + 地图 + 语音】三件，必须做到**单步失败不拖垮整体**：

1. **文字最先发、必送达。** 先把讲稿正文发出去，再去做地图/语音。文字是保底——哪怕地图和语音都失败，用户也已经拿到了今天的讲解。
2. **地图、语音各自独立交付。** 三件互不阻塞：地图失败不影响语音，语音失败不影响地图，二者都失败也不影响已发出的文字。
3. **吞错继续，绝不整轮 abort。** 任何工具调用报错/中断（尤其是 `image_generate` 的 abort/超时），都要就地捕获、跳过该件、继续下一件，**严禁让单步失败导致整个任务 abort、用户什么都收不到**。
4. **进度只在文字发出后推进**，避免重复，也避免漏发。
5. **给 image_generate 设合理 timeoutMs**（如 180000），失败最多重试 1 次就放弃该件。
6. 若用定时任务驱动，建议再配一个**延时校验补发**任务（如主任务后 20–30 分钟跑一次），检查今天三件是否齐全、缺哪件补哪件（已送达则不重发）。

> 经验教训（真实案例）：曾有一期因为地图生成环节 abort，整个定时任务被 abort，导致**文字和语音都没发出去**（只出了图）。根因就是把文字/地图/语音纳入了同一条「要么全成、要么全挂」的线性流程。修正办法就是上面六条：文字先发、各件独立、吞错继续。

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

## 📚 书库归档（Library · 每期必做）

本 skill 产出的**所有东西（讲稿 / 路线地图 / 语音 / 朗读稿）都要按章节顺序归档到自己的书目录**，将来可以按顺序导出成一本书（Markdown / HTML，后续可转 PDF、PPT），用户不用 AI、也不用在聊天记录里翻。

- 书目录：`/workspace/library/xuanzang/`（本书专属，别的 skill 不往这里写）
- 每期一个文件夹：`/workspace/library/xuanzang/volVV/epNNN/`（VV = 卷号两位，NNN = 期号三位，如 `vol01/ep004/`）
  - `lecture.md` 讲稿（图片/音频用**相对路径**引用，文件夹自包含）
  - `map.png` 路线地图
  - `voice.mp3` 语音
  - `read.txt` 朗读稿
- `book.json`：按期号排序的清单（导出脚本读它）；`index.md`：目录（期号、卷、标题、日期、相对链接）。两者都由归档脚本自动维护，**不要手改**。
- 归档脚本：`/workspace/library/library.py`（导出：`/workspace/library/export_book.py xuanzang`）。脚本源文件在本仓库 `daily-library/`；安装时复制或软链接到 `/workspace/library/`，上面的命令默认走这个运行时路径。

归档命令（文件可以先生成在任意临时位置，脚本会复制进书目录、把讲稿里的图片/音频改成相对链接、更新 `book.json` 和 `index.md`）：

```bash
python3 /workspace/library/library.py add --book xuanzang --episode <N> --chapter <卷号> --title "本期标题" \
  --date <YYYY-MM-DD，太平洋时间当天> --range "本期涉及的古国" \
  --lecture <讲稿.md> --image <路线地图文件> --audio <语音.mp3> --read <朗读稿.txt>
```

- **分件归档、可重复执行**：文字写好就先 `add --lecture`（保底）；路线地图、语音做好后再用**同一个 `--episode` 和 `--chapter`** 各补一次 `add --image …` / `add --audio … --read …`。重复 add 同一期只会补齐/覆盖对应文件，不会重复建期。
- 查缺补漏：`python3 /workspace/library/library.py status --book xuanzang` 列出每期缺哪件（`missing`），以及 `next_episode`。
- 期号 `<N>` 以本 skill 进度为准（`progress.py next` 前的已完成期数 + 1，即 `history` 条数 + 1），与讲稿标题里的"第 N 期"一致。
- 归档失败**不阻塞**给用户的交付（吞错继续），但要尽量完成；不要把归档路径、脚本输出念给用户或写进讲稿正文。
- 用户说"导出 西域记"时：`python3 /workspace/library/export_book.py xuanzang` → 生成 `/workspace/library/xuanzang/export/xuanzang.md` 和 `xuanzang.html`（按期序、带图和音频播放器）；加 `--embed-images` 可把图片内嵌进单个 HTML，`--from/--to` 选期号范围。

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
- `aspectRatio 16:9`，分辨率 2K，文件名形如 `xuanzang-NNN-map.png`；生成后用 `library.py add --image` 归档为 `/workspace/library/xuanzang/volVV/epNNN/map.png`（见「书库归档」）。
- **prompt 要点：**
  - 古地图 / 古籍插图风，强对比、深色线条、**标签清晰可读、填满画面**
  - 金色虚线标出玄奘西行路线，**从东往西**推进
  - 标出本期涉及的古国，**每个地名同时标 中文古名 + 今地拼音/英文**（如 龟兹 Kucha、焉耆 Yanqi、那烂陀 Nālandā）
  - 附指南针、标题横幅、山脉与沙漠/河流地貌；博物馆级参考地图质感
  - 背景随西行进度切换区域：丝路北道（塔里木盆地）→ 中亚 → 阿富汗 → 北/中/南印度
  - 标签以中文为主、辅以英文
- 若地图生成失败，仍照常交付文字讲稿，并诚实说明地图缺失，不要假装有图。

### Step 5: 语音朗读（按配置可选 · 默认带轻背景音乐）

- **语音**：中文默认生成适合朗读的稿（300–800 字），讲史/诵经般庄重；叙事类默认**配轻背景音乐（古琴/箫/古筝）**，只做氛围铺底、音量低、**不盖人声**。
- **推荐用封装好的音频助手脚本**（已集成 edge-tts 语音 + 古琴/箫氛围 + 侧链压制，且自带容错与 NO_TTS 检查），避免每次手搓 ffmpeg：

  ```bash
  # 1) 先把朗读纯文本写到一个文件（只放可朗读正文，无 markdown / 路径 / JSON）
  # 2) 调用助手（使用方可把脚本放在自己的 scripts/ 下；参考实现见下）
  bash <WORKSPACE>/scripts/xuanzang-audio.sh /tmp/xz_read_NNN.txt /tmp/xuanzang-NNN-voice.mp3
  # 脚本不可用时兜底：uvx edge-tts --voice zh-CN-XiaoxiaoNeural --rate=-10% --file <read.txt> --write-media <out.mp3>
  # 然后归档：library.py add --book xuanzang --episode N --chapter V --audio <mp3> --read <read.txt>
  ```

  脚本 stdout：`XZAUDIO_OK` = 成功；`XZAUDIO_SKIP` = NO_TTS 跳过（正常）；`XZAUDIO_ERR/WARN` = 音频不可用（跳过，别 abort）。
  > 参考脚本：`~/clawd/scripts/xuanzang-audio.sh`（合成五声音阶 drone 做古琴/箫氛围，sidechain 让配乐自动避让人声）。
- 投递语音：在 Telegram 用消息工具 `asVoice=true` + `media=<本地mp3>` 发语音气泡；只对可朗读正文做 TTS，不要把执行说明/进度播报念出来。
- **配图（可选）**：从本期最有画面感的圣迹/场景生成（佛塔、石窟、那烂陀讲堂、雪山垭口、商旅入城等），水墨/工笔/电影分镜感，重氛围不画证件照。

### Step 6: 写盘 + 推进进度

**交付顺序（弹性优先）：** 先写讲稿 → **先发文字（保底）** → 推进进度 → 地图（独立交付）→ 语音（独立交付）。

讲稿**必须**归档进书库：`library.py add --book xuanzang --episode N --chapter <卷号> --title … --lecture <讲稿.md>`（详见「书库归档」），落到 `/workspace/library/xuanzang/volVV/epNNN/lecture.md`。讲稿正文里不要再写绝对路径的地图引用（如“（路线地图：/workspace/...）”），图片和语音由归档脚本以相对链接插入。

推进进度（`<consumed>` 用 Step 1 拿到的值）：

```bash
python3 SKILL_DIR/scripts/progress.py advance <consumed> --title "本期标题"
```

- 若本期配置为 **文字 + 地图 +（图/语音）**，缺项不算完成（除非用户接受缺项版本）。
- 不允许"先推进进度、地图/语音以后再补"的默认行为。

### Step 6.5: 归档地图与语音（书库 · 重要）

地图、语音各自做好后，分别用同一期号补进书库（互不阻塞，失败吞错继续）：

```bash
python3 /workspace/library/library.py add --book xuanzang --episode N --chapter V --image <地图.png>
python3 /workspace/library/library.py add --book xuanzang --episode N --chapter V --audio <语音.mp3> --read <朗读稿.txt>
```

交付结束前跑一次 `library.py status --book xuanzang`，确认本期 `missing` 为空（或只缺确实失败的那件）。
定时任务的「延时校验补发」也以 `status` 的 `missing` 为准：缺哪件补哪件，并补归档。

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
- 每期产物以 `/workspace/library/xuanzang/` 书库为准；`/workspace/xuanzang/` 只是旧的临时目录，不再作为存档。
