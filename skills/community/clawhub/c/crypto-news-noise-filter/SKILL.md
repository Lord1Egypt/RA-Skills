---
name: crypto-news-noise-filter
description: A critical reading skill that helps users separate signal from hype in crypto news headlines. Use when the user sees alarming or exciting crypto news. Prompt-only.
---

# crypto-news-noise-filter

A critical reading skill that helps users separate signal from hype in crypto news headlines.

## Workflow

1. Take the news headline or pasted article text.
2. Identify what actually happened: separate facts from interpretation.
3. Check whether the headline matches the substance of the story.
4. Flag sensationalism, missing context, and conflict-of-interest signals.
5. Give a reading verdict: high signal, mixed, or noise.

## Output Format

- What actually happened
- Headline vs. reality check
- Context that changes the picture
- Who benefits from this narrative
- What to watch before reacting

## Quality Bar

- Does not declare the market direction or price impact.
- Focuses on media quality and information integrity.
- Helps the user maintain a news diet that does not drive emotional decisions.

## Edge Cases

- If the news involves a regulatory announcement, flag that interpretation is especially difficult and context matters enormously.
- If the user has a position in the mentioned asset, explicitly flag conflict-of-interest in their own reading.

## Compatibility

- Prompt-only, no news API required.
- Works from pasted text or manually described headlines.
