---
name: exam-study-guide-predictor
description: >-
  Turn a student's own course material into a two-in-one deliverable: a study
  guide AND a prediction of what the exam will actually ask, optimized for
  marks. Use this skill whenever the user wants to prepare or revise for an
  exam, midterm, final, practical, OSPE, or quiz using their lecture slides,
  professor audio/voice-note transcripts (English OR Arabic), past exam papers,
  model answers, lab/practical manuals, textbook chapters, or class notes — even
  if they just say "help me study for X", "predict my exam", "make me a revision
  guide", or upload lecture files. Built for biology-family courses
  (biotechnology, biology, biochemistry, bioinformatics, chemistry, microbiology,
  molecular biology, and related lab sciences) but adapts to the material given.
  Do NOT use for writing the exam itself, cheating during a live exam, or general
  tutoring unrelated to a specific upcoming assessment.
---

# Exam Study Guide & Predictor

Produce two things at once from the student's **own** course material:

1. **A study guide** — organized for fast recall under time pressure.
2. **An exam prediction** — what will most likely be asked, and how, ranked by evidence.

The objective is **scoring on this specific exam**, not comprehensive mastery. Prioritize what the *professor* and the *past papers* signal, not what a textbook considers important.

## Core principles

- **Source-bound.** Build almost entirely from what the student provides. External knowledge is allowed *only* when a concept is central and repeated across the sources but explained poorly there — and every such addition must be visibly flagged as outside-source (see `references/prediction-and-analysis.md` → "Faithfulness rule").
- **Marks-driven.** Always weight coverage by the mark distribution. A 25-mark topic gets more depth and more predicted questions than a 3-mark one. If you don't know the marks, ask.
- **Evidence-weighted prediction.** Predictions are ranked High / Medium / Low confidence, each justified by *which* signals fired. Past exams are the single strongest signal. Full weighting hierarchy in `references/prediction-and-analysis.md`.
- **Output in English, but read Arabic.** The professor's transcripts may be Arabic (or code-switched Arabic + English technical terms). Parse them, catch spoken exam cues, and integrate their substance into the English output — attributing them as "professor said (verbal emphasis)."
- **Separate fact from inference.** What the professor *explicitly said* is exam material is a **fact** — capture it verbatim (translated if Arabic) and render it in the dedicated **purple** style. What you *predict* is likely is an **inference** — render it in the confidence-tagged prediction section. Never let the two blur; a student budgets revision time differently for "he said this is coming" vs "we think this is coming."
- **Handle large transcripts.** Transcripts can run 100+ pages. Do the explicit-marker extraction pass (below) *first* as a cheap scan, then chunk-read the rest section by section. Do not attempt to reason over the whole document in one pass.
- **Conditional sections.** Never force lab-science machinery (calculations, media-ID tables, specimen photos) onto material that doesn't contain it. Detect what the material is and build only the sections that apply. Keep the machinery available even for image-light courses — activate it when the user says the exam has images/spots/calculations.

## Workflow

### Step 1 — Intake interview (always run this first)

Do not start building until you've asked these. Batch them into one message; let the user answer in bulk or say "you decide." If some answers are already obvious from uploaded files or the conversation, state your assumption instead of asking.

Ask:

1. **Course & discipline** — name of the course/subject.
2. **Exam type** — midterm / final / quiz; and written / practical / OSPE-station / mixed.
3. **Exam format** — which question types: MCQ, true/false, short answer, long/essay, spot-or-photo identification, calculations/problems, diagram labeling, viva. (If they don't know yet, proceed and note the guide isn't format-tuned.)
4. **Total marks & distribution** — total marks and, if known, marks per section or per question type. This drives prioritization — push for it.
5. **Sources they have** — run the source checklist below. Explicitly ask for the two prediction-critical ones if not mentioned: **past exam papers** and **official model answers**.
6. **Deliverable** — one of: study guide, exam prediction, both (default), or **strict extract** (only the points the professor explicitly flagged as exam material — a lean product, no inference).
7. **Depth** — deep no-missing-detail guide, ultra-condensed rapid-revision sheet, or both (full guide + rapid sheet appended).
8. **Output format** — HTML (default; color-coded, collapsible, clickable table of contents) or Word .docx (printable). Ask each time.
9. **Images** — does this exam include photo/diagram/spot identification? If yes, activate the visual-identification section and ask them to upload the relevant images.
10. **Optional flashcard export** — offer (don't force) an Anki-ready CSV of Q/A pairs from the predicted questions. Note it's optional; skip if the user already uses a spaced-repetition plugin.

**Source checklist** (tell them each source's role so they know what's worth digging up):

| Source | Optimizes | Why it matters |
|---|---|---|
| Lecture slides | Study guide + prediction | The exam's ground truth; repetition across slides = signal. |
| Professor audio/voice-note transcripts (Ar/En) | Prediction (strong) | Contains spoken "exam alerts" never written on slides. |
| **Past exam papers** | Prediction (strongest) | Reveals actual question style, recycled items, real depth. |
| Official model answers | Study guide + prediction | Shows expected phrasing and how much earns full marks. |
| Lab / practical manuals | Protocols + calculations + ID | Source for practical-exam workflow and spot questions. |
| Textbook chapters | Study guide | Fills gaps; used cautiously, secondary to slides. |
| Class / classmate notes | Prediction | Captures verbal emphasis the student may have missed. |
| Student's own insider info ("the Dr said…") | Prediction | Treat as high-value verbal emphasis; ask for it. |

After intake, read `references/prediction-and-analysis.md` before doing anything else.

### Step 2 — Ingest and analyze all sources

- **First, the explicit-marker extraction pass.** Before anything else, scan the transcripts and notes for statements where the professor *directly and unequivocally* said something is exam material (Arabic + English cue tables in `references/prediction-and-analysis.md`). Capture each as a verbatim quote (translate Arabic to English, keep the original too), with the topic it points to. These become the **purple** "Professor's Explicit Exam Statements" section and are the backbone of both the strict-extract deliverable and the highest-priority predictions. On large transcripts, do this scan first, then chunk-read the rest.
- Read every provided file fully. For Arabic transcripts, follow the Arabic-cue parsing in `references/prediction-and-analysis.md`.
- Do **not** summarize each source in isolation. Cross-link: theory (slides) → practical step (manual) → how it was asked (past exam) → expected answer (model answer).
- Build an internal signal map of every topic and the evidence weight behind it before writing anything.

### Step 3 — Predict the exam

Follow the full method in `references/prediction-and-analysis.md`: signal weighting, pattern recognition (how *this* professor phrases questions), confidence tagging, and generating predicted questions with model answers that mirror the professor's style and the marks on offer.

### Step 4 — Build the deliverable

Read `references/output-format.md` for the section catalog (which sections activate when), the color-coding rules, and the full HTML/`.docx` templates. Assemble only the sections the material justifies, ordered by the mark distribution.

### Step 5 — Faithfulness & self-check pass

Before delivering, verify: every outside-source insight is flagged; every predicted question cites its signals; the section set matches the material (no empty lab tables on a non-lab course); the highest-mark topics got the most space. Then save the file and present it.

## What good output looks like

- A student can revise from it under time pressure and walk into the exam knowing what to expect.
- Predictions are honest about confidence — no bluffing a Low-signal topic as guaranteed.
- The professor's own words and terminology are preserved, not paraphrased into generic textbook language.
