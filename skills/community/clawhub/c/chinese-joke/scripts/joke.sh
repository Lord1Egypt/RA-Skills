#!/usr/bin/env bash

# 中文笑话库工具
# 用法：joke <command> [options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

python3 "${ROOT_DIR}/scripts/joke.py" "$@"
