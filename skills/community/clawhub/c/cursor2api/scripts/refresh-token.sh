#!/bin/bash
# cursor-token-refresh.sh - Auto-refresh cursor2api token
# Usage: ./refresh-token.sh <new_token>

set -e

CONTAINER_NAME="cursor-api"
CONTAINER_PORT="3010"
NEW_TOKEN="$1"

if [ -z "$NEW_TOKEN" ]; then
    echo "❌ Usage: ./refresh-token.sh <new_token>"
    echo "    Example: ./refresh-token.sh 'eyJhbGciOiJS...' "
    exit 1
fi

echo "🔄 Stopping existing container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

echo "🚀 Starting new container..."
docker run -d \
  --name $CONTAINER_NAME \
  -p ${CONTAINER_PORT}:3000 \
  -e WORKOS_CURSOR_SESSION_TOKEN="$NEW_TOKEN" \
  waitkafuka/cursor-api:latest

echo ""
echo "✅ Token updated, container restarted on port $CONTAINER_PORT"
docker ps | grep $CONTAINER_NAME
