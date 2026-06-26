#!/bin/bash
# =============================================================================
# canary-test.sh — Pre-flight baseline capture and post-change validation
# =============================================================================
# Usage:
#   bash canary-test.sh baseline    — Capture current system state
#   bash canary-test.sh validate    — Compare current state to baseline
#   bash canary-test.sh rollback    — Restore backed-up config files
#   bash canary-test.sh status      — Show current baseline info
# =============================================================================

set -euo pipefail

CANARY_DIR="${CANARY_DIR:-/tmp/canary-deploy}"
BASELINE_FILE="$CANARY_DIR/baseline.json"
BACKUP_DIR="$CANARY_DIR/backups"
ACTION="${1:-help}"

mkdir -p "$CANARY_DIR" "$BACKUP_DIR"

# --- Helpers -----------------------------------------------------------------

capture_state() {
    local output="$1"
    
    echo "{" > "$output"
    
    # SSH connectivity
    echo '  "ssh_local": '$(ssh -o ConnectTimeout=3 -o BatchMode=yes localhost echo 1 2>/dev/null && echo "true" || echo "false")',' >> "$output"
    
    # Open ports
    echo '  "ports": "'$(ss -tlnp 2>/dev/null | grep LISTEN | awk '{print $4}' | sort | tr '\n' ',' | sed 's/,$//')',"' >> "$output"
    
    # Key services
    echo '  "services": {' >> "$output"
    for svc in sshd openclaw-gateway fail2ban ufw; do
        STATUS=$(systemctl is-active "$svc" 2>/dev/null || echo "inactive")
        echo "    \"$svc\": \"$STATUS\"," >> "$output"
    done
    echo '    "_": "end"' >> "$output"
    echo '  },' >> "$output"
    
    # Firewall rules
    echo '  "firewall": "'$(sudo ufw status 2>/dev/null | head -1 || echo 'unknown')',"' >> "$output"
    
    # DNS
    echo '  "dns": '$(host -W 3 google.com >/dev/null 2>&1 && echo "true" || echo "false")',' >> "$output"
    
    # Config checksums
    echo '  "checksums": {' >> "$output"
    for f in /etc/ssh/sshd_config /etc/fail2ban/jail.local /etc/ufw/user.rules; do
        if [ -f "$f" ]; then
            SUM=$(md5sum "$f" 2>/dev/null | awk '{print $1}')
            echo "    \"$f\": \"$SUM\"," >> "$output"
        fi
    done
    echo '    "_": "end"' >> "$output"
    echo '  },' >> "$output"
    
    # Timestamp
    echo "  \"timestamp\": \"$(date -Iseconds)\"" >> "$output"
    echo "}" >> "$output"
}

# --- Actions -----------------------------------------------------------------

case "$ACTION" in
    baseline)
        echo "📸 Capturing baseline..."
        capture_state "$BASELINE_FILE"
        echo "✅ Baseline saved to $BASELINE_FILE"
        echo "   Timestamp: $(date)"
        echo "   Ports: $(jq -r '.ports' "$BASELINE_FILE" 2>/dev/null)"
        echo
        echo "Next: Make your changes, then run: bash $0 validate"
        ;;
        
    validate)
        if [ ! -f "$BASELINE_FILE" ]; then
            echo "❌ No baseline found. Run 'baseline' first."
            exit 1
        fi
        
        echo "🔍 Validating against baseline..."
        CURRENT="$CANARY_DIR/current.json"
        capture_state "$CURRENT"
        
        FAILURES=0
        
        # Check SSH
        BASELINE_SSH=$(jq -r '.ssh_local' "$BASELINE_FILE")
        CURRENT_SSH=$(jq -r '.ssh_local' "$CURRENT")
        if [ "$BASELINE_SSH" = "true" ] && [ "$CURRENT_SSH" = "false" ]; then
            echo "  ❌ SSH connectivity LOST!"
            FAILURES=$((FAILURES + 1))
        else
            echo "  ✅ SSH connectivity OK"
        fi
        
        # Check ports
        BASELINE_PORTS=$(jq -r '.ports' "$BASELINE_FILE")
        CURRENT_PORTS=$(jq -r '.ports' "$CURRENT")
        if [ "$BASELINE_PORTS" != "$CURRENT_PORTS" ]; then
            echo "  ⚠️  Port changes detected:"
            echo "    Before: $BASELINE_PORTS"
            echo "    After:  $CURRENT_PORTS"
            FAILURES=$((FAILURES + 1))
        else
            echo "  ✅ Ports unchanged"
        fi
        
        # Check DNS
        BASELINE_DNS=$(jq -r '.dns' "$BASELINE_FILE")
        CURRENT_DNS=$(jq -r '.dns' "$CURRENT")
        if [ "$BASELINE_DNS" = "true" ] && [ "$CURRENT_DNS" = "false" ]; then
            echo "  ❌ DNS resolution LOST!"
            FAILURES=$((FAILURES + 1))
        else
            echo "  ✅ DNS OK"
        fi
        
        # Check services
        for svc in sshd openclaw-gateway; do
            BASELINE_SVC=$(jq -r ".services.\"$svc\"" "$BASELINE_FILE")
            CURRENT_SVC=$(jq -r ".services.\"$svc\"" "$CURRENT")
            if [ "$BASELINE_SVC" = "active" ] && [ "$CURRENT_SVC" != "active" ]; then
                echo "  ❌ Service $svc went DOWN! ($BASELINE_SVC → $CURRENT_SVC)"
                FAILURES=$((FAILURES + 1))
            else
                echo "  ✅ $svc: $CURRENT_SVC"
            fi
        done
        
        echo
        if [ $FAILURES -gt 0 ]; then
            echo "🚨 VALIDATION FAILED ($FAILURES issues)"
            echo "   Run: bash $0 rollback"
            exit 1
        else
            echo "✅ ALL CHECKS PASSED — Change is safe"
        fi
        ;;
        
    rollback)
        echo "⏪ Rolling back..."
        if [ -d "$BACKUP_DIR" ] && [ "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
            for f in "$BACKUP_DIR"/*; do
                ORIGINAL=$(cat "$f.path" 2>/dev/null || echo "")
                if [ -n "$ORIGINAL" ] && [ -f "$f" ]; then
                    sudo cp "$f" "$ORIGINAL"
                    echo "  ✅ Restored: $ORIGINAL"
                fi
            done
            echo "✅ Rollback complete. Verify with: bash $0 validate"
        else
            echo "⚠️  No backups found in $BACKUP_DIR"
            echo "   Manual recovery may be needed"
        fi
        ;;
        
    status)
        if [ -f "$BASELINE_FILE" ]; then
            echo "📋 Current baseline:"
            echo "   Created: $(jq -r '.timestamp' "$BASELINE_FILE")"
            echo "   Ports: $(jq -r '.ports' "$BASELINE_FILE")"
            echo "   Backups: $(ls "$BACKUP_DIR" 2>/dev/null | wc -l) files"
        else
            echo "No baseline captured. Run: bash $0 baseline"
        fi
        ;;
        
    *)
        echo "Usage: bash $0 {baseline|validate|rollback|status}"
        echo
        echo "  baseline  — Capture current system state"
        echo "  validate  — Compare current state to baseline"
        echo "  rollback  — Restore backed-up config files"
        echo "  status    — Show current baseline info"
        ;;
esac
