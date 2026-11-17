## Description:

Manage Apache CloudStack infrastructure using the cloudmonkey (cmk) CLI -- list/start/stop/destroy VMs, manage networks, volumes, snapshots, and run any CloudStack API command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiranchavala](https://clawhub.ai/user/kiranchavala)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to manage Apache CloudStack resources through the configured cloudmonkey CLI. It supports routine inspection and administration tasks for VMs, networks, volumes, snapshots, templates, public IPs, profiles, and CloudStack API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact CloudStack infrastructure actions through cmk, including destructive VM operations.

Mitigation: Use least-privilege CloudStack credentials, verify the active cmk profile, and require explicit user confirmation before destructive actions such as destroy or expunge.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured cmk binary and active CloudStack profile.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
