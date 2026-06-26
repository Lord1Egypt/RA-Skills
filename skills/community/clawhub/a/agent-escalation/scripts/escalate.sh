#!/usr/bin/env bash
set -euo pipefail

# Escalation vers le superviseur via webhook gateway OpenClaw
# Usage: escalate.sh "<problème>" "<tentatives>" ["<résultat>"]

PROBLEM="${1:?Usage: escalate.sh '<problème>' '<tentatives>' ['<résultat>']}"
ATTEMPTS="${2:?Usage: escalate.sh '<problème>' '<tentatives>' ['<résultat>']}"
RESULT="${3:-Aucun résultat spécifique}"

# Configuration
GATEWAY_HOST="${GATEWAY_HOST:-127.0.0.1}"
GATEWAY_PORT="${GATEWAY_PORT:-18789}"
HOOKS_TOKEN="${HOOKS_TOKEN:?HOOKS_TOKEN non défini}"
SUPERVISOR_AGENT="${SUPERVISOR_AGENT:-david}"
DELIVER_CHANNEL="${DELIVER_CHANNEL:-telegram}"
DELIVER_TO="${DELIVER_TO:-8678077382}"

# Construire le message d'escalation
MESSAGE="🚨 **Escalation agent**

**Problème :** ${PROBLEM}

**Tentatives :** ${ATTEMPTS}

**Résultat :** ${RESULT}

Merci de traiter ou d'escalader à Erwan si nécessaire."

# Échapper le JSON
JSON_MESSAGE=$(printf '%s' "$MESSAGE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

# Appel webhook
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "http://${GATEWAY_HOST}:${GATEWAY_PORT}/hooks/agent" \
  -H "Authorization: Bearer ${HOOKS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"message\": ${JSON_MESSAGE},
    \"agentId\": \"${SUPERVISOR_AGENT}\",
    \"wakeMode\": \"now\",
    \"deliver\": true,
    \"channel\": \"${DELIVER_CHANNEL}\",
    \"to\": \"${DELIVER_TO}\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "✅ Escalation envoyée au superviseur (${SUPERVISOR_AGENT})"
  echo "HTTP ${HTTP_CODE}"
else
  echo "❌ Échec de l'escalation — HTTP ${HTTP_CODE}"
  echo "$BODY"
  exit 1
fi
