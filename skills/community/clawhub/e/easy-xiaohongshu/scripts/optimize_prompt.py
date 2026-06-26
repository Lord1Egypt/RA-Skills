from __future__ import annotations

import argparse
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from easy_xhs.common import EasyXHSError
from easy_xhs.content import generate_prompts
from easy_xhs.logging_utils import JsonFormatter, error



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='根据账号信息生成提示词')
    parser.add_argument('--account-type', required=True, help='账号定位')
    parser.add_argument('--content-direction', required=True, help='内容方向')
    parser.add_argument('--target-audience', required=True, help='用户对象')
    parser.add_argument('--topic', required=True, help='主题')
    return parser.parse_args()



def main() -> int:
    args = parse_args()
    result = generate_prompts(
        args.account_type,
        args.content_direction,
        args.target_audience,
        args.topic,
    )
    print(JsonFormatter.dumps(result))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except EasyXHSError as exc:
        error(str(exc))
        raise SystemExit(1)
