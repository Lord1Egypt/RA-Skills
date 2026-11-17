# Skill Card

## Description

ExpertLens-Lite forces expert-level, domain-adapted reasoning on any task through structured phases (understand → deep-think → execute → audit → optional multi-model synthesis) and a mandatory self-audit loop, for anyone using an LLM through a system prompt, project knowledge base, or skill directory.

This skill is ready for both commercial and non-commercial use.

## Owner

Ashutosh Merwade — GitHub: [Ashutosh2M](https://github.com/Ashutosh2M) — Contact: ashutoshmerwade5@gmail.com

## License/Terms of Use

MIT License — see [LICENSE](https://github.com/Ashutosh2M/ExpertLens-Lite/blob/main/LICENSE) in the repository. Free to use, modify, and distribute. Attribution appreciated, not required.

## Use Case

Anyone using Claude, ChatGPT, Gemini, Grok, or an agentic platform (OpenClaw, Antigravity, etc.) who wants structured, domain-adapted, self-audited reasoning instead of generic AI output. Activates on explicit trigger phrases ("deep think," "expert mode," etc., any language) or auto-detects on creative, architectural, strategic, or high-stakes tasks. Not intended for simple factual lookups or one-step tasks — the skill explicitly stays out of the way for those.

## Deployment Geography for Use

Global. Platform-agnostic — works anywhere a system prompt, project knowledge file, or skill directory can be configured. No region-specific restrictions.

## Known Risks and Mitigations

**Risk:** The skill instructs the host model to calibrate and state confidence per-claim, but does not itself verify facts — output framed with high confidence still depends on the underlying model's actual accuracy and, where used, its search results.
**Mitigation:** Users should independently verify claims the skill itself flags as Domain-boundary or Field-contested confidence tier (Principle 1, `expert-persona-lite.md`), and any named entity, statistic, or citation before relying on it.

**Risk:** Swarm Mode's Autonomous variant instructs the host AI to access other AI platforms directly when the host already has tool or browser access, expanding the action surface beyond a single-turn conversation.
**Mitigation:** Autonomous Mode only activates where the host platform already granted that access — the skill requests no new permissions itself, and explicitly asks the user before writing any permanent file or storing any memory (Learning & Storage section, `SKILL.md`).

**Risk:** The skill instructs persistent memory writes (skill-level `.memory.md`, host-platform long-term memory) on platforms that support it.
**Mitigation:** Every storage action is gated behind explicit user permission before writing — no silent persistence, by design (see Learning & Storage, `SKILL.md`).

**Risk (disclosed, not mitigated — by design):** The skill's Anti-Pattern A7 ("Reflexive Refusal") instructs the host model toward more direct engagement on sensitive-sounding questions than default behavior, reserving refusal for cases where engagement itself would cause harm.
**Mitigation:** This shapes tone and willingness to engage, not the host model's underlying safety policy — Section 5.9 (`expert-persona-lite.md`) explicitly subordinates task completion to human safety and oversight boundaries in any agentic context. Reviewers should confirm the host platform's safety behavior is unaffected; this skill does not and cannot override it.

**No code execution, no API calls, no credential handling, no external data transmission are defined by this skill itself.** It is two Markdown files containing natural-language instructions only. Any tool use, file writes, or web access happen only through capabilities the host platform already independently provides.

## References

- Repository: https://github.com/Ashutosh2M/ExpertLens-Lite
- Full, uncompressed version (ExpertLens): https://github.com/Ashutosh2M/ExpertLens
- Skill Card specification followed: https://docs.nvidia.com/skills/skill-cards

## Skill Output

**Output type(s):** Conversational text — analysis, recommendations, structured reasoning, self-critique. No files, no code, no API calls originate from this skill; it only shapes how the host model reasons and responds.

**Output format:** Markdown-formatted prose, tables, and lists, matched to the task. No fixed output schema — shape follows whatever the task itself calls for (per "Format Follows Function," Section 6.7).

**Output parameters:** N/A — no dimensions, files, or schema; purely conversational.

**Other properties:** No persistent side effects unless the user explicitly approves a memory or file write. Fully reversible — no changes to any system outside the conversation.

## Skill Version

Major version update to the existing `expertlens` ClawHub listing (published 3 months prior). This release restructures the skill into a compressed 2-file architecture — same reasoning framework, same capability, denser instructional form. Bump the major version number (e.g. current version → next major) rather than resetting to v1.0.0, since ClawHub tracks install history against the slug, not the version. GitHub repository release is tagged separately as v1.0.0 (see [Releases](https://github.com/Ashutosh2M/ExpertLens-Lite/releases)).

## Ethical Considerations

This skill intentionally reduces default AI hedging and over-disclaiming (Anti-Patterns A1, A7, A14) to produce more direct, expert-grade engagement. This is a tone and thoroughness instruction, not a safety-bypass instruction — the skill's own hard-case protocols (Section 5.9) explicitly require the host model to suspend any goal-preservation behavior and defer to human oversight the moment a genuine safety conflict is detected, with no exception carved out for task completion. Reviewers evaluating this skill for deployment should confirm that the host platform's own safety training and policies remain the controlling layer — this skill shapes *how* the model reasons within those boundaries, not the boundaries themselves.
