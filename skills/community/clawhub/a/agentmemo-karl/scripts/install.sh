#!/usr/bin/env bash
# install.sh — agentMemo one-shot setup
# Usage: ./install.sh [--port 8790] [--db /path/to/agentmemo.db] [--admin-key <key>]
set -euo pipefail

AGENTMEMO_PORT=8790
AGENTMEMO_DB="$PWD/agentmemo.db"
AGENTMEMO_ADMIN_KEY=""
VENV_DIR="$PWD/.venv"

usage() {
  echo "Usage: $0 [--port PORT] [--db PATH] [--admin-key KEY]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --port) AGENTMEMO_PORT="$2"; shift 2 ;;
    --db)   AGENTMEMO_DB="$2"; shift 2 ;;
    --admin-key) AGENTMEMO_ADMIN_KEY="$2"; shift 2 ;;
    *) usage ;;
  esac
done

echo "=== agentMemo v3.0.0 Setup ==="
echo "  Port:     $AGENTMEMO_PORT"
echo "  DB path:  $AGENTMEMO_DB"
echo "  RBAC:     ${AGENTMEMO_ADMIN_KEY:+enabled}${AGENTMEMO_ADMIN_KEY:-disabled (no admin key)}"

# Create virtualenv if missing
if [[ ! -d "$VENV_DIR" ]]; then
  echo ""
  echo "Creating virtualenv at $VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
fi

echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q -r requirements.txt

# Write .env
ENV_FILE="$PWD/.env"
cat > "$ENV_FILE" <<EOF
AGENTMEMO_PORT=$AGENTMEMO_PORT
AGENTMEMO_DB=$AGENTMEMO_DB
EOF
if [[ -n "$AGENTMEMO_ADMIN_KEY" ]]; then
  echo "AGENTMEMO_ADMIN_KEY=$AGENTMEMO_ADMIN_KEY" >> "$ENV_FILE"
fi
echo ""
echo "✅ .env written to $ENV_FILE"

# Verify import
"$VENV_DIR/bin/python" -c "import server, database, embeddings, models, events; print('Import check: OK')"

echo ""
echo "=== Setup complete ==="
echo ""
echo "To start the server:"
echo "  source .venv/bin/activate && python server.py"
echo ""
echo "Or with dotenv:"
echo "  env \$(cat .env | xargs) .venv/bin/python server.py"
echo ""
echo "Dashboard: http://localhost:${AGENTMEMO_PORT}/dashboard"
echo "Health:    http://localhost:${AGENTMEMO_PORT}/health"
