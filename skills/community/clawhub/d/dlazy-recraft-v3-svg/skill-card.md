## Description:

Generate high-quality SVG vector graphics from text using Recraft v3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to generate SVG-style vector graphics from text prompts through the dLazy Recraft v3 SVG command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or runs a third-party npm CLI.

Mitigation: Install only if the publisher and @dlazy/cli package are trusted; prefer npx or a contained environment over a long-lived global install.

Risk: Prompts and selected local files are sent to dLazy cloud endpoints.

Mitigation: Avoid submitting sensitive prompts or private file paths unless upload to dLazy is intended and approved.

Risk: The skill requires a dLazy API key stored locally or supplied through an environment variable.

Mitigation: Keep the API key scoped to the intended organization and rotate or revoke it when the service is no longer used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-recraft-v3-svg)
- [dLazy CLI source](https://github.com/dlazyai/cli)
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns JSON containing generated image output URLs, or an asynchronous task identifier when invoked without waiting.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
