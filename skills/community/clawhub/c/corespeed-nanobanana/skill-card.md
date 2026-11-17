## Description:

Generates and edits images, analyzes images, and creates text using Google Gemini models via the Corespeed AI Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zypher-agent](https://clawhub.ai/user/zypher-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images, edit supplied images, analyze visual inputs, and create text with Gemini models through the Corespeed AI Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to Corespeed and Google Gemini for processing.

Mitigation: Use the skill only for data approved for external processing, and set CS_AI_GATEWAY_BASE_URL only to a trusted HTTPS gateway.

Risk: The Corespeed gateway token can authorize remote model access if exposed.

Mitigation: Store CS_AI_GATEWAY_API_TOKEN securely, avoid logging it, and rotate it if disclosure is suspected.

Risk: Runtime dependencies are installed dynamically and are not pinned to exact versions.

Mitigation: For production use, run in a constrained environment and pin or mirror dependencies through an approved package workflow.

## Reference(s):

- [Corespeed](https://corespeed.io)
- [uv](https://github.com/astral-sh/uv)
- [PEP 723 Inline Script Metadata](https://peps.python.org/pep-0723/)
- [Corespeed Skills Issues](https://github.com/corespeed-io/skills/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, image files, JSON]

**Output Format:** [Generated files, plain text, Markdown, and optional structured JSON from the Gemini helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image output is saved to local files; text output is saved to .txt or .md files; optional JSON includes status, file paths, text, model, and token usage.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
