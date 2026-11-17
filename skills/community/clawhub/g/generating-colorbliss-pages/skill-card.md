## Description:

Generates printable coloring pages from text prompts or photos with the ColorBliss API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benrobertsonio](https://clawhub.ai/user/benrobertsonio)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn text prompts or publicly reachable photos into printable coloring-page images, or submit batches of photos for PDF exports through ColorBliss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the external ColorBliss API sends a request that may include prompt or photo data; the security scan does not establish exactly what content is transmitted.

Mitigation: Submit only data the user intends to send, get permission before processing photos, and keep the API key in host secret settings; send it only to ColorBliss API endpoints.

## Reference(s):

- [ColorBliss API overview](https://colorbliss.com/coloring-page-api)
- [ColorBliss API reference](https://colorbliss.com/coloring-page-api/docs/reference)
- [ClawHub release](https://clawhub.ai/benrobertsonio/skills/generating-colorbliss-pages)

## Skill Output:

**Output Type(s):** [Images, PDF files, Guidance]

**Output Format:** [Coloring-page images for prompt and single-photo jobs; bulk photo PDF ZIP export; Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bulk PDF exports are emailed to the key owner's account; bulk polling does not return a ZIP download URL.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
