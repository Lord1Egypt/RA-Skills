# Branch Framework

## Goal

This document defines the standard branch skeleton for future Auto-Proteomics routes.

The purpose is not to claim new execution support immediately.
The purpose is to make every future branch:
- scientifically scoped
- AI-friendly
- low-ambiguity
- executable by smaller models
- consistent with the current decision -> execution architecture

## Standard branch contract

Every new branch should define these eight things explicitly:

1. Problem
- What exact proteomics problem does this branch solve?

2. Route trigger
- What shortest set of user-visible cues should activate this branch?
- What wording should a smaller model match first?

3. Inputs
- What files or metadata are required?
- What file family or upstream software is assumed?

4. Execution file
- What single execution file should the model call first?

5. Outputs
- What result files are expected?

6. Out-of-scope
- What should this branch explicitly refuse or defer?

7. Route disambiguation
- Which nearby branches are easy to confuse with this one?
- What one-line rule separates them?

8. Model-operability
- Can a smaller model tell when to use this branch?
- Can it map the request to the execution file without hidden assumptions?

## Required branch assets

Each branch should eventually have:

- one canonical route id
- one execution file under `scripts/workflows/`
- one branch spec under `references/branches/`
- one routing rule in `references/WORKFLOW_INDEX.yaml`
- one explicit input contract section
- one explicit output contract section
- one explicit out-of-scope section

## Canonical branch spec template

Use this structure for every future branch spec:

```text
Branch name
- route id
- status
- scientific goal
- route trigger
- route disambiguation
- expected upstream input family
- required files
- optional files
- minimal execution command pattern
- expected outputs
- out-of-scope
- validation target
- release-readiness checklist
```

## Status model

To reduce ambiguity, every branch should use one of these statuses:

- `idea`
- `scaffold`
- `prototype`
- `shipped`

Meaning:
- `idea`: concept only, no stable execution file yet
- `scaffold`: branch skeleton exists, but not release-ready
- `prototype`: partially runnable, still not public promise
- `shipped`: public and supported

## Branch naming rules

To keep routing model-friendly:
- route ids should be short and specific
- script names should map directly to route ids
- avoid synonyms for the same branch
- avoid mixing biological goal and software brand into one unstable name

Preferred style:
- `dda-identification`
- `dia-quant`
- `phospho-differential`
- `protein-enrichment`

## Release rule

A branch should not be released just because a script exists.
It becomes releasable only when:
- the route trigger is explicit
- the input contract is explicit
- the output contract is explicit
- the out-of-scope boundary is explicit
- the nearest confusing neighbor route is named
- a smaller model can identify the route and call it correctly
- at least one validation path is defined

## Small-model routing rule

Every branch spec should support a fast three-step decision:
- `What data is it?` example: proteomics vs phosphoproteomics
- `How was it acquired or produced?` example: DDA vs DIA, raw vs processed
- `What output does the user want?` example: identification vs quantification vs differential analysis

If any branch cannot be selected with those three questions plus one short branch-specific disambiguation rule, the spec is still too ambiguous.

## Current branch map

This branch map mixes the one public shipped route with internal non-shipped routes kept in the repository for framework development.

- `dda-lfq-processed`: shipped
- `dda-identification`: scaffold
- `dia-quant`: prototype
- `phospho-differential`: scaffold
- `protein-enrichment`: scaffold
- `multiomics-plan`: scaffold

## Recommended next-branch selection rule

When choosing the next real branch to build, prefer the branch that satisfies most of these:
- common real-world demand
- clear input contract
- strong scientific identity
- minimal overlap with already shipped path
- can be explained in low-token form
- can be executed through one clean entrypoint

Under that rule, the most natural next serious candidates are:
- `dia-quant`
- `phospho-differential`
