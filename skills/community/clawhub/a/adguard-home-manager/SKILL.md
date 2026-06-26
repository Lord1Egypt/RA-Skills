---
name: adguard-home
description: Manage AdGuard Home network-wide DNS ad blocking. Query blocklist stats, add/remove custom DNS rules, check filtering status, and view top blocked domains from your self-hosted DNS server.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - ADGUARD_USERNAME
        - ADGUARD_PASSWORD
        - ADGUARD_BASE_URL
      bins:
        - curl
        - jq
    primaryEnv: ADGUARD_PASSWORD
    emoji: "🛡️"
    homepage: https://github.com/Adguard/AdGuardHome
---

# AdGuard Home

Manage [AdGuard Home](https://adguard.com/adguard-home/overview.html) — the network-wide DNS server that blocks ads, trackers, and malware for your entire network.

## Setup

1. Install AdGuard Home on your VPS or home server
2. Create a user for the agent: Settings → AdGuard Home → Users → Add User
3. Get your base URL (e.g. `http://192.168.1.1:3000` or `https://your-vps.example.com`)
4. Export env vars:

```bash
export ADGUARD_USERNAME=your_username
export ADGUARD_PASSWORD=your_password
export ADGUARD_BASE_URL=http://192.168.1.1:3000
```

## Tools

### `status`

Get overall AdGuard Home status — DNS status, filtering enabled, protection level.

```bash
adguard-home-status
```

### `stats`

Get filtering statistics: total blocked, allowed, queries today, top blocked domains.

```bash
adguard-home-stats [period]   # period: hour, day, week, month, year (default: day)
```

### `blocked_domains`

Get the most frequently blocked domains.

```bash
adguard-home-blocked-domains [limit]   # default: 20
```

### `add_rule`

Add a custom DNS blocking rule.

```bash
adguard-home-add-rule "<domain or rule>"
# Examples:
#   adguard-home-add-rule "example.com"           # block single domain
#   adguard-home-add-rule "||example.com^"       # AdGuard blocking syntax
#   adguard-home-add-rule "@||example.com^"      # allowlist exception
```

### `remove_rule`

Remove a custom DNS rule by content.

```bash
adguard-home-remove-rule "<rule>"
```

### `list_rules`

List all custom DNS rewrite rules.

```bash
adguard-home-list-rules
```

### `query_log`

Query the DNS query log — find what domains were resolved on the network.

```bash
adguard-home-query-log [domain_filter] [limit]
# Example: adguard-home-query-log "ads" 50
```

### `toggle_filtering`

Enable or disable DNS filtering (ad blocking).

```bash
adguard-home-toggle-filtering true   # or false
```

## Notes

- AdGuard Home API: `https://github.com/AdguardTeam/AdGuardHome/wiki/Config#web-interface`
- Authentication uses HTTP Basic Auth with username:password
- Rate limiting: avoid querying the query_log with very large limits
- DNS rewrite rules can create custom DNS responses (A, AAAA, CNAME records)
