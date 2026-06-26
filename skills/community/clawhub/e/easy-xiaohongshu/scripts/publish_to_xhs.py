from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from easy_xhs.common import EasyXHSError, OUTPUT_CAPTION, load_config
from easy_xhs.logging_utils import JsonFormatter, error
from easy_xhs.publish import publish_note



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='通过 xiaohongshu-mcp 发布图文笔记到小红书')
    parser.add_argument('--title', help='标题')
    parser.add_argument('--content', help='正文')
    parser.add_argument('--images', nargs='+', required=True, help='图片路径列表')
    parser.add_argument('--tags', nargs='*', default=[], help='标签列表')
    parser.add_argument('--caption-file', default=str(OUTPUT_CAPTION), help='文案 JSON 文件；当未传 title/content 时自动读取')
    return parser.parse_args()



def load_caption_fields(caption_file: str) -> dict:
    path = Path(caption_file)
    if not path.exists():
        raise EasyXHSError(f'文案文件不存在: {path}')
    data = json.loads(path.read_text(encoding='utf-8'))
    return {
        'title': data.get('title', ''),
        'content': data.get('content', ''),
        'tags': data.get('tags', []),
    }



def main() -> int:
    args = parse_args()
    config = load_config()

    title = args.title or ''
    content = args.content or ''
    tags = list(args.tags or [])

    if not title or not content:
        fields = load_caption_fields(args.caption_file)
        title = title or fields['title']
        content = content or fields['content']
        if not tags:
            tags = list(fields.get('tags', []))

    result = publish_note(config, title, content, args.images, tags)
    print(JsonFormatter.dumps(result))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except EasyXHSError as exc:
        error(str(exc))
        raise SystemExit(1)
