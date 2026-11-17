## Description:

Daxiang Dogfood guides agents through authorized web-application QA by exploring pages, testing workflows, capturing evidence, and producing a structured bug report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to dogfood web applications, reproduce issues, and hand off actionable bug reports with screenshots, videos, severity, category, and repro steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interact with real web applications and may perform testing actions against systems outside the user's authority.

Mitigation: Use it only on applications and scopes the user is authorized to test.

Risk: Screenshots, videos, reports, and saved browser state can contain sensitive application data or credentials.

Mitigation: Use a private output directory, treat generated evidence and auth-state.json as sensitive, and delete saved session state after use.

Risk: Testing with high-privilege production accounts can increase the impact of mistakes or unintended actions.

Mitigation: Prefer test accounts or least-privilege non-admin accounts when authentication is required.

Risk: Using the npx tool path can introduce uncontrolled package-source and version risk.

Mitigation: Use the direct agent-browser binary, or only use npx when the package source and version are controlled.

## Reference(s):

- [Daxiang Dogfood ClawHub Page](https://clawhub.ai/daxiangnaoyang/skills/daxiang-dogfood)
- [Issue Taxonomy](references/issue-taxonomy.md)
- [Dogfood Report Template](templates/dogfood-report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown report with linked screenshot and video evidence plus inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, repro videos, report files, and saved browser authentication state in the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
