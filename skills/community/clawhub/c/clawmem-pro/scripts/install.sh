#!/bin/bash
# OpenClaw Memory System — Installation Script (Unix/Linux/macOS)
# Run this to set up the complete memory architecture in your workspace

set -euo pipefail

# Parse arguments first
WORKSPACE_PATH="."
SKIP_TEMPLATES=false
DRY_RUN=false

for arg in "$@"; do
    case $arg in
        --skip-templates) SKIP_TEMPLATES=true ;;
        --dry-run) DRY_RUN=true ;;
        --*) echo "Unknown option: $arg"; exit 1 ;;
        *) WORKSPACE_PATH="$arg" ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

info() { echo -e "\033[36m[INFO]\033[0m $1"; }
ok()   { echo -e "\033[32m[OK]\033[0m $1"; }
warn() { echo -e "\033[33m[WARN]\033[0m $1"; }
err()  { echo -e "\033[31m[ERR]\033[0m $1"; }

info "OpenClaw Memory System Installer v1.0.0"
info "Workspace: $(cd "$WORKSPACE_PATH" && pwd)"

# Resolve paths
WORKSPACE="$(cd "$WORKSPACE_PATH" && pwd)"
MEMORY_DIR="$WORKSPACE/memory"
DIARY_DIR="$MEMORY_DIR/diary"
DREAMS_DIR="$MEMORY_DIR/dreams"
TEMPLATES_DIR="$SKILL_ROOT/templates"

# Step 1: Create directory structure
info "Creating directory structure..."
for dir in "$MEMORY_DIR" "$DIARY_DIR" "$DREAMS_DIR"; do
    if [ ! -d "$dir" ]; then
        if [ "$DRY_RUN" = false ]; then
            mkdir -p "$dir"
        fi
        ok "Created: $dir"
    else
        warn "Already exists: $dir"
    fi
done

# Step 2: Copy templates (using parallel arrays for macOS bash 3.2 compatibility)
ALL_GOOD=true
if [ "$SKIP_TEMPLATES" = false ]; then
    info "Installing templates..."

    # Template sources and destinations (parallel arrays)
    TEMPLATE_NAMES=(
        "MEMORY.md"
        "HEARTBEAT.md"
        "cron-inbox.md"
        "heartbeat-state.json"
        "platform-posts.md"
        "strategy-notes.md"
    )
    TEMPLATE_DESTS=(
        "$WORKSPACE/MEMORY.md"
        "$WORKSPACE/HEARTBEAT.md"
        "$MEMORY_DIR/cron-inbox.md"
        "$MEMORY_DIR/heartbeat-state.json"
        "$MEMORY_DIR/platform-posts.md"
        "$MEMORY_DIR/strategy-notes.md"
    )

    for i in "${!TEMPLATE_NAMES[@]}"; do
        src_name="${TEMPLATE_NAMES[$i]}"
        src_path="$TEMPLATES_DIR/$src_name"
        dst_path="${TEMPLATE_DESTS[$i]}"
        if [ -f "$src_path" ]; then
            if [ ! -f "$dst_path" ]; then
                if [ "$DRY_RUN" = false ]; then
                    cp "$src_path" "$dst_path"
                fi
                ok "Installed: $dst_path"
            else
                warn "Skipped (already exists): $dst_path"
            fi
        else
            err "Template missing: $src_path"
            ALL_GOOD=false
        fi
    done
else
    warn "Skipping template installation (--skip-templates)"
fi

# Step 3: Create today's daily notes file
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$MEMORY_DIR/$TODAY.md"
if [ ! -f "$TODAY_FILE" ]; then
    DAILY_TEMPLATE="$TEMPLATES_DIR/daily-notes.md"
    if [ -f "$DAILY_TEMPLATE" ]; then
        if [ "$DRY_RUN" = false ]; then
            sed "s/YYYY-MM-DD/$TODAY/g" "$DAILY_TEMPLATE" > "$TODAY_FILE"
        fi
        ok "Created daily notes: $TODAY_FILE"
    else
        if [ "$DRY_RUN" = false ]; then
            echo "# $TODAY — Daily Notes" > "$TODAY_FILE"
        fi
        ok "Created minimal daily notes: $TODAY_FILE"
    fi
fi

# Step 4: Validate installation
info "Validating installation..."

if [ "$DRY_RUN" = true ]; then
    ok "Dry run mode — validation skipped (files would be created in normal mode)"
    ALL_GOOD=true
else
    REQUIRED_FILES=(
        "$WORKSPACE/MEMORY.md"
        "$WORKSPACE/HEARTBEAT.md"
        "$MEMORY_DIR/cron-inbox.md"
        "$MEMORY_DIR/heartbeat-state.json"
    )
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            ok "OK: $file"
        else
            err "MISSING: $file"
            ALL_GOOD=false
        fi
    done
fi

# Step 5: Print next steps
echo ""
ok "Installation complete!"
echo ""
echo -e "\033[33mNext steps:\033[0m"
echo "1. Edit MEMORY.md with your personal context and preferences"
echo "2. Edit HEARTBEAT.md to customize your periodic routines"
echo "3. Add these lines to your AGENTS.md or session startup:"
echo ""
echo -e "\033[36m   ## Every Session\033[0m"
echo -e "\033[36m   1. Read MEMORY.md -- who you are\033[0m"
echo -e "\033[36m   2. Read memory/YYYY-MM-DD.md (today + yesterday) -- recent context\033[0m"
echo -e "\033[36m   3. Check memory/cron-inbox.md -- messages from other sessions\033[0m"
echo ""
echo "4. Set up cron jobs (see scripts/setup-cron.sh)"
echo ""

if [ "$DRY_RUN" = true ]; then
    warn "This was a dry run. No files were actually created."
fi

if [ "$ALL_GOOD" = true ]; then
    exit 0
else
    echo ""
    err "Installation completed with errors. Some files are missing."
    exit 1
fi
