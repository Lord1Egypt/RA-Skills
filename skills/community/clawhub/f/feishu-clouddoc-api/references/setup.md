# Setup

## OpenClaw Bot Routing

Use this skill with one Feishu bot account per OpenClaw agent when possible.

1. Create a Feishu app in the developer console and enable bot capability.
2. Record the app ID and app secret in the target user's secret store or `.env`; do not write them into the skill.
3. Add an OpenClaw Feishu account with a user-chosen account ID, for example `feishu-main`, `pm-bot`, or `copywriter-bot`.
4. Set the account fields outside the skill: `enabled=true`, `domain=feishu`, `connectionMode=websocket`, app ID, and app secret.
5. Bind the account to an agent:

```bash
openclaw agents bind --agent <agent-id> --bind feishu:<account-id>
```

6. Restart or reload the OpenClaw gateway, then check:

```bash
openclaw agents bindings
openclaw channels status --probe
```

Do not change the default Feishu account unless the user explicitly wants the main bot moved. For new sub-agents, add a second account and bind only that account.

## Credential Model

The helper supports two authentication modes:

- Tenant/app token: uses `FEISHU_APP_ID` and `FEISHU_APP_SECRET`. This is enough for many read/write operations on resources the app can access.
- User token: uses `FEISHU_USER_ACCESS_TOKEN`. Use this for user-owned document creation and actions that must happen as the user.

Do not store real secrets in the skill. Keep them in `.env` or the target agent's secret store.

## API-Only Policy

Document-like operations must use OpenAPI calls through this skill:

- Docx: `scripts/feishu_openapi_tool.py` or `scripts/feishu_service_tool.py`
- Sheets, Base, Wiki, Drive, IM: `scripts/feishu_service_tool.py`
- OAuth token acquisition and refresh: `scripts/feishu_oauth_tool.py`

Do not use `lark-cli`, Feishu CLI tools, browser cookies, or browser automation as the implementation path for document operations. The OpenClaw CLI is only for OpenClaw account routing, bindings, and status checks.

## Minimum App Setup

1. Create a Feishu/Lark app in the developer console.
2. Add the OpenAPI permissions needed by the target operations.
3. Publish or re-authorize the app after permission changes.
4. Put `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, and `FEISHU_BASE_URL` in `.env`.
5. For user-owned document creation, complete OAuth or device authorization and set `FEISHU_USER_ACCESS_TOKEN`.

For IM event handling, enable the message events required by OpenClaw. For OpenAPI calls, add only the scopes required by the operations being used, such as Docs, Drive, Sheets, Base, Wiki, or IM.

## Getting User Tokens

`FEISHU_USER_ACCESS_TOKEN` is obtained through Feishu OAuth authorization code flow.

1. In the Feishu app, add the needed OpenAPI permissions and publish or re-authorize the app.
2. If the token must refresh automatically, add `offline_access` and include it in `FEISHU_OAUTH_SCOPE`.
3. In the app security settings, add the exact redirect URI you will use.
4. Put the same redirect URI in `.env`:

```bash
FEISHU_OAUTH_REDIRECT_URI=https://example.com/oauth/feishu/callback
FEISHU_OAUTH_SCOPE=offline_access docx:document
```

5. Generate an authorization URL:

```bash
python scripts/feishu_oauth_tool.py auth-url --env-file .env
```

6. Open the returned `authorization_url`, finish authorization, and copy the full callback URL from the browser address bar. Then exchange the code:

```bash
python scripts/feishu_oauth_tool.py exchange-code --env-file .env --callback-url "$CALLBACK_URL"
```

The script writes user tokens to `FEISHU_USER_TOKEN_FILE` when set, otherwise to a shared local token store under `~/.openclaw/feishu-user-tokens/`, and records that path back into `.env`.

To refresh manually:

```bash
python scripts/feishu_oauth_tool.py refresh --env-file .env
```

The authorization `code` is valid for a short time and can only be exchanged once. If exchange fails because the code is expired or already used, generate a new authorization URL.

## Token Expiry Rules

- Use `expires_in` from the token response to compute `FEISHU_USER_ACCESS_TOKEN_EXPIRES_AT`.
- Use `refresh_token_expires_in` from the token response to compute `FEISHU_USER_REFRESH_TOKEN_EXPIRES_AT`; accept `refresh_expires_in` only for older SDK or legacy responses.
- Do not hard-code the lifetime. Feishu can return different values.
- Refresh user tokens before expiry when `FEISHU_USER_REFRESH_TOKEN` is present.
- A `refresh_token` can be used only once. After refresh, replace both the local access token and refresh token with the newly returned values.
- If the refresh token is expired, missing, revoked, or the user lost app access, restart the OAuth authorization flow.

## Ownership Policy

When creating docs, sheets, bases, wiki pages, or drive resources:

- Default target owner is the requesting user.
- Prefer a user token and a user-owned folder token.
- If only app-token creation is available, stop and say the resource may be app-owned unless the user explicitly accepts that.
- Do not treat "shared with user" as equivalent to "owned by user".

For `scripts/feishu_openapi_tool.py create-doc` and `scripts/feishu_service_tool.py doc-create`, the default is user-token creation. Pass `--allow-app-owned` only after the user confirms app ownership is acceptable.

## Permission Troubleshooting

If a read or write call fails:

- Confirm the document token is from the correct URL segment, such as `/docx/{token}`.
- Confirm the app has access to the document or folder.
- Confirm the tenant has re-authorized the app after scope changes.
- For user-token calls, refresh or reissue `FEISHU_USER_ACCESS_TOKEN` if expired.
- For media upload, verify the Drive or Docx media upload scope separately.
- If OpenClaw receives no messages, check Feishu app event subscriptions, websocket status, the account binding, and gateway logs before changing DNS or model settings.
- If DNS resolution to `open.feishu.cn` fails on a machine, fix that machine's network or DNS layer separately; do not hard-code private DNS patches in the shared skill.
