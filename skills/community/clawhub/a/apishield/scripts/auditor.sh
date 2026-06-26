#!/usr/bin/env bash
# APIShield -- Core Auditing Engine
# Provides: framework detection, route file discovery, security scanning,
#           score calculation, inventory, report, compliance, and hook support.
#
# Sourced by apishield.sh. Requires patterns.sh to be loaded first.

set -euo pipefail

# ─── Colors (safe to re-declare) ──────────────────────────────────────────────

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

APISHIELD_VERSION="${VERSION:-1.0.0}"

# ─── Globals / Accumulators ──────────────────────────────────────────────────

TOTAL_FILES_SCANNED=0
TOTAL_ENDPOINTS=0
TOTAL_ISSUES=0
CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0
LOW_COUNT=0
ALL_FINDINGS=""
ALL_ENDPOINTS_LIST=""
DETECTED_FRAMEWORK="unknown"

# ─── Exclude directories ─────────────────────────────────────────────────────

EXCLUDE_DIRS=(".git" "node_modules" "dist" "build" "vendor" "__pycache__" ".next" ".nuxt" "coverage" ".venv" "venv" "env" ".tox")

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

# ─── Framework Detection ─────────────────────────────────────────────────────
# Detect the primary API framework in a directory by looking for signature files.

detect_api_framework() {
  local target="$1"

  if [[ -f "$target" ]]; then
    # Single file — detect by content
    detect_file_framework "$target"
    return
  fi

  # Directory-level detection
  # Express/Node
  if [[ -f "$target/package.json" ]]; then
    if grep -q '"express"' "$target/package.json" 2>/dev/null; then
      echo "express"; return
    fi
    if grep -q '"next"' "$target/package.json" 2>/dev/null; then
      echo "nextjs"; return
    fi
    if grep -q '"fastify"' "$target/package.json" 2>/dev/null; then
      echo "express"; return  # Fastify patterns similar to Express
    fi
  fi

  # Next.js app directory
  if [[ -d "$target/app/api" || -d "$target/pages/api" || -d "$target/src/app/api" ]]; then
    echo "nextjs"; return
  fi

  # FastAPI
  if [[ -f "$target/requirements.txt" ]]; then
    if grep -qi "fastapi" "$target/requirements.txt" 2>/dev/null; then
      echo "fastapi"; return
    fi
    if grep -qi "flask" "$target/requirements.txt" 2>/dev/null; then
      echo "flask"; return
    fi
    if grep -qi "django" "$target/requirements.txt" 2>/dev/null; then
      echo "django"; return
    fi
  fi
  if [[ -f "$target/pyproject.toml" ]]; then
    if grep -qi "fastapi" "$target/pyproject.toml" 2>/dev/null; then
      echo "fastapi"; return
    fi
    if grep -qi "flask" "$target/pyproject.toml" 2>/dev/null; then
      echo "flask"; return
    fi
    if grep -qi "django" "$target/pyproject.toml" 2>/dev/null; then
      echo "django"; return
    fi
  fi

  # Django
  if [[ -f "$target/manage.py" || -d "$target/django" ]]; then
    echo "django"; return
  fi

  # Rails
  if [[ -f "$target/Gemfile" ]]; then
    if grep -q "rails" "$target/Gemfile" 2>/dev/null; then
      echo "rails"; return
    fi
  fi

  # Flask
  if compgen -G "$target/*.py" &>/dev/null; then
    local pyf
    for pyf in "$target"/*.py; do
      if grep -q "from flask" "$pyf" 2>/dev/null || grep -q "import flask" "$pyf" 2>/dev/null; then
        echo "flask"; return
      fi
    done
  fi

  echo "unknown"
}

# Detect framework for a single file based on content
detect_file_framework() {
  local filepath="$1"
  local ext="${filepath##*.}"

  case "$ext" in
    js|ts|jsx|tsx)
      if grep -qE "(app\.(get|post|put|delete|patch)|router\.(get|post|put|delete|patch)|express\(\))" "$filepath" 2>/dev/null; then
        echo "express"; return
      fi
      if grep -qE "(NextResponse|NextRequest|export.*(GET|POST|PUT|DELETE))" "$filepath" 2>/dev/null; then
        echo "nextjs"; return
      fi
      echo "express"  # Default for JS/TS
      ;;
    py)
      if grep -qE "(@app\.(get|post|put|delete|patch)|FastAPI|APIRouter)" "$filepath" 2>/dev/null; then
        echo "fastapi"; return
      fi
      if grep -qE "(@app\.route|Flask|Blueprint)" "$filepath" 2>/dev/null; then
        echo "flask"; return
      fi
      if grep -qE "(class.*View|urlpatterns|ViewSet|APIView)" "$filepath" 2>/dev/null; then
        echo "django"; return
      fi
      echo "flask"  # Default for Python
      ;;
    rb)
      echo "rails"
      ;;
    *)
      echo "unknown"
      ;;
  esac
}

# ─── Route File Discovery ────────────────────────────────────────────────────
# Find files likely to contain API route definitions.

find_route_files() {
  local target="$1"
  local max_files="${2:-0}"  # 0 = unlimited
  local count=0

  if [[ -f "$target" ]]; then
    echo "$target"
    return
  fi

  # Route file name patterns
  local route_patterns=(
    "route" "routes" "router" "routers"
    "api" "endpoint" "endpoints"
    "controller" "controllers"
    "view" "views"
    "handler" "handlers"
    "urls" "urlconf"
    "app" "server" "index" "main"
  )

  local extensions=("js" "ts" "jsx" "tsx" "py" "rb")

  # Find all source files, then filter for route-like content
  local found_files=()
  local ext f
  for ext in "${extensions[@]}"; do
    while IFS= read -r f; do
      [[ -z "$f" ]] && continue
      should_exclude "$f" && continue
      found_files+=("$f")
    done < <(find "$target" -name "*.$ext" -type f 2>/dev/null)
  done

  # Score each file: prioritize route-like filenames, then check content
  local scored_files=()
  for f in "${found_files[@]}"; do
    local base_lower
    base_lower=$(basename "$f" | tr '[:upper:]' '[:lower:]')
    local score=0

    # Filename scoring
    local p
    for p in "${route_patterns[@]}"; do
      if [[ "$base_lower" == *"$p"* ]]; then
        score=$((score + 10))
        break
      fi
    done

    # Directory scoring
    local dir_lower
    dir_lower=$(dirname "$f" | tr '[:upper:]' '[:lower:]')
    for p in "${route_patterns[@]}"; do
      if [[ "$dir_lower" == *"$p"* ]]; then
        score=$((score + 5))
        break
      fi
    done

    # Content scoring — check if file actually has route definitions
    if grep -qE '(app\.(get|post|put|delete|patch|all|use)|router\.(get|post|put|delete|patch)|@app\.(route|get|post|put|delete)|@router\.(get|post|put|delete)|path\s*\(|url\s*\(|export.*(GET|POST|PUT|DELETE)|def\s+(index|show|create|update|destroy))' "$f" 2>/dev/null; then
      score=$((score + 20))
    fi

    if [[ $score -gt 0 ]]; then
      scored_files+=("$score|$f")
    fi
  done

  # Sort by score descending and output
  local entry
  for entry in $(printf '%s\n' "${scored_files[@]}" | sort -t'|' -k1 -rn); do
    local file_path="${entry#*|}"
    echo "$file_path"
    count=$((count + 1))
    if [[ $max_files -gt 0 && $count -ge $max_files ]]; then
      return
    fi
  done
}

# ─── Count endpoints in a file ───────────────────────────────────────────────

count_endpoints() {
  local filepath="$1"
  local framework="$2"
  local count=0

  case "$framework" in
    express)
      count=$(grep -cE '(app|router)\.(get|post|put|delete|patch|all)\s*\(' "$filepath" 2>/dev/null || echo 0)
      ;;
    fastapi)
      count=$(grep -cE '@(app|router)\.(get|post|put|delete|patch)\s*\(' "$filepath" 2>/dev/null || echo 0)
      ;;
    flask)
      count=$(grep -cE '@(app|.*)\.(route)\s*\(' "$filepath" 2>/dev/null || echo 0)
      ;;
    django)
      count=$(grep -cE '(path|url)\s*\(' "$filepath" 2>/dev/null || echo 0)
      ;;
    rails)
      count=$(grep -cE 'def\s+(index|show|create|update|destroy|new|edit)\b' "$filepath" 2>/dev/null || echo 0)
      ;;
    nextjs)
      count=$(grep -cE 'export\s+(async\s+)?function\s+(GET|POST|PUT|DELETE|PATCH)\b' "$filepath" 2>/dev/null || echo 0)
      ;;
  esac

  echo "$count"
}

# ─── Pattern Scanning ─────────────────────────────────────────────────────────
# Run pattern arrays against a file and collect findings.

scan_file_with_patterns() {
  local filepath="$1"
  shift
  local pattern_arrays=("$@")
  local findings=""

  local arr_name
  for arr_name in "${pattern_arrays[@]}"; do
    # Get the array by reference
    local -n patterns_ref="$arr_name" 2>/dev/null || continue

    local entry
    for entry in "${patterns_ref[@]}"; do
      # Entry format: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
      local regex severity check_id description recommendation

      # Split by | (patterns have complex regexes so split from the back)
      regex=$(echo "$entry" | cut -d'|' -f1)
      severity=$(echo "$entry" | cut -d'|' -f2)
      check_id=$(echo "$entry" | cut -d'|' -f3)
      description=$(echo "$entry" | cut -d'|' -f4)
      recommendation=$(echo "$entry" | cut -d'|' -f5)

      # Skip empty patterns
      [[ -z "$regex" ]] && continue

      # Search for the pattern
      local line_matches
      line_matches=$(grep -nE "$regex" "$filepath" 2>/dev/null || true)

      if [[ -n "$line_matches" ]]; then
        while IFS= read -r match_line; do
          [[ -z "$match_line" ]] && continue
          local line_num="${match_line%%:*}"
          local line_content="${match_line#*:}"
          # Trim long lines
          if [[ ${#line_content} -gt 120 ]]; then
            line_content="${line_content:0:120}..."
          fi

          findings+="$filepath|$line_num|$check_id|$severity|$description|$recommendation|$line_content"$'\n'

          # Increment counters
          TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
          case "$severity" in
            critical) CRITICAL_COUNT=$((CRITICAL_COUNT + 1)) ;;
            high)     HIGH_COUNT=$((HIGH_COUNT + 1)) ;;
            medium)   MEDIUM_COUNT=$((MEDIUM_COUNT + 1)) ;;
            low)      LOW_COUNT=$((LOW_COUNT + 1)) ;;
          esac
        done <<< "$line_matches"
      fi
    done
  done

  echo -n "$findings"
}

# ─── Check for auth middleware / decorators ──────────────────────────────────
# Returns true (0) if file appears to have auth applied at the file level

has_file_level_auth() {
  local filepath="$1"
  local framework="$2"

  case "$framework" in
    express)
      # Check for app.use(auth) or middleware at top level
      grep -qE '(app\.use\s*\(.*auth|middleware.*auth|passport\.|jwt\.|verify.*token)' "$filepath" 2>/dev/null
      ;;
    fastapi)
      grep -qE '(Depends\s*\(.*auth|Security\(|OAuth2)' "$filepath" 2>/dev/null
      ;;
    flask)
      grep -qE '(@login_required|@auth|before_request.*auth|flask_login)' "$filepath" 2>/dev/null
      ;;
    django)
      grep -qE '(permission_classes|login_required|IsAuthenticated|@authentication_classes)' "$filepath" 2>/dev/null
      ;;
    rails)
      grep -qE '(before_action\s*:authenticate|before_action\s*:require_login|devise)' "$filepath" 2>/dev/null
      ;;
    nextjs)
      grep -qE '(getServerSession|auth\(\)|getSession|NextAuth|withAuth)' "$filepath" 2>/dev/null
      ;;
    *)
      return 1
      ;;
  esac
}

# Check for rate limiting at file level
has_file_level_ratelimit() {
  local filepath="$1"
  grep -qE '(rateLimit|rate_limit|RateLimiter|throttle|Throttle|slowDown|limiter)' "$filepath" 2>/dev/null
}

# Check for input validation at file level
has_file_level_validation() {
  local filepath="$1"
  grep -qE '(Joi\.|Zod\.|yup\.|validate|validator|Schema|serializer|Pydantic|BaseModel|marshmallow|wtforms)' "$filepath" 2>/dev/null
}

# ─── Scan a Single File ──────────────────────────────────────────────────────

scan_single_file() {
  local filepath="$1"
  local framework="${2:-}"

  if [[ -z "$framework" ]]; then
    framework=$(detect_file_framework "$filepath")
  fi

  # Determine which pattern arrays to scan with
  local pattern_arrays=()

  # Framework-specific patterns
  case "$framework" in
    express)
      # Only check auth patterns if file doesn't have file-level auth
      if ! has_file_level_auth "$filepath" "express"; then
        pattern_arrays+=("EXPRESS_AUTH_PATTERNS")
      fi
      if ! has_file_level_ratelimit "$filepath"; then
        pattern_arrays+=("EXPRESS_RATELIMIT_PATTERNS")
      fi
      if ! has_file_level_validation "$filepath"; then
        pattern_arrays+=("EXPRESS_VALIDATION_PATTERNS")
      fi
      ;;
    fastapi)
      if ! has_file_level_auth "$filepath" "fastapi"; then
        pattern_arrays+=("FASTAPI_AUTH_PATTERNS")
      fi
      if ! has_file_level_validation "$filepath"; then
        pattern_arrays+=("FASTAPI_VALIDATION_PATTERNS")
      fi
      ;;
    flask)
      if ! has_file_level_auth "$filepath" "flask"; then
        pattern_arrays+=("FLASK_AUTH_PATTERNS")
      fi
      if ! has_file_level_validation "$filepath"; then
        pattern_arrays+=("FLASK_VALIDATION_PATTERNS")
      fi
      ;;
    django)
      if ! has_file_level_auth "$filepath" "django"; then
        pattern_arrays+=("DJANGO_AUTH_PATTERNS")
      fi
      if ! has_file_level_validation "$filepath"; then
        pattern_arrays+=("DJANGO_VALIDATION_PATTERNS")
      fi
      ;;
    rails)
      if ! has_file_level_auth "$filepath" "rails"; then
        pattern_arrays+=("RAILS_AUTH_PATTERNS")
      fi
      if ! has_file_level_validation "$filepath"; then
        pattern_arrays+=("RAILS_VALIDATION_PATTERNS")
      fi
      ;;
    nextjs)
      if ! has_file_level_auth "$filepath" "nextjs"; then
        pattern_arrays+=("NEXTJS_AUTH_PATTERNS")
      fi
      if ! has_file_level_validation "$filepath"; then
        pattern_arrays+=("NEXTJS_VALIDATION_PATTERNS")
      fi
      ;;
  esac

  # Cross-framework patterns (always check)
  pattern_arrays+=("CORS_PATTERNS" "DEBUG_PATTERNS" "INJECTION_PATTERNS" "SENSITIVE_DATA_PATTERNS" "CSRF_PATTERNS" "ERROR_LEAK_PATTERNS" "GENERIC_SECURITY_PATTERNS")

  # Load patterns if not already loaded
  if [[ -z "${CORS_PATTERNS+x}" ]]; then
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    source "$script_dir/patterns.sh"
  fi

  # Run scan
  local file_findings
  file_findings=$(scan_file_with_patterns "$filepath" "${pattern_arrays[@]}")

  # Count endpoints
  local endpoints
  endpoints=$(count_endpoints "$filepath" "$framework")
  TOTAL_ENDPOINTS=$((TOTAL_ENDPOINTS + endpoints))

  TOTAL_FILES_SCANNED=$((TOTAL_FILES_SCANNED + 1))
  ALL_FINDINGS+="$file_findings"

  echo -n "$file_findings"
}

# ─── Security Score Calculation ───────────────────────────────────────────────
# Score 0–100 based on severity-weighted findings and endpoint count

calculate_security_score() {
  local total_endpoints="${1:-$TOTAL_ENDPOINTS}"
  local critical="${2:-$CRITICAL_COUNT}"
  local high="${3:-$HIGH_COUNT}"
  local medium="${4:-$MEDIUM_COUNT}"
  local low="${5:-$LOW_COUNT}"

  # Base score
  local score=100

  # Deductions (weighted)
  local penalty=0
  penalty=$((critical * 25 + high * 10 + medium * 4 + low * 1))

  # Scale penalty relative to number of endpoints (more endpoints = smaller per-issue impact)
  if [[ $total_endpoints -gt 0 ]]; then
    local adjusted_penalty=$(( (penalty * 10) / (total_endpoints + 5) ))
    score=$((100 - adjusted_penalty))
  else
    score=$((100 - penalty))
  fi

  # Clamp to 0–100
  [[ $score -lt 0 ]] && score=0
  [[ $score -gt 100 ]] && score=100

  echo "$score"
}

get_grade() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "A"
  elif [[ $score -ge 80 ]]; then echo "B"
  elif [[ $score -ge 70 ]]; then echo "C"
  elif [[ $score -ge 60 ]]; then echo "D"
  else echo "F"
  fi
}

get_score_color() {
  local score="$1"
  if [[ $score -ge 90 ]]; then echo "$GREEN"
  elif [[ $score -ge 70 ]]; then echo "$YELLOW"
  else echo "$RED"
  fi
}

# ─── Output Formatting ───────────────────────────────────────────────────────

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
    critical) echo "🔴" ;;
    high)     echo "🟠" ;;
    medium)   echo "🟡" ;;
    low)      echo "⚪" ;;
    *)        echo "  " ;;
  esac
}

print_finding() {
  local filepath="$1" line_num="$2" check_id="$3" severity="$4" description="$5" recommendation="$6" line_content="$7"
  local color
  color=$(severity_color "$severity")
  local icon
  icon=$(severity_icon "$severity")

  echo -e "  ${icon} ${color}${BOLD}[${severity^^}]${NC} ${check_id}"
  echo -e "    ${DIM}${filepath}:${line_num}${NC}"
  echo -e "    ${description}"
  if [[ -n "$line_content" ]]; then
    echo -e "    ${DIM}> ${line_content}${NC}"
  fi
  echo -e "    ${CYAN}Fix: ${recommendation}${NC}"
  echo ""
}

print_findings_summary() {
  local findings="$1"
  [[ -z "$findings" ]] && return

  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local filepath line_num check_id severity description recommendation line_content
    IFS='|' read -r filepath line_num check_id severity description recommendation line_content <<< "$line"
    print_finding "$filepath" "$line_num" "$check_id" "$severity" "$description" "$recommendation" "$line_content"
  done <<< "$findings"
}

# ─── Main Scan Command ───────────────────────────────────────────────────────

do_api_scan() {
  local target="$1"
  local max_files="${2:-0}"

  # Reset accumulators
  TOTAL_FILES_SCANNED=0
  TOTAL_ENDPOINTS=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  # Load patterns
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Detect framework
  DETECTED_FRAMEWORK=$(detect_api_framework "$target")
  if [[ "$DETECTED_FRAMEWORK" != "unknown" ]]; then
    echo -e "  Framework: ${BOLD}${DETECTED_FRAMEWORK}${NC}"
  else
    echo -e "  Framework: ${DIM}auto-detect (all patterns)${NC}"
  fi

  # Find route files
  local route_files
  route_files=$(find_route_files "$target" "$max_files")

  if [[ -z "$route_files" ]]; then
    echo ""
    echo -e "  ${GREEN}✓${NC} No route files found — clean scan."
    echo -e "  ${DIM}Tip: run from your API project root, or specify a routes directory.${NC}"
    return 0
  fi

  local file_count=0
  local truncated=false
  while IFS= read -r rf; do
    [[ -z "$rf" ]] && continue
    file_count=$((file_count + 1))
  done <<< "$route_files"

  if [[ $max_files -gt 0 && $file_count -ge $max_files ]]; then
    truncated=true
  fi

  echo -e "  Files: ${BOLD}${file_count}${NC} route file(s)"
  echo ""

  # Scan each file
  while IFS= read -r rf; do
    [[ -z "$rf" ]] && continue
    local rel_path="${rf#$target/}"
    [[ "$rel_path" == "$rf" ]] && rel_path="$rf"

    echo -e "  ${DIM}Scanning: ${rel_path}${NC}"
    local file_framework
    file_framework=$(detect_file_framework "$rf")
    scan_single_file "$rf" "$file_framework"
  done <<< "$route_files"

  # Calculate score
  local score
  score=$(calculate_security_score)
  local grade
  grade=$(get_grade "$score")
  local score_color
  score_color=$(get_score_color "$score")

  # Output summary
  echo ""
  echo -e "  ═══════════════════════════════════════════════════════════════"
  echo -e "  ${BOLD}APIShield Security Scan Results${NC}"
  echo -e "  ═══════════════════════════════════════════════════════════════"
  echo ""
  echo -e "  Security Score: ${score_color}${BOLD}${score}/100 (${grade})${NC}"
  echo ""
  echo -e "  ${DIM}Files scanned:${NC}  ${TOTAL_FILES_SCANNED}"
  echo -e "  ${DIM}Endpoints:${NC}      ${TOTAL_ENDPOINTS}"
  echo -e "  ${DIM}Total issues:${NC}   ${TOTAL_ISSUES}"

  if [[ $TOTAL_ISSUES -gt 0 ]]; then
    echo ""
    [[ $CRITICAL_COUNT -gt 0 ]] && echo -e "  ${RED}● Critical:${NC}  ${CRITICAL_COUNT}"
    [[ $HIGH_COUNT -gt 0 ]]     && echo -e "  ${YELLOW}● High:${NC}      ${HIGH_COUNT}"
    [[ $MEDIUM_COUNT -gt 0 ]]   && echo -e "  ${BLUE}● Medium:${NC}    ${MEDIUM_COUNT}"
    [[ $LOW_COUNT -gt 0 ]]      && echo -e "  ${DIM}● Low:${NC}       ${LOW_COUNT}"
  fi

  echo ""

  # Print detailed findings
  if [[ -n "$ALL_FINDINGS" ]]; then
    echo -e "  ${BOLD}Findings:${NC}"
    echo ""
    print_findings_summary "$ALL_FINDINGS"
  else
    echo -e "  ${GREEN}✓ No security issues found.${NC}"
  fi

  # Free tier warning
  if [[ "$truncated" == true ]]; then
    echo -e "  ${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  ${YELLOW}⚠${NC}  Free tier: scanned ${max_files} of ${file_count}+ route files."
    echo -e "  ${YELLOW}⚠${NC}  Upgrade to Pro for unlimited scanning: ${CYAN}https://apishield.pages.dev/pricing${NC}"
    echo -e "  ${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
  fi

  # Exit code: 0 if score >= 70 and no critical issues, 1 otherwise
  if [[ $score -lt 70 || $CRITICAL_COUNT -gt 0 ]]; then
    return 1
  fi
  return 0
}

# ─── Hook Scan (for lefthook pre-commit) ─────────────────────────────────────

hook_api_scan() {
  echo -e "${BLUE}[APIShield]${NC} Scanning staged route files for security issues..."

  # Get staged files
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    echo -e "${GREEN}[APIShield]${NC} No staged files to scan."
    return 0
  fi

  # Filter to relevant extensions
  local route_files=""
  local ext
  while IFS= read -r sf; do
    [[ -z "$sf" ]] && continue
    ext="${sf##*.}"
    case "$ext" in
      js|ts|jsx|tsx|py|rb) route_files+="$sf"$'\n' ;;
    esac
  done <<< "$staged_files"

  if [[ -z "$route_files" ]]; then
    echo -e "${GREEN}[APIShield]${NC} No route files in staged changes."
    return 0
  fi

  # Load patterns
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Reset counters
  TOTAL_FILES_SCANNED=0
  TOTAL_ENDPOINTS=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  # Scan each staged file
  local has_route_content=false
  while IFS= read -r rf; do
    [[ -z "$rf" ]] && continue
    [[ ! -f "$rf" ]] && continue

    # Quick check: does this file have route-like content?
    if grep -qE '(app\.(get|post|put|delete|patch)|router\.(get|post|put|delete|patch)|@app\.(route|get|post|put|delete)|@router\.(get|post|put|delete)|path\s*\(|export.*(GET|POST|PUT|DELETE)|def\s+(index|show|create|update|destroy))' "$rf" 2>/dev/null; then
      has_route_content=true
      local fw
      fw=$(detect_file_framework "$rf")
      scan_single_file "$rf" "$fw"
    fi
  done <<< "$route_files"

  if [[ "$has_route_content" == false ]]; then
    echo -e "${GREEN}[APIShield]${NC} No API routes in staged files."
    return 0
  fi

  # Summary
  if [[ $CRITICAL_COUNT -gt 0 ]]; then
    echo -e "${RED}[APIShield]${NC} ${BOLD}${CRITICAL_COUNT} critical issue(s)${NC} found in staged files!"
    if [[ -n "$ALL_FINDINGS" ]]; then
      print_findings_summary "$ALL_FINDINGS"
    fi
    return 1
  fi

  if [[ $TOTAL_ISSUES -gt 0 ]]; then
    echo -e "${YELLOW}[APIShield]${NC} ${TOTAL_ISSUES} issue(s) found (${HIGH_COUNT} high, ${MEDIUM_COUNT} medium, ${LOW_COUNT} low)"
    return 0  # Non-critical issues don't block commit
  fi

  echo -e "${GREEN}[APIShield]${NC} ✓ Staged routes look secure."
  return 0
}

# ─── Generate Report (Pro+) ──────────────────────────────────────────────────

generate_report() {
  local target="$1"

  # Run full scan first (silently capture findings)
  echo -e "${BLUE}[APIShield]${NC} Running full security scan..."
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Reset counters
  TOTAL_FILES_SCANNED=0
  TOTAL_ENDPOINTS=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  DETECTED_FRAMEWORK=$(detect_api_framework "$target")

  local route_files
  route_files=$(find_route_files "$target" 0)

  if [[ -z "$route_files" ]]; then
    echo -e "${YELLOW}[APIShield]${NC} No route files found — nothing to report."
    return 0
  fi

  while IFS= read -r rf; do
    [[ -z "$rf" ]] && continue
    local fw
    fw=$(detect_file_framework "$rf")
    scan_single_file "$rf" "$fw" >/dev/null
  done <<< "$route_files"

  local score
  score=$(calculate_security_score)
  local grade
  grade=$(get_grade "$score")

  # Format findings for markdown
  local md_findings=""
  if [[ -n "$ALL_FINDINGS" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local fp ln cid sev desc rec lc
      IFS='|' read -r fp ln cid sev desc rec lc <<< "$line"
      md_findings+="### ${sev^^}: ${cid}"$'\n'
      md_findings+="- **File:** \`${fp}:${ln}\`"$'\n'
      md_findings+="- **Severity:** ${sev}"$'\n'
      md_findings+="- **Description:** ${desc}"$'\n'
      md_findings+="- **Fix:** ${rec}"$'\n'
      [[ -n "$lc" ]] && md_findings+="- **Code:** \`${lc}\`"$'\n'
      md_findings+=""$'\n'
    done <<< "$ALL_FINDINGS"
  else
    md_findings="No security issues found."$'\n'
  fi

  # Build recommendations
  local recommendations=""
  [[ $CRITICAL_COUNT -gt 0 ]] && recommendations+="- **URGENT:** Fix ${CRITICAL_COUNT} critical issue(s) immediately"$'\n'
  [[ $HIGH_COUNT -gt 0 ]] && recommendations+="- Fix ${HIGH_COUNT} high-severity issue(s) before next release"$'\n'
  [[ $MEDIUM_COUNT -gt 0 ]] && recommendations+="- Address ${MEDIUM_COUNT} medium-severity issue(s) in upcoming sprint"$'\n'
  [[ $LOW_COUNT -gt 0 ]] && recommendations+="- Review ${LOW_COUNT} low-severity finding(s) for best practices"$'\n'
  [[ -z "$recommendations" ]] && recommendations="No recommendations — your API routes look secure!"$'\n'

  # Load template and substitute
  local template_path="$script_dir/../templates/report.md.tmpl"
  local report_content
  if [[ -f "$template_path" ]]; then
    report_content=$(< "$template_path")
  else
    # Inline fallback
    report_content="# APIShield Security Audit Report\n\n**Score:** {{SECURITY_SCORE}}/100 ({{GRADE}})\n\n## Findings\n\n{{FINDINGS}}\n\n## Recommendations\n\n{{RECOMMENDATIONS}}"
  fi

  local project_name
  project_name=$(basename "$(cd "$target" 2>/dev/null && pwd || echo "$target")")
  local today
  today=$(date +%Y-%m-%d)

  report_content="${report_content//\{\{DATE\}\}/$today}"
  report_content="${report_content//\{\{PROJECT\}\}/$project_name}"
  report_content="${report_content//\{\{SECURITY_SCORE\}\}/$score}"
  report_content="${report_content//\{\{GRADE\}\}/$grade}"
  report_content="${report_content//\{\{FILES_SCANNED\}\}/$TOTAL_FILES_SCANNED}"
  report_content="${report_content//\{\{ENDPOINTS_FOUND\}\}/$TOTAL_ENDPOINTS}"
  report_content="${report_content//\{\{TOTAL_ISSUES\}\}/$TOTAL_ISSUES}"
  report_content="${report_content//\{\{CRITICAL_COUNT\}\}/$CRITICAL_COUNT}"
  report_content="${report_content//\{\{HIGH_COUNT\}\}/$HIGH_COUNT}"
  report_content="${report_content//\{\{MEDIUM_COUNT\}\}/$MEDIUM_COUNT}"
  report_content="${report_content//\{\{LOW_COUNT\}\}/$LOW_COUNT}"
  report_content="${report_content//\{\{FRAMEWORK\}\}/$DETECTED_FRAMEWORK}"
  report_content="${report_content//\{\{FINDINGS\}\}/$md_findings}"
  report_content="${report_content//\{\{OWASP_MAPPING\}\}/See compliance command for full OWASP mapping.}"
  report_content="${report_content//\{\{RECOMMENDATIONS\}\}/$recommendations}"
  report_content="${report_content//\{\{VERSION\}\}/$APISHIELD_VERSION}"

  local report_file="APISHIELD-REPORT.md"
  echo -e "$report_content" > "$report_file"

  echo -e "${GREEN}[APIShield]${NC} Report generated: ${BOLD}${report_file}${NC}"
  echo -e "  Score: ${score}/100 (${grade})"
  echo -e "  Issues: ${TOTAL_ISSUES} (${CRITICAL_COUNT} critical, ${HIGH_COUNT} high, ${MEDIUM_COUNT} medium, ${LOW_COUNT} low)"
}

# ─── Generate Inventory (Team+) ──────────────────────────────────────────────

generate_inventory() {
  local target="$1"

  echo -e "${BLUE}[APIShield]${NC} Generating API endpoint inventory..."

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  DETECTED_FRAMEWORK=$(detect_api_framework "$target")

  local route_files
  route_files=$(find_route_files "$target" 0)

  if [[ -z "$route_files" ]]; then
    echo -e "${YELLOW}[APIShield]${NC} No route files found."
    return 0
  fi

  echo ""
  echo -e "| ${BOLD}Method${NC} | ${BOLD}Path${NC} | ${BOLD}File${NC} | ${BOLD}Auth${NC} | ${BOLD}Rate Limit${NC} | ${BOLD}Validation${NC} |"
  echo "|--------|------|------|------|------------|------------|"

  while IFS= read -r rf; do
    [[ -z "$rf" ]] && continue
    local fw
    fw=$(detect_file_framework "$rf")
    local has_auth="❌"
    local has_rl="❌"
    local has_val="❌"

    has_file_level_auth "$rf" "$fw" && has_auth="✅"
    has_file_level_ratelimit "$rf" && has_rl="✅"
    has_file_level_validation "$rf" && has_val="✅"

    local rel="${rf#$target/}"
    [[ "$rel" == "$rf" ]] && rel="$rf"

    # Extract routes based on framework
    case "$fw" in
      express)
        grep -nE '(app|router)\.(get|post|put|delete|patch|all)\s*\(' "$rf" 2>/dev/null | while IFS= read -r line; do
          local method path_str
          method=$(echo "$line" | grep -oE '\.(get|post|put|delete|patch|all)' | tr -d '.' | tr '[:lower:]' '[:upper:]')
          path_str=$(echo "$line" | grep -oE "['\"][^'\"]*['\"]" | head -1 | tr -d "'" | tr -d '"')
          [[ -z "$path_str" ]] && path_str="?"
          echo "| ${method:-?} | ${path_str} | ${rel} | ${has_auth} | ${has_rl} | ${has_val} |"
        done
        ;;
      fastapi)
        grep -nE '@(app|router)\.(get|post|put|delete|patch)\s*\(' "$rf" 2>/dev/null | while IFS= read -r line; do
          local method path_str
          method=$(echo "$line" | grep -oE '\.(get|post|put|delete|patch)' | tr -d '.' | tr '[:lower:]' '[:upper:]')
          path_str=$(echo "$line" | grep -oE "['\"][^'\"]*['\"]" | head -1 | tr -d "'" | tr -d '"')
          [[ -z "$path_str" ]] && path_str="?"
          echo "| ${method:-?} | ${path_str} | ${rel} | ${has_auth} | ${has_rl} | ${has_val} |"
        done
        ;;
      flask)
        grep -nE '@(app|.*)\.(route)\s*\(' "$rf" 2>/dev/null | while IFS= read -r line; do
          local path_str methods_str
          path_str=$(echo "$line" | grep -oE "['\"][^'\"]*['\"]" | head -1 | tr -d "'" | tr -d '"')
          methods_str=$(echo "$line" | grep -oE "methods=\[.*\]" | grep -oE "'[A-Z]+'" | tr -d "'" | tr '\n' ',' | sed 's/,$//')
          [[ -z "$methods_str" ]] && methods_str="GET"
          [[ -z "$path_str" ]] && path_str="?"
          echo "| ${methods_str} | ${path_str} | ${rel} | ${has_auth} | ${has_rl} | ${has_val} |"
        done
        ;;
      django)
        grep -nE '(path|url)\s*\(' "$rf" 2>/dev/null | while IFS= read -r line; do
          local path_str
          path_str=$(echo "$line" | grep -oE "['\"][^'\"]*['\"]" | head -1 | tr -d "'" | tr -d '"')
          [[ -z "$path_str" ]] && path_str="?"
          echo "| ALL | ${path_str} | ${rel} | ${has_auth} | ${has_rl} | ${has_val} |"
        done
        ;;
      rails)
        grep -nE 'def\s+(index|show|create|update|destroy|new|edit)\b' "$rf" 2>/dev/null | while IFS= read -r line; do
          local action
          action=$(echo "$line" | grep -oE 'def\s+\w+' | awk '{print $2}')
          local method="GET"
          case "$action" in
            create) method="POST" ;;
            update) method="PUT" ;;
            destroy) method="DELETE" ;;
          esac
          echo "| ${method} | ${action} | ${rel} | ${has_auth} | ${has_rl} | ${has_val} |"
        done
        ;;
      nextjs)
        grep -nE 'export\s+(async\s+)?function\s+(GET|POST|PUT|DELETE|PATCH)\b' "$rf" 2>/dev/null | while IFS= read -r line; do
          local method
          method=$(echo "$line" | grep -oE '(GET|POST|PUT|DELETE|PATCH)')
          local path_str="$rel"
          echo "| ${method:-?} | ${path_str} | ${rel} | ${has_auth} | ${has_rl} | ${has_val} |"
        done
        ;;
    esac
  done <<< "$route_files"

  echo ""
  echo -e "${GREEN}[APIShield]${NC} Inventory complete."
}

# ─── Generate Compliance Report (Team+) ──────────────────────────────────────

generate_compliance() {
  local target="$1"

  echo -e "${BLUE}[APIShield]${NC} Running OWASP API Security Top 10 compliance check..."

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  source "$script_dir/patterns.sh"

  # Run full scan first
  TOTAL_FILES_SCANNED=0
  TOTAL_ENDPOINTS=0
  TOTAL_ISSUES=0
  CRITICAL_COUNT=0
  HIGH_COUNT=0
  MEDIUM_COUNT=0
  LOW_COUNT=0
  ALL_FINDINGS=""

  DETECTED_FRAMEWORK=$(detect_api_framework "$target")

  local route_files
  route_files=$(find_route_files "$target" 0)

  if [[ -n "$route_files" ]]; then
    while IFS= read -r rf; do
      [[ -z "$rf" ]] && continue
      local fw
      fw=$(detect_file_framework "$rf")
      scan_single_file "$rf" "$fw" >/dev/null
    done <<< "$route_files"
  fi

  # Map findings to OWASP categories
  declare -A owasp_map
  owasp_map["API1:2023 Broken Object Level Authorization"]=""
  owasp_map["API2:2023 Broken Authentication"]=""
  owasp_map["API3:2023 Broken Object Property Level Authorization"]=""
  owasp_map["API4:2023 Unrestricted Resource Consumption"]=""
  owasp_map["API5:2023 Broken Function Level Authorization"]=""
  owasp_map["API6:2023 Unrestricted Access to Sensitive Business Flows"]=""
  owasp_map["API7:2023 Server Side Request Forgery"]=""
  owasp_map["API8:2023 Security Misconfiguration"]=""
  owasp_map["API9:2023 Improper Inventory Management"]=""
  owasp_map["API10:2023 Unsafe Consumption of APIs"]=""

  if [[ -n "$ALL_FINDINGS" ]]; then
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      local cid
      cid=$(echo "$line" | cut -d'|' -f3)

      case "$cid" in
        *IDOR*|*OBJECT*|*DIRECT*)
          owasp_map["API1:2023 Broken Object Level Authorization"]+="$cid "
          ;;
        *AUTH*|*NO_AUTH*|*SKIP_AUTH*)
          owasp_map["API2:2023 Broken Authentication"]+="$cid "
          ;;
        *PERMIT_ALL*|*STRONG_PARAMS*|*MASS*|*VALIDATION*)
          owasp_map["API3:2023 Broken Object Property Level Authorization"]+="$cid "
          ;;
        *RATELIMIT*|*RATE*)
          owasp_map["API4:2023 Unrestricted Resource Consumption"]+="$cid "
          ;;
        *ADMIN*|*WILDCARD_METHOD*|*FUNCTION*)
          owasp_map["API5:2023 Broken Function Level Authorization"]+="$cid "
          ;;
        *CSRF*)
          owasp_map["API6:2023 Unrestricted Access to Sensitive Business Flows"]+="$cid "
          ;;
        *SSRF*|*HTTP*|*INSECURE_HTTP*)
          owasp_map["API7:2023 Server Side Request Forgery"]+="$cid "
          ;;
        *CORS*|*DEBUG*|*ERROR*|*SSL*|*HELMET*|*NODE_ENV*)
          owasp_map["API8:2023 Security Misconfiguration"]+="$cid "
          ;;
        *INTERNAL*|*TEST*|*HEALTH*)
          owasp_map["API9:2023 Improper Inventory Management"]+="$cid "
          ;;
        *INJECTION*|*EXEC*|*EVAL*|*SQL*)
          owasp_map["API10:2023 Unsafe Consumption of APIs"]+="$cid "
          ;;
        *SENSITIVE*|*PASSWORD*|*SECRET*|*APIKEY*|*TOKEN*|*BEARER*|*SSN*|*CREDIT*)
          owasp_map["API3:2023 Broken Object Property Level Authorization"]+="$cid "
          ;;
      esac
    done <<< "$ALL_FINDINGS"
  fi

  # Output compliance report
  echo ""
  echo -e "  ${BOLD}OWASP API Security Top 10 (2023) Compliance Report${NC}"
  echo -e "  ══════════════════════════════════════════════════════"
  echo ""

  local covered=0
  local total=10
  local category
  for category in \
    "API1:2023 Broken Object Level Authorization" \
    "API2:2023 Broken Authentication" \
    "API3:2023 Broken Object Property Level Authorization" \
    "API4:2023 Unrestricted Resource Consumption" \
    "API5:2023 Broken Function Level Authorization" \
    "API6:2023 Unrestricted Access to Sensitive Business Flows" \
    "API7:2023 Server Side Request Forgery" \
    "API8:2023 Security Misconfiguration" \
    "API9:2023 Improper Inventory Management" \
    "API10:2023 Unsafe Consumption of APIs"; do

    local findings_for="${owasp_map[$category]}"
    if [[ -n "$findings_for" ]]; then
      echo -e "  ${RED}✗${NC} ${BOLD}${category}${NC}"
      echo -e "    ${DIM}Triggered by: ${findings_for}${NC}"
      echo ""
    else
      echo -e "  ${GREEN}✓${NC} ${BOLD}${category}${NC}"
      echo -e "    ${DIM}No issues detected${NC}"
      echo ""
      covered=$((covered + 1))
    fi
  done

  echo -e "  ──────────────────────────────────────────────────────"
  echo -e "  Coverage: ${BOLD}${covered}/${total}${NC} categories passing"

  if [[ $covered -eq $total ]]; then
    echo -e "  ${GREEN}✓ All OWASP API Security Top 10 categories passing!${NC}"
  else
    local failing=$((total - covered))
    echo -e "  ${YELLOW}⚠ ${failing} category/categories need attention${NC}"
  fi
  echo ""
}
