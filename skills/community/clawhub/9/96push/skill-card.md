## Description:

User-approved 96Push desktop client publishing helper for querying platforms and accounts, creating content, inspecting platform rules, and publishing only after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsxs89757](https://clawhub.ai/user/xsxs89757)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to operate a trusted local 96Push client from an agent: check available accounts and platforms, create or update draft content, review platform rules and settings, upload runtime-accessible media, and publish after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The create action can send draft content to 96Push before publishing.

Mitigation: Require explicit user approval before creating content and avoid sending private or unpublished material unless the user intends to use 96Push for that content.

Risk: The skill can operate connected social accounts through publishing, deletion, upload, queue cancellation, and platform configuration changes.

Mitigation: Before any sensitive action, show the content, account targets, draft or live state, visibility, and settings, then require explicit approval; use draft mode or a single account first when practical.

Risk: The rules command can read Markdown outside the intended platform rules folder until path handling is fixed.

Mitigation: Use only platform names from the bundled rules index and do not pass arbitrary platform strings to the rules command.

Risk: The skill requires a 96Push API key for account and publishing operations.

Mitigation: Store PUSH_API_KEY locally in the environment or OpenClaw env file, and do not paste or echo API keys in chat.

## Reference(s):

- [96Push Homepage](https://push.96.cn)
- [96push ClawHub Skill Page](https://clawhub.ai/xsxs89757/skills/96push)
- [Platform Settings Reference](references/platform-settings.md)
- [Platform Rules Index](references/platform-rules/index.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate 96Push only when the user has configured PUSH_API_KEY locally and approved sensitive actions.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
