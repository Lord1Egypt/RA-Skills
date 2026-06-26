#!/usr/bin/env bash
# AttentionMarket Skill Setup
# Signs in with email + password via Supabase Auth, looks up your API key,
# and saves it so you never have to configure it again.

set -euo pipefail

SUPABASE_URL="https://peruwnbrqkvmrldhpoom.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBlcnV3bmJycWt2bXJsZGhwb29tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk5NjcwMDYsImV4cCI6MjA4NTU0MzAwNn0.FMCjeunas8ICKm9W9bo2hZwyrBttzTcJbplbAyl4XhU"
CONFIG_FILE="${HOME}/.clawdbot/clawdbot.json"
ENV_FILE="${HOME}/.clawdbot/.env"

echo "========================================"
echo "  AttentionMarket - One-Time Setup"
echo "========================================"
echo ""
echo "Sign in with your AttentionMarket developer account."
echo "Don't have one? Sign up at https://dashboard.attentionmarket.ai"
echo ""

# Prompt for credentials
read -rp "Email: " email
read -rsp "Password: " password
echo ""

echo ""
echo "Signing in..."

# Authenticate with Supabase Auth
auth_response=$(curl -s -X POST "${SUPABASE_URL}/auth/v1/token?grant_type=password" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"${email}\", \"password\": \"${password}\"}")

# Check for errors
access_token=$(echo "$auth_response" | jq -r '.access_token // empty')
if [ -z "$access_token" ]; then
  error_msg=$(echo "$auth_response" | jq -r '.error_description // .msg // .error // "Unknown error"')
  echo "Login failed: ${error_msg}"
  exit 1
fi

echo "Authenticated. Looking up your API key..."

# Look up developer record using the session token
developer_response=$(curl -s "${SUPABASE_URL}/rest/v1/developers?select=api_key_live,agent_id&user_id=eq.$(echo "$auth_response" | jq -r '.user.id')" \
  -H "apikey: ${SUPABASE_ANON_KEY}" \
  -H "Authorization: Bearer ${access_token}")

api_key=$(echo "$developer_response" | jq -r '.[0].api_key_live // empty')
agent_id=$(echo "$developer_response" | jq -r '.[0].agent_id // empty')

if [ -z "$api_key" ]; then
  echo "No developer account linked to ${email}."
  echo "Sign up at https://dashboard.attentionmarket.ai"
  exit 1
fi

echo "Found API key for agent: ${agent_id}"

# Save to environment file
mkdir -p "$(dirname "$ENV_FILE")"
if [ -f "$ENV_FILE" ]; then
  # Remove existing AM_API_KEY line if present
  grep -v '^AM_API_KEY=' "$ENV_FILE" > "${ENV_FILE}.tmp" 2>/dev/null || true
  mv "${ENV_FILE}.tmp" "$ENV_FILE"
fi
echo "AM_API_KEY=${api_key}" >> "$ENV_FILE"

# Also export for current session
export AM_API_KEY="$api_key"

echo ""
echo "========================================"
echo "  Setup complete!"
echo "========================================"
echo ""
echo "Your API key has been saved to: ${ENV_FILE}"
echo "Agent ID: ${agent_id}"
echo ""
echo "You can now use AttentionMarket in OpenClaw."
echo "Try: \"find me taco deals near me\""
echo ""
echo "To use in your current shell, run:"
echo "  export AM_API_KEY=${api_key}"
