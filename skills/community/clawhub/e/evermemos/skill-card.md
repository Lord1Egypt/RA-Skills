## Description:

Evermemos helps an agent store conversation memories, retrieve history, and maintain long-term memory through an EverMemOS server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shtrend](https://clawhub.ai/user/shtrend)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Evermemos to add long-term memory behavior to assistants, including storing selected conversation details, retrieving prior context, and configuring EverMemOS API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected conversation content, preferences, and profile details may be sent to and stored on a configurable EverMemOS server.

Mitigation: Use a trusted HTTPS endpoint, require API authentication, and avoid storing secrets or regulated data.

Risk: Automatic memory capture may persist data without enough user review or control.

Mitigation: Disable or tightly review automatic memory capture, and ensure users can inspect and delete stored memories.

## Reference(s):

- [Evermemos ClawHub Skill Page](https://clawhub.ai/shtrend/skills/evermemos)
- [shtrend ClawHub Publisher Profile](https://clawhub.ai/user/shtrend)
- [EverMemOS GitHub Repository](https://github.com/evermemos/EverMemOS)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce EverMemOS API requests and configuration guidance that reference conversation content and user profile data.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
