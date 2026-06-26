## Description: <br>
AI-powered software development workflow orchestration for code analysis, business intelligence extraction, diagnostics, and automated project workflow support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hickhe](https://clawhub.ai/user/hickhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Code Hug to run staged software delivery workflows, extract business rules and PRD material from existing codebases, diagnose build or test failures, and prepare validation or deployment artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad project visibility and may attempt automated repairs. <br>
Mitigation: Use it on a clean branch or disposable clone, disable auto-fix unless each change can be reviewed, and inspect generated diffs before merging. <br>
Risk: Local analysis outputs and notification channels may expose confidential project information. <br>
Mitigation: Inspect .code-hug/ outputs, exclude them from version control when sensitive, and avoid email or external notifications for confidential code. <br>
Risk: Generated business rules, PRDs, diagnostics, and security findings may be incomplete or inaccurate. <br>
Mitigation: Validate outputs with maintainers, domain experts, and existing test or security review processes before relying on them. <br>


## Reference(s): <br>
- [Code Hug on ClawHub](https://clawhub.ai/hickhe/code-hug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, code or configuration changes, shell command guidance, and workspace files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store analysis artifacts under .code-hug/ and can propose or attempt automated fixes when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
