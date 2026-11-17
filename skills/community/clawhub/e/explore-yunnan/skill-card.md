## Description:

Explore Yunnan helps agents answer Yunnan travel requests by using the flyai CLI for real-time flights, hotels, attractions, itineraries, and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search Yunnan flights, hotels, attractions, and itinerary options through flyai CLI output. It is intended to turn real-time CLI results into concise Markdown recommendations with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install and execute an unpinned global @fly-ai/flyai-cli package.

Mitigation: Use an isolated environment, pin and review the CLI version, and require approval before installing or upgrading packages.

Risk: Travel queries and CLI activity may be stored in local logs.

Mitigation: Disable persistent logging where possible, or redact personal travel details before retaining logs.

Risk: Responses include third-party booking links from real-time CLI output.

Mitigation: Check booking URLs and require user confirmation before opening booking flows or making purchases.

## Reference(s):

- [Explore Yunnan Skill Page](https://clawhub.ai/dingtom336-gif/skills/explore-yunnan)
- [Parent flyai Skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data; user-facing results should include booking links and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
