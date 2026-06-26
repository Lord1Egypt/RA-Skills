#!/usr/bin/env bash
# AccessLint — Core Analysis Engine
# Provides: file type detection, file discovery, pattern scanning, WCAG mapping,
#           score calculation, report generation, WCAG compliance, SARIF output,
#           policy enforcement, and pre-commit hook handler.
#
# This file is sourced by accesslint.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# -- Colors (safe to re-declare; sourcing scripts may set these) ---------------

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
ACCESSLINT_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

# -- File Type Detection -------------------------------------------------------

# Detect the template type for a given file.
# Outputs one of: html, jsx, tsx, vue, svelte, css, unknown
detect_filetype() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local ext="${basename_f##*.}"
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')

  case "$ext" in
    html|htm)          echo "html" ;;
    jsx)               echo "jsx" ;;
    tsx)               echo "tsx" ;;
    vue)               echo "vue" ;;
    svelte)            echo "svelte" ;;
    css|scss|less)     echo "css" ;;
    js|mjs|cjs)        echo "javascript" ;;
    ts|mts|cts)        echo "typescript" ;;
    php)               echo "php" ;;
    erb|haml|slim)     echo "ruby-template" ;;
    hbs|handlebars)    echo "handlebars" ;;
    ejs)               echo "ejs" ;;
    astro)             echo "astro" ;;
    mdx)               echo "mdx" ;;
    *)                 echo "unknown" ;;
  esac
}

# Get display label for a file type
filetype_label() {
  local ft="$1"
  case "$ft" in
    html)            echo "HTML" ;;
    jsx)             echo "JSX" ;;
    tsx)             echo "TSX" ;;
    vue)             echo "Vue" ;;
    svelte)          echo "Svelte" ;;
    css)             echo "CSS" ;;
    javascript)      echo "JavaScript" ;;
    typescript)      echo "TypeScript" ;;
    php)             echo "PHP" ;;
    ruby-template)   echo "Ruby Template" ;;
    handlebars)      echo "Handlebars" ;;
    ejs)             echo "EJS" ;;
    astro)           echo "Astro" ;;
    mdx)             echo "MDX" ;;
    *)               echo "Unknown" ;;
  esac
}

# Check if file type supports accessibility scanning
is_scannable_type() {
  local ft="$1"
  case "$ft" in
    html|jsx|tsx|vue|svelte|css|javascript|typescript|php|ruby-template|handlebars|ejs|astro|mdx) return 0 ;;
    *) return 1 ;;
  esac
}

# -- Discover Template Files ---------------------------------------------------

# Find all files that may contain markup/templates.
discover_template_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  if [[ -f "$search_dir" ]]; then
    local ft
    ft=$(detect_filetype "$search_dir")
    if is_scannable_type "$ft"; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  # Template/component file extensions
  local -a extensions=(
    "html" "htm"
    "jsx" "tsx"
    "vue"
    "svelte"
    "css" "scss" "less"
    "js" "mjs" "cjs"
    "ts" "mts" "cts"
    "php"
    "erb" "haml" "slim"
    "hbs" "handlebars"
    "ejs"
    "astro"
    "mdx"
  )

  # Find files, excluding common vendor/build directories
  while IFS= read -r -d '' file; do
    # Quick filter: only include files that contain markup
    if has_markup_content "$file"; then
      _result_files+=("$file")
    fi
  done < <(find "$search_dir" -maxdepth 8 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name "__pycache__" \
       -o -name ".venv" -o -name "venv" -o -name "dist" -o -name "build" \
       -o -name ".next" -o -name ".nuxt" -o -name "target" -o -name "bin" \
       -o -name ".svelte-kit" -o -name ".output" -o -name "coverage" \) -prune -o \
    \( -name "*.html" -o -name "*.htm" \
       -o -name "*.jsx" -o -name "*.tsx" \
       -o -name "*.vue" -o -name "*.svelte" \
       -o -name "*.css" -o -name "*.scss" -o -name "*.less" \
       -o -name "*.js" -o -name "*.mjs" -o -name "*.cjs" \
       -o -name "*.ts" -o -name "*.mts" -o -name "*.cts" \
       -o -name "*.php" \
       -o -name "*.erb" -o -name "*.hbs" -o -name "*.ejs" \
       -o -name "*.astro" -o -name "*.mdx" \) \
    -type f -print0 2>/dev/null)
}

# Quick check: does a file contain HTML/JSX markup?
has_markup_content() {
  local filepath="$1"
  local ext="${filepath##*.}"

  # HTML files always qualify
  if [[ "$ext" == "html" || "$ext" == "htm" || "$ext" == "vue" || "$ext" == "svelte" || "$ext" == "astro" ]]; then
    return 0
  fi

  # CSS files qualify for visual checks
  if [[ "$ext" == "css" || "$ext" == "scss" || "$ext" == "less" ]]; then
    return 0
  fi

  # Check for JSX/HTML markup in the file
  if grep -qiE "(<[a-zA-Z][a-zA-Z0-9]*[[:space:]]|<img[[:space:]]|<button|<input|<select|<textarea|<a[[:space:]]|<div[[:space:]]|<span[[:space:]]|<h[1-6][[:space:]>]|<form[[:space:]>]|<svg[[:space:]]|<video[[:space:]]|<audio[[:space:]]|<iframe[[:space:]]|aria-|role=|onClick|onclick|tabindex|className=|class=|alt=)" "$filepath" 2>/dev/null; then
    return 0
  fi

  return 1
}

# -- Scan File With Patterns ---------------------------------------------------

# Scan a single file against all accessibility pattern categories.
# Appends findings to global FINDINGS array.
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|WCAG|RECOMMENDATION|MATCHED_TEXT
scan_file() {
  local filepath="$1"
  local ft
  ft=$(detect_filetype "$filepath")

  # Run all pattern categories
  local categories=("aria" "semantic" "keyboard" "form" "visual" "dynamic")

  for category in "${categories[@]}"; do
    scan_file_with_category "$filepath" "$category" "$ft"
  done
}

# Scan a file against patterns in a specific category
scan_file_with_category() {
  local filepath="$1"
  local category="$2"
  local ft="$3"

  local patterns_name
  patterns_name=$(get_patterns_for_category "$category")

  if [[ -z "$patterns_name" ]]; then
    return 0
  fi

  local -n _patterns_ref="$patterns_name"

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description wcag recommendation <<< "$entry"

    # Skip placeholder patterns
    [[ "$regex" == PLACEHOLDER_* ]] && continue

    # Skip CSS-only patterns for non-CSS files and vice versa
    if [[ "$category" == "visual" ]]; then
      case "$ft" in
        css) ;; # CSS files get visual checks
        html|jsx|tsx|vue|svelte|astro) ;; # Template files get visual checks
        *) continue ;; # Skip visual checks for pure JS/TS
      esac
    fi

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
        FINDINGS+=("${filepath}|${line_num}|${severity}|${check_id}|${description}|${wcag}|${recommendation}|${matched_text}")
      done <<< "$matches"
    fi
  done
}

# Special handler for HTML files — additional document-level checks
scan_html_file() {
  local filepath="$1"

  # Standard pattern scan
  scan_file "$filepath"

  # Document-level checks

  # Check for missing <main> landmark
  if ! grep -qiE "<main[[:space:]>]" "$filepath" 2>/dev/null; then
    FINDINGS+=("${filepath}|1|medium|SH-013|Page missing <main> landmark region|1.3.1|Wrap primary content in <main> for landmark navigation|Missing <main> element")
  fi

  # Check for missing <html lang>
  if grep -qiE "<html[[:space:]]" "$filepath" 2>/dev/null; then
    if ! grep -qiE "<html[^>]*lang=" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|critical|SH-007|HTML element missing lang attribute|3.1.1|Add lang attribute: <html lang=\"en\">|<html without lang>")
    fi
  fi

  # Check for missing <title>
  if grep -qiE "<head[[:space:]>]" "$filepath" 2>/dev/null; then
    if ! grep -qiE "<title[[:space:]>]" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|high|SH-008|Document missing <title> element|2.4.2|Add <title> element inside <head>|Missing <title> in <head>")
    fi
  fi
}

# Special handler for Vue SFC files
scan_vue_file() {
  local filepath="$1"

  # Standard pattern scan
  scan_file "$filepath"

  # Vue-specific: check for v-html usage
  if grep -qE "v-html" "$filepath" 2>/dev/null; then
    local matches
    matches=$(grep -nE "v-html" "$filepath" 2>/dev/null || true)
    while IFS= read -r match_line; do
      [[ -z "$match_line" ]] && continue
      local line_num="${match_line%%:*}"
      FINDINGS+=("${filepath}|${line_num}|high|SH-010|v-html may inject inaccessible content|4.1.1|Ensure v-html content includes proper accessibility attributes|v-html directive")
    done <<< "$matches"
  fi
}

# Special handler for Svelte files
scan_svelte_file() {
  local filepath="$1"

  # Standard pattern scan
  scan_file "$filepath"

  # Svelte-specific: check for {@html} usage
  if grep -qE '\{@html' "$filepath" 2>/dev/null; then
    local matches
    matches=$(grep -nE '\{@html' "$filepath" 2>/dev/null || true)
    while IFS= read -r match_line; do
      [[ -z "$match_line" ]] && continue
      local line_num="${match_line%%:*}"
      FINDINGS+=("${filepath}|${line_num}|high|SH-010|{@html} may inject inaccessible content|4.1.1|Ensure {@html} content includes proper accessibility attributes|{@html} expression")
    done <<< "$matches"
  fi
}

# -- Calculate Accessibility Score ---------------------------------------------

# Calculate an accessibility score (0-100, higher is better) from findings.
# Score starts at 100 and points are deducted per finding.
calculate_score() {
  local score=100

  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _file _line severity _check _desc _wcag _rec _text <<< "$finding"
    local deduction
    deduction=$(severity_to_points "$severity")
    score=$((score - deduction))
  done

  # Floor at 0
  if [[ $score -lt 0 ]]; then
    score=0
  fi

  echo "$score"
}

# Score to letter grade
get_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 50 ]]; then echo "D"
  else echo "F"
  fi
}

# Color for grade
grade_color() {
  local grade="$1"
  case "$grade" in
    A) echo "$GREEN" ;;
    B) echo "$GREEN" ;;
    C) echo "$YELLOW" ;;
    D) echo "$RED" ;;
    F) echo "$RED" ;;
    *) echo "$NC" ;;
  esac
}

# Severity color
severity_color() {
  local sev="$1"
  case "$sev" in
    critical) echo "$RED" ;;
    high)     echo "$MAGENTA" ;;
    medium)   echo "$YELLOW" ;;
    low)      echo "$CYAN" ;;
    *)        echo "$NC" ;;
  esac
}

# Severity label
severity_label() {
  local sev="$1"
  case "$sev" in
    critical) echo "CRITICAL" ;;
    high)     echo "HIGH    " ;;
    medium)   echo "MEDIUM  " ;;
    low)      echo "LOW     " ;;
    *)        echo "UNKNOWN " ;;
  esac
}

# Category display label
category_label() {
  local cat_id="$1"
  local prefix="${cat_id%%-*}"
  case "$prefix" in
    AR) echo "ARIA & Roles" ;;
    SH) echo "Semantic HTML" ;;
    KB) echo "Keyboard Navigation" ;;
    FM) echo "Form Accessibility" ;;
    VS) echo "Color & Visual" ;;
    DY) echo "Dynamic Content" ;;
    *)  echo "Unknown" ;;
  esac
}

# -- Format Findings -----------------------------------------------------------

format_findings() {
  local finding="$1"
  IFS='|' read -r f_file f_line f_severity f_check f_desc f_wcag f_rec f_text <<< "$finding"

  local color
  color=$(severity_color "$f_severity")
  local label
  label=$(severity_label "$f_severity")
  local cat
  cat=$(category_label "$f_check")

  local display_file
  display_file=$(basename "$f_file")
  local ft
  ft=$(detect_filetype "$f_file")
  local ft_label
  ft_label=$(filetype_label "$ft")

  echo -e "  ${color}${BOLD}${label}${NC}  ${BOLD}${display_file}${NC}:${CYAN}${f_line}${NC}  ${DIM}[${f_check}] ${cat}${NC}"
  echo -e "           ${f_desc}"
  if [[ -n "${f_text:-}" && "$f_text" != "Missing"* ]]; then
    echo -e "           ${DIM}> ${f_text}${NC}"
  fi
  echo -e "           ${DIM}Fix: ${f_rec}${NC}"

  # Show WCAG reference
  if [[ -n "${f_wcag:-}" ]]; then
    local wcag_level
    wcag_level=$(get_wcag_level "$f_wcag")
    echo -e "           ${DIM}WCAG: ${f_wcag} (Level ${wcag_level})${NC}"
  fi

  echo ""
}

# -- Print Summary -------------------------------------------------------------

print_scan_summary() {
  local files_scanned="$1"
  local a11y_score="$2"

  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _w _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done

  local total=$((critical + high + medium + low))
  local grade
  grade=$(get_grade "$a11y_score")
  local gcolor
  gcolor=$(grade_color "$grade")

  echo -e "${BOLD}--- Scan Summary ---${NC}"
  echo ""
  echo -e "  Files scanned:     ${BOLD}$files_scanned${NC}"
  echo -e "  Total issues:      ${BOLD}$total${NC}"
  if [[ $critical -gt 0 ]]; then
    echo -e "    Critical:        ${RED}${BOLD}$critical${NC}"
  else
    echo -e "    Critical:        ${DIM}$critical${NC}"
  fi
  if [[ $high -gt 0 ]]; then
    echo -e "    High:            ${MAGENTA}${BOLD}$high${NC}"
  else
    echo -e "    High:            ${DIM}$high${NC}"
  fi
  if [[ $medium -gt 0 ]]; then
    echo -e "    Medium:          ${YELLOW}$medium${NC}"
  else
    echo -e "    Medium:          ${DIM}$medium${NC}"
  fi
  if [[ $low -gt 0 ]]; then
    echo -e "    Low:             ${CYAN}$low${NC}"
  else
    echo -e "    Low:             ${DIM}$low${NC}"
  fi
  echo ""
  echo -e "  A11y Score:        ${gcolor}${BOLD}$a11y_score/100${NC} (Grade: ${gcolor}${BOLD}$grade${NC})"
  echo ""

  if [[ $a11y_score -lt 70 ]]; then
    echo -e "  ${RED}${BOLD}FAIL${NC} — Accessibility score below 70. Review findings above."
  elif [[ $total -gt 0 ]]; then
    echo -e "  ${YELLOW}${BOLD}WARN${NC} — Issues found, but score is acceptable. Review recommended."
  else
    echo -e "  ${GREEN}${BOLD}PASS${NC} — No accessibility issues detected."
  fi
}

# -- Main Scan Orchestrator ----------------------------------------------------

# Main scan entry point. Finds template files, analyzes each, aggregates results.
# Usage: run_accesslint_scan <target> <max_files>
# max_files=0 means unlimited (Pro/Team), 5 for free tier
run_accesslint_scan() {
  local target="$1"
  local max_files="${2:-0}"

  if [[ ! -e "$target" ]]; then
    echo -e "${RED}[AccessLint]${NC} Target not found: ${BOLD}$target${NC}" >&2
    return 1
  fi

  # Find template files
  local -a template_files=()
  discover_template_files "$target" template_files

  if [[ ${#template_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[AccessLint]${NC} No template files found in ${BOLD}$target${NC}"
    echo -e "${DIM}  Searched for: *.html, *.jsx, *.tsx, *.vue, *.svelte, *.css, and more${NC}"
    return 0
  fi

  # Apply file limit for free tier
  local files_to_scan=("${template_files[@]}")
  local was_limited=false
  if [[ $max_files -gt 0 && ${#template_files[@]} -gt $max_files ]]; then
    files_to_scan=("${template_files[@]:0:$max_files}")
    was_limited=true
  fi

  echo -e "${BOLD}--- AccessLint Accessibility Scan ---${NC}"
  echo ""
  echo -e "Target:   ${BOLD}$target${NC}"
  echo -e "Files:    ${CYAN}${#template_files[@]}${NC} template file(s) found"

  if [[ "$was_limited" == true ]]; then
    echo -e "${YELLOW}  Free tier: scanning $max_files of ${#template_files[@]} files.${NC}"
    echo -e "${YELLOW}  Upgrade to Pro for unlimited scanning: ${CYAN}https://accesslint.pages.dev${NC}"
  fi

  # Show detected file types
  local -A ft_counts=()
  for file in "${files_to_scan[@]}"; do
    local ft
    ft=$(detect_filetype "$file")
    ft_counts[$ft]=$(( ${ft_counts[$ft]:-0} + 1 ))
  done

  echo -e "Types:    ${DIM}$(for t in "${!ft_counts[@]}"; do echo -n "$(filetype_label "$t") (${ft_counts[$t]}) "; done)${NC}"
  echo ""

  # Scan each file
  FINDINGS=()
  local files_scanned=0

  for file in "${files_to_scan[@]}"; do
    files_scanned=$((files_scanned + 1))
    local ft
    ft=$(detect_filetype "$file")
    local ft_lbl
    ft_lbl=$(filetype_label "$ft")

    echo -e "  ${DIM}[$files_scanned/${#files_to_scan[@]}]${NC} $(basename "$file") ${DIM}($ft_lbl)${NC}"

    case "$ft" in
      html)    scan_html_file "$file" ;;
      vue)     scan_vue_file "$file" ;;
      svelte)  scan_svelte_file "$file" ;;
      *)       scan_file "$file" ;;
    esac
  done

  echo ""

  # Print findings
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No accessibility issues detected.${NC}"
    echo ""
    print_scan_summary "$files_scanned" 100
    return 0
  fi

  echo -e "${BOLD}--- Findings ---${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
  done

  local a11y_score
  a11y_score=$(calculate_score)

  print_scan_summary "$files_scanned" "$a11y_score"

  # Exit code: 0 if score >= 70, 1 otherwise
  if [[ $a11y_score -lt 70 ]]; then
    return 1
  fi

  return 0
}

# -- Hook Entry Point ----------------------------------------------------------

# Pre-commit hook entry point. Scans staged files for accessibility issues.
# Returns exit code 1 if critical or high severity findings.
hook_accesslint_scan() {
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  # Filter for files that contain markup
  local -a staged_template_files=()
  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue
    local ft
    ft=$(detect_filetype "$file")
    if is_scannable_type "$ft"; then
      if has_markup_content "$file"; then
        staged_template_files+=("$file")
      fi
    fi
  done <<< "$staged_files"

  if [[ ${#staged_template_files[@]} -eq 0 ]]; then
    return 0
  fi

  echo -e "${BLUE}[AccessLint]${NC} Scanning ${#staged_template_files[@]} staged file(s) for accessibility issues..."

  FINDINGS=()
  local has_critical_or_high=false

  for file in "${staged_template_files[@]}"; do
    local ft
    ft=$(detect_filetype "$file")
    case "$ft" in
      html)    scan_html_file "$file" ;;
      vue)     scan_vue_file "$file" ;;
      svelte)  scan_svelte_file "$file" ;;
      *)       scan_file "$file" ;;
    esac
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[AccessLint]${NC} All staged files look accessible — no WCAG violations."
    return 0
  fi

  echo ""
  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
    IFS='|' read -r _f _l severity _c _d _w _r _t <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_critical_or_high=true
    fi
  done

  local a11y_score
  a11y_score=$(calculate_score)

  print_scan_summary "${#staged_template_files[@]}" "$a11y_score"

  if [[ "$has_critical_or_high" == true ]]; then
    echo ""
    echo -e "${RED}${BOLD}Commit blocked: Critical/high accessibility issues found.${NC}"
    echo -e "${DIM}Run 'accesslint scan' for details. Use 'git commit --no-verify' to skip (NOT recommended).${NC}"
    return 1
  fi

  return 0
}

# -- Generate Accessibility Report ---------------------------------------------

generate_accesslint_report() {
  local target="$1"

  # Find and scan all files (unlimited)
  local -a template_files=()
  discover_template_files "$target" template_files

  if [[ ${#template_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[AccessLint]${NC} No template files found. Nothing to report."
    return 0
  fi

  FINDINGS=()
  local files_scanned=0

  for file in "${template_files[@]}"; do
    files_scanned=$((files_scanned + 1))
    local ft
    ft=$(detect_filetype "$file")
    case "$ft" in
      html)    scan_html_file "$file" ;;
      vue)     scan_vue_file "$file" ;;
      svelte)  scan_svelte_file "$file" ;;
      *)       scan_file "$file" ;;
    esac
  done

  local a11y_score
  a11y_score=$(calculate_score)
  local grade
  grade=$(get_grade "$a11y_score")

  # Count by severity
  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _w _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done
  local total=$((critical + high + medium + low))

  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || pwd)")

  # Read template and substitute
  local template_path="$SKILL_DIR/templates/report.md.tmpl"
  if [[ ! -f "$template_path" ]]; then
    echo -e "${RED}[AccessLint]${NC} Report template not found at $template_path"
    return 1
  fi

  local report
  report=$(cat "$template_path")

  local report_date
  report_date=$(date +"%Y-%m-%d %H:%M:%S")

  # Build findings table
  local findings_table=""
  if [[ $total -gt 0 ]]; then
    local idx=0
    for finding in "${FINDINGS[@]}"; do
      idx=$((idx + 1))
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_wcag f_rec f_text <<< "$finding"
      local ft
      ft=$(detect_filetype "$f_file")
      local ft_lbl
      ft_lbl=$(filetype_label "$ft")
      local wcag_level
      wcag_level=$(get_wcag_level "${f_wcag:-}")
      findings_table+="| $idx | \`$(basename "$f_file")\` | $f_line | **$f_severity** | $f_check | $f_desc | ${f_wcag:-N/A} (${wcag_level}) | $ft_lbl |"$'\n'
    done
  fi

  # Build recommendations
  local recommendations_md=""
  if [[ $critical -gt 0 ]]; then
    recommendations_md+="- **URGENT:** $critical critical accessibility failure(s). These completely block access for some users. Fix immediately."$'\n'
  fi
  if [[ $high -gt 0 ]]; then
    recommendations_md+="- **HIGH PRIORITY:** $high high severity issue(s). These significantly degrade the accessible experience."$'\n'
  fi
  if [[ $medium -gt 0 ]]; then
    recommendations_md+="- **REVIEW:** $medium medium severity issue(s). Best practice violations that should be addressed."$'\n'
  fi
  if [[ $total -eq 0 ]]; then
    recommendations_md="No action items. All templates pass accessibility checks."
  fi

  # Perform substitutions
  report="${report//\{\{DATE\}\}/$report_date}"
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{A11Y_SCORE\}\}/$a11y_score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$files_scanned}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$critical}"
  report="${report//\{\{HIGH_COUNT\}\}/$high}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$medium}"
  report="${report//\{\{LOW_COUNT\}\}/$low}"
  report="${report//\{\{VERSION\}\}/$ACCESSLINT_VERSION}"

  # Multi-line substitutions
  report=$(echo "$report" | awk -v findings="$findings_table" '{gsub(/\{\{FINDINGS_TABLE\}\}/, findings); print}')
  report=$(echo "$report" | awk -v recs="$recommendations_md" '{gsub(/\{\{RECOMMENDATIONS\}\}/, recs); print}')

  # Output report
  local output_file="accesslint-report-$(date +%Y%m%d-%H%M%S).md"
  echo "$report" > "$output_file"

  echo -e "${GREEN}[AccessLint]${NC} Report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:     $files_scanned"
  echo -e "  Total issues:      $total"
  echo -e "  A11y score:        $a11y_score/100 (Grade: $grade)"
}

# -- Deep Accessibility Audit --------------------------------------------------

run_accesslint_audit() {
  local target="$1"

  echo -e "${BOLD}--- AccessLint Deep Accessibility Audit ---${NC}"
  echo ""

  # Find and scan all files (unlimited)
  local -a template_files=()
  discover_template_files "$target" template_files

  if [[ ${#template_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[AccessLint]${NC} No template files found."
    return 0
  fi

  FINDINGS=()
  local files_scanned=0
  local html_count=0
  local component_count=0
  local css_count=0

  for file in "${template_files[@]}"; do
    files_scanned=$((files_scanned + 1))
    local ft
    ft=$(detect_filetype "$file")
    local ft_lbl
    ft_lbl=$(filetype_label "$ft")

    echo -e "  ${DIM}[$files_scanned/${#template_files[@]}]${NC} $(basename "$file") ${DIM}($ft_lbl)${NC}"

    case "$ft" in
      html)
        scan_html_file "$file"
        html_count=$((html_count + 1))
        ;;
      vue)
        scan_vue_file "$file"
        component_count=$((component_count + 1))
        ;;
      svelte)
        scan_svelte_file "$file"
        component_count=$((component_count + 1))
        ;;
      jsx|tsx)
        scan_file "$file"
        component_count=$((component_count + 1))
        ;;
      css)
        scan_file "$file"
        css_count=$((css_count + 1))
        ;;
      *)
        scan_file "$file"
        ;;
    esac
  done

  echo ""

  # Print audit summary
  echo -e "${BOLD}--- Audit Overview ---${NC}"
  echo ""
  echo -e "  Total files analyzed:   ${BOLD}$files_scanned${NC}"
  echo -e "  HTML pages:             ${CYAN}$html_count${NC}"
  echo -e "  Components (JSX/Vue/Svelte): ${CYAN}$component_count${NC}"
  echo -e "  Stylesheets:            ${CYAN}$css_count${NC}"
  echo ""

  # File type breakdown
  local -A ft_counts=()
  for file in "${template_files[@]}"; do
    local ft
    ft=$(detect_filetype "$file")
    ft_counts[$ft]=$(( ${ft_counts[$ft]:-0} + 1 ))
  done

  echo -e "  ${BOLD}File Type Breakdown:${NC}"
  for t in "${!ft_counts[@]}"; do
    echo -e "    $(filetype_label "$t"): ${ft_counts[$t]} file(s)"
  done
  echo ""

  # Print findings
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No accessibility issues detected.${NC}"
    echo ""
    print_scan_summary "$files_scanned" 100
    return 0
  fi

  # Group findings by category
  local -A category_counts=()
  for finding in "${FINDINGS[@]}"; do
    IFS='|' read -r _f _l _s f_check _d _w _r _t <<< "$finding"
    local cat
    cat=$(category_label "$f_check")
    category_counts[$cat]=$(( ${category_counts[$cat]:-0} + 1 ))
  done

  echo -e "  ${BOLD}Issue Categories:${NC}"
  for cat in "${!category_counts[@]}"; do
    echo -e "    $cat: ${category_counts[$cat]} issue(s)"
  done
  echo ""

  echo -e "${BOLD}--- Findings ---${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
  done

  local a11y_score
  a11y_score=$(calculate_score)

  print_scan_summary "$files_scanned" "$a11y_score"

  if [[ $a11y_score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# -- Policy Enforcement --------------------------------------------------------

enforce_a11y_policy() {
  local target="$1"

  echo -e "${BOLD}--- AccessLint Policy Enforcement ---${NC}"
  echo ""

  # Load custom policies from config
  local -a custom_policies=()

  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    if command -v python3 &>/dev/null; then
      local raw
      raw=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    policies = cfg.get('skills', {}).get('entries', {}).get('accesslint', {}).get('config', {}).get('customPolicies', [])
    for p in policies:
        print(p.get('regex', '') + '|' + p.get('severity', 'medium') + '|CUSTOM|' + p.get('description', 'Custom policy') + '|' + p.get('wcag', 'N/A') + '|Fix according to organization policy')
except: pass
" 2>/dev/null) || true

      while IFS= read -r policy; do
        [[ -n "$policy" ]] && custom_policies+=("$policy")
      done <<< "$raw"
    fi
  fi

  if [[ ${#custom_policies[@]} -gt 0 ]]; then
    echo -e "Custom policies loaded: ${CYAN}${#custom_policies[@]}${NC}"
  else
    echo -e "${DIM}No custom policies configured.${NC}"
    echo -e "Add custom policies in ${CYAN}~/.openclaw/openclaw.json${NC}:"
    echo -e "  ${DIM}accesslint.config.customPolicies: [{ \"regex\": \"...\", \"severity\": \"high\", \"description\": \"...\", \"wcag\": \"1.1.1\" }]${NC}"
    echo ""
  fi

  # Run scan with built-in + custom patterns
  local -a template_files=()
  discover_template_files "$target" template_files

  if [[ ${#template_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[AccessLint]${NC} No template files found."
    return 0
  fi

  FINDINGS=()
  for file in "${template_files[@]}"; do
    local ft
    ft=$(detect_filetype "$file")
    case "$ft" in
      html)    scan_html_file "$file" ;;
      vue)     scan_vue_file "$file" ;;
      svelte)  scan_svelte_file "$file" ;;
      *)       scan_file "$file" ;;
    esac

    # Also check custom policies
    for policy in "${custom_policies[@]:-}"; do
      [[ -z "$policy" ]] && continue
      IFS='|' read -r regex severity check_id description wcag recommendation <<< "$policy"

      local matches
      matches=$(grep -nE "$regex" "$file" 2>/dev/null || true)
      if [[ -n "$matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local matched_text="${match_line#*:}"
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi
          FINDINGS+=("${file}|${line_num}|${severity}|${check_id}|${description}|${wcag}|${recommendation}|${matched_text}")
        done <<< "$matches"
      fi
    done
  done

  echo -e "Scanned ${BOLD}${#template_files[@]}${NC} file(s) with ${CYAN}$(accesslint_pattern_count)${NC} built-in + ${CYAN}${#custom_policies[@]}${NC} custom patterns"
  echo ""

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}All policies pass.${NC}"
    return 0
  fi

  echo -e "${BOLD}--- Policy Violations ---${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_findings "$finding"
  done

  local a11y_score
  a11y_score=$(calculate_score)
  print_scan_summary "${#template_files[@]}" "$a11y_score"

  if [[ $a11y_score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# -- WCAG 2.1 Compliance Report ------------------------------------------------

generate_wcag_compliance() {
  local target="$1"

  echo -e "${BOLD}--- AccessLint WCAG 2.1 Compliance Report ---${NC}"
  echo ""

  # Run full scan
  local -a template_files=()
  discover_template_files "$target" template_files

  if [[ ${#template_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[AccessLint]${NC} No template files found."
    return 0
  fi

  FINDINGS=()
  for file in "${template_files[@]}"; do
    local ft
    ft=$(detect_filetype "$file")
    case "$ft" in
      html)    scan_html_file "$file" ;;
      vue)     scan_vue_file "$file" ;;
      svelte)  scan_svelte_file "$file" ;;
      *)       scan_file "$file" ;;
    esac
  done

  local a11y_score
  a11y_score=$(calculate_score)
  local grade
  grade=$(get_grade "$a11y_score")

  # Count by severity
  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _w _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done
  local total=$((critical + high + medium + low))

  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || pwd)")

  local report_date
  report_date=$(date +"%Y-%m-%d %H:%M:%S")

  # Generate compliance report
  local output_file="accesslint-wcag-compliance-$(date +%Y%m%d-%H%M%S).md"

  {
    echo "# AccessLint WCAG 2.1 Compliance Report: $project_name"
    echo ""
    echo "> Generated by [AccessLint](https://accesslint.pages.dev) v${ACCESSLINT_VERSION} on $report_date"
    echo ""
    echo "## Executive Summary"
    echo ""
    echo "| Metric | Value |"
    echo "|--------|-------|"
    echo "| Accessibility Score | **$a11y_score/100** (Grade: **$grade**) |"
    echo "| Files Scanned | ${#template_files[@]} |"
    echo "| Total Findings | $total |"
    echo "| Critical | $critical |"
    echo "| High | $high |"
    echo "| Medium | $medium |"
    echo "| Low | $low |"
    echo ""

    # WCAG 2.1 Success Criteria Compliance
    echo "## WCAG 2.1 Success Criteria Compliance"
    echo ""

    # Perceivable (Principle 1)
    echo "### Principle 1: Perceivable"
    echo ""
    echo "| Criterion | Level | Status | Description |"
    echo "|-----------|-------|--------|-------------|"

    # 1.1.1 Non-text Content
    local status_111="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.1.1" ]]; then
        status_111="FAIL"
        break
      fi
    done
    echo "| 1.1.1 | A | **$status_111** | Non-text Content — alt text for images |"

    # 1.2.1 Audio-only and Video-only
    local status_121="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.2.1" ]]; then
        status_121="FAIL"
        break
      fi
    done
    echo "| 1.2.1 | A | **$status_121** | Audio/Video — alternatives provided |"

    # 1.2.2 Captions
    local status_122="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.2.2" ]]; then
        status_122="FAIL"
        break
      fi
    done
    echo "| 1.2.2 | A | **$status_122** | Captions — video has captions |"

    # 1.3.1 Info and Relationships
    local status_131="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.3.1" ]]; then
        status_131="FAIL"
        break
      fi
    done
    echo "| 1.3.1 | A | **$status_131** | Info and Relationships — semantic structure |"

    # 1.3.5 Identify Input Purpose
    local status_135="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.3.5" ]]; then
        status_135="FAIL"
        break
      fi
    done
    echo "| 1.3.5 | AA | **$status_135** | Identify Input Purpose — autocomplete |"

    # 1.4.1 Use of Color
    local status_141="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.4.1" ]]; then
        status_141="FAIL"
        break
      fi
    done
    echo "| 1.4.1 | A | **$status_141** | Use of Color — not sole indicator |"

    # 1.4.3 Contrast
    local status_143="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.4.3" ]]; then
        status_143="FAIL"
        break
      fi
    done
    echo "| 1.4.3 | AA | **$status_143** | Contrast (Minimum) — 4.5:1 ratio |"

    # 1.4.4 Resize Text
    local status_144="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "1.4.4" ]]; then
        status_144="FAIL"
        break
      fi
    done
    echo "| 1.4.4 | AA | **$status_144** | Resize Text — content zoomable |"

    echo ""

    # Operable (Principle 2)
    echo "### Principle 2: Operable"
    echo ""
    echo "| Criterion | Level | Status | Description |"
    echo "|-----------|-------|--------|-------------|"

    # 2.1.1 Keyboard
    local status_211="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "2.1.1" ]]; then
        status_211="FAIL"
        break
      fi
    done
    echo "| 2.1.1 | A | **$status_211** | Keyboard — all functionality via keyboard |"

    # 2.1.2 No Keyboard Trap
    local status_212="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "2.1.2" ]]; then
        status_212="FAIL"
        break
      fi
    done
    echo "| 2.1.2 | A | **$status_212** | No Keyboard Trap — focus can escape |"

    # 2.3.1 Three Flashes
    local status_231="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "2.3.1" ]]; then
        status_231="FAIL"
        break
      fi
    done
    echo "| 2.3.1 | A | **$status_231** | Three Flashes — no seizure-inducing content |"

    # 2.4.1 Bypass Blocks
    local status_241="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "2.4.1" ]]; then
        status_241="FAIL"
        break
      fi
    done
    echo "| 2.4.1 | A | **$status_241** | Bypass Blocks — skip navigation available |"

    # 2.4.2 Page Titled
    local status_242="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "2.4.2" ]]; then
        status_242="FAIL"
        break
      fi
    done
    echo "| 2.4.2 | A | **$status_242** | Page Titled — descriptive title |"

    # 2.4.3 Focus Order
    local status_243="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "2.4.3" ]]; then
        status_243="FAIL"
        break
      fi
    done
    echo "| 2.4.3 | A | **$status_243** | Focus Order — logical tab sequence |"

    # 2.4.7 Focus Visible
    local status_247="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "2.4.7" ]]; then
        status_247="FAIL"
        break
      fi
    done
    echo "| 2.4.7 | AA | **$status_247** | Focus Visible — keyboard focus indicator |"

    echo ""

    # Understandable (Principle 3)
    echo "### Principle 3: Understandable"
    echo ""
    echo "| Criterion | Level | Status | Description |"
    echo "|-----------|-------|--------|-------------|"

    # 3.1.1 Language of Page
    local status_311="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "3.1.1" ]]; then
        status_311="FAIL"
        break
      fi
    done
    echo "| 3.1.1 | A | **$status_311** | Language of Page — lang attribute |"

    # 3.2.1 On Focus
    local status_321="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "3.2.1" ]]; then
        status_321="FAIL"
        break
      fi
    done
    echo "| 3.2.1 | A | **$status_321** | On Focus — no unexpected context change |"

    # 3.3.1 Error Identification
    local status_331="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "3.3.1" ]]; then
        status_331="FAIL"
        break
      fi
    done
    echo "| 3.3.1 | A | **$status_331** | Error Identification — errors described |"

    # 3.3.2 Labels or Instructions
    local status_332="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "3.3.2" ]]; then
        status_332="FAIL"
        break
      fi
    done
    echo "| 3.3.2 | A | **$status_332** | Labels or Instructions — inputs labeled |"

    echo ""

    # Robust (Principle 4)
    echo "### Principle 4: Robust"
    echo ""
    echo "| Criterion | Level | Status | Description |"
    echo "|-----------|-------|--------|-------------|"

    # 4.1.1 Parsing
    local status_411="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "4.1.1" ]]; then
        status_411="FAIL"
        break
      fi
    done
    echo "| 4.1.1 | A | **$status_411** | Parsing — valid markup |"

    # 4.1.2 Name, Role, Value
    local status_412="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "4.1.2" ]]; then
        status_412="FAIL"
        break
      fi
    done
    echo "| 4.1.2 | A | **$status_412** | Name, Role, Value — ARIA attributes correct |"

    # 4.1.3 Status Messages
    local status_413="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s _c _d f_wcag _r _t <<< "$finding"
      if [[ "${f_wcag:-}" == "4.1.3" ]]; then
        status_413="FAIL"
        break
      fi
    done
    echo "| 4.1.3 | AA | **$status_413** | Status Messages — programmatically determined |"

    echo ""

    # Detailed findings
    if [[ $total -gt 0 ]]; then
      echo "## Detailed Findings"
      echo ""
      echo "| # | File | Line | Severity | Check | Description | WCAG | Level |"
      echo "|---|------|------|----------|-------|-------------|------|-------|"

      local idx=0
      for finding in "${FINDINGS[@]}"; do
        idx=$((idx + 1))
        IFS='|' read -r f_file f_line f_severity f_check f_desc f_wcag f_rec f_text <<< "$finding"
        local wcag_level
        wcag_level=$(get_wcag_level "${f_wcag:-}")
        echo "| $idx | \`$(basename "$f_file")\` | $f_line | **$f_severity** | $f_check | $f_desc | ${f_wcag:-N/A} | ${wcag_level} |"
      done

      echo ""

      echo "## Remediation Roadmap"
      echo ""
      if [[ $critical -gt 0 ]]; then
        echo "### Immediate (Critical)"
        echo ""
        for finding in "${FINDINGS[@]}"; do
          IFS='|' read -r f_file f_line f_severity f_check f_desc f_wcag f_rec f_text <<< "$finding"
          if [[ "$f_severity" == "critical" ]]; then
            echo "- **$f_check** (\`$(basename "$f_file")\`): $f_rec [WCAG ${f_wcag:-N/A}]"
          fi
        done
        echo ""
      fi
      if [[ $high -gt 0 ]]; then
        echo "### Short-term (High)"
        echo ""
        for finding in "${FINDINGS[@]}"; do
          IFS='|' read -r f_file f_line f_severity f_check f_desc f_wcag f_rec f_text <<< "$finding"
          if [[ "$f_severity" == "high" ]]; then
            echo "- **$f_check** (\`$(basename "$f_file")\`): $f_rec [WCAG ${f_wcag:-N/A}]"
          fi
        done
        echo ""
      fi
      if [[ $medium -gt 0 || $low -gt 0 ]]; then
        echo "### Medium-term (Medium/Low)"
        echo ""
        for finding in "${FINDINGS[@]}"; do
          IFS='|' read -r f_file f_line f_severity f_check f_desc f_wcag f_rec f_text <<< "$finding"
          if [[ "$f_severity" == "medium" || "$f_severity" == "low" ]]; then
            echo "- **$f_check** (\`$(basename "$f_file")\`): $f_rec [WCAG ${f_wcag:-N/A}]"
          fi
        done
        echo ""
      fi
    else
      echo "## Result"
      echo ""
      echo "All files pass WCAG 2.1 Level AA compliance checks."
      echo ""
      echo "### Recommendations"
      echo ""
      echo "- Install pre-commit hooks to maintain compliance: \`accesslint hooks install\`"
      echo "- Run periodic audits with: \`accesslint wcag\`"
      echo "- Add CI/CD integration for continuous compliance verification"
    fi

    echo ""
    echo "---"
    echo ""
    echo "*Report generated by [AccessLint](https://accesslint.pages.dev) v${ACCESSLINT_VERSION}. Run \`accesslint scan\` for interactive results.*"

  } > "$output_file"

  echo -e "${GREEN}[AccessLint]${NC} WCAG compliance report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:     ${#template_files[@]}"
  echo -e "  A11y score:        $a11y_score/100 (Grade: $grade)"
  echo -e "  Total findings:    $total"
}

# -- SARIF Output --------------------------------------------------------------

generate_sarif_output() {
  local target="$1"

  # Run full scan
  local -a template_files=()
  discover_template_files "$target" template_files

  if [[ ${#template_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[AccessLint]${NC} No template files found."
    return 0
  fi

  FINDINGS=()
  for file in "${template_files[@]}"; do
    local ft
    ft=$(detect_filetype "$file")
    case "$ft" in
      html)    scan_html_file "$file" ;;
      vue)     scan_vue_file "$file" ;;
      svelte)  scan_svelte_file "$file" ;;
      *)       scan_file "$file" ;;
    esac
  done

  local output_file="accesslint-results-$(date +%Y%m%d-%H%M%S).sarif"

  # Generate SARIF 2.1.0 JSON
  {
    echo '{'
    echo '  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",'
    echo '  "version": "2.1.0",'
    echo '  "runs": [{'
    echo '    "tool": {'
    echo '      "driver": {'
    echo "        \"name\": \"AccessLint\","
    echo "        \"version\": \"$ACCESSLINT_VERSION\","
    echo "        \"informationUri\": \"https://accesslint.pages.dev\","
    echo "        \"semanticVersion\": \"$ACCESSLINT_VERSION\","
    echo '        "rules": ['

    # Collect unique check IDs for rules
    local -A seen_rules=()
    local first_rule=true
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l f_severity f_check f_desc f_wcag f_rec _t <<< "$finding"
      if [[ -z "${seen_rules[$f_check]:-}" ]]; then
        seen_rules[$f_check]=1
        local sarif_level
        case "$f_severity" in
          critical|high) sarif_level="error" ;;
          medium)        sarif_level="warning" ;;
          low)           sarif_level="note" ;;
          *)             sarif_level="none" ;;
        esac

        if [[ "$first_rule" != true ]]; then
          echo ','
        fi
        first_rule=false

        echo '          {'
        echo "            \"id\": \"$f_check\","
        echo "            \"shortDescription\": { \"text\": \"$f_desc\" },"
        echo "            \"helpUri\": \"https://accesslint.pages.dev/rules/$f_check\","
        echo '            "defaultConfiguration": {'
        echo "              \"level\": \"$sarif_level\""
        echo '            },'
        echo '            "properties": {'
        echo "              \"tags\": [\"accessibility\", \"wcag-${f_wcag:-unknown}\"]"
        echo '            }'
        printf '          }'
      fi
    done

    echo ''
    echo '        ]'
    echo '      }'
    echo '    },'
    echo '    "results": ['

    # Output results
    local first_result=true
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_wcag f_rec f_text <<< "$finding"

      local sarif_level
      case "$f_severity" in
        critical|high) sarif_level="error" ;;
        medium)        sarif_level="warning" ;;
        low)           sarif_level="note" ;;
        *)             sarif_level="none" ;;
      esac

      # Escape special JSON characters
      local esc_desc
      esc_desc=$(echo "$f_desc" | sed 's/"/\\"/g')
      local esc_rec
      esc_rec=$(echo "$f_rec" | sed 's/"/\\"/g')

      if [[ "$first_result" != true ]]; then
        echo ','
      fi
      first_result=false

      echo '      {'
      echo "        \"ruleId\": \"$f_check\","
      echo "        \"level\": \"$sarif_level\","
      echo "        \"message\": { \"text\": \"$esc_desc. WCAG ${f_wcag:-N/A}. Fix: $esc_rec\" },"
      echo '        "locations": [{'
      echo '          "physicalLocation": {'
      echo "            \"artifactLocation\": { \"uri\": \"$f_file\" },"
      echo '            "region": {'
      echo "              \"startLine\": $f_line"
      echo '            }'
      echo '          }'
      echo '        }]'
      printf '      }'
    done

    echo ''
    echo '    ]'
    echo '  }]'
    echo '}'
  } > "$output_file"

  echo -e "${GREEN}[AccessLint]${NC} SARIF output generated: ${BOLD}$output_file${NC}"
  echo -e "  ${DIM}Compatible with GitHub Code Scanning, Azure DevOps, and SARIF viewers${NC}"
  echo -e "  Results: ${#FINDINGS[@]} finding(s) from ${#template_files[@]} file(s)"
}
