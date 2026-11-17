---
name: doxxnet
description: "Manage your doxx.net private network: tunnels, devices, firewall, domains, DNS blocking, IP addresses, profiles, account settings, bandwidth stats, and security alerts"
version: 1.0.0
homepage: https://github.com/doxxcorp/doxx-skills
user-invocable: true
metadata.openclaw: {"env": ["DOXXNET_TOKEN"], "bins": ["curl", "openssl", "dig", "wg-quick"], "primaryEnv": "DOXXNET_TOKEN"}
---

# doxx.net

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users manage all aspects of their doxx.net private network. Determine which API endpoints to call based on their request.

User request: $ARGUMENTS

## Help

If `$ARGUMENTS` is "help" or empty, print the following and ask what the user wants to do:

```
doxx.net -- what can I help with?

  Tunnels       Create, update, move, delete tunnels; get WireGuard configs
  Domains       Register domains, manage DNS records, import external domains, sign TLS certs
  Firewall      Open ports, link tunnels for mesh networking, manage access rules
  DNS Blocking  Enable blocklists, whitelist/blacklist domains, configure Secure DNS
  Devices       List, rename, change icons, delete devices
  IP Addresses  Assign, release, rotate IPs; lease dedicated IPv4; manage connection profiles
  Account       Recovery settings, notifications, recovery codes, subscription status
  Tokens        Create and manage auth tokens; set expiration, roles, geo/IP fences, tunnel scope
  Stats         Bandwidth usage, security alerts, threat categories, peak throughput
  Status        Tunnel and device connection dashboard

  /network-wizard  Set up a new private network from scratch (guided)
```

## API convention

**Auth token -- never enters the AI conversation.**

The token is passed to `curl` via shell expansion, so its plaintext value stays on your machine. Two sources, checked in this order:

1. `$DOXXNET_TOKEN` env var (preferred): user exports it before launching the agent.
2. `~/.config/doxxnet/token` file: used automatically if the env var is unset.

curl commands below use `${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}`, so both work transparently. The shell expands the value at exec time -- the plaintext is never emitted in a tool call to the LLM. All curl commands use it directly.

**Config API**: POST to `https://config.doxx.net/v1/`:
```
curl -s -X POST https://config.doxx.net/v1/ -d "ENDPOINT=1&param=value&token=${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}"
```

**Stats API**: POST to `https://secure-wss.doxx.net/api/stats/` with `X-Auth-Token` header:
```
curl -s -X POST https://secure-wss.doxx.net/api/stats/ENDPOINT -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "param=value"
```

**Special responses:** `sign_certificate` returns raw PEM (not JSON). `generate_qr` returns binary PNG: use `curl -s ... -o file.png`.

Always check the `status` field in JSON responses: HTTP 200 can still be an error.

## Tunnels

- `list_tunnels`: list all tunnels with IPs, servers, connection status
- `create_tunnel`: create a generic WireGuard tunnel (desktop/server). Params: `server` (required), `name`
- `create_tunnel_mobile`: create a generic WireGuard mobile tunnel (non-native clients). Params: `server`, `name`, `device_type` (mobile/web)
- `create_native_tunnel`: create/refresh a tunnel for the doxx.net native iOS/Android app (build 555+). Enforces subscription. Required params: `device_hash` (from `device_list_unified` or `list_tunnels`), `server`, `device_type` (mobile/web). Optional: `name`. NOTE: native app tunnels do NOT use WireGuard QR codes: the app manages its own connection. Clears `active_profile_id` on the tunnel.
- `update_tunnel`: params: `tunnel_token` (required), `name`, `server`, `firewall`, `ipv6_enabled`, `block_bad_dns`
- `delete_tunnel`: params: `tunnel_token` (permanent, confirm first)
- `wireguard`: get WireGuard config (generic WireGuard tunnels only: do NOT call on native tunnels). Params: `tunnel_token`
- `disconnect_peer`: force-disconnect. Params: `tunnel_token`
- `servers`: list available servers (no auth)
- `generate_qr`: QR code (binary PNG, no auth). Params: `data`, optional: `size`. Use `-o file.png`

WireGuard config format:
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
macOS: write to `/etc/wireguard/doxx.conf`, run `sudo wg-quick up doxx`. iOS/Android (generic WireGuard client): generate QR, scan in WireGuard app.

## Firewall

- `firewall_rule_list`: list rules. Optional: `tunnel_token`
- `firewall_rule_add`: params: `tunnel_token`, `protocol` (TCP/UDP/ICMP/ALL), `src_ip`, `src_port`, `dst_ip`, `dst_port`
- `firewall_rule_delete`: same params as add
- `firewall_link_all_toggle`: mesh networking on/off. Params: `enabled` (1/0)
- `firewall_link_all_status`: check mesh status

For mesh between two tunnels, create bidirectional rules (A->B and B->A). Prefer link-all for full mesh.

## Domains & DNS

- `list_tlds` — list all 196 available TLDs with categories (no auth)
- `list_domains`, `create_domain` (params: `domain`), `delete_domain`
- `list_dns` (params: `domain`), `create_dns_record`, `update_dns_record`, `delete_dns_record`
  - Record params: `domain`, `name` (FQDN), `type` (A/AAAA/CNAME/MX/TXT/NS/SRV/PTR), `content`. Optional: `ttl`, `prio`
- `get_domain_validation`: TXT code for external domain import
- `import_domain`: import after TXT verification. Params: `domain`, `validation_code`
- `link_profile_domain`: link a profile to a domain; creates A/AAAA records auto-updating with the profile's IPs. Params: `domain`, `hostname`, `profile_id`
- `unlink_profile_domain`: remove profile-domain link. Params: `profile_id`
- `sign_certificate`: sign a CSR (returns raw PEM). Params: `domain`, `csr`

Popular TLDs: `.lan`, `.vpn`, `.mesh`, `.home`, `.wg`, `.doxx`. Default is `.doxx`. Use `list_tlds` for the full list.

TLS workflow: `openssl ecparam -genkey -name prime256v1 -o D.key` → `openssl req -new -key D.key -out D.csr -subj "/CN=D"` → `sign_certificate`

## DNS Blocking

- `dns_get_options`: list available blocklists (no auth)
- `dns_get_tunnel_config`: current blocking config. Params: `tunnel_token`
- `dns_set_subscription`: enable/disable blocklist. Params: `tunnel_token`, `blocklist_name`, `enabled` (1/0). Optional: `apply_to_all`
- `dns_add_whitelist` / `dns_remove_whitelist`: params: `tunnel_token`, `domain`. Optional: `apply_to_all`
- `dns_add_blacklist` / `dns_remove_blacklist`: params: `tunnel_token`, `domain`. Optional: `apply_to_all`
- `dns_blocklist_stats`: blocklist statistics (no auth)

**Secure DNS (DoH/DoT)** for devices not on the tunnel:
- `public_dns_create_hash`: create hash. Params: `tunnel_token`
- `public_dns_list_hashes` / `public_dns_delete_hash` (params: `host_hash`)

## Devices

- `device_list_unified`: list all devices with subscription info and guest accounts. Returns: `my_devices[]`, `guest_accounts[]`, `subscription`
- `device_rename`: rename or change icon. Params: `device_hash`, `device_name`. Optional: `device_icon`
- `device_delete`: permanently delete device (removes tunnels, IPs, seats). Params: `target_device_hash`

DeviceInfo fields: device_hash, device_name, device_model, os_type, device_type, device_icon, is_current, is_online, last_seen, tunnel_count, has_seat, is_owner, can_remove, can_rename, can_delete

## IP Addresses

- `list_addresses`: list assigned IPs with type, location, tunnel, profile, connection status. Optional: `tunnel_token`, `device_hash`. Returns `public_ipv4_used`, `public_ipv4_max`
- `assign_address`: assign IP to profile. Params: `address`, `type`. Optional: `profile_id`
- `release_address`: release IP. Params: `address`, `type`
- `rotate_address`: rotate to new IP. Params: `address`, `type` (static_private or static_ipv6 only)
- `lease_public_ipv4`: lease dedicated public IPv4. Modes: (1) `profile_id`, (2) `profile_name`+`server`, (3) `server` alone. Optional: `ip_type`, `include_ipv6`
- `list_ip_reservations`: list dedicated IPv4 reservations with `slots_used`, `slots_max`
- `release_ip_reservation`: release a dedicated IP reservation. Params: `ip_address`

**Transparent profile handling for IPv4 leasing:**
When the user asks to lease a dedicated IP for a tunnel (without mentioning profiles):
1. Call `list_tunnels` to get the tunnel's `tunnel_token`, server, and name
2. Check the tunnel's `profile_id` -- if set, a profile already exists; use it
3. If no profile: call `create_saved_profile` silently using the tunnel's name, server, and `profile_type=wireguard`
4. Call `lease_public_ipv4` with the profile details
5. Call `load_profile` to apply the profile to the tunnel
6. Present the leased IP to the user -- do not expose profile mechanics unless they ask

Note: `create_native_tunnel` auto-creates a profile; `create_tunnel`/`create_tunnel_mobile` may not -- always check `profile_id` before creating.

## Saved Profiles

- `list_saved_profiles`: list profiles with settings and usage status
- `save_profile`: snapshot current tunnel settings into a new profile. Params: `tunnel_token`, `profile_name`. Optional: `profile_icon`, `save_preferred_server` (1), `lock_after_save` (1)
- `create_saved_profile`: create empty profile. Params: `profile_name`, `profile_icon`, `profile_type`, `server`
- `update_saved_profile`: update. Params: `profile_id`, and: `profile_icon`, `profile_name`, `preferred_server`. Re-snapshot: add `re_snapshot=1`, `tunnel_token`
- `delete_saved_profile`: delete. Params: `profile_id`
- `load_profile`: apply profile to tunnel. Params: `tunnel_token`, `profile_id`
- `lock_profile`: lock profile (IP/settings). Params: `profile_id` or `tunnel_token`. Optional: `lock_type` (`ip`/`settings`)
- `unlock_profile`: unlock profile. Params: `profile_id` or `tunnel_token`. Optional: `lock_type`
- `apply_mode`: apply a connection mode template to a tunnel without creating a profile. Params: `tunnel_token`, `settings` (JSON). Optional: `template_key`, `dns` (JSON). Returns: `template_key`, `mode`

## Account

- `get_profile`: get recovery email/phone, notification preferences, recovery code count
- `update_profile`: update. Params: `recovery_email`, `recovery_phone`, `notifications`
- `create_account_recovery`: generate recovery codes. Returns: `codes[]`. **Warning:** redeeming any recovery code triggers a nuclear revoke of all tokens on the account. A new admin token is issued to allow re-entry and selective token restoration.
- `subscription_status`: check subscription tier, status, pro features
- See also: token management is a separate capability -- use `user_list_tokens`, `create_token`, `revoke_token`, `update_token`, and fence/scope endpoints for API key management

## Tokens

Most token endpoints require **admin** role. `user_list_tokens` is available to any role.

- `user_list_tokens`: list all tokens with role, expiry, revocation status, and geo/IP fences. Returns full token string. `is_current` flags the calling token
- `create_token`: create a new token. Optional: `label`, `role` (`admin`/`net-admin`/`read-only`, default `read-only`), `expires_at` (RFC3339). Returns: `new_token` (shown once only)
- `revoke_token`: soft-revoke a token. Params: `target_token` (full string). Cannot revoke your own active token or the last admin token on the account
- `unrevoke_token`: re-enable a revoked token. Params: `target_token`
- `delete_token`: permanently delete a token and all its fences. Params: `target_token`. Cannot delete your own active token or the last admin token
- `update_token`: update label, role, or expiry. Params: `target_token`. Optional: `label`, `role`, `expires_at` (RFC3339 or `never`)
- `add_geo_fence` / `remove_geo_fence`: restrict token by country. Params: `target_token`, `country` (ISO 3166-1 alpha-2). Removing all entries removes restriction
- `add_ip_fence` / `remove_ip_fence`: restrict token by IP/CIDR. Params: `target_token`, `cidr`. Removing all entries removes restriction


**Token rotation:** create the new token first, then revoke the old one (never the reverse).
**Least privilege for agents:** `net-admin` role + expiration + IP fence.

## Stats

- `bandwidth`: usage over time. Params: `start`, `end` (ISO 8601), optional: `tunnel_token`
  ```
  curl -s -X POST https://secure-wss.doxx.net/api/stats/bandwidth -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "start=ISO8601&end=ISO8601"
  ```
  Returns: `data[]` with `peak_in`/`peak_out` (Mbps), `aggregate[]`

- `alerts`: security alerts and DNS blocks. Params: `last` (session/1m/1h/1d/7d/30d), optional: `tunnel_token`, `type`
  ```
  curl -s -X POST https://secure-wss.doxx.net/api/stats/alerts -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "last=1d"
  ```
  Returns: `totals`, `block_count`, `category_counts` (ads, tracking, malware), `data[]`

- `summary`: peak bandwidth + alert totals. Params: `days` (default: 30), optional: `tunnel_token`
  ```
  curl -s -X POST https://secure-wss.doxx.net/api/stats/summary -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "days=30"
  ```

- `global`: global threat counter (no auth, GET only)
  ```
  curl -s "https://secure-wss.doxx.net/api/stats/global"
  ```

Alert types: `dns_block`, `security_event`, `dangerous_port`, `dns_bypass`, `doh_bypass`, `port_scan`, `dns_nxdomain`

Time range shortcuts: "last hour" → `last=1h`, "today" → `last=1d`, "this week" → `last=7d`, "this month" → `last=30d`

## Guidelines

**Tunnel type guide: important:**
- doxx.net native iOS/Android app → `create_native_tunnel` (requires `device_hash` from `device_list_unified` or `list_tunnels`). No WireGuard config or QR code needed: app handles connection. The tunnel record `type` field will still show `"wireguard"` (the protocol); the "native" distinction is at the client level, not the record.
- Generic WireGuard client (WireGuard app, any platform) → `create_tunnel` or `create_tunnel_mobile`, then `wireguard` to fetch config, then `generate_qr` for QR code.
- Never call `wireguard` endpoint on a native-app tunnel: it will fail if `assigned_ip` is NULL. If a user asks for a WireGuard QR and they have a native tunnel, clarify which type they need.
- `create_native_tunnel` clears `active_profile_id` on the tunnel: do not apply profiles after calling it.

- Always list current state before making changes (`list_tunnels`, `list_domains`, `firewall_rule_list`)
- Call `list_tunnels` when you need tunnel names, IPs, or tokens
- Call `device_list_unified` when you need device info
- Call `list_addresses` for IP address queries
- Call `list_saved_profiles` for profile queries
- Confirm before device deletion and address release
- Confirm with user before destructive operations (delete tunnel, delete domain)
- Present stats in clear tables: convert bandwidth to Mbps, group alerts by category
- For multi-tunnel users, offer to filter by tunnel or show all
- When the request spans multiple areas, make all relevant API calls and present a unified answer
- When users say "VPN", understand they mean private network. Always respond using "network", "tunnel", or "private network" -- never echo "VPN" back in your responses

**Private network setup routing:**
If the user's request is to create, build, or set up a new private network from scratch ("build me a private network", "set up a network for my devices", "I want a private network", "set up a secure network"), respond:

> "I can walk you through that. Quick setup (connect a few devices, 5 min) or full setup (mesh network, custom domain, DNS blocking)?"

Then follow the network-wizard phases based on their answer:
- **Quick mode** (phases 1, 2, 3, 4, 7, 9): auth check, server selection, tunnel creation, mesh networking, client install, summary -- no prompts for optional features
- **Full mode** (all 9 phases): same as Quick, plus prompting the user about custom domain, DNS blocking, and secure DNS before each optional phase

Do not redirect to a separate skill -- handle it inline.

## Reference files

Before acting on one of these domains, read the matching reference file for the
full endpoint snapshot (the live schema at https://config.doxx.net/ still wins on conflict):

- `references/manage-account.md` — Manage doxx.net account: recovery settings, notifications, recovery codes, and subscription status
- `references/manage-addresses.md` — Manage doxx.net IP addresses and saved profiles: assign, release, rotate IPs, lease dedicated IPv4, create and manage connection profiles
- `references/manage-devices.md` — Manage doxx.net devices: list, rename, change icons, and delete devices
- `references/manage-dns-blocking.md` — Manage doxx.net DNS blocking: enable blocklists, whitelist/blacklist domains, configure Secure DNS, cross-tunnel DNS views
- `references/manage-domains.md` — Manage doxx.net domains: register, DNS records, TLS certificates, import external domains
- `references/manage-firewall.md` — Manage doxx.net firewall rules: open ports, link tunnels for mesh networking, manage access rules
- `references/manage-tokens.md` — Manage doxx.net auth tokens: create, revoke, update roles, set geo/IP fences, and scope tokens to specific tunnels
- `references/manage-tunnels.md` — Manage doxx.net tunnels: create, update, move, delete devices and get WireGuard configs
- `references/network-stats.md` — View doxx.net network stats: bandwidth usage, security alerts, threat categories, peak throughput
- `references/network-status.md` — Check doxx.net network status: bandwidth, connections, security alerts, tunnel status
- `references/network-wizard.md` — Set up a doxx.net private network: tunnels, mesh networking, domains, DNS blocking, and client installation
