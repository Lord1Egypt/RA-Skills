#!/usr/bin/env bash
# SimpleViking Read - 读取内容（支持分层）
# 用法: sv_read <viking_uri> [--layer l0|l1|l2]

source "$(dirname "$0")/lib.sh"

uri=""
layer="l2"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --layer)
      layer="$2"
      shift 2
      ;;
    *)
      uri="$1"
      shift
      ;;
  esac
done

if [[ -z "$uri" ]]; then
  echo "用法: sv_read <viking_uri> [--layer l0|l1|l2]"
  echo "示例: sv_read viking://resources/project/README.md"
  echo "示例: sv_read viking://resources/project/docs --layer l1"
  exit 1
fi

target_path=$(sv_resolve_path "$uri")
parent_dir=$(dirname "$target_path")

if [[ ! -e "$target_path" ]]; then
  echo "错误: 文件或目录不存在: $uri"
  exit 1
fi

# 如果是目录，返回 L0/L1 摘要
if [[ -d "$target_path" ]]; then
  case "$layer" in
    l0|abstract)
      if [[ -f "$target_path/.abstract" ]]; then
        cat "$target_path/.abstract"
      else
        sv_log WARN "目录缺少 .abstract 文件"
        echo ""
      fi
      ;;
    l1|overview)
      if [[ -f "$target_path/.overview" ]]; then
        cat "$target_path/.overview"
      else
        sv_log WARN "目录缺少 .overview 文件"
        echo ""
      fi
      ;;
    l2|*)
      # 列出目录下的文件
      echo "目录: $uri"
      find "$target_path" -type f ! -name '.abstract' ! -name '.overview' | sort | while read -r f; do
        rel="${f#$target_path/}"
        echo "  - $rel"
      done
      ;;
  esac
else
  # 文件：根据层级返回摘要或全文
  case "$layer" in
    l0|abstract)
      sv_generate_l0 "$target_path"
      ;;
    l1|overview)
      sv_generate_l1 "$target_path"
      ;;
    l2|*)
      cat "$target_path"
      ;;
  esac
fi