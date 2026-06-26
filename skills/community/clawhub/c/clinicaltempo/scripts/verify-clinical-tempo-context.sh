#!/usr/bin/env bash
# Quick checks from repo root: public/llm-full.txt exists; remind API smoke.
set -euo pipefail
# Script: .cursor/skills/clawhub/scripts/ — repo root is four levels up (scripts→clawhub→skills→.cursor→repo)
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
LLM="$ROOT/public/llm-full.txt"
echo "Clinical Tempo context check (repo: $ROOT)"
if [[ ! -f "$LLM" ]]; then
  echo "MISSING: $LLM — run: npm run build:llm"
  exit 1
fi
BYTES=$(wc -c < "$LLM" | tr -d ' ')
echo "OK: llm-full.txt exists ($BYTES bytes)"
echo "Tip: with server on 8787, run: curl -sS http://127.0.0.1:8787/api/dance-extras/live | head"
exit 0
