## Description:

CreBee content analytics helps agents analyze a user's own connected social media accounts, including account-level operations, follower signals, single-post performance, publication-period reviews, HTML dashboards, and structured analytics data across platforms such as Douyin, Bilibili, Xiaohongshu, WeChat Channels, and Kuaishou.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n8spxd](https://clawhub.ai/user/n8spxd)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and operators use this skill with the CreBee desktop client to inspect their own connected account data, compare account health and publication-period performance, and produce operational summaries, dashboards, or structured data for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags that local client discovery can cause an agent to execute a locally supplied runtime without enough verification.

Mitigation: Install and run the CreBee desktop client only from trusted sources, prefer an explicit trusted executable path when needed, and review this skill before installation.

Risk: Another local process could impersonate the CreBee localhost service on an untrusted machine.

Mitigation: Use the skill only on trusted local machines, keep calls bound to 127.0.0.1, and do not redirect the workflow to a remote service.

Risk: Analytics conclusions can be misleading if account-lifecycle metrics and publication-period snapshot metrics are mixed.

Mitigation: Preserve the metric mode and period semantics returned by CreBee, report partial or empty data explicitly, and avoid combining incompatible cross-platform measures.

## Reference(s):

- [CreBee Analytics Reference](artifact/references/analytics.md)
- [CreBee Troubleshooting Reference](artifact/references/troubleshooting.md)
- [CreBee Website](https://www.crebee.cn)
- [CreBee Download Page](https://www.crebee.cn/#/download)
- [ClawHub Skill Page](https://clawhub.ai/n8spxd/skills/crebee-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CreBee CLI results are structured JSON and may reference HTML reports or analytics data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running CreBee desktop client version 1.9.13 or later on the user's machine; analysis should be based on the returned status, warnings, errors, data quality, and artifacts.]

## Skill Version(s):

1.9.13 (source: evidence.release.version and SKILL.md crebee-skill-version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
