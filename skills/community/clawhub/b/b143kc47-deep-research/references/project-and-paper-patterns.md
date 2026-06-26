# Project and Paper Research Patterns

## Technical project due diligence

Use this when comparing tools, repositories, frameworks, MCP servers, model libraries, or data pipelines.

### Minimum checks

1. Official purpose and scope from README/docs.
2. Installation and quick-start path.
3. Current maintenance signals: latest release, recent commits, issue activity, maintainer presence.
4. Implementation evidence: source files, examples, tests, CI, or docs that prove the claimed feature exists.
5. Integration constraints: dependencies, runtime, API keys, supported platforms, license.
6. Failure signals: open bugs, breaking changes, deprecations, security issues, scalability limitations.
7. Independent signal: external tutorial, benchmark, user report, package registry, or downstream usage when available.

### Output fields

| project | claim | evidence | maintenance | risks | fit |
|---|---|---|---|---|---|

### Project evidence pitfalls

- A README may describe intended behavior that is not implemented.
- A demo may target an old version.
- A project may be popular but abandoned.
- Issues may overrepresent edge cases, but unresolved maintainer-confirmed issues are important.
- Licenses can decide whether the project is usable.

## Academic literature review

Use this when the user asks for papers, methods, benchmarks, or research direction.

### Minimum extraction fields

| field | question |
|---|---|
| bibliographic info | title, authors, venue/year, preprint vs peer-reviewed |
| problem | what problem is the paper trying to solve? |
| method | what is the core mechanism? |
| evidence | what benchmark, dataset, experiment, or theorem supports it? |
| result | what improved and by how much, under what setup? |
| limitations | what assumptions or failure modes are stated or implied? |
| artifacts | code, data, prompts, model, appendix |
| follow-up | citations, replications, surveys, competing methods |

### Literature map structure

Group papers by idea rather than by chronological order when useful:

- retrieval plus generation;
- interleaved retrieve/reason loops;
- self-critique or reflection;
- multi-agent/planner-executor research systems;
- graph or citation-network retrieval;
- evaluation and factuality benchmarks.

## Borrowed design patterns for deep research agents

### Interleaved retrieve-reason loop

Use retrieval as part of reasoning, not only as a one-shot prelude. The next query should depend on what was just learned, and the answer should change when better evidence arrives.

### Adaptive retrieval

Do not retrieve a fixed number of passages or hops regardless of need. Retrieve when the claim is uncertain, time-sensitive, contested, or missing primary support.

### Planner-executor-synthesizer separation

For complex tasks, separate roles:

- planner: decomposes scope and source routes;
- retriever/executor: gathers and logs evidence;
- verifier: looks for contradictions, freshness issues, and weak claims;
- synthesizer: writes the final answer with evidence IDs.

A single agent can play these roles sequentially.

### Source graph

Track relationships among hops, sources, evidence, claims, and contradictions. Use a graph mindset even when the physical artifact is a JSON file.

### Pre-writing outline

For long-form reports, do research before writing the outline. Then revise the outline using the evidence ledger rather than forcing evidence into a premature structure.

## Claim verification matrix

Use this table for important claims before finalizing:

| claim | evidence IDs | source independence | counterevidence checked | freshness checked | confidence |
|---|---|---|---|---|---|

Confidence labels:

- high: primary evidence plus independent corroboration, no strong unresolved contradiction;
- medium: credible evidence but limited independence, freshness, or scope;
- low: weak/single-source support, unresolved conflict, or missing primary source;
- unknown: searched evidence does not settle the claim.
