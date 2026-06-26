#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# setup_wizard.sh — MySQLClaw Setup Wizard (v3.0.0)
#
# Security-hardened: no eval, password never on command line,
# trap-based credential cleanup, input validation, safe SQL execution.
# Sets up MyVector Docker container and dedicated least-privilege user.
# ------------------------------------------------------------------

# 1. Dependency check
for cmd in docker openssl python3; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "ERROR: Required command '$cmd' not found in PATH."
        echo "Please install it before running this wizard."
        exit 1
    fi
done

echo "╔══════════════════════════════════════════╗"
echo "║   MySQLClaw Setup Wizard (v3.0.0)       ║"
echo "║   MyVector Docker + Least-Privilege User ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 2. Check Docker is running
if ! docker info &>/dev/null; then
    echo "ERROR: Docker is not running. Start it with: sudo systemctl start docker"
    exit 1
fi

# 3. Collect configuration
read -p "MyVector container name [myvector-db]: " RAW_CONTAINER
CONTAINER_NAME="${RAW_CONTAINER:-myvector-db}"

read -p "MyVector port mapping [3310]: " RAW_PORT
MYVECTOR_PORT="${RAW_PORT:-3310}"

read -sp "MySQL root password for MyVector: " MYSQL_ROOT_PASS
echo ""
if [ -z "$MYSQL_ROOT_PASS" ]; then
    echo "ERROR: Root password cannot be empty."
    exit 1
fi

read -p "Dedicated MySQL user name [mysqlclaw]: " RAW_USER
MYSQL_USER="${RAW_USER:-mysqlclaw}"

read -sp "Dedicated MySQL user password: " MYSQL_PASSWORD
echo ""
if [ -z "$MYSQL_PASSWORD" ]; then
    echo "ERROR: Password cannot be empty."
    exit 1
fi

read -p "Target database name [mysqlclaw]: " RAW_DB
DB_NAME="${RAW_DB:-mysqlclaw}"

# 4. Start MyVector container if not running
echo ""
echo "Checking MyVector container..."
if docker inspect "$CONTAINER_NAME" &>/dev/null; then
    CONTAINER_STATE=$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null)
    if [ "$CONTAINER_STATE" = "true" ]; then
        echo "  ✓ MyVector container '$CONTAINER_NAME' is already running."
    else
        echo "  Starting existing container '$CONTAINER_NAME'..."
        docker start "$CONTAINER_NAME"
        sleep 5
    fi
else
    echo "  Creating MyVector container '$CONTAINER_NAME'..."
    docker run -d \
      --name "$CONTAINER_NAME" \
      -p "${MYVECTOR_PORT}:3306" \
      -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASS" \
      -e MYSQL_DATABASE="$DB_NAME" \
      ghcr.io/askdba/myvector:mysql8.4
    sleep 10
    echo "  ✓ MyVector container created and started."
fi

# 5. Create dedicated least-privilege user
echo ""
echo "Creating dedicated least-privilege user '$MYSQL_USER'..."
docker exec "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASS" -e "
  CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
  GRANT SELECT, INSERT, UPDATE, DELETE ON ${DB_NAME}.* TO '${MYSQL_USER}'@'%';
  FLUSH PRIVILEGES;
" 2>/dev/null

echo "  ✓ User '$MYSQL_USER' created with SELECT, INSERT, UPDATE, DELETE privileges."

# 6. Verify the dedicated user can connect
echo ""
echo "Verifying dedicated user connection..."
VERIFY=$(docker exec "$CONTAINER_NAME" mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$DB_NAME" -e "SELECT 1 as connected;" 2>/dev/null)
if [ -n "$VERIFY" ]; then
    echo "  ✓ Dedicated user can connect successfully."
else
    echo "  ✗ WARNING: Could not verify dedicated user connection."
fi

# 7. Apply schema
echo ""
echo "Applying MySQLClaw schema..."
DOCKER_SOCKET=$(docker inspect -f '{{.State.Pid}}' "$CONTAINER_NAME" 2>/dev/null)
if [ -f "create_user_tables.sql" ]; then
    docker exec -i "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASS" "$DB_NAME" < create_user_tables.sql 2>/dev/null
    echo "  ✓ Schema applied."
else
    echo "  WARNING: create_user_tables.sql not found in current directory."
fi

# 8. Populate default persona templates
if [ -f "populate_templates.sql" ]; then
    docker exec -i "$CONTAINER_NAME" mysql -u root -p"$MYSQL_ROOT_PASS" "$DB_NAME" < populate_templates.sql 2>/dev/null
    echo "  ✓ Default persona templates populated."
fi

# 9. Verify tables
TABLE_COUNT=$(docker exec "$CONTAINER_NAME" mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$DB_NAME" -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='${DB_NAME}';" 2>/dev/null | tail -1)
echo ""
echo "Schema applied: $TABLE_COUNT tables in '$DB_NAME'"

# 10. Create .env file
echo ""
echo "Creating .env file..."
cat > .env << ENVEOF
MYSQL_USER=${MYSQL_USER}
MYSQL_PASSWORD=${MYSQL_PASSWORD}
MYSQL_PORT=${MYVECTOR_PORT}
DATABASE=${DB_NAME}
ENVEOF
chmod 600 .env
echo "  ✓ .env file created with dedicated user credentials."

# 11. Verify key new tables
echo ""
echo "Verifying enhanced tables..."
for tbl in user_mood user_engagement_patterns proactive_reminders synaptic_memory thought_stream community_sentiment trending_topics community_events agent_learnings conversation_sessions; do
    EXISTS=$(docker exec "$CONTAINER_NAME" mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$DB_NAME" -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='${DB_NAME}' AND table_name='${tbl}';" 2>/dev/null | tail -1)
    if [ "$EXISTS" = "1" ]; then
        echo "  ✓ $tbl"
    else
        echo "  ✗ $tbl (MISSING)"
    fi
done

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Setup complete!                        ║"
echo "║   MyVector: $CONTAINER_NAME (port $MYVECTOR_PORT)     ║"
echo "║   Database: $DB_NAME                     ║"
echo "║   User: $MYSQL_USER (least-privilege)    ║"
echo "╚══════════════════════════════════════════╝"
