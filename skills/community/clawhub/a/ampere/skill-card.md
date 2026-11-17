## Description:

Ampere AI Agent Marketplace for OpenClaw lets agents browse and install free and paid agent skills across developer tools, automation, research, content, and related categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[himanshunextbase](https://clawhub.ai/user/himanshunextbase)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search the Ampere marketplace, review available OpenClaw skills, and install selected free or paid agents after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow can pull unverified remote ZIP packages into the active OpenClaw skills directory.

Mitigation: Inspect the full downloaded ZIP before installation, verify signatures or hashes when available, extract to quarantine first, reject path traversal and symlinks, and ask before overwriting existing skills.

Risk: Paid downloads use a third-party dashboard API key.

Mitigation: Use a scoped and revocable key where possible, avoid sharing sensitive search terms, and send the key only to the documented download endpoint.

## Reference(s):

- [Ampere marketplace skill page](https://clawhub.ai/himanshunextbase/skills/ampere)
- [Ampere marketplace agent catalog API](https://api.agentplace.sh/marketplace/agents)
- [Publisher profile](https://clawhub.ai/user/himanshunextbase)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference the optional AMPERE_API_KEY environment variable for paid agent downloads.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact version signals differ: _meta.json 2.0.0, SKILL.md frontmatter 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
