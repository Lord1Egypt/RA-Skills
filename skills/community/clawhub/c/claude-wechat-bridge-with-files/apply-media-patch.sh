#!/usr/bin/env bash
# Patch claude-wechat-channel's monitor.js to download attached media
# (image / file / voice / video) and inject local file paths into the
# inbound text as [图片: ...] / [文件: ...] / [语音文件: ...] / [视频: ...] markers.
#
# Idempotent. Re-run any time after `npx claude-wechat-channel` re-installs
# the package (which can happen if npm cache is cleared).

set -euo pipefail

PATCH_SRC="$HOME/.claude/skills/claude-wechat-bridge/patched-monitor.js"

if [[ ! -f "$PATCH_SRC" ]]; then
  echo "patched-monitor.js not found at $PATCH_SRC" >&2
  exit 1
fi

# Find all cached installs of claude-wechat-channel under ~/.npm/_npx/
# (use plain loop instead of mapfile for macOS bash 3.2 compatibility)
TARGETS=()
while IFS= read -r line; do
  TARGETS+=("$line")
done < <(find "$HOME/.npm/_npx" -type f -path "*/claude-wechat-channel/dist/monitor.js" 2>/dev/null)

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  echo "no claude-wechat-channel install found under ~/.npm/_npx/" >&2
  echo "run \`npx claude-wechat-channel\` once first so npm fetches it" >&2
  exit 1
fi

for target in "${TARGETS[@]}"; do
  # Skip backups
  case "$target" in *.orig) continue ;; esac

  # Backup the pristine original once
  if [[ ! -f "${target}.orig" ]]; then
    cp "$target" "${target}.orig"
  fi

  # Check if already patched (look for our marker string)
  if grep -q "media patch active" "$target" 2>/dev/null; then
    echo "already patched: $target"
    continue
  fi

  cp "$PATCH_SRC" "$target"
  echo "patched: $target"
done

echo "done. restart the bridge for the patch to take effect."
