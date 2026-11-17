## Description:

Agent SecuritySandbox is intended to help agents run untrusted code or commands in an isolated Docker environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assix](https://clawhub.ai/user/assix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to route suspicious scripts, third-party skills, or unknown commands into an isolated Docker execution workflow before inspecting the resulting output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sandbox security claims cannot be verified from the reviewed package because the evidence says the runner script, Dockerfile, image source, and Docker invocation are missing.

Mitigation: Review the exact runner script, Dockerfile, image source, seccomp profile, and Docker command before installing or using the skill for untrusted code.

Risk: The release has a suspicious security verdict.

Mitigation: Use only in a controlled environment after audit, and do not rely on it as a verified isolation boundary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/assix/skills/agent-securitysandbox)
- [Publisher Profile](https://clawhub.ai/user/assix)
- [Docker Installation Documentation](https://docs.docker.com/get-docker/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sandbox output depends on local Docker availability and the reviewed release's included runner assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
