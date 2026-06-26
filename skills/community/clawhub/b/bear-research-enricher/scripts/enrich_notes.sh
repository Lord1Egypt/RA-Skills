#!/usr/bin/env bash
# enrich_notes.sh — Batch-enrich Bear notes tagged 「待整理」 with thematic GIFs
set -euo pipefail

TOKEN_FILE="${GRIZZLY_TOKEN_FILE:-$HOME/.config/grizzly/token}"
GIF_API="https://api.giphy.com/v1/gifs/search"
GIF_KEY="${GIPHY_API_KEY:-dc6zaTOxFJmzCC}"  # public beta key
DELAY=1  # seconds between GIF API calls

if ! command -v grizzly &>/dev/null; then
  echo "ERROR: grizzly not found. Install: go install github.com/tylerwince/grizzly/cmd/grizzly@latest"
  exit 1
fi

if [ ! -f "$TOKEN_FILE" ]; then
  echo "ERROR: Bear token not found at $TOKEN_FILE"
  exit 1
fi

# Fetch notes with 待整理 tag
echo "Fetching notes tagged 待整理..."
NOTES_JSON=$(grizzly open-tag --name "待整理" --enable-callback --json --token-file "$TOKEN_FILE" 2>/dev/null)

if [ -z "$NOTES_JSON" ] || echo "$NOTES_JSON" | grep -q '"notes"\s*:\s*\[\]'; then
  echo "No notes found with tag 待整理."
  exit 0
fi

# Extract note IDs and titles
NOTE_IDS=($(echo "$NOTES_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for n in data.get('notes', []):
    print(n.get('identifier', n.get('id', '')))
" 2>/dev/null))

NOTE_TITLES=($(echo "$NOTES_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for n in data.get('notes', []):
    print(n.get('title', 'Untitled'))
" 2>/dev/null))

if [ ${#NOTE_IDS[@]} -eq 0 ]; then
  echo "No notes found with tag 待整理."
  exit 0
fi

echo "Found ${#NOTE_IDS[@]} note(s) to enrich."

for i in "${!NOTE_IDS[@]}"; do
  NOTE_ID="${NOTE_IDS[$i]}"
  TITLE="${NOTE_TITLES[$i]}"
  echo ""
  echo "=== Processing: $TITLE (id=$NOTE_ID) ==="

  # Read note content
  NOTE_JSON=$(grizzly open-note --id "$NOTE_ID" --enable-callback --json --token-file "$TOKEN_FILE" 2>/dev/null)
  NOTE_TEXT=$(echo "$NOTE_JSON" | python3 -c "
import sys, json
data = json.load(sys.stdin)
note = data.get('note', data)
print(note.get('text', ''))
" 2>/dev/null)

  # Extract keywords from title + first 200 chars
  KEYWORDS=$(echo -e "$TITLE\n$NOTE_TEXT" | head -c 200 | python3 -c "
import sys, re
text = sys.stdin.read()
# Simple keyword extraction: split on common delimiters, pick top 3 non-stopwords
stop = {'the','a','an','is','are','was','were','be','been','being','have','has','had',
        'do','does','did','will','would','could','should','may','might','shall','can',
        'to','of','in','for','on','with','at','by','from','as','into','through','during',
        'before','after','above','below','between','out','off','over','under','again',
        'further','then','once','and','but','or','nor','not','so','yet','both','either',
        'neither','each','every','all','any','few','more','most','other','some','such',
        'no','only','own','same','than','too','very','just','because','if','when','where',
        'how','what','which','who','whom','this','that','these','those','i','me','my',
        'we','our','you','your','he','him','his','she','her','it','its','they','them',
        'their','的','了','在','是','我','有','和','就','不','人','都','一','上','也',
        '很','到','说','要','去','你','会','着','没有','看','好','自己','这'}
words = re.findall(r'[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}', text.lower())
keywords = [w for w in words if w not in stop]
seen = set()
unique = []
for w in keywords:
    if w not in seen:
        seen.add(w)
        unique.append(w)
    if len(unique) >= 3:
        break
print(' '.join(unique))
" 2>/dev/null)

  if [ -z "$KEYWORDS" ]; then
    echo "  No keywords extracted, skipping note."
    continue
  fi

  echo "  Keywords: $KEYWORDS"

  # Search GIFs per keyword and build insert block
  INSERT_BLOCK=""
  for KW in $KEYWORDS; do
    echo "  Searching GIF for: $KW"
    ENCODED_KW=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$KW'))")
    GIF_RESULT=$(curl -s "${GIF_API}?api_key=${GIF_KEY}&q=${ENCODED_KW}&limit=3" 2>/dev/null)
    GIF_URL=$(echo "$GIF_RESULT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    gifs = data.get('data', [])
    if gifs:
        print(gifs[0].get('images', {}).get('original', {}).get('url', ''))
except: pass
" 2>/dev/null)

    if [ -n "$GIF_URL" ]; then
      INSERT_BLOCK="${INSERT_BLOCK}
![${KW}](${GIF_URL})"
      echo "  ✓ Found GIF for $KW"
    else
      echo "  ✗ No GIF for $KW, skipping"
    fi

    sleep "$DELAY"
  done

  # Insert GIFs into note
  if [ -n "$INSERT_BLOCK" ]; then
    echo -e "\n---\n${INSERT_BLOCK}" | grizzly add-text --id "$NOTE_ID" --mode append --token-file "$TOKEN_FILE"
    echo "  ✓ GIFs inserted into note"
  else
    echo "  No GIFs found for any keyword, skipping insert."
  fi

  # Retag: add 已整理, remove 待整理
  open "bear://x-callback-url/add-tag?id=${NOTE_ID}&name=已整理" 2>/dev/null || true
  open "bear://x-callback-url/remove-tag?id=${NOTE_ID}&name=待整理" 2>/dev/null || true
  echo "  ✓ Retagged: 待整理 → 已整理"
done

echo ""
echo "=== Done. All notes processed. ==="
