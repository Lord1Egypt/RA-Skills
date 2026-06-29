---
name: career-success-predictor
metadata:
  version: 1.0.0
description: Career fit assessment through 10 questions custom-built for a specific occupation. Evaluates how likely the user is to succeed in a target career and produces a short narrative report file. Use this skill whenever the user asks "Am I cut out for X?", "Should I switch careers to X?", "What are my chances of making it as a X?", mentions career assessment, career fit, job success prediction, 我适合做XX吗, 转行成功率, 职业测评 — or expresses any uncertainty about whether a career or job is right for them, even if they never ask for a "test".
---

# Career Success Predictor

Assess the user's odds of succeeding in a target career through 10 tailor-made multiple-choice questions, then deliver a short, story-like report file.

**Language note**: conduct the entire assessment — questions, options, and the final report — in the language the user is speaking.

## Core principles

- **This is a structured self-assessment, not a prophecy.** Results come from self-reported answers. Always present a range (e.g., 55%–70%), never a falsely precise single number.
- **Honest but constructive.** Don't inflate scores to please; don't crush the user either. Name the real weaknesses plainly, but pair every cold splash of water with a walkable path.
- **Measure behavior, not self-image.** Never ask "Are you resilient?" (everyone says yes). Ask about concrete situations and past behavior: "The last time you worked under sustained pressure for two weeks or more, what actually happened?"
- **Separate "fit" from "readiness" to avoid the assessment paradox.** People who seek this assessment usually haven't figured things out yet — that's exactly why they came. If "hasn't decided on a direction" or "hasn't validated anything" subtracts from their success rate, this tool will forever give low scores to precisely the people it serves. Instead:
  - **Fit** (counts toward the success rate): relatively stable traits and objective conditions — behavioral track record of self-discipline, learning, and resilience; available time; financial runway; family support; hard real-world constraints. Answers: "Is this person suited to this path?"
  - **Readiness** (never subtracts from the score; becomes a stage placement and an action plan): clarity of direction, whether anything has been validated, depth of industry knowledge, whether their network is activated. Answers: "How far along are they, and what's next?"
  - Conclusion shape: "Fit is X%–Y%. You're currently at readiness stage N of 4. Once the items below are done, success mostly comes down to execution."

## Workflow

### Step 1: Understand the target career and context

If the user hasn't already said, confirm via AskUserQuestion (or plain conversation):

1. **The target career** — the more specific the better ("frontend engineer" beats "programmer")
2. **Current situation**: student / employed in the field / employed but switching / between jobs
3. **Time horizon**: how soon they hope to make it work (this calibrates the whole assessment)

### Step 2: Design 10 multiple-choice questions for this specific career

Pick the 10 most discriminating angles for this particular occupation from the dimension pools below. **Fit dimensions should fill about 7 questions** (they determine the success rate); **readiness dimensions about 3** (they determine the stage placement and action plan).

**Fit dimensions (count toward the success rate):**

| Dimension | What it measures |
|------|------|
| Core skills | Current level in the occupation's core skills (facts, not intentions) |
| Relevant experience | Direct or transferable experience |
| Learning track record | Actual history of learning new things |
| Personality match | The job's typical working conditions vs. the user's preferences |
| Resilience | Actual past behavior under setbacks |
| Self-management | Track record when nobody is watching |
| Capacity to invest | Weekly available hours, financial runway |
| Family & hard constraints | Family attitudes, health/age/location (only when genuinely relevant) |

**Readiness dimensions (never scored; used for stage placement):**

| Dimension | What it measures |
|------|------|
| Direction clarity | Is the concrete path / income source thought through? |
| Validation | Have they run any cheap real-world test (first client, first artifact, first dollar)? |
| Industry knowledge | Understanding of the real day-to-day vs. the social-media filter |
| Network | Is there anyone in the field they can actually call? |

Question design requirements:

- **Scoring is designed at question-writing time**: for every question, note (to yourself or in a scratchpad) which layer (fit/readiness) and dimension it belongs to, and **pre-assign a score (1–10) to every option**. Scoring happens when you write the questions, not impressionistically after the answers — this is what makes the scores credible.
- **3–4 options per question**, asked via the AskUserQuestion tool **one question at a time**, so the user clicks through like a survey.
- Options describe **concrete behaviors or facts**, never self-ratings. Keep all options neutral in tone — the "right answer" must not be obvious.
- **Favor three high-discrimination question types**:
  1. **Behavioral history** — "The last time you ..., what actually happened?" (past behavior is the best predictor)
  2. **Situational judgment** — pose a real, typical dilemma from this occupation and ask how they'd handle it (tests whether their instincts match the job's demands)
  3. **Objective facts** — savings, available hours, family attitudes: verifiable conditions
  Avoid "do you consider yourself..." intention-statement questions.
- Order questions from light to deep: question 1 should be easy (e.g., experience); motivation and resilience belong in the middle-to-late stretch.
- Prefix each question with progress, e.g. "[3/10]", so the user knows how many remain.
- You may adapt later questions based on earlier answers for sharper assessment. If the framework or the target career changes midway, **write fresh questions** — never force old answers into a new frame.

### Step 3: Scoring

**Fit score** — the discipline below is for you (the assessor), to keep conclusions from being hand-waved; but **do not put the math into the report** (see Step 4 for why):

1. Each fit dimension's score = the value pre-assigned to the chosen option (1–10)
2. Weights reflect the occupation (e.g., "age/physical" weighs heavy for pro athletes; "personality match" weighs heavy for sales). Weights sum to 100%.
3. Midpoint = weighted total × 10 (e.g., weighted total 6.2 → midpoint 62%)
4. Range = midpoint ±5–8 points (reflecting self-report uncertainty; the more contradictions among answers, the wider the range)
5. **Veto items**: when a critical dimension scores ≤3 (e.g., zero available time; family firmly opposed with no room to negotiate), it must not be averaged away by high scores elsewhere — cap the range's upper bound below the midpoint, and let the report convey that weakness's true weight through the narrative.

If the user asks in conversation "how was this percentage computed", then show the method honestly, and explain that it expresses their match against "the typical profile of people who succeed in this occupation" — not a statistical probability.

**Readiness placement**: readiness dimensions are never scored. Place the user at one of four stages:

1. **Exploring** — direction undecided; knowledge mostly secondhand
2. **Validating** — direction tentatively set; running (or about to run) cheap tests
3. **Building** — validation done; now stacking skills, portfolio, and network
4. **Ready to launch** — validated and past the objective threshold to start

If the user's time horizon clearly mismatches their stage (e.g., Exploring but wants to launch in 3 months), say so directly in the report and offer a realistic timeline.

### Step 3.5: Incremental evidence (triggered only when needed)

Try to score after the 10 questions. If any of the following holds, the evidence is too thin for a sharp verdict — **don't rush the report**; invite the user to add information:

- Most dimension scores cluster mid-band (5–6) with no standout strength or weakness — a blurry picture
- Key answers contradict each other (e.g., claims poor self-discipline yet shows a long record of sticking with things)
- The weighted midpoint lands in the mushy 45%–60% zone where any range reads as fence-sitting

Two sources of extra evidence, requested via AskUserQuestion:

1. **Established assessments the user has already taken**: ask whether they've done MBTI, Big Five, Gallup StrengthsFinder (CliftonStrengths), Holland codes (RIASEC), DISC — which ones, and what the results were. Respect the differences in scientific validity:
   - **Big Five**: best academic standing; neuroticism/conscientiousness correlate measurably with job performance — safe to use as corroboration
   - **Holland, Gallup**: useful for interest and strengths orientation
   - **MBTI, DISC**: popular but low test-retest reliability — weak corroboration only; never hang a major conclusion on them
2. **Follow-up questions on the blurriest dimensions**: write 1–2 fresh behavioral-history or situational-judgment questions from a different angle for the 1–2 fuzziest dimensions.

**Usage rule**: incremental evidence only **adjusts range width and lean** (e.g., narrowing a fence-sitting 55%±8 to 57%±5). It can never override direct evidence from the user's own behavioral history — what a person has actually done always outweighs any test label. Note in the report which conclusions drew on external assessments.

### Step 4: Generate the report file

First give the core verdict briefly in conversation (range + one-line characterization), then generate the report file.

- **Prefer .docx**: if a docx skill is available, read it first and follow its method; otherwise produce a well-formatted .md or .html file.
- Put the career in the filename, e.g. `Frontend-Engineer-Career-Fit-Assessment.docx`.
- Present the file via present_files (if available).

**The soul of the report is storytelling, not auditing.** The people who take this assessment are mostly in a foggy stretch of life. What they need is a knowledgeable friend telling them their own story back — not a cold score sheet. Writing requirements:

- **Readable in 3 minutes**: body text (excluding any appendix) within roughly 600–900 words. This is discipline, not laziness — anxious people don't finish long reports. Keep only the single most striking stroke per dimension and cut the rest. Better to leave the reader wanting more than to lose them halfway.
- **The first two lines set the frame**: open with one or two sentences that deliver the verdict outright (fit or not, what odds, what's the bottleneck), then follow with one philosophical line tailored to this person — not a recycled famous quote, but something distilled from their own answers that makes them pause (e.g., for the hype-chaser: "A tailwind can lift you off the ground, but the landing is always on your own legs").
- **Second person throughout** — a letter written to them, unhurried and direct.
- **Use their real answers as narrative material.** Not "you scored 7 on resilience," but "you said three months of no income would keep you up at night — and you still wouldn't quit. That 'scared but steady' state happens to be the most common trait among the people who survive in this field." Weave the 10 answers into one coherent portrait; let the user feel seen.
- **Almost no lists or tables in the body.** Flowing paragraphs. Section headings should read like chapter titles, not field names — "The most valuable thing you carry," not "Strengths analysis."
- **Warm but unambiguous conclusions**: weave the fit range and readiness stage naturally into the narrative; pour the cold water that needs pouring (e.g., unrealistic timelines), but follow every splash with a walkable path.
- **Advice concrete enough to act on tomorrow**, woven into the story ("next week, take that friend you know but never really talked to out for coffee, and ask three questions: ..."), never generic filler like "improve your skills and network."

Narrative skeleton (rewrite the section titles to be more vivid and personal for each user):

```
# To you, who wants to become a [career]

[Opening] One or two sentences with the straight answer: suited or not,
what odds, what's the bottleneck. Then one tailored philosophical line.
Never make the reader wait for what they care about most.

[Who you are] The portrait assembled from their 10 answers — strengths,
soft spots, contradictions they may not see themselves. Only the two or
three most striking strokes.

[What this path is really like] The occupation's real day-to-day vs. their
mental image. Calibrate expectations gently.

[Your odds] The fit range and the reasoning, argued in prose rather than
bullet points — and what would move the number.

[The road from here] The next 1/3/6 months written as a continuous script,
not a checklist, matched to their readiness stage.

[One last thing] A sincere close. Remind them this is a reference built
from self-report, not a verdict on their life.
```

**No score table in the report.** The numerical rigor happens backstage (Step 3's discipline); what reaches the user is a warm, considered judgment. A score table invites the user to litigate "why only 5 on this row" and breeds distrust. At its heart, what this report hands the user is an answer for the soul: to be seen, to be understood, and to know where to step next.

## Edge cases

- Target career too broad (e.g., "business") → help the user narrow to something concrete before starting.
- User switches target career midway → confirm, then write fresh questions; generic answers already given may be reused.
- High-stakes transitions (e.g., quitting with no fallback) → in the action plan, stress validating before betting big. Never make major life decisions for the user.
- User unhappy with a low result → explain the basis, emphasize that weaknesses are fixable: this is a starting-point assessment, not a final judgment.
