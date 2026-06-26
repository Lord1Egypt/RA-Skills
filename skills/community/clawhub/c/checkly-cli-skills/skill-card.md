## Description: <br>
Comprehensive Checkly CLI command reference and Monitoring as Code workflows for authentication, configuration, checks, testing, deployment, imports, constructs, and advanced Checkly patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vince-winkintel](https://clawhub.ai/user/vince-winkintel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, test, deploy, import, and troubleshoot Checkly Monitoring as Code projects through the Checkly CLI. It also helps agents generate Checkly configuration, checks, monitors, Playwright checks, and operational shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-proposed Checkly commands can deploy monitoring changes or target the wrong Checkly account. <br>
Mitigation: Confirm CHECKLY_ACCOUNT_ID and the target environment before execution, and prefer validation, dry-run, or preview steps before deployment. <br>
Risk: CHECKLY_API_KEY, CHECKLY_ACCOUNT_ID, and downloaded result assets can expose sensitive account or application data. <br>
Mitigation: Protect credentials, avoid printing or committing secrets, and download only the assets needed for diagnosis. <br>
Risk: Force deploys, member role changes, member deletes, imports, and check deletes can change production monitoring or account access. <br>
Mitigation: Require explicit review for destructive or access-changing commands, use dry-run where available, and verify target identities before applying changes. <br>


## Reference(s): <br>
- [Checkly CLI Documentation](https://www.checklyhq.com/docs/cli/) <br>
- [Monitoring as Code Guide](https://www.checklyhq.com/docs/monitoring-as-code/) <br>
- [Checkly Runtimes](https://www.checklyhq.com/docs/runtimes/) <br>
- [Playwright Documentation](https://playwright.dev/) <br>
- [Checkly CLI GitHub Repository](https://github.com/checkly/checkly-cli) <br>
- [best-practices.md](references/best-practices.md) <br>
- [troubleshooting.md](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Checkly CLI commands, TypeScript templates, configuration snippets, troubleshooting steps, and account-operation guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
