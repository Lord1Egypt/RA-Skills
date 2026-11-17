## Description:

Calorie Detective uses AI vision to identify food from photos and estimate calories, macronutrients, and diet suggestions with Kimi vision support and a local nutrition database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaa2531349](https://clawhub.ai/user/aaa2531349)

### License/Terms of Use:

MIT

## Use Case:

External users and health-focused consumers use this skill to analyze food photos, estimate nutritional content, and receive practical diet guidance. Developers can deploy it through Kimi Claw or run it locally with configured vision-provider credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food images or other readable files may be sent to external vision providers if upload paths are too broad or file validation is weak.

Mitigation: Use only non-sensitive food images, run with a narrowly scoped upload directory, and add image validation before production use.

Risk: Misconfigured provider credentials may cause requests to use the wrong API key or provider settings.

Mitigation: Fix provider-specific API key selection and verify provider configuration in a non-production environment before release.

Risk: Nutrition estimates and diet suggestions may be inaccurate or inappropriate for users with medical or dietary constraints.

Mitigation: Present results as estimates, keep the disclaimer visible, and direct users with health-specific needs to qualified professionals.

## Reference(s):

- [Calorie Detective ClawHub listing](https://clawhub.ai/aaa2531349/skills/calorie)
- [Kimi API documentation](https://platform.moonshot.cn/docs)
- [Kimi Claw console](https://platform.moonshot.cn/console/claw)
- [Deployment guide](artifact/DEPLOY.md)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown nutrition report with food identification, calorie estimates, macronutrient breakdown, and diet suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external vision APIs and uses estimated nutrition data; outputs should be treated as informational, not medical advice.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
