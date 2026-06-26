# Writing a good idea

A platform `idea` records a **concrete proposal**: apply a technique from a paper to an open **problem**. NOT a paper summary, NOT a restatement of a problem.

## Fields (what `publish` needs)
- `title`: one **searchable sentence** naming the proposal (e.g. "Use [method] to tackle [problem]"). NOT the method's own title.
- `data.background`: which open problem(s) this addresses and why they are stuck (2–4 sentences).
- `data.goal`: what the idea aims to achieve.
- `data.description`: the proposed approach — the method **and** how it maps onto the problem.
- `data.rationale`: **why the shot is strong** — the mechanistic reason this method fits this problem (this is the high bar).
- `data.source_methods`: one-element list containing the method id that supplies the technique.
- `data.target_problems`: list of problem ids it addresses (**≥1**; may be several if one method serves several problems).
- `data.source_domains`: domains list (filterable); = the method's ∪ the problems' domains.
- `domains` (top-level publish arg): same domains, so cross-domain "find similar" surfaces related work.
- `summary` (top-level, optional): one line.

> Searchable text = `title + background + goal + description + rationale` (NOT keywords). Put the de-dup-bearing words in those fields.

## The high bar (when to generate at all)
Generate an idea **only** when:
- **Specific**: a reader can tell what would count as progress.
- **Mechanistically plausible**: you can explain *why* the technique addresses *that* problem, not just "both are about X".
- **Genuinely open**: the source paper does not already solve the target problem.
- **Distinct**: you de-duplicated it against existing ideas (workflow step 6).

Most papers yield **0 ideas**. A vague topical overlap is not enough — drop it.

## De-dup guideline (step 6)
Two ideas are the **same** if they pair the same kind of technique with the same problem, even in different words → keep one. If a candidate only **partially** overlaps an existing idea, rewrite it to state the *new* part (different mechanism, different problem, the next step).

## Bad examples (avoid)
- Restating the paper ("This paper proposes X") — a summary, not an idea.
- Restating a problem without a proposed technique.
- Too broad ("Apply machine learning to photocatalysis").
- A near-duplicate of an existing idea with different words.
- An idea with no `target_problems` — this skill is strictly problem-driven.

## Good example
- **title**: "Use a single-atom Co/N-C catalyst to break the >3% loading recombination wall in BiVO4 photoanodes."
- **target_problems**: `["prob_ab12cd34"]`
- **rationale**: explains that single-atom dispersion avoids the cluster formation that drives recombination above the loading threshold named in the problem — a specific, mechanistic fit, not a topical guess.
