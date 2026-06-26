#!/usr/bin/env python3
import argparse
import datetime as dt
import json
from pathlib import Path

TEMPLATE = Path('/Users/bobzhong/.openclaw/workspace/skills/douyin-video-analysis/analysis_template.md')
VAULT = Path('/Users/bobzhong/Library/Mobile Documents/iCloud~md~obsidian/Documents/BobVault')
INBOX = VAULT / 'OpenClaw' / 'Inbox'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    ap.add_argument('--source-url', default='')
    ap.add_argument('--page-url', default='')
    ap.add_argument('--account', default='')
    ap.add_argument('--title', default='')
    ap.add_argument('--duration', default='')
    ap.add_argument('--basis', nargs='*', default=[])
    ap.add_argument('--transcript-note', default='')
    args = ap.parse_args()

    today = dt.date.today().isoformat()
    note = INBOX / f'{today} 抖音视频分析 - {args.topic}.md'
    template = TEMPLATE.read_text(encoding='utf-8')

    basis_lines = []
    basis_map = {
        'meta': '- [x] 页面元信息',
        'visible': '- [x] 页面可见文字',
        'raw_transcript': '- [x] 音频机器转写',
        'cleaned': '- [x] 清洗后可读稿',
    }
    for key in ['meta', 'visible', 'raw_transcript', 'cleaned']:
        basis_lines.append(basis_map[key] if key in args.basis else basis_map[key].replace('[x]', '[ ]'))

    front = f"# 抖音视频分析 - {args.topic}\n\n- 时间：{today}\n- 来源链接：{args.source_url}\n- 实际视频页：{args.page_url}\n- 账号：{args.account}\n- 标题：{args.title}\n- 时长：{args.duration}\n"
    if args.transcript_note:
        front += f"- 关联转写：[[{args.transcript_note}]]\n"
    front += "\n"

    body = template
    body = body.replace('- 来源链接：', f'- 来源链接：{args.source_url}')
    body = body.replace('- 实际视频页：', f'- 实际视频页：{args.page_url}')
    body = body.replace('- 账号：', f'- 账号：{args.account}')
    body = body.replace('- 标题：', f'- 标题：{args.title}')
    body = body.replace('- 时长：', f'- 时长：{args.duration}')

    # replace basis block
    old_basis = "- [ ] 页面元信息\n  - [ ] 页面可见文字\n  - [ ] 音频机器转写\n  - [ ] 清洗后可读稿"
    new_basis = '\n'.join(basis_lines)
    body = body.replace(old_basis, new_basis)

    note.write_text(front + body, encoding='utf-8')
    print(json.dumps({'analysis_note': str(note)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
