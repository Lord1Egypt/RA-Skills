#!/usr/bin/env bash
# sync-abi.sh — Sync contract ABIs from build artifacts to your frontend
#
# Usage:
#   bash scripts/sync-abi.sh
#
# Config (env vars or edit defaults below):
#   ABI_SOURCE     Build output dir. Foundry: "out"  |  Hardhat: "artifacts/contracts"
#   ABI_DEST       Where to write ABI JSON files. Default: "frontend/src/abis"
#   ABI_CONTRACTS  Space-separated contract names (overrides .abi-sync file)
#
# .abi-sync file (one contract per line, in project root):
#   MyToken
#   MyVault:Vault          ← writes to Vault.json instead of MyVault.json
#   MyFactory

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration defaults
# ---------------------------------------------------------------------------
ABI_SOURCE="${ABI_SOURCE:-out}"
ABI_DEST="${ABI_DEST:-frontend/src/abis}"

# ---------------------------------------------------------------------------
# Load contract list
# ---------------------------------------------------------------------------
declare -a CONTRACTS=()

if [[ -n "${ABI_CONTRACTS:-}" ]]; then
  # Space-separated env var takes precedence
  read -ra CONTRACTS <<< "$ABI_CONTRACTS"
elif [[ -f ".abi-sync" ]]; then
  # Read .abi-sync file, skip empty lines and comments
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%%#*}"      # strip inline comments
    line="${line// /}"      # trim spaces
    [[ -z "$line" ]] && continue
    CONTRACTS+=("$line")
  done < ".abi-sync"
else
  echo "❌ No contracts specified. Set ABI_CONTRACTS env var or create .abi-sync file."
  echo ""
  echo "Example .abi-sync:"
  echo "  MyToken"
  echo "  MyVault:Vault   # write as Vault.json"
  exit 1
fi

if [[ ${#CONTRACTS[@]} -eq 0 ]]; then
  echo "❌ Contract list is empty."
  exit 1
fi

# ---------------------------------------------------------------------------
# Ensure destination exists
# ---------------------------------------------------------------------------
mkdir -p "$ABI_DEST"

echo "Source: $ABI_SOURCE"
echo "Dest:   $ABI_DEST"
echo "Contracts: ${CONTRACTS[*]}"
echo ""

# ---------------------------------------------------------------------------
# Check for jq
# ---------------------------------------------------------------------------
HAS_JQ=false
if command -v jq &>/dev/null; then
  HAS_JQ=true
fi

# ---------------------------------------------------------------------------
# Helper: find artifact JSON for a contract name
# ---------------------------------------------------------------------------
find_artifact() {
  local contract_name="$1"

  # Foundry: out/ContractName.sol/ContractName.json
  local foundry_path="$ABI_SOURCE/$contract_name.sol/$contract_name.json"
  if [[ -f "$foundry_path" ]]; then
    echo "$foundry_path"
    return
  fi

  # Hardhat: artifacts/contracts/**/*.json (excluding .dbg.json)
  local hardhat_result
  hardhat_result=$(find "$ABI_SOURCE" -name "${contract_name}.json" ! -name "*.dbg.json" 2>/dev/null | head -n1)
  if [[ -n "$hardhat_result" ]]; then
    echo "$hardhat_result"
    return
  fi

  # Generic fallback: any .json with matching filename in source tree
  local generic_result
  generic_result=$(find "$ABI_SOURCE" -name "${contract_name}.json" 2>/dev/null | head -n1)
  if [[ -n "$generic_result" ]]; then
    echo "$generic_result"
    return
  fi

  echo ""
}

# ---------------------------------------------------------------------------
# Helper: extract ABI from artifact
# ---------------------------------------------------------------------------
extract_abi() {
  local artifact_path="$1"

  if $HAS_JQ; then
    # Try to extract .abi field (Foundry/Hardhat artifact format)
    local abi
    abi=$(jq -e '.abi' "$artifact_path" 2>/dev/null) && echo "$abi" && return
    # File might already be a raw ABI array
    jq -e 'if type == "array" then . else error end' "$artifact_path" 2>/dev/null && cat "$artifact_path" && return
    echo ""
  else
    # No jq: check if .abi key exists in JSON via grep, then use Python as fallback
    if grep -q '"abi"' "$artifact_path"; then
      if command -v python3 &>/dev/null; then
        python3 -c "import json,sys; d=json.load(open('$artifact_path')); print(json.dumps(d['abi'], indent=2))"
        return
      elif command -v python &>/dev/null; then
        python -c "import json,sys; d=json.load(open('$artifact_path')); print(json.dumps(d['abi'], indent=2))"
        return
      fi
    fi
    # Assume file IS the ABI array
    cat "$artifact_path"
  fi
}

# ---------------------------------------------------------------------------
# Main sync loop
# ---------------------------------------------------------------------------
FAILED=0
SUCCEEDED=0

for entry in "${CONTRACTS[@]}"; do
  # Parse "ContractName:output-name" or just "ContractName"
  contract_name="${entry%%:*}"
  output_name="${entry##*:}"
  [[ "$output_name" == "$entry" ]] && output_name="$contract_name"  # no colon = same name

  dest_file="$ABI_DEST/${output_name}.json"

  # Find artifact
  artifact=$(find_artifact "$contract_name")

  if [[ -z "$artifact" ]]; then
    echo "❌ $contract_name — artifact not found in $ABI_SOURCE"
    FAILED=$((FAILED + 1))
    continue
  fi

  # Extract ABI
  abi=$(extract_abi "$artifact")

  if [[ -z "$abi" ]]; then
    echo "❌ $contract_name — could not extract ABI from $artifact"
    FAILED=$((FAILED + 1))
    continue
  fi

  # Write to destination
  echo "$abi" > "$dest_file"
  echo "✅ $contract_name → $dest_file (from $artifact)"
  SUCCEEDED=$((SUCCEEDED + 1))
done

echo ""
echo "Done: $SUCCEEDED synced, $FAILED failed."

[[ $FAILED -gt 0 ]] && exit 1
exit 0
