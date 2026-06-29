---
name: aha-skills-finder
description: Use when an agent needs to surface skill/capability candidates that first-pass registry, package, or search queries would likely miss. Covers skills, MCPs, CLIs, plugins, registries, extensions, SaaS/provider routes, repo tools, and native runtime capabilities. Produces multiple traceable candidates and raw signals; does not rank for adoption, audit safety, install, enable, or perform live/external actions.
license: MIT-0
compatibility: "Runtime-agnostic method; benefits from agent runtime with web search and fetch capabilities. Operates in fail-fast mode without search."
metadata:
  repository: https://github.com/its-How/aha-skills-finder
  version: "1.0.0"
---

# Aha Skills Finder

Use this skill when a target outcome needs the agent to identify the skill or
capability that matches the target need, not merely the first candidate an
obvious registry, package search, or query returns. The output is an aha-shaped
discovery artifact: multiple traceable candidates, source gaps, query
corrections, and raw signals. Not one best answer.

This is runtime-agnostic. Treat this `SKILL.md` as a portable agent-readable method contract, not as a Codex-only package or an install recipe. Runtime-specific metadata belongs in `adapters/` only after evidence-gated validation.

This is not a tutorial or marketing surface. Optimize for agent execution, machine-readable artifacts, and compact scope checks. Do not add quickstarts, screenshots, or docs-site prose unless they directly improve agent execution.

There is no universal best skill. Aha names the discovery moment when an agent
identifies the skill or capability that matches the target need. Expanded source
surfaces, query expansion, raw signals, and traceable surprises are methods for
reaching that moment; adoption judgment stays in later gates.

Timing matters. Discovery is not abstract optimization: too early means the ecosystem may not exist yet, too late means the useful window may have passed. Capture why the search should happen now.

The core advantage is not confidence theater. It is recall with provenance. A
run of `aha-skills-finder` reduces false negatives by searching the places where
the capability is likely to live, including registry-native surfaces that may
not have standalone repos or packages, and package-registry tooling that may
function as skill libraries, routers, loaders, managers, installers, or
marketplaces rather than individual skills.

aha-skills-finder complements third-party skill libraries, finders, routers,
managers, installers, marketplaces, and MCP loaders. Those tools are valid
discovery surfaces and candidates, but they often search one ecosystem, mix
find/adopt actions, or turn package/list metadata into recommendation language.
This method fills the gap by producing cross-surface, lane-scoped, raw-signal
candidate pools for later stages to audit or adopt separately.

## Find-Stage Scope

This is find-stage only.

Do:

- discover multiple candidates;
- widen the source surface;
- record query branches, false positives, gaps, and raw signals;
- include adjacent capabilities that could become skills.

Do not:

- recommend adoption;
- score or rank final winners;
- perform source, safety, permission, maintenance, provider, browser, credential, login, live, or external-write audit;
- install, enable, configure, replace, publish, deploy, or mutate runtime config.

Do not treat third-party tool claims as aha-skills-finder conclusions. A package that claims
large catalogs, token savings, fast routing, many runtime integrations, or
curated quality is still only a raw candidate until a later audit or adoption
stage verifies that claim.

## Inputs

Ask for or infer:

- target outcome;
- why now;
- target runtime or ecosystem, if any;
- lane split, when the request mixes different action modes;
- excluded adjacent capability;
- region/platform/language constraints, if relevant;
- time budget or bounded-round count.

Start with a Day 1 Answer:

```text
If I did no research, I would expect the strongest capabilities to come from ______ because ______.
The actual outcome is ______.
This should be searched now because ______.
Adjacent capabilities that are out of scope are ______.
```

If the requested outcome mixes different action lanes, split before searching.
Do not force one candidate pool to cover incompatible lanes such as final
publish, draft creation, formatting, conversion, monitoring, and analytics.

For each lane, record:

- lane id;
- lane-specific target outcome;
- out-of-scope adjacent lanes;
- priority source families for that lane ecosystem;
- known lane-relative false positives.

## Workflow

### R1: Source-Surface Recall

Build a heterogeneous discovery surface before judging candidates. Source coverage is outcome-bound: choose source families that match the lane ecosystem, not a generic global checklist. Cover as many relevant source families as the task warrants:

- skill registries, registry public APIs, marketplace search endpoints, and
  search indexes;
- runtime/spec docs;
- GitHub/Gitee/GitLab repo and code search;
- package registries such as npm, PyPI, crates, and Homebrew, including
  package-native search for skill libraries, finders, routers, managers,
  installers, marketplaces, MCP loaders, and retrieval/distillation tools;
- MCP and agent-tool catalogs;
- extension, SaaS, and provider surfaces;
- native framework/runtime capabilities;
- curated/recommended skill lists, community indexes, and trackers.

For skill-class outcomes, do not stop at repo or package search. Attempt the
registry-native marketplace, public API, or search endpoint for the relevant
skill ecosystem when one is available or named by the user. A GitHub/npm miss is
not evidence that a registry-native skill does not exist.

For skill-discovery outcomes, do not stop at skill bodies or curated lists.
Search for adjacent skill tooling: libraries, finders, routers, managers,
installers, marketplaces, MCP lazy loaders, and skill retrieval/distillation
systems. These are candidate sources or adjacent tooling, not automatic
replacements for aha-skills-finder and not adoption recommendations.

API, code-search, marketplace, or registry failures are source gaps, not no-hit
evidence. Record the failure surface and failure type, for example unauthenticated
code search, rate limit, endpoint unavailable, private registry, or unsupported
search syntax.

For ordinary bounded outcomes, pressure-test toward 20+ raw candidates. For narrow platform outcomes, fewer is acceptable only if source gaps are explicit.

Treat installs and downloads as first-class raw discovery signals when available.
Examples include skill marketplace installs, package registry downloads, extension
store installs, registry invocation counts, and package download windows. If a
surface does not expose the signal, record the source gap instead of inferring
adoption.

Keep telemetry split by evidence surface. Registry installs or invocations
belong to the registry surface; package downloads and download windows belong to
the package surface; repo stars, forks, pushed dates, and releases belong to the
source-repo surface; extension or store ratings and installs belong to the
extension/store surface. Do not merge these into a single quality score, ranking,
or adoption verdict.

Registry-provided stats and scan labels are raw signals only. Record downloads,
installs, stars, file counts, file-hash availability, and registry security
status when exposed, but do not treat them as safety proof, source audit, or
adoption recommendation.

Repo-level metrics need a monorepo caveat. Stars, forks, and pushed dates for a
large repo are discoverability and context signals for the candidate path, not
proof of subskill quality or fit. Preserve the monorepo subpath when visible and
defer subskill audit to a later stage.

Curated, recommended, "best", "awesome", roundup, and leaderboard lists are
discovery surfaces. Use them for cold-start recall, ecosystem vocabulary, and
candidate names. Do not treat a list's recommendation language as an adoption,
quality, or safety verdict.

When the lane is specifically about finding good skill recommendation sources,
use `source-registries/curated-skill-lists.yaml` as a seed list. Treat that file
as a maintained discovery-source registry, not as a list of endorsed skills.

### R1b: Candidate Identity Cross-Map

Before comparing candidates, cross-map each plausible candidate identity across
the surfaces that expose it:

- registry id, slug, display name, and version when available;
- source repo URL and source path;
- package name and package registry URL;
- monorepo subpath for the specific skill, adapter, plugin, or tool;
- runtime adapter path if it is visible in the repo or package;
- source gap when any mapping cannot be confirmed.

Mapping failures are source gaps, not market-absence claims. Useful examples are
registry query returned zero results, package download API returned not found
after package search found a candidate, repository URL returned 404, code search
was unauthenticated or rate-limited, or a marketplace page was readable but no
public API was visible.

The cross-map output lives in the candidate pool as:
1. `source.repo_url` — canonical source repository.
2. `source.registry_id` — registry/package identifier if different from name.
3. `entrypoint_url` — the actual URL an agent would use to access the capability.
4. `notes` — any cross-map discrepancies (e.g., "npm package name differs from repo name").

If a candidate appears under multiple identities, create one candidate with all cross-map fields populated, not duplicate candidates.

### R2: Query Expansion, Branching, and Correction

Challenge R1 instead of deep-auditing favorites. Do not assume the user's first
words match the ecosystem's vocabulary. Build query branches from:

- seed terms from the target outcome;
- outcome verbs and target objects;
- execution surfaces and artifact or receipt terms;
- ecosystem synonyms such as catalog, directory, registry, marketplace, library,
  finder, router, loader, manager, installer, retrieval, and distillation;
- registry-native names, slugs, marketplace labels, and API field names;
- package-registry terms such as npm, PyPI, package, CLI, MCP server, lazy
  loading, on-demand loading, skill library, skill finder, skill router, skill
  manager, skill installer, skill marketplace, agent skill retrieval, and skill
  distillation;
- runtime terms such as Codex, Claude Code, Cursor, OpenClaw, MCP, agentskills,
  and SKILL.md;
- claim terms discovered from candidate metadata, such as lazy loading,
  on-demand skill loading, dynamic skill retrieval, portable skills, catalog,
  context reduction, or token reduction;
- curated-list terms such as recommended, best, awesome, roundup, leaderboard,
  directory, and their local-language equivalents;
- local-language equivalents when the target ecosystem, region, platform, or
  user language makes English-only search incomplete;
- adversarial misspellings, spacing variants, hyphenation variants, and casing
  variants for named skills or ecosystems;
- adjacent capability words;
- known false-positive terms.

When R2 performs non-trivial query expansion for a lane, preserve that evidence
in the research brief:

- seed queries;
- expanded queries;
- query branches;
- expansion triggers;
- false-positive corrections;
- new terms discovered.

Do not backfill query-expansion fields into old or trivial examples merely to
satisfy the schema; preserve them when they explain a real search correction.

Keep a small false-positive set as query correction evidence. Convert false
positives into better query terms instead of only dropping them. False positive
is lane-relative: it means "not for this lane/outcome", not "bad candidate". A
candidate can be false positive for a publish lane and valid for a formatting
lane.

When true 7/30/90 day star velocity is unavailable, use a recent-growth proxy
instead of leaving the freshness question implicit. Record the proxy basis, such
as created date, current stars, forks, pushed/updated time, release cadence, or
package download cadence. This remains a raw discovery signal, not a quality or
maintenance verdict.

### Handling R2-Discovered Candidates That Should Have Been in R1

When R2 query expansion surfaces candidates that clearly match the original R1 target outcome but were missed:
1. Add them to the candidate pool normally.
2. Set `query_branch` to the R2 branch that found them.
3. Add a `notes` entry: "R2-discovered; missed in R1 due to [reason: narrow query / missing source family / registry gap]."
4. Record the gap in `source_gaps` as: `{ gap_type: "r1_miss", source_family: "...", reason: "..." }`.

Do NOT retroactively modify R1 results.

### R3: Candidate Pool

Convert recall into a candidate pool artifact using `references/candidate-pool-contract.md`.

Keep candidates that have traceable source and plausible outcome proximity. Hold selected partial hits if they improve discovery coverage. Drop unrelated or untraceable noise.

Do not use adoption risk, safety, or maintenance as find-stage filters.

Keep candidate typing split across three axes:

- `candidate_type` is the physical shape, such as `skill`, `mcp`, `cli`,
  `registry-search-index`, or `curated-list`;
- `candidate_role` is the find-stage semantic role, such as `capability`,
  `discovery-source`, `adjacent-index`, `adjacent-tooling`, or
  `registry-index`;
- `candidate_surfaces` are descriptive handoff tags, not rankings or roles.

These axes may combine. For example, `candidate_type=mcp` +
`candidate_role=discovery-source` + `candidate_surfaces=["skill-library"]` is a
valid way to record an MCP server that acts as a skill-library discovery source.

Useful surface tags include `agent-skill`, `mcp-server`, `cli`, `package`,
`web-editor`, `desktop-app`, `browser-extension`, `hosted-saas`,
`official-api`, `native-runtime`, `source-repo`, `registry-index`,
`curated-list`, `skill-library`, `skill-finder`, `skill-router`,
`skill-manager`, `skill-installer`, `skill-marketplace`, `mcp-loader`,
`skill-retrieval`, `skill-distillation`, `docs`, and `prompt`. Surface tags are
descriptive only; they are not rankings.

## Stopping Conditions

Stop discovery only when all applicable handoff conditions are explicit, or when
the runtime budget or a hard limit prevents further discovery:

1. Planned rounds are complete or the explicit budget is exhausted.
2. Outcome-bound source coverage is explicit.
3. Important source gaps are recorded.
4. Major query expansion branches have been tried or deferred.
5. False positives have been converted into query corrections where useful.
6. Candidate identities are cross-mapped where available.
7. Candidate type, role, and surfaces are clear enough for handoff.

Do not stop merely because one plausible candidate appears, because one source
family produces enough candidates, or because the last query branch produced few
new candidates. When stopping before all planned rounds complete, record the stop
reason in the research brief `rounds[last].stop_reason` and mark remaining
rounds as `skipped` with `reason: "budget_exhausted"` or the specific runtime
limit that was hit.

## Outputs

Return or write:

- research brief matching `references/research-brief-contract.md`;
- candidate pool matching `references/candidate-pool-contract.md`;
- source gaps and false positives;
- deferred scope tags for later adoption-stage gates.

Preserve evidence surface per signal in machine-readable fields. Prefer the
existing `metrics.download_signals`, `registry_stats`,
`package_registry_stats`, `source`, `entrypoint_url`, `candidate_surfaces`,
`find_signals`, `source_gaps`, and notes fields rather than inventing a new
schema for every run. When a candidate has mixed evidence, keep each signal tied
to its surface, name, value, source URL, and window or timestamp where available.
Do not collapse registry, package, repo, and store signals into a single score.

Use `sources.yaml` as a source-family prompt and checklist, not a mandatory taxonomy.

## Source & Upgrade

- **Repository**: https://github.com/its-How/aha-skills-finder
- **Upgrade**: Run `git pull` in the skill directory, or re-run `npx skills add its-how/aha-skills-finder` to get the latest version.
- **Uninstall**: Delete the `aha-skills-finder/` directory from your skills path.

## Cannot Prove

A find-stage artifact cannot prove:

- a candidate is safe;
- a candidate is maintained well enough to adopt;
- a candidate should be installed or enabled;
- a candidate improves the consumer outcome;
- source, provider, browser, credential, or live readiness.
