#!/bin/bash
# Workspace Audit Script
# Scans workspace for dead files, large files, and cleanup opportunities

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
echo "=== Workspace Audit: $WORKSPACE ==="
echo ""

# Check for executable scripts
echo "📁 EXECUTABLE SCRIPTS (in workspace root)"
find "$WORKSPACE" -maxdepth 1 -type f -executable -name "*.sh" 2>/dev/null | while read f; do
    echo "  $f"
done
echo ""

# Check scripts directory
if [ -d "$WORKSPACE/scripts" ]; then
    echo "📁 SCRIPTS DIRECTORY"
    ls -la "$WORKSPACE/scripts/" 2>/dev/null | tail -n +4 | awk '{print "  "$NF" ("$5" bytes)"}'
    echo ""
fi

# Find recently modified files (last 7 days)
echo "📅 RECENTLY MODIFIED (7 days)"
find "$WORKSPACE" -type f -mtime -7 -not -path "*/.git/*" -not -path "*/memory/dreaming/*" 2>/dev/null | head -20 | while read f; do
    size=$(du -h "$f" 2>/dev/null | cut -f1)
    echo "  $f ($size)"
done
echo ""

# Find large files (>1MB)
echo "📊 LARGE FILES (>1MB)"
find "$WORKSPACE" -type f -size +1M -not -path "*/.git/*" 2>/dev/null | while read f; do
    size=$(du -h "$f" 2>/dev/null | cut -f1)
    echo "  $size $f"
done
echo ""

# Count files by extension
echo "📈 FILE COUNT BY TYPE"
echo "  Markdown (.md): $(find "$WORKSPACE" -maxdepth 1 -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Scripts (.sh): $(find "$WORKSPACE" -maxdepth 1 -type f -name "*.sh" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Python (.py): $(find "$WORKSPACE" -maxdepth 1 -type f -name "*.py" 2>/dev/null | wc -l | tr -d ' ')"
echo "  Logs (.log): $(find "$WORKSPACE" -type f -name "*.log" 2>/dev/null | wc -l | tr -d ' ')"
echo "  JSON (.json): $(find "$WORKSPACE" -maxdepth 1 -type f -name "*.json" 2>/dev/null | wc -l | tr -d ' ')"
echo ""

# Directory sizes
echo "📂 DIRECTORY SIZES"
du -sh "$WORKSPACE"/*/ 2>/dev/null | sort -hr | head -10 | awk '{print "  " $1 "\t" $2}'
echo ""

# Memory directory check
if [ -d "$WORKSPACE/memory" ]; then
    echo "📅 MEMORY DIRECTORY"
    echo "  Daily logs: $(find "$WORKSPACE/memory" -maxdepth 1 -name "????-??-??.md" 2>/dev/null | wc -l | tr -d ' ') files"
    echo "  Total size: $(du -sh "$WORKSPACE/memory" 2>/dev/null | cut -f1)"
    echo ""
fi

# Dead file candidates (scripts with no references)
echo "⚠️  DEAD FILE CANDIDATES (no cron references)"
echo "  (Run grep checks manually to verify)"
echo ""

echo "=== Audit Complete ==="
