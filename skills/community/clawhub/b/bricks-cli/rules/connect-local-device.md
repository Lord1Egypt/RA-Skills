# Connect to Local Device

Deploy a BRICKS application and connect to devices on the local network.

## Prerequisites: Enable Local Debugging on Device

The device must have **Local Debugging** enabled. Go to **System Menu → Advanced Setting** on the device and enable the following:

| Setting | English | 繁體中文 | 日本語 |
|---------|---------|----------|--------|
| Main toggle | Enable local debugging | 啟用 Local Debugging | ローカルデバッグを有効化 |
| LAN Discovery | Enable LAN Discovery | 啟用區域網路探索 | LAN探索を有効化 |
| MCP | Enable Model Context Protocol (MCP) | 啟用 Model Context Protocol (MCP) | Model Context Protocol (MCP)を有効化 |
| CDP *(optional)* | Enable Chrome DevTools Protocol (CDP) | 啟用 Chrome DevTools Protocol (CDP) | Chrome DevTools Protocol (CDP)を有効化 |

- **LAN Discovery** must be on for `bricks devtools scan` to find the device.
- **MCP** must be on for MCP bridging (step 3).
- A **Passcode** can be set in the same section (default: `BRICKS_DEVTOOLS`).

## 1. Discover Devices

Scan the LAN for DevTools-enabled devices:

```bash
bricks devtools scan -j
```

The JSON output includes `deviceId`, `name`, `address`, `port`, `workspaceId`, and `hasPasscode` for each device.

Filter to devices matching the current workspace — compare each device's `workspaceId` against the CLI profile's workspace (shown by `bricks auth status`). Ignore devices from other workspaces.

Options:
- `-t <ms>` — scan timeout (default 3000)
- `--verify` — verify each server via HTTP
- `--udp-only` — skip HTTP subnet probe

## 2. Bind Devices to App

Once you have the target device IDs, bind them to the application:

```bash
# Bind specific devices
bricks app bind <app-id> -b <device-id-1>,<device-id-2>

# Unbind devices
bricks app bind <app-id> -u <device-id>

# Bind and unbind in one call
bricks app bind <app-id> -b <new-device> -u <old-device>
```

After binding, the device will load the application on next refresh. Force an immediate reload:

```bash
bricks device refresh <device-id>
```

## 3. Connect via MCP for Debugging

Use [mcporter](https://mcporter.dev) to bridge the device's MCP endpoint so Claude Code (or other MCP clients) can interact with it directly:

```bash
mcporter call --url http://<device-ip>:19851/mcp --header "Authorization: Bearer <passcode>"
```

Through MCP tools you can check device status, read logs, trigger automations, and debug issues without leaving the agent workflow.
