#!/usr/bin/env bash
# install.sh — install claw-config into ~/.openclaw/skills/ and
# symlink the entrypoint onto $PATH. Idempotent.

set -euo pipefail

SLUG="claw-config"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.openclaw/skills/${SLUG}"
BIN_DIR="${HOME}/.local/bin"
ALIAS="${1:-${SLUG}}"   # first arg: optional shorter alias name

# 1. preflight
command -v openclaw >/dev/null 2>&1 || {
  echo "error: 'openclaw' CLI not on PATH. Install OpenClaw first: https://docs.openclaw.ai/" >&2
  exit 1
}
command -v python3 >/dev/null 2>&1 || {
  echo "error: 'python3' not on PATH. Python 3.9+ required." >&2
  exit 1
}

# 2. install skill files
mkdir -p "${SKILLS_DIR}"
cp "${SRC_DIR}/SKILL.md" "${SKILLS_DIR}/SKILL.md"
cp "${SRC_DIR}/claw-config.py" "${SKILLS_DIR}/claw-config.py"
chmod +x "${SKILLS_DIR}/claw-config.py"

# 3. symlink onto PATH
mkdir -p "${BIN_DIR}"
ln -sf "${SKILLS_DIR}/claw-config.py" "${BIN_DIR}/${ALIAS}"

# 4. sanity check
if ! command -v "${ALIAS}" >/dev/null 2>&1; then
  echo "warning: ${BIN_DIR} is not on \$PATH; add it to use \`${ALIAS}\` directly:" >&2
  echo "  export PATH=\"\$HOME/.local/bin:\$PATH\"" >&2
fi

echo "installed:"
echo "  skill dir:  ${SKILLS_DIR}/"
echo "  entrypoint: ${BIN_DIR}/${ALIAS}"
echo
echo "verify:"
echo "  ${ALIAS} --help"
echo "  OPENCLAW_AGENT_ID=<your-agent-id> ${ALIAS} whoami"
