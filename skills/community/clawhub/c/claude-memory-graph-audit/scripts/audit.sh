#!/usr/bin/env bash
# claude-memory-graph-audit / audit.sh
# Usage: ./audit.sh [memory_dir]   (defaults to most recently modified ~/.claude/projects/*/memory)

set -e

MEM_DIR="${1:-$HOME/.claude/projects/$(ls -t $HOME/.claude/projects 2>/dev/null | head -1)/memory}"

if [ ! -d "$MEM_DIR" ]; then
  echo "❌ Memory directory not found: $MEM_DIR"
  exit 1
fi

cd "$MEM_DIR"

NODES=$(ls *.md 2>/dev/null | grep -v "^MEMORY.md$" | wc -l | tr -d ' ')
echo "📁 Memory dir: $MEM_DIR"
echo "🔢 Nodes: $NODES"
echo ""

echo "=== 🐛 Broken wikilinks ==="
broken=0
for link in $(grep -h -oE '\[\[[a-z_-]+\]\]' *.md 2>/dev/null | sed 's/\[\[//;s/\]\]//' | sort -u); do
  if [ ! -f "${link}.md" ]; then
    echo "  ❌ [[$link]] referenced from: $(grep -l "\[\[$link\]\]" *.md | tr '\n' ' ')"
    broken=$((broken+1))
  fi
done
[ $broken -eq 0 ] && echo "  ✅ none"
echo ""

echo "=== 🏝️ Orphan pages (in=0 AND out=0) ==="
orphans=0
for f in *.md; do
  [ "$f" = "MEMORY.md" ] && continue
  base="${f%.md}"
  out=$(grep -oE '\[\[[a-z_-]+\]\]' "$f" 2>/dev/null | sort -u | wc -l | tr -d ' ')
  in=$(grep -l -E "\[\[$base\]\]" *.md 2>/dev/null | grep -v "^$f$" | wc -l | tr -d ' ')
  if [ "$out" = "0" ] && [ "$in" = "0" ]; then
    echo "  🏝️ $f"
    orphans=$((orphans+1))
  fi
done
[ $orphans -eq 0 ] && echo "  ✅ none"
echo ""

echo "=== ⭐ Hub nodes (in-degree ≥ 3) ==="
for f in *.md; do
  [ "$f" = "MEMORY.md" ] && continue
  base="${f%.md}"
  in=$(grep -l -E "\[\[$base\]\]" *.md 2>/dev/null | grep -v "^$f$" | wc -l | tr -d ' ')
  if [ "$in" -ge 3 ]; then
    printf "  ⭐ in=%-3s %s\n" "$in" "$f"
  fi
done
echo ""

echo "=== 🌉 Bridge candidates (out-degree ≥ 3) ==="
for f in *.md; do
  [ "$f" = "MEMORY.md" ] && continue
  out=$(grep -oE '\[\[[a-z_-]+\]\]' "$f" 2>/dev/null | sort -u | wc -l | tr -d ' ')
  if [ "$out" -ge 3 ]; then
    printf "  🌉 out=%-3s %s\n" "$out" "$f"
  fi
done
echo ""

TOTAL_EDGES=$(grep -h -oE '\[\[[a-z_-]+\]\]' *.md 2>/dev/null | wc -l | tr -d ' ')
UNIQ_EDGES=$(grep -h -oE '\[\[[a-z_-]+\]\]' *.md 2>/dev/null | sort -u | wc -l | tr -d ' ')

echo "=== 📊 Summary ==="
echo "  Nodes:             $NODES"
echo "  Total edges:       $TOTAL_EDGES (unique targets: $UNIQ_EDGES)"
echo "  Broken links:      $broken"
echo "  Orphan pages:      $orphans"
echo ""

if [ $broken -gt 0 ] || [ $orphans -gt 0 ]; then
  echo "⚠️  Issues found. Use the SKILL.md guide to fix."
  exit 1
else
  echo "✅ Graph is healthy."
fi
