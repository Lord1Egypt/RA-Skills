# agent matrix

Use this matrix as a default decision aid. Override it when fresher local evidence exists.

## Current workspace snapshot

### Codex
- **Status**: verified
- **Strengths**:
  - strongest current track record for artifact delivery
  - reliable for multi-step coding and file creation
  - good default for deadline-sensitive work
- **Risks**:
  - can still hit provider/auth drift if local model login changes
- **Default use**:
  - reports
  - PPTX / binary artifacts
  - multi-file coding
  - tasks where rework cost is high

### Claude
- **Status**: re-verified on 2026-03-16
- **Passed**:
  - fixed-text response
  - minimal file write
  - real PPTX generation and validation
- **Strengths**:
  - now viable for modest artifact generation in this workspace
  - good fit for presentation/report style tasks when freshly verified
- **Risks**:
  - historically sensitive to provider/relay behavior
  - historically blocked by acpx permission configuration
  - long-running reliability still needs more evidence
- **Default use**:
  - modest delivery tasks after smoke-test success
  - presentation-style outputs
  - parallel second opinion when deadline pressure is moderate

### Pi / Gemini / OpenCode / others
- **Status**: unverified by default unless re-tested locally
- **Rule**:
  - do not assume delivery capability from brand reputation alone
  - require the standard ladder: text -> minimal write -> real artifact

## Selection policy

Choose the agent with the best match on these axes:
1. freshest passing artifact proof
2. lowest workflow risk
3. best fit for the output style
4. lowest retry cost if it fails

## Default routing policy

- if the task is urgent or expensive to redo: choose **Codex**
- if the task is modest and Claude was just re-verified: **Claude** is acceptable
- if the user explicitly wants another agent: honor that, but keep the verification ladder
- if no agent has current proof for the requested output type: test before promising delivery

## Promotion rule

Promote an agent from "experimental" to "delivery-capable" only after it passes:
1. fixed-text response
2. minimal file write
3. one real artifact in the target category

## Demotion rule

Demote an agent back to cautious/experimental if any of these happen repeatedly:
- artifact creation regresses
- permission/tool calls start aborting
- provider starts returning compatibility or quota failures
- output validates inconsistently across repeated runs
