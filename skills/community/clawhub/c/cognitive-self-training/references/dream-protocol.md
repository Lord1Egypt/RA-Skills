# Dream Protocol

Dream review is a scheduled consolidation cycle. It does not hallucinate facts; it recombines known material, explores counterfactuals, and produces testable hypotheses.

## Inputs

Load only the relevant files:

- `.cognitive-training/daily/YYYY-MM-DD.md`
- `.cognitive-training/inbox/YYYY-MM-DD.md`
- `.cognitive-training/cards.md` entries created or reviewed today
- `.cognitive-training/mistakes.md` open entries
- `.cognitive-training/graph.md` recent links
- `.cognitive-training/dream-style-config.md`
- `.learnings/` if present
- `tian-dao` skill body or references if available

## Style Selection

Before writing the dream description, read `.cognitive-training/dream-style-config.md`. If it is missing, create it from [dream-styles.md](dream-styles.md).

Selection rules:

1. If `Mode: fixed`, use `Fixed style`.
2. If `Mode: random`, randomly select one style from `Enabled styles`.
3. If `Mode: weighted-random`, select according to the configured weights.
4. Load the selected style's scene instruction from [dream-styles.md](dream-styles.md).
5. If the selected style conflicts with the user's emotional safety or the seriousness of the content, choose `research-lab` instead and note the override.

The style affects only the dream description. It must not alter evidence, probabilities, scores, or recommendations.

## Dream Stages

### 1. Replay

Summarize the day as factual observations:

- What happened?
- What was learned?
- What failed?
- What remains unresolved?

Label these as `Observation`, not conclusion.

### 2. Compression

Reduce the day into 3-7 fragments:

- one central concept
- one procedure or workflow
- one mistake or correction
- one open question
- one analogy or cross-domain connection
- one strategic implication

### 3. Tian-Dao Deduction

For each important fragment, run the eight dimensions:

| Dimension | Dream Question |
| --- | --- |
| Causal chain | What caused this learning, and what will it change? |
| Forces | Which user needs, tools, constraints, incentives, or agents are involved? |
| Variables | What variables could change the interpretation? |
| Branch points | What decisions or evidence would split the future path? |
| Probability | Which branches are most likely, and how confident are we? |
| Timeline | When should this be reviewed, tested, or applied? |
| Butterfly effect | Which small detail could compound into a large future gain or failure? |
| Terminal state | What does mastery, stagnation, and failure look like? |

Then apply:

- Contradiction analysis: identify the main contradiction and secondary contradictions.
- Practice theory: decide what must be tested in action.
- Inversion: imagine the lesson failed and reverse-engineer why.
- Safety margin: preserve uncertainty and avoid over-promoting weak insights.

### 4. Dream Review Scene

Render the reasoning process as a scene the user can inspect. Use the selected style's scene instruction. The agent should write as if it has crossed into that dream scene to study, replay, and consolidate the day.

Requirements:

- 250-700 words unless the user asks for more or less.
- Include the selected style name.
- Begin with the crossing premise from the style's scene instruction.
- Turn each key fragment into a visible object, actor, room, road, case file, battlefield unit, classroom exercise, lab instrument, or other style-appropriate scene element.
- Show the reasoning movement: conflict, branch, test, uncertainty, and consolidation.
- Add a short `Reasoning map` that links 3-7 scene elements back to source fragments.
- Do not add new factual claims inside the scene.

Use this structure:

```markdown
## Dream Review

Selected style:

Dream scene:

Reasoning map:
- Scene element -> source fragment or hypothesis
```

### 5. Dream Recurrence Statement

Write one compact paragraph explaining why this dream scene recurs today and what learning pattern it is trying to rehearse.

Use this structure:

```markdown
## Dream Recurrence Statement

Tonight's dream recurs as `[style]`: ...
```

### 6. Academic Rigor Pass

Write every important result as one of:

- `Observation`: directly seen in today's work.
- `Inference`: reasoned from observations.
- `Hypothesis`: plausible but needs evidence.
- `Speculation`: useful idea with weak evidence.

For each hypothesis, include:

```markdown
- Hypothesis:
- Why it might be true:
- What would falsify it:
- Evidence to seek:
- Confidence: low | medium | high
- Next experiment:
```

### 7. Recombination

For each fragment, produce:

- near transfer: same domain, new task
- far transfer: different domain, similar structure
- counterexample: where the idea breaks
- research question: what to study next

### 8. Promotion Gate

Do not promote dream outputs directly into durable principles unless one of these is true:

- user explicitly confirms it
- it was validated by a later task
- it survived at least one review cycle
- it corrects a repeated mistake

Unvalidated outputs become cards with `Source: dream` and `Stability: new`.

### 9. Summary Narrative

End the user-facing report and stored dream file with `Summary Narrative`.

Requirements:

- Write one paragraph in Chinese.
- Limit it to 300 Chinese characters.
- Make it read like the closing paragraph of a novel.
- Include the dream scene's sensory detail, the reviewed knowledge, the shift in understanding, and the next learning posture.
- Do not introduce new evidence, tasks, or claims not already represented in earlier sections.

## Output File

Write to `.cognitive-training/dreams/YYYY-MM-DD.md`:

```markdown
# Dream Review YYYY-MM-DD

## Dream Review

## Dream Recurrence Statement

## Tian-Dao Deduction

## Research Hypotheses

## Tomorrow's Practice

## Store Updates

## Summary Narrative
```
