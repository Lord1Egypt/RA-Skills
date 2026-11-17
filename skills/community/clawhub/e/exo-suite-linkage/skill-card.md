## Description:

Links the AI-for-Science toolchain hfpclawer, expflow-pde, and omega-architect through file and CLI contracts with per-layer cost tiers and a degradation ladder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to coordinate literature collection, experiment tracking and HPO, and Lean proof generation while preserving file-based hand-offs, provenance, and cost discipline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External packages and a pinned GitHub tag are installed or launched as part of the workflow.

Mitigation: Review the packages and GitHub tag before installation, prefer the pinned commands shown by the skill, and run them in a project-specific environment.

Risk: The workflow can download data, execute CLIs, and create experiment or proof artifacts.

Mitigation: Run the workflow in an isolated project workspace and review generated artifacts before relying on them.

Risk: A proof claim can be overstated if the proof layer did not run successfully.

Mitigation: Label unverified statements as unverified and rely on compiler-accepted proofs with run metadata for proof-backed claims.

Risk: Experiment and proof stages can increase compute, bandwidth, disk, or API-token cost.

Mitigation: Use the low to medium to high cost ladder, start with low sample and round counts, and record model and budget data with proof artifacts.

## Reference(s):

- [Exo Suite Linkage on ClawHub](https://clawhub.ai/diamond2nv/skills/exo-suite-linkage)
- [omega-architect homepage](https://github.com/diamond2nv/omega-architect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file or JSONL artifact contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference formula registries, citation audit reports, trial records, Lean projects, compile results, and run metadata.]

## Skill Version(s):

0.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
