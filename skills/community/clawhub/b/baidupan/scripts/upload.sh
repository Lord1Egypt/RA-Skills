#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  upload.sh <本地路径> [--remote 网盘目录] [--force]

Examples:
  upload.sh ~/Downloads/video.mp4
  upload.sh ~/Downloads/video.mp4 --remote /我的视频/
  upload.sh ~/项目/素材/ --remote /我的视频/ --force
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

local_path="$1"
remote_dir="/"
force_flag=""

# 解析参数
shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --remote|-r)
      remote_dir="${2:-/}"
      shift 2
      ;;
    --force|-f)
      force_flag="--force"
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      ;;
  esac
done

# 检查本地路径是否存在
if [[ ! -e "$local_path" ]]; then
  echo "错误：本地路径不存在：$local_path" >&2
  exit 1
fi

echo "=========================================="
echo "  百度网盘上传"
echo "=========================================="
echo "本地路径：$local_path"
echo "网盘目录：$remote_dir"
echo ""

# 判断是文件还是目录
if [[ -d "$local_path" ]]; then
  # 目录上传
  echo "正在上传目录..."
  bypy upload "$local_path" "$remote_dir" $force_flag
else
  # 单个文件上传
  echo "正在上传文件..."
  bypy upload "$local_path" "$remote_dir" $force_flag
fi

echo ""
echo "✓ 上传完成！"
echo "网盘位置：$remote_dir/$(basename "$local_path")"
echo ""
