# 课堂听译笔记官：安装与使用

## 1. 放置目录
将整个 `classroom-note-translator-openclaw` 文件夹放到：

- 工作区技能目录，或
- `~/.openclaw/skills/`

例如：

```bash
mkdir -p ~/.openclaw/skills
cp -R classroom-note-translator-openclaw ~/.openclaw/skills/classroom-note-translator
```

## 2. 安装依赖

```bash
cd ~/.openclaw/skills/classroom-note-translator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. 配置 OpenClaw
在 `~/.openclaw/openclaw.json` 中为该 skill 注入环境变量：

```json5
{
  skills: {
    entries: {
      "classroom-note-translator": {
        enabled: true,
        env: {
          SENSEAUDIO_API_KEY: "YOUR_SENSEAUDIO_API_KEY",
          NOTION_TOKEN: "OPTIONAL_NOTION_TOKEN"
        },
        config: {}
      }
    }
  }
}
```

## 4. 直接运行脚本测试

```bash
python3 scripts/classroom_note_translator.py \
  --audio ./sample_lecture.mp3 \
  --title "Deep Learning Lecture 03" \
  --model sense-asr-pro \
  --language en \
  --target-language zh \
  --timestamps segment \
  --speaker-diarization \
  --enable-punctuation \
  --output-dir ./outputs
```

视频输入示例（自动抽取音轨）：

```bash
python3 scripts/classroom_note_translator.py \
  --video ./sample_lecture.mp4 \
  --title "Deep Learning Lecture 03" \
  --model sense-asr-pro \
  --language en \
  --target-language zh \
  --timestamps segment \
  --speaker-diarization \
  --enable-punctuation \
  --output-dir ./outputs
```

## 5. 导出到 Notion

```bash
python3 scripts/classroom_note_translator.py \
  --audio ./sample_lecture.mp3 \
  --title "Deep Learning Lecture 03" \
  --export-notion \
  --notion-parent-page-id "YOUR_PARENT_PAGE_ID"
```

## 6. 写入 Obsidian vault

```bash
python3 scripts/classroom_note_translator.py \
  --audio ./sample_lecture.mp3 \
  --title "Deep Learning Lecture 03" \
  --export-obsidian \
  --obsidian-vault "/Users/yourname/Documents/ObsidianVault" \
  --obsidian-folder "Lecture Notes"
```

## 7. 说明
- 脚本默认优先使用 SenseAudio 的翻译能力；当 `segments[].translation` 有值时，会直接生成中英对照笔记。
- 若要获得更强的总结质量，可将 `--summary-provider openai-compatible` 与 `OPENAI_API_KEY` 配合使用。
- Notion 这里采用“创建页面并通过 children 写入内容”的方式。
- Obsidian 这里采用最稳妥的本地 Markdown 落盘方式，因为 Obsidian 原生以 `.md` 文件为主。
- 若使用 `--video`，需先在本机安装 `ffmpeg`。
