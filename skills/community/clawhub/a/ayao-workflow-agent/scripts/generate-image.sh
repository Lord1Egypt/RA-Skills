#!/bin/bash
# generate-image.sh — Unified image generation entrypoint with fail-safe stub fallback

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKENDS_DIR="$SCRIPT_DIR/backends"
ALLOWED_BACKENDS=("nano-banana" "openai" "stub")

PROMPT=""
OUTPUT=""
BACKEND=""
STYLE=""

usage() {
  cat <<'EOF' >&2
Usage:
  generate-image.sh --prompt "..." --output path/to/image.png [--backend name] [--style "..."]
EOF
}

find_swarm_config() {
  if command -v swarm-config.sh >/dev/null 2>&1; then
    command -v swarm-config.sh
    return 0
  fi

  if [[ -x "$SCRIPT_DIR/swarm-config.sh" ]]; then
    printf '%s\n' "$SCRIPT_DIR/swarm-config.sh"
    return 0
  fi

  return 1
}

parse_args() {
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
      --prompt)
        [[ "$#" -ge 2 ]] || {
          echo "❌ --prompt requires a value" >&2
          usage
          return 1
        }
        PROMPT="$2"
        shift 2
        ;;
      --output)
        [[ "$#" -ge 2 ]] || {
          echo "❌ --output requires a value" >&2
          usage
          return 1
        }
        OUTPUT="$2"
        shift 2
        ;;
      --backend)
        [[ "$#" -ge 2 ]] || {
          echo "❌ --backend requires a value" >&2
          usage
          return 1
        }
        BACKEND="$2"
        shift 2
        ;;
      --style)
        [[ "$#" -ge 2 ]] || {
          echo "❌ --style requires a value" >&2
          usage
          return 1
        }
        STYLE="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "❌ Unknown argument: $1" >&2
        usage
        return 1
        ;;
    esac
  done

}

validate_backend() {
  local backend_name="$1"
  local allowed=""

  for allowed in "${ALLOWED_BACKENDS[@]}"; do
    [[ "$backend_name" == "$allowed" ]] && return 0
  done

  return 1
}

resolve_default_backend() {
  local configured_backend=""
  local swarm_config=""

  if [[ -n "$BACKEND" ]]; then
    printf '%s\n' "$BACKEND"
    return 0
  fi

  if swarm_config="$(find_swarm_config 2>/dev/null)"; then
    configured_backend="$("$swarm_config" get image_generation.default_backend 2>/dev/null || true)"
  fi
  if [[ -n "$configured_backend" ]]; then
    printf '%s\n' "$configured_backend"
    return 0
  fi

  if [[ -n "${GEMINI_API_KEY:-}" ]]; then
    printf '%s\n' "nano-banana"
    return 0
  fi
  if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    printf '%s\n' "openai"
    return 0
  fi

  printf '%s\n' "stub"
}

run_backend_script() {
  local backend_name="$1"
  local backend_script="$BACKENDS_DIR/${backend_name}.sh"

  if [[ ! -f "$backend_script" ]]; then
    echo "⚠️  Backend ${backend_name} not found, using stub" >&2
    return 1
  fi

  bash "$backend_script" "$PROMPT" "$OUTPUT" "$STYLE"
}

call_backend_safe() {
  if ! run_backend_script "$BACKEND"; then
    if [[ "$BACKEND" != "stub" ]]; then
      echo "⚠️  Backend ${BACKEND} failed, using stub" >&2
    fi
    BACKEND="stub"
    run_backend_script "stub" || {
      echo "❌ Stub backend failed" >&2
      return 1
    }
  fi
}

main() {
  parse_args "$@"

  if [[ -z "$PROMPT" || -z "$OUTPUT" ]]; then
    echo "❌ --prompt and --output are required" >&2
    exit 1
  fi

  if [[ -n "$BACKEND" ]] && ! validate_backend "$BACKEND"; then
    echo "❌ Unknown backend: '$BACKEND'. Allowed: ${ALLOWED_BACKENDS[*]}" >&2
    BACKEND="stub"
  fi

  BACKEND="$(resolve_default_backend)"

  if ! validate_backend "$BACKEND"; then
    echo "❌ Unknown backend: '$BACKEND'. Allowed: ${ALLOWED_BACKENDS[*]}" >&2
    BACKEND="stub"
  fi

  mkdir -p "$(dirname "$OUTPUT")"

  call_backend_safe

  if [[ -f "$OUTPUT" ]]; then
    echo "✅ Image generated: $OUTPUT"
    return 0
  fi

  echo "❌ Image generation failed: output file not found" >&2
  exit 1
}

main "$@"
