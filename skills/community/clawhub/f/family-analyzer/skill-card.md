## Description:

Analyzes family or group chat exports and produces Markdown soul and persona files that can be used as AI agent personality foundations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengury](https://clawhub.ai/user/zengury)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process WeChat, WhatsApp, or CSV chat exports into a collective personality document and per-member persona Markdown files for agent configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private family, group, or third-party chat exports and may send content to external model providers.

Mitigation: Run only with participant consent, use non-sensitive test data first, and document every external provider before processing real chat exports.

Risk: The release bundles a raw chat export and server evidence flags under-disclosed external AI calls.

Mitigation: Remove bundled private chat data and verify data paths point only to the user-selected input file before installation or execution.

Risk: Server evidence reports exposed API credentials in the artifact.

Mitigation: Remove hard-coded keys, rotate any exposed credentials, and require API keys to come from user-controlled environment variables.

Risk: Generated soul or persona files could be installed as agent prompts without review.

Mitigation: Review generated Markdown for privacy, accuracy, and impersonation concerns before using it as an agent system prompt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengury/skills/family-analyzer)
- [Publisher profile](https://clawhub.ai/user/zengury)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files with agent-facing progress messages and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a collective soul.md file and per-member persona Markdown files from chat-analysis pipeline output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
