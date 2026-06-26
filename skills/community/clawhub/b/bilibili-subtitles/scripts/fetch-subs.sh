#!/usr/bin/env bash
# 用法: ./fetch-subs.sh <B站视频URL> [可选: cookies.txt路径]
set -euo pipefail
URL="${1:?用法: $0 <bilibili-url> [cookies.txt]}"
COOKIES="${2:-}"

if ! command -v yt-dlp &>/dev/null; then
  echo "请先安装: brew install yt-dlp" >&2
  exit 1
fi

ARGS=(--write-subs --write-auto-subs --skip-download)
ARGS+=(--sub-langs "zh-Hans,zh-CN,zh,zh-Hant,en")
ARGS+=(-o "bilibili_%(id)s.%(ext)s")

if [[ -n "$COOKIES" ]]; then
  ARGS+=(--cookies "$COOKIES")
else
  # 若本机已登录 B 站，可取消下面两行注释，改用浏览器 Cookie
  # ARGS+=(--cookies-from-browser chrome)
  :
fi

yt-dlp "${ARGS[@]}" "$URL"
