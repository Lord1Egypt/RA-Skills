## Description:

Store or retrieve credentials in Bitwarden via the Bitwarden CLI after the user unlocks their vault and provides a BW_SESSION value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users use this skill to store named passwords, API keys, OAuth tokens, and other credentials in a Bitwarden vault through the local Bitwarden CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Bitwarden vault session tokens and plaintext secrets, which can be exposed through chat, command history, process arguments, or agent transcripts.

Mitigation: Keep BW_SESSION and plaintext secrets out of chat, command history, process arguments, and transcripts; prefer local execution with the session already in the environment and hidden prompts or stdin for secrets.

Risk: Bitwarden CLI item creation output can reveal sensitive created-item details if printed without sanitization.

Mitigation: Sanitize or suppress Bitwarden CLI output and avoid printing created-item JSON or secret values.

## Reference(s):

- [Bitwarden](https://bitwarden.com)
- [Bitwarden CLI Download](https://bitwarden.com/download)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Bitwarden CLI, jq, and an unlocked vault session supplied through BW_SESSION.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
