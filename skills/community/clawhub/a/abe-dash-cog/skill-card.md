## Description:

Interactive dashboards and apps powered by SkillBoss API Hub for data visualization, analytics dashboards, KPI trackers, charts and graphs, interactive HTML apps, data explorers, games, and AI-assisted web app generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to generate interactive dashboards, KPI trackers, data explorers, calculators, simple games, and self-contained HTML web apps through the SkillBoss API Hub. It supports prompts that include inline data, uploaded datasets, or generated sample data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and included dataset content may be sent to SkillBoss's external API.

Mitigation: Use synthetic, anonymized, minimized, or approved data for business, employee, customer, financial, log, or regulated datasets.

Risk: The required SkillBoss API key could be exposed if copied into prompts, files, or source control.

Mitigation: Keep SKILLBOSS_API_KEY in an environment variable or secret manager and avoid embedding it directly in generated code.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/abe-dash-cog)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [code, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, shell, prompt, and HTML code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may generate self-contained HTML apps with embedded CSS and JavaScript.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
