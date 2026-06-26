#!/usr/bin/env bash
# ConfigSafe — Core Analysis Engine
# Provides: config type detection, file discovery, pattern scanning, risk scoring,
#           report generation, benchmark checks, policy enforcement, and compliance reports.
#
# This file is sourced by configsafe.sh and by the lefthook pre-commit hook.
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
CONFIGSAFE_VERSION="${VERSION:-1.0.0}"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Global findings array
declare -a FINDINGS=()

# ─── Config Type Detection ──────────────────────────────────────────────────

# Detect the config type for a given file.
# Outputs one of: dockerfile, compose, kubernetes, terraform, cicd, nginx, unknown
detect_config_type() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")
  local basename_lower
  basename_lower=$(echo "$basename_f" | tr '[:upper:]' '[:lower:]')
  local dirpath
  dirpath=$(dirname "$filepath")

  # Dockerfile
  if [[ "$basename_lower" == "dockerfile" || "$basename_lower" == dockerfile.* || "$basename_lower" == *.dockerfile ]]; then
    echo "dockerfile"
    return 0
  fi
  if [[ "$basename_lower" == "containerfile" || "$basename_lower" == containerfile.* ]]; then
    echo "dockerfile"
    return 0
  fi

  # docker-compose
  if [[ "$basename_lower" == "docker-compose.yml" || "$basename_lower" == "docker-compose.yaml" ]]; then
    echo "compose"
    return 0
  fi
  if [[ "$basename_lower" == docker-compose.*.yml || "$basename_lower" == docker-compose.*.yaml ]]; then
    echo "compose"
    return 0
  fi
  if [[ "$basename_lower" == "compose.yml" || "$basename_lower" == "compose.yaml" ]]; then
    echo "compose"
    return 0
  fi

  # Kubernetes YAML — check content for apiVersion/kind
  if [[ "$basename_lower" == *.yml || "$basename_lower" == *.yaml ]]; then
    if grep -qE "^(apiVersion|kind):" "$filepath" 2>/dev/null; then
      # Verify it has Kubernetes-like content
      if grep -qE "kind:[[:space:]]*(Deployment|Pod|Service|StatefulSet|DaemonSet|Job|CronJob|ConfigMap|Secret|Ingress|NetworkPolicy|Namespace|Role|ClusterRole|ServiceAccount|PersistentVolumeClaim)" "$filepath" 2>/dev/null; then
        echo "kubernetes"
        return 0
      fi
    fi
  fi

  # Terraform
  if [[ "$basename_lower" == *.tf || "$basename_lower" == *.tf.json ]]; then
    echo "terraform"
    return 0
  fi

  # CI/CD Pipelines
  # GitHub Actions
  if echo "$filepath" | grep -qE "\.github/workflows/.*\.(yml|yaml)$"; then
    echo "cicd"
    return 0
  fi
  # GitLab CI
  if [[ "$basename_lower" == ".gitlab-ci.yml" || "$basename_lower" == ".gitlab-ci.yaml" ]]; then
    echo "cicd"
    return 0
  fi
  # Jenkinsfile
  if [[ "$basename_lower" == "jenkinsfile" || "$basename_lower" == jenkinsfile.* ]]; then
    echo "cicd"
    return 0
  fi
  # Azure Pipelines
  if [[ "$basename_lower" == "azure-pipelines.yml" || "$basename_lower" == "azure-pipelines.yaml" ]]; then
    echo "cicd"
    return 0
  fi
  # CircleCI
  if echo "$filepath" | grep -qE "\.circleci/config\.(yml|yaml)$"; then
    echo "cicd"
    return 0
  fi

  # Nginx
  if [[ "$basename_lower" == "nginx.conf" || "$basename_lower" == *.nginx || "$basename_lower" == *.nginx.conf ]]; then
    echo "nginx"
    return 0
  fi
  if echo "$dirpath" | grep -qiE "nginx|sites-available|sites-enabled|conf\.d"; then
    if [[ "$basename_lower" == *.conf ]]; then
      echo "nginx"
      return 0
    fi
  fi

  # Apache
  if [[ "$basename_lower" == "httpd.conf" || "$basename_lower" == "apache2.conf" || "$basename_lower" == ".htaccess" ]]; then
    echo "nginx"  # We use the same patterns for both
    return 0
  fi
  if echo "$dirpath" | grep -qiE "apache|httpd"; then
    if [[ "$basename_lower" == *.conf ]]; then
      echo "nginx"
      return 0
    fi
  fi

  echo "unknown"
}

# Detect which config types are present in a directory
detect_config_types() {
  local search_dir="$1"
  local -A found_types=()

  if [[ -f "$search_dir" ]]; then
    local ctype
    ctype=$(detect_config_type "$search_dir")
    if [[ "$ctype" != "unknown" ]]; then
      echo "$ctype"
    fi
    return 0
  fi

  # Quick check for common files
  # Dockerfiles
  if find "$search_dir" -maxdepth 3 \( -name "Dockerfile" -o -name "Dockerfile.*" -o -name "*.dockerfile" -o -name "Containerfile" \) -print -quit 2>/dev/null | grep -q .; then
    found_types[dockerfile]=1
  fi

  # docker-compose
  if find "$search_dir" -maxdepth 3 \( -name "docker-compose*.yml" -o -name "docker-compose*.yaml" -o -name "compose.yml" -o -name "compose.yaml" \) -print -quit 2>/dev/null | grep -q .; then
    found_types[compose]=1
  fi

  # Kubernetes
  if find "$search_dir" -maxdepth 5 -name "*.yml" -o -name "*.yaml" 2>/dev/null | head -20 | xargs grep -lE "^kind:[[:space:]]*(Deployment|Pod|Service|StatefulSet)" 2>/dev/null | head -1 | grep -q .; then
    found_types[kubernetes]=1
  fi

  # Terraform
  if find "$search_dir" -maxdepth 5 -name "*.tf" -print -quit 2>/dev/null | grep -q .; then
    found_types[terraform]=1
  fi

  # CI/CD
  if [[ -d "$search_dir/.github/workflows" ]] || find "$search_dir" -maxdepth 2 \( -name ".gitlab-ci.yml" -o -name "Jenkinsfile" -o -name "azure-pipelines.yml" \) -print -quit 2>/dev/null | grep -q .; then
    found_types[cicd]=1
  fi

  # Nginx/Apache
  if find "$search_dir" -maxdepth 3 \( -name "nginx.conf" -o -name "httpd.conf" -o -name "apache2.conf" -o -name ".htaccess" \) -print -quit 2>/dev/null | grep -q .; then
    found_types[nginx]=1
  fi

  for key in "${!found_types[@]}"; do
    echo "$key"
  done
}

# ─── Find Config Files ─────────────────────────────────────────────────────

# Find all configuration files in a directory tree
find_config_files() {
  local search_dir="$1"
  local -n _result_files="$2"
  _result_files=()

  if [[ -f "$search_dir" ]]; then
    local ctype
    ctype=$(detect_config_type "$search_dir")
    if [[ "$ctype" != "unknown" ]]; then
      _result_files+=("$search_dir")
    fi
    return 0
  fi

  # Dockerfiles
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".terraform" \) -prune -o \
    \( -name "Dockerfile" -o -name "Dockerfile.*" -o -name "*.dockerfile" -o -name "Containerfile" -o -name "Containerfile.*" \) \
    -type f -print0 2>/dev/null)

  # docker-compose files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".terraform" \) -prune -o \
    \( -name "docker-compose*.yml" -o -name "docker-compose*.yaml" -o -name "compose.yml" -o -name "compose.yaml" \) \
    -type f -print0 2>/dev/null)

  # Terraform files
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".terraform" \) -prune -o \
    -name "*.tf" -type f -print0 2>/dev/null)

  # YAML files (Kubernetes + CI/CD)
  while IFS= read -r -d '' file; do
    local ctype
    ctype=$(detect_config_type "$file")
    if [[ "$ctype" == "kubernetes" || "$ctype" == "cicd" ]]; then
      _result_files+=("$file")
    fi
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" -o -name ".terraform" \) -prune -o \
    \( -name "*.yml" -o -name "*.yaml" \) -type f -print0 2>/dev/null)

  # CI/CD specific files
  while IFS= read -r -d '' file; do
    # Avoid duplicates
    local already=false
    for existing in "${_result_files[@]:-}"; do
      if [[ "$existing" == "$file" ]]; then
        already=true
        break
      fi
    done
    [[ "$already" == true ]] && continue
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" \) -prune -o \
    \( -name "Jenkinsfile" -o -name "Jenkinsfile.*" \) -type f -print0 2>/dev/null)

  # Nginx/Apache configs
  while IFS= read -r -d '' file; do
    _result_files+=("$file")
  done < <(find "$search_dir" -maxdepth 5 \
    \( -name ".git" -o -name "node_modules" -o -name "vendor" \) -prune -o \
    \( -name "nginx.conf" -o -name "httpd.conf" -o -name "apache2.conf" -o -name ".htaccess" \) \
    -type f -print0 2>/dev/null)

  # Also check conf.d / sites-available / sites-enabled dirs
  for conf_dir in "conf.d" "sites-available" "sites-enabled"; do
    if [[ -d "$search_dir/$conf_dir" ]]; then
      while IFS= read -r -d '' file; do
        _result_files+=("$file")
      done < <(find "$search_dir/$conf_dir" -name "*.conf" -type f -print0 2>/dev/null)
    fi
  done
}

# ─── Scan File With Patterns ───────────────────────────────────────────────

# Scan a single file against its config type's patterns.
# Appends findings to global FINDINGS array.
# Each finding: FILE|LINE|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION|MATCHED_TEXT
scan_file_with_patterns() {
  local filepath="$1"
  local config_type="$2"

  local patterns_name
  patterns_name=$(get_patterns_for_type "$config_type")

  if [[ -z "$patterns_name" ]]; then
    return 0
  fi

  local -n _patterns_ref="$patterns_name"

  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"

    # Skip placeholder patterns (handled by file-level checks)
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

  # Run file-level checks based on config type
  run_file_level_checks "$filepath" "$config_type"
}

# ─── File-Level Checks ─────────────────────────────────────────────────────

# These checks look at the file as a whole (absence of directives, etc.)
run_file_level_checks() {
  local filepath="$1"
  local config_type="$2"

  case "$config_type" in
    dockerfile)
      check_dockerfile_file_level "$filepath"
      ;;
    compose)
      check_compose_file_level "$filepath"
      ;;
    kubernetes)
      check_kubernetes_file_level "$filepath"
      ;;
    terraform)
      check_terraform_file_level "$filepath"
      ;;
    cicd)
      check_cicd_file_level "$filepath"
      ;;
    nginx)
      check_nginx_file_level "$filepath"
      ;;
  esac
}

# Dockerfile file-level checks
check_dockerfile_file_level() {
  local filepath="$1"

  # Check: no USER directive (DF-001)
  if ! grep -qE "^USER[[:space:]]+" "$filepath" 2>/dev/null; then
    # Exclude scratch and multi-stage intermediate images
    if grep -qE "^FROM" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|critical|DF-001|No USER directive — container runs as root|Add a USER directive to run as a non-root user: USER appuser|Missing USER directive")
    fi
  fi

  # Check: no HEALTHCHECK (DF-010)
  if ! grep -qE "^HEALTHCHECK" "$filepath" 2>/dev/null; then
    if grep -qE "^FROM" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|DF-010|No HEALTHCHECK directive — orchestrator cannot detect unhealthy containers|Add HEALTHCHECK --interval=30s CMD curl -f http://localhost/ || exit 1|Missing HEALTHCHECK directive")
    fi
  fi

  # Check: single-stage build (DF-016)
  local from_count
  from_count=$(grep -cE "^FROM[[:space:]]" "$filepath" 2>/dev/null || echo "0")
  if [[ "$from_count" -eq 1 ]]; then
    # Check if it has build tools that suggest a multi-stage would help
    if grep -qE "(gcc|g\+\+|make|npm[[:space:]]+run[[:space:]]+build|go[[:space:]]+build|cargo[[:space:]]+build|mvn|gradle)" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|DF-016|Single-stage build with build tools — build dependencies included in final image|Use multi-stage builds: FROM builder AS build ... FROM runtime|Single FROM with build tools")
    fi
  fi
}

# docker-compose file-level checks
check_compose_file_level() {
  local filepath="$1"

  # Check for services without resource limits (DC-005)
  # Simple heuristic: if file has services but no deploy/limits or mem_limit
  if grep -qE "^[[:space:]]+[a-z].*:$" "$filepath" 2>/dev/null; then
    if ! grep -qE "(mem_limit|memory|deploy:|resources:|cpus:)" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|DC-005|No resource limits defined — containers can consume all host resources|Add mem_limit, cpus, or deploy.resources.limits to each service|Missing resource limits")
    fi
  fi

  # Check for services without restart policy (DC-013)
  if grep -qE "^[[:space:]]+[a-z].*:$" "$filepath" 2>/dev/null; then
    if ! grep -qE "restart:" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|low|DC-013|No restart policy defined for services|Add restart: unless-stopped or restart: on-failure|Missing restart policy")
    fi
  fi

  # Check for services without healthcheck (DC-014)
  if grep -qE "^[[:space:]]+[a-z].*:$" "$filepath" 2>/dev/null; then
    if ! grep -qE "healthcheck:" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|DC-014|No healthcheck defined for services|Add healthcheck with test, interval, timeout, and retries|Missing healthcheck")
    fi
  fi
}

# Kubernetes file-level checks
check_kubernetes_file_level() {
  local filepath="$1"

  # Check for missing securityContext (K8-004)
  if grep -qE "kind:[[:space:]]*(Deployment|Pod|StatefulSet|DaemonSet|Job|CronJob)" "$filepath" 2>/dev/null; then
    if ! grep -qE "securityContext:" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|high|K8-004|No securityContext defined|Add securityContext with runAsNonRoot, readOnlyRootFilesystem, capabilities|Missing securityContext")
    fi
  fi

  # Check for missing resource limits (K8-005)
  if grep -qE "containers:" "$filepath" 2>/dev/null; then
    if ! grep -qE "resources:" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|high|K8-005|No resource requests/limits defined|Add resources.requests and resources.limits for CPU and memory|Missing resource definitions")
    fi
  fi

  # Check for missing probes (K8-009)
  if grep -qE "containers:" "$filepath" 2>/dev/null; then
    if ! grep -qE "(readinessProbe|livenessProbe):" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|K8-009|No readiness/liveness probes defined|Add readinessProbe and livenessProbe for health monitoring|Missing probes")
    fi
  fi

  # Check for default namespace (K8-008)
  if grep -qE "kind:[[:space:]]*(Deployment|Pod|Service|StatefulSet|DaemonSet)" "$filepath" 2>/dev/null; then
    if ! grep -qE "namespace:" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|K8-008|No namespace specified — defaults to 'default' namespace|Use dedicated namespaces for workload isolation|Missing namespace declaration")
    fi
  fi
}

# Terraform file-level checks
check_terraform_file_level() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")

  # Check for missing state encryption in backend config (TF-019)
  if [[ "$basename_f" == "backend.tf" || "$basename_f" == "main.tf" ]]; then
    if grep -qE "backend[[:space:]]+\"s3\"" "$filepath" 2>/dev/null; then
      if ! grep -qE "encrypt[[:space:]]*=[[:space:]]*true" "$filepath" 2>/dev/null; then
        FINDINGS+=("${filepath}|1|high|TF-019|Terraform S3 state backend without encryption|Add encrypt = true to the backend configuration|Missing state encryption")
      fi
    fi
  fi

  # Check for missing logging (TF-018) — simplified heuristic
  if grep -qE "resource[[:space:]]+\"aws_s3_bucket\"" "$filepath" 2>/dev/null; then
    if ! grep -qE "(aws_s3_bucket_logging|logging)" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|TF-018|S3 bucket without access logging configured|Enable access logging with aws_s3_bucket_logging resource|Missing S3 access logging")
    fi
  fi
}

# CI/CD file-level checks
check_cicd_file_level() {
  local filepath="$1"

  # Check for missing timeout-minutes in GitHub Actions (CI-012)
  if echo "$filepath" | grep -qE "\.github/workflows/"; then
    if grep -qE "jobs:" "$filepath" 2>/dev/null; then
      if ! grep -qE "timeout-minutes:" "$filepath" 2>/dev/null; then
        FINDINGS+=("${filepath}|1|low|CI-012|No timeout-minutes defined for jobs|Add timeout-minutes to prevent runaway builds|Missing timeout-minutes")
      fi
    fi
  fi
}

# Nginx/Apache file-level checks
check_nginx_file_level() {
  local filepath="$1"
  local basename_f
  basename_f=$(basename "$filepath")

  # Check for missing security headers (WS-001)
  if [[ "$basename_f" == *.conf || "$basename_f" == "nginx.conf" ]]; then
    local missing_headers=0
    if ! grep -qE "X-Frame-Options|x-frame-options" "$filepath" 2>/dev/null; then
      ((missing_headers++)) || true
    fi
    if ! grep -qE "X-Content-Type-Options|x-content-type-options" "$filepath" 2>/dev/null; then
      ((missing_headers++)) || true
    fi
    if ! grep -qE "Strict-Transport-Security|strict-transport-security" "$filepath" 2>/dev/null; then
      ((missing_headers++)) || true
    fi
    if [[ "$missing_headers" -gt 0 ]]; then
      FINDINGS+=("${filepath}|1|high|WS-001|Missing $missing_headers security header(s) (X-Frame-Options, X-Content-Type-Options, HSTS)|Add add_header directives for security headers|Missing security headers")
    fi
  fi

  # Check for missing rate limiting (WS-017)
  if [[ "$basename_f" == "nginx.conf" ]]; then
    if ! grep -qE "limit_req" "$filepath" 2>/dev/null; then
      FINDINGS+=("${filepath}|1|medium|WS-017|No rate limiting configuration|Add limit_req_zone and limit_req for rate limiting|Missing rate limiting")
    fi
  fi
}

# ─── Calculate Security Score ──────────────────────────────────────────────

# Calculate a security score (0-100, higher is better) from findings.
# Score starts at 100 and points are deducted per finding.
calculate_security_score() {
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
score_grade() {
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

# Config type display label
config_type_label() {
  local ctype="$1"
  case "$ctype" in
    dockerfile)  echo "Dockerfile" ;;
    compose)     echo "docker-compose" ;;
    kubernetes)  echo "Kubernetes" ;;
    terraform)   echo "Terraform" ;;
    cicd)        echo "CI/CD Pipeline" ;;
    nginx)       echo "Web Server" ;;
    *)           echo "Unknown" ;;
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
  if [[ -n "${f_text:-}" && "$f_text" != "Missing"* ]]; then
    echo -e "           ${DIM}> ${f_text}${NC}"
  fi
  echo -e "           ${DIM}Fix: ${f_rec}${NC}"

  # Show CIS reference if available
  local cis_ref
  cis_ref=$(get_cis_reference "$f_check")
  if [[ -n "$cis_ref" ]]; then
    echo -e "           ${DIM}Ref: ${cis_ref}${NC}"
  fi

  echo ""
}

# ─── Print Summary ─────────────────────────────────────────────────────────

print_scan_summary() {
  local files_scanned="$1"
  local security_score="$2"

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
  grade=$(score_grade "$security_score")
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
  echo -e "  Security Score:    ${gcolor}${BOLD}$security_score/100${NC} (Grade: ${gcolor}${BOLD}$grade${NC})"
  echo ""

  if [[ $security_score -lt 70 ]]; then
    echo -e "  ${RED}${BOLD}FAIL${NC} — Security score below 70. Review findings above."
  elif [[ $total -gt 0 ]]; then
    echo -e "  ${YELLOW}${BOLD}WARN${NC} — Issues found, but score is acceptable. Review recommended."
  else
    echo -e "  ${GREEN}${BOLD}PASS${NC} — No misconfigurations detected."
  fi
}

# ─── Main Scan Orchestrator ────────────────────────────────────────────────

# Main scan entry point. Finds config files, analyzes each, aggregates results.
# Usage: do_config_scan <target> <max_files>
# max_files=0 means unlimited (Pro/Team), 5 for free tier
do_config_scan() {
  local target="$1"
  local max_files="${2:-0}"

  if [[ ! -e "$target" ]]; then
    echo -e "${RED}[ConfigSafe]${NC} Target not found: ${BOLD}$target${NC}" >&2
    return 1
  fi

  # Find config files
  local -a config_files=()
  find_config_files "$target" config_files

  if [[ ${#config_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[ConfigSafe]${NC} No configuration files found in ${BOLD}$target${NC}"
    echo -e "${DIM}  Searched for: Dockerfile, docker-compose.yml, *.yaml (K8s), *.tf, GitHub Actions, nginx.conf${NC}"
    return 0
  fi

  # Apply file limit for free tier
  local files_to_scan=("${config_files[@]}")
  local was_limited=false
  if [[ $max_files -gt 0 && ${#config_files[@]} -gt $max_files ]]; then
    files_to_scan=("${config_files[@]:0:$max_files}")
    was_limited=true
  fi

  echo -e "${BOLD}━━━ ConfigSafe Security Scan ━━━${NC}"
  echo ""
  echo -e "Target:   ${BOLD}$target${NC}"
  echo -e "Files:    ${CYAN}${#config_files[@]}${NC} config file(s) found"

  if [[ "$was_limited" == true ]]; then
    echo -e "${YELLOW}  Free tier: scanning $max_files of ${#config_files[@]} files.${NC}"
    echo -e "${YELLOW}  Upgrade to Pro for unlimited scanning: ${CYAN}https://configsafe.pages.dev${NC}"
  fi

  # Show detected config types
  local -A type_counts=()
  for file in "${files_to_scan[@]}"; do
    local ctype
    ctype=$(detect_config_type "$file")
    type_counts[$ctype]=$(( ${type_counts[$ctype]:-0} + 1 ))
  done

  echo -e "Types:    ${DIM}$(for t in "${!type_counts[@]}"; do echo -n "$(config_type_label "$t") (${type_counts[$t]}) "; done)${NC}"
  echo ""

  # Scan each file
  FINDINGS=()
  local files_scanned=0

  for file in "${files_to_scan[@]}"; do
    files_scanned=$((files_scanned + 1))
    local ctype
    ctype=$(detect_config_type "$file")
    local clabel
    clabel=$(config_type_label "$ctype")

    echo -e "  ${DIM}[$files_scanned/${#files_to_scan[@]}]${NC} $(basename "$file") ${DIM}($clabel)${NC}"

    if [[ "$ctype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ctype"
    fi
  done

  echo ""

  # Print findings
  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}No misconfigurations detected.${NC}"
    echo ""
    print_scan_summary "$files_scanned" 100
    return 0
  fi

  echo -e "${BOLD}━━━ Findings ━━━${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
  done

  local security_score
  security_score=$(calculate_security_score)

  print_scan_summary "$files_scanned" "$security_score"

  # Exit code: 0 if score >= 70, 1 otherwise
  if [[ $security_score -lt 70 ]]; then
    return 1
  fi

  return 0
}

# ─── Hook Entry Point ─────────────────────────────────────────────────────

# Pre-commit hook entry point. Scans staged config files.
# Returns exit code 1 if critical or high severity findings.
hook_config_scan() {
  local staged_files
  staged_files=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || echo "")

  if [[ -z "$staged_files" ]]; then
    return 0
  fi

  # Filter for config files only
  local -a staged_configs=()
  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue
    local ctype
    ctype=$(detect_config_type "$file")
    if [[ "$ctype" != "unknown" ]]; then
      staged_configs+=("$file")
    fi
  done <<< "$staged_files"

  if [[ ${#staged_configs[@]} -eq 0 ]]; then
    return 0
  fi

  echo -e "${BLUE}[ConfigSafe]${NC} Scanning ${#staged_configs[@]} staged config file(s)..."

  FINDINGS=()
  local has_critical_or_high=false

  for file in "${staged_configs[@]}"; do
    local ctype
    ctype=$(detect_config_type "$file")
    scan_file_with_patterns "$file" "$ctype"
  done

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}[ConfigSafe]${NC} All staged config files look secure."
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

  local security_score
  security_score=$(calculate_security_score)

  print_scan_summary "${#staged_configs[@]}" "$security_score"

  if [[ "$has_critical_or_high" == true ]]; then
    echo ""
    echo -e "${RED}${BOLD}Commit blocked: Critical/high security issues in config files.${NC}"
    echo -e "${DIM}Run 'configsafe scan' for details. Use 'git commit --no-verify' to skip (NOT recommended).${NC}"
    return 1
  fi

  return 0
}

# ─── Generate Security Report ─────────────────────────────────────────────

generate_report() {
  local target="$1"

  # Find and scan all config files (unlimited)
  local -a config_files=()
  find_config_files "$target" config_files

  if [[ ${#config_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[ConfigSafe]${NC} No config files found. Nothing to report."
    return 0
  fi

  FINDINGS=()
  local files_scanned=0

  for file in "${config_files[@]}"; do
    files_scanned=$((files_scanned + 1))
    local ctype
    ctype=$(detect_config_type "$file")
    if [[ "$ctype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ctype"
    fi
  done

  local security_score
  security_score=$(calculate_security_score)
  local grade
  grade=$(score_grade "$security_score")

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
    echo -e "${RED}[ConfigSafe]${NC} Report template not found at $template_path"
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
    recommendations_md+="- **URGENT:** $critical critical misconfiguration(s). These are directly exploitable security issues. Fix immediately."$'\n'
  fi
  if [[ $high -gt 0 ]]; then
    recommendations_md+="- **HIGH PRIORITY:** $high high severity issue(s). These significantly weaken your security posture."$'\n'
  fi
  if [[ $medium -gt 0 ]]; then
    recommendations_md+="- **REVIEW:** $medium medium severity issue(s). Best practice violations that should be addressed."$'\n'
  fi
  if [[ $total -eq 0 ]]; then
    recommendations_md="No action items. All configurations pass security checks."
  fi

  # Perform substitutions
  report="${report//\{\{DATE\}\}/$report_date}"
  report="${report//\{\{PROJECT\}\}/$project_name}"
  report="${report//\{\{SECURITY_SCORE\}\}/$security_score}"
  report="${report//\{\{GRADE\}\}/$grade}"
  report="${report//\{\{FILES_SCANNED\}\}/$files_scanned}"
  report="${report//\{\{TOTAL_ISSUES\}\}/$total}"
  report="${report//\{\{CRITICAL_COUNT\}\}/$critical}"
  report="${report//\{\{HIGH_COUNT\}\}/$high}"
  report="${report//\{\{MEDIUM_COUNT\}\}/$medium}"
  report="${report//\{\{LOW_COUNT\}\}/$low}"
  report="${report//\{\{VERSION\}\}/$CONFIGSAFE_VERSION}"

  # Multi-line substitutions
  report=$(echo "$report" | awk -v findings="$findings_table" '{gsub(/\{\{FINDINGS_TABLE\}\}/, findings); print}')
  report=$(echo "$report" | awk -v recs="$recommendations_md" '{gsub(/\{\{RECOMMENDATIONS\}\}/, recs); print}')

  # Output report
  local output_file="configsafe-report-$(date +%Y%m%d-%H%M%S).md"
  echo "$report" > "$output_file"

  echo -e "${GREEN}[ConfigSafe]${NC} Report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:     $files_scanned"
  echo -e "  Total issues:      $total"
  echo -e "  Security score:    $security_score/100 (Grade: $grade)"
}

# ─── CIS Benchmark Checks ────────────────────────────────────────────────

run_benchmark() {
  local target="$1"

  echo -e "${BOLD}━━━ ConfigSafe CIS Benchmark ━━━${NC}"
  echo ""

  # Run a full scan first
  local -a config_files=()
  find_config_files "$target" config_files

  if [[ ${#config_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[ConfigSafe]${NC} No config files found for benchmarking."
    return 0
  fi

  FINDINGS=()
  for file in "${config_files[@]}"; do
    local ctype
    ctype=$(detect_config_type "$file")
    if [[ "$ctype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ctype"
    fi
  done

  # Map findings to CIS benchmarks
  local -A benchmark_results=()
  local total_checks=0
  local passed_checks=0

  # Define CIS checks
  local -a cis_checks=(
    "DF-001|CIS Docker 4.1|Ensure a user for the container has been created"
    "DF-010|CIS Docker 4.6|Ensure HEALTHCHECK instructions have been added"
    "DF-012|CIS Docker 4.10|Ensure secrets are not stored in Dockerfiles"
    "DC-001|CIS Docker 5.4|Ensure privileged containers are not used"
    "DC-004|CIS Docker 5.31|Ensure Docker socket is not mounted"
    "K8-001|CIS K8s 5.2.6|Minimize the admission of root containers"
    "K8-003|CIS K8s 5.2.1|Minimize the admission of privileged containers"
    "K8-005|CIS K8s 5.4.1|Resource requests and limits are set"
    "K8-006|CIS K8s 1.1.9|Ensure hostPath volumes are not used"
    "K8-012|CIS K8s 5.2.5|Minimize allowPrivilegeEscalation"
    "TF-009|CIS AWS 2.1.1|Ensure S3 Bucket is not publicly accessible"
    "TF-014|CIS AWS 5.2|Ensure no security groups allow ingress from 0.0.0.0/0"
    "TF-023|CIS AWS 1.16|Ensure IAM policies follow least privilege"
  )

  for check in "${cis_checks[@]}"; do
    IFS='|' read -r check_id benchmark desc <<< "$check"
    total_checks=$((total_checks + 1))

    local failed=false
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
      if [[ "$f_check" == "$check_id" ]]; then
        failed=true
        break
      fi
    done

    if [[ "$failed" == true ]]; then
      echo -e "  ${RED}FAIL${NC}  ${BOLD}$benchmark${NC} — $desc"
    else
      echo -e "  ${GREEN}PASS${NC}  ${BOLD}$benchmark${NC} — $desc"
      passed_checks=$((passed_checks + 1))
    fi
  done

  echo ""

  local compliance_pct=0
  if [[ $total_checks -gt 0 ]]; then
    compliance_pct=$(( (passed_checks * 100) / total_checks ))
  fi

  echo -e "${BOLD}━━━ Benchmark Summary ━━━${NC}"
  echo ""
  echo -e "  Checks run:        ${BOLD}$total_checks${NC}"
  echo -e "  Passed:            ${GREEN}${BOLD}$passed_checks${NC}"
  echo -e "  Failed:            ${RED}${BOLD}$((total_checks - passed_checks))${NC}"
  echo -e "  Compliance:        ${BOLD}${compliance_pct}%${NC}"
}

# ─── Policy Enforcement ──────────────────────────────────────────────────

enforce_policy() {
  local target="$1"

  echo -e "${BOLD}━━━ ConfigSafe Policy Enforcement ━━━${NC}"
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
    policies = cfg.get('skills', {}).get('entries', {}).get('configsafe', {}).get('config', {}).get('customPolicies', [])
    for p in policies:
        print(p.get('regex', '') + '|' + p.get('severity', 'medium') + '|CUSTOM|' + p.get('description', 'Custom policy') + '|Fix according to organization policy')
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
    echo -e "  ${DIM}configsafe.config.customPolicies: [{ \"regex\": \"...\", \"severity\": \"high\", \"description\": \"...\" }]${NC}"
    echo ""
  fi

  # Run scan with built-in + custom patterns
  local -a config_files=()
  find_config_files "$target" config_files

  if [[ ${#config_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[ConfigSafe]${NC} No config files found."
    return 0
  fi

  FINDINGS=()
  for file in "${config_files[@]}"; do
    local ctype
    ctype=$(detect_config_type "$file")
    if [[ "$ctype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ctype"
    fi

    # Also check custom policies
    for policy in "${custom_policies[@]:-}"; do
      [[ -z "$policy" ]] && continue
      IFS='|' read -r regex severity check_id description recommendation <<< "$policy"

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
          FINDINGS+=("${file}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${matched_text}")
        done <<< "$matches"
      fi
    done
  done

  echo -e "Scanned ${BOLD}${#config_files[@]}${NC} config file(s) with ${CYAN}$(configsafe_pattern_count)${NC} built-in + ${CYAN}${#custom_policies[@]}${NC} custom patterns"
  echo ""

  if [[ ${#FINDINGS[@]} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}All policies pass.${NC}"
    return 0
  fi

  echo -e "${BOLD}━━━ Policy Violations ━━━${NC}"
  echo ""

  for finding in "${FINDINGS[@]}"; do
    format_finding "$finding"
  done

  local security_score
  security_score=$(calculate_security_score)
  print_scan_summary "${#config_files[@]}" "$security_score"

  if [[ $security_score -lt 70 ]]; then
    return 1
  fi
  return 0
}

# ─── Compliance Report ────────────────────────────────────────────────────

generate_compliance() {
  local target="$1"

  echo -e "${BOLD}━━━ ConfigSafe Compliance Report ━━━${NC}"
  echo ""

  # Run full scan
  local -a config_files=()
  find_config_files "$target" config_files

  if [[ ${#config_files[@]} -eq 0 ]]; then
    echo -e "${GREEN}[ConfigSafe]${NC} No config files found."
    return 0
  fi

  FINDINGS=()
  for file in "${config_files[@]}"; do
    local ctype
    ctype=$(detect_config_type "$file")
    if [[ "$ctype" != "unknown" ]]; then
      scan_file_with_patterns "$file" "$ctype"
    fi
  done

  local security_score
  security_score=$(calculate_security_score)
  local grade
  grade=$(score_grade "$security_score")

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

  local report_date
  report_date=$(date +"%Y-%m-%d %H:%M:%S")

  # Generate compliance report
  local output_file="configsafe-compliance-$(date +%Y%m%d-%H%M%S).md"

  {
    echo "# ConfigSafe Compliance Report: $project_name"
    echo ""
    echo "> Generated by [ConfigSafe](https://configsafe.pages.dev) v${CONFIGSAFE_VERSION} on $report_date"
    echo ""
    echo "## Executive Summary"
    echo ""
    echo "| Metric | Value |"
    echo "|--------|-------|"
    echo "| Security Score | **$security_score/100** (Grade: **$grade**) |"
    echo "| Files Scanned | $((${#config_files[@]})) |"
    echo "| Total Findings | $total |"
    echo "| Critical | $critical |"
    echo "| High | $high |"
    echo "| Medium | $medium |"
    echo "| Low | $low |"
    echo ""

    # CIS Docker Benchmark
    echo "## CIS Docker Benchmark v1.6"
    echo ""
    echo "| Control | Status | Description |"
    echo "|---------|--------|-------------|"

    local -a docker_checks=(
      "DF-001|4.1|Ensure a user for the container has been created"
      "DF-010|4.6|Ensure HEALTHCHECK instructions have been added"
      "DF-012|4.10|Ensure secrets are not stored in Dockerfiles"
      "DC-001|5.4|Ensure privileged containers are not used"
      "DC-004|5.31|Ensure Docker socket is not mounted"
      "DC-005|5.10|Ensure memory usage for containers is limited"
    )

    for check in "${docker_checks[@]}"; do
      IFS='|' read -r check_id control desc <<< "$check"
      local status="PASS"
      for finding in "${FINDINGS[@]:-}"; do
        [[ -z "$finding" ]] && continue
        IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
        if [[ "$f_check" == "$check_id" ]]; then
          status="FAIL"
          break
        fi
      done
      echo "| $control | **$status** | $desc |"
    done

    echo ""

    # CIS Kubernetes Benchmark
    echo "## CIS Kubernetes Benchmark v1.8"
    echo ""
    echo "| Control | Status | Description |"
    echo "|---------|--------|-------------|"

    local -a k8s_checks=(
      "K8-003|5.2.1|Minimize the admission of privileged containers"
      "K8-012|5.2.5|Minimize allowPrivilegeEscalation"
      "K8-001|5.2.6|Minimize the admission of root containers"
      "K8-005|5.4.1|Resource requests and limits are set"
      "K8-006|1.1.9|Ensure hostPath volumes are not used"
      "K8-004|5.7.3|Apply Security Context to pods and containers"
    )

    for check in "${k8s_checks[@]}"; do
      IFS='|' read -r check_id control desc <<< "$check"
      local status="PASS"
      for finding in "${FINDINGS[@]:-}"; do
        [[ -z "$finding" ]] && continue
        IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
        if [[ "$f_check" == "$check_id" ]]; then
          status="FAIL"
          break
        fi
      done
      echo "| $control | **$status** | $desc |"
    done

    echo ""

    # CIS AWS Foundations
    echo "## CIS AWS Foundations Benchmark v2.0"
    echo ""
    echo "| Control | Status | Description |"
    echo "|---------|--------|-------------|"

    local -a aws_checks=(
      "TF-023|1.16|Ensure IAM policies follow least privilege"
      "TF-009|2.1.1|Ensure S3 Bucket is not publicly accessible"
      "TF-007|2.1.2|Ensure encryption is enabled for S3 buckets"
      "TF-014|5.2|Ensure no security groups allow ingress from 0.0.0.0/0"
      "TF-018|3.1|Ensure logging is enabled"
      "TF-029|2.3.1|Ensure RDS instances are not publicly accessible"
    )

    for check in "${aws_checks[@]}"; do
      IFS='|' read -r check_id control desc <<< "$check"
      local status="PASS"
      for finding in "${FINDINGS[@]:-}"; do
        [[ -z "$finding" ]] && continue
        IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
        if [[ "$f_check" == "$check_id" ]]; then
          status="FAIL"
          break
        fi
      done
      echo "| $control | **$status** | $desc |"
    done

    echo ""

    # NIST 800-190
    echo "## NIST SP 800-190 (Application Container Security)"
    echo ""
    echo "| Section | Status | Description |"
    echo "|---------|--------|-------------|"

    local nist_pass=0
    local nist_total=5

    # 4.1 Image vulnerabilities
    local img_status="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
      if [[ "$f_check" == "DF-002" || "$f_check" == "DF-003" || "$f_check" == "K8-019" || "$f_check" == "K8-020" ]]; then
        img_status="FAIL"
        break
      fi
    done
    [[ "$img_status" == "PASS" ]] && nist_pass=$((nist_pass + 1))
    echo "| 4.1 | **$img_status** | Image provenance and integrity (pinned versions) |"

    # 4.2 Container runtime config
    local rt_status="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
      if [[ "$f_check" == "DF-001" || "$f_check" == "K8-001" || "$f_check" == "K8-003" || "$f_check" == "DC-001" ]]; then
        rt_status="FAIL"
        break
      fi
    done
    [[ "$rt_status" == "PASS" ]] && nist_pass=$((nist_pass + 1))
    echo "| 4.2 | **$rt_status** | Container runtime configuration (non-root, non-privileged) |"

    # 4.3 Network segmentation
    local net_status="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
      if [[ "$f_check" == "DC-002" || "$f_check" == "DC-003" || "$f_check" == "K8-014" || "$f_check" == "TF-014" ]]; then
        net_status="FAIL"
        break
      fi
    done
    [[ "$net_status" == "PASS" ]] && nist_pass=$((nist_pass + 1))
    echo "| 4.3 | **$net_status** | Network segmentation and isolation |"

    # 4.4 Secrets management
    local sec_status="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
      if [[ "$f_check" == "DF-012" || "$f_check" == "K8-010" || "$f_check" == "DC-006" || "$f_check" == "TF-001" ]]; then
        sec_status="FAIL"
        break
      fi
    done
    [[ "$sec_status" == "PASS" ]] && nist_pass=$((nist_pass + 1))
    echo "| 4.4 | **$sec_status** | Secrets management (no plaintext secrets) |"

    # 4.5 Resource limits
    local res_status="PASS"
    for finding in "${FINDINGS[@]:-}"; do
      [[ -z "$finding" ]] && continue
      IFS='|' read -r _f _l _s f_check _d _r _t <<< "$finding"
      if [[ "$f_check" == "K8-005" || "$f_check" == "DC-005" ]]; then
        res_status="FAIL"
        break
      fi
    done
    [[ "$res_status" == "PASS" ]] && nist_pass=$((nist_pass + 1))
    echo "| 4.5 | **$res_status** | Resource limits and quotas |"

    echo ""

    # Detailed findings
    if [[ $total -gt 0 ]]; then
      echo "## Detailed Findings"
      echo ""
      echo "| # | File | Line | Severity | Check | Description |"
      echo "|---|------|------|----------|-------|-------------|"

      local idx=0
      for finding in "${FINDINGS[@]}"; do
        idx=$((idx + 1))
        IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"
        echo "| $idx | \`$(basename "$f_file")\` | $f_line | **$f_severity** | $f_check | $f_desc |"
      done

      echo ""

      echo "## Remediation Roadmap"
      echo ""
      if [[ $critical -gt 0 ]]; then
        echo "### Immediate (Critical)"
        echo ""
        for finding in "${FINDINGS[@]}"; do
          IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"
          if [[ "$f_severity" == "critical" ]]; then
            echo "- **$f_check** (\`$(basename "$f_file")\`): $f_rec"
          fi
        done
        echo ""
      fi
      if [[ $high -gt 0 ]]; then
        echo "### Short-term (High)"
        echo ""
        for finding in "${FINDINGS[@]}"; do
          IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"
          if [[ "$f_severity" == "high" ]]; then
            echo "- **$f_check** (\`$(basename "$f_file")\`): $f_rec"
          fi
        done
        echo ""
      fi
      if [[ $medium -gt 0 || $low -gt 0 ]]; then
        echo "### Medium-term (Medium/Low)"
        echo ""
        for finding in "${FINDINGS[@]}"; do
          IFS='|' read -r f_file f_line f_severity f_check f_desc f_rec f_text <<< "$finding"
          if [[ "$f_severity" == "medium" || "$f_severity" == "low" ]]; then
            echo "- **$f_check** (\`$(basename "$f_file")\`): $f_rec"
          fi
        done
        echo ""
      fi
    else
      echo "## Result"
      echo ""
      echo "All configuration files pass security and compliance checks."
      echo ""
      echo "### Recommendations"
      echo ""
      echo "- Install pre-commit hooks to maintain compliance: \`configsafe hooks install\`"
      echo "- Run periodic audits with: \`configsafe compliance\`"
      echo "- Add CI/CD integration for continuous compliance verification"
    fi

    echo ""
    echo "---"
    echo ""
    echo "*Report generated by [ConfigSafe](https://configsafe.pages.dev) v${CONFIGSAFE_VERSION}. Run \`configsafe scan\` for interactive results.*"

  } > "$output_file"

  echo -e "${GREEN}[ConfigSafe]${NC} Compliance report generated: ${BOLD}$output_file${NC}"
  echo ""
  echo -e "  Files scanned:     ${#config_files[@]}"
  echo -e "  Security score:    $security_score/100 (Grade: $grade)"
  echo -e "  Total findings:    $total"
  echo -e "  NIST 800-190:      $nist_pass/$nist_total sections pass"
}
