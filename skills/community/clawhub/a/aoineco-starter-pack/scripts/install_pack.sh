#!/usr/bin/env bash
set -euo pipefail

# aoineco-starter-pack: install a curated bundle of @edmonddantesj skills via ClawHub CLI.
# Requirements: clawhub CLI installed + logged in (`clawhub login`).

MODE="${1:-core}"  # core|full|minimal

core=(
  aoi-openclaw-security-toolkit-core
  aoi-prompt-injection-sentinel
  aoi-sandbox-shield-lite
  aoi-cron-ops-lite
  token-guard
)

minimal=(
  aoi-openclaw-security-toolkit-core
  aoi-cron-ops-lite
)

full=(
  aoi-openclaw-security-toolkit-core
  aoi-prompt-injection-sentinel
  aoi-sandbox-shield-lite
  aoi-cron-ops-lite
  token-guard
  publish-guard
  aoi-triple-memory-lite
  aoi-council
  aoi-hackathon-scout-lite
  aoi-squad-orchestrator-lite
  aoineco-squad-dispatch
  aoineco-ledger
  aoi-demo-clip-maker
)

case "$MODE" in
  minimal) skills=("${minimal[@]}") ;;
  core)    skills=("${core[@]}") ;;
  full)    skills=("${full[@]}") ;;
  *)
    echo "Usage: $0 [minimal|core|full]" >&2
    exit 2
    ;;
esac

echo "Installing pack mode=$MODE" >&2
for s in "${skills[@]}"; do
  echo "- clawhub install $s" >&2
  clawhub install "$s" --no-input
done

echo "Done. Installed $((${#skills[@]})) skills." >&2
