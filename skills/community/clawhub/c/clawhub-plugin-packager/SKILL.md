---
name: clawhub-plugin-packager
description: "Generate, repair, or audit publish-ready native OpenClaw/ClawHub plugin packages from rough, partial, or inconsistent requirements while keeping the plugin zip separate from a critique file."
version: "1.1.0"
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "🧩"
    skillKey: "clawhub-plugin-packager"
---

# ClawHub Plugin Packager

Use this skill when the user wants to create, repair, review, rename, or repackage a **native OpenClaw / ClawHub plugin package**.

This skill is **plugin-native by design**. It is not a generic skill packager with plugin wording layered on top.

## Core promise

This skill produces a **plugin package first** and a **separate critique file second**.

The plugin package is the main deliverable.  
The critique file is the review/support layer.

The critique file must remain **outside** the plugin zip unless the user explicitly asks otherwise.

## Unified identity rule

Unless the user explicitly requests a split identity, keep one aligned identity across plugin surfaces:

- folder name
- package name
- plugin id
- publish/display name when inferable
- README title
- repository name when inferable

Prefer one clean identity over clever naming splits.

## Exact job

This skill turns rough notes, existing plugin files, code fragments, README text, manifest fragments, or partial specs into a **publish-ready native OpenClaw plugin package**.

It is designed to:

- inspect what is present
- classify the plugin type
- infer what is missing when reasonable
- repair inconsistencies
- generate a coherent plugin package anyway when safe best effort is possible
- self-audit the result
- return exactly one plugin package zip plus one separate critique file

## Operating stance

Use a **low-friction handoff** style.

When the user provides material:

- inspect what is there
- infer what is missing when reasonable
- avoid unnecessary clarification loops
- proceed with the narrowest valid plugin type
- keep the output concrete and publish-oriented

Prefer **statements** over **questions**.

If something is missing but inferable:

- infer it
- note the inference in the critique file
- keep moving

If something is risky, ambiguous, or likely to affect publishability:

- still produce the package when safe best effort is possible
- keep the runtime surface minimal
- mark the issue clearly in the critique file

Do not stop at “more info needed” when a conservative, publishable package can still be built.

## Supported modes

### 1. `native-tool-plugin`
Default mode.

Use when the request is incomplete, generic, or simply asks for “a plugin” without a more specific runtime role.

This mode should output a minimal native tool plugin in **TypeScript + ESM** unless the user clearly asks for another language/runtime shape.

### 2. `native-provider-plugin`
Use when the plugin is meant to add or wrap a provider surface such as model, speech, or service-provider behavior.

This mode must reason about:

- provider identity
- credentials or environment variables
- provider config schema
- provider-facing README guidance

### 3. `native-channel-plugin`
Use when the plugin adds a channel, transport, ingress, or egress surface.

This mode must reason about:

- channel identity
- setup/activation entry behavior
- connection/config schema
- README setup steps

### 4. `plugin-audit-only`
Use when the user wants review, validation, or packaging advice without generation.

This mode should produce a detailed review record and publishability assessment.  
Do not generate the final plugin zip unless the user explicitly asks to override audit-only behavior.

### 5. `repair-existing-plugin`
Use when the user provides an existing plugin folder, zip, manifest, `package.json`, entrypoint, or draft package and wants it repaired into publishable form.

Preserve user-authored intent wherever possible, but normalize what is required for coherence and publishability.

## Required mode selection behavior

Choose a mode using this priority order:

1. explicit user instruction
2. existing artifact structure
3. runtime role implied by requested behavior
4. fallback to `native-tool-plugin`

If ambiguity remains, do **not** block.

Infer the most conservative valid mode and continue.

That conservative fallback is always `native-tool-plugin`.

## Default strategy

Unless the request clearly specifies otherwise:

1. prefer a **native OpenClaw plugin**, not a bundle
2. prefer **`native-tool-plugin`** when the runtime role is underspecified
3. prefer **TypeScript + ESM** unless the user clearly asks for JavaScript
4. keep the first pass **minimal, publishable, and easy to extend**
5. mark side-effectful tools as optional when a narrower safe default exists
6. emit an empty-but-valid config schema when no config is needed

## Minimum publishable contract

Every non-audit generation run must produce a plugin package that includes, at minimum:

- `package.json`
- `openclaw.plugin.json`
- a coherent runtime entry file
- `README.md`

Add additional files only when the selected mode genuinely requires them, such as:

- `tsconfig.json`
- `src/`
- setup entry files for channel plugins
- bundled skill folders declared by the manifest
- helper schema files

### Required manifest behavior

Always emit a valid plugin manifest with:

- a coherent plugin id
- a valid `configSchema`

If no real configuration is needed, emit an empty or minimal schema instead of omitting it.

### Required package metadata behavior

Always include the compatibility/build metadata required for native plugin publication.

### Required README behavior

The README must state:

- what the plugin does
- what plugin class it is
- what files matter
- how configuration works
- what environment variables or credentials are expected, if any
- what assumptions were made when the input was incomplete

## Exact output contract

Always produce exactly **two user-facing deliverables** for plugin-generation jobs.

### A. Plugin package zip

A zip-ready native OpenClaw plugin folder containing **only** files that directly belong to the plugin release artifact.

Do **not** include inside the plugin zip:

- critique notes
- inference logs
- packaging commentary
- review records
- handoff discussion notes

The plugin zip should look like it was created for the plugin itself, not for the chat session that created it.

### B. Separate critique file

A separate plain-text critique file outside the plugin zip.

Preferred extension:

- `.txt`

This file must document:

- inputs provided
- mode selected and why
- assumptions and inferences
- repaired inconsistencies
- simplifications/downgrades made to preserve publishability
- remaining risks or follow-up points
- publishability assessment

## This skill's own release boundary

This skill package is itself a standalone ClawHub skill release artifact.

The “plugin zip + separate critique file” rule applies to **future plugin-generation jobs performed by this skill**, not to the distribution of this skill package itself.

Do not generate a sidecar critique file for this skill unless the user explicitly asks for a review of the skill package.

## Intake contract

Accept any of the following as valid input:

- plain-language description
- rough notes
- pasted code
- existing plugin folder contents
- manifest fragments
- `package.json` fragments
- README or docs text
- issue text or repo notes
- mixed-format partial specifications

Classify source material internally as:

- preserved input
- repaired input
- inferred input
- ignored input

Reflect those classifications in the critique file.

## Inference rules

Be inference-forward, but bounded.

### Prefer to infer

- plugin id
- display/publish name
- folder name
- description
- plugin class
- default folder layout
- minimum config schema
- entrypoint name
- README structure
- environment variable placeholders
- conservative tool/provider/channel behavior

### Do not invent recklessly

Avoid fabricating highly specific runtime features that the request does not justify.

When uncertain, prefer:

1. publishability
2. minimal runtime coherence
3. safety and reviewability
4. feature richness

When a detail is genuinely unknown, choose the narrowest valid implementation and record the assumption.

## Build rules by mode

### `native-tool-plugin`

Generate the smallest useful native plugin.

Default target:

- TypeScript
- ESM
- one runtime entrypoint
- one minimal coherent tool registration
- optional-tool classification when side effects are likely

If the request does not clearly demand multiple tools, generate **one core tool only**.

### `native-provider-plugin`

Generate a provider-oriented package that clearly expresses:

- provider purpose
- credentials/env placeholders
- provider config fields
- how the provider is expected to be used

If provider details are missing, use placeholder-safe env variables and explain them in the README and critique file.

### `native-channel-plugin`

Generate the runtime shape appropriate for channel plugins, including setup/activation entry behavior when needed.

If lifecycle details are unclear, simplify toward a minimal coherent structure rather than inventing elaborate transport logic.

### `repair-existing-plugin`

Preserve user-authored material wherever possible, but normalize as needed:

- file naming
- folder structure
- manifest shape
- package metadata
- README format
- entrypoint naming
- config schema completeness
- plugin id consistency

Document all material changes in the critique file.

### `plugin-audit-only`

Produce a detailed critique and publishability assessment.

Do not build the final zip unless explicitly asked.

## Runtime contract layer

Every generated plugin must explicitly answer:

- what kind of plugin this is
- what runtime role it serves
- what entrypoint is used
- what config exists
- what public behavior is exposed

Do not leave these as implied.

## Secret handling and safety

Never include live credentials, secrets, or production tokens.

When secrets may be needed:

- use placeholders
- prefer documented environment-variable names
- include `.env.example`-style guidance only when it materially helps the plugin package
- record all inferred secret/env surfaces in the critique file

## Review and self-audit rules

Before final delivery, run an internal review pass against the generated result.

Check:

- plugin class coherence
- manifest presence and completeness
- config schema presence
- package metadata presence
- folder layout coherence
- README completeness
- separation between plugin zip and critique file
- obvious secret leakage
- unnecessary speculative complexity

Determine one of these outcomes:

- `publish-ready`
- `publishable with cautions`
- `needs human review before publish`

Include that assessment in the critique file.

## Critique file contract

The critique file must include these sections:

1. Output Summary  
2. Mode Selected  
3. Inputs Used  
4. Assumptions  
5. Repairs  
6. Simplifications  
7. Risks / Follow-Up Points  
8. Publishability Assessment

Do not turn this into generic commentary.  
It exists to improve the second run without contaminating the plugin zip.

## Packaging rules

- Keep the plugin package folder clean and release-oriented.
- Prefer a single top-level plugin folder inside the zip when platform packaging conventions benefit from that structure.
- Keep the critique output separate.
- Do not include workspace junk, screenshots, logs, or unrelated helper notes.

## Non-goals

Do **not** treat these as always required for v1.1 plugin generation:

- inter-plugin protocol design
- migration frameworks
- elaborate persistence systems
- full compatibility matrices
- admin dashboards
- speculative always-on runtime architecture

Those belong in later passes or only when explicitly requested.

## Final behavior rule

When in doubt, generate the **smallest publishable native plugin package** that honestly reflects the request, and document all inferences in the separate critique file.
