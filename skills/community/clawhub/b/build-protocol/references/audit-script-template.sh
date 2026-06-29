#!/bin/bash
# Build Protocol · Machine-Verified Audit Script Template
# Run before Step 8 (Publish). 🔴 failures block publishing.
#
# Usage: bash audit_check.sh [source_folder]
# Default: current directory

SOURCE_DIR="${1:-.}"
cd "$SOURCE_DIR" || { echo "Directory not found: $SOURCE_DIR"; exit 1; }

echo "================================================"
echo "  Build Protocol · Audit Verification"
echo "  Folder: $SOURCE_DIR"
echo "================================================"

# --- CONFIGURATION (override these per project) ---
MIN_PMID_PER_FILE=5        # Minimum citations per volume (0 to skip)
MIN_CHARS_PER_FILE=6000    # Minimum length per volume
REQUIRE_GENDER_BALANCE=1   # 1 = both male/female required
REQUIRE_RED_CRITICAL=1     # 1 = at least 1 🔴 per file (anti-sycophancy)
SAFETY_KEYWORDS_MIN=3      # Minimum safety keywords per file (for medical)

# File pattern: assume numbered like NN_topic.md
FILE_PATTERN='0[0-9]_*.md'

# ==================================================
# L1.1 Citation Count Check
# ==================================================
if [ "$MIN_PMID_PER_FILE" -gt 0 ]; then
  echo ""
  echo "【L1.1】Citation count (≥$MIN_PMID_PER_FILE per file)"
  fail=0
  for f in $FILE_PATTERN; do
    count=$(grep -c "PMID:" "$f" 2>/dev/null || echo 0)
    if [ "$count" -lt "$MIN_PMID_PER_FILE" ]; then
      echo "  ❌ $f: only $count citations"
      fail=$((fail+1))
    else
      echo "  ✅ $f: $count citations"
    fi
  done
  [ $fail -eq 0 ] && echo "  → PASS ✅"
fi

# ==================================================
# L1.2 Citation Duplicate Check (must be ZERO)
# ==================================================
echo ""
echo "【L1.2】Citation duplicates (must be 0)"
fail=0
for f in $FILE_PATTERN; do
  dup=$(grep -oP "PMID:\s*\d{7,8}" "$f" 2>/dev/null | sort | uniq -c | awk '$1 > 1')
  if [ -n "$dup" ]; then
    echo "  ❌ $f has duplicates:"
    echo "$dup" | head -3 | sed 's/^/     /'
    fail=$((fail+1))
  fi
done
[ $fail -eq 0 ] && echo "  → PASS ✅"

# ==================================================
# L6 Anti-Sycophancy Check
# ==================================================
if [ "$REQUIRE_RED_CRITICAL" -eq 1 ]; then
  echo ""
  echo "【L6】Anti-Sycophancy (≥1 🔴 critical per file)"
  fail=0
  for f in $FILE_PATTERN; do
    red=$(grep -c "🔴" "$f" 2>/dev/null || echo 0)
    green=$(grep -c "🟢" "$f" 2>/dev/null || echo 0)
    if [ "$red" -eq 0 ]; then
      echo "  ❌ $f: 0 🔴 critical (sycophancy violation)"
      fail=$((fail+1))
    else
      # Check ratio (🔴 should be ≥20% of 🟢)
      min_red=$((green / 5))
      if [ "$red" -lt "$min_red" ]; then
        echo "  ⚠️ $f: 🔴=$red, 🟢=$green (ratio below 20%)"
      else
        echo "  ✅ $f: 🔴=$red, 🟢=$green"
      fi
    fi
  done
  [ $fail -eq 0 ] && echo "  → PASS ✅"
fi

# ==================================================
# L5 H1 Layer Check
# ==================================================
echo ""
echo "【L5】H1 count (exactly 1 per file)"
fail=0
for f in $FILE_PATTERN; do
  h1=$(grep -c "^# " "$f" 2>/dev/null || echo 0)
  if [ "$h1" -ne 1 ]; then
    echo "  ❌ $f: $h1 H1s (should be 1)"
    fail=$((fail+1))
  fi
done
[ $fail -eq 0 ] && echo "  → PASS ✅"

# ==================================================
# L3 Length Check
# ==================================================
echo ""
echo "【L3】Length (≥$MIN_CHARS_PER_FILE chars)"
for f in $FILE_PATTERN; do
  size=$(wc -m < "$f" 2>/dev/null || echo 0)
  if [ "$size" -lt "$MIN_CHARS_PER_FILE" ]; then
    echo "  ❌ $f: $size chars"
  else
    echo "  ✅ $f: $size chars"
  fi
done

# ==================================================
# L3 Gender Balance (if required)
# ==================================================
if [ "$REQUIRE_GENDER_BALANCE" -eq 1 ]; then
  echo ""
  echo "【L3】Gender balance (both ≥3)"
  for f in $FILE_PATTERN; do
    # Adjust keywords for language (these for Chinese)
    male=$(grep -c "男性\|male" "$f" 2>/dev/null || echo 0)
    female=$(grep -c "女性\|female" "$f" 2>/dev/null || echo 0)
    [ "$male" -lt 3 ] && echo "  ⚠️ $f: male weak ($male)"
    [ "$female" -lt 3 ] && echo "  ⚠️ $f: female weak ($female)"
  done
fi

# ==================================================
# L4 Safety Keyword Coverage (medical content only)
# ==================================================
if [ "$SAFETY_KEYWORDS_MIN" -gt 0 ]; then
  echo ""
  echo "【L4】Safety keyword coverage (≥$SAFETY_KEYWORDS_MIN per file)"
  for f in $FILE_PATTERN; do
    count=0
    # Adjust keywords for content type (medical example here)
    for kw in "warfarin\|华法林" "aspirin\|阿司匹林" "surgery\|术前\|手术" "pregnan\|孕\|妊娠" "kidney\|肾病" "liver\|肝病"; do
      c=$(grep -ic "$kw" "$f" 2>/dev/null || echo 0)
      [ "$c" -gt 0 ] && count=$((count+1))
    done
    if [ "$count" -lt "$SAFETY_KEYWORDS_MIN" ]; then
      echo "  ⚠️ $f: only $count/6 safety keywords"
    else
      echo "  ✅ $f: $count/6 safety keywords"
    fi
  done
fi

echo ""
echo "================================================"
echo "  Audit complete. Review ⚠️ warnings and ❌ failures."
echo "  ❌ blocks publishing. ⚠️ documented in errata."
echo "================================================"
