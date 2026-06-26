#!/bin/bash
echo "=== Dream Cycle Audit ==="
echo "Time: $(date)"
echo ""

echo "--- Workspace Files ---"
for f in AGENTS.md MEMORY.md USER.md SOUL.md IDENTITY.md HEARTBEAT.md; do
  if [ -f "$HOME/.openclaw/workspace/$f" ]; then
    size=$(wc -c < "$HOME/.openclaw/workspace/$f")
    echo "$f: $size bytes"
  else
    echo "$f: NOT FOUND"
  fi
done

echo ""
echo "--- Memory Directory ---"
if [ -d "$HOME/.openclaw/workspace/memory" ]; then
  count=$(find "$HOME/.openclaw/workspace/memory" -type f -name "*.md" 2>/dev/null | wc -l)
  total=$(find "$HOME/.openclaw/workspace/memory" -type f -name "*.md" -exec cat {} \; 2>/dev/null | wc -c)
  echo "Memory files: $count"
  echo "Total memory size: $total chars"
else
  echo "memory/ directory not found"
fi

echo ""
echo "--- Drafts Directory ---"
if [ -d "$HOME/.openclaw/workspace/memory/drafts" ]; then
  draft_count=$(find "$HOME/.openclaw/workspace/memory/drafts" -type f 2>/dev/null | wc -l)
  echo "Draft files: $draft_count"
else
  echo "drafts/ not found"
fi
