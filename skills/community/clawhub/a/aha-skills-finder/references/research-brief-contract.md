# Research Brief Contract

This markdown contract is authoritative. Converted from JSON Schema; the prose contract is the source of truth for agent output.

Use this contract for Aha Skills Finder (https://github.com/its-How/aha-skills-finder) research brief artifacts. Do not add fields unless the skill explicitly asks for them.

## Minimum Output Shape

Every research brief must include `schema_version`, `created`, `target_outcome`, `day1_answer`, `constraints`, and `rounds`. `rounds` must contain at least one round. When `lanes` is present, it must contain at least one lane.

## Top-Level Fields

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `schema_version` | string | Yes | Constant `0.1` | Contract version. |
| `created` | string | Yes | Date string (RFC 3339 full-date) | Artifact creation date. |
| `target_outcome` | string | Yes | Non-empty outcome statement (minimum 10 characters) | Outcome the research brief is preparing to search for. |
| `lanes` | array of objects | No | At least one item when present | Optional lane-first decomposition for mixed outcomes. Use when one request contains distinct action modes that should not share one candidate pool. |
| `why_now` | string | No | Non-empty string | Why this search is needed now. |
| `day1_answer` | object | Yes | Contains required `expected_source`, `because`, `actual_outcome`, and `out_of_scope` | Initial answer and scope framing before deeper search. Do not add fields unless the skill explicitly asks for them. |
| `constraints` | object | Yes | Contains required `runtime`, `ecosystem`, `language_or_region`, and `excluded_capabilities` | Search constraints. Do not add fields unless the skill explicitly asks for them. |
| `source_gaps` | array of strings | No | May be empty | Known unavailable, weak, or missing source evidence. |
| `false_positives` | array of objects | No | May be empty | Candidates that looked relevant but are outside this brief or lane. |
| `rounds` | array of objects | Yes | At least one item | Search rounds. |

## `lanes` Item Fields

Use `lanes` for lane-first decomposition when a mixed outcome contains distinct action modes that should not share one candidate pool. `priority_source_families` are outcome-bound for the lane ecosystem and are not a universal mandatory checklist. `known_false_positives` are lane-relative and may still be valid in another lane. Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `lane_id` | string | Yes | Pattern `^[a-z0-9][a-z0-9-]*$` | Stable lane identifier. |
| `target_outcome` | string | Yes | Non-empty outcome statement (minimum 10 characters) | Lane-specific target outcome. |
| `out_of_scope` | array of strings | Yes | At least one non-empty string | Outcomes or action modes outside this lane. |
| `priority_source_families` | array of strings | Yes | At least one non-empty string | Outcome-bound source families for this lane ecosystem, not a universal mandatory checklist. |
| `known_false_positives` | array of strings | Yes | Non-empty strings | Lane-relative false positives that may still be valid in another lane. |

## `day1_answer` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `expected_source` | string | Yes | Non-empty string | Expected source or source family before deeper search. |
| `because` | string | Yes | Non-empty string | Reason for the Day 1 answer. |
| `actual_outcome` | string | Yes | Non-empty outcome statement (minimum 10 characters) | Actual outcome to search for after Day 1 framing. |
| `timing_hypothesis` | string | No | Non-empty string | Optional timing hypothesis for why the capability may exist or be emerging now. |
| `out_of_scope` | array of strings | Yes | May be empty | What the research brief will not search for. |

## `constraints` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `runtime` | array of strings | Yes | May be empty | Runtime constraints. |
| `ecosystem` | array of strings | Yes | May be empty | Ecosystem constraints. |
| `language_or_region` | array of strings | Yes | May be empty | Language or region constraints. |
| `excluded_capabilities` | array of strings | Yes | May be empty | Capabilities excluded from the search. |

## `false_positives` Item Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `name` | string | Yes | Non-empty string | False-positive candidate name. |
| `source_url` | string | Yes | Non-empty string | Source URL for the false-positive signal. |
| `why_false_positive` | string | Yes | Non-empty string | Why this candidate is out of scope for this brief or lane. |
| `could_be_valid_in_lanes` | array of strings | No | Each item pattern `^[a-z0-9][a-z0-9-]*$` | Other lanes where this candidate may be valid. |
| `query_correction` | string | Yes | Non-empty string | Query correction learned from the false positive. |

## `rounds` Item Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `round` | string | Yes | `R1`, `R2`, `R3` | Search round identifier. |
| `purpose` | string | Yes | Non-empty string | Purpose of the search round. |
| `queries` | array of strings | Yes | May be empty | Queries tried in this round. |
| `query_expansion` | object | No | Required fields when present are listed below | Evidence for exploratory query expansion, branching, and correction; especially useful in `R2` when ecosystem naming differs from seed terms. Do not add fields unless the skill explicitly asks for them. |
| `source_families` | array of strings | Yes | May be empty | Source families searched in this round. |
| `notes` | array of strings | Yes | May be empty | Round notes. |

## `query_expansion` Fields

Use `query_expansion` to record evidence for exploratory query expansion, branching, and correction; it is especially useful in `R2` when ecosystem naming differs from seed terms. Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `seed_queries` | array of strings | Yes | Non-empty strings | Initial terms from the user target, Day 1 answer, named runtime, or known ecosystem. |
| `expanded_queries` | array of strings | Yes | Non-empty strings | Expanded strings from synonyms, tooling verbs, runtime terms, package terms, claim terms, local-language terms, and spelling variants. |
| `query_branches` | array of strings | Yes | Non-empty strings | Branch labels such as `package-registry`, `skill-tooling`, `registry-native`, `curated-list`, `local-language`, or `false-positive-mining`. |
| `expansion_triggers` | array of strings | Yes | Non-empty strings | Why new terms were added, such as package descriptions, README claims, false positives, registry vocabulary, local-language terms, or source gaps. |
| `false_positive_corrections` | array of strings | Yes | Non-empty strings | Terms added or removed because a false positive showed the original query was too broad or lane-mismatched. |
| `new_terms_discovered` | array of strings | Yes | Non-empty strings | New ecosystem vocabulary discovered during the search. These are recall aids only, not quality or adoption signals. |
