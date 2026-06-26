#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$HOME/.openclaw/workspace/scripts/security-prepublish-guard.sh"
cat > "$TARGET" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="${1:-}"
if [ -z "$SKILL_DIR" ]; then
  echo "Usage: security-prepublish-guard.sh <skill-dir>" >&2
  exit 2
fi
node "$HOME/.openclaw/workspace/skills/openclaw-security-guard/scripts/prepublish-guard.mjs" "$SKILL_DIR"
EOF
chmod +x "$TARGET"
echo "Installed: $TARGET"
