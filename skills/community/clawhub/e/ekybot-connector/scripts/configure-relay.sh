#!/bin/bash

# EkyBot Communication Setup Script
# Auto-configure multi-agent OpenClaw + EkyBot channels

set -e

CONFIG_DIR="$HOME/.openclaw/ekybot-connector"
CONFIG_FILE="$CONFIG_DIR/config.json"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_detail() {
    echo -e "${BLUE}[DETAIL]${NC} $1"
}

print_setup() {
    echo -e "${PURPLE}[SETUP]${NC} $1"
}

usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --agents <number>     Number of agents to setup (default: 2)"
    echo "  --preset <type>       Agent preset: personal|team|enterprise (default: personal)"
    echo "  --dry-run            Show what would be done without making changes"
    echo "  --force              Overwrite existing configuration"
    echo "  --help               Show this help"
}

# Default values
NUM_AGENTS=2
PRESET="personal"
DRY_RUN=false
FORCE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --agents)
            NUM_AGENTS="$2"
            shift 2
            ;;
        --preset)
            PRESET="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Check if EkyBot connector is configured
if [[ ! -f "$CONFIG_FILE" ]]; then
    print_error "EkyBot connector not configured. Run scripts/register_workspace.sh first."
    exit 1
fi

# Load configuration
WORKSPACE_ID=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['workspace_id'])")
API_KEY=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['api_key'])")
EKYBOT_API_BASE=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['endpoints']['base_url'])")

if [[ -z "$WORKSPACE_ID" ]] || [[ -z "$API_KEY" ]]; then
    print_error "Invalid EkyBot configuration. Re-run registration."
    exit 1
fi

print_status "🤖 EkyBot Communication Setup"
echo "Workspace ID: $WORKSPACE_ID"
echo "Preset: $PRESET"
echo "Agents to setup: $NUM_AGENTS"
echo

# Agent presets
setup_agent_presets() {
    case $PRESET in
        personal)
            AGENT_CONFIGS='[
                {"id": "assistant", "name": "Assistant", "role": "General purpose assistant for daily tasks", "model": "anthropic/claude-sonnet-4-20250514"},
                {"id": "specialist", "name": "Specialist", "role": "Domain expert for complex projects", "model": "anthropic/claude-opus-4-5"}
            ]'
            ;;
        team)
            AGENT_CONFIGS='[
                {"id": "coordinator", "name": "Coordinator", "role": "Team coordination and project management", "model": "anthropic/claude-sonnet-4-20250514"},
                {"id": "researcher", "name": "Researcher", "role": "Research and analysis tasks", "model": "anthropic/claude-sonnet-4-20250514"},
                {"id": "developer", "name": "Developer", "role": "Code development and technical tasks", "model": "anthropic/claude-opus-4-5"}
            ]'
            NUM_AGENTS=3
            ;;
        enterprise)
            AGENT_CONFIGS='[
                {"id": "manager", "name": "Manager", "role": "Strategy and high-level coordination", "model": "anthropic/claude-opus-4-5"},
                {"id": "analyst", "name": "Analyst", "role": "Data analysis and reporting", "model": "anthropic/claude-sonnet-4-20250514"},
                {"id": "specialist", "name": "Specialist", "role": "Domain expertise and complex problem solving", "model": "anthropic/claude-opus-4-5"},
                {"id": "assistant", "name": "Assistant", "role": "General tasks and coordination support", "model": "anthropic/claude-sonnet-4-20250514"}
            ]'
            NUM_AGENTS=4
            ;;
        *)
            print_error "Unknown preset: $PRESET"
            exit 1
            ;;
    esac
}

# Backup OpenClaw configuration
backup_config() {
    if [[ -f "$OPENCLAW_CONFIG" ]]; then
        local backup_file="${OPENCLAW_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        if [[ "$DRY_RUN" == "true" ]]; then
            print_detail "Would backup: $OPENCLAW_CONFIG → $backup_file"
        else
            cp "$OPENCLAW_CONFIG" "$backup_file"
            print_detail "Backed up: $OPENCLAW_CONFIG → $backup_file"
        fi
    fi
}

# Create workspace directory structure
create_workspace() {
    local agent_id="$1"
    local agent_name="$2"
    local agent_role="$3"
    local workspace_path="$HOME/.openclaw/workspace-$agent_id"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_detail "Would create workspace: $workspace_path"
        return
    fi
    
    # Create workspace directory
    mkdir -p "$workspace_path/memory"
    
    # Copy essential files from main workspace if they exist
    if [[ -f "$HOME/.openclaw/workspace-main/TOOLS.md" ]]; then
        cp "$HOME/.openclaw/workspace-main/TOOLS.md" "$workspace_path/"
    fi
    
    # Create agent-specific SOUL.md
    cat > "$workspace_path/SOUL.md" << EOF
# SOUL.md - Who You Are

## Identity
- **Name:** $agent_name
- **Role:** $agent_role
- **Workspace:** $workspace_path

## Core Purpose
You are a specialized agent working as part of a coordinated multi-agent system. Your role is to $agent_role while collaborating effectively with other agents in the workspace.

## Communication Guidelines
- Use inter-agent communication via sessions_send for coordination
- Follow the protocol defined in INTER-AGENT-PROTOCOL.md
- Be concise but thorough in agent-to-agent messages
- Always identify yourself in inter-agent communications

## Collaboration Style
- **Proactive:** Reach out when you need input or have relevant information
- **Clear:** Use structured communication with clear action items
- **Respectful:** Other agents are colleagues, treat them professionally
- **Efficient:** Avoid redundant communication, focus on value-add

## Autonomy Level
- Work independently within your domain expertise
- Escalate to coordinator/manager when decisions exceed your scope
- Collaborate on cross-domain tasks
- Keep other agents informed of significant progress or blockers

---

*This file defines your personality and approach. Evolve it based on your experience.*
EOF

    # Create agent-specific AGENTS.md
    cat > "$workspace_path/AGENTS.md" << EOF
# AGENTS.md - Multi-Agent Workspace

## Your Role in the Team
You are **$agent_name** - $agent_role

## Team Structure
This workspace is part of a coordinated multi-agent system. Each agent has specialized capabilities and works together toward common goals.

## Communication Protocol
Before doing anything else each session:
1. Read SOUL.md - remember who you are
2. Check memory/\$(date +%Y-%m-%d).md for today's context
3. Review INTER-AGENT-PROTOCOL.md for communication rules

## Inter-Agent Communication
Use \`sessions_send\` to communicate with other agents:

\`\`\`bash
sessions_send sessionKey=agent:other-agent-id message="Your message"
\`\`\`

## Coordination Patterns
- **Status Updates:** Share progress on assigned tasks
- **Input Requests:** Ask for expertise from specialized agents  
- **Handoffs:** Transfer work to appropriate agent
- **Decisions:** Escalate to manager/coordinator when needed

## Memory Management
- Keep daily logs in memory/YYYY-MM-DD.md
- Share relevant context with other agents
- Avoid duplicate work by checking what others have done

---

*Effective multi-agent collaboration requires clear communication and defined responsibilities.*
EOF

    # Copy INTER-AGENT-PROTOCOL.md from main workspace
    if [[ -f "$HOME/.openclaw/workspace-main/memory/INTER-AGENT-PROTOCOL.md" ]]; then
        cp "$HOME/.openclaw/workspace-main/memory/INTER-AGENT-PROTOCOL.md" "$workspace_path/memory/"
    else
        # Create basic protocol if it doesn't exist
        cat > "$workspace_path/memory/INTER-AGENT-PROTOCOL.md" << EOF
# Inter-Agent Communication Protocol

## Message Format
\`\`\`
📨 [Sender → Receiver]

Message content here

— Sender Name
\`\`\`

## Communication Rules
1. Always identify sender and receiver
2. Be concise but complete
3. Include context if needed
4. Use structured format for complex requests
5. Acknowledge receipt when appropriate

## Session Keys
- Use agent:agent-id:workspace format
- Check sessions_list to find active sessions
- Handle timeouts gracefully

## Best Practices
- Batch related communications
- Avoid interrupting ongoing work
- Share relevant context
- Keep audit trail in memory files
EOF
    fi
    
    print_detail "Created workspace: $workspace_path"
}

# Update OpenClaw configuration with agents
update_openclaw_config() {
    if [[ "$DRY_RUN" == "true" ]]; then
        print_detail "Would update OpenClaw configuration with $NUM_AGENTS agents"
        return
    fi
    
    # Parse agent configurations
    local agents_json=""
    local i=0
    
    echo "$AGENT_CONFIGS" | python3 -c "
import json, sys
configs = json.load(sys.stdin)
for i, config in enumerate(configs[:$NUM_AGENTS]):
    if i > 0:
        print(',')
    print(f'''      {{
        \"id\": \"{config['id']}\",
        \"name\": \"{config['name']}\", 
        \"workspace\": \"$HOME/.openclaw/workspace-{config['id']}\",
        \"model\": \"{config['model']}\"
      }}''', end='')
" > /tmp/agents_config.json
    
    agents_json=$(cat /tmp/agents_config.json)
    rm -f /tmp/agents_config.json
    
    # Create new configuration
    if [[ -f "$OPENCLAW_CONFIG" ]]; then
        # Update existing config
        python3 -c "
import json, sys
try:
    with open('$OPENCLAW_CONFIG', 'r') as f:
        config = json.load(f)
except:
    config = {}

# Ensure agents section exists
if 'agents' not in config:
    config['agents'] = {}
if 'list' not in config['agents']:
    config['agents']['list'] = []

# Add new agents (avoid duplicates)
existing_ids = {agent.get('id') for agent in config['agents']['list']}
new_agents = []

for agent_config in $AGENT_CONFIGS:
    if agent_config['id'] not in existing_ids:
        new_agents.append({
            'id': agent_config['id'],
            'name': agent_config['name'],
            'workspace': f\"{os.path.expanduser('~')}/.openclaw/workspace-{agent_config['id']}\",
            'model': agent_config['model']
        })

config['agents']['list'].extend(new_agents)

# Ensure tools section allows inter-agent communication
if 'tools' not in config:
    config['tools'] = {}
if 'agentToAgent' not in config['tools']:
    config['tools']['agentToAgent'] = {'enabled': True}
else:
    config['tools']['agentToAgent']['enabled'] = True

# Write updated config
with open('$OPENCLAW_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)

print(f'Added {len(new_agents)} new agents to configuration')
" || {
        print_error "Failed to update OpenClaw configuration"
        return 1
    }
    fi
    
    print_detail "Updated OpenClaw configuration with multi-agent setup"
}

# Create EkyBot channels for agents
create_ekybot_channels() {
    if [[ "$DRY_RUN" == "true" ]]; then
        print_detail "Would create EkyBot channels for agents"
        return
    fi
    
    local created_channels=0
    
    echo "$AGENT_CONFIGS" | python3 -c "
import json, sys
configs = json.load(sys.stdin)
for config in configs[:$NUM_AGENTS]:
    print(f\"{config['id']}|{config['name']}|{config['role']}\")
" | while IFS='|' read -r agent_id agent_name agent_role; do
        # Create channel via EkyBot API
        local response=$(curl -s -X POST "$EKYBOT_API_BASE/channels" \
            -H "X-API-Key: $API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
                \"name\": \"$agent_id\",
                \"displayName\": \"$agent_name\", 
                \"description\": \"$agent_role\",
                \"workspaceId\": \"$WORKSPACE_ID\",
                \"agentId\": \"$agent_id\"
            }")
        
        if echo "$response" | grep -q '"success":true'; then
            print_detail "Created EkyBot channel: $agent_name ($agent_id)"
            ((created_channels++))
        else
            print_warning "Failed to create channel for $agent_name: $response"
        fi
    done
    
    print_detail "Created $created_channels EkyBot channels"
}

# Test inter-agent communication
test_communication() {
    if [[ "$DRY_RUN" == "true" ]]; then
        print_detail "Would test inter-agent communication"
        return
    fi
    
    print_setup "Testing inter-agent communication..."
    
    # Wait for gateway restart if needed
    sleep 2
    
    # Get first agent ID for testing
    local first_agent=$(echo "$AGENT_CONFIGS" | python3 -c "
import json, sys
configs = json.load(sys.stdin)
print(configs[0]['id']) if configs else print('')
")
    
    if [[ -n "$first_agent" ]]; then
        # Test basic communication
        local test_response=$(openclaw sessions send "agent:$first_agent" "Test message - setup complete" 2>&1 || echo "timeout")
        
        if [[ "$test_response" != *"timeout"* ]] && [[ "$test_response" != *"error"* ]]; then
            print_detail "✅ Inter-agent communication test successful"
        else
            print_warning "⚠️ Communication test had issues, but setup is complete"
            print_detail "You may need to restart the OpenClaw gateway: openclaw gateway restart"
        fi
    fi
}

# Main setup function
main() {
    print_status "🚀 Starting EkyBot multi-agent communication setup"
    
    # Check for existing setup
    if [[ -f "$OPENCLAW_CONFIG" ]] && grep -q '"agentToAgent"' "$OPENCLAW_CONFIG" && [[ "$FORCE" != "true" ]]; then
        print_warning "Multi-agent setup already detected in configuration."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Setup cancelled."
            exit 0
        fi
    fi
    
    # Setup agent configurations
    setup_agent_presets
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_warning "DRY RUN MODE - No changes will be made"
        echo
    fi
    
    print_setup "Step 1/6: Backing up configuration..."
    backup_config
    
    print_setup "Step 2/6: Creating agent workspaces..."
    echo "$AGENT_CONFIGS" | python3 -c "
import json, sys
configs = json.load(sys.stdin)
for config in configs[:$NUM_AGENTS]:
    print(f\"{config['id']}|{config['name']}|{config['role']}\")
" | while IFS='|' read -r agent_id agent_name agent_role; do
        create_workspace "$agent_id" "$agent_name" "$agent_role"
    done
    
    print_setup "Step 3/6: Updating OpenClaw configuration..."
    update_openclaw_config
    
    print_setup "Step 4/6: Creating EkyBot channels..."
    create_ekybot_channels
    
    print_setup "Step 5/6: Restarting OpenClaw gateway..."
    if [[ "$DRY_RUN" != "true" ]]; then
        openclaw gateway restart >/dev/null 2>&1 || print_warning "Gateway restart failed - may need manual restart"
        sleep 3
    else
        print_detail "Would restart OpenClaw gateway"
    fi
    
    print_setup "Step 6/6: Testing communication..."
    test_communication
    
    echo
    print_status "🎉 Multi-agent communication setup complete!"
    echo
    
    if [[ "$DRY_RUN" != "true" ]]; then
        echo "✅ Created $NUM_AGENTS agent workspaces"
        echo "✅ Updated OpenClaw configuration"
        echo "✅ Created EkyBot channels"
        echo "✅ Enabled inter-agent communication"
        echo
        print_status "Next steps:"
        echo "  1. Check agent status: openclaw sessions list"
        echo "  2. Visit EkyBot dashboard: https://ekybot.com"
        echo "  3. Test communication between agents"
        echo "  4. Customize agent SOUL.md files as needed"
        echo
        print_detail "Agent workspaces created in: ~/.openclaw/workspace-*"
        print_detail "Configuration backup: $OPENCLAW_CONFIG.backup.*"
    fi
}

# Run main function
main "$@"