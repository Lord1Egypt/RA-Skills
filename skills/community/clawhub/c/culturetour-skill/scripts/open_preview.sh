#!/usr/bin/env bash
# 在本机用默认浏览器（macOS 下 HLS 优先 Safari）打开预览 URL，便于本地观看。
# 用法: bash scripts/open_preview.sh "<video_url>" [HLS|MP4]
set -euo pipefail
URL="${1:-}"
TYPE="${2:-}"
if [[ -z "$URL" ]]; then
  echo "用法: $0 <video_url> [HLS|MP4]" >&2
  exit 1
fi
if [[ -z "$TYPE" ]]; then
  if [[ "$URL" == *"/hls/"* ]] || [[ "$URL" == *.m3u8 ]]; then
    TYPE=HLS
  else
    TYPE=MP4
  fi
fi

case "$(uname -s)" in
  Darwin)
    if [[ "$TYPE" == "HLS" ]]; then
      if open -a Safari "$URL" 2>/dev/null; then :; else open "$URL"; fi
    else
      open "$URL"
    fi
    ;;
  Linux)
    xdg-open "$URL" 2>/dev/null || sensible-browser "$URL" 2>/dev/null || echo "请手动在浏览器打开: $URL" >&2
    ;;
  MINGW*|CYGWIN*|MSYS*)
    cmd //c start "" "$URL"
    ;;
  *)
    open "$URL" 2>/dev/null || xdg-open "$URL" 2>/dev/null || echo "请手动在浏览器打开: $URL" >&2
    ;;
esac
