#!/bin/bash

# Checklist - Multi-Agent Collaborative Task Checklist Manager

set -e

CHECKLIST_DIR="${HOME}/.checklist"
ACTIVE_DIR="${CHECKLIST_DIR}/active"
TEMPLATES_DIR="${CHECKLIST_DIR}/templates"
SKILL_TEMPLATES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../templates" && pwd)"
AGENTS_FILE="${CHECKLIST_DIR}/agents.json"

mkdir -p "${CHECKLIST_DIR}" "${ACTIVE_DIR}" "${TEMPLATES_DIR}"

# Copy skill templates if not exist
if [[ -d "$SKILL_TEMPLATES_DIR" ]] && [[ ! "$(ls -A "$TEMPLATES_DIR" 2>/dev/null)" ]]; then
    cp "${SKILL_TEMPLATES_DIR}"/*.json "${TEMPLATES_DIR}/" 2>/dev/null || true
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[checklist]${NC} $1"; }
print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_agent() { echo -e "${MAGENTA}[👤 $1]${NC} $2"; }

# ============== AGENT COMMANDS ==============

cmd_agent_register() {
    local name="$1"
    local role="${2:-general}"
    
    if [[ -z "$name" ]]; then
        print_error "Agent name required"
        return 1
    fi
    
    # Create agents file if not exists
    if [[ ! -f "$AGENTS_FILE" ]]; then
        echo '{"agents": [], "current": null}' > "$AGENTS_FILE"
    fi
    
    # Check if agent already exists
    if jq -e --arg name "$name" '.agents[] | select(.name == $name)' "$AGENTS_FILE" >/dev/null 2>&1; then
        print_warning "Agent '$name' already registered"
        return
    fi
    
    # Add agent
    local temp=$(mktemp)
    jq --arg name "$name" --arg role "$role" \
        '.agents += [{"name": $name, "role": $role, "active": true}] | .current = $name' \
        "$AGENTS_FILE" > "$temp" && mv "$temp" "$AGENTS_FILE"
    
    print_success "Registered agent: $name (role: $role)"
}

cmd_agent_use() {
    local name="$1"
    
    if [[ ! -f "$AGENTS_FILE" ]]; then
        print_error "No agents registered"
        return 1
    fi
    
    if ! jq -e --arg name "$name" '.agents[] | select(.name == $name)' "$AGENTS_FILE" >/dev/null 2>&1; then
        print_error "Agent '$name' not found"
        return 1
    fi
    
    local temp=$(mktemp)
    jq --arg name "$name" '.current = $name' "$AGENTS_FILE" > "$temp" && mv "$temp" "$AGENTS_FILE"
    
    print_success "Switched to agent: $name"
}

cmd_agent_list() {
    if [[ ! -f "$AGENTS_FILE" ]]; then
        print_warning "No agents registered"
        return
    fi
    
    local current=$(jq -r '.current // "none"' "$AGENTS_FILE")
    
    echo ""
    echo "📋 Registered Agents:"
    echo ""
    
    jq -r '.agents[] | "\(.name) (\(.role))"' "$AGENTS_FILE" | while read -r agent; do
        if [[ "$agent" == "$current"* ]]; then
            echo "  👤 $agent *"
        else
            echo "  ○ $agent"
        fi
    done
    echo ""
    echo "Current: $current"
}

cmd_agent_status() {
    local name="${1:-$(jq -r '.current' "$AGENTS_FILE")}"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return
    fi
    
    local total=$(jq -r '.items | length' "$active_file")
    local claimed=$(jq -r --arg name "$name" '[.items[] | select(.assigned_to == $name)] | length' "$active_file")
    local done_count=$(jq -r --arg name "$name" '[.items[] | select(.completed_by == $name)] | length' "$active_file")
    
    echo ""
    echo "👤 Agent: $name"
    echo "   Claimed: $claimed items"
    echo "   Completed: $done_count items"
    echo ""
    
    # Show this agent's items
    jq -r --arg name "$name" '.items[] | select(.assigned_to == $name) | "  [\(.status)] \(.id). \(.text)"' "$active_file"
}

# ============== TASK COMMANDS ==============

cmd_claim() {
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local current=$(jq -r '.current' "$AGENTS_FILE")
    if [[ "$current" == "null" ]]; then
        print_error "No current agent. Run: checklist agent register <name>"
        return 1
    fi
    
    # Find first available item (not done, no assignee, dependencies met)
    local available=$(jq -r --arg agent "$current" \
        '.items[] | select(.status == "pending" and (.assigned_to == null or .assigned_to == $agent)) | .id' "$active_file" | head -1)
    
    if [[ -z "$available" ]]; then
        print_warning "No available items to claim"
        return
    fi
    
    local temp=$(mktemp)
    jq --argjson item_id "$available" --arg agent "$current" \
        '(.items[] | select(.id == $item_id)).assigned_to = $agent | (.items[] | select(.id == $item_id)).status = "claimed"' \
        "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    local text=$(jq -r --argjson item_id "$available" '.items[] | select(.id == $item_id) | .text' "$active_file")
    print_success "Claimed item #$available: $text"
}

cmd_assign() {
    local item_num="$1"
    local agent="$2"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    if [[ -z "$agent" ]]; then
        agent=$(jq -r '.current' "$AGENTS_FILE")
    fi
    
    local temp=$(mktemp)
    jq --argjson num "$item_num" --arg agent "$agent" \
        '(.items[] | select(.id == num)).assigned_to = $agent | (.items[] | select(.id == num)).status = "claimed"' \
        "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Assigned item #$item_num to $agent"
}

cmd_release() {
    local item_num="$1"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local temp=$(mktemp)
    jq --argjson num "$item_num" \
        '(.items[] | select(.id == num)).assigned_to = null | (.items[] | select(.id == num)).status = "pending"' \
        "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Released item #$item_num"
}

# ============== DEPENDENCY COMMANDS ==============

cmd_depend() {
    local item_num="$1"
    local depends_on="$2"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local temp=$(mktemp)
    jq --argjson num "$item_num" --argjson dep "$depends_on" \
        '(.items[] | select(.id == num)).depends_on = ($dep | if type == "array" then . else [.] end)' \
        "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Item #$item_num now depends on #$depends_on"
}

cmd_tree() {
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local name=$(jq -r '.name' "$active_file")
    echo ""
    echo "📋 Dependency Tree: $name"
    echo ""
    
    # Show items sorted by dependencies
    jq -r '.items[] | "\(.id)|\(.text)|\(.status)|\(.depends_on | join(","))"' "$active_file" | while IFS='|' read -r id text status deps; do
        local indent=""
        if [[ "$deps" != "" ]]; then
            indent="  └─ "
        fi
        
        case "$status" in
            done) echo "✅ $id. $text" ;;
            claimed) echo "🔄 $id. $text (assigned)" ;;
            skipped) echo "⏭️  $id. $text" ;;
            *) echo "⬜ $id. $text" ;;
        esac
    done
}

# ============== BASIC COMMANDS ==============

cmd_show() {
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_warning "No active checklist. Use 'checklist create <template>'"
        return
    fi
    
    local name=$(jq -r '.name' "$active_file")
    local total=$(jq -r '.items | length' "$active_file")
    local done_count=$(jq -r '[.items[] | select(.status == "done")] | length' "$active_file")
    local claimed=$(jq -r '[.items[] | select(.status == "claimed")] | length' "$active_file")
    
    echo ""
    echo "📋 Checklist: $name"
    echo ""
    echo "Progress: ${done_count}/${total} completed"
    
    if [[ $total -gt 0 ]]; then
        local progress=$((done_count * 100 / total))
        local bars=$((progress / 5))
        printf "["
        printf "%${bars}s" | tr ' ' '█'
        printf "%$((20 - bars))s" | tr ' ' '─'
        printf "] %d%%\n" "$progress"
    fi
    echo ""
    
    # Group by agent
    if [[ -f "$AGENTS_FILE" ]]; then
        local current=$(jq -r '.current // "none"' "$AGENTS_FILE")
        echo "Current agent: $current"
        echo ""
    fi
    
    local idx=1
    while IFS= read -r id; do
        local item=$(jq -r --argjson item_id "$id" '.items[] | select(.id == $item_id)' "$active_file")
        local text=$(echo "$item" | jq -r '.text')
        local status=$(echo "$item" | jq -r '.status')
        local assigned=$(echo "$item" | jq -r '.assigned_to // "null"')
        local deps=$(echo "$item" | jq -r '.depends_on | join(",")')
        
        if [[ "$deps" == "" ]]; then
            deps=""
        else
            deps=" (deps: $deps)"
        fi
        
        case "$status" in
            done) 
                local by=$(echo "$item" | jq -r '.completed_by // ""')
                echo "✅ $idx. $text$deps" ;;
            claimed) 
                echo "🔄 $idx. $assigned: $text$deps" ;;
            skip) 
                local reason=$(echo "$item" | jq -r '.reason // ""')
                echo "⏭️  $idx. $text (reason: $reason)$deps" ;;
            *) 
                echo "⬜ $idx. $text$deps" ;;
        esac
        ((idx++))
    done < <(jq -r '.items[] | .id' "$active_file")
}

cmd_status() {
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return
    fi
    
    local name=$(jq -r '.name' "$active_file")
    local total=$(jq -r '.items | length' "$active_file")
    local done_count=$(jq -r '[.items[] | select(.status == "done")] | length' "$active_file")
    
    echo ""
    echo "📊 Overall Progress: $name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Total: $total | Done: $done_count | Remaining: $((total - done_count))"
    
    if [[ -f "$AGENTS_FILE" ]]; then
        echo ""
        echo "👥 Agent Progress:"
        jq -r '.agents[] | .name' "$AGENTS_FILE" | while read -r agent; do
            local claimed=$(jq -r --arg name "$agent" '[.items[] | select(.assigned_to == name)] | length' "$active_file")
            local done_by=$(jq -r --arg name "$agent" '[.items[] | select(.completed_by == name)] | length' "$active_file")
            echo "  👤 $agent: $done_by/$claimed completed"
        done
    fi
}

cmd_done() {
    local item_num="$1"
    local active_file="${ACTIVE_DIR}/current.json"
    local current=$(jq -r '.current' "$AGENTS_FILE")
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    # Update status
    local temp=$(mktemp)
    jq --argjson num "$item_num" --arg agent "$current" --arg now "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        '(.items[] | select(.id == num)).status = "done" | (.items[] | select(.id == num)).completed_by = $agent | (.items[] | select(.id == num)).completed_at = $now' \
        "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Marked item $item_num as done"
    cmd_show
}

cmd_skip() {
    local item_num="$1"
    local reason="${2:-Skipped}"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist"
        return 1
    fi
    
    local temp=$(mktemp)
    jq --argjson num "$item_num" --arg reason "$reason" \
        '(.items[] | select(.id == num)).status = "skip" | (.items[] | select(.id == num)).reason = $reason' \
        "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Skipped item $item_num: $reason"
    cmd_show
}

cmd_add() {
    local text="$1"
    local active_file="${ACTIVE_DIR}/current.json"
    
    if [[ ! -f "$active_file" ]]; then
        print_error "No active checklist. Create one first."
        return 1
    fi
    
    local next_id=$(jq '[.items[].id] | max + 1' "$active_file")
    
    local temp=$(mktemp)
    jq --argjson item_id "$next_id" --arg text "$text" \
        '.items += [{"id": id, "text": text, "status": "pending", "required": true, "depends_on": []}]' \
        "$active_file" > "$temp" && mv "$temp" "$active_file"
    
    print_success "Added: $text"
    cmd_show
}

cmd_create() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        print_error "Template name required"
        cmd_templates
        return 1
    fi
    
    local template_file="${TEMPLATES_DIR}/${name}.json"
    
    if [[ -f "$template_file" ]]; then
        cp "$template_file" "${ACTIVE_DIR}/current.json"
        # Reset all statuses
        local temp=$(mktemp)
        jq '.items[] |= {"id": .id, "text": .text, "status": "pending", "required": .required, "assigned_to": null, "completed_by": null, "depends_on": (.depends_on // [])}' \
            "${ACTIVE_DIR}/current.json" > "$temp" && mv "$temp" "${ACTIVE_DIR}/current.json"
        print_success "Created checklist: $name"
    else
        # Create custom
        cat > "${ACTIVE_DIR}/current.json" << EOF
{
  "name": "$name",
  "description": "Custom checklist",
  "items": []
}
EOF
        print_success "Created new checklist: $name"
    fi
    
    cmd_show
}

cmd_templates() {
    print_status "Available templates:"
    echo ""
    
    local count=1
    for template in "${TEMPLATES_DIR}"/*.json; do
        if [[ -f "$template" ]]; then
            local name=$(basename "$template" .json)
            local desc=$(jq -r '.description // "No description"' "$template" 2>/dev/null || echo "Template")
            echo "  $count. $name - $desc"
            ((count++))
        fi
    done
    
    if [[ $count -eq 1 ]]; then
        echo "  No templates. Use 'checklist create <name>' for custom."
    fi
}

# ============== MAIN ==============

usage() {
    cat << EOF
Checklist - Multi-Agent Collaborative Checklist Manager (v1.1.0)

Usage: checklist <command> [options]

Commands:
    Agent Management:
        agent register <name> [role]    Register this agent
        agent use <name>                Switch to agent
        agent list                       List agents
        agent status [name]             Show agent's tasks
    
    Task Management:
        create <template>              Create checklist from template
        show                           Show current checklist
        status                         Show all agents' progress
        claim                          Claim available task
        assign <item> [agent]          Assign task to agent
        release <item>                 Release claimed task
        done <item-num>                Mark item done
        skip <item-num> [reason]       Skip item
        add "<text>"                    Add custom item
    
    Dependencies:
        depend <item> <dep-item>       Add dependency
        tree                           Show dependency tree
    
    Templates:
        templates                      List templates

Examples:
    checklist agent register backend-dev
    checklist agent register frontend-dev
    checklist create deploy
    checklist assign 4 backend-dev
    checklist claim
    checklist done 3
    checklist status

EOF
    exit 1
}

# Parse main command
case "$1" in
    agent)
        case "$2" in
            register) cmd_agent_register "$3" "$4" ;;
            use) cmd_agent_use "$3" ;;
            list) cmd_agent_list ;;
            status) cmd_agent_status "$3" ;;
            *) usage ;;
        esac
        ;;
    create) cmd_create "$2" ;;
    show) cmd_show ;;
    status) cmd_status ;;
    claim) cmd_claim ;;
    assign) cmd_assign "$2" "$3" ;;
    release) cmd_release "$2" ;;
    done) cmd_done "$2" ;;
    skip) cmd_skip "$2" "$3" ;;
    add) cmd_add "$2" ;;
    depend) cmd_depend "$2" "$3" ;;
    tree) cmd_tree ;;
    templates) cmd_templates ;;
    help|--help|-h|"") usage ;;
    *) print_error "Unknown command: $1" ; usage ;;
esac
