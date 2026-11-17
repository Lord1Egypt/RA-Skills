---
name: candor-ui
description: Build agent product UIs with Candor UI, a shadcn/ui registry of React components for agents that do real work - approvals, plans, diffs, run logs, chat and tool calls, traces and evals, and the app shell around them. Use when building or changing a React or Next.js interface for an AI agent, when the project's components.json lists the @candor registry, or when the user mentions Candor. Covers installing components, choosing the right one, wiring the Vercel AI SDK, Claude Agent SDK or AG-UI adapter, and the honesty rules every Candor screen follows.
---

# Candor UI

Candor UI is for agents that change real things: approvals, plans, diffs and run logs, with data that says how sure it
is (a value is measured or provisional, a reasoning step verified or believed) and honesty rules every component
keeps (`https://candor.themethodic.com/principles`). It is a shadcn/ui registry: components are copied into the project
with the shadcn CLI and then belong to it. Every component takes plain, typed data, so it works with any model or
backend; adapters map the Vercel AI SDK, the Claude Agent SDK and AG-UI onto that data.

## Set up and install

Use the `candor-ui` CLI; it wraps the shadcn CLI and keeps a lockfile so updates can merge.

```bash
npx candor-ui@latest init --yes        # registry in components.json, the theme, its import; sets up shadcn if missing
npx candor-ui@4 add thread message composer
```

- **Where files land:** in folders of their own: `ui` primitives in `@/components/candor/ui/…`, libraries and types
  in `@/lib/candor/…` (for example `@/lib/candor/chat`), everything else in `@/components/candor/…` (for example
  `@/components/candor/thread`). Import from those paths; the `@/registry/…` paths in Candor's own repo don't exist in
  an app, and `@/components/ui/…` is shadcn's, not Candor's.
- **Client components:** anything with state or handlers needs `"use client"` at the top in the Next.js App Router.
- **Pro and Premium items** need the buyer's licence key. The person runs `npx candor-ui key <key>` themselves (it
  goes in `.env.local`, which must stay out of git); never ask for the key in chat or put it in a file you write. In
  CI, `CANDOR_LICENSE_KEY` is a secret.
- **Updates:** `npx candor-ui update` brings installed items to the latest release and keeps local changes with a
  three-way merge; commit `candor-lock.json`.
- **When something looks wrong:** `npx candor-ui doctor` checks the registry, the key, the theme import, dark mode,
  React and Tailwind, and says how to fix each.

Without the CLI, add `"@candor": "https://candor.themethodic.com/r/{name}.json"` to `components.json` and run
`npx shadcn@latest add @candor/<name>` (for paid items the registry entry needs
`"headers": { "Authorization": "Bearer ${CANDOR_LICENSE_KEY}" }`). `npx shadcn@latest mcp init --client claude` lets a
coding agent browse the registry.

Themes switch with `data-theme="light" | "dark" | "hc"` on `<html>`. With none set, the system's light or dark setting
applies; `"light"` turns that off. `"dark"` and `"hc"` also work on an inner element (a dark panel in a light page),
but `"light"` doesn't switch back inside a dark one: light is the `:root` default, not a theme of its own.

## Look things up

The docs MCP server is the quickest way to the right component and its exact props. It's free and read-only (no
licence key; it serves docs, never paid source). If it isn't connected, suggest the person adds it:

```bash
claude mcp add --transport http candor https://candor.themethodic.com/mcp
```

Other clients add `https://candor.themethodic.com/mcp` as a remote (streamable HTTP) server. When you build a new
screen, call `list_screens` first: it lists the screens an agent product needs, and `get_screen` gives one with its
layouts, the items that build each, the rules that matter on it and a brief for the agent that builds it. Its thirteen
tools:

- `list_screens` and `get_screen`: the screen catalogue, as above.
- `suggest_components`: describe the screen or feature; get the items that fit, an install command per tier, and a
  plain "Candor has no item for this" when nothing does. Pass `sdk` (`ai-sdk`, `claude` or `ag-ui`) so only your
  agent SDK's adapter is suggested.
- `search_docs`: find items and patterns by what they do.
- `get_component_docs`: one item's page (props, example with app import paths, functions, types, `LocaleProvider`
  keys). Read it before using an item.
- `get_brief`: the same page, as the brief to hand to another coding agent.
- `list_components`: every item by group, or one group's items.
- `get_pattern`: a common problem in agent UIs and the items that solve it.
- `get_started`: installing, connecting an agent SDK, licence keys and updates.
- `get_design`: the colour roles, type, radius, motion and themes, and how to re-token for a brand.
- `get_review_checklist`: the checks to run after each screen.
- `theme_check`: after editing `candor-brand.css`, call it with the file's contents; it runs the checks of
  `npx candor-ui theme check` and says what it couldn't measure.
- `item_changes`: before updating an item, what changed in it between the project's version (in `candor-lock.json`)
  and another: props, exports and string keys added, removed or retyped, files touched, and the CHANGELOG entries that
  name it. Records start at 2.7.0; for an earlier version it says what isn't known.

Without it, every docs page is Markdown at `https://candor.themethodic.com/docs/<name>.md`, indexed in
`https://candor.themethodic.com/llms.txt`.

## Choose components

Read `references/components.md` for every item, grouped by job, with its tier and what it exports. Pick by the job
the screen does, not by name similarity:

- **A conversation with an agent:** `thread`, `message`, `composer`, `tool-call`, `reasoning`, `citation`,
  `prompt-suggestions`, `permission-prompt` (a tool call waiting on the person), `ai-disclosure` (says it's an AI).
- **Work the agent proposes or does:** plans, approvals, diffs, run logs and run receipts are under *work*.
- **Trust and control:** `locked` for controls a person can't use (it says why), `approval-request` and
  `approval-queue` for decisions, `blast-radius` for what a change touches, `audit-log`, `type-to-confirm`,
  `permission-mode`, `checkpoint-list` and `restore-dialog` (a restore that says what it didn't undo),
  `ai-content-label`.
- **Operating agents:** *ops* and *evals* hold traces, usage, scorecards and review queues.
- **The app around it:** *shell* (layout, sidebar, command menu, session list).
- **App scaffolding:** *billing*, *team*, *admin*, *charts* and *layout* are the screens every app has, in Candor's
  theme. Not agent surfaces; the list puts them after the agent groups.

Install only what the screen needs. Check an item's props in its docs page or its source after installing; don't
guess them.

## Wire an agent

**Vercel AI SDK 7:** `useCandorChat(useChat(...), { agent })` returns `{ messages, composer, approvals, respond }`.

**AG-UI:** `useAgUi({ url: "/api/agent", agent })` returns the same `{ messages, composer, approvals, respond }`; a
run that ends on an interrupt shows it in `approvals`, and `respond` resumes it.

**Claude Agent SDK:** on the server, `streamClaudeAgent(({ canUseTool, abortController }) => query({ prompt,
options: { canUseTool, abortController, resume: sessionId, includePartialMessages: true } }), { signal:
request.signal, owner: userId })`; a second route calls `answerClaudeApproval(approvals, id, answer, { owner: userId
})`. In the browser, `useClaudeAgent({ api, approveApi, agent })` returns the same shape plus `usage` and
`permissionMode`. Approvals wait in an `ApprovalStore` (memory by default; pass your own so any instance can answer,
or answer from your own route with `onRespond`). For runs that survive a reload, pass a `ClaudeRunStore` and
`detach`, and re-attach with `attachClaudeAgentRun` and the hook's `attachUrl` and `runId`.

Both render the same way:

```tsx
<Thread footer={<Composer {...composer} />}>
  {messages.map((m) => <Message key={m.id} message={m} />)}
</Thread>
```

Show `approvals` with `PermissionPrompt` (or your own Allow and Deny buttons) and call `respond(id, approved, reason?,
{ updatedInput, answers, alwaysAllow })`. Never approve on the user's behalf, and never tick "always allow" for them.

## The honesty rules

Candor screens are built so a person can trust what an agent did. Keep these when you build with it:

- **Never render model output as HTML or as a clickable link.** Adapters read model text as a safe subset of
  markdown; links become plain text. Don't bypass this with `dangerouslySetInnerHTML` or a markdown renderer.
- **Unknown stays unknown.** If the service didn't measure a duration, cost or count, leave it empty. Never estimate
  one and present it as measured; an SDK's estimate is labelled as an estimate.
- **Reasoning is believed, not verified.** Show model reasoning as the model's own account.
- **A control that can't be used says why.** Use `locked` with a reason instead of a disabled button with no
  explanation.
- **Nothing is pre-selected** in a decision a person has to make (approve or deny, a destructive choice).
- **The agent is always named,** from your app's data, never from model output. System lines are your app's own
  strings.
- **Destructive actions confirm by typing,** and say what can and can't be undone.

## After each screen

Before moving on, run the review checklist in the `candor-agent-ui` skill (`skills/candor-agent-ui/references/review-checklist.md`
in the same repo, or the docs MCP's `get_review_checklist`): one line per check, each tied to a rule above. Fix what
fails first. For colours, type, radius, shadows, motion, density, themes and how to re-token for the brand, read
`references/design.md` (generated from the shipped CSS, so its values are the kit's; also the MCP's `get_design`).
Your own animation takes its timing from one of the fourteen motion families described there (reveal, arrive, pop, mark,
fill, value, move, overlay, press, tint, refuse, attention, live, clock), never a raw duration.
The manifest `motion.json` (served at `/r/v/<version>/motion-manifest.json`, and in each item's docs page under Motion) lists every
item's moments, each with its family, defaults and the sentence that says when it plays; read it before you tune or
add motion, instead of guessing which moments a component has. Sound has five events and its own rules, in the same
reference.
`candor-agent-ui` holds the design fundamentals for screens where an agent acts, with or without Candor: approval
ergonomics, the status vocabulary, folding turns, what to show while an agent works, AI disclosure and accessibility.

## Next.js and React Server Components

Components that need the browser are marked `"use client"`; display pieces stay server components. Put providers
that take icons or functions (`AgentRolesProvider`, `EntityKindsProvider`, `CardRegistryProvider`, presets) in one
client providers file. Event handlers and helpers exported from client modules (`formatRelative`, `defineCard`,
`toast`) belong in client code.

## Make it the product's own

- Override colour and type tokens in a CSS file imported after `candor.css` (shadcn names such as `--primary`,
  plus Candor's `--cd-*` and status pairs like `--cd-success-weak` / `--cd-success-text`), for every theme you support.
- `LocaleProvider`'s `nouns` sets the app's words ("project", "workspace"); `EntityKindsProvider` and `AgentRolesProvider`
  register its entity types and agent roles. Policy (who may do what, why something is locked) stays in the app and
  arrives as props.
