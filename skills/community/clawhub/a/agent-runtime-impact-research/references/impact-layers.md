# Impact Layers Analysis

Detail for Step 7 of the main workflow. Analyze each layer separately; a change that is large in one layer may be neutral in another.

## Layer 1: Model economics
- Does the release change inference cost, model routing, or local/offload options?
- Signal: pricing pages, provider support matrices, local-run requirements.

## Layer 2: Evaluation
- Does it change how agents are measured — event logs, replay, benchmark harness integration?
- Separate "recorded" (event log exists) from "evaluated" (correctness proven).

## Layer 3: Runtime / platform competition
- Which existing runtimes does it overlap with? Where does it differentiate (policy layer, sandbox, session model)?
- Compare against at least one integrated product and one open/configurable runtime.

## Layer 4: Skills and plugins
- Composition model: temporal (lifecycle effects) vs spatial (dependency coordination).
- Security story: scanning, approval, supply-chain position.

## Layer 5: Agent / subagent design
- Does it change how subagents are spawned, isolated, or reviewed?

## Layer 6: Enterprise security & governance
- Audit trail, approval gates, credential handling, data residency.

## Layer 7: Local / private deployment
- Can it run fully offline? What breaks without network access?

## Output discipline
For each layer, write one of: `immediate change`, `likely 6–18 months`, `uncertain`, `no change` — with a one-line justification. Mark speculation as judgment.
