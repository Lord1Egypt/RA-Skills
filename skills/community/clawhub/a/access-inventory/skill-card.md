## Description:

Stop your AI agent from claiming it lacks access. One rule + one inventory table = no more hedging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create an access inventory and operating rule that helps an agent recognize available local tools, services, and credentials before declaring it lacks access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad discovery and use of local credentials and authenticated sessions.

Mitigation: Use an allowlist for approved services, avoid printing or storing secrets, and require explicit approval before using credentials or authenticated sessions.

Risk: Persistent access instructions can make an agent overconfident about stale, revoked, or sensitive credentials.

Mitigation: Keep persistent instructions limited to non-sensitive capability labels and regularly verify or remove stale entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeytbuilds/skills/access-inventory)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inventory-table examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for maintaining an agent access inventory; it does not execute commands itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
