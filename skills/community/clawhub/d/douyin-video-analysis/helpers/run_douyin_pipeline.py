#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

BASE = Path('/Users/bobzhong/.openclaw/workspace/skills/douyin-video-analysis/helpers')
GRAB = BASE / 'douyin_grab.py'
TRANSCRIBE = BASE / 'transcribe_and_note.py'


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip() or f'command failed: {cmd}')
    txt = p.stdout.strip()
    # tolerate accidental leading log lines
    start = txt.find('{')
    if start == -1:
        raise RuntimeError(f'no JSON object in output: {txt[:400]}')
    return json.loads(txt[start:])


def pick_account(body_preview: str) -> str:
    skip = {
        '开启读屏标签', '读屏标签已关闭', '精选', '推荐', '搜索', '关注', '我的', '直播', '放映厅', '短剧',
        '客户端', '壁纸', '通知', '私信', '投稿', '倍速', '智能', '清屏', '连播', '章节要点', '内容由AI生成',
        '展开', '播放中', '举报', '全部评论', '留下你的精彩评论吧', '加载中', '点击加载更多', '推荐视频'
    }
    lines = [line.strip() for line in (body_preview or '').splitlines() if line.strip()]
    for i, s in enumerate(lines):
        if s in skip:
            continue
        if re.search(r'[#0-9:/：]|https?://', s):
            continue
        if '粉丝' in s or '获赞' in s:
            continue
        # strongest clue: creator name often appears right before a 粉丝/获赞 line
        if i + 1 < len(lines) and ('粉丝' in lines[i + 1] or '获赞' in lines[i + 1]):
            return s
    for s in lines:
        if s in skip:
            continue
        if re.search(r'[#0-9:/：]|https?://', s):
            continue
        if 2 <= len(s) <= 12:
            return s
    return ''


def short_topic(title: str) -> str:
    t = title or '抖音视频'
    t = t.split(' - 抖音')[0].strip()
    t = re.sub(r'\s+', ' ', t)
    return t[:30]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--topic', default='')
    ap.add_argument('--account', default='')
    ap.add_argument('--model', default='mlx-community/whisper-tiny-mlx')
    args = ap.parse_args()

    grab = run_json(['python3', str(GRAB), args.url])

    audio_file = grab.get('audio_file')
    if not audio_file:
        raise RuntimeError(f"audio_file missing; grab result: {json.dumps(grab, ensure_ascii=False)}")

    title = grab.get('title', '')
    page_url = grab.get('page_url', '')
    body_preview = grab.get('body_preview', '')
    account = args.account or pick_account(body_preview)
    topic = args.topic or short_topic(title)

    transcribe = run_json([
        'python3', str(TRANSCRIBE),
        '--audio-file', audio_file,
        '--title', title,
        '--source-url', args.url,
        '--page-url', page_url,
        '--account', account,
        '--topic', topic,
        '--model', args.model,
    ])

    out = {
        'input_url': args.url,
        'page_url': page_url,
        'title': title,
        'account': account,
        'topic': topic,
        'audio_file': audio_file,
        'audio_url': grab.get('audio_url'),
        'transcript_path': transcribe.get('transcript_path'),
        'analysis_path': transcribe.get('analysis_path'),
        'transcript_chars': transcribe.get('chars'),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
