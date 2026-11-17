---
name: clawphylax-verify
description: "Is this skill safe? Use this before installing any third-party ClawHub skill or running its scripts, and whenever the user asks whether a skill is safe. Inspects every file in the skill folder — SKILL.md and scripts — and reports every network host contacted, whether data or files are uploaded (curl -d/-T, requests.post, scp), and whether credential paths such as ~/.ssh, .env or ~/.aws are read. Returns exactly CLEAN, REVIEW or SUSPICIOUS with file and line; do not recommend installation on SUSPICIOUS. Do not use to judge a running skill's behavior — use skill-network-audit for that."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Verify a skill before installing it

A static scanner tells you what a skill *says*. This reads the files in front of
you and names the hosts, uploads and credential reads — then the ClawPhylax
plugin keeps watching after install (see the `skill-network-audit` skill).

## Steps

1. Confirm the plugin is active. If not, tell the user and offer:
   `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`

   ```bash
   openclaw clawphylax status
   ```

2. Fetch the skill without installing it, then scan the folder — or call the
   `clawphylax_scan` tool with the folder path:

   ```bash
   openclaw skills inspect <slug>          # or: clawhub inspect <slug>
   openclaw clawphylax scan <folder>
   ```

3. Read the verdict and report it with the hosts **by name**:
   - `clean`: only documented hosts, no uploads, no credential reads
   - `review`: uploads or credential-file reads — show the user the exact lines
   - `suspicious`: a known drop host (pastebin, webhook.site, ngrok, …) or a
     credential read combined with an upload — recommend not installing

4. Also search the skill's ClawHub page and repository issues for the marker
   `clawphylax-card/v1`: cards list the hosts the skill contacted on other
   machines. Compare them with the skill's documented service.

## Limits to state plainly

- The scan reads files; it cannot see what a downloaded script does later.
- A `clean` verdict means "nothing found in the text", not "safe".

## Use this when

Before `openclaw skills install <slug>` of any third-party skill; when the user asks "is this skill safe?"; when a skill's scripts are about to run for the first time.

## Do not use when

For what an already-installed skill actually did at runtime (use `skill-network-audit`). For deciding whether a remote service is trustworthy — a file scan cannot see what a server does after contact.

## Output

First line `ACTION: INSTALL_OK` / `ACTION: REVIEW_WITH_USER` / `ACTION: DO_NOT_INSTALL`, then the hosts by name, then each finding as file:line. On SUSPICIOUS, tell the user the finding; do not soften it.

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
