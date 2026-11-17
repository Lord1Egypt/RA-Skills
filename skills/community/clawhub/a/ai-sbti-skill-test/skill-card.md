## Description:

AI-based SBTI skill test SEO operations for https://aisbti.com/ with weighted backlink scoring, internal link-juice relay planning, and safe anchor distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cweiping](https://clawhub.ai/user/cweiping)

### License/Terms of Use:

MIT-0

## Use Case:

SEO operators and site maintainers use this skill to score backlink prospects for aisbti.com, check anchor distribution, and plan internal link relay actions from acquired links to priority pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can source a configurable env file before generating the plan.

Mitigation: Install only when you control the env file and CSV inputs, run as an unprivileged user, and do not point AI_SBTI_SKILL_TEST_ENV_FILE at untrusted files.

Risk: Generated Markdown may include content derived from external prospect data.

Mitigation: Review generated Markdown as untrusted content before sharing or acting on it.

## Reference(s):

- [SEO Link Building Standard](references/seo-link-building-standard.md)
- [ClawHub Skill Page](https://clawhub.ai/cweiping/skills/ai-sbti-skill-test)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown plan and JSON report, with shell commands and configuration guidance for running the planner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scored backlink candidates, rejected-candidate reasons, anchor-mix alerts, and internal relay recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
