## Description:

Test and debug CORS (Cross-Origin Resource Sharing) configurations on live URLs, including CORS headers, preflight OPTIONS requests, allowed origins, methods, headers, security posture, and generated framework configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to test live URLs for CORS behavior, debug browser CORS failures, audit common CORS misconfigurations, and draft framework-specific CORS configuration snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send test and audit requests to user-provided URLs, including multiple CORS probe origins.

Mitigation: Run it only against systems you own or have permission to test.

Risk: Generated server configuration snippets may be incomplete or unsafe for a specific production environment.

Mitigation: Treat generated configuration as a draft and validate it with the target framework or server configuration checker before deployment.

Risk: User-controlled origin, method, header, or URL values could lead to misleading tests or unsafe copied configuration.

Mitigation: Review inputs before execution and avoid feeding attacker-controlled values into configuration generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/cors-tester)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact user-provided URLs and print CORS header analysis, audit findings, or draft configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
