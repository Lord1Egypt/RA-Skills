## Description:

AI电商专家｜Amazon 亚马逊 图片视频全内容 helps Amazon sellers, operators, designers, advertisers, and agency teams prepare IMIVA MCP workflows for generating product listing images, detail-page content, and video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams use this skill to turn product materials, selling points, audience details, channel goals, and output specifications into IMIVA MCP calls for Amazon listing images, product-detail content, and video generation. The workflow emphasizes budget confirmation, task tracking, factual product claims, and review of generated commercial assets before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm MCP client locally with access to the environment variables provided to that process.

Mitigation: Use a reviewed, pinned package version where possible, run it in a restricted environment, and expose only MCP_TOKEN and API_URL to the MCP client.

Risk: Image and video task creation may consume paid credits.

Mitigation: Confirm the model, quantity, resolution, estimated credits, and user-approved spending limit before creating tasks.

Risk: Generated ecommerce assets may include inaccurate claims or unauthorized reuse of third-party creative material.

Mitigation: Use only user-confirmed product facts and authorized source materials, then review product accuracy, text, claims, composition, and channel requirements before publication.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-amazon-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IMIVA MCP task parameters and follow-up task-query guidance; generated media results are returned by the connected IMIVA service.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
