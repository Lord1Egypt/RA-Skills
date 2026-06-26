#!/usr/bin/env bash
# Start GateCrash Forms HTTP server

set -e

PORT="${1:-3000}"

echo "🚀 Starting GateCrash Forms server on port $PORT..."
gatecrash-forms serve "$PORT"
