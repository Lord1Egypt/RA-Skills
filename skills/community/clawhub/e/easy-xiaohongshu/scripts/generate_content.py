from __future__ import annotations

import argparse
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from easy_xhs.common import EasyXHSError, OUTPUT_CAPTION, OUTPUT_CONTENT, load_config, save_json
from easy_xhs.content import generate_content, generate_prompts
from easy_xhs.logging_utils import JsonFormatter, error, info



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='生成小红书图文方案与发布文案')
    parser.add_argument('--account-type', required=True, help='账号定位')
    parser.add_argument('--content-direction', required=True, help='内容方向')
    parser.add_argument('--target-audience', required=True, help='用户对象')
    parser.add_argument('--topic', required=True, help='主题')
    parser.add_argument('--print-only', action='store_true', help='仅输出结果，不写入文件')
    return parser.parse_args()



def main() -> int:
    args = parse_args()
    config = load_config()
    prompts = generate_prompts(
        args.account_type,
        args.content_direction,
        args.target_audience,
        args.topic,
    )
    result = generate_content(config, prompts['caption_prompt'], prompts['image_prompt'])

    payload = {
        'style_preset': prompts['style_preset'],
        'recommended_tags': prompts['recommended_tags'],
        **result,
    }

    if args.print_only:
        print(JsonFormatter.dumps(payload))
    else:
        save_json(OUTPUT_CAPTION, payload['generated_caption'])
        save_json(OUTPUT_CONTENT, payload['generated_content'])
        print(JsonFormatter.dumps(payload))
        info(f'已写入 {OUTPUT_CONTENT.name} 和 {OUTPUT_CAPTION.name}')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except EasyXHSError as exc:
        error(str(exc))
        raise SystemExit(1)
