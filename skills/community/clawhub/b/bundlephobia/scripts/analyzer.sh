#!/usr/bin/env bash
# BundlePhobia — Core Analysis Engine
# Provides: project type detection, file discovery, pattern scanning, risk scoring,
#           report generation, dependency auditing, budget enforcement, SARIF output,
#           and pre-commit hook handler.
#
# This file is sourced by bundlephobia.sh and by the lefthook pre-commit hook.
# Requires patterns.sh to be sourced first.

set -euo pipefail

# ─── Colors (safe to re-declare; sourcing scripts may set these) ─────────────

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
BUNDLEPHOBIA_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

# ─── Project Type Detection ──────────────────────────────────────────────────

# Detect the JS/TS project type and package manager.
# Outputs: npm, yarn, pnpm, or monorepo
detect_project_type() {
  local dir="$1"

  if [[ -f "$dir/pnpm-workspace.yaml" ]] || [[ -f "$dir/lerna.json" ]]; then
    echo "monorepo"
    return 0
  fi

  if [[ -f "$dir/package.json" ]]; then
    if [[ -f "$dir/pnpm-lock.yaml" ]]; then
      echo "pnpm"
    elif [[ -f "$dir/yarn.lock" ]]; then
      echo "yarn"
    else
      echo "npm"
    fi
    return 0
  fi

  echo "unknown"
}

# Detect bundler type from config files
detect_bundler_type() {
  local dir="$1"

  if [[ -f "$dir/webpack.config.js" ]] || [[ -f "$dir/webpack.config.ts" ]] || [[ -f "$dir/webpack.config.mjs" ]]; then
    echo "webpack"
    return 0
  fi
  if [[ -f "$dir/vite.config.js" ]] || [[ -f "$dir/vite.config.ts" ]] || [[ -f "$dir/vite.config.mjs" ]]; then
    echo "vite"
    return 0
  fi
  if [[ -f "$dir/rollup.config.js" ]] || [[ -f "$dir/rollup.config.ts" ]] || [[ -f "$dir/rollup.config.mjs" ]]; then
    echo "rollup"
    return 0
  fi
  if [[ -f "$dir/esbuild.config.js" ]] || [[ -f "$dir/esbuild.config.mjs" ]]; then
    echo "esbuild"
    return 0
  fi
  if [[ -f "$dir/next.config.js" ]] || [[ -f "$dir/next.config.mjs" ]] || [[ -f "$dir/next.config.ts" ]]; then
    echo "nextjs"
    return 0
  fi
  if [[ -f "$dir/nuxt.config.js" ]] || [[ -f "$dir/nuxt.config.ts" ]]; then
    echo "nuxt"
    return 0
  fi
  if [[ -f "$dir/parcel.config.js" ]] || [[ -f "$dir/.parcelrc" ]]; then
    echo "parcel"
    return 0
  fi

  echo "unknown"
}

# ─── File Discovery ─────────────────────────────────────────────────────────

# Determine the file category for scanning
get_file_category() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')

  # package.json
  if [[ "$basename_lower" == "package.json" ]]; then
    echo "package"
    return 0
  fi

  # Bundler config files
  if [[ "$basename_lower" == webpack.config.* ]] || \
     [[ "$basename_lower" == vite.config.* ]] || \
     [[ "$basename_lower" == rollup.config.* ]] || \
     [[ "$basename_lower" == esbuild.config.* ]] || \
     [[ "$basename_lower" == next.config.* ]] || \
     [[ "$basename_lower" == nuxt.config.* ]] || \
     [[ "$basename_lower" == .parcelrc ]] || \
     [[ "$basename_lower" == parcel.config.* ]] || \
     [[ "$basename_lower" == tsconfig.json ]] || \
     [[ "$basename_lower" == babel.config.* ]] || \
     [[ "$basename_lower" == .babelrc ]]; then
    echo "config"
    return 0
  fi

  # JS/TS source files
  if [[ "$basename_lower" == *.js ]] || \
     [[ "$basename_lower" == *.jsx ]] || \
     [[ "$basename_lower" == *.ts ]] || \
     [[ "$basename_lower" == *.tsx ]] || \
     [[ "$basename_lower" == *.mjs ]] || \
     [[ "$basename_lower" == *.cjs ]]; then
    echo "source"
    return 0
  fi

  echo "unknown"
}

# Find all relevant files in a directory tree
discover_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  # If target is a single file
  if [[ -f "$search_dir" ]]; then
    local cat
    cat=$(get_file_category "$search_dir")
    if [[ "$cat" != "unknown" ]]; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  # Find package.json files (not in node_modules)
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name "node_modules" -o -name ".git" -o -name "dist" -o -name "build" -o -name ".next" -o -name "coverage" \) -prune -o \
    -name "package.json" -type f -print0 2>/dev/null)

  # Find bundler config files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 3 \
    \( -name "node_modules" -o -name ".git" -o -name "dist" -o -name "build" \) -prune -o \
    \( -name "webpack.config.*" -o -name "vite.config.*" -o -name "rollup.config.*" \
       -o -name "esbuild.config.*" -o -name "next.config.*" -o -name "nuxt.config.*" \
       -o -name ".parcelrc" -o -name "babel.config.*" -o -name ".babelrc" \) \
    -type f -print0 2>/dev/null)

  # Find JS/TS source files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name "node_modules" -o -name ".git" -o -name "dist" -o -name "build" -o -name ".next" \
       -o -name "coverage" -o -name "__tests__" -o -name "__mocks__" -o -name "*.test.*" \
       -o -name "*.spec.*" -o -name "*.stories.*" \) -prune -o \
    \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.mjs" -o -name "*.cjs" \) \
    -type f -print0 2>/dev/null)
}

# ─── Scan File With Patterns ───────────────────────────────────────────────

# Scan a single file against its category's patterns.
# Appends findings to global FINDINGS array.
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
scan_file() {
  local filepath="$1"
  local file_category="$2"

  # For package.json, run special handler
  if [[ "$file_category" == "package" ]]; then
    scan_package_json "$filepath"
    return 0
  fi

  # Determine which pattern arrays to use
  local -a pattern_arrays=()

  case "$file_category" in
    source)
      pattern_arrays=("BUNDLEPHOBIA_TREESHAKE_PATTERNS" "BUNDLEPHOBIA_OVERSIZED_PATTERNS")
      ;;
    config)
      pattern_arrays=("BUNDLEPHOBIA_CONFIG_PATTERNS")
      ;;
  esac

  for patterns_name in "${pattern_arrays[@]}"; do
    local -n _patterns_ref="$patterns_name"

    for entry in "${_patterns_ref[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

      # Skip placeholder patterns
      [[ "$regex" == PLACEHOLDER_* ]] && continue

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
          FINDINGS+=("${filepath}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}")
        done <<< "$matches"
      fi
    done
  done

  # Run file-level checks
  run_source_file_level_checks "$filepath" "$file_category"
}

# ─── Package.json Scanner ──────────────────────────────────────────────────

# Special handler for package.json — checks dependencies, devDependencies, etc.
scan_package_json() {
  local filepath="$1"

  # Scan oversized and hygiene patterns against the package.json
  for patterns_name in "BUNDLEPHOBIA_OVERSIZED_PATTERNS" "BUNDLEPHOBIA_HYGIENE_PATTERNS"; do
    local -n _patterns_ref="$patterns_name"

    for entry in "${_patterns_ref[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
      [[ "$regex" == PLACEHOLDER_* ]] && continue

      local matches
      matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local matched_text="${match_line#*:}"
          matched_text=$(echo "$matched_text" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
          if [[ ${#matched_text} -gt 120 ]]; then
            matched_text="${matched_text:0:117}..."
          fi
          FINDINGS+=("${filepath}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}")
        done <<< "$matches"
      fi
    done
  done

  # Run package.json file-level checks
  run_package_json_level_checks "$filepath"

  # Run duplicate dependency checks
  check_duplicate_dependencies "$filepath"
}

# ─── File-Level Checks ─────────────────────────────────────────────────────

run_source_file_level_checks() {
  local filepath="$1"
  local file_category="$2"

  # Only for config files
  if [[ "$file_category" == "config" ]]; then
    check_config_file_level "$filepath"
  fi
}

# Config file-level checks
check_config_file_level() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')

  # Webpack-specific checks
  if [[ "$basename_lower" == webpack.config.* ]]; then
    # BC-001: Missing splitChunks
    if ! grep -qE "splitChunks" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|BC-001|No webpack splitChunks configuration — all code in one bundle|Add optimization.splitChunks to separate vendor code|Missing splitChunks config")
    fi

    # BC-011: No terser/minification
    if ! grep -qE "(terser|minimize|TerserPlugin|UglifyJsPlugin|esbuild)" "$filepath" 2>/dev/null; then
      if ! grep -qE "mode:[[:space:]]*['\"]production['\"]" "$filepath" 2>/dev/null; then
        FINDINGS+=("${filepath}|1|high|BC-011|No minification plugin detected in webpack config|Add TerserPlugin or set mode: production for automatic minification|Missing terser/minification")
      fi
    fi

    # BC-016: No runtimeChunk
    if ! grep -qE "runtimeChunk" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|low|BC-016|Runtime chunk not separated — invalidates vendor cache on changes|Add optimization.runtimeChunk: single for better caching|Missing runtimeChunk")
    fi

    # BC-018: No CSS extraction
    if grep -qE "(css|style|sass|less)" "$filepath" 2>/dev/null; then
      if ! grep -qE "(MiniCssExtractPlugin|ExtractTextPlugin|mini-css-extract)" "$filepath" 2>/dev/null; then
        FINDINGS+=("${filepath}|1|medium|BC-018|CSS bundled with JS — no separate CSS extraction|Use MiniCssExtractPlugin to extract CSS into separate files|Missing CSS extraction")
      fi
    fi
  fi

  # Vite/Rollup/Next config — check for missing code splitting hint
  if [[ "$basename_lower" == vite.config.* ]] || [[ "$basename_lower" == rollup.config.* ]]; then
    # BC-015: No compression
    if ! grep -qE "(compress|gzip|brotli|vite-plugin-compress)" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|low|BC-015|No compression plugin configured (gzip/brotli)|Add vite-plugin-compression or rollup-plugin-gzip for pre-compressed assets|Missing compression plugin")
    fi
  fi
}

# Package.json file-level checks
run_package_json_level_checks() {
  local filepath="$1"

  # DH-009: Missing browserslist
  if ! grep -qE "\"browserslist\"" "$filepath" 2>/dev/null; then
    local dir
    dir=$(dirname "$filepath")
    if [[ ! -f "$dir/.browserslistrc" ]]; then
      FINDINGS+=("${filepath}|1|low|DH-009|No browserslist configuration — may include unnecessary polyfills|Add browserslist field to package.json or create .browserslistrc|Missing browserslist")
    fi
  fi

  # DH-010: No engines field
  if ! grep -qE "\"engines\"" "$filepath" 2>/dev/null; then
    FINDINGS+=("${filepath}|1|low|DH-010|No engines field in package.json — Node.js version not specified|Add engines.node to specify minimum Node.js version|Missing engines field")
  fi

  # DH-011: Missing sideEffects
  if ! grep -qE "\"sideEffects\"" "$filepath" 2>/dev/null; then
    # Only flag for libraries (those with "main" or "module" field)
    if grep -qE "\"(main|module|exports)\"" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|DH-011|No sideEffects field in package.json — hinders tree-shaking|Add \"sideEffects\": false (or array of files with side effects)|Missing sideEffects field")
    fi
  fi
}

# ─── Duplicate Dependency Checks ───────────────────────────────────────────

check_duplicate_dependencies() {
  local filepath="$1"
  local content
  content=$(cat "$filepath" 2>/dev/null) || return 0

  # Helper: check if both packages exist in deps
  check_both() {
    local pkg1="$1" pkg2="$2" check_id="$3" severity="$4" desc="$5" rec="$6"
    if echo "$content" | grep -qE "\"$pkg1\"[[:space:]]*:" && \
       echo "$content" | grep -qE "\"$pkg2\"[[:space:]]*:"; then
      FINDINGS+=("${filepath}|1|${severity}|${check_id}|${desc}|${rec}|Both $pkg1 and $pkg2 found")
    fi
  }

  # DD-001: Both axios and node-fetch
  check_both "axios" "node-fetch" "DD-001" "medium" \
    "Both axios and node-fetch detected — redundant HTTP clients" \
    "Choose one HTTP client; prefer native fetch() in Node 18+"

  # DD-002: Both moment and dayjs
  check_both "moment" "dayjs" "DD-002" "high" \
    "Both moment.js and dayjs detected — redundant date libraries" \
    "Remove moment.js; dayjs is the lighter alternative (2KB vs 290KB)"

  # DD-003: Both lodash and underscore
  check_both "lodash" "underscore" "DD-003" "high" \
    "Both lodash and underscore detected — redundant utility libraries" \
    "Remove underscore; use lodash-es or native methods"

  # DD-004: Both express and koa
  check_both "express" "koa" "DD-004" "medium" \
    "Both express and koa detected — redundant web frameworks" \
    "Choose one web framework to reduce dependencies"

  # DD-005: Both jest and mocha
  check_both "jest" "mocha" "DD-005" "medium" \
    "Both jest and mocha detected — redundant test runners" \
    "Standardize on one test runner to simplify dependencies"

  # DD-006: Multiple CSS-in-JS libs
  local css_in_js_count=0
  for pkg in "styled-components" "@emotion/react" "@emotion/styled" "styled-jsx" "linaria" "vanilla-extract" "stitches"; do
    if echo "$content" | grep -qE "\"$pkg\"[[:space:]]*:" 2>/dev/null; then
      css_in_js_count=$((css_in_js_count + 1))
    fi
  done
  if [[ $css_in_js_count -ge 2 ]]; then
    FINDINGS+=("${filepath}|1|medium|DD-006|Multiple CSS-in-JS libraries detected ($css_in_js_count) — redundant styling solutions|Standardize on one CSS-in-JS solution to reduce bundle size|$css_in_js_count CSS-in-JS libraries")
  fi

  # DD-007: Both uuid and nanoid
  check_both "uuid" "nanoid" "DD-007" "low" \
    "Both uuid and nanoid detected — redundant ID generators" \
    "Choose one: nanoid (130B) is much smaller than uuid (12KB)"

  # DD-008: Multiple loggers
  local logger_count=0
  for pkg in "winston" "bunyan" "pino" "log4js" "signale"; do
    if echo "$content" | grep -qE "\"$pkg\"[[:space:]]*:" 2>/dev/null; then
      logger_count=$((logger_count + 1))
    fi
  done
  if [[ $logger_count -ge 2 ]]; then
    FINDINGS+=("${filepath}|1|low|DD-008|Multiple logging libraries detected ($logger_count) — redundant loggers|Standardize on one logging library|$logger_count logging libraries")
  fi

  # DD-009: Both node-fetch and isomorphic-fetch
  check_both "node-fetch" "isomorphic-fetch" "DD-009" "medium" \
    "Both node-fetch and isomorphic-fetch detected" \
    "Use native fetch() or choose one polyfill"

  # DD-010: Both dotenv and env-cmd
  check_both "dotenv" "env-cmd" "DD-010" "low" \
    "Both dotenv and env-cmd detected — redundant env loaders" \
    "Choose one environment variable solution"

  # DD-011: Both chalk and colors
  check_both "chalk" "colors" "DD-011" "low" \
    "Both chalk and colors detected — redundant terminal color libraries" \
    "Choose one; chalk is actively maintained"

  # DD-012: Both yargs and commander
  check_both "yargs" "commander" "DD-012" "low" \
    "Both yargs and commander detected — redundant CLI argument parsers" \
    "Choose one CLI argument parser"

  # DD-015: Both core-js and babel-polyfill
  check_both "core-js" "babel-polyfill" "DD-015" "high" \
    "Both core-js and babel-polyfill — duplicate polyfills" \
    "Remove babel-polyfill (deprecated); use core-js with @babel/preset-env useBuiltIns: usage"

  # DD-016: Both webpack and rollup
  check_both "webpack" "rollup" "DD-016" "medium" \
    "Both webpack and rollup detected — unusual dual-bundler setup" \
    "Consolidate to one bundler unless intentionally using both for different targets"

  # DD-017: Both prop-types and typescript
  check_both "prop-types" "typescript" "DD-017" "low" \
    "Both prop-types and typescript detected — redundant type checking" \
    "TypeScript interfaces replace prop-types; remove prop-types to reduce bundle"
}

# ─── Calculate Security Score ──────────────────────────────────────────────

# Calculate a bloat score (0-100, higher is better) from findings.
# Score starts at 100 and points are deducted per finding.
calculate_score() {
  local score=100

  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _file _line severity _check _desc _rec _text <<< "$finding"
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

# File category display label
file_category_label() {
  local cat="$1"
  case "$cat" in
    package) echo "package.json" ;;
    config)  echo "Bundler Config" ;;
    source)  echo "JS/TS Source" ;;
    *)       echo "Unknown" ;;
  esac
}

# ─── Format Finding ───────────────────────────────────────────────────────

format_finding() {
  local finding="$1"
  IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"

  local color
  color=$(severity_color "$f_severity")
  local label
  label=$(severity_label "$f_severity")

  local display_file
  display_file=$(basename "$f_file")

  echo -e "  ${color}${BOLD}${label}${NC}  ${BOLD}${display_file}${NC}:${CYAN}${f_line}${NC}  ${DIM}[${f_check}]${NC}"
  echo -e "           ${f_desc}"
  if [[ -n "${f_text:-}" && "$f_text" != "Missing"* && "$f_text" != "Both "* ]]; then
    echo -e "           ${DIM}> ${f_text}${NC}"
  fi
  echo -e "           ${DIM}Fix: ${f_rec}${NC}"
  echo ""
}

# ─── Print Summary ─────────────────────────────────────────────────────────

print_scan_summary() {
  local files_scanned="$1"
  local bloat_score="$2"

  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done

  local total=$((critical + high + medium + low))
  local grade
  grade=$(get_grade "$bloat_score")
  local gcolor
  gcolor=$(grade_color "$grade")

  echo -e "${BOLD}━━━ Scan Summary ━━━${NC}"
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
  echo -e "  Bloat Score:       ${gcolor}${BOLD}$bloat_score/100${NC} (Grade: ${gcolor}${BOLD}$grade${NC})"
  echo ""

  if [[ $bloat_score -lt 70 ]]; then
    echo -e "  ${RED}${BOLD}FAIL${NC} — Bloat score below 70. Review findings above."
  elif [[ $total -gt 0 ]]; then
    echo -e "  ${YELLOW}${BOLD}WARN${NC} — Issues found, but score is acceptable. Review recommended."
  else
    echo -e "  ${GREEN}${BOLD}PASS${NC} — No bundle bloat detected."
  fi
}

# ─── Main Scan Orchestrator ────────────────────────────────────────────────

# Main scan entry point. Finds files, analyzes each, aggregates results.
# Usage: run_bundlephobia_scan <target> <max_files>
# max_files=0 means unlimited (Pro/Team), 5 for free tier
run_bundlephobia_scan() {
  local target="$1"
  local max_files="${2:-0}"

  if [[ ! -e "$target" ]]; then
    echo -e "${RED}[BundlePhobia]${NC} Target not found: ${BOLD}$target${NC}" >&2
    return 1
  fi

  # Detect project type
  local project_type
  if [[ -d "$target" ]]; then
    project_type=$(detect_project_type "$target")
  else
    project_type="file"
  fi

  local bundler_type="unknown"
  if [[ -d "$target" ]]; then
    bundler_type=$(detect_bundler_type "$target")
  fi

  # Find files
  local -a project_files=()
  discover_files "$target" project_files

  if [[ ${#project_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[BundlePhobia]${NC} No JS/TS files found in ${BOLD}$target${NC}"
    echo -e "${DIM}  Searched for: package.json, *.js, *.jsx, *.ts, *.tsx, webpack/vite/rollup configs${NC}"
    return 0
  fi

  # Apply file limit for free tier
  local files_to_scan=("${project_files[@]}")
  local was_limited=false
  if [[ $max_files -gt 0 && ${#project_files[@]} -gt $max_files ]]; then
    files_to_scan=("${project_files[@]:0:$max_files}")
    was_limited=true
  fi

  echo -e "${BOLD}━━━ BundlePhobia Bundle Bloat Scan ━━━${NC}"
  echo ""
  echo -e "Target:   ${BOLD}$target${NC}"
  echo -e "Project:  ${CYAN}$project_type${NC}"
  if [[ "$bundler_type" != "unknown" ]]; then
    echo -e "Bundler:  ${CYAN}$bundler_type${NC}"
  fi
  echo -e "Files:    ${CYAN}${#project_files[@]}${NC} file(s) found"

  if [[ "$was_limited" == true ]]; then
    echo -e "${YELLOW}  Free tier: scanning $max_files of ${#project_files[@]} files.${NC}"
    echo -e "${YELLOW}  Upgrade to Pro for unlimited scanning: ${CYAN}https://bundlephobia.pages.dev${NC}"
  fi

  # Show file category breakdown
  local -A cat_counts=()
  for file in "${files_to_scan[@]}"; do
    local fcat
    fcat=$(get_file_category "$file")
    cat_counts[$fcat]=$(( ${cat_counts[$fcat]:-0} + 1 ))
  done

  echo -e "Types:    ${DIM}$(for t in "${!cat_counts[@]}"; do echo -n "$(file_category_label "$t") (${cat_counts[$t]}) "; done)${NC}"
  echo ""

  # Scan each file
  FINDINGS=()
  local files_scanned=0

  for file in "${files_to_scan[@]}"; do
    files_scanned=$((files_scanned + 1))
    local fcat
    fcat=$(get_file_category "$file")
    local flabel
    flabel=$(file_category_label "$fcat")

    echo -e "  ${DIM}[$files_scanned/${#files_to_scan[@]}]${NC} $(basename "$file") ${DIM}($flabel)${NC}"

    if [[ "$fcat" != "unknown" ]]; then
      scan_file "$file" "$fcat"
    fi
  done

  echo ""

  # Print findings
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No bundle bloat detected.${NC}"
    echo ""
    print_scan_summary "$files_scanned" 100
    return 0
  fi

  echo -e "${BOLD}━━━ Findings ━━━${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
  done

  local bloat_score
  bloat_score=$(calculate_score)

  print_scan_summary "$files_scanned" "$bloat_score"

  # Exit code: 0 if score >= 70, 1 otherwise
  if [[ $bloat_score -lt 70 ]]; then
    return 1
  fi

  return 0
}

# ─── Hook Entry Point ─────────────────────────────────────────────────────

# Pre-commit hook entry point. Scans staged JS/TS files.
# Returns exit code 1 if critical or high severity findings.
hook_bundlephobia_scan() {
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  # Filter for JS/TS files and package.json
  local -a staged_targets=()
  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue
    local fcat
    fcat=$(get_file_category "$file")
    if [[ "$fcat" != "unknown" ]]; then
      staged_targets+=("$file")
    fi
  done <<< "$staged_files"

  if [[ ${#staged_targets[@]} -eq 0 ]]; then
    return 0
  fi

  echo -e "${BLUE}[BundlePhobia]${NC} Scanning ${#staged_targets[@]} staged file(s)..."

  FINDINGS=()
  local has_critical_or_high=false

  for file in "${staged_targets[@]}"; do
    local fcat
    fcat=$(get_file_category "$file")
    scan_file "$file" "$fcat"
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[BundlePhobia]${NC} All staged files look clean."
    return 0
  fi

  echo ""
  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    if [[ "$severity" == "critical" || "$severity" == "high" ]]; then
      has_critical_or_high=true
    fi
  done

  local bloat_score
  bloat_score=$(calculate_score)

  print_scan_summary "${#staged_targets[@]}" "$bloat_score"

  if [[ "$has_critical_or_high" == true ]]; then
    echo ""
    echo -e "${RED}${BOLD}Commit blocked: Critical/high bundle bloat in staged files.${NC}"
    echo -e "${DIM}Run 'bundlephobia scan' for details. Use 'git commit --no-verify' to skip (NOT recommended).${NC}"
    return 1
  fi

  return 0
}

# ─── Generate Bundle Health Report ─────────────────────────────────────────

generate_bundlephobia_report() {
  local target="$1"

  # Find and scan all files (unlimited)
  local -a project_files=()
  discover_files "$target" project_files

  if [[ ${#project_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[BundlePhobia]${NC} No JS/TS files found. Nothing to report."
    return 0
  fi

  FINDINGS=()
  local files_scanned=0

  for file in "${project_files[@]}"; do
    files_scanned=$((files_scanned + 1))
    local fcat
    fcat=$(get_file_category "$file")
    if [[ "$fcat" != "unknown" ]]; then
      scan_file "$file" "$fcat"
    fi
  done

  local bloat_score
  bloat_score=$(calculate_score)
  local grade
  grade=$(get_grade "$bloat_score")

  # Count by severity
  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
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
    echo -e "${RED}[BundlePhobia]${NC} Report template not found at $template_path"
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
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"
      findings_table+="| $idx | \`$(basename "$f_file")\` | $f_line | **$f_severity** | $f_check | $f_desc |"$'\n'
    done
  fi

  # Build recommendations
  local recommendations_md=""
  if [[ $critical -gt 0 ]]; then
    recommendations_md+="- **URGENT:** $critical critical bloat issue(s). These massively inflate your bundle. Fix immediately."$'\n'
  fi
  if [[ $high -gt 0 ]]; then
    recommendations_md+="- **HIGH PRIORITY:** $high high severity issue(s). These significantly increase bundle size."$'\n'
  fi
  if [[ $medium -gt 0 ]]; then
    recommendations_md+="- **REVIEW:** $medium medium severity issue(s). Best practice violations that should be addressed."$'\n'
  fi
  if [[ $total -eq 0 ]]; then
    recommendations_md="No action items. All files pass bundle bloat checks."
  fi

  # Perform substitutions
  report="${report//\{\{DATE\}\}/$report_date}"
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{SECURITY_SCORE\}\}/$bloat_score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$files_scanned}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$critical}"
  report="${report//\{\{HIGH_COUNT\}\}/$high}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$medium}"
  report="${report//\{\{LOW_COUNT\}\}/$low}"
  report="${report//\{\{VERSION\}\}/$BUNDLEPHOBIA_VERSION}"

  # Multi-line substitutions
  report=$(echo "$report" | awk -v findings="$findings_table" '{gsub(/\{\{FINDINGS_TABLE\}\}/, findings); print}')
  report=$(echo "$report" | awk -v recs="$recommendations_md" '{gsub(/\{\{RECOMMENDATIONS\}\}/, recs); print}')

  # Output report
  local output_file="bundlephobia-report-$(date +%Y%m%d-%H%M%S).md"
  echo "$report" > "$output_file"

  echo -e "${GREEN}[BundlePhobia]${NC} Report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:     $files_scanned"
  echo -e "  Total issues:      $total"
  echo -e "  Bloat score:       $bloat_score/100 (Grade: $grade)"
}

# ─── Deep Dependency Audit (PRO) ──────────────────────────────────────────

run_bundlephobia_audit() {
  local target="$1"

  echo -e "${BOLD}━━━ BundlePhobia Deep Dependency Audit ━━━${NC}"
  echo ""

  local pkg_json="$target/package.json"
  if [[ ! -f "$pkg_json" ]]; then
    echo -e "${RED}[BundlePhobia]${NC} No package.json found in $target"
    return 1
  fi

  # Run full scan first
  local -a project_files=()
  discover_files "$target" project_files

  FINDINGS=()
  for file in "${project_files[@]}"; do
    local fcat
    fcat=$(get_file_category "$file")
    if [[ "$fcat" != "unknown" ]]; then
      scan_file "$file" "$fcat"
    fi
  done

  local bloat_score
  bloat_score=$(calculate_score)
  local grade
  grade=$(get_grade "$bloat_score")

  # Count dependencies
  local dep_count=0
  local dev_dep_count=0
  if command -v node &>/dev/null; then
    dep_count=$(node -e "
try {
  const pkg = require('$pkg_json');
  console.log(Object.keys(pkg.dependencies || {}).length);
} catch(e) { console.log(0); }
" 2>/dev/null) || dep_count=0
    dev_dep_count=$(node -e "
try {
  const pkg = require('$pkg_json');
  console.log(Object.keys(pkg.devDependencies || {}).length);
} catch(e) { console.log(0); }
" 2>/dev/null) || dev_dep_count=0
  elif command -v python3 &>/dev/null; then
    dep_count=$(python3 -c "
import json
try:
    with open('$pkg_json') as f:
        pkg = json.load(f)
    print(len(pkg.get('dependencies', {})))
except: print(0)
" 2>/dev/null) || dep_count=0
    dev_dep_count=$(python3 -c "
import json
try:
    with open('$pkg_json') as f:
        pkg = json.load(f)
    print(len(pkg.get('devDependencies', {})))
except: print(0)
" 2>/dev/null) || dev_dep_count=0
  fi

  echo -e "  Dependencies:      ${BOLD}$dep_count${NC} production, ${DIM}$dev_dep_count dev${NC}"
  echo -e "  Files scanned:     ${BOLD}${#project_files[@]}${NC}"
  echo -e "  Bloat score:       $(grade_color "$grade")${BOLD}$bloat_score/100${NC} (Grade: $(grade_color "$grade")${BOLD}$grade${NC})"
  echo ""

  # Print findings categorized
  local critical=0 high=0 medium=0 low=0
  for finding in "${FINDINGS[@]:-}"; do
    [[ -z "$finding" ]] && continue
    IFS='|' read -r _f _l severity _c _d _r _t <<< "$finding"
    case "$severity" in
      critical) critical=$((critical + 1)) ;;
      high)     high=$((high + 1)) ;;
      medium)   medium=$((medium + 1)) ;;
      low)      low=$((low + 1)) ;;
    esac
  done

  if [[ ${#FINDINGS[@]} -gt 0 ]]; then
    echo -e "${BOLD}━━━ Audit Findings ━━━${NC}"
    echo ""
    for finding in "${FINDINGS[@]}"; do
      format_finding "$finding"
    done
  fi

  print_scan_summary "${#project_files[@]}" "$bloat_score"

  if [[ $bloat_score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# ─── Size Budget Enforcement (TEAM) ──────────────────────────────────────

enforce_size_budget() {
  local target="$1"

  echo -e "${BOLD}━━━ BundlePhobia Size Budget ━━━${NC}"
  echo ""

  # Load budget config
  local max_size="500KB"
  if [[ -f "$OPENCLAW_CONFIG" ]] && command -v python3 &>/dev/null; then
    local configured_size
    configured_size=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('skills', {}).get('entries', {}).get('bundlephobia', {}).get('config', {}).get('maxBundleSize', '500KB'))
except: print('500KB')
" 2>/dev/null) || true
    [[ -n "$configured_size" ]] && max_size="$configured_size"
  fi

  echo -e "Budget:   ${BOLD}$max_size${NC} max bundle size"
  echo ""

  # Run full scan
  local -a project_files=()
  discover_files "$target" project_files

  FINDINGS=()
  for file in "${project_files[@]}"; do
    local fcat
    fcat=$(get_file_category "$file")
    if [[ "$fcat" != "unknown" ]]; then
      scan_file "$file" "$fcat"
    fi
  done

  local bloat_score
  bloat_score=$(calculate_score)
  local grade
  grade=$(get_grade "$bloat_score")

  # Check for dist/build directory sizes
  local total_dist_size=0
  for dist_dir in "dist" "build" ".next" "out"; do
    if [[ -d "$target/$dist_dir" ]]; then
      local dir_size
      dir_size=$(du -sk "$target/$dist_dir" 2>/dev/null | cut -f1 || echo "0")
      total_dist_size=$((total_dist_size + dir_size))
      echo -e "  ${DIM}$dist_dir/:${NC} ${BOLD}${dir_size}KB${NC}"
    fi
  done

  if [[ $total_dist_size -gt 0 ]]; then
    echo -e "  Total build output: ${BOLD}${total_dist_size}KB${NC}"
    echo ""
  else
    echo -e "  ${DIM}No build output found (dist/, build/, .next/, out/)${NC}"
    echo -e "  ${DIM}Run your build command first for accurate size measurement${NC}"
    echo ""
  fi

  print_scan_summary "${#project_files[@]}" "$bloat_score"

  if [[ $bloat_score -lt 70 ]]; then
    echo ""
    echo -e "${RED}${BOLD}Budget enforcement FAILED.${NC}"
    return 1
  fi

  echo ""
  echo -e "${GREEN}${BOLD}Budget enforcement PASSED.${NC}"
  return 0
}

# ─── SARIF Output (TEAM) ──────────────────────────────────────────────────

generate_sarif_output() {
  local target="$1"

  # Run full scan
  local -a project_files=()
  discover_files "$target" project_files

  FINDINGS=()
  for file in "${project_files[@]}"; do
    local fcat
    fcat=$(get_file_category "$file")
    if [[ "$fcat" != "unknown" ]]; then
      scan_file "$file" "$fcat"
    fi
  done

  local output_file="bundlephobia-results.sarif"

  # Generate SARIF JSON
  {
    echo '{'
    echo '  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",'
    echo '  "version": "2.1.0",'
    echo '  "runs": [{'
    echo '    "tool": {'
    echo '      "driver": {'
    echo "        \"name\": \"BundlePhobia\","
    echo "        \"version\": \"$BUNDLEPHOBIA_VERSION\","
    echo '        "informationUri": "https://bundlephobia.pages.dev",'
    echo '        "rules": []'
    echo '      }'
    echo '    },'
    echo '    "results": ['

    local first=true
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"

      local sarif_level="note"
      case "$f_severity" in
        critical) sarif_level="error" ;;
        high)     sarif_level="error" ;;
        medium)   sarif_level="warning" ;;
        low)      sarif_level="note" ;;
      esac

      if [[ "$first" != true ]]; then
        echo ','
      fi
      first=false

      # Escape strings for JSON
      local escaped_desc
      escaped_desc=$(echo "$f_desc" | sed 's/"/\\"/g')
      local escaped_rec
      escaped_rec=$(echo "$f_rec" | sed 's/"/\\"/g')
      local escaped_file
      escaped_file=$(echo "$f_file" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')

      echo '      {'
      echo "        \"ruleId\": \"$f_check\","
      echo "        \"level\": \"$sarif_level\","
      echo '        "message": {'
      echo "          \"text\": \"$escaped_desc. Fix: $escaped_rec\""
      echo '        },'
      echo '        "locations": [{'
      echo '          "physicalLocation": {'
      echo '            "artifactLocation": {'
      echo "              \"uri\": \"$escaped_file\""
      echo '            },'
      echo '            "region": {'
      echo "              \"startLine\": $f_line"
      echo '            }'
      echo '          }'
      echo '        }]'
      echo -n '      }'
    done

    echo ''
    echo '    ]'
    echo '  }]'
    echo '}'

  } > "$output_file"

  echo -e "${GREEN}[BundlePhobia]${NC} SARIF output written to ${BOLD}$output_file${NC}"
  echo -e "  Upload to GitHub Code Scanning or any SARIF-compatible tool."
  echo -e "  Total findings: ${BOLD}${#FINDINGS[@]}${NC}"
}
