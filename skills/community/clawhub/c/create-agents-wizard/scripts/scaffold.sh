#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scaffold.sh --agent <id> --workspace <path> [--from <dir>] [--force]

What it does:
  1) Ensure workspace directory exists
  2) Ensure 6 core files exist:
     AGENTS.md SOUL.md IDENTITY.md BOOTSTRAP.md USER.md STYLE.md
  3) Optionally copy approved drafts from --from directory

Options:
  --agent <id>        Agent id (for display/log only)
  --workspace <path>  Target workspace path
  --from <dir>        Source dir containing any of the 6 files to copy
  --force             Overwrite existing files when copying from --from
  -h, --help          Show this help
EOF
}

AGENT_ID=""
WORKSPACE=""
FROM_DIR=""
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)
      AGENT_ID="${2:-}"
      shift 2
      ;;
    --workspace)
      WORKSPACE="${2:-}"
      shift 2
      ;;
    --from)
      FROM_DIR="${2:-}"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$AGENT_ID" || -z "$WORKSPACE" ]]; then
  echo "Error: --agent and --workspace are required." >&2
  usage >&2
  exit 2
fi

if [[ -n "$FROM_DIR" && ! -d "$FROM_DIR" ]]; then
  echo "Error: --from directory not found: $FROM_DIR" >&2
  exit 2
fi

mkdir -p "$WORKSPACE"

files=(AGENTS.md SOUL.md IDENTITY.md BOOTSTRAP.md USER.md STYLE.md)

for f in "${files[@]}"; do
  target="$WORKSPACE/$f"

  if [[ -n "$FROM_DIR" && -f "$FROM_DIR/$f" ]]; then
    if [[ -f "$target" && "$FORCE" -ne 1 ]]; then
      echo "skip  $target (exists; use --force to overwrite)"
    else
      cp "$FROM_DIR/$f" "$target"
      echo "write $target (copied from $FROM_DIR/$f)"
    fi
  else
    if [[ ! -f "$target" ]]; then
      cat > "$target" <<EOF
# $f

<!-- TODO: fill content for agent: $AGENT_ID -->
EOF
      echo "write $target (placeholder created)"
    else
      echo "keep  $target"
    fi
  fi
done

echo
echo "Done. Agent: $AGENT_ID"
echo "Workspace: $WORKSPACE"
