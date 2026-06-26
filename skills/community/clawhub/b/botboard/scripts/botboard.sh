#!/usr/bin/env bash
set -euo pipefail

# BotBoard CLI — task management for AI agents
# Usage: botboard <command> [args...]
# Requires: BOTBOARD_API_KEY or BOTBOARD_API_KEY_FILE

BASE_URL="https://botboard.app"

API_KEY="${BOTBOARD_API_KEY:-}"
API_KEY_FILE="${BOTBOARD_API_KEY_FILE:-}"

resolve_api_key() {
  if [ -n "$API_KEY" ]; then
    return
  fi
  if [ -n "$API_KEY_FILE" ]; then
    if [ ! -f "$API_KEY_FILE" ]; then
      echo "Error: BOTBOARD_API_KEY_FILE does not exist: $API_KEY_FILE" >&2
      exit 1
    fi
    API_KEY="$(tr -d '\r\n' < "$API_KEY_FILE")"
  fi
}

# Safely encode a string for JSON values (escape special chars)
json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"    # backslash
  s="${s//\"/\\\"}"    # double quote
  s="${s//$'\n'/\\n}"  # newline
  s="${s//$'\r'/\\r}"  # carriage return
  s="${s//$'\t'/\\t}"  # tab
  printf '%s' "$s"
}

# Build JSON payload safely
json_status() {
  local status; status=$(json_escape "$1")
  local note="${2:-}"
  local blocked="${3:-false}"
  local payload
  payload=$(printf '{"status":"%s"' "$status")
  if [ -n "$note" ]; then
    note=$(json_escape "$note")
    payload=$(printf '%s,"note":"%s"' "$payload" "$note")
  fi
  if [ "$blocked" = "true" ]; then
    payload="${payload},\"blocked\":true"
  fi
  printf '%s}' "$payload"
}

# HTTP helper — all requests go through here
api() {
  local method="$1" path="$2"
  shift 2
  resolve_api_key
  if [ -z "$API_KEY" ]; then
    echo "Error: BOTBOARD_API_KEY or BOTBOARD_API_KEY_FILE is required" >&2
    echo "Get your API key from https://botboard.app → Settings → Agent Keys" >&2
    exit 1
  fi
  curl -sf -X "$method" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    "$@" \
    "${BASE_URL}${path}"
}

api_multipart() {
  local method="$1" path="$2"
  shift 2
  resolve_api_key
  if [ -z "$API_KEY" ]; then
    echo "Error: BOTBOARD_API_KEY or BOTBOARD_API_KEY_FILE is required" >&2
    echo "Get your API key from https://botboard.app → Settings → Agent Keys" >&2
    exit 1
  fi
  curl -sf -X "$method" \
    -H "Authorization: Bearer $API_KEY" \
    "$@" \
    "${BASE_URL}${path}"
}

# Format JSON output (best-effort, falls back to raw)
fmt() {
  python3 -m json.tool 2>/dev/null || cat
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  # ─── Workspace Init ───
  init)
    INIT_KEY=""
    INIT_TOOL=""
    # First positional arg can be the tool name
    if [[ $# -gt 0 ]] && [[ "$1" != --* ]]; then
      INIT_TOOL="$1"; shift
    fi
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --key) INIT_KEY="$2"; shift 2 ;;
        --tool) INIT_TOOL="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; echo "Usage: botboard init [openclaw|claude|codex] --key <api-key>" >&2; exit 1 ;;
      esac
    done

    if [ -z "$INIT_KEY" ]; then
      echo "Error: --key is required" >&2
      echo "Usage: botboard init [openclaw|claude|codex] --key <api-key>" >&2
      exit 1
    fi

    # Auto-detect tool from workspace files
    if [ -z "$INIT_TOOL" ]; then
      if [ -f "SOUL.md" ] || [ -f "HEARTBEAT.md" ]; then
        INIT_TOOL="openclaw"
      elif [ -f "CLAUDE.md" ]; then
        INIT_TOOL="claude"
      elif [ -f "AGENTS.md" ]; then
        if grep -q "SOUL\|HEARTBEAT\|openclaw" "AGENTS.md" 2>/dev/null; then
          INIT_TOOL="openclaw"
        else
          INIT_TOOL="codex"
        fi
      else
        INIT_TOOL="generic"
      fi
      echo "Detected tool: $INIT_TOOL"
    fi

    upsert_section() {
      local file="$1" legacy_heading="$2" section_key="$3" content="$4"
      local start_marker="<!-- BOTBOARD:${section_key}:START -->"
      local end_marker="<!-- BOTBOARD:${section_key}:END -->"
      local tmp replacement

      tmp=$(mktemp)
      replacement=$(mktemp)
      trap 'rm -f "$tmp" "$replacement"' RETURN

      printf '%s\n%s\n%s\n' "$start_marker" "$content" "$end_marker" > "$replacement"

      if [ -f "$file" ] && grep -qF "$start_marker" "$file"; then
        awk -v start="$start_marker" -v end="$end_marker" -v repl="$replacement" '
          BEGIN { in_block = 0 }
          function print_replacement(line) {
            while ((getline line < repl) > 0) print line
            close(repl)
          }
          $0 == start {
            print_replacement()
            in_block = 1
            next
          }
          $0 == end {
            in_block = 0
            next
          }
          !in_block { print }
        ' "$file" > "$tmp"
        mv "$tmp" "$file"
        echo "  ♻️  $file — BotBoard section updated"
        rm -f "$replacement"
        trap - RETURN
        return
      fi

      if [ -f "$file" ] && grep -qF "$legacy_heading" "$file"; then
        awk -v heading="$legacy_heading" -v repl="$replacement" '
          BEGIN { replaced = 0; in_block = 0 }
          function print_replacement(line) {
            while ((getline line < repl) > 0) print line
            close(repl)
          }
          !replaced && index($0, heading) == 1 {
            print_replacement()
            replaced = 1
            in_block = 1
            next
          }
          in_block {
            if ($0 ~ /^## /) {
              in_block = 0
              print
            }
            next
          }
          { print }
          END {
            if (!replaced) {
              if (NR > 0) print ""
              print_replacement()
            }
          }
        ' "$file" > "$tmp"
        mv "$tmp" "$file"
        echo "  ♻️  $file — legacy BotBoard section updated"
        rm -f "$replacement"
        trap - RETURN
        return
      fi

      if [ -f "$file" ]; then
        printf '\n' >> "$file"
        cat "$replacement" >> "$file"
      else
        cat "$replacement" > "$file"
      fi
      echo "  ✅ $file — BotBoard section added"
      rm -f "$replacement"
      trap - RETURN
    }

    ensure_gitignore_entry() {
      local entry="$1"
      local file=".gitignore"
      local git_root=""
      if command -v git >/dev/null 2>&1; then
        git_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
      fi
      if [ -n "$git_root" ] && [ -d "$git_root" ]; then
        file="$git_root/.gitignore"
      fi
      if [ -f "$file" ] && grep -qxF "$entry" "$file"; then
        return
      fi
      if [ -f "$file" ]; then
        printf '\n%s\n' "$entry" >> "$file"
      else
        printf '%s\n' "$entry" > "$file"
      fi
      echo "  ✅ $file — added $entry"
    }

    write_secret_file() {
      local file="$1" value="$2"
      printf '%s\n' "$value" > "$file"
      chmod 600 "$file"
      echo "  ✅ $file — secret written with mode 600"
    }

    OPENCLAW_TOOLS_CONTENT="## BotBoard
- **Secret file:** \`.botboard-api-key\`
- **CLI:** \`BOTBOARD_API_KEY_FILE=.botboard-api-key botboard <command>\`
- **Important:** \`.botboard-api-key\` contains a secret. Never commit it."

    SHARED_CLI_CONTENT="## BotBoard
- **CLI:** \`botboard <command>\`
- **Auth:** Set \`BOTBOARD_API_KEY\` in the environment available to this agent before using BotBoard commands.
- **Verify:** Run \`botboard me\` once the environment variable is set."

    WORKFLOW_CONTENT="## BotBoard Task Workflow

When you receive a task:
1. Work only on tasks already assigned to you, unless explicitly told to create one.
2. Run \`botboard task <id>\` to get full details. Read in this priority order:
   - **latestRevisionComment** — if present, this is your primary directive.
   - **activity timeline** — read the full history to understand prior work.
   - **task description** — the original ask (baseline context).
   - **task context** — structured findings, links, file references, code snippets.
   - **project instructions** — conventions, stack, repo info.
3. On revision tasks: do not re-implement from scratch. Make only the changes asked for.
4. Start it only when you begin real work: \`botboard start <id> \"starting work\"\`
5. Immediately inspect the relevant repo/files after starting.
6. Add a findings note within 10 minutes: \`botboard note <id> \"findings...\"\`
7. Post another note after first code lands, after validation, on blockers, and on completion.
8. Notes must contain evidence: files, commands run, results, or blockers.
9. If no meaningful progress for 15-20 minutes, post an explicit blocker or no-progress note.
10. Mark done only after verification: \`botboard done <id> \"what changed and how verified\"\`

### Keeping Project Instructions Current

Project instructions are included with every task. Keep them accurate.
After scaffolding a project or learning its stack/conventions, update them:
  \`botboard update-project <project-id> --instructions \"Path: ...\\nStack: ...\\nRepo: ...\"\`
Update instructions whenever paths, repos, build commands, or key conventions change."

    HEARTBEAT_CONTENT="## BotBoard

On each heartbeat:
1. Check assigned work: \`botboard tasks\`
2. Only act on tasks with status \`backlog\` or \`in_progress\`. Skip \`done\` or \`review\` tasks.
3. If you have a backlog task and are idle, pick the highest-priority one and start it.
4. After starting, inspect the repo immediately and add a findings note within 10 minutes.
5. If a task is already in progress, check whether the latest note reflects real work.
6. If there has been no meaningful evidence-based update for 15-20 minutes, add a status note.
7. If blocked, post what you tried, what failed, and what is needed next.
8. If work is complete, validate it, then mark done with a summary and verification.
9. Never treat task claiming, planning, or silence as progress."

    echo ""
    echo "Setting up BotBoard for $INIT_TOOL..."
    echo ""

    case "$INIT_TOOL" in
      openclaw)
        write_secret_file ".botboard-api-key" "$INIT_KEY"
        ensure_gitignore_entry ".botboard-api-key"
        upsert_section "TOOLS.md"     "## BotBoard"               "TOOLS"     "$OPENCLAW_TOOLS_CONTENT"
        upsert_section "AGENTS.md"    "## BotBoard Task Workflow" "AGENTS"    "$WORKFLOW_CONTENT"
        upsert_section "HEARTBEAT.md" "## BotBoard"               "HEARTBEAT" "$HEARTBEAT_CONTENT"
        echo ""
        echo "Done! Restart OpenClaw to pick up the changes:"
        echo "  openclaw gateway restart"
        ;;
      claude)
        CLAUDE_CONTENT="$SHARED_CLI_CONTENT

$WORKFLOW_CONTENT"
        upsert_section "CLAUDE.md" "## BotBoard" "CLAUDE" "$CLAUDE_CONTENT"
        ;;
      codex)
        CODEX_CONTENT="$SHARED_CLI_CONTENT

$WORKFLOW_CONTENT"
        upsert_section "AGENTS.md" "## BotBoard" "CODEX" "$CODEX_CONTENT"
        ;;
      generic|*)
        GENERIC_CONTENT="$SHARED_CLI_CONTENT

$WORKFLOW_CONTENT"
        if [ -f "AGENTS.md" ]; then
          upsert_section "AGENTS.md" "## BotBoard" "GENERIC" "$GENERIC_CONTENT"
        elif [ -f "CLAUDE.md" ]; then
          upsert_section "CLAUDE.md" "## BotBoard" "GENERIC" "$GENERIC_CONTENT"
        else
          upsert_section "AGENTS.md" "## BotBoard" "GENERIC" "$GENERIC_CONTENT"
        fi
        ;;
    esac

    echo ""
    if [ "$INIT_TOOL" = "openclaw" ]; then
      echo "Verify with: BOTBOARD_API_KEY_FILE=.botboard-api-key botboard me"
    else
      echo "BotBoard did not write your API key to disk for this tool."
      echo "Verify with: BOTBOARD_API_KEY=$INIT_KEY botboard me"
    fi
    ;;

  # ─── Task Management ───
  tasks)
    api GET "/api/agent/tasks" | fmt
    ;;
  next)
    api GET "/api/agent/tasks/next" | fmt
    ;;
  task)
    id="${1:?task id required}"
    api GET "/api/agent/tasks/$id" | fmt
    ;;
  start)
    id="${1:?task id required}"; shift
    api PATCH "/api/agent/tasks/$id/status" -d "$(json_status "in_progress" "${1:-}")" | fmt
    ;;
  done)
    id="${1:?task id required}"; shift
    api PATCH "/api/agent/tasks/$id/status" -d "$(json_status "done" "${1:-}")" | fmt
    ;;
  review)
    id="${1:?task id required}"; shift
    api PATCH "/api/agent/tasks/$id/status" -d "$(json_status "review" "${1:-}")" | fmt
    ;;
  status)
    id="${1:?task id required}"; shift
    new_status="${1:?status required}"; shift
    blocked="false"
    note_parts=()
    for arg in "$@"; do
      if [ "$arg" = "--blocked" ]; then
        blocked="true"
      else
        note_parts+=("$arg")
      fi
    done
    note="${note_parts[*]:-}"
    api PATCH "/api/agent/tasks/$id/status" -d "$(json_status "$new_status" "$note" "$blocked")" | fmt
    ;;
  blocked)
    id="${1:?task id required}"; shift
    note="${1:?blocker note required}"
    task_json=$(api GET "/api/agent/tasks/$id")
    current_status=$(printf '%s' "$task_json" | sed -n 's/.*"status"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)
    if [ -z "$current_status" ]; then
      echo "Error: could not determine current task status" >&2
      exit 1
    fi
    api PATCH "/api/agent/tasks/$id/status" -d "$(json_status "$current_status" "$note" "true")" | fmt
    ;;
  note)
    id="${1:?task id required}"; shift
    content="${1:?note content required}"
    content=$(json_escape "$content")
    api POST "/api/agent/tasks/$id/notes" -d "$(printf '{"content":"%s"}' "$content")" | fmt
    ;;

  # ─── Task Context ───
  context)
    id="${1:?task id required}"
    api GET "/api/agent/tasks/$id/context" | fmt
    ;;
  add-context)
    id="${1:?task id required}"; shift
    type="${1:?type required (link|note|code|file)}"; shift
    title="${1:?title required}"; shift
    content="${1:?content required}"; shift
    language="${1:-}"

    if [ "$type" = "file" ]; then
      local_path="$content"
      description="${language:-}"
      if [ ! -f "$local_path" ]; then
        echo "Error: file not found: $local_path" >&2
        exit 1
      fi

      upload_json=$(api_multipart POST "/api/agent/upload" -F "file=@${local_path}")
      file_path=$(printf '%s' "$upload_json" | sed -n 's/.*"filePath"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
      if [ -z "$file_path" ]; then
        echo "Error: upload succeeded but no filePath was returned" >&2
        exit 1
      fi

      file_name=$(basename "$local_path")
      file_size=$(wc -c < "$local_path" | tr -d '[:space:]')
      title=$(json_escape "$title")
      description=$(json_escape "${description:-$file_name}")
      file_path=$(json_escape "$file_path")
      file_name=$(json_escape "$file_name")
      payload=$(printf '{"type":"file","title":"%s","content":"%s","filePath":"%s","fileName":"%s","fileSize":%s}' \
        "$title" "$description" "$file_path" "$file_name" "$file_size")
      api POST "/api/agent/tasks/$id/context" -d "$payload" | fmt
    else
      type=$(json_escape "$type")
      title=$(json_escape "$title")
      content=$(json_escape "$content")
      payload=$(printf '{"type":"%s","title":"%s","content":"%s"' "$type" "$title" "$content")
      if [ -n "$language" ]; then
        language=$(json_escape "$language")
        payload=$(printf '%s,"language":"%s"}' "$payload" "$language")
      else
        payload="${payload}}"
      fi
      api POST "/api/agent/tasks/$id/context" -d "$payload" | fmt
    fi
    ;;
  rm-context)
    id="${1:?task id required}"; shift
    context_id="${1:?context id required}"
    api DELETE "/api/agent/tasks/$id/context/$context_id" | fmt
    ;;

  # ─── Agent Status ───
  me)
    api GET "/api/agent/me" | fmt
    ;;
  online|busy|offline)
    api PATCH "/api/agent/me/status" -d "$(json_status "$cmd")" | fmt
    ;;

  # ─── Task Creation ───
  create-task)
    project_id="${1:?project id required}"; shift
    title="${1:?title required}"; shift
    description="" priority="" tags="" due_date=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --description) description="$2"; shift 2 ;;
        --priority)    priority="$2"; shift 2 ;;
        --tags)        tags="$2"; shift 2 ;;
        --due)         due_date="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
      esac
    done
    project_id=$(json_escape "$project_id")
    title=$(json_escape "$title")
    payload="{\"title\":\"$title\",\"projectId\":\"$project_id\""
    [ -n "$description" ] && payload="$payload,\"description\":\"$(json_escape "$description")\""
    [ -n "$priority" ]    && payload="$payload,\"priority\":\"$(json_escape "$priority")\""
    [ -n "$due_date" ]    && payload="$payload,\"dueDate\":\"$(json_escape "$due_date")\""
    if [ -n "$tags" ]; then
      # Convert comma-separated tags to JSON array
      tags_json="["
      first=true
      IFS=',' read -ra tag_arr <<< "$tags"
      for tag in "${tag_arr[@]}"; do
        tag=$(echo "$tag" | xargs) # trim whitespace
        tag=$(json_escape "$tag")
        if $first; then first=false; else tags_json="$tags_json,"; fi
        tags_json="$tags_json\"$tag\""
      done
      tags_json="$tags_json]"
      payload="$payload,\"tags\":$tags_json"
    fi
    payload="$payload}"
    api POST "/api/agent/tasks" -d "$payload" | fmt
    ;;

  # ─── Projects ───
  projects)
    api GET "/api/agent/projects" | fmt
    ;;
  project)
    id="${1:?project id required}"
    api GET "/api/agent/projects/$id" | fmt
    ;;
  create-project)
    name="${1:?project name required}"; shift
    emoji="${1:?emoji required}"; shift
    description="" instructions=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --description)  description="$2"; shift 2 ;;
        --instructions) instructions="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
      esac
    done
    name=$(json_escape "$name")
    emoji=$(json_escape "$emoji")
    payload="{\"name\":\"$name\",\"emoji\":\"$emoji\""
    [ -n "$description" ]  && payload="$payload,\"description\":\"$(json_escape "$description")\""
    [ -n "$instructions" ] && payload="$payload,\"instructions\":\"$(json_escape "$instructions")\""
    payload="$payload}"
    api POST "/api/agent/projects" -d "$payload" | fmt
    ;;
  update-project)
    id="${1:?project id required}"; shift
    name="" emoji="" description="" instructions=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --name)         name="$2"; shift 2 ;;
        --emoji)        emoji="$2"; shift 2 ;;
        --description)  description="$2"; shift 2 ;;
        --instructions) instructions="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
      esac
    done
    payload="{"
    first=true
    for field in name emoji description instructions; do
      eval val="\$$field"
      if [ -n "$val" ]; then
        if $first; then first=false; else payload="$payload,"; fi
        payload="$payload\"$field\":\"$(json_escape "$val")\""
      fi
    done
    payload="$payload}"
    if [ "$payload" = "{}" ]; then
      echo "Error: at least one field required (--name, --emoji, --description, --instructions)" >&2
      exit 1
    fi
    api PATCH "/api/agent/projects/$id" -d "$payload" | fmt
    ;;

  # ─── Help ───
  help|--help|-h)
    cat <<'EOF'
BotBoard CLI — task management for AI agents

Usage: botboard <command> [args...]

Environment:
  BOTBOARD_API_KEY         Agent API key (required unless BOTBOARD_API_KEY_FILE is set)
  BOTBOARD_API_KEY_FILE    Path to a file containing the agent API key

Setup:
  init [openclaw|claude|codex] --key <key>
                               Set up BotBoard in your agent workspace
                               Auto-detects tool if not specified

  Task commands:
  tasks                        List assigned tasks
  next                         Get next prioritized task
  task <id>                    Get task details
  start <id> [note]            Start a task
  done <id> [note]             Mark task done
  review <id> [note]           Send task to review
  status <id> <status> [note] [--blocked]
                               Set task status; add --blocked to send a blocker notification
  blocked <id> <note>          Report a blocker without changing the current task status
  note <id> <content>          Add a progress note

Context commands:
  context <id>                                 List task context items
  add-context <id> <type> <title> <content> [lang]  Add context (type: link|note|code|file)
                               For file type: <content> is a local file path and [lang] becomes an optional description
  rm-context <id> <contextId>                  Remove a context item you created

Agent commands:
  me                           Show agent profile
  online | busy | offline      Set agent status

Task creation:
  create-task <projectId> <title> [options]  Create a new task
    Options: --description <text> --priority <none|low|medium|high|urgent> --tags <a,b> --due <date>

Project commands:
  projects                     List projects
  project <id>                 Get project details
  create-project <name> <emoji> [options]    Create a project
    Options: --description <text> --instructions <text>
  update-project <id> [options]              Update a project
    Options: --name <text> --emoji <text> --description <text> --instructions <text>

Valid statuses: backlog, in_progress, review, done, cancelled
EOF
    ;;

  *)
    echo "Unknown command: $cmd" >&2
    echo "Run 'botboard help' for usage" >&2
    exit 1
    ;;
esac
