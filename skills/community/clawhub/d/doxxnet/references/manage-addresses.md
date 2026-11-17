# Manage doxx.net Addresses & Profiles

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users manage their doxx.net IP addresses and saved connection profiles.


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

## IP Address Endpoints

- `list_addresses`: list all assigned IPs. Optional: `tunnel_token`, `device_hash`. Returns `addresses[]` with: address, type (static_public/static_private/static_ipv6), site_id, location, profile_id, profile_name, tunnel_token, tunnel_name, connected, device_name, persistent. Also returns `public_ipv4_used`, `public_ipv4_max`.
- `assign_address`: assign IP to a profile. Params: `address`, `type`. Optional: `profile_id` (omit to unassign)
- `release_address`: release an assigned IP. Params: `address`, `type`
- `rotate_address`: rotate to a new IP (releases current, assigns new). Params: `address`, `type` (static_private or static_ipv6 only -- public IPv4 cannot be rotated)
- `lease_public_ipv4`: lease a dedicated public IPv4. Three modes: (1) `profile_id` for existing profile, (2) `profile_name` + `server` to create new profile, (3) `server` alone for pool-only. Optional: `ip_type` (ipv6), `include_ipv6` (1). Returns: `ip_address`, `profile_id`, flags: `pool_only`, `profile_created`, `requires_reconnect`
- `list_ip_reservations`: list all dedicated public IPv4 reservations with slot usage. Returns `reservations[]` with `ip_address`, `server`, `profile_id`, `profile_name`, plus `slots_used`, `slots_max`
- `release_ip_reservation`: release a dedicated IP reservation (returns IP to pool, different from `release_address`). Params: `ip_address`

## Saved Profile Endpoints

- `list_saved_profiles`: list all profiles. Returns `profiles[]` with: profile_id, profile_name, profile_icon, profile_type (ios/wireguard/android), preferred_server, domain_name, created_at, updated_at, ipv4_public_enabled, onion_enabled, proxy_enabled, ip_locked, settings_locked, in_use, in_use_by, in_use_device_icon, source_tunnel_name
- `save_profile`: snapshot current tunnel settings (DNS blocklists, firewall, proxy, transport) into a new profile. Params: `tunnel_token`, `profile_name`. Optional: `profile_icon`, `save_preferred_server` (1), `lock_after_save` (1). Returns: `profile_id`
- `create_saved_profile`: create an empty profile (for static IP management). Params: `profile_name`, `profile_icon`, `profile_type` (wireguard), `server`
- `update_saved_profile`: update profile metadata. Params: `profile_id`. Optional: `profile_icon`, `profile_name`, `preferred_server`. For re-snapshot from tunnel: add `re_snapshot=1`, `tunnel_token`
- `delete_saved_profile`: delete. Params: `profile_id`
- `load_profile`: apply a profile to a tunnel. Params: `tunnel_token`, `profile_id`
- `lock_profile`: lock a profile to prevent IP/settings changes. Params: `profile_id` or `tunnel_token`. Optional: `lock_type` (`ip`, `settings`, or omit for both)
- `unlock_profile`: unlock a locked profile. Params: `profile_id` or `tunnel_token`. Optional: `lock_type`

## Context Endpoints

- `list_tunnels`: list tunnels (for tunnel tokens when applying profiles)
- `servers`: list available servers (for profile creation and IP leasing, no auth needed)

## Address Types

| Type | Description |
|------|-------------|
| `static_public` | Dedicated public IPv4 address |
| `static_private` | Static private network address |
| `static_ipv6` | Static IPv6 address |

## Guidelines

- Always list current addresses/profiles before making changes
- When leasing public IPv4, explain it's a dedicated IP that persists across reconnections
- When rotating, warn that the old IP is released and a new one assigned
- Confirm before releasing addresses (especially persistent/dedicated ones)
- Show which profiles are in_use and by which tunnel/device
- When creating profiles, list available servers for the user to choose
- Group addresses by type when presenting
- Always check API response `status` field: HTTP 200 can still be an error
