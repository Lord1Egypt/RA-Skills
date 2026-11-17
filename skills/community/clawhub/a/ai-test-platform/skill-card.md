## Description:

Guides development and use of an AI-powered automated testing platform based on LangChain and DeepSeek for generating test cases, executing API and UI automation scripts, creating reports, and managing authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yontlly](https://clawhub.ai/user/yontlly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internal QA engineers use this skill to build, configure, and operate an AI-assisted test automation platform for generating test cases and API/UI scripts, executing tests, and producing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or user-provided test scripts can introduce broad code execution risk.

Mitigation: Run scripts only in a real sandboxed runner with restricted filesystem and network access, and review scripts before execution.

Risk: Admin authorization and role separation are weak for shared or production deployment.

Mitigation: Use deny-by-default admin authorization, separate administrative roles from normal execution roles, and audit privileged actions.

Risk: Secret and database handling are not production hardened.

Mitigation: Store secrets in a dedicated secret manager or protected environment, use non-root database credentials, close public database ports, and rotate exposed defaults.

Risk: Dependency and installation guidance may leave known vulnerabilities or unsafe defaults in place.

Mitigation: Upgrade dependencies, pin reviewed versions, and validate deployment instructions before production or shared use.

## Reference(s):

- [System architecture](references/architecture.md)
- [Project README](project/README.md)
- [Deployment guide](deploy/部署文档.md)
- [ClawHub skill page](https://clawhub.ai/yontlly/skills/ai-test-platform)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code, configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated test cases, API/UI automation scripts, reports, authorization setup, and deployment configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontend package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
