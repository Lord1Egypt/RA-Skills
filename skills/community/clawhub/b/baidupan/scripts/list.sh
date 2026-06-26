#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  list.sh [网盘路径] [--detail]

Examples:
  list.sh                  # 列出根目录
  list.sh /我的视频        # 列出指定目录
  list.sh /我的视频 --detail  # 显示详细信息
EOF
  exit 2
}

path="${1:-/}"
detail=false

# 解析参数
if [[ "$#" -gt 1 ]]; then
  for arg in "${@:2}"; do
    case "$arg" in
      --detail|-d)
        detail=true
        ;;
      -h|--help)
        usage
        ;;
    esac
  done
fi

echo "=========================================="
echo "  百度网盘文件列表"
echo "=========================================="
echo "路径：$path"
echo ""

if [[ "$detail" == true ]]; then
  bypy list "$path" -v
else
  bypy list "$path"
fi

echo ""
