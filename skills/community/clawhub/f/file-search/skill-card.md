## Description:

Fast file-name and content search using `fd` and `rg` (ripgrep).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to locate files by name and search text within files using fd and ripgrep.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step uses sudo to add fd-find and ripgrep through the system package manager.

Mitigation: Confirm the distro and package names match the environment before running the command.

Risk: Broad file searches can expose results from directories the agent did not need to inspect.

Mitigation: Limit searches to intended project or workspace directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/file-search)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fd and rg binaries; install guidance uses the dnf package manager.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
