#!/usr/bin/env bash
# generate-shared-types.sh — Generate TypeScript types from OpenAPI spec
#
# Usage: bash generate-shared-types.sh /path/to/project
#
# Requires: npx (Node.js)
# Uses openapi-typescript to generate types from api-spec.yaml

set -euo pipefail

PROJECT="${1:-.}"
SPEC="$PROJECT/contracts/api-spec.yaml"
OUTPUT="$PROJECT/contracts/shared-types.generated.ts"

if [[ ! -f "$SPEC" ]]; then
  echo "❌ API spec not found: $SPEC"
  exit 1
fi

if ! command -v npx &>/dev/null; then
  echo "❌ npx not found. Install Node.js first."
  exit 1
fi

echo "🛡️  Generating shared types from: $SPEC"
npx --yes openapi-typescript "$SPEC" -o "$OUTPUT"
echo "✅ Generated: $OUTPUT"
echo ""
echo "Note: This is auto-generated. For manual shared types, edit contracts/shared-types.ts directly."
