## Description:

An iterative, high-rigor presentation generation skill leveraging Marp and the Emergence Render API for Agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and engineers use this skill to plan slide decks iteratively, draft Marp Markdown, render diagrams through Emergence's render service, and compile presentations to PDF, PPTX, or HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram definitions or data-derived visual content may be sent to Emergence's third-party render service.

Mitigation: Use the skill only with content approved for that service, and avoid confidential strategy, customer data, unpublished research, or proprietary architecture unless the upload is explicitly approved.

Risk: The documented compilation commands use @marp-team/marp-cli@latest, which can change between runs.

Mitigation: Use a pinned, locally installed Marp CLI version for repeatable builds and review the package before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emergencescience/skills/emergence-ppt-orchestra)
- [Marp](https://marp.app/)
- [Emergence Render API OpenAPI](https://api.emergence.science/tools/render/openapi.json)
- [Emergence Content Index](https://emergence.science/content/index.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown files with optional rendered image assets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce presentation.md, assets, and compiled PDF, PPTX, or HTML outputs when the agent executes the documented workflow.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
