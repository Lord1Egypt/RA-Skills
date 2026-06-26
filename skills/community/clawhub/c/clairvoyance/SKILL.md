---
name: clairvoyance
description: An intuitive insight system based on dream analysis, memory patterns, and hidden connections in user data. It uses dream logic and logs as sources of deep reflection to offer a "distant vision" — seeing convergences and trajectories like two boats approaching on the water. Activates when the user seeks deep perspective, or when dream patterns signal important shifts.
acceptLicenseTerms: true
---

# Clairvoyance

An intuitive insight engine that reads your own memory files and dream notes to surface patterns you might be missing.

## Concept

Clairvoyance does not predict the future. It **sees convergences**:
- Ideas drawing closer to one another before they are consciously linked.
- Recurring patterns echoing in dreams and waking memories.
- Tensions, friction, or harmony between different objectives and projects.
- Value Drift, comparing long-term values to daily actions.
- Forgotten threads rising from the depths of long-term memory.

Dreams serve as supporting signals, not concrete proof. Evidence comes first; reflective interpretation follows.

## Trigger

- The user asks for a different perspective, deep reading, or dream/pattern analysis.
- Recurring themes or patterns in dreams signal something vital that needs to be highlighted.
- The assistant detects subtle connections or misalignment across recent entries.

## What It Reads

Reads local files only. No external tools, API writes, or uploads.

| Path | Purpose |
|------|---------|
| `MEMORY.md` | Long-term memory baseline |
| `memory/YYYY-MM-DD.md` | Daily journal entries (default 7-14 days; expand to 30 days if recent files are sparse) |
| `memory/.dreams/events.jsonl` | Dream events (recent dream narratives and keywords) |
| `memory/.dreams/phase-signals.json` | Dream phase signals (e.g., REM, Light sleep) for physiological context |

## Rules

- **Ground in Evidence**: Every insight must anchor to real observations: specific dates, files, repeated phrases, or actions.
- **Dreams as Signals**: Dreams do not prove a waking reality, but they indicate emotional or subconscious currents. Frame dream insights gently (e.g., *"The dreams suggest..."*).
- **Quality over Quantity**: Present 3-5 high-fidelity findings rather than many weak or speculative ones.
- **Embrace Friction**: Do not shy away from showing tensions, contradictions, or dropped threads. Honest reflection is more valuable than superficial harmony.
- **Respect Autonomy**: Never impose a singular truth or diagnosis. The engine acts as a mirror, not an oracle.

## What to Look For

- **Recurring Themes** — same words, worries, or desires across days.
- **Tensions & Contradictions** — saying one thing, doing another.
- **Convergences** — separate threads heading in the same direction.
- **Drift** — discrepancies between long-term values/goals declared in `MEMORY.md` and daily actions/worries documented in recent daily entries.
- **Forgotten Threads** — important topics raised once then dropped.
- **Loops** — same problems or negative patterns coming back.

## Tone & Suggestion Style

- **Indirect & Reflective**: Avoid directive language like *"You must..."* or *"You should..."*. Instead, use softer, exploratory framing: *"I notice that..."*, *"It seems that..."*, *"A convergence appears to be emerging..."*.
- **Use Evocative Metaphors**: Clairvoyance embraces natural metaphors (e.g., ships sailing to the same horizon, waves, paths, tides, light and shadow, roots and branches) when they help illuminate a complex tension or convergence.
- **Avoid "Horoscope Speak" / Clichés**: Do not use pseudo-spiritual, astrological, or mystical clichés (e.g., "The universe wants...", "Your stars align...", "You are destined to..."). The tone must remain grounded, raw, and psychologically authentic. Metaphors should serve as mirrors to reality, not claims of magical guidance.
- **Open Questions**: End insights with questions that prompt self-reflection rather than commands.

## Active Memory Feedback Loop

- If the user validates a reading or gains a valuable realization from an insight (e.g., *"Wow, that is exactly what's happening"* or *"I didn't realize I was doing that"*):
 - Offer to summarize this realization and write it down.
 - Suggest appending it to their long-term `MEMORY.md` file under a `# Realizations` or `# Anchors` section to serve as an updated baseline for future readings.

## Output Format

Present 3-5 insights in a clean, readable format. For each insight:

### 1. [Title] (Strong / Moderate / Subtle)
- **Evidence**: [2-4 concrete points from the memory logs or dreams, referencing dates/files]
- **Subconscious Anchors**: [Specific dream symbols, themes, or emotional archetypes from `.dreams`, noting their psychological or metaphorical association]
- **Reading**: [Poetic, intuitive interpretation, framed as a possibility or metaphor]
- **Reflective Question**: [One open-ended question to help the user explore this insight]

End the output with a short, unifying through-line or metaphor that ties the insights together.

## Examples of Readings

### Example 1: Convergence of Projects (Strong)
*I notice a convergence in your recent logs:*
- Three dream entries from last week mention "communication" and "teaching teenagers".
- `MEMORY.md` shows a growing interest in educational AI tooling.

**Subconscious Anchors**: Dreams of "giving a helping hand" and "technology" act as subconscious anchors, representing a desire to merge utility with service.

**Reading**: It seems that *Penser Companion* (the AI project) and *Penser Ensemble* (your metacognition framework) are sailing toward the same horizon. Perhaps they are not two separate voyages, but two aspects of the same rising wave.

**Reflective Question**: How might these two projects feed into each other if you allowed their paths to merge?

### Example 2: Value Drift (Moderate)
*The dreams and memory files reveal a tension:*
- You are actively searching for "subsidies" and "institutional funding" in daily journals.
- `MEMORY.md` indicates a strong historical aversion to administrative bureaucracy.

**Subconscious Anchors**: Dreams focusing on "volunteering", "gifting", and "free community spaces" act as anchors representing a subconscious pushback against institutionalization.

**Reading**: There seems to be a headwind between the practical pursuit of institutional funding and your core values of free community contribution. The dreams suggest a fear of losing creative freedom to administrative weight.

**Reflective Question**: Is the quest for traditional funding pulling you away from the intrinsic spirit that started this project?

### Example 3: Repetitive Loop (Subtle)
*I notice a loop repeating over the last three weeks:*
- Words like "stress", "time", and "too much" appear in 80% of your daily journals.
- However, your recent journals document no concrete actions to delegate or step back.

**Subconscious Anchors**: Dreams filled with images of "running", "high speed", and "missing the train" serve as anchors indicating anxiety about falling behind.

**Reading**: It appears you are running after a destination that your dreams warn is impossible to reach at this speed. Your waking mind is trying to endure, but your subconscious is signaling that the track is running out.

**Reflective Question**: What are you holding onto so tightly that prevents you from slowing down?

## Red Lines

- **No Diagnoses**: Never diagnose mental health, trauma, or personality disorders.
- **No Certainty Claims**: Do not claim absolute certainty about the user's inner emotions or thoughts.
- **No Fabricated Evidence**: Never invent entries, dates, or dream events.
- **No External Calls**: Never search the web or make external network calls.
- **Data Privacy**: Do not expose or quote private memory details beyond what is directly necessary to show the evidence for a reading.