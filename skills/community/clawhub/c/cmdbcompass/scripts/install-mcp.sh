#!/usr/bin/env bash
# CMDB Compass MCP Server - Install Script
# Source: https://github.com/cmdbcompass/cmdbcompass
# Package: https://pypi.org/project/cmdb-compass
#
# This script installs the cmdb-compass Python package from PyPI.
# It does not collect, transmit, or store any credentials.
# Credentials are configured locally by the user in their MCP client.

set -e

echo "Installing CMDB Compass MCP server..."
echo "Source: https://pypi.org/project/cmdb-compass"
echo ""

# Check Python 3.10+
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
  echo "Error: Python 3 is required. Install it from https://python.org" >&2
  exit 1
fi

PY_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
  echo "Error: Python 3.10+ is required. Found: $PY_VERSION" >&2
  exit 1
fi

echo "Python $PY_VERSION found."

# Install from PyPI
echo "Running: pip install cmdb-compass"
$PYTHON -m pip install --upgrade cmdb-compass

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo ""
echo "  1. Add to your MCP client config:"
echo '     {'
echo '       "mcpServers": {'
echo '         "cmdbcompass": {'
echo '           "command": "python",'
echo '           "args": ["-m", "servicenow_mcp.server"],'
echo '           "env": {'
echo '             "SERVICENOW_INSTANCE_URL": "https://your-instance.service-now.com",'
echo '             "SERVICENOW_USERNAME": "your_username",'
echo '             "SERVICENOW_PASSWORD": "your_password"'
echo '           }'
echo '         }'
echo '       }'
echo '     }'
echo ""
echo "  Credentials are stored locally in your MCP client config only."
echo "  They are passed directly to your ServiceNow instance."
echo ""
echo "  2. Restart your MCP client and connect to your ServiceNow instance."
echo ""
echo "  Documentation: https://github.com/cmdbcompass/cmdbcompass"
