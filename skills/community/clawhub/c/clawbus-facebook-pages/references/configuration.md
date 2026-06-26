# Configuration

Read this file when the Facebook Pages script cannot find credentials or when
you need to confirm the default MyBrandMetrics API host.

## Supported config sources

The script supports these configuration sources:

1. Command-line arguments:
   - `--api-key`
   - `--access-token`
   - `--base-url`
   - `--page-id`
   - `--account-id`
   - `--connection-id`
   - `--config`
2. Environment variables:
   - `MBM_API_KEY`
   - `MBM_ACCESS_TOKEN`
   - `MBM_BASE_URL`
   - `FACEBOOK_PAGES_API_KEY`
   - `FACEBOOK_PAGES_ACCESS_TOKEN`
   - `FACEBOOK_PAGES_PAGE_ID`
   - `FACEBOOK_PAGES_ACCOUNT_ID`
   - `FACEBOOK_PAGES_CONNECTION_ID`
   - optional `FACEBOOK_PAGES_CONFIG`
3. A workspace `config.json` file with a `facebook_pages` object

Arguments take precedence over environment variables, and environment variables
take precedence over `config.json`.

## Authentication modes

The script supports either of these auth styles:

1. Bearer token auth:
   - send `Authorization: Bearer <token>`
   - recommended for the Facebook Pages endpoints described in this skill
2. API key auth:
   - send `X-API_KEY: <api_key>`
   - useful if your environment is already provisioned that way

If both are available, the script prefers the bearer token.

## Default base URL

The default API base URL is:

```text
https://api.mybrandmetrics.com
```

Override it with `--base-url` or `MBM_BASE_URL` only when you intentionally need
another environment.

## Expected config.json shape

```json
{
  "facebook_pages": {
    "access_token": "YOUR_ACCESS_TOKEN",
    "api_key": "YOUR_API_KEY",
    "base_url": "https://api.mybrandmetrics.com",
    "page_id": "YOUR_PAGE_ID",
    "account_id": "YOUR_ACCOUNT_ID",
    "connection_id": "YOUR_CONNECTION_ID"
  }
}
```

The script also accepts `authorization_token` as a fallback key name for the
bearer token.

## Security rules

- Never commit real access tokens, API keys, Page IDs, account IDs, or
  connection IDs into the repository.
- Prefer environment variables or runtime arguments in shared environments.
- Do not echo secrets in logs or terminal output.
