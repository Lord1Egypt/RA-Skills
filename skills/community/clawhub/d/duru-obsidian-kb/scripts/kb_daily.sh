#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$SKILL_ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$SKILL_ROOT/.env"
  set +a
fi

WORKSPACE_DEFAULT="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
CONFIG_DEFAULT="${KB_CONFIG_PATH:-$WORKSPACE_DEFAULT/knowledge-bases/config/repos.json}"
PYTHON_DEFAULT="${KB_PYTHON:-python3}"
VENV_PY="${KB_VENV_PYTHON:-$WORKSPACE_DEFAULT/.venvs/duru-kb/bin/python}"

if [[ -x "$VENV_PY" ]]; then
  PYTHON_DEFAULT="$VENV_PY"
fi

usage() {
  cat <<'EOF'
kb_daily.sh - Minimal daily ops wrapper for duru-obsidian-kb

Usage:
  kb_daily.sh add   --source <url|file> [--repo <name>] [--type <article|paper|repo|spreadsheet|file>] [--title <title>] [--tags <a,b>] [--notes <text>] [--no-build] [--no-summarize]
  kb_daily.sh ask   --question <text> [--repo <name>] [--root <kb-root>] [--format <md|marp>] [--top-k <n>] [--file-back] [--target-concept <slug>]
  kb_daily.sh check [--repo <name>]

Optional globals:
  --config <path>   (default: knowledge-bases/config/repos.json)
  --python <path>   (default: venv python if available, else python3)

Examples:
  kb_daily.sh add --source "https://arxiv.org/abs/2602.12430" --tags "ai,llm,agent"
  kb_daily.sh ask --question "MCP agent security tradeoffs" --repo ai-research --top-k 8
  kb_daily.sh check
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1"; exit 1; }
}

resolve_repo_root() {
  local config="$1"
  local repo_name="$2"
  "$PYTHON_DEFAULT" - <<PY
import json
from pathlib import Path
cfg=Path(${config@Q})
if not cfg.exists():
    raise SystemExit(f"config not found: {cfg}")
data=json.loads(cfg.read_text(encoding='utf-8'))
repos=data.get('repos',[])
name=${repo_name@Q}
if not name:
    name=data.get('routing',{}).get('default_repo')
repo=next((r for r in repos if r.get('name')==name), None)
if not repo:
    raise SystemExit(f"repo not found: {name}")
print(repo.get('root',''))
PY
}

main() {
  if [[ $# -lt 1 ]]; then
    usage
    exit 1
  fi

  if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    usage
    exit 0
  fi

  local cmd="$1"; shift
  local config="$CONFIG_DEFAULT"

  # parse global flags only when placed before subcommand args
  local -a remaining=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --config)
        config="$2"; shift 2 ;;
      --python)
        PYTHON_DEFAULT="$2"; shift 2 ;;
      -h|--help)
        usage; exit 0 ;;
      *)
        remaining+=("$1"); shift ;;
    esac
  done

  if [[ ${#remaining[@]} -gt 0 ]]; then
    set -- "${remaining[@]}"
  else
    set --
  fi

  case "$cmd" in
    add)
      require_cmd "$PYTHON_DEFAULT"
      "$PYTHON_DEFAULT" "$SCRIPT_DIR/kb_add.py" --config "$config" "$@"
      ;;
    ask)
      require_cmd "$PYTHON_DEFAULT"
      local repo=""
      local root=""
      local pass=()
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --repo)
            repo="$2"; shift 2 ;;
          --root)
            root="$2"; shift 2 ;;
          *)
            pass+=("$1"); shift ;;
        esac
      done
      if [[ -z "$root" ]]; then
        root="$(resolve_repo_root "$config" "$repo")"
      fi
      "$PYTHON_DEFAULT" "$SCRIPT_DIR/kb_ask.py" --root "$root" "${pass[@]}"
      ;;
    check)
      require_cmd "$PYTHON_DEFAULT"
      "$PYTHON_DEFAULT" "$SCRIPT_DIR/kb_healthcheck.py" --config "$config" "$@"
      ;;
    *)
      echo "Unknown command: $cmd"
      usage
      exit 1
      ;;
  esac
}

main "$@"
