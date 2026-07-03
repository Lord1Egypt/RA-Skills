#!/bin/bash
# Bambu 打印机 FTPS 操作封装
# 用法: ftp.sh <command> [args]
# 命令: list [path], upload <local_file> [remote_path], download <remote_path> [local_path], delete <remote_path]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$SCRIPT_DIR/../config.json"

# 读取配置（兼容无 python 的情况）
read_config() {
  local key="$1"
  if command -v python3 &>/dev/null; then
    python3 -c "import json,sys; c=json.load(open('$CONFIG')); print(c$key)" 2>/dev/null || echo ""
  else
    # 简单 grep fallback
    grep -o "\"${key##*.}\": *\"[^\"]*\"" "$CONFIG" | head -1 | sed 's/.*: *"\(.*\)"/\1/'
  fi
}

IP=$(read_config "['printer']['ip']")       || IP="192.168.1.68"
AC=$(read_config "['printer']['access_code']") || AC="31713703"
USER=$(read_config "['printer']['username']")  || USER="bblp"

CURL="/usr/bin/curl"
BASE_URL="ftps://${IP}:990"
AUTH="${USER}:${AC}"

cmd="${1:-help}"
shift || true

case "$cmd" in
  list|ls)
    path="${1:-/}"
    [[ "$path" != /* ]] && path="/$path"
    exec $CURL -s --insecure --connect-timeout 10 -u "$AUTH" "${BASE_URL}${path}" 2>&1
    ;;

  upload|put)
    local_file="${1:?需要指定本地文件路径}"
    remote_dir="${2:-/cache/}"
    [[ "$remote_dir" != /* ]] && remote_dir="/$remote_dir"
    if [ ! -f "$local_file" ]; then
      echo "❌ 文件不存在: $local_file" >&2
      exit 1
    fi
    filename=$(basename "$local_file")
    echo "⬆️ 上传 $filename 到 ${remote_dir}..."
    exec $CURL -T "$local_file" --insecure --connect-timeout 10 -u "$AUTH" "${BASE_URL}${remote_dir}${filename}" 2>&1
    ;;

  download|get)
    remote_path="${1:?需要指定远程文件路径}"
    [[ "$remote_path" != /* ]] && remote_path="/$remote_path"
    local_path="${2:-.}"
    filename=$(basename "$remote_path")
    if [ -d "$local_path" ]; then
      local_path="$local_path/$filename"
    fi
    echo "⬇️ 下载 $remote_path 到 $local_path..."
    exec $CURL -s --insecure --connect-timeout 10 -u "$AUTH" -o "$local_path" "${BASE_URL}${remote_path}" 2>&1
    echo "✅ 下载完成: $local_path"
    ;;

  delete|rm|del)
    remote_path="${1:?需要指定远程文件路径}"
    [[ "$remote_path" != /* ]] && remote_path="/$remote_path"
    echo "🗑️ 删除 $remote_path"
    exec $CURL -s --insecure --connect-timeout 10 -u "$AUTH" -Q "DELE $remote_path" "${BASE_URL}/" 2>&1
    ;;

  size|info)
    path="${1:-/}"
    [[ "$path" != /* ]] && path="/$path"
    $CURL -s --insecure --connect-timeout 10 -u "$AUTH" "${BASE_URL}${path}" 2>&1 | \
      awk '/^-/{total += $5; count++} END {printf "文件数: %d, 总大小: %.1f MB\n", count, total/1024/1024}'
    ;;

  help|--help|-h)
    echo "Bambu 打印机 FTPS 工具"
    echo ""
    echo "用法: $0 <command> [args]"
    echo ""
    echo "命令:"
    echo "  list [path]              列出文件 (默认根目录)"
    echo "  upload <file> [remotedir] 上传文件 (默认 /cache/)"
    echo "  download <remote> [local] 下载文件 (默认当前目录)"
    echo "  delete <remote>          删除远程文件"
    echo "  size [path]              统计文件数和总大小"
    ;;

  *)
    echo "❌ 未知命令: $cmd" >&2
    echo "运行 '$0 help' 查看帮助" >&2
    exit 1
    ;;
esac
