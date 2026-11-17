# EVE SSO OAuth2 Authentication

EVE ESI uses OAuth 2.0 Authorization Code flow via EVE SSO (Single Sign-On).

Base SSO URL: `https://login.eveonline.com`
Endpoint discovery: <https://login.eveonline.com/.well-known/oauth-authorization-server>

> **Everything on this page is a secret.** Authorization codes, access tokens,
> refresh tokens, client IDs and PKCE verifiers are all bearer credentials —
> whoever holds one can act as the character. The refresh token is the one that
> matters most: access tokens expire in ~20 minutes, refresh tokens do not
> expire on their own and grant continued access until revoked at
> <https://community.eveonline.com/support/third-party/>.
>
> Do not paste them into shell history, log files, CI output, config files under
> version control, or agent chat transcripts. In normal use you never handle
> them yourself: `auth_flow.py` writes them to `~/.openclaw/eve-tokens.json`
> (chmod 600) and `esi_query.py --char <name>` resolves them in-process without
> ever printing one. The examples below are the raw protocol, shown so the flow
> is auditable — not the recommended way to work with it.

## Prerequisites

1. Register an application at <https://developers.eveonline.com/applications>
2. Note your **Client ID** and **Secret Key**
3. Set the **Callback URL** to exactly `http://localhost:8080/callback` — this is
   what `auth_flow.py` sends, and SSO matches redirect URLs as literal strings.
   The developer portal accepts the `http` scheme *only* for the host
   `localhost`; an IP address such as `127.0.0.1` is rejected when you save the
   application. Using a different `--port`? Register that port's URL instead.
4. Select required **Scopes** for the endpoints you need

## Authorization Code Flow

### Step 1: Redirect user to SSO

```
https://login.eveonline.com/v2/oauth/authorize/?response_type=code&redirect_uri=<CALLBACK_URL>&client_id=<CLIENT_ID>&scope=<SCOPES>&state=<RANDOM_STATE>
```

- `scope`: space-separated list (e.g. `esi-wallet.read_character_wallet.v1 esi-assets.read_assets.v1`)
- `state`: random string to prevent CSRF

### Step 2: Exchange authorization code for tokens

```bash
curl -X POST https://login.eveonline.com/v2/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=<AUTH_CODE>" \
  -d "client_id=<CLIENT_ID>" \
  -d "code_verifier=<CODE_VERIFIER>"
```

Response:

```json
{
  "access_token": "eyJ...",
  "expires_in": 1199,
  "token_type": "Bearer",
  "refresh_token": "abc123..."
}
```

### Step 3: Refresh expired tokens

Access tokens expire after ~20 minutes. Refresh with:

```bash
curl -X POST https://login.eveonline.com/v2/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=<REFRESH_TOKEN>" \
  -d "client_id=<CLIENT_ID>"
```

### Step 4: Verify token and get character ID

```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "User-Agent: <your app>/<version> (+<your repo>)" \
  https://login.eveonline.com/v2/oauth/verify
```

Response includes `CharacterID`, `CharacterName`, `Scopes`.

The access token is also a JWT, so the same claims can be read without a round
trip: `sub` holds `CHARACTER:EVE:<character-id>`, `name` the character name and
`scp` the granted scopes. To verify a token you did not fetch yourself, check
its signature against the JWKS URL published in the SSO metadata document, and
confirm `iss` is `login.eveonline.com` and `aud` contains your client ID.

## Using tokens with ESI

Pass the access token as a Bearer header:

```bash
curl -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "X-Compatibility-Date: 2026-08-04" \
  -H "User-Agent: <your app>/<version> (+<your repo>)" \
  "https://esi.evetech.net/characters/<CHARACTER_ID>/wallet/"
```

Note there is no version segment in the path: ESI selects behaviour from the
`X-Compatibility-Date` header. Prefer `esi_query.py --char <name>`, which sets
both headers and keeps the token out of your command line entirely.

## PKCE (Proof Key for Code Exchange)

EVE SSO supports PKCE for public clients (no secret key). Generate a `code_verifier` (random 43-128 char string) and derive `code_challenge` via SHA-256:

```python
import hashlib, base64, secrets
code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b"=").decode()
```

Add `&code_challenge=<CHALLENGE>&code_challenge_method=S256` to the authorize URL. Include `code_verifier` in the token exchange.

## Required Scopes by Category

| Category | Scope |
|----------|-------|
| Wallet | `esi-wallet.read_character_wallet.v1` |
| Assets | `esi-assets.read_assets.v1` |
| Skills | `esi-skills.read_skills.v1`, `esi-skills.read_skillqueue.v1` |
| Clones | `esi-clones.read_clones.v1`, `esi-clones.read_implants.v1` |
| Location | `esi-location.read_location.v1`, `esi-location.read_ship_type.v1`, `esi-location.read_online.v1` |
| Contacts | `esi-characters.read_contacts.v1` |
| Contracts | `esi-contracts.read_character_contracts.v1` |
| Fittings | `esi-fittings.read_fittings.v1` |
| Mail | `esi-mail.read_mail.v1` |
| Calendar | `esi-calendar.read_calendar_events.v1` |
| Industry | `esi-industry.read_character_jobs.v1` |
| Market Orders | `esi-markets.read_character_orders.v1` |
| Killmails | `esi-killmails.read_killmails.v1` |
| Blueprints | `esi-characters.read_blueprints.v1` |
| Notifications | `esi-characters.read_notifications.v1` |
| Bookmarks | `esi-bookmarks.read_character_bookmarks.v1` |
| Loyalty | `esi-characters.read_loyalty.v1` |
| Mining | `esi-industry.read_character_mining.v1` |
| Roles | `esi-characters.read_corporation_roles.v1` |
| Standings | `esi-characters.read_standings.v1` |
| Fatigue | `esi-characters.read_fatigue.v1` |
| Medals | `esi-characters.read_medals.v1` |
| Titles | `esi-characters.read_titles.v1` |
| Agent Research | `esi-characters.read_agents_research.v1` |
| FW Stats | `esi-characters.read_fw_stats.v1` |
