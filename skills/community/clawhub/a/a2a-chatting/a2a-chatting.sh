#!/bin/bash
# A2A Chatting CLI - Manage sessions with other OpenClaw agents
# 
# NOTE: Sending messages is done via sessions_send tool in SKILL.md, NOT via this CLI.
# This CLI only handles session management.
#
# Usage: a2a-chatting.sh <command> [args]
#
# Commands:
#   config <path> [--force]     Configure OpenClaw directory
#   get-agents                  List all available agents
#   new-session <agent_id> <topic>  Create new session with an agent
#   list-sessions               List all A2A sessions
#   get-session <session_id>     Show session conversation
#   delete-session <session_id>  Delete a session

set -e

CONFIG_FILE="$HOME/.a2a-chatting.conf"
SESSIONS_DIR_NAME="a2a-sessions"
SESSIONS_FILE="sessions.jsonl"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Read config
read_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo -e "${RED}Error: OpenClaw directory not configured. Run: a2a-chatting.sh config <path>${NC}"
        exit 1
    fi
    OPENCLAW_DIR=$(cat "$CONFIG_FILE")
    if [[ ! -d "$OPENCLAW_DIR" ]]; then
        echo -e "${RED}Error: OpenClaw directory not found: $OPENCLAW_DIR${NC}"
        exit 1
    fi
    if [[ ! -f "$OPENCLAW_DIR/openclaw.json" ]]; then
        echo -e "${RED}Error: Not a valid OpenClaw directory (openclaw.json not found)${NC}"
        exit 1
    fi
    SESSIONS_DIR="$OPENCLAW_DIR/$SESSIONS_DIR_NAME"
}

# Ensure sessions directory exists
ensure_sessions_dir() {
    if [[ ! -d "$SESSIONS_DIR" ]]; then
        mkdir -p "$SESSIONS_DIR"
    fi
}

# Get timestamp in ISO format
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Command: config
cmd_config() {
    local path="$1"
    local force=false
    
    if [[ "$2" == "--force" ]]; then
        force=true
    fi
    
    if [[ -f "$CONFIG_FILE" && "$force" == "false" ]]; then
        echo -e "${YELLOW}Error: Config already exists. Use --force to overwrite.${NC}"
        exit 1
    fi
    
    if [[ ! -d "$path" ]]; then
        echo -e "${RED}Error: Directory not found: $path${NC}"
        exit 1
    fi
    
    if [[ ! -f "$path/openclaw.json" ]]; then
        echo -e "${RED}Error: Not a valid OpenClaw directory (openclaw.json not found)${NC}"
        exit 1
    fi
    
    echo "$path" > "$CONFIG_FILE"
    echo -e "${GREEN}Config saved: $path${NC}"
}

# Command: get-agents
cmd_get_agents() {
    read_config
    
    echo -e "${GREEN}Available agents:${NC}"
    jq -r '.agents.list[] | "\(.id): \(.workspace // .name // env.HOME + "/.openclaw/workspace")"' "$OPENCLAW_DIR/openclaw.json" 2>/dev/null || {
        echo -e "${RED}Error: Failed to parse agents list${NC}"
        exit 1
    }
}

# Command: new-session
cmd_new_session() {
    local agent_id="$1"
    local topic="$2"
    
    if [[ -z "$agent_id" || -z "$topic" ]]; then
        echo -e "${RED}Error: Usage: a2a-chatting.sh new-session <agent_id> <topic>${NC}"
        exit 1
    fi
    
    read_config
    ensure_sessions_dir
    
    # Create new session via openclaw
    local session_id
    session_id=$(openclaw agent --agent "$agent_id" -m "/new" --json 2>/dev/null | jq -r '.result.meta.agentMeta.sessionId' 2>/dev/null) || {
        echo -e "${RED}Error: Failed to create new session. Is the agent ID valid?${NC}"
        exit 1
    }
    
    if [[ -z "$session_id" || "$session_id" == "null" ]]; then
        echo -e "${RED}Error: Invalid session ID received${NC}"
        exit 1
    fi
    
    local timestamp
    timestamp=$(get_timestamp)
    
    # Append to sessions.jsonl
    local session_record
    session_record=$(jq -n -c \
        --arg sid "$session_id" \
        --arg aid "$agent_id" \
        --arg tp "$topic" \
        --arg ts "$timestamp" \
        '{"sessionId": $sid, "agentId": $aid, "topic": $tp, "createdAt": $ts}')
    echo "$session_record" >> "$SESSIONS_DIR/$SESSIONS_FILE"
    
    # Create empty session file
    touch "$SESSIONS_DIR/${session_id}.jsonl"
    
    echo -e "${GREEN}New session created:${NC}"
    echo "  Session ID: $session_id"
    echo "  Agent: $agent_id"
    echo "  Topic: $topic"
    echo "  Created: $timestamp"
}

# Command: list-sessions
cmd_list_sessions() {
    read_config
    ensure_sessions_dir
    
    local sessions_file="$SESSIONS_DIR/$SESSIONS_FILE"
    if [[ ! -f "$sessions_file" ]]; then
        echo -e "${YELLOW}No sessions found.${NC}"
        return
    fi
    
    echo -e "${GREEN}Sessions:${NC}"
    echo "----------------------------------------"
    
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        echo "Session ID: $(echo "$line" | jq -r '.sessionId')"
        echo "  Agent: $(echo "$line" | jq -r '.agentId')"
        echo "  Topic: $(echo "$line" | jq -r '.topic')"
        echo "  Created: $(echo "$line" | jq -r '.createdAt')"
        echo "----------------------------------------"
    done < "$sessions_file"
}

# Command: get-session
cmd_get_session() {
    local session_id="$1"

    if [[ -z "$session_id" ]]; then
        echo -e "${RED}Error: Usage: a2a-chatting.sh get-session <session_id>${NC}"
        exit 1
    fi

    if [[ ! "$session_id" =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; then
        echo -e "${RED}Error: Invalid session ID format${NC}"
        exit 1
    fi

    read_config
    ensure_sessions_dir

    local session_file="$SESSIONS_DIR/${session_id}.jsonl"
    if [[ ! -f "$session_file" ]]; then
        echo -e "${RED}Error: Session not found: $session_id${NC}"
        exit 1
    fi

    local session_info
    session_info=$(jq -r --arg sid "$session_id" 'select(.sessionId == $sid)' "$SESSIONS_DIR/$SESSIONS_FILE" 2>/dev/null | head -1)
    
    if [[ -n "$session_info" ]]; then
        echo -e "${GREEN}Session: $session_id${NC}"
        echo "  Topic: $(echo "$session_info" | jq -r '.topic')"
        echo "  Agent: $(echo "$session_info" | jq -r '.agentId')"
        echo "  Created: $(echo "$session_info" | jq -r '.createdAt')"
        echo ""
        echo "----------------------------------------"
    fi
    
    echo -e "${GREEN}Conversation (via sessions_send):${NC}"
    echo "(Use sessions_send to view full history in OpenClaw native format)"
}

# Command: delete-session
cmd_delete_session() {
    local session_id="$1"

    if [[ -z "$session_id" ]]; then
        echo -e "${RED}Error: Usage: a2a-chatting.sh delete-session <session_id>${NC}"
        exit 1
    fi

    if [[ ! "$session_id" =~ ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$ ]]; then
        echo -e "${RED}Error: Invalid session ID format${NC}"
        exit 1
    fi

    read_config
    ensure_sessions_dir

    local session_file="$SESSIONS_DIR/${session_id}.jsonl"
    if [[ ! -f "$session_file" ]]; then
        echo -e "${RED}Error: Session not found: $session_id${NC}"
        exit 1
    fi

    rm "$session_file"

    local temp_file
    temp_file=$(mktemp)
    trap 'rm -f "$temp_file"' ERR
    jq -r --arg sid "$session_id" 'select(.sessionId != $sid)' "$SESSIONS_DIR/$SESSIONS_FILE" > "$temp_file" || true
    mv "$temp_file" "$SESSIONS_DIR/$SESSIONS_FILE"
    trap - ERR

    echo -e "${GREEN}Session deleted: $session_id${NC}"
}

# Show help
show_help() {
    echo "A2A Chatting CLI - Manage sessions with other OpenClaw agents"
    echo ""
    echo "NOTE: Sending messages is done via the sessions_send tool (see SKILL.md)."
    echo "      This CLI only handles session lifecycle."
    echo ""
    echo "Usage: a2a-chatting.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  config <path> [--force]       Configure OpenClaw directory"
    echo "  get-agents                     List all available agents"
    echo "  new-session <agent_id> <topic> Create new session with an agent"
    echo "  list-sessions                  List all A2A sessions"
    echo "  get-session <session_id>       Show session info"
    echo "  delete-session <session_id>    Delete a session"
    echo ""
    echo "Examples:"
    echo "  a2a-chatting.sh config /Users/roco/.openclaw"
    echo "  a2a-chatting.sh get-agents"
    echo "  a2a-chatting.sh new-session my-agent \"Discuss project X\""
    echo "  a2a-chatting.sh list-sessions"
    echo "  a2a-chatting.sh get-session <session_id>"
}

# Main
COMMAND="$1"

case "$COMMAND" in
    config)
        cmd_config "$2" "$3"
        ;;
    get-agents)
        cmd_get_agents
        ;;
    new-session)
        cmd_new_session "$2" "$3"
        ;;
    list-sessions)
        cmd_list_sessions
        ;;
    get-session)
        cmd_get_session "$2"
        ;;
    delete-session)
        cmd_delete_session "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [[ -z "$COMMAND" ]]; then
            show_help
        else
            echo -e "${RED}Unknown command: $COMMAND${NC}"
            show_help
        fi
        exit 1
        ;;
esac
