#!/usr/bin/env python3
import json, sys
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print('Usage: compose_wechat_markdown.py <article.json> <output.md> [coverImage] [author]')
        sys.exit(1)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    cover = sys.argv[3] if len(sys.argv) > 3 else ''
    author = sys.argv[4] if len(sys.argv) > 4 else '阿爪'
    data = json.loads(src.read_text(encoding='utf-8'))
    title = data.get('title', '未命名文章')
    summary = data.get('summary', '')
    body = data.get('body', '')
    fm = ['---', f'title: {title}', f'author: {author}', f'summary: {summary}']
    if cover:
        fm.append(f'coverImage: {cover}')
    fm.append('---\n')
    text = '\n'.join(fm) + body.strip() + '\n'
    out.write_text(text, encoding='utf-8')
    print(str(out))

if __name__ == '__main__':
    main()
