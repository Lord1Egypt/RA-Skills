#!/bin/bash

resolve_workspace() {
    local skill_dir="$1"
    local candidate

    if [ -n "${OPENCLAW_WORKSPACE:-}" ] && [ -d "$OPENCLAW_WORKSPACE" ]; then
        (cd "$OPENCLAW_WORKSPACE" && pwd)
        return 0
    fi

    for candidate in "$skill_dir/.." "$skill_dir/../.." "$PWD"; do
        if [ -d "$candidate" ]; then
            candidate="$(cd "$candidate" && pwd)"
            if [ -f "$candidate/AGENTS.md" ] || [ -f "$candidate/HEARTBEAT.md" ] || [ -f "$candidate/MEMORY.md" ] || [ -d "$candidate/reports" ] || [ -d "$candidate/skills" ]; then
                printf '%s\n' "$candidate"
                return 0
            fi
        fi
    done

    (cd "$skill_dir/.." && pwd)
}

resolve_peer_skill_dir() {
    local workspace="$1"
    local current_skill_dir="$2"
    local slug="$3"
    local parent
    local candidate

    parent="$(cd "$current_skill_dir/.." && pwd)"

    for candidate in \
        "$workspace/$slug" \
        "$workspace/skills/$slug" \
        "$parent/$slug" \
        "$parent/skills/$slug"; do
        if [ -d "$candidate" ]; then
            (cd "$candidate" && pwd)
            return 0
        fi
    done

    printf '%s\n' "$workspace/skills/$slug"
}
