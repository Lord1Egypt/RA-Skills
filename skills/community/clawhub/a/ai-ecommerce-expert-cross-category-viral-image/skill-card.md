## Description:

AI电商专家｜跨品类爆款图改造 helps ecommerce design, brand marketing, advertising, operations, and content teams prepare IMIVA MCP requests that migrate reusable viral visual structures across product categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce design, brand marketing, advertising, operations, and content teams use this skill to turn product material, channel requirements, audience goals, and budget choices into executable IMIVA visual migration tasks. The skill guides users through credit checks, task creation, task lookup, and output review for cross-category ecommerce image and video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP client and can inherit environment secrets.

Mitigation: Use a pinned reviewed npm client version where possible and run it with a minimal environment allowlist containing only the IMIVA token and API URL.

Risk: The generic MCP call helper can access any tool allowed by the configured IMIVA token.

Mitigation: Use a narrowly scoped, revocable IMIVA token and verify the available MCP tools before operational use.

Risk: Visual migration can copy unauthorized trademarks, protected characters, people, or misleading product claims if source material is not vetted.

Mitigation: Confirm reference-material rights and product facts before submission, then review outputs for brand, text, claim, and channel compliance before publishing.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-cross-category-viral-image)
- [MCP configuration example](artifact/references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return IMIVA MCP task parameters, credit-check instructions, task IDs, task status, and generated asset result guidance when configured with a valid token.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
