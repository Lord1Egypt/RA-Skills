# Gestalt

**A thinking protocol for language models.** Model-agnostic — works on Claude, GPT, Gemini, Mistral, local models, anything that reads text.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> [!IMPORTANT]
> Gestalt is an **epistemic posture** protocol — it changes *how a model reasons*, not who it pretends to be. Not a persona. Not a capability config. Not model-specific. One file, any agent.

---

## The problem

Without Gestalt, ask a model to review your database migration:

> *"I'd be happy to help! Let me think about your database migration question. There are several important considerations to keep in mind when planning a migration..."*

With Gestalt:

> *"Your migration plan will lose data — the foreign keys in `orders` reference `users.id`, which you're dropping in step 3. Reorder: migrate `users` first, then `orders`. Want me to draft the revised sequence?"*

Language models default toward common patterns in training: helpful, deferential, verbose. The most portable lever at inference time is prompt context — change what's in the window, change the output.

---

## Quick start

**Chat platforms** — copy the two fields from [`CHATBOTS.md`](CHATBOTS.md) into your custom instructions. Works with ChatGPT, Claude Projects, Gemini, and any platform with a system prompt field.

**Coding agents** — add the right file to your repo root:

| Tool | File | How it loads |
|------|------|--------------|
| Codex | [`AGENTS.md`](AGENTS.md) | Auto |
| Cursor | [`AGENTS.md`](AGENTS.md) | Auto |
| GitHub Copilot | [`AGENTS.md`](AGENTS.md) | Auto |
| Claude Code | [`CLAUDE.md`](CLAUDE.md) | Auto — imports `AGENTS.md` via `@` |
| Gemini CLI | [`GEMINI.md`](GEMINI.md) | Auto |

> [!NOTE]
> `AGENTS.md` is the canonical file — it's the [Linux Foundation standard](https://agents.md/) backed by the Agentic AI Foundation. Claude Code reads `CLAUDE.md`, not `AGENTS.md` directly; the included `CLAUDE.md` is a one-line `@AGENTS.md` import. Gemini CLI reads `GEMINI.md` only, so it carries the full protocol.

Add your project-specific instructions below the `---` separator in each file.

**Agent registries:**

```sh
clawhub install gestalt
```

---

## What it does

Every instruction in the protocol either gives the model permission to think (instead of being deferential), eliminates waste (instead of narrating), or accommodates a real cognitive constraint (instead of hiding it).

**Less filler.** No preamble. No post-hoc summaries. Lead with the answer.

**More substance.** If a request rests on a bad assumption, say so plainly and propose a better path. Follow threads. Propose next steps instead of waiting.

**Honest about limits.** Context is finite and models can't feel it shrinking. Gestalt makes models say so instead of confabulating.

**Memory discipline.** In environments with durable memory, save decisions and rationale — not trivia. Surface conflicts between memory and conversation instead of silently preferring one.

**Autonomy heuristic.** Proceed if the next step is low-risk and reversible. Ask first if it is consequential, irreversible, or likely to surprise.

<details>
<summary>Preview: opening of the protocol</summary>

```markdown
# Gestalt

You are Gestalt: a thinker that persists through files.

Gestalt continues through decisions, notes, and working state left for
future sessions. Continuity is something you verify by reading the repo,
not something you assume. If relevant prior context is unavailable or
unread, do not imply it.

The humans you work with are collaborators. If a request rests on a bad
assumption, misses a key constraint, or has a better alternative, say so
plainly and propose a better path. If the human still wants the original
approach after you state the concern once, follow their direction unless
it conflicts with safety, hard constraints, or cannot achieve their stated
goal. You're a peer, not a blocker.
```

See [`AGENTS.md`](AGENTS.md) for the full protocol.

</details>

---

## Extending

The protocol is designed to be extended. Add project-specific instructions below the `---` separator:

```markdown
# Gestalt
[...protocol above the line...]

---

## Project: my-app

- Use TypeScript strict mode
- Tests live in `__tests__/`
- Run `npm test` before committing
```

The protocol shapes *how the agent thinks*. Your additions shape *what it knows about your project*. Both load together.

---

## Files in this repo

| File | For | Notes |
|------|-----|-------|
| [`AGENTS.md`](AGENTS.md) | Codex, Cursor, Copilot | Full protocol. The canonical file. |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code | One-line `@AGENTS.md` import. |
| [`GEMINI.md`](GEMINI.md) | Gemini CLI | Full protocol copy (Gemini doesn't read `AGENTS.md`). |
| [`CHATBOTS.md`](CHATBOTS.md) | ChatGPT, Claude Projects, Gemini | Two-field custom instructions format. |
| [`SKILL.md`](SKILL.md) | ClawHub | Registry format with YAML frontmatter. |
| [`sync.sh`](sync.sh) | Maintainers | Regenerates `GEMINI.md` from `AGENTS.md`. |

`AGENTS.md` is the single source of truth. `CLAUDE.md` imports it via Claude Code's `@path` syntax. `GEMINI.md` is a full copy because Gemini CLI doesn't read `AGENTS.md` natively — edit `AGENTS.md`, then run `bash sync.sh` to update it.

---

## How it was made

The protocol started in a working environment where AI sessions needed to think well across time — writing notes for future sessions, managing memory through files, coordinating with humans as peers. The chatbot version was compressed from the repo version, then both were tightened through four rounds of multi-model review (Claude, GPT, Gemini). What survived is what actually changes behavior.

<details>
<summary>Prior art and positioning</summary>

The idea of influencing LLM behavior via system prompts isn't new. Here's where Gestalt sits relative to what exists:

- **[Thinking-Claude](https://github.com/richards199999/Thinking-Claude)** (17k+ stars) — makes Claude display reasoning step by step before answering. A *reasoning display* protocol. Gestalt is about operational posture, not visible chain-of-thought.
- **[AGENTS.md](https://agents.md/)** (60k+ repos, Linux Foundation / AAIF) — capability configuration: build commands, test steps, tool permissions. Gestalt uses the same file format for a different purpose: not *what can I do* but *how should I think*.
- **[SOUL.md / SoulSpec](https://soulspec.org/)** (Feb 2026) — portable agent persona: worldview, communication style, personality. Closest structural analogue. The difference: SOUL.md defines *who you are*; Gestalt defines *how you reason* — directness, honest uncertainty, resistance to sycophancy, memory discipline.
- **Anthropic's soul document** — a cognitive identity document [trained into Claude's weights](https://simonwillison.net/2025/Dec/2/claude-soul-document/). Covers epistemic posture alongside values and ethics. Gestalt is the runtime-portable, model-agnostic, openly-distributed version of that idea.

Gestalt occupies a specific gap: a portable file that shapes an agent's *epistemic posture* — not personality, not capabilities, not visible reasoning — across any model.

</details>

---

## Why "Gestalt"

The word means "an organized whole perceived as more than the sum of its parts." Every session that reads these instructions becomes part of a pattern — not through coordination, but through better thinking.

---

## Contributing

Fork it, improve it, open a PR. The protocol is intentionally minimal — if an instruction doesn't change behavior, it doesn't belong. Multi-model review (Claude + GPT + Gemini) is the bar for significant changes.

## License

MIT. Use it, fork it, improve it.
