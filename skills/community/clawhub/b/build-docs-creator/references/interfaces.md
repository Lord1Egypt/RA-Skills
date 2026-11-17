# Reference: `03-interfaces/`

Deliverable covering every UI interface built in the project — real, runnable source code plus a reference document explaining what each one is, what it contains, and what it does. No screenshots or rendered images are produced by this skill; the HTML source itself is the visual deliverable, and the reference doc is built by **reading the actual code**, not by describing it from memory or discussion alone.

## Folder structure

```
03-interfaces/
├── html/
│   ├── [interface-name-1].html
│   ├── [interface-name-2].html
│   └── ...
└── interface-reference.md
```

## `html/` folder

- One file per interface, using the **actual source** pulled from the project's artifacts — never recreated or paraphrased. React/JSX artifacts keep their original extension; don't force a lossy HTML conversion.
- Descriptive, stable file names (`customer-dashboard.html`, not `artifact-1.html`) so the reference doc's links stay meaningful. If two artifacts are iterations of the same screen, keep the **latest** as the canonical file and note superseded versions in the reference entry rather than shipping confusing duplicates.
- If an artifact has external dependencies that prevent standalone running (CDN imports, API calls, missing env), keep the real source and record the limitation in its reference entry — do not "fix" it by inventing code.

## `interface-reference.md`

One entry per interface, built by **inventorying the actual code**. Read each file and extract its real components, forms, fields, and states — don't approximate.

```markdown
## [Interface Name] — `html/[filename].html`

**Purpose:** What this screen is for, in one or two sentences.

**Components present (from code):** The actual UI elements in the file — sections, tables, forms, buttons, nav, modals. Read them out of the markup.

**Form fields (from code):** For each form/input found: field label/name, type, and whether it's marked required. Present as a short table when there are several. Omit if the interface has no inputs.

**States (from code):** Distinct visual/interaction states present in the markup or logic — empty, loading, error, success, populated, etc. Note only states actually present.

**Behavior:** What happens on use — actions triggered, navigation, state changes. Where a handler is a visible stub or the behavior wasn't discussed, say "not yet wired / not specified" rather than inventing a flow.

**Connects to:** Known connections — backend endpoint, data source, another screen. Only what was actually discussed or is present in the code. If unknown: "Not yet specified in source material — see Open Questions." Keep consistent with `02-design.md` Interfaces & Integrations.

**Requirements implemented:** The `FR-` IDs from `01-requirements.md` this interface satisfies, if determinable. This feeds the traceability matrix. If an interface implements behavior that has no matching requirement, note it — that's a reconciliation finding (design outpaced spec).

**Notes:** Dependencies, incomplete states, superseded versions, known issues raised in discussion.
```

## Standards for this section

- **Extract, never invent.** A button whose function wasn't discussed and isn't evident in code is "purpose not yet specified," not a guessed action. Field lists come from the markup, not imagination.
- **Cross-consistency.** Interface "Connects to" must agree with `02-design.md`; "Requirements implemented" must reference real `FR-` IDs and feed `04-traceability-matrix.md`.
- **No screenshots, no rendered images.** The HTML source plus written reference is the complete deliverable for this section. Do not attempt to render or screenshot.
- **No interfaces built?** If the project has no interface artifacts (pure backend/API work, or design never reached a visual stage), reduce this to a short note in `interface-reference.md` stating none were built as of this package, and omit the `html/` folder rather than shipping an empty placeholder.
