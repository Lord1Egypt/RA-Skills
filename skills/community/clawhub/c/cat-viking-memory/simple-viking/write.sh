#!/usr/bin/env bash
# SimpleViking Write - 写入内容并自动更新层级
# 用法: sv_write <viking_uri> "内容"

source "$(dirname "$0")/lib.sh"

if [[ $# -lt 2 ]]; then
  echo "用法: sv_write <viking_uri> \"内容\""
  echo "示例: sv_write viking://resources/my_project/notes.md \"# 项目笔记\""
  exit 1
fi

uri="$1"
content="$2"

target_path=$(sv_resolve_path "$uri")

# 确保父目录存在
parent_dir=$(dirname "$target_path")
sv_ensure_dir "$parent_dir"

# 写入内容
echo -n "$content" > "$target_path"
sv_log INFO "已写入: $uri"

# 自动更新所在目录及祖先目录的 L0/L1
dir="$parent_dir"
while [[ "$dir" != "$SV_WORKSPACE" && "$dir" != "/" ]]; do
  sv_update_dir_layers "$dir"
  dir=$(dirname "$dir")
done

# 跳过自动向量生成（由 memory-pipeline 处理）
# sv_update_vector_index "$target_path" "$SV_WORKSPACE"