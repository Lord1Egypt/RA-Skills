## Description: <br>
Knowledge and guardrails for the mise + fnox + infisical secrets toolchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[basher83](https://clawhub.ai/user/basher83) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to validate local secret-tool availability and receive configuration guidance for mise, fnox, and Infisical-based secret injection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill concerns developer secret tooling and may lead an agent to suggest commands that expose or persist secrets. <br>
Mitigation: Review every export or hook command before execution, avoid printing secrets to stdout, and prefer process-scoped secret injection such as fnox exec or infisical run. <br>
Risk: Secret values can be accidentally committed when written to .env files, fnox configuration, or local generated files. <br>
Mitigation: Keep generated secret files out of git, use encrypted providers or remote references for sensitive values, and scan before pushing. <br>
Risk: Misconfigured profiles, paths, or expired Infisical authentication can silently omit expected secrets. <br>
Mitigation: Confirm fnox profiles match Infisical environment slugs, verify secret paths and token scope, and refresh authentication before relying on injected values. <br>


## Reference(s): <br>
- [Devtools Secrets ClawHub release](https://clawhub.ai/basher83/devtools-secrets) <br>
- [fnox Configuration Reference](references/fnox-configuration.md) <br>
- [Infisical Patterns Reference](references/infisical-patterns.md) <br>
- [mise Integration Reference](references/mise-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance should validate installed tools before configuration steps and avoid exposing secrets in stdout or persisted environment files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
