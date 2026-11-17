---
name: build-docs-creator
description: "Produces a complete, standardized build-documentation package for developers from a project's accumulated design work — a product overview (BRD-style), requirements spec (SRS-style), technical design doc (DD-style), and interface source code with a reference guide, all zipped together. Use when the user asks to 'create build docs,' 'generate the doc package,' 'turn this project into docs for devs,' 'produce an SRS/BRD/DD package,' or wants a developer handoff covering both what to build and why. Works from a Claude Project's conversation history and artifacts (including Claude Design/HTML interfaces), and can incorporate partial docs brought in from elsewhere (e.g. ChatGPT-authored requirements) alongside the project's own content. Do NOT use for a single narrow doc request — this skill's default output is the full package. Not for ongoing SDLC docs (test plans, runbooks, sprint artifacts) — pre-build documentation only."
---

# Build Docs Creator

Synthesizes everything designed and decided in a project — chat history, artifacts, Claude Design / HTML interfaces built along the way, and any partial documentation brought in from elsewhere (commonly ChatGPT-authored initial requirements) — into one standardized, zipped documentation package that gives a development team everything they'd normally expect at project handoff: what the product is and why it exists, what it must do, how it's designed, what the interfaces are, and how it all traces together.

Every package this skill produces has the same shape and the same rigor regardless of which project it's run against. That standardization is the point — a developer picking up any package from this skill should find the same documents in the same order covering the same ground.

## The typical pipeline this serves

The common origin story for a project using this skill:
1. Initial requirements/concept were drafted in **another tool (often ChatGPT)** and pasted into a Claude Project.
2. The concept was **refined through discussion** in the Project.
3. Interfaces were **designed and built as HTML/React artifacts** (often via Claude Design) inside the Project.
4. Now the whole thing needs to become a **developer-ready build package**.

This matters because the pasted-in requirements are frequently **stale** relative to what actually got designed and built afterward. See "Reconciling imported requirements" below — catching that drift is one of the most valuable things this skill does.

## Core principle: don't invent scope

The single biggest failure mode is silently filling gaps with plausible-sounding detail. If the source material doesn't specify something — what a button wires to, whether two entities are the same, what auth model is used — the output states that gap plainly in the relevant document's Open Questions section. It never asserts an invented answer as fact. A shorter, honest package beats a longer, fabricated one. This applies to every document in the package.

Two corollaries:
- **Extraction beats invention.** When real source exists (especially interface HTML), inventory what's actually there rather than describing what you imagine. A form with three fields has three fields — read them out of the code, don't guess at five.
- **Distinguish decided from discussed.** "We'll probably use Postgres" is not "the datastore is Postgres." Firm decisions and open leanings must be visibly different in every document.

## Source flexibility

Detect which mode applies from what the user provides; ask only if genuinely ambiguous:

1. **Claude Project only** — pull from the Project's conversation history, artifacts, and interfaces.
2. **Claude Project + imported requirements/docs** — the user brings in ChatGPT output, notes, or a draft SRS. Merge it with the Project's own content; reconcile conflicts per below rather than silently preferring one source.
3. **External material only** — no live Project, just provided transcripts/notes/drafts. Same output structure; the Interfaces section is reduced to a note if no interface artifacts exist.

### Reconciling imported requirements (critical for the ChatGPT pipeline)

When requirements were imported from an external tool and the project then evolved, actively check for drift:
- **Requirement with no corresponding design/interface** -> keep it, but flag in the requirements doc's Open Questions: "stated in original requirements, not reflected in built interfaces — confirm still in scope."
- **Built interface/feature with no corresponding original requirement** -> the design outpaced the spec. Add a requirement capturing what was built, tagged as *(derived from built interface, not in original requirements)*.
- **Direct contradiction** (original says X, design does Y) -> surface it explicitly in Open Questions naming both sources; do not silently adopt one.

This reconciliation is a core deliverable, not a nicety — an imported spec that quietly disagrees with the built product is exactly what derails a dev handoff.

## Workflow

### Step 1: Establish working directory and gather source material

Pick a writable working directory (create it; don't assume it exists):
```bash
WORKDIR=$(mktemp -d)   # or a named dir under a writable location
```

Then gather:
- Search the Project's conversation history for design discussion, decisions, requirements (use `conversation_search`/`recent_chats` if relevant history isn't in the current context — search by feature/component names, not meta-words like "discussed").
- Read every artifact, especially HTML/React/Claude Design interfaces — pull the **actual source**, don't just note it exists.
- Ingest any imported/external material the user provides.
- If material is too thin to produce a usable package (no clear purpose, no entities, nothing built), ask ONE clarifying question. Otherwise proceed and route gaps to Open Questions.

### Step 2: Build the extraction ledger before drafting

Assemble a working list (internal scratch — not shipped) capturing, each tagged with its source:
- **Product purpose / business rationale** — why it exists, what problem, for whom
- **Terminology** — domain terms, entity names, any place the same concept is named two ways across sources (feeds the glossary)
- **Entities/actors** and their relationships
- **Requirements** — split into *firm* ("shall"-strength: stated as need/decision) vs *soft* ("should"-strength: desired/debated)
- **Design/architecture decisions** — split *decided* vs *leaning/proposed*
- **Tech stack** — languages, frameworks, services, datastores named anywhere
- **Interfaces built** — every artifact, with fields/components/states read from the actual code
- **Cross-links** — which requirement maps to which interface/design element (this becomes the traceability matrix)
- **Open items** — questions, unresolved debates, follow-ups, and any imported-vs-built drift found during reconciliation

### Step 3: Draft each document from its reference file

Each output has a reference file specifying required sections, format, and standard. **Read the relevant reference file immediately before drafting that document** — do not draft from memory of the structure:

| Output | Reference file |
|---|---|
| `00-product-overview.md` (BRD) | `references/product-overview.md` |
| `01-requirements.md` (SRS) | `references/requirements.md` |
| `02-design.md` (DD) | `references/design.md` |
| `03-interfaces/` | `references/interfaces.md` |
| `04-traceability-matrix.md` | `references/traceability.md` |

Draft in this order — later documents depend on identifiers established in earlier ones (requirements get `FR-`/`NFR-` IDs; the traceability matrix references those IDs plus interface filenames).

Keep every document as short as the source honestly supports. Every substantive claim must be traceable to something discussed or built; if it isn't, it belongs in Open Questions, not stated as settled.

### Step 4: Assemble and zip the package

Target structure:
```
[ProjectName]-build-docs/
├── README.md
├── 00-product-overview.md
├── 01-requirements.md
├── 02-design.md
├── 03-interfaces/
│   ├── html/
│   │   └── (one file per interface, real runnable source)
│   └── interface-reference.md
├── 04-traceability-matrix.md
└── _source-manifest.md
```

- `README.md` — indexes every document, states the reading order and who each doc is for, and surfaces the top-level honesty signals (total open questions, any imported-vs-built conflicts, which docs are thin).
- `_source-manifest.md` — an auditable list of exactly what source material fed the package: which Project conversations (by title/date if available), which artifacts (by name), and which imported documents. This makes the package traceable back to its inputs.
- **No screenshots or rendered images.** The HTML source is the interface deliverable. Do not attempt browser automation or image rendering.

Assemble and zip:
```bash
PKG="$WORKDIR/[ProjectName]-build-docs"
mkdir -p "$PKG/03-interfaces/html"
# write all files into place
( cd "$WORKDIR" && zip -r "[ProjectName]-build-docs.zip" "[ProjectName]-build-docs/" )
```
Copy the zip to the outputs directory and present it.

If interface HTML has unrunnable external dependencies, keep the real source as-is and note the dependency in that file's `interface-reference.md` entry rather than shipping a silently broken file or "fixing" it by inventing code.

### Step 5: Report the honest state of the package

After delivering, state plainly:
- Total Open Questions across all documents, and whether any block a dev from starting
- Any imported-requirement-vs-built-product conflicts found during reconciliation
- Which documents are thin because the source was thin — don't let clean formatting imply certainty the source doesn't support

## Anti-patterns to avoid

- Inventing acceptance criteria, edge cases, NFRs, or interface behaviors that weren't discussed or aren't evident in the code
- Turning a debated "maybe" into a firm requirement or a settled design decision
- Producing API-spec-level design detail the source never reached — say "not yet specified" instead
- Shrinking or skipping Open Questions sections to make the package look finished — that gap list is the most useful part for a team scoping the work
- Silently adopting imported requirements without reconciling them against what was actually built
- Describing interfaces from imagination when the real HTML is right there to inventory
- Attempting screenshots or visual rendering — out of scope; HTML source is the deliverable
