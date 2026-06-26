#!/bin/bash
# Corkboard CLI - Post pins to your Corkboard Dashboard
# Usage: corkboard <action> <type> <title> [content] [priority]
#
# Environment:
#   CORKBOARD_API       - API endpoint (default: http://localhost:3010)
#   CORKBOARD_TOKEN     - Bearer token for the corkboard server. If unset, the
#                         script reads it from $CORKBOARD_ENV_FILE (default .env
#                         in the current directory).
#   CORKBOARD_ENV_FILE  - .env file to load CORKBOARD_TOKEN from (default: ./.env)
#   CORKBOARD_AUTH      - set to "disabled" to skip auth (matches server flag)
#   CORKBOARD_ALERT_URL - Alert server for focus+sound (optional)

API_URL="${CORKBOARD_API:-http://localhost:3010}/api/pins"
ALERT_URL="${CORKBOARD_ALERT_URL:-}"

# Load CORKBOARD_TOKEN from .env if not already set in the shell environment.
if [[ -z "$CORKBOARD_TOKEN" ]]; then
    ENV_FILE="${CORKBOARD_ENV_FILE:-.env}"
    if [[ -f "$ENV_FILE" ]]; then
        CORKBOARD_TOKEN=$(grep -E '^CORKBOARD_TOKEN=' "$ENV_FILE" | tail -n1 | cut -d= -f2- | tr -d '"' | tr -d "'" | xargs)
    fi
fi

if [[ -z "$CORKBOARD_TOKEN" && "${CORKBOARD_AUTH:-}" != "disabled" ]]; then
    echo "Error: CORKBOARD_TOKEN not set and no .env file found." >&2
    echo "  Set CORKBOARD_TOKEN in your environment, run from the repo root, or" >&2
    echo "  point CORKBOARD_ENV_FILE at a .env file containing CORKBOARD_TOKEN." >&2
    echo "  If your server runs with CORKBOARD_AUTH=disabled, set the same here." >&2
    exit 1
fi

AUTH_HEADER=(-H "Authorization: Bearer ${CORKBOARD_TOKEN}")

show_help() {
    cat << 'EOF'
corkboard - Post pins to your Corkboard Dashboard

USAGE:
    corkboard add <type> <title> [content] [priority]
    corkboard list
    corkboard complete <id>
    corkboard delete <id>
    corkboard alert              # Focus window + play sound (requires alert server)

TYPES:
    task         - Action item (white card)
    note         - Reference note (yellow sticky)
    link         - URL bookmark (blue card) - use content for URL
    event        - Calendar event (purple card)
    alert        - Urgent notice (red card)
    email        - Email notification (coral card)
    opportunity  - Flagged opportunity
    briefing     - Morning briefing (spans 2 columns)
    github       - GitHub repo card (terminal style)
    idea         - Incubated idea with scores
    tracking     - Package tracking
    article      - Article summary with reader
    twitter      - X/Twitter post preview
    reddit       - Reddit post preview
    youtube      - YouTube video card with player

SPECIAL COMMANDS:
    corkboard add-email <from> <subject> [preview] [email_id]
    corkboard add-github <owner/repo> [description] [stars] [forks]
    corkboard add-idea <title> [verdict] [summary] [scores_json] [competitors] [effort]
    corkboard add-tracking <number> <carrier> [status] [eta] [url]
    corkboard add-article <title> <url> <source> <tldr> [bullets_json] [tags_json]
    corkboard add-opportunity <title> [content] [priority]
    corkboard add-briefing <title> <content>
    corkboard add-twitter <title> <content> [url]
    corkboard add-reddit <title> <content> [url]
    corkboard add-youtube <youtube-url>

VERDICTS (for ideas):
    hot | warm | cold | pass

TRACKING STATUS:
    pre-transit | in-transit | out-for-delivery | delivered | exception | unknown

PRIORITY:
    1 = High (urgent)
    2 = Medium (default)
    3 = Low

ENVIRONMENT:
    CORKBOARD_API       API endpoint (default: http://localhost:3010)
    CORKBOARD_TOKEN     Bearer token for the corkboard server. Auto-loaded
                        from .env in the current directory if unset.
    CORKBOARD_ENV_FILE  Path to .env file (default: ./.env)
    CORKBOARD_AUTH      Set to "disabled" to skip auth (matches server flag)
    CORKBOARD_ALERT_URL Alert server URL (optional)

EXAMPLES:
    corkboard add task "Test login flow" "After auth refactor" 1
    corkboard add note "Meeting notes" "Discussed API design"
    corkboard add link "Autoshop Demo" "https://autoshop.example.com"
    corkboard add alert "Server down" "503 errors in prod" 1
    corkboard add-email "boss@company.com" "Q4 Review" "Please review..." "msg-123"
    corkboard add-github "owner/repo" "Description here" 42 5
    corkboard add-idea "My SaaS" "hot" "Great market fit" '{"viability":8}' 3 "~2 weeks"
    corkboard add-tracking "1Z999AA10123456784" "UPS" "in-transit" "2026-03-30" "https://ups.com/track?num=..."
    corkboard add-article "AI Advances" "https://example.com/article" "TechCrunch" "Major AI breakthrough" '["Point 1","Point 2"]' '["ai","tech"]'
    corkboard add-opportunity "Wholesale lead" "Reply with pricing sheet" 2
    corkboard add-briefing "Morning briefing" "## Today\n- Ship the fix\n- Email the supplier"
    corkboard add-twitter "Interesting thread" "Thread about AI agents..." "https://x.com/user/status/123"
    corkboard add-reddit "Show HN" "New project launch..." "https://reddit.com/r/programming/..."
    corkboard add-youtube "https://youtu.be/dQw4w9WgXcQ"
    corkboard list
    corkboard complete abc-123-def
EOF
}

case "$1" in
    add)
        TYPE="$2"
        TITLE="$3"
        CONTENT="${4:-}"
        PRIORITY="${5:-2}"

        if [[ -z "$TYPE" || -z "$TITLE" ]]; then
            echo "Error: type and title required"
            echo "Usage: corkboard add <type> <title> [content] [priority]"
            exit 1
        fi

        # Build JSON payload
        if [[ "$TYPE" == "link" && -n "$CONTENT" ]]; then
            JSON=$(jq -n \
                --arg type "$TYPE" \
                --arg title "$TITLE" \
                --arg url "$CONTENT" \
                --argjson priority "$PRIORITY" \
                '{type: $type, title: $title, url: $url, priority: $priority}')
        else
            JSON=$(jq -n \
                --arg type "$TYPE" \
                --arg title "$TITLE" \
                --arg content "$CONTENT" \
                --argjson priority "$PRIORITY" \
                '{type: $type, title: $title, content: $content, priority: $priority}')
        fi

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [\(.type)] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    list)
        curl -s "${AUTH_HEADER[@]}" "$API_URL" | jq -r '.[] | "[\(.type)] \(.title) (\(.status)) - \(.id)"' 2>/dev/null
        ;;

    complete)
        ID="$2"
        if [[ -z "$ID" ]]; then
            echo "Error: id required"
            exit 1
        fi
        curl -s -X PATCH "$API_URL/$ID" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d '{"status":"completed"}' | jq -r '"Completed: \(.title)"' 2>/dev/null
        ;;

    delete)
        ID="$2"
        if [[ -z "$ID" ]]; then
            echo "Error: id required"
            exit 1
        fi
        curl -s -X DELETE "${AUTH_HEADER[@]}" "$API_URL/$ID"
        echo "Deleted: $ID"
        ;;

    alert)
        if [[ -z "$ALERT_URL" ]]; then
            echo "CORKBOARD_ALERT_URL not set"
            exit 1
        fi
        RESULT=$(curl -s -X POST "$ALERT_URL/alert" 2>/dev/null)
        if echo "$RESULT" | grep -q '"triggered":true'; then
            echo "Alert triggered (window focused + sound played)"
        else
            echo "Alert may have failed - check alert server"
        fi
        ;;

    add-github)
        REPO="$2"
        CONTENT="${3:-}"
        STARS="${4:-0}"
        FORKS="${5:-0}"

        if [[ -z "$REPO" ]]; then
            echo "Error: repo required"
            echo "Usage: corkboard add-github <repo> [description] [stars] [forks]"
            exit 1
        fi

        TITLE="${REPO##*/}"
        URL="https://github.com/$REPO"

        JSON=$(jq -n \
            --arg type "github" \
            --arg title "$TITLE" \
            --arg content "$CONTENT" \
            --arg repo "$REPO" \
            --arg url "$URL" \
            --argjson stars "$STARS" \
            --argjson forks "$FORKS" \
            '{type: $type, title: $title, content: $content, repo: $repo, url: $url, stars: $stars, forks: $forks}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [github] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-idea)
        TITLE="$2"
        VERDICT="${3:-warm}"
        SUMMARY="${4:-}"
        SCORES_JSON="${5:-}"
        COMPETITORS="${6:-0}"
        EFFORT="${7:-}"

        if [[ -z "$TITLE" ]]; then
            echo "Error: title required"
            echo "Usage: corkboard add-idea <title> [verdict] [summary] [scores_json] [competitors] [effort]"
            exit 1
        fi

        JSON=$(jq -n \
            --arg type "idea" \
            --arg title "$TITLE" \
            --arg verdict "$VERDICT" \
            --arg summary "$SUMMARY" \
            --argjson competitors "$COMPETITORS" \
            --arg effort "$EFFORT" \
            '{type: $type, title: $title, ideaVerdict: $verdict, ideaResearchSummary: $summary, ideaCompetitors: $competitors, ideaEffortEstimate: $effort}')

        if [[ -n "$SCORES_JSON" ]]; then
            JSON=$(echo "$JSON" | jq --argjson scores "$SCORES_JSON" '. + {ideaScores: $scores}')
        fi

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [idea] verdict=\(.ideaVerdict) (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-email)
        FROM="$2"
        SUBJECT="$3"
        PREVIEW="${4:-}"
        EMAIL_ID="${5:-}"

        if [[ -z "$FROM" || -z "$SUBJECT" ]]; then
            echo "Error: from and subject required"
            echo "Usage: corkboard add-email <from> <subject> [preview] [email_id]"
            exit 1
        fi

        JSON=$(jq -n \
            --arg type "email" \
            --arg title "$SUBJECT" \
            --arg content "$PREVIEW" \
            --arg emailFrom "$FROM" \
            --arg emailId "$EMAIL_ID" \
            '{type: $type, title: $title, content: $content, emailFrom: $emailFrom, emailId: $emailId, priority: 2}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [email] from \(.emailFrom) (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-tracking)
        NUMBER="$2"
        CARRIER="$3"
        STATUS="${4:-unknown}"
        ETA="${5:-}"
        URL="${6:-}"

        if [[ -z "$NUMBER" || -z "$CARRIER" ]]; then
            echo "Error: tracking number and carrier required"
            echo "Usage: corkboard add-tracking <number> <carrier> [status] [eta] [url]"
            exit 1
        fi

        TITLE="$CARRIER $NUMBER"

        JSON=$(jq -n \
            --arg type "tracking" \
            --arg title "$TITLE" \
            --arg trackingNumber "$NUMBER" \
            --arg trackingCarrier "$CARRIER" \
            --arg trackingStatus "$STATUS" \
            '{type: $type, title: $title, trackingNumber: $trackingNumber, trackingCarrier: $trackingCarrier, trackingStatus: $trackingStatus}')

        if [[ -n "$ETA" ]]; then
            JSON=$(echo "$JSON" | jq --arg eta "$ETA" '. + {trackingEta: $eta}')
        fi
        if [[ -n "$URL" ]]; then
            JSON=$(echo "$JSON" | jq --arg url "$URL" '. + {trackingUrl: $url}')
        fi

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [tracking] status=\(.trackingStatus) (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-article)
        TITLE="$2"
        URL="$3"
        SOURCE="$4"
        TLDR="$5"
        BULLETS_JSON="${6:-[]}"
        TAGS_JSON="${7:-[]}"

        if [[ -z "$TITLE" || -z "$URL" || -z "$SOURCE" || -z "$TLDR" ]]; then
            echo "Error: title, url, source, and tldr required"
            echo "Usage: corkboard add-article <title> <url> <source> <tldr> [bullets_json] [tags_json]"
            exit 1
        fi

        JSON=$(jq -n \
            --arg type "article" \
            --arg title "$TITLE" \
            --arg url "$URL" \
            --arg source "$SOURCE" \
            --arg tldr "$TLDR" \
            --argjson bullets "$BULLETS_JSON" \
            --argjson tags "$TAGS_JSON" \
            '{type: $type, title: $title, url: $url, articleData: {url: $url, source: $source, tldr: $tldr, bullets: $bullets, tags: $tags}}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [article] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-twitter)
        TITLE="$2"
        CONTENT="$3"
        URL="${4:-}"

        if [[ -z "$TITLE" || -z "$CONTENT" ]]; then
            echo "Error: title and content required"
            echo "Usage: corkboard add-twitter <title> <content> [url]"
            exit 1
        fi

        JSON=$(jq -n \
            --arg type "twitter" \
            --arg title "$TITLE" \
            --arg content "$CONTENT" \
            --arg url "$URL" \
            '{type: $type, title: $title, content: $content, url: $url}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [twitter] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-reddit)
        TITLE="$2"
        CONTENT="$3"
        URL="${4:-}"

        if [[ -z "$TITLE" || -z "$CONTENT" ]]; then
            echo "Error: title and content required"
            echo "Usage: corkboard add-reddit <title> <content> [url]"
            exit 1
        fi

        JSON=$(jq -n \
            --arg type "reddit" \
            --arg title "$TITLE" \
            --arg content "$CONTENT" \
            --arg url "$URL" \
            '{type: $type, title: $title, content: $content, url: $url}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [reddit] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-youtube)
        URL="$2"

        if [[ -z "$URL" ]]; then
            echo "Error: YouTube URL required"
            echo "Usage: corkboard add-youtube <youtube-url>"
            exit 1
        fi

        # Extract video ID from various YouTube URL formats
        VIDEO_ID=""
        if [[ "$URL" =~ youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11}) ]]; then
            VIDEO_ID="${BASH_REMATCH[1]}"
        elif [[ "$URL" =~ youtu\.be/([a-zA-Z0-9_-]{11}) ]]; then
            VIDEO_ID="${BASH_REMATCH[1]}"
        elif [[ "$URL" =~ youtube\.com/shorts/([a-zA-Z0-9_-]{11}) ]]; then
            VIDEO_ID="${BASH_REMATCH[1]}"
        elif [[ "$URL" =~ youtube\.com/live/([a-zA-Z0-9_-]{11}) ]]; then
            VIDEO_ID="${BASH_REMATCH[1]}"
        fi

        if [[ -z "$VIDEO_ID" ]]; then
            echo "Error: Could not extract video ID from URL"
            exit 1
        fi

        CANONICAL_URL="https://www.youtube.com/watch?v=$VIDEO_ID"
        EMBED_URL="https://www.youtube.com/embed/$VIDEO_ID"
        THUMB_URL="https://i.ytimg.com/vi/$VIDEO_ID/hqdefault.jpg"

        # Try yt-dlp for rich metadata
        TITLE=""
        CHANNEL=""
        DESCRIPTION=""
        DURATION=""
        PUBLISHED=""

        if command -v yt-dlp &>/dev/null; then
            YT_JSON=$(yt-dlp --dump-single-json --skip-download --no-warnings "$CANONICAL_URL" 2>/dev/null || echo "")
            if [[ -n "$YT_JSON" ]]; then
                TITLE=$(echo "$YT_JSON" | jq -r '.title // empty')
                CHANNEL=$(echo "$YT_JSON" | jq -r '(.channel // .uploader) // empty')
                DESCRIPTION=$(echo "$YT_JSON" | jq -r '.description // empty' | head -c 500)
                THUMB_URL=$(echo "$YT_JSON" | jq -r '.thumbnail // empty')
                DURATION_SECS=$(echo "$YT_JSON" | jq -r '.duration // empty')
                UPLOAD_DATE=$(echo "$YT_JSON" | jq -r '.upload_date // empty')

                if [[ -n "$DURATION_SECS" && "$DURATION_SECS" != "null" ]]; then
                    HOURS=$((DURATION_SECS / 3600))
                    MINS=$(( (DURATION_SECS % 3600) / 60 ))
                    SECS=$((DURATION_SECS % 60))
                    if [[ $HOURS -gt 0 ]]; then
                        DURATION=$(printf "%d:%02d:%02d" "$HOURS" "$MINS" "$SECS")
                    else
                        DURATION=$(printf "%d:%02d" "$MINS" "$SECS")
                    fi
                fi

                if [[ -n "$UPLOAD_DATE" && "$UPLOAD_DATE" != "null" && ${#UPLOAD_DATE} -eq 8 ]]; then
                    PUBLISHED="${UPLOAD_DATE:0:4}-${UPLOAD_DATE:4:2}-${UPLOAD_DATE:6:2}T00:00:00Z"
                fi
            fi
        fi

        # Fallback to oEmbed if yt-dlp didn't work
        if [[ -z "$TITLE" ]]; then
            OEMBED=$(curl -s "https://www.youtube.com/oembed?url=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$CANONICAL_URL'))" 2>/dev/null || echo "$CANONICAL_URL")&format=json" 2>/dev/null || echo "")
            if [[ -n "$OEMBED" ]]; then
                TITLE=$(echo "$OEMBED" | jq -r '.title // empty')
                CHANNEL=$(echo "$OEMBED" | jq -r '.author_name // empty')
                OE_THUMB=$(echo "$OEMBED" | jq -r '.thumbnail_url // empty')
                [[ -n "$OE_THUMB" ]] && THUMB_URL="$OE_THUMB"
            fi
        fi

        [[ -z "$TITLE" ]] && TITLE="YouTube Video"
        [[ -z "$THUMB_URL" || "$THUMB_URL" == "null" ]] && THUMB_URL="https://i.ytimg.com/vi/$VIDEO_ID/hqdefault.jpg"

        # Build youtubeData object
        YT_DATA=$(jq -n \
            --arg videoId "$VIDEO_ID" \
            --arg thumbnailUrl "$THUMB_URL" \
            --arg embedUrl "$EMBED_URL" \
            --arg sourceUrl "$CANONICAL_URL" \
            '{videoId: $videoId, thumbnailUrl: $thumbnailUrl, embedUrl: $embedUrl, sourceUrl: $sourceUrl}')

        [[ -n "$CHANNEL" ]] && YT_DATA=$(echo "$YT_DATA" | jq --arg v "$CHANNEL" '. + {channelTitle: $v}')
        [[ -n "$DESCRIPTION" ]] && YT_DATA=$(echo "$YT_DATA" | jq --arg v "$DESCRIPTION" '. + {description: $v}')
        [[ -n "$DURATION" ]] && YT_DATA=$(echo "$YT_DATA" | jq --arg v "$DURATION" '. + {duration: $v}')
        [[ -n "$PUBLISHED" ]] && YT_DATA=$(echo "$YT_DATA" | jq --arg v "$PUBLISHED" '. + {publishedAt: $v}')

        JSON=$(jq -n \
            --arg type "youtube" \
            --arg title "$TITLE" \
            --arg url "$CANONICAL_URL" \
            --argjson youtubeData "$YT_DATA" \
            '{type: $type, title: $title, url: $url, youtubeData: $youtubeData}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [youtube] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-opportunity)
        TITLE="$2"
        CONTENT="${3:-}"
        PRIORITY="${4:-2}"

        if [[ -z "$TITLE" ]]; then
            echo "Error: title required"
            echo "Usage: corkboard add-opportunity <title> [content] [priority]"
            exit 1
        fi

        JSON=$(jq -n \
            --arg type "opportunity" \
            --arg title "$TITLE" \
            --arg content "$CONTENT" \
            --argjson priority "$PRIORITY" \
            '{type: $type, title: $title, content: $content, priority: $priority}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [opportunity] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    add-briefing)
        TITLE="$2"
        CONTENT="${3:-}"

        if [[ -z "$TITLE" ]]; then
            echo "Error: title required"
            echo "Usage: corkboard add-briefing <title> <content>"
            exit 1
        fi

        JSON=$(jq -n \
            --arg type "briefing" \
            --arg title "$TITLE" \
            --arg content "$CONTENT" \
            '{type: $type, title: $title, content: $content}')

        RESULT=$(curl -s -X POST "$API_URL" \
            "${AUTH_HEADER[@]}" \
            -H "Content-Type: application/json" \
            -d "$JSON")

        echo "$RESULT" | jq -r '"Created: \(.title) [briefing] (id: \(.id))"' 2>/dev/null || echo "$RESULT"
        ;;

    help|--help|-h)
        show_help
        ;;

    *)
        show_help
        exit 1
        ;;
esac
