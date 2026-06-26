---
name: component-library-audit
description: Audit React, Vue, or Svelte component libraries — find unused components, inconsistent props, missing documentation, accessibility issues, missing tests, and naming convention violations.
---

# Component Library Audit

Analyze a front-end component library for quality, consistency, and completeness. Finds unused components, prop inconsistencies, missing docs, accessibility gaps, and testing holes.

Use when: "audit our components", "find unused components", "check component quality", "component library health", "are our components consistent", "which components need tests", or maintaining a design system.

## Commands

### 1. `audit` — Full Component Library Audit

Run all checks and produce a health report.

#### Step 1: Discover Components

```bash
echo "=== Component Discovery ==="

# React components (.tsx/.jsx)
echo "--- React Components ---"
find . -type f \( -name "*.tsx" -o -name "*.jsx" \) \
  -not -path '*/node_modules/*' -not -path '*/dist/*' -not -path '*/build/*' \
  -not -name '*.test.*' -not -name '*.spec.*' -not -name '*.stories.*' \
  2>/dev/null | while read f; do
  # Check if it exports a component (function starting with uppercase or default export)
  if rg -q "export (default |)(function |const )[A-Z]|export default class [A-Z]" "$f" 2>/dev/null; then
    COMP=$(rg -o "(function|const|class) ([A-Z][a-zA-Z]+)" "$f" 2>/dev/null | head -1 | awk '{print $2}')
    echo "  $f → ${COMP:-UnnamedComponent}"
  fi
done

# Vue components (.vue)
echo "--- Vue Components ---"
find . -type f -name "*.vue" \
  -not -path '*/node_modules/*' -not -path '*/dist/*' \
  -not -name '*.test.*' -not -name '*.stories.*' \
  2>/dev/null | while read f; do
  NAME=$(basename "$f" .vue)
  echo "  $f → $NAME"
done

# Svelte components (.svelte)
echo "--- Svelte Components ---"
find . -type f -name "*.svelte" \
  -not -path '*/node_modules/*' -not -path '*/dist/*' \
  -not -name '*.test.*' -not -name '*.stories.*' \
  2>/dev/null | while read f; do
  NAME=$(basename "$f" .svelte)
  echo "  $f → $NAME"
done

# Count
TOTAL=$(find . -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" \) \
  -not -path '*/node_modules/*' -not -path '*/dist/*' -not -path '*/build/*' \
  -not -name '*.test.*' -not -name '*.spec.*' -not -name '*.stories.*' 2>/dev/null | wc -l)
echo "Total components found: $TOTAL"
```

#### Step 2: Find Unused Components

```bash
echo ""
echo "=== Unused Components ==="

# Get all component names
COMPONENTS=$(find . -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" \) \
  -not -path '*/node_modules/*' -not -path '*/dist/*' \
  -not -name '*.test.*' -not -name '*.spec.*' -not -name '*.stories.*' 2>/dev/null)

echo "$COMPONENTS" | while read f; do
  NAME=$(basename "$f" | sed 's/\.[^.]*$//')
  # Skip index files
  [ "$NAME" = "index" ] && continue

  # Count imports of this component (excluding its own file and tests)
  IMPORT_COUNT=$(rg -c "import.*$NAME|from.*/$NAME['\"]|<$NAME[ />]" \
    -g '*.{tsx,jsx,vue,svelte,ts,js}' -g '!node_modules' -g '!dist' \
    --type-not binary 2>/dev/null | \
    grep -v "$(basename "$f")" | \
    awk -F: '{s+=$2} END {print s+0}')

  if [ "$IMPORT_COUNT" -eq 0 ]; then
    LINES=$(wc -l < "$f" 2>/dev/null || echo "?")
    echo "  ⚠️  UNUSED: $NAME ($f) — $LINES lines"
  fi
done
```

#### Step 3: Check Documentation

```bash
echo ""
echo "=== Documentation Check ==="

echo "$COMPONENTS" | while read f; do
  NAME=$(basename "$f" | sed 's/\.[^.]*$//')
  DIR=$(dirname "$f")

  # Check for JSDoc/TSDoc comments
  HAS_JSDOC=$(rg -c "/\*\*" "$f" 2>/dev/null || echo "0")

  # Check for Storybook stories
  HAS_STORY=$(find "$DIR" -maxdepth 1 \( -name "${NAME}.stories.*" -o -name "${NAME}.story.*" \) 2>/dev/null | head -1)

  # Check for README in component directory
  HAS_README=$(find "$DIR" -maxdepth 1 -name "README*" 2>/dev/null | head -1)

  if [ "$HAS_JSDOC" = "0" ] && [ -z "$HAS_STORY" ] && [ -z "$HAS_README" ]; then
    echo "  ❌ $NAME — no docs, no stories, no README"
  elif [ -z "$HAS_STORY" ]; then
    echo "  ⚠️  $NAME — no Storybook story"
  fi
done
```

#### Step 4: Prop Consistency Analysis

```bash
echo ""
echo "=== Prop Consistency ==="

# Find common prop naming patterns
echo "--- Common Props Across Components ---"
rg -o "interface \w+Props \{[^}]*\}" -g '*.tsx' -g '!node_modules' --multiline 2>/dev/null | \
  rg -o "\w+[?]?:" | sed 's/[?:]//g' | sort | uniq -c | sort -rn | head -20

# Check for inconsistent naming
echo ""
echo "--- Potential Naming Inconsistencies ---"
# onClick vs onPress vs handleClick
rg -l "onPress" -g '*.{tsx,jsx}' -g '!node_modules' 2>/dev/null | head -5
rg -l "onClick" -g '*.{tsx,jsx}' -g '!node_modules' 2>/dev/null | head -5

# isVisible vs visible vs show
rg -o "(is[A-Z]\w+|visible|show|hidden|disabled|enabled|active|selected|checked|open|closed)" \
  -g '*.{tsx,jsx}' -g '!node_modules' 2>/dev/null | sort | uniq -c | sort -rn | head -20

# className vs class vs style
rg -c "className" -g '*.{tsx,jsx}' -g '!node_modules' 2>/dev/null | awk -F: '{s+=$2} END {print "className:", s+0}'
rg -c "class=" -g '*.{vue,svelte}' -g '!node_modules' 2>/dev/null | awk -F: '{s+=$2} END {print "class:", s+0}'

# Size props: small/medium/large vs sm/md/lg
echo "Size prop conventions:"
rg -o "size['\"]?\s*[:=]\s*['\"]?(small|medium|large|xs|sm|md|lg|xl|xxl)" \
  -g '*.{tsx,jsx,vue,svelte}' -g '!node_modules' 2>/dev/null | sort | uniq -c | sort -rn
```

#### Step 5: Test Coverage

```bash
echo ""
echo "=== Test Coverage ==="

echo "$COMPONENTS" | while read f; do
  NAME=$(basename "$f" | sed 's/\.[^.]*$//')
  DIR=$(dirname "$f")

  TEST=$(find "$DIR" -maxdepth 2 \( -name "${NAME}.test.*" -o -name "${NAME}.spec.*" \) \
    -not -path '*/node_modules/*' 2>/dev/null | head -1)

  if [ -z "$TEST" ]; then
    LINES=$(wc -l < "$f" 2>/dev/null || echo "?")
    echo "  ❌ $NAME ($LINES lines) — NO TEST"
  fi
done | sort -t'(' -k2 -rn | head -20
```

#### Step 6: Accessibility Check

```bash
echo ""
echo "=== Accessibility Audit ==="

# Images without alt
echo "--- Images without alt text ---"
rg -n "<img[^>]+(?!alt=)" -g '*.{tsx,jsx,vue,svelte}' -g '!node_modules' 2>/dev/null | \
  grep -v "alt=" | head -10

# Interactive elements without aria labels
echo "--- Buttons/links without accessible names ---"
rg -n "<(button|a|input)[^>]*>" -g '*.{tsx,jsx,vue,svelte}' -g '!node_modules' 2>/dev/null | \
  grep -v "aria-label\|aria-labelledby\|aria-describedby" | head -10

# Missing role attributes on custom interactive elements
echo "--- Custom elements that may need role ---"
rg -n "onClick=\{" -g '*.{tsx,jsx}' -g '!node_modules' 2>/dev/null | \
  grep -v "<button\|<a \|<input\|<select\|<textarea\|role=" | head -10

# Color contrast hints (inline styles with color)
echo "--- Inline color styles (verify contrast) ---"
rg -n "color:\s*['\"]?#" -g '*.{tsx,jsx,vue,svelte,css}' -g '!node_modules' 2>/dev/null | head -10

# Form inputs without labels
echo "--- Inputs without associated labels ---"
rg -n "<input" -g '*.{tsx,jsx,vue,svelte}' -g '!node_modules' 2>/dev/null | \
  grep -v "aria-label\|id=.*label\|<label" | head -10
```

#### Step 7: Naming Convention Audit

```bash
echo ""
echo "=== Naming Conventions ==="

# Component file naming
echo "--- File naming patterns ---"
find . -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.svelte" \) \
  -not -path '*/node_modules/*' -not -path '*/dist/*' \
  -not -name '*.test.*' -not -name '*.spec.*' -not -name '*.stories.*' 2>/dev/null | \
  xargs -I{} basename {} | sort | python3 -c "
import sys
files = [l.strip() for l in sys.stdin if l.strip()]
pascal = sum(1 for f in files if f[0].isupper() and '-' not in f.split('.')[0])
kebab = sum(1 for f in files if '-' in f.split('.')[0])
camel = sum(1 for f in files if f[0].islower() and '-' not in f.split('.')[0] and '_' not in f.split('.')[0])

total = len(files)
print(f'PascalCase: {pascal}/{total}')
print(f'kebab-case: {kebab}/{total}')
print(f'camelCase: {camel}/{total}')

if pascal > 0 and kebab > 0:
    print('⚠️  MIXED conventions — pick one and stick to it')
" 2>/dev/null

# Directory structure
echo "--- Component organization ---"
find . -maxdepth 3 -type d -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/dist/*' 2>/dev/null | grep -iE "(component|ui|atoms|molecules|organisms|layouts|pages|widgets|common|shared)" | head -10
```

### 2. `unused` — Focus on Unused Components

Run Step 2 in detail, with import chain analysis.

### 3. `a11y` — Accessibility Deep Dive

Run Step 6 with expanded checks including keyboard navigation, focus management, ARIA patterns.

### 4. `consistency` — Prop and Pattern Consistency

Run Step 4 and Step 7 with detailed recommendations for standardization.

### 5. `coverage` — Test and Documentation Coverage Matrix

Combined Step 3 and Step 5 as a coverage matrix:

```markdown
| Component | Tests | Stories | Docs | Lines |
|-----------|-------|---------|------|-------|
| Button | ✅ | ✅ | ✅ | 45 |
| Modal | ❌ | ✅ | ⚠️ | 120 |
| DataTable | ❌ | ❌ | ❌ | 380 |
```

## Output Formats

- **text** (default): Human-readable audit report
- **json**: `{components: [{name, path, lines, hasTest, hasStory, hasDocs, isUsed, a11yIssues: []}], summary: {}}`
- **markdown**: Report with tables, suitable for PRs or wikis

## Notes

- Supports React (TSX/JSX), Vue (.vue SFC), and Svelte (.svelte) components
- Unused component detection uses import/usage grep — may miss dynamic imports
- Accessibility checks are pattern-based, not runtime — complement with axe-core or Lighthouse
- Prop analysis works best with TypeScript (explicit interfaces)
- Naming convention detection helps enforce consistency but doesn't judge which convention is "correct"
- For Storybook detection, supports both `.stories.tsx` and `.story.tsx` patterns
