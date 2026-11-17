## Description:

AI接单画师工作站 helps agents structure AI image-order workflows for commercial artists and designers, including style routing, prompt checks, image-generation guidance, and delivery steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Commercial artists, designers, and agent operators use this skill to convert customer image requests into structured AI image-generation steps, with routing between portrait and general image workflows, sensitive-content checks, and delivery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may handle customer images and business-order data without enough scope boundaries.

Mitigation: Use it only with explicit rules for customer-data access, storage, uploads, and message delivery.

Risk: The workflow describes ecommerce messages, refunds, file uploads, and shell command use that could affect customer accounts or local systems.

Mitigation: Require approval for uploads, customer communications, refunds, and shell commands, and run the agent in a controlled environment.

Risk: API keys for image and portrait engines could be exposed if configured or logged incorrectly.

Mitigation: Store keys in environment variables, avoid printing secrets, and limit access to only the services required for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-artist-workstation-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON-style response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image URLs, local output paths, selected engine names, style labels, prompt text, status fields, and error codes.]

## Skill Version(s):

1.0.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
