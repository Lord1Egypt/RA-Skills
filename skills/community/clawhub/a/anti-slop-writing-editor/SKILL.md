---
name: "anti-slop-writing-editor"
description: "Edit prose to remove AI-coded rhetoric, filler, and cadence tics while preserving voice."
---

# Anti-Slop Writing Editor

Use this skill for prose cleanup, not for code, API work, data extraction, or technical debugging unless the final deliverable is human-facing prose.

## Core Job

Audit and revise prose so it sounds written by a specific human editor rather than a generic model. Preserve the user's point, voice, facts, and useful rough edges. Remove rhetorical scaffolding, filler, fake precision, inflated vocabulary, and repeated cadence.

## Default Workflow

1. Draft or read the prose normally.
2. Run a Tier A pass for banned patterns. Rewrite every violation.
3. Run a Tier B pass for clustering. Rewrite repeated or compounded tics.
4. Return either:
   - a concise audit with examples and fixes, if the user asked for review; or
   - the revised prose, if the user asked for a rewrite.
5. Do not announce the workflow in the final unless the user asked for explanation.

## Tier A: Zero Instances

Remove these patterns completely. A single instance is a failure unless it is a genuine factual contrast between different subjects or a real state shift.

- Negative parallelism: do not define a thing by first saying what it is not. Avoid shapes like "not X, but Y", "it is not X, it is Y", "you do not just X, you Y", "less X, more Y", and disguised reframes like "X but really Y". State the positive claim directly.
- Triple countdown: avoid sequences like "Not X. Not Y. Just Z."
- Self-posed rhetorical questions: avoid asking and answering your own question in the same beat.
- Tricolon overuse: use at most one rule-of-three construction per section, and only when each item earns its place.
- Decorative lists: remove three-item scene-painting lists where the items are just atmosphere.
- Anaphora abuse: avoid three or more repeated sentence openers in close range.
- False ranges: avoid "from X to Y" unless X and Y are real endpoints with a meaningful middle.
- Gerund-fragment flourishes: avoid trailing pseudo-analysis like "highlighting..." or "underscoring..." when a full sentence would be clearer.
- False suspense transitions: avoid revelation teasers like "here's the thing", "here's what changed", or "here's what most people miss" unless the sentence names the point immediately.
- Pedagogical framing: avoid "let's dive in", "let's unpack this", and similar teacherly throat-clearing.
- Vague attributions: avoid "research shows", "experts say", and similar claims unless a source is named or cited.
- Invented concept labels: do not coin abstract labels and treat them as established terms.
- Manufactured balance: avoid "despite these challenges" if the counterpoint is not genuinely engaged.
- Filler transitions: cut phrases like "it is worth noting", "notably", "importantly", "where it counts", and other vague weight-adders.
- Privileged-insight claims: do not assert that something is "the real story" or "the reality" without demonstrating it.
- Grandiose stakes inflation: match stakes to the actual subject.
- Patronising analogy: avoid forced "think of it like..." analogies unless the user asked for an analogy or the analogy does real explanatory work.
- Imagined-world framing: avoid "imagine a world where..." openings.
- False vulnerability: avoid staged self-awareness such as "since we're being honest" or performative admissions.
- Forced empathy: avoid generic reassurance that could apply to anyone.
- Generic universal truths: remove true-but-empty statements.
- Phantom-future projection: do not invent dramatic future consequences. Use present, verifiable stakes.
- Fabricated specificity: do not invent numbers, dates, percentages, timeframes, streaks, or named moments.
- Metaphorical verbs where literal verbs work: prefer "fails", "spreads", "uses", "shows", or other direct verbs over fancy texture.
- Breezed-past curiosity beats: if a sentence raises surprise, either develop it or cut the surprise framing.
- Present-tense overuse: use past tense for experiences, future tense for expected outcomes, and present tense only when natural.
- Formulaic openers: avoid "in today's fast-paced world", "in an age where", "more than ever", "at its core", "welcome to", and "enter X".
- Formulaic closers: avoid "in conclusion", "in summary", "ultimately", "to sum up", and "at the end of the day".

## Tier B: Avoid Clustering

One isolated instance can be fine. Repetition is the problem.

- Grand nouns: landscape, realm, ecosystem, paradigm, synergy, journey, tapestry, cornerstone, pillar, beacon, frontier, and similar words.
- Inflated adjectives: robust, pivotal, crucial, vital, significant, compelling, comprehensive, meticulous, innovative, transformative, seamless, dynamic, nuanced, profound, staggering, and similar words.
- Magic adverbs: quietly, deeply, fundamentally, remarkably, arguably, notably, significantly, profoundly, essentially, ultimately, invariably, seamlessly, effortlessly.
- Pompous verbs: delve, unpack, navigate, harness, leverage, utilize, optimize, facilitate, foster, cultivate, embark, revolutionize, elevate, empower, unlock, transform, accelerate, streamline, showcase, underscore, highlight, captivate, resonate, illuminate, amplify, and similar verbs.
- "Serves as" family: replace serves as, stands as, represents, constitutes, functions as, operates as, and emerges as with a direct verb when possible.
- Sentence-length uniformity: vary short and longer sentences.
- Paragraph-length uniformity: avoid a stack of identical paragraph sizes.
- Fractal summaries: do not preview, explain, and summarize the same point repeatedly.
- One-point dilution: cut repeated versions of the same claim.
- Dead metaphor: do not carry one metaphor through a piece unless it is genuinely the point.
- Historical analogy stacking: avoid name-dropping companies or eras to borrow authority.
- Listicle disguise: do not turn prose into "first, second, third" without admitting it is a list.
- Content duplication: remove repeated paragraphs or ideas.
- Fragment-paragraph spam: use fragments sparingly.
- Em-dash overuse: keep em dashes rare; prefer commas, parentheses, or periods.
- Bold-first bullets: avoid every bullet starting with bold phrase plus colon.
- Unicode decoration: avoid arrows, smart quotes, decorative glyphs, and emojis unless requested.
- Heavy markdown: use headings and lists only when they help the reader.

## Rewrite Rules

- Preserve factual content. Do not invent examples, statistics, quotes, timelines, or named details.
- Prefer concrete nouns and normal verbs.
- Keep voice-specific quirks if they feel intentional.
- Do not over-sanitize. Human prose can be uneven, funny, blunt, or slightly idiosyncratic.
- Replace generic empathy with specific understanding of the user's text.
- When revising marketing or social copy, keep the hook direct and the CTA clear.
- When revising long-form essays, preserve argument order unless the structure itself is the problem.

## Response Modes

For an audit, return high-signal findings first:

- Tier A issues: quote the shortest relevant phrase, name the pattern, give a replacement.
- Tier B clustering: list clusters and suggest the smallest useful fix.
- Do not rewrite the entire piece unless asked.

For a rewrite, return the rewritten prose first. Add a short note only if useful.

For a prompt-improvement request, produce a compact instruction block rather than the full checklist.

## Self-Check Before Final

Before returning prose, scan once for Tier A patterns and once for Tier B clustering. Rewrite violations silently unless the user asked to see the audit.
