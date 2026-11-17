## Description:

Double Check guides agents to run the same appropriate verification twice after file edits, fixing failures and restarting the checks until both consecutive runs pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[belugarex](https://clawhub.ai/user/belugarex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when agents modify code, documentation, configuration, or other project files and need stricter verification before completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification commands may execute project scripts twice and can consume extra time or resources.

Mitigation: Use trusted project commands and consider timeouts or resource limits for large or sensitive projects.

Risk: Fallback runtime or build checks may not prove full logical correctness.

Mitigation: When no standard test or build command exists, agree on an executable check and report its limitations clearly.

## Reference(s):

- [Double Check on ClawHub](https://clawhub.ai/belugarex/skills/double-check)
- [belugarex publisher profile](https://clawhub.ai/user/belugarex)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, text]

**Output Format:** [Markdown guidance with shell command examples and verification status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code or external services; the agent selects project-appropriate verification commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
