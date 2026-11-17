---
name: backlink-audit
version: 1.1.3
description: 'Discover all inbound links (backlinks) to a domain, subdomain, or GitHub repo, then classify each as "ours" (we created/control the source) vs "organic" (someone else). Use when the user asks to find/audit backlinks or inbound links to a site, check who links to a domain or a GitHub repo, separate self-made links from organic ones, or refresh an inbound-links graph. Wraps four sources (GitHub repo referrers, a list of URLs you found, the backlinks.sh Common-Crawl API, and a Google Search Console CSV export) behind one classify-and-report CLI. Two of the four need no account at all; the one optional API key is stored in your OS keychain and cleared by --logout. Built for the TinkerClaw fork — github.com/globalcaos/tinkerclaw. See Permissions, Data Flow & Consent.'
metadata:
  openclaw:
    emoji: "🔗"
    os: ["linux", "darwin"]
    requires:
      bins: ["node"]
    notes:
      security: "A read-mostly link classifier. Two of its four sources (urls, gsc-csv) make no network call at all; `github` shells out to the `gh` CLI you already authenticated, and `backlinks` is the only one that uses a credential — a backlinks.sh API key, resolved from BACKLINKS_SH_API_KEY (transient) or the OS keychain (secret-tool/security) — and from nowhere else. There is NO plaintext fallback: if no keychain is available `--login` refuses and writes nothing, rather than silently downgrading a long-lived API key to a file on disk. A credentials.json left by an older version is detected and explained but never read as a credential, and `--logout` still deletes it. The key reaches the keychain on stdin on both platforms (macOS uses `security -i` so it is never an argv element visible in `ps`); `--logout` prints where to revoke it server-side. Nothing is written outside the skill folder unless you pass a flag: `--write-state` updates one JSON file under ~/.openclaw, and scripts/build-history.mjs writes to your control-panel store only with --yes (bare, it is a dry run). No telemetry, no third-party endpoint beyond api.backlinks.sh, no source-tree patching, no privilege escalation. See the Permissions, Data Flow & Consent section."
    # Declared capabilities. Each is used for exactly the reason given; anything not
    # listed here, the skill does not do.
    permissions:
      network:
        required: false
        scope: "Only two sources reach the network, and only when you select them: `--source backlinks` calls the hardcoded constant https://api.backlinks.sh/v1/backlinks (your key in an x-api-key header), and `--source github` runs the `gh` CLI, which talks to api.github.com. `--source urls` and `--source gsc-csv` are fully offline. No telemetry, no analytics, no other endpoint."
      shell:
        required: true
        scope: "Three external binaries, each for one job: `gh` (GitHub referrer API), `secret-tool` or `security` (keychain get/set/clear), and `openclaw` (only in scripts/build-history.mjs, only with --yes). No shell interpreter is invoked; arguments are passed as an argv array, never interpolated into a command string."
      env_read:
        required: false
        scope: "BACKLINKS_SH_API_KEY, and nothing else. No env file is read or sourced."
      credentials:
        required: false
        scope: "One optional secret: your backlinks.sh API key, needed only by `--source backlinks`. It lives in the OS keychain (service backlinks-sh, account api-key) or in the BACKLINKS_SH_API_KEY environment variable, and nowhere else — there is no plaintext file fallback and none is ever written. The key is sent only to api.backlinks.sh, is never logged, never placed on a command line on either platform, and `--logout` removes it locally."
      file_read:
        required: true
        scope: "assets/ours-allowlist.json (or the --allowlist path you pass), the CSV given to --csv, the file given to --urls-file, the inbound-campaign-state.json it is about to update, and — only to tell you it is stale — the presence of a legacy ~/.config/backlinks-sh/credentials.json."
      file_write:
        required: false
        scope: "Off unless you ask, and it never writes a credential anywhere. `--write-state` writes inbound_targets.<key> into ~/.openclaw/workspace/memory/online-presence/inbound-campaign-state.json (creating it if absent). `--login` writes only to the OS keychain, and refuses outright if there is not one. scripts/build-history.mjs writes dated points to your control-panel store, and only with --yes."
      file_delete:
        required: false
        scope: "Exactly one path, only on explicit command: `--logout` deletes a legacy ~/.config/backlinks-sh/credentials.json if an older version left one. No other file is ever removed, and the scripts contain no recursive or glob delete. The only recursive delete in the package is the test suite removing the mktemp directory it created."
repository: https://github.com/globalcaos/tinkerclaw
homepage: https://github.com/globalcaos/tinkerclaw
---

# Backlink Audit

> One of dozens of skills and plugins in **[TinkerClaw](https://github.com/globalcaos/tinkerclaw)** — a self-improving OpenClaw fork that's been running 24/7 for months.

**Who actually links to you — and how much of that did you build yourself?**

Every backlink report you can buy gives you one number. That number is two very different things added together: links strangers made because your work was worth linking, and links you made because you were doing your own marketing. The first is traction. The second is homework. A tool that adds them up is telling you a flattering lie.

This one separates them. You get `ours`, `organic`, and an honest `ambiguous` bucket for the cases a hostname genuinely cannot settle — because a link from `github.com` might be your comment or a stranger's, and pretending otherwise is how a growth chart starts lying to you.

Two of the four sources need no account and no key. The one that does keeps it in your OS keychain — or refuses to store it at all, rather than dropping an API key into a file in the clear — and hands you a `--logout` that actually removes it.

## Overview

Finding inbound links and telling "ours" from "organic" is two jobs: (1) get a link list from a real index, (2) match each source against surfaces you control. This skill does both via `scripts/backlink-audit.mjs` and an editable allowlist.

## Quick start

```bash
S=~/.openclaw/workspace/skills/backlink-audit/scripts/backlink-audit.mjs

# GitHub repo (works now — no extra auth; referrers, not raw backlinks)
node "$S" globalcaos/tinkerclaw --source github

# Discovered links (poor-man's backlink finder, works now): web-search the target
# term yourself, collect referring URLs, classify them — best source at small scale
node "$S" globalcaos/tinkerclaw --source urls --urls "https://a.com/x,https://b.com/y"

# Any owned domain via backlinks.sh (needs a key; 3 free calls, then ~$0.01/call)
BACKLINKS_SH_API_KEY=… node "$S" thetinkerzone.com --source backlinks --json

# Owned site, authoritative + free: export GSC Links→Top linking sites to CSV, then
node "$S" sprintpaper.com --source gsc-csv --csv ./gsc-export.csv

# Feed the Inbound-links pulse graph for one target:
node "$S" globalcaos/tinkerclaw --source github --write-state --target-key tinkerclaw
```

Storing the one optional credential, and taking it back:

```bash
printf %s "$BACKLINKS_SH_API_KEY" | node "$S" --login   # → OS keychain (stdin, never argv)
node "$S" --logout                                      # → clears the keychain (and any legacy file)
```

## Choosing a source

| Target | Source | Auth | Cost | Notes |
|---|---|---|---|---|
| GitHub repo | `github` | none (`gh`) | free | referrers/traffic proxy, repo-scoped |
| Anything | `urls` | none | free | classify a list of links you found (e.g. via web search); works now, best at small scale |
| Owned domain, one-shot | `backlinks` | backlinks.sh API key | 3 free calls, then ~$0.01/call | Common-Crawl backlink list |
| Owned domain, authoritative | `gsc-csv` | a CSV export (no OAuth) | free | Google's own link report |

Read `references/sources.md` before picking — it has the auth setup, the backlinks.sh signup/limits, how to export the GSC CSV, and the per-source caveats.

## Classify: ours vs organic

Edit `assets/ours-allowlist.json`. A link is **ours** if its source host (+ optional `path_prefix`) matches a rule; hosts listed in `ambiguous_domains` with no resolving path-rule are reported **ambiguous** (e.g. a github.com link could be a comment you wrote or a stranger's — resolve it by hand, then pin the resolved URL in `ours_urls`); everything else is **organic**. Keep the allowlist current as new owned surfaces appear.

The shipped allowlist is the author's, kept as a worked example of the rule shapes. Replace the domains with yours.

## Feed the pulse graph

`--write-state --target-key <key>` writes `inbound_targets.<key>.{external,ours}` into `inbound-campaign-state.json`; the control-panel pollers render it (solid=external, dashed=ours, one hue per target). Ambiguous links are excluded from the written counts. Without `--write-state` the tool writes nothing at all — it just prints.

## Count strategy (how many backlinks do we have?)

At small scale, crawl indexes (backlinks.sh/Common Crawl) return ~0 for new sites, so the **search strategy** is the workhorse. To count inbound links to a target:
1. Web-search the target term several ways: `"github.com/globalcaos/tinkerclaw"`, `tinkerclaw`, `"thetinkerzone.com"`, plus `site:` excluded variants to find third-party mentions.
2. Collect the distinct referring URLs (one page = one backlink; dedupe).
3. `node scripts/backlink-audit.mjs <target> --source urls --urls "u1,u2,…"` → ours/organic/ambiguous counts.
4. `--write-state --target-key <k>` to push the count to the graph.

## Historical dataset (when did each backlink go live?)

`scripts/build-history.mjs` writes **dated cumulative `ours` observations** so the graph shows real growth, not just today. Its dataset is *derived* (not invented) from:
- **Authored GitHub comments**: `gh api repos/<r>/issues/<n>/comments`, filter by your login, body contains your URL → dated by each thread's first backlink-bearing comment (one thread = one linking page).
- **`git log -S "<domain>"`** in the linking repo → when an outbound link to your site (e.g. README→yourdomain.com) first went live.

Re-derive by re-running those two mines, updating `SERIES` in the script, and re-running it.

**Two things to know before you run it.** The `SERIES` in the file is the *author's* dataset, shipped as a worked example of the shape and the provenance discipline — replace it with yours or your graph will show someone else's history. And it is **opt-in**: bare (or with `--dry-run`) it prints exactly what it would write and writes nothing; `--yes` is what actually sends the points to your control-panel store.

## Permissions, Data Flow & Consent

Short version: this reads public link data, classifies it against a list you edit, and prints the result. Two of its four sources never touch the network. The one credential it can use is optional, keychain-first, and revocable. Longer version, because you should not have to take that on trust:

**What data it touches.** Referring URLs — from the GitHub traffic API, from a list you paste, from a CSV you exported, or from backlinks.sh. Plus the allowlist you edit. That is the whole input surface. It does not read your repos, your mail, your browser, your shell history or your source tree.

**What leaves your machine.** Only what the source you picked requires:
- `--source urls` and `--source gsc-csv`: **nothing**. Fully offline; the CSV is parsed locally.
- `--source github`: the `gh` CLI you already authenticated calls `api.github.com` for your repo's referrer list.
- `--source backlinks`: one HTTPS GET to `https://api.backlinks.sh/v1/backlinks?target=<domain>` with your API key in an `x-api-key` header. The URL is a constant in the script, not something the target string can redirect.

There is no telemetry, no analytics, no "phone home", and no other endpoint anywhere in the code.

**What it costs.** Nothing, except `--source backlinks`: backlinks.sh gives 3 free calls, then charges roughly $0.01 per call. Every other source is free. Nothing subscribes you to anything.

**What credentials it reads.** One, optional: your backlinks.sh API key, and only for `--source backlinks`. There are exactly two places it can come from — `BACKLINKS_SH_API_KEY` (transient, nothing on disk) or your **OS keychain** (`secret-tool` on Linux, `security` on macOS; service `backlinks-sh`, account `api-key`).

**There is no plaintext fallback, by design.** An earlier version wrote the key to `~/.config/backlinks-sh/credentials.json` when no keychain was present, warning on every use. A warning is not a control: the thing it warned about was still a long-lived API key sitting in the clear, readable by anything running as you. Now `--login` **refuses** when there is no keychain and writes nothing, telling you to install libsecret or pass the key per-run through the environment. If an older version left a file behind, it is detected and explained — so you learn why your key stopped working — but it is never read as a credential, and `--logout` still deletes it.

`--login` reads the key from **stdin**, never from argv, because argv is visible in `ps`. That now holds on **both** platforms: macOS `security add-generic-password -w <key>` would have put the key in an argv element, so the key is piped to `security -i` instead and the entry is verified by reading it back (`-i` exits 0 even when a command inside it fails).

**The off switch.** `node scripts/backlink-audit.mjs --logout` clears the keychain entry **and** deletes any legacy plaintext file, tells you which of the two actually existed, and reminds you if `BACKLINKS_SH_API_KEY` is still set in your environment (it cannot reach into your shell to unset it). Local removal does not revoke the key server-side — rotate or delete it in your backlinks.sh account at https://backlinks.sh.

**What it needs, and why.**

| Capability | Why | Scope |
| --- | --- | --- |
| Network | Fetch the link list | `api.backlinks.sh` (constant URL) and `api.github.com` via `gh` — only for those two sources |
| Local shell exec | `gh`, `secret-tool`/`security`, `openclaw` | argv arrays, no shell interpreter, no string interpolation |
| Env read | `BACKLINKS_SH_API_KEY` | that one variable; no env file is sourced |
| Credential read | backlinks.sh API key | env var or OS keychain only — no file fallback; sent only to `api.backlinks.sh` |
| File read | Allowlist, your `--csv` / `--urls-file`, the credentials file, the state file | the paths you name, plus those two fixed ones |
| File write | `--write-state` state file; `build-history.mjs --yes` | **both are opt-in**; nothing is written on a plain run, and no credential is ever written to disk |
| File delete | `--logout` removes the credentials file | that single path — the scripts have no recursive or glob delete (the test suite removes only its own mktemp dir) |

**The consent steps, and what each is protecting you from:**

```bash
node "$S" <target> --source urls --urls "…"              # reads nothing, writes nothing, sends nothing
node "$S" <target> --source backlinks                    # spends a paid API call, sends your key
node "$S" <target> --source github --write-state --target-key k   # writes one JSON file under ~/.openclaw
node scripts/build-history.mjs                           # DRY RUN — prints what it would write
node scripts/build-history.mjs --yes                     # actually writes to your control-panel store
node "$S" --logout                                       # removes the stored key
```

**Read it before you run it.** `scripts/backlink-audit.mjs` is ~300 lines of plain Node and `scripts/build-history.mjs` about 100. `tests/test-credentials.sh` runs the tool against stub `secret-tool`/`security` executables in a temp dir and aborts if a real keychain binary is reachable, so running it never changes your stored key. It also preloads a fake `fetch()`, so the suite makes no network request; it deletes only its own temp dir. Every claim above is visible in them. That is the whole security model: short enough to audit over a coffee.

## Changelog

- 1.1.3 — `tests/test-credentials.sh` no longer calls api.backlinks.sh (fake `fetch()` preloaded, request shape asserted offline); SKILL.md now states the test's temp-dir cleanup is the package's only recursive delete.
- 1.1.2 — `tests/test-credentials.sh` no longer reaches the real OS keychain (stub keychain binaries on PATH, hard abort otherwise); `references/sources.md` no longer describes the removed plaintext-file fallback.

## Honest limits

- No SEO tool isolates a *path* on github.com → repos only get referrer data, not raw backlinks.
- Free backlink web UIs (OpenLinkProfiler, Semrush, Majestic) are JS-rendered with no free API; not scriptable here.
- New/small sites have thin coverage in any crawl index — expect sparse results until they accrue links.
- The `ambiguous` bucket is a real answer, not a failure. A hostname alone cannot tell your comment from a stranger's; resolving it takes a human, and the tool refuses to guess in your favour.

---

**Part of [TinkerClaw](https://github.com/globalcaos/tinkerclaw)** — real-time token tracking, self-improving crons, persistent cognitive memory. This is one piece of that stack; the repo has dozens more.

👉 **https://github.com/globalcaos/tinkerclaw**

_Clone it. Fork it. Break it. Make it yours._
