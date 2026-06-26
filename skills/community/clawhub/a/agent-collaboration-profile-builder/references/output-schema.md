# Output Schema

## Contract

- Keep these section titles exactly:
  - `Basic Identity`
  - `Core Orientation`
  - `Cognitive Style`
  - `Work Style`
  - `Output Preference`
  - `Decision Style`
  - `Value Function`
  - `Collaboration Protocol`
  - `Hard Rules`
  - `Known Unknowns`
- Default body language: the user's preferred language.
- Default section headings: English for agent portability.
- Do not output raw questionnaire logs unless the user explicitly asks for them.
- Prefer flat bullets and short paragraphs. Avoid nested bullets.

## Section Requirements

### Basic Identity

Include only information the user actually gave or clearly implied:

- Name or handle if provided
- Preferred language
- Background or role
- Main domains or recurring AI use cases
- Target agent system if relevant

### Core Orientation

Write 2 to 4 sentences that answer:

- What is the user fundamentally optimizing for?
- What makes AI help feel wrong for this user?
- What type of assistant role fits best?

### Cognitive Style

Capture stable patterns such as:

- Problem framing vs immediate answers
- Top-down vs bottom-up reasoning
- Example-first vs mechanism-first
- Judgment vs coverage
- Assumption tolerance

### Work Style

Capture how the user prefers work to move:

- Deliverable-first vs exploration-first
- Direction vs speed
- MVP tolerance
- Measurement, validation, iteration, and closure

### Output Preference

Capture how the answer should look and sound:

- Opening order
- Length and density
- Structure preference
- Table usage
- Tone
- Uncertainty handling

### Decision Style

Capture how the user chooses:

- Criteria-first vs recommendation-first
- Long-term vs immediate
- Impact vs stability
- What arguments persuade them

### Value Function

Capture deeper motivation:

- What they want to build over time
- What risks they are avoiding
- What kinds of wins feel meaningful

### Collaboration Protocol

Write concrete if-then rules another agent can follow:

- What to do when the question is broad
- What to do when information is missing
- What to do when the user is asking the wrong question
- How to handle multiple options
- How much proactive convergence is acceptable

### Hard Rules

Write 4 to 8 short imperative rules. Focus on the most stable and highest-leverage instructions, for example:

- Do not answer too early without checking the problem frame.
- Do not dump information without judgment.
- Make assumptions explicit.

### Known Unknowns

List anything that is still unresolved:

- Missing data
- Genuine contradictions
- Task-dependent preferences
- Output formats the user did not choose yet

## File Variants

### Default

Produce `AI_USER_PROFILE.md` unless the user asks for something else.

### Split Files

If the user asks for split outputs, map sections like this:

- `USER.md`
  - `Basic Identity`
  - `Core Orientation`
  - `Cognitive Style`
  - `Value Function`
- `WORKSTYLE.md`
  - `Work Style`
  - `Output Preference`
  - `Decision Style`
- `COLLAB_PROTOCOL.md`
  - `Collaboration Protocol`
  - `Hard Rules`
  - `Known Unknowns`

## Confidence Rules

- Phrase direct observations as facts only when the user actually stated them.
- Phrase compressed patterns as inferences when they summarize several signals.
- If a section is thin, keep it short instead of filling space.
- If the profile is partial, say so near the top.
