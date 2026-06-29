#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  codex-delegate.sh --prompt TEXT [options]
  command | codex-delegate.sh --prompt TEXT [options]

Options:
  --cwd PATH                  Run Codex from PATH. Default: current directory.
  --prompt TEXT               Task prompt to send to Codex.
  --prompt-file PATH          Read the task prompt from PATH.
  --stdin-file PATH           Read additional context from PATH and pipe it to Codex.
  --sandbox MODE              read-only, workspace-write, or danger-full-access.
                              Default: read-only.
  --json-log PATH             Capture Codex JSONL events to PATH and print final answer.
  --output PATH               Write Codex final message to PATH.
  --ephemeral                 Do not persist Codex session rollout files.
  --skip-git-repo-check       Allow running outside a git repository.
  -h, --help                  Show this help.

The wrapper intentionally clears OPENAI_API_KEY and CODEX_API_KEY before running
codex exec so it uses saved Codex CLI authentication instead of an inline API key.
USAGE
}

cwd="."
prompt=""
prompt_file=""
stdin_file=""
sandbox="read-only"
json_log=""
output_file=""
ephemeral=false
skip_git_repo_check=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cwd)
      cwd="${2:?--cwd requires a path}"
      shift 2
      ;;
    --prompt)
      prompt="${2:?--prompt requires text}"
      shift 2
      ;;
    --prompt-file)
      prompt_file="${2:?--prompt-file requires a path}"
      shift 2
      ;;
    --stdin-file)
      stdin_file="${2:?--stdin-file requires a path}"
      shift 2
      ;;
    --sandbox)
      sandbox="${2:?--sandbox requires a mode}"
      shift 2
      ;;
    --json-log)
      json_log="${2:?--json-log requires a path}"
      shift 2
      ;;
    --output)
      output_file="${2:?--output requires a path}"
      shift 2
      ;;
    --ephemeral)
      ephemeral=true
      shift
      ;;
    --skip-git-repo-check)
      skip_git_repo_check=true
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

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found on PATH. Install Codex CLI and authenticate with ChatGPT sign-in." >&2
  exit 127
fi

case "$sandbox" in
  read-only|workspace-write|danger-full-access) ;;
  *)
    echo "--sandbox must be read-only, workspace-write, or danger-full-access" >&2
    exit 2
    ;;
esac

if [[ -n "$prompt_file" ]]; then
  if [[ -n "$prompt" ]]; then
    echo "Use either --prompt or --prompt-file, not both." >&2
    exit 2
  fi
  prompt="$(<"$prompt_file")"
fi

if [[ -z "$prompt" && -z "$stdin_file" && -t 0 ]]; then
  echo "Provide --prompt, --prompt-file, --stdin-file, or pipe a full prompt on stdin." >&2
  usage >&2
  exit 2
fi

if [[ ! -d "$cwd" ]]; then
  echo "--cwd does not exist or is not a directory: $cwd" >&2
  exit 2
fi

cmd=(codex exec --sandbox "$sandbox")

if [[ "$ephemeral" == true ]]; then
  cmd+=(--ephemeral)
fi

if [[ "$skip_git_repo_check" == true ]]; then
  cmd+=(--skip-git-repo-check)
fi

tmp_dir=""
if [[ -n "$json_log" ]]; then
  cmd+=(--json)
  mkdir -p "$(dirname "$json_log")"
fi

if [[ -z "$output_file" && -n "$json_log" ]]; then
  tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-codex.XXXXXX")"
  output_file="$tmp_dir/final.md"
fi

if [[ -n "$output_file" ]]; then
  mkdir -p "$(dirname "$output_file")"
  cmd+=(-o "$output_file")
fi

# Force saved Codex CLI auth instead of inline API-key authentication.
unset OPENAI_API_KEY
unset CODEX_API_KEY

run_codex() {
  if [[ -n "$stdin_file" ]]; then
    if [[ -n "$prompt" ]]; then
      "${cmd[@]}" "$prompt" <"$stdin_file"
    else
      "${cmd[@]}" - <"$stdin_file"
    fi
  elif [[ ! -t 0 ]]; then
    if [[ -n "$prompt" ]]; then
      "${cmd[@]}" "$prompt"
    else
      "${cmd[@]}" -
    fi
  else
    "${cmd[@]}" "$prompt"
  fi
}

if [[ -n "$json_log" ]]; then
  (cd "$cwd" && run_codex) >"$json_log"
  if [[ -n "$output_file" && -s "$output_file" ]]; then
    cat "$output_file"
  else
    echo "Codex completed, but no final message was written. JSONL log: $json_log" >&2
  fi
else
  cd "$cwd"
  run_codex
fi

if [[ -n "$tmp_dir" ]]; then
  rm -rf "$tmp_dir"
fi
