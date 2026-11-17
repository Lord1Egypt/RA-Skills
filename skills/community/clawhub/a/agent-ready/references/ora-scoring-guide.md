# Ora Scoring Guide

Reference for interpreting a report from https://ora.sh before acting on it. Read this
before working the 9-item checklist in `SKILL.md` — it tells you which findings are
worth fixing and which aren't, which is most of the judgment this skill requires.

## How the score is built

Ora returns a single 0–100 score built from two tiers of findings:

- **Essential findings** — things that materially block or degrade an agent's ability
  to understand or trust the site. Missing trust anchor pages, missing structured data,
  a missing or broken `llms.txt`, and genuine content-behind-JavaScript gaps live here.
  These carry the most weight in the score and are the ones worth spending session time
  on.
- **Recommended findings** — things that help but aren't load-bearing. Brand
  discoverability signals, secondary schema completeness, and some crawler-specific
  checks live here. These move the score less and are lower priority when time is
  limited.

Treat the tier label as a priority order, not a pass/fail gate. A site can score
respectably with a couple of unresolved Recommended findings; it should not ship with
unresolved Essential ones.

## What each finding actually means

Ora's evidence field is more useful than its headline finding name. Two sites can get
the same finding label for different underlying reasons — one because the content is
genuinely missing, one because the probe tripped over something structural (a redirect,
a caching layer, a sparse-but-legitimate homepage). Always read the evidence before
deciding an item needs work. The 9-item checklist in `SKILL.md` encodes this: several
items are marked "investigate before acting" specifically because the raw finding
alone is not enough signal to act on.

## Findings that are Ghost Pro platform limitations, not owner-fixable gaps

These will show up in a report and cannot be resolved within Ghost Pro's managed
hosting, regardless of how much time is spent:

- **Markdown content negotiation** (checklist item 9) — requires server config Ghost
  Pro does not expose.
- **`robots.txt` customization** — not editable on Ghost Pro; the platform serves its
  own default.
- **Fine-grained crawler/bot-level access rules** (part of checklist item 6) — the WAF
  and bot handling layer is platform-controlled.

When a report surfaces one of these, the correct action is to flag it to the owner as a
known ceiling, not to spend a session hunting for a workaround inside Ghost Pro. If the
owner wants it resolved, that's a decision to move specific functionality to
infrastructure outside Ghost — a larger call than a single audit session, and out of
scope for this skill's direct execution (see the Codex/coding-agent handoff triggers in
`SKILL.md` for what that would actually require).

## Findings that are commonly false positives on sparse homepages

A homepage that's mostly a hero image, a short tagline, and a feed teaser will often
trip:

- **Content without JavaScript** (checklist item 5) — Ghost is server-rendered by
  default, so a low-content reading is usually about how *little* content the homepage
  has, not about it being client-rendered. Confirm with the direct curl/character-count
  check in `SKILL.md` before treating this as real.
- **Agent-friendly 404s** (checklist item 7) — an automated probe can be thrown off by
  redirects or edge caching in ways a direct manual curl check will not be. Confirm
  manually before acting.

Both of these are called out in the checklist as "investigate before acting" for this
reason — the automated finding is a prompt to check, not a fix ticket on its own.

## Score interpretation

- **Below ~50:** Usually indicates one or more Essential findings are genuinely unmet —
  most commonly missing trust anchor pages or missing structured data. These are the
  fastest, highest-leverage fixes available (checklist items 1 and 2) and should be
  addressed first.
- **50–70:** Typically means the Essential basics are in place but `llms.txt` is either
  missing or thin, or a Recommended finding or two remain open. Work through the
  remaining checklist items in order.
- **70+:** Represents most of what's actually achievable on Ghost Pro without adding a
  CDN or edge layer in front of it. Some Recommended findings (brand discoverability,
  the platform-limited items above) will likely remain open indefinitely on this stack
  — that is expected, not a failure of the audit or the fix work.
- **There is a practical ceiling on Ghost Pro without a CDN.** Markdown content
  negotiation and fine-grained crawler rules are structurally unavailable, so a report
  that has resolved every fixable item may still sit short of a perfect score. Don't
  chase the last few points by working around platform limitations — flag them and
  move on.
