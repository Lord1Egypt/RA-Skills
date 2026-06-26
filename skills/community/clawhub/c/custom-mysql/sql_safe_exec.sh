#!/usr/bin/env bash
set -euo pipefail

# sql_safe_exec.sh - Hardened MyVector MySQL wrapper v3.0.0
# Routes all SQL through the MyVector Docker container's mysql client.
# MyVector (ghcr.io/askdba/myvector:mysql8.4) is a MySQL 8.4 server
# with vector search extensions. It replaces the need for a separate
# MySQL installation.
#
# Security controls:
#   - Single-statement only (semicolons rejected)
#   - DDL blocked (DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE, EXEC, EXECUTE, PREPARE, DEALLOCATE)
#   - DML requires interactive confirmation (no non-interactive bypass)
#   - Table allowlist enforced for all write operations (26 approved tables)
#   - Path traversal / sensitive file patterns blocked
#   - Credentials via temporary --defaults-extra-file (password never on command line)
#   - .env file parsed as KEY=VALUE (never shell-sourced)
#   - Comment injection blocked (/* */ and -- style)
#   - Hex-encoded string detection blocked
#   - Temp credentials file cleaned up on ANY exit
#   - FAIL CLOSED: refuses to connect if MYSQL_USER or MYSQL_PASSWORD is missing
#   - REJECTS root/admin users — requires dedicated least-privilege account
#   - All queries routed through MyVector Docker container via docker exec

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load .env safely — parse as KEY=VALUE only, never evaluate as shell code
MYSQL_USER_VAL=""
MYSQL_PASSWORD_VAL=""
MYSQL_PORT_VAL="3310"
DATABASE_VAL="mysqlclaw"
DOCKER_CONTAINER="myvector-db"

if [ -f "$SCRIPT_DIR/.env" ]; then
    while IFS='=' read -r key val; do
        [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue
        [[ -z "$key" || "$key" =~ ^# ]] && continue
        case "$key" in
            MYSQL_USER)     MYSQL_USER_VAL="$val" ;;
            MYSQL_PASSWORD) MYSQL_PASSWORD_VAL="$val" ;;
            MYSQL_PORT)     MYSQL_PORT_VAL="$val" ;;
            DATABASE)       DATABASE_VAL="$val" ;;
        esac
    done < <(grep -v '^[[:space:]]*#' "$SCRIPT_DIR/.env" | grep '=')
fi

# --- FAIL CLOSED: refuse to connect without credentials ---
if [ -z "$MYSQL_USER_VAL" ]; then
    echo "ERROR: MYSQL_USER is not set in .env. Refusing to connect." >&2
    echo "Create a dedicated least-privilege MySQL user and set MYSQL_USER in .env." >&2
    exit 1
fi

if [ -z "$MYSQL_PASSWORD_VAL" ]; then
    echo "ERROR: MYSQL_PASSWORD is not set in .env. Refusing to connect." >&2
    exit 1
fi

# --- REJECT root/admin users ---
if [ "$MYSQL_USER_VAL" = "root" ] || [ "$MYSQL_USER_VAL" = "admin" ] || [ "$MYSQL_USER_VAL" = "mysql" ]; then
    echo "ERROR: Refusing to connect as '$MYSQL_USER_VAL'. Use a dedicated least-privilege account." >&2
    echo "Create a dedicated user with only SELECT, INSERT, UPDATE, DELETE on the mysqlclaw database." >&2
    exit 1
fi

# --- Verify MyVector container is running ---
if ! docker inspect "$DOCKER_CONTAINER" &>/dev/null; then
    echo "ERROR: MyVector container '$DOCKER_CONTAINER' not found." >&2
    echo "Start it with: docker run -d --name $DOCKER_CONTAINER -p ${MYSQL_PORT_VAL}:3306 -e MYSQL_ROOT_PASSWORD=<pw> -e MYSQL_DATABASE=mysqlclaw ghcr.io/askdba/myvector:mysql8.4" >&2
    exit 1
fi

CONTAINER_STATE=$(docker inspect -f '{{.State.Running}}' "$DOCKER_CONTAINER" 2>/dev/null)
if [ "$CONTAINER_STATE" != "true" ]; then
    echo "ERROR: MyVector container '$DOCKER_CONTAINER' is not running." >&2
    echo "Start it with: docker start $DOCKER_CONTAINER" >&2
    exit 1
fi

# Build temporary credentials file (password never on command line)
CREDS_FILE=$(mktemp /tmp/.mysqlclaw_XXXXXX.cnf)
chmod 600 "$CREDS_FILE"
cat > "$CREDS_FILE" << CREDS_EOF
[client]
user=${MYSQL_USER_VAL}
password=${MYSQL_PASSWORD_VAL}
host=localhost
port=3306
CREDS_EOF

# Build MySQL command: docker exec into MyVector, mount creds file as volume
# Copy creds file into running container for mysql client to use locally
CONTAINER_CREDS_PATH="/tmp/.mysqlclaw_creds.cnf"
docker cp "$CREDS_FILE" "$DOCKER_CONTAINER:${CONTAINER_CREDS_PATH}" 2>/dev/null

# Trap-based cleanup – runs on ANY exit (normal, error, signal)
# Removes BOTH the host temp file AND the copy inside the Docker container
cleanup_all_creds() {
    docker exec "$DOCKER_CONTAINER" rm -f "${CONTAINER_CREDS_PATH}" 2>/dev/null || true
    rm -f "$CREDS_FILE"
}
trap cleanup_all_creds EXIT

MYSQL_CMD="docker exec -i ${DOCKER_CONTAINER} mysql --defaults-extra-file=${CONTAINER_CREDS_PATH} -D ${DATABASE_VAL} -e"

SQL="${1:-}"
READONLY_MODE=false

# Check for --readonly flag
if [ "$SQL" = "--readonly" ]; then
    READONLY_MODE=true
    SQL="${2:-}"
fi

[ -z "$SQL" ] && echo "ERROR: No SQL" >&2 && exit 1

# --- 1. Single-statement check: reject semicolons ---
if echo "$SQL" | grep -q ';'; then
    echo "ERROR: Multi-statement SQL not allowed. Execute one statement at a time." >&2
    exit 1
fi

# --- 2. DDL blocking ---
if echo "$SQL" | grep -iqE "\b(DROP|TRUNCATE|CREATE|ALTER|GRANT|REVOKE|EXEC|EXECUTE|PREPARE|DEALLOCATE|RENAME|COMMENT)\b"; then
    echo "ERROR: DDL statements are blocked. Only SELECT, INSERT, UPDATE, DELETE, REPLACE are allowed." >&2
    exit 1
fi

# --- 3. Path traversal / sensitive file blocking ---
if echo "$SQL" | grep -iqE "(\.ssh|\.gnupg|\.aws|\.config|/etc/|/root/|/var/|LOAD_FILE|INTO\s+OUTFILE|INTO\s+DUMPFILE|\.\./|\.\.\\\\)"; then
    echo "ERROR: SQL contains blocked path or file operation patterns." >&2
    exit 1
fi

# --- 4. Comment injection blocking ---
if echo "$SQL" | grep -iqE "(/\*|\*/|--\s|[#]\s)"; then
    echo "ERROR: SQL comments are not allowed (/* */ or -- or #). Possible injection attempt." >&2
    exit 1
fi

# --- 5. Hex-encoded string detection ---
if echo "$SQL" | grep -iqE "(0x[0-9a-fA-F]+|UNHEX|HEX\()"; then
    echo "ERROR: Hex-encoded values are not allowed. Possible injection attempt." >&2
    exit 1
fi

# --- 6. Readonly mode: SELECT only ---
if $READONLY_MODE; then
    if ! echo "$SQL" | grep -qiE "^\s*SELECT\b"; then
        echo "ERROR: --readonly mode only accepts SELECT statements." >&2
        exit 1
    fi
    $MYSQL_CMD "$SQL"
    exit $?
fi

# --- 7. Table allowlist for write operations ---
ALLOWED_WRITE_TABLES=(
    "users"
    "user_preferences"
    "user_attributes"
    "user_media"
    "user_food_preferences"
    "user_personas"
    "persona_templates"
    "user_interactions"
    "conversation_sessions"
    "session_interactions"
    "user_relationships"
    "user_context"
    "skill_usage"
    "user_notes"
    "user_mood"
    "user_engagement_patterns"
    "user_activity_heatmap"
    "proactive_reminders"
    "synaptic_memory"
    "thought_stream"
    "topic_keywords"
    "community_sentiment"
    "trending_topics"
    "community_events"
    "agent_learnings"
    "memory_consolidation_log"
)

TABLE_NAME=""
if echo "$SQL" | grep -iqE "\b(INSERT|UPDATE|DELETE|REPLACE)\b"; then
    TABLE_NAME=$(echo "$SQL" | grep -oiE "(INTO|UPDATE|FROM|TABLE)\s+([a-zA-Z_][a-zA-Z0-9_]*)" | grep -oE "[a-zA-Z_][a-zA-Z0-9_]*$" | head -1)

    if [ -z "$TABLE_NAME" ]; then
        echo "ERROR: Could not determine target table for write operation." >&2
        exit 1
    fi

    ALLOWED=false
    for t in "${ALLOWED_WRITE_TABLES[@]}"; do
        if [ "$TABLE_NAME" = "$t" ]; then
            ALLOWED=true
            break
        fi
    done

    if ! $ALLOWED; then
        echo "ERROR: Table '$TABLE_NAME' is not in the write allowlist." >&2
        echo "Allowed tables: ${ALLOWED_WRITE_TABLES[*]}" >&2
        exit 1
    fi
fi

# --- 8. DML confirmation ---
if echo "$SQL" | grep -iqE "\b(INSERT|UPDATE|DELETE|REPLACE)\b"; then
    echo "WARNING: Modifying data: $SQL"
    read -p "Confirm? (yes/no): " ans
    [ "$ans" != "yes" ] && echo "Aborted." && exit 0
fi

$MYSQL_CMD "$SQL"
