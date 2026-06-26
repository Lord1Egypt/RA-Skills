#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.env"

DEFAULT_OUT_DIR="$HOME/backups/openclaw-snapshots"
DEFAULT_PREFIX="occt7pkbak"
DEFAULT_KEEP="5"

CONFIG_OUT_DIR=""
CONFIG_PREFIX=""
CONFIG_KEEP=""
if [[ -f "$CONFIG_FILE" ]]; then
  while IFS='=' read -r key value; do
    case "$key" in
      OPENCLAW_SNAPSHOT_DIR) CONFIG_OUT_DIR="${value//\$HOME/$HOME}" ;;
      OPENCLAW_SNAPSHOT_PREFIX) CONFIG_PREFIX="$value" ;;
      OPENCLAW_SNAPSHOT_KEEP) CONFIG_KEEP="$value" ;;
    esac
  done < "$CONFIG_FILE"
fi

ENV_OUT_DIR="${OPENCLAW_SNAPSHOT_DIR:-}"
ENV_PREFIX="${OPENCLAW_SNAPSHOT_PREFIX:-}"
ENV_KEEP="${OPENCLAW_SNAPSHOT_KEEP:-}"

EFFECTIVE_OUT_DIR="${CONFIG_OUT_DIR:-${ENV_OUT_DIR:-$DEFAULT_OUT_DIR}}"
EFFECTIVE_PREFIX="${CONFIG_PREFIX:-${ENV_PREFIX:-$DEFAULT_PREFIX}}"
EFFECTIVE_KEEP="${CONFIG_KEEP:-${ENV_KEEP:-$DEFAULT_KEEP}}"

printf 'Config file: %s\n' "$CONFIG_FILE"
printf 'Default backup directory: %s\n' "$DEFAULT_OUT_DIR"
printf 'Config backup directory: %s\n' "${CONFIG_OUT_DIR:-<unset>}"
printf 'Env backup directory: %s\n' "${ENV_OUT_DIR:-<unset>}"
printf 'Effective backup directory: %s\n' "$EFFECTIVE_OUT_DIR"
printf '\n'
printf 'Default prefix: %s\n' "$DEFAULT_PREFIX"
printf 'Config prefix: %s\n' "${CONFIG_PREFIX:-<unset>}"
printf 'Env prefix: %s\n' "${ENV_PREFIX:-<unset>}"
printf 'Effective prefix: %s\n' "$EFFECTIVE_PREFIX"
printf '\n'
printf 'Default retention count: %s\n' "$DEFAULT_KEEP"
printf 'Config retention count: %s\n' "${CONFIG_KEEP:-<unset>}"
printf 'Env retention count: %s\n' "${ENV_KEEP:-<unset>}"
printf 'Effective retention count: %s\n' "$EFFECTIVE_KEEP"
