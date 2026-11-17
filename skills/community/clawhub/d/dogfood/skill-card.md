## Description:

Systematically explores and tests a web application for bugs, UX issues, and other quality problems, producing a structured report with screenshots, repro videos, and detailed reproduction steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thedalbee](https://clawhub.ai/user/thedalbee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to perform exploratory browser QA on web applications and hand off reproducible findings. It is suited for local, staging, or scoped production-like testing where screenshots, videos, and step-by-step evidence are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle login credentials and save reusable browser authentication state during authenticated testing.

Mitigation: Use least-privileged test accounts, prefer local or staging targets, avoid production credentials, keep the output directory private, and do not share auth-state.json.

Risk: The skill records screenshots and videos that may capture sensitive application data.

Mitigation: Run only on scoped targets with appropriate permission and review generated reports, screenshots, and videos before sharing them.

Risk: Security evidence flags risky command allowance patterns for browser automation.

Mitigation: Review the allowed command surface before installation and remove or pin the npx agent-browser allowance before relying on the skill.

## Reference(s):

- [Issue Taxonomy](references/issue-taxonomy.md)
- [Dogfood Report Template](templates/dogfood-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown report with linked screenshot and video evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create screenshots, repro videos, a report.md file, and auth-state.json when authenticated testing is used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
