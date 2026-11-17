# Changelog - Beckmann Knowledge Graph

All notable changes to the Beckmann Knowledge Graph are documented in this file.
The graph and the skill are intended to be iteratively refined. Agents should always check this file and `package.json` for the current version and prefer the latest available version.

Format: Based on Keep a Changelog. Latest version first.



## [4.1.1] - 2026-10-14

### Changed

- Changes made based on the ClawHub scanner findings:

  - New Version of the Graph-Overview-Generator.html

  - All Unicode control characters have been removed.

  - New Version of the SKILL.md


### Graph state as of v4.1.1
- Entities: 749
- Relations: 1290
- Parts: 4 (see `_meta.segment_total` in any part file for current count)





## [4.1.0] 

### Changed

- Two subgraphs created using the skill “beckmann-knowledge-graph-self-optimizer”: 
  - Institutional and Collective Reversal Dynamics in Social Systems
  - Reversal Mechanism Threshold Operationalization and Collective-Individual Differentiation

- Subgraph "dark matter": 
  - It incorporates the scientific principles currently under discussion. The currently preferred solution, the "Gravity factor", had already been included in the graph for some time.





## [4.0.0] 

### Changed

- BREAKING CHANGE – Structural reorganization: All data files moved into the subfolder `Results-and-Tools/`.
- The knowledge graph is now split into part files (`graph_Part_X_of_N.json`) for efficient staged loading.
- New loading strategy with four phases:
  - Phase 1: `graph_overview.json` — global structural map of the entire graph
  - Phase 2: `UNDERSTANDING-REPORT.md` — human-readable analytical interpretation
  - Phase 3: `graph_Part_X_of_N_summary.md` — lightweight content index per part (new)
  - Phase 4: `graph_Part_X_of_N.json` — full detail data, loaded selectively
- `graph.json`, `Knowledge-Graph-Splitter.html`, and `Graph-Overview-Generator.html` remain in `Results-and-Tools/` as maintenance tools and are not required for skill usage.
- SKILL.md completely rewritten to reflect the new loading strategy (v4.0.0).



## [3.1.0] 

### Changed

- new subgraph for connecting the human brain with quantum mechanics


## [3.0.1]

- BREAKING CHANGE - Quality update: `type` is now the canonical field name (not `typ`). This supersedes the note in v3.0.0.

## [3.0.0]

- Complete rewrite of skill wording.
- Versioning policy: All versioning information now lives exclusively in this CHANGELOG.md file. SKILL.md only contains a reference to this file, no hard-coded version numbers.
- Future-proofing against graph growth: Removed hard-coded counts (e.g., number of entities, relations, predicate frequencies, scientific_status distributions) from SKILL.md. The skill now instructs agents to read counts dynamically from graph.json. Where a number is mentioned for illustration, it is explicitly marked as "as of v3.0.0" and should be re-checked.
- Data model correction: graph.json now canonically uses `scientific_status` (with underscore) for both entities and relations. SKILL.md has been updated to reflect this as primary field, with backward-compatible fallback to `scientific status` (space) for older graphs.
- NOTE: In this version `typ` was declared canonical. This was superseded in v3.0.1 by `type`.

## [2.4.0]

- Quality update
- As of this version: All relations include a `scientific_status` field (canonical name; legacy `scientific status` still supported)
- The scientific status values were assigned following analysis by an AI model

## [2.3.0]

- Quality update
- Duplicate, multiple, and directly inverse relations have been removed
- As of this version: All entities include a `scientific_status` field (counts as of this release: ~681 entities - see graph.json for current)

## [2.2.0]

- Over 240 relations were optimized
- AI models were used to generate `descriptions` and verify `predicates`. Approximately 70% of the predicates were improved
- The entire process was automated using Markdown scripts and small HTML programs
- Descriptions underwent human review and minor corrections

## [2.1.0]

- language and narrative structure as a framework of expectations (topic generated independently by an AI model)
- assessment of expectations and measurement of dominance (topic generated independently by an AI model)
- climate systems as expectation and feedback dynamics (topic generated independently by an AI model)
- music (topic chosen by user, everything else generated independently by an AI model)

## [2.0.0]

- The first version created in self-improvement mode
- New topics generated independently by an AI model:
  - Game Theory
  - Behavioral Economics / Cognitive Biases
  - Capacity for action and free will
  - Nash equilibria as stabilizers of dominant expectations
- New graph structures created autonomously by an AI model
- "Autonomous" means operating according to a general script that can be reused, further developed, or optimized
- Remaining work automated using small HTML programs

## [1.4.0]

- Attempt to explain the Beckmann logic in greater detail
- Alan Watts' perspective
- Subsection on problem-solving strategies
- Problem hierarchy

## [1.3.0]

- stock trading

## [1.2.0]

- Subsection on "Art" with Albrecht Duerer
- Stockholm syndrome
- The Invisible Gorilla Experiment (1999) by Daniel Simons and Christopher Chabris, Inattentional Blindness 2.0 & Cognitive Ego Traps, Retrocausal Attention & Future Meaning (Daryl Bem), Survival-Based Attention & Threat Avoidance
- Duplicates removed
- Errors corrected

## [1.1.0]

- first being (limitation: the solvability of all problems in being is connected with the insolubility of the origin of first philosophical being)
- Three-body problem
- Squaring the circle and the goldfish analogy
