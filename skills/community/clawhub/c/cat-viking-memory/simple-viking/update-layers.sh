#!/usr/bin/env bash
# SimpleViking Update Layers - 更新目录的 L0/L1 元数据
# 用法: sv_update_layers [根路径]

source "$(dirname "$0")/lib.sh"

root_uri="${1:-viking://}"
root_path=$(sv_resolve_path "$root_uri")

if [[ ! -d "$root_path" ]]; then
  echo "错误: 路径不存在 $root_uri -> $root_path"
  exit 1
fi

sv_update_tree_layers "$root_path"