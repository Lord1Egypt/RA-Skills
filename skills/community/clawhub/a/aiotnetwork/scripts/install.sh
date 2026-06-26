#!/usr/bin/env bash
set -euo pipefail

# Install all AIOT Network skills via ClawHub
# Usage: bash scripts/install.sh

SKILLS=(
  "aiotnetwork-account-auth"
  "aiotnetwork-kyc-identity"
  "aiotnetwork-card-management"
  "aiotnetwork-payments-banking"
  "aiotnetwork-crypto-wallet"
  "aiotnetwork-blockchain-did"
)

echo "Installing ${#SKILLS[@]} AIOT Network skills..."
echo ""

FAILED=0
SUCCEEDED=0

for slug in "${SKILLS[@]}"; do
  echo "→ Installing ${slug}..."
  if clawhub install "${slug}"; then
    ((SUCCEEDED++))
  else
    echo "  ✗ Failed to install ${slug}"
    ((FAILED++))
  fi
done

echo ""
echo "Done. ${SUCCEEDED} installed, ${FAILED} failed."

if [ "${FAILED}" -gt 0 ]; then
  exit 1
fi
