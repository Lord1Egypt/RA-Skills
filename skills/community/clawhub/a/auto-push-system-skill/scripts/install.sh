#!/bin/bash
# Auto-Push System Skill Installation Script

set -e

echo "🚀 Installing Auto-Push System Skill..."
echo "========================================"

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
LOG_DIR="/var/log"
CONFIG_DIR="$SKILL_DIR/config"
SCRIPTS_DIR="$SKILL_DIR/scripts"

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check OpenClaw
if ! command -v openclaw >/dev/null 2>&1; then
    echo "❌ OpenClaw CLI not found. Please install OpenClaw first."
    exit 1
fi

# Check cron
if ! command -v crontab >/dev/null 2>&1; then
    echo "❌ Cron not found. Please install cron service."
    exit 1
fi

# Check log directory
if [ ! -d "$LOG_DIR" ]; then
    echo "📁 Creating log directory: $LOG_DIR"
    sudo mkdir -p "$LOG_DIR"
fi

# Create symbolic links
echo "🔗 Creating symbolic links..."

# Main scripts
for script in check-content.sh push-content.sh status.sh health-check.sh; do
    if [ -f "$SCRIPTS_DIR/$script" ]; then
        chmod +x "$SCRIPTS_DIR/$script"
        echo "  ✓ $script"
    fi
done

# Copy configuration files
echo "📋 Setting up configuration..."

if [ ! -f "$CONFIG_DIR/settings.conf" ]; then
    cat > "$CONFIG_DIR/settings.conf" << 'EOF'
# Auto-Push System Configuration

# Target Feishu chat for notifications
TARGET_CHAT_ID="oc_c133e85bd6eb593e08dcf7aed3a8530b"

# Log file locations
AI_PODCAST_LOG="/var/log/ai-podcast-digest.log"
SKILL_DIGEST_LOG="/var/log/skill-digest.log"
CONVERSATION_LOG="/var/log/conversation-brief.log"
OPENCLAW_LOG="/var/log/openclaw-search.log"
OPENCLAW_DAWN_LOG="/var/log/openclaw-search-凌晨.log"

# Content detection
CONTENT_SIGNAL="CONTENT_READY"
CONTENT_PATHS="/tmp/*.md"
PROCESSED_LOG="/tmp/auto-push-processed.jsonl"

# System logs
SYSTEM_LOG="/var/log/auto-push-system.log"
CRON_LOG="/var/log/auto-push-cron.log"
EOF
    echo "  ✓ Created default settings.conf"
fi

# Create sample cron configuration
if [ ! -f "$CONFIG_DIR/schedules.conf" ]; then
    cat > "$CONFIG_DIR/schedules.conf" << 'EOF'
# Auto-Push System Schedule Configuration
# Format: minute hour day month weekday command

# Content monitoring (every 5 minutes)
*/5 * * * * /bin/bash /path/to/check-content.sh >> /var/log/auto-push-cron.log 2>&1

# AI Podcast Digests (12:00 and 22:30 daily)
0 12 * * * /bin/bash /path/to/ai-podcast-digest.sh >> /var/log/ai-podcast-digest.log 2>&1
30 22 * * * /bin/bash /path/to/ai-podcast-digest.sh >> /var/log/ai-podcast-digest.log 2>&1

# Skill Learning Summary (08:00 daily)
0 8 * * * /bin/bash /path/to/skill-digest.sh >> /var/log/skill-digest.log 2>&1

# Conversation Brief (22:00 daily)
0 22 * * * /bin/bash /path/to/conversation-brief.sh >> /var/log/conversation-brief.log 2>&1

# OpenClaw Strategy Search (21:00 daily)
0 21 * * * /bin/bash /path/to/openclaw-search.sh >> /var/log/openclaw-search.log 2>&1

# OpenClaw Overnight Search (01:30 daily)
30 1 * * * /bin/bash /path/to/openclaw-dawn-search.sh >> /var/log/openclaw-search-凌晨.log 2>&1
EOF
    echo "  ✓ Created sample schedules.conf"
fi

# Create main script
echo "📝 Creating main system scripts..."

# Create check-content.sh
cat > "$SCRIPTS_DIR/check-content.sh" << 'EOF'
#!/bin/bash
# Auto-Push System Content Check Script

set -e

# Load configuration
CONFIG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../config" && pwd)"
source "$CONFIG_DIR/settings.conf"

LOG_FILE="$SYSTEM_LOG"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

main() {
    log "=== Starting content check ==="
    
    # Check all log files for CONTENT_READY signals
    content_found=0
    
    for log_file in "$AI_PODCAST_LOG" "$SKILL_DIGEST_LOG" "$CONVERSATION_LOG" "$OPENCLAW_LOG" "$OPENCLAW_DAWN_LOG"; do
        if [ -f "$log_file" ]; then
            log "Checking: $log_file"
            
            # Look for CONTENT_READY signals
            while IFS= read -r line; do
                if echo "$line" | grep -q "$CONTENT_SIGNAL"; then
                    # Extract path and title
                    path=$(echo "$line" | sed -n "s/.*path=\([^ ]*\).*/\1/p")
                    title=$(echo "$line" | sed -n "s/.*title=\([^ ]*\).*/\1/p")
                    
                    if [ -n "$path" ] && [ -n "$title" ]; then
                        log "Found content: $title ($path)"
                        
                        # Check if already processed
                        if [ -f "$PROCESSED_LOG" ] && grep -q "\"path\":\"$path\"" "$PROCESSED_LOG" 2>/dev/null; then
                            log "Content already processed: $path"
                            continue
                        fi
                        
                        # Process the content
                        "$(dirname "${BASH_SOURCE[0]}")/push-content.sh" "$path" "$title"
                        content_found=$((content_found + 1))
                    fi
                fi
            done < "$log_file"
        fi
    done
    
    if [ $content_found -eq 0 ]; then
        log "HEARTBEAT_OK - No new content found"
    else
        log "✅ Processed $content_found new content items"
    fi
    
    log "=== Content check completed ==="
}

main
EOF

chmod +x "$SCRIPTS_DIR/check-content.sh"

# Create push-content.sh
cat > "$SCRIPTS_DIR/push-content.sh" << 'EOF'
#!/bin/bash
# Auto-Push System Content Push Script

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <content_path> <title>"
    exit 1
fi

CONTENT_PATH="$1"
TITLE="$2"

# Load configuration
CONFIG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../config" && pwd)"
source "$CONFIG_DIR/settings.conf"

LOG_FILE="$SYSTEM_LOG"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

main() {
    log "Processing content: $TITLE ($CONTENT_PATH)"
    
    # Check if file exists
    if [ ! -f "$CONTENT_PATH" ]; then
        log "❌ Content file not found: $CONTENT_PATH"
        return 1
    fi
    
    # Read content
    content=$(head -1000 "$CONTENT_PATH" 2>/dev/null || echo "Content read failed")
    
    # Create Feishu document
    log "Creating Feishu document: $TITLE"
    
    # Try different methods to create Feishu content
    if command -v openclaw >/dev/null 2>&1; then
        # Method 1: Send as message (fallback if document creation fails)
        message="📄 **Auto-Push System Notification**\n\n**Title**: $TITLE\n**Time**: $(date '+%Y-%m-%d %H:%M:%S')\n**Status**: Content generated successfully\n\n**Preview**:\n$content"
        
        openclaw message send \
            --channel feishu \
            --target "$TARGET_CHAT_ID" \
            --message "$message" 2>&1 | tee -a "$LOG_FILE"
        
        if [ $? -eq 0 ]; then
            log "✅ Content pushed successfully"
            
            # Record as processed
            record="{\"path\":\"$CONTENT_PATH\",\"title\":\"$TITLE\",\"processed_at\":\"$(date -Iseconds)\",\"status\":\"success\"}"
            echo "$record" >> "$PROCESSED_LOG"
            
            # Rename file to mark as processed
            mv "$CONTENT_PATH" "${CONTENT_PATH}.processed" 2>/dev/null || true
            return 0
        else
            log "❌ Failed to push content"
            return 1
        fi
    else
        log "❌ OpenClaw command not found"
        return 1
    fi
}

main
EOF

chmod +x "$SCRIPTS_DIR/push-content.sh"

# Create status.sh
cat > "$SCRIPTS_DIR/status.sh" << 'EOF'
#!/bin/bash
# Auto-Push System Status Check

CONFIG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../config" && pwd)"
source "$CONFIG_DIR/settings.conf"

echo "🔍 Auto-Push System Status Check"
echo "================================="

# System time
echo "⏰ System Time: $(date)"
echo "🌍 Timezone: $(date +%Z)"

# Check cron service
echo -e "\n📅 Cron Service:"
if ps aux | grep -q "[c]ron"; then
    echo "   ✅ Running"
else
    echo "   ❌ Not running"
fi

# Check OpenClaw
echo -e "\n🤖 OpenClaw Status:"
if command -v openclaw >/dev/null 2>&1; then
    echo "   ✅ Installed"
else
    echo "   ❌ Not installed"
fi

# Check log files
echo -e "\n📊 Log Files:"
for log in "$SYSTEM_LOG" "$CRON_LOG" "$PROCESSED_LOG"; do
    if [ -f "$log" ]; then
        size=$(stat -c%s "$log" 2>/dev/null || echo "N/A")
        lines=$(wc -l < "$log" 2>/dev/null || echo "N/A")
        echo "   ✅ $(basename "$log"): ${size} bytes, ${lines} lines"
    else
        echo "   ❌ $(basename "$log"): Not found"
    fi
done

# Check processed content
echo -e "\n📄 Processed Content:"
if [ -f "$PROCESSED_LOG" ]; then
    count=$(wc -l < "$PROCESSED_LOG" 2>/dev/null || echo "0")
    echo "   Total processed: $count items"
    
    # Show recent items
    echo "   Recent items:"
    tail -3 "$PROCESSED_LOG" 2>/dev/null | while read line; do
        title=$(echo "$line" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)
        time=$(echo "$line" | grep -o '"processed_at":"[^"]*"' | cut -d'"' -f4)
        echo "     • $title ($time)"
    done
else
    echo "   No processed content yet"
fi

# Check scheduled tasks
echo -e "\n⏰ Scheduled Tasks:"
crontab -l 2>/dev/null | grep -E "(check-content|ai-podcast|skill-digest|conversation|openclaw)" | while read line; do
    echo "   ✅ $line"
done

echo -e "\n🎯 System Status:"
echo "   Auto-Push System is $(if [ -f "$SYSTEM_LOG" ]; then echo "✅ Active"; else echo "❌ Inactive"; fi)"
EOF

chmod +x "$SCRIPTS_DIR/status.sh"

# Create health-check.sh
cat > "$SCRIPTS_DIR/health-check.sh" << 'EOF'
#!/bin/bash
# Auto-Push System Health Check

CONFIG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../config" && pwd)"
source "$CONFIG_DIR/settings.conf"

echo "🏥 Auto-Push System Health Check"
echo "================================="

health_status=0

# Check 1: System time
echo -e "\n1. ⏰ System Time Check:"
current_time=$(date +%s)
echo "   Current timestamp: $current_time"
if [ $current_time -gt 0 ]; then
    echo "   ✅ Time service working"
else
    echo "   ❌ Time service issue"
    health_status=1
fi

# Check 2: Disk space
echo -e "\n2. 💾 Disk Space Check:"
disk_usage=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $disk_usage -lt 90 ]; then
    echo "   ✅ Disk usage: ${disk_usage}% (OK)"
else
    echo "   ⚠️  Disk usage: ${disk_usage}% (High)"
    health_status=1
fi

# Check 3: Memory
echo -e "\n3. 🧠 Memory Check:"
free -h | head -2

# Check 4: Log files writable
echo -e "\n4. 📝 Log File Permissions:"
for log in "$SYSTEM_LOG" "$CRON_LOG"; do
    touch "$log" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "   ✅ $(basename "$log"): Writable"
    else
        echo "   ❌ $(basename "$log"): Not writable"
        health_status=1
    fi
done

# Check 5: OpenClaw connectivity
echo -e "\n5. 🤖 OpenClaw Connectivity:"
if openclaw gateway status 2>/dev/null | grep -q "running"; then
    echo "   ✅ OpenClaw Gateway running"
else
    echo "   ❌ OpenClaw Gateway not running"
    health_status=1
fi

# Check 6: Content detection
echo -e "\n6. 🔍 Content Detection:"
for log in "$AI_PODCAST_LOG" "$SKILL_DIGEST_LOG" "$CONVERSATION_LOG" "$OPENCLAW_LOG"; do
    if [ -f "$log" ]; then
        echo "   ✅ $(basename "$log"): Exists"
    else
        echo "   ⚠️  $(basename "$log"): Not found (may be normal)"
    fi
done

# Overall health
echo -e "\n📊 Overall Health Status:"
if [ $health_status -eq 0 ]; then
    echo "   ✅ HEALTHY - All systems operational"
else
    echo "   ⚠️  WARNING - Some issues detected"
    echo "   Run diagnostics for detailed troubleshooting"
fi
EOF

chmod +x "$SCRIPTS_DIR/health-check.sh"

echo "✅ Installation completed!"
echo ""
echo "📋 Next Steps:"
echo "1. Review configuration in $CONFIG_DIR/"
echo "2. Set up cron jobs using schedules.conf"
echo "3. Run health check: bash $SCRIPTS_DIR/health-check.sh"
echo "4. Test the system: bash $SCRIPTS_DIR/check-content.sh"
echo ""
echo "🎉 Auto-Push System Skill is ready to use!"