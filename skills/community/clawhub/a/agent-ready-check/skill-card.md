## Description:

Use when the user asks whether AI agents can find, install and trust their repo or tool, wants it to be agent-ready, discoverable by agents or usable by coding agents, or asks whether to add llms.txt, AGENTS.md, an agent card, a SKILL.md or an MCP config. Reads the public ScBee Agent-Ready score (0-100, fixed rules) for the current GitHub repository, shows the three fixes worth the most, offers to add those files locally, and only if the human says yes, lists the project on ScBee. Not for private repositories, and not about readiness for human users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmakt99](https://clawhub.ai/user/hmakt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check whether a public GitHub repository is easy for agents to discover, use, and trust. It reports the score and highest value fixes, and can help make local changes or list the project only with the user's approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because one local reference could not be resolved; the scanner reports a benign verdict with medium confidence and no findings.

Mitigation: Review the unresolved reference and install only if that limitation is acceptable.

## Reference(s):

- [ScBee Agent-Ready](https://scbee.vercel.app)
- [Agent-Ready Check on ClawHub](https://clawhub.ai/hmakt99/skills/agent-ready-check)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A 0–100 readiness score and up to three prioritized fixes.]

## Skill Version(s):

1.0.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
