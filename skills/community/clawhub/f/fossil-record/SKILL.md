---
name: fossil-record
version: 1.0.0
description: >
  Git archaeology engine that reconstructs the WHY behind code — not what
  changed, but what pressures, failures, and pivots shaped the codebase into
  its current form. Reads commit history the way a paleontologist reads
  sediment layers: to understand the forces that created the present.
author: J. DeVere Cooley
category: code-archaeology
tags:
  - git-analysis
  - code-history
  - decision-reconstruction
  - archaeology
metadata:
  openclaw:
    emoji: "🦴"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - history
---

# Fossil Record

> "Code tells you what a system does. History tells you what a system *survived*."

## What It Does

`git blame` tells you WHO changed a line. `git log` tells you WHEN. Fossil Record tells you **WHY** — by analyzing patterns across the entire commit history to reconstruct the evolutionary pressures that shaped the codebase.

Every line of code is the result of a decision. Most decisions aren't documented. But they leave fossils: commit patterns, revert sequences, hotfix clusters, refactor waves, and the sediment of a hundred small choices that accumulated into the architecture you see today.

## The Geological Model

Fossil Record treats your git history as a geological record, with distinct layers and eras:

| Geological Concept | Code Equivalent |
|---|---|
| **Sediment Layers** | Periods of steady development (feature commits) |
| **Fault Lines** | Major refactors, rewrites, or architecture changes |
| **Impact Craters** | Incident responses, emergency hotfixes, reverts |
| **Fossil Beds** | Code that hasn't changed in a long time (stable or forgotten?) |
| **Erosion Patterns** | Gradual drift from original design intent |
| **Extinction Events** | Deleted modules, abandoned features, removed dependencies |
| **Adaptive Radiation** | Rapid diversification after a major change (new abstraction spawning many implementations) |

## The Eight Excavation Modes

### 1. Pressure Analysis
**Question:** What external forces shaped this code?

Analyzes commit message patterns, timing, and clustering to identify:
- **Deadline pressure**: Commits accelerating toward a date, then stopping
- **Incident pressure**: Hotfix → fix → fix-the-fix → revert → different-fix patterns
- **Stakeholder pressure**: Feature requests appearing as interruptive commit sequences
- **Technical debt pressure**: Refactors that are started, abandoned, restarted

```
Output: Timeline of external pressures with their impact on code quality.
Example: "Between March 3-17, commit velocity tripled and test coverage
dropped from 84% to 61%. Three hotfixes followed in the next week.
This region of code still carries the scars of that deadline."
```

### 2. Decision Reconstruction
**Question:** What decisions were made here, and what alternatives were considered?

Analyzes:
- Reverted commits (something was tried and rejected)
- Branches that were created but never merged (abandoned approaches)
- Comments that reference alternatives ("we could have used X but...")
- Sequential implementations of the same feature (iteration history)

```
Output: Decision tree showing what was tried, what stuck, and what was abandoned.
Example: "Authentication was implemented 3 times:
  v1 (session-based, commits a1b2..c3d4, reverted)
  v2 (JWT, commits e5f6..g7h8, lived 4 months)
  v3 (OAuth2, commits i9j0..k1l2, current)
  Pressure: v1→v2 driven by scaling issues. v2→v3 driven by SSO requirement."
```

### 3. Hotspot Archaeology
**Question:** Why is this specific area of code so volatile?

Goes beyond "this file changes often" to ask "what *kind* of changes happen here and what drives them?"

```
CHANGE TAXONOMY:
├── Bug Fix: Same function modified to fix different bugs (fragile design)
├── Feature Accretion: Function grows as features are bolted on (missing abstraction)
├── Config Churn: Constants/thresholds repeatedly adjusted (unclear requirements)
├── Refactor Oscillation: Code restructured back and forth (no consensus on design)
└── Dependency Turbulence: Changes driven by upstream library updates (fragile coupling)
```

### 4. Extinction Mapping
**Question:** What used to be here, and why did it die?

Traces deleted code through git history to reconstruct what was removed and the conditions of its removal:
- Was it replaced? By what?
- Was it gradually abandoned or suddenly deleted?
- Did its removal cause any subsequent issues (fixes referencing the deleted module)?
- Is anything still alive that was designed to work with the extinct module?

```
Output: Extinction timeline showing what disappeared, when, and what it left behind.
Example: "The 'recommendations' module was deleted in commit x1y2z3 (June 2024).
  3 orphaned database tables still exist.
  2 API routes still reference recommendation types in their schemas.
  1 test file still imports a mock of the recommendation engine."
```

### 5. Sediment Dating
**Question:** How old is this code *really*, and has it been maintained or just preserved?

For each module/file, determines:
- **Birth date**: When was it first created?
- **Last meaningful change**: Not just whitespace/formatting — actual behavior change
- **Maintenance frequency**: Is it regularly updated or untouched?
- **Author diversity**: Has only one person ever modified this? (bus factor = 1)
- **Era classification**: Which architectural era does this code belong to?

```
Output: Age map of the codebase with era boundaries.
Example:
  src/auth/     Born: 2023-01, Last modified: 2025-11, Era: "Current" (3rd gen)
  src/utils/    Born: 2021-06, Last modified: 2022-03, Era: "Founding" (1st gen)
  src/payments/ Born: 2024-08, Last modified: 2024-08, Era: "Growth" (2nd gen)
  ⚠️ src/utils/ hasn't been meaningfully modified in 3 years. Fossil bed.
```

### 6. Fault Line Detection
**Question:** Where are the tectonic boundaries in this codebase?

Identifies major architectural shifts by finding:
- Large-scale rename/move operations
- Dependency replacements (library A → library B)
- Directory restructuring
- Changes to build systems, frameworks, or deployment targets

```
Output: Fault line map showing architectural eras and their boundaries.
Example: "3 major fault lines detected:
  1. [2022-09] Monolith → microservices split (142 files moved)
  2. [2023-06] REST → GraphQL migration (89 files modified)
  3. [2024-03] JavaScript → TypeScript conversion (204 files renamed)
  Warning: Fault line #2 is incomplete. 23 endpoints still REST."
```

### 7. Author Topology
**Question:** How was knowledge distributed, and where are the gaps?

Maps which developers contributed to which areas, and identifies:
- **Knowledge monopolies**: Areas only one person has ever touched
- **Knowledge transfers**: When a new contributor takes over an area
- **Knowledge voids**: When all contributors to an area have left the project
- **Collaboration patterns**: Which areas have healthy multi-author contribution

```
Output: Knowledge topology map with risk assessment.
Example: "src/billing/ — ALL 247 commits by developer X (last active: 2024-01).
  Developer X is no longer on the team.
  No other contributor has ever modified this module.
  Knowledge void. Recommend: dedicated onboarding session for this module."
```

### 8. Evolution Trajectory
**Question:** Where is this codebase *heading*?

Extrapolates from historical patterns to predict:
- Which areas are actively evolving (increasing commit diversity and frequency)
- Which areas are calcifying (decreasing modifications, aging contributors)
- Which architectural patterns are expanding vs. contracting
- What the next likely "extinction event" or "fault line" might be

```
Output: Trajectory forecast based on historical momentum.
Example: "The codebase is trending toward:
  ✓ Full TypeScript adoption (92% converted, ~2 months to completion)
  ✓ GraphQL as primary API layer (78% migrated)
  ⚠ Growing divergence between /api and /services naming conventions
  ⚠ Test coverage declining in modules > 2 years old (neglect pattern)"
```

## Integration

```
Invoke Fossil Record when:
├── Joining a new project      → Run full geological survey
├── Before modifying old code  → Run sediment dating + decision reconstruction
├── After an incident          → Run pressure analysis on the affected area
├── During architecture review → Run fault line detection + evolution trajectory
├── When someone asks "why?"   → Run decision reconstruction on that specific area
└── Onboarding new developers  → Generate the complete evolutionary narrative
```

## Output: The Geological Survey

```
╔══════════════════════════════════════════════════════════════╗
║                 FOSSIL RECORD: GEOLOGICAL SURVEY            ║
║                 Repository: acme-platform                   ║
║                 History depth: 3 years, 4,721 commits       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ERAS IDENTIFIED: 3                                          ║
║  ├── Founding (2022-01 → 2022-09): Monolith, Express, JS    ║
║  ├── Growth (2022-09 → 2024-03): Microservices, REST, JS/TS ║
║  └── Current (2024-03 → now): Microservices, GraphQL, TS    ║
║                                                              ║
║  FAULT LINES: 3 major, 7 minor                              ║
║  IMPACT CRATERS: 12 incidents (3 P0, 5 P1, 4 P2)           ║
║  FOSSIL BEDS: 4 modules unchanged > 18 months               ║
║  KNOWLEDGE VOIDS: 2 modules (all authors departed)          ║
║  EXTINCTION EVENTS: 8 modules deleted, 3 left artifacts     ║
║                                                              ║
║  TRAJECTORY: Healthy evolution with 2 risk areas             ║
╚══════════════════════════════════════════════════════════════╝
```

## Why It Matters

Code review looks at the **present**. Testing validates the **expected**. Fossil Record illuminates the **past** — because a codebase that doesn't understand its own history is condemned to repeat its own mistakes.

Zero external dependencies. Pure git analysis. No APIs, no cloud, no cost.
