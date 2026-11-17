## Description:

Generate images with Black Forest Labs FLUX models using a direct BFL API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gamaleldientarek](https://clawhub.ai/user/gamaleldientarek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate images through Black Forest Labs' direct FLUX API when they have a BFL API key and want direct BFL model access rather than another image provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Black Forest Labs using a BFL API key from the local environment.

Mitigation: Use a restricted BFL API key with spending limits and avoid sending sensitive prompts.

Risk: The security summary flags API-key handling and response-controlled polling URL behavior as credential risks that require review before installation.

Mitigation: Review the output path before use and consider updating the script to parse dotenv safely and validate polling and download URLs before attaching credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gamaleldientarek/skills/black-forest-labs-flux)
- [Black Forest Labs API Endpoint](https://api.bfl.ai/v1/${MODEL})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; script output is a saved image file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BFL_API_KEY and optional BFL_MODEL, BFL_WIDTH, and BFL_HEIGHT environment variables.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
