#!/bin/bash
# adversarial-review: Synthesize reviewer outputs into a sorted combined redline
#
# Usage: synthesize.sh <session-name>
#
# Reads all .md files in {session}/redlines/ (except combined.md)
# Extracts REDLINE-* blocks, sorts by severity (CRITICAL → MAJOR → MINOR)
# Writes {session}/redlines/combined.md

set -e

REVIEWS_DIR="${HOME}/.openclaw/workspace/reviews"

if [ -z "$1" ]; then
  echo "Usage: synthesize.sh <session-name>"
  echo "Example: synthesize.sh 2026-03-06-bitwage-taxonomy"
  echo ""
  echo "Available sessions:"
  ls "$REVIEWS_DIR" 2>/dev/null || echo "  (none)"
  exit 1
fi

SESSION_NAME="$1"
REDLINES_DIR="${REVIEWS_DIR}/${SESSION_NAME}/redlines"
OUTPUT="${REDLINES_DIR}/combined.md"

if [ ! -d "$REDLINES_DIR" ]; then
  echo "Error: Redlines directory not found: $REDLINES_DIR"
  exit 1
fi

SOURCE_COUNT=$(find "$REDLINES_DIR" -name "*.md" ! -name "combined.md" | wc -l | tr -d ' ')

if [ "$SOURCE_COUNT" -eq 0 ]; then
  echo "Error: No reviewer output files found in $REDLINES_DIR"
  echo "Write reviewer outputs as reviewer-{role}.md before synthesizing."
  exit 1
fi

echo "Synthesizing ${SOURCE_COUNT} reviewer file(s)..."

# Write node script to a temp file to avoid heredoc env var issues
TMPSCRIPT=$(mktemp /tmp/synthesize-XXXXXX.js)

cat > "$TMPSCRIPT" << 'JSEOF'
const fs = require('fs');
const path = require('path');

const sessionName = process.argv[2];
const reviewsDir  = process.argv[3];
const redlinesDir = path.join(reviewsDir, sessionName, 'redlines');
const outputFile  = path.join(redlinesDir, 'combined.md');

const files = fs.readdirSync(redlinesDir)
  .filter(f => f.endsWith('.md') && f !== 'combined.md')
  .map(f => path.join(redlinesDir, f));

const severityOrder = { CRITICAL: 0, MAJOR: 1, MINOR: 2 };
const redlines = [];

for (const file of files) {
  const content = fs.readFileSync(file, 'utf8');
  const reviewer = path.basename(file, '.md').replace('reviewer-', '');

  // Split on REDLINE block boundaries
  const blocks = content.split(/(?=\*\*\[REDLINE-)/).filter(b =>
    b.includes('**Severity:**') && b.includes('**[REDLINE-')
  );

  for (const block of blocks) {
    const idMatch  = block.match(/\*\*\[REDLINE-([A-Z])-(\d+)\]\*\*/);
    const sevMatch = block.match(/\*\*Severity:\*\*\s*(CRITICAL|MAJOR|MINOR)/);
    if (!idMatch || !sevMatch) continue;

    redlines.push({
      id:       `REDLINE-${idMatch[1]}-${idMatch[2]}`,
      type:     idMatch[1],
      num:      parseInt(idMatch[2]),
      severity: sevMatch[1],
      order:    severityOrder[sevMatch[1]] ?? 99,
      reviewer,
      text:     block.trim()
    });
  }
}

// Sort: severity first, then reviewer, then number
redlines.sort((a, b) =>
  a.order - b.order ||
  a.reviewer.localeCompare(b.reviewer) ||
  a.num - b.num
);

const counts = { CRITICAL: 0, MAJOR: 0, MINOR: 0 };
redlines.forEach(r => counts[r.severity]++);

const date = new Date().toISOString().split('T')[0];
let out = `# Combined Redlines — ${sessionName}\n\n`;
out += `**Synthesized:** ${date}  \n`;
out += `**Source files:** ${files.length}  \n`;
out += `**Total redlines:** ${redlines.length}`;
out += ` (🔴 CRITICAL: ${counts.CRITICAL} | 🟡 MAJOR: ${counts.MAJOR} | 🟢 MINOR: ${counts.MINOR})\n\n---\n\n`;

let currentSeverity = null;
for (const r of redlines) {
  if (r.severity !== currentSeverity) {
    currentSeverity = r.severity;
    const emoji = currentSeverity === 'CRITICAL' ? '🔴' : currentSeverity === 'MAJOR' ? '🟡' : '🟢';
    out += `## ${emoji} ${currentSeverity}\n\n`;
  }
  out += `${r.text}\n\n---\n\n`;
}

fs.writeFileSync(outputFile, out);

console.log(`\n✓ Combined redlines written: ${outputFile}`);
console.log(`\n  🔴 CRITICAL: ${counts.CRITICAL}`);
console.log(`  🟡 MAJOR:    ${counts.MAJOR}`);
console.log(`  🟢 MINOR:    ${counts.MINOR}`);
console.log(`  TOTAL:    ${redlines.length}`);

if (counts.CRITICAL === 0) {
  console.log('\n⚠ Zero CRITICAL issues — consider whether reviewers were adversarial enough.');
}
JSEOF

node "$TMPSCRIPT" "$SESSION_NAME" "$REVIEWS_DIR"
rm -f "$TMPSCRIPT"
