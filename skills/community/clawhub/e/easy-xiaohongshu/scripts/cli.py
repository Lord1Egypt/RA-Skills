from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from easy_xhs.common import EasyXHSError, OUTPUT_CAPTION, OUTPUT_CONTENT, load_config, save_json
from easy_xhs.content import generate_content, generate_prompts, parse_generated_content_prompts
from easy_xhs.image import generate_images
from easy_xhs.logging_utils import JsonFormatter, error, info
from easy_xhs.publish import publish_note



def cmd_optimize(args: argparse.Namespace) -> int:
    result = generate_prompts(args.account_type, args.content_direction, args.target_audience, args.topic)
    print(JsonFormatter.dumps(result))
    return 0



def cmd_generate(args: argparse.Namespace) -> int:
    config = load_config()
    prompts = generate_prompts(args.account_type, args.content_direction, args.target_audience, args.topic)
    result = generate_content(config, prompts['caption_prompt'], prompts['image_prompt'])
    save_json(OUTPUT_CONTENT, result['generated_content'])
    save_json(OUTPUT_CAPTION, result['generated_caption'])
    print(JsonFormatter.dumps({**prompts, **result}))
    return 0



def cmd_images(args: argparse.Namespace) -> int:
    config = load_config()
    content_path = Path(args.content_file)
    if not content_path.exists():
        raise EasyXHSError(f'图文方案文件不存在: {content_path}')
    content_text = content_path.read_text(encoding='utf-8')
    try:
        content_data = json.loads(content_text)
    except json.JSONDecodeError:
        content_data = content_text
    prompts = parse_generated_content_prompts(content_data)
    if not prompts:
        raise EasyXHSError('未从图文方案中解析到任何“成品图生成提示词”')
    try:
        style = json.loads(args.style)
    except json.JSONDecodeError as exc:
        raise EasyXHSError(f'--style 不是合法 JSON: {exc}') from exc
    if not isinstance(style, dict):
        raise EasyXHSError('--style 必须是 JSON 对象')
    images = generate_images(config, prompts, style, args.negative_prompt)
    print(JsonFormatter.dumps({'images': images}))
    return 0



def cmd_publish(args: argparse.Namespace) -> int:
    config = load_config()
    result = publish_note(config, args.title, args.content, args.images, args.tags)
    print(JsonFormatter.dumps(result))
    return 0



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Easy-xiaohongshu 统一 CLI')
    sub = parser.add_subparsers(dest='command', required=True)

    p1 = sub.add_parser('optimize', help='生成提示词')
    for p in [p1]:
        p.add_argument('--account-type', required=True)
        p.add_argument('--content-direction', required=True)
        p.add_argument('--target-audience', required=True)
        p.add_argument('--topic', required=True)
    p1.set_defaults(func=cmd_optimize)

    p2 = sub.add_parser('generate', help='生成图文方案和发布文案')
    for p in [p2]:
        p.add_argument('--account-type', required=True)
        p.add_argument('--content-direction', required=True)
        p.add_argument('--target-audience', required=True)
        p.add_argument('--topic', required=True)
    p2.set_defaults(func=cmd_generate)

    p3 = sub.add_parser('images', help='批量生成图片')
    p3.add_argument('--content-file', default=str(OUTPUT_CONTENT))
    p3.add_argument('--style', default='{}')
    p3.add_argument('--negative-prompt', default='')
    p3.set_defaults(func=cmd_images)

    p4 = sub.add_parser('publish', help='发布到小红书')
    p4.add_argument('--title', required=True)
    p4.add_argument('--content', required=True)
    p4.add_argument('--images', nargs='+', required=True)
    p4.add_argument('--tags', nargs='*', default=[])
    p4.set_defaults(func=cmd_publish)

    return parser



def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except EasyXHSError as exc:
        error(str(exc))
        raise SystemExit(1)
