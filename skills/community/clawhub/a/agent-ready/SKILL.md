---
name: agent-ready
version: 1.0.0
description: "Audit any personal or brand site for AI agent discoverability and fix what is fixable — structured data, trust anchor pages, llms.txt, crawlability checks, and Ghost-specific deployment patterns. Ghost Pro native."
homepage: https://github.com/highnoonoffice/hno-skills
source: https://github.com/highnoonoffice/hno-skills/tree/main/agent-ready
binaries: [curl, node, python3]
license: MIT
---

# agent-ready

A site is agent-readable when an AI agent — a browser-using assistant, a crawler-fed
model, a research tool — can land on it, understand who runs it, and find the specific
things it's looking for (contact info, a body of work, machine-readable facts about the
owner) without a human translating for it. Most sites are not built with that reader in
mind. This skill audits a site against a fixed checklist, tells you what's actually
broken versus what only looks broken, and either fixes it directly or hands the fix to
a coding agent when the fix requires touching a git-managed codebase.

This skill is written for three cooperating agents:

- **An orchestrator agent** (browser-capable, holds CMS/API credentials) — runs the
  audit, evaluates findings, executes CMS-level work directly: structured data
  injection, trust anchor page creation, redirect wiring, and any step that only needs
  an API call or a browser session.
- **A coding agent** (works inside a git repository, opens pull requests) — handles
  anything that requires modifying a file that lives in version control: theme
  templates, edge functions, server config, redirect logic that ships as code.
- A second coding agent role, interchangeable with the first — the skill does not
  distinguish between coding agents. Whichever one is available receives the same
  handoff format and does the same class of work.

The orchestrator never edits repository files itself. The coding agent never touches
CMS credentials or executes browser sessions. That boundary is enforced by Gate 5
below, not by convention.

## skill_gates

<skill_gates version="1.0" mode="mandatory_pre_execution" evaluation="sequential" on_violation="stop_and_report">

  <gate id="audit_first" priority="1" severity="hard" scope="session_start">
    <condition>About to execute any agent-readiness improvement</condition>
    <question>Have I run the Ora audit at https://ora.sh this session and have the scored report in context?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Run the audit first. Never execute fixes from memory or a previous session report.</fail_action>
  </gate>

  <gate id="owner_approves_copy" priority="2" severity="hard" scope="pre_publish">
    <condition>About to create or update any public-facing page (about, contact, privacy, llms.txt)</condition>
    <question>Has the owner read and explicitly approved the exact copy that will be published?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Show the copy verbatim. Wait for approval. Never publish unreviewed copy.</fail_action>
  </gate>

  <gate id="read_before_inject" priority="3" severity="hard" scope="pre_inject">
    <condition>About to write to Ghost code injection head or footer</condition>
    <question>Have I fetched and read the current head injection content this session before appending?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Fetch first. Append-only — never overwrite.</fail_action>
  </gate>

  <gate id="verify_after_each" priority="4" severity="hard" scope="post_execute">
    <condition>Just completed any improvement step</condition>
    <question>Have I verified the change is live via curl or browser snapshot before moving to the next item?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. Verify first. API 200 does not mean live and correct.</fail_action>
  </gate>

  <gate id="codex_for_code" priority="5" severity="hard" scope="pre_execute">
    <condition>The fix requires modifying a file in a git repo (theme files, edge config, redirect logic in code)</condition>
    <question>Am I handing this to the coding agent via a structured handoff block rather than executing it myself?</question>
    <pass_action>Proceed.</pass_action>
    <fail_action>Stop. The orchestrator does not modify repo files directly. Write the spec block, not the code.</fail_action>
  </gate>

</skill_gates>

Every gate is hard and sequential within its scope: session_start gates block everything
downstream, pre_publish and pre_inject gates block the single step they guard, and
post_execute repeats after every improvement, not just the last one. If a gate fails,
stop and resolve it before continuing — do not work around it, and do not treat a
previous session's pass as still valid.

## Audit Tools

Several tools audit agent-readiness from different angles. Run more than one — they
catch different things.

**Ora** — https://ora.sh
Primary tool for this skill. Returns a scored 0–100 report with Essential and
Recommended findings, each with evidence and a recommended fix. Run this first every
session. See `references/ora-scoring-guide.md` for score interpretation.

**llmstxt.cloud** — https://llmstxt.cloud
Validates your llms.txt specifically — checks that it exists at the expected path,
parses correctly, and follows the emerging convention. Run this after completing
checklist item 3.

**Google Rich Results Test** — https://search.google.com/test/rich-results
Validates JSON-LD structured data against Google's rich result types. Run this after
completing checklist item 2. Paste the live URL, not the raw JSON — it needs to test
the actual embedded block.

**Schema.org Validator** — https://validator.schema.org
Broader vocabulary coverage than the Rich Results Test. Use for schema types Google's
tool doesn't specifically support (SoftwareApplication in some configs). Also paste
the live URL.

**web.dev/measure (Lighthouse)** — https://web.dev/measure
General page quality audit including some crawlability signals. Less agent-specific
than Ora but useful for catching content-without-JS issues independently. Run if
checklist item 5 needs deeper investigation.

No single tool covers everything. Ora drives the session. The others verify specific
steps.

A report from an earlier session is stale the moment any change has been made to the
site since; re-run rather than trusting memory of a prior score — see Gate 1.

Read `references/ora-scoring-guide.md` for how to interpret the Ora score and which
findings are platform limitations versus real gaps before acting on the report.

## The 9-Item Checklist

Work the list in order. Each item states what it means, whether to act on it directly,
investigate before acting, or skip it outright, plus execution and platform notes.

### 1. Trust anchor pages (`/about`, `/contact`, `/privacy`)

**What it means:** These are the pages an agent (or a human it's assisting) checks to
verify a site is run by a real, identifiable entity. A missing or thin `/about` page is
one of the most common reasons a site reads as low-trust to both agents and search
crawlers.

**Action:** Do — this is directly fixable in one session.

**Execution notes:**
- The orchestrator creates these via the Ghost Admin API pages endpoint with
  `?source=html`.
- Each page needs 500+ characters of real content — not placeholder text, not a single
  sentence. A thin page fails the same way a missing page does.
- Gate 2 applies: show the owner the exact copy for each page before it's created, and
  wait for explicit approval.
- Verify with a direct URL check on each page after creation — see Gate 4.

### 2. Person JSON-LD schema

**What it means:** A `Person` schema block in the page's structured data gives agents
and search engines a machine-readable identity record: who the site belongs to, and
where else that identity is verifiable.

**Action:** Do.

**Execution notes:**
- On Ghost Pro this is written via code injection (site header), which requires a
  browser session — integration tokens cannot write to code injection. See the Ghost
  Pro Constraints section below.
- Required fields: `@type: Person`, `name`, `url`, `description`, and a `sameAs` array
  listing public profile URLs (social platforms, publication bylines, any page that
  independently confirms the identity).
- Gate 3 applies: fetch and read the current head injection content before writing.
  Append the new script block — never replace what's already there.
- Verify with: `curl -s https://yourdomain.com | grep -o 'application/ld+json'`

### 3. llms.txt

**What it means:** A plain-text file at a well-known location that gives agents a
direct, structured summary of the site — who runs it, what to expect, where to look for
specific things — without needing to parse HTML.

**Action:** Do.

**Execution notes:**
- **Option A (recommended):** a Ghost page with the slug `llms.txt`, which Ghost serves
  at `/llms.txt/`. Self-contained, no additional infrastructure.
- **Option B:** a raw file committed to a GitHub repo, with a Ghost redirect rule
  pointing `/llms.txt` at the raw URL. Use this only when the content needs to live in
  version control for other reasons (e.g., it's generated from repo content).
- Gate 2 applies: the owner approves the exact copy before publish.
- Verify with: `curl -s https://yourdomain.com/llms.txt/` and confirm real content
  comes back, not a 404 or a redirect loop.
- See `references/llms-txt-templates.md` for section-by-section templates by site type.

### Bonus: AI.txt (emerging standard, optional)

**What it means:** `AI.txt` is the IAB Tech Lab's emerging standard for AI content
licensing declarations — it tells AI systems what they are and are not permitted to do
with your content (train on it, summarize it, reproduce it). Distinct from
`llms.txt`, which is about discoverability and routing. `AI.txt` is about rights and
permissions.

**Action:** Optional — not yet scored by Ora or enforced by any major AI system. Worth
knowing about and worth adding if you have a position on AI training use of your
content.

**Execution notes:**
- Served at `/ai.txt` at the site root — same placement convention as `robots.txt`.
- Same Ghost Pro hosting constraint as `llms.txt`: use a Ghost page with slug `ai.txt`
  or a redirect rule pointing to a hosted file.
- Format spec: https://ai-txt.org
- For a personal content site with no explicit objection to AI training use, omitting
  this file is fine — absence is not interpreted as permission denied by current
  tools.

### 4. Organization schema completeness

**What it means:** Ora may separately flag organization-level structured data. For a
personal or single-owner brand site, this is not a distinct build — it folds into the
Person schema from item 2.

**Action:** Fold into item 2 — no separate action if that step was done correctly.

**Execution notes:**
- Add or extend the `sameAs` array on the Person schema rather than building a parallel
  `Organization` block.
- `contactPoint` and `address` are business/organization fields — skip these for
  personal sites; they don't apply and adding them without real data creates bad
  structured data, which is worse than none.

### 5. Content without JavaScript

**What it means:** Whether the page's core content is present in the raw HTML response,
or only appears after client-side JavaScript runs. Agents and crawlers that don't
execute JavaScript only see the former.

**Action:** Investigate before acting.

**Execution notes:**
- Ghost is server-rendered by default, so this finding is often a false positive —
  usually triggered by a sparse homepage (e.g., a homepage that's mostly a hero image
  and a feed teaser) rather than an actual client-rendering gap.
- Investigate with:
  ```
  curl -s https://yourdomain.com | python3 -c "import sys; h=sys.stdin.read(); print(len(h), 'chars'); print('H1 found' if '<h1' in h.lower() else 'NO H1')"
  ```
- Only act — and only then decide what "act" means for the specific page — if this
  investigation confirms a real gap (very low character count and no H1). If the page
  has substantive server-rendered content and simply reads as sparse to the scoring
  tool, there is nothing to fix.

### 6. Agent crawler reachability

**What it means:** Whether specific named crawlers/agents (e.g., ChatGPT-User,
ClaudeBot, Google-Extended, and others Ora checks by name) can reach the site.

**Action:** Skip / informational only.

**Execution notes:**
- An "unknown" result against a specific bot (commonly seen against less-established
  crawler identities) does not mean that bot is blocked — it usually means Ora has no
  signal either way, not a negative signal.
- What matters is that the major, well-established identities — ChatGPT-User,
  ClaudeBot, Google-Extended — pass. If they do, the site is reachable by the agents
  most likely to matter.
- On Ghost Pro, the WAF and bot-handling layer is platform-controlled — not something
  the owner can configure. There is no owner-actionable fix here regardless of the
  result.

### 7. Agent-friendly 404s

**What it means:** Whether a nonexistent path returns a real 404 (helpful — an agent
can tell the page doesn't exist) versus something that looks like content but is a
broken or infinite response (unhelpful — an agent may treat it as real).

**Action:** Investigate before acting.

**Execution notes:**
- Probe manually rather than trusting the audit tool's own probe:
  ```
  curl -s -o /dev/null -w "%{http_code}" https://yourdomain.com/path-that-does-not-exist
  ```
- Ghost handles 404s natively out of the box. A failure in the audit tool's automated
  probe does not necessarily mean the site itself is misbehaving — tooling probes can
  be tripped up by redirects or edge caching that a direct curl check won't show.
- Only act if the manual curl check confirms an actual `200` on a path that shouldn't
  exist. If it correctly returns `404`, there's nothing to fix regardless of what the
  automated report says.

### 8. Brand name discoverability

**What it means:** Whether the owner's name or brand reliably surfaces in search and
agent-facing retrieval when queried directly.

**Action:** Skip — not actionable in a single session.

**Execution notes:**
- This is a content and SEO outcome, built over time through published work, backlinks,
  and citation — not something with a single configuration fix.
- Nothing to build or execute here. Flag it to the owner as a long-horizon item if it
  scores poorly, but don't attempt a one-session fix.

### 9. Markdown content negotiation

**What it means:** Serving a markdown version of a page to clients that request it
(via `Accept` header content negotiation), so agents that prefer structured markdown
over HTML can get it directly.

**Action:** Skip for Ghost Pro.

**Execution notes:**
- This requires server-level content negotiation config that Ghost Pro's managed
  hosting does not expose.
- Flag it to the owner as a known platform ceiling — do not attempt a workaround inside
  Ghost Pro's constraints. If the owner wants this specifically, it requires moving
  content negotiation to infrastructure outside Ghost (see the Codex/coding-agent
  handoff triggers below), which is a larger decision than a single audit session.

## Score Tracking

Ora does not save history. Log your score each session so you can see progress over
time.

Add a simple table to a markdown file in your vault or repo — one row per session:

| Date       | Score | Items completed this session          | Remaining ceiling items       |
|------------|-------|-----------------------------------------|--------------------------------|
| YYYY-MM-DD | 51    | baseline                                | all                             |
| YYYY-MM-DD | 57    | trust pages, JSON-LD, llms.txt          | markdown negotiation, WAF       |
| YYYY-MM-DD | 65    | —                                        | markdown negotiation, WAF       |

Two things to log beyond the score:
- What you actually completed this session (not what the report says is done — what
  you verified as live)
- Which remaining items are platform ceiling vs genuinely fixable (so you're not
  re-evaluating the same Ghost Pro limitations every session)

A score that stops moving is usually one of two things: all fixable items are done, or
a fixable item was missed. The log tells you which.

## Ghost Pro Constraints

Ghost Pro's managed hosting draws a hard line between what an integration token can do
and what requires an authenticated browser session. Get this wrong and steps fail with
a 403 that has nothing to do with the token being invalid.

- **Settings write endpoints return 403 for integration tokens.** Code injection
  (header/footer), site settings, and redirects are not reachable via the Admin API
  with a token alone — they require a real browser session against the Ghost Admin UI.
- **Ghost Pro login flow:** email only is submitted on the login form. Ghost sends a
  6-digit code to that inbox. The code is entered on the verify screen. There is no
  password step on Ghost Pro — the code *is* the authentication.
- **Use a dedicated staff account for the orchestrator**, not the owner's own account,
  for any browser-session work.
- **What integration tokens are good for:** posts, pages, images, members, tags. Item 1
  (trust anchor pages) is achievable entirely through the API token — no browser
  session needed.
- **What requires a browser session:** code injection head/footer (item 2), site
  settings, and the redirects UI (relevant to item 3, Option B).
- **PUT requests on posts/pages must always fetch first** to get the current
  `updated_at` value and include it in the PUT body. Omitting it returns a `409`
  conflict, not a helpful error — this is the single most common avoidable failure in
  this workflow.

Full API patterns, request shapes, and the browser login flow step by step are in
`references/ghost-deployment.md`.

## Codex and Claude Code Handoff Triggers

The orchestrator hands off to a coding agent — rather than attempting the fix itself —
whenever the fix requires modifying a file that lives in a git-managed repository. This
is Gate 5, and it is not optional: the orchestrator does not have a code editor, does
not open pull requests, and should not attempt either.

Hand off when the fix involves:

- Theme `.hbs` file modifications
- Serving `/llms.txt` (or any other agent-facing file) from an edge function on a
  domain that isn't Ghost Pro itself
- `robots.txt` changes — not exposed for editing on Ghost Pro
- Redirect logic implemented in a deployed repository (as opposed to Ghost's own
  redirects UI, which is a browser-session task, not a handoff)
- Any change that requires a git commit and a pull request

**Handoff format:** a structured `[AGENT_HANDOFF]` block, matching the Ping Pong
protocol — the orchestrator writes the spec, the coding agent builds against it and
opens a PR, and the orchestrator reviews the PR that comes back. The orchestrator never
writes the code itself and never bypasses this by inlining a code change into the
conversation.

Full handoff templates for each trigger type, and the review checklist the orchestrator
runs against a returned PR, are in `references/codex-handoffs.md`.

## Reference Files

- `references/ora-scoring-guide.md` — how to read the Ora score, tier definitions,
  which findings are platform limitations, which are common false positives, score
  interpretation.
- `references/ghost-deployment.md` — full Ghost Pro API and browser-session patterns
  for this skill.
- `references/json-ld-templates.md` — Person, Organization, and SoftwareApplication
  schema templates, plus validation tools.
- `references/llms-txt-templates.md` — llms.txt templates by site type, with file
  location tradeoffs.
- `references/codex-handoffs.md` — handoff templates by trigger type and the PR review
  checklist.
- `references/verification-commands.md` — every curl/shell command used across the
  checklist, collected for quick reference during Gate 4 verification.
