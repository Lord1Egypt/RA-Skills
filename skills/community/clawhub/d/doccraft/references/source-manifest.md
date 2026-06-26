# Source Manifest

Create a source manifest before drafting when the task uses multiple files, multiple directories, or mixed authoritative and derivative materials.

## Purpose

Use the manifest to separate what the document may rely on from what is only convenient context.

The manifest is a planning artifact. It does not need to be shown to the user unless requested.

## Minimum fields

Record these fields for each file:

- `id`: stable short id.
- `path`: file path.
- `kind`: `source`, `outline`, `draft`, `output`, or `reference`.
- `format`: `pdf`, `docx`, `txt`, `md`, and so on.
- `title`: human-readable label.
- `authority`: `authoritative`, `derived`, or `working`.
- `notes`: what the file is good for.
- `risk_flags`: facts that require extra care, such as counts, scope, quantities, interfaces, legal language, or standards.

Optional fields:

- `likely_sections`
- `owner`
- `revision_date`
- `exclusions`

## Classification rules

Use these distinctions consistently:

- `authoritative`: the factual basis of the deliverable.
- `derived`: extracted text, OCR text, summaries, or converted files.
- `working`: outlines, drafts, merged files, or review notes.

Do not cite a derived or working file when the authoritative original is available.

## Practical workflow

1. Run [scripts/build_manifest.py](../scripts/build_manifest.py) on the source directories.
2. Remove noise files such as `.DS_Store`, upload markers, and previous outputs that should not guide drafting.
3. Mark template files and target-outline files explicitly.
4. Identify files that contain high-risk facts.
5. Note which files are useful only for navigation or lookup.

## Output shape

Prefer one of these:

- JSON when another script or agent will consume it.
- Markdown when humans will review and edit it.

## High-risk fact categories

Always flag files that control any of the following:

- Scope boundaries
- Quantities and counts
- Milestones and schedule
- Technical indicators
- Standards and clause numbers
- External interfaces
- Responsibilities and contractual boundaries

These categories require extra checking during drafting and final review.
