## Description: <br>
This skill helps agents design end-to-end testing strategies, automation frameworks, and implementation examples for cross-browser, API, visual regression, accessibility, mobile, CI, and test data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and automation specialists use this skill to plan, generate, and document end-to-end test suites and supporting test infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or copied test code can target the wrong application environment or API if endpoint variables are not checked. <br>
Mitigation: Confirm BASE_URL, API_BASE_URL, API tokens, and related environment variables point only to local, staging, or disposable test systems before execution. <br>
Risk: Database setup, seeding, cleanup, or reset examples can affect production-like data if reused without review. <br>
Mitigation: Run DB_* examples only against dedicated test databases and review cleanup or delete steps before using generated code. <br>


## Reference(s): <br>
- [E2E Test Specialist Code Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include test strategy notes, framework configuration, CI examples, and test data guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
