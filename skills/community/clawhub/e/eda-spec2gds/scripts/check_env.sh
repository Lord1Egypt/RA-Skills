#!/usr/bin/env bash
set -euo pipefail

TOOLS=(python3 yosys iverilog vvp docker)
OPTIONAL=(verilator klayout gtkwave)

STATUS=0

find_openlane() {
  if command -v openlane >/dev/null 2>&1; then
    command -v openlane
    return 0
  fi
  if [[ -x "$HOME/.venvs/openlane/bin/openlane" ]]; then
    echo "$HOME/.venvs/openlane/bin/openlane"
    return 0
  fi
  return 1
}

echo "[required]"
for tool in "${TOOLS[@]}"; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'ok  %s -> %s\n' "$tool" "$(command -v "$tool")"
  else
    printf 'miss %s\n' "$tool"
    STATUS=1
  fi
done

echo

echo "[optional]"
for tool in "${OPTIONAL[@]}"; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'ok  %s -> %s\n' "$tool" "$(command -v "$tool")"
  else
    printf 'miss %s\n' "$tool"
  fi
done

if OPENLANE_PATH=$(find_openlane); then
  printf 'ok  openlane -> %s\n' "$OPENLANE_PATH"
else
  printf 'miss openlane\n'
fi

exit "$STATUS"
