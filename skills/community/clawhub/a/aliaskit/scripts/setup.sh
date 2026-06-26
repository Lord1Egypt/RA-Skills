#!/usr/bin/env bash
set -euo pipefail

# Resolve skill directory (where this script lives)
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
IDENTITY_FILE="$SKILL_DIR/identity.json"

# 1. Check if identity already exists
if [ -f "$IDENTITY_FILE" ]; then
  echo "Identity already exists: $IDENTITY_FILE"
  cat "$IDENTITY_FILE"
  exit 0
fi

# 2. Check for API key (env var, or prompt)
if [ -z "${ALIASKIT_API_KEY:-}" ]; then
  echo "No ALIASKIT_API_KEY found in environment."
  echo ""
  echo "Get your key at: https://aliaskit.com/dashboard"
  echo ""
  printf "Paste your API key (or press Enter to cancel): "
  read -r ALIASKIT_API_KEY 2>/dev/null || ALIASKIT_API_KEY=""

  if [ -z "$ALIASKIT_API_KEY" ]; then
    echo "No key provided. Run this script again when you have one."
    exit 1
  fi

  export ALIASKIT_API_KEY
fi

# 3. Install or update aliaskit SDK to latest
echo "Ensuring latest aliaskit SDK..."
npm install aliaskit@latest --save 2>/dev/null || npm install aliaskit@latest 2>/dev/null

# 4. ASK: existing identity or new one?
echo ""
echo "Do you have an existing AliasKit identity ID?"
echo ""
echo "  If YES: paste the identity ID below"
echo "  If NO:  press Enter to create a new identity"
echo ""
printf "Identity ID (or Enter for new): "
read -r EXISTING_ID 2>/dev/null || EXISTING_ID=""

if [ -n "$EXISTING_ID" ]; then
  # Fetch existing identity
  echo "Fetching identity $EXISTING_ID..."
  node -e "
const { AliasKit, generateCardKey } = require('aliaskit');

(async () => {
  try {
    const ak = new AliasKit();
    const identity = await ak.identities.get('$EXISTING_ID');
    const cardKey = generateCardKey();

    const state = {
      apiKey: process.env.ALIASKIT_API_KEY,
      identityId: identity.id,
      email: identity.email,
      phone: identity.phone_number || null,
      name: identity.name,
      dob: identity.date_of_birth || null,
      cardKey: cardKey,
      createdAt: new Date().toISOString()
    };

    require('fs').writeFileSync(
      '$IDENTITY_FILE',
      JSON.stringify(state, null, 2)
    );

    console.log('');
    console.log('Identity loaded:');
    console.log('  Name:  ' + state.name);
    console.log('  Email: ' + state.email);
    console.log('  Phone: ' + (state.phone || 'not provisioned'));
    console.log('  ID:    ' + state.identityId);
    console.log('');
    console.log('Saved to: $IDENTITY_FILE');
  } catch (err) {
    console.error('Failed to fetch identity:', err.message || err);
    process.exit(1);
  }
})();
"
else
  # Create new identity
  echo "Creating a new identity..."
  node -e "
const { AliasKit, generateCardKey } = require('aliaskit');

(async () => {
  try {
    const ak = new AliasKit();
    const identity = await ak.identities.create({ provisionPhone: true });
    const cardKey = generateCardKey();

    const state = {
      apiKey: process.env.ALIASKIT_API_KEY,
      identityId: identity.id,
      email: identity.email,
      phone: identity.phone_number || null,
      name: identity.name,
      dob: identity.date_of_birth || null,
      cardKey: cardKey,
      createdAt: new Date().toISOString()
    };

    require('fs').writeFileSync(
      '$IDENTITY_FILE',
      JSON.stringify(state, null, 2)
    );

    console.log('');
    console.log('Identity created:');
    console.log('  Name:  ' + state.name);
    console.log('  Email: ' + state.email);
    console.log('  Phone: ' + (state.phone || 'not provisioned'));
    console.log('  ID:    ' + state.identityId);
    console.log('');
    console.log('Saved to: $IDENTITY_FILE');
  } catch (err) {
    console.error('Failed to create identity:', err.message || err);
    process.exit(1);
  }
})();
"
fi

echo ""
echo "Setup complete. Your agent now has a digital identity."
