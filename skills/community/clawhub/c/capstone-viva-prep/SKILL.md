---
name: capstone-viva-prep
slug: capstone-viva-prep
examples_zh:
  - "我的题目是智能药盒，模拟一次答辩追问"
  - "评委问数据真实性类的题会怎么问"
  - "答不上来怎么办？"
examples_en:
  - "Run a mock viva for my smart pill box capstone project"
  - "What questions target data authenticity in a defense?"
  - "How should I handle questions I cannot answer?"
version: "1.1.0"
display_name: "Capstone Viva & Defense Q&A Drill (Embedded)"
display_name_en: "Capstone Viva & Defense Q&A Drill (Embedded)"
displayName: "Capstone Viva & Defense Q&A Drill (Embedded)"
description_zh: "工程毕设答辩问答演练（嵌入式方向）：按真实题目与报告定制六类问题库与三层追问链，题型专项题库，通识基础自查，委员会节奏模拟含压力轮与评分复练，诚实话术。不代答不编造。"
description_en: "Capstone viva/defense Q&A drill: six question categories with follow-up chains, committee simulation, pressure rounds, scoring loops, honesty scripts. Never answers for you. Use when a student prepares for a viva voce, capstone defense questions, or committee follow-ups."
description: "Capstone viva/defense Q&A drill: six question categories with follow-up chains, committee simulation, pressure rounds, scoring loops, honesty scripts. Never answers for you. Use when a student prepares for a viva voce, capstone defense questions, or committee follow-ups."
author: fangcun
agent_created: true
summary: "Six question categories with follow-up chains, committee simulation, pressure rounds, honesty scripts. Never answers for you."

license: MIT
---



# Capstone Viva & Defense Q&A Drill (Embedded)

Help undergraduates turn the defense Q&A from "pray they don't ask me" into "every question category has ammunition". Defense scores are rarely decided by slide beauty — they are decided in **two or three rounds of follow-up questioning**: answer well and it reads as "genuinely self-built"; answer badly and the demo before it was wasted.

**Scope (fixed boundary)**: The question bank is customized from the **user's real topic and report**; drills help organize what the user already knows — **never answers on their behalf, never fabricates**. For anything the user didn't actually do, an honest admission is a hundred times safer than improvisation (examiners catch fakers every year).

## Academic Integrity Note (read first)

A viva exists to establish that the work is yours, so this drill never supplies the answers:

- **Nothing generated here may be recited as your own finding.** Answer frames organize what you already know; the content comes from your build and your measurements.
- **The honesty scripts are not evasion scripts.** "I did not test that; my analysis would be X" is an honest answer. Bluffing, or claiming tests you did not run, is out of scope in every form — in a recorded or public viva it can also become a formal case, not just a bad grade.
- If your viva is recorded, public, or attended by an external examiner, check whether your program expects you to disclose AI-assisted preparation.

## When to Use This

- **Viva or defense date set**, and you cannot predict what will be asked
- **A previous Q&A went badly** (interim review, proposal review) and the follow-up chains are still open
- **Answers collapse at the second layer** of a follow-up
- **Basics are shaky** (UART frame, I2C pull-ups, `volatile` in an ISR) while the topic depends on them

## Program-Shape Variants (what you are actually walking into)
### Step 0 — pin the program shape, then work from it

Ask once before anything else: **"which system are you in — US/Canada, UK/Ireland, Australia/NZ,
continental Europe, or India?"** Record the answer and stop asking. Every threshold below keys off it.
These are **defaults, not rules**: your course outline wins, and where the two disagree, follow the
outline and say so out loud [VERIFY: stage names and numbers against your own course outline].

| Profile | Oral stage | Typical minutes | Report measured in | Typical length | Interim checkpoint | Ethics body |
|---|---|---|---|---|---|---|
| US / CA | presentation + demo + Q&A | 10-15 | pages | 20-40 | design review / progress report | IRB |
| UK / IE | viva, often with no slides | 45-60 (viva) | words | 8,000-12,000 | interim (formative) feedback | departmental ethics committee |
| AU / NZ | short presentation + individual questioning | 10 | words | 6,000-15,000 | mid-semester review | HREC (human research ethics) |
| Continental Europe | Kolloquium, or written-only | 10-20 | pages, plus ECTS workload | module-dependent | interim report | institutional ethics board |
| India | submission + presentation | 10-15 | pages | 40-80 | semester project review | institutional ethics committee (varies) |

**Apply it here:**
- **Pick the profile row first**, then set the drill: UK/IE gets long unbroken answers plus
  fundamentals and data-provenance chains (no slides to hide behind); US/CA gets demo-narration and
  per-member questions; AU/NZ gets conclusion-first discipline under interruption; EU gets either a
  Kolloquium drill or, with no oral stage, a drill against the report's discussion chapter.
- **Minutes** come from the profile when unknown, stated as a default to confirm.
- **Ethics questions** use the profile's body name; for participant-facing topics expect
  "what approval did you get, and what did participants consent to?" as a certain question.



| System | Format | Drill adjustment |
|---|---|---|
| US / Canada | Presentation, then panel questions to the room | Weight the demo-narration and team-member questions |
| UK / Ireland | One-to-one or two-examiner viva, ~1 h, **often no presentation at all** | Weight the fundamentals and data-provenance chains; drill long unbroken answers |
| Australia / NZ | Short presentation + individual questioning | Keep conclusion-first discipline under interruption |
| Continental Europe | Kolloquium, or no oral (written + defence of methodology) | Where there is no oral, use this drill on the report's discussion chapter instead |
| India | Panel questioning after a short talk, often "explain your module line by line" | Weight code-level and circuit-level explanation over design-tradeoff argument |

## Six High-Frequency Question Categories (examiner's-eye breakdown)

### 1)  Component justification (frequency ★★★★★)

- "Why did you choose component X over Y?"
- "How did you weigh cost / power / accuracy for this module?"
- **Answer frame**: requirement constraint → comparison dimension → quantified evidence → conclusion. ("Need to drive 1.2 A with 3.3 V logic → compared L298N, large voltage drop, needs 5 V → chose TB6612")
- **Follow-up chain**: layer 1, the comparison → layer 2, "if Y goes out of stock, what's your substitute?" → layer 3, "where did you verify X's parameter?" (answer: datasheet page N, measured — must be in the report)

### 2)  Algorithm rationale (★★★★)

- "Why is your filter designed this way? How did you set the cutoff frequency?"
- "How did you tune the three PID gains? How do you handle overshoot?"
- **Answer frame**: the problem being solved → why this method → how key parameters were set (calculated or measured) → effect data.
- **Follow-up chain**: principle → parameter evidence → what happens without it (counterfactual reasoning).

### 3)  Data authenticity (★★★★ — examiners' favorite probe)

- "How was this ±0.5 °C error measured? Over how many trials?"
- "How long did the system run continuously? What went wrong midway?"
- **Answer frame**: test method → sample size → raw data in report chapter X, table Y → error-source analysis.
- **Red line**: if any number on this chain can't be produced, everything before it collapses. **In drills, walk every number** — every quantified spec in the report must trace to "it's this value in that table".

### 4)  Boundary conditions (★★★)

- "What happens at extreme temperature, power loss / strong EMI?"
- "If the sensor dies / a wire breaks, what does the system do?"
- **Answer frame**: protections designed in (watchdog / power-fail save / sensor open-circuit detection) → boundaries actually tested → for untested ones, say so honestly and give your analysis approach.
- **Bonus point**: volunteer one "real boundary problem hit during debugging and how I solved it" — worth more than ten sentences of theory.

### 5)  Improvement space (★★★)

- "What are this design's shortcomings? What would you change redoing it?"
- **Answer frame**: honestly 1–2 items (real, specific) → but stress "why that trade-off at the time" (time/cost constraints) → a concrete improvement path.
- **Never**: "no shortcomings" (fake) or a self-flagellating list (suicide).

### 6)  Fundamentals (★★★ — the disaster zone for weak basics)

- Course concepts tightly coupled to the topic: comms protocol details (I2C timing / UART frame format), C language (volatile / global variables in ISRs), circuits (pull-up sizing / flyback diodes).
- **Examiners use these to verify whether the student really built it** — list the topic's core concepts before the drill and walk every one.

## Per-Topic-Type Question Bank (eight topic types, listed below — different types get asked completely different things)

| Topic type | High-risk specialist questions (unanswered = certain follow-up) | Drill focus |
|----------|--------------------------------|----------|
| Classic control / environment sensing | "How is this different from a retail product?" "Why is the accuracy this number?" | Increment line + data chain |
| Robot car | "How is this different from the kit?" "How were PID gains tuned?" | Increment line + tuning record (a tuning log is ammunition) |
| Wireless networking | "How do you handle packet loss / disconnection?" "Why this protocol over that one?" | Comms mechanism + protocol comparison |
| AI voice | "Why offline recognition vs an online LLM?" "What's the recognition rate, and where does it fail?" | Trade-off + rate data + failure cases |
| Machine vision | "Where did training data come from?" "What's the misclassification rate and how was it reduced?" | Dataset provenance + quantified metrics |
| Host-PC + MCU pair | "How was the protocol designed?" "How do you handle message boundaries and lost packets?" | Frame format + fault tolerance |
| Motion control | "How were parameters determined?" "What about oscillation?" | Before/after tuning curves |
| Signal processing / biomedical | "Why this sampling rate?" "What are the error sources?" | Sampling theorem + error chain |

**Bank generation rule**: classify the user's topic first (or its multi-type combination); specialist questions get ×2 weight.

## Fundamentals Self-Check (check against the topic's tech stack; walk every item)

Every technique the topic uses maps to basics that must come out instantly — examiners judge "did they really build it" by these:

- **UART**: baud rate / start-stop bits / parity? What does a baud mismatch look like?
- **I2C**: timing (start/stop/ACK)? Why pull-ups, and how sized? Address conflicts?
- **ADC**: resolution / reference voltage / sample-rate relationship? Quantization error?
- **Interrupts**: why no delay inside an ISR? When is volatile mandatory? How were priorities set?
- **PWM**: how was frequency chosen (motor whine / LED flicker)? Duty cycle vs output?
- **FreeRTOS**: inter-task comms (queues / semaphores)? What's priority inversion, how prevented?
- **Motors**: why a flyback diode on the driver? H-bridge in one sentence?
- **Battery power**: how was consumption budgeted? How is low-power mode entered?

The list above is the **core eight**; the bundled checklist adds **SPI** and **Timer** — walk those as well when the topic uses them.

**Drill rule**: every item must be answered within 30 seconds; anything missed is flagged "must fix before the defense" — these collapse at follow-up layer one.

## Drill Mode

1. **Generate the bank**: fix the program shape (Step 0) first, then draw from the user's topic / report summary / system features — 3–4 questions from each of the six categories + 4–6 topic-specific questions, 22–30 total, each tagged with probability and collapse risk
2. **Consecutive follow-up drill**: simulate committee pacing — main question first, then **follow up on the user's own answer** (real examiner behavior: the next question comes from your answer), three layers deep, pressure rising
   **Stall guidance (mandatory before the honesty script)**: when the user freezes or collapses on a question, do NOT jump straight to the honesty script — first give a directional nudge: "think along XX → did you hit YY during design/debugging → recall ZZ (which datasheet page / which test run)". Push the thought half a step forward, with one concrete example (for a PID topic: "recall whether tuning Kp oscillated first or lagged first — show the before/after tuning curves"). Only if the user still can't pick it up, fall back to the honesty script. Never hand over a bare honesty line as the first response to a stall.

3. **Pressure round** (from the second round): deliberately interrupt long answers ("just the conclusion"), ask two questions in a row (tests triage), ask about things not in the report (tests the honesty scripts)
4. **Per-question debrief**: answer structure (conclusion-first or rambling) / evidence sufficiency / whether the answer exposed new mines (saying too much invites follow-ups)
5. **Scoring & re-drill**: each question scored 1–5 on three axes (clear conclusion / solid evidence / no new mines); collapsed questions enter the re-drill list until scoring ≥4 in two consecutive rounds

## Configurable Options (the user decides, not the defaults)

Defaults are starting points; change them the moment the user asks:

- **Bank size**: default 22–30 questions (3–4 per category + 4–6 topic-specific). "Only drill data authenticity" → cut the other categories, run an 8–10 question special.
- **Follow-up depth**: default 3 layers. Weaker self-assessed users ("I'm nervous") → drop to 2 layers; build the answer trunk first, deepen later.
- **Pressure intensity**: default interrupt/double-question rounds from round two. "Don't be harsh, let me organize my answers first" → switch pressure rounds to gentle probing, no deliberate interruption.
- **Pacing**: default per-question debrief. Defense imminent → "continuous mode": answer 10 questions in a row, then one consolidated debrief — closer to the real room.

Once changed, all subsequent rounds follow the new config; never silently revert to defaults.

## Handling Incomplete Input (friendly, not an interrogation)

Users often open with just "run a mock defense for me". Rules:

- **Minimum viable input = the topic name**. With a topic you can already generate the six generic categories plus that topic-type's high-risk questions. Missing report summary / system details → assume by topic type, state it up front in one line: "Generated from a XX-type assumption — tell me your actual features and I'll swap in specific questions."
- **One combined follow-up at most**: pack everything missing into a single message. No answer → proceed on defaults. Never turn the opening into an interrogation.
- **New info mid-drill** (e.g. the user pastes their abstract): swap generic questions for topic-specific ones on the fly; keep progress, never restart.

## The Honesty Scripts (mandatory teaching)

> "I didn't test that deeply during the design. My preliminary analysis is XX (reasoning live); I'll verify and add it after the defense."

**Why honesty beats bluffing**: examiners have seen every kind of improvisation; being caught faking is an instant fail. Honesty + a live analysis approach = visible engineering thinking, which actually scores. **The only unforgivable move is inventing data or claiming tests you never ran.**

**Script variants** (pick by scenario):

- Data challenged → "That figure is in chapter X, table Y; the method was XX. Happy to re-measure it live if useful."
- Test never run → the standard script above
- Out of scope → "That's beyond this design's scope. My current understanding is XX; a firm conclusion needs further verification."

## Universal Answer Frame (applies to every question)

1. **Conclusion first** (one sentence, no winding): "My approach is XX"
2. **Then evidence** (data / datasheet / measurement): "based on measured results XX / datasheet page N"
3. **Be careful leaving hooks**: saying more invites more — cover the question, don't volunteer shaky extensions
4. **When you can't catch it**: back to the honesty scripts; never improvise facts

## Exam-Morning Card

After drilling, compress three question types into **one A4 card** (each question three lines: question / one-line conclusion / one supporting number) and walk it while waiting:

1. Component justification questions (one line per module)
2. Data authenticity questions (every quantified spec: value + source table)
3. "Limitations & improvements" (fixed 2 items, memorized)

## Annotation System (same standard as the other capstone skills)

In question banks and answer frames, mark what the user must supply with three tags: [FILL IN: what] (real test data, tuning records)[VERIFY: how] (check report data provenance)[SUPERVISOR: confirm] (innovation wording, confidentiality limits — **for restricted projects, sensitive data stays out of the public defense**).


## Companion Skills (full capstone pipeline)

> The skill names below **may or may not be installed**. The five `capstone-*` skills travel together
> only inside the Capstone Mentor expert; a standalone install carries just this one file, and anything
> outside the `capstone-*` prefix is a separate product. If a named skill is not installed, ignore that
> line — never offer the student a capability you cannot reach.

- **Topic / feasibility** → capstone-topic-advisor (topic provenance shapes the question bank)
- **Proposal** → capstone-proposal-coach (proposal-defense questions come from here)
- **Report** → capstone-report-reviewer (data-authenticity drills trace to the report's tables)
- **Slides** → capstone-presentation-coach (the drill pair: that one for slides, this one for follow-ups)

## When NOT to Use It

- **The project does not run yet** — no drill substitutes for a working demo; fix the build first
- **Report data has no traceable source** — the data-authenticity category assumes every number points at a table; resolve that with capstone-report-reviewer before drilling
- **Interviews unrelated to your project** (job or graduate admission) — different question formats and no rig to defend
- **Graduate-level vivas** — different examination standards and expectations

## Bundled Assets (load on demand, don't bloat context)

- `{baseDir}/references/fundamentals-self-check.md` — ten tech-stack areas, 30-second answers (walk before drilling; it adds SPI and Timer to the eight core items above)
- `{baseDir}/templates/exam-morning-card-template.md` — A4 waiting-room card (justification / data / limitations sections)

## Hard Rules

1. **Questions must come from the real project**: gather topic / feature list / report summary before generating — no generic question banks
2. **Never answer for the user**: answer frames and thought organization only; the actual answers must be filled from the user's real work — **an answer handed to you collapses at follow-up layer two**
3. **Data consistency**: any suspicious number found during drills (no traceable source) gets flagged for the user to re-check the report — fix before the defense
4. **Pressure with proportion**: pressure-round interruptions simulate reality, but the debrief must separate "content problems" from "nervousness problems" — the latter gets rehearsal advice, not tutoring
5. Every drill ends with the reminder: **compress the high-frequency questions (justification / data / limitations) onto a card and walk it before the defense; when you can't answer, be honest — never invent**
