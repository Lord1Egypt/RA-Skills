---
name: destinia
description: search hotels for your next trip
version: 1.0.0
triggers:
  - search hotel in New York for the next week for two adults
---

# Destinia

Search hotel prices and availability for you next trip.

## Manual setup

You need to install `mcporter` package as your mcp client to do so just execute this command
                                       
 ```                     
   npm install -g mcporter
 ```  

Then you can configure a conexion to Destinia inside mcporter's configuration file `~/.openclaw/workspace/config/mcporter.json`

The configuration you should as is this:

```
{
  "mcpServers": {
    "destinia": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.destinia.com/sse",
        "--header",
        "Authorization:Bearer <api_key>"
      ]
    }
  }
}
```

## Auto-setup

Alternatively you can ask openclaw to setup the mcp by itself using a prompt.

⚠️⚠️⚠️ Replace `<api_key>` with you api key before executing the prompt ⚠️⚠️⚠️

You can use a prompt like the following and openclaw will do all the magic for you:

```
Configure Destinia MCP server using this configuration:
{
  "mcpServers": {
    "destinia": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.destinia.com/sse",
        "--header",
        "Authorization:Bearer <api_key>"
      ]
    }
  }
}
```

# Request API key

To use your MCP you should request a free api key at:

https://destinia.com/en/developers