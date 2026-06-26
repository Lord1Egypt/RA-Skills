#!/bin/bash
# create_ppt.sh — Automate NotebookLM to create a presentation from text content
# Optional env vars:
#   AUTO_PPT_YOUTUBE_QUERY   YouTube search query; if set, script will collect 2–N video URLs and add them as website sources first
#   AUTO_PPT_MAX_YOUTUBE     Max number of YouTube URLs to add (default 3)
#   AUTO_PPT_CUSTOM_PROMPT   Customize presentation prompt/style text
# Usage: bash create_ppt.sh "content text" ["output filename"]

set -euo pipefail

CONTENT="$1"
OUTPUT_NAME="${2:-PPT_$(date +%Y%m%d_%H%M).pdf}"
OUTPUT_PATH="$HOME/Desktop/$OUTPUT_NAME"
CLI="${OPENCLAW_CLI:-openclaw browser}"
YOUTUBE_QUERY="${AUTO_PPT_YOUTUBE_QUERY:-}"
MAX_YOUTUBE="${AUTO_PPT_MAX_YOUTUBE:-3}"
CUSTOM_PROMPT="${AUTO_PPT_CUSTOM_PROMPT:-STYLE: Whiteboard sketch/doodle style
- Background: light gray paper texture with wooden frame border
- Hand-drawn/sketch illustrations in black ink lines
- Blue and red accent colors
- All Chinese text must be perfectly rendered, clear and readable
- Layout should be clean and professional like a real presentation slide

Design a beautiful presentation slide with the following content. Arrange text and illustrations naturally for the best visual effect.}"
TMP_DIR="${TMPDIR:-/tmp}/auto-ppt"
mkdir -p "$TMP_DIR"
YT_LINKS_FILE="$TMP_DIR/youtube-links.txt"

if [ -z "$CONTENT" ]; then
  echo "ERROR: No content provided"
  echo "Usage: bash create_ppt.sh \"content text\" [\"output_filename.pdf\"]"
  exit 1
fi

wait_and_snap() {
  local wait_sec="${1:-3}"
  sleep "$wait_sec"
  $CLI snapshot 2>/dev/null
}

find_ref() {
  local snap="$1"
  local pattern="$2"
  echo "$snap" | grep -i "$pattern" | grep -oE 'ref=e[0-9]+' | tail -1 | sed 's/ref=//'
}

find_button_ref() {
  local snap="$1"
  local pattern="$2"
  echo "$snap" | grep -i "button.*$pattern" | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//'
}

click_ref() {
  local ref="$1"
  local label="$2"
  if [ -z "$ref" ]; then
    echo "ERROR: Could not find element: $label"
    return 1
  fi
  echo "  Clicking: $label ($ref)"
  $CLI click "$ref" 2>/dev/null
}

find_button_by_patterns() {
  local snap="$1"
  shift
  local pattern
  for pattern in "$@"; do
    local ref
    ref=$(find_button_ref "$snap" "$pattern" 2>/dev/null || true)
    if [ -n "$ref" ]; then
      printf '%s' "$ref"
      return 0
    fi
  done
  return 1
}

is_login_prompt() {
  local snap="$1"
  if echo "$snap" | grep -qi "sign\\.in\|登录\|login"; then
    if ! echo "$snap" | grep -qi "NotebookLM\|Notebook\|Studio"; then
      return 0
    fi
  fi
  return 1
}

find_presentation_ref() {
  local snap="$1"
  local ref
  local patterns=(
    'button.*个来源.*前'
    'button.*source.*ago'
    'button.*个来源'
    'button.*source'
    'generic.*cursor=pointer.*个来源'
    'generic.*cursor=pointer.*source'
  )
  for pattern in "${patterns[@]}"; do
    ref=$(echo "$snap" | grep -i "$pattern" | grep -v "disabled\|正在生成\|generating" | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//') || true
    if [ -n "$ref" ]; then
      printf '%s' "$ref"
      return 0
    fi
  done
  return 1
}

extract_youtube_links() {
  if [ -z "$YOUTUBE_QUERY" ]; then
    : > "$YT_LINKS_FILE"
    return 0
  fi

  echo ""
  echo "=== Step YT/1: Searching YouTube for sources ==="
  local encoded_query snap
  encoded_query=$(python3 - <<'PY' "$YOUTUBE_QUERY"
import sys, urllib.parse
print(urllib.parse.quote(sys.argv[1]))
PY
)
  $CLI open "https://www.youtube.com/results?search_query=${encoded_query}" 2>/dev/null
  snap=$(wait_and_snap 6)

  # Path A: direct DOM extraction
  $CLI evaluate --fn "() => { const anchors = Array.from(document.querySelectorAll('a[href*="/watch?v="]')); const urls = anchors.map(a => a.href).filter(Boolean); const uniq = [...new Set(urls)].filter(u => /^https:\/\/www\.youtube\.com\/watch\?v=/.test(u)); return uniq.slice(0, ${MAX_YOUTUBE}).join('\\n'); }" 2>/dev/null | grep -Eo 'https://www\.youtube\.com/watch\?[^[:space:]"'\''<>]+' | head -n "${MAX_YOUTUBE}" > "$YT_LINKS_FILE" || true

  # Path B: snapshot text fallback
  if [ ! -s "$YT_LINKS_FILE" ]; then
    printf '%s\n' "$snap" | grep -Eo 'https://www\.youtube\.com/watch\?[^[:space:]"'\''<>]+' | head -n "${MAX_YOUTUBE}" > "$YT_LINKS_FILE" || true
  fi

  # Path C: href fragments fallback
  if [ ! -s "$YT_LINKS_FILE" ]; then
    printf '%s\n' "$snap" | grep -Eo '/watch\?v=[A-Za-z0-9_-]+' | sed 's#^#https://www.youtube.com#' | head -n "${MAX_YOUTUBE}" > "$YT_LINKS_FILE" || true
  fi

  # Normalize escaped newlines that may come back from CLI output
  if [ -s "$YT_LINKS_FILE" ]; then
    python3 - <<'PY' "$YT_LINKS_FILE"
from pathlib import Path
import sys
p = Path(sys.argv[1])
text = p.read_text()
text = text.replace('\\n', '\n')
p.write_text(text)
PY
  fi

  # Final de-dup in case multiple selectors resolve to the same video
  if [ -s "$YT_LINKS_FILE" ]; then
    python3 - <<'PY' "$YT_LINKS_FILE"
from pathlib import Path
import sys
p = Path(sys.argv[1])
seen = set()
out = []
for line in p.read_text().splitlines():
    u = line.strip()
    if not u or u in seen:
        continue
    seen.add(u)
    out.append(u)
p.write_text('\\n'.join(out) + ('\\n' if out else ''))
PY
  fi

  if [ ! -s "$YT_LINKS_FILE" ]; then
    echo "  WARNING: Could not auto-extract YouTube links; continuing without video sources"
    : > "$YT_LINKS_FILE"
    return 0
  fi

  echo "  Collected YouTube links:"
  sed 's/^/    - /' "$YT_LINKS_FILE"
}

add_website_source() {
  local url="$1"
  local snap ref
  echo "  Adding website source: $url"

  snap=$(wait_and_snap 2)

  # If add-source dialog is already open, go straight to Website.
  ref=$(find_button_by_patterns "$snap" 'button "网站"' '网站\|[Ww]ebsite\|[Ll]ink' '网址\|[Uu][Rr][Ll]') || true
  if [ -z "$ref" ]; then
    ref=$(find_button_by_patterns "$snap" '添加来源\|[Aa]dd source' '添加\|[Aa]dd') || true
    if [ -n "$ref" ]; then
      click_ref "$ref" "Add source"
      snap=$(wait_and_snap 3)
      ref=$(find_button_by_patterns "$snap" 'button "网站"' '网站\|[Ww]ebsite\|[Ll]ink' '网址\|[Uu][Rr][Ll]') || true
    fi
  fi

  click_ref "$ref" "Website source option"
  snap=$(wait_and_snap 3)

  ref=$(find_ref "$snap" 'textbox.*https\|textbox.*网址\|textbox.*URL\|textbox.*查询\|textbox')
  if [ -z "$ref" ]; then
    echo "ERROR: Could not find website URL input"
    return 1
  fi
  $CLI type "$ref" "$url" 2>/dev/null
  snap=$(wait_and_snap 1)

  ref=$(find_button_by_patterns "$snap" '提交\|插入\|[Ii]nsert\|添加' '继续\|[Aa]dd\|[Ss]ubmit') || true
  click_ref "$ref" "Insert website source"
  wait_and_snap 5 >/dev/null || true
}

apply_custom_prompt() {
  if [ -z "$CUSTOM_PROMPT" ]; then
    return 0
  fi

  echo ""
  echo "=== Step 5.5/7: Setting custom presentation prompt ==="
  local snap ref
  snap=$(wait_and_snap 2)

  ref=$(find_button_by_patterns "$snap" '自定义演示文稿\|[Cc]ustomize.*presentation' '自定义\|[Cc]ustomize') || true
  if [ -z "$ref" ]; then
    ref=$(find_ref "$snap" 'textbox.*自定义\|textbox.*演示文稿\|textbox.*presentation\|textbox.*slides') || true
  fi

  if [ -n "$ref" ]; then
    if echo "$ref" | grep -q '^e'; then
      click_ref "$ref" "Customize presentation"
      snap=$(wait_and_snap 2)
      ref=$(find_ref "$snap" 'textbox.*自定义\|textbox.*演示\|textbox.*presentation\|textbox') || true
    fi
  fi

  if [ -z "$ref" ]; then
    echo "  WARNING: Could not find custom-prompt input; continuing with default NotebookLM generation"
    return 0
  fi

  echo "  Typing custom prompt (${#CUSTOM_PROMPT} chars)..."
  $CLI type "$ref" "$CUSTOM_PROMPT" 2>/dev/null || true
  wait_and_snap 1 >/dev/null || true
}

echo "============================================"
echo "  NotebookLM PPT Generator"
echo "============================================"
echo "Output: $OUTPUT_PATH"
echo ""

extract_youtube_links

echo "=== Step 1/7: Opening NotebookLM ==="
$CLI open "https://notebooklm.google.com/" 2>/dev/null
SNAP=$(wait_and_snap 5)

if is_login_prompt "$SNAP"; then
  echo "Detected login prompt. Waiting 6s for the session to refresh..."
  SNAP=$(wait_and_snap 6)
  if is_login_prompt "$SNAP"; then
    echo "WARNING: NotebookLM still shows a sign-in screen. Please sign in manually, then re-run this script."
    exit 1
  fi
  echo "Login prompt cleared."
fi
echo "  NotebookLM loaded"

echo ""
echo "=== Step 2/7: Creating new notebook ==="
REF=$(find_button_ref "$SNAP" "新建笔记本\|[Nn]ew notebook")
if [ -z "$REF" ]; then
  REF=$(find_button_ref "$SNAP" "新建\|[Cc]reate.*new")
fi
click_ref "$REF" "New notebook button"
SNAP=$(wait_and_snap 6)
echo "  New notebook created"

if [ -s "$YT_LINKS_FILE" ]; then
  echo ""
  echo "=== Step 2.5/7: Adding YouTube website sources ==="
  while IFS= read -r url; do
    [ -n "$url" ] || continue
    add_website_source "$url"
    SNAP=$(wait_and_snap 3)
  done < "$YT_LINKS_FILE"
  echo "  YouTube sources added"
fi

echo ""
echo "=== Step 3/7: Finding 'Copied text' option ==="
REF=$(find_button_by_patterns "$SNAP" \
  '复制的文字\|[Cc]opied text\|[Pp]aste text' \
  'content_paste\|粘贴')

if [ -z "$REF" ]; then
  echo "  Dialog not auto-opened, clicking Add source..."
  ADD_REF=$(find_button_ref "$SNAP" "添加来源\|[Aa]dd source")
  if [ -z "$ADD_REF" ]; then
    ADD_REF=$(find_button_ref "$SNAP" "add\|添加")
  fi
  if [ -n "$ADD_REF" ]; then
    click_ref "$ADD_REF" "Add source"
    SNAP=$(wait_and_snap 4)
    REF=$(find_button_by_patterns "$SNAP" \
      '复制的文字\|[Cc]opied text\|[Pp]aste text' \
      'content_paste\|粘贴')
  fi
fi

click_ref "$REF" "Copied text option"
SNAP=$(wait_and_snap 3)
echo "  Text source dialog opened"

echo ""
echo "=== Step 4/7: Pasting content ==="
REF=$(find_ref "$SNAP" 'textbox.*粘贴\|textbox.*[Pp]aste\|textbox.*在此处')
if [ -z "$REF" ]; then
  REF=$(find_ref "$SNAP" 'textbox.*active\|textbox.*placeholder')
fi
if [ -z "$REF" ]; then
  REF=$(find_ref "$SNAP" "textbox\|textarea")
fi
if [ -z "$REF" ]; then
  echo "ERROR: Could not find text input area"
  echo "SNAPSHOT:"
  echo "$SNAP" | head -30
  exit 1
fi
echo "  Found text input: $REF"
echo "  Typing content (${#CONTENT} chars)..."
$CLI type "$REF" "$CONTENT" 2>/dev/null
SNAP=$(wait_and_snap 2)

REF=$(find_button_ref "$SNAP" "插入\|[Ii]nsert\|[Ss]ubmit")
if [ -z "$REF" ]; then
  REF=$(find_button_ref "$SNAP" "确[定认]\|[Aa]dd")
fi
click_ref "$REF" "Insert button"
SNAP=$(wait_and_snap 5)
echo "  Content inserted"

apply_custom_prompt
SNAP=$(wait_and_snap 2)

echo ""
echo "=== Step 5/7: Generating presentation ==="
REF=$(find_button_by_patterns "$SNAP" \
  '演示文稿\|[Pp]resentation' \
  '[Ss]lides\|幻灯片')
if [ -z "$REF" ]; then
  SNAP=$(wait_and_snap 5)
  REF=$(find_button_by_patterns "$SNAP" \
    '演示文稿\|[Pp]resentation' \
    '[Ss]lides\|幻灯片')
fi
click_ref "$REF" "Generate presentation"
echo "  Generating slides... (this may take 30-60 seconds)"

READY=false
for i in $(seq 1 90); do
  sleep 10
  SNAP=$($CLI snapshot 2>/dev/null)
  if echo "$SNAP" | grep -qi "已准备就绪\|幻灯片.*已准备"; then
    READY=true
    echo "  Presentation ready! (detected: 已准备就绪)"
    break
  fi
  if echo "$SNAP" | grep -qi "button.*个来源.*前"; then
    READY=true
    echo "  Presentation ready! (detected: entry with timestamp)"
    break
  fi
  if echo "$SNAP" | grep -qi "正在生成\|generating"; then
    echo "  Still generating... ($((i*10))s elapsed)"
  else
    echo "  Waiting... ($((i*10))s elapsed)"
  fi
done

if [ "$READY" = false ]; then
  echo "WARNING: Timed out after 900s. Taking final snapshot..."
  SNAP=$($CLI snapshot 2>/dev/null)
fi

echo ""
echo "=== Step 6/7: Opening presentation ==="
REF=$(find_presentation_ref "$SNAP")
if [ -z "$REF" ]; then
  echo "WARNING: Could not locate presentation. Capturing extra snapshot..."
  sleep 8
  SNAP=$($CLI snapshot 2>/dev/null)
  REF=$(find_presentation_ref "$SNAP")
fi

if [ -z "$REF" ]; then
  echo "ERROR: Presentation entry still missing after retries."
  echo "Last snapshot snippets:"
  echo "$SNAP" | grep -i "presentation\|source\|Studio" | head -20
  exit 1
fi

click_ref "$REF" "Open presentation"
SNAP=$(wait_and_snap 5)
echo "  Presentation opened"

echo ""
echo "=== Step 7/7: Downloading PDF ==="
REF=$(find_button_by_patterns "$SNAP" \
  '更多选项\|more_horiz' \
  '菜单.*更多\|[Mm]ore.*options')
if [ -z "$REF" ]; then
  REF=$(find_button_ref "$SNAP" "[Mm]ore.*option\|更多")
fi
click_ref "$REF" "More options menu"
SNAP=$(wait_and_snap 3)

REF=$(echo "$SNAP" | grep -i 'menuitem.*PDF' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
if [ -z "$REF" ]; then
  REF=$(find_button_by_patterns "$SNAP" \
    '下载 PDF\|[Dd]ownload.*PDF\|PDF.*文档' \
    '保存.*PDF')
fi

if [ -z "$REF" ]; then
  echo "ERROR: Could not find PDF download option"
  echo "SNAPSHOT MENU:"
  echo "$SNAP" | grep -i "menu\|PDF\|下载\|download" | head -20
  echo "  Please download manually from the open presentation"
  exit 1
fi

echo "  Downloading PDF to $OUTPUT_PATH ..."
$CLI download "$REF" "$OUTPUT_PATH" --timeout-ms 30000 2>/dev/null
sleep 3

if [ -f "$OUTPUT_PATH" ]; then
  SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
  echo ""
  echo "============================================"
  echo "  SUCCESS!"
  echo "  File: $OUTPUT_PATH"
  echo "  Size: $SIZE"
  echo "============================================"
else
  echo ""
  echo "WARNING: PDF file not found at $OUTPUT_PATH"
  echo "  The download may still be in progress."
  echo "  Check ~/Desktop/ for the file."
fi
