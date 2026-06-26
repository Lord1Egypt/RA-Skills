#!/bin/bash
# Check Context Health
# Reports current context status and recommendations

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
MEMORY_DIR="$WORKSPACE/memory"
SUMMARIES_DIR="$MEMORY_DIR/summaries"

echo "=== Context Health Check ==="
echo ""

# Char estimation (rough: 1 char ≈ 3 bytes for mixed content)
estimate_units() {
    local bytes=$1
    echo $((bytes / 3))
}

# Check session files
echo "📊 Session Files:"
echo "----------------"
total_session_bytes=0
total_session_lines=0
large_sessions=0

for f in "$SESSIONS_DIR"/*.jsonl; do
    [ -f "$f" ] || continue
    [ -f "${f}.lock" ] && continue
    [ "$f" == *".deleted."* ] && continue
    
    lines=$(wc -l < "$f" 2>/dev/null || echo 0)
    bytes=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo 0)
    total_session_bytes=$((total_session_bytes + bytes))
    total_session_lines=$((total_session_lines + lines))
    
    if [ "$bytes" -gt 307200 ]; then
        ((large_sessions++))
        echo "  ⚠️  $(basename "$f"): $lines lines, $((bytes / 1024))KB (needs truncation)"
    fi
done

session_units=$(estimate_units $total_session_bytes)
echo ""
echo "  Total: $total_session_lines lines, ~$session_units chars"
echo "  Large files: $large_sessions"
echo ""

# Check memory files
echo "📝 Memory Files:"
echo "----------------"

# MEMORY.md
if [ -f "$MEMORY_DIR/../MEMORY.md" ]; then
    memory_bytes=$(stat -c%s "$MEMORY_DIR/../MEMORY.md" 2>/dev/null || stat -f%z "$MEMORY_DIR/../MEMORY.md" 2>/dev/null || echo 0)
    memory_units=$(estimate_units $memory_bytes)
    echo "  MEMORY.md: ~$memory_units chars"
else
    echo "  MEMORY.md: ❌ Not found"
fi

# Daily notes
echo ""
echo "  Daily Notes:"
today=$(date '+%Y-%m-%d')
yesterday=$(date -d "yesterday" '+%Y-%m-%d' 2>/dev/null || date -v-1d '+%Y-%m-%d' 2>/dev/null)

for date in "$today" "$yesterday"; do
    note="$MEMORY_DIR/$date.md"
    if [ -f "$note" ]; then
        bytes=$(stat -c%s "$note" 2>/dev/null || stat -f%z "$note" 2>/dev/null || echo 0)
        chars=$(estimate_units $bytes)
        echo "    $date.md: ~$chars chars ✅"
    else
        echo "    $date.md: Not found"
    fi
done

# Summaries
echo ""
echo "  Summaries:"
if [ -d "$SUMMARIES_DIR" ]; then
    summary_count=$(find "$SUMMARIES_DIR" -name "*.md" | wc -l)
    summary_bytes=$(find "$SUMMARIES_DIR" -name "*.md" -exec cat {} \; 2>/dev/null | wc -c)
    summary_units=$(estimate_units $summary_bytes)
    echo "    $summary_count summaries, ~$summary_units chars total"
else
    echo "    No summaries directory"
fi

echo ""

# Context budget calculation
echo "📈 Context Budget:"
echo "-----------------"
echo "  Model limit: 80,000 chars"
echo ""

# Estimate each layer
l4_units=0
l3_units=0
l2_units=0

# L4: MEMORY.md
if [ -f "$MEMORY_DIR/../MEMORY.md" ]; then
    bytes=$(stat -c%s "$MEMORY_DIR/../MEMORY.md" 2>/dev/null || stat -f%z "$MEMORY_DIR/../MEMORY.md" 2>/dev/null || echo 0)
    l4_units=$(estimate_units $bytes)
fi

# L3: Summaries
if [ -d "$SUMMARIES_DIR" ]; then
    summary_bytes=$(find "$SUMMARIES_DIR" -name "*.md" -exec cat {} \; 2>/dev/null | wc -c)
    l3_units=$(estimate_units $summary_bytes)
fi

# L2: Session files (limited to window)
l2_units=$session_units
if [ "$l2_units" -gt 25000 ]; then
    l2_units=25000
fi

echo "  L4 (Long-term memory): ~$l4_units chars"
echo "  L3 (Summaries):        ~$l3_units chars"
echo "  L2 (Recent sessions):  ~$l2_units chars"
echo "  L1 (Current session):  ~30,000 chars (estimated)"
echo "  System messages:       ~10,000 chars"
echo ""
total_estimated=$((l4_units + l3_units + l2_units + 30000 + 10000))
echo "  Estimated total:       ~$total_estimated chars"

if [ "$total_estimated" -gt 80000 ]; then
    echo ""
    echo "  ⚠️  WARNING: Estimated context exceeds limit!"
    echo "  Recommendations:"
    echo "    1. Run truncation: truncate-sessions-safe.sh"
    echo "    2. Reduce L3 summaries: delete older summaries"
    echo "    3. Compress MEMORY.md"
else
    echo ""
    echo "  ✅ Context within budget"
fi

echo ""

# Check crontab
echo "⚙️  System Configuration:"
echo "-----------------------"
if crontab -l 2>/dev/null | grep -q "truncate-sessions"; then
    echo "  Truncation cron: ✅ Installed"
else
    echo "  Truncation cron: ❌ Not installed"
    echo "    Run: crontab -e and add:"
    echo "    */10 * * * * $WORKSPACE/skills/context-compression/truncate-sessions-safe.sh"
fi

if crontab -l 2>/dev/null | grep -q "generate-daily-summary"; then
    echo "  Summary cron: ✅ Installed"
else
    echo "  Summary cron: ⚠️  Not installed (optional)"
fi

echo ""
echo "=== End of Health Check ==="
