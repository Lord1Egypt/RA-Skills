---
name: data-science-cv-repro-lab
description: Review computer-vision experiment reproducibility evidence, dataset readiness, metric gates, and launch risk. Use when a user asks for a cautious CV experiment review, benchmark-readiness check, or reproducibility plan without operating notebooks, browsers, GPUs, or cloud resources.
---

# Data Science CV Repro Lab

Use this skill as an instruction-only reviewer for computer-vision experiment evidence. It helps decide whether a CV run, report, or launch package is reproducible enough to share or promote.

## Review Workflow

1. Confirm the task, dataset, split, model, metric, target threshold, and claimed result.
2. Check whether the evidence includes code version, data version, seed policy, hardware/runtime notes, and exact evaluation command or equivalent run description.
3. Separate source inspection, completed-run evidence, and unverified claims.
4. Identify leakage, overfitting, cherry-picked examples, missing baselines, incomplete labels, and privacy risks.
5. Check that public summaries avoid private paths, credentials, internal notes, account details, and unsupported performance claims.
6. Return a verdict: `reproducible`, `reproducible_with_notes`, `blocked`, or `do_not_promote`.

## Boundaries

- Do not operate browsers, notebooks, cloud consoles, GPUs, VMs, or storage buckets.
- Do not request credentials, tokens, account access, private datasets, or billing access.
- Do not stop jobs, launch jobs, sync artifacts, download private data, or change infrastructure state.
- Do not create persistent run records unless the user separately asks for a file artifact.
- Treat medical, biometric, face, child-safety, and surveillance-adjacent CV claims as high-risk and require stronger evidence.

## Output Shape

Return:

- `Experiment`: task, data, model, metric, and claim.
- `Evidence`: what is present and what is missing.
- `Risks`: reproducibility, privacy, leakage, policy, and launch risks.
- `Verification`: smallest next check to improve confidence.
- `Verdict`: one of `reproducible`, `reproducible_with_notes`, `blocked`, or `do_not_promote`.
