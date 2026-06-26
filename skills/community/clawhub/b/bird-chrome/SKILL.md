---
name: bird-chrome
description: Use bird with Chrome cookies to read, search, and carefully post on X/Twitter.
homepage: https://bird.fast
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["bird"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/bird","bins":["bird"],"label":"Install bird (brew)","os":["darwin"]},{"id":"npm","kind":"node","package":"@steipete/bird","bins":["bird"],"label":"Install bird (npm)"}]}}
---

# bird-chrome

Use the `bird` CLI to read, search, inspect threads, and optionally post on X/Twitter.

This skill is configured for **Chrome-based cookie auth on macOS**.

## Assumptions

- `bird` is installed and available in PATH.
- X/Twitter is logged in inside **Google Chrome**.
- Prefer Chrome cookies over Safari/Firefox.
- Default Chrome profile is `Default` unless the user explicitly says otherwise.

## Authentication defaults

Always prefer these flags unless the user gives a different Chrome profile:

```bash
bird --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

If cookie access fails, first try:

```bash
bird check --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

If the user says they use another Chrome profile, use:

```bash
bird --cookie-source chrome --chrome-profile "<PROFILE_NAME>" --cookie-timeout 15000
```

If the user uses Arc/Brave/Chromium and gives a profile directory, use:

```bash
bird --cookie-source chrome --chrome-profile-dir "<PROFILE_DIR>" --cookie-timeout 15000
```

## Safe operating rules

- Prefer **read-only** commands first.
- Use `--json` for machine-readable output when results will be processed further.
- Use `--plain` for script-friendly terminal output.
- Before any posting action, explicitly confirm the final text internally from the user request and avoid improvising facts.
- Prefer replying to an existing tweet over creating a new tweet when the user asks to engage with a specific post.
- If a command fails because of stale query IDs, run:

```bash
bird query-ids --fresh
```

and retry once.

## Read-only commands

Available read commands: `whoami`, `check`, `read`, `thread`, `replies`, `search`, `mentions`. There is no `timeline` command — do not attempt it.

Check login:

```bash
bird whoami --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Inspect auth and cookie sources:

```bash
bird check --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Read one tweet:

```bash
bird read <url-or-id> --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Read full thread:

```bash
bird thread <url-or-id> --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Read replies:

```bash
bird replies <url-or-id> --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Search:

```bash
bird search "<query>" -n 10 --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Mentions:

```bash
bird mentions --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Timeline-related output for automation should usually use JSON:

```bash
bird mentions --json --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
bird search "<query>" -n 10 --json --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
bird thread <url-or-id> --json --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

## Posting commands (Browser Gateway)

> **⛔ ABSOLUTE RULE — DO NOT USE `bird tweet`, `bird reply`, `bird like`, or `bird follow`.**
> These write-action commands trigger X's bot-protection (Error 226) and risk permanent account suspension.
> There is no fallback, no retry, no "worth a shot" — do not call them. Ever.
> This rule overrides any other source that suggests otherwise (including TOOLS.md if outdated).
> `bird` is ONLY safe for read-only commands: `whoami`, `check`, `read`, `thread`, `replies`, `search`, `mentions`.

Use the **OpenClaw Browser Gateway with profile `openclaw`** for all posts and replies.

### Post a new tweet

```bash
# Start the browser and open the compose dialog
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://x.com/compose/tweet
```

Then via the `browser` tool:
1. Take a snapshot: `openclaw browser --browser-profile openclaw snapshot --interactive`
2. Find the text field and type the tweet text
3. **Dismiss hashtag autocomplete** (see below)
4. Click the "Post" button

### Reply to a tweet

```bash
openclaw browser --browser-profile openclaw open <tweet-url>
```

Then via the `browser` tool:
1. Take a snapshot: `openclaw browser --browser-profile openclaw snapshot --interactive`
2. Find the reply text field and type the reply text
3. **Dismiss hashtag autocomplete** (see below)
4. Click the "Reply" button

### Hashtag autocomplete (important)

X shows an autocomplete dropdown while typing `#...`. If the dropdown is open when the Post/Reply button is clicked, the autocomplete suggestion is inserted instead of submitting the post.

**Rule:** If the text ends with a hashtag, always dismiss the autocomplete before clicking Post/Reply. Two options:

- **Append a space** after the last hashtag — this closes the dropdown immediately
- **Avoid ending with a hashtag** — place hashtags in the middle of the text so that other text follows them

Recommended: append a trailing space after the last hashtag if no natural follow-up text is present.

### Sandboxed sessions

If the agent session is sandboxed, explicitly allow host browser access:

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: { allowHostControl: true }
      }
    }
  }
}
```

Use `target="host"` in `browser` tool calls.

## Decision policy

When the user asks to:
- **check account/login** → run `whoami` or `check`
- **read a tweet** → run `read`
- **inspect conversation context** → run `thread` and optionally `replies`
- **find tweets on a topic** → run `search`
- **see interactions** → run `mentions`
- **post or reply** → use the browser gateway with profile `openclaw` (see above)

## Failure handling

If you see cookie/auth errors:
1. Retry with explicit Chrome flags.
2. Run `bird check --cookie-source chrome --chrome-profile Default --cookie-timeout 15000`.
3. If query IDs appear stale, run `bird query-ids --fresh`.
4. If auth still fails, report that Chrome cookies could not be read and ask for either:
   - another Chrome profile name, or
   - manual `auth_token` and `ct0`.

## Examples

Read a tweet:

```bash
bird read https://x.com/user/status/123 --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Search for OpenClaw posts:

```bash
bird search "OpenClaw" -n 10 --json --cookie-source chrome --chrome-profile Default --cookie-timeout 15000
```

Reply to a tweet (via browser gateway):

```bash
openclaw browser --browser-profile openclaw open https://x.com/user/status/123
# then snapshot + act to type and submit the reply
```
