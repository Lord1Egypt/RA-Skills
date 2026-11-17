## Description:

Orchestrates end-to-end testing by planning cases, implementing Playwright or Cypress automation, executing tests, repairing script issues, and producing structured reports with evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklldog](https://clawhub.ai/user/kklldog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to design traceable E2E test cases, create and run browser automation, classify failures, repair test scripts when appropriate, and report results with screenshots, traces, videos, and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags command-injection and supply-chain risk in the Docker runner.

Mitigation: Review before installing or running, avoid untrusted filter strings, pass arguments safely, enforce locked dependencies, remove npm install fallback behavior, pin container images by digest, and limit writable mounts and network access.

Risk: E2E evidence artifacts can contain sensitive application data.

Mitigation: Treat captured screenshots, traces, videos, and logs as sensitive and store or share them only in approved locations.

## Reference(s):

- [E2E test case template](references/case-template.md)
- [Locator strategy](references/locator-strategy.md)
- [Playwright usage and Docker fallback](references/playwright-重点与docker兜底.md)
- [E2E test report template](references/report-template.md)
- [ClawHub skill page](https://clawhub.ai/kklldog/skills/e2e-test-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with test plans, TypeScript or JavaScript test code, shell commands, configuration guidance, and structured report sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated evidence artifacts such as screenshots, videos, traces, and logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
