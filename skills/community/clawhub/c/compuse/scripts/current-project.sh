#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
case "$(uname -s)" in
  Darwin)
    printf '%s\n' "$SKILL_ROOT/project/platforms/macos"
    ;;
  Linux)
    printf '%s\n' "$SKILL_ROOT/project/platforms/linux"
    ;;
  CYGWIN*|MINGW*|MSYS*)
    printf '%s\n' "$SKILL_ROOT/project/platforms/windows"
    ;;
  *)
    printf 'Unsupported platform: %s\n' "$(uname -s)" >&2
    exit 1
    ;;
esac
