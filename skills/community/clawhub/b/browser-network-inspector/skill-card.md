## Description:

Browser-side request inspection and reporting for user-authorized web debugging of page fetch, XMLHttpRequest, WebSocket, login, registration, and API flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougzl](https://clawhub.ai/user/dougzl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to capture browser-side fetch, XHR, and basic WebSocket activity during authorized web debugging flows and produce redacted JSON and Markdown reports for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext capture reports may contain tokens, cookies, passwords, personal data, or private API payloads.

Mitigation: Use include-host filters, avoid sensitive login flows unless necessary, disable WebSocket capture when possible, and treat generated JSON and Markdown reports as sensitive files.

Risk: The security summary reports weaker redaction than users are told to expect.

Mitigation: Review generated reports before sharing or storing them, and remove sensitive payloads that redaction did not suppress.

## Reference(s):

- [Browser Network Inspector ClawHub page](https://clawhub.ai/dougzl/skills/browser-network-inspector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts produce JSON capture logs and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are local files. Captured request and response bodies are truncated and redacted by default, but security evidence warns sensitive data may still appear in plaintext outputs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
