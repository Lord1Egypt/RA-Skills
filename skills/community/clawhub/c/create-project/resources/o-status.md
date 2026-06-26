---
description: Show Orchestrix server status
---

# Orchestrix Status

Please check and display the current Orchestrix status:

## Status Check Items

1. **MCP Server Connection**: Check if Orchestrix MCP Server is connected
2. **Available Agents**: Call `list-agents` tool to verify agents are loaded
3. **License Status**: Display current license tier (if applicable)

## Expected Output

Display the status in this format:

```
Orchestrix Status
=================
Server: Connected / Disconnected
Agents: [count] agents available
License: [tier] mode

Available Commands:
  /o [agent]  - Activate agent
  /o-help     - Show help
  /o-status   - This status
```

## Troubleshooting

If the server is not connected:
1. Check `.mcp.json` configuration
2. Verify the MCP server process is running
3. Check server logs for errors
