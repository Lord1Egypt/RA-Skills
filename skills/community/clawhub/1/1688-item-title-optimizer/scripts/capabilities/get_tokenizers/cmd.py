#!/usr/bin/env python3
"""分词器列表获取 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.get_tokenizers.service import get_tokenizers

COMMAND_NAME = "get_tokenizers"
COMMAND_DESC = "获取可用的分词器列表"


def main():
    try:
        result = get_tokenizers()
        print_output(True, "✅ 分词器列表获取成功", result)
    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    main()
