#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${1:-$HOME/bin}"

mkdir -p "$BIN_DIR"

ln -sfn "${SCRIPT_DIR}/codex-dev-dispatch" "${BIN_DIR}/codex-dev-dispatch"
ln -sfn "${SCRIPT_DIR}/codex-dev-dispatch" "${BIN_DIR}/codex-dev"
ln -sfn "${SCRIPT_DIR}/codex-dev-dispatch" "${BIN_DIR}/codex-help"

cat >"${BIN_DIR}/codex-dev-status" <<EOF
#!/usr/bin/env bash
exec "${SCRIPT_DIR}/codex-dev-dispatch" status "\$@"
EOF

cat >"${BIN_DIR}/codex-dev-show" <<EOF
#!/usr/bin/env bash
exec "${SCRIPT_DIR}/codex-dev-dispatch" show "\$@"
EOF

chmod +x "${BIN_DIR}/codex-dev-status" "${BIN_DIR}/codex-dev-show"

echo "Installed wrappers into ${BIN_DIR}"
echo "Make sure ${BIN_DIR} is on PATH."
