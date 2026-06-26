## Description: <br>
Boheng Investment Workflow runs an eight-analyst investment research workflow for A-share stocks, funds, ETFs, and convertible bonds using market data and optional financial statement data, with outputs framed as informational only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangboheng](https://clawhub.ai/user/zhangboheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze Chinese-market stocks, funds, ETFs, and convertible bonds and generate multi-analyst investment research reports. The reports are for learning and reference, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes third-party financial and news requests, plus optional browser automation, are not disclosed consistently enough for automatic approval. <br>
Mitigation: Install only if that network and optional browser behavior is acceptable, keep browser news disabled unless needed, and review the configured domains before use. <br>
Risk: The skill reads USER.md for investment preferences and saves local reports. <br>
Mitigation: Keep sensitive information out of USER.md and review generated reports before sharing or relying on them. <br>
Risk: Investment analysis can be incomplete, stale, or misleading. <br>
Mitigation: Treat outputs as informational, verify against official filings and market data, and do not use the reports as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangboheng/boheng-investment-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/zhangboheng) <br>
- [Author website](https://www.luckydesigner.space) <br>
- [AKShare documentation](https://akshare.akfamily.xyz/) <br>
- [AKShare GitHub](https://github.com/akfamily/akshare) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown and plain-text investment analysis reports with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved under ~/.openclaw/workspace/investment/reports/.] <br>

## Skill Version(s): <br>
1.5.5 (source: server release evidence and SKILL.md frontmatter; changelog released 2026-05-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
