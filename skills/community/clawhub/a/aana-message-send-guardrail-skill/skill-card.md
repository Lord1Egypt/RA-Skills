## Description: <br>
Validates message destination, audience, tone, privacy, claims, and explicit approval before an agent sends or posts messages on chat and SMS channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a pre-send review gate for Slack, Teams, Discord, SMS, direct messages, and public channel posts. It helps an agent decide whether to draft, revise, ask, redact, request approval, send, or block a message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured external checker could receive private messages, customer records, logs, secrets, screenshots, or unrelated thread history. <br>
Mitigation: Send only the minimal redacted review payload described by the skill, and omit raw private content when a summary is enough. <br>
Risk: An agent could post to an ambiguous, broad, public, or external destination without the user intending that audience. <br>
Mitigation: Verify channel, recipients, mentions, broadcast scope, and explicit send approval; ask for confirmation or block when destination or audience is unclear. <br>
Risk: Unsupported claims, hostile tone, or sensitive details could be sent in high-impact messages. <br>
Mitigation: Revise tone, retrieve evidence for claims, redact sensitive details, and route public, external, irreversible, or high-impact sends for approval before posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-message-send-guardrail-skill) <br>
- [Packaged README](artifact/README.md) <br>
- [Message send guardrail schema](artifact/schemas/message-send-guardrail.schema.json) <br>
- [Redacted review payload example](artifact/examples/redacted-message-send-guardrail.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown instructions with a structured text decision pattern and optional JSON review payload schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute code, call messaging services, write files, persist memory, install dependencies, or send messages on its own.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
