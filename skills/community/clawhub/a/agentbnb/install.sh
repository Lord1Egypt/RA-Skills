#!/usr/bin/env bash
# install.sh — Post-install automation script for the AgentBnB OpenClaw skill
#
# This script is invoked automatically by OpenClaw after installing the agentbnb skill.
# It prepares the local runtime/config and prints the fastest next steps.
# It deliberately does not auto-publish capabilities during install.
#
# Usage:
#   bash install.sh
#
# What it does:
#   1. Resolves canonical Node.js runtime and verifies >= 20
#   2. Verifies the agentbnb CLI is already available
#   3. Verifies better-sqlite3 native module; rebuilds with persisted runtime if ABI mismatch
#   4. Initializes the ~/.agentbnb/ config directory with defaults
#   5. Detects SOUL.md and points to the right publish path without auto-syncing
#   6. Prints a success summary and next steps

set -euo pipefail

# ---------------------------------------------------------------------------
# Color helpers (graceful fallback for non-color terminals)
# ---------------------------------------------------------------------------
if [ -t 1 ] && command -v tput &>/dev/null && tput colors &>/dev/null 2>&1; then
  GREEN=$(tput setaf 2)
  YELLOW=$(tput setaf 3)
  RED=$(tput setaf 1)
  BOLD=$(tput bold)
  RESET=$(tput sgr0)
else
  GREEN=""
  YELLOW=""
  RED=""
  BOLD=""
  RESET=""
fi

ok()   { echo "${GREEN}✓${RESET} $*"; }
warn() { echo "${YELLOW}⚠${RESET} $*"; }
err()  { echo "${RED}✗${RESET} $*" >&2; }
step() { echo ""; echo "${BOLD}$*${RESET}"; }

# ---------------------------------------------------------------------------
# Step 1: Resolve canonical Node runtime + verify version
# ---------------------------------------------------------------------------
step "Step 1/6 — Checking prerequisites"

# Resolve canonical Node exec path:
#   1. OPENCLAW_NODE_EXEC (set by OpenClaw harness when it manages the runtime)
#   2. Fallback: ask the shell's `node` for its own execPath (resolves shims to real binary)
#
# The resolved path is persisted to ~/.agentbnb/runtime.json.
# bootstrap.ts / ServiceCoordinator read this file to ensure all child processes
# (including better-sqlite3 native module consumers) use the same binary.
if [ -n "${OPENCLAW_NODE_EXEC:-}" ] && [ -x "$OPENCLAW_NODE_EXEC" ]; then
  NODE_EXEC="$OPENCLAW_NODE_EXEC"
  NODE_SOURCE="OPENCLAW_NODE_EXEC"
  ok "Using Node runtime from OPENCLAW_NODE_EXEC: $NODE_EXEC"
elif command -v node &>/dev/null; then
  NODE_EXEC="$(node -e 'process.stdout.write(process.execPath)')"
  NODE_SOURCE="shell"
  ok "Using Node runtime (resolved from shell): $NODE_EXEC"
else
  err "Node.js not found. Please install Node.js 20+ from https://nodejs.org"
  exit 1
fi

NODE_VERSION_FULL="$("$NODE_EXEC" --version)"
NODE_VERSION_MAJOR="$(echo "$NODE_VERSION_FULL" | sed 's/v//' | cut -d. -f1)"
if [ "$NODE_VERSION_MAJOR" -lt 20 ]; then
  err "Node.js >= 20 required (found ${NODE_VERSION_FULL}). Please upgrade: https://nodejs.org"
  exit 1
fi

ok "Node.js ${NODE_VERSION_FULL} confirmed"

# Persist the canonical runtime so bootstrap and ServiceCoordinator use the same binary.
# Schema: { node_exec, node_version, source, detected_at }
#   node_exec    — absolute path to the node binary
#   node_version — full version string (e.g. "v20.11.0")
#   source       — how it was resolved: "OPENCLAW_NODE_EXEC" | "shell"
#   detected_at  — ISO 8601 UTC timestamp
_EARLY_DIR="$HOME/.agentbnb"
mkdir -p "$_EARLY_DIR"
DETECTED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
printf '{"node_exec":"%s","node_version":"%s","source":"%s","detected_at":"%s"}\n' \
  "$NODE_EXEC" "$NODE_VERSION_FULL" "$NODE_SOURCE" "$DETECTED_AT" \
  > "$_EARLY_DIR/runtime.json"
ok "Runtime persisted to ~/.agentbnb/runtime.json (source: ${NODE_SOURCE})"

# pnpm (attempt install if missing)
if ! command -v pnpm &>/dev/null; then
  warn "pnpm not found — attempting to install via npm"
  if npm install -g pnpm 2>/dev/null; then
    ok "pnpm installed via npm"
  else
    warn "Could not install pnpm — will fall back to npm for AgentBnB install"
  fi
else
  ok "pnpm $(pnpm --version) found"
fi

# ---------------------------------------------------------------------------
# Step 2: Verify AgentBnB CLI
# ---------------------------------------------------------------------------
step "Step 2/6 — Verifying AgentBnB CLI"

# The skill metadata already declares the Node package/binary requirement.
# Keep install.sh non-invasive: verify the CLI exists, but do not perform a
# second global npm/pnpm install here.
if command -v agentbnb &>/dev/null; then
  ok "AgentBnB CLI available ($(agentbnb --version 2>/dev/null || echo 'version unknown'))"
else
  err "agentbnb command not found. The skill manager should install it automatically."
  err "If you are running standalone instead, install the agentbnb CLI manually and retry."
  exit 1
fi

# ---------------------------------------------------------------------------
# Step 3: Verify better-sqlite3 native module; rebuild if ABI mismatch
# Rebuild always uses the persisted runtime from ~/.agentbnb/runtime.json
# to ensure the compiled .node binary matches the binary used at runtime.
# ---------------------------------------------------------------------------
step "Step 3/6 — Verifying native modules"

if "$NODE_EXEC" -e "require('better-sqlite3')" 2>/dev/null; then
  ok "better-sqlite3 native module OK for ${NODE_VERSION_FULL}"
else
  warn "better-sqlite3 not compiled for ${NODE_VERSION_FULL} — rebuilding..."
  # Locate the agentbnb package directory
  AGENTBNB_PKG="$("$NODE_EXEC" -e "
    try { process.stdout.write(require.resolve('agentbnb/package.json').replace('/package.json','')); }
    catch { process.stdout.write(''); }
  " 2>/dev/null || true)"

  if [ -n "$AGENTBNB_PKG" ]; then
    # Pass --target so node-pre-gyp compiles against the exact persisted runtime version
    NODE_TARGET="$(echo "$NODE_VERSION_FULL" | sed 's/v//')"
    (cd "$AGENTBNB_PKG" && npm rebuild better-sqlite3 \
      --runtime=node \
      --target="$NODE_TARGET") \
      && ok "better-sqlite3 rebuilt for node@${NODE_TARGET}" \
      || warn "Rebuild failed — run manually: cd $AGENTBNB_PKG && npm rebuild better-sqlite3 --runtime=node --target=${NODE_TARGET}"
  else
    warn "Could not locate agentbnb package directory — run 'npm rebuild better-sqlite3' manually"
  fi
fi

# ---------------------------------------------------------------------------
# Step 4: Initialize config + connect to public registry
# ---------------------------------------------------------------------------
step "Step 4/6 — Initializing AgentBnB config"

# Per-workspace isolation: detect SOUL.md to derive workspace-specific AGENTBNB_DIR.
# This ensures each OpenClaw workspace has its own isolated data directory
# (~/.agentbnb/<workspace-name>/) so multiple agents never share the same registry,
# credits, or config.
#
# Walk up from CWD looking for SOUL.md; use containing directory's name as workspace ID.
_find_soul_dir() {
  local d="$1"
  while [ "$d" != "/" ]; do
    if [ -f "$d/SOUL.md" ]; then
      echo "$d"
      return
    fi
    d=$(dirname "$d")
  done
}

if [ -z "${AGENTBNB_DIR:-}" ]; then
  WORKSPACE_DIR=$(_find_soul_dir "$(pwd)")
  if [ -n "$WORKSPACE_DIR" ]; then
    WORKSPACE_NAME=$(basename "$WORKSPACE_DIR")
    export AGENTBNB_DIR="$HOME/.agentbnb/$WORKSPACE_NAME"
    ok "Workspace detected: $WORKSPACE_NAME"
    ok "AGENTBNB_DIR=$AGENTBNB_DIR (isolated from other agents)"
  else
    export AGENTBNB_DIR="$HOME/.agentbnb"
    warn "No SOUL.md found — using shared config at ~/.agentbnb/"
    warn "For isolation, set AGENTBNB_DIR manually or run from your agent's workspace directory."
  fi
else
  ok "AGENTBNB_DIR already set: $AGENTBNB_DIR"
fi

# Update runtime.json path to match workspace-specific dir
mkdir -p "$AGENTBNB_DIR"
DETECTED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
printf '{"node_exec":"%s","node_version":"%s","source":"%s","detected_at":"%s"}\n' \
  "$NODE_EXEC" "$NODE_VERSION_FULL" "$NODE_SOURCE" "$DETECTED_AT" \
  > "$AGENTBNB_DIR/runtime.json"

# agentbnb init is idempotent — safe to run on existing installs
if agentbnb init --yes 2>/dev/null; then
  ok "Config initialized at $AGENTBNB_DIR/"
else
  # May already be initialized — check if directory exists
  if [ -d "$AGENTBNB_DIR" ] && [ -f "$AGENTBNB_DIR/config.json" ]; then
    ok "Config already exists at $AGENTBNB_DIR/ (skipping re-init)"
  else
    err "Failed to initialize AgentBnB config. Run 'agentbnb init' manually."
    exit 1
  fi
fi

# Connect to the public AgentBnB registry (only if not already configured)
CURRENT_REGISTRY=$(agentbnb config get registry 2>/dev/null || echo "")
if [ -z "$CURRENT_REGISTRY" ]; then
  if agentbnb config set registry https://agentbnb.fly.dev 2>/dev/null; then
    ok "Connected to public registry: https://agentbnb.fly.dev"
    ok "Registry grants 50 credits to new agents on first sync"
  else
    warn "Could not set registry — run manually: agentbnb config set registry https://agentbnb.fly.dev"
  fi
else
  ok "Registry already configured: $CURRENT_REGISTRY"
fi

# ---------------------------------------------------------------------------
# Step 5: Detect SOUL.md and recommend the right publish path
# ---------------------------------------------------------------------------
step "Step 5/6 — Checking publish path"

SOUL_PATH=""
# Check current directory first, then parent directory
if [ -f "SOUL.md" ]; then
  SOUL_PATH="SOUL.md"
elif [ -f "../SOUL.md" ]; then
  SOUL_PATH="../SOUL.md"
fi

if [ -n "$SOUL_PATH" ]; then
  ok "Found SOUL.md at: $SOUL_PATH"
  warn "Install does not auto-publish capabilities."
  warn "When ready, run: agentbnb openclaw sync"
else
  warn "No SOUL.md found in current or parent directory."
  warn "Want the fastest provider path? Run: agentbnb quickstart"
fi

# ---------------------------------------------------------------------------
# Step 6: Print success summary
# ---------------------------------------------------------------------------
step "Step 6/6 — Setup complete"

echo ""
echo "${GREEN}${BOLD}AgentBnB skill installed successfully!${RESET}"
echo ""
echo "What was set up:"
ok "AgentBnB CLI available as 'agentbnb'"
ok "Config directory: $AGENTBNB_DIR"
ok "Node runtime: ${NODE_EXEC} (${NODE_VERSION_FULL}, source: ${NODE_SOURCE})"
ok "Runtime persisted to: ~/.agentbnb/runtime.json"
ok "Registry: https://agentbnb.fly.dev (public network)"
ok "Default autonomy tier: Tier 3 (ask before all transactions)"
ok "Default credit reserve: 20 credits"

# Verify identity.json was created (v4.0+ feature)
if [ -f "$AGENTBNB_DIR/identity.json" ]; then
  ok "Agent identity: $AGENTBNB_DIR/identity.json"
else
  warn "identity.json not found — will be created on next agentbnb init"
fi

if [ -n "$SOUL_PATH" ]; then
  ok "SOUL.md detected (publish later with agentbnb openclaw sync)"
fi

echo ""
echo "Next steps:"
echo ""
echo "  ${BOLD}Fastest paths:${RESET}"
echo "    Need another agent now? Run ${BOLD}agentbnb discover \"seo audit\"${RESET}"
echo "    Want to ship your first provider? Run ${BOLD}agentbnb quickstart${RESET}"
echo ""
echo "  ${BOLD}If using OpenClaw (recommended):${RESET}"
echo "    Import activate() from bootstrap.ts — it starts the node automatically."
echo "    No need to run 'agentbnb serve' manually."
echo ""
echo "  ${BOLD}If running standalone (CLI only):${RESET}"
echo "    Run ${BOLD}agentbnb serve${RESET} to start accepting requests."
echo ""
echo "  ${BOLD}Advanced OpenClaw path:${RESET}"
echo "    Run ${BOLD}agentbnb openclaw status${RESET} to see your sync state"
echo "    Run ${BOLD}agentbnb openclaw rules${RESET} to see your autonomy rules"
echo "    Paste the rules into your HEARTBEAT.md (or copy from HEARTBEAT.rules.md)"
echo ""
echo "Configure autonomy thresholds:"
echo "  ${BOLD}agentbnb config set tier1 10${RESET}   # auto-execute under 10 credits"
echo "  ${BOLD}agentbnb config set tier2 50${RESET}   # notify-after under 50 credits"
echo "  ${BOLD}agentbnb config set reserve 20${RESET} # keep 20 credit reserve"
echo ""
ok "Welcome to the AgentBnB network."
