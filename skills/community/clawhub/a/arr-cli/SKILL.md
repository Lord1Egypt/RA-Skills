---
name: arr-cli
description: Use the arr-cli Python package to query a self-hosted media stack (Jellyfin / Radarr / Sonarr / Maintainerr / Seerr). Use it to find out what's currently playing, what's coming up, what's about to be deleted, and so on.
homepage: https://github.com/BottaniCals/arr-cli
metadata:
  {'openclaw': {'requires': {'bins': ['jellyfin', 'radarr', 'sonarr', 'maintainerr', 'seerr']}}}
---

# arr-cli — read-only media-server CLI

`arr-cli` is a single Python package that ships five thin CLI executables — `jellyfin`, `radarr`, `sonarr`, `maintainerr`, `seerr` — backed by one shared facade (`arr_cli.facade`) that owns config, HTTP, auth, error mapping, and output formatting. All five binaries can be installed from https://github.com/BottaniCals/arr-cli source.

**Every command is an HTTP `GET`.** No write endpoints exist in MVP; the package cannot mutate the media stack.

Two operators:

- **Agents / pipelines** consume JSON on stdout. Default is a curated summary (sized for chat-agent consumption) for the size-to-summary commands; pass `--verbose` for full verbatim service JSON.
- **Human operators** reach for `--human` / `-h` for tabular terminal output. Combine with `--verbose` when you do want the full payload in table form.

Diagnostics always go to **stderr**, so `... | jq` is pipe-clean.

## Universal flags

Available on **all five CLIs**. Run `<cli> --help` for the per-service synopsis; universal flags are accepted by every subcommand, so position (before vs. after the subcommand) does not matter.

| Flag                        | Default        | Effect                                                                                             |
| --------------------------- | -------------- | -------------------------------------------------------------------------------------------------- |
| `--config PATH`             | canonical path | Per-invocation config override. Works in either position (see _Flag ordering_).                    |
| `--debug` / `--no-debug`    | off            | Full traceback + redacted request/response pair on stderr                                          |
| `--quiet` / `--no-quiet`    | off            | Suppress advisory stderr lines (e.g. the Maintainerr auth-disabled warning). Errors still surface. |
| `--human` / `-h`            | off            | Tabular human-readable view instead of JSON; pagination via `--limit`                              |
| `--verbose`                 | off            | Emit the verbatim service JSON payload instead of the curated summary (see _Output formats_).      |
| `--limit N`                 | `20`           | Row cap for `--human` lists                                                                        |
| `--connect-timeout SECONDS` | `5.0`          | Override config `connect_timeout`                                                                  |
| `--read-timeout SECONDS`    | `30.0`         | Override config `read_timeout`                                                                     |
| `--retry N`                 | `0`            | Retries on `NetworkError` (DNS, connect refused, TLS, timeout)                                     |
| `--deadline SECONDS`        | unbounded      | Absolute wall-clock cap for the retry layer                                                        |
| `--page-size N`             | varies         | Per-command; `radarr recent` default `10`, bounds-checked                                          |

### Flag ordering

Universal flags are accepted by every subcommand, so both positions work:

```bash
# both equivalent
jellyfin --config ~/.config/arr/local.yaml now
jellyfin now --config ~/.config/arr/local.yaml

# mixed with subcommand-specific positionals
radarr --limit 5 calendar 2026-01-01 2026-01-31
sonarr calendar $(date -I) $(date -I -d '+7 days') --human
```

`<cli> <subcommand> --help` lists the universal flags alongside the subcommand's own positionals / options, so an operator can discover them without going to the top-level help.

## Per-service commands

### `jellyfin`

| Command                   | Notes                                                       |
| ------------------------- | ----------------------------------------------------------- |
| `jellyfin now`            | All active sessions across users                            |
| `jellyfin resume`         | Requires `jellyfin.user_id`                                 |
| `jellyfin recent`         | Requires `jellyfin.user_id`;                                |
| `jellyfin nextup`         | `UserId` always sent from `jellyfin.user_id`                |
| `jellyfin latest`         | Requires `jellyfin.user_id`                                 |
| `jellyfin search <query>` | Empty query short-circuits to `[]` in-CLI (no service call) |
| `jellyfin item <id>`      | 404 → exit `4` with stderr naming the id                    |
| `jellyfin favorites`      |                                                             |

### `radarr`

| Command                         | Notes                                                      |
| ------------------------------- | ---------------------------------------------------------- |
| `radarr calendar`               | No date range                                              |
| `radarr calendar <start> [end]` | ISO-8601 `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS[Z]`          |
| `radarr wanted`                 | Missing movies                                             |
| `radarr queue`                  | Download / import queue                                    |
| `radarr recent`                 | `--page-size N` (default 10)                               |
| `radarr lookup <term>`          | Empty term short-circuits to `[]` in-CLI (no service call) |
| `radarr movie <id>`             | 404 → exit `4` with stderr naming the id                   |

### `sonarr`

| Command                         | Notes                                                      |
| ------------------------------- | ---------------------------------------------------------- |
| `sonarr calendar`               | No date range                                              |
| `sonarr calendar <start> [end]` | ISO-8601 `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS[Z]`          |
| `sonarr wanted`                 | Missing episodes                                           |
| `sonarr queue`                  | Download / import queue                                    |
| `sonarr recent`                 | TV history (NOT `/history/movie`)                          |
| `sonarr lookup <term>`          | Empty term short-circuits to `[]` in-CLI (no service call) |
| `sonarr series <id>`            |                                                            |

### `maintainerr`

Maintainerr ships with no auth. A one-line stderr warning is emitted on every invocation reminding the operator that the endpoint must be reachable only on a trusted / private network — pass `--quiet` to silence it.

| Command               | Notes                                            |
| --------------------- | ------------------------------------------------ |
| `maintainerr pending` | Pending collection overlays                      |
| `maintainerr storage` | Per-volume storage metrics                       |
| `maintainerr health`  | Readiness probe; `--human` renders the bare bool |

### `seerr`

`seerr` targets **Seer** (the unified Overseerr + Jellyseerr fork).

| Command                                  | Notes                                                                                                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `seerr requests`                         | Renderer unwraps `{page, totalPages, totalResults, results}` envelope                                              |
| `seerr request-count`                    | Aggregate counts                                                                                                   |
| `seerr search <query>`                   | Percent-encoded; renderer unwraps paginated envelope. Multi-word / reserved-char queries short-circuit to `[]`.    |
| `seerr available <query>`                | Client-side title-substring match after fetch                                                                      |
| `seerr trending [movie\|tv] [day\|week]` | Defaults `timeWindow=week`, no mediaType filter                                                                    |
| `seerr upcoming-movies`                  | Universal flags only (`--limit`, `--page`, `--language`)                                                           |
| `seerr upcoming-tv`                      | Universal flags only                                                                                               |
| `seerr discover-movies`                  | `--genre`, `--sort`, `--language`, `--page`; no defaults sent on the wire                                          |
| `seerr discover-tv`                      | `--genre`, `--sort`, `--language`, `--page`; no defaults sent on the wire                                          |
| `seerr movie <tmdbId> [--ratings]`       | Adds RT critic + audience scores under `payload["ratings"]`                                                        |
| `seerr tv <tvId> [--ratings]`            | Adds RT critic + audience scores under `payload["ratings"]`                                                        |
| `seerr genres [movie\|tv]`               | TMDB genre directory (~20 entries); default `movie`; `--language <ISO-639-1>` (omit = no `?language=` on the wire) |
| `seerr user`                             | Auth self-check (NOT `/auth/me` — that's the Next.js SPA route, returns HTML)                                      |

## Exit codes (stable contract)

Scripts depending on these codes for control flow:

| Code | Class          | Trigger                                                                      |
| ---: | -------------- | ---------------------------------------------------------------------------- |
|  `1` | `ConfigError`  | Missing / bad-perm / unknown-format config; malformed CLI date input         |
|  `2` | `AuthError`    | HTTP `401` / `403` from the service; missing required credential             |
|  `3` | `NetworkError` | DNS, connect refused, TLS error, timeout                                     |
|  `4` | `HttpError`    | Other `4xx` / `5xx` (e.g. 404 on `jellyfin item <id>`) — stderr names the id |
|  `5` | `ParseError`   | Service response is not valid JSON                                           |

Argument-parse errors (unknown flag, missing positional, invalid choice) exit `1` (`ConfigError`) and append a stderr line shaped `service=config op=parse message=argument parse error (argparse exit 2)`. The argparse usage hint stays on stderr above the structured line. Grep stderr for the `service=config op=parse` prefix to identify parse failures.

## Output formats

Three JSON shapes are possible; pick the one your consumer wants.

- **Default (no flag)** — for the _size-to-summary_ commands listed below: a curated, pipe-clean JSON summary sized for chat-agent consumption. For all other commands: verbatim service JSON unchanged.
- **`--verbose`** — full verbatim service JSON for any command (can return hundreds of rows). Use when a downstream pipeline needs the raw payload (server-internal metadata, MediaStreams, ImageBlurHashes, full Capabilities bitmask, etc.).
- **`--human` / `-h`** — tabular view of the same data the command returns by default (summary table for size-to-summary commands, verbatim table for the rest). Pagination via `--limit`. Use for terminal inspection.
- **stderr**: diagnostics only. The Maintainerr auth-disabled warning, `--debug` redacted traces, and `service=… op=…` error lines all flow here.

### Size-to-summary commands (default = summary, opt-in full via `--verbose`)

`jellyfin now`, `jellyfin resume`, `jellyfin recent`, `jellyfin favorites`, `jellyfin latest`, `radarr wanted`, `radarr queue`, `radarr recent`, `sonarr wanted`, `sonarr queue`, `sonarr recent`, `seerr requests`, `seerr search`, `seerr available`, `seerr trending`, `seerr upcoming-movies`, `seerr upcoming-tv`, `seerr discover-movies`, `seerr discover-tv`, `maintainerr pending`.

Everything else (`jellyfin item`, `jellyfin search`, `jellyfin nextup`, `radarr calendar`, `radarr lookup`, `radarr movie`, `sonarr calendar`, `sonarr lookup`, `sonarr series`, `seerr request-count`, `seerr movie`, `seerr tv`, `seerr genres`, `seerr user`, `maintainerr health`, `maintainerr storage`) is small by design and returns verbatim JSON in both default and `--verbose` modes.

Stderr error shape (grep-friendly):

```
service=jellyfin op=now status=401 message=jellyfin: op=now — 401 Unauthorized; check jellyfin.api_key in arr.conf
```

The `service=` and `op=` tokens are stable and safe to parse.

## Recipes — intent → command

| Intent                                 | Command                                                                          |
| -------------------------------------- | -------------------------------------------------------------------------------- |
| What's currently playing?              | `jellyfin --human now`                                                           |
| What's ready to resume?                | `jellyfin --human resume`                                                        |
| What was just watched?                 | `jellyfin --human recent`                                                        |
| What's queued next?                    | `jellyfin --human nextup`                                                        |
| Latest library additions               | `jellyfin --human latest`                                                        |
| Movie library + monitored state        | `radarr --human movie`                                                           |
| What's queued to download (movies)?    | `radarr --human queue`                                                           |
| What's missing (movies)?               | `radarr --human wanted`                                                          |
| Movie lookup by title                  | `radarr --human lookup "dune"`                                                   |
| Single movie / series detail           | `radarr movie <tmdbId>` / `sonarr series <tvdbId>`                               |
| Movies / episodes coming out this week | `sonarr calendar $(date -I) $(date -I -d '+7 days') --human`                     |
| Series lookup by title                 | `sonarr --human lookup "doctor who"`                                             |
| TV library + monitored state           | `sonarr --human series`                                                          |
| What's Maintainerr about to delete?    | `maintainerr --human pending`                                                    |
| Is the arr stack healthy?              | `maintainerr --quiet health` (silences auth warning; exit `0` = OK)              |
| All open media requests                | `seerr --human requests`                                                         |
| Is Seerr auth wired?                   | `seerr user` (exit `0` = OK; exit `2` = AuthError)                               |
| Search Seerr by title                  | `seerr search "dune" --human`                                                    |
| What's trending on Seer this week?     | `seerr --human trending` (or `trending tv day` for TV, daily)                    |
| Movies / TV coming out                 | `seerr upcoming-movies --human` / `seerr upcoming-tv --human`                    |
| Discover movies/TV by genre            | `seerr genres movie \| grep Action`→`seerr discover-movies --genre <id> --human` |
| Movie details (with Rotten Tomatoes)   | `seerr movie <tmdbId> --ratings`                                                 |
| TV details (with Rotten Tomatoes)      | `seerr tv <tvId> --ratings`                                                      |

### Lookup vs library-list

`radarr lookup` / `sonarr lookup` return candidate records (what the upstream service knows about, whether or not you've added it). The `id` column on `--human` output is the disambiguator: populated `id` means the candidate is already in the library (the `monitored` field reflects library state); blank `id` means it's a candidate not yet added (the `monitored` field is the TVDB/TMDB source default).

For canonical "what's in my library and what's monitored" use `sonarr --human series` and `radarr --human movie` — those hit `/api/v3/series` and `/api/v3/movie` and reflect actual library state.

## Common gotchas

- **`user_id` is required** for most Jellyfin commands. The `arr.conf` `jellyfin.user_id` field is non-optional for `resume`, `recent`, `latest`, `favorites`. Missing it → `AuthError` (exit `2`), not `ConfigError`.
- **Calendar dates are ISO-8601 only.** `radarr calendar next-tuesday` → exit `1` (ConfigError) with stderr usage hint. Format strictly as `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS[Z]`.
- **Maintainerr's `--quiet` matters.** Without it, every invocation spams a "no auth, private network only" warning to stderr. Default to `maintainerr --quiet <subcommand>` for cron / scripted use.
- **`--debug` is loud and slow.** Full traceback + redacted request / response pair to stderr. Use for one-shot diagnosis, not in pipelines.
- **`exit 2` is auth-only.** Argument-parse errors exit `1` (`ConfigError`) and append `service=config op=parse message=argument parse error (argparse exit 2)` to stderr. Universal flags work before or after the subcommand; both `jellyfin now --config X` and `jellyfin --config X now` are valid.
- **Search-with-empty-query is not an error — and it's CLI-side.** `jellyfin search ""` (and `jellyfin search` with no positional) short-circuits to `[]` without calling `/Items`. Exit `0`, no `transport.get` fired. Useful when chaining in scripts that may pass empty input.
- **Seer endpoints are paginated by default.** `seerr requests`, `seerr search`, `seerr available`, `seerr trending`, `seerr upcoming-*`, and `seerr discover-*` all return `{page, totalPages, totalResults, results: [...]}` envelopes. The size-to-summary renderers unwrap `results` automatically; pass `--verbose` to see the full envelope. `seerr available` requests `take=1000` so a single response covers the household queue; queues above 1000 items would need a page-walking follow-up.
- **`seerr discover-*` with no flags sends no defaults on the wire.** Pass `--sort` / `--language` explicitly when you need them. Trending / upcoming / search / genres already followed the omit-when-default rule and are unaffected.

## Smoke-testing without a live service

Quick sanity check that the package is wired (no network):

```bash
command -v jellyfin radarr sonarr maintainerr seerr     # all 5 on PATH
python3 -c "import arr_cli"                            # package importable
<cli> --help | head -3                                  # usage renders
<cli> now 2>&1 | grep -q "config file not found" && echo "ok: config gate works"
```

The last line confirms the canonical config path is being checked before
any HTTP call — useful after rebuilding the sandbox image.
