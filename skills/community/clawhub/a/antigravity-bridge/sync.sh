#!/usr/bin/env bash
# Antigravity Bridge — sync.sh v2.0.0
# One-way sync: Antigravity/Gemini projects → OpenClaw workspace
# Relies on OpenClaw native embedding (memorySearch.extraPaths) for indexing.
#
# Usage: sync.sh [--config <path>] [--project <name>] [--dry-run] [--verbose] [--help]
#
# Prerequisites: yq (https://github.com/mikefarah/yq), rsync

set -euo pipefail

# ─── Defaults ─────────────────────────────────────────────────────────────────
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
DEFAULT_CONFIG="$WORKSPACE_DIR/antigravity-bridge.yaml"

CONFIG="$DEFAULT_CONFIG"
PROJECT_FILTER=""
DRY_RUN=false
VERBOSE=false

TOTAL_SYNCED=0
TOTAL_SKIPPED=0

# ─── Colors ───────────────────────────────────────────────────────────────────
if [[ -t 1 ]]; then
  RED='\033[0;31m'
  YELLOW='\033[1;33m'
  GREEN='\033[0;32m'
  CYAN='\033[0;36m'
  BOLD='\033[1m'
  RESET='\033[0m'
else
  RED='' YELLOW='' GREEN='' CYAN='' BOLD='' RESET=''
fi

# ─── Help ─────────────────────────────────────────────────────────────────────
usage() {
  cat <<EOF
${BOLD}Antigravity Bridge v2.0.0${RESET}
One-way sync from Google Antigravity IDE projects to OpenClaw workspace.

${BOLD}USAGE${RESET}
  sync.sh [options]

${BOLD}OPTIONS${RESET}
  --config <path>    Config file path
                     (default: ~/.openclaw/workspace/antigravity-bridge.yaml)
  --project <name>   Sync only this project (by name field in config)
  --dry-run          Show what would be synced without making changes
  --verbose          Show rsync output and detailed progress
  --help             Show this help and exit

${BOLD}EXAMPLES${RESET}
  sync.sh
  sync.sh --project acme-platform
  sync.sh --dry-run --verbose
  sync.sh --config ~/my-bridge.yaml --verbose

${BOLD}PREREQUISITES${RESET}
  yq    https://github.com/mikefarah/yq  (brew install yq)
  rsync pre-installed on macOS/Linux     (brew install rsync)

${BOLD}CONFIG FILE${RESET}
  Default: ~/.openclaw/workspace/antigravity-bridge.yaml
  Template: ~/.openclaw/workspace/skills/antigravity-bridge/config-template.yaml

EOF
  exit 0
}

# ─── Argument parsing ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)       usage ;;
    --config)        CONFIG="$2"; shift 2 ;;
    --project)       PROJECT_FILTER="$2"; shift 2 ;;
    --dry-run)       DRY_RUN=true; shift ;;
    --verbose)       VERBOSE=true; shift ;;
    *)
      echo -e "${RED}Unknown option: $1${RESET}" >&2
      echo "Run sync.sh --help for usage." >&2
      exit 1
      ;;
  esac
done

# ─── Dependency checks ────────────────────────────────────────────────────────
check_deps() {
  if ! command -v yq &>/dev/null; then
    echo -e "${RED}Error: yq not found.${RESET}" >&2
    echo "" >&2
    echo "yq is required for YAML config parsing. Install it:" >&2
    echo "  macOS:        brew install yq" >&2
    echo "  Ubuntu/Debian: sudo apt install yq" >&2
    echo "  Ubuntu snap:  snap install yq" >&2
    echo "  Manual:       https://github.com/mikefarah/yq/releases" >&2
    exit 1
  fi

  if ! command -v rsync &>/dev/null; then
    echo -e "${RED}Error: rsync not found.${RESET}" >&2
    echo "Install rsync: brew install rsync (macOS) or sudo apt install rsync" >&2
    exit 1
  fi
}

# ─── Logging helpers ──────────────────────────────────────────────────────────
log_info()    { echo -e "${CYAN}[info]${RESET}  $*"; }
log_ok()      { echo -e "${GREEN}[ok]${RESET}    $*"; }
log_warn()    { echo -e "${YELLOW}[warn]${RESET}  $*"; }
log_error()   { echo -e "${RED}[error]${RESET} $*" >&2; }
log_verbose() { $VERBOSE && echo -e "        $*" || true; }

# ─── Expand ~ in paths ────────────────────────────────────────────────────────
expand_path() {
  local path="$1"
  # Replace leading ~ with $HOME
  echo "${path/#\~/$HOME}"
}

# ─── Rsync a source to a destination ─────────────────────────────────────────
# Returns number of files transferred via exit code (captured by caller)
do_rsync() {
  local src="$1"
  local dst="$2"
  local is_file="${3:-false}"

  local rsync_opts=(-a --out-format="%n")
  $DRY_RUN   && rsync_opts+=(--dry-run)
  $VERBOSE   || rsync_opts+=(--quiet)
  ! $VERBOSE && rsync_opts=(${rsync_opts[@]/--quiet/})

  local transferred=0

  if [[ "$is_file" == "true" ]]; then
    # Single file sync
    local dst_dir
    dst_dir="$(dirname "$dst")"
    $DRY_RUN || mkdir -p "$dst_dir"

    local rsync_out
    rsync_out=$(rsync "${rsync_opts[@]}" "$src" "$dst" 2>&1) || true
    transferred=$(echo "$rsync_out" | grep -c '^[^/]*\.md$' 2>/dev/null) || transferred=0
    $VERBOSE && [[ -n "$rsync_out" ]] && echo "$rsync_out" | sed 's/^/          /' >&2
  else
    # Directory sync — only .md files
    $DRY_RUN || mkdir -p "$dst"

    local rsync_out
    rsync_out=$(rsync "${rsync_opts[@]}" \
      --filter='+ */' \
      --filter='+ *.md' \
      --filter='- *' \
      "$src/" "$dst/" 2>&1) || true
    transferred=$(echo "$rsync_out" | grep -c '\.md$' 2>/dev/null) || transferred=0
    $VERBOSE && [[ -n "$rsync_out" ]] && echo "$rsync_out" | sed 's/^/          /' >&2
  fi

  echo "$transferred"
}

# ─── Sync a single configured project ─────────────────────────────────────────
sync_project() {
  local name="$1"
  local repo="$2"
  local destination="$3"

  local project_synced=0
  local project_skipped=0

  log_info "${BOLD}Project: $name${RESET}"
  log_verbose "Repo: $repo"

  repo="$(expand_path "$repo")"

  if [[ ! -d "$repo" ]]; then
    log_warn "Project repo not found, skipping: $repo"
    TOTAL_SKIPPED=$((TOTAL_SKIPPED + 1))
    return
  fi

  local dest_base="$destination/$name"

  # Sync configured paths
  local path_count
  path_count=$(yq eval ".projects[] | select(.name == \"$name\") | .paths | length" "$CONFIG" 2>/dev/null || echo 0)
  path_count="${path_count:-0}"

  local i=0
  while [[ $i -lt $path_count ]]; do
    local rel_path
    rel_path=$(yq eval ".projects[] | select(.name == \"$name\") | .paths[$i]" "$CONFIG")
    i=$((i + 1))

    local src="$repo/$rel_path"

    if [[ "$rel_path" == *.md ]]; then
      # Single markdown file
      if [[ ! -f "$src" ]]; then
        log_warn "  Path not found, skipping: $rel_path"
        project_skipped=$((project_skipped + 1))
        continue
      fi

      local dst_file="$dest_base/$rel_path"
      log_verbose "  Sync file: $rel_path"
      local n
      n=$(do_rsync "$src" "$dst_file" "true")
      project_synced=$((project_synced + n))
    else
      # Directory
      if [[ ! -d "$src" ]]; then
        log_warn "  Path not found, skipping: $rel_path/"
        project_skipped=$((project_skipped + 1))
        continue
      fi

      local dst_dir="$dest_base/$rel_path"
      log_verbose "  Sync dir:  $rel_path/"
      local n
      n=$(do_rsync "$src" "$dst_dir" "false")
      project_synced=$((project_synced + n))
    fi
  done

  # Sync root *.md if include_root_md: true
  local include_root
  include_root=$(yq eval ".projects[] | select(.name == \"$name\") | .include_root_md // false" "$CONFIG" 2>/dev/null || echo "false")

  if [[ "$include_root" == "true" ]]; then
    log_verbose "  Sync root *.md"
    local root_dst="$dest_base"
    $DRY_RUN || mkdir -p "$root_dst"

    local root_rsync_opts=(-a --out-format="%n" --filter='- */' --filter='+ *.md' --filter='- *')
    $DRY_RUN && root_rsync_opts+=(--dry-run)

    local rsync_out
    rsync_out=$(rsync "${root_rsync_opts[@]}" "$repo/" "$root_dst/" 2>&1) || true
    $VERBOSE && [[ -n "$rsync_out" ]] && echo "$rsync_out" | sed 's/^/          /' >&2
    local n
    n=$(echo "$rsync_out" | grep -c '\.md$' 2>/dev/null) || n=0
    project_synced=$((project_synced + n))
  fi

  TOTAL_SYNCED=$((TOTAL_SYNCED + project_synced))

  if [[ $project_synced -gt 0 ]]; then
    log_ok "  $name — $project_synced file(s) synced"
  else
    log_info "  $name — up to date (0 files changed)"
  fi
}

# ─── Sync a knowledge source ──────────────────────────────────────────────────
sync_knowledge() {
  local name="$1"
  local path="$2"
  local destination="$3"

  log_info "${BOLD}Knowledge: $name${RESET}"

  path="$(expand_path "$path")"

  if [[ ! -d "$path" ]]; then
    log_warn "Knowledge path not found, skipping: $path"
    TOTAL_SKIPPED=$((TOTAL_SKIPPED + 1))
    return
  fi

  local dst="$destination/$name"
  log_verbose "  $path → $dst"

  local n
  n=$(do_rsync "$path" "$dst" "false")
  TOTAL_SYNCED=$((TOTAL_SYNCED + n))

  if [[ $n -gt 0 ]]; then
    log_ok "  $name — $n file(s) synced"
  else
    log_info "  $name — up to date (0 files changed)"
  fi
}

# ─── Main ─────────────────────────────────────────────────────────────────────
main() {
  check_deps

  # Resolve config path
  CONFIG="$(expand_path "$CONFIG")"

  if [[ ! -f "$CONFIG" ]]; then
    log_error "Config file not found: $CONFIG"
    echo "" >&2
    echo "Copy the template to get started:" >&2
    echo "  cp ~/.openclaw/workspace/skills/antigravity-bridge/config-template.yaml \\" >&2
    echo "     ~/.openclaw/workspace/antigravity-bridge.yaml" >&2
    exit 1
  fi

  local ts
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  echo -e "${BOLD}🌉 Antigravity Bridge v2.0.0${RESET} — $ts"
  $DRY_RUN && echo -e "${YELLOW}[DRY RUN — no files will be modified]${RESET}"
  echo ""

  # Resolve destination
  local dest_rel
  dest_rel=$(yq eval '.destination // "antigravity"' "$CONFIG")
  local destination
  destination="$WORKSPACE_DIR/$(expand_path "$dest_rel")"

  log_verbose "Workspace: $WORKSPACE_DIR"
  log_verbose "Config:    $CONFIG"
  log_verbose "Dest:      $destination"
  $VERBOSE && echo ""

  # ── Projects ──────────────────────────────────────────────────────────────
  local project_count
  project_count=$(yq eval '.projects | length' "$CONFIG" 2>/dev/null || echo 0)
  project_count="${project_count:-0}"

  local i=0
  while [[ $i -lt $project_count ]]; do
    local pname
    pname=$(yq eval ".projects[$i].name" "$CONFIG")
    local prepo
    prepo=$(yq eval ".projects[$i].repo" "$CONFIG")
    i=$((i + 1))

    # Filter by --project if specified
    if [[ -n "$PROJECT_FILTER" && "$pname" != "$PROJECT_FILTER" ]]; then
      continue
    fi

    sync_project "$pname" "$prepo" "$destination"
    echo ""
  done

  # If --project was specified but not found, warn
  if [[ -n "$PROJECT_FILTER" && $i -eq 0 ]]; then
    log_warn "No project named '$PROJECT_FILTER' found in config."
  fi

  # ── Knowledge sources ─────────────────────────────────────────────────────
  # Skip knowledge sources if --project filter is active
  if [[ -z "$PROJECT_FILTER" ]]; then
    local knowledge_count
    knowledge_count=$(yq eval '.knowledge | length' "$CONFIG" 2>/dev/null || echo 0)
    knowledge_count="${knowledge_count:-0}"

    local j=0
    while [[ $j -lt $knowledge_count ]]; do
      local kname
      kname=$(yq eval ".knowledge[$j].name" "$CONFIG")
      local kpath
      kpath=$(yq eval ".knowledge[$j].path" "$CONFIG")
      j=$((j + 1))

      sync_knowledge "$kname" "$kpath" "$destination"
      echo ""
    done
  fi

  # ── Summary ───────────────────────────────────────────────────────────────
  echo -e "${BOLD}Summary${RESET}"
  echo "  Files synced: $TOTAL_SYNCED"
  [[ $TOTAL_SKIPPED -gt 0 ]] && echo -e "  ${YELLOW}Paths skipped: $TOTAL_SKIPPED (source not found)${RESET}"
  $DRY_RUN && echo -e "  ${YELLOW}Dry run — no changes were made${RESET}"
  echo ""
  echo -e "${GREEN}Done.${RESET}"
}

main "$@"
