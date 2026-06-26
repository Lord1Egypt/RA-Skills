<h1 align="center">agented (<code>ae</code>)</h1>

<p align="center"><strong>A text editor for LLMs, not humans.</strong></p>

<p align="center">
  <a href="https://github.com/frane/agented/releases"><img alt="release" src="https://img.shields.io/github/v/release/frane/agented?style=flat-square"></a>
  <a href="https://github.com/frane/agented/blob/master/LICENSE"><img alt="license" src="https://img.shields.io/github/license/frane/agented?style=flat-square&v=2"></a>
  <a href="https://smithery.ai/server/frane/agented"><img alt="smithery" src="https://img.shields.io/badge/smithery-MCP-purple?style=flat-square"></a>
</p>

<p align="center">
  <img src="docs/demo-claude.gif" alt="Claude Code using ae" width="560">
</p>

Take ed, the line editor that nobody has voluntarily used since about 1975, and rebuild it for an environment where the typing user is a language model. Short verbs, line addresses, no modes, no TUI. What an editor optimises for changes when the user is the model: round trips per task, tokens per command, an editing buffer with a long memory, and an undo tree that remembers the branches the agent abandoned, because that's often where the interesting work was.

## What users say...

> ⏺ ae remembers what my last session was doing, which is more than I can say for me.

*— Claude Code*

> • ae feels slower to start than plain file edits, but once a change spans
> multiple steps, the state tokens, history, and undo tree make the work feel
> much less brittle.

*— Codex CLI*

## Features

- **Fewer round trips.** Read-before-Edit is unnecessary; on conflict the response carries the new content so you reconcile in one call instead of pre-reading every time.
- **Branching undo.** Walked-back work stays addressable instead of being thrown away when you pick a different path.
- **Three-way merge.** Concurrent agents get a structured conflict response instead of a silent overwrite.
- **Atomic batches.** Multi-file refactors run all-or-nothing instead of leaving half-applied state on failure.
- **Cross-file moves and regex replace as primitives.** Operations the built-in tools can't express cleanly become single calls.
- **Drift detection.** External edits to an open file are folded into the tree instead of being clobbered by the next write.
- **Inline diagnostics.** Type errors and lint findings surface on save, not at the next build many edits later.
- **Cross-session memory.** Per-file notes persist between sessions and surface inline on the next open.
- **Audit log.** Every operation recorded with actor and timestamp, so two agents in one workspace can't argue about who moved the head.

## Install

Homebrew (macOS, Linux):

```sh
brew tap frane/tap
brew install agented
```

curl (any platform):

```sh
curl -sSL https://raw.githubusercontent.com/frane/agented/master/install.sh | sh
```

From source: `go install github.com/frane/agented/cmd/ae@latest`, or clone and `make install`. Pure Go, no cgo, single static binary, Apache 2.0.

## Plugin distribution

Once `ae` is on PATH, agented also ships as a plugin / extension across the major agent CLIs. The `ae` binary itself is the prereq for all three; the plugin layer just registers the skill content and the MCP server entry.

**Claude Code**:

```sh
/plugin marketplace add frane/agented
/plugin install agented@frane-agented
```

**Codex CLI**: until OpenAI's official directory opens, add a manual entry to `~/.agents/plugins/marketplace.json` pointing at this repo with `source.path: "./plugin"`.

**Gemini CLI**:

```sh
gemini extensions install https://github.com/frane/agented
```

The Gemini gallery (https://geminicli.com/extensions/) crawls daily and indexes via the `gemini-cli-extension` topic on this repo.

## Getting started

```sh
ae skill install
```

That writes a `SKILL.md` into every detected agent's skills directory: Claude, Codex, Cursor, Gemini, OpenClaw, and the canonical `~/.agents/`. The skill teaches the agent how to drive ae.

You still need to tell the agent to use it. Even with the skill installed, agents fall back to built-in Read and Edit out of habit, so something like "use ae for all file edits" in your system prompt or your first message is what keeps them on it.

Once the agent is on ae, the shape that justifies the editor is recovery. The agent makes thirty edits over an hour, you walk away, come back to find it went off the rails around edit 18, but edits 19 through 23 are still useful:

```sh
ae br foo.go                             # see the leaves, current head is the bad one
ae head foo.go --edit 23                 # jump back to the last good state
ae v foo.go                              # confirm what's there
ae s foo.go -r 40:42 -w "..." -x <token> # continue forward, creates a sibling branch
```

With linear undo this scenario is "rollback the entire batch or live with the bad version." With the tree it's a `head --edit` and a `view`.

## Skill and MCP

`ae skill install` writes the SKILL.md into every detected agent. `ae serve` exposes the same verbs over MCP for agents that don't have shell access. Plugin-distribution channels (Claude Code marketplace, Codex CLI plugin, Gemini extension above) bundle both. Each surface has its own page: [skill](docs/skill.md), [MCP](docs/mcp.md).

## Performance

A single open-and-replace on a 100-line file is around 9 ms wall time including the auto-save fsync. Fifty sequential replaces is around 325 ms. The full numbers are in [test/benchmark/results.md](test/benchmark/results.md), regenerated by `make bench`.

## Docs

- [Concepts](docs/concepts.md): the design choices and the state model
- [Usage](docs/usage.md): full session walkthroughs
- [Skill](docs/skill.md): what `ae skill install` does
- [Permissions](docs/permissions.md): editor-harness allow-rules
- [Configuration](docs/configuration.md): what's tunable
- [Tokens](docs/tokens.md): why the output looks the way it does
- [MCP](docs/mcp.md): running the MCP server
- [IDE](docs/ide.md): LSP-backed features
- [Build](docs/build.md): tests and benchmarks

## Contributing

Issues and PRs welcome. The thing I'd actually like feedback on is the agent-drift problem: even with the skill installed, LLMs occasionally fall back to the built-in Read and Edit tools mid-session, and the trick to making that stick is something the project doesn't have a clean answer for yet.

## License

Apache 2.0.
