## Description:

Produces procurement-focused company background reports or two-company comparisons using bidding records, business profiles, partner relationships, and sourced public information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Business users researching a Chinese company or comparing two companies use this skill to assess bidding history, customers and suppliers, competitors, and publicly reported risks before procurement or partnership decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party service receives company queries and account registration metadata.

Mitigation: Review the service's data handling before use and share only the company details needed for the report.

Risk: Automatic registration sends a hashed device identifier and creates a local credential.

Mitigation: Configure your own ZLBX_API_KEY to skip automatic registration, or give explicit consent before registration.

Risk: Reports are saved locally by default and may contain sensitive findings or contact details.

Mitigation: Review saved files and restrict access and sharing; request contact lookups only when necessary.

Risk: Some service-call instructions are not obvious in the visible skill text.

Mitigation: Review the full skill and its network and account actions before enabling it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dragonzu/skills/company-background-check-qixinbao)
- [Skill setup documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [API quick reference](references/api-quick.md)
- [Company intelligence workflow](references/workflow.md)
- [Report templates](references/report-template.md)
- [Account registration and privacy](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML files]

**Output Format:** [Markdown report in chat and locally saved HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-company or two-company comparison; reports include cited findings and data-coverage caveats.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
