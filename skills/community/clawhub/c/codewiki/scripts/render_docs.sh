#!/usr/bin/env bash
# render_docs.sh
# ===============
#
# Unified entry point for rendering a Markdown documentation collection
# into static MkDocs and/or VitePress sites with Mermaid diagram support.
#
# Why this script exists:
#   The underlying Python (render_mkdocs.py) and Node (render_vitepress.mjs)
#   renderers are *already self-contained* — each one creates its own
#   isolated sandbox (Python venv / private node_modules) and installs
#   its dependencies from the Aliyun mirror at run time. The user never
#   needs to `pip install` or `npm install` anything by hand.
#
#   This wrapper exists purely to:
#     1. Verify the host has python3 / node available (with a friendly
#        message pointing at how to install them if missing).
#     2. Dispatch to one or both renderers with a single consistent CLI.
#     3. Capture per-stack exit codes and report a clean summary.
#
# Usage:
#   ./render_docs.sh --src <markdown_dir> [options]
#
# Required:
#   -s, --src <path>           Source directory containing *.md files.
#
# Optional:
#   --mkdocs-out <path>         Output directory for the MkDocs site.
#                               Default: <repo_root>/mkdocs
#   --vitepress-out <path>      Output directory for the VitePress site.
#                               Default: <repo_root>/vitepress
#   --stack <mkdocs|vitepress|both>
#                               Which renderer(s) to invoke. Default: both
#   --force                     Overwrite existing output directories.
#   --clean-sandbox             Re-create venv / node_modules before build.
#   -h, --help                  Show this help message.
#
# Example:
#   ./scripts/render_docs/render_docs.sh \
#       --src wiki \
#       --mkdocs-out ./mkdocs \
#       --vitepress-out ./vitepress \
#       --force
#
# Exit codes:
#   0  all requested renderers succeeded
#   1  invalid arguments / missing host tool
#   2  MkDocs render failed
#   3  VitePress render failed
#   4  both renderers failed

set -euo pipefail

# -----------------------------------------------------------------------------
# Locate the directory that holds render_mkdocs.py and render_vitepress.mjs.
# This makes the script invokable from anywhere — we resolve the script's own
# path rather than relying on the caller's CWD.
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
MKDOCS_SCRIPT="${SCRIPT_DIR}/render_mkdocs.py"
VITEPRESS_SCRIPT="${SCRIPT_DIR}/render_vitepress.mjs"

# -----------------------------------------------------------------------------
# Defaults — the caller can override via flags.
# -----------------------------------------------------------------------------
# Repo root = two levels up from this script (scripts/render_docs/ -> repo).
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SRC=""
MKDOCS_OUT="${REPO_ROOT}/mkdocs"
VITEPRESS_OUT="${REPO_ROOT}/vitepress"
STACK="both"
FORCE=0
CLEAN_SANDBOX=0
SERVE=0
SERVE_PORT=8000

# -----------------------------------------------------------------------------
# Logging helpers. Tagged prefixes make it easy to grep build logs.
# -----------------------------------------------------------------------------
log()  { printf '[render_docs] %s\n' "$*"; }
err()  { printf '[render_docs] ERROR: %s\n' "$*" >&2; }
die()  { err "$1"; exit "${2:-1}"; }

# -----------------------------------------------------------------------------
# Help text — mirrors the script header so it stays authoritative.
# -----------------------------------------------------------------------------
print_help() {
  cat <<'EOF'
render_docs.sh — Unified MkDocs + VitePress markdown renderer.

USAGE
  ./render_docs.sh --src <markdown_dir> [options]

REQUIRED
  -s, --src <path>             Source directory containing *.md files.

OPTIONAL
  --mkdocs-out <path>          Output directory for MkDocs site.
                               Default: <repo_root>/mkdocs
  --vitepress-out <path>       Output directory for VitePress site.
                               Default: <repo_root>/vitepress
  --stack <mkdocs|vitepress|both>
                               Which renderer(s) to invoke. Default: both
  --force                      Overwrite existing output directories.
  --clean-sandbox              Re-create venv / node_modules before build.
  --serve [PORT]               After a successful build, start a static HTTP
                               server (python3 -m http.server) on the built
                               site(s). Default port is 8000; pass an integer
                               to override. When --stack=both, MkDocs is
                               served on PORT and VitePress on PORT+1. Use
                               Ctrl-C to stop the server(s).
  -h, --help                   Show this help message.

EXAMPLE
  ./scripts/render_docs/render_docs.sh \
      --src wiki \
      --force

HOST REQUIREMENTS
  python3 (>=3.9)    https://www.python.org/downloads/
  node    (>=18)     https://nodejs.org/

  No manual pip / npm installs are needed — each renderer creates its own
  isolated sandbox (venv / node_modules) and installs from the Aliyun mirror.

EXIT CODES
  0  all requested renderers succeeded
  1  invalid arguments / missing host tool
  2  MkDocs render failed
  3  VitePress render failed
  4  both renderers failed
EOF
}

# -----------------------------------------------------------------------------
# Parse CLI arguments. Hand-rolled parsing (instead of getopts) lets us
# support long flags and helpful error messages without bringing in any
# external dependency.
# -----------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      print_help
      exit 0
      ;;
    -s|--src)
      SRC="$2"; shift 2
      ;;
    --mkdocs-out)
      MKDOCS_OUT="$2"; shift 2
      ;;
    --vitepress-out)
      VITEPRESS_OUT="$2"; shift 2
      ;;
    --stack)
      STACK="$2"; shift 2
      ;;
    --force)
      FORCE=1; shift
      ;;
    --clean-sandbox)
      CLEAN_SANDBOX=1; shift
      ;;
    --serve)
      SERVE=1
      # Optional next token may be a port number. Peek without consuming —
      # if it isn't a number we leave it for the next loop iteration.
      if [[ "${2:-}" =~ ^[0-9]+$ ]]; then
        SERVE_PORT="$2"; shift 2
      else
        shift
      fi
      ;;
    *)
      die "Unknown argument: $1 (pass -h for usage)" 1
      ;;
  esac
done

# -----------------------------------------------------------------------------
# Validate required arguments before doing any work.
# -----------------------------------------------------------------------------
if [[ -z "$SRC" ]]; then
  print_help
  die "Missing required argument: --src" 1
fi
case "$STACK" in
  mkdocs|vitepress|both) ;;
  *) die "Invalid --stack '$STACK'. Use mkdocs, vitepress, or both." 1 ;;
esac

# -----------------------------------------------------------------------------
# Host tool check. We need python3 for MkDocs and node for VitePress. Only
# the tools we will actually invoke are required, so missing-stack tools
# are silently tolerated when --stack excludes them.
# -----------------------------------------------------------------------------
if [[ "$STACK" == "mkdocs" || "$STACK" == "both" ]]; then
  command -v python3 >/dev/null 2>&1 || die \
    "python3 not found on PATH. Install Python >= 3.9 from https://www.python.org/downloads/" 1
  PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  log "Found python3 ${PYTHON_VERSION} at $(command -v python3)"
fi
if [[ "$STACK" == "vitepress" || "$STACK" == "both" ]]; then
  command -v node >/dev/null 2>&1 || die \
    "node not found on PATH. Install Node.js >= 18 from https://nodejs.org/" 1
  command -v npm >/dev/null 2>&1 || die \
    "npm not found on PATH. It ships with Node.js — reinstall from https://nodejs.org/" 1
  log "Found node $(node -v) at $(command -v node)"
fi

# -----------------------------------------------------------------------------
# Resolve source to an absolute path so the renderer scripts (which may use
# a different CWD) see a stable input.
# -----------------------------------------------------------------------------
SRC="$(cd "$SRC" 2>/dev/null && pwd)" || die "Source directory not found: $SRC" 1

# -----------------------------------------------------------------------------
# Build the shared flags. --force is appended only if requested so that
# re-runs against an existing output directory fail loudly by default
# (catches accidental overwrites).
# -----------------------------------------------------------------------------
SHARED_FLAGS=("--src" "$SRC")
(( FORCE )) && SHARED_FLAGS+=("--force")
(( CLEAN_SANDBOX )) && SHARED_FLAGS+=("--clean-venv")

# Track per-stack outcomes so we can produce a clean summary at the end.
MKDOCS_RC=0
VITEPRESS_RC=0

# -----------------------------------------------------------------------------
# Dispatchers. Each block delegates to the renderer script, then records
# the resulting exit code without aborting (so the other stack still runs).
# -----------------------------------------------------------------------------
run_mkdocs() {
  log "==== MkDocs ===="
  local flags=("${SHARED_FLAGS[@]}" "--out" "$MKDOCS_OUT")
  # --clean-venv (Python) and --clean-node (Node) are different flags, so
  # translate the shared --clean-sandbox into each script's native form.
  if (( CLEAN_SANDBOX )); then
    flags+=("--clean-venv")
  fi
  if python3 "$MKDOCS_SCRIPT" "${flags[@]}"; then
    log "MkDocs OK  → $MKDOCS_OUT/site/index.html"
  else
    MKDOCS_RC=$?
    err "MkDocs render failed (exit=$MKDOCS_RC)"
  fi
}

run_vitepress() {
  log "==== VitePress ===="
  local flags=("${SHARED_FLAGS[@]}" "--out" "$VITEPRESS_OUT")
  if (( CLEAN_SANDBOX )); then
    flags+=("--clean-node")
  fi
  # The shared flags may contain --clean-venv (translated above); strip
  # it before forwarding because the Node script only knows --clean-node.
  local filtered=()
  for f in "${flags[@]}"; do
    [[ "$f" == "--clean-venv" ]] && continue
    filtered+=("$f")
  done
  if node "$VITEPRESS_SCRIPT" "${filtered[@]}"; then
    log "VitePress OK  → $VITEPRESS_OUT/site/index.html"
  else
    VITEPRESS_RC=$?
    err "VitePress render failed (exit=$VITEPRESS_RC)"
  fi
}

# -----------------------------------------------------------------------------
# Run the requested stacks in order. We don't parallelize because both
# renderers write to disk simultaneously and the npm/pip network traffic
# would contend for bandwidth on the Aliyun mirror.
# -----------------------------------------------------------------------------
case "$STACK" in
  mkdocs)    run_mkdocs ;;
  vitepress) run_vitepress ;;
  both)      run_mkdocs; run_vitepress ;;
esac

# -----------------------------------------------------------------------------
# Final summary. The composite exit code lets CI decide whether to gate.
# -----------------------------------------------------------------------------
log "==== Summary ===="
[[ "$STACK" == "mkdocs" || "$STACK" == "both" ]] \
  && log "  mkdocs    : $([ $MKDOCS_RC -eq 0 ] && echo OK || echo FAIL)"
[[ "$STACK" == "vitepress" || "$STACK" == "both" ]] \
  && log "  vitepress : $([ $VITEPRESS_RC -eq 0 ] && echo OK || echo FAIL)"

# -----------------------------------------------------------------------------
# Optional static-server step. Only triggered by --serve. The server(s)
# run in the foreground; Ctrl-C terminates the script and all children.
#
# Why this exists: VitePress is a client-side SPA whose in-page search,
# localStorage-backed dark-mode toggle, and SPA-style navigation only work
# under an HTTP origin. MkDocs is fully self-contained HTML and works via
# file://, but serving it over HTTP is still convenient for previewing.
# -----------------------------------------------------------------------------
SERVE_PIDS=()

cleanup_serve() {
  [[ "${#SERVE_PIDS[@]}" -eq 0 ]] && return 0
  log "Stopping preview server(s)..."
  for pid in "${SERVE_PIDS[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
}

if (( SERVE )); then
  # Build the list of (label, dir, port) tuples to serve. Only sites that
  # were actually built and produced a site/index.html are considered.
  declare -a SERVE_TARGETS=()
  port="$SERVE_PORT"

  if [[ "$STACK" == "mkdocs" || "$STACK" == "both" ]] && (( MKDOCS_RC == 0 )) \
     && [[ -f "$MKDOCS_OUT/site/index.html" ]]; then
    SERVE_TARGETS+=("mkdocs|$(cd "$MKDOCS_OUT/site" && pwd)|$port")
    port=$((port + 1))
  fi
  if [[ "$STACK" == "vitepress" || "$STACK" == "both" ]] && (( VITEPRESS_RC == 0 )) \
     && [[ -f "$VITEPRESS_OUT/site/index.html" ]]; then
    SERVE_TARGETS+=("vitepress|$(cd "$VITEPRESS_OUT/site" && pwd)|$port")
    port=$((port + 1))
  fi

  if [[ "${#SERVE_TARGETS[@]}" -eq 0 ]]; then
    err "--serve requested but no successful build output was found. Nothing to serve."
  else
    trap cleanup_serve EXIT INT TERM
    log "==== Preview (Ctrl-C to stop) ===="
    for tuple in "${SERVE_TARGETS[@]}"; do
      IFS='|' read -r label dir tport <<<"$tuple"
      log "  $label → http://localhost:$tport  (serving $dir)"
      # Run each server detached so its logs don't interleave with ours.
      ( cd "$dir" && exec python3 -m http.server "$tport" --bind 127.0.0.1 \
          >/tmp/render_docs_${label}.log 2>&1 ) &
      SERVE_PIDS+=("$!")
    done
    log "Open any URL above in your browser. Press Ctrl-C to stop the server(s)."
    # Block until the user interrupts. `wait` without args waits for all
    # backgrounded children; when the user hits Ctrl-C the trap fires and
    # cleanup_serve() kills the children before the script exits.
    wait
  fi
fi

if (( MKDOCS_RC == 0 && VITEPRESS_RC == 0 )); then
  exit 0
elif (( MKDOCS_RC != 0 && VITEPRESS_RC != 0 )); then
  exit 4
elif (( MKDOCS_RC != 0 )); then
  exit 2
else
  exit 3
fi
