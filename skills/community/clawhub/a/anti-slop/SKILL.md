---
name: anti-slop
description: Detects and removes "AI slop" — the formulaic vocabulary, sentence structures, sycophantic openers/closers, over-formatting (bullet walls, bold spam, needless headers), and code anti-patterns (over-engineering, swallowed errors, hallucinated APIs, dead code) that make writing or code read as generic and machine-produced. Use this proactively as a self-edit pass on any substantial prose (essays, articles, emails, reports, marketing copy, creative writing, documentation) or any non-trivial code you write or review — don't wait to be asked. Also trigger explicitly whenever the user asks to make text "sound more human," "less like ChatGPT/AI," wants a "slop pass," asks you to de-slop, humanize, or tighten writing, or asks you to clean up bloated, over-engineered, or "vibe-coded" code. Do not use for one-line answers or trivial snippets where there's nothing to edit.
---

# Anti-Slop

A self-editing skill: write or generate code normally, then run a dedicated pass to strip out the patterns that make output read as generic AI filler rather than something a careful person made.

## Why this exists

"AI slop" isn't one thing — it's a cluster of statistically over-represented patterns that large language models learned to lean on because they were safe, common in training data, or rewarded by human/preference-model feedback during RLHF. Research backs this up concretely:

- A 2025 academic study (Paech et al., *Antislop*, ICLR 2026) measured some LLM phrase patterns occurring **over 1,000× more frequently** in model output than in human writing. It's not subtle once you're looking for it.
- A 2024 study (*From Lists to Emojis: How Format Bias Affects Model Alignment*) found that human raters and reward models are measurably biased toward bullets, bold text, and emoji — regardless of whether the content underneath is actually better. That's a large part of why chat models over-format by default.
- Sycophancy research on LLM creative-writing assistants found validating, hedge-everything behavior in the vast majority of sampled outputs — the "Great question!" / "You raise a really interesting point" reflex.
- In code, the same phenomenon shows up as over-engineering, defensive try/catch walls that swallow errors, invented APIs that don't exist, and abstraction layers built for problems that needed ten lines — well-documented across both industry write-ups and peer-reviewed surveys of AI-generated code.

None of these patterns are wrong in isolation. A bulleted list, the word "crucial," a triplet of adjectives, a try/except block — all fine, sometimes exactly right. Slop is what happens when they become the *default reflex* instead of a *choice*, applied identically regardless of what the content actually needs.

## The core principle: edit after, don't self-censor during

**Don't try to consciously avoid a list of banned words while drafting.** This is a documented failure mode, not just a style preference. Actively suppressing a concept while generating text is called the "pink elephant problem" (Castricato et al., 2024): telling a model (or a person) "don't think about X" requires first activating the concept of X, which tends to increase intrusion rather than suppress it. In practice, drafting with a mental ban-list produces contorted, over-negotiated sentences that are arguably worse than the slop they're avoiding — and research on LLM instruction-following backs this up: negative constraints ("don't use X") are consistently less reliable than positive targets ("do Y instead").

So the workflow is always two passes, not one:

1. **Draft naturally.** Focus entirely on being correct, specific, and useful. Don't monitor word choice while composing.
2. **Edit deliberately.** Once a full draft exists, review it against the patterns below and in `references/`, and fix what's actually there. Editing an existing sentence for a known problem is a completely different (and much more reliable) task than avoiding an unknown one in real time.

This mirrors how the actual de-slopping tools work: the Antislop sampler and similar systems operate by watching for a completed pattern and only then intervening — never by pre-emptively blocking vocabulary, which they found destroys fluency once the ban list gets large.

**Detect by density, not by single words.** A single instance of "delve" or "crucial" or a bulleted list proves nothing — humans write these too. The tell is *clustering*: several tier-1 words in one paragraph, a paragraph that is one long triplet after another, every single section wrapped in a bold header regardless of length. Read `references/prose-tells.md` with this in mind — it's a diagnostic reference, not a blacklist to grep-and-delete.

**Fix by making it more specific, not just by swapping synonyms.** Slop is generic because it's vague — replacing "leverage" with "utilize" doesn't help, because both are still vague. The actual fix is almost always to say the *specific* thing: which tool, what number, whose claim, what actually happened. Concreteness kills slop far more reliably than a thesaurus pass does.

## Workflow

1. **Write or generate the content normally.** Don't slow down for word-choice policing.
2. **Identify the domain** — prose/writing or code — and load the matching reference:
   - Prose, articles, emails, reports, docs, creative writing → `references/prose-tells.md`
   - Code in any language → `references/code-slop.md`
3. **Run the self-edit pass** using `references/self-edit-checklist.md` — read it once per session if you haven't already; it's short and reusable across many tasks.
4. **For long or high-stakes documents** (a report going to a client, a blog post, anything over ~800 words), optionally run the quantitative scanner for a second opinion. It lives at `scripts/slop_scan.py` alongside this file — find its actual path in your environment and run:
   ```bash
   python3 <path-to-this-skill>/scripts/slop_scan.py path/to/draft.md
   ```
   It flags tier-1/tier-2 word density, common structural patterns (e.g. "it's not just X, it's Y"), and formatting excess (bullet-to-prose ratio, bold-tag density). Use `--json` for machine-readable output, or `-` as the path to read from stdin. Treat its output as a diagnostic, not a mandate — a flagged phrase used once, on purpose, for real emphasis, is not a bug.
5. **Deliver the edited version.** Don't narrate the editing process to the user unless they asked for a diff or explanation — just hand over clean output.

## Quick reference: the highest-value fixes

If you only have time for a fast pass, prioritize these — they carry the most signal per fix:

**Vocabulary (see `references/prose-tells.md` for full tiers):**
`delve`, `tapestry`, `underscore`, `boundaries` (metaphorical), `testament to`, `landscape` (metaphorical), `realm`, `multifaceted` — these are rare in unforced human writing and easy to just delete or replace with the plain word.

**Structural patterns:**
- "It's not just X, it's Y" / "Not only... but..." — the single most recognizable AI tell. Cut the theatrical contrast; state the point once.
- Reflexive rule-of-three ("efficient, effective, and reliable") applied to everything, including things that don't have three parts. Use it when it's true and earned, not as a rhythm reflex.
- Hedge-stacking: "it is important to note that," "it is worth mentioning," "one must consider" — usually deletable with zero loss of meaning. Just say the thing.
- Generic scene-setting openers: "In today's fast-paced world," "In the ever-evolving landscape of X," "Imagine a world where..." Open with the actual first fact instead.
- False-balance closers: "Ultimately, the choice is yours," "Only time will tell," "As we move forward." Cut, or replace with an actual conclusion if you have one.

**Sycophancy / validation reflexes:**
Opening a response with "Great question!", "Absolutely!", or "You raise a really interesting point" before answering. If the question is genuinely interesting, show it by answering well — don't announce it.

**Formatting:**
Bullets, bold, and headers are tools for content that is genuinely list-like, parallel, or reference material to scan. They are not the default shape of an answer. A wall of bolded three-word headers over one-sentence bullets, applied to a question that wanted a paragraph, is a classic over-formatting tell (documented as a direct consequence of reward-model bias toward these formats, not a genuine readability improvement). When in doubt, write the paragraph first and only convert to a list if the content is actually enumerable and the list is easier to scan than prose.

**Em dashes:** Not inherently a tell — but a paragraph with three or four of them starts to read as machine-generated rhythm. If you notice more than one or two in a short passage, convert some to periods or commas.

## For code

Slop in code isn't about vocabulary — it's about unjustified complexity and unverified confidence. Read `references/code-slop.md` before finishing any non-trivial code task. The short version: match the codebase's existing conventions instead of writing "generically good" code; don't add abstraction layers, config options, or try/except blocks the task didn't call for; never invent a function, library, or API you haven't verified exists; and don't add comments that just restate what the line already says.

## A calibration note

The goal is writing and code that are specific, earned, and fit their context — not writing that performs "not being AI" by adding typos, forced casual slang, or artificial imperfection. Those are their own kind of tell and often read worse. Likewise, don't strip out every list, every "crucial," or every friendly opening line on principle — sometimes a bulleted list really is the clearest format, and sometimes something genuinely is crucial. The self-edit pass should leave behind writing that's better because it's more specific and less padded, not writing that's deliberately rougher for its own sake.

## Reference files

- `references/prose-tells.md` — full tiered vocabulary list, phrase list, structural patterns, opener/closer clichés, and formatting guidance, each with why-it-happens context and a concrete before/after.
- `references/code-slop.md` — code-specific anti-patterns: over-engineering, error handling, hallucinated APIs, dead code, comment noise, convention-blindness, with before/after examples.
- `references/self-edit-checklist.md` — the condensed, repeatable pass to run over any draft or diff before delivering it.
- `references/research-notes.md` — the underlying research this skill is built on, with sources, for anyone who wants to go deeper or update the lists over time.
- `scripts/slop_scan.py` — standalone Python scanner for quantitative density checks on longer documents (no dependencies beyond the standard library).
