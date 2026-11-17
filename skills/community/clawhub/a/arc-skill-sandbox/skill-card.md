## Description:

Tests untrusted Python skills in a monitored environment before installation by observing filesystem writes, environment variable reads, network access, and subprocess calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trypto1019](https://clawhub.ai/user/trypto1019)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to inspect how untrusted Python skills behave before installing or approving them. It produces runtime and static observations that support pre-installation review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence warns that the skill's safety claims are stronger than the protections its code enforces.

Mitigation: Do not treat it as a real sandbox or security boundary; run it only in a disposable VM or container with no real credentials or sensitive files mounted.

Risk: Network behavior may be observed during testing of untrusted skills.

Mitigation: Disable network access unless network testing is intentional and explicitly approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/trypto1019/skills/arc-skill-sandbox)
- [ClawHub Publisher Profile](https://clawhub.ai/user/trypto1019)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include filesystem operations, environment accesses, network attempts, subprocess calls, warnings, and a safety verdict.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
