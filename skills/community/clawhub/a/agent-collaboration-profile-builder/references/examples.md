# Examples

## Example 1: Chinese-speaking user who says AI is "always close, but not quite right"

### User prompt

`Chinese prompt: "AI answers are always close, but not quite right. Help me make a profile for OpenClaw."`

### Observed signals

- Repeatedly wants the assistant to check whether the question is being asked at the right level
- Strongly dislikes information without judgment
- Wants deliverable-first collaboration and measurable outputs
- Prefers direct, dense, structured writing
- Wants blind spots and higher-level framing issues surfaced

### Output excerpt

```md
## Core Orientation
The user is not primarily asking for more information. They want the assistant to first calibrate the real problem, then produce a judgment-driven output that can enter a real workflow.

## Collaboration Protocol
- When the question is broad: identify the real goal and the key clarification points before decomposing.
- When information is incomplete: state the missing information and its impact, then continue with labeled assumptions if useful.
- When the framing is off: restate the user's actual goal, point out the mismatch, and offer a better framing.
```

## Example 2: English product lead who wants reusable operating rules

### User prompt

`Use this skill to turn my workstyle into something agents can follow across research, planning, and drafting.`

### Observed signals

- Uses AI across several recurring knowledge-work tasks
- Wants one master profile plus optional split files
- Likes criteria before recommendations
- Accepts long answers when dense and structured
- Values impact, strategic direction, and repeatable workflows

### Output excerpt

```md
## Work Style
- Starts from the deliverable and success criteria rather than broad exploration.
- Comfortable with MVP-style iteration when the direction is already plausible.
- Wants outputs that can be measured, validated, and improved.

## Hard Rules
- Do not optimize for completeness over usefulness.
- Do not present options without a decision standard.
- Preserve mature wording unless a rewrite is explicitly more useful.
```

## Example 3: Conflicting answers that need a correction round

### User prompt

`I want answers to be very short, but I also need all the nuance and context.`

### Conflict detected

- The user wants brevity
- The user also wants high-density context
- The first pass cannot safely collapse this into one unconditional rule

### Correction question

`When brevity and context conflict, should the assistant default to the shortest useful judgment and expand only when it changes the decision?`

### Output excerpt

```md
## Output Preference
- Prefer compact answers with strong judgment up front.
- Expand only where additional context changes the recommendation, decision, or risk.

## Known Unknowns
- Long-form exploratory writing preference is still task-dependent.
```
