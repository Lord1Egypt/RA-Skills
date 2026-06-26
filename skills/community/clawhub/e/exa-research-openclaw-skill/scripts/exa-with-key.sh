#!/usr/bin/env bash
set -euo pipefail

EXA_BIN="${EXA_BIN:-exa}"
EXA_API_KEY_FILE="${EXA_API_KEY_FILE:-$HOME/.openclaw/credentials/exa/api-key.txt}"

if [[ "$EXA_BIN" != */* ]]; then
  if ! EXA_BIN="$(command -v "$EXA_BIN" 2>/dev/null)"; then
    echo "Missing Exa binary on PATH: ${EXA_BIN:-exa}" >&2
    echo "Install Exa from the upstream project or set EXA_BIN to its full path." >&2
    exit 1
  fi
fi

if [[ ! -x "$EXA_BIN" ]]; then
  echo "Missing or non-executable Exa binary: $EXA_BIN" >&2
  exit 1
fi

# Preferred auth source order:
# 1. Existing EXA_API_KEY in the environment
# 2. EXA_API_KEY_FILE override
# 3. Default local credential file path
if [[ -z "${EXA_API_KEY:-}" ]]; then
  if [[ ! -f "$EXA_API_KEY_FILE" ]]; then
    cat >&2 <<EOF
Missing Exa credentials.

Provide one of:
- skills.entries.exa-research.apiKey (OpenClaw config)
- skills.entries.exa-research.env.EXA_API_KEY (OpenClaw config)
- EXA_API_KEY in the environment
- EXA_API_KEY_FILE pointing at a readable file
- the default file at: $EXA_API_KEY_FILE

Recommended file setup:
  mkdir -p "$(dirname "$EXA_API_KEY_FILE")"
  printf '%s\n' '<your-exa-api-key>' > "$EXA_API_KEY_FILE"
  chmod 600 "$EXA_API_KEY_FILE"
EOF
    exit 1
  fi

  if [[ ! -r "$EXA_API_KEY_FILE" ]]; then
    echo "Unreadable Exa API key file: $EXA_API_KEY_FILE" >&2
    exit 1
  fi

  EXA_API_KEY="$(head -n 1 "$EXA_API_KEY_FILE" | tr -d '\r\n')"
fi

if [[ -z "$EXA_API_KEY" ]]; then
  echo "Exa API key is empty. Set EXA_API_KEY, provide a non-empty key file, or configure skills.entries.exa-research.apiKey." >&2
  exit 1
fi

export EXA_API_KEY
exec "$EXA_BIN" "$@"
