# Prediction & Analysis Method

This is the intellectual core: how to reverse-engineer what the exam will ask and how confident to be. Read after intake, before building output.

## 0. Explicit-marker extraction pass (run first)

Before weighting anything, scan transcripts and notes for statements where the professor *explicitly and unequivocally* flagged exam material. This pass produces **facts**, not inferences, and feeds the purple "Professor's Explicit Exam Statements" section.

For each hit, capture: the verbatim statement (original Arabic *and* an English translation if spoken in Arabic), the exact topic/concept it points to, and the source location (which lecture/slide). Do not paraphrase away the professor's wording — the point is fidelity.

**Large transcripts (100+ pages):** run this scan first as a lightweight pass over the whole file, logging hits with their line/section, then chunk-read the rest of the document section by section for the deeper synthesis. Never try to hold the entire transcript in one reasoning pass.

**Purple vs red — keep them distinct:**
- **Purple** = the professor literally said this is on the exam. A *fact*. Highest study priority, quoted.
- **Red** = a HIGH-confidence *prediction* (from past papers / convergent signals) or an exam trap. An *inference* or a warning.

A topic can be both (professor flagged it *and* it's in past papers) — show the purple statement and the red prediction together.

## 1. Signal-weighting hierarchy

Rank every candidate topic by the evidence behind it. Signals from strongest to weakest:

1. **Past exam papers (strongest).** If a topic, question stem, or figure appeared in a previous paper, weight it heavily. Professors recycle and lightly rephrase. Note whether the item repeats across *multiple* past papers — a recurring past question is close to a guarantee. Track the exact phrasing; predict the rephrase.
2. **Official model answers.** Reveal the depth and wording that earn full marks. If a model answer is long/structured, the exam expects a long/structured answer.
3. **Repetition across the slides.** A concept restated on many slides, or given its own summary/objectives slide, is emphasized. Count the repetitions.
4. **Professor verbal emphasis (transcripts / notes).** Explicit spoken exam cues — see the Arabic + English cue tables below. Treat "this is important for the exam" as a near-guarantee even if the topic looks minor on the slides.
5. **Student-provided insider info.** "The Dr said the calculation is coming" — treat as high-value verbal emphasis. Always ask the student for this.
6. **Textbook prominence (weakest).** Only relevant if it aligns with a higher signal. Do not predict something *just* because a textbook stresses it — the professor may not.

**Combining signals:** a topic backed by multiple independent signals (e.g., in a past paper AND verbally emphasized AND repeated on slides) is the highest-priority prediction. Isolated single-signal topics are lower confidence.

## 2. Confidence tagging

Every predicted question carries a tag with a one-line justification naming the signals:

- 🔴 **HIGH** — appeared in past exam(s), or explicitly flagged by the professor as exam material, or multiple strong signals converge. Phrase these as "expect this."
- 🟡 **MEDIUM** — repeated across slides/lectures or single verbal emphasis, but not confirmed by a past paper. "Likely."
- 🟢 **LOW** — plausible from the syllabus/marks but weak signal. "Possible; cover if time allows."

Never inflate confidence. A student allocating scarce revision time is relying on this being honest.

## 3. Reverse-engineering the professor's question style

Before writing predicted questions, extract the *pattern* from past exams + model answers:

- **Question stems** the professor favors ("Compare…", "Explain the mechanism…", "Given the following data, calculate…", "Identify the organism/medium in the photo and justify…").
- **Depth expected** — do short-answer questions want 2 lines or 10? Infer from model answers.
- **Recurring structures** — e.g., every paper has one calculation, one diagram-ID, one compare/contrast. Predict the *slots*, then fill them with this year's likely content.
- **Distractor style** for MCQs — how the professor builds wrong options (common misconceptions, near-synonyms, unit traps).

Then generate predicted questions that mirror this style and phrasing, each with a model answer written to the depth the marks imply (a 2-mark answer ≠ a 10-mark answer).

## 4. Parsing professor transcripts (Arabic & code-switched)

Transcripts are often spoken Arabic with English technical terms mixed in. Read them for meaning, then surface spoken exam cues. Output stays English; attribute as "professor's verbal emphasis."

**Arabic exam-cue phrases to scan for** (dialectal variants included):

| Arabic cue | Meaning | Treat as |
|---|---|---|
| ده مهم للامتحان / دي مهمة في الامتحان | this is important for the exam | HIGH signal |
| هييجي في الامتحان / ده جاي / متوقع ييجي | this is coming in the exam | HIGH signal |
| ركزوا على / خدوا بالكم من | focus on / pay attention to | HIGH/MEDIUM |
| لازم تعرفوا / لازم تعرفوا دي | you must know this | HIGH signal |
| متوقع سؤال / في سؤال على ده | expect a question on this | HIGH signal |
| احفظوا / دي محفوظة | memorize this | must-memorize |
| ده أساسي / دي نقطة أساسية | this is fundamental / key point | MEDIUM/HIGH |
| النقطة دي مهمة | this point is important | MEDIUM |
| اللي فات ده مش مهم / سيبوا ده | skip this / not important | de-prioritize |

**English cues** (for English transcripts): "important for the exam," "this will be on the test," "you must know this," "expect a question," "key concept for the exam," "focus your study on," "the most critical part here for the exam is," "guaranteed," "exam alert."

When a cue fires, capture: the exact topic it points to, translate/paraphrase the professor's statement into English, and log it as a prediction signal with its topic linked back to the relevant slide.

## 5. Faithfulness rule

- Default: build only from the student's sources; preserve the professor's exact terminology, naming, and phrasing (do not "correct" it into standard textbook language — the exam grades *their* terms).
- Outside knowledge is permitted **only** when a concept is (a) central to the material and (b) mentioned/repeated by slides or professor but explained too poorly to study from. In that case add the minimum clarification and mark it explicitly, e.g. `[Outside-source clarification: …]` in the HTML "outside" style. Never let external content dominate a section or introduce topics the professor never raised.
- If asked to verify a fact against the live web, do it only on explicit request; by default web search is OFF because the exam tests the professor's material, not the literature.
