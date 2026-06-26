#!/bin/bash
# find-rss.sh - Find RSS/Atom feeds for a given website
# Usage: find-rss.sh <website_url>

URL="$1"

if [ -z "$URL" ]; then
    echo "Usage: find-rss.sh <website_url>"
    echo "Example: find-rss.sh https://techcrunch.com/"
    exit 1
fi

echo "🔍 Searching for RSS/Atom feeds on: $URL"
echo ""

# Fetch the page and extract RSS/Atom links
echo "📄 Checking HTML for RSS link tags..."
RSS_LINKS=$(curl -s -L "$URL" | grep -iE 'type="application/(rss|atom)"|rel="alternate"' | grep -iE 'href="[^"]*"' | sed 's/.*href="\([^"]*\)".*/\1/' | sort -u)

if [ -n "$RSS_LINKS" ]; then
    echo "✅ Found RSS/Atom feeds:"
    echo "$RSS_LINKS" | while read -r feed; do
        # Handle relative URLs
        if [[ "$feed" == /* ]]; then
            # Extract domain from URL
            DOMAIN=$(echo "$URL" | sed -E 's|(https?://[^/]+).*|\1|')
            echo "   $DOMAIN$feed"
        elif [[ "$feed" == http* ]]; then
            echo "   $feed"
        else
            # Relative path without leading slash
            BASE=$(echo "$URL" | sed -E 's|/[^/]*$|/|')
            echo "   $BASE$feed"
        fi
    done
else
    echo "❌ No RSS/Atom feeds found in HTML link tags"
fi

echo ""
echo "🔎 Checking common RSS paths..."

# Extract domain
DOMAIN=$(echo "$URL" | sed -E 's|(https?://[^/]+).*|\1|')

# Common RSS paths to check
COMMON_PATHS=(
    "/feed"
    "/feed/"
    "/rss"
    "/rss/"
    "/atom"
    "/atom/"
    "/feeds"
    "/feeds/"
    "/index.xml"
    "/feed.xml"
    "/rss.xml"
    "/atom.xml"
    "/blog/feed"
    "/blog/rss"
    "/news/feed"
    "/news/rss"
)

FOUND=0
for path in "${COMMON_PATHS[@]}"; do
    TEST_URL="${DOMAIN}${path}"
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -L "$TEST_URL" 2>/dev/null)
    if [ "$STATUS" = "200" ]; then
        # Check if it's actually an RSS/Atom feed
        CONTENT_TYPE=$(curl -s -I -L "$TEST_URL" 2>/dev/null | grep -i "content-type" | head -1)
        if echo "$CONTENT_TYPE" | grep -qiE "(rss|atom|xml)"; then
            echo "   ✅ $TEST_URL"
            FOUND=$((FOUND + 1))
        fi
    fi
done

if [ $FOUND -eq 0 ]; then
    echo "   ❌ No common RSS paths found"
fi

echo ""
echo "💡 Tip: If no feeds found, try:"
echo "   - Checking the website's footer for 'RSS' link"
echo "   - Searching '[sitename] RSS feed' on Google"
echo "   - Using a feed discovery service like feedly.com"
