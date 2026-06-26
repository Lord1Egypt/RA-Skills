#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/export-agent-core-pack.sh [options]

Detect supported agent frameworks, extract agent-core files, and build a pure source-only zip.

Options:
  --base-dir <path>    Base repo directory. Default: ~/Documents/GitHub
  --output-dir <path>  Output directory. Default: current directory
  --name <name>        Archive base name. Default: agent-core-pack-<timestamp>
  --repos <list>       Comma-separated repo names. Default: nanoclaw,nanobot,nullclaw,zeroclaw,openfang,codex
  --help               Show this help
EOF
}

expand_path() {
  case "$1" in
    "~") printf '%s\n' "$HOME" ;;
    "~/"*) printf '%s\n' "$HOME/${1#"~/"}" ;;
    *) printf '%s\n' "$1" ;;
  esac
}

resolve_path() {
  local raw
  raw="$(expand_path "$1")"
  if [[ "$raw" == /* ]]; then
    printf '%s\n' "$raw"
  else
    printf '%s/%s\n' "$PWD" "$raw"
  fi
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

copy_file() {
  local src="$1"
  local dst="$2"
  [[ -f "$src" ]] || return 0
  mkdir -p "$(dirname "$dst")"
  cp -p "$src" "$dst"
  INCLUDED_PATHS+=("$src")
}

copy_dir() {
  local src="$1"
  local dst="$2"
  [[ -d "$src" ]] || return 0
  mkdir -p "$(dirname "$dst")"
  cp -Rp "$src" "$dst"
  INCLUDED_PATHS+=("$src")
}

detect_framework() {
  local repo_dir="$1"
  if [[ -f "$repo_dir/src/config.ts" && -f "$repo_dir/groups/main/CLAUDE.md" ]]; then
    printf '%s\n' "nanoclaw-ts-bootstrap"
  elif [[ -f "$repo_dir/nanobot/config/schema.py" && -f "$repo_dir/nanobot/templates/AGENTS.md" ]]; then
    printf '%s\n' "nanobot-py-templates"
  elif [[ -f "$repo_dir/src/agent/prompt.zig" && -d "$repo_dir/src/workspace_templates" ]]; then
    printf '%s\n' "nullclaw-zig-bootstrap"
  elif [[ -f "$repo_dir/src/config/schema.rs" && -f "$repo_dir/src/agent/prompt.rs" ]]; then
    printf '%s\n' "zeroclaw-rs-config-prompt"
  elif [[ -f "$repo_dir/crates/openfang-kernel/src/config.rs" && -d "$repo_dir/agents" ]]; then
    printf '%s\n' "openfang-rs-manifests"
  elif [[ -d "$repo_dir/codex-rs/core/src/agent/builtins" && -f "$repo_dir/AGENTS.md" ]]; then
    printf '%s\n' "codex-rs-builtins"
  else
    printf '%s\n' "unknown"
  fi
}

extract_by_framework() {
  local repo="$1"
  local repo_dir="$2"
  local framework="$3"
  local dest="$4"

  case "$framework" in
    nanoclaw-ts-bootstrap)
      copy_file "$repo_dir/CLAUDE.md" "$dest/CLAUDE.md"
      copy_file "$repo_dir/groups/global/CLAUDE.md" "$dest/groups/global/CLAUDE.md"
      copy_file "$repo_dir/groups/main/CLAUDE.md" "$dest/groups/main/CLAUDE.md"
      copy_file "$repo_dir/.claude/settings.json" "$dest/.claude/settings.json"
      copy_file "$repo_dir/src/config.ts" "$dest/src/config.ts"
      copy_file "$repo_dir/config-examples/mount-allowlist.json" "$dest/config-examples/mount-allowlist.json"
      ;;
    nanobot-py-templates)
      copy_file "$repo_dir/nanobot/config/schema.py" "$dest/nanobot/config/schema.py"
      copy_file "$repo_dir/nanobot/config/loader.py" "$dest/nanobot/config/loader.py"
      copy_file "$repo_dir/nanobot/config/paths.py" "$dest/nanobot/config/paths.py"
      copy_file "$repo_dir/nanobot/templates/AGENTS.md" "$dest/nanobot/templates/AGENTS.md"
      copy_file "$repo_dir/nanobot/templates/SOUL.md" "$dest/nanobot/templates/SOUL.md"
      copy_file "$repo_dir/nanobot/templates/USER.md" "$dest/nanobot/templates/USER.md"
      copy_file "$repo_dir/nanobot/templates/TOOLS.md" "$dest/nanobot/templates/TOOLS.md"
      copy_file "$repo_dir/nanobot/templates/HEARTBEAT.md" "$dest/nanobot/templates/HEARTBEAT.md"
      copy_file "$repo_dir/nanobot/templates/memory/MEMORY.md" "$dest/nanobot/templates/memory/MEMORY.md"
      ;;
    nullclaw-zig-bootstrap)
      copy_file "$repo_dir/config.example.json" "$dest/config.example.json"
      copy_file "$repo_dir/docs/en/configuration.md" "$dest/docs/en/configuration.md"
      copy_dir "$repo_dir/src/workspace_templates" "$dest/src/workspace_templates"
      copy_file "$repo_dir/src/agent/prompt.zig" "$dest/src/agent/prompt.zig"
      ;;
    zeroclaw-rs-config-prompt)
      copy_file "$repo_dir/CLAUDE.md" "$dest/CLAUDE.md"
      copy_file "$repo_dir/examples/config.example.toml" "$dest/examples/config.example.toml"
      copy_file "$repo_dir/docs/reference/api/config-reference.md" "$dest/docs/reference/api/config-reference.md"
      copy_file "$repo_dir/src/config/schema.rs" "$dest/src/config/schema.rs"
      copy_file "$repo_dir/src/agent/prompt.rs" "$dest/src/agent/prompt.rs"
      ;;
    openfang-rs-manifests)
      copy_file "$repo_dir/docs/configuration.md" "$dest/docs/configuration.md"
      copy_file "$repo_dir/docs/agent-templates.md" "$dest/docs/agent-templates.md"
      copy_file "$repo_dir/crates/openfang-kernel/src/config.rs" "$dest/crates/openfang-kernel/src/config.rs"
      copy_file "$repo_dir/crates/openfang-cli/src/bundled_agents.rs" "$dest/crates/openfang-cli/src/bundled_agents.rs"
      copy_dir "$repo_dir/agents" "$dest/agents"
      ;;
    codex-rs-builtins)
      copy_file "$repo_dir/AGENTS.md" "$dest/AGENTS.md"
      copy_file "$repo_dir/docs/config.md" "$dest/docs/config.md"
      copy_file "$repo_dir/docs/example-config.md" "$dest/docs/example-config.md"
      copy_file "$repo_dir/.github/codex/home/config.toml" "$dest/.github/codex/home/config.toml"
      copy_file "$repo_dir/codex-rs/core/src/external_agent_config.rs" "$dest/codex-rs/core/src/external_agent_config.rs"
      copy_dir "$repo_dir/codex-rs/core/src/agent/builtins" "$dest/codex-rs/core/src/agent/builtins"
      copy_file "$repo_dir/codex-rs/core/prompt.md" "$dest/codex-rs/core/prompt.md"
      copy_file "$repo_dir/codex-rs/core/gpt_5_codex_prompt.md" "$dest/codex-rs/core/gpt_5_codex_prompt.md"
      copy_file "$repo_dir/codex-rs/core/src/config/schema.rs" "$dest/codex-rs/core/src/config/schema.rs"
      ;;
    *)
      return 1
      ;;
  esac
}

BASE_DIR="~/Documents/GitHub"
OUTPUT_DIR="."
NAME="agent-core-pack-$(date +"%Y%m%d-%H%M%S")"
REPOS_RAW="nanoclaw,nanobot,nullclaw,zeroclaw,openfang,codex"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-dir) BASE_DIR="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;
    --repos) REPOS_RAW="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

require_cmd zip

BASE_DIR="$(resolve_path "$BASE_DIR")"
OUTPUT_DIR="$(resolve_path "$OUTPUT_DIR")"
STAGING_DIR="$OUTPUT_DIR/$NAME"
ZIP_PATH="$OUTPUT_DIR/$NAME.zip"

[[ ! -e "$STAGING_DIR" ]] || { echo "Refusing to overwrite: $STAGING_DIR" >&2; exit 1; }
[[ ! -e "$ZIP_PATH" ]] || { echo "Refusing to overwrite: $ZIP_PATH" >&2; exit 1; }

mkdir -p "$STAGING_DIR"
declare -a INCLUDED_PATHS=()
declare -a FRAMEWORK_LINES=()

IFS=',' read -r -a REPOS <<<"$REPOS_RAW"
for repo in "${REPOS[@]}"; do
  repo="$(printf '%s' "$repo" | xargs)"
  [[ -n "$repo" ]] || continue
  repo_dir="$BASE_DIR/$repo"
  [[ -d "$repo_dir" ]] || { echo "Missing repo: $repo_dir" >&2; exit 1; }
  framework="$(detect_framework "$repo_dir")"
  [[ "$framework" != "unknown" ]] || { echo "Unsupported framework in $repo" >&2; exit 1; }
  FRAMEWORK_LINES+=("$repo | $framework")
  mkdir -p "$STAGING_DIR/$repo"
  extract_by_framework "$repo" "$repo_dir" "$framework" "$STAGING_DIR/$repo"
done

cat >"$STAGING_DIR/README.txt" <<'EOF'
This archive is a pure source-only agent core export.

Included:
- identity files
- instruction files
- context/bootstrap files
- runtime config files
- prompt-composition files
- multi-agent manifest files

Excluded:
- target-framework metadata
- migration data
- tests
- build artifacts
- unrelated application code
EOF

{
  echo "Detected frameworks:"
  for line in "${FRAMEWORK_LINES[@]}"; do
    echo "- $line"
  done
  echo
  echo "Included source paths:"
  for path in "${INCLUDED_PATHS[@]}"; do
    echo "- $path"
  done
} >"$STAGING_DIR/MANIFEST.txt"

(
  cd "$OUTPUT_DIR"
  zip -qry "$ZIP_PATH" "$NAME"
)

echo "Created: $ZIP_PATH"
