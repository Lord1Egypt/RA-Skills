## Description:

Verify skill authorship, enforce capability manifests, and audit tool usage to secure and control OpenClaw skills with identity and access management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunilp](https://clawhub.ai/user/sunilp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to verify OpenClaw skill signatures and manifests, inspect audit logs, view security status, and manage trusted authors before relying on installed skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact delegates core behavior to an unpinned third-party npm package installed globally.

Mitigation: Review the aip-openclaw npm package and source before installing, avoid elevated privileges, and prefer a pinned reviewed version if available.

Risk: Trust decisions and audit logs may be stored outside the reviewed skill artifact.

Mitigation: Confirm where aip-openclaw stores trust decisions and audit logs before using it to enforce security policy.

## Reference(s):

- [AIP Protocol](https://sunilprakash.com/aip/)
- [AIP Paper](https://arxiv.org/abs/2603.24775)
- [aip-openclaw GitHub Repository](https://github.com/sunilp/aip-openclaw)
- [ClawHub Skill Page](https://clawhub.ai/sunilp/skills/aip-agent-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local trust decisions, capability manifests, and audit-log checks.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
