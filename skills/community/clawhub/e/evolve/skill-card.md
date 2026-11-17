## Description:

Local DevOps/autonomy skill for OpenClaw (safe evolution loop with guardrails).

This skill is ready for commercial/non-commercial use.

## Publisher:

[delkoman88](https://clawhub.ai/user/delkoman88)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run an OpenClaw skill evolution loop that snapshots status, generates candidates, tests them, promotes candidates into active skills, and supports rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local controller can change active OpenClaw skills, and the documented safeguard boundaries are incomplete.

Mitigation: Review the local evolvectl.sh implementation before use, including writable paths, promotion overwrite behavior, backup creation, and rollback behavior.

Risk: Automated skill changes may be inappropriate in workspaces where active skills must remain stable.

Mitigation: Use this skill only in a workspace where automated skill changes are acceptable and test generated candidates before promotion.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for invoking a local evolvectl.sh controller; EVOLVECTL can override the controller path.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
