## Description:

Coze is an AI bot development assistant for building bots, developing plugins, orchestrating workflows, and configuring knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bot builders use this skill for guidance on creating Coze bots, configuring plugins and knowledge bases, designing workflows, publishing bots, and adapting Coze API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API example includes a placeholder bearer token pattern that could be copied into real code with hardcoded credentials.

Mitigation: Use real Coze tokens only from a secret store or environment variable, and avoid logging tokens.

Risk: Coze bot integrations can send user content or uploaded knowledge-base data to external services.

Mitigation: Avoid sending sensitive user data unless consent, privacy basis, and the appropriate Coze environment are confirmed.

## Reference(s):

- [ClawHub Coze skill page](https://clawhub.ai/zhangifonly/skills/coze)
- [ClawHub publisher profile](https://clawhub.ai/user/zhangifonly)
- [Coze chat API endpoint referenced by the skill](https://api.coze.cn/v3/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
