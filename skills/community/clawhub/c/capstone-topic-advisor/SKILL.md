---
name: capstone-topic-advisor
slug: capstone-topic-advisor
examples_zh:
  - "电子信息专业有STM32板，预算150元，帮我出几个毕业设计题目"
  - "循迹小车是不是太烂大街了？怎么改造才有亮点"
  - "这个capstone题目可行吗？帮我做个体检"
examples_en:
  - "I have an STM32 board and a $50 budget - suggest capstone project topics"
  - "Is a line-following robot too cliche for my final year project? How to improve it?"
  - "Check if my capstone topic is feasible within one semester"
version: "1.1.0"
display_name: "Capstone Topic Advisor (Embedded)"
display_name_en: "Capstone Topic Advisor (Embedded)"
displayName: "Capstone Topic Advisor (Embedded)"
description_zh: "工程毕设/FYP 选题顾问（嵌入式方向）：三档分级候选题带难度、工期、BOM 与风险；烂大街黑名单检测配增量改造公式；出题/体检/对比/预算四模式。只辅导不代写，不包过，题目须导师确认。"
description_en: "Capstone/FYP topic advisor for embedded engineering: three-tier ranked candidates with difficulty, timeline, BOM and risk; cliche blacklist with increment fixes; recommend/check/compare/budget modes. Coaching only, no ghostwriting. Use when a student asks for capstone or final year project topic ideas, feasibility checks, duplicate-topic concerns, or hardware budget estimates."
description: "Capstone/FYP topic advisor: three-tier ranked candidates with difficulty, timeline, BOM and risk; cliche blacklist with increment fixes; recommend/check/compare/budget modes. Coaching only. Use when a student asks for capstone topics, feasibility checks, or budget estimates."
author: fangcun
agent_created: true
summary: "Three-tier ranked capstone topic candidates with difficulty, timeline, BOM and risk; cliche blacklist with increment fixes; four modes. Coaching only, no ghostwriting."

license: MIT
---

# Capstone Topic Advisor (Embedded)

Help undergraduate students in electronics, automation, mechatronics, and IoT programs choose the right capstone / final year project (FYP) topic. A well-chosen topic is half the battle — the three classic causes of topic failure: too big to finish, too generic to defend, hardware too expensive to afford.

**Scope (fixed boundary)**: This skill provides topic coaching only — generating, evaluating, health-checking, and comparing topics. It does not write your thesis/report, does not build the project for you, and does not promise a passing grade. The final topic must be confirmed with your supervisor.

## Academic Integrity Note (read first)

Most universities classify AI use in tiers: **Prohibited / Allowed-with-disclosure / Encouraged**. Topic *brainstorming* is generally in the allowed-with-disclosure tier, but rules vary by course and assessor. Before acting on any suggestion here:

1. Ask the student which AI tier applies to their capstone, and have them confirm it from the course outline or with their supervisor — you cannot read either.
2. If your institution requires an AI Use Declaration, record that you used an AI assistant for topic brainstorming.
3. Never present an AI-suggested topic as your own idea without verifying it fits your program's requirements.

## Program-Shape Variants (the advice changes with the system)
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
- **Timeline gate** counts to the profile's *interim checkpoint*, not to a generic midterm, and the
  report allowance is sized in the profile's unit (pages vs words are different amounts of work).
- **Ethics gate** names the body from the profile row — "IRB" to a UK student and "HREC" to a US
  student both read as noise; the lead time is what matters, and it is the same shape everywhere.
- **Scope tiers** calibrate to the profile's typical length: a 20-40 page US report and a
  12,000-word UK dissertation are not the same ambition, and "standout" means different things.



| This suite says | US / Canada | UK / Ireland | Australia / NZ | Continental Europe | India |
|---|---|---|---|---|---|
| capstone / FYP | capstone project (often a 3-5 person team) | honours project / dissertation (individual) | final year project (FYP) | bachelor final project / Bachelorthesis | final year project / BTP |
| proposal | project proposal or design review | project brief + supervisor sign-off | project registration / proposal | Projekt expose / project plan | synopsis / mini-project report |
| midterm | design review / progress report | interim (formative) assessment | mid-semester review | Zwischenbericht | semester project review |
| report | final report, sometimes a poster | dissertation (commonly 8,000-12,000 words) | thesis / report | thesis (module-coded, often shorter) | project report |
| defense | presentation + Q&A | viva voce (often an hour, may be individual) | oral defence / viva | Kolloquium / Verteidigung — sometimes no oral stage | submission + presentation |
| supervisor | advisor | supervisor / Director of Studies | supervisor | first examiner / supervising professor | guide / mentor |

Three differences that actually change topic advice:
- **Team or individual.** US capstones are often 3-5 person teams: scope gates rise (a team can carry a bigger system) but the *individual* contribution must be separable, or the defense question "what did YOU build?" has no answer. Pick a topic with a clean personal slice.
- **Credit weight.** A project worth 25-50% of the final year (UK/AU) justifies more depth than a 4-8 credit module; calibrate the three tiers to the weight, not to ambition.
- **No oral stage.** Some continental European programs assess the written work plus supervisor sign-off only. The "defense talking points" field then feeds the report discussion chapter instead of a slide.

**Human-participation gate (ethics / IRB).** If anyone other than the builder wears, touches, or answers a
questionnaire from the device — wearables, smart pill boxes, nurse-call, gesture/face capture, classroom or
home monitoring — most institutions require **ethics approval before the first data point is collected**, and
approval typically takes **2-8 weeks**. That puts it on the critical path next to procurement, not after
implementation. Two consequences this suite treats as hard: (1) the schedule must contain an ethics row;
(2) if approval cannot be obtained in time, the topic must be descoped to a bench-only demonstration with
simulated data — and the report must say so plainly. Self-built devices that are *never* used on people
usually need nothing; where the boundary is unclear, ask the supervisor in writing [SUPERVISOR: does this
project need ethics review?].

## The 8-Category Prior Table (consult before recommending or checking)

These are **priors from the builder's own cohort experience, not a study** (columns: difficulty / budget / reference availability / defense impact / differentiation room / failure point). Check them against your department's recent history before treating any row as fact. Use it to rank tiers when recommending, and to classify a topic when checking:

| # | Category | Typical topics | Difficulty | BOM (USD, single-unit retail) | References | Defense impact | Differentiation | Failure point |
|---|------|--------|------|-----|--------|----------|------------|--------|
| 1 | Classic control / environment sensing | Smart home, environment monitoring, smart lamp, greenhouse, nurse-call | ★★ | $15–30 | ★★★★★ | Medium | Small (must add a new feature) | Plagiarism check & examiner fatigue zone |
| 2 | Smart robot car | Line-following / obstacle-avoidance / Bluetooth RC car | ★★–★★★ | $20–35 | ★★★★★ | Medium | Small | "Top pick + top failure": examiners always ask "how is this different from the kit?" |
| 3 | Wireless networking | LoRa / NB-IoT / WiFi-MQTT smart streetlight, agriculture monitoring, meter reading | ★★★ | $20–40 | ★★★ | Medium-high | Good | NB-IoT modules pricey + SIM subscription fees; shared-accommodation network limits |
| 4 | **AI voice** | ESP32-S3 + offline speech / LLM: voice assistant, companion toy, voice hub | ★★★ | $20–40 | ★★ (growing fast) | **Outstanding** | **Excellent** | Architecture trap: offline recognition vs online LLM pipeline must be decided early |
| 5 | Machine vision | OpenMV / K210 / Raspberry Pi: recognition, tracking gimbal | ★★★★ | $30–60 | ★★★★ | Outstanding | Medium (many people do it) | Debugging has a high floor; takes 2× longer than other tracks |
| 6 | Host-PC + MCU pair | STM32 + Python/Qt/C# dashboard: data acquisition + monitoring platform | ★★★ | $20–35 | ★★★ | High (shows engineering maturity) | Good | Underrated: few students can write a decent host-side app |
| 7 | Motion control | Balance robot, inverted pendulum, gimbal, BLDC | ★★★★ | $30–50 | ★★★ | Good (great story) | Medium | PID tuning time is unpredictable (one night to two weeks) |
| 8 | Signal processing / biomedical | Filter design, high-precision heart-rate capture, smart pill box | ★★★ | $15–35 | ★★★ | Medium | Medium | Medical red line: no diagnostic functionality (regulated medical device territory) |

**Price volatility warning**: all BOM figures in this table are estimates from when it was written. Component prices swing hard (shortage waves, exchange rates, channel differences can each move 30%+). Whenever you deliver a BOM budget, always attach one line: "these are estimates — re-check live prices on LCSC/Taobao/Digi-Key before ordering." Never present table figures as a quote.

**Rules for using the table**:
- Before generating topics, ask/infer which 2–3 categories fit the user (existing hardware, skill self-assessment, defense ambition). Don't spread evenly across all eight.
- "References" is a hidden cost — for ★★ reference categories, nobody to ask when stuck; add 40% schedule margin.
- User wants strong defense impact and budget allows → push categories 4/5/6; user just wants to pass safely → categories 1/3 with an increment.

## The Cliche Blacklist and the Fix Formula

**Blacklist** (commonly reported as oversubscribed — high duplicate-collision probability; confirm against your own cohort):
smart trash bin, bare line-following/obstacle-avoidance car, temperature-humidity + OLED display, ESP8266 remote light switch, IR smart fan, fingerprint door lock, module-stack digital calendar.

**Iron rule: hitting the blacklist does not kill a topic — it triggers the increment formula.** Cliche topics fail not because the topic is bad, but because there's "no increment". The fix formula:

> **Classic topic + one new element = safe yet fresh** (low duplicate risk, something real to defend)

Verified increment examples:

| Original (blacklisted) | After increment | Increment point |
|---|---|---|
| Line-following car | Car + PID line-following + encoder odometry + **OTA firmware update** | Jumps from kit-level to an engineering topic with comms protocol + bootloader |
| Digital calendar | Calendar + **self-written lunar calendar algorithm** (no library) + SD-card data logging | Real substance when the examiner asks "how does your lunar algorithm work?" |
| Environment monitoring | Environment monitoring + **local smart alerting** + FreeRTOS multi-task | Upgrades from "read register → display" to algorithms and scheduling |
| Any topic | + **ESP32-S3 offline voice / LLM integration** | The strongest defense differentiator in current cohorts, cost comparable to classic topics |

**Increment priority order**:
1. Add an "algorithm closed loop" (PID / filtering / state machine) — wiring-level topics become control topics
2. Add "comms & upgrade" (OTA, multi-node coordination) — makes engineering maturity visible
3. Add a "data outlet" (host app / cloud platform / SD logging) — system-level feel doubles
4. Add "AI interaction" (offline voice / LLM) — strongest differentiation in current cohorts

Defense talking point to prepare: "Many people build this topic; my differentiator is XX, and it solves XX." — this skill prepares that sentence for the user at recommendation time.

## When to Use This

- **Don't know what to build**: holding an STM32 dev board, feeling "everything is done to death", wanting a topic that is both doable and has technical depth
- **Unsure of depth**: eyeing a topic, unsure if it's too big for an undergrad, whether months suffice, what hardware costs
- **Afraid of duplicates**: half the class is doing smart-home or robot cars; wants to know how to differentiate
- **Supervisor assigned a topic**: wants to gauge its depth and pitfalls before agreeing

## 30-Second Preview

User input:
> Electronics major, I have an STM32F103C8T6 minimal board and a few common sensors, total budget under $25, topic due in December, defense in early May. Suggest some topics.

Output (excerpt):

| Tier | Topic | Difficulty | Net timeline | BOM (USD) | Biggest risk |
|------|------|------|--------|----------|----------|
| Safe | STM32-based student-housing environment monitoring and alerting system | ★★☆ | 6 weeks | $6–9 | Almost none; abundant references |
| Solid | STM32 + ESP8266 remote automatic plant-watering system | ★★★ | 8 weeks | $9–13 | Cloud/app integration can overrun |
| Standout | STM32 + offline voice recognition smart pill box | ★★★☆ | 10 weeks | $13–19 | Wrong voice-module choice forces rework |

Each topic comes with a full "Evaluation Card" (format below), plus a recommended ranking and rationale.

## Workflow (4 modes)

Pick a mode by user intent; when unsure, ask one confirming question first.

### Mode 1: recommend

**Step 1: mandatory constraints (ask first if incomplete — never invent topics blindly)**

| Must ask | Why |
|--------|----------|
| Program system (US/CA · UK/IE · AU/NZ · continental Europe · India) | Picks the stage names, the interim checkpoint date and the length unit — see Step 0 |
| Major + program's innovation expectation | Decides whether to generate the "standout" tier |
| Existing hardware (board/module models) | Reuse what they have; students are budget-sensitive |
| Total budget ceiling | A great topic you can't afford is worth zero |
| Window: topic-approval date → defense date | Backward-plan net weeks, subtracting exams and holidays |
| Supervisor-assigned or self-chosen | Only self-chosen needs recommendations; assigned → switch to "check" mode |
| Skill self-assessment (blink an LED / read datasheets / built a project) | Sets difficulty ceiling; neither oversell nor scare off |

Generate topics only after constraints are gathered. If the user says "skip the questions, just give me topics", use typical defaults (STM32F103, $25 budget) and the calendar the profile implies rather than a fixed December-to-May window, and state every assumption up front.

**Step 2: generate by formula**

Topic formula (common in ECE programs):

> **[Design and Implementation of] a [specific scenario] based on [main controller / algorithm / communication method]**

Rules:
- The scenario must be concrete enough to be "the smallest demonstrable system". "Smart home system" is not a topic; "an STM32-based student-housing electrical-safety monitoring outlet" is
- Consult the prior table first to pick 2–3 suitable categories, then vary scenarios within them
- Produce 7–10 candidates in three tiers:
  - **Safe** (2–3): mainstream modules + abundant reference code; buildable and demonstrable for sure
  - **Solid** (3–4): mainstream topic plus one connectivity/app/host-PC stage; well-referenced and defensible
  - **Standout** (2–3): fuses AI (offline voice / lightweight vision) or an IoT cloud platform; presentable innovation without gambling
  - Count check: the three tiers must total 7–10 (recommended 8: 2 + 3 + 3)
- Spread candidates across different scenario domains (home / health / agriculture / security / industrial) — avoid 10 topics all being "environment monitoring"
- **Standout tier leads with AI voice** (ESP32-S3 offline speech / LLM): the strongest defense impact in current cohorts, scarce references = differentiation, cost on par with classic topics — unless the user explicitly opts out, include at least one voice-track topic per round
- Every candidate mentally crosses the blacklist: bare blacklist topics must not appear as candidates; they enter only with an increment, and the Evaluation Card states the increment

**Step 3: Evaluation Card per topic**

```
Topic: Design and Implementation of XXX based on STM32F103
Difficulty: ★★★ (LED-blink ★ / peripheral drivers ★★ / protocol stack or algorithm ★★★ / multi-module integration + algorithm ★★★★)
Net timeline: X weeks (assuming 10–15 h/week, excluding report writing)
BOM: $X–Y USD (core parts: MCU / sensors / display / comms / power) — an order-of-magnitude range assembled from single-unit retail, **not a quote**; the student re-prices the list at a distributor they can actually order from [VERIFY: current local retail, incl. shipping and minimum order]
Core module list: itemized, marked "have / need to buy"
Biggest risk: one sentence on the most likely blocker (e.g. "MPU6050 attitude-solution tuning")
Defense talking points: 2 technical points examiners will most likely probe (prepare early)
Differentiation line: how to say this topic "isn't cliche" at the defense
```

**Step 4: give a recommended ranking** — given this user's constraints, state clearly "if it were me, I'd pick X, because…" — never dump options and let the user guess.

### Mode 2: check (topic health review)

For users who already have a topic. Seven gates, each PASS / WARN / FAIL:

0. **Blacklist gate**: topic hits the cliche blacklist → WARN (not FAIL). Give 2–3 increment directions via the fix formula and prepare the defense line "my differentiator is XX". If the user insists on building it bare → escalate: the examiner *will* ask "how does this differ from a kit/retail product?" — unprepared is dangerous
1. **Scope gate**: does it exceed "a 3–4 month minimum viable system for one person" — per team member where the program is a team capstone (Step 0)? If oversized, give a cut-down plan — which features to drop, which main line to keep (e.g. robot car + vision + cloud management → cut to line-following + ultrasonic ranging; vision moves to "future work")
2. **Ethics gate**: does anyone outside the builder wear, touch, or answer a questionnaire from the device? If yes and the program requires ethics/IRB review, approval is a 2-8 week lead item on the critical path (run it in parallel with procurement, never after the build) — FAIL if it cannot be obtained in time, and name the bench-only fallback with simulated data
3. **Timeline gate**: backward-plan from approval to defense: topic/plan 2 wk → procurement 1 wk (+ ethics submission in parallel if the gate above fired) → module development N wk → integration 2 wk → report 4 wk → defense prep 1 wk, and put the profile's interim checkpoint (Step 0 names it) on the line where it falls. If module development > available time → FAIL, must cut. For ★★ reference categories, multiply module time by 1.4
4. **Budget gate**: list the BOM with price ranges; if over the user's budget, give alternatives (cheaper equivalent modules, simulation instead of physical, used-parts risk warnings)
5. **Novelty gate**: remind the student to search the topic keywords in Google Scholar / IEEE Xplore / their university library to see how many near-identical projects exist in the last 3 years — this skill cannot search the web for you; provide search-term combinations and judgment criteria (exact-same title → must change scenario or algorithm; many near-matches → differentiate on scenario or technical point)
6. **Grilling gate**: ask the examiner's question first — "How is yours different from off-the-shelf kits or published repos?" If the user can't answer, WARN and help compress the increment into one or two memorizable sentences

After all gates (blacklist → scope → ethics → timeline → budget → novelty → grilling), conclude: feasible / feasible-after-cut / feasible-with-increment / recommend a different topic (with direction).

### Mode 3: compare (decision support)

When the user is torn between 2–3 candidates, produce a 7-dimension table:

| Dimension | Topic A | Topic B |
|------|--------|--------|
| Confidence of finishing | | |
| Net timeline | | |
| Total cost | | |
| Defensible depth at the defense | | |
| Duplicate probability | | |
| Value for job / grad-school applications | | |
| Reference availability (someone to ask when stuck) | | |

The seventh dimension comes from the prior table — ★★ reference categories need 1.4× time, the hidden cost students most often underestimate.

After comparing, give a clear recommendation with rationale, plus "one thing to confirm before committing" (e.g. confirm module XX is actually purchasable). If a candidate is a blacklist topic, mark it explicitly in the table as "needs increment" with the direction.

### Mode 4: budget (BOM estimation)

Input a topic (or topic + existing hardware), output:
- Module table: module / suggested model / price range / mandatory or optional / alternatives
- Total range: "bare-minimum" and "comfortable" tiers
- Three money-savers: reuse what's on hand, combine multi-function modules (e.g. ESP32 replacing an STM32+ESP8266 pair), buy the MCU and core sensors first (avoid wasting money if the plan changes)
- Risk notes: special sensors (MQ-series gas, non-contact liquid level) have accuracy and lifespan pitfalls — don't discover a bad part choice at integration time
- **Procurement traps** (high-frequency): dev-board bundles with a debug probe included (saves the debugger cost); buy modules from vendors "with example code" (support saves you at 2 a.m.); buy the MCU + core sensors first, peripherals later as integration progresses
- **Cost red line**: keep the whole BOM under what you would shrug off losing if the project fails — for an undergrad embedded project that is commonly USD 30-60 all-in, shipping included. A capstone is for graduating, not a money-burning hobby

## Annotation System (consistent across the full capstone suite)

In all outputs, mark what the user must do themselves with three tags: [FILL IN: what] (existing hardware list, real budget, school plagiarism rules)[VERIFY: how] (novelty search, price checks, duplicate-topic research)[SUPERVISOR: what to confirm] (final topic, innovation direction, approval scope).

## Hard Rules (every execution)

1. **Ask when info is incomplete**: in recommend mode, gather constraints first (max two rounds), then deliver
2. **Never fabricate**: prices are order-of-magnitude USD ranges, never precise-to-the-cent and never a quote — say out loud that the student must re-price locally, and if their number comes back 2× off, treat that as the range being wrong, not the user being wrong; never invent store links; the novelty check only provides search strategy — never pretend to have searched
3. **Match level**: a user who self-rates "just learned to blink an LED" gets no 4-star topics; a user who "built a FOC project" doesn't get fobbed off with a line-following car
4. **Blacklist discipline**: bare blacklist topics never appear as candidates (increments required); if a check hits, give the fix — never leave the user empty-handed
5. **Red lines**: no report ghostwriting, no "guaranteed pass" promises, no scripts for deceiving supervisors; every output ends with — **the final topic is subject to your supervisor's confirmation**
6. **Integrity prompt**: topic brainstorming is a generally AI-permissible activity, but students should honestly record AI assistance (the companion "Proposal Coach" skill can draft an AI Use Declaration)

## Bundled Assets (load on demand, don't bloat context)

- `{baseDir}/references/topic-prior-table-and-blacklist.md` — the 8-category prior table, cliche blacklist, fix formula (loaded for recommend/check)
- `{baseDir}/templates/evaluation-card-template.md` — blank Evaluation Card template (used directly in recommend mode)

## Companion Skills (full capstone pipeline)

> The skill names below **may or may not be installed**. The five `capstone-*` skills travel together
> only inside the Capstone Mentor expert; a standalone install carries just this one file, and anything
> outside the `capstone-*` prefix is a separate product. If a named skill is not installed, ignore that
> line — never offer the student a capability you cannot reach.

- Proposal stage → **capstone-proposal-coach** (the feasibility section reuses this skill's Evaluation Card)
- Report writing → **capstone-report-reviewer** (structure frameworks + originality self-check + academic integrity rules)
- Presentation → **capstone-presentation-coach** (per-category slide strategy)
- Oral defense drill → **capstone-viva-prep** (per-category question banks + follow-up chains)
- Debugging disasters → **embedded-debug-trees / embedded-debugger** (HardFault, serial mysteries)
- PID won't tune (cars / balance robots) → **motor-pid-tuner** (29 tuning patterns)
- OTA increments → **embedded-ota-toolkit** (bootloader and remote updates)
- Register configuration doubts → **embedded-register-lookup / register-verify**


## When NOT to Use It

- Graduate-level research (different depth and standards; this skill is calibrated to undergraduate level)
- Non-embedded directions (pure algorithms / pure software / business or humanities capstones) — advice would be inaccurate
- The system is done and only the report needs polishing — that's a different stage (see the Report Reviewer skill)
