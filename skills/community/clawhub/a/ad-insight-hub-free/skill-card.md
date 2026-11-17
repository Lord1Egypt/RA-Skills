## Description:

AdMapix广告情报API基础查询，参数翻译+创意搜索+应用画像。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, growth teams, developers, and automation workflow users use this skill to translate Chinese advertising lookup requests into AdMapix API queries for creative search, creative counts, and app or developer profile retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags the release as suspicious because it advertises file-writing and broad automation capabilities that are not clearly needed for AdMapix lookup workflows.

Mitigation: Grant only the permissions required for AdMapix API queries, and avoid enabling local write access unless a specific output-file workflow requires it.

Risk: The skill uses curl commands with ADMAPIX_API_KEY to call a remote API.

Mitigation: Keep ADMAPIX_API_KEY in the environment rather than chat or files, and inspect generated curl commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ad-insight-hub-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)
- [AdMapix API endpoint](https://api.admapix.com)
- [AdMapix registration](https://www.admapix.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ADMAPIX_API_KEY from the environment and returns AdMapix structured JSON without renaming fields.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
