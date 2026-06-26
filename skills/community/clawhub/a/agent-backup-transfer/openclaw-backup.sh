#!/bin/bash

# OpenClaw Backup - Skill for ClawHub
# Backup and restore your OpenClaw agent

set -e

BACKUP_DIR="$HOME/openclaw-backups"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"

usage() {
    echo "Usage: openclaw-backup <create|restore|list|setup-auto> [args]"
    echo ""
    echo "Commands:"
    echo "  create               Create a backup (workspace + config)"
    echo "  restore <file>      Restore from a backup tar.gz file"
    echo "  list                 List available backups"
    echo "  setup-auto           Set up auto-backup hook"
    echo ""
    echo "Examples:"
    echo "  openclaw-backup create"
    echo "  openclaw-backup restore ~/Downloads/openclaw-backup-2026-03-09.tar.gz"
    echo "  openclaw-backup list"
    exit 1
}

cmd_create() {
    mkdir -p "$BACKUP_DIR"
    
    DATE=$(date +%Y-%m-%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/openclaw-backup-$DATE.tar.gz"
    
    cd "$HOME"
    
    # Backup workspace and config
    tar -czf "$BACKUP_FILE" \
        --exclude='*.log' \
        --exclude='*.tmp' \
        --exclude='node_modules' \
        --exclude='.git' \
        .openclaw/workspace \
        .openclaw/openclaw.json \
        .openclaw/identity \
        .openclaw/agents
    
    echo "✅ Backup created: $BACKUP_FILE"
    ls -lh "$BACKUP_FILE"
    
    # Keep only last 10 backups
    cd "$BACKUP_DIR"
    ls -t openclaw-backup-*.tar.gz 2>/dev/null | tail -n +11 | while read f; do rm -f "$f"; done
    echo "🧹 Cleaned up old backups (kept last 10)"
}

cmd_restore() {
    if [ -z "$1" ]; then
        echo "❌ Error: Please specify a backup file to restore"
        echo "Usage: openclaw-backup restore <file>"
        echo ""
        echo "📂 Place your backup file anywhere, e.g.:"
        echo "   ~/Downloads/openclaw-backup-2026-03-09.tar.gz"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    
    # Expand ~ if present
    BACKUP_FILE="${BACKUP_FILE/#\~/$HOME}"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "❌ Error: File not found: $BACKUP_FILE"
        exit 1
    fi
    
    echo "⚠️  This will restore your agent from: $BACKUP_FILE"
    echo "   Existing files may be overwritten."
    read -p "Continue? (y/n) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    
    cd "$HOME"
    tar -xzf "$BACKUP_FILE"
    
    echo ""
    echo "✅ Restore complete!"
    echo ""
    echo "Next steps:"
    echo "1. Start OpenClaw: openclaw gateway start"
    echo "2. Open dashboard: http://127.0.0.1:18789/"
}

cmd_list() {
    if [ ! -d "$BACKUP_DIR" ]; then
        echo "No backups found. Run 'openclaw-backup create' first."
        exit 0
    fi
    
    echo "📦 Available backups in $BACKUP_DIR:"
    ls -lth "$BACKUP_DIR"/openclaw-backup-*.tar.gz 2>/dev/null || echo "  (none)"
}

cmd_setup_auto() {
    echo "🔧 Setting up auto-backup hook..."
    
    # Create a hook script that backs up when called
    mkdir -p "$WORKSPACE_DIR/.hooks"
    
    cat > "$WORKSPACE_DIR/.hooks/post-memory-save.sh" << 'HOOK'
#!/bin/bash
# Auto-backup after important memory updates

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="$SCRIPT_DIR/../../skills/openclaw-backup/openclaw-backup.sh"

if [ -f "$BACKUP_SCRIPT" ]; then
    "$BACKUP_SCRIPT" create
    echo "💾 Agent backed up!"
else
    echo "⚠️ Backup script not found at: $BACKUP_SCRIPT"
fi
HOOK
    
    chmod +x "$WORKSPACE_DIR/.hooks/post-memory-save.sh"
    
    echo ""
    echo "✅ Auto-backup hook created!"
    echo ""
    echo "To use: When important memories are saved, run:"
    echo "   ~/.openclaw/workspace/.hooks/post-memory-save.sh"
    echo ""
    echo "Or add to crontab for daily backups:"
    echo "   crontab -e"
    echo "   # Add: 0 2 * * * ~/.openclaw/workspace/skills/openclaw-backup/openclaw-backup.sh create"
}

case "$1" in
    create)
        cmd_create
        ;;
    restore)
        shift
        cmd_restore "$@"
        ;;
    list)
        cmd_list
        ;;
    setup-auto)
        cmd_setup_auto
        ;;
    *)
        usage
        ;;
esac
