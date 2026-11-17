#!/usr/bin/env bash
# cli-butler function-view categorizer (v0.1.1): bucket a CLI by purpose, not
# by channel. Rules are ordered — first hit wins; gpg-agent must NOT land in
# AI (no bare "agent" keyword). Called once per row by list.sh --by-function.

# category|extended-regex, matched case-insensitively against "<name> <desc>"
FUNC_RULES='
AI / Agent 工具|claude|codex|kimi|opencode|cursor|gemini|copilot|ollama|llama|llm|aichat|aider|cline|openai|anthropic|deepseek|gpt|mcp|hermes|wigolo|mcporter|zread|uipro
移动开发|adb|fastboot|apktool|jadx|gradle|sdkmanager|avd|android|etc1tool|hprof|mke2fs|make_f2fs|emulator|flutter|dart|fvm
容器 / 基础设施|docker|kubernetes|kubectl|helm|terraform|orbstack|compose|colima|lima|qemu
版本控制|git|gh|glab|lazygit|svn|mercurial|gws
库依赖|^lib|library|libraries|bindings|codec|decoder|runtime library
Web / 网络|caddy|nginx|cloudflared|aria2|curl|wget|http|dns|ssh|proxy|tunnel|webget|openssl|certbot|network|server
多媒体|ffmpeg|ffprobe|lame|leptonica|imagemagick|magick|video|audio|image|jpeg|png|gif|vpx|av1|dav1d|opus|vorbis|media|font
语言运行时|node|npm|npx|bun|deno|typescript|tsc|yarn|pnpm|python|pip|conda|jupyter|uv|cargo|rust|golang|java|jdk|dotnet|ruby|perl|php|zig|llvm|gcc|clang|swift|compiler
'

categorize() { # <row-category> <name> <desc> -> sets global FUNC_CAT
  local rowcat="$1" nm="$2" ds="$3" label pat s
  [ "$rowcat" = "system" ] && { FUNC_CAT="系统自带（SIP）"; return 0; }
  s="$nm $ds"
  FUNC_CAT=""
  while IFS='|' read -r label pat; do
    [ -n "$pat" ] || continue
    if [ -n "${s//[[:space:]]/}" ] && printf '%s\n' "$s" | grep -qEi -- "$pat"; then
      FUNC_CAT="$label"; return 0
    fi
  done <<EOF
$FUNC_RULES
EOF
  # shellcheck disable=SC2034  # consumed by caller (list.sh function view)
  FUNC_CAT="其他独立工具"
}
