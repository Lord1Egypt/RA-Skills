#!/bin/bash
# Search Discord message history via discrawl
# Usage: search_history.sh <query> [channel_id] [limit]

QUERY="$1"
CHANNEL_ID="${2:-}"
LIMIT="${3:-10}"

if [ -z "$QUERY" ]; then
    echo "Usage: search_history.sh <query> [channel_id] [limit]"
    exit 1
fi

if [ -n "$CHANNEL_ID" ]; then
    discrawl sql "SELECT m.content, m.created_at, COALESCE(u.username, m.author_id) as author, COALESCE(c.name, m.channel_id) as channel FROM messages m LEFT JOIN members u ON m.author_id = u.user_id LEFT JOIN channels c ON m.channel_id = c.id WHERE m.channel_id = '$CHANNEL_ID' AND (m.content LIKE '%$QUERY%' OR m.normalized_content LIKE '%$QUERY%') ORDER BY m.created_at DESC LIMIT $LIMIT;"
else
    discrawl sql "SELECT m.content, m.created_at, COALESCE(u.username, m.author_id) as author, COALESCE(c.name, m.channel_id) as channel FROM messages m LEFT JOIN members u ON m.author_id = u.user_id LEFT JOIN channels c ON m.channel_id = c.id WHERE m.content LIKE '%$QUERY%' OR m.normalized_content LIKE '%$QUERY%' ORDER BY m.created_at DESC LIMIT $LIMIT;"
fi
