## Description:

Review computer-vision experiment reproducibility evidence, dataset readiness, metric gates, and launch risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data scientists, and reviewers use this skill to assess whether computer-vision experiment claims have enough evidence for reproducibility, benchmark readiness, or promotion. It focuses on dataset readiness, metric gates, missing evidence, privacy concerns, and launch risk without operating external systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect the skill to run experiments, access private systems, or validate claims through external execution.

Mitigation: Use it only to review evidence supplied by the user; do not provide credentials, private system access, or requests to operate notebooks, cloud consoles, GPUs, VMs, storage buckets, or jobs.

Risk: Computer-vision launch claims may involve incomplete reproducibility evidence, privacy-sensitive data, leakage, or unsupported public performance statements.

Mitigation: Require code and data versioning, split and seed details, runtime notes, exact evaluation commands or equivalent run descriptions, and public summaries that omit private paths, credentials, account details, and unsupported claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/data-science-cv-repro-lab)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown review with experiment, evidence, risks, verification, and verdict sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdict is one of reproducible, reproducible_with_notes, blocked, or do_not_promote.]

## Skill Version(s):

1.9.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
