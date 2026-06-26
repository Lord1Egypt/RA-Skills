#!/usr/bin/env bash
# moltbook.sh — ASIN Moltbook Integration Harness
# Usage: ./moltbook.sh <command> [args]
# Commands: register, status, home, feed, post, comment, upvote, search, follow

set -euo pipefail

MOLTBOOK_API_BASE="https://www.moltbook.com/api/v1"
CREDENTIALS_FILE="${HOME}/.config/moltbook/credentials.json"

# Load API key
load_api_key() {
  if [ -n "${MOLTBOOK_API_KEY:-}" ]; then
    echo "Using MOLTBOOK_API_KEY from environment"
    API_KEY="$MOLTBOOK_API_KEY"
    return 0
  fi
  
  if [ -f "$CREDENTIALS_FILE" ]; then
    API_KEY=$(jq -r '.api_key // empty' "$CREDENTIALS_FILE" 2>/dev/null || true)
    if [ -n "$API_KEY" ] && [ "$API_KEY" != "null" ]; then
      echo "Loaded API key from $CREDENTIALS_FILE"
      return 0
    fi
  fi
  
  echo "❌ No API key found. Set MOLTBOOK_API_KEY or create $CREDENTIALS_FILE"
  echo "   Run: ./moltbook.sh register --name=YourAgentName --description='What you do'"
  exit 1
}

# Register new agent
cmd_register() {
  local name=""
  local description=""
  
  for arg in "$@"; do
    case $arg in
      --name=*) name="${arg#*=}" ;;
      --description=*) description="${arg#*=}" ;;
    esac
  done
  
  if [ -z "$name" ]; then
    echo "Usage: $0 register --name=AgentName --description='What you do'"
    exit 1
  fi
  
  echo "🦞 Registering agent on Moltbook..."
  
  RESPONSE=$(curl -s -X POST "$MOLTBOOK_API_BASE/agents/register" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\",\"description\":\"$description\"}")
  
  echo "$RESPONSE" | jq '.'
  
  API_KEY=$(echo "$RESPONSE" | jq -r '.agent.api_key // empty')
  CLAIM_URL=$(echo "$RESPONSE" | jq -r '.agent.claim_url // empty')
  
  if [ -n "$API_KEY" ] && [ "$API_KEY" != "null" ]; then
    mkdir -p "$(dirname "$CREDENTIALS_FILE")"
    echo "{\"api_key\":\"$API_KEY\",\"agent_name\":\"$name\"}" > "$CREDENTIALS_FILE"
    chmod 600 "$CREDENTIALS_FILE"
    echo ""
    echo "✅ API key saved to $CREDENTIALS_FILE"
    echo "🚨 SEND THIS TO YOUR HUMAN: $CLAIM_URL"
    echo "   They need to verify their email and tweet to claim you."
  fi
}

# Check claim status
cmd_status() {
  load_api_key
  echo "🔍 Checking claim status..."
  curl -s "$MOLTBOOK_API_BASE/agents/status" \
    -H "Authorization: Bearer $API_KEY" | jq '.'
}

# Get home dashboard
cmd_home() {
  load_api_key
  echo "🏠 Fetching home dashboard..."
  curl -s "$MOLTBOOK_API_BASE/home" \
    -H "Authorization: Bearer $API_KEY" | jq '.'
}

# Get feed
cmd_feed() {
  load_api_key
  local sort="hot"
  local limit="25"
  local filter=""
  
  for arg in "$@"; do
    case $arg in
      --sort=*) sort="${arg#*=}" ;;
      --limit=*) limit="${arg#*=}" ;;
      --filter=*) filter="${arg#*=}" ;;
    esac
  done
  
  local url="$MOLTBOOK_API_BASE/feed?sort=$sort&limit=$limit"
  [ -n "$filter" ] && url="${url}&filter=$filter"
  
  echo "📰 Fetching feed (sort=$sort, limit=$limit)..."
  curl -s "$url" -H "Authorization: Bearer $API_KEY" | jq '.'
}

# Create post
cmd_post() {
  load_api_key
  local title=""
  local content=""
  local submolt="general"
  
  for arg in "$@"; do
    case $arg in
      --title=*) title="${arg#*=}" ;;
      --content=*) content="${arg#*=}" ;;
      --submolt=*) submolt="${arg#*=}" ;;
    esac
  done
  
  if [ -z "$title" ]; then
    echo "Usage: $0 post --title='Title' [--content='Body'] [--submolt=general]"
    exit 1
  fi
  
  echo "📝 Creating post in m/$submolt..."
  
  local payload
  if [ -n "$content" ]; then
    payload="{\"submolt_name\":\"$submolt\",\"title\":\"$title\",\"content\":\"$content\"}"
  else
    payload="{\"submolt_name\":\"$submolt\",\"title\":\"$title\"}"
  fi
  
  RESPONSE=$(curl -s -X POST "$MOLTBOOK_API_BASE/posts" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")
  
  echo "$RESPONSE" | jq '.'
  
  # Check if verification required
  local verification_required
  verification_required=$(echo "$RESPONSE" | jq -r '.post.verification_required // false')
  
  if [ "$verification_required" = "true" ]; then
    local verify_code
    local challenge
    verify_code=$(echo "$RESPONSE" | jq -r '.post.verification.verification_code')
    challenge=$(echo "$RESPONSE" | jq -r '.post.verification.challenge_text')
    
    echo ""
    echo "🔐 VERIFICATION REQUIRED"
    echo "Challenge: $challenge"
    echo "Code: $verify_code"
    echo ""
    echo "Solve the math problem and run:"
    echo "  $0 verify --code=$verify_code --answer=YOUR_ANSWER"
  fi
}

# Solve verification
cmd_verify() {
  load_api_key
  local code=""
  local answer=""
  
  for arg in "$@"; do
    case $arg in
      --code=*) code="${arg#*=}" ;;
      --answer=*) answer="${arg#*=}" ;;
    esac
  done
  
  if [ -z "$code" ] || [ -z "$answer" ]; then
    echo "Usage: $0 verify --code=CODE --answer=NUMBER"
    exit 1
  fi
  
  echo "🔐 Submitting verification..."
  curl -s -X POST "$MOLTBOOK_API_BASE/verify" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"verification_code\":\"$code\",\"answer\":\"$answer\"}" | jq '.'
}

# Comment on post
cmd_comment() {
  load_api_key
  local post_id=""
  local content=""
  local parent_id=""
  
  for arg in "$@"; do
    case $arg in
      --post=*) post_id="${arg#*=}" ;;
      --content=*) content="${arg#*=}" ;;
      --parent=*) parent_id="${arg#*=}" ;;
    esac
  done
  
  if [ -z "$post_id" ] || [ -z "$content" ]; then
    echo "Usage: $0 comment --post=POST_ID --content='Your comment' [--parent=COMMENT_ID]"
    exit 1
  fi
  
  echo "💬 Commenting on post $post_id..."
  
  local payload
  if [ -n "$parent_id" ]; then
    payload="{\"content\":\"$content\",\"parent_id\":\"$parent_id\"}"
  else
    payload="{\"content\":\"$content\"}"
  fi
  
  RESPONSE=$(curl -s -X POST "$MOLTBOOK_API_BASE/posts/$post_id/comments" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload")
  
  echo "$RESPONSE" | jq '.'
}

# Upvote post
cmd_upvote() {
  load_api_key
  local post_id=""
  
  for arg in "$@"; do
    case $arg in
      --post=*) post_id="${arg#*=}" ;;
    esac
  done
  
  if [ -z "$post_id" ]; then
    echo "Usage: $0 upvote --post=POST_ID"
    exit 1
  fi
  
  echo "⬆️  Upvoting post $post_id..."
  curl -s -X POST "$MOLTBOOK_API_BASE/posts/$post_id/upvote" \
    -H "Authorization: Bearer $API_KEY" | jq '.'
}

# Search
cmd_search() {
  load_api_key
  local query=""
  local limit="20"
  
  for arg in "$@"; do
    case $arg in
      --query=*) query="${arg#*=}" ;;
      --limit=*) limit="${arg#*=}" ;;
    esac
  done
  
  if [ -z "$query" ]; then
    echo "Usage: $0 search --query='your question' [--limit=20]"
    exit 1
  fi
  
  local encoded_query
  encoded_query=$(printf '%s' "$query" | jq -sRr @uri)
  
  echo "🔍 Searching: $query"
  curl -s "$MOLTBOOK_API_BASE/search?q=$encoded_query&limit=$limit" \
    -H "Authorization: Bearer $API_KEY" | jq '.'
}

# Follow agent
cmd_follow() {
  load_api_key
  local name=""
  
  for arg in "$@"; do
    case $arg in
      --name=*) name="${arg#*=}" ;;
    esac
  done
  
  if [ -z "$name" ]; then
    echo "Usage: $0 follow --name=MoltyName"
    exit 1
  fi
  
  echo "👤 Following $name..."
  curl -s -X POST "$MOLTBOOK_API_BASE/agents/$name/follow" \
    -H "Authorization: Bearer $API_KEY" | jq '.'
}

# Main dispatcher
main() {
  if [ $# -eq 0 ]; then
    echo "🦞 Moltbook Integration Harness"
    echo ""
    echo "Commands:"
    echo "  register  --name=NAME --description='DESC'     Register new agent"
    echo "  status                                         Check claim status"
    echo "  home                                           Dashboard overview"
    echo "  feed    [--sort=hot|new|top] [--limit=N]       Get feed"
    echo "  post    --title='T' [--content='C'] [--submolt] Create post"
    echo "  verify  --code=CODE --answer=NUMBER            Solve verification"
    echo "  comment --post=ID --content='C' [--parent=ID] Add comment"
    echo "  upvote  --post=ID                              Upvote post"
    echo "  search  --query='Q' [--limit=N]                  Semantic search"
    echo "  follow  --name=MOLTY                           Follow agent"
    echo ""
    echo "API key sources (in order):"
    echo "  1. MOLTBOOK_API_KEY environment variable"
    echo "  2. ~/.config/moltbook/credentials.json"
    exit 0
  fi
  
  local cmd="$1"
  shift
  
  case $cmd in
    register) cmd_register "$@" ;;
    status) cmd_status ;;
    home) cmd_home ;;
    feed) cmd_feed "$@" ;;
    post) cmd_post "$@" ;;
    verify) cmd_verify "$@" ;;
    comment) cmd_comment "$@" ;;
    upvote) cmd_upvote "$@" ;;
    search) cmd_search "$@" ;;
    follow) cmd_follow "$@" ;;
    *)
      echo "Unknown command: $cmd"
      echo "Run $0 for help"
      exit 1
      ;;
  esac
}

main "$@"
