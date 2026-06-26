#!/bin/bash
# Quick IAP health monitoring script
# Usage: ./scripts/quick-monitor.sh <cluster-name> <vc-ip> [categories] [password]

set -e

CLUSTER_NAME=${1:-"office-iap"}
VC_IP=${2:-"192.168.20.56"}
CATEGORIES=${3:-"system ap clients wlan rf arm wired logging security"}
SSH_PASSWORD=${4:-""}

OUTPUT_DIR="./monitor/$(date +%Y%m%d_%H%M%S)"

echo "📊 Monitoring IAP cluster: ${CLUSTER_NAME}"
echo "🌐 Virtual Controller: ${VC_IP}"
echo "📁 Output directory: ${OUTPUT_DIR}"
echo "📋 Categories: ${CATEGORIES}"
echo ""

# Build monitor command
MONITOR_CMD="iapctl monitor-cmd --cluster ${CLUSTER_NAME} --vc ${VC_IP} --out ${OUTPUT_DIR} --categories ${CATEGORIES}"

# Add password if provided
if [ -n "${SSH_PASSWORD}" ]; then
    MONITOR_CMD="${MONITOR_CMD} --ssh-password ${SSH_PASSWORD}"
fi

# Run monitor command
${MONITOR_CMD}

# Check result
if [ -f "${OUTPUT_DIR}/result.json" ]; then
    echo ""
    echo "✅ Monitoring completed successfully!"
    echo ""
    echo "📦 Artifacts generated:"
    ls -lh "${OUTPUT_DIR}/raw/"
    echo ""
    echo "📄 Result summary:"
    cat "${OUTPUT_DIR}/result.json" | python3 -m json.tool | grep -E '"action"|"cluster"|"vc"|"ok"|"timing"|"artifacts"'

    # Check for any errors or warnings
    ERRORS=$(cat "${OUTPUT_DIR}/result.json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(len(data.get('errors', [])))")
    WARNINGS=$(cat "${OUTPUT_DIR}/result.json" | python3 -c "import json, sys; data=json.load(sys.stdin); print(len(data.get('warnings', [])))")

    if [ "${ERRORS}" -gt 0 ]; then
        echo ""
        echo "❌ Errors detected: ${ERRORS}"
        cat "${OUTPUT_DIR}/result.json" | python3 -c "import json, sys; data=json.load(sys.stdin); [print(f'  - {e}') for e in data.get('errors', [])]"
    fi

    if [ "${WARNINGS}" -gt 0 ]; then
        echo ""
        echo "⚠️  Warnings: ${WARNINGS}"
        cat "${OUTPUT_DIR}/result.json" | python3 -c "import json, sys; data=json.load(sys.stdin); [print(f'  - {w}') for w in data.get('warnings', [])]"
    fi

    echo ""
    echo "📊 Quick health check:"

    # Check AP status
    if [ -f "${OUTPUT_DIR}/raw/show_ap_database.txt" ]; then
        AP_COUNT=$(grep -c "^" "${OUTPUT_DIR}/raw/show_ap_database.txt" || echo "0")
        echo "  - APs: ${AP_COUNT}"
    fi

    # Check client count
    if [ -f "${OUTPUT_DIR}/raw/show_user-table.txt" ]; then
        CLIENT_COUNT=$(grep -c "^" "${OUTPUT_DIR}/raw/show_user-table.txt" || echo "0")
        echo "  - Clients: ${CLIENT_COUNT}"
    fi

    # Check interface status
    if [ -f "${OUTPUT_DIR}/raw/show_interface.txt" ]; then
        echo "  - Interfaces: UP"
    fi

    echo ""
    echo "💡 View full results: cat ${OUTPUT_DIR}/result.json"
    echo "💡 View raw outputs: ls -la ${OUTPUT_DIR}/raw/"
else
    echo ""
    echo "❌ Monitoring failed! Check errors above."
    exit 1
fi
