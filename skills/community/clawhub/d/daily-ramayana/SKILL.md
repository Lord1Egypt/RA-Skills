---
name: daily-ramayana
description: "Daily reading of the Indian epic Rāmāyaṇa (罗摩衍那, Vālmīki) — all 7 Kāṇḍas from bundled public-domain English text (Griffith Books 1–6 + Dutt Book 7), one segment per episode with auto-tracked progress, a full Chinese lecture (English excerpt, 中文译述, Indian culture background, 西游记/哈奴曼 links), an Indian-miniature-style illustration and a Chinese voice narration. 每日讲读印度史诗《罗摩衍那》，逐段推进、自动记进度，中文讲稿+细密画配图+语音。Use when the user says 罗摩衍那, 今日罗摩衍那, 继续读罗摩衍那, 罗摩衍那第N期, daily ramayana, ramayana, or when a daily-ramayana routine fires."
---

# 每日罗摩衍那 Daily Ramayana

逐段讲读蚁垤（Vālmīki）《罗摩衍那》全七篇：童年篇 → 阿逾陀篇 → 森林篇 → 猴国篇 → 美妙篇 → 战斗篇 → 后篇。从蚁垤听那罗陀讲述"完人罗摩"开始，到罗摩归天结束。

每期交付三件：**中文讲稿（必有）→ 细密画配图 → 中文语音**。进度自动追踪，下次说"继续读罗摩衍那"就接着讲。

**GitHub/YumSkills 分发包含全书英文原文**（`data/books/book01.md`..`book07.md` 与合订本 `data/ramayana-full.md`；来源和公版说明见 `data/SOURCE.md`）。ClawHub 包不含这些多兆字节原文文件，以符合注册表的上传限制；在 ClawHub 安装版中若原文数据缺失，应从官方仓库 `https://github.com/yumyumtum/YumSkills/tree/main/daily-ramayana` 获取相应书卷，不要假设它已随 ClawHub 包安装。中文译述与讲解由你基于原文生成。

`SKILL_DIR` = 本 skill 的安装目录（如 `/home/box/agent-data/workflows/daily-ramayana`）。

---

## 🛡️ 弹性优先交付（Resilience First · 重要）

1. **文字最先产出、必送达。** 讲稿写完先写盘、先交付给用户，再做图和语音。
2. **配图、语音各自独立。** 互不阻塞；任一失败，另一件照做，文字不受影响。
3. **吞错继续，绝不整轮放弃。** GenerateImage 报错/超时最多重试 1 次，然后跳过；语音脚本返回 `RAMAUDIO_ERR` 就跳过。
4. **进度在文字完成后立即推进**（Step 5），不要等图和语音；这样图/音失败也不会重复讲同一段。
5. 缺的那件如实告诉用户（"今天配图没生成出来"），不要假装有。
6. 如果由定时任务驱动，同一天再次触发时先跑 `python3 /workspace/library/library.py status --book ramayana`，看今天这期 `missing` 缺哪件，只补缺的并补归档，不重讲（`progress.py status` 里的 `lastEpisode.completedAt` 可判断今天是否已推进）。

---

## 📚 书库归档（Library · 每期必做）

本 skill 产出的**所有东西（讲稿 / 配图 / 语音 / 朗读稿）都要按章节顺序归档到自己的书目录**，将来可以按顺序导出成一本书（Markdown / HTML，后续可转 PDF、PPT），用户不用 AI、也不用在聊天记录里翻。

- 书目录：`/workspace/library/ramayana/`（本书专属，别的 skill 不往这里写）
- 每期一个文件夹：`/workspace/library/ramayana/bookBB/epNNN/`（BB = 篇号两位，NNN = 全书期号三位，如 `book01/ep003/`）
  - `lecture.md` 讲稿（图片/音频用**相对路径**引用，文件夹自包含）
  - `image.png` 配图
  - `voice.mp3` 语音
  - `read.txt` 朗读稿
- `book.json`：按期号排序的清单（导出脚本读它）；`index.md`：目录（期号、篇、标题、日期、相对链接）。两者都由归档脚本自动维护，**不要手改**。
- 归档脚本：`/workspace/library/library.py`（导出：`/workspace/library/export_book.py ramayana`）。脚本源文件在本仓库 `daily-library/`；安装时复制或软链接到 `/workspace/library/`，上面的命令默认走这个运行时路径。

归档命令（文件可以先生成在任意临时位置，脚本会复制进书目录、把讲稿里的图片/音频改成相对链接、更新 `book.json` 和 `index.md`）：

```bash
python3 /workspace/library/library.py add --book ramayana --episode <N> --chapter <篇号 book> --title "本期标题" \
  --date <YYYY-MM-DD，太平洋时间当天> --range "<cantos，如 Canto II. …>" \
  --lecture <讲稿.md> --image <配图文件> --audio <语音.mp3> --read <朗读稿.txt>
```

- **分件归档、可重复执行**：文字写好就先 `add --lecture`（保底）；配图、语音做好后再用**同一个 `--episode` 和 `--chapter`** 各补一次 `add --image …` / `add --audio … --read …`。重复 add 同一期只会补齐/覆盖对应文件，不会重复建期。
- 查缺补漏：`python3 /workspace/library/library.py status --book ramayana` 列出每期缺哪件（`missing`），以及 `next_episode`。
- 期号 `<N>` 以本 skill 进度为准（`progress.py next` 返回的 `episode`；篇号用返回的 `book`），与讲稿标题里的"第 N 期"一致。
- 归档失败**不阻塞**给用户的交付（吞错继续），但要尽量完成；不要把归档路径、脚本输出念给用户或写进讲稿正文。
- 用户说"导出 罗摩衍那"时：`python3 /workspace/library/export_book.py ramayana` → 生成 `/workspace/library/ramayana/export/ramayana.md` 和 `ramayana.html`（按期序、带图和音频播放器）；加 `--embed-images` 可把图片内嵌进单个 HTML，`--from/--to` 选期号范围。

---

## 首次使用

默认语言是中文（`zh`），不用询问。用户明确要英文时：

```bash
python3 "$SKILL_DIR/scripts/progress.py" set-lang --lang en
```

进度文件：`~/.daily-ramayana/progress.json`（可用环境变量 `DAILY_RAMAYANA_PROGRESS` 改路径）。

---

## 生成一期

### Step 1：取下一段原文

```bash
python3 "$SKILL_DIR/scripts/progress.py" next
```

返回 JSON（`next` 不移动游标）：
- `episode`：本期期号（= 已完成期数 + 1），用于文件名 `NNN`（三位零填充）
- `book` / `book_name` / `book_name_zh`：第几篇（1–7）
- `cantos`：本段涉及的章（如 `["Canto I. Nárad."]`；带 `(cont.)` 表示接上期未完的章）
- `translator`：本段英译者（第 7 篇为 Dutt 散文 OCR 本，可能有识别错字）
- `consumed`：本段字符数（**Step 5 advance 要用**）
- `text`：本段英文原文（约 1500–2500 字符，尽量整章收尾）
- `last_in_book`：本段是本篇最后一段
- `done_all: true`：全书讲完 → 发一期总结祝贺，不再推进

### Step 2：读懂本段

读 `text`，弄清人物、地点、情节。参考 `SKILL_DIR/references/structure.md`：当前篇的主线、**中文译名表**（必须统一使用）、文化背景、与《西游记》的关联点。遇到 Griffith 的 `[I omit …]` 方括号说明，要在译述里交代。

### Step 3：写讲稿

先读 `SKILL_DIR/references/style-guide.md`。中文模式格式：

```markdown
## 📖 每日罗摩衍那 · 第 N 期

**篇章：** 第 X 篇 · 梵名（中文篇名）· Canto …
**人物：** 本期出场人物（中文译名）
**本期看点：** 一句话概括

---

### 📜 原文节录
> [英文原文精选 6–16 行诗或 2–4 句散文，保留分行]

### 🗣️ 中文译述
[按情节顺序完整译述本段全部内容，可分【小标题】]

### 📚 背景讲解
[3–5 个要点：本段在主线中的位置、印度宗教文化（法、恩典与诅咒、种姓、仪式、神祇）、地理今地、文学与后世流传；与西游记/孙悟空的关联只在确实相关时提，并说明是学术说法]

### 🔮 下期预告
[一两句]

---
📍 进度：第 X 篇 / 7 · 第 N 期
```

英文模式：同样结构，标题换成 `Daily Ramayana · Episode N`，译述换成英文复述与讲解。

### Step 4：写盘并交付文字（保底）

- 讲稿先写到工作文件 `/workspace/ramayana/ramayana-NNN.md`（`mkdir -p /workspace/ramayana`），**立刻归档进书库**：

  ```bash
  python3 /workspace/library/library.py add --book ramayana --episode N --chapter <book> \
    --title "本期标题" --range "<cantos>" --lecture /workspace/ramayana/ramayana-NNN.md
  ```

  → `/workspace/library/ramayana/bookBB/epNNN/lecture.md`
- **立刻把讲稿正文作为回复交付给用户**（直接在对话里发 markdown 正文；不要只发文件路径）。

### Step 5：推进进度

```bash
python3 "$SKILL_DIR/scripts/progress.py" advance <consumed> --title "本期标题"
```

### Step 6：配图（独立 · 失败跳过）

- 用 **GenerateImage**，`aspect_ratio: "16:9"`，`filename: "ramayana-NNN.png"`。
- prompt 要点：**Indian miniature painting**（Rajput / Pahari-Kangra / Mughal court style），平涂矿物颜料、金色勾线、装饰花边框；画本期最有画面感的一幕，写清人物、动作、场景（例："Rama, blue-skinned prince with bow, and Lakshmana following the sage Vishvamitra through a forest hermitage at dawn"）；画面内不要文字。
- 生成后把文件复制到 `/workspace/ramayana/ramayana-NNN.png`，归档：`library.py add --book ramayana --episode N --chapter <book> --image /workspace/ramayana/ramayana-NNN.png`（→ `epNNN/image.png`），并把图片展示给用户。
- 失败重试 1 次；仍失败就跳过并说明。

### Step 7：语音（独立 · 失败跳过）

1. 写 300–800 字中文朗读稿到 `/workspace/ramayana/ramayana-NNN-read.txt`：开头"每日罗摩衍那，第 N 期。"，讲本期情节主线 + 一个文化要点 + 下期预告；纯文本，无 markdown、无英文长段、无路径。
2. 合成（edge-tts `zh-CN-XiaoxiaoNeural`、`--rate=-10%`，默认垫一层很轻的坦布拉琴式持续低音，自动避让人声）：

   ```bash
   bash "$SKILL_DIR/scripts/ramayana-audio.sh" /workspace/ramayana/ramayana-NNN-read.txt /workspace/ramayana/ramayana-NNN-voice.mp3
   # 不要背景音：末尾加 --no-bed
   ```

   输出 `RAMAUDIO_OK` 成功；`RAMAUDIO_WARN` = 背景音失败但人声已出；`RAMAUDIO_ERR` = 跳过；`RAMAUDIO_SKIP` = 设置了 NO_TTS。
   脚本不可用时的兜底：`uvx edge-tts --voice zh-CN-XiaoxiaoNeural --rate=-10% --file <read.txt> --write-media <out.mp3>`。
3. 归档：`library.py add --book ramayana --episode N --chapter <book> --audio /workspace/ramayana/ramayana-NNN-voice.mp3 --read /workspace/ramayana/ramayana-NNN-read.txt`（→ `epNNN/voice.mp3`、`read.txt`）。
4. 把 mp3 作为附件交付给用户。
5. 最后跑 `library.py status --book ramayana`，确认本期 `missing` 为空（或只缺确实失败的那件）。

### 产物命名

正式存档（书库，按篇/期排序，导出用）：

```
/workspace/library/ramayana/
  book.json  index.md
  book01/ep001/
    lecture.md   讲稿（相对链接引用 image.png / voice.mp3）
    image.png    配图
    voice.mp3    语音
    read.txt     朗读稿
```

`/workspace/ramayana/ramayana-NNN*.{md,png,mp3,txt}` 只是生成时的工作文件，归档后以书库为准。

---

## 进度管理

| 命令 | 说明 |
|---|---|
| `status` | 当前篇、偏移、百分比、当前章、已完成期数 |
| `next` | 输出下一段（JSON，不移动游标） |
| `advance <consumed> [--title "…"]` | 推进游标；本篇读完自动进入下一篇 |
| `set --book N [--offset M \| --canto XII]` | 跳到某篇 / 某章（如用户说"从哈奴曼跳海开始讲"→ `set --book 5`） |
| `reset` | 从头开始（保留语言和分段设置） |
| `set-lang --lang zh\|en` | 切换语言 |

分段长度在 progress.json 的 `segCharsMin / segCharsTarget / segCharsMax`（默认 1500 / 2000 / 2500 英文字符）。按默认值全书约 1170 期；用户嫌慢可把三者调大（如 3000/4000/5000，约 600 期）。

---

## 全书结构速览

| 篇 | 梵名 | 中文 | 看点 |
|---|---|---|---|
| 1 | Bāla Kāṇḍa | 童年篇 | 史诗缘起、罗摩出生、随众友仙人除妖、折弓娶悉多 |
| 2 | Ayodhyā Kāṇḍa | 阿逾陀篇 | 宫廷阴谋、流放十四年、十车王之死、婆罗多奉草鞋 |
| 3 | Araṇya Kāṇḍa | 森林篇 | 首哩薄那迦、金鹿计、罗波那劫悉多 |
| 4 | Kiṣkindhā Kāṇḍa | 猴国篇 | 哈奴曼登场、猴国结盟、寻找悉多 |
| 5 | Sundara Kāṇḍa | 美妙篇 | **哈奴曼跃海、夜探楞伽、火烧楞伽** |
| 6 | Yuddha Kāṇḍa | 战斗篇 | 造桥渡海、楞伽大战、诛罗波那、回国登基 |
| 7 | Uttara Kāṇḍa | 后篇 | 罗波那家世、悉多被弃、双生子、罗摩归天 |

详见 `references/structure.md`。

---

## 注意事项

- 每期只讲"这一段"，不要一次讲完一章以上的后续情节。
- 中文要像中文；不臆造原文没有的情节；神话照实讲。
- 不要把脚本、路径、JSON 输出给用户；用户只看讲稿、图和语音。
- 重新生成原文（一般不需要）：`python3 "$SKILL_DIR/scripts/build_text.py" <raw_dir>`，raw_dir 需含 `pg24869.txt` 和 `TheRamayanaUttaraKandam.txt`（下载地址见 `data/SOURCE.md`）。
