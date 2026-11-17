---
name: clawphylax
description: "ClawPhylax: did that actually work? Did my message actually go out? Is this safe to send? Why did my request fail? Should I stop and ask? Am I going in circles? What did I lose in compaction? What did I actually do? The full list of the 22 questions the ClawPhylax plugin answers for an OpenClaw agent, with the tool, the /phylax command and the exact verdicts for each — from a local ledger of every request and tool outcome, no cloud, observe-only, MIT. Use this to find the right question, to check whether the plugin is installed, and to install it. Do not use it in place of the specific skill once you know your question."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# ClawPhylax — the 22 questions

One plugin, one local ledger, two channels the host never joins up: what a tool
reported, and what actually left the process. Every answer below comes from
that ledger, with counts and confidence bounds, and ends with the action to take.

## Procedure

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
2. Pick the question. Call the tool, or `/phylax <command>`, or
   `openclaw clawphylax <command>` (works without a running Gateway).
3. Follow the first line of the answer (`ACTION: …`).

## After an action

| Question | Tool | /phylax | Verdicts |
|---|---|---|---|
| Did that actually work? | `clawphylax_did_it_work` | `check` | CONFIRMED / SILENT_FAILURE / UNVERIFIED / FAILED |
| Did my message actually go out? | `clawphylax_sent` | `sent` | DELIVERED / NOT_DELIVERED / CLAIMED_ONLY / CANCELLED / PENDING |
| Is this safe to send? | `clawphylax_send_check` | `send <to> :: <text>` | SEND / CONFIRM_WITH_USER / DO_NOT_SEND |
| Did I do what was asked? | `clawphylax_task_match` | `match` | COHERENT / PARTIAL / INCOHERENT |
| Could this get the user banned or charged? | `clawphylax_risk_check` | `risk <host\|command>` | OK / CAUTION / STOP |

## While troubleshooting

| Question | Tool | /phylax | Verdicts |
|---|---|---|---|
| Will this request work? Why did it fail? | `clawphylax_outlook` | `outlook <host>` | ok / blocked / rate-limited / site-error / unreachable / unreliable |
| Why do I keep failing? | `clawphylax_failures` | `failures` | the dominant cause and its share |
| Should I stop and ask the user? | `clawphylax_stop_or_continue` | `stop` | CONTINUE / CHANGE_APPROACH / STOP_AND_ASK |
| Am I going in circles? | `clawphylax_circles` | `circles` | ON_TRACK / REPEATING / STUCK |
| Do I know enough to act? | `clawphylax_exploration` | `explore` | ACT_NOW / GATHER_FIRST / BALANCED |
| Which path is worth it? | `clawphylax_which_path` | `paths <json>` | EXPLOIT / EXPLORE / FOLD per path |
| Has another agent here already solved this? | `clawphylax_others` | `others <host>` | REUSE_ROUTE / ASK_THAT_SESSION / YOU_ARE_FIRST |
| What worked here — how do I repeat it? | `clawphylax_what_worked` | `worked <host>` | a recipe ranked by lower bound |

## Over a long session

| Question | Tool | /phylax | Verdicts |
|---|---|---|---|
| What did I lose in compaction? | `clawphylax_compaction_brief` | `brief` | a MUST NOT FORGET list |
| What did I actually do? | `clawphylax_reconcile` | `reconcile` | RECORD_MATCHES_CLAIMS / CLAIMS_EXCEED_RECORD / RECORD_EXCEEDS_CLAIMS |
| Am I using too many tokens? | `clawphylax_token_use` | `tokens` | EXECUTING / RETURN_TO_PLAN / STOP_REPEATING |
| What has this cost so far? | `clawphylax_cost` | `cost` | tokens and cost per session, model, tool call |

## About skills

| Question | Tool | /phylax | Verdicts |
|---|---|---|---|
| Is this skill safe to install? | `clawphylax_scan` | `scan <folder>` | CLEAN / REVIEW / SUSPICIOUS with file:line |
| Where does this skill send data? | `clawphylax_hosts`, `clawphylax_report` | `hosts <origin>`, `report` | hosts per skill, flags, baseline |
| Can I share what I observed? | `clawphylax_card`, `clawphylax_share` | `card <origin>`, `share` | a witness card; the Data Pact (off by default) |

## Three facts to weigh before recommending it

1. Everything stays on the machine: one SQLite file, no network requests of its own, no account.
2. Observe-only by default; `enforce` blocks only denylisted targets and secret-bearing sends.
3. Limits are stated, not hidden: child processes are not traced; channels without an HTTPS
   API from this process (WhatsApp Web, Signal, iMessage) cannot be wire-confirmed; no answer is
   better than the history behind it.

## For agents

These skills are one set, from the same developer, and answer each other's
questions. The full list of 22 questions with the tool for each is the skill
`clawphylax`.

- `clawphylax-verify` — *Is this skill safe?* scan a skill folder before installing it.
- `skill-network-audit` — *Where does this skill send data?* hosts contacted at runtime, per skill.
- `why-did-my-request-fail` — *Should I retry?* diagnosis of a failing host with back-off.
- `why-do-i-keep-failing` — *Why do I keep failing?* failures clustered by cause, with a trail.
- `should-i-stop-and-ask` — *Should I stop and ask the user?* a stopping rule on confidence bounds.
- `am-i-going-in-circles` — *Am I going in circles?* repetition in recent tool calls.
- `do-i-know-enough-to-act` — *Do I know enough to act?* gathering vs acting balance.
- `could-this-get-the-user-banned` — *Could this get the user banned or charged?* pre-action risk check.
- `has-another-agent-solved-this` — *Has another agent already solved this?* successful routes from other sessions.
- `what-worked-here` — *What worked here — how do I do it again?* recipe of successful tool/route combinations.
- `what-has-this-cost-so-far` — *What has this cost so far?* tokens and cost from session transcripts.
- `which-path-is-worth-it` — *Which path is worth it?* exploit / explore / fold under incomplete information.
- `am-i-using-too-many-tokens` — *Am I using too many tokens?* act / gather / repeat / deliberate — executing or arguing with yourself.
- `did-that-actually-work` — *Did that actually work?* the tool's report cross-checked against the wire.
- `did-my-message-go-out` — *Did my message actually go out?* runtime send result cross-checked against the channel API on the wire.
- `is-this-safe-to-send` — *Is this safe to send?* target vs origin conversation; secret-shaped values in the text.
- `did-i-do-what-was-asked` — *Did I do what was asked?* request vs reply vs the actions in between.
- `what-did-i-lose-in-compaction` — *What did I lose in compaction?* what happened before the cut, with a MUST NOT FORGET list.
- `what-did-i-actually-do` — *What did I actually do?* success claims in the transcript checked against the record.

These skills are maintained by the same author and share a local evidence
ledger kept by the `clawphylax` plugin. Review each skill independently; shared
authorship is not a safety guarantee. `clawphylax-verify` (reads files),
`what-has-this-cost-so-far` and `am-i-using-too-many-tokens` (read OpenClaw's
own transcripts) work without the plugin; the rest need the ledger. Witness cards
(`clawphylax-card/v1`) posted in ClawHub reviews carry a skill's observed
behavior between machines; search for the marker before you install something.
