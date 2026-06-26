#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
HOOKS_DEST="$WORKSPACE/hooks"

success() { echo "✅ $*"; echo ""; }
warn()    { echo "⚠️  $*"; echo ""; }
fail()    { echo "❌ $*"; exit 1; }
header()  { echo ""; echo "**$***"; echo ""; }

echo "> 🗂️  **agent-changelog**"
echo "> _workspace version control — setup_"

# ─── Prerequisites ────────────────────────────────────────────────────
header "Prerequisites"

command -v git &>/dev/null || fail "git not found — install it first"
success "git $(git --version | awk '{print $3}')"

command -v jq &>/dev/null || fail "jq not found — install it first"
success "jq $(jq --version)"

[ -d "$WORKSPACE" ] || fail "Workspace not found: $WORKSPACE"
success "workspace \`$WORKSPACE\`"

if command -v openclaw &>/dev/null; then
  success "openclaw $(openclaw --version 2>/dev/null | head -1 | awk '{print $3}')"
else
  warn "openclaw CLI not found — you'll need to enable hooks manually"
fi

# ─── Install hooks ────────────────────────────────────────────────────
header "🪝 Installing hooks"

mkdir -p "$HOOKS_DEST"

HOOKS=("agent-changelog-capture" "agent-changelog-commit")
for hook in "${HOOKS[@]}"; do
  src="$SCRIPT_DIR/hooks/$hook"
  dest="$HOOKS_DEST/$hook"

  if [ ! -d "$src" ]; then
    warn "Hook source not found: \`$src\`"
    continue
  fi

  if [ -L "$dest" ]; then
    rm "$dest"
  elif [ -d "$dest" ]; then
    rm -rf "$dest"
  fi

  cp -r "$src" "$dest"
  success "Installed \`$hook\`"
done

# ─── Enable hooks via config ──────────────────────────────────────────
header "⚡ Activating hooks"

OPENCLAW_CFG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"

if [ -f "$OPENCLAW_CFG" ] && command -v jq &>/dev/null; then
  TMP=$(mktemp)
  jq '
    .hooks.internal.enabled = true |
    .hooks.internal.entries["agent-changelog-capture"].enabled = true |
    .hooks.internal.entries["agent-changelog-commit"].enabled = true
  ' "$OPENCLAW_CFG" > "$TMP" && mv "$TMP" "$OPENCLAW_CFG"
  success "Hooks enabled in config"
else
  warn "Could not update hook config — enable manually after restarting:"
  for hook in "${HOOKS[@]}"; do
    echo "  - \`openclaw hooks enable $hook\`"
  done
fi

# ─── Register cron ────────────────────────────────────────────────────
header "⏱️  Registering cron"

if command -v openclaw &>/dev/null; then
  CRON_NAME="agent-changelog-commit"
  CRON_CMD="bash $SCRIPT_DIR/scripts/commit.sh"
  if openclaw cron list --json 2>/dev/null | jq -e --arg name "$CRON_NAME" '.jobs[] | select(.name == $name)' >/dev/null 2>&1; then
    success "Cron \`$CRON_NAME\` already registered"
  elif openclaw cron add \
    --name "$CRON_NAME" \
    --cron "*/10 * * * *" \
    --message "$CRON_CMD" \
    --session isolated \
    --no-deliver >/dev/null 2>&1; then
    success "Registered \`$CRON_NAME\` _(every 10 min)_"
  else
    warn "Cron registration failed — check with: \`openclaw cron list\`"
  fi
else
  warn "Register cron manually after gateway starts:"
  echo "  \`openclaw cron add --name agent-changelog-commit --cron '*/10 * * * *' --message 'bash $SCRIPT_DIR/scripts/commit.sh' --session isolated --no-deliver\`"
fi

# ─── Initialize git repo ──────────────────────────────────────────────
header "📦 Git repository"

if [ -d "$WORKSPACE/.git" ]; then
  COMMIT_COUNT=$(cd "$WORKSPACE" && git rev-list --count HEAD 2>/dev/null || echo "0")
  success "Already initialized _($COMMIT_COUNT commits)_"
else
  (cd "$WORKSPACE" && git init -b main) >/dev/null 2>&1
  success "Initialized git repository"
fi

if [ ! -f "$WORKSPACE/.gitignore" ]; then
  cat > "$WORKSPACE/.gitignore" << 'GITIGNORE'
# secrets
.env
.env.*
*.env
.envrc
**/credentials/
**/secrets/
**/.credentials
**/.secrets
**/api_key*
**/apikey*
**/*_key.txt
**/*_key.json
**/*_token*
**/*_secret*
**/auth_token*
**/access_token*
**/refresh_token*
*.pem
*.key
*.p12
*.pfx
id_rsa
id_ed25519
*.ppk
client_secret*.json
service_account*.json
*-credentials.json
.aws/
.azure/
.gcloud/
gcloud*.json
aws_credentials

# runtime
*.log
*.tmp
*.temp
*.swp
*.swo
*~
*.jsonl
.version-context
state/
state.json
memory/
.DS_Store
Thumbs.db
desktop.ini

# openclaw internal
.openclaw/

# build
node_modules/
__pycache__/
*.pyc
.cache/
dist/
build/
*.egg-info/

# generated
bin/
GITIGNORE
  success "Created \`.gitignore\`"
else
  warn ".gitignore already exists and was left untouched. Review it before pushing to a remote to make sure secrets are excluded."
fi

# ─── Seed workspace config ────────────────────────────────────────────
header "🔧 Workspace config"

WORKSPACE_CFG="$WORKSPACE/.agent-changelog.json"
if [ ! -f "$WORKSPACE_CFG" ]; then
  cat > "$WORKSPACE_CFG" << 'EOF'
{
  "tracked": [
    "."
  ]
}
EOF
  success "Created \`.agent-changelog.json\`"
else
  success "\`.agent-changelog.json\` already exists — leaving as-is"
fi

# ─── First snapshot ───────────────────────────────────────────────────
header "📸 First snapshot"

cd "$WORKSPACE"
while IFS= read -r f; do
  git add "$f" 2>/dev/null || true
done < <(jq -r '.tracked[]?' "$WORKSPACE/.agent-changelog.json" 2>/dev/null)

if ! git diff --cached --quiet 2>/dev/null; then
  git commit -m "Initial snapshot — agent versioning setup" >/dev/null 2>&1
  HASH=$(git rev-parse --short HEAD)
  success "Snapshot \`$HASH\` created"
else
  echo "_No new files to commit_"
fi

# ─── Done ─────────────────────────────────────────────────────────────
echo ""
echo "🎉 **Setup complete!**"
