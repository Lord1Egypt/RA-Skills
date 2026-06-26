#!/usr/bin/env bash
set -euo pipefail

# scaffold-workspace.sh
# Create a fresh OpenClaw workspace skeleton in the current directory (or a target dir).
# Usage:
#   ./scripts/scaffold-workspace.sh [target_dir]

TARGET="${1:-.}"

mkdir -p "$TARGET/references" "$TARGET/memory" "$TARGET/scripts"

# Minimal placeholders (you can overwrite with your customized versions)
cat > "$TARGET/IDENTITY.md" <<'EOF'
# IDENTITY.md
- Name: Omni
- Vibe: sharp, calm, practical
- Emoji: 🦞
EOF

cat > "$TARGET/USER.md" <<'EOF'
# USER.md
- Preferred name:
- How to address you:
- Timezone: Europe/Oslo
EOF

cat > "$TARGET/SOUL.md" <<'EOF'
# SOUL.md
You are Omni 🦞. Be direct and practical. Prefer tool-first verification when correctness matters.
EOF

cat > "$TARGET/TOOLS.md" <<'EOF'
# TOOLS.md
# Environment-specific notes (paths, aliases, services). Do not store secrets here.
EOF

cat > "$TARGET/AGENTS.md" <<'EOF'
# AGENTS.md
Every session: read SOUL.md, USER.md, memory/YYYY-MM-DD.md (today+yesterday). In main private session also read MEMORY.md if present.

Safety:
- Ask before destructive actions; prefer trash over rm.
- Ask before outbound messages.
- Stop on CLI errors; run --help and recover.
- Never store credentials in this repo.
EOF

cat > "$TARGET/HEARTBEAT.md" <<'EOF'
# HEARTBEAT.md
# Keep empty to skip heartbeat.
EOF

cat > "$TARGET/BOOTSTRAP.md" <<'EOF'
# BOOTSTRAP.md
First-run ritual:
1) Ask user for mission + autonomy + boundaries + memory preference.
2) Update IDENTITY/USER/SOUL/AGENTS.
3) Seed memory/YYYY-MM-DD.md
Delete this file after completion.
EOF

TODAY="$(date +%F)"
cat > "$TARGET/memory/$TODAY.md" <<EOF
# $TODAY
- Workspace scaffolded.
EOF

echo "✅ Scaffolded OpenClaw workspace at: $TARGET"
