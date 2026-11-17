## Description:

Guides an agent through protecting local credential files with CredAgent and limiting access to explicitly authorized programs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benson666](https://clawhub.ai/user/benson666)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and users managing local secrets use this skill to identify credential files, allow specific programs to access them, and verify or reverse CredAgent protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may change or permanently remove sensitive credential files through protection and lifecycle commands.

Mitigation: Approve each credential path and authorized program separately; understand how to release or recover a protected file before approving protect, update, or remove.

Risk: Broad program permissions or mutable scripts can weaken restrictions on who can read secrets.

Mitigation: Avoid authorizing broad interpreters for cloud credentials; inspect and secure the authorized program and its dependencies before granting access.

Risk: System-level installation and broad credential searches can affect more files than intended.

Mitigation: Require user approval for privileged setup and avoid whole-home scans or bulk protection.

## Reference(s):

- [CredAgent ClawHub release](https://clawhub.ai/benson666/skills/credagent)
- [CredAgent software and releases](https://github.com/aliyun/credagent)
- [Installation guide](references/installation.md)
- [Command reference](references/manual.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide approved changes to local credential access policies.]

## Skill Version(s):

0.2.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
