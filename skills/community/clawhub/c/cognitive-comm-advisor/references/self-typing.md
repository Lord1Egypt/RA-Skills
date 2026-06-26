# Cognitive Function Self-Assessment

Use this when the user does not know their own cognitive type. Goal: identify likely
dominant and auxiliary functions in ~60 seconds as a working hypothesis for communication
strategy. This is a heuristic, not a scientific instrument.

## Rules

- Ask the 4 core questions together.
- Every question must have numbered choices: `1` or `2`.
- Ask for degree on each: `strongly`, `slightly`, or `hard to say`.
- **Language**: present all questions and descriptions in the user's input language.
  The English templates below are for reference — always translate/adapt to match the
  user's language naturally (not word-for-word translation).
- Accept mobile shorthand: `1 strong`, `2 slight`, `1s`, `2?`, `hard`, `not sure`.
- Treat the result as a communication heuristic, not identity truth.
- If 3-4 dimensions are clear, proceed. If 1-2 are unclear, ask only the relevant follow-up(s).

## User-Facing Prompt

```markdown
No problem — quick 60-sec self-read. For each one, pick 1 or 2 + degree:
`strongly / slightly / hard to say`.

1. Energy / processing style
   1) I often think by talking. Interaction helps me clarify what I mean.
   2) I usually think first, then speak. I prefer showing up with formed thoughts.

2. Information style
   1) I trust concrete examples, specifics, precedent, and what has actually worked.
   2) I naturally look for patterns, possibilities, implications, and the bigger idea.

3. Decision style
   1) I default to logic, consistency, tradeoffs, and what's objectively true/workable.
   2) I default to values, people impact, motivation, and what feels aligned/fair.

4. Work style
   1) I like closure: plans, decisions, clear next steps, fewer open loops.
   2) I like flexibility: options open, adapting as new info appears, room to improvise.

Reply like: `1 strong, 2 slight, 1 strong, 2 hard`.
```

## Scoring

Map answers as:

1. Energy / processing:
   - `1` = E
   - `2` = I
2. Information:
   - `1` = S
   - `2` = N
3. Decision:
   - `1` = T
   - `2` = F
4. Work style:
   - `1` = J
   - `2` = P

Degree handling:

- `strongly` = clear signal
- `slightly` = weak signal
- `hard to say` = unknown / low confidence

Confidence guide:

1. 4 clear signals: high enough to use the type directly.
2. 3 clear + 1 weak/unknown: use likely type with a hedge.
3. 2 clear + 2 weak/unknown: use temperament-level advice and ask 1-2 follow-ups.
4. 0-1 clear: ask follow-ups or switch to scenario-first, type-light advice.

## Optional Follow-Ups

Ask only the follow-ups needed for unclear dimensions. Keep numbered format.

### E/I Follow-Up

```markdown
One tie-breaker for energy style:

1. After a full day of meetings, I usually want:
   1) More interaction / debriefing with people
   2) Quiet time to decompress alone

Degree: strongly / slightly / hard to say
```

### S/N Follow-Up

```markdown
One tie-breaker for information style:

2. When someone pitches an idea, I first want:
   1) The practical details: what exactly happens, examples, risks, constraints
   2) The concept: why it matters, where it could go, what it unlocks

Degree: strongly / slightly / hard to say
```

### T/F Follow-Up

```markdown
One tie-breaker for decision style:

3. In a tense work decision, I trust myself more when I:
   1) Separate feelings out and pressure-test the logic
   2) Include people's motivations, morale, and values in the judgment

Degree: strongly / slightly / hard to say
```

### J/P Follow-Up

```markdown
One tie-breaker for work style:

4. When a plan changes late, my honest first reaction is:
   1) Frustration — we had a plan, why are we reopening this?
   2) Curiosity/adaptation — okay, what's changed and what can we do now?

Degree: strongly / slightly / hard to say
```

## Interpreting the Result

Lead with cognitive functions, use four-letter shorthand as a familiar anchor:

- "This points to Ti-dominant with Ne-auxiliary (maps to INTP in shorthand): you process
  through internal logic frameworks, and your auxiliary mode is divergent pattern-making."
- "The J/P signal is weak — functionally that's the difference between Si-tertiary (INTP)
  and Ni-tertiary (ISTP). I'll give advice that works for both since your Dom/Aux are clear."
- "Good enough for communication strategy — this is a working hypothesis, not a tattoo."

## Common Ambiguities

- High-performing professionals may look more J at work than they are internally (developed
  Te/Si for survival). Ask whether structure feels energizing or merely necessary.
- Managers may look more E because the role requires visibility (developed Fe/Te). Ask how
  they recover after interaction.
- People in analytical cultures may answer T because it is rewarded (cultural overlay on
  actual Fi/Fe). Ask what they privately track when the decision affects people.
- S/N often blurs when someone is senior: senior Si/Se-doms can discuss strategy; Ni/Ne-doms
  can handle detail. Ask what they naturally reach for first under time pressure.
- The four-letter shorthand is a convenient index into function stacks, not the framework
  itself. When in doubt, describe the user's likely Dom/Aux rather than insisting on an
  exact four-letter label.
