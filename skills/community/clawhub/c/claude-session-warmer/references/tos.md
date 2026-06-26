# Is this allowed? — the terms-of-service position

Short version: **yes, when the primer is sent through the official `claude` CLI that is
installed and logged in on your own box, on your own Pro/Max subscription** — and only
then. This file explains why, and exactly where the lines are.

## The controlling clause

Anthropic's **Consumer Terms of Service, Section 3** lists prohibited uses. Item 7
prohibits accessing the Services

> "through automated or non-human means, whether through a bot, script, or otherwise"

**except** — same sentence —

> "when you are accessing our Services via an Anthropic API Key **or where we
> otherwise explicitly permit it.**"

## Why the official CLI is covered

The **Claude Code CLI is Anthropic's own official product, explicitly built and
documented for scripted, piped, and scheduled use.** Anthropic's docs show pipelines like
`tail -f app.log | claude -p "..."` and ship a GitHub Action that runs Claude Code
unattended on cron. A scheduled `claude -p "<tiny primer>"` is exactly that pattern, so
item 7's automation prohibition does **not** catch it.

Running the CLI on a **VPS** is also fine — none of the Consumer Terms, Commercial Terms,
or Acceptable Use Policy restrict *where* you run the official CLI. The clean requirement
is simply that the box is **logged in via the official flow** (run `claude` interactively
once, or use `claude setup-token`), not authenticated by copying credentials from
elsewhere.

## What Anthropic actually enforces against (and this skill never does)

The Jan–Feb 2026 enforcement wave that blocked OpenClaw, OpenCode, Roo Code, Goose, etc.
was about a **completely different behaviour**: third-party harnesses that **extracted
OAuth tokens from a subscription and spoofed the Claude Code client** to get subscription
pricing inside their own API clients. That is token theft / client impersonation — the
opposite of calling the real CLI.

claude-session-warmer must therefore **never**:
- extract, copy, or transfer Claude OAuth tokens between machines,
- spoof or impersonate the Claude Code client,
- route the primer through the **Agent SDK with subscription OAuth** (the Feb 2026 legal
  docs require an **API key** there),
- run through any third-party harness.

It only ever shells out to the genuine `claude` binary already installed and logged in on
the box. That is the entire safety argument — keep it true. (This is also why "just copy
my Mac's token to the VPS" is **not** how you set this up — that crosses into the
prohibited token-transfer territory. Log in on the VPS itself.)

## Two soft caveats (interpretive, honest)

1. **"Ordinary, individual usage."** Anthropic's Feb 2026 legal docs state subscription
   limits assume *"ordinary, individual usage."* A primer whose only purpose is to
   position the window pushes against the *spirit* of that phrase, though it breaks no
   specific rule. Crucially **it never exceeds quota** — you can't beat the 5-hour or
   weekly cap; you only shift *when* the window opens. Keep it single-user and low-volume
   (one trivial prompt per primer; ~4 tiny prompts/day) so "ordinary, individual" stays
   accurate. (Those few prompts draw a negligible amount of the weekly cap.)

2. **Framing optics.** A tool *marketed* as "bypass / beat / hack your Claude limits"
   reads far worse than the same code described as "align your usage window to your
   working hours" — which is the accurate description, because nothing is bypassed. Always
   use the accurate framing. The README and SKILL.md do.

## The API-key dead end (why we use the subscription path on purpose)

You might think "use an API key to be safe." But the **API has its own separate quota and
does not share the subscription's 5-hour window** — so an API call cannot prime the
subscription window at all. The only mechanism that warms the subscription window is the
subscription-authenticated CLI, which is also the ToS-exempt one. The facts line up.

## Bottom line

- ✅ Permitted: scheduled `claude -p` primer, official CLI, your box, logged in on that box.
- ❌ Not this skill: token extraction/transfer, client spoofing, Agent-SDK-with-OAuth,
  third-party harnesses, shared accounts.
- ⚠️ Keep honest: single-user, low-volume, framed as window *alignment* not bypass.

Not legal advice; terms change. If publishing, link the current
[Anthropic Consumer Terms](https://www.anthropic.com/legal/consumer-terms) and
[Claude Code Legal & Compliance](https://code.claude.com/docs/en/legal-and-compliance)
and let installers read them.
