---
name: cookie-use
description: Manage many logged-in account sessions for any website — capture, store, list, switch, and apply saved logins across Chrome profiles, isolated browsers, and connected sessions. Use when the user wants to "save this account", "switch to account X", "log in as another account", "manage my N ChatGPT/Claude accounts", "move a login between profiles/browsers", or juggle dozens of accounts on one site. Sessions live in an encrypted local vault; browser/cookie I/O is delegated to chrome-use. macOS.
allowed-tools: Bash(cookie-use:*), Bash(chrome-use:*), Bash(curl:*)
---

# cookie-use

A site-agnostic, agent-friendly **multi-account session manager**. It keeps an
encrypted vault of logged-in sessions for *any* website (e.g. 100 ChatGPT
accounts) and lets you list, capture, switch, and apply them to a browser.

It sits on top of [`chrome-use`](https://github.com/leeguooooo/chrome-use): all
browser and cookie work (decrypting a profile's cookies, injecting into a live
browser, launching isolated contexts) is delegated there. cookie-use owns the
account model, the vault, and orchestration.

## Install / self-heal

If the `cookie-use` command is missing (`command not found`), install it — do
NOT fall back to other tools:

```sh
curl -fsSL https://raw.githubusercontent.com/leeguooooo/cookie-use/main/install.sh | sh
```

cookie-use **requires `chrome-use`** on PATH. If that's missing too:

```sh
curl -fsSL https://raw.githubusercontent.com/leeguooooo/chrome-use/main/install.sh | sh
```

macOS only (uses the Keychain for the vault key and chrome-use's macOS cookie
decryption).

## Mental model

An **account** is one stored session for one site: its full cross-domain cookie
set plus metadata (id, site, label, hint, timestamps, status). The vault holds
many accounts across many sites, **encrypted at rest** (AES-256-GCM, key in the
macOS Keychain, at `~/.cookie-use/vault.enc`). Cookie values never touch disk in
plaintext, and `list`/`show` never print them.

`--site` takes a comma-separated domain list, so multi-host auth (e.g.
`chatgpt.com,openai.com`) is captured as one account.

## Commands

```bash
# Capture a logged-in session from a Chrome profile (any site).
cookie-use add --from-profile "<profile>" --site "<domain[,domain]>" [--id <id>] [--label <l>]
#   <profile> = directory name ("Profile 14"), display name ("Davian"), or "auto".
#   --with-localstorage  also snapshot the primary origin's localStorage
#                        (one in-browser read; for SPAs that keep token/user
#                        info in localStorage, not cookies).

# Import from a JSON cookie array or a bare "name=value; ..." Cookie header.
cookie-use import --file <path> --site <domain> --id <id>

# Inspect.
cookie-use list [--site <domain>] [--json]
cookie-use show <id>                       # metadata only, never secrets
cookie-use check <id>                      # liveness from cookie expiry

# Apply / switch.
cookie-use use <id> --target session:<name>     # inject into a connected chrome-use session
cookie-use use <id> --target isolated           # spin up a throwaway browser with this account
cookie-use switch <id> --target session:<name>  # clear the site's cookies, then apply
#   add --no-open to skip opening the site after applying.
#   --rewrite-domain <host>   rewrite cookie domains on apply (e.g. "localhost")
#                             so a prod/test session works on a different origin.
#   --open-url <url>          open this exact URL afterwards (e.g. a dev server's
#                             "http://localhost:8001"); pair with --rewrite-domain.
#   --no-localstorage         skip injecting the account's captured localStorage
#                             (injected by default when present and a page opens).
#   --no-confirm              skip the Touch ID / TTY gate before injecting.

# Cross-origin QA sugar: replay a captured session onto a local dev origin.
cookie-use replay <id> --to localhost:8001    # = use --rewrite-domain localhost
#                                               --open-url http://localhost:8001

# Open many accounts at once, each in its own isolated window (side by side).
cookie-use run <id>                            # one account, isolated
cookie-use run --site chatgpt.com --all        # every chatgpt account, side by side
cookie-use run --all                           # the whole vault

# Agent identity: run a command in an environment scoped to an account's session.
# Sets COOKIE_USE_ACCOUNT / _SITE / _TARGET and CHROME_USE_SESSION for the child,
# so an agent (or any chrome-use call) acts AS that account for one task.
cookie-use as <id> --target session:work -- chrome-use open https://dash.cloudflare.com

# Share a session with a teammate as a password-encrypted bundle (viral loop:
# redeeming requires installing cookie-use). Never writes plaintext cookies.
cookie-use share <id> [--out <path.cusession>] [--password <pw>]
cookie-use redeem <path.cusession> [--password <pw>] [--id <new-id>]

# Manage.
cookie-use rename <id> <new-id>
cookie-use rm <id>                             # (alias: revoke <id>)
cookie-use wipe [--yes]                        # delete the ENTIRE vault
```

## Confirmation gate (Touch ID)

Injecting a live session is the dangerous action, so `use` / `switch` / `replay`
/ `as` confirm before they inject: **Touch ID** on macOS (LocalAuthentication),
falling back to a TTY y/N prompt. An agent driving the CLI non-interactively
must either pass `--no-confirm` or set `COOKIE_USE_YES=1`; without a bypass,
injection is *refused* in a non-interactive shell rather than proceeding
silently.

## Environment variables

- `COOKIE_USE_YES=1` — bypass the injection confirmation (agent / automation).
- `COOKIE_USE_VAULT_KEY` — base64 of a 32-byte key; used directly instead of the
  macOS Keychain. For headless / CI / agent hosts with no login Keychain (the
  caller owns key custody). Without it, the key lives in the Keychain.
- `COOKIE_USE_VAULT` — override the vault file path (multiple isolated vaults,
  headless hosts, tests). Defaults to `~/.cookie-use/vault.enc`.
- `CHROME_USE_BIN` — path to the `chrome-use` binary if not on `PATH`.

## Targets

- `session:<name>` (default `session:default`) — an existing chrome-use session.
  Connect it first to wherever you want the account applied: the user's real,
  logged-in Chrome via `chrome-use extension connect`, or a browser you launched.
  This is the most reliable path and works without restarting Chrome.
- `isolated` — cookie-use launches a fresh throwaway browser via
  `chrome-use --launch`, seeds the account, and opens the site. Good for running
  an account in a clean context.

## Typical workflows

Bulk-import every logged-in profile, then use one:

```bash
cookie-use add --from-profile "花月社" --site "chatgpt.com,openai.com" --id chatgpt/huayue
cookie-use add --from-profile "Davian" --site "claude.ai,anthropic.com" --id claude/davian
cookie-use list
cookie-use use chatgpt/huayue --target isolated      # opens ChatGPT logged in as that account
```

Apply an account into the user's real Chrome (drive their live browser):

```bash
chrome-use extension connect                 # connect a session to the real Chrome
cookie-use use claude/davian --target session:default
```

Reuse a production/test login on a local dev server (cross-origin testing). The
cookies are domain-bound to the prod host, so `localhost` can't see them — rewrite
the domain (and bring the localStorage too if the SPA needs it):

```bash
# capture the prod session incl. localStorage (token/user info often lives there)
cookie-use add --from-profile auto --site "example.com" --id app/prod --with-localstorage

# replay it onto the local dev origin
cookie-use use app/prod --target session:real \
  --rewrite-domain localhost \
  --open-url http://localhost:8001
```

Note: this only fixes domain-binding and storage. If the dev server talks to a
different backend/gateway than prod, the token may not be honored there — that's
an environment-config issue, not something cookie-use can bridge.

Hand a session to a teammate (and pull it into your own vault):

```bash
cookie-use share chatgpt/team-seat --out seat.cusession   # prompts for a password
# teammate runs (installs cookie-use if missing, then imports):
cookie-use redeem seat.cusession --id chatgpt/team-seat
```

Let an agent act as a specific account for one task, several accounts at once:

```bash
cookie-use run --site chatgpt.com --all                   # open every seat side by side
COOKIE_USE_YES=1 cookie-use as chatgpt/seat-07 --target session:agent -- \
  chrome-use open https://chatgpt.com                     # agent now acts as seat-07
```

## Notes

- Reserved per-account `proxy` / `fingerprint` fields exist for future
  anti-correlation; not applied yet.
- `share` bundles are `argon2id` + AES-256-GCM, encrypted with the chosen
  password — the only artifact that leaves the machine, and only when you run
  `share`. The vault itself is always local-only.
- `check` is a generic expiry heuristic (no per-site probes yet) — it can't tell
  a server-revoked session from a live one, only an expired cookie set.
- Repo & issues: <https://github.com/leeguooooo/cookie-use>
