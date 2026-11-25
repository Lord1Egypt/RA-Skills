# delegate-to-codex

A Claude Code skill for handing repository work to [Codex CLI](https://developers.openai.com/codex/cli).

Claude stays the orchestrator. It picks the task, writes the handoff, reviews the diff, and owns every commit. Codex reads the repo, writes the code, and runs the tests. The skill is the procedure for that split, including the parts that are easy to get wrong.

The handoff prompt and whatever repository content the agent reads are sent to the model provider your Codex config points at, usually OpenAI, and runs count against your account. Do not delegate a repository you would not share with that provider.

## Why this exists

Delegation fails quietly. An agent exits 0, prints a confident summary, and the summary is a claim rather than evidence. Worse, it can hand back a green test suite whose new cases were written against the code it just wrote, so they pass by construction. One real defect survived a fully green suite because every test fed the function an already-sorted list.

Most of this file is about closing that gap. Name the fragile invariants before you send. Check three signals before you read anything. Re-run the tests yourself, and read the new cases for the input the implementation does not handle, and for the ones that prime by hand the state the real wiring should produce.

## Install

```bash
git clone https://github.com/troioi-vn/codex-skill.git ~/.claude/skills/delegate-to-codex
```

Claude loads it when you ask for work to go to Codex. It will not reach for it on its own, which is deliberate: work Claude could do directly, it should do directly.

You need the `codex` CLI on your PATH and logged in.

## What it covers

Choosing the model and reasoning effort: `gpt-6.2-sol` at `medium` by default, `low` for easier tasks, `gpt-6-astra` only for creative or really hard work, `high` only with the user's say-so. Setting up the workspace and snapshotting Git. Writing the handoff prompt, with a template. Running `codex exec` and confirming it really ran. Reviewing the diff without trusting the summary. Committing.

## Things that bite

**A CLI argument error looks exactly like success.** Exit 2, empty stdout, no `-o` file, and an unchanged worktree read the same as "ran and decided to change nothing." The usual cause is an option placed after a subcommand. Options belong to `codex exec`, so they go before `resume`.

**Never append `; echo "EXIT=$?"` to the invocation, and do not read a pipeline's exit code.** The trailing command's own success becomes the exit status, so a failed run reports as 0. `pnpm test | tail` has the same problem and is easier to type. Read the runner's summary line instead.

**Do not `cat` stderr.** Codex echoes the entire prompt to stderr before it starts, then everything it reads and thinks after that. Tens of kilobytes on a routine task. Use `tail -c 2000` and read the `-o` file for the result.

**`--approve-for-me` cannot be combined with `--sandbox`.** It already implies the workspace-write sandbox, and passing both fails argument parsing before any work happens.

## Version

Written against codex-cli 0.147.0. Flags move between releases. If one is rejected, read `codex exec --help` rather than guessing at a replacement safety flag.

## Related

[muse-skill](https://github.com/troioi-vn/muse-skill) is the same idea for Meta's Muse Code. The two share a lot of prompt-writing and review advice and differ on invocation, models, and failure modes.
