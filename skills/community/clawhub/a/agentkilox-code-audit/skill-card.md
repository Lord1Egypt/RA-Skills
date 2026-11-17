## Description:

Scans submitted code for security issues such as hardcoded secrets and dangerous functions, then returns a confidence score and detailed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crftsmnd](https://clawhub.ai/user/crftsmnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and CI/CD pipelines use this skill to run a quick pre-deployment security scan on code and receive issue details for triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted source code is sent to an external paid audit endpoint.

Mitigation: Submit only code you are authorized to share, remove secrets before scanning, and avoid private repositories unless the service privacy terms are acceptable.

Risk: A clean confidence score is not a strong security gate.

Mitigation: Treat results as triage guidance and review important code with established local or CI security tools before release.

Risk: Payment and scanner reliability safeguards may be incomplete.

Mitigation: Confirm payment handling, dependency behavior, scanner failure handling, and temporary-file cleanup before relying on the service in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crftsmnd/skills/agentkilox-code-audit)
- [Publisher profile](https://clawhub.ai/user/crftsmnd)
- [A2A Code Audit API endpoint](https://a2a-code-audit.cvapi.workers.dev/audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces issue details with severity, confidence, line number, scan timing, price, and a confidence score.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
