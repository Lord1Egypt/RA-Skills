## Description:

Analyze an uploaded portrait photo with MiniMax-M3 and generate a playful, shareable camera-presence report with a 1-10 lens score, positive visual highlights, practical photo tips, social captions, and a report-card image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airbai](https://clawhub.ai/user/airbai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn a portrait, selfie, avatar, or profile photo into lightweight entertainment feedback, practical photo tips, social copy, and shareable report-card files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Request-controlled image paths and output directories can expose local files or write generated reports outside the intended workspace.

Mitigation: Run only with trusted request files, avoid absolute paths, and constrain imagePath and outputDir to the workspace before deployment.

Risk: Portrait images and analysis prompts may be sent to a third-party MiniMax endpoint during real analysis.

Mitigation: Obtain explicit upload consent, avoid sensitive portraits, and use mock mode when external model calls are not appropriate.

Risk: Request or environment-controlled API endpoint and key handling could expose the MiniMax API key or send data to an unintended service.

Mitigation: Keep API keys in trusted environment variables, do not let untrusted users set baseUrl or apiKey, and review network configuration before use.

Risk: The generated report includes a built-in QR code and browser-rendered HTML that may not be appropriate for all sharing contexts.

Mitigation: Review the QR destination and generated HTML before publishing or sharing report-card outputs.

## Reference(s):

- [Beauty Karma ClawHub Skill Page](https://clawhub.ai/airbai/skills/beauty-karma)
- [MiniMax API Endpoint](https://api.minimax.io/v1)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands, configuration, files, guidance]

**Output Format:** [JSON status output plus generated analysis.json, HTML report-card page, SVG preview, and social caption text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a portrait input and, outside mock mode, a MiniMax API key.]

## Skill Version(s):

1.0.3 (source: frontmatter, package.json, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
