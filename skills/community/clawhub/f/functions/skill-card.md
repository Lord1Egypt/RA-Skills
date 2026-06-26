## Description: <br>
Guide Claude through deploying serverless browser automation using the official bb CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peytoncasper](https://clawhub.ai/user/peytoncasper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create, test, deploy, and invoke Browserbase Functions for scheduled, webhook, or cloud-hosted browser automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browserbase API keys and project IDs may be exposed if environment files, logs, or generated examples are handled carelessly. <br>
Mitigation: Keep .env files out of version control, avoid printing secrets in logs, and prefer scoped or short-lived credentials. <br>
Risk: Package commands and publish steps can install dependencies or deploy cloud automation in the wrong project. <br>
Mitigation: Review generated automation before publishing and run package commands only in the intended project directory. <br>
Risk: Authenticated browser automation may access sensitive account data or perform unintended actions. <br>
Mitigation: Use test accounts where possible and review workflows before running them against production services. <br>


## Reference(s): <br>
- [Functions on ClawHub](https://clawhub.ai/peytoncasper/functions) <br>
- [Browserbase settings](https://browserbase.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of Browserbase API credentials, local development commands, deployment commands, invocation examples, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
