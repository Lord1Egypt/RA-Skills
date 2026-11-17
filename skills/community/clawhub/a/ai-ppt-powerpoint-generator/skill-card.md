## Description:

AI PPT PowerPoint Presentation Generator Skills to Generate Multi-Page Image Carousels from Templates of AI PPT PowerPoint, Sota Models Nano Banana, Nano Banana-2 ,Imagen-2 and more are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call the Craftsman image generator through OneKey Gateway and generate multi-page PowerPoint-style image carousels or editable poster-style presentation assets from prompts, templates, images, and layout settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, images, and generated workspace content to external services.

Mitigation: Use only non-sensitive prompts and images unless third-party processing and shareable remote workspaces are acceptable for the intended use.

Risk: The documented CLI path uses an unpinned npx command.

Mitigation: Prefer the documented direct API call, or pin and isolate the CLI while exposing only the required OneKey Gateway API key.

Risk: The artifact documents photo-editing and watermark-removal capabilities alongside presentation generation.

Mitigation: Use those media-editing capabilities only when the user has rights to the media and understands the applicable service terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/ai-ppt-powerpoint-generator)
- [Craftsman Image Generator Console](https://craftsman-agent.aiagenta2z.com/app/image-generator)
- [Craftsman Website](https://craftsman-agent.aiagenta2z.com)
- [DeepNLP Workspace Keys](https://deepnlp.org/workspace/keys)
- [DeepNLP Agent Router Endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown usage guidance with curl and npx command examples plus JSON request and response structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated presentation outputs may include a session ID, title or summary, share URL, image URLs, editable page-layer data, card count, and canvas geometry.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
