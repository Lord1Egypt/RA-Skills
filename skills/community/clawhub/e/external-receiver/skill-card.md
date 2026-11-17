## Description:

External Receiver starts an HTTP receiver that accepts file uploads, text messages, and webhook JSON, then forwards the received content into an OpenClaw session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kriouerlia](https://clawhub.ai/user/kriouerlia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to receive files, text messages, or webhook JSON from external systems and make those inputs available in an OpenClaw session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default receiver can expose uploaded files and allow external messages to reach an OpenClaw session.

Mitigation: Bind the service to localhost or a trusted interface, require a strong receiver secret, and restrict access with a firewall before use.

Risk: Status and download endpoints can reveal or serve received files.

Mitigation: Protect or remove status and download endpoints when deploying outside a trusted environment.

Risk: Received files, text, and webhook payloads are untrusted content before they enter an OpenClaw session.

Mitigation: Review, scan, and size-limit received content before allowing it to influence agent work.

## Reference(s):

- [External Receiver on ClawHub](https://clawhub.ai/kriouerlia/skills/external-receiver)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local HTTP service and writes received messages or file notifications into an OpenClaw queue.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
