#!/usr/bin/env bash
# em-intel launcher — auto-detects Python or Docker.
# Usage: ./run.sh <command> [--dry-run]
# Examples:
#   ./run.sh setup
#   ./run.sh morning-brief
#   ./run.sh morning-brief --dry-run
#   ./run.sh doctor

set -e
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="em-intel"
ENV_FILE="$SKILL_DIR/.env"

# ── Detect runtime ─────────────────────────────────────────────────────────────
HAS_PYTHON=false
HAS_DOCKER=false

if command -v python3 &>/dev/null && python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)" 2>/dev/null; then
  HAS_PYTHON=true
fi

if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
  HAS_DOCKER=true
fi

# ── No runtime available ────────────────────────────────────────────────────────
if ! $HAS_PYTHON && ! $HAS_DOCKER; then
  echo ""
  echo "❌  em-intel needs Python 3.9+ or Docker to run."
  echo ""
  echo "  Install Python:  https://www.python.org/downloads/"
  echo "  Install Docker:  https://docs.docker.com/get-docker/"
  echo ""
  echo "  Or use the cloud shell — no install required:"
  echo "    https://clawhub.com/larryfang/em-intel"
  echo ""
  exit 1
fi

# ── Python path ─────────────────────────────────────────────────────────────────
if $HAS_PYTHON; then
  # Auto-install deps if needed (silent)
  pip3 install -r "$SKILL_DIR/requirements.txt" -q 2>/dev/null || true
  exec python3 "$SKILL_DIR/em_intel.py" "$@"
fi

# ── Docker path ─────────────────────────────────────────────────────────────────
# Build image if not present or Dockerfile is newer
if ! docker image inspect "$IMAGE_NAME" &>/dev/null 2>&1 || \
   [ "$SKILL_DIR/Dockerfile" -nt <(docker image inspect "$IMAGE_NAME" --format '{{.Metadata.LastTagTime}}' 2>/dev/null) ]; then
  echo "🐳  Building em-intel Docker image (first time, ~30s)..."
  docker build -t "$IMAGE_NAME" "$SKILL_DIR" -q
  echo "✓  Image ready"
fi

# Run with .env if it exists
if [ -f "$ENV_FILE" ]; then
  exec docker run --rm --env-file "$ENV_FILE" "$IMAGE_NAME" "$@"
else
  exec docker run --rm "$IMAGE_NAME" "$@"
fi
