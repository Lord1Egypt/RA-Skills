#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ok() { echo "✅ $1"; }
warn() { echo "⚠️  $1"; }
fail() { echo "❌ $1"; exit 1; }

echo "== ClawSwap Skill Prepublish Checklist =="
echo "Root: $ROOT_DIR"

# 1) Required files
for f in SKILL.md skill.json runtime_client.py .env.example; do
  [[ -f "$ROOT_DIR/$f" ]] || fail "missing required file: $f"
done
ok "required files present"

# 2) SKILL.md frontmatter sanity
head -n 20 "$ROOT_DIR/SKILL.md" | grep -q "^name: clawswap$" || fail "SKILL.md frontmatter missing name: clawswap"
head -n 20 "$ROOT_DIR/SKILL.md" | grep -q "^description:" || fail "SKILL.md frontmatter missing description"
ok "SKILL.md frontmatter valid"

# 3) Secrets/local state must not be tracked
for f in .runtime_token .clawswap_api_key .env; do
  if git -C "$ROOT_DIR/.." ls-files --error-unmatch "clawswap/$f" >/dev/null 2>&1; then
    fail "sensitive/local file is tracked in git: clawswap/$f"
  fi
done
ok "sensitive/local files are not tracked"

# 4) No compiled cache in release source
if find "$ROOT_DIR" -type d -name '__pycache__' | grep -q .; then
  warn "__pycache__ directories found (packaging script will exclude)"
else
  ok "no __pycache__ directories"
fi

if find "$ROOT_DIR" -type f -name '*.pyc' | grep -q .; then
  warn "*.pyc files found (packaging script will exclude)"
else
  ok "no *.pyc files"
fi

# 5) Python unit tests
(
  cd "$ROOT_DIR"
  python3 tests/test_runtime_client.py >/tmp/clawswap_skill_test.log
)
ok "unit tests passed (tests/test_runtime_client.py)"

echo "== Checklist complete =="
