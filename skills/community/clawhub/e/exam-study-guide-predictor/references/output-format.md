# Output Format & Section Catalog

Read before building the deliverable. Covers: which sections activate, color coding, and the HTML / .docx templates.

## Section catalog — activation rules

Build a section only if its trigger is met. Order sections by the mark distribution (highest-mark topics first within the guide), but keep the fixed scaffold below.

| Section | Activate when | Notes |
|---|---|---|
| 1. Table of Contents | Always | Clickable anchors in HTML. |
| 2. Exam Blueprint | Always | Exam type, total marks, per-section marks, question types, predicted paper structure. The prioritization map. |
| 3. Professor's Explicit Exam Statements | Transcripts/notes contain explicit markers | **Purple.** Verbatim quotes (Arabic + English translation) of everything the professor said is on the exam, each linked to its topic. This is the strict-extract deliverable on its own. |
| 4. High-Yield Concepts & Frameworks | Always | The must-know core, sorted by confidence + marks. Tag must-memorize vs must-understand. Include mnemonics/memory triggers. |
| 5. Core Mechanisms & Frameworks | Concept/process content present | WHY & HOW, not just WHAT — covers wet-lab mechanisms, analytical frameworks, and algorithmic/bioinformatics logic alike. Common-misunderstanding traps. Blue styling. |
| 6. Applied Methodologies / Workflows | Lab manual or protocol/code/pipeline present, OR practical/OSPE exam | Step → reason-for-step → critical-error point → result interpretation. Covers wet-lab protocols and computational/analysis pipelines. |
| 7. Visual / Data Interpretation | Image/graph/code-based exam, OR user uploaded visuals | Table: item • purpose/function • distinguishing features • expected result • "how it appears in the exam." Covers specimens, plates, gels, graphs, code blocks, maps, diagrams. Keep this machinery available even when dormant. |
| 8. Analytical / Calculations | Quantitative or formula content present (CFU/mL, dilutions, BOD, COD, enzyme activity/units, % solubilization, molarity, Beer–Lambert, yield, statistical tests, etc.) | Formula/framework + every variable defined + ≥2 solved step-by-step examples from the actual sources/past papers + common mistakes. |
| 9. Predicted Exam Questions + Model Answers | Always (unless strict-extract) | Core deliverable. Each tagged HIGH/MEDIUM/LOW with signal justification. Mirror the professor's phrasing; answer to the mark depth. |
| 10. Exam Traps & Common Mistakes | Always | Confused-pair contrasts, unit traps, misread mechanisms. |
| 11. Rapid Revision Sheet | User chose "rapid" or "both" | Ultra-condensed one-pager: memory triggers, mnemonics, must-memorize list, formula strip, top predicted Qs. |

If a triggered section has no real content in the sources, omit it rather than padding.

## Color coding (consistent across HTML and docx)

- 🟣 **Purple** — the professor's *explicit* exam statements, quoted verbatim. Facts, not predictions. Highest priority.
- 🔴 **Red** — Exam Alerts, Traps, HIGH-confidence *predictions*, "we think this is coming."
- 🟢 **Green** — Key concepts / must-know facts.
- 🔵 **Blue** — Mechanisms & frameworks / the WHY & HOW.
- ⚪ **Grey/italic** — Outside-source clarifications (must be visually distinct so the student knows it wasn't from the professor).

**Strict-extract deliverable:** if the user chose "strict extract," output *only* Section 3 (Professor's Explicit Exam Statements) plus a one-line blueprint — no predictions, no synthesis, ultra-condensed. This mirrors the "extract only what the professor explicitly flagged" objective.

## HTML template

Self-contained single file, internal CSS, collapsible sections, sticky clickable TOC. Skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[COURSE] — Exam Master Guide</title>
<style>
  :root{
    --exam:#7c3aed; --exam-bg:#f3edfd;
    --alert:#c0392b; --alert-bg:#fdecea;
    --key:#1e8449;   --key-bg:#eafaf1;
    --mech:#1f6feb;  --mech-bg:#eaf2fd;
    --outside:#6b7280; --ink:#1a1a1a; --line:#e5e7eb; --bg:#ffffff;
  }
  *{box-sizing:border-box} 
  body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:var(--ink);
       max-width:900px;margin:0 auto;padding:24px;line-height:1.55;background:var(--bg)}
  h1{border-bottom:3px solid var(--ink);padding-bottom:8px}
  h2{margin-top:36px;border-left:6px solid var(--ink);padding-left:10px}
  nav{position:sticky;top:0;background:var(--bg);border:1px solid var(--line);
      border-radius:10px;padding:14px 18px;margin:16px 0;box-shadow:0 1px 4px rgba(0,0,0,.05)}
  nav a{display:inline-block;margin:4px 10px 4px 0;text-decoration:none;color:var(--mech)}
  table{border-collapse:collapse;width:100%;margin:14px 0}
  th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
  th{background:#f5f6f8}
  .exam{background:var(--exam-bg);border-left:5px solid var(--exam);padding:10px 14px;border-radius:6px;margin:12px 0}
  .exam blockquote{margin:6px 0;padding-left:10px;border-left:3px solid var(--exam);color:#4c1d95}
  .alert{background:var(--alert-bg);border-left:5px solid var(--alert);padding:10px 14px;border-radius:6px;margin:12px 0}
  .key{background:var(--key-bg);border-left:5px solid var(--key);padding:10px 14px;border-radius:6px;margin:12px 0}
  .mech{background:var(--mech-bg);border-left:5px solid var(--mech);padding:10px 14px;border-radius:6px;margin:12px 0}
  .outside{color:var(--outside);font-style:italic;border-left:3px dashed var(--outside);padding-left:10px;margin:10px 0}
  .tag{font-size:.75em;font-weight:700;padding:2px 8px;border-radius:20px;color:#fff}
  .high{background:var(--alert)} .med{background:#d68910} .low{background:var(--key)}
  details{border:1px solid var(--line);border-radius:8px;margin:10px 0;padding:6px 12px}
  summary{cursor:pointer;font-weight:600;padding:6px 0}
  .qa{border:1px solid var(--line);border-radius:8px;padding:12px;margin:12px 0}
  .marks{float:right;font-weight:700;color:var(--mech)}
  code,.formula{background:#f5f6f8;padding:2px 6px;border-radius:4px;font-family:Menlo,Consolas,monospace}
</style>
</head>
<body>
  <h1>[COURSE] — Exam Master Guide</h1>
  <p><em>[exam type] · Total: [marks] · [date if known]</em></p>

  <nav id="toc"><strong>Contents</strong><br>
    <!-- one <a href="#sec-N"> per active section -->
  </nav>

  <!-- SECTION PATTERN -->
  <h2 id="sec-2">2 · Exam Blueprint</h2>
  <!-- marks table + predicted paper structure -->

  <h2 id="sec-8">8 · Predicted Questions</h2>
  <div class="qa">
    <span class="marks">[X marks]</span>
    <span class="tag high">HIGH</span>
    <p><strong>Q:</strong> [predicted question in professor's style]</p>
    <p><em>Signal: appeared in 2023 & 2024 papers; verbally emphasized.</em></p>
    <details><summary>Model answer</summary>[answer to mark depth]</details>
  </div>

  <!-- Callout examples -->
  <div class="exam">🟣 Professor said (exam): <blockquote>"[verbatim quote]" — [English translation if Arabic]</blockquote>→ points to: [topic]</div>
  <div class="alert">⚠️ Exam alert: …</div>
  <div class="key">✅ Key: …</div>
  <div class="mech">🔵 Mechanism: …</div>
  <div class="outside">[Outside-source clarification: …]</div>
</body>
</html>
```

Fill every `[...]` placeholder. Remove sections that didn't activate and their TOC links. Keep the file fully self-contained (no external assets); embed uploaded images as base64 in `<img>` if the visual-ID section is active.

## Word (.docx) output

If the user picks docx, first read `/mnt/skills/public/docx/SKILL.md` and build with that skill. Map the same color coding to shaded paragraph/heading styles, keep the same section catalog and predicted-question tagging, and use a real Word table of contents. Save to `/mnt/user-data/outputs/`.

## Optional flashcard export

If the user opts in, also produce an **Anki-ready CSV** (`flashcards.csv`): two columns, `Front,Back`, one predicted or key Q/A per row, properly quoted. This is a bonus artifact, not a replacement for a spaced-repetition plugin — mention that and skip it if they already use one.

## Delivery

Save the file to `/mnt/user-data/outputs/` and present it with `present_files`. Keep any closing message short: name the sections built, the top few HIGH-confidence predictions, and what extra source (usually past papers) would most improve the prediction next time.
