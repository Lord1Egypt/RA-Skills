#!/usr/bin/env bash
# arxiv-to-obsidian 主脚本
# 获取 arXiv 最新论文并写入 Obsidian

set -euo pipefail

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 加载配置
source "$SCRIPT_DIR/config.sh"

NOTE_PATH="$VAULT_FOLDER/$NOTE_NAME"
SECTION_TITLE="## 今日AI论文"

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Error: required command not found: $1" >&2
        exit 1
    fi
}

echo "=== arxiv-to-obsidian ==="
echo "Vault: $VAULT_NAME"
echo "Folder: $VAULT_FOLDER"
echo "Note: $NOTE_PATH"
echo "Paper Count: $PAPER_COUNT"
echo "RSS URL: $ARXIV_RSS_URL"
echo "Dry Run: $DRY_RUN"
echo ""

require_command curl
require_command python3
require_command claude
require_command obsidian

# 检查 vault 是否存在
echo "Checking vault..."
if ! obsidian vault="$VAULT_NAME" vault >/dev/null 2>&1; then
    echo "Error: Vault '$VAULT_NAME' not found." >&2
    exit 1
fi

# 获取 RSS feed
echo "Fetching RSS feed..."
RSS_CONTENT="$(curl -fsSL "$ARXIV_RSS_URL")"

if [[ -z "$RSS_CONTENT" ]]; then
    echo "Error: Failed to fetch RSS feed from $ARXIV_RSS_URL" >&2
    exit 1
fi

echo "Parsing papers..."
PARSED_PAPERS="$(printf '%s' "$RSS_CONTENT" | python3 "$SCRIPT_DIR/parser.py" "$PAPER_COUNT")"

if [[ -z "$PARSED_PAPERS" ]]; then
    echo "Error: Failed to parse RSS feed" >&2
    exit 1
fi

echo "Generating Markdown..."
MARKDOWN_TABLE="$(printf '%s' "$PARSED_PAPERS" | python3 "$SCRIPT_DIR/translator.py")"

SECTION_CONTENT="$SECTION_TITLE

$MARKDOWN_TABLE"

if [[ "$DRY_RUN" == "1" ]]; then
    echo ""
    echo "=== Dry Run ==="
    printf '%s\n' "$SECTION_CONTENT"
    exit 0
fi

if ! obsidian vault="$VAULT_NAME" folder path="$VAULT_FOLDER" >/dev/null 2>&1; then
    echo "Creating target folder via Obsidian CLI..."
    BOOTSTRAP_PATH="$VAULT_FOLDER/.obsidian-bootstrap.md"
    obsidian vault="$VAULT_NAME" create path="$BOOTSTRAP_PATH" content=""
    obsidian vault="$VAULT_NAME" delete path="$BOOTSTRAP_PATH" permanent >/dev/null 2>&1 || true
fi

if obsidian vault="$VAULT_NAME" file path="$NOTE_PATH" >/dev/null 2>&1; then
    echo "Appending to existing note..."
    APPEND_CONTENT="

$SECTION_CONTENT"
    obsidian vault="$VAULT_NAME" append path="$NOTE_PATH" content="$APPEND_CONTENT"
else
    echo "Creating today's note..."
    obsidian vault="$VAULT_NAME" create path="$NOTE_PATH" content="$SECTION_CONTENT"
fi

echo ""
echo "=== Success! ==="
echo "Location: $VAULT_NAME/$NOTE_PATH"
echo ""
echo "Found $PAPER_COUNT papers and written to Obsidian."
