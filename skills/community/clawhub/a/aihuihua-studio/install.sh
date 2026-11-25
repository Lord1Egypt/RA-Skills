#!/usr/bin/env bash
# 把这个技能装到本机的技能目录里。
#   ./install.sh          装到 ~/.claude/skills（所有项目都能用）
#   ./install.sh --here   装到当前项目的 .claude/skills
# 用的是别的 AI 工具？把这个目录拷到它的技能目录下即可，内容完全一样。
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="$(basename "$SRC")"
if [ "${1:-}" = "--here" ]; then DEST_ROOT="$(pwd)/.claude/skills"; else DEST_ROOT="$HOME/.claude/skills"; fi
DEST="$DEST_ROOT/$NAME"
command -v node >/dev/null 2>&1 || { echo "✗ 没找到 node，这个技能要 Node 20 以上" >&2; exit 1; }
[ "$(node -p 'process.versions.node.split(".")[0]')" -ge 20 ] || { echo "✗ Node 版本太低（$(node -v)），需要 20 以上" >&2; exit 1; }
mkdir -p "$DEST_ROOT"
if [ "$SRC" != "$DEST" ]; then rm -rf "$DEST"; cp -R "$SRC" "$DEST"; fi
chmod +x "$DEST/scripts/studio.mjs" "$DEST/install.sh"
echo "✓ 已安装到 $DEST"
echo "在 AI 工具里说「用 鼓鼓AI 画一张……」即可；也可以自己跑：node $DEST/scripts/studio.mjs login"
