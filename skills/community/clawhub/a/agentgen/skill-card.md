## Description:

Generate PDFs and images from HTML through AgentGen, with a no-sign-up free tier and optional AGENTGEN_API_KEY authentication for higher volume and watermark-free output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyair1](https://clawhub.ai/user/lyair1)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert HTML documents, reports, invoices, web pages, and social images into PDFs or raster image files through the AgentGen CLI/API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML submitted for rendering is sent to AgentGen's service.

Mitigation: Review submitted HTML and avoid including secrets, private content, or sensitive metadata.

Risk: Uploaded assets are publicly accessible for 24 hours.

Mitigation: Do not upload private images, documents, fonts, or files with sensitive metadata unless that exposure is acceptable.

Risk: Authenticated use requires trusting the installed CLI with AGENTGEN_API_KEY.

Mitigation: Install the CLI from the documented source, keep AGENTGEN_API_KEY out of committed files, and rotate the key if exposure is suspected.

## Reference(s):

- [AgentGen homepage](https://www.agent-gen.com)
- [ClawHub skill page](https://clawhub.ai/lyair1/skills/agentgen)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local PNG, JPEG, WebP, or PDF files when executed with the AgentGen CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
