---
name: codebase-explainer
description: >-
    Produce a durable onboarding artifact for a codebase — writes ONBOARDING.md covering a
    "read this first" minimum, system overview, dependency map, startup flow, auth flow, and
    5-15 important files, every claim backed by file:line citations; refreshes an existing
    onboarding doc instead of rewriting it. Use this skill whenever the user says "explain this
    codebase", "explain the codebase", "onboard me", "give me a tour", "tour this repo", "what
    does this repo do", "where do I start", "codebase overview", "read this first", "I haven't
    looked at this in months", or "/codebase-explainer" — even if they don't name the skill.
---

# Codebase Explainer

Produce a durable onboarding artifact — the document past-you wishes you'd written before stepping away from this repo for six months. Not a chat answer that disappears: a committed `ONBOARDING.md` with a tight "read this first" list, system overview, dependency map, startup flow, auth flow, and the important files. Every claim cited with `file:line`.

## When to use this skill

- "explain this codebase" / "explain the codebase" / "what does this repo do"
- "onboard me" / "give me a tour" / "tour this repo" / "where do I start"
- "I haven't looked at this in months" / "I forgot how this works"
- "codebase overview" / "read this first" / "create an onboarding doc"
- `/codebase-explainer` / `/onboard`

Do **not** auto-trigger for:

- Architecture refactor suggestions → [`improve-codebase-architecture`](../improve-codebase-architecture/SKILL.md)
- Feature implementation → [`task-executor`](../task-executor/SKILL.md)
- Bug triage → [`diagnose`](../diagnose/SKILL.md)
- A specific diff review → [`code-review`](../code-review/SKILL.md)
- Session hand-off (different artifact, session-scoped) → [`handoff`](../handoff/SKILL.md)

## Workflow

### 1. Detect the lay of the land (no sub-agents yet)

Read root-level signals directly to scope the exploration:

- **Manifests** — `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `*.csproj`, `*.sln`, `Gemfile`, `composer.json`, `pom.xml`, `build.gradle*`.
- **Entry-point hints** — `next.config.*`, `vite.config.*`, `tsconfig.json`, `Procfile`, `Dockerfile`, `docker-compose*.yml`, `main.*`, `Program.cs`, `manage.py`.
- **Existing docs** — `README.md`, `CONTEXT.md`, `docs/`, any `ONBOARDING.md` already present.
- **Workspace shape** — monorepo (`pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`) vs. single project.

If an `ONBOARDING.md` already exists, this is **refresh mode**: read it first, then look for drift (new top-level deps, moved entry points, new/removed routes, auth changes) and update in place — don't rewrite from scratch.

### 2. Run Explore sub-agents in parallel

Spawn `subagent_type=Explore` calls in a **single message** so they run concurrently. Brief each agent self-containedly — it has no conversation context. Default fan-out:

- **System overview** — what this project actually does, key domains, top-level modules, public-facing surfaces (HTTP routes / CLI commands / exported APIs).
- **Dependency map** — top-level prod deps only (skip dev/test/types). For each: what it does *in this codebase* (not generic), and the load-bearing call site (`file:line`). If a dep is genuinely non-obvious (niche library, internal fork, name that doesn't reveal its purpose), the agent MAY check `context7` (or any docs-MCP server available in the environment) for a one-line "what is this library" — `context7__resolve-library-id` → `context7__query-docs`. Skip the lookup for well-known libraries (React, Express, Prisma, etc.) — the *generic* description is what we're trying to avoid; what matters is how it's used *here*. The "how it's used here" line requires a call site the agent actually opened. If no call site is found, the row reads **"declared but no usage found"** — that's a finding (candidate for removal), not a gap to paper over with a guess from the package name.
- **Startup flow** — entry point → bootstrap → config loading → server start. A numbered sequence with `file:line` per step.
- **Auth flow** — login/session/token handling, middleware/guards, user model, where authorization decisions are made. This section must be a **traced code path** — a middleware/guard/session check the agent read this session, cited `file:line` — never an inference from an auth library appearing in the manifest. If none, the agent must say "no auth detected" explicitly AND state what was searched (e.g. "grepped for middleware, `session`, `jwt`, `[Authorize]`, guards — no hits") so Step 3 doesn't fabricate one.
- **Important files** — the 5–15 files a new contributor *must* know about, each with a one-line "why it matters." A file earns its slot by being load-bearing, and the agent names the evidence per file: imported widely (roughly how many importers), owns a core domain concept, or is an entry point. "Looks important" is not evidence.

Each agent reports back in ≤300 words with `file:line` citations. Don't ask Explore to read entire files — ask for the specific answer plus citations.

### 3. Synthesize ONBOARDING.md

Write the artifact to `docs/ONBOARDING.md` if a `docs/` directory exists, otherwise `ONBOARDING.md` at repo root.

**No-fabrication gate:** every claim in the file traces to a probe run this session — a file an agent read, a grep it ran. If a claim can't name its probe, it's a hypothesis: verify it or omit it. Never fill a section by inference from framework conventions ("Next.js apps usually…").

Sections, in this order:

1. **Read this first** — 3–7 bullets max. The minimum a fresh contributor needs to not be dangerous.
2. **System overview** — 1–3 paragraphs. What it does, who it serves, the dominant architectural shape.
3. **Startup flow** — numbered, with `file:line` per step.
4. **Auth flow** — same shape, or a one-liner "No authentication layer — this is X (searched: middleware, session/token handling, guards)" if the agent confirmed none.
5. **Dependency map** — table: `Dependency | What it does here | Key call site`.
6. **Important files** — bulleted list with `file:line` and a one-line "why it matters."
7. **Project glossary** *(optional)* — only if `CONTEXT.md` exists or domain terms surfaced repeatedly during exploration.
8. **Footer** — one line: *"Generated by `/codebase-explainer`. Re-run to refresh."*

No timestamps in the file body (dates rot). The git history is the timestamp.

### 4. Render a condensed summary inline

After writing the file, render in chat: the "Read this first" bullets verbatim, plus a one-sentence pointer to the file path. Do **not** re-paste the full document — the file is the artifact.

### 5. Offer the share step (optional)

If making this teammate-accessible would help, mention `ShareOnboardingGuide` — it uploads `ONBOARDING.md` and returns a link. Offer once; never auto-invoke.

## Examples

### Example 1: First pass on a six-month-old project

**User:** "I haven't touched this repo since November — onboard me"

**Claude:**
1. Reads `package.json`, `next.config.ts`, `prisma/schema.prisma`, existing `README.md`. Notes: Next.js App Router + NextAuth + Prisma + Postgres.
2. Spawns five Explore agents in parallel (overview, deps, startup, auth, important files) in one message.
3. Synthesizes → writes `ONBOARDING.md` with startup flow rooted at `app/layout.tsx:12` → `lib/auth.ts:34` and auth flow citing the NextAuth `authOptions` and the `requireSession()` helper.
4. Prints the "Read this first" bullets and the file path. Offers `ShareOnboardingGuide`.

### Example 2: Refresh against an existing onboarding doc

**User:** "/codebase-explainer — refresh the onboarding doc, I added Stripe and a new admin route last sprint"

**Claude:**
1. Reads existing `docs/ONBOARDING.md`. Spawns Explore agents scoped to "what's changed": new top-level deps, new routes under `app/**/route.ts`, auth changes.
2. Updates the dependency map (Stripe row added with `lib/payments/stripe.ts:18` citation), appends the admin route to startup flow, leaves untouched sections alone.
3. Reports a diff-style summary in chat: "+1 dep, +1 route, auth unchanged."

## Anti-patterns

- ❌ Generic framework descriptions ("This is a Next.js app."). Call out what makes THIS codebase non-obvious — the custom session helper, the funky background job runner, the legacy module that traps newcomers.
- ❌ Listing every dependency including dev/test/types. Prod + top-level only.
- ❌ "Important files" with 40 entries. 5–15 is the budget. If you can't pick, you don't understand the codebase yet — Explore more.
- ❌ Inventing an auth flow when there isn't one. If the agent reports no auth, the section says "No authentication layer" plus what was searched. That's load-bearing information for a future reader.
- ❌ Auth described from the manifest instead of the code. ❌ "Uses NextAuth for authentication" because `next-auth` sits in `package.json` vs. ✅ "Requests hit `middleware.ts:8` → `auth()` from `lib/auth.ts:12`; unauthenticated users redirect at `middleware.ts:19`." Trace the path or write "none detected (searched: …)".
- ❌ Papering over a dependency with no found call site. "Declared but no usage found" goes in the table verbatim — it's a finding.
- ❌ Important files picked by vibes. Each entry names its evidence: import count, domain concept owned, or entry-point role.
- ❌ Reading whole source files into the main context. Sub-agents return summaries with `file:line` citations — trust them.
- ❌ Claims without `file:line` citations. A claim the next reader can't verify rots fast.
- ❌ Hard-coded dates ("as of November 2025") in the file body. Git history is the timestamp.
- ❌ Rewriting an existing `ONBOARDING.md` from scratch when the user asked to refresh.
- ✅ Tight "read this first," cited everywhere, explicit about absences, refreshable.

## Notes

- **Composes with** [`improve-codebase-architecture`](../improve-codebase-architecture/SKILL.md): an onboarding pass often surfaces shallow-module clusters worth a deepening review. Hand the user a pointer; don't propose refactors here.
- **Composes with** [`handoff`](../handoff/SKILL.md): `ONBOARDING.md` is project-level orientation (durable across many sessions); a handoff is session-level state. Different artifacts, both useful.
- `ShareOnboardingGuide` (when available in the environment) uploads `ONBOARDING.md` and returns a teammate-shareable link. Optional; user-initiated.
