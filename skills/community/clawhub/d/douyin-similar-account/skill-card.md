## Description:

This skill queries RedFox with a Douyin account name or ID to return account data, similar account recommendations, top-account benchmarks, and optimization analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin creators, content operators, brand marketers, and MCN teams use this skill to find comparable and leading accounts, compare RedFox Index gaps, and identify content or placement opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin account names or IDs to RedFox and requires a RedFox API key.

Mitigation: Use it only for account queries you are comfortable sharing with RedFox, and provide the API key through a platform secret store or a temporary session environment variable.

Risk: Security evidence reports API-key persistence/search behavior and an unsafe wrapper script.

Mitigation: Review the scripts before execution, avoid shell-profile modification, and do not expose API keys in prompts, logs, source files, or generated output.

Risk: The subscription prompt behavior is under-specified.

Mitigation: Treat subscription as opt-in only after the publisher documents unsubscribe, retention, and notification behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-similar-account)
- [Publisher profile](https://clawhub.ai/user/redfox-data)
- [Core workflow](references/core_workflow.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox querySimilarAccounts API endpoint](https://redfox.hk/story/api/dyUser/querySimilarAccounts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown-formatted text with account summary sections, comparison tables, account links, data notes, and a subscription prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill requires REDFOX_API_KEY and sends the queried Douyin account name or ID to RedFox.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
