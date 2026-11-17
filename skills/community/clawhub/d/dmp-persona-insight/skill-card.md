## Description:

DMP Persona Insight analyzes DMP audience profile data, identifies high-signal persona features with TGI and coverage metrics, and produces structured user insight reports and presentation-ready strategy outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts, growth teams, product operators, and developers use this skill to retrieve or analyze DMP audience insight data, build user personas, and generate campaign, channel, content, and product strategy recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-looking DMP credentials may be exposed in examples or guidance.

Mitigation: Remove and rotate exposed AK/SK examples before using the skill with real DMP data, and configure credentials only through OpenClaw secret configuration or a secrets manager.

Risk: Unsafe TLS guidance or code may weaken API transport security.

Mitigation: Enable TLS verification and remove curl -k and verify=False usage before deployment.

Risk: Audience data and generated reports may contain sensitive commercial or user-profile information.

Mitigation: Document how uploaded audience data and generated reports are handled, reviewed, retained, and shared before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingri26/skills/dmp-persona-insight)
- [Mingdata Open Platform](https://open.mingdata.com)
- [Mingdata Ability Center](https://open.mingdata.com/ability-center)
- [Quickstart guide](references/quickstart.md)
- [Operation guide](references/operation-guide.md)
- [DMP API integration guide](references/api-integration.md)
- [Insight integration guide](references/insight-integration.md)
- [Analysis framework](references/analysis-framework.md)
- [Feature extraction standard](references/FEATURE_EXTRACTION_STANDARD.md)
- [PPT v4.2 usage guide](references/ppt-v4.2-usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports, PowerPoint files, Python usage snippets, shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DMP_AK and DMP_SK for Mingdata DMP API access; can also work from uploaded Excel or CSV audience data as documented.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter version: 9.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
