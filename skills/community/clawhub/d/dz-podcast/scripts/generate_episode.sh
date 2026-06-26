#!/bin/bash
# Upload podcast episode to S3 and update RSS feed
# Usage: ./generate_episode.sh <date> <ep-number> <title> <description> <mp3-file>
# Example: ./generate_episode.sh 2026-03-04 EP006 "标题" "描述" /tmp/2026-03-04-ep006.mp3

set -e

DATE="$1"
EP="$2"
TITLE="$3"
DESC="$4"
MP3_FILE="$5"

BUCKET="${S3_BUCKET:-my-podcast-bucket}"
S3_BASE="${PODCAST_DOMAIN:-https://my-podcast-bucket.s3.amazonaws.com}"
EP_LOWER=$(echo "$EP" | tr '[:upper:]' '[:lower:]')
S3_KEY="episodes/${DATE}-${EP_LOWER}.mp3"

if [ ! -f "$MP3_FILE" ]; then
  echo "❌ MP3 file not found: $MP3_FILE"
  exit 1
fi

FILESIZE=$(stat -c%s "$MP3_FILE")

# Get actual duration via ffprobe
DURATION_SEC=$(ffprobe -i "$MP3_FILE" -show_entries format=duration -v quiet -of csv="p=0" | cut -d. -f1)
DURATION_MIN=$((DURATION_SEC / 60))
DURATION_REM=$((DURATION_SEC % 60))
DURATION=$(printf "%02d:%02d" $DURATION_MIN $DURATION_REM)

echo "📊 File: ${FILESIZE} bytes, Duration: ${DURATION}"

# 1. Upload MP3
echo "☁️ Uploading ${S3_KEY}..."
aws s3 cp "$MP3_FILE" "s3://${BUCKET}/${S3_KEY}" --content-type "audio/mpeg"

# 2. Download current RSS
aws s3 cp "s3://${BUCKET}/feed.xml" /tmp/feed_current.xml 2>/dev/null

# 3. Build new item
PUBDATE=$(date -d "${DATE}" -u '+%a, %d %b %Y 08:00:00 +0800')
BUILDDATE=$(date -u '+%a, %d %b %Y %H:%M:%S +0000')
NEW_ITEM="<item>\n      <title>${TITLE}</title>\n      <description>${DESC}</description>\n      <enclosure url=\"${S3_BASE}/${S3_KEY}\" length=\"${FILESIZE}\" type=\"audio/mpeg\"/>\n      <pubDate>${PUBDATE}</pubDate>\n      <itunes:duration>${DURATION}</itunes:duration>\n      <itunes:summary>${DESC}</itunes:summary>\n      <itunes:image href=\"${S3_BASE}/cover.jpg\"/>\n      <guid isPermaLink=\"false\">podcast-${DATE}-${EP_LOWER}</guid>\n    </item>"

# 4. Insert new item after <lastBuildDate> line and update build date
sed -i "s|<lastBuildDate>.*</lastBuildDate>|<lastBuildDate>${BUILDDATE}</lastBuildDate>\n\n    ${NEW_ITEM}|" /tmp/feed_current.xml

# 5. Upload updated RSS
aws s3 cp /tmp/feed_current.xml "s3://${BUCKET}/feed.xml" --content-type "application/rss+xml"

echo "✅ Published: ${TITLE}"
echo "🔗 ${S3_BASE}/${S3_KEY}"
echo "📻 ${S3_BASE}/feed.xml"
