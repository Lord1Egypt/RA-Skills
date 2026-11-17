## Description:

Reviews Dockerfiles and docker-compose files for security, image size, build efficiency, and best-practice issues, returning severity-rated findings with corrected examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnguyen1996](https://clawhub.ai/user/lnguyen1996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Dockerfiles, docker-compose files, and .dockerignore inputs for container security, reliability, image-size, and build-cache issues before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to keep review-derived notes across runs without clear limits or user control.

Mitigation: Use the skill only when that retention behavior is acceptable, or remove/ignore the self-improvement section so reviews depend only on the current conversation and user-supplied files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnguyen1996/skills/container-reviewer)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown report with severity sections and corrected code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include critical findings, warnings, suggestions, validated good patterns, and a short summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
