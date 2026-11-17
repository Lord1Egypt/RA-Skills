## Description:

Anthropic's latest Sonnet model for reasoning, code generation, and complex tool orchestration, with text, image, and video inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can send prompts to dLazy's hosted Claude Sonnet service for reasoning, code generation, and tool-oriented assistance. The CLI can also pass image or video inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan could not establish the CLI's exact authentication effects or package behavior, and flagged login and authentication setup that are not clearly connected to the skill's stated purpose.

Mitigation: Before installing, review the third-party CLI and its login/API-key setup, and confirm you intend to use the dLazy service.

Risk: Prompts and local image or video files may be sent to dLazy's hosted service.

Mitigation: Avoid sending sensitive prompts or media unless you are authorized to share them and have reviewed the service terms.

## Reference(s):

- [dLazy service](https://dlazy.com)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)
- [CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [CLI project link from skill metadata](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Text, Code, JSON]

**Output Format:** [Model-generated text or JSON in a JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports prompt, image, and video inputs; can return results asynchronously or save result assets.]

## Skill Version(s):

1.2.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
