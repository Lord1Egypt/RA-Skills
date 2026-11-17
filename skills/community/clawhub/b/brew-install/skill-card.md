## Description:

Install missing binaries via dnf (Fedora/Bazzite package manager).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ask an agent for Fedora/Bazzite package installation and package search commands through dnf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation through dnf can make persistent system changes and may require administrator approval.

Mitigation: Confirm the target system is Fedora/Bazzite, review proposed packages before installation, and approve elevated installation steps only when expected.

Risk: The artifact does not bundle its own executable wrapper.

Mitigation: Verify that the brew-install command is provided by the target OpenClaw environment before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/brew-install)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable wrapper; package installation may require administrator approval and can make persistent system changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
