#!/usr/bin/env bash
# 兼容入口：委托总 skill 根目录的共享 install.sh
exec "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/install.sh" "$@"
