## Description:

Aggregates public trending lists from supported Chinese content platforms and can produce terminal summaries or JSON reports for trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loveyou001](https://clawhub.ai/user/loveyou001)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, analysts, and operators use this skill to fetch public hot-list items from supported platforms and generate a daily text or JSON summary for trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and dependency setup may need review before use.

Mitigation: Review the package before installing, prefer a pinned ClawHub installer version, and avoid running npm install unless the python npm dependency is removed or audited.

Risk: Feature claims may overstate platform support.

Mitigation: Expect only Bilibili, Douyin, and Toutiao fetching to work unless additional platform support is verified.

Risk: Unsupported platforms may require cookies or authorization.

Mitigation: Do not provide account cookies for unsupported platforms.

Risk: The --output option writes to the specified path.

Mitigation: Use --output only with a path that is intended to be created or overwritten.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loveyou001/skills/databass001)
- [Bilibili popular endpoint](https://api.bilibili.com/x/web-interface/popular)
- [Douyin hot search endpoint](https://www.douyin.com/aweme/v1/web/hot/search/list/)
- [Toutiao hot board endpoint](https://www.toutiao.com/hot-event/hot-board/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; script output is terminal text or JSON when an output path is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, performs public web requests, and may overwrite the file named by --output.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
