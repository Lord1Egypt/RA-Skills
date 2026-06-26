# Loop State Machine

The autonomous pipeline is a state machine with 10 phases. Phases 1-4 run once (setup). Phases 5-9 iterate until convergence. Phase 10 runs once at completion.

## Phase Diagram

```
INIT ──► DISCOVER ──► DISTILL ──► COUNCIL ──► SCORE
                                                │
                                     score < 100│
                                                ▼
                  GAP_FILL ◄── RESCORE ◄── DEBUG ◄── BUILD
                      │
                      │ needs new experts
                      ▼
                   DISCOVER (single) ──► DISTILL (single) ──► update COUNCIL
                      │
                      │ score = 100 + all pass
                      ▼
                   SUBMIT (terminal)
```

## Phase Definitions

### Phase 1: INIT
- **Input**: User idea/domain string, optional target repo URL
- **Action**: Parse idea into domain spec, initialize directory layout, create domain.json
- **Output**: Initialized forum root with domain definition
- **CLI**: `python3 scripts/expert_distiller.py init`
- **Transition**: Always → DISCOVER

### Phase 2: DISCOVER
- **Input**: Domain topic, coverage axes
- **Action**: Web search for expert candidates, collect source URLs
- **Output**: Candidate JSON files with auto-collected source dossiers
- **Tools**: web-search-prime, web-reader
- **CLI**: `python3 scripts/expert_distiller.py discover` / `python3 scripts/expert_distiller.py candidate` / `python3 scripts/expert_distiller.py source`
- **Transition**: Always → DISTILL
- **Minimum**: At least 3 candidates discovered

### Phase 3: DISTILL
- **Input**: Candidate dossiers with source URLs
- **Action**: Audit each candidate, LLM-driven profile filling from sources
- **Output**: Promoted expert profiles with filled contract fields
- **Agent**: profile-distiller
- **CLI**: `python3 scripts/expert_distiller.py audit` / `python3 scripts/expert_distiller.py fill` / `python3 scripts/expert_distiller.py profile`
- **Transition**: Always → COUNCIL
- **Gate**: At least 2 experts must pass promotion audit

### Phase 4: COUNCIL
- **Input**: Promoted expert profiles
- **Action**: Form council with role assignment, weight balancing
- **Output**: Council definition JSON
- **CLI**: `python3 scripts/expert_distiller.py council create`
- **Transition**: Always → SCORE

### Phase 5: SCORE (first pass)
- **Input**: Council definition, empty artifact
- **Action**: First scoring pass — all axes start at 0 (no artifact exists yet)
- **Output**: Scoring report with total = 0, gaps = "everything"
- **Agent**: maturity-scorer
- **CLI**: `python3 scripts/expert_distiller.py score`
- **Transition**: Always → BUILD (first pass always needs work)

### Phase 6: BUILD
- **Input**: Domain spec, expert profiles, scoring report (gaps), council lenses
- **Action**: Generate project code targeting weakest axes
- **Output**: Built artifact at target repo
- **Agent**: project-builder
- **CLI**: `python3 scripts/expert_distiller.py build`
- **Transition**: Always → DEBUG

### Phase 7: DEBUG
- **Input**: Built artifact
- **Action**: Run verification loop (build, types, lint, tests, security, diff)
- **Output**: Verification report (PASS/FAIL per stage)
- **Transition**:
  - All PASS → RESCORE
  - Any FAIL → fix and re-run DEBUG (up to 3 retries per failure)
  - 3 retries exhausted → GAP_FILL with debug failure as gap

### Phase 8: RESCORE
- **Input**: Council definition, improved artifact, previous scoring report
- **Action**: Full 4-axis scoring with council debate protocol
- **Output**: Updated scoring report
- **Agent**: maturity-scorer
- **CLI**: `python3 scripts/expert_distiller.py score`
- **Transition**:
  - total = 100 + verification all PASS → SUBMIT
  - total < 100 → GAP_FILL
  - iteration > max_iterations → PAUSE

### Phase 9: GAP_FILL
- **Input**: Latest scoring report, coverage analysis
- **Action**: Identify gaps, determine if new experts needed
- **Output**: Gap analysis with recommendations
- **Agent**: gap-analyst
- **CLI**: `python3 scripts/expert_distiller.py coverage`
- **Transition**:
  - Missing expertise → DISCOVER (single candidate, fast-track)
  - Knowledge gaps (no new expert needed) → BUILD
  - Score regression → BUILD with focus on regressed axis

### Phase 10: SUBMIT
- **Input**: Final artifact, scoring report (100/100), verification report
- **Action**: Create branch, commit, push, create PR
- **Output**: GitHub PR URL
- **Transition**: Terminal (pipeline complete)

## Convergence Criteria

The pipeline terminates only when ALL conditions are met:

1. **Maturity score = 100** (sum of 4 axes, each exactly 25)
2. **Verification all PASS** (build, types, lint, tests, security, diff)
3. **No coverage gaps** flagged by gap analyst
4. **Council consensus** that artifact is submission-ready

These conditions are intentionally strict. A score of 100 means the expert council cannot find meaningful improvements.

## Failure Recovery

### Max Iterations Reached (default: 10)
- Write pipeline state to disk
- Generate maturity report with current scores
- Print summary with specific gaps preventing convergence
- Status: `paused`

### Build Failure After 3 Retries
- Log failure details to `build_logs/`
- Flag the failing axis in pipeline state
- Continue to GAP_FILL to potentially re-approach the build differently

### Score Regression (score decreases between iterations)
- If score drops by >10 points, pause and flag for review
- Use the previous iteration's artifact as base for next attempt
- Log the regression with expert vote details

### Context Window Pressure
- After each iteration, check remaining context budget
- If <30% remaining, compact: write full state to `pipeline_state.json`, summarize history
- Next iteration reads state from disk, starts with clean context

## Pipeline State File

Stored at `<root>/pipeline_state.json`:

```json
{
  "domain": "domain-id",
  "current_phase": "rescore",
  "iteration": 3,
  "max_iterations": 10,
  "last_score": {
    "total": 72,
    "breadth": 20,
    "depth": 18,
    "thickness": 15,
    "effectiveness": 19
  },
  "status": "running",
  "started_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T01:00:00Z",
  "target_repo": "https://github.com/user/project",
  "github_branch": "council-pilot/domain-id",
  "active_council": "domain-id-main",
  "experts_added_mid_loop": [],
  "history": [
    {
      "iteration": 1,
      "total": 35,
      "phase_reached": "rescore",
      "action": "initial_build"
    },
    {
      "iteration": 2,
      "total": 72,
      "phase_reached": "rescore",
      "action": "addressed_depth_gaps"
    }
  ],
  "build_failures": 0,
  "score_regressions": 0
}
```

Status values:
- `running`: pipeline is active
- `paused`: stopped due to max iterations or regression
- `converged`: score = 100, ready for submission
- `failed`: unrecoverable error
- `submitted`: PR created successfully
