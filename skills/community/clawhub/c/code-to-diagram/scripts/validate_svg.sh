#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ $# -eq 0 ]; then
    echo "Usage: $0 <svg-file>"
    exit 1
fi

SVG_FILE="$1"

if [ ! -f "$SVG_FILE" ]; then
    echo -e "${RED}Error: File not found: $SVG_FILE${NC}"
    exit 1
fi

echo "Validating SVG: $SVG_FILE"
echo "----------------------------------------"

FAILURES=0

# Check 0: XML syntax (xmllint)
echo -n "Checking XML syntax... "
if command -v xmllint &> /dev/null; then
    if xmllint --noout "$SVG_FILE" 2>/dev/null; then
        echo -e "${GREEN}✓ Pass${NC}"
    else
        echo -e "${RED}✗ Fail${NC}"
        xmllint --noout "$SVG_FILE" 2>&1 || true
        FAILURES=$((FAILURES + 1))
    fi
else
    echo -e "${YELLOW}⚠ Skipped${NC} (xmllint not found)"
fi

# Check 1: Tag balance
echo -n "Checking tag balance... "
OPEN_TAGS=$( { grep -o '<[A-Za-z][A-Za-z0-9:-]*' "$SVG_FILE" || true; } | { grep -v '</' || true; } | wc -l | tr -d ' ' )
SELF_CLOSING=$( { grep -o '/>' "$SVG_FILE" || true; } | wc -l | tr -d ' ' )
CLOSE_TAGS=$( { grep -o '</[A-Za-z][A-Za-z0-9:-]*>' "$SVG_FILE" || true; } | wc -l | tr -d ' ' )
TOTAL_CLOSE=$((SELF_CLOSING + CLOSE_TAGS))

if [ "$OPEN_TAGS" -eq "$TOTAL_CLOSE" ]; then
    echo -e "${GREEN}✓ Pass${NC} (${OPEN_TAGS} tags)"
else
    echo -e "${RED}✗ Fail${NC} (${OPEN_TAGS} open, ${TOTAL_CLOSE} close)"
    FAILURES=$((FAILURES + 1))
fi

# Check 2: Attribute quote balance
echo -n "Checking attribute quotes... "
UNQUOTED=$( { grep -oE '[a-z-]+=[^"'\''> ]' "$SVG_FILE" || true; } | wc -l | tr -d ' ' )
if [ "$UNQUOTED" -eq 0 ]; then
    echo -e "${GREEN}✓ Pass${NC}"
else
    echo -e "${RED}✗ Fail${NC} (${UNQUOTED} unquoted attributes)"
    grep -n -oE '[a-z-]+=[^"'\''> ]' "$SVG_FILE" | head -5 || true
    FAILURES=$((FAILURES + 1))
fi

# Check 3: Marker references
echo -n "Checking marker references... "
MARKER_REFS=$( { grep -oE 'marker-end="url\(#[^)]+\)"' "$SVG_FILE" || true; } | { grep -oE '#[^)]+' || true; } | tr -d '#' | sort -u )
MARKER_DEFS=$( { grep -oE '<marker id="[^"]+"' "$SVG_FILE" || true; } | { grep -oE 'id="[^"]+"' || true; } | sed 's/id="//;s/"//' | sort -u )

MISSING=0
for ref in $MARKER_REFS; do
    if ! echo "$MARKER_DEFS" | grep -q "^${ref}$"; then
        echo ""
        echo -e "  ${RED}Missing marker: $ref${NC}"
        MISSING=$((MISSING + 1))
    fi
done

if [ "$MISSING" -eq 0 ]; then
    if [ -n "$MARKER_REFS" ]; then
        echo -e "${GREEN}✓ Pass${NC}"
    else
        echo -e "${GREEN}✓ Pass${NC} (no markers)"
    fi
else
    FAILURES=$((FAILURES + 1))
fi

# Check 4: Closing </svg> tag
echo -n "Checking closing tag... "
if grep -q '</svg>' "$SVG_FILE"; then
    echo -e "${GREEN}✓ Pass${NC}"
else
    echo -e "${RED}✗ Fail${NC} (missing </svg>)"
    FAILURES=$((FAILURES + 1))
fi

# Check 5: rsvg-convert render test
echo -n "Running rsvg-convert validation... "
if command -v rsvg-convert &> /dev/null; then
    TMPOUT=$(mktemp /tmp/svg-validate-XXXXXX.png)
    if rsvg-convert "$SVG_FILE" -o "$TMPOUT" 2>/dev/null; then
        echo -e "${GREEN}✓ Pass${NC}"
        rm -f "$TMPOUT"
    else
        echo -e "${RED}✗ Fail${NC}"
        rsvg-convert "$SVG_FILE" -o "$TMPOUT" 2>&1 || true
        rm -f "$TMPOUT"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo -e "${YELLOW}⚠ Skipped${NC} (rsvg-convert not found)"
fi

echo "----------------------------------------"
if [ "$FAILURES" -eq 0 ]; then
    echo -e "${GREEN}Validation passed${NC}"
    exit 0
fi

echo -e "${RED}Validation failed (${FAILURES} error(s))${NC}"
exit 1
