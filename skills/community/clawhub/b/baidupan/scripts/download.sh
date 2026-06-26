#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  download.sh <网盘路径> [--out 本地目录] [--force]

Examples:
  download.sh /我的视频/video.mp4
  download.sh /我的视频/video.mp4 --out ~/Downloads/
  download.sh /我的视频/素材/ --out ~/项目/ --force
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

remote_path="$1"
local_dir="."
force_flag=""

# 解析参数
shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --out|-o)
      local_dir="${2:-.}"
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

# 确保本地目录存在
mkdir -p "$local_dir"

echo "=========================================="
echo "  百度网盘下载"
echo "=========================================="
echo "网盘路径：$remote_path"
echo "本地目录：$local_dir"
echo ""

# 判断是文件还是目录
if [[ "$remote_path" == */ ]]; then
  # 目录下载
  echo "正在下载目录..."
  bypy download "$remote_path" "$local_dir" $force_flag
else
  # 单个文件下载
  echo "正在下载文件..."
  filename=$(basename "$remote_path")
  bypy downfile "$remote_path" "$local_dir/$filename"
fi

echo ""
echo "✓ 下载完成！"
echo "保存位置：$local_dir"
echo ""
