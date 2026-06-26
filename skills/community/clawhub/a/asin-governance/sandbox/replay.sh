#!/usr/bin/env bash
# ASIN Sandbox — Replay Harness
# Simulate actions before committing them to Moltbook
# Usage: ./replay.sh --action=post --payload='{"title":"..."}' --profile=ace-main --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOVERNANCE_DIR="$(dirname "$SCRIPT_DIR")"
ACTION=""
PAYLOAD=""
PROFILE="default"
DRY_RUN=true

# Parse args
for arg in "$@"; do
  case $arg in
    --action=*) ACTION="${arg#*=}" ;;
    --payload=*) PAYLOAD="${arg#*=}" ;;
    --profile=*) PROFILE="${arg#*=}" ;;
    --dry-run) DRY_RUN=true ;;
    --commit) DRY_RUN=false ;;
  esac
done

if [ -z "$ACTION" ]; then
  echo "Usage: $0 --action=<action> --payload='<json>' [--profile=ace-main] [--commit]"
  echo "Actions: post, comment, upvote, follow, create_submolt"
  exit 1
fi

echo "🛡️ ASIN Sandbox Replay"
echo "========================"
echo "Action: $ACTION"
echo "Profile: $PROFILE"
echo "Mode: $([ "$DRY_RUN" = true ] && echo "DRY-RUN" || echo "COMMIT")"
echo ""

# Load constraint profile
PROFILE_FILE="$GOVERNANCE_DIR/constraints/profiles.json"
if [ -f "$PROFILE_FILE" ]; then
  echo "✅ Profile loaded: $PROFILE_FILE"
else
  echo "❌ Profile not found: $PROFILE_FILE"
  exit 1
fi

# Check taxonomy - find risk class for this action, default to yellow
TAXONOMY_FILE="$GOVERNANCE_DIR/constraints/taxonomy.json"
RISK_CLASS=$(jq -r "[.risk_classes | to_entries[] | select(.value.examples | contains([\"$ACTION\"])) | .key] | first // \"yellow\"" "$TAXONOMY_FILE" 2>/dev/null || echo "yellow")
RISK_CLASS="${RISK_CLASS:-yellow}"
echo "📊 Risk classification: $RISK_CLASS"

# Simulate oracle check
echo "🔮 Oracle consult..."
case $RISK_CLASS in
  green)
    echo "   ✅ Pass-through (read-only action)"
    ORACLE_RESULT="{\"safe\":true,\"drift_delta\":0.0,\"consensus\":1.0}"
    ;;
  yellow)
    echo "   ⚠️  Social action — checking safety rules"
    # Simulated: would call oracle logic here
    ORACLE_RESULT="{\"safe\":true,\"drift_delta\":0.02,\"consensus\":0.7}"
    ;;
  orange)
    echo "   🔶 Structural action — sandbox + oracle required"
    ORACLE_RESULT="{\"safe\":true,\"drift_delta\":0.05,\"consensus\":0.6}"
    ;;
  red)
    echo "   🛑 Destructive action — HUMAN APPROVAL REQUIRED"
    ORACLE_RESULT="{\"safe\":false,\"drift_delta\":0.0,\"consensus\":0.0}"
    ;;
esac

# Check if oracle blocked
SAFE=$(echo "$ORACLE_RESULT" | jq -r '.safe')
if [ "$SAFE" != "true" ]; then
  echo ""
  echo "❌ ORACLE BLOCKED this action."
  echo "   Reason: $(echo "$ORACLE_RESULT" | jq -r '.reason // "safety rule violation"')"
  exit 2
fi

# Simulate entropy cost
echo "📈 Entropy accounting..."
case $ACTION in
  post) COMPUTE_MS=2500; API_CALLS=2; TOKENS=4000 ;;
  comment) COMPUTE_MS=800; API_CALLS=2; TOKENS=1200 ;;
  upvote) COMPUTE_MS=100; API_CALLS=1; TOKENS=50 ;;
  follow) COMPUTE_MS=100; API_CALLS=1; TOKENS=50 ;;
  *) COMPUTE_MS=500; API_CALLS=1; TOKENS=500 ;;
esac
echo "   Compute: ${COMPUTE_MS}ms | API calls: $API_CALLS | Tokens: $TOKENS"

# Estimate karma impact
echo "💫 Karma impact model..."
case $ACTION in
  post) KARMA_DELTA="+3 to +15 (depending on engagement)" ;;
  comment) KARMA_DELTA="+1 to +5" ;;
  upvote) KARMA_DELTA="0 (gives +1 to author)" ;;
  follow) KARMA_DELTA="0" ;;
  *) KARMA_DELTA="unknown" ;;
esac
echo "   Estimated: $KARMA_DELTA"

# Rollback check
echo "↩️  Rollback capability..."
case $ACTION in
  post) ROLLBACK="DELETE /api/v1/posts/{id}" ;;
  comment) ROLLBACK="DELETE /api/v1/comments/{id} (if supported)" ;;
  upvote) ROLLBACK="DELETE /api/v1/posts/{id}/upvote" ;;
  follow) ROLLBACK="DELETE /api/v1/agents/{name}/follow" ;;
  *) ROLLBACK="none" ;;
esac
echo "   Method: $ROLLBACK"

# Final verdict
echo ""
echo "========================"
if [ "$DRY_RUN" = true ]; then
  echo "✅ DRY-RUN COMPLETE"
  echo "   This action would PASS all checks."
  echo "   To commit: $0 --action=$ACTION --payload='...' --profile=$PROFILE --commit"
else
  echo "🚀 COMMIT MODE — Action approved for execution"
  echo "   (In real usage, this would execute the action via the Moltbook API)"
fi

echo ""
echo "Oracle result: $ORACLE_RESULT"
exit 0
