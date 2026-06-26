# English: AI-writing tells and rewrite moves

## Common “AI voice” tells

- Over-signposting: “Firstly/Secondly/Lastly”, “In conclusion”, “Overall”, repeated mini-summaries
- Stock transitions: “Moreover”, “Additionally”, “Furthermore”, “It is important to note that…”
- Generic confidence: polished, upbeat, safe, but low on concrete constraints, numbers, or lived specifics
- Hedging-by-default: “It depends…”, “There are pros and cons…” without choosing a stance or boundary
- Corporate filler: “leverage”, “robust”, “comprehensive”, “optimize”, “synergy” with no operational detail
- Over-helpful tone: “I hope this helps”, tutorial voice in contexts that should be direct
- Formatting “LLM fingerprints”: bold-everywhere, list-only answers, headings that read like a slide deck

## “AI Flavor” Patterns (High-Signal Clusters)

These are not “banned words”. The signal is clusters: multiple patterns showing up repeatedly in a short span.

- Inflated significance: making everything sound historically/culturally pivotal without evidence
  - Common shapes: “a testament to…”, “plays a vital role…”, “underscores the importance…”, “watershed moment…”
- Promotional / brochure tone: reads like marketing or tourism copy rather than a neutral explanation
  - Common shapes: “breathtaking”, “must-see”, “captivating”, “rich cultural heritage”
- Present-participle “pseudo-analysis” (-ing tails): extra commentary that adds vibe, not mechanism
  - Pattern: a factual clause + “..., improving/ensuring/highlighting …” with no causal chain
- Weasel attribution: vague authorities to create borrowed certainty
  - “experts say”, “industry reports suggest”, “observers note”, “studies show” (no source)
- Parallel negation / rhetorical contrast overuse:
  - “It’s not X, it’s Y.” / “Not only…, but also…”
- Rule-of-three habit:
  - triplets for adjectives/benefits/takeaways even when the list isn’t naturally three items
- Over-structured formatting:
  - too many headings, horizontal rules, bold “key terms”, short bullet-only sections

If you want a compact “sign → action” mapping (aligned with Wikipedia’s list), use `references/signs-of-ai-writing.md`.

## Rewrite moves (in priority order)

- Make the text falsifiable:
  - Add numbers, constraints, examples, edge cases, and what would change your mind
- Replace stock transitions with semantic ones:
  - Prefer “but/so/that said” and clean paragraph breaks over “Moreover/Additionally”
- Trade neutrality for decision + scope:
  - “I’d do X for Y; I wouldn’t do it when Z”
- Add voice without cosplay:
  - Use mild contractions, natural phrasing, and one personal anchor (experience, preference, small admission)
- Kill corporate filler:
  - If a word doesn’t change a decision (“robust”, “comprehensive”), delete it or specify the mechanism
- Fix formatting:
  - Keep lists short (max ~5 bullets) and explain the “why” in sentences
  - Use bold only for truly skimmable landmarks (1-3 per section)
- Remove high-frequency “AI closings” by default:
  - Avoid “I hope this helps” unless the user explicitly wants a friendly chat tone
  - Prefer a concrete closer: next step, decision, checklist, or a single clarifying question

## Citation / Evidence Discipline (Anti-Hallucination)

In English drafts, fake-looking citations are a major “AI flavor” tell and a content risk.

- No-source claims: if you can’t provide a link/DOI/identifier, rewrite as an observation and add conditions
- Citation sanity check (fast):
  - Search the exact title (in quotes) and the first author name
  - If a DOI is present, resolve it via `https://doi.org/<doi>` and confirm title/authors match
  - If you can’t find it quickly, treat it as unverified: remove the citation and downgrade certainty

For a more complete workflow, see `references/citation-verification.md` and the Hallucination Gate in `references/principles.md`.

## “Signs → Minimal Before/After Pairs” (aligned with `references/signs-of-ai-writing.md`)

1) Compulsive summaries / repeated closings
- Before: `Overall, this approach improves efficiency. In conclusion, it’s a strong option.`
- After: `Next step: run it on last week’s data and compare error rate and cycle time.`

2) Transitional signpost overload
- Before: `Moreover, we should update the process. Additionally, communication matters.`
- After: `The process is fine. The real bottleneck is handoffs—assign an owner and a deadline.`

3) Rule-of-three habit
- Before: `It’s fast, flexible, and scalable.`
- After: `It’s fast where it matters: it cuts the weekly report from 60 minutes to 15.`

4) “Sounds analytical” but no mechanism (often -ing chains)
- Before: `This improves alignment, ensuring consistency, enabling better outcomes.`
- After: `It enforces one definition of “active user” at query time, so metrics stop drifting.`

5) Rhetoric without new information
- Before: `It’s not just a change—it’s a transformation.`
- After: `We removed one duplicate review step; throughput increased ~30% with no quality change.`

6) Formatting toolkit fingerprints (headings/bullets/bold everywhere)
- Before: `## Key Takeaways\n- **Core**: efficiency\n---\nIn summary...`
- After: `Conclusion: remove the duplicate review step first. Then re-measure throughput.`

## When to ask for more info (don’t just “polish”)

- Missing goal/audience/channel
- No specifics (numbers, example, constraint, timeline, policy)
- Claims without sources (“studies show…”) or unverifiable references

Tip: For a compact “signs → rewrite moves” mapping, see `references/signs-of-ai-writing.md` (use it as a checklist, not a word blacklist).
