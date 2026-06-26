#!/usr/bin/env python3
"""
transcribe_and_note.py — Linux 版
使用 faster-whisper 替代 mlx-whisper
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get('DOUYIN_OUTPUT_DIR',
                                  str(Path.home() / 'Documents' / 'douyin_analysis')))
VENV_PY = os.environ.get('DOUYIN_VENV_PY', '/tmp/douyin_transcribe/venv/bin/python3')


def slugify_topic(title: str) -> str:
    title = re.sub(r'\s+', ' ', title).strip()
    for ch in '/', ':', '?', '*':
        title = title.replace(ch, '？' if ch == '?' else '／')
    return title[:60] if title else '未命名主题'


def run_transcribe(audio_file: str, model: str = 'Systran/faster-whisper-medium') -> str:
    code = f"""
from faster_whisper import transcribe
r, info = None, None
def _run():
    global r, info
    r, info = transcribe({str(audio_file)!r}, model="medium", language="zh", task="transcribe")
    text = " ".join([s.text for s in r[0]])
    print(text)
_run()
"""
    p = subprocess.run([VENV_PY, '-c', code], capture_output=True, text=True, timeout=600)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip() or 'transcription failed')
    return p.stdout.strip()


def write_note(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audio-file', required=True)
    ap.add_argument('--title', default='')
    ap.add_argument('--page-url', default='')
    ap.add_argument('--source-url', default='')
    ap.add_argument('--account', default='')
    ap.add_argument('--topic', default='')
    ap.add_argument('--model', default='Systran/faster-whisper-medium')
    args = ap.parse_args()

    today = dt.date.today().isoformat()
    topic = slugify_topic(args.topic or args.title or '抖音视频')
    note_name = f"{today} 抖音视频分析 - {topic}.md"
    note_path = OUTPUT_DIR / note_name

    text = run_transcribe(args.audio_file, args.model)

    combined_md = f"""# 抖音视频分析 - {topic}

- 时间：{today}
- 来源链接：{args.source_url}
- 实际视频页：{args.page_url}
- 账号：{args.account}
- 音频文件：{args.audio_file}
- 转写模型：{args.model}

---

## 口播转写

> 说明：以下为机器转写初稿，可能存在专有名词、数字、断句错误。

{text}

---

## 分析笔记

### 1. 视频核心在说什么
-

### 2. 内容摘要
- 钩子：
- 核心主张：
- 论据支撑：
- 结论：

### 3. 有效信息 + 证据清单

| 信息点 | 视频提供的证据 | 可信度 |
|--------|--------------|--------|
|        |              | 高/中/低 |

### 4. 标题/封面钩子怎么设计
-

### 5. 文案是否像 AI 生成 / AI 辅助
-

### 6. 批判性思维分析
- 情绪钩子：
- 偷换概念：
- 夸大之处：
- 幸存者偏差：
- 真正有价值的部分：
- 不值得轻信的部分：

### 7. 最终结论
-
"""

    write_note(note_path, combined_md)

    print(json.dumps({
        'note_path': str(note_path),
        'topic': topic,
        'chars': len(text)
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
