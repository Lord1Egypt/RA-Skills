## Description:

Verify skill authorship, enforce declared permissions, and audit tool usage to secure OpenClaw environments using Agent Identity Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunilp](https://clawhub.ai/user/sunilp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to check skill signatures and manifests, inspect audit logs, review security status, and manage trusted authors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install mutable third-party security tooling that is not included in the reviewed artifact.

Mitigation: Install only if the publisher and package are trusted; prefer a pinned, reviewed version and avoid administrator installation.

Risk: The tooling can influence skill trust decisions, capability enforcement, and local audit or trust-list state.

Mitigation: Review security decisions before relying on them and keep trust-list changes auditable and reversible.

## Reference(s):

- [AIP Protocol](https://sunilprakash.com/aip/)
- [AIP Paper](https://arxiv.org/abs/2603.24775)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational security guidance for installing and using external AIP/OpenClaw tooling.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
