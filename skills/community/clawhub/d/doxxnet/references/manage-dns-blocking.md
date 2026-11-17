# Manage doxx.net DNS Blocking

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users configure DNS-level ad/tracker/malware blocking on their doxx.net tunnels, plus Secure DNS (DoH/DoT) for devices not on the tunnel.


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

- `dns_get_options`: list available blocklists (no auth needed)
- `dns_get_tunnel_config`: get a tunnel's DNS blocking config. Params: `tunnel_token`
- `dns_set_subscription`: enable/disable a blocklist. Params: `tunnel_token`, `blocklist_name`, `enabled` (1/0). Optional: `apply_to_all`
- `dns_add_whitelist`: whitelist a domain (stop blocking it). Params: `tunnel_token`, `domain`. Optional: `apply_to_all`
- `dns_remove_whitelist`: remove from whitelist. Params: `tunnel_token`, `domain`
- `dns_add_blacklist`: blacklist a domain (force block it). Params: `tunnel_token`, `domain`. Optional: `apply_to_all`
- `dns_remove_blacklist`: remove from blacklist. Params: `tunnel_token`, `domain`
- `dns_blocklist_stats`: blocklist statistics (no auth needed)
- `dns_get_all_tunnel_configs`: get DNS config across all tunnels in one call (no per-tunnel token needed)
- `dns_get_user_custom_rules`: get all custom blacklist/whitelist entries across all tunnels. Optional: `domain` (substring filter)
- `dns_get_user_subscriptions`: get all blocklist subscriptions across all tunnels with per-list summary
- `public_dns_create_hash`: create Secure DNS hash. Params: `tunnel_token`
- `public_dns_list_hashes`: list Secure DNS hashes
- `public_dns_delete_hash`: delete a hash. Params: `host_hash`
- `list_tunnels`: list tunnels (to find tunnel tokens)

## Secure DNS setup

After creating a hash with `public_dns_create_hash`, provide setup instructions:

- **iOS:** Settings → General → VPN & Device Management → DNS → add DoH URL
- **Android:** Settings → Network → Private DNS → enter DoT hostname (`HASH.sdns.doxx.net`)
- **Chrome:** Settings → Security → Use secure DNS → Custom → DoH URL
- **Firefox:** Settings → Network → DNS over HTTPS → Custom → DoH URL

## Guidelines

- Show current DNS config before making changes
- When enabling blocklists, recommend defaults: ads, tracking, malware
- When a user reports a site is broken, suggest whitelisting the specific domain
- Use `apply_to_all` parameter when the user wants consistent blocking across all devices
- If user has multiple tunnels, ask which to configure (or offer apply_to_all)
- For cross-tunnel overview queries ("show all my DNS rules", "what blocklists am I using"), prefer the bulk endpoints (`dns_get_all_tunnel_configs`, `dns_get_user_custom_rules`, `dns_get_user_subscriptions`) over looping per-tunnel calls
