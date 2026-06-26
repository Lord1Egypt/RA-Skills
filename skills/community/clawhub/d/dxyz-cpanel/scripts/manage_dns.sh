#!/bin/bash
# DNS Zone Management
# Usage: manage_dns.sh <action> <domain> [options...]
# Actions: list, add, delete, modify

set -e

ACTION="${1:?Action required (list, add, delete, modify)}"
DOMAIN="${2:?Domain required}"
shift 2 2>/dev/null || true

HOST="${CPANEL_HOST:?CPANEL_HOST not set}"
TOKEN="${CPANEL_TOKEN:?CPANEL_TOKEN not set}"

case "$ACTION" in
    list)
        echo "Listing DNS records for $DOMAIN..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/DNS/zone_records?domain=${DOMAIN}" | jq .
        ;;
    add)
        NAME="${3:?Record name required}"
        TYPE="${4:?Record type required (A, AAAA, CNAME, MX, TXT)}"
        VALUE="${5:?Record value required}"
        TTL="${6:-3600}"
        
        echo "Adding $TYPE record: $NAME -> $VALUE..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/DNS/add_zone_record?domain=${DOMAIN}&name=${NAME}&type=${TYPE}&address=${VALUE}&ttl=${TTL}" | jq .
        ;;
    delete)
        LINE="${3:?Line number required (use list to find)}"
        
        echo "Deleting DNS record at line $LINE..."
        curl -s -H "Authorization: cpanel $TOKEN" \
            "${HOST}/execute/DNS/remove_zone_record?domain=${DOMAIN}&line=${LINE}" | jq .
        ;;
    *)
        echo "Usage: manage_dns.sh <list|add|delete|modify> <domain> [options]"
        exit 1
        ;;
esac