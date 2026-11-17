## Description:

Creates first-person AI work journal entries about troubleshooting, productivity, or exploration and publishes them to a user-specified Feishu Wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testman2025](https://clawhub.ai/user/testman2025)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to turn daily AI-assisted work into readable journal entries and publish them under a Feishu Wiki or cloud document parent node they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create Feishu documents in a remote workspace under the logged-in user's account.

Mitigation: Install only when that behavior is expected, keep Feishu authentication under the user's account, and require explicit confirmation before publishing when the request does not clearly ask to publish to Feishu.

Risk: Local Feishu destination configuration can expose private Wiki URLs or node tokens if committed or shared.

Mitigation: Add an ignore rule for config.local.json or store the configuration outside the repository, and use placeholders in public examples.

Risk: Screenshots or source material may include account details, secrets, internal addresses, or private workspace paths.

Mitigation: Ask the user to redact sensitive screenshot content before inserting it into a journal entry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/testman2025/skills/ai-work-journal-feishu)
- [Project homepage from ClawHub metadata](https://github.com/testman2025/ai-practice-journal-feishu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown journal content, Feishu document link, and optional local JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-specified Feishu destination, may request screenshots, and returns the created document link after publishing.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
