#!/usr/bin/env bash
# EnvGuard — Secret Scanning Engine
# Scans files and directories for leaked secrets, credentials, and API keys

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Load patterns
source "$SCRIPT_DIR/patterns.sh"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# ─── Redact sensitive values ──────────────────────────────────────────────
# Show first 4 and last 4 chars, mask the rest

redact_match() {
  local match="$1"
  local len=${#match}

  if [[ $len -le 12 ]]; then
    # Too short to meaningfully redact — show first 4 + stars
    echo "${match:0:4}********"
  else
    local prefix="${match:0:4}"
    local suffix="${match: -4}"
    local mask_len=$((len - 8))
    local mask=""
    for ((i = 0; i < mask_len && i < 20; i++)); do
      mask+="*"
    done
    echo "${prefix}${mask}${suffix}"
  fi
}

# ─── Severity colorization ────────────────────────────────────────────────

severity_color() {
  case "$1" in
    critical) echo -e "${RED}${BOLD}CRITICAL${NC}" ;;
    high)     echo -e "${RED}HIGH${NC}" ;;
    medium)   echo -e "${YELLOW}MEDIUM${NC}" ;;
    low)      echo -e "${BLUE}LOW${NC}" ;;
    *)        echo -e "${DIM}UNKNOWN${NC}" ;;
  esac
}

severity_icon() {
  case "$1" in
    critical) echo -e "${RED}!!${NC}" ;;
    high)     echo -e "${RED}!${NC}" ;;
    medium)   echo -e "${YELLOW}~${NC}" ;;
    low)      echo -e "${BLUE}-${NC}" ;;
    *)        echo "?" ;;
  esac
}

# ─── Load allowlist from config ───────────────────────────────────────────

load_allowlist() {
  local allowlist=()

  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local raw=""
    if command -v python3 &>/dev/null; then
      raw=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    items = cfg.get('skills', {}).get('entries', {}).get('envguard', {}).get('config', {}).get('allowlist', [])
    for item in items:
        print(item)
except: pass
" 2>/dev/null) || true
    elif command -v node &>/dev/null; then
      raw=$(node -e "
try {
  const cfg = require('$OPENCLAW_CONFIG');
  const items = cfg?.skills?.entries?.envguard?.config?.allowlist || [];
  items.forEach(i => console.log(i));
} catch(e) {}
" 2>/dev/null) || true
    elif command -v jq &>/dev/null; then
      raw=$(jq -r '.skills.entries.envguard.config.allowlist[]? // empty' "$OPENCLAW_CONFIG" 2>/dev/null) || true
    fi

    while IFS= read -r line; do
      [[ -n "$line" ]] && allowlist+=("$line")
    done <<< "$raw"
  fi

  printf '%s\n' "${allowlist[@]}" 2>/dev/null || true
}

# ─── Load .envguardignore patterns ────────────────────────────────────────

load_ignore_patterns() {
  local dir="$1"
  local ignore_file="$dir/.envguardignore"
  local patterns=()

  if [[ -f "$ignore_file" ]]; then
    while IFS= read -r line; do
      # Skip comments and empty lines
      [[ -z "$line" || "$line" =~ ^# ]] && continue
      patterns+=("$line")
    done < "$ignore_file"
  fi

  printf '%s\n' "${patterns[@]}" 2>/dev/null || true
}

# ─── Check if file should be ignored ──────────────────────────────────────

should_ignore_file() {
  local filepath="$1"
  local ignore_patterns="$2"

  # Check against default exclude directories
  for exclude_dir in "${ENVGUARD_EXCLUDE_DIRS[@]}"; do
    if [[ "$filepath" == *"/$exclude_dir/"* || "$filepath" == "$exclude_dir/"* ]]; then
      return 0
    fi
  done

  # Check against binary extensions
  local ext="${filepath##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  for bin_ext in "${ENVGUARD_BINARY_EXTENSIONS[@]}"; do
    if [[ "$ext" == "$bin_ext" ]]; then
      return 0
    fi
  done

  # Check against .envguardignore patterns
  if [[ -n "$ignore_patterns" ]]; then
    while IFS= read -r pattern; do
      [[ -z "$pattern" ]] && continue
      # Simple glob matching
      if [[ "$filepath" == $pattern ]]; then
        return 0
      fi
      # Check basename match
      local basename
      basename=$(basename "$filepath")
      if [[ "$basename" == $pattern ]]; then
        return 0
      fi
    done <<< "$ignore_patterns"
  fi

  return 1
}

# ─── Check if match is allowlisted ────────────────────────────────────────

is_allowlisted() {
  local match="$1"
  local allowlist="$2"

  [[ -z "$allowlist" ]] && return 1

  while IFS= read -r pattern; do
    [[ -z "$pattern" ]] && continue
    if [[ "$match" == *"$pattern"* ]]; then
      return 0
    fi
  done <<< "$allowlist"

  return 1
}

# ─── Check if file is binary ──────────────────────────────────────────────

is_binary_file() {
  local filepath="$1"

  # Check extension first (fast path)
  local ext="${filepath##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  for bin_ext in "${ENVGUARD_BINARY_EXTENSIONS[@]}"; do
    if [[ "$ext" == "$bin_ext" ]]; then
      return 0
    fi
  done

  # Check with file command if available
  if command -v file &>/dev/null; then
    local file_type
    file_type=$(file -b --mime-type "$filepath" 2>/dev/null) || return 1
    if [[ "$file_type" != text/* && "$file_type" != application/json && "$file_type" != application/xml && "$file_type" != application/javascript ]]; then
      return 0
    fi
  fi

  return 1
}

# ─── Scan a single file ───────────────────────────────────────────────────
# Returns findings as tab-separated lines:
# filepath \t line_number \t severity \t service \t description \t redacted_match

scan_file() {
  local filepath="$1"
  local allowlist="$2"
  local findings=0
  local is_env_file=false

  # Check if this is actually an .env file (skip .env leak patterns for .env files)
  local basename
  basename=$(basename "$filepath")
  if [[ "$basename" == .env* || "$basename" == *.env || "$basename" == ".env" ]]; then
    is_env_file=true
  fi

  # Read file line by line
  local line_num=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    ((line_num++)) || true

    # Skip empty lines and comment-only lines for performance
    [[ -z "$line" ]] && continue

    # Test each pattern
    for entry in "${ENVGUARD_PATTERNS[@]}"; do
      IFS='|' read -r regex severity service description <<< "$entry"

      # Skip .env patterns for actual .env files
      if [[ "$is_env_file" == "true" && "$service" == "DotEnv" ]]; then
        continue
      fi

      # Match the line against the pattern
      local match=""
      match=$(echo "$line" | grep -oE -- "$regex" 2>/dev/null | head -1) || true

      if [[ -n "$match" ]]; then
        # Check allowlist
        if is_allowlisted "$match" "$allowlist"; then
          continue
        fi

        local redacted
        redacted=$(redact_match "$match")

        # Output finding
        printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
          "$filepath" "$line_num" "$severity" "$service" "$description" "$redacted"

        ((findings++)) || true

        # Only report first match per line to avoid duplicates
        break
      fi
    done
  done < "$filepath"

  return 0
}

# ─── Find all scannable files ─────────────────────────────────────────────

find_scannable_files() {
  local target="$1"
  local ignore_patterns="$2"

  if [[ -f "$target" ]]; then
    # Single file
    if ! is_binary_file "$target"; then
      echo "$target"
    fi
    return
  fi

  # Build find exclude arguments
  local exclude_args=""
  for dir in "${ENVGUARD_EXCLUDE_DIRS[@]}"; do
    exclude_args="$exclude_args -name $dir -prune -o"
  done

  # Find all regular files, excluding directories
  if command -v find &>/dev/null; then
    find "$target" \
      -name ".git" -prune -o \
      -name "node_modules" -prune -o \
      -name "dist" -prune -o \
      -name "build" -prune -o \
      -name "vendor" -prune -o \
      -name "__pycache__" -prune -o \
      -name ".venv" -prune -o \
      -name "venv" -prune -o \
      -name "target" -prune -o \
      -name ".next" -prune -o \
      -name ".nuxt" -prune -o \
      -name "coverage" -prune -o \
      -name ".terraform" -prune -o \
      -type f -print 2>/dev/null | while IFS= read -r file; do
        # Skip binary files and ignored files
        if ! is_binary_file "$file" && ! should_ignore_file "$file" "$ignore_patterns"; then
          echo "$file"
        fi
      done
  fi
}

# ─── Main scan function ──────────────────────────────────────────────────

do_secret_scan() {
  local target="${1:-.}"
  local quiet="${2:-false}"

  # Resolve absolute path
  if [[ ! -e "$target" ]]; then
    echo -e "${RED}[EnvGuard]${NC} Target not found: ${BOLD}$target${NC}" >&2
    return 1
  fi

  # Load configurations
  local allowlist ignore_patterns
  allowlist=$(load_allowlist)

  local scan_root="$target"
  [[ -f "$target" ]] && scan_root=$(dirname "$target")
  ignore_patterns=$(load_ignore_patterns "$scan_root")

  # Collect scannable files
  local files_tmp
  files_tmp=$(mktemp)
  find_scannable_files "$target" "$ignore_patterns" > "$files_tmp"

  local file_count
  file_count=$(wc -l < "$files_tmp" | tr -d ' ')

  if [[ "$file_count" -eq 0 ]]; then
    if [[ "$quiet" != "true" ]]; then
      echo -e "${GREEN}[EnvGuard]${NC} No scannable files found in ${BOLD}$target${NC}"
    fi
    rm -f "$files_tmp"
    return 0
  fi

  if [[ "$quiet" != "true" ]]; then
    echo -e "${BOLD}━━━ EnvGuard Secret Scan ━━━${NC}"
    echo ""
    echo -e "Target:   ${BOLD}$target${NC}"
    echo -e "Files:    ${CYAN}$file_count${NC}"
    echo -e "Patterns: ${CYAN}$(envguard_pattern_count)${NC}"
    echo ""
  fi

  # Scan all files
  local findings_tmp
  findings_tmp=$(mktemp)
  local scanned=0

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    ((scanned++)) || true

    # Progress indicator for large scans
    if [[ "$quiet" != "true" && $((scanned % 50)) -eq 0 ]]; then
      echo -ne "\r${DIM}  Scanning... $scanned / $file_count files${NC}"
    fi

    scan_file "$file" "$allowlist" >> "$findings_tmp" 2>/dev/null || true
  done < "$files_tmp"

  # Clear progress line
  if [[ "$quiet" != "true" && "$scanned" -ge 50 ]]; then
    echo -ne "\r\033[K"
  fi

  # Count findings by severity
  local total=0 critical=0 high=0 medium=0 low=0

  while IFS=$'\t' read -r f_file f_line f_severity f_service f_desc f_redacted; do
    [[ -z "$f_file" ]] && continue
    ((total++)) || true
    case "$f_severity" in
      critical) ((critical++)) || true ;;
      high)     ((high++)) || true ;;
      medium)   ((medium++)) || true ;;
      low)      ((low++)) || true ;;
    esac
  done < "$findings_tmp"

  # Display findings
  if [[ "$total" -gt 0 ]]; then
    if [[ "$quiet" != "true" ]]; then
      echo -e "${RED}${BOLD}Secrets detected!${NC}"
      echo ""

      # Sort by severity: critical first
      local sorted_tmp
      sorted_tmp=$(mktemp)
      {
        grep "^[^\t]*\tcritical\t" "$findings_tmp" 2>/dev/null || true
        grep "^[^\t]*\t[0-9]*\tcritical\t" "$findings_tmp" 2>/dev/null || true
      } > "$sorted_tmp" 2>/dev/null || true

      # Display each finding
      while IFS=$'\t' read -r f_file f_line f_severity f_service f_desc f_redacted; do
        [[ -z "$f_file" ]] && continue
        local icon
        icon=$(severity_icon "$f_severity")
        local sev_display
        sev_display=$(severity_color "$f_severity")

        echo -e "  $icon ${BOLD}$f_file${NC}:${CYAN}$f_line${NC}"
        echo -e "    $sev_display  ${DIM}$f_service${NC} - $f_desc"
        echo -e "    Match: ${DIM}$f_redacted${NC}"
        echo ""
      done < "$findings_tmp"

      rm -f "$sorted_tmp"

      # Summary
      echo -e "${BOLD}━━━ Summary ━━━${NC}"
      echo -e "  Files scanned: ${CYAN}$scanned${NC}"
      echo -e "  Total findings: ${BOLD}$total${NC}"
      [[ "$critical" -gt 0 ]] && echo -e "  ${RED}${BOLD}Critical: $critical${NC}"
      [[ "$high" -gt 0 ]]     && echo -e "  ${RED}High:     $high${NC}"
      [[ "$medium" -gt 0 ]]   && echo -e "  ${YELLOW}Medium:   $medium${NC}"
      [[ "$low" -gt 0 ]]      && echo -e "  ${BLUE}Low:      $low${NC}"
      echo ""

      # Remediation advice
      echo -e "${BOLD}Remediation:${NC}"
      echo -e "  1. Remove secrets from source code"
      echo -e "  2. Rotate any exposed credentials immediately"
      echo -e "  3. Use environment variables or a secret manager"
      echo -e "  4. Add sensitive files to .gitignore"
      echo -e "  5. Add false positives to allowlist: ${CYAN}envguard allowlist add <pattern>${NC}"
    fi
  else
    if [[ "$quiet" != "true" ]]; then
      echo -e "${GREEN}${BOLD}No secrets detected.${NC}"
      echo ""
      echo -e "  Files scanned: ${CYAN}$scanned${NC}"
      echo -e "  Patterns checked: ${CYAN}$(envguard_pattern_count)${NC}"
    fi
  fi

  # Store findings path for report generation
  ENVGUARD_LAST_FINDINGS="$findings_tmp"
  ENVGUARD_LAST_STATS="total=$total critical=$critical high=$high medium=$medium low=$low scanned=$scanned"

  rm -f "$files_tmp"

  # Exit with error if critical or high findings
  if [[ "$critical" -gt 0 || "$high" -gt 0 ]]; then
    return 1
  fi

  return 0
}

# ─── Scan staged changes only (PRO) ──────────────────────────────────────

do_diff_scan() {
  local allowlist
  allowlist=$(load_allowlist)

  echo -e "${BOLD}━━━ EnvGuard Staged Changes Scan ━━━${NC}"
  echo ""

  # Get staged files
  local staged_files
  staged_files=$(git diff --cached --name-only 2>/dev/null) || {
    echo -e "${RED}[EnvGuard]${NC} Not inside a git repository or no staged files."
    return 1
  }

  if [[ -z "$staged_files" ]]; then
    echo -e "${GREEN}[EnvGuard]${NC} No staged files to scan."
    return 0
  fi

  local file_count
  file_count=$(echo "$staged_files" | wc -l | tr -d ' ')
  echo -e "Staged files: ${CYAN}$file_count${NC}"
  echo ""

  # Get diff content with line context
  local findings_tmp
  findings_tmp=$(mktemp)
  local total=0 critical=0 high=0 medium=0 low=0

  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue

    # Skip binary files
    is_binary_file "$file" && continue

    # Get only added lines from diff
    local diff_output
    diff_output=$(git diff --cached -U0 "$file" 2>/dev/null) || continue

    local current_line=0
    while IFS= read -r diff_line; do
      # Track line numbers from @@ headers
      if [[ "$diff_line" =~ ^@@.*\+([0-9]+) ]]; then
        current_line="${BASH_REMATCH[1]}"
        continue
      fi

      # Only scan added lines
      if [[ "$diff_line" =~ ^\+ && ! "$diff_line" =~ ^\+\+\+ ]]; then
        local content="${diff_line:1}"

        for entry in "${ENVGUARD_PATTERNS[@]}"; do
          IFS='|' read -r regex severity service description <<< "$entry"

          local match=""
          match=$(echo "$content" | grep -oE -- "$regex" 2>/dev/null | head -1) || true

          if [[ -n "$match" ]]; then
            if is_allowlisted "$match" "$allowlist"; then
              continue
            fi

            local redacted
            redacted=$(redact_match "$match")

            printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
              "$file" "$current_line" "$severity" "$service" "$description" "$redacted" >> "$findings_tmp"

            ((total++)) || true
            case "$severity" in
              critical) ((critical++)) || true ;;
              high)     ((high++)) || true ;;
              medium)   ((medium++)) || true ;;
              low)      ((low++)) || true ;;
            esac

            break
          fi
        done

        ((current_line++)) || true
      fi
    done <<< "$diff_output"
  done <<< "$staged_files"

  # Display findings
  if [[ "$total" -gt 0 ]]; then
    echo -e "${RED}${BOLD}Secrets detected in staged changes!${NC}"
    echo ""

    while IFS=$'\t' read -r f_file f_line f_severity f_service f_desc f_redacted; do
      [[ -z "$f_file" ]] && continue
      local icon sev_display
      icon=$(severity_icon "$f_severity")
      sev_display=$(severity_color "$f_severity")

      echo -e "  $icon ${BOLD}$f_file${NC}:${CYAN}$f_line${NC}"
      echo -e "    $sev_display  ${DIM}$f_service${NC} - $f_desc"
      echo -e "    Match: ${DIM}$f_redacted${NC}"
      echo ""
    done < "$findings_tmp"

    echo -e "${BOLD}━━━ Summary ━━━${NC}"
    [[ "$critical" -gt 0 ]] && echo -e "  ${RED}${BOLD}Critical: $critical${NC}"
    [[ "$high" -gt 0 ]]     && echo -e "  ${RED}High:     $high${NC}"
    [[ "$medium" -gt 0 ]]   && echo -e "  ${YELLOW}Medium:   $medium${NC}"
    [[ "$low" -gt 0 ]]      && echo -e "  ${BLUE}Low:      $low${NC}"
  else
    echo -e "${GREEN}${BOLD}No secrets detected in staged changes.${NC}"
  fi

  rm -f "$findings_tmp"

  if [[ "$critical" -gt 0 || "$high" -gt 0 ]]; then
    return 1
  fi
  return 0
}

# ─── Git history scan (TEAM) ──────────────────────────────────────────────

do_history_scan() {
  local dir="${1:-.}"
  local allowlist
  allowlist=$(load_allowlist)

  echo -e "${BOLD}━━━ EnvGuard Git History Scan ━━━${NC}"
  echo ""
  echo -e "Target: ${BOLD}$dir${NC}"
  echo -e "${DIM}Scanning all commits for secrets... this may take a while.${NC}"
  echo ""

  local findings_tmp
  findings_tmp=$(mktemp)
  local total=0 critical=0 high=0 medium=0 low=0
  local commits_scanned=0

  # Walk git log
  (cd "$dir" && git log --all --diff-filter=A --diff-filter=M -p --format="%H|%an|%ai" 2>/dev/null) | {
    local current_commit="" current_author="" current_date="" current_file="" current_line=0

    while IFS= read -r line; do
      # Parse commit header
      if [[ "$line" =~ ^[0-9a-f]{40}\| ]]; then
        IFS='|' read -r current_commit current_author current_date <<< "$line"
        ((commits_scanned++)) || true

        # Progress
        if [[ $((commits_scanned % 100)) -eq 0 ]]; then
          echo -ne "\r${DIM}  Scanned $commits_scanned commits...${NC}"
        fi
        continue
      fi

      # Track file
      if [[ "$line" =~ ^diff\ --git\ a/.*\ b/(.*) ]]; then
        current_file="${BASH_REMATCH[1]}"
        current_line=0
        continue
      fi

      # Track line numbers
      if [[ "$line" =~ ^@@.*\+([0-9]+) ]]; then
        current_line="${BASH_REMATCH[1]}"
        continue
      fi

      # Only scan added lines
      if [[ "$line" =~ ^\+ && ! "$line" =~ ^\+\+\+ ]]; then
        local content="${line:1}"
        ((current_line++)) || true

        for entry in "${ENVGUARD_PATTERNS[@]}"; do
          IFS='|' read -r regex severity service description <<< "$entry"

          local match=""
          match=$(echo "$content" | grep -oE -- "$regex" 2>/dev/null | head -1) || true

          if [[ -n "$match" ]]; then
            if is_allowlisted "$match" "$allowlist"; then
              continue
            fi

            local redacted
            redacted=$(redact_match "$match")
            local short_commit="${current_commit:0:8}"

            printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
              "$current_file" "$current_line" "$severity" "$service" "$description" \
              "$redacted" "$short_commit" "$current_author" "$current_date" >> "$findings_tmp"

            ((total++)) || true
            case "$severity" in
              critical) ((critical++)) || true ;;
              high)     ((high++)) || true ;;
              medium)   ((medium++)) || true ;;
              low)      ((low++)) || true ;;
            esac

            break
          fi
        done
      fi
    done

    # Clear progress
    echo -ne "\r\033[K"

    # Display findings
    if [[ "$total" -gt 0 ]]; then
      echo -e "${RED}${BOLD}Secrets found in git history!${NC}"
      echo ""

      while IFS=$'\t' read -r f_file f_line f_severity f_service f_desc f_redacted f_commit f_author f_date; do
        [[ -z "$f_file" ]] && continue
        local icon sev_display
        icon=$(severity_icon "$f_severity")
        sev_display=$(severity_color "$f_severity")

        echo -e "  $icon ${BOLD}$f_file${NC}:${CYAN}$f_line${NC} ${DIM}(commit $f_commit by $f_author)${NC}"
        echo -e "    $sev_display  ${DIM}$f_service${NC} - $f_desc"
        echo -e "    Match: ${DIM}$f_redacted${NC}"
        echo ""
      done < "$findings_tmp"

      echo -e "${BOLD}━━━ History Scan Summary ━━━${NC}"
      echo -e "  Commits scanned: ${CYAN}$commits_scanned${NC}"
      echo -e "  Total findings:  ${BOLD}$total${NC}"
      [[ "$critical" -gt 0 ]] && echo -e "  ${RED}${BOLD}Critical: $critical${NC}"
      [[ "$high" -gt 0 ]]     && echo -e "  ${RED}High:     $high${NC}"
      [[ "$medium" -gt 0 ]]   && echo -e "  ${YELLOW}Medium:   $medium${NC}"
      [[ "$low" -gt 0 ]]      && echo -e "  ${BLUE}Low:      $low${NC}"
      echo ""
      echo -e "${BOLD}Remediation:${NC}"
      echo "  Secrets found in git history require credential rotation."
      echo "  Even deleted secrets remain in git objects."
      echo -e "  Consider: ${CYAN}git filter-branch${NC} or ${CYAN}BFG Repo-Cleaner${NC} to purge history."
    else
      echo -e "${GREEN}${BOLD}No secrets found in git history.${NC}"
      echo -e "  Commits scanned: ${CYAN}$commits_scanned${NC}"
    fi
  }

  rm -f "$findings_tmp"
}

# ─── Report generation (TEAM) ─────────────────────────────────────────────

do_secret_report() {
  local dir="${1:-.}"
  local output="$dir/ENVGUARD-REPORT.md"
  local project_name
  project_name=$(basename "$(cd "$dir" && pwd)")

  echo -e "${BLUE}[EnvGuard]${NC} Generating security report for ${BOLD}$dir${NC}"

  # Run scan quietly to collect findings
  local findings_tmp
  findings_tmp=$(mktemp)
  local total=0 critical=0 high=0 medium=0 low=0 scanned=0
  local allowlist ignore_patterns
  allowlist=$(load_allowlist)
  ignore_patterns=$(load_ignore_patterns "$dir")

  local files_tmp
  files_tmp=$(mktemp)
  find_scannable_files "$dir" "$ignore_patterns" > "$files_tmp"
  scanned=$(wc -l < "$files_tmp" | tr -d ' ')

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    scan_file "$file" "$allowlist" >> "$findings_tmp" 2>/dev/null || true
  done < "$files_tmp"

  while IFS=$'\t' read -r f_file f_line f_severity f_service f_desc f_redacted; do
    [[ -z "$f_file" ]] && continue
    ((total++)) || true
    case "$f_severity" in
      critical) ((critical++)) || true ;;
      high)     ((high++)) || true ;;
      medium)   ((medium++)) || true ;;
      low)      ((low++)) || true ;;
    esac
  done < "$findings_tmp"

  # Generate report from template or inline
  local template="$SKILL_DIR/templates/report.md.tmpl"

  {
    echo "# EnvGuard Security Report: $project_name"
    echo ""
    echo "> Generated by [EnvGuard](https://envguard.pages.dev) on $(date +%Y-%m-%d' '%H:%M:%S)"
    echo ""
    echo "## Scan Summary"
    echo ""
    echo "| Metric | Value |"
    echo "|--------|-------|"
    echo "| Files scanned | $scanned |"
    echo "| Patterns checked | $(envguard_pattern_count) |"
    echo "| Total findings | $total |"
    echo "| Critical | $critical |"
    echo "| High | $high |"
    echo "| Medium | $medium |"
    echo "| Low | $low |"
    echo ""

    if [[ "$total" -gt 0 ]]; then
      echo "## Findings"
      echo ""
      echo "| File | Line | Severity | Service | Description | Match (redacted) |"
      echo "|------|------|----------|---------|-------------|------------------|"

      while IFS=$'\t' read -r f_file f_line f_severity f_service f_desc f_redacted; do
        [[ -z "$f_file" ]] && continue
        echo "| \`$f_file\` | $f_line | **$f_severity** | $f_service | $f_desc | \`$f_redacted\` |"
      done < "$findings_tmp"

      echo ""
      echo "## Severity Breakdown"
      echo ""
      [[ "$critical" -gt 0 ]] && echo "- **CRITICAL ($critical):** Immediate credential exposure. Rotate these credentials NOW."
      [[ "$high" -gt 0 ]]     && echo "- **HIGH ($high):** Likely valid secrets. Remove from source and rotate."
      [[ "$medium" -gt 0 ]]   && echo "- **MEDIUM ($medium):** Possible secrets. Verify and remediate if confirmed."
      [[ "$low" -gt 0 ]]      && echo "- **LOW ($low):** Generic patterns with higher false positive rate. Review manually."
      echo ""
      echo "## Remediation Steps"
      echo ""
      echo "1. **Remove** all secrets from source code immediately"
      echo "2. **Rotate** any exposed credentials (API keys, tokens, passwords)"
      echo "3. **Use** environment variables or a secrets manager (Vault, AWS SSM, etc.)"
      echo "4. **Add** sensitive files to \`.gitignore\`"
      echo "5. **Install** pre-commit hooks: \`envguard hooks install\`"
      echo "6. **Scan** git history: \`envguard history\` (may contain historical secrets)"
      echo "7. **Allowlist** false positives: \`envguard allowlist add <pattern>\`"
    else
      echo "## Result"
      echo ""
      echo "No secrets detected. Your codebase appears clean."
      echo ""
      echo "### Recommendations"
      echo ""
      echo "- Install pre-commit hooks to maintain this status: \`envguard hooks install\`"
      echo "- Periodically scan git history: \`envguard history\`"
      echo "- Add a CI/CD check: \`envguard scan --exit-code\`"
    fi

    echo ""
    echo "---"
    echo ""
    echo "*Report generated by [EnvGuard](https://envguard.pages.dev). Run \`envguard scan\` for interactive results.*"

  } > "$output"

  rm -f "$findings_tmp" "$files_tmp"

  echo -e "${GREEN}[EnvGuard]${NC} Report written to ${BOLD}$output${NC}"
}

# ─── Policy enforcement (TEAM) ────────────────────────────────────────────

do_policy_scan() {
  local dir="${1:-.}"

  echo -e "${BOLD}━━━ EnvGuard Policy Enforcement ━━━${NC}"
  echo ""

  # Load custom patterns from config
  local custom_patterns=()

  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    if command -v python3 &>/dev/null; then
      local raw
      raw=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    patterns = cfg.get('skills', {}).get('entries', {}).get('envguard', {}).get('config', {}).get('customPatterns', [])
    for p in patterns:
        print(p.get('regex', '') + '|' + p.get('severity', 'medium') + '|' + p.get('service', 'Custom') + '|' + p.get('description', 'Custom pattern'))
except: pass
" 2>/dev/null) || true

      while IFS= read -r pattern; do
        [[ -n "$pattern" ]] && custom_patterns+=("$pattern")
      done <<< "$raw"
    fi
  fi

  if [[ ${#custom_patterns[@]} -gt 0 ]]; then
    echo -e "Custom patterns loaded: ${CYAN}${#custom_patterns[@]}${NC}"

    # Add custom patterns to the pattern list temporarily
    for cp in "${custom_patterns[@]}"; do
      ENVGUARD_PATTERNS+=("$cp")
    done
  else
    echo -e "${DIM}No custom patterns configured.${NC}"
    echo -e "Add custom patterns in ${CYAN}~/.openclaw/openclaw.json${NC}:"
    echo -e "  ${DIM}envguard.config.customPatterns: [{ \"regex\": \"...\", \"severity\": \"high\", \"service\": \"MyApp\", \"description\": \"...\" }]${NC}"
    echo ""
  fi

  echo -e "Running scan with ${CYAN}$(envguard_pattern_count)${NC} patterns (built-in + custom)..."
  echo ""

  # Run the full scan
  do_secret_scan "$dir"
}

# ─── Hook entry point — called by lefthook ────────────────────────────────

hook_secret_scan() {
  local staged_files
  staged_files=$(git diff --cached --name-only 2>/dev/null) || return 0

  [[ -z "$staged_files" ]] && return 0

  local allowlist
  allowlist=$(load_allowlist)

  local total=0 critical=0 high=0

  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue
    is_binary_file "$file" && continue

    local findings
    findings=$(scan_file "$file" "$allowlist") || true

    if [[ -n "$findings" ]]; then
      while IFS=$'\t' read -r f_file f_line f_severity f_service f_desc f_redacted; do
        [[ -z "$f_file" ]] && continue
        ((total++)) || true
        case "$f_severity" in
          critical) ((critical++)) || true ;;
          high)     ((high++)) || true ;;
        esac

        local icon sev_display
        icon=$(severity_icon "$f_severity")
        sev_display=$(severity_color "$f_severity")

        echo -e "  $icon ${BOLD}$f_file${NC}:${CYAN}$f_line${NC}"
        echo -e "    $sev_display  $f_desc"
        echo -e "    Match: ${DIM}$f_redacted${NC}"
      done <<< "$findings"
    fi
  done <<< "$staged_files"

  if [[ "$critical" -gt 0 || "$high" -gt 0 ]]; then
    echo ""
    echo -e "${RED}${BOLD}Commit blocked: $total secret(s) detected ($critical critical, $high high)${NC}"
    return 1
  fi

  if [[ "$total" -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}[EnvGuard]${NC} $total potential secret(s) found (low/medium severity). Commit allowed."
  fi

  return 0
}
