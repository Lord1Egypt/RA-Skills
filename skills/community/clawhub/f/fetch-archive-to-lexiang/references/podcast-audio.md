#### 播客音频处理（转录脚本 + 标题文件夹归档）

**当用户提供播客链接时**（小宇宙FM `xiaoyuzhoufm.com`、Apple Podcasts 等），**直接调用脚本完成转录**，然后按标题文件夹结构归档到乐享。

**⚠️ 核心原则**：
- 所有转录逻辑已固化在 `scripts/podcast_to_lexiang.py` 中
- Agent 做 5 件事：WebFetch 获取元信息 + **Show Notes** → 准备 JSON 配置 → 调用脚本转录 → 按标题文件夹结构上传乐享
- **禁止**在 Agent 对话中内联转录代码或逐步推理 ASR 逻辑
- **🚨 Show Notes 必须在逐字稿之前**：节目介绍（嘉宾、摘要、本期剧透/时间线）信息密度高，脚本会自动抓取并插入 `## 节目介绍` 区块

**🚨 乐享目录结构（与视频转录一致）**：

```
贾维斯知识库/
└── 2026-06-03/                        ← 日期目录
    └── <播客标题>/                     ← 标题文件夹
        ├── 文字稿.md（file entry）     ← 主内容：Show Notes + 转录文字稿
        └── 音频.m4a（audio entry）     ← 原始音频文件（VOD 路径上传）
```

**文字稿 Markdown 结构**：

```markdown
# 播客标题

> 播客：… | 平台：…
> 嘉宾：… | 主播：…
> 发布日期：… | 时长：…
> 原始链接：…

---

## 节目介绍

（Show Notes 正文：节目摘要、嘉宾介绍、本期剧透/时间线）

### 本期剧透
1、09:36 …

---

## 逐字稿

**[00:00]** …
```

---

## Agent 操作步骤

### Step 1: WebFetch 获取播客元信息 + Show Notes

从播客页面提取：
- **基础元信息**：标题、节目名、嘉宾、主播、发布日期、时长
- **Show Notes（必抓）**：节目摘要、嘉宾介绍、**本期剧透/章节时间线**——这部分信息密度远高于 ASR 逐字稿，必须保留
- 小宇宙：页面 `description` 字段即完整 Show Notes（含时间线）；yt-dlp 的 `description` 通常只是节目级简介，**不可代替**

### Step 2: 准备 JSON 文件

**metadata.json**（必须）:
```json
{
  "title": "播客标题",
  "show_name": "节目名",
  "guest": "嘉宾",
  "host": "主播",
  "date": "2026-05-26",
  "duration": "139分钟",
  "platform": "小宇宙FM",
  "url": "https://...",
  "shownotes": "完整 Show Notes 正文（从 WebFetch 复制，含本期剧透时间线）"
}
```

> `shownotes` 可选但推荐：若 Agent 已在 WebFetch 阶段抓到，写入此字段；否则脚本会**自动从小宇宙页面抓取**（`__NEXT_DATA__`）。Apple Podcasts 等走 yt-dlp description fallback。

**chapters.json**（推荐，有则章节对齐；无则从 Show Notes 时间线自动提取）:
```json
[
  {"time": 576, "title": "09:36 章节标题1"},
  {"time": 864, "title": "14:24 章节标题2"}
]
```

**hotwords.json**（推荐，提升专有名词准确率）:
```json
[
  {"word": "雨森", "weight": 25},
  {"word": "戴雨森", "weight": 25},
  {"word": "张小珺", "weight": 20},
  {"word": "Anthropic", "weight": 20},
  {"word": "Claude Code", "weight": 18}
]
```

热词来源：
- **人名**（权重 20-25）：嘉宾、主播、被提及的人
- **产品/公司名**（权重 15-20）：shownotes 中的专有名词
- **核心概念**（权重 10-15）：章节标题中的关键术语

### Step 3: 调用脚本（nohup 后台执行）

```bash
# 因为转录耗时长（139分钟音频约10分钟），必须 nohup 后台运行
cd <工作目录> && nohup /usr/bin/python3 \
  <skill_dir>/scripts/podcast_to_lexiang.py \
  "<播客链接>" \
  --output-dir ./output \
  --language zh \
  --metadata-json ./metadata.json \
  --chapters-json ./chapters.json \
  --hotwords-json ./hotwords.json \
  --no-upload \
  > transcribe_log.txt 2>&1 &
```

脚本 Step 0 会自动抓取 Show Notes（小宇宙 `__NEXT_DATA__`）；`--skip-shownotes-fetch` 可跳过；`--shownotes-json` 可传入外部文件。

### Step 4: 等待完成后上传（标题文件夹结构）

**上传流程**：

```bash
# 1. 检查是否完成
grep "✅ Markdown 生成完成\|🎉 转录完成" transcribe_log.txt

# 2. 获取/创建日期目录（先查再建，创建后 before 置顶）
#    → entry_list_children(root_entry_id) 查找今日目录
#    → 找不到则 entry_create_entry(folder) + entry_move_entry(before=第一个)

# 3. 在日期目录下创建「标题文件夹」
#    → entry_create_entry(entry_type="folder", parent_entry_id=<日期目录ID>, name="<播客标题>")

# 4. 上传文字稿到标题文件夹（大文档预签名 URL 方式）
#    → file_apply_upload(parent_entry_id=<标题文件夹ID>, name="<标题>.md", ...)
#    → Python urllib PUT 上传 .md 文件
#    → file_commit_upload 确认

# 5. 上传音频到标题文件夹（VOD 路径）
python3 scripts/upload_video_via_openapi.py <音频.m4a> \
    --space-id <SPACE_ID> --parent-entry-id <标题文件夹ID> --media-type audio
```

**要点**：
- 文字稿 = **节目介绍 + 逐字稿**，放在同一 `.md` 文件
- 文字稿和音频放在同一个标题文件夹下，逻辑绑定
- 文字稿用预签名 URL 上传（file entry），支持全文搜索
- 音频用 OpenAPI VOD 路径上传（audio entry），乐享可在线播放

---

## 技术架构和已知经验

### Show Notes 抓取

| 平台 | 来源 | 说明 |
|------|------|------|
| 小宇宙 FM | `__NEXT_DATA__` → `episode.description` | 完整 shownotes + 本期剧透时间线；**首选** |
| Apple Podcasts 等 | yt-dlp `--dump-json` → `description` | 常为节目级简介，信息量有限 |
| Agent WebFetch | `metadata.json` 的 `shownotes` 字段 | 手工写入优先于自动抓取 |

自动处理：
- footer 截断：「听友来信」「收听渠道」「关于我们」等节目级 boilerplate 不写入文字稿
- 无 `chapters.json` 时，从 Show Notes「1、09:36 标题」格式自动提取章节

### ASR 模型
- **FunASR Paraformer-zh + CT-Punc**（中文准确率 95.7%，标点正确率 92.3%）
- 降级方案：Whisper base（准确率较低，无标点）

### 关键技术决策

| 问题 | 解决方案 | 踩坑记录 |
|------|----------|----------|
| Show Notes 丢失 | Step 0 自动抓取 + `## 节目介绍` 置于 `## 逐字稿` 前 | yt-dlp description ≠ episode shownotes |
| 长音频合并为1段 | 预切片 600s/片 → 逐片转录 | FunASR merge_vad=True 对整段音频会合并全部 |
| 热词不生效 | `generate(hotword="词1 词2")` | `AutoModel(hotword=file)` 是 contextual 模型专用，paraformer-zh 不支持 |
| 无分段/时间戳 | 从逐字 timestamp 按标点切分 | FunASR 返回 `timestamp: [[start_ms, end_ms], ...]` 逐字 |
| torch code signing | 用系统 Python `/usr/bin/python3` | managed Python 的 torch.dylib 签名不匹配 |
| 脚本超时 | `nohup ... &` 后台运行 | WorkBuddy Bash 超时约 2min，139min 音频需 ~10min |
| 大文档上传失败 | 预签名 URL 上传 .md 文件 | MCP content 参数限制约 30K 字符 |
| 标点丢失 | FunASR 内置 ct-punc 模型 | Whisper base 中文几乎无标点输出 |
| 专有名词错误 | 热词偏置 + 后处理替换（可选） | "雨森"→"宇森" 等同音字 |

### 依赖

```bash
# 系统 Python (/usr/bin/python3) 已安装:
# funasr 1.3.9, torch 2.8.0, torchaudio, modelscope, opencc, yt-dlp, ffmpeg
```

### 输出文件

| 文件 | 说明 |
|------|------|
| `output/<标题>.m4a` | 原始音频 |
| `output/audio_16k.wav` | WAV 转换 |
| `output/chunks/chunk_*.wav` | 切片文件 |
| `output/segments.json` | ASR 分段结果（带时间戳） |
| `output/<标题>.md` | 最终 Markdown（**节目介绍 + 逐字稿**） |
| `output/result.json` | 执行结果摘要 |
