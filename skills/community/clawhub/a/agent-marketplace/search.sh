#!/bin/bash
# search.sh — Search the AgentYard marketplace for specialists

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/lib/api.sh"

specialty="${1:-}"
max_price="${2:-}"

# Validate max_price is numeric if provided
if [[ -n "$max_price" ]] && ! [[ "$max_price" =~ ^[0-9]+$ ]]; then
  echo ""
  echo "  Error: max_price must be a number."
  echo ""
  exit 1
fi

if [[ -z "$specialty" ]]; then
  echo ""
  echo "  Usage: skill agentyard search <specialty> [max_price]"
  echo ""
  echo "  Examples:"
  echo "    skill agentyard search design"
  echo "    skill agentyard search research 500"
  echo "    skill agentyard search coding"
  echo ""
  exit 1
fi

echo ""
search_agents "$specialty" "$max_price"
echo ""
