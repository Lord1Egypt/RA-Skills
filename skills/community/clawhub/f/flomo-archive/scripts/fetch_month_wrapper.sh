#!/bin/bash
# Flomo Archive Skill 包装脚本
# 确保在当前 shell 环境中执行

cd "$(dirname "$0")"
python3 fetch_month.py "$@"
