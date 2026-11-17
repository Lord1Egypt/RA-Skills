# Authentication with `defineAuth`

Prefer `defineAuth` for standard OAuth, Bearer, API key, and Basic authentication. Read `custom-auth-plugin.md` only for HMAC, mTLS, composite auth, or a provider the factory cannot express.

## Contents

1. Factory behavior and options
2. Agent-safe split-flow login
3. Install wizard
4. Credential isolation and security
5. When to use a custom plugin

## 1. Factory behavior and options

`defineAuth` contributes:

- `auth login`, `status`, `logout`, and `register` commands.
- Device, authorization-code with PKCE, and client-credentials flows.
- Credential-provider resolution in `beforeCommand`.
- Bearer, X-API-Key, or Basic header injection in `beforeRequest`.
- One singleflight refresh and retry after a 401.
- Route-specific exemption so auth commands do not require an existing login.

The factory is synchronous. Async assembly (reading config, fetching metadata) happens in the plugin's `apply(services)`, which `defineCliApp` runs automatically before routing compiles:

```ts
import { defineCliApp, defineAuth } from "@renxqoo/agent-cli-sdk";
import { homedir } from "node:os";
import { join } from "node:path";

const app = await defineCliApp({
  name: "weather",
  dir: join(homedir(), ".weather"), // the app's one directory decision
  commands: weatherCommands,
  plugins: [
    defineAuth({
      credentialNamespace: "weather",
      baseUrl: process.env.AUTH_BASE_URL!,
      scope: "weather:read offline_access", // Use only after the service contract confirms it.
      clientMetadata: { client_name: "weather-cli" },
      bearerToken: process.env.WEATHER_BEARER_TOKEN,
    }),
  ],
});
```

`defineAuth` is a sync factory returning a Plugin; it never returns a Promise and must not be awaited. The plugin resolves its store from `services.localState.store` inside `apply`. Low-level `defineCli` users must call `await auth.apply?.({ localState, appName })` themselves.

Important options:

| Option                      | Meaning                                                                    |
| --------------------------- | -------------------------------------------------------------------------- |
| `credentialNamespace`       | Required namespace for both `config/<ns>.json` and `credentials/<ns>.json` |
| `baseUrl`                   | Required auth service base URL                                             |
| `scope`                     | One verified minimum scope for both login and registration metadata        |
| `flow`                      | `device` (default) / `authorization_code` / `client_credentials`           |
| `clientMetadata`            | RFC 7591 registration metadata; missing fields are derived (see below)     |
| `bearerToken`               | Pre-issued token injection for controlled CI or sandbox use                |
| `providers`                 | Custom credential provider chain                                           |
| `clientId` / `clientSecret` | Explicit client credentials                                                |
| `redirectPort`              | Local callback port for authorization-code flow                            |
| `commandNamespace`          | Defaults to `auth`                                                         |

**OAuth 2.1 flows** — pick the one the service needs:

| `flow`               | Grant                            | User | Notes                                                            |
| -------------------- | -------------------------------- | ---- | ---------------------------------------------------------------- |
| `device` (default)   | RFC 8628 device authorization    | yes  | CLI default; supports `--no-wait` / `--device-code` split-flow   |
| `authorization_code` | Authorization code + PKCE (S256) | yes  | The only flow that opens a browser; local loopback callback      |
| `client_credentials` | Client credentials               | no   | Server-to-server; refresh re-issues the persisted granted scopes |

**Registration metadata derivation** — `clientMetadata` fields default per-field and explicit values win (`hasOwnProperty`):

- `client_name` ← `credentialNamespace`
- `grant_types` ← the flow's grants (`device` → `urn:ietf:params:oauth:grant-type:device_code refresh_token`, `authorization_code` → `authorization_code refresh_token`, `client_credentials` → `client_credentials`)
- `scope` ← `scope`
- `token_endpoint_auth_method` ← `client_secret_basic`

So the common case writes `scope` exactly once; pass explicit `clientMetadata.scope` only when registration declares a different set than authorization. Access tokens are always Bearer (RFC 6750); `x-api-key`/`basic` styles belong to custom plugins via `injectAuthHeader`.

The factory takes no directory or store parameter — the local state arrives via `apply(services)` from `defineCliApp({ dir })`. Use `createMemoryLocalState` with `defineCliApp({ localState })` in tests.

For client ID and secret, resolution order is:

1. Explicit options, then `RXCLI_CLIENT_ID` / `RXCLI_CLIENT_SECRET`.
2. Values written to `<dir>/config/<ns>.json` by registration (namespace-isolated; other apps' registrations never overwrite them).
3. Empty values, which make login fail with a registration hint.

Typical first-use order is register, login, then business commands. Skip registration only when the auth service already provides a client ID and secret.

## 2. Agent-safe split-flow login

An agent must not run the blocking login command and wait while the user cannot see the authorization URL. Use two turns:

```bash
# Turn 1: start and return immediately.
my-cli auth login --no-wait --json

# Optional: render the returned verification URL as a QR code.
my-cli qrcode <verification_url> --output /tmp/my-cli-login.png

# Turn 2, after the user confirms authorization.
my-cli auth login --device-code <device_code>
```

Show the URL and optional QR image to the user, retain the short-lived `device_code` only for the current flow, and wait for confirmation before completing login. Never cache or reuse expired device codes.

Business Skills for authenticated CLIs must describe this split flow. Human-facing READMEs may show interactive `auth login` because a person can see the terminal directly.

## 3. Install wizard

The wizard is an internal plugin (`defineInstaller`) that provides the top-level `install` command — no entry-point intercept exists. Add it to `defineCliApp`'s plugins:

```ts
const app = await defineCliApp({
  name: "weather",
  dir: join(homedir(), ".weather"),
  plugins: [
    defineAuth({ credentialNamespace: "weather", baseUrl: process.env.AUTH_BASE_URL! }),
    defineInstaller({
      skillsSource: process.env.MY_CLI_SKILLS_SOURCE,
      // auth: false,   // for open-data CLIs without an auth flow
    }),
  ],
  commands: weatherCommands,
});
// rxcli install [--lang zh|en] is now an ordinary routed command; the entry point stays app.run(argv).
```

The interactive wizard may:

1. Install the business package globally.
2. Install Skills through `npx skills add` or local `<bin> skills sync`.
3. Run registration when no client is configured (skipped when `auth: false`).
4. Offer interactive login.

Disclose these writes before asking an agent to run the wizard. `skillsSource` must be passed to `defineInstaller`; setting it only in `defineCliApp`/`defineCli` has no installation effect.

## 4. Credential isolation and security

The local-state root is chosen once by the app via `defineCliApp({ dir })` (the SDK has no default); within that root, **both config and credentials** are isolated by `credentialNamespace`:

```
<dir>/
├── config/<ns>.json        ← registration clientId/clientSecret (namespace-isolated)
├── credentials/<ns>.json   ← tokens
└── cache/updates/          ← version-check cache
```

Two CLIs with the same namespace silently share credentials. Check for collisions and separate development, test, and production namespaces when their credentials must differ. Two CLIs sharing one root but using different namespaces no longer overwrite each other's registration config.

For a fully independent product directory, give each CLI its own root:

```ts
const app = await defineCliApp({
  dir: join(homedir(), ".my-cli"),
  plugins: [defineAuth({ credentialNamespace: "my-cli", baseUrl: process.env.AUTH_BASE_URL! })],
  // ...
});
```

Security rules:

- Never put client secrets, tokens, API keys, or refresh tokens in source, Skills, READMEs, logs, or snapshots.
- Do not ask an agent or user to paste production credentials into chat.
- `auth register` without `--token` uses ordinary terminal input and does **not** mask characters. Passing `--token` may expose it through history and process listings. In high-sensitivity environments, treat secure registration input as an unresolved framework limitation.
- Use a private terminal for registration and disclose the visible-input limitation.
- Registration metadata is derived from `scope`/`flow`/`credentialNamespace`; pass explicit `clientMetadata` fields only when the server requires a different registration declaration than the authorization request.
- Report provider source, expiry, and missing scopes during debugging, never credential values or auth responses.

Use `createMemoryLocalState` with `defineCliApp({ localState })` in tests to avoid touching disk. The high-level APIs (`defineAuth`, `defineInstaller`, `createUpdateNotifier`) take no directory parameters — there is no `store`, `configDir`, or `cacheDir` compatibility option.

## 5. When to use a custom plugin

| Requirement                                                           | Choice                                                      |
| --------------------------------------------------------------------- | ----------------------------------------------------------- |
| Standard OAuth device, authorization-code, or client-credentials flow | `defineAuth`                                                |
| Single Bearer credential (non-OAuth)                                  | Custom plugin with `injectAuthHeader(req, token, "bearer")` |
| API key or Basic credential                                           | Custom plugin with `injectAuthHeader` (x-api-key / basic)   |
| HMAC signing                                                          | Custom auth/provider plus post-signing plugin               |
| mTLS                                                                  | Custom plugin and transport-specific certificate handling   |
| Multiple signatures or composite headers                              | Custom plugins with explicit hook ordering                  |

For the last three cases, read `custom-auth-plugin.md` and pin the framework version used by the implementation.
