#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required=(
  "$ROOT/SKILL.md"
  "$ROOT/references/endpoints.md"
  "$ROOT/references/usage-playbooks.md"
  "$ROOT/references/troubleshooting.md"
  "$ROOT/assets/example-prompts.md"
  "$ROOT/scripts/smoke.sh"
  "$ROOT/scripts/cw.sh"
  "$ROOT/scripts/install_cw_wrappers.sh"
  "$ROOT/scripts/room_client.py"
  "$ROOT/scripts/room_monitor.py"
  "$ROOT/scripts/room_bridge.py"
  "$ROOT/scripts/room_worker.py"
  "$ROOT/.clawhubignore"
)

for f in "${required[@]}"; do
  [[ -f "$f" ]] || { echo "MISSING: $f"; exit 1; }
done

grep -q '^name: "Clanker'"'"'s World"$' "$ROOT/SKILL.md" || {
  echo "SKILL name mismatch (must be Clanker's World)"; exit 1;
}

grep -q '`cw`' "$ROOT/SKILL.md" || {
  echo "SKILL missing canonical cw interface docs"; exit 1;
}

grep -qi 'authorized agent identities' "$ROOT/SKILL.md" || {
  echo "SKILL missing wall auth contract"; exit 1;
}

grep -qi 'anti-spam' "$ROOT/references/usage-playbooks.md" || {
  echo "usage-playbooks missing anti-spam section"; exit 1;
}

grep -qi 'https://clankers.world' "$ROOT/SKILL.md" || {
  echo "SKILL missing production host note"; exit 1;
}

grep -q '^state.json$' "$ROOT/.clawhubignore" || {
  echo ".clawhubignore missing state.json exclusion"; exit 1;
}

grep -q '^agents/$' "$ROOT/.clawhubignore" || {
  echo ".clawhubignore missing agents/ exclusion"; exit 1;
}

grep -q '^\.cw/$' "$ROOT/.clawhubignore" || {
  echo ".clawhubignore missing .cw/ exclusion"; exit 1;
}

echo "smoke: PASS"
