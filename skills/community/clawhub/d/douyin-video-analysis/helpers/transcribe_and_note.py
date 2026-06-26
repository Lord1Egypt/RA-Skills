#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

VAULT = Path('/Users/bobzhong/Library/Mobile Documents/iCloud~md~obsidian/Documents/BobVault')
INBOX = VAULT / 'OpenClaw' / 'Inbox'
INBOX.mkdir(parents=True, exist_ok=True)
VENV_PY = '/tmp/douyin_transcribe/venv/bin/python3'


def slugify_topic(title: str) -> str:
    title = re.sub(r'\s+', ' ', title).strip()
    title = title.replace('/', '／')
    title = title.replace(':', '：')
    title = title.replace('?', '？')
    title = title.replace('*', '＊')
    return title[:60] if title else '未命名主题'


def run_transcribe(audio_file: str, model: str = 'mlx-community/whisper-tiny-mlx') -> str:
    code = f"""
from mlx_whisper import transcribe
result = transcribe({audio_file!r}, path_or_hf_repo={model!r}, language='zh', task='transcribe')
print(result['text'])
"""
    p = subprocess.run([VENV_PY, '-c', code], capture_output=True, text=True)
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
    ap.add_argument('--model', default='mlx-community/whisper-tiny-mlx')
    args = ap.parse_args()

    today = dt.date.today().isoformat()
    topic = slugify_topic(args.topic or args.title or '抖音视频')
    transcript_name = f"{today} 抖音视频口播转写 - {topic}.md"
    analysis_name = f"{today} 抖音视频分析 - {topic}.md"
    transcript_path = INBOX / transcript_name
    analysis_path = INBOX / analysis_name

    text = run_transcribe(args.audio_file, args.model)

    transcript_md = f"""# 抖音视频口播转写 - {topic}

- 时间：{today}
- 来源链接：{args.source_url}
- 实际视频页：{args.page_url}
- 账号：{args.account}
- 音频文件：{args.audio_file}
- 转写模型：{args.model}
- 说明：以下为机器转写初稿，可能存在专有名词、数字、断句错误。

## 机器转写初稿

{text}
"""

    analysis_md = f"""# 抖音视频分析 - {topic}

- 时间：{today}
- 来源链接：{args.source_url}
- 实际视频页：{args.page_url}
- 账号：{args.account}
- 关联笔记：[[{transcript_path.stem}]]

## 待分析提纲

### 1. 视频核心在说什么
- 

### 2. 标题/封面钩子怎么设计
- 

### 3. 文案是否像 AI 生成 / AI 辅助
- 

### 4. 批判性思维分析
- 情绪钩子：
- 偷换概念：
- 夸大之处：
- 幸存者偏差：
- 真正有价值的部分：
- 不值得轻信的部分：

### 5. 最终结论
- 
"""

    write_note(transcript_path, transcript_md)
    write_note(analysis_path, analysis_md)

    print(json.dumps({
        'transcript_path': str(transcript_path),
        'analysis_path': str(analysis_path),
        'topic': topic,
        'chars': len(text)
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
