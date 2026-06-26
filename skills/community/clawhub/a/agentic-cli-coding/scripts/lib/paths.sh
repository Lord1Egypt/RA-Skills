#!/usr/bin/env bash
# paths.sh — Robust path resolution for the agentic_cli_coding skill.
#
# Sourced by every oce-* script BEFORE common.sh. It computes OCE_HOME
# from the actual script location (resolving symlinks) so the skill works
# no matter where it's installed or invoked from. Also picks workspace-
# scoped storage dirs so backups/transactions live next to the project,
# not in the user's home, which keeps the skill self-contained.

# Resolve the directory of the *calling* script, following symlinks.
# Caller must have set OCE_CALLER="${BASH_SOURCE[0]}" or pass $0 in.
_oce_resolve_home() {
  local src="${OCE_CALLER:-${BASH_SOURCE[1]:-$0}}"
  # Follow symlinks
  while [ -h "$src" ]; do
    local dir
    dir="$(cd -P "$(dirname "$src")" && pwd)"
    src="$(readlink "$src")"
    [[ "$src" != /* ]] && src="$dir/$src"
  done
  local script_dir
  script_dir="$(cd -P "$(dirname "$src")" && pwd)"
  # The calling script lives in <OCE_HOME>/scripts/, so go one up.
  printf '%s\n' "$(cd -P "$script_dir/.." && pwd)"
}

# Only set OCE_HOME if not already exported by the caller
if [ -z "${OCE_HOME:-}" ]; then
  OCE_HOME="$(_oce_resolve_home)"
  export OCE_HOME
fi

# Workspace-scoped state. Defaults to a hidden dir in the current working
# directory, falling back to /tmp if cwd isn't writable. This keeps each
# project's edit history isolated and makes the skill safe to install
# read-only at OCE_HOME.
if [ -z "${OCE_STATE_DIR:-}" ]; then
  if [ -w "$PWD" ]; then
    OCE_STATE_DIR="$PWD/.oce"
  else
    OCE_STATE_DIR="${TMPDIR:-/tmp}/oce-$(id -u)"
  fi
  export OCE_STATE_DIR
fi

OCE_BACKUP_DIR="${OCE_BACKUP_DIR:-$OCE_STATE_DIR/backups}"
OCE_TXN_DIR="${OCE_TXN_DIR:-$OCE_STATE_DIR/transactions}"
OCE_LOG="${OCE_LOG:-$OCE_STATE_DIR/edit.log}"
export OCE_BACKUP_DIR OCE_TXN_DIR OCE_LOG

mkdir -p "$OCE_BACKUP_DIR" "$OCE_TXN_DIR" "$(dirname "$OCE_LOG")" 2>/dev/null || true

# NODE_PATH so ast-helper.js can `require('acorn')` regardless of cwd
if [ -d "$OCE_HOME/node_modules" ]; then
  export NODE_PATH="$OCE_HOME/node_modules${NODE_PATH:+:$NODE_PATH}"
fi
