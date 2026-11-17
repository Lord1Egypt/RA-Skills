# Manage doxx.net Tokens

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users manage their doxx.net auth tokens: create scoped tokens for agents or team members, revoke compromised tokens, set expiration, restrict by country or IP, and limit to specific tunnels.


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

Most token management endpoints require **admin** role. `user_list_tokens` is available to all roles.

## Endpoints

### Listing
- `user_list_tokens`: list all tokens for the account. Returns: `tokens[]` with `token` (full token string -- use directly as `target_token` in other operations), `label`, `role`, `created_at`, `expires_at`, `revoked_at`, `is_current`, `geo_fence[]`, `ip_fence[]`

### Creating and updating (admin only)
- `create_token`: create a new token. Optional params: `label` (max 64 chars), `role` (`admin`/`net-admin`/`read-only`, default `read-only`), `expires_at` (RFC3339). Returns: `new_token` (shown once, store securely)
- `update_token`: update label, role, or expiry. Params: `target_token` (required), optional: `label`, `role`, `expires_at` (RFC3339 or `never`). Can reactivate expired tokens.
- `revoke_token`: soft-revoke immediately. Params: `target_token` (required). Cannot revoke your own active token or the last admin token on the account. Revoked tokens remain in `user_list_tokens` with `revoked_at` set.
- `unrevoke_token`: re-enable a revoked token. Params: `target_token` (required). Only works on revoked tokens. Restores original role, fences, and settings.
- `delete_token`: permanently hard-delete a token and all its fences. Params: `target_token` (required). Cannot delete your own active token or the last admin token. Token will no longer appear in `user_list_tokens`.

### Geo fencing (admin only)
When a token has geo fence entries, it can only be used from those countries (GeoIP lookup).
- `add_geo_fence`: params: `target_token`, `country` (ISO 3166-1 alpha-2, e.g. `US`). Optional: `label`
- `remove_geo_fence`: params: `target_token`, `country`. Removing all entries removes the restriction.

### IP fencing (admin only)
When a token has IP fence entries, it can only be used from matching IPs/CIDRs.
- `add_ip_fence`: params: `target_token`, `cidr` (IPv4/IPv6 address or CIDR, e.g. `203.0.113.0/24`). Optional: `label`. Bare IPs normalized to /32 or /128.
- `remove_ip_fence`: params: `target_token`, `cidr` (must match stored value exactly). Removing all entries removes the restriction.

## Roles

| Role | Can do |
|------|--------|
| `admin` | Everything, including token management |
| `net-admin` | All tunnel/network operations, no token management |
| `read-only` | Read-only access to all resources |

## Guidelines

- Always call `user_list_tokens` first to show the current token landscape before making changes
- When creating tokens for AI agents or automation: suggest `net-admin` role + expiration + IP fence for least privilege
- Strongly warn users when they revoke a token that is currently in use (they will need to update their configuration)
- `new_token` from `create_token` is shown only once -- remind users to store it securely before moving on
- When a user asks to "rotate" their token: create a new admin token first, then revoke the old one in that order
- `revoke_token` is reversible (use `unrevoke_token`); `delete_token` is permanent -- prefer revoke unless the user explicitly wants to purge the token entirely

## Account Recovery

When a user redeems any recovery code (`verify_account_recovery`), the system performs a **nuclear revoke**: every token on the account is immediately revoked (assumes compromise). A single new admin token is generated and returned -- this is the only way back in.

**Post-recovery workflow:**
1. User receives the new admin token from the recovery code redemption
2. Log into the portal at `a0x13.doxx.net` using the new token to investigate
3. Call `user_list_tokens` to see all revoked tokens with their labels, roles, and `created_at` dates
4. For each token: decide whether it was trusted (unrevoke) or potentially compromised (leave revoked or delete)
5. Use `unrevoke_token` to restore trusted tokens one by one
6. Use `delete_token` to permanently purge tokens that should never be used again
7. Consider adding IP fencing to restored tokens before re-enabling them if the compromise vector is unknown
- Suggest IP fencing for tokens used from known fixed IPs (servers, CI systems)
- For geo fencing: note that GeoIP lookup failure allows the request by default
- Always check API response `status` field -- HTTP 200 can still be an error
