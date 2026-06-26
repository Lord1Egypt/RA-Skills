## Description: <br>
端到端（E2E）测试编排与执行。用于用户要求：设计测试用例、基于 Playwright/Cypress 实现自动化脚本、通过源码优先定位元素并在必要时使用截图/图像识别兜底、执行测试、自动修复脚本问题（如定位器或等待策略）、并输出结构化测试报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklldog](https://clawhub.ai/user/kklldog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to plan end-to-end test coverage, implement Playwright or Cypress automation, run targeted or regression suites, triage failures, and produce structured evidence-backed reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run npm, Playwright, and Docker against the user's project, which may execute project scripts or containerized commands with broad workspace access. <br>
Mitigation: Review the runner scripts before installation, run tests against staging systems, and use non-production data and accounts. <br>
Risk: The Docker fallback uses a configurable Playwright image and mounts the current workspace into the container. <br>
Mitigation: Pin or restrict the Docker image in sensitive repositories and run only from a workspace intended for test execution. <br>
Risk: Untrusted grep filters passed to test runners may affect shell command construction in the Docker runner. <br>
Mitigation: Avoid passing untrusted filter values and prefer known test tags such as smoke or regression labels. <br>


## Reference(s): <br>
- [E2E test case template](references/case-template.md) <br>
- [Locator strategy](references/locator-strategy.md) <br>
- [Playwright local and Docker fallback guidance](references/playwright-重点与docker兜底.md) <br>
- [E2E test report template](references/report-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/kklldog/e2e-test-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with test cases, automation code, shell commands, execution notes, and structured reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include evidence paths for screenshots, videos, traces, logs, and test result artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
