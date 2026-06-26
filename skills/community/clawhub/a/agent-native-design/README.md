# Design CLIs that AI agents can actually use

![One CLI · Three Audiences · Three Channels](docs/assets/concept-hero-en.png)

[中文文档](README_CN.md) · [Docs site](https://agents365-ai.github.io/agent-native-design/)

## What it does

- Evaluates whether an existing CLI is reliably usable by AI agents
- Designs CLI interfaces that serve humans, agents, and orchestration systems simultaneously
- Converts REST APIs and SDKs into agent-native CLI command trees
- Reviews stdout contracts, exit code semantics, and error envelope design
- Designs schema-driven self-description, dry-run previews, and schema introspection
- Defines safety tiers (open / warned / hidden) for graduated command visibility
- Designs delegated authentication so agents never own the auth lifecycle
- Produces prioritized refactor plans with concrete interface examples

## Multi-Platform Support

The core `SKILL.md` is portable, and this repository includes metadata for the platforms listed below:

| Platform | Status | Details |
|----------|--------|---------|
| **Claude Code** | ✅ Full support | Native SKILL.md format |
| **OpenClaw / ClawHub** | ✅ Full support | `metadata.openclaw` namespace |
| **Hermes Agent** | ✅ Full support | `metadata.hermes` namespace, category: engineering |
| **[pi-mono](https://github.com/badlogic/pi-mono)** | ✅ Full support | `metadata.pimo` namespace |
| **OpenAI Codex** | ✅ Full support | `agents/openai.yaml` sidecar |
| **SkillsMP** | ✅ Indexed | GitHub topics configured |

## Comparison: with vs. without this skill

| Capability | Native agent | This skill |
|------------|-------------|------------|
| Evaluate whether a CLI is agent-native | No | Yes — structured diagnosis across 7 principles |
| Design stdout JSON contract | Inconsistent | Always — stable envelope with `ok`, `data`, `error` |
| Define exit code semantics | Ad hoc | Yes — documented, deterministic per failure class |
| Design layered `--help` and schema introspection | No | Yes — full self-description pattern |
| Design dry-run previews | Rarely | Always — request shape preview without execution |
| Define safety tiers for commands | No | Yes — open / warned / hidden tiers |
| Design delegated authentication | No | Yes — human manages auth lifecycle; agent uses token |
| Separate trust levels for env vs. CLI args | No | Yes — directional trust model |
| Produce prioritized refactor plan | Rarely | Always — P0 / P1 / P2 with examples |
| Score CLI across 14-criterion rubric | No | Yes — 0–2 per criterion with verdict |

## When to use

- Evaluating whether an existing CLI is usable by an AI agent
- Designing a new CLI interface for an API or SDK
- Refactoring a human-first CLI to be machine-readable
- Reviewing stdout, stderr, and exit code contract design
- Defining dry-run, schema introspection, and self-description layers
- Designing auth delegation and trust boundaries for agent safety
- Producing a SKILL.md or skill docs from a CLI schema

## Skill Installation

### Quick install — ask any agent

The simplest install is to ask any code-capable agent (Claude Code, Codex, Cursor, Aider, Gemini CLI, …) to clone the repo into your platform's skills directory. Just hand it the URL and the destination path:

```
Clone https://github.com/Agents365-ai/agent-native-design into ~/.claude/skills/agent-native-design for me.
```

Substitute the destination for your platform — see the **Installation paths summary** table at the end of this section. Because the prompt names the exact path, this works for any agent regardless of whether it has built-in knowledge of skills conventions. For environments without an agent handy (CI, fresh machines, headless scripts), use the per-platform `git clone` commands in the sub-sections that follow.

### Claude Code

```bash
# Global install (available in all projects)
git clone https://github.com/Agents365-ai/agent-native-design.git ~/.claude/skills/agent-native-design

# Project-level install
git clone https://github.com/Agents365-ai/agent-native-design.git .claude/skills/agent-native-design
```

### OpenClaw / ClawHub

```bash
# Via ClawHub
clawhub install agent-native-design

# Manual install
git clone https://github.com/Agents365-ai/agent-native-design.git ~/.openclaw/skills/agent-native-design

# Project-level install
git clone https://github.com/Agents365-ai/agent-native-design.git skills/agent-native-design
```

### Hermes Agent

```bash
git clone https://github.com/Agents365-ai/agent-native-design.git ~/.hermes/skills/engineering/agent-native-design
```

Or add to `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/myskills/agent-native-design
```

### pi-mono

```bash
git clone https://github.com/Agents365-ai/agent-native-design.git ~/.pimo/skills/agent-native-design
```

### OpenAI Codex

```bash
# User-level install (default CODEX_HOME)
git clone https://github.com/Agents365-ai/agent-native-design.git ~/.codex/skills/agent-native-design

# Project-level install
git clone https://github.com/Agents365-ai/agent-native-design.git .codex/skills/agent-native-design
```

### SkillsMP

```bash
skills install agent-native-design
```

### Installation paths summary

| Platform | Global path | Project path |
|----------|-------------|--------------|
| Claude Code | `~/.claude/skills/agent-native-design/` | `.claude/skills/agent-native-design/` |
| OpenClaw | `~/.openclaw/skills/agent-native-design/` | `skills/agent-native-design/` |
| Hermes Agent | `~/.hermes/skills/engineering/agent-native-design/` | Via `external_dirs` config |
| pi-mono | `~/.pimo/skills/agent-native-design/` | — |
| OpenAI Codex | `~/.codex/skills/agent-native-design/` | `.codex/skills/agent-native-design/` |

## License

MIT

## Changelog

### v1.3.3 — May 5, 2026

**Replaced Step 0 silent auto-pull with a notify-only update check.**

On review, the v1.3.2 silent `git pull` proved inconsistent with this skill's own *Principle 2 (trust is directional)* and *Principle 7 (auth/lifecycle is delegated to the human, not owned by the agent)*. The new Step 0:

- **Throttles to one check per 24 h per installation** (was: every fresh conversation)
- **Notifies and asks** — surfaces the actual version delta (`vX.Y.Z → vA.B.C`) and pulls only with explicit user consent
- Same silent fallback for non-git-checkout installs (ClawHub copy, read-only paths)
- Removes the supply-chain attack surface where a compromised upstream could be silently fetched into every installation on the next conversation

If you upgraded to v1.3.2, this is the right reason to upgrade once more.

### v1.3.2 — May 5, 2026

**Auto-update step.** Added `Step 0` to the standard review workflow: on first use per conversation, the model checks `.last_update` and runs `git pull --ff-only` if older than 24 h, silently. Failure modes (offline, conflict, not a git checkout — e.g. ClawHub-installed copy) are ignored. Frees git-clone users from depending on whether the host runtime auto-pulls skills, and works identically across Claude Code / OpenClaw / Hermes / pi-mono / Codex.

### v1.3.1 — May 5, 2026

**Content depth + visual identity.**

- New `references/testing.md` (~235 lines): for every design pattern in `references/design-patterns.md`, a corresponding test recipe — envelope contracts, stdout/stderr separation, exit codes, idempotency replay, TTY behavior, schema drift, dry-run safety, auth delegation, locale determinism, streaming. Closes the "skill teaches how to design but not how to verify" gap.
- Bilingual concept hero image (`docs/assets/concept-hero-{en,zh}.png`) embedded in both READMEs and both landing pages — one visual carrying the "one CLI · three audiences · three channels" mental model.
- Title cleanup in both READMEs (dropped doubled "design", redundant "Skill" suffix, and the redundant repo-name prefix); landing pages re-synced to current name and version.
- `.claude/` is now gitignored.

### v1.3.0 — May 5, 2026

**Structural cleanup** — same content, leaner SKILL.md, on-demand reference loading.

- Split SKILL.md (919 → 237 lines) into a lean core plus `references/` (examples, rubric, checklists, design patterns, hybrid CLI/MCP discussion, citations). Reference files load only when needed, mirroring the progressive-disclosure pattern this skill teaches.
- Deduplicated overlapping discussion: hybrid CLI+MCP and schema versioning each have one detailed home now, with brief pointers elsewhere.
- Verified all citations against their primary sources; corrected two metadata errors (Manveer Chawla, not "Chugh"; Ugo Enyioha's piece is Feb 2025, not Feb 2026).
- Moved one-time review artifacts (`REVIEW_2026.md`, `IMPROVEMENTS_APPLIED.md`) into `docs/maintainers/` so they no longer appear at the repo root.

### [v1.2.0](https://github.com/Agents365-ai/agent-native-design/releases/tag/v1.2.0) — April 26, 2026

**2026 Research Update** — Aligned with latest agent-CLI design patterns and benchmarks.

**New Content:**
- Added hybrid MCP-CLI decision framework with decision matrix (3 scenarios for each pattern)
- Strengthened Principle 6 with schema versioning in response envelopes and deprecation signals
- Added Example 8: Schema versioning with drift detection for agent caching scenarios
- Quantified anti-pattern: eager schema dumps (55K tokens per 10 invocations)
- Added token efficiency checklist (6 items for evaluating CLI context cost)

**Research Alignment:**
- Cite 2026 benchmarks: CLI achieves 28% higher task completion, 33% token efficiency vs. MCP-only
- Added 4 new references: Reinhardt, Chugh, RudderStack on hybrid patterns (2026)
- Validated all 7 principles through April 2026 production deployments

**Recommendation:** This version reflects the consensus that large production agents (Claude Code, Cursor, Gemini CLI) use both CLI (for local/scriptable tasks) and MCP (for multi-tenant SaaS). Skill remains fundamentally sound; no principles required rewriting.

### v1.1.0 — Early 2026

Initial version with seven principles, 14-criterion rubric, and examples.

---

## Support

If this skill helps your work, consider supporting the author:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="WeChat Pay">
      <br>
      <b>WeChat Pay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="Alipay">
      <br>
      <b>Alipay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/awarding/award.gif" width="180" alt="Give a Reward">
      <br>
      <b>Give a Reward</b>
    </td>
  </tr>
</table>

## Author

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
