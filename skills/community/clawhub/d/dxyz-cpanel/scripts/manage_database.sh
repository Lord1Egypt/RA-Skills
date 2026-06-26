#!/bin/bash
# Database Management (MySQL/PostgreSQL)
# Usage: manage_database.sh <action> [options...]
# Actions: list, create_db, create_user, grant, delete_db, delete_user

set -e

ACTION="${1:?Action required}"
shift 1 2>/dev/null || true

HOST="${CPANEL_HOST:?CPANEL_HOST not set}"
TOKEN="${CPANEL_TOKEN:?CPANEL_TOKEN not set}"

case "$ACTION" in
    list)
        TYPE="${2:-mysql}"
        echo "Listing $TYPE databases..."
        if [[ "$TYPE" == "mysql" ]]; then
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Mysql/list_databases" | jq '.data'
        else
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Postgresql/list_databases" | jq '.data'
        fi
        ;;
    create_db)
        NAME="${2:?Database name required}"
        TYPE="${3:-mysql}"
        
        echo "Creating $TYPE database: $NAME..."
        if [[ "$TYPE" == "mysql" ]]; then
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Mysql/create_database?name=${NAME}" | jq .
        else
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Postgresql/create_database?name=${NAME}" | jq .
        fi
        ;;
    create_user)
        NAME="${2:?Username required}"
        PASSWORD="${3:?Password required}"
        TYPE="${4:-mysql}"
        
        echo "Creating $TYPE user: $NAME..."
        if [[ "$TYPE" == "mysql" ]]; then
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Mysql/create_user?name=${NAME}&password=${PASSWORD}" | jq .
        else
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Postgresql/create_user?name=${NAME}&password=${PASSWORD}" | jq .
        fi
        ;;
    grant)
        USER="${2:?Username required}"
        DB="${3:?Database required}"
        PRIVS="${4:-ALL PRIVILEGES}"
        TYPE="${5:-mysql}"
        
        echo "Granting '$PRIVS' on $DB to $USER..."
        PRIVS_ENCODED=$(echo "$PRIVS" | jq -sRr @uri)
        if [[ "$TYPE" == "mysql" ]]; then
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Mysql/set_privileges_on_database?user=${USER}&database=${DB}&privileges=${PRIVS_ENCODED}" | jq .
        else
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Postgresql/set_privileges_on_database?user=${USER}&database=${DB}&privileges=${PRIVS_ENCODED}" | jq .
        fi
        ;;
    delete_db)
        NAME="${2:?Database name required}"
        TYPE="${3:-mysql}"
        
        echo "Deleting $TYPE database: $NAME..."
        if [[ "$TYPE" == "mysql" ]]; then
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Mysql/delete_database?name=${NAME}" | jq .
        else
            curl -s -H "Authorization: cpanel $TOKEN" \
                "${HOST}/execute/Postgresql/delete_database?name=${NAME}" | jq .
        fi
        ;;
    *)
        echo "Usage: manage_database.sh <list|create_db|create_user|grant|delete_db> [options]"
        exit 1
        ;;
esac