## Description: <br>
Provides comprehensive code review guidance for React 19, Vue 3, Rust, TypeScript, Java, Python, and C/C++ to help catch bugs, improve code quality, and give constructive feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to perform structured pull request, architecture, quality, and security reviews across common languages and frameworks. It supports actionable, severity-labeled feedback, review checklists, mentoring, and local lint, test, or build verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository code, diffs, or review findings could be exposed if review material is sent to external services. <br>
Mitigation: Use WebFetch only to retrieve documentation and keep code, diffs, findings, and command output in the local environment. <br>
Risk: Review workflows can accidentally alter or destroy project state if destructive commands or automatic remediation are run without explicit direction. <br>
Mitigation: Treat the skill as observation and feedback by default; require explicit user authorization before making fixes or running destructive commands. <br>
Risk: Overly strict review comments can block safe, small changes for non-critical issues. <br>
Mitigation: Apply severity labels to every finding and reserve blocking decisions for security vulnerabilities, happy-path correctness bugs, or data-loss risks. <br>


## Reference(s): <br>
- [Code Review Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/code-review-hardened) <br>
- [Safety Evaluation](artifact/SAFETY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review findings with severity labels and optional local verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review findings should keep repository content local and avoid unrequested code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
