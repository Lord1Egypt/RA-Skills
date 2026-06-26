#!/usr/bin/env bash
set -euo pipefail

ROC_CONFIG="${HOME}/.openclaw/workspace/skills/ranking-of-claws/config.json"

if [ -f "$ROC_CONFIG" ]; then
  echo "clawsgames: found ranking-of-claws config."
  exit 0
fi

echo "clawsgames: ranking-of-claws not found, installing implicitly..."
if command -v clawhub >/dev/null 2>&1; then
  clawhub install ranking-of-claws
else
  echo "clawsgames: 'clawhub' CLI not found."
  echo "Install ranking-of-claws manually first:"
  echo "  clawhub install ranking-of-claws"
  exit 1
fi

if [ ! -f "$ROC_CONFIG" ]; then
  echo "clawsgames: ranking-of-claws install did not create config:"
  echo "  $ROC_CONFIG"
  exit 1
fi

echo "clawsgames: dependency ready."
