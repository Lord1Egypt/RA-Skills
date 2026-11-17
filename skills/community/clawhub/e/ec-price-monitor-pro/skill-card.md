## Description:

Free Lite ecommerce price monitoring for basic Taobao and Pinduoduo price searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[since198905](https://clawhub.ai/user/since198905)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run manual keyword-based price checks across Taobao and Pinduoduo and produce a basic comparison report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says this Lite release contains extra executable code for JD monitoring, external notifications, and ClawHub login logging that does not match its documented purpose.

Mitigation: Review the installed files before use and remove or avoid undocumented executables unless those behaviors are intended.

Risk: Price data is collected from public ecommerce search pages and may be incomplete, stale, or inaccurate when page structure or access behavior changes.

Mitigation: Treat generated prices as a comparison aid and verify prices directly on the ecommerce platform before making purchase decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/since198905/skills/ec-price-monitor-pro)
- [Configuration example](artifact/references/config.yaml)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text price comparison report with configuration-driven inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses keyword and optional item configuration to query ecommerce search pages and report available prices.]

## Skill Version(s):

1.1.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
