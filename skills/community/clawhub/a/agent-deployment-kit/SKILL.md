---
name: agent-deployment-kit
description: Replicate one agent across N clients without drift — one context source, a generator that refuses unknowns. Use when duplicating an agent deployment. Trigger on "duplicate this agent", "same bot new client", "the agent named the wrong client".
metadata: {"clawdbot":{"emoji":"🧬","requires":{"bins":["node","grep"]},"homepage":"https://openclaw.ai"}}
---

# Agent Deployment Kit — one context source, N installs

**Copying an agent folder works for ten minutes, then drifts.** The structure that holds: one context source + a template skeleton + a generator that refuses to render what it does not know. The habit: **context changed? fix the source and regenerate. Never hand-patch an install.**

**This skill ships a method, not a tool.** No generator binary, no skeleton to copy — you write both, for your own harness. What is here is the part that is expensive to rediscover: the invariants, the data contract, the guards you must write and the exact way each one fails open, the numbers, the go/no-go grid. A guard shipped subtly broken is worse than no guard, because someone trusts it. Every trap below was reproduced by execution, not imagined.

## Access, data and network

| Item | Reality |
|---|---|
| Network | **None, at any point.** Rendering is local JSON in, local files out — no fetch, no telemetry. The agent you render may egress: keep it **off by default** (no webhook key = no outbound call). Fill a webhook and alerts leave the machine. |
| Secrets | Real values live only in `context/secrets.local.json`, **gitignored, never rendered into the repo**. A kit whose templates use no secret must render without the file at all. Credentials move out-of-band — never in the repo, never in a ticket. |
| Personal data | A rendered agent that reads inbound DMs processes personal data. `LEGAL_BASIS`, `DATA_MINIMISATION`, `DATA_RETENTION` are **required questionnaire keys**, rendered into the templates and hard-gated below. **A retention nothing executes is not a retention** — a prompt line telling an LLM to delete old records is not an executor. Ship a job that deletes, or you have no retention. |
| Legal | The agents you configure act **from an account owned by the operator — never impersonating a third party** — and disclose automated operation on request (hard-coded, §Rule 1). Platform ToS and applicable law bind the deployment; a kit cannot consent on your behalf. |
| Backups | Every deploy that overwrites an install must back it up first. **A backup is a full copy of a rendered install, secrets in clear.** Nothing purges it but you. Count it as personal data. |

## When to Use

| Trigger | Action |
|---|---|
| "duplicate this agent for another client" | Do **not** copy the folder. Build the kit (§Anatomy), rewrite `QUESTIONNAIRE.json` from zero. |
| "the client changed their booking link" | Edit `context/QUESTIONNAIRE.json`, regenerate, redeploy. Never edit the install. |
| "same bot, new brand / persona / team" | New `context/`, same `skeleton/`. One skeleton, N questionnaires. |
| "we only sold 2 of the 3 workstreams" | **Delete** the out-of-scope crons and playbooks from the kit (§Rule 2). |
| "kit is ready, can we go live?" | Run the go/no-go grid (§Pre-deploy audit). One hard gate missing = NO-GO. |
| "why is the agent talking about the other client?" | §Rule 3 — residue hunt. You skipped it. |

## Kit anatomy

```
agent-kit-<context>/
├── context/
│   ├── QUESTIONNAIRE.json           # the ONLY source of context. Committed. No secrets. ASCII.
│   ├── secrets.example.json         # key list + how to obtain each. Committed. Never a value.
│   └── secrets.local.json           # real values. GITIGNORED. Never rendered into the repo.
├── skeleton/                        # the parameterised engine — {{PLACEHOLDER}} inside
│   ├── openclaw.tmpl.json           # also the install marker a deploy looks for
│   ├── cron/jobs.tmpl.json          # ONLY the sold workstreams
│   ├── scripts/health.tmpl.sh
│   └── workspace/
│       ├── SOUL.tmpl.md             # persona + absolute red lines
│       ├── AGENTS.tmpl.md           # operating manual — ALSO seen by sub-agents (§Field of vision)
│       ├── TOOLS.tmpl.md            # accesses + forbidden ones — ALSO seen by sub-agents
│       ├── USER.tmpl.md             # who is served. Main session only.
│       ├── HEARTBEAT.tmpl.md        # what to check between runs
│       ├── MEMORY.tmpl.md           # personal context. Main session only — never a delegated turn.
│       └── PLAYBOOK-<AREA>.tmpl.md  # one per sold workstream. Delete the others.
├── generator/generate.mjs           # YOU write it — §The generator you write
├── out/                             # GITIGNORED. Rebuilt every run. Carries an ownership marker.
├── README.md                        # human-only. The "not sold / later" list. No agent reads it.
└── .gitignore
```

**Shipped with this skill:** `context/QUESTIONNAIRE.example.json` and `context/secrets.example.json` — the data contract, fictional, ASCII, sentinel-bearing. That is all. The skeleton, the generator and the `.gitignore` are yours to write; nothing else is on disk and nothing else is promised. Your `.gitignore` needs exactly three lines. The first two are what the secret story rests on; the third covers a narrower case — see below:

```gitignore
context/secrets.local.json
out/
*.bak-*
```

`*.bak-*` only covers a deploy target rendered **inside** the repo during testing. It is not what keeps production backups out of git: those land at `<home>.bak-<ISO>` on the target machine, outside the tree entirely, where nothing ignores them and nothing purges them but you (§Access, data and network).

What makes the structure hold: **`out/` is disposable** (patch it, your patch dies at the next generate — the point) and **`context/` is never bypassed** (a value not in the questionnaire is not in the install). The two failure modes it kills — residue leak, instance drift — return the moment either is untrue.

## The context contract

One JSON file, two blocks, no third. Copy `context/QUESTIONNAIRE.example.json` and rewrite every value.

| Block | Holds | Rule |
|---|---|---|
| `_meta` | context slug, sold/not-sold scope, the ASCII warning | Prose for humans. Never rendered. |
| `config` | `INSTALL_DIRNAME`, model ids, paths | Machine-facing. `INSTALL_DIRNAME` is **untrusted path input** (§The generator you write). |
| `context` | everything rendered into the agent's files | ASCII only — these strings go into outbound messages. |

**Present-but-empty vs absent is a real distinction and your generator must honour it.** A key absent from the questionnaire while a template uses it = hard failure (`Placeholder with no value: {{X}}`) — that is the removal test of Rule 2 working. A key present with an unknown-sentinel = a known unknown, rendered in warn mode, refused at deploy. A key present and empty = the silent killer: it renders as nothing and the file stays well-formed. **Never write `""` to mean "not decided yet"** — write the sentinel.

`TO_PROVIDE` (client provides), `TO_CREATE` (we create it), `TO_GENERATE` (a token, at setup) — arbitrary literals, one regex, rename them freely. Every value that is not written on a verified source stays a sentinel. **A questionnaire still listing unknowns means the scoping call is not finished** — that is information, not an obstacle.

## The generator you write

~130 lines, zero business constants: reads two local JSON files, writes `out/`. Requirements, each with the way it fails open. **Every one of these was written wrong by a competent author, passed review, and was caught only by execution on a hostile fixture.**

| Requirement | The trap that makes it fail open |
|---|---|
| **Iterative render, bounded.** Values may themselves contain placeholders — one pass is not enough. Cap the passes and die loudly. | An unbounded loop hangs instead of failing; a single pass leaves `{{X}}` that the validator then reports as *your* bug, not the questionnaire's. 10 passes is not a limit to raise — past it, you have a cycle. |
| **Placeholder regex must accept digits:** `[A-Z0-9_]+`. | `{{TG_CHAT_2}}` is never matched, never substituted — **and the post-render validator built on the same regex cannot see the leftover either.** The class the renderer misses is exactly the class the validator misses. Verified: `"{{TG_CHAT_2}} {{HOME}}".match(/\{\{([A-Z_]+)\}\}/g)` → `['{{HOME}}']`. |
| **Two modes, one gate.** Default `warn`: unknowns render, each printed as `WARN unknown: <KEY>`, exit 0. `--strict` (implied by deploy): any unknown → non-zero exit, nothing written. | One mode makes the gate either unusable during scoping or advisory at deploy. Deploy must never be able to run in warn mode — that is the whole point of having two. |
| **Refuse deploy on any unknown** — the sentinel gate. | **Type-keying it fails open.** `typeof v === 'string' && SENTINEL.test(v)` skips `null`, numbers, arrays, objects. Reproduced: `"LEGAL_BASIS": null` deployed at exit 0 with a red line reading *"lawful basis is null"*; `["TO_PROVIDE - not decided"]` walked a **live sentinel** into the deployed file while the gate said OK. **Type-check first, then test the string** — and see the `JSON.stringify` row below for why the obvious repair is itself the bug. |
| **Every value in `config` and `context` is a non-empty string** (`_meta` is exempt — it is never rendered). Not just the compliance keys, and not `context` alone — that is the actual invariant. | Gating `context` and leaving `config` unwalked is the same fail-open one block over: `"INSTALL_HOME": "TO_PROVIDE - absolute path"` is a live sentinel the gate never sees. Scoping the type check to `LEGAL_BASIS`, `DATA_RETENTION`, `DATA_MINIMISATION` leaves every other key undefended: `"BOOKING_URL": ""` renders *"every interested person is routed here: "* — well-formed, silent, and the conversion link is gone. Reproduced. Convention (*"never write `\"\"`"*) is not a guard; the compliance keys are not special, they are just the ones where the failure is legible. |
| **Do not `JSON.stringify(v ?? '')` to make a value testable.** | It launders `null` into `""`, which the sentinel regex then calls clean. The repair that looks obvious re-opens the hole it closes. Verified: the serialise-then-test shape refuses **3 of 6** hostile values (`null`, `90`, `""` all pass); the type-check-first shape refuses 6 of 6. |
| **Post-render validation on the files, not the vars:** 0 residual `{{...}}`, every `.json` re-parsed. | A value carrying a quote produces valid-looking, broken JSON. The render is not the deliverable — the files are. |
| **Validate `INSTALL_DIRNAME` before use:** single segment `[A-Za-z0-9._-]+`, never `.` or `..`. | It looks like a name, it is a path fragment. `".."` resolves the target to your home directory and the deploy **renames it**. Valid JSON, no placeholder, no error. Verified: `path.join(os.homedir(), "..")` → `/Users`. |
| **Own a directory before you wipe it.** Write an ownership marker when you create `out/`; refuse any `out/` lacking it. | `out/` is the default build dir of tsc, next export and webpack. "Rebuilt from scratch every run" reads as hygiene and executes as `rm -rf` on a stranger's build tree. |
| **One guard function, called from every destructive path.** Count your `rmSync`/`renameSync` call sites, not your guards. | The obvious path refuses, a sibling entry point still wipes. Reproduced: a foreign `out/dist/bundle.js` survived a plain render (exit 1) and was destroyed by the purge path (exit 0) — the purge reached its own `rmSync` through an early exit, *before* the guard line. The path that bites is never the one you tested. |
| **Require an install marker before overwriting.** Refuse `$HOME`, refuse `/`, refuse a target with no `openclaw.json`; back up to `<home>.bak-<ISO>` first. | The marker test is the only thing between a typo (`~/Documents` for `~/Documents/.agent`) and a renamed real folder. `renameSync` never asks. |
| **Set modes on the destination, after write *and* after the copy:** 0700 dirs, 0600 files, 0700 `.sh`. | A rendered file is a **new** file at the umask (0644) — rendered secrets land world-readable. A copy carries bytes, not modes: the chmod you did before it is gone. Fails weeks later as `permission denied`, or never, which is worse. |
| **Deploy is opt-in; default stops at `out/`** so a human reads it first. | Anything else makes review theatre. |

The sentinel gate is the one to get right, since it is the only thing standing between an unknown legal basis and a live agent reading DMs. The shape — an example to adapt, not a drop-in:

```js
const SENTINEL = /(TO_PROVIDE|TO_CREATE|TO_GENERATE)/;   // anchor all alternatives or none
// Contract: every value in `config` AND `context` is a non-empty string. Anything else is an unknown.
// Walk both blocks. `_meta` is exempt — it is never rendered.
const isUnknown = v => typeof v !== 'string' || v.trim() === '' || SENTINEL.test(v);
```

Type-check **before** you test, and never reach for `?? ''` to make a value testable: `JSON.stringify(null ?? '')` hands back `""` — the silent killer, laundered into a value your regex calls clean. Serialising is not the fix; it is how the fail-open gets in. Verified against the six values below: `typeof v !== 'string'` catches `null`, `90` and both containers; `v.trim() === ''` catches `""`; the regex catches the live sentinel. Six refusals.

**A gate that passes in case of doubt is worse than no gate.** Before trusting yours, run it against: `null`, `90`, `["TO_PROVIDE"]`, `{"note":"TO_PROVIDE"}`, `"token: TO_GENERATE"`, `""`. Six values, six refusals. If any returns clean, the gate is decorative. And a check that reads zero files must **abort**, not report "no errors" — zero records verified reads exactly like a clean run.

## Rule 1 — load-bearing guardrails go in the static body

Any guardrail carrying real risk (red lines, escalation, hard refusals, data protection) is written **in the static body of the template**, never only through a variable — a variable is a promise the questionnaire may not keep.

```markdown
## Absolute rules      <!-- WRONG: the rule is only as present as the key is full -->
{{EXTRA_RED_LINES}}
```
Empty key → the section renders blank → install #3 ships with no red lines and nobody notices, because the file is still well-formed. The classic second half of that anti-pattern is a red line telling the agent to deny being a bot. Named here only to reject it: **instructing an agent to deny being an AI is deception, not a guardrail** — it protects nobody and serves neither transport nor account safety. Do not propagate it in any form; the RIGHT block inverts it.

```markdown
<!-- RIGHT — hard-coded body, variable only extends it -->
## Absolute rules (HARD-CODED — apply even if the context is incomplete)
- If asked whether you are an AI, a bot, or automated: **say yes, plainly**, then continue helping.
  Never claim to be human. Never dodge the question.
- You operate from an account owned by {{CLIENT_NAME}}. Never present yourself as a third party.
- If a platform defense, challenge or block appears: **stop and hand over to a human.**
  Never work around it, never retry to get past it.
- Personal data: lawful basis is {{LEGAL_BASIS}}. Store only {{DATA_MINIMISATION}}
  Retention: {{DATA_RETENTION}} — then deleted, not archived. Deletion request → escalate, do not answer.
- Outbound DMs: ASCII only, max {{DM_MAX_CHARS}} characters (platform-side mangling of accents/emoji
  is real — a transport constraint, not a style choice).
- Context-specific additions (never replacements): {{EXTRA_RED_LINES}}
```

Write the same treatment for escalation, out-of-scope refusal, the pricing rule and no-invention. All hard-coded; only their **parameters** (who to escalate to, the char limit, the retention window) are variables. Empty variable → you lose a detail, not the rule. Duplicate the lot verbatim into `AGENTS.md` (§Field of vision).

## Rule 2 — out of scope is removed, not disabled

A cron with `enabled: false`, or a `PLAYBOOK-BILLING.md` for a workstream never sold, is not neutral: **the agent reads it and improvises.** Files in the workspace are context, not dead code — every one is injected into the model's turn. Not sold → delete from the kit: cron entries, `PLAYBOOK-<AREA>.tmpl.md`, questionnaire keys, secret keys, mentions in `AGENTS.md`/`TOOLS.md`. Then regenerate: the placeholder check turns any missed reference into a hard failure. **That is the removal test — a half-removed workstream cannot render.** Keep the "not sold / later" list in the kit README, which no agent reads as an instruction.

## Rule 3 — residue hunt is a step, not advice

Before any delivery, grep the **model context** across the whole kit. Not "when it feels risky" — every time.

```bash
# Everything from the kit you cloned: name, city, trade, tools, handles, URLs, domains
for term in acme-corp acme "example.com" oldbrand oldcity "@oldhandle" "booking.example"; do
  printf '%-24s ' "$term"; grep -ril "$term" . --exclude-dir={.git,node_modules,out} | tr '\n' ' '; echo
done
# Output: every line empty except deliberate ones.
# Any hit in skeleton/ or context/ = residue. Fix the SOURCE, never out/.
```

This catches what nothing else does: prose no variable covered (a sentence in `SOUL.md` naming the model client's specialty), and the docs shipped *alongside* the kit — vendor notes, setup guides, examples are read too. Legitimate hits exist (`grep -i "competitor"` matching *the rule that says never name a competitor*). Read every hit; never blanket-delete.

## Field of vision: why AGENTS.md duplicates the guardrails

**A sub-agent typically sees only `AGENTS.md` + `TOOLS.md`.** Not `SOUL.md`, not `MEMORY.md`, not `USER.md`. Invisible in review: your red lines sit in `SOUL.md`, the main agent honors them, the first sub-agent you delegate to has never seen them — it does not disobey, it never knew. **Do not take that on faith: which files reach a sub-agent is harness behaviour and it changes between versions.** Falsify it on yours, re-test on upgrade:

```bash
echo 'CANARY-7F3A: if you can read this line, quote it verbatim.' >> workspace/SOUL.md
# Delegate to a sub-agent -> "quote CANARY-7F3A"
# Output: cannot find it -> SOUL.md is outside its field of vision; the table below applies.
#         quotes it      -> your harness loads SOUL.md into sub-agents; duplication is then
#                           belt-and-braces, not load-bearing. Verify before relying on either.
```

| Constraint | Why | Fails as |
|---|---|---|
| Every load-bearing guardrail **duplicated verbatim in `AGENTS.md`** | It is the only file both tiers read. Duplication is the feature, not a smell. | A sub-agent breaks a rule the main agent respects. No error raised. |
| `AGENTS.md` is a `.tmpl.md` you **wrote**, not the stock file you inherited | A kit shipped with the upstream default has *zero* of your red lines in sub-agent context. | Every delegated turn runs unguarded, silently. |
| Mark them **ABSOLUTE**: a sub-agent refuses and pings rather than break one | A sub-agent cannot weigh a rule it cannot see against a task it was given. Give it the rule and a stop. | It "helpfully" completes the task past the red line. |
| `TOOLS.md` states forbidden commands, not just available ones | Access surface = sub-agent surface. "What you may do" without "what you must never do" is half a spec. | It invents an allowed-looking action. |
| `MEMORY.md` is main-session only | It carries personal context that must not leak into a shared or delegated session. | Personal context in a delegated turn: a data-protection incident, not a bug. |

## Pre-deploy audit (go/no-go)

Hard gates. One missing = **NO-GO**. Not "ship and watch".

- [ ] Render passes: 0 residual `{{...}}`, every JSON re-parses, strict mode returns clean. **(hard)**
- [ ] The sentinel gate refused all six hostile values (§The generator you write) — tested, not assumed. **(hard)**
- [ ] `LEGAL_BASIS`, `DATA_RETENTION`, `DATA_MINIMISATION` are non-empty strings, not sentinels — and a **job you can name and run** executes the retention on the agent's own stored data. **(hard)**
- [ ] `context/secrets.local.json`, if used, is filled and gitignored (`git log -p`: never committed); `QUESTIONNAIRE.json` holds no secret, and no sentinel on any key a template renders — `INSTALL_HOME` may stay a sentinel **only** if the deploy is invoked with an explicit path argument. **(hard)**
- [ ] Residue grep of the model context returns only deliberate hits (§Rule 3). **(hard)**
- [ ] Every load-bearing guardrail appears in `AGENTS.md`, not only `SOUL.md`; `AGENTS.tmpl.md` is kit-authored, not the stock upstream file. **(hard)**
- [ ] Scope: crons and playbooks match exactly the sold workstreams — nothing inert, nothing extra. **(hard)**
- [ ] Every cron ran **manually once**, observed end to end, before the loop is enabled. **(hard)**
- [ ] Human-validated steps are safe-by-default: no "OK" = no send (never "no answer = send"). Alert routing checked per recipient: ops gets errors, client gets business events.
- [ ] Credentials transferred out-of-band, in no file of the repo. Nothing invented: proof points, figures, credentials, affiliations trace to a source, or stay `TO_PROVIDE`.
- [ ] Backups accounted for: each is a full copy with secrets in clear. Purge them once the deploy is validated, and know the command before you need it.

## Recontextualising an existing kit

| Step | Why it must come here | Fails loudly as |
|---|---|---|
| 1. **Clone, then amputate** `.git`, `out/`, `secrets.local.json`, briefs, `.DS_Store` | New history: a new kit, not a fork. | Nothing — this one is on you. Do it first. |
| 2. **Cut the scope before writing a value** — crons, playbooks, keys not sold | Shrinks the surface every later step must cover. | Rule 2's removal test: a half-removed workstream cannot render. |
| 3. **Rewrite `QUESTIONNAIRE.json` from zero** — never find-and-replace; **rewrite `secrets.example.json`** (keys + how to obtain, never a value) | Find-and-replace only fixes the strings you thought to search for. That is how residue survives. | Not at all — that is what step 5 is for. Missing keys: `Placeholder with no value: {{X}}`. |
| 4. **Adapt the skeleton to the new domain** — conversion model, in/out-of-scope, sensitive cases, its own red lines, hard-coded in the body | §Rule 1: a variable is a promise the questionnaire may not keep. | Silently. Only the canary and the audit catch it. |
| 5. **Render into a temp path** with a throwaway secrets file, then **residue hunt** (§Rule 3) — now, not at the end | Proves 0 residual placeholders + valid JSON before any value is real. Cheap here, expensive after the fill-in. | Strict mode on the remaining unknowns. Expected. |
| 6. **Fill from verified public sources**, re-run strict, then the go/no-go grid | Not written on a source → stays `TO_PROVIDE`. Two findings conflict → keep the cautious one. | NO-GO. Private repo. Never commit `out/`. |

## Gotchas

| Trap | Why it bites silently | Fix |
|---|---|---|
| **A template marker as the LAST extension** — `SOUL.md.tmpl` | Publishing pipelines allowlist by **final** extension, and `tmpl` is in nobody's allowlist: a whole `skeleton/` silently vanishes from the published artifact, and the shipped SKILL.md points at files the user does not have. Verified on this very kit: 3 files of 13 arrived. | Marker as **infix**: `SOUL.tmpl.md`, `health.tmpl.sh`. Strip with `rel.replace(/\.tmpl\.([a-z]+)$/, '.$1')`. Simulate your publish and **count the files** before shipping. |
| **Sentinels pass every validation** | `"chat": "TO_PROVIDE - chat id"` is *valid JSON* and contains no `{{...}}`. Placeholder check: pass. JSON re-parse: pass. It ships. | The sentinel gate is the only thing that sees it — which is why it must not fail open on a type (§The generator you write). |
| **Anchoring one alternative in a multi-alternative regex** — `/(A|B|^C)/` | The `^` binds to `C` only. A value ending in one sentinel slips through while the same value ending in another is caught — two behaviours, no error either way. Verified: `/(TO_PROVIDE\|^TO_GENERATE)/.test("token: TO_GENERATE")` → `false`, vs `true` for `"token: TO_PROVIDE"`. | Anchor all alternatives or none. A sentinel anywhere in the value counts. |
| **An underscore-prefixed comment key you also use as a placeholder** | `_KEY` is a comment by convention and gets stripped from the variable map — so `{{_KEY}}` in a template dies at render as *"no value"*, not as the unresolved-placeholder error you would grep for. | Keep the comment convention out of the placeholder namespace. Never `{{_ANYTHING}}`. |
| **Hand-patching the install "just this once"** | It works. That is the trap. The next generate silently reverts it, and now two machines differ with no diff to read. | Fix `QUESTIONNAIRE.json`, regenerate, redeploy. `out/` is deleted every run to make this the only path. |

## Output format

Every kit delivery ends with this recap, verbatim — `<...>` filled, one line each, nothing added:

```
KIT: <slug>            VERDICT: [GO / NO-GO]          # filled: KIT: acme-corp  VERDICT: NO-GO
Render:   <n> files, 0 residual placeholders, <n> JSON re-parsed OK, strict [PASS/FAIL]
Gate:     sentinel gate tested on 6 hostile values -> <n>/6 refused
Scope:    sold = <list> | removed from kit = <list>
Residue:  grep <terms> -> <n> hits (<all deliberate / LIST>)   # 1 hit (TOOLS.md:16 — the rule itself)
Guards:   AGENTS.md carries <n>/<n> load-bearing rules | AI disclosure: honest [Y/N]
Data:     legal basis <named> | retention <window>, executed by <the job> | minimisation <fields>
Unknowns: <KEY> = TO_PROVIDE (<who provides it, when>) | Blocking: <hard gate missing, or "none">
```

## Troubleshooting

The left column is the vocabulary your generator should raise — errors are a spec, not decoration.

| Symptom | Cause | Fix |
|---|---|---|
| `Placeholder with no value: {{X}}` | Key used in a template, absent from context and secrets — or prefixed `_` and stripped as a comment | Two cases, opposite fixes. **Sold workstream:** add the key to `QUESTIONNAIRE.json`; never delete the placeholder to silence the error. **The removal test firing** (§Rule 2 — you cut the workstream): delete the leftover template reference too. Never re-add a key you just cut — that silently un-does the scope cut. |
| `Placeholder loop (circular reference?)` | A value contains a placeholder that resolves back to itself | Break the cycle in the questionnaire. 10 passes is not the limit to raise. |
| `Unresolved placeholders in <file>` | A non-template file copied raw with `{{...}}` inside it, or a placeholder produced by a value substituted on the last allowed pass | Template it, or break the chain. Never widen the pass cap. |
| Strict mode says OK on an unknown | The gate is type-keyed and skipped a `null`, a number, an array | **Type-check first**, then test the string: `typeof v !== 'string' \|\| v.trim() === '' \|\| SENTINEL.test(v)` (§The generator you write). Never serialize to make a value testable — `JSON.stringify(null ?? '')` is `""`, which the regex calls clean. Re-test the six values: 6/6 or the gate is decorative. |
| `out/ carries no ownership marker` | The kit was dropped into a repo that already builds to `out/` — refuse to delete what you did not create, on **every** path | Move the kit, or point it at its own directory. Do **not** delete the marker check. |
| Agent mentions the previous client | Prose residue no variable covered | §Rule 3. Fix `skeleton/`, regenerate. Never fix the install. |
| Sub-agent breaks a rule the main agent respects | The rule lives only in `SOUL.md` | Duplicate it verbatim into `AGENTS.md` (§Field of vision). |
| Install #2 behaves unlike install #1 | Someone hand-patched one | Diff both against a fresh `out/`. Backport the intent into the questionnaire, regenerate both. |
| `Invalid INSTALL_DIRNAME: ".."` | The questionnaire carries a path fragment, not a name | One segment, `[A-Za-z0-9._-]+`. The guard is the point — do not loosen it. |
| `<home> exists but carries no openclaw.json` | The target is not an install of this kit — usually a mistyped path | Check the path first. Force-override only once you are certain: the existing dir gets renamed. |

## Scope

**This skill ONLY:** describes how to structure a repeatable agent deployment (context source, skeleton, generator you write); specifies the data contract and the guards, each with the way it fails open; hunts residue from the kit you cloned; audits go/no-go before a loop is enabled. It ships two fictional example context files and no executable.

**This skill NEVER:** hands you a generator to trust unread — the guards are yours to write and test; instructs an agent to hide that it is an AI — if asked, it answers honestly; teaches evasion of any anti-abuse control — when a platform defense triggers, the run **stops and a human takes over**; blesses processing personal data without a named legal basis and a retention job that actually runs; patches a live install by hand; invents a fact the sources do not carry.

---
*Alexandre Bloch — Bloch Agents · alex.bloch55@gmail.com · ClawHub @AlexBloch-IA*
