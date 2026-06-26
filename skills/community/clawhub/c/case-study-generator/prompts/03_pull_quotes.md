# Prompt 3: Pull Quotes & Testimonial Extraction

## Purpose
Pull quotes are the most-repurposed element of any case study. Sales reps paste them in emails. Marketing puts them on landing pages. Ad teams use them in retargeting. This prompt generates 5 quotes targeting different buyer stages and objections, plus a testimonial block and a one-liner for ads.

---

## Prompt

```
You are a B2B copywriter specializing in social proof and testimonial copy. 

Using the case study narrative and customer details below, write the following:

---

**SECTION A: 5 Pull Quotes (for case study + sales collateral)**

Write 5 distinct quotes from the customer's perspective, each targeting a different buyer stage or objection. Format each as:

> "[Quote — 1–3 sentences. Specific, personal, and in the customer's voice.]"
> — [Customer Name], [Title], [Company]

**Quote 1 — The Problem Recognition Quote**
Target: Buyers who are still in denial that they have the problem.
Tone: "We didn't realize how bad it was until..."
Goal: Make the reader identify with the pre-solution pain.

**Quote 2 — The Decision Confidence Quote**
Target: Buyers in evaluation mode who fear making the wrong choice.
Tone: "What gave us confidence was..." or "We compared several options..."
Goal: Address evaluation anxiety, validate the decision process.

**Quote 3 — The Implementation Quote**
Target: Buyers worried about disruption, onboarding complexity, or IT lift.
Tone: "We were up and running in..." or "The rollout was..."
Goal: Remove the "this will be painful to implement" objection.

**Quote 4 — The Results Quote**
Target: Buyers who need proof from someone like them.
Tone: Hard numbers, specific outcomes. The CFO quote.
Goal: Give procurement/finance the proof they need to approve the spend.

**Quote 5 — The Advocate Quote**
Target: Buyers who will share this with their team.
Tone: "I tell everyone I know..." or "If you're on the fence..."
Goal: Create word-of-mouth trigger. This is the quote that gets forwarded.

---

**SECTION B: 3-Sentence Email Testimonial**

Write a polished 3-sentence testimonial suitable for:
- Website testimonial section
- Sales email signature
- Case study PDF header

Format: 
> "[Sentence 1: the problem they had]. [Sentence 2: how the solution worked]. [Sentence 3: specific result + recommendation]."
> — [Name], [Title], [Company]

---

**SECTION C: One-Line Social Proof Snippet**

Write 3 variations of a one-line quote (under 15 words each) suitable for:
- Google/Facebook ad copy
- Homepage hero subheading
- Slide deck proof point

Each should be punchy, specific, and stand alone without context.

---

INPUTS:
- Customer name/title/company: [NAME, TITLE, COMPANY]
- Key result (most impressive metric): [METRIC]
- The core problem they had: [PROBLEM]
- The moment it clicked for them: [TURNING POINT — or write "not specified"]
- Any real quotes they provided: [QUOTE — or write "generate all quotes"]

TONE GUIDELINES:
- Sound like a real human, not a PR department
- Each quote should have a slightly different voice (analytical, relieved, enthusiastic, cautious)
- Avoid generic superlatives: "amazing," "incredible," "game-changer"
- Short sentences. Real people speak in fragments.
- Specific details make quotes credible — name the day, the metric, the team member

NOTE: If this is for a real customer, these quotes must be approved by the customer before use. Mark all generated quotes with [REQUIRES CUSTOMER APPROVAL] in the output.
```

---

## Usage Notes

- Run after Prompt 1 (narrative) for context.
- The 5 pull quotes map directly to the 5 stages of B2B buying — use them strategically: Quote 1-2 in awareness content, 3 in consideration, 4-5 in decision-stage emails.
- Sales teams love Section C — the one-liners go in every email sequence.
- If customer quotes were collected, paste them in. The AI will polish and expand them while preserving voice.
- Always get customer approval before publishing real names and companies.
