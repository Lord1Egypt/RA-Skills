# Backlink sources — auth, limits, when to use

Pick the source by what the target is and what auth is available.

## 1. `github` — repo referrers (works now, no extra auth)
- Target: `owner/repo` (e.g. `globalcaos/tinkerclaw`).
- Uses `gh api repos/<owner>/<repo>/traffic/popular/referrers` (gh must be authed; it is).
- **Caveat**: returns traffic REFERRERS (top ~10 sites that sent visitors), NOT a raw backlink list. Counts are views, not links. No SEO tool can isolate a path on github.com, so this is the only repo-scoped signal.
- Best for: the tinkerclaw repo.

## 2. `backlinks` — backlinks.sh (Common Crawl web graph)
- Target: a bare domain (`thetinkerzone.com`).
- Endpoint: `GET https://api.backlinks.sh/v1/backlinks?target=<domain>`, header `x-api-key: <key>`. That URL is a constant in the script — it is the only host this skill ever contacts on its own.
- Auth: a backlinks.sh API key. Sign up at https://backlinks.sh — **3 free calls**, then pay-as-you-go (~$0.01/call, no subscription). This is the only paid thing in the skill, and only the `backlinks` source spends it.
- **Where the key lives**: the `BACKLINKS_SH_API_KEY` env var, or your OS keychain (`secret-tool` on Linux, `security` on macOS; service `backlinks-sh`, account `api-key`). Nowhere else — there is no plaintext-file fallback. If no keychain is available, `--login` refuses and writes nothing. A `~/.config/backlinks-sh/credentials.json` left by an older version is detected only to explain why it stopped working; it is never used to authenticate.
  - Store it: `printf %s "$KEY" | node scripts/backlink-audit.mjs --login` (stdin, never argv).
  - Remove it: `node scripts/backlink-audit.mjs --logout` — clears the keychain entry **and** deletes that legacy file if present. Local removal does not revoke the key server-side; rotate it in your backlinks.sh account.
- Returns up to ~10k referring domains. Response shape is parsed defensively (backlinks/referring_domains/results array; string or object items). If the live shape differs, adjust `fromBacklinks` in the script.
- Best for: a real crawl-based backlink list for any owned site; one-shot audits.

## 3. `gsc-csv` — Google Search Console export (authoritative, free, owned sites only)
- Target: a domain we own and have verified in GSC (`thetinkerzone.com`, `sprintpaper.com`).
- GSC's **Links → Top linking sites** report lists every external site Google knows links to us — the authoritative free source, but only for properties we own/verify.
- This skill ingests a CSV **export** (no OAuth needed): in GSC open the property → Links → Top linking sites → Export → CSV, then run with `--source gsc-csv --csv <path>`.
- The CSV's first column is the linking site/domain; a later numeric column is the linking-pages count. Parser is tolerant of header variations.
- The CSV path deliberately avoids OAuth: no Google credential is requested, stored or sent by this skill. Wiring full OAuth would let it run unattended — that is a future upgrade, not something shipped here.

## Classification (all sources)
Edit `assets/ours-allowlist.json`. A link is **ours** if its source host (and optional `path_prefix`) matches a rule; hosts in `ambiguous_domains` that no path rule resolves are reported **ambiguous** (e.g. a link from github.com could be a comment you wrote or a stranger's — resolve it by hand from your own record of authored comments, then pin it in `ours_urls`); everything else is **organic** (external).

## Feeding the pulse graph
`--write-state --target-key <tinkerclaw|thetinkerzone|sprintpaper>` writes `inbound_targets.<key>.{external,ours}` into `inbound-campaign-state.json`. The control-panel pollers read those into the Inbound-links graph (solid=external, dashed=ours, one hue per target). Ambiguous links are excluded from the written counts (they'd otherwise inflate "ours").
