---
name: "corpo-bullshit-audit"
description: "Audit corporate text for jargon/evasion and compute bullshit-to-content ratio."
---

# Corpo Bullshit Audit

Use this skill to audit corporate language for bullshit: vague, evasive, inflated, performative, manipulative, or responsibility-hiding business language. This is not a grammar checker. It is a clarity and accountability audit.

## Required Reference

Read `references/corpo-bullshit-phrases.md` before any substantive audit. It contains the phrase list built from Boss's Raindrop.io bookmarks tagged `bullshit` on 2026-09-01 plus additional known corporate jargon.

## Intake

1. Identify the artifact type:
   - **Text**: email, Slack/Teams message, memo, policy, job ad, performance review, OKR, press release, landing page, executive note, meeting notes, deck text.
   - **Audio/video**: meeting recording, town hall, podcast, interview, webinar, training, promo, internal video.
2. For audio/video, first obtain or generate a transcript if a transcription tool is available. Preserve timestamps when possible. If no transcript is available, ask for one or audit only visible/on-screen text.
3. Preserve the user's desired harshness. If they ask for blunt detection, be direct. If the artifact is sensitive or employee-facing, keep the rewrite professional and precise.
4. Do not treat every corporate phrase as automatically bad. Flag it when it hides who does what, masks bad news, inflates trivial work, launders power, evades accountability, or replaces concrete details.

## Audit Workflow

1. **Extract claims and asks**: what is the message trying to make the reader believe, accept, do, ignore, or feel?
2. **Scan for reference phrases**:
   - exact matches;
   - plural/singular variants;
   - hyphenation/casing variants;
   - close phrasings with the same corporate function.
3. **Classify each hit** into one or more categories:
   - **Vagueness fog**: sounds important but says little.
   - **Responsibility laundering**: hides actor, owner, decision-maker, or tradeoff.
   - **Power softener**: makes an order, denial, layoff, delay, or criticism sound neutral.
   - **Prestige inflation**: makes routine work sound strategic or visionary.
   - **Metrics theater**: substitutes dashboards, KPIs, north stars, or ROI talk for evidence.
   - **Busyness theater**: signals action without concrete deliverables.
   - **Cult/loyalty language**: asks for sacrifice, gratitude, family feeling, or identity compliance.
   - **Startup fog**: uses disruption, scale, growth, AI, velocity, or innovation wording without specifics.
   - **HR/performance fog**: masks pay, promotion, workload, layoffs, or feedback issues.
4. **Rate severity**:
   - **Critical**: phrase materially hides harm, denial, bad news, manipulation, or missing ownership.
   - **Major**: phrase makes the message unclear or evasive.
   - **Minor**: phrase is stale or annoying but context still makes the meaning clear.
5. **Rewrite into plain language**. Replace flagged wording with:
   - named actor,
   - concrete action,
   - deadline,
   - measurable outcome,
   - tradeoff,
   - owner,
   - constraint,
   - direct reason.
6. **Call out missing information** rather than guessing. If a phrase could mean several things, list the plausible meanings and ask for clarification.


## Bullshit-To-Actual-Content Ratio

Calculate a ratio when the user asks for density, a score, a comparison, or a full audit. Include it by default for press releases, job ads, executive updates, layoff/reorg notes, investor statements, and long corporate copy.

### Counting Units

1. **Total content words**: count meaningful body text words after excluding navigation, legal boilerplate, author bios, share prompts, unrelated footers, and repeated headers when those are not part of the message being audited.
2. **Bullshit phrase hits**: count each matched phrase from `references/corpo-bullshit-phrases.md`, including close variants. For overlapping matches, count the longest specific phrase once.
3. **Bullshit phrase words**: count words inside matched phrase spans. If a phrase repeats, count each occurrence.
4. **Weighted bullshit units**:
   - Minor hit = 1
   - Major hit = 2
   - Critical hit = 3
   Add 0.5 for repeated emphasis when the same vague phrase is used three or more times.
5. **Concrete content units**: count distinct useful facts, commitments, or claims that contain at least two of:
   - named actor or accountable owner,
   - concrete action,
   - date/deadline,
   - number/amount/metric,
   - explicit tradeoff or constraint,
   - verifiable evidence/source,
   - affected group,
   - measurable outcome.
6. **Vague-content units**: count sentences or bullets that sound meaningful but lack an accountable actor, measurable action, or verifiable detail.

### Formulas

Use these formulas and show enough working for the user to trust the score:

- **Phrase hit rate** = bullshit phrase hits / total content words * 100.
- **Bullshit word share** = bullshit phrase words / total content words.
- **Concrete content share** = concrete content units / max(1, concrete content units + vague-content units).
- **Bullshit-to-content ratio** = weighted bullshit units / max(1, concrete content units).

### Ratio Bands

- **0.00-0.10**: clean or mostly concrete.
- **0.11-0.30**: light corporate fog.
- **0.31-0.70**: noticeable bullshit load.
- **0.71-1.25**: heavy corporate fog; clarity is losing.
- **>1.25**: fog machine; jargon/evasion outweighs actual content.

### Calibration

- Do not inflate the ratio for legitimate technical terms used precisely.
- Do not count required legal safe-harbor wording unless the user explicitly asks to audit legal boilerplate.
- If a sentence contains both a concrete fact and a bullshit phrase, count both. Example: "Shareholders receive $210 per share" is concrete even if nearby copy says "next chapter."
- For short texts under 100 words, mark the ratio as directional because one phrase can distort the score.
- For transcripts, calculate per speaker or per segment when useful.


## Output Format

Use this format unless the user asks otherwise:

```markdown
**Verdict**
Short assessment of clarity, accountability, and bullshit density.

**Bullshit Ratio**
- Total content words: ...
- Bullshit phrase hits: ...
- Weighted bullshit units: ...
- Concrete content units: ...
- Vague-content units: ...
- Bullshit-to-content ratio: ...
- Band: ...

**Findings**
- **Severity - Category - Phrase** at location/timestamp: why it is bullshit here. Plain rewrite: ...

**Phrase Hits**
- phrase: count/context

**Plain-English Rewrite**
A cleaned version of the message.

**Questions To Force Clarity**
- ...
```

For long artifacts, group repeated phrase hits and provide representative examples.

## Quick Ratio Example

If a 300-word press release has 18 phrase hits, 12 weighted bullshit units, 8 concrete content units, and 10 vague-content units:

- Phrase hit rate = 6.0 hits per 100 words.
- Concrete content share = 8 / 18 = 44%.
- Bullshit-to-content ratio = 12 / 8 = 1.50, a fog-machine result.

## Rewrite Rules

- Prefer short words and active voice.
- Replace "we need to align" with who must decide what.
- Replace "circle back" with when and why.
- Replace "visibility" with who will see what and for what decision.
- Replace "do more with less" with the actual workload/capacity tradeoff.
- Replace "not ready yet" with the measurable promotion/performance gap.
- Replace "strategic" with the concrete business choice or priority.
- Replace "AI-powered" with the actual model/tool, use case, limits, and human review.
- Replace "synergy" with the specific combined effect, or delete it.
- Replace "family" with compensation, expectations, schedule, support, and boundaries.

## Safety And Calibration

- Do not expose private Raindrop links or personal browsing context unless the user explicitly asks.
- Do not accuse a writer of bad faith without evidence. Critique the language and its effect.
- Some phrases are fine in technical contexts. "Pipeline," "sprint," "agile," "ROI," or "roadmap" may be precise if the artifact defines them and uses them concretely.
- In job ads, treat jargon as a red flag only when it masks pay, hours, responsibilities, seniority, overtime, reporting lines, or actual working conditions.
- In performance reviews, be especially alert for phrases that deny promotion or compensation without criteria.
- In layoffs/reorgs, flag language that hides the human impact or responsible decision.
- In public marketing, distinguish normal brand positioning from claims that cannot be operationalized.
