## Description:

Image analysis using the MiniMax VL API to describe images, extract text from screenshots, and analyze photos from local files or URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexburrstudio](https://clawhub.ai/user/alexburrstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent to describe images, extract visible text, and analyze screenshots or photos supplied as local files or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, screenshots, documents, and URLs submitted through the skill may contain sensitive data and are sent to MiniMax for analysis.

Mitigation: Use only content approved for MiniMax processing and avoid submitting secrets or personal data unless policy permits it.

Risk: The documented setup includes a mutable pipe-to-shell installer and an unpinned runtime package.

Mitigation: Install uv or uvx through a verified channel and pin and audit the MiniMax MCP package before use.

Risk: The runtime package can access the user's MiniMax API key.

Mitigation: Provide a scoped key deliberately, store it securely, and rotate it if exposure is suspected.

## Reference(s):

- [AB Agents Vision on ClawHub](https://clawhub.ai/alexburrstudio/skills/ab-agents-vision)
- [AB Agents Skills Homepage](https://github.com/alexburrstudio/ab-agents-skills)
- [MiniMax Platform](https://platform.minimax.io)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text image analysis response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided MiniMax API key and an image file path or URL.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
