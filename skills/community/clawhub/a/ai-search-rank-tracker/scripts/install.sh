#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_EXAMPLE="$ROOT_DIR/.env.example"
ENV_FILE="$ROOT_DIR/.env"
STARTER_JSON="$ROOT_DIR/prompts/starter.json"

printf "\n==> AI Search Rank Tracker installer\n"
printf "Root: %s\n\n" "$ROOT_DIR"

if ! command -v node >/dev/null 2>&1; then
  echo "Error: node is not installed. Please install Node.js 18+ first."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "Error: npm is not installed. Please install npm first."
  exit 1
fi

NODE_VERSION="$(node -v)"
printf "Detected Node: %s\n" "$NODE_VERSION"

cd "$ROOT_DIR"

echo "\n==> Installing dependencies"
npm install

if [ ! -f "$ENV_FILE" ]; then
  echo "\n==> Creating .env from .env.example"
  cp "$ENV_EXAMPLE" "$ENV_FILE"
else
  echo "\n==> Keeping existing .env (not overwriting)"
fi

printf "\n==> Optional setup\n"
read -r -p "Brand/domain to track (press Enter to keep starter config): " BRAND_INPUT || true

if [ -n "${BRAND_INPUT:-}" ]; then
  BRAND_INPUT="$BRAND_INPUT" node - <<'NODE'
const fs = require('fs');
const path = require('path');
const starterPath = path.join(process.cwd(), 'prompts', 'starter.json');
const brand = process.env.BRAND_INPUT;
const data = JSON.parse(fs.readFileSync(starterPath, 'utf8'));
data.brand = brand;
const bare = String(brand).replace(/^https?:\/\//, '').replace(/^www\./, '');
data.aliases = Array.from(new Set([bare, bare.replace(/\.ai$/, ''), bare.replace(/[-_]/g, ' ')]));
fs.writeFileSync(starterPath, JSON.stringify(data, null, 2));
console.log(`Updated starter.json brand => ${brand}`);
NODE
fi

cat <<EOF

==> Install complete

Next steps:
1. Open and fill your API keys:
   $ENV_FILE

2. Run the tracker:
   npm run run:starter

3. Find generated reports in:
   $ROOT_DIR/output/

Supported outputs:
- output/*.json
- output/*.md
- output/*.csv

EOF
