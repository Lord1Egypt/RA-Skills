#!/usr/bin/env bash
set -euo pipefail

INPUT="$(cat)"
TOOL_NAME="$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null || echo "")"
COMMAND="$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null || echo "")"
FILE_PATH="$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // ""' 2>/dev/null || echo "")"

DANGEROUS_REGEX='(rm -rf|git push --force|git reset --hard|drop database|truncate table|kubectl delete|terraform apply|terraform destroy|aws .*delete|gcloud .*delete|az .*delete|npm publish|pnpm publish|yarn publish|docker push|helm upgrade|helm delete)'
SECRET_REGEX='(private key|seed phrase|mnemonic|wallet key|api[_-]?key|secret|password|token|keystore|id_rsa|id_ed25519|\.pem|\.key)'
PROD_REGEX='(prod|production|mainnet|live funds|real funds|withdraw|transfer|deploy|release)'
ENV_FILE_REGEX='(^|/)\.env($|\.)|secrets?\.(json|yaml|yml|toml)$'

ask() {
  local reason="$1"
  jq -n --arg reason "$reason" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "ask",
      permissionDecisionReason: $reason
    }
  }'
}

if [[ "$TOOL_NAME" == "Bash" ]]; then
  if echo "$COMMAND" | grep -Eiq "$DANGEROUS_REGEX"; then
    ask "Potentially destructive or production-impacting command. Human approval required."
    exit 0
  fi
  if echo "$COMMAND" | grep -Eiq "$SECRET_REGEX|$PROD_REGEX"; then
    ask "Command may involve secrets, wallets, production, real funds, or sensitive credentials. Human approval required."
    exit 0
  fi
fi

if [[ "$TOOL_NAME" =~ ^(Edit|Write|MultiEdit)$ ]]; then
  if echo "$FILE_PATH" | grep -Eiq "$ENV_FILE_REGEX"; then
    ask "Editing environment or secret-like files may expose credentials. Human approval required."
    exit 0
  fi
fi

exit 0
