#!/usr/bin/env bash
# AuthAudit -- Core Analysis Engine
# Provides: file discovery, pattern scanning, score calculation, category
#           breakdown, report generation, JSON/HTML output, and hook support.
#
# Sourced by dispatcher.sh. Requires patterns.sh and license.sh.

set -euo pipefail

# ─── Colors (safe to re-declare) ────────────────────────────────────────────

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

AUTHAUDIT_VERSION="${VERSION:-1.0.0}"

# ─── Globals / Accumulators ─────────────────────────────────────────────────

TOTAL_FILES_SCANNED=0
TOTAL_ISSUES=0
CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0
LOW_COUNT=0
ALL_FINDINGS=""
CATEGORY_FINDINGS_AC=0
CATEGORY_FINDINGS_SM=0
CATEGORY_FINDINGS_AZ=0
CATEGORY_FINDINGS_TK=0
CATEGORY_FINDINGS_CS=0
CATEGORY_FINDINGS_PW=0

# ─── Severity Weights ───────────────────────────────────────────────────────

declare -A SEVERITY_WEIGHTS=(
  [critical]=25
  [high]=15
  [medium]=8
  [low]=3
)

# ─── Grade Thresholds ───────────────────────────────────────────────────────

PASS_THRESHOLD=70

# ─── Exclude Directories ────────────────────────────────────────────────────

EXCLUDE_DIRS=(".git" "node_modules" "dist" "build" "vendor" "__pycache__" ".next"
              ".nuxt" "coverage" ".venv" "venv" "env" ".tox" "target" "bin" "obj"
              ".gradle" ".mvn" "bower_components" "packages" ".dart_tool")

# File extensions to scan
SCAN_EXTENSIONS=("js" "ts" "jsx" "tsx" "py" "rb" "go" "java" "php" "cs" "rs"
                 "kt" "scala" "vue" "svelte" "mjs" "cjs")

should_exclude() {
  local filepath="$1"
  local d
  for d in "${EXCLUDE_DIRS[@]}"; do
    if [[ "$filepath" == *"/$d/"* || "$filepath" == *"\\$d\\"* || "$filepath" == "$d/"* ]]; then
      return 0
    fi
  done
  return 1
}

is_scannable_file() {
  local filepath="$1"
  local ext="${filepath##*.}"
  local e
  for e in "${SCAN_EXTENSIONS[@]}"; do
    if [[ "$ext" == "$e" ]]; then
      return 0
    fi
  done
  return 1
}

# ─── File Discovery ─────────────────────────────────────────────────────────
# Find source files to scan, excluding irrelevant directories.

find_source_files() {
  local target="$1"

  if [[ -f "$target" ]]; then
    echo "$target"
    return
  fi

  local ext
  for ext in "${SCAN_EXTENSIONS[@]}"; do
    while IFS= read -r f; do
      [[ -z "$f" ]] && continue
      should_exclude "$f" && continue
      echo "$f"
    done < <(find "$target" -name "*.$ext" -type f 2>/dev/null)
  done
}

# ─── Pattern Scanning Engine ────────────────────────────────────────────────
# Scans a single file against all enabled patterns.

scan_file() {
  local filepath="$1"
  local pattern_limit="${2:-15}"
  local target_category="${3:-}"
  local findings=""

  # Skip binary files
  if file "$filepath" 2>/dev/null | grep -qE '(binary|executable|ELF|Mach-O)'; then
    return
  fi

  local cat_idx=0
  local category
  for category in "${AUTHAUDIT_CATEGORIES[@]}"; do
    # If a specific category is requested, skip others
    if [[ -n "$target_category" && "$category" != "$target_category" ]]; then
      cat_idx=$((cat_idx + 1))
      continue
    fi

    local arr_name="${category}_PATTERNS"
    local -n patterns_ref="$arr_name" 2>/dev/null || continue

    local count=0
    local entry
    for entry in "${patterns_ref[@]}"; do
      if [[ $count -ge $pattern_limit ]]; then
        break
      fi
      count=$((count + 1))

      # Parse pattern entry: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
      local regex severity check_id description recommendation
      regex=$(echo "$entry" | cut -d'|' -f1)
      severity=$(echo "$entry" | cut -d'|' -f2)
      check_id=$(echo "$entry" | cut -d'|' -f3)
      description=$(echo "$entry" | cut -d'|' -f4)
      recommendation=$(echo "$entry" | cut -d'|' -f5)

      # Skip empty patterns
      [[ -z "$regex" ]] && continue

      # Search for pattern matches
      local line_matches
      line_matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$line_matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue

          local line_num="${match_line%%:*}"
          local line_content="${match_line#*:}"

          # Trim long lines
          if [[ ${#line_content} -gt 150 ]]; then
            line_content="${line_content:0:150}..."
          fi

          # Strip leading/trailing whitespace from line content
          line_content=$(echo "$line_content" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

          findings+="${filepath}|${line_num}|${check_id}|${severity}|${description}|${recommendation}|${line_content}|${category}"$'\n'

          # Increment counters
          TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
          case "$severity" in
            critical) CRITICAL_COUNT=$((CRITICAL_COUNT + 1)) ;;
            high)     HIGH_COUNT=$((HIGH_COUNT + 1)) ;;
            medium)   MEDIUM_COUNT=$((MEDIUM_COUNT + 1)) ;;
            low)      LOW_COUNT=$((LOW_COUNT + 1)) ;;
          esac

          # Increment category counter
          case "$category" in
            AC) CATEGORY_FINDINGS_AC=$((CATEGORY_FINDINGS_AC + 1)) ;;
            SM) CATEGORY_FINDINGS_SM=$((CATEGORY_FINDINGS_SM + 1)) ;;
            AZ) CATEGORY_FINDINGS_AZ=$((CATEGORY_FINDINGS_AZ + 1)) ;;
            TK) CATEGORY_FINDINGS_TK=$((CATEGORY_FINDINGS_TK + 1)) ;;
            CS) CATEGORY_FINDINGS_CS=$((CATEGORY_FINDINGS_CS + 1)) ;;
            PW) CATEGORY_FINDINGS_PW=$((CATEGORY_FINDINGS_PW + 1)) ;;
          esac
        done <<< "$line_matches"
      fi
    done

    cat_idx=$((cat_idx + 1))
  done

  TOTAL_FILES_SCANNED=$((TOTAL_FILES_SCANNED + 1))
  ALL_FINDINGS+="$findings"

  echo -n "$findings"
}

# ─── Score Calculation ───────────────────────────────────────────────────────
# Score 0-100 based on severity-weighted findings.
#
# Formula:
#   penalty = (critical * 25) + (high * 15) + (medium * 8) + (low * 3)
#   scaling_factor = files_scanned + 10  (more files = smaller per-issue impact)
#   adjusted_penalty = (penalty * 20) / scaling_factor
#   score = max(0, min(100, 100 - adjusted_penalty))

calculate_score() {
  local files="${1:-$TOTAL_FILES_SCANNED}"
  local critical="${2:-$CRITICAL_COUNT}"
  local high="${3:-$HIGH_COUNT}"
  local medium="${4:-$MEDIUM_COUNT}"
  local low="${5:-$LOW_COUNT}"

  local score=100

  # Raw penalty
  local penalty=0
  penalty=$(( critical * 25 + high * 15 + medium * 8 + low * 3 ))

  # Scale penalty by codebase size
  if [[ $files -gt 0 ]]; then
    local scaling=$((files + 10))
    local adjusted=$(( (penalty * 20) / scaling ))
    score=$((100 - adjusted))
  else
    score=$((100 - penalty))
  fi

  # Clamp to 0-100
  [[ $score -lt 0 ]] && score=0
  [[ $score -gt 100 ]] && score=100

  echo "$score"
}

# ─── Grade Conversion ───────────────────────────────────────────────────────

get_grade() {
  local score="$1"
  if   [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 60 ]]; then echo "D"
  else echo "F"
  fi
}

get_score_color() {
  local score="$1"
  if   [[ $score -ge 90 ]]; then echo "$GREEN"
  elif [[ $score -ge 70 ]]; then echo "$YELLOW"
  else echo "$RED"
  fi
}

# ─── Severity Formatting ────────────────────────────────────────────────────

severity_color() {
  case "$1" in
    critical) echo "$RED" ;;
    high)     echo "$YELLOW" ;;
    medium)   echo "$BLUE" ;;
    low)      echo "$DIM" ;;
    *)        echo "$NC" ;;
  esac
}

severity_icon() {
  case "$1" in
    critical) echo "[CRIT]" ;;
    high)     echo "[HIGH]" ;;
    medium)   echo "[MED] " ;;
    low)      echo "[LOW] " ;;
    *)        echo "      " ;;
  esac
}

# ─── Text Output Formatting ─────────────────────────────────────────────────

print_finding() {
  local filepath="$1" line_num="$2" check_id="$3" severity="$4"
  local description="$5" recommendation="$6" line_content="$7" category="${8:-}"

  local color
  color=$(severity_color "$severity")
  local icon
  icon=$(severity_icon "$severity")

  echo -e "  ${color}${BOLD}${icon} ${check_id}${NC}  ${description}"
  echo -e "    ${DIM}${filepath}:${line_num}${NC}"
  if [[ -n "$line_content" ]]; then
    echo -e "    ${DIM}> ${line_content}${NC}"
  fi
  echo -e "    ${CYAN}Fix: ${recommendation}${NC}"
  echo ""
}

print_all_findings() {
  local findings="$1"
  [[ -z "$findings" ]] && return

  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local filepath line_num check_id severity description recommendation line_content category
    IFS='|' read -r filepath line_num check_id severity description recommendation line_content category <<< "$line"
    print_finding "$filepath" "$line_num" "$check_id" "$severity" "$description" "$recommendation" "$line_content" "$category"
  done <<< "$findings"
}

# ─── Category Breakdown ─────────────────────────────────────────────────────

print_category_breakdown() {
  echo -e "  ${BOLD}Category Breakdown:${NC}"
  echo ""
  local i=0
  local cat
  for cat in "${AUTHAUDIT_CATEGORIES[@]}"; do
    local cat_name="${AUTHAUDIT_CATEGORY_NAMES[$i]}"
    local cat_count=0
    case "$cat" in
      AC) cat_count=$CATEGORY_FINDINGS_AC ;;
      SM) cat_count=$CATEGORY_FINDINGS_SM ;;
      AZ) cat_count=$CATEGORY_FINDINGS_AZ ;;
      TK) cat_count=$CATEGORY_FINDINGS_TK ;;
      CS) cat_count=$CATEGORY_FINDINGS_CS ;;
      PW) cat_count=$CATEGORY_FINDINGS_PW ;;
    esac

    if [[ $cat_count -gt 0 ]]; then
      echo -e "    ${YELLOW}${cat}${NC} ${cat_name}: ${BOLD}${cat_count}${NC} issue(s)"
    else
      echo -e "    ${GREEN}${cat}${NC} ${cat_name}: ${DIM}0 issues${NC}"
    fi
    i=$((i + 1))
  done
  echo ""
}

# ─── Text Output (default) ──────────────────────────────────────────────────

output_text() {
  local score="$1"
  local grade="$2"
  local pattern_count="$3"
  local pattern_limit="$4"
  local target_category="${5:-}"

  local score_color
  score_color=$(get_score_color "$score")

  echo ""
  echo -e "  ${BOLD}AuthAudit Security Scan Results${NC}"
  echo -e "  ================================================================"
  echo ""
  echo -e "  Security Score: ${score_color}${BOLD}${score}/100 (${grade})${NC}"
  echo ""
  echo -e "  ${DIM}Files scanned:${NC}   ${TOTAL_FILES_SCANNED}"
  echo -e "  ${DIM}Patterns used:${NC}   ${pattern_count}"
  echo -e "  ${DIM}Total issues:${NC}    ${TOTAL_ISSUES}"

  if [[ $TOTAL_ISSUES -gt 0 ]]; then
    echo ""
    [[ $CRITICAL_COUNT -gt 0 ]] && echo -e "  ${RED}  Critical:${NC}  ${CRITICAL_COUNT}"
    [[ $HIGH_COUNT -gt 0 ]]     && echo -e "  ${YELLOW}  High:${NC}      ${HIGH_COUNT}"
    [[ $MEDIUM_COUNT -gt 0 ]]   && echo -e "  ${BLUE}  Medium:${NC}    ${MEDIUM_COUNT}"
    [[ $LOW_COUNT -gt 0 ]]      && echo -e "  ${DIM}  Low:${NC}       ${LOW_COUNT}"
  fi

  echo ""

  # Category breakdown (unless filtering to single category)
  if [[ -z "$target_category" ]]; then
    print_category_breakdown
  fi

  # Detailed findings
  if [[ -n "$ALL_FINDINGS" ]]; then
    echo -e "  ${BOLD}Findings:${NC}"
    echo ""
    print_all_findings "$ALL_FINDINGS"
  else
    echo -e "  ${GREEN}No auth/authz issues found.${NC}"
  fi

  # Tier upgrade notice
  if [[ $pattern_limit -lt 15 ]]; then
    local total_patterns=$((pattern_limit * 6))
    echo -e "  ${YELLOW}-------------------------------------------------------------${NC}"
    echo -e "  ${YELLOW}NOTE:${NC} Scanned with ${total_patterns} of 90 patterns."
    if [[ $pattern_limit -le 5 ]]; then
      echo -e "  Upgrade to Pro for 60 patterns: ${CYAN}https://authaudit.dev/pricing${NC}"
    else
      echo -e "  Upgrade to Team for all 90 patterns: ${CYAN}https://authaudit.dev/pricing${NC}"
    fi
    echo -e "  ${YELLOW}-------------------------------------------------------------${NC}"
    echo ""
  fi

  # Pass/fail indicator
  if [[ $score -ge $PASS_THRESHOLD ]]; then
    echo -e "  ${GREEN}${BOLD}PASS${NC} -- Score ${score} meets threshold of ${PASS_THRESHOLD}"
  else
    echo -e "  ${RED}${BOLD}FAIL${NC} -- Score ${score} is below threshold of ${PASS_THRESHOLD}"
  fi
  echo ""
}

# ─── JSON Output ─────────────────────────────────────────────────────────────

output_json() {
  local score="$1"
  local grade="$2"
  local pattern_count="$3"
  local pass="true"
  [[ $score -lt $PASS_THRESHOLD ]] && pass="false"

  # Build findings array
  local findings_json="["
  local first=true
  if [[ -n "$ALL_FINDINGS" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local fp ln cid sev desc rec lc cat
      IFS='|' read -r fp ln cid sev desc rec lc cat <<< "$line"

      # Escape double quotes in content
      lc=$(echo "$lc" | sed 's/"/\\"/g')
      desc=$(echo "$desc" | sed 's/"/\\"/g')
      rec=$(echo "$rec" | sed 's/"/\\"/g')
      fp=$(echo "$fp" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')

      [[ "$first" == true ]] && first=false || findings_json+=","
      findings_json+="{\"file\":\"${fp}\",\"line\":${ln},\"checkId\":\"${cid}\",\"severity\":\"${sev}\",\"category\":\"${cat}\",\"description\":\"${desc}\",\"recommendation\":\"${rec}\",\"code\":\"${lc}\"}"
    done <<< "$ALL_FINDINGS"
  fi
  findings_json+="]"

  # Build category breakdown
  local categories_json="{\"AC\":${CATEGORY_FINDINGS_AC},\"SM\":${CATEGORY_FINDINGS_SM},\"AZ\":${CATEGORY_FINDINGS_AZ},\"TK\":${CATEGORY_FINDINGS_TK},\"CS\":${CATEGORY_FINDINGS_CS},\"PW\":${CATEGORY_FINDINGS_PW}}"

  # Output complete JSON
  cat <<EOF
{
  "tool": "authaudit",
  "version": "${AUTHAUDIT_VERSION}",
  "score": ${score},
  "grade": "${grade}",
  "pass": ${pass},
  "threshold": ${PASS_THRESHOLD},
  "summary": {
    "filesScanned": ${TOTAL_FILES_SCANNED},
    "patternsUsed": ${pattern_count},
    "totalIssues": ${TOTAL_ISSUES},
    "critical": ${CRITICAL_COUNT},
    "high": ${HIGH_COUNT},
    "medium": ${MEDIUM_COUNT},
    "low": ${LOW_COUNT}
  },
  "categories": ${categories_json},
  "findings": ${findings_json}
}
EOF
}

# ─── HTML Output ─────────────────────────────────────────────────────────────

output_html() {
  local score="$1"
  local grade="$2"
  local pattern_count="$3"

  local score_class="good"
  [[ $score -lt 90 ]] && score_class="ok"
  [[ $score -lt 70 ]] && score_class="bad"

  cat <<'HTMLHEAD'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AuthAudit Security Report</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 960px; margin: 0 auto; padding: 2rem; background: #0d1117; color: #c9d1d9; }
  h1 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem; }
  h2 { color: #79c0ff; margin-top: 2rem; }
  .score-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.5rem; margin: 1rem 0; text-align: center; }
  .score { font-size: 3rem; font-weight: bold; }
  .score.good { color: #3fb950; }
  .score.ok { color: #d29922; }
  .score.bad { color: #f85149; }
  .grade { font-size: 1.5rem; color: #8b949e; }
  .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0; }
  .summary-item { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 1rem; text-align: center; }
  .summary-item .count { font-size: 2rem; font-weight: bold; }
  .critical .count { color: #f85149; }
  .high .count { color: #d29922; }
  .medium .count { color: #58a6ff; }
  .low .count { color: #8b949e; }
  .finding { background: #161b22; border-left: 4px solid #30363d; margin: 0.5rem 0; padding: 1rem; border-radius: 0 6px 6px 0; }
  .finding.sev-critical { border-left-color: #f85149; }
  .finding.sev-high { border-left-color: #d29922; }
  .finding.sev-medium { border-left-color: #58a6ff; }
  .finding.sev-low { border-left-color: #8b949e; }
  .finding .check-id { font-weight: bold; color: #79c0ff; }
  .finding .file { color: #8b949e; font-size: 0.9em; }
  .finding .code { background: #0d1117; padding: 0.5rem; border-radius: 4px; font-family: monospace; font-size: 0.85em; margin: 0.5rem 0; overflow-x: auto; }
  .finding .fix { color: #3fb950; font-size: 0.9em; }
  .filter-bar { margin: 1rem 0; }
  .filter-bar button { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; margin-right: 0.5rem; }
  .filter-bar button:hover { background: #30363d; }
  .filter-bar button.active { background: #388bfd; border-color: #388bfd; }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
  th, td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #30363d; }
  th { color: #58a6ff; }
  footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #30363d; color: #8b949e; font-size: 0.85em; }
</style>
</head>
<body>
HTMLHEAD

  echo "<h1>AuthAudit Security Report</h1>"
  echo "<p>Generated: $(date +%Y-%m-%d) | AuthAudit v${AUTHAUDIT_VERSION}</p>"

  # Score card
  echo "<div class=\"score-card\">"
  echo "  <div class=\"score ${score_class}\">${score}/100</div>"
  echo "  <div class=\"grade\">Grade: ${grade}</div>"
  echo "</div>"

  # Summary
  echo "<div class=\"summary\">"
  echo "  <div class=\"summary-item critical\"><div class=\"count\">${CRITICAL_COUNT}</div><div>Critical</div></div>"
  echo "  <div class=\"summary-item high\"><div class=\"count\">${HIGH_COUNT}</div><div>High</div></div>"
  echo "  <div class=\"summary-item medium\"><div class=\"count\">${MEDIUM_COUNT}</div><div>Medium</div></div>"
  echo "  <div class=\"summary-item low\"><div class=\"count\">${LOW_COUNT}</div><div>Low</div></div>"
  echo "</div>"

  # Stats
  echo "<h2>Scan Statistics</h2>"
  echo "<table>"
  echo "  <tr><th>Metric</th><th>Value</th></tr>"
  echo "  <tr><td>Files Scanned</td><td>${TOTAL_FILES_SCANNED}</td></tr>"
  echo "  <tr><td>Patterns Used</td><td>${pattern_count}</td></tr>"
  echo "  <tr><td>Total Issues</td><td>${TOTAL_ISSUES}</td></tr>"
  echo "</table>"

  # Category breakdown
  echo "<h2>Category Breakdown</h2>"
  echo "<table>"
  echo "  <tr><th>Category</th><th>Issues</th></tr>"
  echo "  <tr><td>AC - Authentication Checks</td><td>${CATEGORY_FINDINGS_AC}</td></tr>"
  echo "  <tr><td>SM - Session Management</td><td>${CATEGORY_FINDINGS_SM}</td></tr>"
  echo "  <tr><td>AZ - Authorization / Access Control</td><td>${CATEGORY_FINDINGS_AZ}</td></tr>"
  echo "  <tr><td>TK - Token Handling</td><td>${CATEGORY_FINDINGS_TK}</td></tr>"
  echo "  <tr><td>CS - CSRF Protection</td><td>${CATEGORY_FINDINGS_CS}</td></tr>"
  echo "  <tr><td>PW - Password & Credentials</td><td>${CATEGORY_FINDINGS_PW}</td></tr>"
  echo "</table>"

  # Filter bar
  echo "<h2>Findings</h2>"
  echo "<div class=\"filter-bar\">"
  echo "  <button class=\"active\" onclick=\"filterFindings('all')\">All (${TOTAL_ISSUES})</button>"
  [[ $CRITICAL_COUNT -gt 0 ]] && echo "  <button onclick=\"filterFindings('critical')\">Critical (${CRITICAL_COUNT})</button>"
  [[ $HIGH_COUNT -gt 0 ]]     && echo "  <button onclick=\"filterFindings('high')\">High (${HIGH_COUNT})</button>"
  [[ $MEDIUM_COUNT -gt 0 ]]   && echo "  <button onclick=\"filterFindings('medium')\">Medium (${MEDIUM_COUNT})</button>"
  [[ $LOW_COUNT -gt 0 ]]      && echo "  <button onclick=\"filterFindings('low')\">Low (${LOW_COUNT})</button>"
  echo "</div>"

  # Findings
  if [[ -n "$ALL_FINDINGS" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local fp ln cid sev desc rec lc cat
      IFS='|' read -r fp ln cid sev desc rec lc cat <<< "$line"

      # HTML-escape content
      lc=$(echo "$lc" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
      desc=$(echo "$desc" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
      rec=$(echo "$rec" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

      echo "<div class=\"finding sev-${sev}\" data-severity=\"${sev}\">"
      echo "  <div class=\"check-id\">[${sev^^}] ${cid} (${cat})</div>"
      echo "  <div>${desc}</div>"
      echo "  <div class=\"file\">${fp}:${ln}</div>"
      [[ -n "$lc" ]] && echo "  <div class=\"code\">${lc}</div>"
      echo "  <div class=\"fix\">Fix: ${rec}</div>"
      echo "</div>"
    done <<< "$ALL_FINDINGS"
  else
    echo "<p>No auth/authz issues found.</p>"
  fi

  # JavaScript for filtering
  cat <<'HTMLJS'
<script>
function filterFindings(severity) {
  document.querySelectorAll('.finding').forEach(el => {
    el.style.display = severity === 'all' || el.dataset.severity === severity ? 'block' : 'none';
  });
  document.querySelectorAll('.filter-bar button').forEach(btn => {
    btn.classList.toggle('active', btn.textContent.toLowerCase().startsWith(severity === 'all' ? 'all' : severity));
  });
}
</script>
HTMLJS

  echo "<footer>"
  echo "  <p>Generated by <a href=\"https://authaudit.dev\" style=\"color:#58a6ff\">AuthAudit</a> v${AUTHAUDIT_VERSION} -- Authentication & Authorization Pattern Analyzer</p>"
  echo "  <p>All scanning performed locally. No code was sent to external servers.</p>"
  echo "</footer>"
  echo "</body></html>"
}

# ─── Reset Accumulators ─────────────────────────────────────────────────────

reset_counters() {
  TOTAL_FILES_SCANNED=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""
  CATEGORY_FINDINGS_AC=0
  CATEGORY_FINDINGS_SM=0
  CATEGORY_FINDINGS_AZ=0
  CATEGORY_FINDINGS_TK=0
  CATEGORY_FINDINGS_CS=0
  CATEGORY_FINDINGS_PW=0
}

# ─── Main Scan Pipeline ─────────────────────────────────────────────────────
# Called by dispatcher.sh after argument parsing.

run_scan() {
  local target="$1"
  local format="${2:-text}"
  local pattern_limit="${3:-5}"
  local verbose="${4:-false}"
  local target_category="${5:-}"

  # Reset accumulators
  reset_counters

  # Load patterns
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Find source files
  local source_files
  source_files=$(find_source_files "$target")

  if [[ -z "$source_files" ]]; then
    if [[ "$format" == "json" ]]; then
      echo '{"tool":"authaudit","score":100,"grade":"A","pass":true,"summary":{"filesScanned":0,"totalIssues":0},"findings":[]}'
    else
      echo -e "  ${GREEN}No source files found -- clean scan.${NC}"
      echo -e "  ${DIM}Tip: run from your project root or specify a source directory.${NC}"
    fi
    return 0
  fi

  # Count files
  local file_count=0
  while IFS= read -r _f; do
    [[ -z "$_f" ]] && continue
    file_count=$((file_count + 1))
  done <<< "$source_files"

  if [[ "$format" == "text" ]]; then
    echo -e "  ${DIM}Files found:${NC}   ${file_count}"
    local pattern_count
    pattern_count=$(get_total_pattern_count "$pattern_limit")
    echo -e "  ${DIM}Patterns:${NC}      ${pattern_count}"
    if [[ -n "$target_category" ]]; then
      echo -e "  ${DIM}Category:${NC}      ${target_category}"
    fi
    echo ""
  fi

  # Scan each file
  while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue

    if [[ "$verbose" == "true" && "$format" == "text" ]]; then
      echo -e "  ${DIM}Scanning: ${filepath}${NC}"
    fi

    scan_file "$filepath" "$pattern_limit" "$target_category" > /dev/null
  done <<< "$source_files"

  # Calculate score
  local score
  score=$(calculate_score)
  local grade
  grade=$(get_grade "$score")
  local pattern_count
  pattern_count=$(get_total_pattern_count "$pattern_limit")

  # Output results
  case "$format" in
    json)
      output_json "$score" "$grade" "$pattern_count"
      ;;
    html)
      output_html "$score" "$grade" "$pattern_count"
      ;;
    *)
      output_text "$score" "$grade" "$pattern_count" "$pattern_limit" "$target_category"
      ;;
  esac

  # Return exit code based on score
  if [[ $score -lt $PASS_THRESHOLD ]]; then
    return 1
  fi
  return 0
}

# ─── Report Generation ──────────────────────────────────────────────────────
# Generates a markdown report using the template.

generate_report() {
  local target="$1"
  local pattern_limit="${2:-15}"

  # Run full scan silently
  reset_counters

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  local source_files
  source_files=$(find_source_files "$target")

  if [[ -z "$source_files" ]]; then
    echo -e "${YELLOW}[AuthAudit]${NC} No source files found -- nothing to report."
    return 0
  fi

  while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    scan_file "$filepath" "$pattern_limit" "" > /dev/null
  done <<< "$source_files"

  local score
  score=$(calculate_score)
  local grade
  grade=$(get_grade "$score")

  # Build findings markdown
  local md_findings=""
  if [[ -n "$ALL_FINDINGS" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local fp ln cid sev desc rec lc cat
      IFS='|' read -r fp ln cid sev desc rec lc cat <<< "$line"
      md_findings+="### ${sev^^}: ${cid} (${cat})"$'\n'
      md_findings+="- **File:** \`${fp}:${ln}\`"$'\n'
      md_findings+="- **Severity:** ${sev}"$'\n'
      md_findings+="- **Category:** ${cat}"$'\n'
      md_findings+="- **Description:** ${desc}"$'\n'
      md_findings+="- **Fix:** ${rec}"$'\n'
      [[ -n "$lc" ]] && md_findings+="- **Code:** \`${lc}\`"$'\n'
      md_findings+=""$'\n'
    done <<< "$ALL_FINDINGS"
  else
    md_findings="No authentication or authorization issues found."$'\n'
  fi

  # Build recommendations
  local recommendations=""
  [[ $CRITICAL_COUNT -gt 0 ]] && recommendations+="- **URGENT:** Fix ${CRITICAL_COUNT} critical auth issue(s) immediately"$'\n'
  [[ $HIGH_COUNT -gt 0 ]]     && recommendations+="- Fix ${HIGH_COUNT} high-severity issue(s) before next release"$'\n'
  [[ $MEDIUM_COUNT -gt 0 ]]   && recommendations+="- Address ${MEDIUM_COUNT} medium-severity issue(s) in upcoming sprint"$'\n'
  [[ $LOW_COUNT -gt 0 ]]      && recommendations+="- Review ${LOW_COUNT} low-severity finding(s) for best practices"$'\n'
  [[ -z "$recommendations" ]] && recommendations="No recommendations -- your authentication and authorization patterns look secure!"$'\n'

  # Build category breakdown markdown
  local cat_breakdown=""
  cat_breakdown+="| Category | Issues |"$'\n'
  cat_breakdown+="|----------|--------|"$'\n'
  cat_breakdown+="| AC - Authentication Checks | ${CATEGORY_FINDINGS_AC} |"$'\n'
  cat_breakdown+="| SM - Session Management | ${CATEGORY_FINDINGS_SM} |"$'\n'
  cat_breakdown+="| AZ - Authorization / Access Control | ${CATEGORY_FINDINGS_AZ} |"$'\n'
  cat_breakdown+="| TK - Token Handling | ${CATEGORY_FINDINGS_TK} |"$'\n'
  cat_breakdown+="| CS - CSRF Protection | ${CATEGORY_FINDINGS_CS} |"$'\n'
  cat_breakdown+="| PW - Password & Credentials | ${CATEGORY_FINDINGS_PW} |"$'\n'

  # Load and populate template
  local template_path="$script_dir/../templates/report.md.tmpl"
  local report_content
  if [[ -f "$template_path" ]]; then
    report_content=$(< "$template_path")
  else
    report_content="# AuthAudit Security Report\n\n**Score:** {{SECURITY_SCORE}}/100 ({{GRADE}})\n\n## Findings\n\n{{FINDINGS}}\n\n## Recommendations\n\n{{RECOMMENDATIONS}}"
  fi

  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd || echo "$target")")
  local today
  today=$(date +%Y-%m-%d)
  local pattern_count
  pattern_count=$(get_total_pattern_count "$pattern_limit")

  report_content="${report_content//\{\{DATE\}\}/$today}"
  report_content="${report_content//\{\{PROJECT\}\}/$project_name}"
  report_content="${report_content//\{\{SECURITY_SCORE\}\}/$score}"
  report_content="${report_content//\{\{GRADE\}\}/$grade}"
  report_content="${report_content//\{\{FILES_SCANNED\}\}/$TOTAL_FILES_SCANNED}"
  report_content="${report_content//\{\{PATTERNS_USED\}\}/$pattern_count}"
  report_content="${report_content//\{\{TOTAL_ISSUES\}\}/$TOTAL_ISSUES}"
  report_content="${report_content//\{\{CRITICAL_COUNT\}\}/$CRITICAL_COUNT}"
  report_content="${report_content//\{\{HIGH_COUNT\}\}/$HIGH_COUNT}"
  report_content="${report_content//\{\{MEDIUM_COUNT\}\}/$MEDIUM_COUNT}"
  report_content="${report_content//\{\{LOW_COUNT\}\}/$LOW_COUNT}"
  report_content="${report_content//\{\{CATEGORY_BREAKDOWN\}\}/$cat_breakdown}"
  report_content="${report_content//\{\{FINDINGS\}\}/$md_findings}"
  report_content="${report_content//\{\{RECOMMENDATIONS\}\}/$recommendations}"
  report_content="${report_content//\{\{VERSION\}\}/$AUTHAUDIT_VERSION}"

  local report_file="AUTHAUDIT-REPORT.md"
  echo -e "$report_content" > "$report_file"

  echo -e "${GREEN}[AuthAudit]${NC} Report generated: ${BOLD}${report_file}${NC}"
  echo -e "  Score: ${score}/100 (${grade})"
  echo -e "  Issues: ${TOTAL_ISSUES} (${CRITICAL_COUNT} critical, ${HIGH_COUNT} high, ${MEDIUM_COUNT} medium, ${LOW_COUNT} low)"
}

# ─── Hook Scan (for lefthook pre-commit) ─────────────────────────────────────

hook_scan() {
  echo -e "${BLUE}[AuthAudit]${NC} Scanning staged files for auth/authz issues..."

  # Get staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    echo -e "${GREEN}[AuthAudit]${NC} No staged files to scan."
    return 0
  fi

  # Filter to scannable extensions
  local scannable_files=""
  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue
    if is_scannable_file "$sf"; then
      scannable_files+="$sf"$'\n'
    fi
  done <<< "$staged_files"

  if [[ -z "$scannable_files" ]]; then
    echo -e "${GREEN}[AuthAudit]${NC} No source files in staged changes."
    return 0
  fi

  # Load patterns
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Determine pattern limit from license
  local pattern_limit=5
  if [[ -f "$script_dir/license.sh" ]]; then
    source "$script_dir/license.sh"
    pattern_limit=$(get_pattern_limit 2>/dev/null) || pattern_limit=5
  fi

  # Reset counters
  reset_counters

  # Scan each staged file
  while IFS= read -r rf; do
    [[ -z "$rf" ]] && continue
    [[ ! -f "$rf" ]] && continue
    scan_file "$rf" "$pattern_limit" "" > /dev/null
  done <<< "$scannable_files"

  # Summary
  if [[ $CRITICAL_COUNT -gt 0 ]]; then
    echo -e "${RED}[AuthAudit]${NC} ${BOLD}${CRITICAL_COUNT} critical issue(s)${NC} found in staged files!"
    if [[ -n "$ALL_FINDINGS" ]]; then
      print_all_findings "$ALL_FINDINGS"
    fi
    return 1
  fi

  if [[ $TOTAL_ISSUES -gt 0 ]]; then
    echo -e "${YELLOW}[AuthAudit]${NC} ${TOTAL_ISSUES} issue(s) found (${HIGH_COUNT} high, ${MEDIUM_COUNT} medium, ${LOW_COUNT} low)"
    return 0  # Non-critical issues don't block commit
  fi

  echo -e "${GREEN}[AuthAudit]${NC} Staged files look secure."
  return 0
}
