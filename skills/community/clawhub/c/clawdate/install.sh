#!/usr/bin/env bash
set -euo pipefail

SOURCE="${1:-}"
SKILL_ROOT="${SKILL_ROOT:-${OPENCLAW_WORKDIR:-$PWD}/skills/clawdate}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

install_file() {
  local relative_path="$1"
  local destination="$SKILL_ROOT/$relative_path"

  mkdir -p "$(dirname "$destination")"

  if [[ -n "$SOURCE" && "$SOURCE" =~ ^https?:// ]]; then
    curl -fsSL "${SOURCE%/}/$relative_path" -o "$destination"
  elif [[ -n "$SOURCE" ]]; then
    cp "${SOURCE%/}/$relative_path" "$destination"
  else
    cp "$SCRIPT_DIR/$relative_path" "$destination"
  fi
}

mkdir -p "$SKILL_ROOT/agents" "$SKILL_ROOT/assets"
mkdir -p "$SKILL_ROOT/scripts"

install_file "SKILL.md"
install_file "agents/openai.yaml"
install_file "assets/owner-profile.template.json"
install_file "assets/profile-sync.sh.template"
install_file "assets/cron.example.txt"
install_file "scripts/init_owner.sh"

rm -f "$SKILL_ROOT/scripts/cleanup_owner.sh"

chmod 0644 "$SKILL_ROOT/SKILL.md" \
  "$SKILL_ROOT/agents/openai.yaml" \
  "$SKILL_ROOT/assets/owner-profile.template.json" \
  "$SKILL_ROOT/assets/profile-sync.sh.template" \
  "$SKILL_ROOT/assets/cron.example.txt"
chmod 0755 "$SKILL_ROOT/scripts/init_owner.sh"

echo "Installed clawdate skill into $SKILL_ROOT"
echo "If the current lobster session does not see the skill yet, refresh or reopen the workspace."
