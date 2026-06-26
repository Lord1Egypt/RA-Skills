#!/bin/bash
#
# Daily Briefing Generator
# Generates a morning briefing with weather, calendar, news, and insights.
#
# Usage: ./generate-briefing.sh
# Output: Formatted briefing text to stdout
#

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="${SCRIPT_DIR}/lib"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"

# Default location (Leyton, London)
CITY="Leyton,London"
LAT="51.5667"
LON="-0.0167"

# Colors (disable if not TTY)
if [[ -t 1 ]]; then
    BOLD='\033[1m'
    RESET='\033[0m'
else
    BOLD=''
    RESET=''
fi

# Helper functions
print_header() {
    echo -e "${BOLD}$1${RESET}"
    echo
}

print_section() {
    local emoji="$1"
    local title="$2"
    local content="$3"
    
    if [[ -n "$content" && "$content" != "null" ]]; then
        echo "$emoji $title"
        echo "$content"
        echo
    fi
}

# Get current date
date_str=$(date +"%A, %B %d")

# Output header
echo "📰 Good morning! Here's your briefing for $date_str"
echo

# 1. Weather
weather_output=$(python3 "${LIB_DIR}/weather.py" "$CITY" "$LAT" "$LON" 2>/dev/null || echo "⚠️ Weather unavailable")
print_section "🌤️" "Weather in Leyton" "$weather_output"

# 2. Calendar
calendar_output=$(python3 "${LIB_DIR}/calendar.py" 2>/dev/null || echo "   📭 Calendar unavailable")
print_section "📅" "Today" "$calendar_output"

# 3. News
news_output=$(python3 "${LIB_DIR}/news.py" 5 2>/dev/null || echo "   ⚠️ News unavailable")
print_section "📰" "Top Stories" "$news_output"

# 4. AI/Tech Pulse
ai_output=$(python3 "${LIB_DIR}/ai_pulse.py" 4 2>/dev/null || echo "   ⚠️ AI pulse unavailable")
print_section "🤖" "AI/Tech Pulse" "$ai_output"

# 5. OpenClaw Deep Dive
openclaw_output=$(python3 "${LIB_DIR}/openclaw_dive.py" 2>/dev/null || echo "   📦 Check out the latest skills in ~/openclaw/skills/")
print_section "🦾" "OpenClaw Deep Dive" "$openclaw_output"

# 6. Model Usage / Costs
cost_output=$(python3 "${LIB_DIR}/cost_tracker.py" 2>/dev/null || echo "   💸 Cost tracking unavailable")
print_section "💸" "AI Spend Tracker" "$cost_output"

# 7. Two Things to Try
suggestions_output=$(python3 "${LIB_DIR}/suggestions.py" 2 2>/dev/null || echo "   1. Review your TOOLS.md and update with any new learnings")
print_section "💡" "Two Things to Try" "$suggestions_output"

# Footer
echo "☕ Have a great day!"
