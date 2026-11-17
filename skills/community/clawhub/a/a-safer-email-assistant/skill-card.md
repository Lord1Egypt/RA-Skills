## Description:

Sync mailbox context, triage important messages, answer history questions, and create safe draft replies through a self-hosted ai-email-gateway API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[remimikalsen](https://clawhub.ai/user/remimikalsen)

### License/Terms of Use:

MIT-0

## Use Case:

People who connect an agent to a self-hosted email gateway use this skill to sync selected mailbox context, identify important new messages, answer email-history questions, and prepare draft replies without sending mail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox contents or message metadata may be exposed through helper output or shared logs.

Mitigation: Run the helper only in trusted environments, avoid shared stdout logging, and limit output to the messages needed for the task.

Risk: Bearer-token access to the configured gateway can expose selected mailbox accounts if the endpoint or key is mismanaged.

Mitigation: Use HTTPS for non-local gateways, prefer narrowly scoped and revocable API keys, and protect required environment variables.

Risk: The local state file records polling metadata for mailbox accounts.

Mitigation: Keep the state file in a restricted location with appropriate file permissions and change its path only intentionally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/remimikalsen/skills/a-safer-email-assistant)
- [ai-email-gateway source and deployment docs](https://github.com/ArktIQ-IT/ai-email-gateway)
- [API reference](api-reference.md)
- [Importance classifier template](prompts/importance-classifier.md)
- [Drafting style template](prompts/drafting-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON draft payloads, and shell/API command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can cite message ids, draft ids, account ids, timeframes, findings, and suggested actions.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
