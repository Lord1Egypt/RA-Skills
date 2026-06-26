#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  sync.sh <direction> <源路径> <目标路径>

Direction:
  down  - 从网盘同步到本地（网盘为主）
  up    - 从本地同步到网盘（本地为主）
  both  - 双向同步（谨慎使用）

Examples:
  sync.sh down /我的视频/项目 ~/本地备份/
  sync.sh up ~/本地项目/ /我的视频/项目/
EOF
  exit 2
}

if [[ $# -lt 3 ]]; then
  usage
fi

direction="$1"
source_path="$2"
target_path="$3"

echo "=========================================="
echo "  百度网盘同步"
echo "=========================================="

case "$direction" in
  down)
    echo "同步方向：网盘 → 本地"
    echo "网盘路径：$source_path"
    echo "本地路径：$target_path"
    echo ""
    mkdir -p "$target_path"
    bypy syncdown "$source_path" "$target_path"
    ;;
  up)
    echo "同步方向：本地 → 网盘"
    echo "本地路径：$source_path"
    echo "网盘路径：$target_path"
    echo ""
    if [[ ! -e "$source_path" ]]; then
      echo "错误：本地路径不存在：$source_path" >&2
      exit 1
    fi
    bypy syncup "$source_path" "$target_path"
    ;;
  both)
    echo "同步方向：双向同步"
    echo "本地路径：$source_path"
    echo "网盘路径：$target_path"
    echo ""
    echo "⚠️  警告：双向同步可能导致文件冲突！"
    read -p "确认继续？(y/N) " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
      echo "已取消"
      exit 0
    fi
    bypy sync "$source_path" "$target_path"
    ;;
  *)
    echo "错误：未知的同步方向：$direction" >&2
    usage
    ;;
esac

echo ""
echo "✓ 同步完成！"
echo ""
