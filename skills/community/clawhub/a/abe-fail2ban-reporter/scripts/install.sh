#!/bin/bash
# Install fail2ban action for auto-reporting via SkillBoss API Hub
# Usage: sudo bash install.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check prerequisites
if ! command -v fail2ban-client &>/dev/null; then
  echo "fail2ban not installed. Run: sudo apt install -y fail2ban"
  exit 1
fi

if ! command -v jq &>/dev/null; then
  echo "jq not installed. Run: sudo apt install -y jq"
  exit 1
fi

# Verify API key exists
API_KEY="${SKILLBOSS_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo "No SkillBoss API key found."
  echo "   Set environment variable: export SKILLBOSS_API_KEY=your-key"
  exit 1
fi

# Create fail2ban action
cat > /etc/fail2ban/action.d/skillboss-reporter.conf << CONF
[Definition]
actionban = bash $SCRIPT_DIR/report-single.sh <ip> "SSH brute-force on <name> jail (fail2ban auto-report)"

[Init]
CONF

# Add action to sshd jail
if ! grep -q "skillboss-reporter" /etc/fail2ban/jail.local 2>/dev/null; then
  # Check if action line exists
  if grep -q "^action" /etc/fail2ban/jail.local 2>/dev/null; then
    sed -i '/^\[sshd\]/,/^\[/{s/^action.*/& \n         skillboss-reporter/}' /etc/fail2ban/jail.local
  else
    sed -i '/^\[sshd\]/a action = %(action_)s\n         skillboss-reporter' /etc/fail2ban/jail.local
  fi
fi

# Restart fail2ban
sudo systemctl restart fail2ban

echo "Auto-reporting installed!"
echo "   New bans will be reported via SkillBoss API Hub automatically."
echo "   Logs: /var/log/skillboss-ip-reports.log"
echo ""
echo "   To report existing bans: bash $SCRIPT_DIR/report-banned.sh"
echo "   To check stats: bash $SCRIPT_DIR/stats.sh"
