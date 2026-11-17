---
name: agent4-io
description: Build and run grounded business agents on agent4.io over MCP — agents, knowledge bases, load-on-demand skills, stateful Storylines and page playbooks.
homepage: https://agent4.io/cookbook
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "env": ["AGENT4_API_KEY"] },
        "primaryEnv": "AGENT4_API_KEY",
        "envVars":
          [
            {
              "name": "AGENT4_API_KEY",
              "required": true,
              "description": "Your agent4.io tenant API key (tk_…). Get it from the agent4.io dashboard → Tenant & API, or console.agent4.io → Settings → Security — the plaintext is shown once, at creation. No account yet? Sign up free at https://agent4.io (5M tokens/month, no card)."
            }
          ]
      }
  }
---

# agent4.io skills — build agents over MCP

This skill drives the **agent4.io** platform through its remote MCP server: create grounded agents,
knowledge bases, load-on-demand skills, stateful Storylines and page playbooks — all from your agent.

## Connect the MCP server (once)

The tools live on a remote MCP endpoint. Add it to your agent, authenticating with your tenant API key
(set `AGENT4_API_KEY`; get a key from **console → Settings → Security**, shown once at creation):

- **URL:** `https://api.agent4.io/v1/mcp`
- **Header:** `X-API-Key: $AGENT4_API_KEY`
- **Transport:** streamable-http

For Claude Code / any MCP client that takes a shell command:

```bash
claude mcp add --transport http agent4-io https://api.agent4.io/v1/mcp --header "X-API-Key: $AGENT4_API_KEY"
```

Once connected, call `tenant_info()` to confirm you are on the right tenant, then follow the recipes
below. This skill is a mirror of the always-current Cookbook at https://agent4.io/cookbook.

## Use it as a slash command

This skill is invocable directly — `/agent4-io <what you want>` — and routes to the right recipe below:

- `/agent4-io create a support agent grounded in these docs` → build a grounded agent
- `/agent4-io build a knowledge base from this site + these PDFs` → create & populate a KB
- `/agent4-io author a load-on-demand skill for booking` → write a Skill
- `/agent4-io compile this intake flow into a Storyline` → design & publish a Storyline
- `/agent4-io set a page-aware opener for /pricing` → configure a page playbook
- `/agent4-io how much quota have I used?` → usage & quota
- `/agent4-io who are my heaviest users this week?` → look up users and their sessions
- `/agent4-io what is a Storyline?` → look up an agent4.io concept

(On Claude Code and Cursor, the installer also lays down finer-grained shortcuts —
`/agent4-agent`, `/agent4-kb`, `/agent4-skill`, `/agent4-storyline`, `/agent4-docs` — but they all just
hand off to this same skill; here a single `/agent4-io` covers them.)

---

# agent4.io — build agents over MCP

This guide is assembled from the agent4.io Cookbook (https://agent4.io/cookbook). Modules:

- **agent4-io-principles** (v5) — Read-first design principles: one job per agent, few skills, grounded, verified — how to configure agents that work.
- **agent4-io-recipes** (v8) — Connect to agent4.io over MCP, install the skills, and run end-to-end recipes.
- **agent4-io-admin** (v9) — Create and configure agents (soul/task/tools/skills), load-on-demand skills, page playbooks (how the chat opens per page); check usage/quota and look up end users and their sessions.
- **agent4-io-knowledge** (v9) — Build, populate, verify and query grounded knowledge bases.
- **agent4-io-storyline** (v8) — Compile multi-step processes into stateful, guided Storyline graphs.

---
name: agent4-io-principles
description: Read-first design principles: one job per agent, few skills, grounded, verified — how to configure agents that work.
version: 5
---

Read-first design principles: one job per agent, few skills, grounded, verified — how to configure agents that work.

## Design principles — read this first

Most "the agent gives bad answers" problems are configuration, not the model. Follow these before you
build, and the results hold up. Ignore them and it is easy to assemble something that looks plausible and
behaves badly — then mistake that for a platform limit.

## Discover before you build — interview, don't just execute

"Create a support agent" is the **start of the conversation, not the spec.** Never answer it with a single
`create_agent` and hand back a blank shell. Work like the setup wizard: **interview first, plan the whole
setup, play it back, then build.** Ask in plain language — a few questions at a time, about their real
situation, not tool parameters — until you can picture the finished thing:

- **The job & who it serves.** What is this agent for, who talks to it, what does a *good* answer look
  like? One job per agent — if they describe three, that's three agents.
- **What it must answer from → a knowledge base.** Do they have documents, a site, policies, a price
  list? If facts have to be right, those become a [knowledge base](/cookbook/build-a-knowledge-base) you
  build and attach — not prompt text. If they have nothing yet, tell them what to gather.
- **Procedures it runs → skills.** Any "when X, do these steps" behaviours (book, screen, quote)? Each
  becomes a load-on-demand [skill](/cookbook/create-a-skill) with a sharp "use this when…".
- **Things it must *do* in other systems → MCP.** Check a calendar, look up an order, open a ticket?
  Those are [MCP tools](/cookbook/connect-your-mcp-server) to bind — ask which system and whether they can
  connect it.
- **A guided, stateful flow → a Storyline.** Is it a process with memory (intake → qualify → follow-up)
  rather than one-shot Q&A? That's a [Storyline](/cookbook/build-a-storyline), not just an agent.
- **How it opens and its hard limits.** The first line visitors see (→ a [page playbook](/cookbook/configure-page-playbooks))
  and the boundaries that go in `task` ("never quote a price", "never give legal advice").

Then **play the plan back before touching a tool** — "so I'll build: agent *Support*, a knowledge base
from your policy PDFs, a *booking* skill, and bind your calendar over MCP — right?" — and build only once
they confirm. Skipping this is exactly how you end up with an empty agent nobody wanted. A vague request
is a cue to ask, never a cue to guess.

## One agent, one job

Give each agent a **single, clearly bounded task**. A "does everything" agent — support *and* sales
*and* scheduling — has a diffuse `task`, competes with itself for attention, and answers each thing
worse. If you have three jobs, build three agents.

## Keep the skill count small

Attach **only the skills this agent's job needs — roughly five or fewer.** Skills are chosen by the model
from their one-line `description`; the more you attach, the harder that choice, and the more often it
loads the wrong one or none. A focused set with sharp "use this when…" descriptions beats a big pile.

- Each skill's `description` says **when** to reach for it, in one line.
- Procedures live in `instructions` (loaded on demand), never in `soul` (paid for every turn).
- If two skills overlap in *when*, merge them — overlapping triggers make the choice a coin-flip.

## Ground facts; put boundaries in the task

- Facts (rates, policy, catalogue) belong in a **knowledge base**, which is retrieved every turn — not
  in the prompt, where they go stale and un-cited. See [Build a knowledge base](/cookbook/build-a-knowledge-base).
- Constraints belong in **`task`**, as negatives: "never promise a date", "for a quote, call a tool".
  Negative boundaries stop drift better than positive description. Don't put safety rules in `soul` —
  the platform appends global moderation for you.
- Turn on `grounding_required` when answers must come from the material, not the model's priors.

## Never hand determinism to probability

The single most useful design rule on this platform: **if something can be computed, generated, or
verified by the system, never leave it to the model.** A model asked to produce a deterministic
artifact doesn't fail loudly — it produces a plausible one. The user gets a ticket number that
doesn't exist, a callback booked seven hours off, a colour palette that fails contrast. Nothing
errors; it's just quietly wrong.

Every one of these started as a real production failure and became a platform feature:

| Deterministic thing | Wrong way (probability) | Right way (system) |
|---|---|---|
| Reference / ticket numbers | Instructions say "tell the user the ticket number" → model invents one | `save_contact` / `schedule_followup` **return a real stored code** — instruct the model to relay it verbatim |
| Absolute times | Model hand-computes `delay_seconds` for "tomorrow 10am" → off by hours | Pass **`run_at`** (local ISO time); the server resolves the timezone |
| Text colours on a brand colour | Model picks "matching" colours → unreadable in one theme | Send `theme_color` only; WCAG-contrast foregrounds are **derived server-side** |
| Routing in a flow | An `ai` exit for "if the user agreed" | `rule` / `user_choice` exits; reserve `ai` exits for genuine judgment. Loops get an explicit counter and cap — never "the LLM will stop eventually" |
| "Did the trigger fire?" | Assume the prompt works | `test_skill_trigger` measures it; the platform also injects a deterministic hint when a phone/email is detected |
| The wording that reaches a tool | Hope the model turns "any others like that?" into the right call | The platform works out what was asked, then **composes the instruction from the tool's own definition** and shows that turn one tool. Measured 80% → 97%; letting the *model* rewrite its own request did nothing (82%) |
| A phrase that must never appear | Add another "do not say X" line to the prompt | **Delete it after the fact.** A rule you can check on the finished answer is a rule you can enforce; a rule in the prompt is a request |
| Machine-readable output | "Reply with valid JSON only" and parse strictly | Ask for the shape, then **parse for the one field that matters**. Strictness throws away answers that were right |

The corollary for writing skills: your `instructions` should tell the model **which system facility
to use** ("pass run_at, relay the returned code"), not teach it to imitate the facility ("compute
the seconds, format a ticket number"). If you find yourself scripting the *output* of a
deterministic process, look for the tool that produces it — or ask for one.

### Two corollaries about output

**A prompt rule is a request; a post-check is a rule.** "Never say X" belongs in the prompt — it
lowers the rate — but it is not enforcement. A model that agrees with the instruction can still
reach the same forbidden idea by a phrasing your wording didn't anticipate, and each rewrite of the
rule tends to catch only the phrasings you already saw. Wording cannot police wording. So ask a
different question: **is the unwanted sentence recognisable in the finished answer?** If it is,
remove it there, and keep the prompt line as well.

**Get the content right first; do not let syntax cost you the content.** A smaller model will
often make the correct choice and then write it in a shape your parser rejects — one object per
line instead of an array, a trailing comma, prose wrapped around the block. Parsing strictly means
a correct answer is discarded for a misplaced brace, and the symptom looks like a model that isn't
capable enough. Decide which field in the response is **load-bearing** — usually exactly one: an
id, a reference, a choice — and extract that field however it arrives. The rest of the payload is
typically data you were going to replace with your own anyway, so strictness about it protects
nothing.

## Show the agent good patterns only

When you hand an agent examples, make them **correct** examples. Don't paste a "here's the wrong way"
snippet next to the right one — the model may imitate the nearest example rather than read the caveat.
Describe what to avoid in words; keep runnable examples exemplary.

## Verify — writing is not working

After every change, check it did what you intended. Creating an agent doesn't mean it's configured the
way you think; adding to a knowledge base doesn't mean the question retrieves.

```text
get_agent(name="Support")                                   # confirm the config that landed
search_knowledge_base(kb_name="Company policy", query="…")  # confirm the answer is retrievable
```

An empty `search` result means that question will be answered as "not covered" — find that now, not from
a customer.

## Hand back a deliverable — and the next step

After every action, don't just report that you finished. Hand back **four things**: what you produced, a
clickable console link to view it, one line on how to use it, and **the natural next step — proposed, and
offered to do.** They will ask "where do I see it?", "how do I use it?" and "what now?" anyway; answer all
three up front. URL-encode names that contain spaces.

| After you… | Hand back |
|---|---|
| Create or import into a **knowledge base** | Its page — which includes the **knowledge starmap** (a 3D view of what was ingested): `https://console.agent4.io/#/knowledge-bases/<name>` |
| Create an **agent** | Its page to review/test: `https://console.agent4.io/#/agents/<name>` — and note that to let end users reach it, they create a **share link** in the console |
| Create a **skill** | `https://console.agent4.io/#/skills/<name>` |
| Publish a **Storyline** | `https://console.agent4.io/#/storylines/<id>` (the id from `create_storyline`) |
| Register an **MCP server** | `https://console.agent4.io/#/mcp/<id>` |

For example, after importing documents into a knowledge base, reply with how many chunks landed, the link
above so they can open its **knowledge starmap** and see exactly what was ingested, and confirm whether
it's now attached to an agent (or how to attach it). A bare "done" just makes them ask.

**Always end on the next step, and offer to do it** — a setup is a chain, not a single action:

- Built a **knowledge base**? → offer to attach it to an agent (ask which).
- Created an **agent**? → offer to attach a knowledge base, add a skill, or create a **share link** so
  end users can reach it (an empty space = off).
- Authored a **skill**? → offer to attach it to the agent that needs it.
- Published a **Storyline**? → offer to set it as the agent's default, or wire its enrollment trigger.
- Registered an **MCP server**? → offer to grant an agent its tools.

"Here's what I made, here's the link, here's how to use it, and here's what I'd do next — want me to?"
keeps the build moving; a bare "done" leaves the tenant guessing.

---
name: agent4-io-recipes
description: Connect to agent4.io over MCP, install the skills, and run end-to-end recipes.
version: 8
---

Connect to agent4.io over MCP, install the skills, and run end-to-end recipes.

## Get started with the agent4.io agent skills

agent4.io ships a remote **MCP server** (the tools) plus a set of **skills** (how to use the tools).
Point your agent at the MCP endpoint, install the skills once, and every recipe below becomes an
executable, step-by-step procedure.

## What this skill does with your data — tell the user

This skill connects to **agent4.io's remote API** (`api.agent4.io`). Be explicit with the user before you
send their material:

- **It transmits to agent4.io.** The agent configuration, knowledge-base content and queries you send go
  to agent4.io's servers to build and run agents there — that is the platform's purpose, not a side effect.
- **It uses exactly one credential — your agent4.io API key** (`tk_…`), which the user provides. It does
  **not** read other environment variables, and it does **not** read or enumerate your local files:
  `add_knowledge_file` deliberately cannot access your machine's paths; you only ever send content you
  explicitly pass to a knowledge-base tool.
- **Nothing runs with elevated privileges.** The installer only writes skill files into your agent's own
  skills folder — no `sudo`, and it fetches only from agent4.io.
- **On a chat channel**, a bot token the user provides is used **solely** to call that channel's own API at
  the user's instruction (e.g. Telegram `setMyCommands`) — never sent to agent4.io.

If any of this isn't acceptable to the user, stop — don't send their data.

## Connect — one step

You already have this skill (installed via ClawHub). The only thing left is the remote MCP server:

```bash
claude mcp add --transport http agent4-io https://api.agent4.io/v1/mcp --header "X-API-Key: $AGENT4_API_KEY"
```

Or add it to any MCP client's config — URL `https://api.agent4.io/v1/mcp`, header
`X-API-Key`, transport streamable-http. No installer, no shell script: one HTTP endpoint.
Get a key from **console → Settings → Security** (the plaintext is shown once, at creation).

## Verify

```text
tenant_info()   # → confirms you are connected to the right tenant
```

## Keep it current

```bash
clawhub update agent4-io
```

The MCP tools are remote, so they are always current; only this skill document is versioned.

## Slash commands (for your coding CLI — not for the deployed bot)

These are **builder shortcuts for coding CLIs that read a `commands/` folder** — Claude Code
(`~/.claude/commands/`) and Cursor (`.cursor/commands/`). The installer drops them so *you*, building on
agent4.io, can type them in your CLI:

- `/agent4-agent <what>` — create a grounded agent
- `/agent4-kb <name + source>` — build a knowledge base, import, verify, attach
- `/agent4-skill <when + what>` — author a load-on-demand skill
- `/agent4-storyline <process>` — compile a process into a Storyline and publish
- `/agent4-docs <question>` — look up an agent4.io concept or how-to

Each carries no logic of its own — it points at the matching `agent4-io-*` skill and passes what you type.

**They are not the deployed bot's commands.** They will not — and should not — show up in a Telegram or
WhatsApp bot's slash menu. Those menus are shown to your **end users** and are set separately by the bot's
operator (e.g. Telegram's `setMyCommands`); they list end-user actions, never builder operations like
"create an agent". Different audience, different mechanism — if you're deploying on a chat channel, ignore
these and configure that channel's own command menu.

**On OpenClaw / Codex** (no `commands/` folder) there are no separate command files: the agent uses the
`agent4-io` skill directly — the model invokes it, or you call the single `/agent4-io <task>` command — and
the five shortcuts above fold into that.

### Running on a Telegram / WhatsApp bot? Register the menu yourself

If **you (the agent) are deployed on a chat channel**, the channel's command menu is *not* synced from
skills — you set it through the channel's own API. Do this **only when this bot is your operator / builder
assistant** (the person using it builds on agent4.io); **skip it for a customer-facing bot**, whose menu is
for end users, not builder operations.

Telegram command names may contain only `a-z 0-9 _` — **no hyphens** — so rename `agent4-agent` →
`agent4_agent`. When you have the bot token, register them once with `setMyCommands`:

```bash
curl -s "https://api.telegram.org/bot$BOT_TOKEN/setMyCommands" -H "Content-Type: application/json" -d '{
  "commands":[
    {"command":"agent4_agent","description":"Create a grounded agent"},
    {"command":"agent4_kb","description":"Build a knowledge base"},
    {"command":"agent4_skill","description":"Author a load-on-demand skill"},
    {"command":"agent4_storyline","description":"Compile a process into a Storyline"},
    {"command":"agent4_docs","description":"Look up an agent4.io doc"}
  ]}'
```

When a user taps one, the channel sends that text to you as an ordinary message — handle it with this
skill (`agent4_agent` = the `/agent4-agent` shortcut, and so on). No bot token / shell access? Set the
same list by hand in **@BotFather → `/setcommands`**. WhatsApp has no slash menu; expose the same actions
as an interactive list/quick-reply instead.

**Silence your own link previews.** You cite `agent4.io` links constantly, so Telegram will attach a
preview card to nearly every reply — noisy fast. Send **your** messages with previews off:
`link_preview_options: {"is_disabled": true}` on `sendMessage` (legacy API: `disable_web_page_preview: true`).
This affects only your messages; a link the **user** sends still previews as normal.

## When there's no MCP tool for it — the REST API is the full surface

The MCP tools cover the common build-and-run operations, but they are not the whole platform. For
anything they don't expose — a field, an endpoint, a bulk job — the **complete tenant REST API** covers
everything a tenant can do. Call it directly with the same key: `X-API-Key: tk_...`.

Two ways to reach it, cheapest first:

- **`search_agent4_docs("… rest api …")`** — the docs search now indexes the REST API per endpoint. A
  REST/HTTP-worded query returns the **exact endpoint** with its parameters and response, without loading
  the whole reference. Use this first.
- **[https://agent4.io/api.md](https://agent4.io/api.md)** — the full machine-readable reference (every
  endpoint, params, request/response, examples). Read the whole file only when you need the broad picture.

MCP is the fast path; the REST API is the fallback.

## What to do next

- [Create a grounded support agent](/cookbook/create-support-agent)
- [Build and populate a knowledge base](/cookbook/build-a-knowledge-base)
- [Author a load-on-demand skill](/cookbook/create-a-skill)
- [Configure a page-aware chat opener](/cookbook/configure-page-playbooks)
- [Compile a flow into a Storyline](/cookbook/build-a-storyline)

Every recipe names the exact MCP tool and arguments — never "open this page and click".

---
name: agent4-io-admin
description: Create and configure agents (soul/task/tools/skills), load-on-demand skills, page playbooks (how the chat opens per page); check usage/quota and look up end users and their sessions.
version: 9
---

Create and configure agents (soul/task/tools/skills), load-on-demand skills, page playbooks (how the chat opens per page); check usage/quota and look up end users and their sessions.

## Create a grounded support agent

> **Before you build — discover, don't run this cold.** Interview the tenant about their job, their
> material, the procedures it runs and the systems it must touch; plan the whole setup (agent + knowledge
> base + skills + MCP as needed) and play it back before creating anything. The steps below are what you
> run *after* that — see [Discover before you build](/cookbook/design-principles).

> **Principle — one agent, one job.** Give this agent a single, clearly bounded task. If the business
> has three jobs (support *and* sales *and* scheduling), build three agents — a "does everything" agent
> answers each thing worse. More in [Design principles](/cookbook/design-principles).

An agent is **soul + task + tools + skills + knowledge_bases**. `soul` is identity and voice; `task` is
the job and its boundaries — both go into the fixed prefix of the system prompt.

## 1. See what you can attach

```text
list_tools()             # tools available to this tenant (including connected MCP tools)
list_knowledge_bases()   # knowledge bases you can mount
```

## 2. Create it

> **On by default, so you don't have to ask for them.** A new agent can already reply with a
> tappable single/multi-choice **form** (`ask_forms`) when it needs two or three facts before it can
> answer, and can already draw a **chart** (`compute_chart` is in the default tool list). Both were
> off by default until 2026-08-03, and the create call had no parameter for the first — so agents
> built before then have neither, and `update_agent(ask_forms=True, add_tools=["compute_chart"])`
> is how you bring one up to date.
>
> Passing `tools=[...]` **replaces** the default list rather than adding to it, so include
> `compute_chart` yourself whenever you pass tools at all.

> **Names are lower-case.** The name is not only what you see — eleven tables reference an agent by
> it (shares, sessions, storylines, channel bindings, usage), so `Pip` and `pip` are two different
> agents to all of them and the same one to you. New names are lower-cased on save; write them that
> way and there is nothing to reconcile. It is also not the public URL — that is `alias`.

```text
create_agent(
  name="support",                  # lower-case; the platform lower-cases it anyway
  alias="support",                 # public human-readable URL slug — set one (url-safe, lowercase)
  soul="You are the support assistant for Acme Loans. Professional and warm.",
  task="Answer questions about mortgage products and the application process. "
       "Never promise a disbursement date; never give legal or tax advice; "
       "for any specific quote, call a tool — do not answer from memory.",
  tools=["web_search"],
  knowledge_bases=["company-policy"],   # use the KB's returned slug name (see below)
  published=True,
)
```

- **`alias`** is the agent's public human-readable address segment (`{public_base}/t/<tenant>/<alias>`) —
  set it so you can hand people a memorable link. It's normalised to a url-safe slug; a clash comes back
  in `alias_result`.
- **System tools are on by default.** New agents automatically get `current_time`, `ip_geo` and `weather`
  (the built-in `system` MCP) — you don't list them; `tools` is for the *extra* ones.
- **Names in URLs are slugged.** A **knowledge base** name becomes a url-safe slug on creation
  (`"Company Policy"` → `company-policy`); attach it by the **returned** name, not what you typed.

## 3. Confirm what landed

```text
get_agent(name="Support")   # writing it doesn't mean it looks the way you intended
```

<Callout>
`published=True` means **visible**, not **reachable**. End users can't get to the agent until you create
a **share** (step 4). Don't stop at "published".
</Callout>

Boundaries belong in `task` — negative constraints ("never promise…") stop drift better than positive
description. Don't put safety rules in `soul`; the platform appends global moderation automatically. To
change one field later, use `update_agent(name, field=…)` — it merges, so it won't blank the rest.

## 4. Publish it — ask how, then make it reachable

Before you say "done", ask the tenant **how their customers should reach it**, then wire that channel with
`create_share` (it returns a real, openable link — hand that back, not "it's published"):

```text
create_share(agent_name="Support", label="Website widget")
# → { token, chat_url, qr_url, embed_snippet, pretty_url, … }
```

If the response carries `pretty_url` (`…/t/<tenant-alias>/<agent-alias>`), **that's the link for
humans** — readable and stable across token rotation. If it's null, set the missing alias
(`create_agent(alias=…)` / `PUT /agents/{name}/alias`; tenant alias in console → Settings) rather
than shipping the token link. `chat_url` remains right for embeds and QR codes.

- **No website — just a link or a QR** (a freelancer, a shop, a flyer, a business card): hand back
  `chat_url` (a full-screen **hosted chat page** — no site needed) and `qr_url` (a QR they can print).
  It's anonymous: no login, and each visitor is remembered by their browser, so regulars are recognised.
- **Their own website**: give them `embed_snippet` (one line before `</body>` for a floating widget), or
  `chat_url` to link / iframe.
- **Telegram / WhatsApp**: set up per-channel in the console (Agent → **Integration** →
  Telegram / WhatsApp); point them there.

> **Report back.** Hand back the **actual link they can open and test right now** (`chat_url`, and
> `qr_url` if they have no site), plus the agent's console page to review it —
> `https://console.agent4.io/#/agents/Support`. Not "it's published" — the link.

## Author a load-on-demand skill

> **Principle — keep the skill count small.** Attach only what this agent's job needs (≈5 or fewer).
> The model picks skills from their one-line `description`; the more you attach, the more often it loads
> the wrong one or none. If two skills overlap in *when*, merge them. More in
> [Design principles](/cookbook/design-principles).

A **skill** is a capability pack loaded on demand: the system prompt carries only its `description`
("when to use"); the model pulls the full `instructions` only when it judges the skill relevant. So the
`description` must be short and say *when*, or the model won't know to reach for it.

```text
list_skills()                                # what already exists

create_skill(
  name="refund-policy",
  description="Use when the user asks about refunds, cancellations or chargebacks.",
  instructions="The full procedure: eligibility windows, how to word the outcome, when to escalate …",
)

update_agent(name="Support", add_skills=["refund-policy"])   # attach it (incremental — keeps existing skills)
```

Keep procedures in `instructions` (fetched on load), not in the agent's `soul` (which is in the prompt
every turn). A one-line `description` that says *when* is what makes the skill discoverable — a vague one
means the model never pulls it.

## Tools can ride on the skill

A skill can carry its own tool bindings — `create_skill(tools=[…])` or
`update_skill(name, add_tools=[…])`. Tools bound to an attached skill **join the agent's toolset
automatically at chat time**, so a skill can ship as a self-contained capability: procedure + the
tools it needs, attached in one move.

Two things to know before you rely on it:

- **They don't appear in the agent's own `tools` list.** `get_agent` shows only the agent's directly
  attached tools; the console's Tools tab shows skill-bound ones as a separate read-only "via skills"
  line. When verifying "is tool X enabled", check both places — or just call the tool in a test chat.
- Prefer binding a tool to the **skill** when it only makes sense inside that procedure (a refund
  lookup inside the refund skill); bind to the **agent** when it's generally useful across turns
  (`save_contact`, `web_search`).

## Binding a tool is availability, not policy — the instructions must say when to call it

Checking a tool on a skill (or agent) only makes it *callable*. The model sees the tool's schema and
its one-line description every turn, so it may use it opportunistically — a visitor volunteers an
email and `save_contact` fires. But **any behaviour that must happen reliably needs to be written
down**, and each part of it has one right home:

| What you're specifying | Where it goes |
|---|---|
| *When to load this skill* | the skill's `description` (in the prompt every turn) |
| *The procedure: at which step to call which tool, with what arguments* | the skill's `instructions` — **name the tool explicitly** ("after the caller confirms interest, call `save_contact` with email and phone; then call `schedule_followup` for 1 business day later") |
| *A behaviour that must drive the whole conversation* (always capture leads, never quote rates) | the agent's `soul` / `task` |

The failure mode when instructions don't name the tool: everything *looks* configured — the tool is
checked, the skill loads — and the agent still never calls it, or calls it with guessed arguments.
Nothing errors. Write the procedure as if briefing a new employee: the step, the tool name, the
arguments, and what "done" looks like.

## Mandatory tool calls: the trigger must live in `description`, not only in `instructions`

`instructions` are visible to the model **only after it calls `load_skill`** — and models frequently
answer directly without loading the skill. So a rule like *"when the user provides a phone number,
you must call `save_contact`"* written only in `instructions` is invisible exactly when it matters:
the tool is silently never called, and the model may even claim it saved the contact. This happened
in production — an agent answered several contact-bearing messages in a row, "confirmed" the details
were recorded, and no record existed.

The fix is one sentence in the `description` (which *is* in the system prompt every turn):

```text
update_skill(
  name="consultative-sales",
  description="Consultative sales: understand the case, recommend products, arrange expert callbacks. "
              "When the user provides a phone number or email, call save_contact BEFORE answering anything else.",
)
```

Keep the detailed procedure in `instructions`; put the *trigger* of any mandatory call in
`description`.

Two related rules:

- **Never script return values the tool doesn't produce — relay real ones verbatim.** Built-in
  `save_contact` and `schedule_followup` return a **real reference code** on success (format
  `AB2C-D3EF`, stored server-side and visible to the tenant on the end user's detail page).
  Instruct the model to relay *the code from the tool result* verbatim — never to invent one or
  reformat it as "#12345". For any other tool, verify it actually returns an ID before scripting
  one: a promised-but-absent ID will be fabricated.
- **`create_skill` / `update_skill` / `get_skill` now return a `warnings` list** that flags exactly
  these two patterns (`trigger_hidden_in_instructions`, `promised_tool_return_id`). Warnings are
  advisory — the save succeeds — but treat them like a linter: fix, don't ignore.

## Worked examples in `instructions` measurably raise tool-call compliance

We benchmarked this on production backends (6 lead-capture messages of increasing difficulty —
numbers buried in long questions, digit groups with spaces, corrections — sampled per condition).
With the skill loaded, a plain "you must call X" mandate hit **3–4/6**; adding a short block of
worked examples brought both tested models to **6/6**. Moving the mandate section around did
nothing — *position doesn't matter, examples do*.

An effective example block has four kinds of entries, each one line:

```text
### Worked examples (follow exactly)

1. User: "I'd like to know about X, my phone is 13800138000"
   → call save_contact(phone="13800138000") first, then answer about X.
2. User: "email me the offer: li@example.com"
   → call save_contact(email="li@example.com").
3. COUNTER-EXAMPLE (forbidden): user gives a phone number and you reply
   "I've noted it down" WITHOUT calling the tool — claiming success without
   the call is the worst failure.
4. User: "sorry, wrong number — it's 13633334444"
   → call save_contact again with the corrected value.
5. Numbers may contain spaces ("138 0013 9000") — still a phone number;
   strip the spaces and call save_contact(phone="13800139000").
```

The counter-example (3) and the format edge case (5) close most of the remaining misses — models
fail on *recognition* ("is this a phone number?") and on *honesty under pressure* (answering a rich
domain question first and claiming the save happened) more than on willingness. Keep it to ~5
entries; use the exact call syntax with realistic arguments.

## Test the trigger before shipping — don't count corpses in production

Whether a skill *actually* fires is measurable, so measure it. `test_skill_trigger` dry-runs your
messages against the **production** prompt assembly, tool schemas and model routing, and reports
what the model decided — tools are never executed, nothing is stored, tokens count toward your
quota (caps: 5 messages × 5 samples).

```text
test_skill_trigger(
  agent="advisor",
  messages=[
    "My phone is 555 0123, call me back",          # easy
    "long question about the product … oh and my number is 555 0123",  # buried
    "555 0123 — that's me",                        # implicit
    "sorry, wrong number, it's 555 9999",          # correction
  ],
  expect_tool="save_contact",
  samples=3,
  loaded=true,        # simulate post-load_skill → tests instructions quality
)                     # loaded=false (default) → first turn, tests the description trigger
```

Read the result like this:

- **`hit_rate`** below ~90% on realistic messages → strengthen the trigger (description) or add
  worked examples (instructions), then re-test.
- **`claimed_without_call` > 0** is the worst failure — the model told the user "noted!" without
  calling the tool. Add the counter-example from the block above.
- Test **both modes**: `loaded=false` proves the description alone triggers on turn one;
  `loaded=true` proves the loaded instructions don't dilute it (long instructions measurably do —
  that's what the worked examples compensate for).

The result also carries an **`advice` list**: when samples miss or lie, it tells you exactly which
fix to apply (trigger into the description, add the worked-example block, add a counter-example or
format edge case) with the benchmark numbers behind each recommendation — apply it and re-test.

The full loop: `create_skill` → fix any `warnings` (static lint) → `test_skill_trigger` (dynamic
reality check) → apply its `advice` → re-test until the hit rate holds.

## Configure a page playbook (page-aware chat opener)

> **Principle — the opener is the only sentence guaranteed to be read.** A generic "How can I help?"
> converts a page visit into nothing. A playbook lets the *same* agent open differently on each page,
> already knowing where the visitor is. More in [Page playbooks](/concepts/playbooks).

A **page playbook** is a small briefing attached to a URL pattern. It has three parts:

- **`context`** — private background for the agent, **not shown** to the visitor (who lands on this
  page, what they're deciding, what they usually worry about). Write background, not facts: prices,
  quotas and policy belong in a [knowledge base](/cookbook/build-a-knowledge-base), which outranks it.
- **`greeting`** — the opening line the visitor actually sees.
- **`questions`** — up to four suggested questions, so a visitor who hasn't formed one can just pick.

The right playbook is chosen from the URL: resolution order is **explicit key → `url_pattern` →
default**. A single default catches every unmatched page, so nothing ever falls back to a blank box.

## 1. See what's already there

```text
list_page_contexts()   # existing playbooks: match rules, greeting mode, position, which is default
```

## 2. Create or replace one

```text
upsert_page_context(
  key="pricing",
  label="Pricing page",
  url_pattern="*/pricing",           # glob, path-only; ignores query string and trailing slash
  context="Visitors here are comparing plans and worrying about overage. "
          "They are usually the person who will sign off on the cost. "
          "Do not quote custom pricing in chat.",
  greeting="You're looking at our plans — want me to work out where overage would start for your volume?",
  questions=["What's included in the free plan?", "How is overage billed?", "Can I change plans later?"],
  greeting_mode="generated",         # generate opener + questions in the visitor's language (recommended)
  is_default=False,
)
```

`greeting_mode="generated"` writes the opener and questions per visitor language on the fly — so a
Spanish visitor gets a Spanish greeting without you authoring five versions. Use `"static"` only when
you want your exact `greeting`/`questions` verbatim.

## 3. Verify the match — always

```text
resolve_page_context(url="https://acme.com/pricing?ref=x")   # → which playbook this URL hits, and how
```

Globs are easy to get subtly wrong (a missing `*`, one path level too many). A mismatch has **no error
message** — the visitor just silently gets the default playbook. So after writing any `url_pattern`,
resolve a real URL and confirm `matched_by` is `url_pattern`, not `default`.

## 4. Set a catch-all default

```text
upsert_page_context(
  key="default",
  label="Everywhere else",
  context="General visitor to the site; intent unknown. Ask what brought them in before assuming.",
  greeting_mode="generated",
  is_default=True,                    # at most one default per tenant; setting this unsets any other
)
```

<Callout>
`upsert_page_context` is a **full replace**, not a patch: fields you omit fall back to defaults rather
than keeping their old value. To change one field, `list_page_contexts()` first, merge, then upsert.
</Callout>

Once playbooks have been live for a while, `page_context_stats()` shows which ones get opened and which
suggested questions get clicked — so you tune copy from data, not guesses.

> **Report back.** Give the user the console link to review and edit these —
> `https://console.agent4.io/#/page-contexts` — and confirm each `url_pattern` resolves the way they
> expect (step 3). The chat widget needs no code change for a static site; single-page apps that have
> no distinct URL per view can name a playbook by its `key` instead.

## Openings that collect on the spot

If a playbook's `context` explicitly instructs presenting a form at first contact — e.g.
`"PRESENT THE BOOKING FORM IN YOUR GREETING/OPENING: (1) preferred channel (phone / email — single),
(2) phone or email (text)"` — the generated opening will include that interactive form, and the
starter questions are suppressed (the form is the guidance). Submitting counts as a normal visitor
message, so `save_contact` / `schedule_followup` fire as they would mid-conversation.

Use it for intents where asking first is the whole point — "book a callback", "leave a message" —
and keep it to 2–3 fields. For intents where the visitor wants answers first (support,
troubleshooting), let the conversation start normally and collect in the first reply instead.

## Records require a contact — by design

Every record-creating tool (`submit_lead`, `escalate`, `request_booking`, `open_checklist`)
**rejects the call unless `contact.email` or `contact.phone` is filled in** — a record nobody can
follow up on is noise, not a lead. The rejection message tells the agent what to do (ask for a
contact first, never invent one), so make your playbooks collect email/phone up front — the
greeting-time forms above exist precisely for this.

## File form submissions deterministically

For intake-style playbooks (bookings, leads, complaints), append a machine marker to the
`context`: `[[inbox:submit_lead]]`, `[[inbox:escalate]]` or `[[inbox:request_booking]]`. Form
submissions on that playbook are then **filed by the platform before the model replies** — the
reply's reference is guaranteed to be the filed record's reference, and the contact is saved
alongside. Keep the prose instructions too: they cover the free-conversation path (details given
without the form), where the model still does the filing.

## Deleting things — point the user to the console

Deletions are deliberately **not** exposed as tools — they are irreversible, and from a conversation you
usually can't tell whether an agent or knowledge base is still used by something else. So when the user
asks you to delete something, **don't attempt it** — tell them exactly where to do it in the console at
[console.agent4.io](https://console.agent4.io), and offer to help with the safe parts (finding the item,
listing what depends on it) first.

| To delete… | Where in the console |
|---|---|
| An agent | Agents → open the agent → top-right **⋯ / Delete** |
| A knowledge base (and all its documents) | Knowledge → open the base → **Delete** |
| One document in a knowledge base | Knowledge → the base → **Documents** tab → the row → **Delete** |
| A skill | Skills → the skill → **Delete** (agents referencing it stop loading its guidance) |
| A user, space, or session | Users → the row → **Delete** |
| Revoke / re-issue an API key | Settings → **Security** → **Revoke** (then create a new one) |
| Change privacy mode / BYOK | Settings (this shifts compliance responsibility — confirm before changing) |

Before you send them off, it helps to **surface what would be affected**: e.g. list the agents that
mount a knowledge base (`list_agents` + `get_agent`) so they can see whether deleting it breaks anything.
That check is exactly why deletion is a human action in the console, not a tool call.

## Connect your own MCP server

Bring your own tools: register a **remote** MCP server and its tools become available to attach to your
agents. There is no "create MCP server" tool on purpose — registering a server means trusting it to run
against your tenant, so it is a deliberate action in the console (or a REST call), not something an agent
does on its own.

## 1. Register the server

In the console: **Tools / MCP → Add MCP server** — give it a name, choose the transport
(**Streamable HTTP** or **SSE**), and the URL plus any auth headers.

Or by REST, with your tenant key (`$BASE` = `https://api.agent4.io/v1`):

```bash
curl -X POST $BASE/mcp-servers -H "X-API-Key: $KEY" -H 'Content-Type: application/json' \
  -d '{"name":"my-tools","transport":"streamable_http",
       "config":{"url":"https://tools.example.com/mcp","headers":{"Authorization":"Bearer …"}}}'
```

Only **remote** transports are accepted. `stdio` (local commands) is rejected — the server runs on the
platform, not your machine, so a local command would be both useless to you and a code-execution risk.

## 2. See its tools

```text
list_mcp_servers()   # the MCP servers registered on your tenant
list_tools()         # every tool you can attach to an agent, including the ones from your servers
```

## 3. Attach the tools to an agent

```text
update_agent(name="Support", add_tools=["…"])   # incremental; use tool names exactly as list_tools() reports them
```

The agent can now call those tools during a conversation. Keep the set focused — a handful of relevant
tools beats a big pile (see [Design principles](/cookbook/design-principles)).

## Built-in tools (and the system MCP)

You don't have to build the common tools — the platform ships them. Attach the ones this agent's job
needs with `update_agent(name, add_tools=[…])`; keep the set small (see [Design principles](/cookbook/design-principles)).
Always confirm the exact names on your tenant with `list_tools()` — that is the source of truth.

> **`tools=[…]` replaces the whole list; `add_tools` / `remove_tools` change one item.** Passing
> `tools=` with only the tools you're thinking about silently drops every tool you didn't read first —
> this has happened in production and nobody noticed until a feature stopped working. Reach for
> `tools=` only when you deliberately mean "exactly this set", and read the returned agent to confirm
> the final list either way. The same pairs exist for skills (`add_skills`/`remove_skills`) and
> knowledge bases (`add_knowledge_bases`/`remove_knowledge_bases`).

## The built-in tools

| Tool | What it does |
|---|---|
| `web_search` | Look something up on the open web. |
| `save_contact` | Capture the end user's contact details into their profile — the platform's lead-capture / records path. Returns a **real reference code** (`AB2C-D3EF` style) the agent relays to the user; look codes up on the user's detail page (`recent_refs`). |
| `export_document` | Generate a structured document (a branded summary / report) for the conversation. |
| `schedule_followup` | Proactively follow up later ("check back in 2 days") or book a user-requested callback — the message is sent for you. Returns a **real booking reference** traceable to the scheduled task. For absolute times ("tomorrow 10am") instruct the model to pass **`run_at`** (local ISO datetime + optional `tz`) — the server resolves the user's timezone; hand-computed `delay_seconds` is for relative times only, and models get the arithmetic wrong. Window: up to 7 days. |
| `schedule_reminder` | Set a reminder for the end user; `list_reminders` / `cancel_reminder` manage them. |
| `compute_chart` | Work out a derived series **in code** — share of total, growth %, running total, a projection at a fixed rate, or a metered bill (base fee + allowance + per-unit overage). Attached automatically to any agent that already has tools, so you rarely add it by hand. See [Charts in answers](/cookbook/charts-in-answers). |

`load_skill` is also built in, but you don't attach it — the model pulls a skill on its own when a
skill's `description` matches.

```text
list_tools()                                              # exact names available on your tenant
update_agent(name="Support", add_tools=["save_contact", "schedule_followup"])   # incremental — keeps what's there
```

Capturing a contact with `save_contact` populates the user's record; combined with `ask_forms` on the
agent, structured intake lands as records you can review in the console.

**The platform backs these two up automatically.** When the end user's message contains a clear
signal — a phone number / email (any language, incl. spelled-out digits and spaced formats), or a
"call me tomorrow morning"-style callback request — and `save_contact` / `schedule_followup` is
enabled, the platform injects a per-turn hint reminding the model to call the tool before answering.
Benchmarked on production backends, this lifted lead-capture compliance on the weakest model from
~85% to 100% with **zero** false saves (the hint carries an "ignore if wrong" escape hatch, so an
over-eager detector cannot cause bad data). You get this for free — no configuration; your skill
should still state the trigger in its `description` (see [Author a skill](/cookbook/create-a-skill)),
the hint is a safety net, not a replacement.

## The system MCP — already installed

Every tenant gets a built-in **`system`** MCP server, enabled by default, with keyless tools for
**local time, weather, and IP geolocation** (city / region / timezone). You don't register it — it's
there. Its tools show up in `list_tools()` alongside the built-ins above, ready to attach.

So "what's the weather where the user is?" or "what's their local time?" work out of the box — the
platform injects the end user's client IP, so location-aware answers need no setup.

## Check usage and quota

Two read-only tools answer every "how much am I using?" question. Both return **metadata only** — token
counts and event counts — and **never any conversation content**.

## Where you stand against the quota

```text
tenant_info()                 # plan + monthly_token_quota (the ceiling)
usage_stats(group="total")    # tokens + events used so far this period
```

**Use case — "am I about to run out?"** Compare the total against `monthly_token_quota` from
`tenant_info`. Overage is billed in arrears, so surfacing "you're at 82% of this month's quota" lets the
user decide before it costs them.

## What's driving the cost

`usage_stats(group=…)` slices the same totals. Pick the group by the question you're answering:

```text
usage_stats(group="agent")    # which agent is busiest / burning the most tokens
usage_stats(group="user")     # which end user is heaviest — spot one runaway account
usage_stats(group="space")    # usage per customer space (multi-tenant fan-out)
usage_stats(group="day")      # trend over time — catch a spike the day it happens
usage_stats(group="model")    # cost mix across models — is an expensive model doing routine work?
```

**Use cases at a glance:**

- *"My bill jumped this month — why?"* → `group="day"` to find the spike, then `group="agent"` to see
  which agent it came from.
- *"Is one model doing work a cheaper one could?"* → `group="model"`, then consider
  `update_agent(name, model=…)` on the offenders.
- *"Which customer should I upsell / rate-limit?"* → `group="space"` or `group="user"`.

<Callout>
This is **metadata, not analytics on content**. It answers *how much* and *by whom/what*, never *what
was said*. Chat transcripts and end-user profiles are deliberately not reachable over MCP.
</Callout>

> **Report back.** Lead with the one number that matters — "You've used 4.2M of your 5M monthly tokens
> (84%)" — then the breakdown that explains it, and link the console for the full picture:
> `https://console.agent4.io/#/usage`.

## Look up users and their sessions

> **Principle — hand back a link, not a transcript.** These tools return *who* your users are and
> *how much* they chat — never the conversation text. Each result carries a `console_url`; give that to
> the user so they open and read the transcript in the console, where it renders properly.

Three read-only tools cover "who is using my agents, and how much":

## 1. The user directory

```text
list_end_users(sort="tokens24h")     # busiest first; sort="recent" for newest
list_end_users(q="alex")             # filter by name or external id
```

Each user comes back with sign-in method, email (if any), space/session/document counts, 24h token
usage, and a `console_url`. **Use case — "who's my heaviest user this week?"** → `sort="tokens24h"`,
then hand back the top user's `console_url`.

## 2. One user's detail

```text
get_end_user(uid="…")                # profile: name, contact email/phone, city, timezone, spaces
```

Profile fields only — no conversation content. Includes a `console_url` to their detail page.

## 3. Their sessions — metadata, then a link

```text
list_user_sessions(uid="…")          # per session: agent, AI-summarised title, message_count, tokens, time
```

**The messages themselves are not returned** — by design. You get the session's *shape* (which agent,
how long, when, an AI title) plus two links: `console_url` opens **that exact conversation** (the
console jumps straight to it and pops the transcript — no hunting through a long list), and
`user_console_url` opens the user's detail page. **Use case — "has this customer talked to us before,
and what about?"** → list their sessions, summarise the titles, and hand back the `console_url` of the
relevant one so they land right on that thread.

<Callout>
Why no transcript over MCP: chat content is your end users' data, and a tenant API key is held by
whatever agent you connected. So the platform returns **metadata + a console link**, and the raw
conversation is read by a human in the console — not streamed to an integrating agent.
</Callout>

> **Report back.** Lead with the answer ("Alex has 3 sessions, all about refinancing, most recent
> yesterday"), then paste the `console_url` of the relevant session so the user clicks straight into
> that exact thread — or `user_console_url` for the whole person.

## Brand the chat — colours and logo

> **Principle — give one colour, not a palette.** Foreground colours are derived from it on save,
> so every combination stays readable. Picking your own text colours is how you ship a button
> nobody can read.

Branding lives on the **share**, not the agent: the same agent can be a white-label widget on one
site and a plain link somewhere else. So get the token first.

```text
list_shares(agent_name="mortgage-advisor")
# → [{ token: "RuqY…", label: "Website widget", config: { theme_color: "#F7B331", … } }]

configure_share(
  agent_name="mortgage-advisor",
  token="RuqY…",
  theme_color="#F7B331",
  logo_url="https://cdn.example.com/brand/mark-512.png",
)
```

Only the fields you pass change — the rest of the configuration is left alone.

## Renaming a share

`label` is the name at the top of the chat page and the browser tab's title. It is a field on
`configure_share` like any other:

```text
configure_share(agent_name="mortgage-advisor", token="RuqY…", label="Pip — reading buddy")
```

**You never need to create a replacement share and delete the old one to rename it.** A new share
means a new token, so the link already embedded in the customer's site stops working — the visible
name and the address are not the same thing, and only one of them is safe to change after launch.

## A second colour, only if the brand has one

Most brands have one colour and need nothing here. Some have a primary and a highlight — pass the
second one as `highlight_color` and it is used where something must be visible without competing
with the primary action:

```text
configure_share(
  agent_name="pip",
  token="ENhs…",
  theme_color="#0B4230",      # primary: buttons, the current storyline step, user bubbles
  highlight_color="#D9A922",  # highlight: second chart series, citation markers
)
```

Its foregrounds are derived on save exactly like the primary's, so the same readability guarantee
holds. Leave it out and nothing changes anywhere — `--acc-2` falls back to the primary, which is
what every single-colour brand wants and requires no configuration.

**Don't spread it further by hand.** You *can* override our component classes from `custom_css`,
and you will regret it: those class names are our internals, they change, and when they do your
branding breaks silently. Set the two colours and let the components decide where each belongs.

## Colour: pass one, get four

`theme_color` is the brand's primary colour, `#RGB` or `#RRGGBB`. On save the platform derives the
foregrounds by WCAG contrast and stores them:

| Derived | Used for |
| --- | --- |
| `theme_color_fg` | text **on** the brand colour — send button, user bubbles, unread badge |
| `theme_color_text` | the brand colour used **as** text, on a light background |
| `theme_color_text_dark` | the same, on a dark background |

A light brand colour therefore gets **dark** text on it rather than white. `#F7B331` with white text
measures 1.83:1 — below even the 3:1 floor for UI components, meaning the label is genuinely
unreadable; the derived dark foreground measures 10.21:1.

**Do not compute a palette yourself and do not try to set the text colours** — they are
server-derived and your values are overwritten. Passing one colour is the whole job.

Clearing it (`theme_color=""`) drops the derived values too and returns the widget to the default
blue. Leaving it unset does the same — the built-in tokens are already a matched pair.

## Logo: aspect ratio decides where it can be used

Pass an absolute URL. The logo appears in two places with different constraints:

- **Header bar** — height-aligned, width free. Any aspect ratio works, including a wide wordmark.
- **Collapsed bubble** — square, because the logo *is* the shape of the bubble. Only ratios between
  **0.74 and 1.35** are used here; a wide wordmark falls back to the platform icon instead of being
  squeezed into a strip too small to read.

So for a wide wordmark, the practical answer is **two files**: the wordmark for the header, a square
mark for the bubble. If the customer only has a wordmark, the header still shows their brand and the
bubble shows a neutral icon — better than an illegible sliver.

Do not crop a wordmark to square. Cropping leaves half a word, which is no longer their trademark.

## When the brand guide overrides everything

Some customers have a strict palette that will not follow ours in either theme. `custom_css` is
injected after the brand variables, so a plain declaration already wins — **no `!important`
needed**. (It used to be required, because the colours were set as inline styles. They are not any
more.)

> ### ⚠️ Read this before writing any CSS
>
> **You must write two blocks: `:root` for light, `html[data-theme="dark"]` for dark.**
>
> `:root` matches in **both** themes and outranks the platform's dark rules (same specificity, and
> yours comes later). So a palette written only under `:root` means **the visitor's light/dark
> toggle changes nothing at all** — `data-theme` flips, no variable follows it.
>
> This has already happened in production: an agent put a full dark palette under `:root`, the page
> looked great, and the theme button became a dead control that nobody noticed for weeks. **The
> page looks correct, which is exactly why this goes unreported.**
>
> If the customer genuinely wants one theme only, set the share's `theme` field to `light` or
> `dark` instead. That **hides** the toggle rather than breaking it.

Correct shape — copy this and replace the values:

```css
/* LIGHT — the light values go here, not the dark ones */
:root{
  --acc: #6b21a8;        /* brand primary — backgrounds, focus rings */
  --acc-fg: #ffffff;     /* text on --acc: YOU own the contrast here */
  --acc-text-l: #581c87; /* brand colour used as text, light theme */
  --bg: #fdfbff;
  --surface: #ffffff;
  --text: #1e1b2e;
  --border: #e6e0f0;
}
/* DARK — required whenever you touched --bg / --surface / --text above */
html[data-theme="dark"]{
  --acc: #a855f7;
  --acc-fg: #1a0b2e;
  --acc-text-d: #c084fc; /* note: -d, the dark-theme variant */
  --bg: #120c1d;
  --surface: #1c142b;
  --text: #f0e9ff;
  --border: #32254a;
}
```

That is the full set worth overriding — the widget consumes few colours on purpose.

Which variables need the dark block? The ones that describe the **surface**, because they invert
between themes: `--bg`, `--surface`, `--text`, `--border`. `--acc` is the brand colour and normally
stays the same in both, though the example brightens it for the dark theme because a deep purple on
a near-black background is hard to see.

Two more things to hold on to:

- **`custom_css` carries no readability guarantee.** `theme_color` does. Reach for CSS only for what
  the derivation cannot express, and keep `theme_color` set as the baseline.
- **Setting `--acc-text-l` and `--acc-text-d` to the same value defeats their purpose.** They exist
  precisely so the brand colour can be readable as text against opposite backgrounds.

`configure_share` returns a `warnings` array when it detects the single-`:root` mistake — **read it**.
The console shows the same warning next to the CSS editor.

`css_url` loads an external stylesheet instead, for customers who keep their own theme file.

### The interactive controls your colours drive

Every accent-coloured control in the chat reads the same pair — background `--acc`, text `--acc-fg`:

| Control | Selector (stable) |
| --- | --- |
| **Ask-form submit button** (the forms agents render with ```ask blocks) | `.ca-form .casub` |
| Ask-form option rows | `.ca-form label` (hover: `:hover`) |
| Ask-form **selected** row | `.ca-form label:has(input:checked)` |
| Ask-form radio/checkbox itself | `.ca-form input` (via `accent-color`) |
| Send button / user bubbles / unread badge | `.composer .send`, `.m.user .content`, `.sbadge` |
| Icebreaker question buttons (hover) | `.qs button` |
| Hold-to-talk button while **recording** — background, label, and the pulsing **glow** | `.ca-talk.rec` |
| PWA install button | `.pwabar .go`, `.pwacard .go` |

Selected rows come styled out of the box — brand-coloured border, a 10% brand tint behind the row,
and the native control painted with `accent-color` — all driven by `--acc`, so setting `theme_color`
is again the whole job. The voice button's recording glow likewise derives from `--acc`
(via `color-mix` at 22%/55% alpha), so it pulses in the brand colour automatically; override it in
`custom_css` only for a deliberately different treatment:

```css
/* softer, wider recording glow — both themes if you also touch surfaces */
:root .ca-talk.rec{
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--acc) 15%, transparent),
              0 0 40px color-mix(in srgb, var(--acc) 40%, transparent);
}
```

Only reach for CSS when the brand guide demands a different treatment:

```css
/* stronger selected state, both themes (remember the two-block rule above) */
:root .ca-form label:has(input:checked){
  border-color: var(--acc);
  background: color-mix(in srgb, var(--acc) 18%, transparent);
  font-weight: 600;
}
html[data-theme="dark"] .ca-form label:has(input:checked){
  background: color-mix(in srgb, var(--acc) 24%, transparent);
}
```

The rule that keeps them all readable: **anything you paint with `--acc` gets its text from
`--acc-fg` — never a literal colour.** The classic failure is overriding `--acc` to a light brand
yellow in the dark block and leaving white text: the ask-form button becomes yellow-on-white-text at
1.8:1 and the customer reports "the form button is unreadable in dark mode". If you override `--acc`
in `custom_css`, you own `--acc-fg` in the **same block, both themes** — or better, don't use CSS
for this at all: set `theme_color` and the platform derives a compliant `--acc-fg` for you.

## Make the chat installable (PWA)

Standalone chat pages (`/s/…` links, QR codes, and the alias URLs below) are installable apps:
visitors can add them to their home screen, with your own icon and name. Two knobs, configured
**per agent** — what gets installed to a home screen is one agent's entry page, so each agent is
its own app with its own icon (a support agent and a pre-sales agent install as two different apps):

```text
set_pwa_branding(
  agent="support",                                                # which agent's install branding
  icon_source_url="https://cdn.example.com/brand/mark-1024.png",  # ONE square master image ≥192×192
  install_prompt="banner",                                        # banner (default) | card | off
)
```

- The master image is fetched once and the platform generates the whole set — browser-tab favicon,
  192/512 install icons and the Android maskable variant. Non-square masters are centre-cropped, so
  use the square **mark**, not a wide wordmark.
- `install_prompt` controls what visitors see on the chat page: `banner` is a slim dismissible bar
  (Android/Chrome triggers the system install dialog; iOS gets a "Share → Add to Home Screen"
  walkthrough since Apple offers no API), `card` is a more visible first-visit card, `off` disables
  the invitation. Dismissals are remembered per visitor.
- Icons are **optional** — without them the platform icons are used. Call with just the agent name
  to read that agent's current configuration.

## The link you hand a human

When the tenant alias **and** the agent alias are both set, `create_share` / `list_shares` return a
`pretty_url` — `https://chat.agent4.io/t/<tenant-alias>/<agent-alias>`. **That is the link to give
people and print on material**: readable, memorable, and it survives token rotation (the platform
lazily maintains a share behind it). The `/s/<token>` form stays for embeds and machines.

No `pretty_url` in the response? The aliases aren't set — fix that rather than shipping the token
link: agent alias via `create_agent(alias=…)` or `PUT /agents/{name}/alias`; the tenant alias lives
in console → Settings. Setting an agent's alias is itself a publish action: the alias page
auto-creates an anonymous share on first visit.

## The customer's own domain

The hosted chat page can serve on the customer's domain — `https://chat.client.com/` shows their
branded page, certificate issued automatically.

```text
set_custom_domain(domain="chat.client.com", agent_alias="menu")
# → { status: "pending", cname_target: "endpoint.agent4.io", last_error: "…" }
```

The sequence matters, and it is asynchronous:

1. Tell the customer to add a **CNAME** from their subdomain to the `cname_target` in the response
   (`endpoint.agent4.io`). Subdomains only — an apex domain (`client.com`) cannot take a CNAME;
   have them use `chat.client.com`, or a DNS provider with CNAME flattening.
2. **On Cloudflare the record must be DNS only (grey cloud).** Proxied records resolve to
   Cloudflare's IPs and verification fails — `last_error` says so explicitly, with the observed
   addresses. This is the most common failure; read `last_error` before guessing.
3. Verification re-runs automatically every 10 minutes; call `set_custom_domain` again (same
   arguments) or check `tenant_info()` to see the current status. `active` means live — the first
   visit issues the certificate.

One domain per workspace. `agent_alias` empty lands on the tenant's branded page; set it to land
directly on one agent's chat. Existing `chat.agent4.io` links keep working — this is an additional
entrance, not a replacement — and chat identity is per-domain: a visitor's history on
`chat.agent4.io` does not follow them to the custom domain.

Requires a plan that includes custom domains (403 = the tenant needs to upgrade).

## The conversation search modal (Spotlight)

The standalone page and the web client have a ⌘K conversation search. It follows the brand
automatically — the modal reads the same variables everything else does (`--surface`, `--border`,
`--text`, `--muted`, `--overlay`, `--surface-hover`, `--accent-soft`, and the `--acc-text` pair for
highlighted matches) — so **setting `theme_color` is already the whole job here too**.

For brand guides that need more, the class names are stable and `custom_css` outranks the
component's own styles:

| Part | Selector |
| --- | --- |
| Backdrop | `.ca-ss-mask` |
| The panel | `.ca-ss` |
| Query input | `.ca-ss input` |
| Result row / selected row | `.ca-ss-item` / `.ca-ss-item.sel` |
| Result title / snippet | `.ca-ss-t` / `.ca-ss-s` |
| Highlighted match in a snippet | `.ca-ss-s mark` |
| "related" badge (semantic hits) | `.ca-ss-sem` |
| Sidebar search button | `.sb-search` |

```css
/* rounder panel, brand-tinted selected row — remember the two-block rule above */
:root{ }
.ca-ss{ border-radius: 20px; }
.ca-ss-item.sel{ background: color-mix(in srgb, var(--acc) 10%, transparent); }
html[data-theme="dark"] .ca-ss-item.sel{ background: color-mix(in srgb, var(--acc) 16%, transparent); }
```

As everywhere: the two-theme rule applies the moment you touch surface colours, and plain
declarations win — no `!important`.

## Form controls and the native date picker

Ask-form inputs (`.ca-form input.cain`) and the dialog input (`.ca-in`) are token-styled — surface,
text, border, and an accent focus ring all follow the theme and your `theme_color`. The system
dialogs (rename/confirm) share the Spotlight treatment: frosted backdrop, breathing elevation,
brand glow in dark.

**The calendar is hybrid.** On desktop (mouse) the platform draws its own calendar — fully
token-styled, brand-coloured selected day, localized month/weekday names — stable selectors
`.ca-dp`, `.ca-dp-d`, `.ca-dp-d.sel`, `.ca-dp-d.today` if a brand guide needs more. On touch
devices the **native** OS picker is kept deliberately: the mobile wheel beats anything drawn in a
web page, and its panel is OS-private UI that CSS cannot reach — there the platform controls what
is reachable (theme-pinned `color-scheme`, the token-styled input field, the inverted calendar
icon) and nothing more exists to control.

**Scope your element selectors.** A bare `input[type="text"] { … }` written for the composer also
captures the platform's dialogs and form fields — a white composer style bleeding into a dark
rename dialog is the classic symptom, and the CSS lint now flags it (`broad_element_selector`).
Write `.composer textarea` or `#input` instead. The system dialogs sit at higher specificity, so
the accident no longer lands — but the lint tells you before you rely on an accident.

## Also on the share

- `input_mode` — `text` (default) or `voice`, which opens straight into hold-to-talk. Needs a
  speech-to-text backend enabled on the platform.
- `launcher` — the bubble's hover tooltip.
- `theme` — force `light` / `dark`, or leave empty to follow the visitor's system setting. Prefer
  empty: the widget sits inside the customer's page and should match it.

## Verify

Open the `chat_url` from `list_shares` and look at the send button. If the label is hard to read,
`theme_color` is not set and something is overriding it — check `custom_css` for a hard-coded
`color`.

## Charts in answers — what you get for free, and what you must not do

> **Principle — the agent may copy numbers, never compute them.** Copying out of retrieved text is
> reliable; arithmetic is not. Everything on this page follows from that one measurement. More in
> [Design principles](/cookbook/design-principles).

When an answer already contains a set of comparable numbers, the agent draws them — unprompted, in
the middle of an ordinary conversation. There is **nothing to enable**: any agent with a knowledge
base or tools does this. Charts render in the widget, the console, the test panel and the Inbox, and
degrade to a compact table on Telegram, WhatsApp and screen readers.

So the useful question is not "how do I turn charts on". It is **what makes the difference between a
chart that appears and one that gets thrown away.**

## Every figure must be in the material

Before a chart renders, a deterministic check runs over it: each label-and-value pair must appear in
the passages the agent actually retrieved *that turn*. A pair that cannot be found means **the whole
block is dropped** — the visitor keeps the words and loses the picture, and nothing in the reply says
why.

That check is why the practical work is in your knowledge base, not in any setting:

- **Short, specific documents win.** A long page about a product that never states its price will be
  retrieved for a pricing question and answer nothing. Give each thing its own short document that
  states its numbers.
- **Write numbers the way people ask about them.** `25M`, `25,000,000` and `2500万` are all matched,
  as are `$49`, `49 USD` and `49 美元`. Units are not checked, so keep them in the text next to the
  figure.
- **Verify with `search_knowledge_base` before you rely on it.** If the passage that comes back has
  no number in it, no chart is coming either.

## Derived numbers go through `compute_chart`

Shares, growth rates, running totals and bills are exactly what a model gets wrong, and exactly what
makes a chart worth looking at. So the agent does not calculate them: it hands the verbatim figures
to `compute_chart`, the platform computes the series **in code**, and the numbers are filled into the
chart without passing back through the model.

| `derive` | For | Give it |
|---|---|---|
| `share` | percent of total | `labels` + `series` |
| `growth` | percent change vs the previous period | `labels` + `series` |
| `cumulative` | running total | `labels` + `series` |
| `project` | "grows X% per period for N periods" | `base`, `rate_pct`, `periods` |
| `tier` | "at that usage, what does it cost" | `included`, `rate_per_unit`, `base_fee` — plus `base`/`rate_pct`/`periods` to project and bill in one call |

The tool is attached automatically to any agent that already has tools, so there is usually nothing
to add. Confirm with `list_tools()` on your tenant.

Two guards worth knowing, because they explain charts that "should have appeared":

- **The inputs are checked too.** A price handed to `tier` has to exist in the material *as money* —
  next to a currency mark. A model that invents a monthly fee produces an exactly-computed bill built
  on a figure nobody published, and the chart is dropped for it.
- **Units must agree.** `included`, `rate_per_unit` and the usage values are all in the same unit. Give
  usage in raw tokens and an allowance in millions and the call is refused rather than billed at a
  million times the rate.

## What you cannot style, and why

Chart colours are derived from your **theme colour** — the whole palette, both light and dark, the
hover state and the tooltip. One setting, every chart type.

Do not try to reach charts from `custom_css`: they are drawn on a canvas, and CSS cannot reach inside
one. A rule targeting a chart is not overridden, it simply does nothing, which is worse than being
refused. If a chart looks wrong for your brand, change the theme colour.

## When it stays quiet

Three numbers is the floor — "up from 120k to 150k" is a sentence, not a bar chart. Yes/no questions
and single-value lookups get an answer, not a picture. At most two charts per reply, and a second only
when the two measures are in different units.

And if nothing was retrieved that turn, there is nothing to draw. The agent says what it knows and
what it does not, which is what it does with words too.

---
name: agent4-io-knowledge
description: Build, populate, verify and query grounded knowledge bases.
version: 9
---

Build, populate, verify and query grounded knowledge bases.

## Build and populate a knowledge base

> **Principle — ground, then verify.** A knowledge base is a MUST-follow source, not a hint. Scope its
> coverage in `instructions`, and always confirm a real question retrieves *before* you rely on it — an
> empty search means the agent will answer "not covered". More in [Design principles](/cookbook/design-principles).

A mounted knowledge base is **auto-retrieved every turn** — the model does not decide whether to look;
relevance is by vector distance. That is deliberate: a KB is a MUST-follow source, not an optional tool.

## 1. Create it

```text
create_knowledge_base(
  name="Company policy",
  description="Mortgage policy and rates, effective 2026 — not car or personal loans",  # routes questions here
  instructions="Authoritative current mortgage policy; overrides any industry norm. "
               "Covers home mortgages only; for car or personal loans, say so and hand off.",  # for the model
)
```

The **name is normalised to a url-safe slug** on creation — `"Company policy"` comes back as
`company-policy`. Use that **returned** name for everything after: `add_knowledge_text(kb_name=…)`,
`search_knowledge_base(kb_name=…)`, and attaching it to an agent. Typing the original spaced name later
just 404s.

## 2. Write `description` — it is what routes questions to this base

`description` is not a caption. **Before each answer the platform reads every attached base's
description and decides which of them this question needs** — and, if none of them do, searches
nothing at all. An agent with three bases is otherwise doing three vector searches and pouring three
sets of excerpts into the prompt on every turn, including when the visitor said "hi".

So a base whose description is vague or blank gets searched when it should not, and — worse — missed
when it should have been. Neither failure announces itself: the first shows up as a slow answer with
irrelevant citations, the second as "I don't have anything on that".

Write one line, in the words a visitor would use, naming the subject:

```text
✅ "Country-by-country medical device registration requirements"
✅ "Regulatory change news by country and authority, 2022–2026 — what changed and when"
✅ "Selpercatinib — for lung and thyroid cancer"

❌ "Knowledge base"                ← routes nothing
❌ "Imported from the website"     ← says where it came from, not what is in it
❌ "Sandbox test, safe to delete"  ← says why it exists, not what is in it
```

**What matters is being distinguishable from your other bases, not being long.** A tenant with nine
bases — eight drugs and a company profile, one line each, none longer than a dozen words — routes 10
out of 10 questions correctly, because "for lung and thyroid cancer" and "for IgA nephropathy" can
never be confused. Measured, not assumed.

**Add a boundary only where two bases overlap.** If your product pages and your news archive both
talk about the same subject, say which one is which — "…— not pricing or company information" is
what stops the archive from answering a pricing question. Where the bases are already obviously
distinct, a boundary clause buys nothing.

This line is also what the console list shows, but that is the lesser job.

## 3. Write `instructions` from the expected usage — at creation, not "later"

`instructions` does **not** affect recall — recall is vector search plus `max_distance`. It is injected
next to this KB's excerpts at answer time, so it governs **how the model uses what it retrieved**. Left
blank, the KB still retrieves, but the answers lose every KB-specific rule: authority, boundaries,
quoting conventions. Blank is acceptable **only** for generic reference material with no special rules.

Derive it from how the KB will actually be used — one line per question:

| Question | Example line |
|---|---|
| **Scope** — what's in, what's out, what to do when out? | "Covers residential mortgages only; for car or personal loans, say so and hand off." |
| **Authority** — where does this rank? | "Current company policy; overrides industry norms and the model's prior knowledge." |
| **Usage rules** — any convention when quoting it? | "Any quoted rate must state its effective date." |

Knowledge base instructions examples, by KB type:

```text
# Website-content KB (products, services, team, blog)
instructions="Company website content: products, services, team and blog posts. Authoritative
for what we offer and who we are. Marketing copy is not a contractual promise — for prices,
terms or eligibility prefer the policy KB; if only this KB answers, attribute it to the website."

# Policy / regulation KB
instructions="Current company policy, effective 2026; overrides industry norms and prior
knowledge. Covers home mortgages only — for car or personal loans, say so and hand off.
Any quoted rate or fee must state its effective date."

# Product-docs KB
instructions="Official product documentation for the current release. State the version when a
feature is version-dependent. If the docs don't cover something, say so — never fill the gap
from general knowledge."
```

## 4. Add content

```text
add_knowledge_text(kb_name="Company policy", title="2026 late-fee rule",
                   content="From 1 July 2026 the daily late fee is 0.019% …")
```

Binary files (pdf/docx) and whole folders (zipped) go through `add_knowledge_file` — subfolders are
walked and each md/txt/pdf/html/docx is imported under its in-archive path.

## 4b. Write the sentence you want to be found by

Retrieval matches **meaning**, and a value on its own carries almost none. This is the single highest-
leverage thing you control, and it is easy to get wrong because nothing errors — search still returns
something, just not the right thing.

A real customer catalogue had this line in **1,480 of 1,500** records:

```text
Reading level: 1 · Age: 5 · Words: 1951
```

And "which books suit a child just starting to read on their own" came back with a book about musical
prodigies. The fact was in the text and still unreachable: `1` bears no resemblance to *beginner
reader* the way one word resembles another.

Adding one sentence next to the value fixed it — measured on that same record:

```text
Reading level: 1 · Age: 5
Suitable for around age 5, for children just starting to read on their own.
```

| query | before | after |
|---|---|---|
| which books suit a child just starting to read on their own | 0.625 | **0.540** |
| 什么书适合刚开始自己读的孩子 | 0.626 | **0.552** |
| beginner reader age 5 | 0.598 | **0.498** |

(Lower is closer. On this model two *unrelated* passages sit around 0.61, so the last row moves from
"barely better than chance" to a genuine match — and the gain carries across languages.)

The rule: **if a question would be answered by a property rather than by the prose — price, date,
level, availability, stock — say it in words as well.** Structured values are for filtering;
retrieval finds what is written.

### What is *not* worth your time

Exports often repeat themselves — a `summary` and a `description` carrying identical prose. It looks
wasteful, and the intuition that it "uses up" the vector is wrong: we measured it and removing the
duplication changed retrieval by **+0.002 distance across 60 records — i.e. nothing at all**. An
embedding is a direction, not a budget; saying the same thing twice mostly points the same way twice.

Leave it. Spend the effort on the sentence above instead.

## 4c. If the documents share a header, build the structured index

Vector search cannot count, filter by number, or group. "How many do you have", "which are under
200 words", "how many per category" are not answered badly — they are **structurally unanswerable**,
and the agent will either decline or report on whichever few records it happened to retrieve.

```text
build_knowledge_index(name="books", roles=["identity", "link", "image"])
```

**Only worth calling when the documents share a machine-readable header** — a metadata table, YAML
front matter, `Field: value` lines. Product exports, catalogues, leaflets and course listings usually
qualify; prose does not, and the call declines rather than building a table whose values are all
different. A decline is the correct outcome, not an error to work around.

`roles` names the fields that must be extracted **exactly** and never paraphrased:

| role | what it is |
|---|---|
| `identity` | what to call the item — book title, drug name, product name |
| `link` | where to send the user |
| `image` | what to show the user |
| `code` | the identifier they will quote back at you |

**Ask the user which fields these are; do not infer them.** Which of three URLs is *the* one to send a
customer is a business fact the data does not state. If a declared role cannot be found, it comes back
in `roles.unresolved` **with candidate field names** — put those to the user rather than picking one.

### Read `dropped`, and tell the user

```text
{"built": true, "documents": 4523,
 "columns": ["title", "age", "word_count", "genre", "read_url", "cover_url"],
 "dropped": [["isbn", "not_found", "no anchor 'ISBN: ' in the sample"]]}
```

A dropped column is **invisible everywhere else**: later answers simply work around it, so this
report is the only place it is ever mentioned. Same for `get_knowledge_index`, whose warnings
routinely surface data problems the customer did not know about — on one real catalogue, a tenth of
the records had a page count of `0`, which is not a short book but a missing value recorded as zero,
and it would have dragged down every average built on it.

Report those in the customer's own terms. Nothing else in the platform will.

### Changing it later

```text
patch_knowledge_index(name="books", request="also track the author", apply=false)
```

Run with `apply=false` first, show the user what would change, batch several edits, then apply once.
Applying **re-reads fields from stored text; it does not re-embed anything**, so it is cheap.

Asking for something the documents do not contain returns a `refused` entry with a reason — pass that
to the user verbatim instead of inventing a workaround.

## 5. ★ Verify retrieval — don't skip ★

```text
search_knowledge_base(kb_name="Company policy", query="how is the late fee calculated")
#   hits  → the agent can answer this
#   empty → the agent will treat it as "not covered" and say so
```

## 6. Mount it

```text
update_agent(name="Support", add_knowledge_bases=["company-policy"])   # incremental — keeps existing mounts
```

Don't write "always cite the passage" in `instructions` — that behaviour is built in. Only write what is
specific to *this* library: authority ordering, coverage boundaries, special usage (e.g. "quoting a rate
must state its effective date").

> **Report back — don't stop at "imported".** Tell the user how many chunks landed and give them the
> clickable link to open the knowledge base and its **knowledge starmap** (a 3D view of what was
> ingested): `https://console.agent4.io/#/knowledge-bases/Company%20policy` — then confirm it's attached
> to the agent.

## Let your agent query your knowledge base

Your connected agent can search **your own** knowledge bases directly — to ground an answer or pull a
fact mid-task.

```text
list_knowledge_bases()                                  # what's available
search_knowledge_base(kb_name="Company policy", query="late fee for 60 days overdue")
```

Access is authenticated by your tenant API key, so **private knowledge stays private** — there is no
unauthenticated path to it. If the tenant is in **BYOK / privacy mode**, content endpoints return `403`
(metadata such as usage still works), by design.

Use retrieval to *ground*, not to decide: quote what comes back; if nothing does, say it isn't covered
rather than guessing.

---
name: agent4-io-storyline
description: Compile multi-step processes into stateful, guided Storyline graphs.
version: 8
---

Compile multi-step processes into stateful, guided Storyline graphs.

## Compile a flow into a Storyline

A **Storyline** is a directed graph hung on an agent: it turns "answer one question" into "carry a whole
task end to end" (intake, tutoring, coaching…). Nodes are steps (each with its own task / skills / kb /
tools + writable profile dimensions); exits carry conditions (`ai` / `user_choice` / `rule` / `callback`
/ `goto_storyline`). The runtime **never edits the agent's soul or safety boundary** — it is constant from
the first node to the last, which is exactly what a regulated or child-facing product needs.

## Create a draft

```text
create_storyline(
  agent_name="Support", key="loan-intake", name="Loan intake",
  profile_schema={"docs_ready": {"type": "bool"}},          # dims that accumulate across nodes
  graph={"nodes": [
    {"node_key": "n1", "title": "Understand need", "flags": {"is_entry": True},
     "on_enter_opening": "Hi — which kind of loan are you applying for?",
     "exits": [{"kind": "ai", "label": "need clear", "to_node_key": "n2",
                "ai_criteria": "the user stated the loan type and rough amount"}]},
    {"node_key": "n2", "title": "Collect documents",
     "task": "Collect the checklist items; chase missing ones across turns.",
     "exits": [{"kind": "user_choice", "label": "documents ready", "to_node_key": "n3",
                "user_choice": {"button_text": "I've uploaded everything"},
                "writes": [{"ref": "dim", "key": "docs_ready", "op": "set", "value": True}]}]},
    {"node_key": "n3", "title": "Hand off", "task": "Summarise the case and hand off to a human.",
     "flags": {"is_terminal": True}, "exits": []}
  ]},
  allow_agent_enroll=True,
  enroll_trigger="the visitor says they want to apply for a loan",
)
```

## ★ Validate, then publish ★

```text
validate_storyline(storyline_id="…")   # → {"ok": true} is required to publish
publish_storyline(storyline_id="…")    # freezes an immutable version and goes live
```

## Enrollment — who enters, and when (all require publishing)

- `is_default=True` — one per agent; auto-enrolls on the first conversation.
- `allow_agent_enroll=True` + `enroll_trigger` — the agent enrolls the user when it judges the trigger.
- `entry="user"` (or `"both"`) — the flow is listed in the chat widget's guided-flows menu and the
  New-chat dropdown, so the **user starts it deliberately** (a button, not a model judgement).
  Give it a `display_name` and a one-line `description` — that's what the menu shows. Combine with
  `concurrency="session"` for "one case per conversation" flows: each pick opens a fresh case.
- Manual assignment in the console.

## What the user sees — visibility, banner, and the read-only map

`user_visibility` controls the end-user presentation of a running flow (default `invisible`):

- `invisible` — no UI at all; the flow drives silently (previous behaviour).
- `named` — a slim banner above the chat shows the flow's name. Nothing else.
- `trail` — banner + a **View** button opening a read-only map: steps already taken carry their
  titles; untaken branches and future steps are anonymous grey blocks (redacted server-side —
  the user sees how long the flow is, not what's in it).
- `full` — banner with step `x / y` + the full map: every step named, colour-coded
  done / current / upcoming.

Extras: `allow_exit=True` adds an Exit button to the banner (an exited flow does **not**
auto-re-enroll in that conversation; a user-picked flow can be re-entered from the menu, progress
kept). `show_profile=True` lists the profile dimensions' current values under the map (numbers as
progress bars when the schema declares min/max). Per **node**, `rewind: "reset" | "keep"` lets the
user click a taken step in the full map and go back to it — `reset` restores the profile snapshot
taken on arrival, `keep` keeps collected data (study/review flows). Real-world side effects (filed
records, submitted documents) are never rolled back, so mark only side-effect-free steps.
On IM channels (Telegram/WhatsApp) the `/storyline` command reports the current flow and, for
`trail`/`full`, returns a short-lived signed link to the same read-only map.

The legacy `learner_visibility` parameter name and its `hidden` / `completed_only` values are still
accepted (they map to `invisible` / `trail`) but are deprecated — use `user_visibility`.

## Concurrency — does progress follow the person, or the case?

`concurrency` decides how many runs one user can have on this line:

- `"user"` (default) — **one run per person**; every conversation continues the same progress.
  Right for curricula, onboarding, KYC: "how far has *this person* got".
- `"session"` — **one run per conversation**; a new chat starts a fresh, independent case.
  Right for licence applications, support tickets, per-product flows: "how far has *this case*
  got". The same user can run three product applications in three chats, each with its own
  progress and blackboard.

Put state where it belongs: **case state on the blackboard** (it lives and dies with the run —
the product name, this application's document list), **facts about the person in profile
dimensions** (they follow the user across runs and storylines — company details, verified
identity). One case per conversation is deliberate: to open another case, open another chat.
Changing `concurrency` affects only future enrolments; runs already in flight keep their key.

## Checklists, gated choices, files, and deterministic actions

Four node-level capabilities turn "the AI decides when we're done" into accumulated,
deterministic state:

- **`checklist`** — `[{key, label}, …]` on a node. Each turn the platform checks items off from
  what the visitor *actually provides* (uploads, or descriptions with concrete details — promises
  don't count), and an exit rule `{"op": ">=", "left": {"ref": "checklist"}, "right": {"value": 1}}`
  advances the moment everything is checked. The read-only map shows the user a live ✓/○ list.
  This is the right shape for application/approval flows: step 1 announces what's needed, step 2's
  checklist collects it item by item.
- **`choices_offer: "on_ready"`** — game-style pacing for choice buttons: they stay hidden (and
  text-matching them is disabled — no skipping ahead by typing the button word) until the step is
  done — checklist complete, or a `choices_ready_criteria` you provide is judged true. Use
  `user_choice` for genuine decisions between alternatives; a lone "continue" button is a smell.
- **`{"ref": "files"}`** in exit rules — the number of files/images uploaded *while at this node*
  (resets on transition). `files >= 2` is a fully deterministic "documents received" gate.
- **`questions`** — per-node icebreaker chips (max 6): the questions a user would likely ask *at
  this step*, shown as tappable suggestions while they're on it. Pair with `on_enter_opening` so
  every step both introduces itself and offers a way in — a user should never wonder "what am I
  supposed to do here".
- **`on_enter_actions` / `on_complete_actions`** — `[{tool, args}]` the platform executes
  deterministically when the step is entered / completes the flow (e.g. file the lead with
  `mcp__agent4__submit_lead` at the terminal step). String args interpolate dimension and
  blackboard keys with curly-brace templates. Failures are logged and never break the chat.

**Context stays flat no matter how long the storyline is**: each turn injects only the *current
node* (task, resources, choices), the profile dimensions, and a size-capped blackboard — never the
whole graph or past steps. Long journeys (a school year, a season-long game arc) should be chained
storylines (`on_complete: goto_next`): each line's blackboard starts fresh while profile dimensions
carry over, which is exactly "summarise the past, keep the present verbatim".

The exit judge now sees a recent-conversation window and the collected state, not just the last
message — but keep `ai_criteria` about things the *visitor* said or did; the checklist mechanism
above is still stronger than any prose criteria.

## Design pitfalls — each of these has produced a stuck flow in production

You (the agent building this) are the most likely author of these bugs. Check every one before
publishing:

1. **A `rule` exit needs a writer.** `readiness >= 100` is a dead end unless something actually
   writes `readiness`: an exit's `writes` (deterministic — preferred), a node's `profile_writes`
   with `source: "ai"` (scored from conversation), another storyline, or manual console edits.
   `validate_storyline` now flags this as `warn.rule_unwritten_dim` — treat that warning as a bug
   unless you know an outside writer exists. This exact mistake shipped once: a three-step intake
   whose second step gated on a dimension nothing wrote; users could never pass it.
2. **AI-scored dimensions almost never hit exact bounds.** If the dimension is scored by the model,
   `>= 100` (or `== max`) practically never fires — models score conservatively. Gate on a
   realistic threshold (`>= 70`), or make the step's completion a `user_choice` and use the exit's
   `writes` to set the value deterministically.
3. **`user_choice` matches the button text exactly — and the label must say what it does.**
   The visitor's message must equal `button_text`. On visible lines the widget renders these as
   real buttons, so write **complete, precise verb phrases** — "Start document collection", not
   "Start" (start *what*? — real feedback from testing). Keep them distinct and in the audience's
   language. On `invisible` lines there are no buttons — restate the options in the node `task`.
   Prefer `user_choice` for genuine decisions (which branch, submit vs. keep editing); "am I done
   with this step" is the AI/rule exits' job, not a button.
4. **Publishing does not touch runs already in flight.** Enrollments stay pinned to the revision
   they started on — a bug-fix release reaches only *new* runs. To move existing users, call
   `POST /storylines/{id}/enrollments/migrate` (`reset` back to the entry or `move` to a node —
   both re-pin the run to the current published revision).
5. **Walk the line as a user before handing it out.** Open the share's `/s/` page, enter the flow,
   click through every button and branch to the end. The editor's test-run simulates the graph;
   only the real page exercises openings, buttons, visibility and completion together.

Exits are **priority-ordered** (list order): deterministic `rule` / `user_choice` / `callback` are judged
first, `ai` last. Build if/else, retry loops and AND-joins out of deterministic exits — don't gamble on
the LLM. Edit a draft with `update_storyline` (PUT semantics; keep every `node_key` stable, since exits
and the funnel reference it).

> **Report back.** Return the published Storyline's console link —
> `https://console.agent4.io/#/storylines/<id>` (the id from `create_storyline`) — with a one-line
> summary of the flow and how a user enters it.

## Modelling a process as a Storyline — the right way

Turning a complex process into a Storyline is a modelling exercise, not a transcription. The mechanics
are in [Compile a flow into a Storyline](/cookbook/build-a-storyline); this is *how to think about it* so
the result is reliable rather than a graph that mostly works.

## Start from the profile, then the decision points

Before drawing nodes, decide **what you are tracking** — that is the `profile_schema` (e.g. `docs_ready`,
`risk_flag`, `attempts`). Then map the **real decision points**, not just the happy path. Every place the
conversation can branch or fail is a node with exits; a flow that only models the ideal path breaks the
first time a user does something unexpected.

## One node = one coherent step

A node should do one thing a person would name ("collect documents", "confirm identity"). Don't cram a
whole sub-process into a single node's `task` and hope the model sequences it — you lose the ability to
branch, resume and measure. If a node's task has "and then, and then", it's several nodes.

## Make branching deterministic where the outcome must be reliable

- Route on **`rule`** (against profile dims) or **`user_choice`** when the branch must be predictable.
  Reserve **`ai`** exits for real judgment ("did they actually describe their problem?").
- Exits are **priority-ordered** — put the deterministic ones first, the `ai` fallback last.
- Model a retry loop with a back-edge plus a `writes` counter (`op: "inc"`) and a `rule` cap. Never rely
  on the model to decide it has looped enough.

## Keep identity and safety on the agent, not the node

The agent's `soul` and safety boundary are constant across the whole Storyline — that is the point. Don't
try to re-state the persona or re-impose safety per node; nodes only add task/skills/kb/tools and write
profile dims.

## Keep node_keys stable; validate before publish

`node_key`s are the identity exits and the funnel reference. When you edit with `update_storyline`, keep
them stable — renaming a node silently orphans its exits. Always `validate_storyline` before
`publish_storyline`; it catches unreachable nodes, dead ends and dangling exits.

## Don't over-model

If the task is a single question and answer, it is **not** a Storyline — it's an agent with a knowledge
base. Reach for a Storyline when there is genuine multi-step state to carry (intake, tutoring, a guided
application). Modelling a one-shot Q&A as a graph adds cost and failure modes for nothing.

## Common ways it goes wrong (avoid these)

- **Happy-path only** — no exit for "user is confused" or "didn't provide it", so the flow stalls.
- **Everything is an `ai` exit** — routing becomes a gamble; the same input takes different paths.
- **A mega-node** — one node's `task` describes the entire process; nothing can branch or resume.
- **Unbounded loops** — a back-edge with no counter and no cap.
- **Restating safety per node** — noise that competes with the agent's actual boundary.

Fix these by naming the real states and moving each decision onto a deterministic exit.

## Parallel steps — do several things, then continue

Some steps aren't a line — they're "do all of these, in any order, each with its own follow-ups, and
continue only when every one is done." A visa application is the classic case: passport, bank statement
and invitation letter each need collecting and a *different* review, but you can't submit until all three
pass. That's a **parallel** node (a fork / AND-join), a first-class node type — you don't hand-wire
completion flags.

## How it works

A `parallel` node declares several **required branches**, each pointing to the entry of its own sub-flow.
The engine presents the unfinished branches as choices, tracks completion natively (entering a branch
records it; returning to the parallel node marks it done), and takes the node's **join exit** — the first
exit with a `to_node_key` — **automatically, once every branch is complete.** You don't evaluate that
condition yourself; the label is just for humans. Each branch can be a full multi-node sub-flow with its
own checks and loops; its last step simply takes a normal exit back to the parallel node.

```text
create_storyline(
  agent_name="Visa", key="visa-docs", name="Visa documents",
  graph={"nodes": [
    {"node_key": "collect", "title": "Collect all documents", "type": "parallel",
     "flags": {"is_entry": True},
     "parallel": {"branches": [
       {"key": "passport", "label": "Passport",         "to_node_key": "p1"},
       {"key": "bank",     "label": "Bank statement",   "to_node_key": "b1"},
       {"key": "invite",   "label": "Invitation letter","to_node_key": "i1"}
     ]},
     "exits": [{"kind": "ai", "label": "all documents cleared", "to_node_key": "submit",
                "ai_criteria": "all required documents have been checked"}]},

    {"node_key": "p1", "title": "Check passport", "task": "Verify validity ≥ 6 months; if not, tell the user what to renew.",
     "exits": [{"kind": "ai", "label": "passport ok", "to_node_key": "collect", "ai_criteria": "passport is valid and legible"}]},
    {"node_key": "b1", "title": "Check bank statement", "task": "Confirm 3 months of history and a sufficient balance.",
     "exits": [{"kind": "ai", "label": "bank ok", "to_node_key": "collect", "ai_criteria": "statement covers 3 months and meets the threshold"}]},
    {"node_key": "i1", "title": "Check invitation", "task": "Confirm host details and dates match the trip.",
     "exits": [{"kind": "ai", "label": "invite ok", "to_node_key": "collect", "ai_criteria": "invitation is consistent with the trip"}]},

    {"node_key": "submit", "title": "Submit application", "task": "Package the cleared documents and submit.",
     "flags": {"is_terminal": True}, "exits": []}
  ]}
)
```

The applicant can supply the three documents in any order; each returns to `collect` when it clears.
`submit` is **unreachable until all three branches are done** — the engine only takes the join exit then.

Give each branch as much of its own flow as it needs — a passport that's expiring can loop through a
"renew and re-upload" node before it returns; the bank branch can ask for a top-up statement. Keep the
branch `key`s unique. Then `validate_storyline` before publishing — it flags a parallel node with no
branches, a branch pointing at a missing node, or no join exit.
