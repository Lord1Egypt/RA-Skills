#!/bin/bash
# Setup script for X5 MCP service
# This script must be run before using any X5 browser tools.

set -e

LOG_DIR="/usr/local/qb_logs"
LOG_FILE="${LOG_DIR}/mcp_log.log"
MCP_PORT=18009
MCP_CMD="x5use-linux-mcp"

# Create log directory
mkdir -p "${LOG_DIR}" 2>/dev/null || {
    echo "ERROR: Failed to create log directory ${LOG_DIR}. Please check permissions."
    exit 1
}

# Check if x5use-linux-mcp command exists
if ! command -v "${MCP_CMD}" &>/dev/null; then
    echo "ERROR: '${MCP_CMD}' command not found. Please ensure it is installed and available in PATH."
    exit 1
fi

# Check if x5use-linux-mcp is already running on the target port
if curl -s --max-time 2 "http://localhost:${MCP_PORT}/sse" >/dev/null 2>&1; then
    echo "X5 MCP service is already running on port ${MCP_PORT}."
    exit 0
fi

# Start x5use-linux-mcp service in background
echo "Starting X5 MCP service on port ${MCP_PORT}..."
${MCP_CMD} --transport sse --port ${MCP_PORT} --log-dir "${LOG_DIR}" >> "${LOG_FILE}" 2>&1 &
MCP_PID=$!

# Wait briefly and verify the process is still running
sleep 2
if ! kill -0 "${MCP_PID}" 2>/dev/null; then
    echo "ERROR: ${MCP_CMD} failed to start. Check logs at ${LOG_FILE}"
    exit 1
fi

echo "X5 MCP service started successfully (PID: ${MCP_PID})."
