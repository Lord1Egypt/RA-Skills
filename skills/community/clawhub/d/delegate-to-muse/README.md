# delegate-to-muse

A Claude Code skill for handing repository work to [Muse Code](https://developer.meta.com/ai/products/muse-code/), Meta's terminal coding agent.

Claude stays the orchestrator. It picks the task, writes the handoff, reviews the diff, and owns every commit. Muse reads the repo, writes the code, and runs the tests. The skill is the procedure for that split, including the parts that are easy to get wrong.

The handoff prompt and whatever repository content the agent reads are sent to Meta's model service, and runs count against your account. Do not delegate a repository you would not share with that provider.

## Why this exists

Delegation fails quietly. An agent exits 0, prints a confident summary, and the summary is a claim rather than evidence. Worse, it can hand back a green test suite whose new cases were written against the code it just wrote, so they pass by construction.

Most of this file is about closing that gap. Name the fragile invariants before you send. Check three signals before you read anything. Re-run the tests yourself. Delete the feature and confirm the new tests actually go red.

## Install

```bash
git clone https://github.com/troioi-vn/muse-skill.git ~/.claude/skills/delegate-to-muse
```

Claude loads it when you ask for work to go to Muse. It will not reach for it on its own, which is deliberate: work Claude could do directly, it should do directly.

You need the `muse` CLI on your PATH and logged in.

## What it covers

Choosing a model and reasoning effort. Setting up the workspace and snapshotting Git. Writing the handoff prompt, with a template. Running `muse exec` and confirming it really ran. Reviewing the diff without trusting the summary. Committing.

## Things that bite

Three differences from other agent CLIs, each of which has cost a round trip:

**Workspace trust gates your project rules.** Muse reads a repo's `AGENTS.md` only if the workspace is trusted. An untrusted run still edits files and still reports confidently, having never seen your instructions. It does warn on stderr, and stderr is small enough to read in full, so read it.

**There is no `-o` flag.** Stdout is the result. Redirect it or lose it.

**There is no `-C` flag.** Set the working directory with your shell.

One nice surprise: you pick the session UUID yourself with `uuidgen` and pass `--session-id`, so a correction round trip needs no parsing of session ids out of the output.

## Version

Invocation checked with Muse Code 1.4.7. The current default is `muse-wonder-1.0` at medium reasoning effort. Flags move between releases. If one is rejected, read `muse exec --help` rather than guessing at a replacement safety flag.

## Related

[codex-skill](https://github.com/troioi-vn/codex-skill) is the same idea for Codex CLI. The two share a lot of prompt-writing and review advice and differ on invocation, models, and failure modes.
