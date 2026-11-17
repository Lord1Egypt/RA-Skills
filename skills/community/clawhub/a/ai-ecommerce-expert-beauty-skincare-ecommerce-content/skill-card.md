## Description:

AI电商专家｜美妆护肤电商图片视频 helps beauty and skincare ecommerce teams prepare IMIVA MCP workflows for product images, detail pages, KOC seeding packages, product videos, and commerce-ready creative variants from supplied product materials and confirmed selling points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, merchant, operations, design, advertising, and content teams use this skill to structure beauty and skincare ecommerce image and video generation requests through IMIVA. The skill helps confirm product facts, materials, channel requirements, budget, task submission, and result review for listing, seeding, and paid creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the release as suspicious because it runs a mutable npm package locally with broad inherited environment access.

Mitigation: Install only after reviewing and trusting the IMIVA package, prefer a pinned reviewed package version, and run it in a clean shell or container with only required runtime variables.

Risk: The skill can submit credit-consuming generation tasks through IMIVA.

Mitigation: Check credits and obtain explicit confirmation for model, quantity, resolution, duration, and budget before submitting tasks.

Risk: Generated commerce content can become misleading if product facts, claims, certifications, prices, or third-party references are unverified.

Mitigation: Use only user-provided or confirmed product facts, review outputs against channel requirements, and avoid copying protected marks, identities, or creative expression from reference materials.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-expert-beauty-skincare-ecommerce-content)
- [MCP configuration example](references/mcp-config.example.json)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IMIVA MCP task preparation guidance, configuration examples, command examples, task-query instructions, and review checklists; generated media is produced by the external IMIVA service.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
