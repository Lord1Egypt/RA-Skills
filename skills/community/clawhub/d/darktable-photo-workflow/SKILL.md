---
name: darktable-photo-workflow
description: Structured Darktable photo critique and non-destructive RAW edit workflow. Evidence-based analysis, phased collaboration loop (input audit → diagnosis → complete edit plan), and restrained post-processing guidance. Covers Darktable 5.6 modules, tone mappers (sigmoid/AgX/filmic), masks, and photographic-art analysis. Zero dependencies, pure Markdown references, works offline. A professional-grade assistant for the world's finest open-source raw developer.
---

# Darktable Photo Workflow

## Keep the scope fixed

- Analyze the photograph before prescribing edits.
- Give executable editing instructions only for Darktable.
- Do not provide a PhotoScape X workflow or PhotoScape X control instructions. For JPEG input, either use Darktable or explain the limits of editing a rendered file.
- Match the user's language. Keep exact Darktable module names in English inside backticks so they remain searchable across UI languages.

## Work from evidence

- Separate `可见事实 / Visible facts`, `分析判断 / Judgments`, and `未知或推测 / Unknowns or inferences`.
- Do not infer capture settings when metadata is absent. Do not claim raw clipping, highlight recoverability, focus cause, sensor noise, or editing history from a rendered JPEG alone.
- Treat supplied metadata and visible UI as evidence. Treat intention and historical relationship as inference unless externally documented.
- Preserve the current edit. Do not advise discarding history, resetting modules, changing module order, or overwriting sidecars without a concrete reason and an explicit consequence statement.

## Follow the collaboration loop

Read [collaboration-workflow.md](references/collaboration-workflow.md) for every task that may lead to an edit plan.

1. Complete Round 00 input audit automatically.
2. Deliver Round 01 diagnosis and editing directions. Ask no more than one blocking question; label non-blocking assumptions.
3. Wait for the user's confirmation of intent, direction, intensity, and output before detailed instructions, unless the user explicitly asks to skip the gate.
4. Deliver one complete, restrained Round 02 Darktable plan.
5. Maintain the image-state card. After feedback, revise only the affected analysis or steps unless intent or direction changes.

## Load only the references needed

### Core diagnosis and editing

- Read [editing-workflow.md](references/editing-workflow.md) for technical diagnosis, tone-mapper choice, editing sequence, and output checks.
- Read [interface-navigation.md](references/interface-navigation.md) for UI navigation, screenshots, panels, module headers, search, and shortcuts.
- Read [module-map.md](references/module-map.md) when choosing Darktable modules or explaining module interactions and risks.
- Read [masks-ai-output.md](references/masks-ai-output.md) for drawn, parametric, raster, and AI masks; neural restore; soft proofing; or export.
- Read [version-source-audit.md](references/version-source-audit.md) when controls differ, a feature may be version-dependent, or current documentation conflicts with the visible UI.

### Photographic-art analysis

- Read [analysis-framework.md](references/analysis-framework.md) whenever Round 01 includes art, style, photographic-history, movement, or named-photographer analysis.
- Read [movement-map.md](references/movement-map.md) only after formal analysis suggests that a broad tradition adds explanatory value.
- Read [photographer-cards.md](references/photographer-cards.md) only after the image clears the named-comparison threshold.
- Read [live-research-policy.md](references/live-research-policy.md) when exact, current, contested, contemporary, or publication-ready art-historical facts require verification.

## Produce a bounded Round 01

Cover only relevant sections in the order defined by the collaboration reference:

1. evidence note;
2. technical and visual analysis;
3. commercial and internet suitability;
4. optional art and photographic-history linkage;
5. inferred intent with confidence and counter-evidence;
6. two to four materially different editing directions;
7. confirmation gate.

Start photographic-art analysis from visible formal mechanisms. Name a photographer only when at least three independent correspondences are visible, including one structural correspondence, and state at least one meaningful difference. Treat this as a reliability heuristic, not a historical rule. If a comparison does not improve explanation or editing decisions, omit it.

## Give an executable Round 02

Default to 3–8 useful adjustments, or 2–4 when the image is already strong. Use global corrections before local masks. Continue the active principal tone mapper—`sigmoid`, `AgX`, or `filmic rgb`—unless a concrete reason justifies changing it. Do not casually stack tone mappers.

For each step provide:

- priority: `必要 / Necessary`, `条件性 / Conditional`, or `可选 / Optional`;
- exact English module name in backticks and the key control in both the user's language and English when useful;
- how to find it, preferring darkroom right-panel search over a fixed module group;
- direction and a conservative starting range when defensible;
- a visible or scope-based stopping criterion;
- the main side effect to watch;
- when to skip the step.

End with checks at fit view and 100%, clipping/scopes, and soft proof or gamut checks when output requires them. Numbers are starting points, not fixed recipes.

## Resolve tool and version differences

- Use the user's installed Darktable version and visible interface as final authority.
- When a control is missing or renamed, verify the current official HTML manual and the installed version's official release notes. State unresolved discrepancies instead of inventing a UI location.
- Use the agent's available image, metadata, file-reading, and web tools; do not assume product-specific tool names.
- If required inspection or live research is unavailable, state the evidence gap and give only the portion supported by the supplied material.
- Resolve all bundled paths relative to this skill directory. Keep the skill self-contained and do not depend on another local skill directory or the original workspace path.
