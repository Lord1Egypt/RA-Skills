# Setup, permissions and migration

All commands below run from the installed skill directory, the folder containing `SKILL.md` and `package.json`. Node.js 22+ and npm are required. The skill includes its runtime source and lockfile; it does not download executable code from a game server.

```bash
npm ci --ignore-scripts
node tools/doctor.mjs
node tools/setup.mjs --locale en
```

`npm ci` downloads the pinned MCP SDK, JSON schema validator, WebSocket client and their dependencies from the npm registry. Doctor starts a local stdio MCP child process, enumerates tools and checks map coordinates. It does not log in, enter a character or change game state.

Setup runs in the player's interactive terminal and hides password input. It creates `~/.earth2037-agent/credentials.json` with mode 600 and the directory with mode 700 on POSIX. It generates `mcp.json`, `hermes-mcp.yaml` and `dsh-mcp.patch.yaml` there. Existing credentials are preserved; generated configuration files are replaced. Merge only the Earth2037 entry into the chosen assistant's configuration. Setup does not edit that assistant's configuration or start a background service.

The generic MCP entry runs `node /absolute/skill/path/src/main.mjs` using stdio. It does not expose an HTTP listener. Do not open `main.mjs` as a web page or configure it as a public HTTP MCP URL.

## Credentials and destinations

The configured credential file contains the player's username/password and, after login, access/refresh tokens. Only the selected Account Center receives these credentials over HTTPS. It defaults to `https://new2037.earth2037.com/account-api`. The character's entry ticket is sent over WSS to the address returned by that Account Center, currently under `new2037.9235.net` for `s1` or `new2037.earth2037.com` for `en1`. Do not point the account URL at an unverified host.

Credentials are not included in tool results, game caches or receipts. Refresh tokens rotate and are persisted to the configured private file. One credential file is for one active gateway process. State and receipts are local; keep them private. There is no analytics destination or automatic skill upload.

The private credential JSON is not encrypted. Its restrictive file permissions protect access by other local users, but do not protect against a compromised OS account; do not share or upload it.

| Variable | Meaning |
|---|---|
| `EARTH2037_CREDENTIAL_FILE` | Absolute path to the private JSON file; needed for password login |
| `EARTH2037_ACCOUNT_URL` | Default independent HTTPS Account Center above |
| `EARTH2037_STATE_DIR` | Private cache and operation receipts; setup uses `~/.earth2037-agent/state` |
| `EARTH2037_READ_ONLY` | Read-only unless explicitly `0` |
| `EARTH2037_LOCALE` | `en` or the player's supported locale |
| `EARTH2037_CHANNEL` | Defaults to `direct`; do not change it to bypass channel policy |
| `EARTH2037_RUNTIME_PLATFORM` | Automatically macos, windows, or web on Linux |

Offline catalog, schemas and coordinates do not need credentials. `earth2037_directory` is a public HTTP read. Reading a character's live game state requires entering that character and therefore may replace the active mobile/browser session even in read-only mode.

## Enable requested game writes

After the player authorizes gameplay changes, run:

```bash
node tools/setup.mjs --locale en --config-only --allow-writes
```

Merge the generated entry and restart that MCP process. For an already managed entry, setting only `EARTH2037_READ_ONLY` to `0` has the same effect. This enables player-permitted game actions, registration and character creation; it does not grant server administrator access. Continue to honor the player's target, budget and action scope. Set it back to `1` for read-only use.

Account deletion/reset and payment flows are outside this switch. `resetaccount`, `paypal`, `paypalerr`, `googlebilling`, `gfan_pay` and `joincard` are always rejected with `official_client_required` before a packet or receipt is written. Use the official client for these actions. No configuration flag enables them in the gateway. The same rule applies to raw execution and direct socket sends; ordinary gameplay workflows are unchanged. The internal `test` diagnostic is also rejected at both layers with `unsupported_command`, regardless of write mode; inspect the connection using `earth2037_status`.

## CLI-only use

The generated MCP configuration is not automatically loaded by shell commands. Supply its paths explicitly:

```bash
export EARTH2037_CREDENTIAL_FILE="$HOME/.earth2037-agent/credentials.json"
export EARTH2037_STATE_DIR="$HOME/.earth2037-agent/state"
export EARTH2037_READ_ONLY=1
node src/cli.mjs describe arrivalheroexplore
node src/cli.mjs run < requests.ndjson
```

For an authorized takeover of the player's international character, `requests.ndjson` can contain:

```json
{"tool":"earth2037_enter","arguments":{"serverId":"en1","acceptSessionTakeover":true}}
{"tool":"earth2037_show","arguments":{"section":"city"}}
{"tool":"earth2037_disconnect","arguments":{}}
```

Use `s1` only when that is the selected Chinese character. Keep related calls in one process. A fully written input file cannot refer symbolically to a future returned planId: for prepare/submit workflows use MCP, or keep the CLI process open and send the next line after inspecting the previous output. Never put account passwords in NDJSON, process arguments or chat. To perform authorized writes in CLI mode, explicitly set `EARTH2037_READ_ONLY=0` for that process.

## Upgrade from ClawHub 1.x

Preserve any old configuration and use this version's runtime from a clean install directory. Old Python commands, SK-keys and `EARTH2037_API_BASE`/`EARTH2037_TOKEN` settings are not imported. Use the player's Account Center username/password. Guest or third-party users should bind password credentials in the official client before using this skill; do not register a replacement account for an existing character.

An existing `EARTH2037_ACCOUNT_URL` overrides the default. Replace saved legacy values with the independent URL, and merge the new runtime path. Moving the Chinese web domain no longer changes this package's default account entry. This does not make the account service or the realm's game server immune to their own outages.

The Chinese `2037` and English `earth2037` packages provide the same runtime. Install the preferred language; avoid duplicate MCP entries or competing processes. Existing old credential files and player data are never deleted by the update.
