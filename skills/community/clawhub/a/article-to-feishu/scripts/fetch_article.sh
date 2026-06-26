#!/bin/bash
# Fetch article content from Toutiao (今日头条) using Jina AI Reader API
# Usage: fetch_article.sh <toutiao_url>

set -e

if [ -z "$1" ]; then
    echo "Usage: fetch_article.sh <toutiao_url>"
    echo "Example: fetch_article.sh 'https://m.toutiao.com/is/m3EX1m0Z3Mo/'"
    exit 1
fi

URL="$1"
JINA_API="https://r.jina.ai/"

# Build Jina Reader URL
JINA_URL="${JINA_API}${URL}"

# Fetch article content
curl -sL "$JINA_URL" 2>/dev/null