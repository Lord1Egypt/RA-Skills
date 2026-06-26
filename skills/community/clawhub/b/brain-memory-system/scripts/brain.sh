#!/usr/bin/env bash
# brain — Unified Cognitive Memory CLI
# Usage: brain <command> [args...]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
BRAIN_DB="${BRAIN_DB:-$SCRIPT_DIR/brain.db}"

# Parse global --agent flag (can appear anywhere)
BRAIN_AGENT="${BRAIN_AGENT:-margot}"
ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent|-a) BRAIN_AGENT="$2"; shift 2 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done
set -- "${ARGS[@]}"

CMD="${1:-help}"
shift || true

# Agent scope: see own + shared by default
AGENT_SCOPE="('$BRAIN_AGENT', 'shared')"

sql() {
    sqlite3 -header -column "$BRAIN_DB" "$@"
}

sql_csv() {
    sqlite3 -csv -header "$BRAIN_DB" "$@"
}

sql_plain() {
    sqlite3 "$BRAIN_DB" "$@"
}

# --- EPISODE commands ---

# --- SAFE DATABASE OPERATIONS (via Python — parameterized queries) ---
# All episode/recall/query operations route through db_ops.py
# to prevent SQL injection. See: Nygma audit 2026-03-15.

_db() {
    BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/db_ops.py" "$@"
}

cmd_store() {
    _db store "$@"
}

cmd_recall() {
    _db recall "$@"
}

cmd_episodes() {
    _db episodes "$@"
}

cmd_emotions() {
    _db emotions "$@"
}

cmd_important() {
    _db important "$@"
}

cmd_stats() {
    _db stats "$@"
}

cmd_health() {
    BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/erosion.py" "$@"
}

cmd_config() {
    local subcmd="${1:-show}"
    shift || true
    
    local conf_file="$SCRIPT_DIR/brain.conf"
    
    case "$subcmd" in
        show)
            echo "=== BRAIN LLM CONFIG ==="
            echo "Config file: $conf_file"
            echo ""
            if [[ -f "$conf_file" ]]; then
                grep -v '^#' "$conf_file" | grep -v '^$' | while IFS='=' read -r key val; do
                    key=$(echo "$key" | xargs)
                    val=$(echo "$val" | xargs)
                    if [[ "$key" == "key" && -n "$val" ]]; then
                        echo "  $key = ${val:0:8}..."
                    else
                        echo "  $key = $val"
                    fi
                done
            else
                echo "  (no config file — using defaults)"
            fi
            echo ""
            echo "Env overrides:"
            [[ -n "${BRAIN_LLM_URL:-}" ]] && echo "  BRAIN_LLM_URL=$BRAIN_LLM_URL" || echo "  BRAIN_LLM_URL=(not set)"
            [[ -n "${BRAIN_LLM_KEY:-}" ]] && echo "  BRAIN_LLM_KEY=***" || echo "  BRAIN_LLM_KEY=(not set)"
            [[ -n "${BRAIN_LLM_MODEL:-}" ]] && echo "  BRAIN_LLM_MODEL=$BRAIN_LLM_MODEL" || echo "  BRAIN_LLM_MODEL=(not set)"
            [[ -n "${GOOGLE_API_KEY:-}" ]] && echo "  GOOGLE_API_KEY=***" || echo "  GOOGLE_API_KEY=(not set)"
            ;;
        set)
            local key="${1:?Usage: brain config set <url|model|key> <value>}"
            local val="${2:?Usage: brain config set <url|model|key> <value>}"
            
            if [[ ! -f "$conf_file" ]]; then
                echo "# brain.conf" > "$conf_file"
            fi
            
            # Update or append the key
            if grep -q "^$key " "$conf_file" 2>/dev/null; then
                sed -i "s|^$key .*|$key = $val|" "$conf_file"
            else
                echo "$key = $val" >> "$conf_file"
            fi
            echo "✅ Set $key = $val"
            ;;
        help|--help|-h)
            cat <<CONFEOF
brain config — LLM Configuration

Commands:
  show                         Show current config + env overrides
  set <key> <value>            Update config file

Keys:
  url    — OpenAI-compatible chat completions endpoint
  model  — Model name for evolution
  key    — API key (or set via GOOGLE_API_KEY / BRAIN_LLM_KEY env)

Environment overrides (highest priority):
  BRAIN_LLM_URL, BRAIN_LLM_KEY, BRAIN_LLM_MODEL

Examples:
  brain config show
  brain config set model gemini-2.5-flash
  brain config set url http://localhost:11434/v1/chat/completions
  BRAIN_LLM_MODEL=gpt-4o brain proc evolve deploy-hga
CONFEOF
            ;;
        *)
            echo "Unknown config command: $subcmd"
            echo "Try: brain config help"
            exit 1
            ;;
    esac
}

cmd_filter() {
    local content="${1:?Usage: brain filter \"content\" [--source <source>] [--json]}"
    shift || true
    BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/attention.py" "$content" "$@"
}

# --- WORKING MEMORY commands (Prefrontal Cortex) ---

cmd_wm() {
    local subcmd="${1:-show}"
    shift || true
    
    case "$subcmd" in
        show|add|clear|load|dump|sync)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/working_memory.py" "$subcmd" "$@"
            ;;
        help|--help|-h)
            cat <<WMEOF
brain wm — Working Memory (Prefrontal Cortex)

Capacity-limited active context with TTL expiry.
Syncs with SESSION-STATE.md for persistence across sessions.

Commands:
  show [--json]                                  Show active slots
  add "content" [--type T] [--ttl 4h] [--pri 5]  Add a slot (goal|context|task|note)
  clear [--expired]                              Clear all or just expired
  load                                           Load from SESSION-STATE.md
  dump                                           Write back to SESSION-STATE.md
  sync                                           Bidirectional sync

Examples:
  brain wm add "Fix LightRAG crash" --type task --priority 8 --ttl 8h
  brain wm add "Puddin' testing car mode" --type context --ttl 2h
  brain wm show
  brain wm sync
WMEOF
            ;;
        *)
            echo "Unknown wm command: $subcmd"
            echo "Try: brain wm help"
            exit 1
            ;;
    esac
}

# --- FACTS commands (Semantic Memory) ---

cmd_facts() {
    local subcmd="${1:-help}"
    shift || true
    
    case "$subcmd" in
        get|set|search|list|delete|stats)
            python3 "$SCRIPT_DIR/facts.py" "$subcmd" "$@"
            ;;
        help|--help|-h)
            cat <<FACTSEOF
brain facts — Structured Fact Storage (Semantic Memory)

Commands:
  get <entity> <key>                          Get a fact value
  set <entity> <key> <value> [--category C]   Set a fact (upsert)
  search <query> [--limit N] [--json]         Full-text search
  list [--entity E] [--category C] [--limit]  List facts
  delete <entity> <key>                       Delete a fact
  stats                                       Database statistics

Examples:
  brain facts get puddin favorite_team
  brain facts set Mae birthday "September 12" --category date --permanent
  brain facts search "SSH" --limit 5
  brain facts list --entity puddin --limit 10
FACTSEOF
            ;;
        *)
            echo "Unknown facts command: $subcmd"
            echo "Try: brain facts help"
            exit 1
            ;;
    esac
}

# --- PROCEDURE commands (Cerebellum) ---

cmd_proc() {
    local subcmd="${1:-help}"
    shift || true
    
    case "$subcmd" in
        list)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/evolve.py" list
            ;;
        show)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/evolve.py" show "$@"
            ;;
        create)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/evolve.py" create "$@"
            ;;
        success)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/evolve.py" success "$@"
            ;;
        fail)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/evolve.py" fail "$@"
            ;;
        evolve)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/evolve.py" evolve "$@"
            ;;
        history)
            BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$SCRIPT_DIR/evolve.py" history "$@"
            ;;
        help|--help|-h)
            cat <<PROCEOF
brain proc — Procedural Memory (Cerebellum)

Commands:
  list                                        List all procedures
  show <slug>                                 Show procedure details + steps
  create <slug> --title "T" --steps '["s1"]'  Create new procedure
  success <slug>                              Record successful execution
  fail <slug> --step N --error "desc" [--fix] Record failure at step N
  evolve <slug> [--dry-run]                   LLM-driven evolution from failures
  history <slug>                              View full evolution timeline

Examples:
  brain proc create deploy-api --title "Deploy API" --steps '["Pull latest","Run tests","Deploy"]'
  brain proc success deploy-api
  brain proc fail deploy-api --step 2 --error "Tests timed out" --fix "Increased timeout to 60s"
  brain proc evolve deploy-api --dry-run
  brain proc evolve deploy-api
  brain proc history deploy-api
PROCEOF
            ;;
        *)
            echo "Unknown proc command: $subcmd"
            echo "Try: brain proc help"
            exit 1
            ;;
    esac
}

cmd_ingest() {
    # Combined filter + store: only stores if attention score >= threshold
    local content="${1:?Usage: brain ingest \"content\" --title \"T\" [--source <source>] [--emotion E]}"
    local source="manual"
    local title="" emotion="" intensity="" importance=""
    
    # Parse all args
    local args=("$@")
    for ((i=0; i<${#args[@]}; i++)); do
        case "${args[$i]}" in
            --source) source="${args[$((i+1))]}"; ((i++)) ;;
            --title|-t) title="${args[$((i+1))]}"; ((i++)) ;;
            --emotion|-e) emotion="${args[$((i+1))]}"; ((i++)) ;;
            --intensity|-i) intensity="${args[$((i+1))]}"; ((i++)) ;;
            --importance) importance="${args[$((i+1))]}"; ((i++)) ;;
        esac
    done
    
    # Run attention filter
    local result
    result=$(BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$(dirname "$(readlink -f "$0")")/attention.py" "$content" --source "$source" --json)
    local action score
    action=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin)['action'])")
    score=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin)['score'])")
    
    case "$action" in
        store)
            # Use attention score as importance if not explicitly set
            [[ -z "$importance" ]] && importance=$(echo "$score" | python3 -c "import sys; print(min(10, int(float(sys.stdin.read().strip()) + 0.5)))")
            local store_args=("$content")
            [[ -n "$title" ]] && store_args+=(--title "$title")
            [[ -n "$emotion" ]] && store_args+=(--emotion "$emotion")
            [[ -n "$intensity" ]] && store_args+=(--intensity "$intensity")
            store_args+=(--importance "$importance")
            cmd_store "${store_args[@]}"
            ;;
        summarize)
            echo "📋 BATCHED (score: $score) — below store threshold, queued for summary"
            ;;
        discard)
            echo "🗑️ DISCARDED (score: $score) — routine noise, not stored"
            ;;
    esac
}

cmd_consolidate() {
    local extra_args=""
    [[ "${1:-}" == "--dry-run" ]] && extra_args="--dry-run"
    [[ "${1:-}" == "-v" || "${2:-}" == "-v" ]] && extra_args="$extra_args --verbose"
    BRAIN_AGENT="$BRAIN_AGENT" BRAIN_DB="$BRAIN_DB" python3 "$(dirname "$(readlink -f "$0")")/consolidate.py" $extra_args
}

cmd_who() {
    _db who "$@"
}

cmd_help() {
    cat <<EOF
brain — Unified Cognitive Memory System

GLOBAL FLAGS:
  --agent <name>               Set agent identity (default: margot, env: BRAIN_AGENT)

STORE & RECALL:
  store "content" --title "T" [--emotion E] [--importance N]   Store an episode (bypasses filter)
  ingest "content" --title "T" [--source S] [--emotion E]      Filter + store (attention-gated)
  recall <query> [--type episodic|fact|proc|all] [--limit N]   Search all memory

ATTENTION:
  filter "content" [--source <source>]   Test attention score (store/summarize/discard)
  
QUERY:
  episodes [date]              Show episodes for a date (default: today)
  emotions [days]              Show emotional timeline (default: 7 days)
  important [threshold] [days] Show high-importance episodes

MULTI-AGENT:
  who                          Show all agents and their memory counts

CONSOLIDATION:
  consolidate [--dry-run] [-v]   Run sleep replay (hippocampal consolidation)

WORKING MEMORY (Prefrontal Cortex):
  wm show [--json]                                Show active slots
  wm add "content" [--type T] [--ttl 4h]          Add slot (goal|context|task|note)
  wm clear [--expired]                            Clear all or expired
  wm load                                         Load from SESSION-STATE.md
  wm dump                                         Write back to SESSION-STATE.md
  wm sync                                         Bidirectional sync

SEMANTIC MEMORY (Neocortex):
  facts get <entity> <key>                        Get a fact value
  facts set <entity> <key> <value> [--category]   Set a fact (upsert)
  facts search <query> [--limit N] [--json]       Full-text search
  facts list [--entity E] [--category C]          List facts
  facts delete <entity> <key>                     Delete a fact
  facts stats                                     Database statistics

PROCEDURES (Cerebellum):
  proc list                                       List all procedures
  proc show <slug>                                Show procedure + steps
  proc create <slug> --title "T" --steps '[...]'  Create procedure
  proc success <slug>                             Record success
  proc fail <slug> --step N --error "desc"        Record failure
  proc evolve <slug> [--dry-run]                  LLM-driven evolution from failures
  proc history <slug>                             View evolution timeline

CONFIG:
  config show                  Show LLM config + env overrides
  config set <key> <value>     Update LLM config (url, model, key)

SYSTEM:
  stats                        Overview statistics
  health [-v] [--json]         Soul erosion detection (7 metrics, scored 1-10)
  
Examples:
  brain store "Fixed LightRAG" --title "LightRAG Fix" --emotion focused --importance 8
  brain recall "car mode bluetooth"
  brain --agent bud store "GPU temp normal" --title "GPU Check" --importance 3
  brain proc fail deploy-hga --step 3 --error "SSH refused" --fix "Check addon first"
  brain proc evolve deploy-hga
  brain who
  brain episodes 2026-03-14
EOF
}

# Dispatch
case "$CMD" in
    store)      cmd_store "$@" ;;
    ingest)     cmd_ingest "$@" ;;
    filter)     cmd_filter "$@" ;;
    recall)     cmd_recall "$@" ;;
    episodes)   cmd_episodes "$@" ;;
    emotions)   cmd_emotions "$@" ;;
    important)  cmd_important "$@" ;;
    consolidate) cmd_consolidate "$@" ;;
    config)     cmd_config "$@" ;;
    wm)         cmd_wm "$@" ;;
    facts)      cmd_facts "$@" ;;
    proc)       cmd_proc "$@" ;;
    who)        cmd_who "$@" ;;
    stats)      cmd_stats "$@" ;;
    health)     cmd_health "$@" ;;
    help|--help|-h) cmd_help ;;
    *)          echo "Unknown command: $CMD"; cmd_help; exit 1 ;;
esac
