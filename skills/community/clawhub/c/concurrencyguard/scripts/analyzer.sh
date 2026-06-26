#!/usr/bin/env bash
# ConcurrencyGuard -- Core Analysis Engine
# Provides: file discovery, pattern scanning, .gitignore-aware scanning,
#           allowlist support, score calculation, grades, report generation,
#           hook integration, watch mode, CI mode, team reports, baseline management.
#
# This file is sourced by concurrencyguard.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# --- Colors (safe to re-declare; sourcing scripts may set these) --------------

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
SKILL_DIR="${SKILL_DIR:-$(dirname "$SCRIPT_DIR")}"
CONCURRENCYGUARD_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

# ============================================================================
# File Discovery
# ============================================================================

# Source file extensions that are relevant for concurrency analysis
is_concurrency_relevant() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local ext="${basename_f##*.}"
  local ext_lower
  ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')

  case "$ext_lower" in
    # JavaScript / TypeScript
    js|jsx|ts|tsx|mjs|cjs) return 0 ;;
    # Python
    py|pyw) return 0 ;;
    # Java
    java) return 0 ;;
    # Go
    go) return 0 ;;
    # Rust
    rs) return 0 ;;
    # C#
    cs) return 0 ;;
    # Kotlin
    kt|kts) return 0 ;;
    # Scala
    scala) return 0 ;;
    # C/C++
    c|h|cpp|hpp|cc|hh|cxx|hxx) return 0 ;;
    # Ruby
    rb) return 0 ;;
    # PHP
    php) return 0 ;;
    # Swift
    swift) return 0 ;;
    # SQL (for transaction patterns)
    sql) return 0 ;;
    # Config / build files
    yaml|yml|toml|gradle) return 0 ;;
    *) return 1 ;;
  esac
}

# Check if a file should be skipped (binary, generated, vendor, etc.)
should_skip_file() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')
  local ext="${basename_lower##*.}"

  # Skip binary/image/compiled file extensions
  case "$ext" in
    png|jpg|jpeg|gif|bmp|ico|svg|webp|mp3|mp4|avi|mov|mkv|wav|flac|ogg) return 0 ;;
    zip|tar|gz|bz2|xz|7z|rar|tgz) return 0 ;;
    exe|dll|so|dylib|o|a|class|pyc|pyo|wasm) return 0 ;;
    woff|woff2|ttf|eot|otf) return 0 ;;
    pdf|doc|docx|xls|xlsx|ppt|pptx) return 0 ;;
    lock) return 0 ;;
    map) return 0 ;;
  esac

  # Skip minified files
  case "$basename_lower" in
    *.min.js|*.min.css|*.min.mjs) return 0 ;;
    *.bundle.js|*.chunk.js) return 0 ;;
  esac

  # Skip known non-source files
  case "$basename_lower" in
    package-lock.json|yarn.lock|pnpm-lock.yaml|composer.lock|gemfile.lock|cargo.lock|poetry.lock) return 0 ;;
    .ds_store|thumbs.db|desktop.ini) return 0 ;;
  esac

  # Only analyze concurrency-relevant file types
  if ! is_concurrency_relevant "$filepath"; then
    return 0
  fi

  return 1
}

# Check if a path is in a directory that should be skipped
is_excluded_dir() {
  local filepath="$1"

  case "$filepath" in
    */.git/*|*/.git) return 0 ;;
    */node_modules/*|*/node_modules) return 0 ;;
    */vendor/*|*/vendor) return 0 ;;
    */.next/*|*/.next) return 0 ;;
    */dist/*|*/dist) return 0 ;;
    */build/*|*/build) return 0 ;;
    */coverage/*|*/coverage) return 0 ;;
    */__pycache__/*|*/__pycache__) return 0 ;;
    */.venv/*|*/.venv) return 0 ;;
    */venv/*|*/venv) return 0 ;;
    */.tox/*|*/.tox) return 0 ;;
    */.eggs/*|*/.eggs) return 0 ;;
    */.terraform/*|*/.terraform) return 0 ;;
    */.cache/*|*/.cache) return 0 ;;
    */target/*|*/target) return 0 ;;
    */bin/*|*/obj/*) return 0 ;;
  esac

  return 1
}

# Check if a file is ignored by .gitignore
is_gitignored() {
  local filepath="$1"

  if command -v git &>/dev/null; then
    if git rev-parse --git-dir &>/dev/null 2>&1; then
      if git check-ignore -q "$filepath" 2>/dev/null; then
        return 0
      fi
    fi
  fi

  return 1
}

# Find all scannable files in a directory tree
find_scannable_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  if [[ -f "$search_dir" ]]; then
    if ! should_skip_file "$search_dir"; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  while IFS= read -r -d '' file; do
    # Skip excluded directories
    is_excluded_dir "$file" && continue

    # Skip binary/generated files
    should_skip_file "$file" && continue

    # Skip gitignored files
    is_gitignored "$file" && continue

    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 10 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".next" \
       -o -name "dist" -o -name "build" -o -name "coverage" -o -name "__pycache__" \
       -o -name ".venv" -o -name "venv" -o -name ".tox" -o -name ".terraform" \
       -o -name ".cache" -o -name "target" -o -name "bin" -o -name "obj" \) -prune -o \
    -type f -print0 2>/dev/null)
}

# ============================================================================
# Allowlist Support
# ============================================================================

declare -a ALLOWLIST_PATTERNS=()

load_allowlist() {
  local search_dir="${1:-.}"
  ALLOWLIST_PATTERNS=()

  local allowlist_file=""

  if [[ -f "$search_dir/.concurrencyguard-allowlist" ]]; then
    allowlist_file="$search_dir/.concurrencyguard-allowlist"
  fi

  if [[ -z "$allowlist_file" ]] && command -v git &>/dev/null; then
    local repo_root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
    if [[ -n "$repo_root" && -f "$repo_root/.concurrencyguard-allowlist" ]]; then
      allowlist_file="$repo_root/.concurrencyguard-allowlist"
    fi
  fi

  # Read from openclaw.json config
  local config_allowlist=""
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    if command -v python3 &>/dev/null; then
      config_allowlist=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    af = cfg.get('skills', {}).get('entries', {}).get('concurrencyguard', {}).get('config', {}).get('allowlistFile', '')
    print(af)
except: pass
" 2>/dev/null)
    fi

    if [[ -n "$config_allowlist" && -f "$search_dir/$config_allowlist" ]]; then
      allowlist_file="$search_dir/$config_allowlist"
    fi
  fi

  if [[ -n "$allowlist_file" && -f "$allowlist_file" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" || "$line" == \#* ]] && continue
      ALLOWLIST_PATTERNS+=("$line")
    done < "$allowlist_file"
  fi
}

is_allowlisted() {
  local finding="$1"

  for pattern in "${ALLOWLIST_PATTERNS[@]}"; do
    if echo "$finding" | grep -qF "$pattern" 2>/dev/null; then
      return 0
    fi
  done

  return 1
}

# ============================================================================
# Baseline Support
# ============================================================================

declare -a BASELINE_HASHES=()

load_baseline() {
  local search_dir="${1:-.}"
  BASELINE_HASHES=()

  local baseline_file=""

  if [[ -f "$search_dir/.concurrencyguard-baseline.json" ]]; then
    baseline_file="$search_dir/.concurrencyguard-baseline.json"
  fi

  if [[ -z "$baseline_file" ]] && command -v git &>/dev/null; then
    local repo_root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
    if [[ -n "$repo_root" && -f "$repo_root/.concurrencyguard-baseline.json" ]]; then
      baseline_file="$repo_root/.concurrencyguard-baseline.json"
    fi
  fi

  if [[ -n "$baseline_file" && -f "$baseline_file" ]]; then
    if command -v python3 &>/dev/null; then
      while IFS= read -r hash; do
        [[ -n "$hash" ]] && BASELINE_HASHES+=("$hash")
      done < <(python3 -c "
import json
try:
    with open('$baseline_file') as f:
        data = json.load(f)
    for h in data.get('hashes', []):
        print(h)
except: pass
" 2>/dev/null)
    fi
  fi
}

finding_hash() {
  local finding="$1"
  local file line severity check_id
  IFS='|' read -r file line severity check_id _ _ _ <<< "$finding"
  echo "${file}:${line}:${check_id}" | md5sum 2>/dev/null | cut -d' ' -f1 || \
  echo "${file}:${line}:${check_id}" | openssl md5 2>/dev/null | awk '{print $NF}' || \
  echo "${file}:${line}:${check_id}"
}

is_baselined() {
  local finding="$1"
  local hash
  hash=$(finding_hash "$finding")

  for baseline_hash in "${BASELINE_HASHES[@]}"; do
    if [[ "$hash" == "$baseline_hash" ]]; then
      return 0
    fi
  done

  return 1
}

# ============================================================================
# Pattern Scanning
# ============================================================================

# Scan a single file against all concurrency pattern categories.
# Appends findings to global FINDINGS array.
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
scan_file_with_patterns() {
  local filepath="$1"

  local categories
  categories=$(get_all_concurrencyguard_categories)

  for category in $categories; do
    local patterns_name
    patterns_name=$(get_concurrencyguard_patterns_for_category "$category")

    if [[ -z "$patterns_name" ]]; then
      continue
    fi

    local -n _patterns_ref="$patterns_name"

    for entry in "${_patterns_ref[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

      # Use grep -nE to find matches with line numbers
      local matches
      matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local matched_text="${match_line#*:}"
          # Trim whitespace
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
          # Truncate long lines
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi

          local finding="${filepath}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}"

          # Check allowlist
          if [[ ${#ALLOWLIST_PATTERNS[@]} -gt 0 ]] && is_allowlisted "$finding"; then
            continue
          fi

          # Check baseline
          if [[ ${#BASELINE_HASHES[@]} -gt 0 ]] && is_baselined "$finding"; then
            continue
          fi

          FINDINGS+=("$finding")
        done <<< "$matches"
      fi
    done
  done
}

# ============================================================================
# Score Calculation & Grading
# ============================================================================

# Calculate a concurrency safety score based on findings.
# Score starts at 100 (clean) and decreases with each finding.
# critical=25pts, high=15pts, medium=8pts, low=3pts
calculate_score() {
  local score=100

  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _file _line severity _check_id _desc _rec _text <<< "$finding"
    local points
    points=$(severity_to_points "$severity")
    score=$((score - points))
  done

  # Floor at 0
  if [[ $score -lt 0 ]]; then
    score=0
  fi

  echo "$score"
}

# Convert score to letter grade
score_to_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 60 ]]; then echo "D"
  else echo "F"
  fi
}

# Grade color
grade_color() {
  local grade="$1"
  case "$grade" in
    A) echo "$GREEN" ;;
    B) echo "$GREEN" ;;
    C) echo "$YELLOW" ;;
    D) echo "$YELLOW" ;;
    F) echo "$RED" ;;
    *) echo "$NC" ;;
  esac
}

# Severity color
severity_color() {
  local severity="$1"
  case "$severity" in
    critical) echo "$RED" ;;
    high)     echo "$MAGENTA" ;;
    medium)   echo "$YELLOW" ;;
    low)      echo "$CYAN" ;;
    *)        echo "$NC" ;;
  esac
}

# ============================================================================
# Output Formatting
# ============================================================================

print_findings() {
  local count=0
  local crit_count=0
  local high_count=0
  local med_count=0
  local low_count=0

  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    count=$((count + 1))

    case "$severity" in
      critical) crit_count=$((crit_count + 1)) ;;
      high)     high_count=$((high_count + 1)) ;;
      medium)   med_count=$((med_count + 1)) ;;
      low)      low_count=$((low_count + 1)) ;;
    esac

    local sev_col
    sev_col=$(severity_color "$severity")

    echo -e "  ${sev_col}${severity^^}${NC} ${DIM}${check_id}${NC} ${file}:${line}"
    echo -e "    ${description}"
    echo -e "    ${DIM}Matched: ${matched_text}${NC}"
    echo -e "    ${DIM}Fix: ${recommendation}${NC}"
    echo ""
  done

  echo -e "${BOLD}--- Summary ---${NC}"
  echo -e "  Total findings: ${BOLD}$count${NC}"
  if [[ $crit_count -gt 0 ]]; then
    echo -e "  ${RED}Critical: $crit_count${NC}"
  fi
  if [[ $high_count -gt 0 ]]; then
    echo -e "  ${MAGENTA}High: $high_count${NC}"
  fi
  if [[ $med_count -gt 0 ]]; then
    echo -e "  ${YELLOW}Medium: $med_count${NC}"
  fi
  if [[ $low_count -gt 0 ]]; then
    echo -e "  ${CYAN}Low: $low_count${NC}"
  fi
}

print_score() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local gc
  gc=$(grade_color "$grade")

  echo ""
  echo -e "${BOLD}Concurrency Safety Score: ${gc}${score}/100${NC} (Grade: ${gc}${BOLD}${grade}${NC})"

  if [[ $score -ge 70 ]]; then
    echo -e "${GREEN}PASS${NC} -- Score is above threshold (70)"
  else
    echo -e "${RED}FAIL${NC} -- Score is below threshold (70)"
  fi
}

# ============================================================================
# Main Scan Function (FREE)
# ============================================================================

# do_concurrency_scan <target> <file_limit>
# file_limit: max files for free tier (0 = unlimited)
do_concurrency_scan() {
  local target="${1:-.}"
  local file_limit="${2:-0}"
  FINDINGS=()

  # Load allowlist
  load_allowlist "$target"

  # Load baseline if exists
  load_baseline "$target"

  # Discover files
  local -a files=()
  find_scannable_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[ConcurrencyGuard]${NC} No scannable source files found in ${BOLD}$target${NC}"
    echo -e "  Clean scan -- no files to check."
    return 0
  fi

  # Apply file limit for free tier
  local scan_count=$total_files
  local limited=false
  if [[ $file_limit -gt 0 && $total_files -gt $file_limit ]]; then
    scan_count=$file_limit
    limited=true
    echo -e "${YELLOW}[ConcurrencyGuard]${NC} Free tier: scanning $file_limit of $total_files files"
    echo -e "  ${DIM}Upgrade to Pro for unlimited scans: https://concurrencyguard.pages.dev/pricing${NC}"
    echo ""
  fi

  echo -e "${BLUE}[ConcurrencyGuard]${NC} Scanning ${BOLD}$scan_count${NC} files for concurrency issues..."
  echo ""

  local i=0
  for filepath in "${files[@]}"; do
    if [[ $file_limit -gt 0 && $i -ge $file_limit ]]; then
      break
    fi

    scan_file_with_patterns "$filepath"
    i=$((i + 1))
  done

  # Print results
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No concurrency issues detected!${NC}"
    echo ""
    echo -e "Concurrency Safety Score: ${GREEN}${BOLD}100/100${NC} (Grade: ${GREEN}${BOLD}A${NC})"
    echo -e "${GREEN}PASS${NC}"
    return 0
  fi

  print_findings

  local score
  score=$(calculate_score)
  print_score "$score"

  if [[ $limited == true ]]; then
    echo ""
    echo -e "${YELLOW}Note:${NC} Only $file_limit of $total_files files were scanned (free tier limit)."
    echo -e "  Upgrade to Pro for a complete scan: ${CYAN}https://concurrencyguard.pages.dev/pricing${NC}"
  fi

  # Exit code
  if [[ $score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# ============================================================================
# Report Generation (FREE)
# ============================================================================

generate_concurrency_report() {
  local target="${1:-.}"
  FINDINGS=()

  load_allowlist "$target"
  load_baseline "$target"

  local -a files=()
  find_scannable_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[ConcurrencyGuard]${NC} No scannable files found."
    return 0
  fi

  echo -e "${BLUE}[ConcurrencyGuard]${NC} Scanning ${BOLD}$total_files${NC} files for report..." >&2

  for filepath in "${files[@]}"; do
    scan_file_with_patterns "$filepath"
  done

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Count severities
  local crit_count=0 high_count=0 med_count=0 low_count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    case "$severity" in
      critical) crit_count=$((crit_count + 1)) ;;
      high)     high_count=$((high_count + 1)) ;;
      medium)   med_count=$((med_count + 1)) ;;
      low)      low_count=$((low_count + 1)) ;;
    esac
  done

  local total_issues=${#FINDINGS[@]}

  # Build category breakdown
  local cat_breakdown=""
  local -A cat_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ _ check_id _ _ _ <<< "$finding"
    local prefix="${check_id%%-*}"
    cat_counts["$prefix"]=$(( ${cat_counts["$prefix"]:-0} + 1 ))
  done

  for cat in "${!cat_counts[@]}"; do
    local cat_label
    case "$cat" in
      SS) cat_label="Shared State" ;;
      LK) cat_label="Locking & Mutex" ;;
      TC) cat_label="TOCTOU & Atomicity" ;;
      AW) cat_label="Async/Await Pitfalls" ;;
      TS) cat_label="Thread Safety" ;;
      DL) cat_label="Deadlock & Starvation" ;;
      *)  cat_label="$cat" ;;
    esac
    cat_breakdown="${cat_breakdown}| ${cat_label} | ${cat_counts[$cat]} |"$'\n'
  done

  # Build findings table
  local findings_table=""
  local idx=0
  for finding in "${FINDINGS[@]}"; do
    idx=$((idx + 1))
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    findings_table="${findings_table}| ${idx} | ${file} | ${line} | ${severity} | ${check_id} | ${description} |"$'\n'
  done

  # Build recommendations
  local recommendations=""
  if [[ $crit_count -gt 0 ]]; then
    recommendations="${recommendations}1. **CRITICAL:** ${crit_count} critical concurrency issues found -- fix immediately to prevent data corruption"$'\n'
  fi
  if [[ $high_count -gt 0 ]]; then
    recommendations="${recommendations}2. **HIGH:** ${high_count} high-severity findings -- address in current sprint"$'\n'
  fi
  if [[ $med_count -gt 0 ]]; then
    recommendations="${recommendations}3. **MEDIUM:** ${med_count} medium findings -- review and refactor"$'\n'
  fi
  if [[ $low_count -gt 0 ]]; then
    recommendations="${recommendations}4. **LOW:** ${low_count} low findings -- review for false positives"$'\n'
  fi

  # Get project name
  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd)" 2>/dev/null || echo "$target")

  # Read template and substitute
  local template_file="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_file" ]]; then
    echo -e "${RED}[ConcurrencyGuard]${NC} Report template not found: $template_file" >&2
    return 1
  fi

  local report
  report=$(cat "$template_file")
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{VERSION\}\}/$CONCURRENCYGUARD_VERSION}"
  report="${report//\{\{DATE\}\}/$date_str}"
  report="${report//\{\{CONCURRENCY_SCORE\}\}/$score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$total_files}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total_issues}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$crit_count}"
  report="${report//\{\{HIGH_COUNT\}\}/$high_count}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$med_count}"
  report="${report//\{\{LOW_COUNT\}\}/$low_count}"
  report="${report//\{\{CATEGORY_BREAKDOWN\}\}/$cat_breakdown}"
  report="${report//\{\{FINDINGS_TABLE\}\}/$findings_table}"
  report="${report//\{\{RECOMMENDATIONS\}\}/$recommendations}"

  echo "$report"

  echo "" >&2
  echo -e "${GREEN}[ConcurrencyGuard]${NC} Report generated. Score: ${BOLD}$score/100${NC} (Grade: ${BOLD}$grade${NC})" >&2
}

# ============================================================================
# Watch Mode (PRO+)
# ============================================================================

watch_mode() {
  local target="${1:-.}"

  echo -e "${BLUE}[ConcurrencyGuard]${NC} Watch mode started on ${BOLD}$target${NC}"
  echo -e "  ${DIM}Press Ctrl+C to stop${NC}"
  echo ""

  # Use filesystem polling as a fallback (works everywhere)
  local -A file_mtimes=()

  # Initial scan
  local -a files=()
  find_scannable_files "$target" files

  for filepath in "${files[@]}"; do
    local mtime
    mtime=$(stat -c %Y "$filepath" 2>/dev/null || stat -f %m "$filepath" 2>/dev/null || echo "0")
    file_mtimes["$filepath"]="$mtime"
  done

  echo -e "${GREEN}[ConcurrencyGuard]${NC} Watching ${#files[@]} files. Initial scan..."
  echo ""

  # Run initial scan
  FINDINGS=()
  load_allowlist "$target"
  load_baseline "$target"

  for filepath in "${files[@]}"; do
    scan_file_with_patterns "$filepath"
  done

  if [[ ${#FINDINGS[@]} -gt 0 ]]; then
    print_findings
    local score
    score=$(calculate_score)
    print_score "$score"
  else
    echo -e "${GREEN}${BOLD}Clean!${NC} No concurrency issues detected."
  fi

  echo ""
  echo -e "${DIM}Watching for changes...${NC}"

  # Poll loop
  while true; do
    sleep 2

    local changed=false
    local -a changed_files=()

    find_scannable_files "$target" files

    for filepath in "${files[@]}"; do
      local mtime
      mtime=$(stat -c %Y "$filepath" 2>/dev/null || stat -f %m "$filepath" 2>/dev/null || echo "0")
      local prev_mtime="${file_mtimes[$filepath]:-0}"

      if [[ "$mtime" != "$prev_mtime" ]]; then
        changed=true
        changed_files+=("$filepath")
        file_mtimes["$filepath"]="$mtime"
      fi
    done

    if [[ "$changed" == true ]]; then
      echo ""
      echo -e "${BLUE}[ConcurrencyGuard]${NC} Changes detected in ${#changed_files[@]} file(s). Rescanning..."

      FINDINGS=()
      for filepath in "${changed_files[@]}"; do
        scan_file_with_patterns "$filepath"
      done

      if [[ ${#FINDINGS[@]} -gt 0 ]]; then
        print_findings
        local score
        score=$(calculate_score)
        print_score "$score"
      else
        echo -e "${GREEN}${BOLD}Clean!${NC} No new concurrency issues."
      fi

      echo ""
      echo -e "${DIM}Watching for changes...${NC}"
    fi
  done
}

# ============================================================================
# CI Mode (PRO+)
# ============================================================================

ci_mode() {
  local target="${1:-.}"
  FINDINGS=()

  load_allowlist "$target"
  load_baseline "$target"

  local -a files=()
  find_scannable_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo "::notice::ConcurrencyGuard: No scannable files found"
    exit 0
  fi

  for filepath in "${files[@]}"; do
    scan_file_with_patterns "$filepath"
  done

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")

  # Output GitHub Actions annotations
  local crit_count=0 high_count=0 med_count=0 low_count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"

    case "$severity" in
      critical)
        crit_count=$((crit_count + 1))
        echo "::error file=${file},line=${line}::${check_id}: ${description}"
        ;;
      high)
        high_count=$((high_count + 1))
        echo "::error file=${file},line=${line}::${check_id}: ${description}"
        ;;
      medium)
        med_count=$((med_count + 1))
        echo "::warning file=${file},line=${line}::${check_id}: ${description}"
        ;;
      low)
        low_count=$((low_count + 1))
        echo "::notice file=${file},line=${line}::${check_id}: ${description}"
        ;;
    esac
  done

  echo ""
  echo "ConcurrencyGuard CI Report"
  echo "========================="
  echo "Score: ${score}/100 (Grade: ${grade})"
  echo "Files scanned: ${total_files}"
  echo "Total issues: ${#FINDINGS[@]}"
  echo "Critical: ${crit_count} | High: ${high_count} | Medium: ${med_count} | Low: ${low_count}"

  # Exit codes: 0=clean, 1=critical/high, 2=medium
  if [[ $crit_count -gt 0 || $high_count -gt 0 ]]; then
    exit 1
  elif [[ $med_count -gt 0 ]]; then
    exit 2
  fi
  exit 0
}

# ============================================================================
# Team Report (TEAM+)
# ============================================================================

team_report() {
  local target="${1:-.}"
  FINDINGS=()

  load_allowlist "$target"
  load_baseline "$target"

  local -a files=()
  find_scannable_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[ConcurrencyGuard]${NC} No scannable files found."
    return 0
  fi

  echo -e "${BLUE}[ConcurrencyGuard]${NC} Generating team report for ${BOLD}$total_files${NC} files..." >&2

  for filepath in "${files[@]}"; do
    scan_file_with_patterns "$filepath"
  done

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Count severities
  local crit_count=0 high_count=0 med_count=0 low_count=0
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    case "$severity" in
      critical) crit_count=$((crit_count + 1)) ;;
      high)     high_count=$((high_count + 1)) ;;
      medium)   med_count=$((med_count + 1)) ;;
      low)      low_count=$((low_count + 1)) ;;
    esac
  done

  # Hotspot analysis: find files with most issues
  local -A file_issue_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file _ _ _ _ _ _ <<< "$finding"
    file_issue_counts["$file"]=$(( ${file_issue_counts["$file"]:-0} + 1 ))
  done

  # Category distribution
  local -A cat_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ _ check_id _ _ _ <<< "$finding"
    local prefix="${check_id%%-*}"
    cat_counts["$prefix"]=$(( ${cat_counts["$prefix"]:-0} + 1 ))
  done

  # Output team report
  echo "# ConcurrencyGuard Team Report"
  echo ""
  echo "> Generated on ${date_str} by ConcurrencyGuard v${CONCURRENCYGUARD_VERSION}"
  echo ""
  echo "## Overview"
  echo ""
  echo "| Metric | Value |"
  echo "|--------|-------|"
  echo "| Concurrency Safety Score | **${score}/100** (Grade: **${grade}**) |"
  echo "| Files Scanned | ${total_files} |"
  echo "| Total Issues | ${#FINDINGS[@]} |"
  echo "| Critical | ${crit_count} |"
  echo "| High | ${high_count} |"
  echo "| Medium | ${med_count} |"
  echo "| Low | ${low_count} |"
  echo ""
  echo "## Category Distribution"
  echo ""
  echo "| Category | Count |"
  echo "|----------|-------|"
  for cat in "${!cat_counts[@]}"; do
    local cat_label
    case "$cat" in
      SS) cat_label="Shared State" ;;
      LK) cat_label="Locking & Mutex" ;;
      TC) cat_label="TOCTOU & Atomicity" ;;
      AW) cat_label="Async/Await Pitfalls" ;;
      TS) cat_label="Thread Safety" ;;
      DL) cat_label="Deadlock & Starvation" ;;
      *)  cat_label="$cat" ;;
    esac
    echo "| ${cat_label} | ${cat_counts[$cat]} |"
  done
  echo ""
  echo "## Hotspot Files"
  echo ""
  echo "| File | Issues |"
  echo "|------|--------|"
  # Sort by count (simple approach: iterate)
  for file in "${!file_issue_counts[@]}"; do
    echo "| ${file} | ${file_issue_counts[$file]} |"
  done | sort -t'|' -k3 -rn | head -10
  echo ""

  # Git blame integration if available
  if command -v git &>/dev/null && git rev-parse --git-dir &>/dev/null 2>&1; then
    echo "## Author Distribution"
    echo ""
    echo "| Author | Issues |"
    echo "|--------|--------|"
    local -A author_counts=()
    for finding in "${FINDINGS[@]}"; do
      IFS='|' read -r file line _ _ _ _ _ <<< "$finding"
      if [[ -f "$file" ]]; then
        local author
        author=$(git blame -L "${line},${line}" --porcelain "$file" 2>/dev/null | grep "^author " | sed 's/^author //' || echo "unknown")
        author_counts["$author"]=$(( ${author_counts["$author"]:-0} + 1 ))
      fi
    done
    for author in "${!author_counts[@]}"; do
      echo "| ${author} | ${author_counts[$author]} |"
    done | sort -t'|' -k3 -rn
    echo ""
  fi

  echo "---"
  echo ""
  echo "*Report generated by [ConcurrencyGuard](https://concurrencyguard.pages.dev). Run \`concurrencyguard scan\` for interactive results.*"

  echo "" >&2
  echo -e "${GREEN}[ConcurrencyGuard]${NC} Team report generated. Score: ${BOLD}$score/100${NC} (Grade: ${BOLD}$grade${NC})" >&2
}

# ============================================================================
# Baseline Management (TEAM+)
# ============================================================================

baseline_mode() {
  local target="${1:-.}"
  FINDINGS=()

  # Scan without loading existing baseline
  BASELINE_HASHES=()
  load_allowlist "$target"

  local -a files=()
  find_scannable_files "$target" files

  for filepath in "${files[@]}"; do
    scan_file_with_patterns "$filepath"
  done

  # Compute hashes for all findings
  local hashes_json="["
  local first=true
  for finding in "${FINDINGS[@]}"; do
    local hash
    hash=$(finding_hash "$finding")
    if [[ "$first" == true ]]; then
      first=false
    else
      hashes_json="${hashes_json},"
    fi
    hashes_json="${hashes_json}\"${hash}\""
  done
  hashes_json="${hashes_json}]"

  local date_str
  date_str=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%d 2>/dev/null || echo "unknown")

  local baseline_file="$target/.concurrencyguard-baseline.json"

  if command -v python3 &>/dev/null; then
    python3 -c "
import json
data = {
    'version': '1.0.0',
    'created': '$date_str',
    'tool': 'concurrencyguard',
    'total_findings': ${#FINDINGS[@]},
    'hashes': json.loads('$hashes_json')
}
with open('$baseline_file', 'w') as f:
    json.dump(data, f, indent=2)
print('OK')
" 2>/dev/null
  else
    # Fallback: write JSON manually
    cat > "$baseline_file" <<BASELINE_EOF
{
  "version": "1.0.0",
  "created": "${date_str}",
  "tool": "concurrencyguard",
  "total_findings": ${#FINDINGS[@]},
  "hashes": ${hashes_json}
}
BASELINE_EOF
  fi

  echo -e "${GREEN}[ConcurrencyGuard]${NC} Baseline created: ${BOLD}$baseline_file${NC}"
  echo -e "  ${#FINDINGS[@]} findings baselined."
  echo -e "  Future scans will only report NEW concurrency issues not in this baseline."
}

# ============================================================================
# Hook Integration
# ============================================================================

# Called by lefthook pre-commit hook
hook_concurrency_scan() {
  # Get list of staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  FINDINGS=()
  load_allowlist "."
  load_baseline "."

  local file_count=0
  while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    [[ ! -f "$filepath" ]] && continue

    # Skip excluded dirs and binary files
    is_excluded_dir "$filepath" && continue
    should_skip_file "$filepath" && continue

    scan_file_with_patterns "$filepath"
    file_count=$((file_count + 1))
  done <<< "$staged_files"

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[ConcurrencyGuard]${NC} No concurrency issues detected in $file_count staged files."
    return 0
  fi

  # Check if any critical or high findings exist
  local has_blocking=false
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_blocking=true
      break
    fi
  done

  echo -e "${RED}${BOLD}[ConcurrencyGuard] Concurrency issues detected in staged files!${NC}"
  echo ""
  print_findings

  local score
  score=$(calculate_score)
  print_score "$score"

  if [[ "$has_blocking" == true ]]; then
    echo ""
    echo -e "${RED}Commit blocked.${NC} Fix concurrency issues before committing."
    echo -e "  Run: ${CYAN}concurrencyguard scan${NC} for details"
    echo -e "  Skip: ${DIM}git commit --no-verify${NC} (not recommended)"
    return 1
  fi

  return 0
}
