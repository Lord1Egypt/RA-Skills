## Description:

Use the dLazy CLI to access Moonshot AI's Kimi K3 model for text, image, and video understanding, analysis, coding, and writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use the Kimi K3 model through dLazy for complex analysis, coding, writing, and tasks involving image or video inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied media are sent to dLazy's hosted API and media storage for processing.

Mitigation: Avoid submitting sensitive content unless permitted by your organization; review dLazy's service terms and data handling first.

Risk: Using the CLI requires an external package and API-key setup, which stores or handles credentials on the user's system.

Mitigation: Review the package and its credential handling before installation; protect the API key and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-kimi-k3)
- [dLazy CLI project link listed in skill metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Text, Code, JSON, Files]

**Output Format:** [JSON response containing generated content or asset URLs; optional local file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the prompt; asynchronous requests can return a task ID and status.]

## Skill Version(s):

1.2.36 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
