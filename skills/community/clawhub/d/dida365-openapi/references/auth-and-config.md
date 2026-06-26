# Auth And Config

## OAuth Flows

### Setup-only flow

Persist app settings before logging in:

```bash
python scripts/dida365.py auth setup \
  --client-id ... \
  --client-secret ... \
  --redirect-uri ...
```

This writes the provided non-default auth settings to `config.json` but does not contact the OAuth server.

### Manual flow

1. Run `python scripts/dida365.py auth authorize-url --client-id ... --redirect-uri ...`.
2. Open the returned `authorize_url` in a browser.
3. After Dida365 redirects back, copy the `code` query parameter.
4. Exchange it with `python scripts/dida365.py auth exchange-code --code ... --client-id ... --client-secret ... --redirect-uri ...`.

### Localhost flow

1. Run `python scripts/dida365.py auth login-local --client-id ... --client-secret ...`.
2. The CLI prints an authorization URL to stderr and starts an HTTP listener.
3. Open the URL in a browser and complete the OAuth flow.
4. The callback server captures `code`, verifies `state`, exchanges the code, and writes `token.json`.

`login-local` defaults to `http://127.0.0.1:36500/callback`. Override it with `--redirect-uri` only when the Dida365 app registration uses a different localhost callback URL.
Use Python 3.9 or newer for the bundled CLI.

## Config Precedence

The CLI resolves settings in this order:

1. CLI flags
2. Environment variables
3. Local files

This applies to:

- `client_id`
- `client_secret`
- `redirect_uri`
- `scope`
- `access_token`
- `auth_base_url`
- `api_base_url`

## Environment Variables

- `DIDA365_CLIENT_ID`
- `DIDA365_CLIENT_SECRET`
- `DIDA365_REDIRECT_URI`
- `DIDA365_SCOPE`
- `DIDA365_ACCESS_TOKEN`
- `DIDA365_AUTH_BASE_URL`
- `DIDA365_API_BASE_URL`

## Local Files

Default config directory:

`~/.config/dida365-openapi/`

Files:

- `config.json`: stores resolved auth settings such as `client_id`, `client_secret`, `redirect_uri`, `scope`, and optional base URLs.
- `token.json`: stores the raw token response from Dida365. The CLI only requires `access_token`, but it preserves any extra fields returned by the server.

The CLI redacts `client_secret`, `access_token`, and `refresh_token` when printing status to the terminal.

## Notes

- The bundled CLI does not auto-open a browser in v1. It prints the authorization URL and waits for the user to open it.
- The CLI does not implement automatic refresh-token handling in v1 because the provided official docs do not document a refresh flow.
- `auth clear-token` only deletes the cached token file. It does not modify environment variables.
- `auth setup` is useful when you want the agent to save resolved auth settings once and keep later commands shorter.
