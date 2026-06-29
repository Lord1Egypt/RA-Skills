#!/usr/bin/env bash
# book-report 主入口
# 用法：
#   ./agent.sh book <书名> [--author "作者"] [--lang zh|en] [--pdf <path>] [--html-only|--chat-only]
#   ./agent.sh help
set -euo pipefail

AGENT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$AGENT_DIR"

cmd="${1:-help}"
shift || true

case "$cmd" in
  book|html|chat)
    if [[ $# -lt 1 ]]; then
      echo "用法: $0 $cmd <书名> [--author '作者'] [--lang zh|en] [--pdf <path>]" >&2
      exit 1
    fi
    title="$1"
    shift || true

    author=""
    lang="zh"
    pdf_path=""
    mode="both"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --author) author="${2:-}"; shift 2 ;;
        --lang)   lang="${2:-zh}"; shift 2 ;;
        --pdf)    pdf_path="${2:-}"; shift 2 ;;
        --html-only) mode="html"; shift ;;
        --chat-only) mode="chat"; shift ;;
        *) echo "未知参数: $1" >&2; exit 1 ;;
      esac
    done

    if [[ "$cmd" == "html" ]]; then mode="html"; fi
    if [[ "$cmd" == "chat" ]]; then mode="chat"; fi

    cmd_args=("--title" "$title" "--mode" "$mode" "--lang" "$lang")
    [[ -n "$author" ]]   && cmd_args+=("--author" "$author")
    [[ -n "$pdf_path" ]] && cmd_args+=("--pdf" "$pdf_path")

    exec python3 lib/render.py "${cmd_args[@]}"
    ;;

  pdf)
    # 单独测 PDF 抽取能力（不渲染）
    if [[ $# -lt 1 ]]; then
      echo "用法: $0 pdf <pdf_path>" >&2
      exit 1
    fi
    exec python3 lib/pdf_extract.py "$1"
    ;;

  help|--help|-h|"")
    cat <<EOF
book-report — 书籍研究工具

用法:
  $0 book <书名> [--author '作者'] [--lang zh|en] [--pdf <path>] [--html-only|--chat-only]
  $0 html <书名> [选项]                     只生成 HTML 报告
  $0 chat <书名> [选项]                     只生成弹药库
  $0 pdf <pdf_path>                         单独测 PDF 抽取
  $0 help                                   显示本帮助

选项:
  --author '作者'         书的作者（可选）
  --lang zh|en            语言（默认 zh=中文经典, en=英文经典）
  --pdf <path>            提供 PDF 文件，4 字段从 PDF 抽，其余 5 字段从 web 抓
  --html-only             只出 HTML 报告
  --chat-only             只出弹药库

示例:
  $0 book 平凡的世界
  $0 book 活着 --author 余华
  $0 book 红楼梦 --author 曹雪芹 --html-only
  $0 book "The Old Man and the Sea" --author "Hemingway" --lang en
  $0 book 三体 --pdf /path/to/三体.pdf

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
