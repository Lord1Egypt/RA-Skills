## Description:

Data processing pipelines for OpenClaw. Deploy skills from the Expanso marketplace to transform, analyze, and process data locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install Expanso Edge and CLI, connect a local Edge node to Expanso Cloud, and deploy marketplace data-processing pipelines for OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow runs mutable remote shell scripts from get.expanso.io at install time.

Mitigation: Review the installer contents before running them and prefer signed, pinned, checksum-verified packages when available.

Risk: The Expanso Edge bootstrap token is sensitive and could allow unintended registration or access if exposed.

Mitigation: Store the token in a secret manager or protected environment, avoid logging it, and rotate or revoke it after exposure.

Risk: Expanso Cloud orchestrates pipeline deployment to local Edge nodes, which may affect private data handling and control boundaries.

Mitigation: Confirm what Expanso Cloud can see or control before using the skill with private or regulated data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aronchick/skills/expanso-edge)
- [Expanso Skills Marketplace](https://skills.expanso.io)
- [Expanso Cloud](https://cloud.expanso.io)
- [Expanso Documentation](https://docs.expanso.io)
- [Expanso Edge Installer](https://get.expanso.io/edge/install.sh)
- [Expanso CLI Installer](https://get.expanso.io/cli/install.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus EXPANSO_EDGE_BOOTSTRAP_URL and EXPANSO_EDGE_BOOTSTRAP_TOKEN.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
