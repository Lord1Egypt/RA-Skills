---
name: doccraft
description: Create complete, source-grounded professional documents from existing materials, outlines, or templates, then generate, edit, review, or redline the final .docx files. Use when Codex needs to turn PDFs, DOCX, TXT, Markdown, or mixed project sources into proposals, technical方案, implementation plans, construction schemes, reports,申报材料, and other formal long-form deliverables with structured drafting, Word formatting, and review-ready document workflows.
---

# DocCraft

## Overview

Use this skill in two layers:

1. Build grounded text from source materials and a target framework.
2. If needed, create or revise the final `.docx` deliverable.

Keep Markdown or plain text as the working source of truth until the wording and structure are stable. Move into DOCX creation, formatting, tracked changes, or comments only after the content is sufficiently mature.

This skill vendors the DOCX capability locally. Do not assume a separate `$docx` skill is installed.

Some upload targets reject bundled OOXML schema files such as `.xsd`. When preparing a publishable package, use the packaged upload-safe variant from this skill. That variant keeps document generation and editing workflows, but omits the strict schema-validation bundle.

When the final deliverable is a Word document, always determine the format authority before finalization:

1. User-provided template or existing target document.
2. Explicit written formatting requirements from the user.
3. An accepted sample deliverable in the same domain.
4. The default format profile in this skill.

## Workflow Decision Tree

### A. Build a new document from existing materials

Use the source-grounded text workflow:

1. Normalize the task inputs.
2. Build a source manifest.
3. Create section briefs from the target outline.
4. Draft section files.
5. Run document-level consistency review.
6. Assemble the final Markdown or text output.

### B. Read, create, or edit a Word document

Use the DOCX workflows in this skill:

1. Read existing `.docx` content with `pandoc` when text extraction is enough.
2. Create a new `.docx` from scratch only after fully reading [docx-js.md](docx-js.md).
3. Edit or redline existing `.docx` files only after fully reading [ooxml.md](ooxml.md).
4. Default to tracked changes or comments for government, legal, academic, commercial, or third-party documents.

### C. Do both

Split the work into phases:

1. Draft and stabilize text first.
2. Freeze the source-backed wording.
3. Move into `.docx` generation or `.docx` editing.

Do not mix heavy content generation and low-level OOXML editing in the same pass unless the task is trivial.

## Source-Grounded Text Workflow

### 1. Normalize the inputs

Confirm these four inputs before drafting:

- Source corpus: directories and files that contain the facts.
- Target structure: required outline, template, or chapter list.
- Writing rules: tone, exclusions, terminology, formatting, review constraints.
- Output contract: section files, merged Markdown, DOCX, review memo, or tracked-change file.

If any input is missing, infer the minimum safe default and state the assumption in the working notes, not in the final deliverable.

If the output contract includes `.docx`, also determine the format authority early. Read [references/word-format-profile.md](references/word-format-profile.md) and use [scripts/init_format_profile.py](scripts/init_format_profile.py) when a format profile needs to be captured or confirmed.

If the task is to produce a formal, complete Word deliverable, capture a delivery brief before drafting. Read [references/word-delivery-brief.md](references/word-delivery-brief.md) and use [scripts/init_delivery_brief.py](scripts/init_delivery_brief.py) to record what the user must specify and what still needs confirmation.

### 2. Build a source manifest

Before writing, create a manifest of the available materials. Read [references/source-manifest.md](references/source-manifest.md) when the corpus has more than a few files.

Use [scripts/build_manifest.py](scripts/build_manifest.py) to generate a first-pass inventory. Then enrich or trim it manually as needed.

The manifest should separate:

- Authoritative source files.
- Derivative files such as extracted text, drafts, or previous outputs.
- Template or outline files.
- Files that are only useful for lookup, not for quoting.

### 3. Create section briefs

Do not draft directly from a large corpus into the final chapters. First create a section brief for each target section.

Read [references/section-briefs.md](references/section-briefs.md) when building the planning layer. Use [scripts/plan_sections.py](scripts/plan_sections.py) to bootstrap the outline into brief stubs.

Each section brief should contain at least:

- Section id and title.
- Purpose of the section.
- Must-cover points.
- Allowed generic material.
- Primary and secondary sources.
- Expected figures, tables, and checklists.
- Exclusions and collision boundaries with nearby sections.
- Open questions or unresolved source gaps.

For large projects, section briefs are the shared contract between multiple agents.

### 4. Draft sections

Read [references/drafting-rules.md](references/drafting-rules.md) before drafting.

Draft against the section brief, not against the whole corpus. This keeps the writing grounded and reduces repetition.

Rules:

- Keep verifiable facts tied to source material.
- Allow generic boilerplate only for management, quality, safety, process, or industry-standard measures that do not conflict with the source corpus.
- Prefer concrete implementation language over slogan-style abstractions.
- Integrate figures and tables into nearby prose. Do not create headings that only say "figure" or "table".
- If the final deliverable must not show source notes, keep any evidence notes in working files only.

### 5. Run consistency review

Read [references/consistency-review.md](references/consistency-review.md) before merging the full document.

Run a full-pass review for:

- Terminology consistency.
- Number, quantity, scope, and interface consistency.
- Duplicate or contradictory paragraphs.
- Section boundary collisions.
- Heading numbering and naming consistency.
- Hidden source labels that should not appear in final copy.

### 6. Assemble the output

Use [scripts/assemble_markdown.py](scripts/assemble_markdown.py) to merge ordered chapter files into a single Markdown draft when needed.

Keep a clear distinction between:

- Working drafts with evidence or TODO notes.
- Clean deliverables prepared for DOCX conversion.

## Default Execution Pattern

### Single-agent mode

Default to a single agent when:

- The outline is short.
- The source corpus is small.
- Cross-section dependencies are high.
- The user mainly wants a coherent draft, not parallel throughput.

### Multi-agent mode

Use multiple agents only when:

- The source corpus is large.
- Sections are sufficiently independent.
- A shared glossary, writing rules, and section-brief set can be produced first.

In multi-agent mode, create these shared artifacts before splitting work:

1. Source manifest.
2. Section brief pack.
3. Glossary or terminology list if naming is fragile.
4. Shared writing rules.

Do not let agents improvise different naming systems, evidence rules, or section boundaries.

## DOCX Workflows

### Read or analyze `.docx`

If only the text is needed, convert the file with:

```bash
pandoc --track-changes=all path-to-file.docx -o output.md
```

If structure, comments, media, or tracked changes matter, unpack the OOXML package and inspect the XML.

### Create a new `.docx`

Before writing any code, fully read [docx-js.md](docx-js.md) without truncation.

Use the bundled `docx` JavaScript workflow when:

- Creating a new Word document from stable text.
- Rebuilding a formatted deliverable from Markdown or structured content.
- Generating tables, headings, page settings, headers, or footers programmatically.

Before final DOCX generation, lock the format profile. If no authoritative template exists, use the default profile in [references/word-format-profile.md](references/word-format-profile.md).

Before final DOCX generation, also resolve the delivery brief items that affect document completeness, review mode, and output packaging.

Before final DOCX generation, run [scripts/resolve_word_job.py](scripts/resolve_word_job.py) or follow [references/word-assembly-plan.md](references/word-assembly-plan.md) to determine whether the Word job is actually ready for delivery, which package components will be generated, and which blockers remain.

When the job is ready, generate the file with [scripts/generate_docx_from_markdown.cjs](scripts/generate_docx_from_markdown.cjs). Feed it the merged Markdown body, the delivery brief JSON, and the format profile JSON.

### Edit an existing `.docx`

Before editing, fully read [ooxml.md](ooxml.md) without truncation.

Use the bundled OOXML workflow when:

- Editing an existing Word file.
- Preserving existing formatting.
- Adding comments.
- Inserting tracked changes.
- Performing safe structural edits in a professional document.

### Redline and review mode

Default to tracked changes or comments when editing:

- Government documents.
- Legal, commercial, or academic documents.
- Another author's file.
- Any document where reviewability matters as much as correctness.

Use the bundled local resources in this skill:

- [scripts/document.py](scripts/document.py)
- [scripts/utilities.py](scripts/utilities.py)
- [ooxml/scripts/unpack.py](ooxml/scripts/unpack.py)
- [ooxml/scripts/pack.py](ooxml/scripts/pack.py)
- [ooxml/scripts/validate.py](ooxml/scripts/validate.py)

If the upload-safe package excluded the OOXML `.xsd` schema set, treat strict schema validation as unavailable and continue with unpack, edit, and repack workflows only.

### Format confirmation rule

Do not ask the user to confirm formatting too early if the task is still in the text-drafting phase. Draft the content first unless formatting decisions would change the structure materially.

Ask the user to confirm the format before final Word delivery when any of these are true:

- The document is an external or formal deliverable.
- No authoritative template or accepted sample document exists.
- The user gave conflicting formatting signals.
- The output must match an institutional standard closely.

Do not ask for confirmation when:

- The user already provided a template or a target `.docx` to match.
- The task is still a Markdown or text-only draft.
- The user explicitly accepts the skill default.

When confirmation is needed, present the resolved format profile, not an open-ended question. Default to the profile in [references/word-format-profile.md](references/word-format-profile.md) if the user does not override it.

### Delivery-brief rule

For a complete Word deliverable, separate user inputs into two buckets.

The user must specify these before drafting:

- Document title
- Source corpus or authoritative source set
- Target outline, template, or existing document to match
- Document purpose and intended audience
- Output mode: new document, rewrite, or edit existing `.docx`

The user must confirm these before final Word delivery:

- Delivery stage is final, not just draft
- Completeness scope such as cover, table of contents, appendices, glossary, lists, and attachments
- Review mode: clean copy, tracked changes, or comments
- Format profile or template choice
- File naming or versioning if the delivery package is formal
- Whether working notes, source markers, or traceability hints must be removed from the final copy

If these items are unclear, proceed with text drafting only when safe defaults will not invalidate the content. Do not finalize the Word deliverable until the unresolved delivery-brief items are closed.

### Word assembly rule

Treat final Word generation as a gated assembly step, not just a file export.

Before assembly, resolve:

- readiness for draft or final stage
- required package components such as cover, table of contents, appendices, glossary, lists, and attachment manifest
- review artifact mode such as clean copy, tracked changes, or comments
- cleanup behavior for working notes and source traces

If the job is not ready, stop at Markdown or internal DOCX draft output and surface the blockers explicitly.

## Resource Map

- [references/source-manifest.md](references/source-manifest.md): how to inventory and classify the source corpus.
- [references/section-briefs.md](references/section-briefs.md): how to convert an outline into executable chapter briefs.
- [references/drafting-rules.md](references/drafting-rules.md): drafting standards for grounded long-form writing.
- [references/consistency-review.md](references/consistency-review.md): document-level review checklist.
- [references/word-format-profile.md](references/word-format-profile.md): format authority rules and the default Word style profile.
- [references/word-delivery-brief.md](references/word-delivery-brief.md): what the user must specify and confirm for a complete Word deliverable.
- [references/word-assembly-plan.md](references/word-assembly-plan.md): how to decide readiness and package composition before final DOCX delivery.
- [references/publishing-installation.md](references/publishing-installation.md): how to package, publish, and install the skill.
- [scripts/generate_docx_from_markdown.cjs](scripts/generate_docx_from_markdown.cjs): generate a `.docx` from Markdown, the delivery brief, and the format profile.
- [docx-js.md](docx-js.md): full reference for creating new `.docx` files.
- [ooxml.md](ooxml.md): full reference for editing existing OOXML-based Word files.

## Non-Negotiable Rules

- Do not invent facts that should come from the source corpus.
- Do not treat draft text as a primary source when an authoritative source exists.
- Do not move to OOXML-level editing before the content is stable unless the task is purely editorial.
- Do not assume a separate DOCX skill is available. Use the bundled resources in this skill.
- Do not finalize Word output without resolving the format authority.
- Do not finalize a formal Word deliverable without resolving the delivery brief.
