## Description:

Cid Tracking helps agents manage CID-based advertising workflows for OceanEngine, Kuaishou Magnetic Engine, and Tencent Guangdiantong, including tracking link generation, conversion postbacks, ROI analysis, anomaly monitoring, and Excel reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaohang497-tech](https://clawhub.ai/user/zhaohang497-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operations teams, e-commerce ad buyers, and developers use this skill to generate CID tracking links, fetch multi-platform ad data, post conversion events, analyze ROI, detect account anomalies, and produce daily or weekly performance reports.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Ad-platform credentials and conversion data may be exposed or used with excessive account privileges.

Mitigation: Use least-privilege API tokens, keep config.json out of source control, restrict local file permissions, and avoid sending personal identifiers unless legally authorized.

Risk: Generated Excel reports may be vulnerable to formula injection when report fields contain spreadsheet formulas.

Mitigation: Treat generated .xlsx files as untrusted until formula escaping is added, and review files before opening or sharing them.

Risk: Conversion postbacks and data-fetching scripts may affect production advertising accounts.

Mitigation: Review configuration and test against a non-production or limited-scope account before enabling production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaohang497-tech/skills/cid-tracking)
- [OceanEngine open platform](https://oceanengine.github.io/open-platform/)
- [Kuaishou Magnetic Engine platform](https://mp.kuaishou.com/)
- [Tencent Guangdiantong developer platform](https://e.qq.com/dev/)
- [CID tracking best practices](references/cid_best_practices.md)
- [OceanEngine API reference](references/oceanengine_api.md)
- [Kuaishou API reference](references/kuaishou_api.md)
- [Tencent API reference](references/tencent_api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, JSON data files, and Excel workbook outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may include CID link lists, platform ad data, ROI analysis JSON, anomaly alerts, and .xlsx reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
