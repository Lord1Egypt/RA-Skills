#!/bin/bash
# API Gateway Starter

ACTION="${1:-start}"

case $ACTION in
  start)
    echo "🚀 Starting API Gateway..."
    echo "📍 Default: http://localhost:8080"
    ;;
  add)
    echo "➕ Adding upstream: $2"
    ;;
  auth)
    echo "🔐 Configuring auth: $2"
    ;;
esac
