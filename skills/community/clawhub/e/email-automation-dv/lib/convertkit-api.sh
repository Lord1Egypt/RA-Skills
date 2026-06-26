#!/usr/bin/env bash
# ConvertKit API wrapper functions

CONVERTKIT_API_BASE="https://api.convertkit.com/v3"

# Check if API key is set
check_convertkit_auth() {
  if [[ -z "${CONVERTKIT_API_SECRET:-}" ]]; then
    echo "Error: CONVERTKIT_API_SECRET not set"
    echo "Get your API secret from: https://app.convertkit.com/account/edit"
    echo "Then: export CONVERTKIT_API_SECRET=your_secret"
    return 1
  fi
  return 0
}

# Create a sequence
# Usage: convertkit_create_sequence "Sequence Name"
convertkit_create_sequence() {
  local sequence_name="$1"
  check_convertkit_auth || return 1
  
  curl -s -X POST "$CONVERTKIT_API_BASE/sequences" \
    -H "Content-Type: application/json" \
    -d "{
      \"api_secret\": \"$CONVERTKIT_API_SECRET\",
      \"name\": \"$sequence_name\"
    }"
}

# List all sequences
convertkit_list_sequences() {
  check_convertkit_auth || return 1
  
  curl -s "$CONVERTKIT_API_BASE/sequences?api_secret=$CONVERTKIT_API_SECRET"
}

# Subscribe email to sequence
# Usage: convertkit_subscribe_to_sequence SEQUENCE_ID EMAIL [FIRST_NAME]
convertkit_subscribe_to_sequence() {
  local sequence_id="$1"
  local email="$2"
  local first_name="${3:-}"
  check_convertkit_auth || return 1
  
  local data="{
    \"api_secret\": \"$CONVERTKIT_API_SECRET\",
    \"email\": \"$email\""
  
  if [[ -n "$first_name" ]]; then
    data="$data, \"first_name\": \"$first_name\""
  fi
  
  data="$data }"
  
  curl -s -X POST "$CONVERTKIT_API_BASE/sequences/$sequence_id/subscribe" \
    -H "Content-Type: application/json" \
    -d "$data"
}

# Get sequence subscribers
convertkit_get_subscribers() {
  local sequence_id="$1"
  check_convertkit_auth || return 1
  
  curl -s "$CONVERTKIT_API_BASE/sequences/$sequence_id/subscriptions?api_secret=$CONVERTKIT_API_SECRET"
}

# Add email to sequence
# Usage: convertkit_add_email SEQUENCE_ID SUBJECT CONTENT DELAY_DAYS
convertkit_add_email() {
  local sequence_id="$1"
  local subject="$2"
  local content="$3"
  local delay_days="${4:-0}"
  check_convertkit_auth || return 1
  
  curl -s -X POST "$CONVERTKIT_API_BASE/sequences/$sequence_id/emails" \
    -H "Content-Type: application/json" \
    -d "{
      \"api_secret\": \"$CONVERTKIT_API_SECRET\",
      \"subject\": \"$subject\",
      \"content\": \"$content\",
      \"delay_days\": $delay_days
    }"
}

# Test connection
convertkit_test_connection() {
  check_convertkit_auth || return 1
  
  echo "Testing ConvertKit API connection..."
  local response
  response=$(convertkit_list_sequences)
  
  if echo "$response" | jq -e '.sequences' >/dev/null 2>&1; then
    echo "✓ ConvertKit API connection successful"
    local count
    count=$(echo "$response" | jq '.sequences | length')
    echo "  Found $count sequences"
    return 0
  else
    echo "✗ ConvertKit API connection failed"
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
    return 1
  fi
}
