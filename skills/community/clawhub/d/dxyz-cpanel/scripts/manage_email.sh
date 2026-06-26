#!/bin/bash
# Email Account Management
# Usage: manage_email.sh <action> [options...]
# Actions: list, create, delete, passwd, forward

set -e

ACTION="${1:?Action required (list, create, delete, passwd, forward)}"
shift 1 2>/dev/null || true

HOST="${CPANEL_HOST:?CPANEL_HOST not set}"
TOKEN="${CPANEL_TOKEN:?CPANEL_TOKEN not set}"

case "$ACTION" in
    list)
        DOMAIN="${2:?Domain required}"
        echo "Listing email accounts for $DOMAIN..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/Email/list_pops?domain=${DOMAIN}" | jq '.data'
        ;;
    create)
        EMAIL="${2:?Email required (user@domain.com)}"
        PASSWORD="${3:?Password required}"
        QUOTA="${4:-250}"
        
        USER=$(echo "$EMAIL" | cut -d@ -f1)
        DOMAIN=$(echo "$EMAIL" | cut -d@ -f2)
        
        echo "Creating email: $EMAIL..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/Email/add_pop?email=${USER}&password=${PASSWORD}&domain=${DOMAIN}&quota=${QUOTA}" | jq .
        ;;
    delete)
        EMAIL="${2:?Email required}"
        USER=$(echo "$EMAIL" | cut -d@ -f1)
        DOMAIN=$(echo "$EMAIL" | cut -d@ -f2)
        
        echo "Deleting email: $EMAIL..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/Email/delete_pop?email=${USER}&domain=${DOMAIN}" | jq .
        ;;
    passwd)
        EMAIL="${2:?Email required}"
        PASSWORD="${3:?New password required}"
        USER=$(echo "$EMAIL" | cut -d@ -f1)
        DOMAIN=$(echo "$EMAIL" | cut -d@ -f2)
        
        echo "Changing password for $EMAIL..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/Email/passwd_pop?email=${USER}&password=${PASSWORD}&domain=${DOMAIN}" | jq .
        ;;
    forward)
        EMAIL="${2:?Email required}"
        DEST="${3:?Destination email required}"
        USER=$(echo "$EMAIL" | cut -d@ -f1)
        DOMAIN=$(echo "$EMAIL" | cut -d@ -f2)
        
        echo "Setting forwarder: $EMAIL -> $DEST..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/Email/add_forwarder?domain=${DOMAIN}&email=${USER}&fwdopt=fwd&fwdemail=${DEST}" | jq .
        ;;
    *)
        echo "Usage: manage_email.sh <list|create|delete|passwd|forward> [options]"
        exit 1
        ;;
esac