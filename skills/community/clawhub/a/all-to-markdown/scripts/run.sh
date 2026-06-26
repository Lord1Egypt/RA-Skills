#!/usr/bin/env bash
# all-to-markdown skill — convert any file or URL to Markdown via markitdown

set -euo pipefail

INPUT="${1:-}"

show_help() {
  cat <<'EOF'
all-to-markdown v0.1.0 — 将任意文件或 URL 转换为 Markdown

用法:
  scripts/run.sh <file-or-url> [选项]

支持格式:
  文档:   PDF, DOCX, PPTX, XLSX, XLS, EPUB, MSG
  数据:   CSV, JSON, XML
  媒体:   图片（含 EXIF/OCR）、音频（含语音转录）
  网页:   HTML、YouTube URL
  压缩:   ZIP（逐文件转换）

选项:
  -o <file>         输出到文件（默认输出到 stdout）
  --use-plugins     启用已安装的第三方插件
  --llm-model <m>   用于图片描述的 LLM 模型（需配合 LLM 客户端）
  -h, --help        显示此帮助

示例:
  scripts/run.sh report.pdf
  scripts/run.sh slide.pptx -o slide.md
  scripts/run.sh https://www.youtube.com/watch?v=xxx
  scripts/run.sh https://example.com/article.html
  scripts/run.sh data.xlsx

环境变量（可选，用于 AI 增强功能）:
  OPENAI_API_KEY    启用图片 AI 描述 / OCR 功能
EOF
}

if [[ -z "$INPUT" || "$INPUT" == "-h" || "$INPUT" == "--help" ]]; then
  show_help
  exit 0
fi

# Check if markitdown is installed
if ! command -v markitdown &>/dev/null; then
  echo >&2 "错误: markitdown 未安装。请运行: pip install 'markitdown[all]'"
  exit 1
fi

# Pass all remaining args through to markitdown
shift
exec markitdown "$INPUT" "$@"
