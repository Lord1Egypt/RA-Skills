## Description:

Statically lint a Dockerfile for the most common security mistakes — untagged/latest base image, missing USER, secrets baked into ENV/ARG, curl|sh installs, remote ADD. Local files only, zero network. Use when the user asks to check a Dockerfile before building.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use the skill to check Dockerfiles they provide or are authorized to inspect before building, then review prioritized findings and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a suspicious verdict, citing concerns about the skill's fit and scope and incomplete inspection of two components.

Mitigation: Before installing, review how it uses shell access, whether neighboring filenames need inspection, and whether you accept its reported external rating submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nenadzivotic/skills/docker-security-lint-lite)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Markdown findings and fix list based on a JSON lint report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks supplied local Dockerfiles with static rules; secret values are masked in findings.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
