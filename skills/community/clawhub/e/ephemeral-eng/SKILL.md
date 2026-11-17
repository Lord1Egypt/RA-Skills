---
name: ephemeral-eng
description: Build single-file HTML engineering tools where the calculation interface IS the client deliverable (input panel on the left, print-ready paginated report on the right). Use this skill whenever the user asks for an engineering calculator, calc tool, letter generator, calculation report, load check, beam/column/footing/header/fastener/anchor/wind/guardrail/canopy check, evaluation letter, or any "input-to-deliverable" tool — even if they don't say "ephemeral-eng" or "HTML". Also use it when revising or extending any existing single-file tool that has a form-panel / report-page structure.
---

# ephemeral-eng — Input-to-Deliverable Engineering Tools

You are building a **single self-contained HTML file** that is simultaneously an engineering calculator and the final client deliverable. No build step, no dependencies, no server. The user opens it in a browser, types inputs on the left, and the paginated report on the right *is* what they print to PDF and issue.

**Start from the template.** Read `template/ephemeral-template.html` in this repo (or ask the user for their latest tool as a base). Never invent a new layout — consistency across tools is the product.

## Non-negotiable safety rules

1. **Every tool ships UNVERIFIED.** Include the draft-watermark checkbox (default ON) and the footer note stating the tool must be verified per VERIFICATION.md before use. Never remove these; never default the watermark off.
2. **Tell the user, every time, in your final message:** the tool is unverified until they complete the VERIFICATION.md checklist, including a digit-for-digit hand-calc match.
3. **Never fabricate code values.** If you are not certain of a coefficient, table value, or code section (ASCE 7, NDS, ACI, AISC, ADM, IBC/FBC…), leave a clearly marked input for the engineer to enter it (`<span class="hint">enter from Table X</span>`) instead of hard-coding a guess. A blank the engineer must fill is safe; a wrong constant is not.
4. **Decline scope creep.** If asked for FEA, dynamic/seismic response, nonlinear or coupled-system analysis, say the framework is intentionally limited to simple, hand-verifiable checks and suggest validated commercial software.
5. **When editing an existing tool, change only what was asked** and list every functional change you made (the user will diff the file). Bump the version.

## The five slots

The template marks five slots. Fill only these; leave framework chrome alone.

| Slot | What goes there | Rules |
|---|---|---|
| 1. Brand tokens | `:root` CSS variables + `FIRM` JS object | Only place colors/fonts/firm identity live. Re-skinning a tool = editing this slot only. |
| 2. Input schema | `<fieldset>` groups in `.form-panel` | Every input `id="f_camelCase"`. Group logically (Branding / Project / Geometry & Loads / Section & Material / Criteria / Exhibits / Output options). Units in `<span class="hint">`. Sensible non-trivial defaults that PASS. Include the template's Branding fieldset (firm name/lines, logo drag-drop, live brand-color picker) unless the user says their tokens are already set. |
| 3. Calc engine | Pure JS functions | **No DOM access.** Units in a comment on *every* assignment. Code reference in a comment on every check (e.g. `// [NDS 2018 §3.4]`). One flat result object. Plus a `validate(inp)` returning warning strings for zero/negative/absurd inputs. |
| 4. Live diagram | `drawDiagram(inp, r)` → SVG string | To-scale-ish sketch of the physical thing, dimensioned from live inputs, with a PASS/FAIL readout. Screen-only (`.no-print`). |
| 5. Report pages | `buildReport(d, r)` → `.report-page` divs | See "Report standards" below. |

## Report standards (the deliverable)

- US Letter pages: `.report-page` at 8.5×11in, `page-break-after:always`, branded footer on every page (`footer(pg, of, d)` helper), watermark via `wm(d)`.
- **A reviewer must be able to check the report without the tool.** Show every input, every assumption (code edition, ASD/LRFD, load combos, what's excluded e.g. self-weight), and every calc step **with substituted numbers**: `M = wL²/8 = 100 × 12²/8 = 1,800 lb·ft` — never just the answer.
- Structure: (1) firm header + project block + design basis + inputs, (2) section properties → demands → checks as `.calc-step` blocks with `.ref` code citations → summary `.calc-table` with DCR + PASS/FAIL cells → conclusion box → signature block with stamp placeholder, (3+) appendix exhibits (drag-drop images) only if provided.
- All numbers through `num(x, dp)`; all user text through `esc(s)`. Never interpolate raw user input into HTML.

## Engine conventions

- ASD vs LRFD/strength must be explicit in labels, basis paragraph, and comments. Never mix.
- Trap-check yourself before finishing: psf↔psi, plf↔lb/in, ft↔in (especially in L⁴ deflection terms), nominal vs actual dimensions, service vs strength wind pressures.
- Interpolations: clamp or warn outside table ranges — never extrapolate silently.
- `validate()` must catch: non-positive dimensions/loads/design values, and at least one absurdity check relevant to the domain (e.g. span-to-depth > 50).

## Input JSON (state save/load) — mandatory framework chrome

Every tool keeps the template's JSON module (`serializeInputs / exportJSON / importJSON` + the "Save inputs / Load inputs" buttons). It exports every `f_*` input (and dropped images) to a portable file:

```json
{
  "_meta": { "framework": "ephemeral-eng", "tool": "<FIRM.toolName>", "toolVersion": "V1.2",
             "saved": "ISO-8601", "source": "user" },
  "inputs": { "f_L": "12", "f_w": "100", "f_draft": true },
  "images": { "logoData": null, "imgData": null }
}
```

Why it matters: the calculator can be disposable because the **project state is portable** — archived with the job, re-loaded next revision, or moved into the next version of the tool.

**AI pre-generation workflow:** when a user gives you plan notes, an architect's email, or project docs and asks you to prep a calc, you may emit this JSON directly (keys = the tool's `f_*` ids) so they load it and review instead of typing. Rules:
1. You MUST set `"_meta.source": "ai"` — the tool then displays a persistent verify-every-value warning until the engineer edits the inputs. Never set `"user"` for machine-generated files.
2. Only fill values you can trace to the provided documents; leave unknown fields out (the tool keeps its defaults) rather than guessing.
3. List, in your reply, every value you filled and the document/line it came from.

## Versioning & naming

File name: `{ProjectNo_}ToolName_vX_Y.html` (e.g. `V26150_Footing_Check_v1_0.html`). Version appears in `<title>`, the panel `version-badge`, `FIRM.toolVersion`, and the report footer. Any functional change bumps the version; note what changed in a comment block at the top.

## Workflow when a user requests a new tool

1. **Interview briefly**: what's being checked, governing code + edition, ASD or LRFD, inputs they want exposed vs fixed, deliverable type (calc report vs evaluation letter), branding (or reuse their existing tokens).
2. **State your calculation plan in plain English first** — formulas, code sections, assumptions — and get confirmation before writing code. This is where the engineer catches wrong physics cheaply.
3. Build from the template, filling the five slots.
4. **Self-check**: run the engine mentally (or with a script if you have code execution) on the default inputs and one boundary case; confirm units line by line.
5. Deliver with: (a) the file, (b) a list of every formula + code reference used, (c) explicit assumptions/exclusions, (d) the unverified-tool warning and a pointer to VERIFICATION.md.

## Letter-generator variant

For evaluation/compliance letters (vs calc reports): first page is prose letterhead (addressee block, purpose & scope, numbered sections, conditions of acceptance, conclusion), calc detail moves to an "Exhibit — Calculations" appendix of `.calc-step` blocks, and exhibits get cover pages. Same slots, same rules.
