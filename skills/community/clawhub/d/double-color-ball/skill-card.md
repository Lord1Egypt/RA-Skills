## Description:

Provides recent China Double Color Ball lottery draw results, trend analysis, and entertainment-only number suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltap266](https://clawhub.ai/user/ltap266)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve recent Double Color Ball lottery results, review simple trend summaries, and generate entertainment-only number suggestions. It should not be treated as financial, gambling, or wagering advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The environment checker looks for Baidu-related credentials and local configuration paths.

Mitigation: Remove the checker or restrict diagnostics to explicit user-provided settings; avoid scanning workspace files or printing configuration lines.

Risk: The network code disables TLS certificate and hostname verification.

Mitigation: Restore default TLS verification and fail clearly when a source cannot be reached securely.

Risk: The skill can fall back to simulated lottery records when live sources fail.

Mitigation: Fail clearly or label synthetic records prominently, and do not present them as usable draw results.

Risk: The artifact includes default-routing and MEMORY.md binding claims.

Mitigation: Remove default-routing claims and require explicit user invocation or platform-approved routing.

Risk: Entertainment predictions may be mistaken for wagering advice.

Mitigation: Keep suggestions labeled as entertainment-only and avoid purchase, betting, or financial recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ltap266/skills/double-color-ball)
- [Publisher profile](https://clawhub.ai/user/ltap266)
- [China Welfare Lottery draw notice API](https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=10)
- [17500 Double Color Ball information](https://www.17500.cn/ssq/newinfo.php)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with headings, tables, trend bullets, and entertainment-only suggestion sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output can include data source and freshness labels; artifact behavior shows fallback to simulated records when live sources fail.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
