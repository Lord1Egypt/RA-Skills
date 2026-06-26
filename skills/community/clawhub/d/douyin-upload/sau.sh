#!/bin/bash
# Social Auto Upload CLI
# 保存到: /usr/local/bin/sau

# 项目路径
PROJECT_DIR="/Users/yiwanjun/Downloads/github/social-auto-upload"

# 激活虚拟环境并执行
source "${PROJECT_DIR}/venv/bin/activate"
python "${PROJECT_DIR}/cli_main.py" "$@"
