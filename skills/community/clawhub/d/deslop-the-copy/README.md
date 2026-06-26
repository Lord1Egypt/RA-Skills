# deslop-the-copy

A Claude Code skill that strips AI-generated writing patterns and makes text sound like a real person wrote it.

Three passes: kill AI patterns, add soul, final audit.

## Why this exists

Wikipedia's [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) maintains a detailed guide called [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), cataloging patterns observed across thousands of AI-generated texts. NPR, TechCrunch, and FlowingData have all covered it as the best reference for spotting machine-written prose.

Existing tools use these patterns to detect and strip AI tells from text — banned phrases, structural cliches, sentence-level rules. They focus on **detection and removal**. They strip the bad stuff out.

deslop-the-copy goes further. It doesn't just remove AI tells, it **adds back what's missing**: varied sentence rhythm, real opinions, contractions, rough edges, the things that make writing feel like a person actually wrote it. Three passes instead of two. Zero em dash tolerance. And a final audit that asks the only question that matters: "Would someone suspect AI wrote this?"

## Installation

**Clone directly into Claude Code skills:**

```bash
cd ~/.claude/skills
git clone https://github.com/skyzer/deslop-the-copy.git
```

**Or copy manually:**

Copy `SKILL.md` into `~/.claude/skills/deslop-the-copy/SKILL.md`.

## Usage

Ask Claude to clean up any AI-sounding text:

- "Deslop this paragraph"
- "Make this not sound like AI"
- "Clean up this copy"
- "This reads like slop, fix it"

## What it does

AI text has a recognizable smell. This skill teaches Claude to identify and remove it through three passes.

### Pass 1: Kill AI patterns

Targets four categories of AI tells:

**Content patterns** like significance inflation ("stands as a testament"), promotional language ("groundbreaking", "nestled in the heart of"), vague attributions ("experts argue"), and generic "challenges and future" wrap-ups.

**Language patterns** like AI vocabulary (robust, leverage, navigate, landscape, paradigm, delve, foster, synergy), copula avoidance ("serves as" instead of "is"), negative parallelisms ("it's not just about X, it's about Y"), rule-of-three overuse, synonym cycling, false ranges, filler phrases, and excessive hedging.

**Style patterns** like em dash overuse (zero tolerance), boldface overuse, inline-header vertical lists, Title Case headings, emojis in headers, and curly quotes.

**Communication artifacts** like chatbot language ("I hope this helps!"), knowledge-cutoff disclaimers, sycophancy, and meta-signposting ("let's explore", "here's the thing").

### Pass 2: Add soul

After removing the AI patterns, it makes the text feel human:

- Varies sentence rhythm aggressively (mix 3-word fragments with 25-word sentences)
- Adds opinions where appropriate
- Uses contractions naturally
- Starts sentences with And, But, So
- Leaves rough edges and trusts the reader

### Pass 3: Final audit

One last check: "What would make someone suspect AI wrote this?" Fix anything that still feels off. Zero em dashes, contractions in place, meaning preserved.

## Before and after

**Before:**
> In today's rapidly evolving digital landscape, artificial intelligence stands as a transformative force that is fundamentally reshaping how businesses navigate the complexities of modern commerce. From small startups to large enterprises, organizations are leveraging robust AI solutions to enhance their operational efficiency, foster innovation, and drive sustainable growth. It's not just about automation -- it's about reimagining what's possible.

**After:**
> AI is changing how businesses work. Companies of all sizes are using it to cut costs, speed up processes, and try things they couldn't before. That matters. But we're still figuring out the real risks, and not everyone benefits equally.

## License

MIT
