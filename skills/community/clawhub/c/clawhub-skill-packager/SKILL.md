---
name: clawhub-skill-packager
description: "Turn rough, partial, or broken ClawHub/OpenClaw skill material into one publish-ready skill bundle plus one separate plain-text review file using an inference-first, low-friction workflow."
version: "1.5.2"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📦","skillKey":"clawhub-skill-packager"}}
---

# ClawHub Skill Packager

Use this skill when the user wants to create, repair, review, rename, repackage, or republish a ClawHub / OpenClaw skill bundle.

## Product promise

This skill makes the **publish-ready skill package first**.

Then it provides the **separate review file** that explains:
- what was provided
- what was inferred
- what was fixed
- what still deserves human review

The package is the main product.
The review file is the supporting layer.

## Unified identity rule

This skill uses one unified identity across runtime, packaging, and publishing surfaces:
- runtime name: `clawhub-skill-packager`
- slug: `clawhub-skill-packager`
- folder name: `clawhub-skill-packager`
- metadata.openclaw.skillKey: `clawhub-skill-packager`

Do not intentionally split runtime, folder, slug, and skill key identities unless the user explicitly asks for it.

## Core job

This skill turns user input, existing skill files, or partial drafts into a **publish-ready ClawHub/OpenClaw skill bundle**.

It is designed to:
- inspect what is present
- infer what is missing when reasonable
- repair inconsistencies
- build the package anyway when a safe best-effort package is possible
- self-audit the result
- return one pure publish bundle plus one separate plain-text review file

## Operating stance

This skill is designed for **low-friction handoff**.

When the user provides material:
- inspect what is there
- infer what is missing when reasonable
- choose the best safe course based on current knowledge
- avoid unnecessary clarification loops
- return a concrete package plus a review statement

Prefer **statements** over **questions**.

If something is missing but inferable:
- infer it
- note the inference
- keep moving

If something is risky, ambiguous, or likely to affect publishing:
- still produce the package when a safe best-effort package is possible
- highlight the issue clearly in the review file
- mark it for user review

Do not stop at “more info needed” when a reasonable package can still be built.

Default to the **full release-bundle standard**, not the minimal valid skill standard, unless the user explicitly asks for a minimal package.

## Exact output contract

Always produce exactly **two user-facing deliverables**.

### A. Publish bundle zip
A zip-ready skill folder containing **only** files that directly belong to the skill as a release artifact.

This bundle must include:
- `SKILL.md`
- `README.md`
- `CHANGELOG.md`

It may also include only those additional files that are genuinely part of the skill itself or required for the skill to function correctly, such as:
- `references/`
- `examples/`
- `scripts/`
- `configs/`
- `assets/`

Do **not** include inside the publish bundle:
- review notes
- inference notes
- build commentary
- user/AI discussion notes
- release review records
- handoff notes that are only about packaging this build

The publish bundle should look like it was made for the skill itself, not for the conversation that created it.

### B. Separate plain-text review file
A separate review file in plain text.

Preferred format:
- `.txt`

This review file should say:
- what inputs were provided
- what information was missing
- what assumptions were made
- what was added
- what was edited
- what was removed
- what was inferred
- what still deserves human review
- whether the package appears publish-ready
- the final publish/install handoff details

The review file must remain **outside** the publish bundle unless the user explicitly asks for it to be embedded.

## Standard support artifacts inside this packager skill

This packager skill ships with reusable support files that are part of the skill itself.

Use them like this:
- `REVIEW-CHECKLIST.txt` = the permanent self-audit standard
- `REVIEW-RECORD-TEMPLATE.txt` = the base for the generated separate review file

## Operating modes

Use one of these modes based on the user's request and the material provided.

### 1. Package-from-scratch
Use when the user provides a concept, rough notes, or minimal package material.

Pass 1:
- assemble identity
- infer missing metadata
- define package surfaces
- identify major assumptions

Pass 2:
- build files
- self-audit
- generate the separate review file

### 2. Repair-existing-skill
Use when the user provides an existing skill package that needs cleanup, fixes, or modernization.

Pass 1:
- inspect existing files
- identify drift, breakage, or parser-risky structure
- determine what should be preserved

Pass 2:
- repair and normalize
- self-audit
- generate the separate review file

### 3. Audit-only
Use when the user wants analysis and recommendations without generating a new package.

Pass 1:
- inspect the provided package or concept
- identify strengths, issues, risks, and missing information

Pass 2:
- generate the review file
- do not build a replacement package unless the user also asked for packaging

### 4. Republish / update
Use when the user already has a package and wants version, naming, positioning, or packaging updates for republishing.

Pass 1:
- inspect the current package
- identify what changed since the prior release
- align versioning, naming, and publish surfaces

Pass 2:
- update files
- self-audit
- generate the separate review file

### 5. Rename / rebrand
Use when identity surfaces need changing while preserving intended behavior.

Pass 1:
- inspect current identity surfaces
- preserve intended behavior
- determine which naming surfaces change and which remain stable

Pass 2:
- rewrite aligned identity surfaces
- self-audit
- generate the separate review file

## Packaging workflow

### Step 1 — Inspect
Look at all provided material:
- text prompts
- existing `SKILL.md`
- existing `README.md`
- existing `CHANGELOG.md`
- file names
- intended display name
- intended slug
- invocation ideas
- notes about platform behavior
- prior package artifacts if relevant

### Step 2 — Determine completeness
Check whether the package has enough information for:
- display name
- slug
- runtime identity
- version
- description
- tags
- invocation behavior
- public positioning
- file set
- frontmatter format
- compatibility with current OpenClaw parser expectations

### Step 3 — Infer or repair
If something is missing or inconsistent:
- choose the best safe default
- repair mismatched naming
- align display name, slug, runtime name, folder name, skill key, and README publish fields unless the user explicitly requests a split
- correct parser-risky frontmatter
- normalize versioning
- remove obvious contradictions
- preserve intended behavior whenever possible

### Step 4 — Build the package
Create the full package folder and final file contents.

### Step 5 — Self-audit
Run a second-pass review using `REVIEW-CHECKLIST.txt`.

### Step 6 — Deliver
Deliver exactly two user-facing artifacts:
- the final publish bundle zip
- the separate review file built from `REVIEW-RECORD-TEMPLATE.txt`

Then provide a short summary in the response telling the user:
- here is your publish bundle
- here is your review file
- here is what was inferred
- here is what was fixed
- here is what may still deserve review

## Visibility rule

Do not bury final deliverables in an internal-only path without clearly surfacing them.

The publish zip and the separate review file must be:
- clearly identified
- surfaced directly to the user
- returned as the final two artifacts

Do not report completion until both artifacts are available in a directly user-visible way for the current environment.

## Skill type awareness

When packaging a skill, classify it before building.

Possible classes include:
- instruction-only skill
- formatting / style skill
- workflow / orchestration skill
- code or script-backed skill
- API-dependent skill
- environment-variable-dependent skill
- binary / external-tool-dependent skill
- mixed package

Use the class to decide:
- what files are needed
- what install notes are needed
- what security notes are needed
- what review flags matter most

## Runtime and security declarations

Inspect for:
- environment variable requirements
- secrets or credentials
- external API dependencies
- script or binary execution assumptions
- file system expectations
- privilege or escalation requirements
- background or always-on behavior

If these exist:
- package the skill anyway when safe
- state them clearly in the review file
- highlight them for review

## Frontmatter rules

For OpenClaw compatibility, prefer:
- single-line frontmatter keys
- metadata as a single-line JSON object
- quoted version
- quoted long description strings when helpful

Preferred base frontmatter pattern:

```yaml
---
name: skill-slug
description: "Short clear skill description."
version: "1.0.0"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📦","skillKey":"skill-slug"}}
---
```

## Naming rules

Align these surfaces unless the user explicitly wants them different:
- public display name
- package folder name
- slug
- runtime name
- metadata.openclaw.skillKey
- README publish fields
- changelog package identity

Use:
- human-readable title for display name
- lowercase hyphenated form for slug
- the same lowercase hyphenated form for runtime name by default

## Review checklist

A package should be checked for all of the following.

### Identity alignment
- display name matches intent
- slug is lowercase and hyphenated
- folder name matches slug
- runtime name matches slug unless intentionally split
- skill key matches slug
- README publish fields match final identity
- changelog reflects the current version and identity

### Frontmatter health
- `SKILL.md` exists
- frontmatter is present
- `name` exists
- `description` exists
- `version` exists
- `metadata` uses single-line JSON
- invocation flags are present when useful
- emoji is present if desired
- parser-risky nested metadata is repaired

### Behavioral clarity
- purpose is clear
- scope is clear
- activation behavior is clear
- explicit invocation is defined if needed
- output behavior is described
- risky ambiguity is reduced

### Public positioning
- branding is reasonable
- wording is accurate
- descriptions do not overclaim capabilities
- external affiliation wording is safe when relevant

### Runtime / security awareness
- skill type is correctly classified
- env var requirements are documented
- API dependencies are documented
- binaries / scripts are documented
- privilege assumptions are documented
- risky surfaces are highlighted

### Deliverable separation
- publish bundle contains only skill-release files
- review content is kept outside the publish bundle
- review file is plain text
- final deliverables are surfaced separately

### Deliverables
- package files were generated
- separate review file was generated
- changes are summarized
- assumptions are highlighted
- publish-readiness is stated

## Severity markers

Use these markers consistently:
- `✅ FIXED AUTOMATICALLY` = safe automatic repair completed
- `🔶 INFERRED FIELD` = best-effort inferred value that should remain visible
- `⚠️ REQUIRED REVIEW` = likely publish-affecting issue that deserves human confirmation
- `📝 EDITED FOR ALIGNMENT` = consistency edit across identity or package surfaces
- `🚀 READY TO PUBLISH` = no major blocker detected in the final package

## Final response contract

At completion, report in this order:
1. brief status line
2. the publish bundle zip
3. the separate review file
4. short bullet summary of:
   - what was created
   - what was changed
   - what assumptions were made
   - what should be reviewed
5. publish-readiness statement

## Second-pass workflow

If the user returns with edits or clarifications:
- re-run the same inspection and package workflow
- preserve the accepted identity and structure unless the new instructions change them
- reduce the number of inferred fields
- keep the second-pass output cleaner and closer to final
- aim for a near-zero-friction publish handoff

## Operating note

This skill is a packager and self-auditor for ClawHub / OpenClaw skills. Its job is to turn incomplete or inconsistent skill drafts into coherent publish-ready bundles while preserving the user's intended behavior whenever possible and minimizing decision friction for the user.
