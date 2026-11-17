## Description:

Triggers Bazhuayu RPA tasks through a configured webhook and passes custom parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blogwebsem](https://clawhub.ai/user/blogwebsem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to configure and invoke Bazhuayu RPA webhook triggers from an agent workflow, including test runs, parameter overrides, and configuration checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships live-looking tenant URLs and a Feishu authorization value in config.json.

Mitigation: Rotate the exposed authorization value, remove tenant-specific URLs, and ship only placeholder configuration before installation or redistribution.

Risk: Setup and migration flows can print or write real secrets.

Mitigation: Review script output before use, avoid persisting secrets in generated files or shell history, and prefer environment variables or a secret manager for webhook keys.

Risk: A live RPA webhook can trigger external automation with user-provided parameters.

Mitigation: Use a test webhook first and require an explicit user-selected production webhook before running live RPA tasks.

Risk: Logs can expose business data or sensitive parameter values.

Mitigation: Redact parameter values by default, restrict log file permissions, and clean up logs that may contain tenant data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blogwebsem/skills/bazhuayu-rpa-webhook)
- [Bazhuayu RPA Help Center](https://rpa.bazhuayu.com/helpcenter)
- [Bazhuayu webhook trigger documentation](https://rpa.bazhuayu.com/helpcenter/docs/skmvua)
- [Bazhuayu RPA API documentation](https://rpa.bazhuayu.com/helpcenter/docs/rpaapi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/text guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and Bazhuayu webhook URL/key configuration before live webhook calls.]

## Skill Version(s):

2.0.5 (source: ClawHub release evidence; artifact package.json reports 2.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
