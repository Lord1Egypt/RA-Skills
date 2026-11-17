# Manage doxx.net Tunnels

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users manage their doxx.net tunnels. Each tunnel represents a device on the network.


## API convention

**Auth token -- never enters the AI conversation.**

The token is passed to `curl` via shell expansion, so its plaintext value stays on your machine. Two sources, checked in this order:

1. `$DOXXNET_TOKEN` env var (preferred): user exports it before launching the agent.
2. `~/.config/doxxnet/token` file: used automatically if the env var is unset.

curl commands below use `${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}`, so both work transparently. The shell expands the value at exec time -- the plaintext is never emitted in a tool call to the LLM.

**Config API**: POST to `https://config.doxx.net/v1/`:
```
curl -s -X POST https://config.doxx.net/v1/ -d "ENDPOINT=1&param=value&token=${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}"
```

## Endpoints

- `list_tunnels`: list all tunnels with IPs, servers, and connection status
- `create_tunnel`: create a generic WireGuard tunnel (desktop/server). Params: `server` (required), `name`
- `create_tunnel_mobile`: create a generic WireGuard mobile tunnel (non-native clients). Params: `server`, `name`, `device_type` (mobile/web)
- `create_native_tunnel`: create/refresh a tunnel for the doxx.net native iOS/Android app (build 555+). Enforces subscription. Required params: `device_hash` (from `device_list_unified` or `list_tunnels`), `server`, `device_type` (mobile/web). Optional: `name`. NOTE: native app tunnels do NOT use WireGuard QR codes: the app manages its own connection. Clears `active_profile_id` on the tunnel.
- `update_tunnel`: update settings. Params: `tunnel_token` (required), `name`, `server`, `firewall`, `ipv6_enabled`, `block_bad_dns`
- `delete_tunnel`: delete a tunnel (permanent). Params: `tunnel_token`
- `wireguard`: get WireGuard config (generic WireGuard tunnels only: do NOT call on native tunnels). Params: `tunnel_token`
- `disconnect_peer`: force-disconnect a peer. Params: `tunnel_token`
- `servers`: list available servers (no auth needed)
- `generate_qr`: generate QR code (binary PNG response, no auth). Params: `data`, optional: `size`. Use `curl -s ... -o file.png`

## Client installation

After getting a WireGuard config with `wireguard=1`, build a .conf file:

```
[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {public_key}
AllowedIPs = {allowed_ips}
Endpoint = {endpoint}
PersistentKeepalive = 25
```

**macOS:** Write to `/etc/wireguard/doxx.conf`, run `sudo wg-quick up doxx`
**iOS/Android (generic WireGuard client):** Generate QR code with `generate_qr`, scan in WireGuard app

## Guidelines

**Tunnel type guide: important:**
- doxx.net native iOS/Android app → `create_native_tunnel` (requires `device_hash` from `device_list_unified` or `list_tunnels`). No WireGuard config or QR code needed: app handles connection. The tunnel record `type` field will still show `"wireguard"` (the protocol); the "native" distinction is at the client level, not the record.
- Generic WireGuard client (WireGuard app, any platform) → `create_tunnel` or `create_tunnel_mobile`, then `wireguard` to fetch config, then `generate_qr` for QR code.
- Never call `wireguard` endpoint on a native-app tunnel: it will fail if `assigned_ip` is NULL. If a user asks for a WireGuard QR and they have a native tunnel, clarify which type they need.
- `create_native_tunnel` clears `active_profile_id` on the tunnel: do not apply profiles after calling it.

- Always list tunnels first to show current state before making changes
- When creating tunnels, suggest the nearest server based on the user's context
- When moving a tunnel to a new server, explain that the WireGuard config changes and needs to be re-installed
- Always check API response `status` field: HTTP 200 can still be an error
- Confirm with user before deleting tunnels
