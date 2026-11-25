## Description:

Efficient text generation, dialogue QA, and logical reasoning using Grok 4.2 text model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

For users who choose to invoke it, this skill provides a CLI workflow for submitting prompts to dLazy's hosted service. Its stated purpose is text generation, question answering, and reasoning with Grok 4.2.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because generic chat triggers may route ordinary requests to dLazy, and the scanned instructions do not demonstrate a link between the CLI invocation and the stated Grok 4.2 purpose.

Mitigation: Review the invocation and CLI behavior before use; invoke it only when dLazy processing is intended, and avoid sending sensitive prompts or media unless that transfer is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-grok-4-2)
- [dLazy homepage](https://dlazy.com)
- [@dlazy/cli package](https://www.npmjs.com/package/@dlazy/cli)
- [CLI project link listed in skill metadata](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Generated text or a JSON result envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous runs may return a task ID before the generated result is ready.]

## Skill Version(s):

1.3.44 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
