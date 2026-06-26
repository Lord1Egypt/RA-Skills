# Layered Memory Architecture

This skill separates memory by job instead of storing everything in one place.

## The three layers

### Instruction layer

This is the rule layer. It belongs in the host tool's durable instruction file.

Use it for:

- repo-wide conventions
- stable team expectations
- durable personal collaboration preferences
- approval and release boundaries

This layer should be hard to change and easy to trust.

### Session layer

This is the active work notebook for the current thread.

Use it for:

- what is being worked on now
- next steps
- important files
- key commands
- errors and corrections
- output artifacts produced in the session

This layer is optimized for continuity and compaction, not permanence.

### Durable layer

This is the cross-session fact layer.

Use it for:

- information about the user
- collaboration guidance
- project facts not visible in the repo
- references to external systems

This layer should be slower to grow than the session layer.

## Routing rules

Ask three questions before saving:

1. Is this already derivable from the repo
2. Will this matter outside the current thread
3. Is this a rule, a temporary state, or a reusable fact

Route based on the answer:

- rule -> instruction layer
- temporary state -> session layer
- reusable fact -> durable layer

## Durable memory hygiene

The durable layer fails when it becomes a junk drawer.

Watch for these smells:

- duplicate topic files
- stale release notes stored as memory
- copied commit summaries
- code structure that should have been rediscovered from the repo
- team policies mixed with one user's personal preference

When you see drift, prefer:

- consolidate
- shorten
- delete stale entries
- promote only the most stable items into the instruction layer

## Why this pattern works

It reduces two common agent failures:

- forgetting important non-code context
- polluting long-term memory with transient work details

The instruction layer tells the agent how to behave.
The session layer helps it resume work.
The durable layer helps it remember facts worth carrying forward.
