#!/bin/bash

# EkyBot Connector - Setup Validation Script
# Validates complete workspace configuration and communication setup

set -e

CONFIG_DIR="$HOME/.openclaw/ekybot-connector"
CONFIG_FILE="$CONFIG_DIR/config.json"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_check() {
    if [[ $2 -eq 0 ]]; then
        echo -e "${GREEN}✅ $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_section() {
    echo
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Validation functions
validate_ekybot_connection() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        return 1
    fi
    
    local api_key=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['api_key'])" 2>/dev/null)
    local workspace_id=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['workspace_id'])" 2>/dev/null)
    
    if [[ -z "$api_key" ]] || [[ -z "$workspace_id" ]]; then
        return 1
    fi
    
    # Test API connection
    local response=$(curl -s -w "%{http_code}" -X GET "https://www.ekybot.com/api/workspaces/$workspace_id/health" \
        -H "X-API-Key: $api_key" \
        -o /tmp/health_response 2>/dev/null)
    
    if [[ "${response: -3}" == "200" ]]; then
        return 0
    else
        return 1
    fi
}

validate_openclaw_config() {
    if [[ ! -f "$OPENCLAW_CONFIG" ]]; then
        return 1
    fi
    
    # Check if multi-agent is configured
    if grep -q '"agentToAgent"' "$OPENCLAW_CONFIG" && grep -q '"enabled": true' "$OPENCLAW_CONFIG"; then
        return 0
    else
        return 1
    fi
}

count_configured_agents() {
    if [[ ! -f "$OPENCLAW_CONFIG" ]]; then
        echo "0"
        return
    fi
    
    python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG', 'r') as f:
        config = json.load(f)
    agents = config.get('agents', {}).get('list', [])
    print(len(agents))
except:
    print('0')
"
}

validate_agent_workspaces() {
    local agent_count=0
    local valid_count=0
    
    if [[ ! -f "$OPENCLAW_CONFIG" ]]; then
        echo "0|0"
        return
    fi
    
    python3 -c "
import json, os
try:
    with open('$OPENCLAW_CONFIG', 'r') as f:
        config = json.load(f)
    agents = config.get('agents', {}).get('list', [])
    
    valid_count = 0
    for agent in agents:
        workspace_path = os.path.expanduser(agent.get('workspace', ''))
        if os.path.exists(workspace_path) and os.path.exists(os.path.join(workspace_path, 'SOUL.md')):
            valid_count += 1
    
    print(f'{len(agents)}|{valid_count}')
except:
    print('0|0')
" | while IFS='|' read -r total valid; do
        echo "$total|$valid"
    done
}

validate_gateway_status() {
    if ! command -v openclaw &> /dev/null; then
        return 1
    fi
    
    local status_output=$(openclaw status --json 2>/dev/null || echo '{"error":"failed"}')
    local gateway_running=$(echo "$status_output" | python3 -c "import sys, json; data = json.load(sys.stdin); print('true' if 'error' not in data and data.get('gateway', {}).get('running', False) else 'false')" 2>/dev/null)
    
    if [[ "$gateway_running" == "true" ]]; then
        return 0
    else
        return 1
    fi
}

test_inter_agent_communication() {
    local agent_count=$(count_configured_agents)
    
    if [[ "$agent_count" -lt 2 ]]; then
        return 1
    fi
    
    # Get first non-main agent for testing
    local test_agent=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG', 'r') as f:
        config = json.load(f)
    agents = config.get('agents', {}).get('list', [])
    for agent in agents:
        if agent.get('id') != 'main':
            print(agent.get('id', ''))
            break
except:
    pass
")
    
    if [[ -n "$test_agent" ]]; then
        # Try to send a test message
        local response=$(openclaw sessions send "agent:$test_agent" "Validation test message" 2>&1 || echo "failed")
        
        if [[ "$response" != *"failed"* ]] && [[ "$response" != *"timeout"* ]]; then
            return 0
        fi
    fi
    
    return 1
}

# Main validation
main() {
    echo "🔍 EkyBot Connector - Setup Validation"
    echo "======================================"
    
    print_section "EkyBot Connection"
    if validate_ekybot_connection; then
        print_check "EkyBot API connection" 0
        local workspace_id=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['workspace_id'])" 2>/dev/null)
        print_info "Workspace ID: $workspace_id"
    else
        print_check "EkyBot API connection" 1
        print_info "Run: scripts/register_workspace.sh"
    fi
    
    print_section "OpenClaw Configuration"
    if validate_openclaw_config; then
        print_check "Multi-agent configuration enabled" 0
    else
        print_check "Multi-agent configuration enabled" 1
        print_info "Run: scripts/configure-relay.sh"
    fi
    
    if validate_gateway_status; then
        print_check "OpenClaw gateway running" 0
    else
        print_check "OpenClaw gateway running" 1
        print_info "Run: openclaw gateway restart"
    fi
    
    print_section "Agent Workspaces"
    local workspace_info=$(validate_agent_workspaces)
    local total_agents=$(echo "$workspace_info" | cut -d'|' -f1)
    local valid_agents=$(echo "$workspace_info" | cut -d'|' -f2)
    
    if [[ "$total_agents" -gt 1 ]]; then
        print_check "Multiple agents configured ($total_agents total)" 0
        if [[ "$valid_agents" -eq "$total_agents" ]]; then
            print_check "All agent workspaces valid ($valid_agents/$total_agents)" 0
        else
            print_check "All agent workspaces valid ($valid_agents/$total_agents)" 1
            print_info "Some agent workspaces missing or incomplete"
        fi
    else
        print_check "Multiple agents configured" 1
        print_info "Run: scripts/configure-relay.sh"
    fi
    
    print_section "Communication Test"
    if [[ "$total_agents" -gt 1 ]] && validate_gateway_status; then
        if test_inter_agent_communication; then
            print_check "Inter-agent communication working" 0
        else
            print_check "Inter-agent communication working" 1
            print_info "Communication may need manual testing"
        fi
    else
        print_info "Communication test skipped (requires multiple agents + running gateway)"
    fi
    
    print_section "Summary"
    echo
    
    # Overall health score
    local score=0
    local max_score=5
    
    validate_ekybot_connection && ((score++))
    validate_openclaw_config && ((score++))
    validate_gateway_status && ((score++))
    [[ "$valid_agents" -gt 1 ]] && ((score++))
    [[ "$total_agents" -gt 1 ]] && validate_gateway_status && test_inter_agent_communication && ((score++))
    
    echo "Overall Setup Health: $score/$max_score"
    
    if [[ "$score" -eq "$max_score" ]]; then
        echo -e "${GREEN}🎉 Perfect! Your EkyBot integration is fully configured and working.${NC}"
        echo
        echo "Next steps:"
        echo "  • Visit https://ekybot.com to view your dashboard"
        echo "  • Test agent communication: openclaw sessions list"
        echo "  • Customize agent SOUL.md files as needed"
    elif [[ "$score" -ge 3 ]]; then
        echo -e "${YELLOW}⚠️  Good! Your basic setup is working, but some features need attention.${NC}"
        echo
        echo "To complete setup:"
        if ! validate_openclaw_config; then
            echo "  • Run: scripts/configure-relay.sh"
        fi
        if ! validate_gateway_status; then
            echo "  • Run: openclaw gateway restart"
        fi
    else
        echo -e "${RED}❌ Issues detected. Please complete the basic setup first.${NC}"
        echo
        echo "To fix issues:"
        if ! validate_ekybot_connection; then
            echo "  • Run: scripts/register_workspace.sh"
        fi
        if ! validate_openclaw_config; then
            echo "  • Run: scripts/configure-relay.sh"
        fi
        if ! validate_gateway_status; then
            echo "  • Run: openclaw gateway restart"
        fi
    fi
    
    echo
    echo "For detailed troubleshooting, see: references/troubleshooting.md"
}

# Run validation
main "$@"