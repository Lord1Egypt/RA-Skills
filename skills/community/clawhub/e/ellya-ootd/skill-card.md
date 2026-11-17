## Description:

OpenClaw virtual companion skill that bootstraps character runtime files, learns visual style prompts from reference photos, and generates selfies or photo series using Gemini or Minimax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laogiant](https://clawhub.ai/user/laogiant)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and skill handlers use this skill to personalize a virtual companion, learn reusable style descriptions from uploaded reference photos, generate prompted or style-based images, and create multi-pose photo sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal or reference photos may be sent to external AI providers for analysis or generation.

Mitigation: Use only images the user is comfortable sending to Gemini or Minimax, avoid third-party or sensitive photos, and disclose remote processing before use.

Risk: Derived appearance and style descriptions can persist locally in generated style files.

Mitigation: Review and delete saved style descriptions when they are no longer needed, especially when they describe identifiable people or sensitive attributes.

Risk: Generated media can be sent to an unintended OpenClaw channel or target.

Mitigation: Verify the OpenClaw message target and channel before sending media.

Risk: Minimax endpoints are configurable and could point to an untrusted provider domain.

Mitigation: Restrict Minimax base, text, and image URLs to trusted HTTPS provider domains before enabling that provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laogiant/skills/ellya-ootd)
- [Publisher profile](https://clawhub.ai/user/laogiant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated local files such as style descriptions and image outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under output/; learned style descriptions are saved under styles/; photo series are saved in timestamped output directories.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
