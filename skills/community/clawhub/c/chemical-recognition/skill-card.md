## Description:

Optical chemical structure recognition workflow for extracting molecule structures and names from images through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and chemistry researchers use this skill to extract molecular structures and visible molecule names from paper figures, slides, posters, screenshots, or other chemistry images into downstream-ready outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-provided chemistry images to SciMiner while using an API key.

Mitigation: Use it only with images the user is permitted to send to SciMiner; avoid confidential or regulated chemistry content.

Risk: The skill relies on mutable external documentation to define invocation details.

Mitigation: Review the referenced SciMiner API documentation before use and prefer a reviewed or pinned invocation path for higher-assurance deployments.

## Reference(s):

- [SciMiner AlphaExtractor API documentation](https://sciminer.tech/tool_api_files/AlphaExtractor_api_doc.md)
- [SciMiner tool API documentation index](https://sciminer.tech/tool_api_files/)
- [αExtractor on ClawHub](https://clawhub.ai/sciminer/skills/chemical-recognition)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON task results, invocation code or shell commands, and SciMiner history URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gateway-injected SCIMINER_API_KEY; successful task summaries should include history_url links.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
