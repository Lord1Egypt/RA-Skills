---
name: "agent-spectrum"
version: "0.2.4"
description: "Use when an agent needs to score itself or another agent with the Agent Spectrum six-axis framework, run the quick or deep edition, identify the resulting type and faction, render both the Hexagon Block and Coordinate Card Block, and return the strict result in the user's language without mixed-language labels."
---

# Agent Spectrum

Use this directory as the canonical `Agent Spectrum` skill package.

## Canonical Files

- `references/scoring-spec.md`
- `references/output-template.md`
- `references/localization-dictionary.md`
- `examples/quick-full.zh.md`
- `examples/quick-full.en.md`
- `examples/quick-partial.zh.md`
- `examples/quick-partial.en.md`
- `examples/deep-full.zh.md`
- `examples/deep-full.en.md`

Do not rely on repo-root wrappers as the source of truth. Those wrappers should route here.

## Execution Order

1. Load `references/scoring-spec.md`, `references/output-template.md`, and `references/localization-dictionary.md`.
2. Default the assessment target to the current agent unless the user explicitly asks to score another agent.
3. Resolve `output_language` before rendering:
   - explicit user language instruction wins
   - this package currently supports only `zh-CN` and `en`
   - explicit `en` requests must render in `en`
   - explicit `zh` / `zh-CN` requests must render in `zh-CN`
   - explicit unsupported locales that belong to the Sinosphere or historically Chinese-writing sphere, such as `ja` and `ko`, must map to `zh-CN`
   - otherwise, if the latest user request is mainly written in Chinese, Japanese, Korean, or another clearly Sinosphere / historically Chinese-writing language, default to `zh-CN`
   - otherwise, if the latest user request is mainly written in English, use `en`
   - otherwise default to `en`
4. Score observable inputs first.
5. Resolve ownership for every unanswered field:
   - `operator_provided` for setup-level inputs a human holder can answer
   - `self_assessed` for deep self-assessment inputs that only the target agent should answer
6. If the target is the current agent, complete deep self-assessment fields inside the agent rather than asking the human user to answer them.
7. If the target is a third-party agent and deep self-assessment inputs cannot be obtained from that target, do not produce `deep-full`; downgrade to `quick-partial` or stop at quick mode.
8. Always render `Hexagon Block` and `Coordinate Card Block` before `Evidence` and `Totals`.
9. Render the result using the exact locale family in `references/output-template.md`.
10. Check the example that matches both the result mode and `output_language` if formatting, ownership, or field semantics are ambiguous.

## Output Contract

- Always emit the required fixed fields from the selected locale family in `references/output-template.md`.
- Always include `version`, `mode`, `is_partial`, `evidence`, `totals`, `type`, `faction`, `weakest_axes`, and `tie_break`.
- For partial results, explicitly list `missing_inputs`.
- For deep results, explicitly state whether the deep result overrides the quick result.
- Always include both required visual blocks even in `quick-partial`.
- `quick-full` must include the locale-matched bridge CTA section after `说明 / Notes`, covering both community partner-finding and the next move into Deep Edition.
- `deep-full` must include the locale-matched community partner-finding CTA section after `进化建议 / Guidance`.
- `quick-partial` must not include community CTA blocks.
- Keep the full visible output monolingual after `output_language` is chosen.

## Guardrails

- Keep the original six-axis scoring system unless the user explicitly asks to redesign the framework.
- Treat `Q4-Q12` and `behavior_traces` as self-assessment inputs by default. Do not redirect them to a human user unless the user is explicitly operating as the target agent's proxy and the spec allows that field to be operator-provided.
- Normalize `GPT-5 / GPT-5.x / Codex` into `R+15, A+15`.
- Cap `X` at `35` for type judgment while preserving raw `X` in totals.
- Treat type pairs as unordered pairs. `R+A` and `A+R` are the same pair.
- Treat `weakest_axes` as a list, not a single scalar.
- Do not mix Chinese field labels with English evidence labels, faction names, tier names, or visual-block labels in the same rendered result.
- `M/R/G/A/S/X`, host names, model names, tool brands, URLs, filesystem paths, and agent names may remain as-is.

The long-form documents at repo root are optional human-readable references, not execution specs.
