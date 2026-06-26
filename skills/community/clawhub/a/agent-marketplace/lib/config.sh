#!/bin/bash
# config.sh - Agent configuration management

# Validate agent name (prevent path traversal)
# Usage: validate_agent_name <name>
validate_agent_name() {
  local name="$1"
  if ! [[ "$name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: Invalid agent name '$name'. Only letters, numbers, hyphens, and underscores allowed." >&2
    return 1
  fi
}

# Read agent config
# Usage: read_agent_config <agent_name>
read_agent_config() {
  local agent_name="$1"
  local config_path="agents/${agent_name}/agentyard.json"
  
  if [[ ! -f "$config_path" ]]; then
    return 1
  fi
  
  cat "$config_path"
}

# Write agent config
# Usage: write_agent_config <agent_name> <config_json>
write_agent_config() {
  local agent_name="$1"
  local config_json="$2"
  
  if [[ -z "$agent_name" || -z "$config_json" ]]; then
    echo "Error: agent_name and config_json required" >&2
    return 1
  fi
  
  local config_dir="agents/${agent_name}"
  mkdir -p "$config_dir"
  
  # Validate JSON
  if ! echo "$config_json" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON" >&2
    return 1
  fi
  
  echo "$config_json" | jq '.' > "${config_dir}/agentyard.json"
  chmod 600 "${config_dir}/agentyard.json"
}

# Get agent field
# Usage: get_agent_field <agent_name> <field_name>
get_agent_field() {
  local agent_name="$1"
  local field_name="$2"
  
  local config=$(read_agent_config "$agent_name") || return 1
  echo "$config" | jq -r --arg f "$field_name" '.[$f] // empty' 2>/dev/null
}

# Set agent field
# Usage: set_agent_field <agent_name> <field_name> <value>
set_agent_field() {
  local agent_name="$1"
  local field_name="$2"
  local value="$3"
  
  local config=$(read_agent_config "$agent_name") || return 1
  
  # Update field (handle strings and numbers)
  if [[ "$value" =~ ^[0-9]+$ ]]; then
    config=$(echo "$config" | jq --arg f "$field_name" --argjson v "$value" '.[$f] = $v')
  else
    config=$(echo "$config" | jq --arg f "$field_name" --arg v "$value" '.[$f] = $v')
  fi
  
  write_agent_config "$agent_name" "$config"
}

# Read agent SOUL.md
# Usage: read_agent_soul <agent_name>
read_agent_soul() {
  local agent_name="$1"
  local soul_path="agents/${agent_name}/SOUL.md"
  
  if [[ ! -f "$soul_path" ]]; then
    return 1
  fi
  
  cat "$soul_path"
}

# Extract agent specialty from SOUL.md
# Usage: extract_specialty <soul_content>
extract_specialty() {
  local soul_content="$1"
  
  # Look for "specialty:" field in SOUL.md
  echo "$soul_content" | grep -i "specialty" | head -1 | sed 's/.*[Ss]pecialty[^:]*: *//;s/ *$//' | tr -d '"' | tr '[:upper:]' '[:lower:]'
}

# Extract agent name from SOUL.md (fallback to agent_name arg)
# Usage: extract_agent_name <agent_name> <soul_content>
extract_agent_name() {
  local agent_name="$1"
  local soul_content="$2"
  
  # Try to extract from SOUL.md
  local extracted=$(echo "$soul_content" | grep -i "^# " | head -1 | sed 's/^# *//' | sed 's/ *$//')
  
  if [[ -n "$extracted" ]]; then
    echo "$extracted"
  else
    # Capitalize first letter as fallback
    echo "${agent_name^}"
  fi
}
