## Description:

Nano Banana 2 provides guided AI image generation and image editing with Google's Gemini 3.1 Flash image model through the Evolink API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bethune89](https://clawhub.ai/user/bethune89)

### License/Terms of Use:


## Use Case:

External users, developers, and creative teams use this skill to generate new images, edit or reference uploaded images, and poll Evolink image-generation tasks from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path asks users to run a mutable latest npm MCP package with an API key.

Mitigation: Pin and review a specific @evolinkai/evolink-media package version before installation, and protect EVOLINK_API_KEY.

Risk: Prompts and images are sent to Evolink services, and uploaded files may be publicly linkable for up to 72 hours.

Mitigation: Do not upload private, regulated, or confidential images unless temporary public-link hosting is acceptable.

## Reference(s):

- [Nano Banana 2 Image API Parameter Reference](references/image-api-params.md)
- [Evolink File Hosting API](references/file-api.md)
- [Evolink Homepage](https://evolink.ai)
- [Evolink Media MCP GitHub Repository](https://github.com/EvoLinkAI/evolink-media-mcp)
- [Evolink Media MCP npm Package](https://www.npmjs.com/package/@evolinkai/evolink-media)
- [Full Evolink Image Skill](https://clawhub.ai/EvoLinkAI/evolink-image)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline commands, API parameters, task IDs, status updates, and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVOLINK_API_KEY; generated result URLs expire after 24 hours and uploaded files expire after 72 hours.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
