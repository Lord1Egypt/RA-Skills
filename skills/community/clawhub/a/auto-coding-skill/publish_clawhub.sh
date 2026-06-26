#!/usr/bin/env bash
# ClawHub publish script for auto-coding-v3
# Backup → modify for compliance → publish → restore
set -euo pipefail
cd "$(dirname "$0")"

echo "📦 Auto-Coding ClawHub Publish"
echo "=============================="

# --- Backup ---
echo "1️⃣ Backing up local files..."
cp SKILL.md SKILL.md.bak
cp README.md README.md.bak
cp clawhub.json clawhub.json.bak

# Trap: restore on failure
cleanup() {
  echo "⚠️ Restoring local files due to error..."
  [ -f SKILL.md.bak ] && mv SKILL.md.bak SKILL.md
  [ -f README.md.bak ] && mv README.md.bak README.md
  [ -f clawhub.json.bak ] && mv clawhub.json.bak clawhub.json
}
trap cleanup EXIT

# --- Modify for ClawHub compliance ---
echo "2️⃣ Applying ClawHub compliance modifications..."

# Genericize model names (avoid appearing to recommend specific models)
sed -i '' 's/`deepseek-v4-pro`/`your-primary-model`/g' SKILL.md
sed -i '' 's/`MiMo v2.5 Pro`/`your-review-model`/g' SKILL.md

# Verify no PII remains
if grep -q 'krislu\|虾软\|虾总\|ou_71\|ou_72\|foxmail\|krislu666' SKILL.md README.md; then
  echo "❌ PII detected! Aborting."
  exit 1
fi

# --- Publish ---
echo "3️⃣ Publishing to ClawHub..."
clawhub publish . --version "$(python3 -c "import json; print(json.load(open('clawhub.json'))['version'])")"

# --- Restore (disable trap since we succeeded) ---
trap - EXIT
echo "4️⃣ Restoring local files..."
mv SKILL.md.bak SKILL.md
mv README.md.bak README.md
mv clawhub.json.bak clawhub.json

echo "✅ Done! Local files restored."
