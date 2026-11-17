## Description:

Generate and edit images using the AceData Nano Banana API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images from text prompts or edit existing images through AceData Nano Banana models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected images are sent to AceData for generation or editing.

Mitigation: Use the skill only with content appropriate for AceData processing and avoid sensitive prompts or images unless that transfer is acceptable.

Risk: The skill may save an AceData API token in a plaintext .env file when entered through the prompt or --api_key.

Mitigation: Prefer the ACEDATA_API_KEY environment variable and remove any generated .env file when finished.

Risk: Generated image downloads rely on remote URLs returned by the API.

Mitigation: Run the script in a contained environment with limited network and disk exposure.

## Reference(s):

- [Nano Banana Images API Documentation](references/api_docs.md)
- [AceData Cloud Platform](https://platform.acedata.cloud)
- [ClawHub Skill Page](https://clawhub.ai/xiyunnet/skills/ace-banana)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, Files, JSON]

**Output Format:** [Generated image files with console status text and JSON API response output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AceData API key and network access; generated images are saved locally.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
