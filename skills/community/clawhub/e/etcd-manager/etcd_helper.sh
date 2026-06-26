#!/bin/bash
set -euo pipefail

# etcd Helper Script
# Version: 1.0.0
# A clean and safe etcd management tool

ACTION="${1:-}"
ENDPOINTS="${2:-}"
TARGET="${3:-}"
VALUE="${4:-}"

# etcdctl 3.6.1+ doesn't need ETCDCTL_API=3 environment variable

show_usage() {
    echo "etcd Helper Script"
    echo "=================="
    echo "Usage: $0 <list|get|put|delete> <endpoints> <target> [value]"
    echo ""
    echo "Examples:"
    echo "  $0 list http://localhost:2379 /app/config/"
    echo "  $0 get http://localhost:2379 /app/config/database"
    echo "  $0 put http://localhost:2379 /test/key \"test value\""
    echo "  $0 delete http://localhost:2379 /test/old_key"
    echo ""
    echo "Options:"
    echo "  list    - List keys with given prefix"
    echo "  get     - Get value of a specific key"
    echo "  put     - Put value for a key (shows old value first)"
    echo "  delete  - Delete a key (shows old value first)"
}

case "$ACTION" in
    list)
        if [ -z "$ENDPOINTS" ] || [ -z "$TARGET" ]; then
            echo "Error: Missing endpoints or target prefix"
            show_usage
            exit 1
        fi
        echo "Listing keys with prefix: $TARGET"
        echo "================================"
        etcdctl --endpoints="$ENDPOINTS" get "$TARGET" --prefix --keys-only
        ;;
        
    get)
        if [ -z "$ENDPOINTS" ] || [ -z "$TARGET" ]; then
            echo "Error: Missing endpoints or key"
            show_usage
            exit 1
        fi
        echo "Getting value for key: $TARGET"
        echo "============================="
        etcdctl --endpoints="$ENDPOINTS" get "$TARGET"
        ;;
        
    put)
        if [ -z "$ENDPOINTS" ] || [ -z "$TARGET" ] || [ -z "$VALUE" ]; then
            echo "Error: Missing endpoints, key, or value"
            show_usage
            exit 1
        fi
        echo "Putting value for key: $TARGET"
        echo "=============================="
        echo ">>> Old value (if exists):"
        etcdctl --endpoints="$ENDPOINTS" get "$TARGET" 2>/dev/null || echo "(key does not exist)"
        echo ""
        echo ">>> Writing new value..."
        etcdctl --endpoints="$ENDPOINTS" put "$TARGET" "$VALUE"
        echo ""
        echo ">>> New value:"
        etcdctl --endpoints="$ENDPOINTS" get "$TARGET"
        ;;
        
    delete)
        if [ -z "$ENDPOINTS" ] || [ -z "$TARGET" ]; then
            echo "Error: Missing endpoints or key"
            show_usage
            exit 1
        fi
        echo "Deleting key: $TARGET"
        echo "===================="
        echo ">>> Backup before delete:"
        etcdctl --endpoints="$ENDPOINTS" get "$TARGET" 2>/dev/null || echo "(key does not exist)"
        echo ""
        echo ">>> Deleting..."
        etcdctl --endpoints="$ENDPOINTS" del "$TARGET"
        echo ">>> Key deleted"
        ;;
        
    *)
        echo "Error: Unknown action '$ACTION'"
        show_usage
        exit 1
        ;;
esac