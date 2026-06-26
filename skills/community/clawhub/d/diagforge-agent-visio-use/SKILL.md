---
name: diagforge-bootstrap
description: Bootstrap skill for DiagForge. Use this skill to onboard an agent into the DiagForge GitHub repository, understand the project structure, run the canonical cold-start smoke test, and begin working with the Visio-based drawing loop safely.
version: 0.1.2
metadata:
  openclaw:
    homepage: https://github.com/qweadzchn/DiagForge
    requires:
      bins:
        - git
        - python
      env:
        - VISIO_BRIDGE_TOKEN
---

# DiagForge Bootstrap

This is a lightweight onboarding skill for the DiagForge repository.

It is not the full DiagForge system.
Its job is to guide an agent to the correct GitHub repository, documents, smoke test, and execution flow.

DiagForge itself is an agent-driven closed loop built on top of Microsoft Visio.
Its goal is to turn reference figures into directly editable diagram assets by helping agents operate Visio more like a capable human user rather than as a blind API caller.

## What this skill can do

This skill can help an agent:

- understand what DiagForge is trying to achieve
- find the correct GitHub repository and entry documents
- avoid random first-run behavior and jump into the intended workflow
- run the canonical cold-start smoke test
- start reproducing reference figures through the DiagForge Visio loop
- move toward a result that a human can continue editing directly in Visio

## Typical outcomes

After using this skill, an agent should be able to:

- explain the DiagForge workflow clearly
- bootstrap itself into the repository with the correct read order
- validate that the Visio bridge and execution path are working
- begin work on figure reproduction with better layer awareness
- help produce editable `.vsdx` outputs instead of dead image copies

## What this skill is for

Use this skill when an agent needs to:

- find the DiagForge source repository
- understand the top-level architecture quickly
- avoid free-form blind retries
- run the canonical cold-start smoke test
- begin work in the correct layer

## When to use it

Use this skill when:

- an agent is entering DiagForge for the first time
- a new environment needs to be validated before real drawing work
- a user wants an agent to help reproduce a figure through Visio
- the goal is not only to look similar to the reference, but to obtain a directly editable diagram asset

## What this skill is not

This skill does not bundle the whole repository.
It does not include Visio bridge code, benchmark PNGs, or runtime artifacts.

The full project lives in the GitHub repository:

`https://github.com/qweadzchn/DiagForge`

## Recommended workflow

1. Clone the GitHub repository locally.
2. Read the cold-start entry documents.
3. Run the canonical smoke test before doing open-ended drawing work.
4. Only then move on to real jobs or system improvements.

## Clone the repository

```bash
git clone git@github.com:qweadzchn/DiagForge.git
cd DiagForge
```

If SSH is not available, use HTTPS instead.

## Read order

Read these files first:

1. `AGENT_START_HERE.md`
2. `AGENT_GUIDE.md`
3. `GET_STARTED.md`
4. `docs/human/setup/AGENT_COLD_START_SMOKE_TEST.md`
5. `MODE_POLICY.md`

## Canonical smoke test

From the repo root:

```powershell
python Setup\prepare_smoke_test.py --config Setup\examples\smoke-test-inputpng-1.json
python Setup\run_draw_job.py --config Setup\examples\smoke-test-inputpng-1.json
python Setup\execute_drawdsl.py --config Setup\examples\smoke-test-inputpng-1.json --round 1 --save-final
```

Expected outputs:

- `OutputPreview/smoke-inputpng-1/round-01.png`
- `OutputEditable/1_smoke_test_final.vsdx`

## Routing rule

When working inside DiagForge:

- if the issue is round-specific, keep it in review artifacts
- if it looks structural but still needs validation, write a proposal
- if it is already reusable experience, promote it into a lesson
- if the shared fix is clear, patch the owning layer directly

## Where to go next

See:

- `README.md`
- `CONTRIBUTING.md`
- `docs/architecture/FEEDBACK_PROMOTION_LOOP.md`
