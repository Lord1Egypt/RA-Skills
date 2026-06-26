#!/usr/bin/env bash
# CloudGuard -- Core Analysis Engine
# Provides: file discovery, pattern scanning, tier-limited scanning, score calculation,
#           grades, category breakdown, report generation, JSON/HTML output,
#           and hook integration.
#
# This file is sourced by dispatcher.sh and by the lefthook pre-commit hook.
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
CLOUDGUARD_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

# ============================================================================
# File Discovery
# ============================================================================

# Check if a file is a cloud/IaC configuration file we should scan
is_iac_file() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')
  local ext="${basename_lower##*.}"

  # Terraform files
  case "$ext" in
    tf|tfvars|hcl) return 0 ;;
  esac

  # CloudFormation, Kubernetes, Ansible, Docker Compose
  case "$ext" in
    yml|yaml|json|template) return 0 ;;
  esac

  # Configuration files
  case "$ext" in
    conf|cfg|ini|toml) return 0 ;;
  esac

  # Script files that may contain IaC
  case "$ext" in
    sh|bash|ps1|py) return 0 ;;
  esac

  # Policy files
  case "$ext" in
    rego) return 0 ;;
  esac

  # Specific filenames
  case "$basename_lower" in
    dockerfile|docker-compose.yml|docker-compose.yaml) return 0 ;;
    jenkinsfile|vagrantfile) return 0 ;;
    .env|.env.*) return 0 ;;
    serverless.yml|serverless.yaml) return 0 ;;
    buildspec.yml|buildspec.yaml) return 0 ;;
    appspec.yml|appspec.yaml) return 0 ;;
    taskdef.json|task-definition.json) return 0 ;;
    samconfig.toml) return 0 ;;
  esac

  return 1
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
    terraform.tfstate|terraform.tfstate.backup) return 0 ;;
  esac

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
    */.terragrunt-cache/*|*/.terragrunt-cache) return 0 ;;
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

# Find all scannable IaC files in a directory tree
find_scannable_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  # If it is a single file, check if scannable
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

    # For cloud scanning, prefer IaC files but scan all text files
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 10 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".next" \
       -o -name "dist" -o -name "build" -o -name "coverage" -o -name "__pycache__" \
       -o -name ".venv" -o -name "venv" -o -name ".tox" -o -name ".terraform" \
       -o -name ".terragrunt-cache" -o -name ".cache" \) -prune -o \
    -type f -print0 2>/dev/null)
}

# Find only IaC-specific files (for focused scanning)
find_iac_files() {
  local search_dir="$1"
  local -n _iac_result_files="$2"
  _iac_result_files=()

  if [[ -f "$search_dir" ]]; then
    if is_iac_file "$search_dir" && ! should_skip_file "$search_dir"; then
      _iac_result_files+=("$search_dir")
    fi
    return 0
  fi

  while IFS= read -r -d '' file; do
    is_excluded_dir "$file" && continue
    should_skip_file "$file" && continue
    is_gitignored "$file" && continue

    # Only include IaC files
    if is_iac_file "$file"; then
      _iac_result_files+=("$file")
    fi
  done < <(find "$search_dir" -maxdepth 10 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".next" \
       -o -name "dist" -o -name "build" -o -name ".terraform" \
       -o -name ".terragrunt-cache" \) -prune -o \
    -type f -print0 2>/dev/null)
}

# ============================================================================
# Pattern Scanning
# ============================================================================

# Scan a single file against patterns for a specific category.
# Respects tier-based pattern limits.
# Appends findings to global FINDINGS array.
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
scan_file() {
  local filepath="$1"
  local pattern_limit="${2:-90}"        # Total patterns allowed by tier
  local category_filter="${3:-all}"     # Optional category filter

  local per_category_limit
  per_category_limit=$(get_tier_pattern_count_per_category "$pattern_limit")

  local categories
  if [[ "$category_filter" != "all" ]]; then
    categories="$category_filter"
  else
    categories=$(get_all_cloudguard_categories)
  fi

  for category in $categories; do
    local patterns_name
    patterns_name=$(get_cloudguard_patterns_for_category "$category")

    if [[ -z "$patterns_name" ]]; then
      continue
    fi

    local -n _scan_patterns_ref="$patterns_name"
    local pattern_idx=0

    for entry in "${_scan_patterns_ref[@]}"; do
      # Enforce per-category pattern limit for tier
      if [[ $pattern_idx -ge $per_category_limit ]]; then
        break
      fi
      pattern_idx=$((pattern_idx + 1))

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
          FINDINGS+=("$finding")
        done <<< "$matches"
      fi
    done
  done
}

# ============================================================================
# Score Calculation & Grading
# ============================================================================

# Calculate a cloud security score based on findings.
# Score starts at 100 (clean) and decreases with each finding.
# Weights: critical=25pts, high=15pts, medium=8pts, low=3pts
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
# A(90-100), B(80-89), C(70-79), D(60-69), F(<60)
score_to_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 60 ]]; then echo "D"
  else echo "F"
  fi
}

# Pass threshold: 70
score_passes() {
  local score="$1"
  [[ $score -ge 70 ]]
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
# Category Breakdown
# ============================================================================

# Build category breakdown counts from FINDINGS
get_category_breakdown() {
  local -A cat_counts=()

  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ _ check_id _ _ _ <<< "$finding"
    local prefix="${check_id%%-*}"
    cat_counts["$prefix"]=$(( ${cat_counts["$prefix"]:-0} + 1 ))
  done

  for cat in S3 IM NW EN LG CF; do
    local count="${cat_counts[$cat]:-0}"
    if [[ $count -gt 0 ]]; then
      local label
      label=$(get_cloudguard_category_label "$cat")
      echo "$cat|$label|$count"
    fi
  done
}

# Get severity counts from FINDINGS
get_severity_counts() {
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

  echo "$crit_count|$high_count|$med_count|$low_count"
}

# ============================================================================
# Output Formatting -- Text
# ============================================================================

# Print findings to stdout in text format
print_findings_text() {
  local count=0
  local crit_count=0 high_count=0 med_count=0 low_count=0

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

  # Category breakdown
  echo ""
  echo -e "${BOLD}--- Category Breakdown ---${NC}"
  local breakdown
  breakdown=$(get_category_breakdown)
  if [[ -n "$breakdown" ]]; then
    while IFS='|' read -r cat label count_val; do
      echo -e "  ${BOLD}${cat}${NC} ${label}: ${count_val} findings"
    done <<< "$breakdown"
  else
    echo -e "  ${GREEN}No findings in any category${NC}"
  fi
}

# Print score and grade
print_score() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local gc
  gc=$(grade_color "$grade")

  echo ""
  echo -e "${BOLD}Cloud Security Score: ${gc}${score}/100${NC} (Grade: ${gc}${BOLD}${grade}${NC})"

  if score_passes "$score"; then
    echo -e "${GREEN}PASS${NC} -- Score is above threshold (70)"
  else
    echo -e "${RED}FAIL${NC} -- Score is below threshold (70)"
  fi
}

# ============================================================================
# Output Formatting -- JSON
# ============================================================================

print_findings_json() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local total_files="$2"

  local severity_data
  severity_data=$(get_severity_counts)
  IFS='|' read -r crit_count high_count med_count low_count <<< "$severity_data"

  # Start JSON output
  echo "{"
  echo "  \"tool\": \"CloudGuard\","
  echo "  \"version\": \"${CLOUDGUARD_VERSION}\","
  echo "  \"score\": ${score},"
  echo "  \"grade\": \"${grade}\","
  echo "  \"pass\": $(score_passes "$score" && echo "true" || echo "false"),"
  echo "  \"filesScanned\": ${total_files},"
  echo "  \"totalFindings\": ${#FINDINGS[@]},"
  echo "  \"severity\": {"
  echo "    \"critical\": ${crit_count},"
  echo "    \"high\": ${high_count},"
  echo "    \"medium\": ${med_count},"
  echo "    \"low\": ${low_count}"
  echo "  },"

  # Category breakdown
  echo "  \"categories\": {"
  local first_cat=true
  local breakdown
  breakdown=$(get_category_breakdown)
  if [[ -n "$breakdown" ]]; then
    while IFS='|' read -r cat label count_val; do
      if [[ "$first_cat" == true ]]; then
        first_cat=false
      else
        echo ","
      fi
      printf "    \"%s\": { \"label\": \"%s\", \"count\": %s }" "$cat" "$label" "$count_val"
    done <<< "$breakdown"
    echo ""
  fi
  echo "  },"

  # Findings array
  echo "  \"findings\": ["
  local first_finding=true
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"

    # Escape JSON special chars
    local escaped_desc
    escaped_desc=$(echo "$description" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')
    local escaped_rec
    escaped_rec=$(echo "$recommendation" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')
    local escaped_text
    escaped_text=$(echo "$matched_text" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')

    if [[ "$first_finding" == true ]]; then
      first_finding=false
    else
      echo ","
    fi

    printf "    {\n"
    printf "      \"file\": \"%s\",\n" "$file"
    printf "      \"line\": %s,\n" "$line"
    printf "      \"severity\": \"%s\",\n" "$severity"
    printf "      \"checkId\": \"%s\",\n" "$check_id"
    printf "      \"category\": \"%s\",\n" "${check_id%%-*}"
    printf "      \"description\": \"%s\",\n" "$escaped_desc"
    printf "      \"recommendation\": \"%s\",\n" "$escaped_rec"
    printf "      \"matchedText\": \"%s\"\n" "$escaped_text"
    printf "    }"
  done
  echo ""
  echo "  ]"
  echo "}"
}

# ============================================================================
# Output Formatting -- HTML
# ============================================================================

print_findings_html() {
  local score="$1"
  local grade
  grade=$(score_to_grade "$score")
  local total_files="$2"

  local severity_data
  severity_data=$(get_severity_counts)
  IFS='|' read -r crit_count high_count med_count low_count <<< "$severity_data"

  local pass_fail="PASS"
  local pass_color="#22c55e"
  if ! score_passes "$score"; then
    pass_fail="FAIL"
    pass_color="#ef4444"
  fi

  local grade_color_hex
  case "$grade" in
    A) grade_color_hex="#22c55e" ;;
    B) grade_color_hex="#22c55e" ;;
    C) grade_color_hex="#eab308" ;;
    D) grade_color_hex="#eab308" ;;
    F) grade_color_hex="#ef4444" ;;
  esac

  cat <<HTML_EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CloudGuard Security Report</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f8fafc; color: #1e293b; }
    .container { max-width: 960px; margin: 0 auto; }
    h1 { color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }
    h2 { color: #334155; margin-top: 32px; }
    .score-card { display: flex; gap: 24px; margin: 24px 0; }
    .score-item { background: white; border-radius: 8px; padding: 16px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; flex: 1; }
    .score-value { font-size: 2em; font-weight: bold; }
    .score-label { color: #64748b; font-size: 0.9em; margin-top: 4px; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    th { background: #f1f5f9; color: #334155; padding: 12px 16px; text-align: left; font-weight: 600; }
    td { padding: 10px 16px; border-top: 1px solid #e2e8f0; }
    tr:hover { background: #f8fafc; }
    .sev-critical { color: #ef4444; font-weight: bold; }
    .sev-high { color: #a855f7; font-weight: bold; }
    .sev-medium { color: #eab308; font-weight: bold; }
    .sev-low { color: #06b6d4; font-weight: bold; }
    .footer { margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.85em; }
  </style>
</head>
<body>
  <div class="container">
    <h1>CloudGuard Security Report</h1>
    <div class="score-card">
      <div class="score-item">
        <div class="score-value" style="color: ${grade_color_hex}">${score}/100</div>
        <div class="score-label">Security Score</div>
      </div>
      <div class="score-item">
        <div class="score-value" style="color: ${grade_color_hex}">${grade}</div>
        <div class="score-label">Grade</div>
      </div>
      <div class="score-item">
        <div class="score-value" style="color: ${pass_color}">${pass_fail}</div>
        <div class="score-label">Status</div>
      </div>
      <div class="score-item">
        <div class="score-value">${#FINDINGS[@]}</div>
        <div class="score-label">Findings</div>
      </div>
      <div class="score-item">
        <div class="score-value">${total_files}</div>
        <div class="score-label">Files Scanned</div>
      </div>
    </div>

    <h2>Severity Breakdown</h2>
    <table>
      <tr><th>Severity</th><th>Count</th></tr>
      <tr><td class="sev-critical">Critical</td><td>${crit_count}</td></tr>
      <tr><td class="sev-high">High</td><td>${high_count}</td></tr>
      <tr><td class="sev-medium">Medium</td><td>${med_count}</td></tr>
      <tr><td class="sev-low">Low</td><td>${low_count}</td></tr>
    </table>

    <h2>Category Breakdown</h2>
    <table>
      <tr><th>Category</th><th>Label</th><th>Findings</th></tr>
HTML_EOF

  local breakdown
  breakdown=$(get_category_breakdown)
  if [[ -n "$breakdown" ]]; then
    while IFS='|' read -r cat label count_val; do
      echo "      <tr><td>${cat}</td><td>${label}</td><td>${count_val}</td></tr>"
    done <<< "$breakdown"
  fi

  cat <<HTML_EOF2
    </table>

    <h2>Findings</h2>
    <table>
      <tr><th>#</th><th>File</th><th>Line</th><th>Severity</th><th>Check</th><th>Description</th></tr>
HTML_EOF2

  local idx=0
  for finding in "${FINDINGS[@]}"; do
    idx=$((idx + 1))
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    local sev_class="sev-${severity}"
    # HTML-escape description
    local escaped_desc
    escaped_desc=$(echo "$description" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    echo "      <tr><td>${idx}</td><td>${file}</td><td>${line}</td><td class=\"${sev_class}\">${severity^^}</td><td>${check_id}</td><td>${escaped_desc}</td></tr>"
  done

  cat <<HTML_EOF3
    </table>

    <div class="footer">
      Generated by <a href="https://cloudguard.pages.dev">CloudGuard</a> v${CLOUDGUARD_VERSION} |
      $(date +%Y-%m-%d 2>/dev/null || echo "unknown date")
    </div>
  </div>
</body>
</html>
HTML_EOF3
}

# ============================================================================
# Report Generation (Markdown template)
# ============================================================================

generate_cloudguard_report() {
  local target="${1:-.}"
  local pattern_limit="${2:-90}"
  local category_filter="${3:-all}"
  FINDINGS=()

  local -a files=()
  find_iac_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[CloudGuard]${NC} No IaC files found in ${BOLD}$target${NC}"
    return 0
  fi

  echo -e "${BLUE}[CloudGuard]${NC} Scanning ${BOLD}$total_files${NC} IaC files for report..." >&2

  for filepath in "${files[@]}"; do
    scan_file "$filepath" "$pattern_limit" "$category_filter"
  done

  local score
  score=$(calculate_score)
  local grade
  grade=$(score_to_grade "$score")
  local date_str
  date_str=$(date +%Y-%m-%d 2>/dev/null || echo "unknown")

  # Severity counts
  local severity_data
  severity_data=$(get_severity_counts)
  IFS='|' read -r crit_count high_count med_count low_count <<< "$severity_data"

  local total_issues=${#FINDINGS[@]}

  # Category breakdown for template
  local cat_breakdown=""
  local breakdown
  breakdown=$(get_category_breakdown)
  if [[ -n "$breakdown" ]]; then
    while IFS='|' read -r cat label count_val; do
      cat_breakdown="${cat_breakdown}| ${label} (${cat}) | ${count_val} |"$'\n'
    done <<< "$breakdown"
  fi

  # Findings table for template
  local findings_table=""
  local idx=0
  for finding in "${FINDINGS[@]}"; do
    idx=$((idx + 1))
    IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
    findings_table="${findings_table}| ${idx} | ${file} | ${line} | ${severity} | ${check_id} | ${description} |"$'\n'
  done

  # Recommendations
  local recommendations=""
  if [[ $crit_count -gt 0 ]]; then
    recommendations="${recommendations}1. **CRITICAL:** ${crit_count} critical misconfigurations found -- fix immediately before deployment"$'\n'
  fi
  if [[ $high_count -gt 0 ]]; then
    recommendations="${recommendations}2. **HIGH:** ${high_count} high-severity findings -- address in current sprint"$'\n'
  fi
  if [[ $med_count -gt 0 ]]; then
    recommendations="${recommendations}3. **MEDIUM:** ${med_count} medium findings -- plan remediation within 30 days"$'\n'
  fi
  if [[ $low_count -gt 0 ]]; then
    recommendations="${recommendations}4. **LOW:** ${low_count} low findings -- review and address as needed"$'\n'
  fi

  # Project name
  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd)" 2>/dev/null || echo "$target")

  # Read template and substitute
  local template_file="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_file" ]]; then
    echo -e "${RED}[CloudGuard]${NC} Report template not found: $template_file" >&2
    return 1
  fi

  local report
  report=$(cat "$template_file")
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{VERSION\}\}/$CLOUDGUARD_VERSION}"
  report="${report//\{\{DATE\}\}/$date_str}"
  report="${report//\{\{CLOUDGUARD_SCORE\}\}/$score}"
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
  echo -e "${GREEN}[CloudGuard]${NC} Report generated. Score: ${BOLD}$score/100${NC} (Grade: ${BOLD}$grade${NC})" >&2
}

# ============================================================================
# Main Scan Function
# ============================================================================

# do_cloudguard_scan <target> <pattern_limit> <format> <category_filter> <verbose>
do_cloudguard_scan() {
  local target="${1:-.}"
  local pattern_limit="${2:-30}"
  local format="${3:-text}"
  local category_filter="${4:-all}"
  local verbose="${5:-false}"
  FINDINGS=()

  # Discover IaC files
  local -a files=()
  find_iac_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    if [[ "$format" == "json" ]]; then
      echo '{"tool":"CloudGuard","score":100,"grade":"A","pass":true,"filesScanned":0,"totalFindings":0,"findings":[]}'
    else
      echo -e "${GREEN}[CloudGuard]${NC} No IaC files found in ${BOLD}$target${NC}"
      echo -e "  Clean scan -- no infrastructure files to check."
      echo -e "  ${DIM}Scanned for: .tf, .tfvars, .yml, .yaml, .json, Dockerfile, etc.${NC}"
    fi
    return 0
  fi

  local per_cat
  per_cat=$(get_tier_pattern_count_per_category "$pattern_limit")

  if [[ "$format" == "text" ]]; then
    echo -e "${BLUE}[CloudGuard]${NC} Scanning ${BOLD}$total_files${NC} IaC files (${pattern_limit} patterns, ${per_cat}/category)..."
    if [[ $pattern_limit -lt 90 ]]; then
      echo -e "  ${DIM}Upgrade for full 90-pattern scan: https://cloudguard.pages.dev/pricing${NC}"
    fi
    echo ""
  fi

  # Scan all files
  for filepath in "${files[@]}"; do
    if [[ "$verbose" == "true" && "$format" == "text" ]]; then
      echo -e "  ${DIM}Scanning: $filepath${NC}"
    fi
    scan_file "$filepath" "$pattern_limit" "$category_filter"
  done

  # Output results based on format
  case "$format" in
    json)
      if [[ ${#FINDINGS[@]} -eq 0 ]]; then
        echo '{"tool":"CloudGuard","score":100,"grade":"A","pass":true,"filesScanned":'$total_files',"totalFindings":0,"findings":[]}'
      else
        local score
        score=$(calculate_score)
        print_findings_json "$score" "$total_files"
      fi
      ;;
    html)
      local score=100
      if [[ ${#FINDINGS[@]} -gt 0 ]]; then
        score=$(calculate_score)
      fi
      print_findings_html "$score" "$total_files"
      ;;
    text|*)
      if [[ ${#FINDINGS[@]} -eq 0 ]]; then
        echo -e "${GREEN}${BOLD}No cloud security issues detected!${NC}"
        echo ""
        echo -e "Cloud Security Score: ${GREEN}${BOLD}100/100${NC} (Grade: ${GREEN}${BOLD}A${NC})"
        echo -e "${GREEN}PASS${NC}"
        return 0
      fi

      print_findings_text

      local score
      score=$(calculate_score)
      print_score "$score"

      # Exit code
      if ! score_passes "$score"; then
        return 1
      fi
      return 0
      ;;
  esac

  # For JSON/HTML: return exit code based on score
  if [[ ${#FINDINGS[@]} -gt 0 ]]; then
    local score
    score=$(calculate_score)
    if ! score_passes "$score"; then
      return 1
    fi
  fi
  return 0
}

# ============================================================================
# Deep Audit (Pro+)
# ============================================================================

do_cloudguard_audit() {
  local target="${1:-.}"
  local pattern_limit="${2:-60}"
  local category_filter="${3:-all}"
  FINDINGS=()

  local -a files=()
  find_iac_files "$target" files

  local total_files=${#files[@]}

  if [[ $total_files -eq 0 ]]; then
    echo -e "${GREEN}[CloudGuard]${NC} No IaC files found in ${BOLD}$target${NC}"
    return 0
  fi

  echo -e "${BLUE}[CloudGuard]${NC} Deep audit: scanning ${BOLD}$total_files${NC} IaC files across all categories..."
  echo ""

  for filepath in "${files[@]}"; do
    scan_file "$filepath" "$pattern_limit" "$category_filter"
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No cloud security issues detected!${NC}"
    echo ""
    echo -e "Cloud Security Score: ${GREEN}${BOLD}100/100${NC} (Grade: ${GREEN}${BOLD}A${NC})"
    echo -e "${GREEN}PASS${NC}"
    return 0
  fi

  print_findings_text

  local score
  score=$(calculate_score)
  print_score "$score"

  if ! score_passes "$score"; then
    return 1
  fi
  return 0
}

# ============================================================================
# Hook Integration
# ============================================================================

# Called by lefthook pre-commit hook
hook_cloudguard_check() {
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true)

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  FINDINGS=()

  local file_count=0
  while IFS= read -r filepath; do
    [[ -z "$filepath" ]] && continue
    [[ ! -f "$filepath" ]] && continue

    # Skip excluded dirs
    is_excluded_dir "$filepath" && continue

    # Skip binary files
    should_skip_file "$filepath" && continue

    # Only scan IaC files for hooks
    if ! is_iac_file "$filepath"; then
      continue
    fi

    # Use full pattern set for hooks (team tier assumed for CI integration)
    scan_file "$filepath" 90 "all"

    file_count=$((file_count + 1))
  done <<< "$staged_files"

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[CloudGuard]${NC} No cloud security issues in $file_count staged IaC files."
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

  echo -e "${RED}${BOLD}[CloudGuard] Cloud security issues detected in staged files!${NC}"
  echo ""
  print_findings_text

  local score
  score=$(calculate_score)
  print_score "$score"

  if [[ "$has_blocking" == true ]]; then
    echo ""
    echo -e "${RED}Commit blocked.${NC} Fix cloud security issues before committing."
    echo -e "  Run: ${CYAN}cloudguard scan${NC} for details"
    echo -e "  Skip: ${DIM}git commit --no-verify${NC} (not recommended)"
    return 1
  fi

  return 0
}

# Called by lefthook pre-push hook
hook_cloudguard_prepush() {
  local target="${1:-.}"
  FINDINGS=()

  local -a files=()
  find_iac_files "$target" files

  if [[ ${#files[@]} -eq 0 ]]; then
    return 0
  fi

  for filepath in "${files[@]}"; do
    scan_file "$filepath" 90 "all"
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[CloudGuard]${NC} Pre-push check passed. No critical cloud security issues."
    return 0
  fi

  # Only block on critical findings for push
  local has_critical=false
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _ _ severity _ _ _ _ <<< "$finding"
    if [[ "$severity" == "critical" ]]; then
      has_critical=true
      break
    fi
  done

  if [[ "$has_critical" == true ]]; then
    echo -e "${RED}${BOLD}[CloudGuard] CRITICAL cloud security issues found -- push blocked.${NC}"
    echo ""

    # Print only critical findings
    for finding in "${FINDINGS[@]}"; do
      IFS='|' read -r file line severity check_id description recommendation matched_text <<< "$finding"
      if [[ "$severity" == "critical" ]]; then
        echo -e "  ${RED}CRITICAL${NC} ${DIM}${check_id}${NC} ${file}:${line}"
        echo -e "    ${description}"
        echo ""
      fi
    done

    echo -e "Fix critical issues before pushing."
    echo -e "  Run: ${CYAN}cloudguard scan${NC} for full details"
    echo -e "  Skip: ${DIM}git push --no-verify${NC} (not recommended)"
    return 1
  fi

  local score
  score=$(calculate_score)
  echo -e "${YELLOW}[CloudGuard]${NC} Pre-push check: ${#FINDINGS[@]} non-critical findings. Score: $score/100"
  return 0
}

# ============================================================================
# Pattern Listing
# ============================================================================

do_list_patterns() {
  echo -e "${BOLD}--- CloudGuard Detection Patterns ---${NC}"
  echo ""
  echo -e "${BOLD}$(cloudguard_pattern_count) patterns across 6 categories${NC}"
  echo ""

  local categories
  categories=$(get_all_cloudguard_categories)

  for cat in $categories; do
    local label
    label=$(get_cloudguard_category_label "$cat")
    echo -e "${CYAN}${BOLD}${label} (${cat}):${NC}"
    cloudguard_list_patterns "$cat" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  done
}
