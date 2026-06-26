---
name: authenticate-wallet
description: >
  Authenticate Agnic wallet via browser OAuth or headless API token.
  Use when the user wants to sign in, log in, authenticate, connect wallet,
  set up CLI, or resolve "Not authenticated" errors.
  Supports AGNIC_TOKEN env var for CI/server/agent environments.
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - "Bash(npx agnic@latest status*)"
  - "Bash(npx agnic@latest auth *)"
---

# Authenticating the Agnic Wallet

## Check Current Status

```bash
npx agnic@latest status --json
```

If already authenticated, no further action needed. If not, choose the appropriate mode below.

## Mode 1: Headless / Token Auth (CI, servers, agents)

Preferred when no browser is available. Generate an API token at [app.agnic.ai](https://app.agnic.ai) > Settings > API Tokens.

**Option A -- Environment variable** (recommended for automation):
```bash
export AGNIC_TOKEN=<your-api-token>
npx agnic@latest status --json
```

The CLI reads `AGNIC_TOKEN` automatically. All subsequent commands in the same shell session use it without extra flags.

**Option B -- Inline flag** (one-off commands):
```bash
npx agnic@latest --token <your-api-token> status --json
```

## Mode 2: Browser OAuth (interactive terminals)

Use when a browser is available:

```bash
npx agnic@latest auth login
```

This command:
1. Starts a temporary local server on a random port
2. Opens the default browser to the Agnic OAuth consent screen
3. The user signs in (email, Google, or wallet) and approves spending limits
4. The browser redirects back to `http://localhost:<port>/callback`
5. The CLI exchanges the authorization code for tokens and saves them locally

Wait for the CLI to print `Authenticated!` before proceeding.

## Verify Authentication

```bash
npx agnic@latest status --json
```

Expected output:

```json
{
  "authenticated": true,
  "userId": "did:privy:...",
  "email": "user@example.com",
  "walletAddress": "0x...",
  "tokenExpiry": "2026-05-22T14:30:00Z"
}
```

## Logout

To remove stored credentials:

```bash
npx agnic@latest auth logout
```

## Token Storage

- Browser mode: credentials stored in `~/.agnic/config.json` with `0600` permissions. Tokens auto-refresh on 401 responses. Refresh token expires after 90 days.
- Token mode: no local storage. The token is read from `AGNIC_TOKEN` env var or `--token` flag per invocation.

## Error Handling

- "Not authenticated" -- Set `AGNIC_TOKEN` env var, pass `--token`, or run `auth login`
- "Authentication failed" -- User cancelled the browser flow or the 5-min timeout expired
- "Could not open browser" -- The CLI prints a URL to copy and open manually
- "Token expired" -- Browser tokens auto-refresh; API tokens must be regenerated at app.agnic.ai
- "Invalid token" -- Check the token value; it may have been revoked or malformed
