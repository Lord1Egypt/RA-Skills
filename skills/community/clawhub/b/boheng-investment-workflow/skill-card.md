## Description:

Investment research multi-agent decision system that runs eight analyst roles in parallel, applies weighted voting, and produces informational analysis for A-share stocks, funds, ETFs, and convertible bonds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangboheng](https://clawhub.ai/user/zhangboheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Chinese A-share stocks, funds, ETFs, and convertible bonds through multi-agent financial analysis, data-source labeling, and generated research reports. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically reads USER.md investment preferences and can persist derived profile details in local reports.

Mitigation: Remove sensitive details from USER.md before use, run the skill in an isolated workspace, and review or delete generated reports before sharing the workspace.

Risk: The skill performs external financial and news data requests, and optional browser news collection can launch browser subprocesses.

Mitigation: Keep browser news disabled unless needed, use a virtual environment with pinned dependencies, and review allowed network domains before deployment.

Risk: Generated investment recommendations may be incomplete, stale, or misleading.

Mitigation: Treat outputs as informational research only, verify data against official filings or trusted market sources, and consult a qualified professional before making investment decisions.

Risk: Security disclosures in the artifact may not fully match saved-data, HTTP-traffic, and browser-subprocess behavior reported by server scanning.

Mitigation: Use evidence.security as the authoritative risk source during review and update public disclosures before broad release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangboheng/skills/boheng-investment-workflow)
- [Author Website](https://www.luckydesigner.space)
- [AKShare Official Documentation](https://akshare.akfamily.xyz/)
- [AKShare GitHub](https://github.com/akfamily/akshare)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain-text reports with shell command examples and structured analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis scripts can write reports under ~/.openclaw/workspace/investment/reports/.]

## Skill Version(s):

1.5.5 (source: server release evidence, frontmatter, and changelog released 2026-05-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
