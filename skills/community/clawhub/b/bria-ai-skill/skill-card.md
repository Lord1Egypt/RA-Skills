## Description:

Helps agents generate, edit, upscale, restyle, and remove image backgrounds through Bria AI API workflows for product, marketing, and visual asset creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galbria](https://clawhub.ai/user/galbria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and e-commerce teams use this skill to ask an agent for Bria-powered image generation, editing, background removal, product photography, and batch visual asset workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected image content are sent to Bria when the skill is used for generation or editing.

Mitigation: Use the skill only for content that may be shared with Bria, and avoid submitting sensitive, confidential, or regulated image data unless approved for that service.

Risk: API keys may be exposed if users paste them into chat, print them with echo, or copy examples without secret handling.

Mitigation: Configure BRIA_API_KEY through a private environment or secret manager and avoid displaying the token in agent transcripts or logs.

Risk: Bundled clients can upload local files, download remote image URLs, and poll returned status URLs.

Mitigation: Before production use, restrict allowed local upload paths and remote URL sources, and validate status URLs before polling.

## Reference(s):

- [Bria AI homepage](https://bria.ai)
- [ClawHub skill page](https://clawhub.ai/galbria/skills/bria-ai-skill)
- [API Endpoints Reference](references/api-endpoints.md)
- [Workflows and Pipelines](references/workflows.md)
- [Python Client Example](references/code-examples/bria_client.py)
- [TypeScript Client Example](references/code-examples/bria_client.ts)
- [Bash/curl Reference](references/code-examples/bria_client.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, curl commands, and Python, TypeScript, or shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May help an agent issue Bria API requests and relay returned image URLs; background removal workflows return PNG images with transparency.]

## Skill Version(s):

1.2.5 (source: server release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
