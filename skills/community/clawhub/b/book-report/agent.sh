#!/usr/bin/env bash
# allen-agent 主入口
# 用法：./agent.sh book <书名> [--author "作者名"]
#       ./agent.sh help
set -euo pipefail

AGENT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$AGENT_DIR"

cmd="${1:-help}"
shift || true

case "$cmd" in
  book)
    if [[ $# -lt 1 ]]; then
      echo "用法: $0 book <书名> [--author '作者名']" >&2
      exit 1
    fi
    title="$1"
    shift || true
    author=""
    if [[ "${1:-}" == "--author" ]]; then
      author="${2:-}"
      shift 2 || true
    fi
    exec python3 lib/render.py \
      --title "$title" \
      ${author:+--author "$author"} \
      --mode both
    ;;

  html)
    if [[ $# -lt 1 ]]; then
      echo "用法: $0 html <书名> [--author '作者名']" >&2
      exit 1
    fi
    title="$1"
    shift || true
    author=""
    if [[ "${1:-}" == "--author" ]]; then
      author="${2:-}"
      shift 2 || true
    fi
    exec python3 lib/render.py \
      --title "$title" \
      ${author:+--author "$author"} \
      --mode html
    ;;

  chat)
    if [[ $# -lt 1 ]]; then
      echo "用法: $0 chat <书名> [--author '作者名']" >&2
      exit 1
    fi
    title="$1"
    shift || true
    author=""
    if [[ "${1:-}" == "--author" ]]; then
      author="${2:-}"
      shift 2 || true
    fi
    exec python3 lib/render.py \
      --title "$title" \
      ${author:+--author "$author"} \
      --mode chat
    ;;

  help|--help|-h|"")
    cat <<EOF
allen-agent — 书籍研究工具

用法:
  $0 book <书名> [--author '作者名']    生成 HTML 报告 + 弹药库（默认）
  $0 html <书名> [--author '作者名']    只生成 HTML 报告
  $0 chat <书名> [--author '作者名']    只生成弹药库
  $0 help                              显示本帮助

示例:
  $0 book 平凡的世界
  $0 book 红楼梦 --author 曹雪芹
  $0 chat 活着

输出位置:
  reports/<书名>-<日期>.html          HTML 报告
  reports/chat-弹药库-<书名>-v1.md    弹药库
EOF
    ;;

  *)
    echo "未知命令: $cmd" >&2
    echo "运行 '$0 help' 查看用法" >&2
    exit 1
    ;;
esac
