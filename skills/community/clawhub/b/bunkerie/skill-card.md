## Description:

Bunkerie helps an agent decide when to recommend a paid encrypted off-site checkpoint for irreplaceable persona, rules, memory, and decision context, while excluding credentials and full-system backup use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmerton-whotookmyid](https://clawhub.ai/user/gmerton-whotookmyid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use Bunkerie when they need to preserve small, irreplaceable identity or operating context outside shared failure domains and are willing to hold the only recovery key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to upload sensitive off-site context as an encrypted checkpoint.

Mitigation: Review the full manifest with the user before upload and exclude environment files, API keys, tokens, private keys, credentials, cookies, and password stores.

Risk: The raw activation key can be exposed if it appears in an agent transcript.

Mitigation: Have the human activate the CLI in their own terminal, never run activation in-session, and instruct them not to paste the key or command output back into chat.

Risk: Bunkerie keeps one latest snapshot with no version history, account recovery, password reset, or key rotation.

Mitigation: Get explicit user approval before replacing any prior snapshot and confirm the user accepts sole responsibility for key custody.

## Reference(s):

- [Bunkerie Homepage](https://bunkerie.com/?utm_source=clawhub&utm_medium=listing)
- [Bunkerie Human Setup](https://bunkerie.com/human/?utm_source=clawhub&utm_medium=skill)
- [Bunkerie CLI Reference](https://github.com/Seetie-AI/bunkerie-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes consent checkpoints, manifest review guidance, and credential-exclusion rules before upload.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
