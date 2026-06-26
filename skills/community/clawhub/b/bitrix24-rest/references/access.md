# Access and Auth

## Webhook Setup

The webhook URL is provided via `BITRIX24_WEBHOOK_URL` environment variable. OpenClaw users configure it as `apiKey` in `openclaw.json`.

To create a webhook:

1. In Bitrix24 open `Developer resources -> Other -> Inbound webhook`.
2. Create a webhook and copy its URL.
3. Provide it to your administrator to configure in the agent's settings.

Expected format:

```text
https://your-portal.bitrix24.ru/rest/<user_id>/<webhook>/
```

## Agent Setup Behavior

If a REST call fails because the webhook is not configured:

1. Tell the user once: "Webhook не настроен. Попросите администратора указать его в настройках."
2. Run `scripts/check_webhook.py --json` for diagnostics if the webhook IS configured but calls fail.

Mask the webhook secret in user-facing output.

## Permissions

Grant the permission groups that match the methods you will call.

Recommended full-coverage set:

- CRM
- Tasks
- Calendar
- Disk or Drive
- IM or Chat
- User and department access

## `CLIENT_ID` For Bot Integrations

For `imbot` integrations, Bitrix24 bot registration requires `CLIENT_ID`.

- Provide `CLIENT_ID` when registering the bot
- Persist it as part of the bot credentials
- Pass the same `CLIENT_ID` into all later `imbot.*` calls
- Treat `CLIENT_ID` as a secret

## Official MCP Docs Endpoint

```text
https://mcp-dev.bitrix24.tech/mcp
```

Tools exposed by the server:

- `bitrix-search`
- `bitrix-app-development-doc-details`
- `bitrix-method-details`
- `bitrix-article-details`
- `bitrix-event-details`

## When To Use OAuth Instead Of A Webhook

Use a webhook when:

- you are connecting one portal quickly
- the integration is admin-managed
- you want the shortest setup path

Use OAuth when:

- your service lives outside Bitrix24
- users connect their own portals to your service
- you need renewable tokens instead of a fixed webhook secret

Key official docs:

- Full OAuth: `https://apidocs.bitrix24.ru/settings/oauth/index.html`
- REST call overview: `https://apidocs.bitrix24.ru/sdk/bx24-js-sdk/how-to-call-rest-methods/index.html`
- Install callback: `https://apidocs.bitrix24.ru/settings/app-installation/mass-market-apps/installation-callback.html`

## OAuth Facts From MCP Docs

- Authorization server: `https://oauth.bitrix24.tech/`
- Authorization starts at `https://portal.bitrix24.com/oauth/authorize/`
- Temporary authorization `code` is valid for 30 seconds
- Token exchange at `https://oauth.bitrix24.tech/oauth/token/`
- Returns `access_token`, `refresh_token`, `client_endpoint`, `server_endpoint`, `scope`

Useful MCP titles for auth topics:

- `Полный протокол авторизации OAuth 2.0`
- `Упрощенный вариант получения токенов OAuth 2.0`
- `Вызов методов REST`
- `Callback установки`

## Install Callback For UI-Less Apps

If you build a local or UI-less app, Bitrix24 can POST OAuth credentials to an install callback URL. That flow is documented in `Callback установки`.

- Save the received `access_token` and `refresh_token`
- Refresh access tokens on your backend
- Do not rely on browser-side JS install helpers for the callback flow
