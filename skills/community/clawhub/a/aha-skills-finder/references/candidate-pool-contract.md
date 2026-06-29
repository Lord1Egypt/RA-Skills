# Candidate Pool Contract

This markdown contract is authoritative. Converted from JSON Schema; the prose contract is the source of truth for agent output.

Use this contract for Aha Skills Finder (https://github.com/its-How/aha-skills-finder) candidate pool artifacts. Do not add fields unless the skill explicitly asks for them, except for the intentionally open `claims` and `verified` keyed objects.

## Minimum Output Shape

Every candidate pool must include `schema_version`, `created`, `target_outcome`, `find_stage_boundary`, `source_gaps`, `false_positives`, and `candidates`. `candidates` must contain at least one candidate. `find_stage_boundary.does` and `find_stage_boundary.does_not` must each contain at least one string.

## Top-Level Fields

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `schema_version` | string | Yes | Constant `0.1` | Contract version. |
| `artifact_type` | string | No | `research-output`, `synthetic-fixture` | Artifact classification. |
| `created` | string | Yes | Date string (RFC 3339 full-date) | Artifact creation date. |
| `target_outcome` | string | Yes | Non-empty outcome statement (minimum 10 characters) | Outcome the candidate pool is searching for. |
| `lane_id` | string or null | No | Pattern `^[a-z0-9][a-z0-9-]*$` | Optional lane id when a mixed outcome has been split before search. One candidate pool should describe one lane. |
| `lane_description` | string | No | Non-empty string | Optional lane-specific scope note, including adjacent lanes that are out of scope for this pool. |
| `why_now` | string | No | Non-empty string | Why this search is needed now. |
| `find_stage_boundary` | object | Yes | Contains required `does` and `does_not` arrays | Boundary of the find stage. Do not add fields unless the skill explicitly asks for them. |
| `source_gaps` | array of strings | Yes | May be empty | Known unavailable, weak, or missing source evidence. |
| `false_positives` | array of objects | Yes | May be empty | Candidates that looked relevant but are outside this pool or lane. |
| `candidates` | array of objects | Yes | At least one item | Candidate records found during research. |

## `find_stage_boundary` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `does` | array of strings | Yes | At least one item | What this find stage does cover. |
| `does_not` | array of strings | Yes | At least one item | What this find stage explicitly does not cover. |

## `false_positives` Item Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `name` | string | Yes | Non-empty string | False-positive candidate name. |
| `source_url` | string | Yes | Non-empty string | Source URL for the false-positive signal. |
| `lane_id` | string or null | No | Pattern `^[a-z0-9][a-z0-9-]*$` | Lane where this candidate is a false positive. Null means the artifact did not use lane decomposition. |
| `why_false_positive` | string | Yes | Non-empty string | Why this candidate is out of scope for this pool or lane. |
| `could_be_valid_in_lanes` | array of strings | No | Each item pattern `^[a-z0-9][a-z0-9-]*$` | Other lanes where this candidate may be valid; this prevents lane-relative false positives from becoming global rejections. |
| `query_correction` | string | Yes | Non-empty string | Query correction learned from the false positive. |

## `candidates` Item Fields

Do not add fields unless the skill explicitly asks for them, except for `claims` and `verified`, which are intentionally open keyed objects.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `candidate_id` | string | Yes | Pattern `^[a-z0-9][a-z0-9-]*$` | Stable candidate identifier. |
| `name` | string | Yes | Non-empty string | Candidate name. |
| `lane_id` | string or null | No | Pattern `^[a-z0-9][a-z0-9-]*$` | Lane where this candidate belongs when the artifact uses lane decomposition. Null or absent means the artifact did not use lane decomposition. |
| `candidate_role` | string | No | `capability`, `discovery-source`, `adjacent-index`, `adjacent-tooling`, `registry-index` | Optional role for separating ordinary capability candidates from source, index, and adjacent tooling candidates. `discovery-source`, `adjacent-index`, `adjacent-tooling`, and `registry-index` entries are recall surfaces only and must not be treated as an adoption shortlist. |
| `source` | object | Yes | Contains required `source_family`, `source_url`, and `repo_url` | Source where the candidate was found. Do not add fields unless the skill explicitly asks for them. |
| `entrypoint_url` | string | Yes | Non-empty string | Primary entrypoint for inspecting or using the candidate. |
| `candidate_type` | string | Yes | `skill`, `scripted-skill`, `prompt-only`, `docs-only`, `mcp`, `cli`, `plugin`, `registry-search-index`, `curated-list`, `extension`, `saas-provider`, `repo-tool`, `native-framework-capability` | Candidate type. |
| `candidate_surfaces` | array of strings | No | Items: `agent-skill`, `mcp-server`, `cli`, `package`, `web-editor`, `desktop-app`, `browser-extension`, `hosted-saas`, `official-api`, `native-runtime`, `source-repo`, `registry-index`, `curated-list`, `skill-library`, `skill-finder`, `skill-router`, `skill-manager`, `skill-installer`, `skill-marketplace`, `mcp-loader`, `skill-retrieval`, `skill-distillation`, `docs`, `prompt` | Optional finer surface tags for handoff typing. Tags are descriptive raw signals, not rankings. |
| `target_outcome` | string | Yes | Non-empty outcome statement (minimum 10 characters) | Outcome this candidate may serve. |
| `outcome_mode` | string | Yes | Non-empty string | Mode by which the candidate may serve the outcome. |
| `query_branch` | string | Yes | `skill-native`, `runtime-spec`, `source-code`, `package-cli`, `registry-search-index`, `outcome-native`, `extension-saas`, `mcp-agent-tool-catalog`, `false-positive-mining`, `curated-community`, `curated-recommended`, `package-registry`, `skill-tooling` | Search branch that produced or justified this candidate. |
| `metrics` | object | Yes | Contains required `installs`, `stars`, `forks`, `star_velocity`, `first_seen`, and `last_update` | Raw popularity, freshness, and availability signals. Do not add fields unless the skill explicitly asks for them. |
| `registry_stats` | object | No | Required fields when present are listed below | Optional registry-native raw signals for skills or capabilities found through marketplace/API/search endpoints. These fields are discovery signals only; they are not safety proof, source audit, maintenance verdict, or adoption recommendation. Do not add fields unless the skill explicitly asks for them. |
| `package_registry_stats` | object | No | Required fields when present are listed below | Optional package-registry raw signals. Package names, versions, descriptions, repository URLs, keywords, publish/update dates, and downloads are discovery signals only; they are not safety proof, source audit, maintenance verdict, or adoption recommendation. Do not add fields unless the skill explicitly asks for them. |
| `find_signals` | array of strings | Yes | May be empty | Evidence signals found during search. |
| `signal_completeness` | string | Yes | `high`, `medium`, `low`, `unknown` | Completeness of find-stage signals. |
| `false_positive_note` | string or null | Yes | String or null | Note explaining false-positive risk or lane boundary. |
| `deferred_boundary_tags` | array of strings | Yes | May be empty | Boundary questions deferred to later review. |
| `notes` | array of strings | Yes | May be empty | Candidate notes. |
| `adjacent_candidates` | array of objects | No | Item fields listed below | Related candidates or adjacent records. |
| `claims` | object | No | Open keyed object | Object for tool self-claims keyed by claim names or facets. |
| `claims_source` | string | No | URL string | URL to the claims page. |
| `verified` | object | No | Open keyed object | Object for confirmations keyed by verified facets. |
| `verified_method` | string | No | `source_inspection`, `web_search_corroboration`, `tool_smoke`, `docs_only` | Verification method used for `verified`. |

## `source` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `source_family` | string | Yes | Non-empty string | Source family or category. |
| `source_url` | string | Yes | Non-empty string | URL for the source record. |
| `repo_url` | string or null | Yes | String or null | Repository URL when available, otherwise null. |

## `metrics` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `installs` | integer or null | Yes | Minimum 0 when integer | Install count when available, otherwise null. |
| `download_signals` | array of objects | No | At least one item when present | Optional install/download/invocation raw signals. Capture source, period, and count when available; record gaps in `source_gaps` when unavailable. These are not quality, safety, or adoption verdicts. |
| `stars` | integer or null | Yes | Minimum 0 when integer | Star count when available, otherwise null. |
| `forks` | integer or null | Yes | Minimum 0 when integer | Fork count when available, otherwise null. |
| `star_velocity` | object or null | Yes | Required fields when non-null: `days_7`, `days_30`, `days_90` | Star velocity over 7, 30, and 90 day windows when available, otherwise null. |
| `recent_growth_proxy` | object or null | No | Required fields when non-null: `basis`, `summary` | Fallback freshness signal when true 7/30/90 day star velocity is unavailable. This is not a maintenance or quality verdict. |
| `first_seen` | string or null | Yes | String or null | First observed date or source timestamp when available. |
| `last_update` | string or null | Yes | String or null | Last update date or source timestamp when available. |

### `download_signals` Item Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `source` | string | Yes | Non-empty string | Source for the download or install signal. |
| `period` | string or null | No | Non-empty string or null | Period covered by the count. |
| `count` | integer or null | Yes | Minimum 0 when integer | Count value when available, otherwise null. |
| `source_url` | string or null | No | Non-empty string or null | Source URL for the count. |
| `note` | string or null | No | Non-empty string or null | Note about the signal. |

### `star_velocity` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `days_7` | integer or null | Yes | Integer or null | Star change over 7 days. |
| `days_30` | integer or null | Yes | Integer or null | Star change over 30 days. |
| `days_90` | integer or null | Yes | Integer or null | Star change over 90 days. |

### `recent_growth_proxy` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `basis` | array of strings | Yes | At least one non-empty string | Evidence basis for the fallback freshness signal. |
| `summary` | string | Yes | Non-empty string | Summary of the fallback freshness signal. |

## `registry_stats` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `registry` | string | Yes | Non-empty string | Registry name. |
| `slug` | string | Yes | Non-empty string | Registry slug. |
| `version` | string or null | Yes | String or null | Registry-reported version. |
| `downloads` | integer or null | Yes | Minimum 0 when integer | Registry-reported downloads. |
| `installs_all_time` | integer or null | Yes | Minimum 0 when integer | Registry-reported all-time installs. |
| `installs_current` | integer or null | Yes | Minimum 0 when integer | Registry-reported current installs. |
| `stars` | integer or null | Yes | Minimum 0 when integer | Registry-reported stars. |
| `file_count` | integer or null | Yes | Minimum 0 when integer | Registry-reported file count. |
| `file_hashes_available` | boolean or null | Yes | Boolean or null | Whether registry file hashes are available. |
| `registry_security_status` | string or null | Yes | String or null | Registry-provided scan/status label as a raw signal only. Do not treat clean/verified labels as safety proof. |

## `package_registry_stats` Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `registry` | string | Yes | Non-empty string | Package registry name. |
| `package_name` | string | Yes | Non-empty string | Package name. |
| `version` | string or null | Yes | String or null | Package version. |
| `description` | string or null | Yes | String or null | Package description. |
| `repository_url` | string or null | Yes | String or null | Package repository URL. |
| `downloads` | integer or null | Yes | Minimum 0 when integer | Package download count. |
| `downloads_period` | string or null | Yes | String or null | Period covered by the download count. |
| `created` | string or null | Yes | String or null | Package creation date. |
| `modified` | string or null | Yes | String or null | Package modification date. |
| `keywords` | array of strings | No | Non-empty strings | Package keywords. |
| `raw_claims` | array of strings | No | Non-empty strings | Claims copied or paraphrased from package metadata or README. These must remain raw signals. |

## `adjacent_candidates` Item Fields

Do not add fields unless the skill explicitly asks for them.

| Name | Type | Required | Allowed values or constraints | Description |
|---|---|---:|---|---|
| `candidate_id` | string | Yes | String | Adjacent candidate identifier. |
| `relationship` | string | Yes | `fork`, `competitor`, `superset`, `subset`, `related-registry-entry`, `shared-maintainer`, `shared-ecosystem` | Relationship to the current candidate. |
| `note` | string | No | String | Optional relationship note. |
