## Description:

Collects China Ministry of Finance fiscal revenue and expenditure announcements, extracts monthly indicators, derives deficit metrics, and helps analyze or troubleshoot the resulting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cy7533](https://clawhub.ai/user/cy7533)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run a fiscal data collection pipeline for China Ministry of Finance announcements, then inspect Excel workbooks and Markdown reports for monthly revenue, expenditure, and deficit analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler may make outbound requests beyond the intended Ministry of Finance source.

Mitigation: Run it in a constrained environment and restrict outbound network access to the intended Ministry of Finance host.

Risk: Dependencies are unpinned.

Mitigation: Pin and review dependencies before installing or running the skill.

Risk: Automated parsing can miss or misread data when the source page structure or fiscal wording changes.

Mitigation: Review generated warning records and validate important results against the retained source announcement links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cy7533/skills/financial-data-collection)
- [Publisher profile](https://clawhub.ai/user/cy7533)
- [China Ministry of Finance fiscal data releases](https://www.mof.gov.cn/gkml/caizhengshuju/)
- [Skill README](FinancialDataCollection/README.md)
- [Agent requirements](FinancialDataCollection/docs/AGENT.MD)
- [Data collection requirements](FinancialDataCollection/docs/REQUIREMENT.MD)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Analysis, Files, Markdown]

**Output Format:** [Markdown guidance with shell commands, plus generated Excel workbooks and Markdown run reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline outputs are organized by fiscal period and timestamped summary directories.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
