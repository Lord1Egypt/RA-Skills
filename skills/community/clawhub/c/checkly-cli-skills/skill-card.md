## Description:

Comprehensive Checkly CLI command reference and Monitoring as Code workflows for authoring, testing, deploying, importing, and operating synthetic checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to plan and execute Checkly CLI workflows for Monitoring as Code, including authentication, configuration, check creation, local testing, imports, deployment, account usage, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkly credentials and account identifiers may allow cloud account changes.

Mitigation: Use a least-privilege Checkly API key and account for agent-assisted workflows.

Risk: Deployment, destroy, import commit or cancel, check delete or run, and member changes can affect live Checkly resources.

Mitigation: Review previews and dry-runs before approving cloud-changing commands.

Risk: Floating npx or npm resolution can change the Checkly CLI version used in automation.

Mitigation: Pin the Checkly CLI version in CI when repeatable behavior is required.

## Reference(s):

- [Checkly CLI Skills on ClawHub](https://clawhub.ai/vince-winkintel/skills/checkly-cli-skills)
- [Best Practices](references/best-practices.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, TypeScript snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command previews, dry-run guidance, and confirmation steps for Checkly cloud changes.]

## Skill Version(s):

1.0.19 (source: server release metadata and VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
