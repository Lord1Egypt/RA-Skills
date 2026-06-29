#!/usr/bin/env bash
# Usage: bash scripts/publish.sh
# 1. Update version in SKILL.md frontmatter
# 2. Commit + push to GitHub
# 3. Publish to ClawHub

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR"

# ── Read current version ──
CURRENT=$(grep '^version: ' SKILL.md | head -1 | sed 's/version: //')
echo "当前版本: $CURRENT"

# ── Compute next patch version ──
MAJOR=$(echo "$CURRENT" | cut -d. -f1)
MINOR=$(echo "$CURRENT" | cut -d. -f2)
PATCH=$(echo "$CURRENT" | cut -d. -f3)
NEXT_PATCH=$((PATCH + 1))
NEXT="${MAJOR}.${MINOR}.${NEXT_PATCH}"
echo "下一个版本: $NEXT"

# ── Prompt for version ──
read -r -p "版本号 [$NEXT]: " INPUT
VERSION="${INPUT:-$NEXT}"

# ── Update SKILL.md version ──
sed -i '' "s/^version: .*/version: $VERSION/" SKILL.md
echo "SKILL.md → version: $VERSION"

# ── Write CHANGELOG entry ──
DATE=$(date +%Y-%m-%d)
CHANGELOG_HEADER="## $VERSION ($DATE)"
if ! grep -q "^## $VERSION" CHANGELOG.md 2>/dev/null; then
  # Insert after first line
  sed -i '' "2s/^/$CHANGELOG_HEADER\n\n### Added\n\n- \n\n/" CHANGELOG.md 2>/dev/null || true
  echo "请在 CHANGELOG.md 中填写改动内容，然后按回车继续..."
  read -r
fi

# ── Confirm before pushing (irreversible: makes version public) ──
read -r -p "即将推送 v$VERSION 到 GitHub 并发布到 ClawHub,确认? [y/N]: " CONFIRM
case "$CONFIRM" in
  y|Y|yes|YES) echo "→ 继续发布" ;;
  *) echo "已取消,未推送/未发布"; exit 0 ;;
esac

# ── Commit ──
git add -A
git commit -m "chore: bump version to $VERSION"
git push origin main
echo "✅ GitHub 推送完成"

# ── Publish to ClawHub ──
# .claude-plugin（目录）会导致 clawhub 误判为 plugin，临时移开
# 用 -e 匹配目录和文件；用 trap 保证无论 publish 成败都恢复，避免目录被丢在 /tmp
CLAUDE_PLUGIN_BAK=""
restore_plugin() {
  if [ -n "$CLAUDE_PLUGIN_BAK" ]; then
    mv "$CLAUDE_PLUGIN_BAK" .claude-plugin
  fi
}
trap restore_plugin EXIT

if [ -e .claude-plugin ]; then
  CLAUDE_PLUGIN_BAK=$(mktemp -u /tmp/ai-capsule-claude-plugin.XXXXXX)
  mv .claude-plugin "$CLAUDE_PLUGIN_BAK"
fi

clawhub skill publish . --slug ai-capsule --version "$VERSION" --owner webpudge

trap - EXIT
restore_plugin

echo "✅ ClawHub 发布完成 → v$VERSION"