## Description:

Use dLazy's Claude Sonnet 5 service for reasoning, coding, and complex tool orchestration, with text, image, and video inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send prompts, optionally with images or videos, to dLazy's hosted Claude Sonnet 5 service and receive generated text or media for reasoning and coding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied media are sent to dLazy's hosted service, and the partial security scan did not fully verify package behavior.

Mitigation: Review the CLI package and service terms before sending sensitive data; protect the API key and rotate or revoke it when needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-claude-sonnet-5)
- [dLazy service](https://dlazy.com)
- [CLI project page](https://github.com/dlazy-ai/cli)
- [npm package](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Generated media files]

**Output Format:** [JSON API response with generated text or media output references; optional saved asset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a prompt with optional image or video inputs; supports asynchronous jobs and optional local saving.]

## Skill Version(s):

1.2.47 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
