#!/usr/bin/env bash
set -euo pipefail

# scaffold.sh — Agent Orchestration Kit scaffolding
# Creates workspace directories, copies templates, injects orchestration rules

# Cross-platform sed -i (macOS vs GNU/Linux)
if [[ "$(uname)" == "Darwin" ]]; then
  sedi() { sed -i '' "$@"; }
else
  sedi() { sed -i "$@"; }
fi

# Convert a hyphenated slug to Title Case display name
# Usage: slug_to_display_name "senior-developer"  => "Senior Developer"
slug_to_display_name() {
  echo "$1" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2)); print}'
}

# ── Defaults ──────────────────────────────────────────────────────────

BASE_DIR="${HOME}/.openclaw"
TEAM="minimal"
SKILL_DIR=""
INJECT_ONLY_PATH=""
LEADER_WS_NAME="workspace"
QUIET=false
DRY_RUN=false
ADD_AGENTS=()

# ── Usage ─────────────────────────────────────────────────────────────

usage() {
  cat <<'EOF'
Usage: scaffold.sh [OPTIONS]

Options:
  --skill-dir DIR              Path to this skill's directory (required)
  --team NAME                  Team preset to use (default: minimal)
                               Available: minimal, software-dev, content-studio, research-analysis
  --add-agent NAME             Add a specialist agent (repeatable)
                               Example: --add-agent researcher --add-agent senior-developer
  --base-dir DIR               OpenClaw root directory (default: ~/.openclaw)
  --leader-workspace NAME      Leader workspace directory name (default: workspace)
                               Example: --leader-workspace workspace-bae
  --inject-orchestration PATH  Inject orchestration rules into a specific AGENTS.md file and exit
  --quiet                      Suppress progress messages
  --dry-run                    Print what would be created without writing
  -h, --help                   Show this help

Examples:
  scaffold.sh --skill-dir /path/to/agent-orchestration-kit
  scaffold.sh --skill-dir /path/to/agent-orchestration-kit --team software-dev
  scaffold.sh --skill-dir /path/to/agent-orchestration-kit --add-agent researcher
  scaffold.sh --inject-orchestration /path/to/AGENTS.md --skill-dir /path/to/agent-orchestration-kit
EOF
  exit 0
}

# ── Argument Parsing ──────────────────────────────────────────────────

needs_arg() { if [[ $# -lt 2 || "$2" == --* ]]; then echo "[ERROR] $1 requires an argument"; exit 1; fi; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-dir)              needs_arg "$@"; BASE_DIR="$2";           shift 2 ;;
    --skill-dir)             needs_arg "$@"; SKILL_DIR="$2";          shift 2 ;;
    --team)                  needs_arg "$@"; TEAM="$2";               shift 2 ;;
    --add-agent)             needs_arg "$@"; ADD_AGENTS+=("$2");      shift 2 ;;
    --leader-workspace)      needs_arg "$@"; LEADER_WS_NAME="$2";    shift 2 ;;
    --inject-orchestration)  needs_arg "$@"; INJECT_ONLY_PATH="$2";  shift 2 ;;
    --quiet)                 QUIET=true;              shift   ;;
    --dry-run)               DRY_RUN=true;            shift   ;;
    -h|--help)               usage ;;
    *)                       echo "[ERROR] Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$SKILL_DIR" ]]; then
  echo "[ERROR] --skill-dir is required"
  exit 1
fi

if [[ ! -d "$SKILL_DIR/templates" ]]; then
  echo "[ERROR] Skill directory does not contain templates/: $SKILL_DIR"
  exit 1
fi

TEMPLATES="$SKILL_DIR/templates"
REFERENCES="$SKILL_DIR/references"
ASSETS="$SKILL_DIR/assets"

# ── Helpers ───────────────────────────────────────────────────────────

log() {
  if [[ "$QUIET" != true ]]; then
    echo "$1"
  fi
}

ok()   { log "[OK]   $1"; }
skip() { log "[SKIP] $1"; }
info() { log "[INFO] $1"; }
dry()  { log "[DRY]  $1"; }

# Copy a file only if the destination does not exist
# Usage: copy_if_missing <src> <dst> <label>
copy_if_missing() {
  local src="$1" dst="$2" label="$3"
  if [[ ! -f "$src" ]]; then
    return
  fi
  if [[ -f "$dst" ]]; then
    skip "$label (already exists)"
    return
  fi
  if [[ "$DRY_RUN" == true ]]; then
    dry "$label"
    return
  fi
  cp "$src" "$dst"
  ok "$label"
}

# Copy file, overwriting if exists (backup if content differs)
# Usage: copy_with_backup <src> <dst> <label>
copy_with_backup() {
  local src="$1" dst="$2" label="$3"
  if [[ ! -f "$src" ]]; then
    return
  fi
  if [[ "$DRY_RUN" == true ]]; then
    dry "$label"
    return
  fi
  if [[ -f "$dst" ]]; then
    if diff -q "$src" "$dst" > /dev/null 2>&1; then
      skip "$label (already up to date)"
      return
    fi
    cp "$dst" "${dst}.bak"
    log "[BAK]  ${label}.bak"
  fi
  cp "$src" "$dst"
  ok "$label"
}

# Idempotently inject orchestration rules into an AGENTS.md file
# Usage: inject_orchestration <agents_md_path>
ORCHESTRATION_MARKER="<!-- ORCHESTRATION PROTOCOL — AUTO-INJECTED, DO NOT REMOVE -->"
inject_orchestration() {
  local target="$1"
  local injection_src="$TEMPLATES/agents/orchestration-injection.md"

  if [[ ! -f "$injection_src" ]]; then
    log "[WARN] orchestration-injection.md not found, skipping injection"
    return
  fi

  if [[ ! -f "$target" ]]; then
    log "[WARN] Target AGENTS.md not found: $target"
    return
  fi

  # Check if already injected (idempotency)
  if grep -qF "$ORCHESTRATION_MARKER" "$target" 2>/dev/null; then
    skip "orchestration injection in $(basename "$(dirname "$target")")/AGENTS.md (already injected)"
    return
  fi

  if [[ "$DRY_RUN" == true ]]; then
    dry "inject orchestration into $(basename "$(dirname "$target")")/AGENTS.md"
    return
  fi

  # Append marker + content
  printf '\n%s\n\n' "$ORCHESTRATION_MARKER" >> "$target"
  cat "$injection_src" >> "$target"
  ok "inject orchestration into $(basename "$(dirname "$target")")/AGENTS.md"
}

# Specialist capability descriptions for §8 Team Reference
# Uses case statement instead of associative array for bash 3.2 compatibility (macOS)
get_specialist_caps() {
  local id="$1"
  case "$id" in
    senior-developer)    echo "**Senior Developer:** Full-stack implementation, TDD, code quality." ;;
    code-reviewer)       echo "**Code Reviewer:** Code review, security audit, quality assessment." ;;
    researcher)          echo "**Researcher:** Market research, investigation, evidence-based analysis." ;;
    content-creator)     echo "**Content Creator:** Copywriting, visual direction, platform packaging." ;;
    software-architect)  echo "**Software Architect:** System design, ADRs, trade-off analysis." ;;
    *)
      # Fallback: generate from display name
      local display_name
      display_name="$(slug_to_display_name "$id")"
      echo "**${display_name}:** See workspace-${id}/SOUL.md for capabilities."
      ;;
  esac
}

# ── Inject-Only Mode ─────────────────────────────────────────────────

if [[ -n "$INJECT_ONLY_PATH" ]]; then
  info "Inject-only mode: $INJECT_ONLY_PATH"
  inject_orchestration "$INJECT_ONLY_PATH"
  info "Done."
  exit 0
fi

# ── Validate base dir ─────────────────────────────────────────────────

info "Base directory: $BASE_DIR"

if [[ ! -d "$BASE_DIR" ]]; then
  echo "[ERROR] Base directory does not exist: $BASE_DIR"
  echo "        Create it first: mkdir -p $BASE_DIR"
  exit 1
fi

if [[ "$DRY_RUN" == true ]]; then
  info "DRY RUN — no files will be created or modified"
fi

# ── Team Preset Parsing ───────────────────────────────────────────────

TEAM_FILE="$TEMPLATES/teams/${TEAM}.md"

if [[ ! -f "$TEAM_FILE" ]]; then
  echo "[ERROR] Team preset not found: $TEAM_FILE"
  exit 1
fi

# Extract specialist names from first line: <!-- agents: name1, name2 -->
FIRST_LINE="$(head -1 "$TEAM_FILE")"
# Pull out the content between "agents: " and " -->"
AGENTS_RAW="$(echo "$FIRST_LINE" | sed 's/.*agents: *//; s/ *-->.*//')"

# Build specialist list from team preset + --add-agent flags
SPECIALISTS=()
if [[ -n "$AGENTS_RAW" ]]; then
  IFS=',' read -ra PRESET_AGENTS <<< "$AGENTS_RAW"
  for agent in "${PRESET_AGENTS[@]}"; do
    # Trim whitespace
    agent="$(echo "$agent" | sed 's/^ *//; s/ *$//')"
    if [[ -n "$agent" ]]; then
      SPECIALISTS+=("$agent")
    fi
  done
fi

# Add --add-agent entries (deduplicate)
for agent in "${ADD_AGENTS[@]+"${ADD_AGENTS[@]}"}"; do
  already=false
  for existing in "${SPECIALISTS[@]+"${SPECIALISTS[@]}"}"; do
    if [[ "$existing" == "$agent" ]]; then
      already=true
      break
    fi
  done
  if [[ "$already" == false ]]; then
    SPECIALISTS+=("$agent")
  fi
done

info "Team preset: $TEAM"
if [[ ${#SPECIALISTS[@]} -gt 0 ]]; then
  info "Specialists: ${SPECIALISTS[*]}"
else
  info "Specialists: (none — core agents only)"
fi

# ── Step 1: Create Core Agent Workspaces ─────────────────────────────

info "Setting up core agent workspaces..."

# Leader workspace
LEADER_WS="$BASE_DIR/$LEADER_WS_NAME"
if [[ "$DRY_RUN" != true ]]; then
  mkdir -p "$LEADER_WS/tasks/archive"
else
  dry "mkdir $LEADER_WS_NAME/tasks/archive"
fi

copy_with_backup "$TEMPLATES/leader/SOUL.md"       "$LEADER_WS/SOUL.md"       "$LEADER_WS_NAME/SOUL.md"
copy_with_backup "$TEMPLATES/leader/AGENTS.md"     "$LEADER_WS/AGENTS.md"     "$LEADER_WS_NAME/AGENTS.md"
copy_with_backup "$TEMPLATES/leader/HEARTBEAT.md"  "$LEADER_WS/HEARTBEAT.md"  "$LEADER_WS_NAME/HEARTBEAT.md"

# Inject team routing matrix into Leader's AGENTS.md
PLACEHOLDER_LINE='| _(add rows per specialist in your team)_ | _(agent name)_ |'
if [[ "$DRY_RUN" != true && -f "$TEAM_FILE" ]] && grep -qF "$PLACEHOLDER_LINE" "$LEADER_WS/AGENTS.md" 2>/dev/null; then
  # Extract routing table rows from team preset (skip header/separator, keep data rows)
  ROUTING_ROWS=$(awk '/^## Routing Matrix/{found=1; next} found && /^## /{exit} found && /^\| / && !/^\| Task Type/ && !/^\|---/{print}' "$TEAM_FILE")
  if [[ -n "$ROUTING_ROWS" ]]; then
    # Save routing rows to temp file, then use awk to replace placeholder with file contents
    ROWS_TMP="$(mktemp)"
    echo "$ROUTING_ROWS" > "$ROWS_TMP"
    awk -v placeholder="$PLACEHOLDER_LINE" -v rowsfile="$ROWS_TMP" '{
      if (index($0, placeholder) > 0) { while ((getline line < rowsfile) > 0) print line } else { print }
    }' "$LEADER_WS/AGENTS.md" > "$LEADER_WS/AGENTS.md.tmp"
    rm -f "$ROWS_TMP"
    if [[ -s "$LEADER_WS/AGENTS.md.tmp" ]]; then
      mv "$LEADER_WS/AGENTS.md.tmp" "$LEADER_WS/AGENTS.md"
      ok "$LEADER_WS_NAME/AGENTS.md routing matrix populated from team preset"
    else
      rm -f "$LEADER_WS/AGENTS.md.tmp"
      log "[WARN] awk produced empty output for AGENTS.md routing matrix — skipping"
    fi
  fi
elif [[ "$DRY_RUN" == true ]]; then
  dry "populate $LEADER_WS_NAME/AGENTS.md routing matrix from team preset"
fi

# Inject specialist capabilities into §8 Team Reference
SPEC_CAP_START="<!-- SPECIALIST_CAPABILITIES — AUTO-FILLED BY SCAFFOLD -->"
SPEC_CAP_END="<!-- /SPECIALIST_CAPABILITIES -->"
if [[ "$DRY_RUN" != true && -f "$LEADER_WS/AGENTS.md" ]] && grep -qF "$SPEC_CAP_START" "$LEADER_WS/AGENTS.md" 2>/dev/null; then
  if [[ ${#SPECIALISTS[@]} -gt 0 ]]; then
    CAPS_TMP="$(mktemp)"
    for specialist in "${SPECIALISTS[@]}"; do
      get_specialist_caps "$specialist" >> "$CAPS_TMP"
      echo "" >> "$CAPS_TMP"
    done
    awk -v marker="$SPEC_CAP_START" -v endmarker="$SPEC_CAP_END" -v capsfile="$CAPS_TMP" '
      index($0, endmarker) > 0 { skip=0; print; next }
      skip { next }
      index($0, marker) > 0 {
        print
        print ""
        while ((getline line < capsfile) > 0) print line
        skip=1
        next
      }
      { print }
    ' "$LEADER_WS/AGENTS.md" > "$LEADER_WS/AGENTS.md.tmp"
    rm -f "$CAPS_TMP"
    if [[ -s "$LEADER_WS/AGENTS.md.tmp" ]]; then
      mv "$LEADER_WS/AGENTS.md.tmp" "$LEADER_WS/AGENTS.md"
      ok "$LEADER_WS_NAME/AGENTS.md §8 specialist capabilities populated"
    else
      rm -f "$LEADER_WS/AGENTS.md.tmp"
      log "[WARN] awk produced empty output for AGENTS.md §8 capabilities — skipping"
    fi
  fi
elif [[ "$DRY_RUN" == true && ${#SPECIALISTS[@]} -gt 0 ]]; then
  dry "populate $LEADER_WS_NAME/AGENTS.md §8 specialist capabilities"
fi

# Executor workspace
EXECUTOR_WS="$BASE_DIR/workspace-executor"
if [[ "$DRY_RUN" != true ]]; then
  mkdir -p "$EXECUTOR_WS"
else
  dry "mkdir workspace-executor"
fi

copy_with_backup "$TEMPLATES/executor/SOUL.md"   "$EXECUTOR_WS/SOUL.md"   "workspace-executor/SOUL.md"
copy_with_backup "$TEMPLATES/executor/AGENTS.md" "$EXECUTOR_WS/AGENTS.md" "workspace-executor/AGENTS.md"

# Reviewer workspace
REVIEWER_WS="$BASE_DIR/workspace-reviewer"
if [[ "$DRY_RUN" != true ]]; then
  mkdir -p "$REVIEWER_WS"
else
  dry "mkdir workspace-reviewer"
fi

copy_with_backup "$TEMPLATES/reviewer/SOUL.md"   "$REVIEWER_WS/SOUL.md"   "workspace-reviewer/SOUL.md"
copy_with_backup "$TEMPLATES/reviewer/AGENTS.md" "$REVIEWER_WS/AGENTS.md" "workspace-reviewer/AGENTS.md"

# ── Step 2: Create Specialist Workspaces ─────────────────────────────

if [[ ${#SPECIALISTS[@]} -gt 0 ]]; then
  info "Setting up specialist workspaces..."
fi

for specialist in "${SPECIALISTS[@]+"${SPECIALISTS[@]}"}"; do
  spec_template="$TEMPLATES/agents/${specialist}.md"
  spec_ws="$BASE_DIR/workspace-${specialist}"
  spec_label="workspace-${specialist}"

  if [[ ! -f "$spec_template" ]]; then
    log "[WARN] Template not found for specialist '$specialist': $spec_template — skipping"
    continue
  fi

  if [[ "$DRY_RUN" != true ]]; then
    mkdir -p "$spec_ws"
  else
    dry "mkdir $spec_label"
  fi

  # Extract SOUL.md content: text after "## SOUL.md" heading's ```markdown until closing ```
  SOUL_CONTENT="$(awk '
    /^## SOUL\.md$/ { in_section=1; next }
    in_section && /^```markdown$/ { in_block=1; next }
    in_block && /^```$/ { exit }
    in_block { print }
  ' "$spec_template")"

  # Extract AGENTS.md content: text after "## AGENTS.md " heading (prefix match) ```markdown until closing ```
  AGENTS_CONTENT="$(awk '
    /^## AGENTS\.md / { in_section=1; next }
    in_section && /^```markdown$/ { in_block=1; next }
    in_block && /^```$/ { exit }
    in_block { print }
  ' "$spec_template")"

  SOUL_DST="$spec_ws/SOUL.md"
  AGENTS_DST="$spec_ws/AGENTS.md"

  if [[ "$DRY_RUN" == true ]]; then
    dry "$spec_label/SOUL.md"
    dry "$spec_label/AGENTS.md"
    dry "inject orchestration into $spec_label/AGENTS.md"
    continue
  fi

  # Write SOUL.md (with backup if differs)
  if [[ -f "$SOUL_DST" ]]; then
    EXISTING="$(cat "$SOUL_DST")"
    if [[ "$EXISTING" == "$SOUL_CONTENT" ]]; then
      skip "$spec_label/SOUL.md (already up to date)"
    else
      cp "$SOUL_DST" "${SOUL_DST}.bak"
      log "[BAK]  $spec_label/SOUL.md.bak"
      printf '%s\n' "$SOUL_CONTENT" > "$SOUL_DST"
      ok "$spec_label/SOUL.md"
    fi
  else
    printf '%s\n' "$SOUL_CONTENT" > "$SOUL_DST"
    ok "$spec_label/SOUL.md"
  fi

  # Write AGENTS.md (with backup if differs)
  if [[ -f "$AGENTS_DST" ]]; then
    EXISTING="$(cat "$AGENTS_DST")"
    # Strip orchestration injection for comparison (compare only the base content)
    BASE_EXISTING="$(awk "/^${ORCHESTRATION_MARKER//\//\\/}/{exit} {print}" "$AGENTS_DST")"
    if [[ "$BASE_EXISTING" == "$AGENTS_CONTENT" ]]; then
      skip "$spec_label/AGENTS.md (already up to date)"
    else
      cp "$AGENTS_DST" "${AGENTS_DST}.bak"
      log "[BAK]  $spec_label/AGENTS.md.bak"
      printf '%s\n' "$AGENTS_CONTENT" > "$AGENTS_DST"
      ok "$spec_label/AGENTS.md"
    fi
  else
    printf '%s\n' "$AGENTS_CONTENT" > "$AGENTS_DST"
    ok "$spec_label/AGENTS.md"
  fi

  # Inject orchestration rules
  inject_orchestration "$AGENTS_DST"
done

# ── Step 3: Create Shared Operations Directory ────────────────────────

info "Setting up shared operations..."

SHARED="$BASE_DIR/$LEADER_WS_NAME/shared"
SHARED_OPS="$SHARED/operations"

if [[ "$DRY_RUN" != true ]]; then
  mkdir -p "$SHARED_OPS"
else
  dry "mkdir $LEADER_WS_NAME/shared/operations"
fi

# Copy instance config template
copy_if_missing "$TEMPLATES/shared/INSTANCE.md" "$SHARED/INSTANCE.md" "shared/INSTANCE.md"

# Copy from templates/shared/operations/
for file in channel-map.md team-roster.md communication-signals.md; do
  copy_if_missing "$TEMPLATES/shared/operations/$file" "$SHARED_OPS/$file" "shared/operations/$file"
done

# Copy from references/
for file in brief-templates.md approval-workflow.md; do
  copy_if_missing "$REFERENCES/$file" "$SHARED_OPS/$file" "shared/operations/$file"
done

# ── Step 4: Update Team Roster ────────────────────────────────────────

if [[ ${#SPECIALISTS[@]} -gt 0 ]]; then
  ROSTER_FILE="$SHARED_OPS/team-roster.md"
  if [[ -f "$ROSTER_FILE" && "$DRY_RUN" != true ]]; then
    info "Updating team roster with specialists..."
    for specialist in "${SPECIALISTS[@]}"; do
      # Capitalize first letter, replace hyphens with spaces for display name
      display_name="$(slug_to_display_name "$specialist")"
      # Check if already in roster (match display name)
      if grep -qF "$display_name" "$ROSTER_FILE" 2>/dev/null; then
        skip "team-roster.md entry for $display_name (already present)"
      else
        # Remove the placeholder comment if it's still there (first specialist replaces it)
        sedi '/^_(Specialist agents are added below during setup)_$/d' "$ROSTER_FILE"
        # Insert specialist row before the ## Communication heading
        if grep -q '^## Communication' "$ROSTER_FILE" 2>/dev/null; then
          sedi "/^## Communication/i\\
| ${display_name} | Specialist | See workspace-${specialist}/SOUL.md |
" "$ROSTER_FILE"
        else
          printf '| %s | Specialist | See workspace-%s/SOUL.md |\n' "$display_name" "$specialist" >> "$ROSTER_FILE"
        fi
        ok "team-roster.md: added $display_name"
      fi
    done
  elif [[ "$DRY_RUN" == true ]]; then
    for specialist in "${SPECIALISTS[@]}"; do
      dry "add $specialist to team-roster.md"
    done
  fi
fi

# ── Step 5: Create Symlinks for Non-Leader Workspaces ────────────────

info "Creating symlinks to shared knowledge base..."

NON_LEADER_WORKSPACES=("workspace-executor" "workspace-reviewer")
for specialist in "${SPECIALISTS[@]+"${SPECIALISTS[@]}"}"; do
  NON_LEADER_WORKSPACES+=("workspace-${specialist}")
done

for ws_dir in "${NON_LEADER_WORKSPACES[@]}"; do
  ws_path="$BASE_DIR/$ws_dir"
  link_path="$ws_path/shared"

  if [[ "$DRY_RUN" == true ]]; then
    dry "$ws_dir/shared -> $LEADER_WS_NAME/shared"
    continue
  fi

  if [[ ! -d "$ws_path" ]]; then
    # Workspace doesn't exist (specialist may have been skipped), skip symlink
    continue
  fi

  if [[ -L "$link_path" ]]; then
    skip "$ws_dir/shared (symlink already exists)"
  elif [[ -d "$link_path" ]]; then
    skip "$ws_dir/shared (directory exists — not overwriting)"
  else
    ln -s "$BASE_DIR/$LEADER_WS_NAME/shared" "$link_path"
    ok "$ws_dir/shared -> $LEADER_WS_NAME/shared"
  fi
done

# ── Note: Cron ────────────────────────────────────────────────────────
# The orchestration kit uses OpenClaw's Heartbeat mechanism instead of
# workspace-level cron. See templates/leader/HEARTBEAT.md for details.
# To configure heartbeat interval, set agents.defaults.heartbeat in openclaw.json.

# ── Summary ───────────────────────────────────────────────────────────

info ""
info "=== Scaffold Complete ==="
info ""
info "Team:      $TEAM"
if [[ ${#SPECIALISTS[@]} -gt 0 ]]; then
  info "Agents:    leader, executor, reviewer + ${SPECIALISTS[*]}"
else
  info "Agents:    leader, executor, reviewer"
fi
info "Base dir:  $BASE_DIR"
info ""
info "Next steps:"
info "  1. Open $BASE_DIR/$LEADER_WS_NAME/ in your Claude Code session"
info "  2. Read SOUL.md and AGENTS.md to load your agent context"
info "  3. Check shared/operations/ for team configuration"
