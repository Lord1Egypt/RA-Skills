## Description: <br>
This skill supports development and operation of an AI-powered automated testing platform based on LangChain and DeepSeek, with test case generation, API and UI test automation, reporting, and authorization management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yontlly](https://clawhub.ai/user/yontlly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to build, configure, and operate an internal AI-assisted test automation platform. It helps generate test cases and API/UI automation scripts, run tests in isolated environments, track execution, and produce reports with AI-assisted failure analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The platform has broad authority over authorization, system configuration, backups, generated scripts, reports, and execution artifacts. <br>
Mitigation: Use a tightly isolated internal deployment, require separate admin authorization for auth, system, and backup functions, and add owner checks for task, script, report, and artifact access. <br>
Risk: The release requires sensitive credentials, including a DeepSeek API key and application secrets. <br>
Mitigation: Replace all default credentials and secrets before deployment, disable query-string tokens, and keep secrets in environment-managed storage. <br>
Risk: Uploaded requirements and execution logs may be sent to an external model provider during generation or failure analysis. <br>
Mitigation: Redact data before DeepSeek calls or use a local model when test assets include sensitive business, customer, or production data. <br>
Risk: Generated Python and Playwright tests can execute active network, filesystem, and browser automation behavior. <br>
Mitigation: Run generated tests only in disposable sandboxes with minimal network and filesystem access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yontlly/ai-test-platform) <br>
- [Architecture reference](references/architecture.md) <br>
- [Project README](project/README.md) <br>
- [Deployment guide](deploy/部署文档.md) <br>
- [AI generator guide](project/backend/docs/AI_GENERATOR_GUIDE.md) <br>
- [API test guide](project/backend/docs/API_TEST_GUIDE.md) <br>
- [UI test guide](project/backend/docs/UI_TEST_GUIDE.md) <br>
- [Execution guide](project/backend/docs/EXECUTION_GUIDE.md) <br>
- [Report guide](project/backend/docs/REPORT_GUIDE.md) <br>
- [System management guide](project/backend/docs/SYSTEM_MANAGEMENT_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and code-oriented guidance with configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce platform code, generated test scripts, deployment configuration, test reports, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
