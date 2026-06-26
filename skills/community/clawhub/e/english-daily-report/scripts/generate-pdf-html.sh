#!/bin/bash
# Generate English Daily Report PDF
# Usage: generate-pdf-html.sh "DATE" "TYPE" "ENGLISH_TITLE" "ENGLISH_CONTENT" "CHINESE_TRANSLATION" "WORD1:MEANING1" "WORD2:MEANING2" ...
#   TYPE: "real" for real news, "study" for study material

set -euo pipefail

# Get workspace directory (portable across users and OS)
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
cd "$WORKSPACE_DIR"

# Parse arguments
DATE="${1:-$(date +%Y-%m-%d)}"
CONTENT_TYPE="${2:-study}"  # "real" or "study"
ENGLISH_TITLE="${3:-Daily Report}"
ENGLISH_CONTENT="${4:-No content provided}"
CHINESE_TRANSLATION="${5:-无内容}"
shift 5 || true
VOCAB_WORDS=("$@")

# Output paths (portable)
PDF_FILE="${WORKSPACE_DIR}/uploads/english-daily-${DATE}.pdf"
HTML_FILE="${WORKSPACE_DIR}/uploads/report-temp.html"

# Function to escape HTML special characters
escape_html() {
    local text="$1"
    text="${text//&/&amp;}"
    text="${text//</&lt;}"
    text="${text//>/&gt;}"
    text="${text//\"/&quot;}"
    text="${text//\'/&#39;}"
    printf '%s' "$text"
}

# Escape all user-provided content to prevent XSS/injection
ENGLISH_TITLE_ESCAPED=$(escape_html "$ENGLISH_TITLE")
ENGLISH_CONTENT_ESCAPED=$(escape_html "$ENGLISH_CONTENT")
CHINESE_TRANSLATION_ESCAPED=$(escape_html "$CHINESE_TRANSLATION")

# Build content type badge and warning (hardcoded, safe)
if [[ "$CONTENT_TYPE" == "real" ]]; then
    TYPE_BADGE="【真实新闻 · Real News】"
    TYPE_WARNING=""
    TYPE_BG="#667eea"
    TYPE_BG_END="#764ba2"
else
    TYPE_BADGE="【学习材料 · Study Material · 非真实新闻】"
    TYPE_WARNING="⚠️ 本文为英语学习材料，基于真实时事趋势编写，非真实新闻报道"
    TYPE_BG="#f093fb"
    TYPE_BG_END="#f5576c"
fi

# Escape static content for consistency (defense in depth)
TYPE_BADGE_ESCAPED=$(escape_html "$TYPE_BADGE")
TYPE_WARNING_ESCAPED=$(escape_html "$TYPE_WARNING")
DATE_ESCAPED=$(escape_html "$DATE")

# Build vocabulary HTML safely
VOCAB_HTML=""
for word in "${VOCAB_WORDS[@]}"; do
    if [[ -n "$word" ]]; then
        WORD_NAME=$(echo "$word" | cut -d':' -f1)
        WORD_MEANING=$(echo "$word" | cut -d':' -f2-)
        WORD_NAME_ESCAPED=$(escape_html "$WORD_NAME")
        WORD_MEANING_ESCAPED=$(escape_html "$WORD_MEANING")
        VOCAB_HTML="${VOCAB_HTML}    <div class=\"vocab\"><span class=\"word\">${WORD_NAME_ESCAPED}</span> - ${WORD_MEANING_ESCAPED}</div>\n"
    fi
done

# Detect Chrome/Chromium executable (cross-platform)
detect_chrome() {
    # macOS
    if [[ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
        echo "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        return 0
    fi
    # Linux (common paths)
    for chrome in "google-chrome" "chromium" "chromium-browser"; do
        if command -v "$chrome" &>/dev/null; then
            echo "$chrome"
            return 0
        fi
    done
    # Windows (WSL or native)
    if [[ -f "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" ]]; then
        echo "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
        return 0
    fi
    echo ""
    return 1
}

CHROME_BIN=$(detect_chrome || echo "")

# Create HTML file with embedded CSS for print
cat > "$HTML_FILE" << HTMLEOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <style>
    @page { 
      size: A4;
      margin: 1.5cm 1cm;
      @top-left { content: none; }
      @top-center { content: none; }
      @top-right { content: none; }
      @bottom-left {
        content: none;  /* 移除左下角路径 */
      }
    }
    body { 
      font-family: "PingFang SC", "Microsoft YaHei", "SimSun", sans-serif; 
      max-width: 800px; 
      margin: 0 auto;
      line-height: 1.6;
    }
    .header { 
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
      color: white; 
      padding: 20px; 
      border-radius: 10px; 
      margin-bottom: 20px;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .title { font-size: 28px; font-weight: bold; margin-bottom: 10px; }
    .date { font-size: 16px; opacity: 0.9; }
    .type-badge {
      background: linear-gradient(135deg, ${TYPE_BG} 0%, ${TYPE_BG_END} 100%);
      color: white;
      padding: 8px 15px;
      border-radius: 5px;
      font-size: 14px;
      font-weight: bold;
      margin-top: 10px;
      display: inline-block;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .type-warning {
      background: #fff3cd;
      border-left: 4px solid #ffc107;
      color: #856404;
      padding: 10px 15px;
      margin: 15px 0;
      border-radius: 5px;
      font-size: 13px;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .section { 
      margin: 20px 0; 
      padding: 20px; 
      background: #f8f9fa; 
      border-radius: 8px;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .section-title { 
      font-size: 18px; 
      font-weight: bold; 
      color: #667eea; 
      margin-bottom: 15px; 
      border-bottom: 2px solid #667eea; 
      padding-bottom: 8px; 
    }
    .english { font-size: 16px; color: #333; }
    .chinese { font-size: 16px; color: #555; margin-top: 15px; }
    .english-title { margin-bottom: 8px; display: block; }
    .vocab { 
      background: white; 
      padding: 15px; 
      border-radius: 5px; 
      margin: 10px 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    .word { font-weight: bold; color: #764ba2; }
    .footer { 
      text-align: center; 
      margin-top: 40px; 
      color: #999; 
      font-size: 12px; 
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title">📰 English Daily Report</div>
    <div class="date">${DATE_ESCAPED}</div>
    <div class="type-badge">${TYPE_BADGE_ESCAPED}</div>
  </div>

  ${TYPE_WARNING_ESCAPED:+<div class="type-warning">${TYPE_WARNING_ESCAPED}</div>}

  <div class="section">
    <div class="section-title">📄 News Summary</div>
    <div class="english">
      <strong class="english-title">${ENGLISH_TITLE_ESCAPED}</strong>
${ENGLISH_CONTENT_ESCAPED}
    </div>
  </div>

  <div class="section">
    <div class="section-title">📖 全文释义</div>
    <div class="chinese">
${CHINESE_TRANSLATION_ESCAPED}
    </div>
  </div>

  <div class="section">
    <div class="section-title">📝 Vocabulary & Grammar</div>
$(echo -e "${VOCAB_HTML}")
  </div>

  <div class="footer">
    英语学习计划 · 每日推送 · Generated on ${DATE}
  </div>
</body>
</html>
HTMLEOF

echo "HTML created at ${HTML_FILE}"

# Convert to PDF with date in filename
if [[ -n "$CHROME_BIN" ]]; then
    "$CHROME_BIN" --headless --disable-gpu --print-to-pdf="${PDF_FILE}" "${HTML_FILE}" 2>&1
    echo "PDF created at ${PDF_FILE}"
else
    echo "ERROR: Chrome/Chromium not found. Please install Chrome or Chromium."
    echo "PDF file would be: ${PDF_FILE}"
    exit 1
fi

# Audio file path (for reference, TTS will be called separately)
AUDIO_FILE="${WORKSPACE_DIR}/uploads/english-daily-${DATE}.mp3"
echo "Audio should be saved to: ${AUDIO_FILE}"
