## Description:

AI元认知置信度追踪器 checks an agent answer for confidence using hedging detection and a MiniMax TRUE/FALSE consistency check, then advises adding an uncertainty marker when confidence is low.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freak30](https://clawhub.ai/user/freak30)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add confidence-checking behavior to a conversational agent, especially when they want low-confidence answers flagged before a response is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Question and answer content can be sent to an external MiniMax model even though the skill documentation says question context is not uploaded.

Mitigation: Disclose the external data flow, review prompts for private code, credentials, business data, or personal information before use, and minimize transmitted content.

Risk: The checker uses a local API key and the local mmx command, which may inherit broader environment context than intended.

Mitigation: Run it in a constrained environment with only the required MiniMax credential and review command execution before deployment.

Risk: The weekly research behavior described in the skill could become recurring work without explicit user direction.

Mitigation: Require user confirmation before recurring research or reporting tasks and document the expected cadence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freak30/skills/ai-self-awareness-tracker)
- [UQLM project reference](https://github.com/cvs-health/uqlm)
- [arXiv:2602.17431](https://arxiv.org/abs/2602.17431)
- [arXiv:2604.13068](https://arxiv.org/abs/2604.13068)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance and JSON command-line output from the bundled Python checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external MiniMax model and may recommend prepending an uncertainty marker to an answer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
