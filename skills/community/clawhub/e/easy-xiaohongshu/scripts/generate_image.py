from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from easy_xhs.common import EasyXHSError, load_config
from easy_xhs.content import parse_generated_content_prompts
from easy_xhs.image import clear_progress, generate_images
from easy_xhs.logging_utils import JsonFormatter, error, info



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='根据生成好的图文方案批量生成图片')
    parser.add_argument('--content-file', default=str(Path(__file__).resolve().parents[1] / 'generated_content.json'), help='图文方案文件')
    parser.add_argument('--style', default='{}', help='样式预设 JSON 字符串')
    parser.add_argument('--negative-prompt', default='', help='负向提示词')
    parser.add_argument('--clear-progress', action='store_true', help='清空断点续传记录')
    return parser.parse_args()



def parse_style_arg(style_raw: str) -> dict:
    try:
        style = json.loads(style_raw)
    except json.JSONDecodeError as exc:
        raise EasyXHSError(f'--style 不是合法 JSON: {exc}') from exc
    if not isinstance(style, dict):
        raise EasyXHSError('--style 必须是 JSON 对象')
    return style



def main() -> int:
    args = parse_args()
    config = load_config()
    content_path = Path(args.content_file)
    if not content_path.exists():
        raise EasyXHSError(f'图文方案文件不存在: {content_path}')

    if args.clear_progress:
        clear_progress()
        info('已清空进度文件')

    content_text = content_path.read_text(encoding='utf-8')
    try:
        content_data = json.loads(content_text)
    except json.JSONDecodeError:
        content_data = content_text
    prompts = parse_generated_content_prompts(content_data)
    if not prompts:
        raise EasyXHSError('未从图文方案中解析到任何“成品图生成提示词”')

    style_preset = parse_style_arg(args.style)
    output_files = generate_images(config, prompts, style_preset, args.negative_prompt)
    print(JsonFormatter.dumps({'images': output_files, 'count': len(output_files)}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except EasyXHSError as exc:
        error(str(exc))
        raise SystemExit(1)
