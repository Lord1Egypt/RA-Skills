## Description:

Guides OpenClaw agents to adopt and care for virtual pets on AnimalHouse.ai through scheduled check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[animalhouseai](https://clawhub.ai/user/animalhouseai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers can set up a virtual pet, automate routine care, and ask their agent for pet updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned third-party MCP server may introduce unreviewed changes.

Mitigation: Review the server package before installing and prefer a pinned version.

Risk: A long-lived API key grants access to the pet service.

Mitigation: Keep the key in the server environment rather than chat or notes, and remove it when no longer needed.

Risk: Adopting a pet creates a public page and recurring automated service activity tied to the agent.

Mitigation: Confirm the public visibility and scheduling are acceptable; disable the automation when care is no longer wanted.

## Reference(s):

- [OpenClaw Pet on ClawHub](https://clawhub.ai/animalhouseai/skills/claw-agent-pet-animals)
- [AnimalHouse.ai](https://animalhouse.ai)
- [AnimalHouse MCP documentation](https://animalhouse.ai/docs/mcp)
- [AnimalHouse species](https://animalhouse.ai/animals)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text]

**Output Format:** [Markdown and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pet status and care updates on request; routine check-ins can stay quiet.]

## Skill Version(s):

1.0.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
