#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""风格推荐器。"""

from __future__ import annotations

import argparse
import json

from easy_xhs.common import EasyXHSError
from easy_xhs.style import load_style_presets, match_style_preset



def main() -> int:
    parser = argparse.ArgumentParser(description="根据账号定位推荐风格预设")
    parser.add_argument("account_type", help="账号定位，例如：科技博主")
    args = parser.parse_args()

    presets = load_style_presets()
    if not presets:
        raise EasyXHSError("未读取到 style-presets.json")

    result = match_style_preset(args.account_type, presets)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
