# Adaptive Deep Research Protocol

## Purpose

Use this protocol when a user needs broad, accurate, cited research rather than a quick lookup. The protocol is optimized for current information, technical due diligence, literature review, project evaluation, and contested questions.

## Core loop

1. **Frame**: restate the exact question, audience, decision, constraints, and freshness requirement.
2. **Map**: create an aspect map with source classes and subquestions.
3. **Seed**: search broadly with diverse queries and open primary anchors first.
4. **Extract**: record specific claims, locators, versions, dates, and source quality.
5. **Expand**: follow entities, citations, repository links, benchmark names, standards, datasets, issues, and changelogs.
6. **Verify**: run counterevidence searches and source-independence checks.
7. **Synthesize**: answer with evidence IDs, uncertainty labels, and a method appendix.

## Effort calibration

- `quick`: when the user needs orientation or a simple confidence check. Stop after 2-4 meaningful hops if evidence agrees.
- `standard`: when the user asks for a researched answer. Search enough to cover primary source, secondary explanation, and at least one counterevidence route.
- `deep`: when the user asks for comprehensive research, comparison, literature review, market/project due diligence, or an implementation decision.
- `exhaustive`: when the topic is high-impact, contested, fast-changing, safety/legal/medical/financial, or when the user explicitly asks for extensive coverage.

Do not force a fixed hop count. A run is sufficient when additional searching is unlikely to change the answer, the strongest claims have source support, and the gaps are clear.

## Aspect map template

| aspect | examples | preferred source classes |
|---|---|---|
| definitions and scope | terms, aliases, standards, entities | official docs, standards, papers |
| current state | latest version, release, policy, ranking, price, schedule | official docs, release notes, live repos, filings |
| evidence base | papers, benchmarks, datasets, experiments | papers, datasets, benchmark leaderboards, replications |
| implementation reality | source code, examples, issues, commits | GitHub, docs, tests, CI, releases |
| limitations | failure cases, critiques, risks, deprecated paths | issues, errata, reviews, security advisories, counterpapers |
| synthesis | what matters for the user's decision | evidence ledger and source graph |

## Breadth-first, then depth-first

Start with several distinct seed routes before diving deep:

- official or primary route;
- academic route;
- implementation/project route;
- user/local context route if files are provided;
- counterevidence route.

After the seed stage, pick the branch that resolves the largest uncertainty. Avoid chasing popularity signals unless they relate to the user's decision.

## Checkpoints

At each checkpoint, write a short public summary in the run notes or final method appendix:

- what is known;
- which claims are well supported;
- which claims are weak, stale, or contested;
- what source would most likely change the answer;
- whether to broaden, deepen, verify, or stop.

## Stop conditions

Stop research when most are true:

- the answer directly addresses the user's requested deliverable;
- high-impact claims have evidence IDs;
- key source classes have been checked or explicitly ruled out;
- counterevidence was searched for when the topic is debatable;
- current/version-sensitive claims were checked against recent or official sources;
- remaining gaps are labeled rather than hidden.

Continue beyond the nominal target only when a concrete unresolved claim would materially change the conclusion.

## Handling conflicting evidence

1. Separate factual disagreement from framing difference.
2. Prefer primary evidence for factual claims, but do not ignore credible criticism.
3. Check dates and versions before deciding which source supersedes another.
4. State the disagreement in the final answer, with evidence IDs for each side.
5. Avoid averaging claims that are not measuring the same thing.

## Handling missing evidence

When evidence is missing, say so explicitly:

- `not found in searched sources` for absent evidence after reasonable search;
- `single-source` for one credible source but no corroboration;
- `stale` for information likely outdated;
- `unclear` for conflicting or incomplete sources;
- `out of scope` for deliberately excluded branches.
