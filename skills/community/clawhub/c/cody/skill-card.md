## Description: <br>
Analyzes Git diffs, pull requests, pasted code, or specified files and produces structured Chinese code review reports covering bugs, security issues, performance, readability, best practices, type safety, error handling, and test coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xonet1](https://clawhub.ai/user/xonet1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review local diffs, GitHub or GitLab PR/MR diffs, pasted code, or selected files and receive actionable Chinese-language review findings. It supports configurable strictness and language-specific checks for Python, JavaScript, TypeScript, Java, Go, and Rust. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read diffs, files, or PR/MR content that the user asks it to review, which can include secrets or sensitive code. <br>
Mitigation: Avoid reviewing changes that contain secrets or sensitive data, and redact confidential content before providing it to the assistant. <br>
Risk: Fetching GitHub or GitLab diffs can require access tokens. <br>
Mitigation: Use read-only, least-privilege GitHub or GitLab tokens and avoid passing broader credentials than the review requires. <br>
Risk: Self-hosted GitLab URLs can point the assistant at an unintended service or repository. <br>
Mitigation: Verify the GitLab base URL and project path before requesting remote diff retrieval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xonet1/cody) <br>
- [Review report template](artifact/references/report-template.md) <br>
- [Review dimensions](artifact/references/review-dimensions.md) <br>
- [Severity guide](artifact/references/severity-guide.md) <br>
- [Python review rules](artifact/references/languages/python.md) <br>
- [JavaScript and TypeScript review rules](artifact/references/languages/javascript.md) <br>
- [Java review rules](artifact/references/languages/java.md) <br>
- [Go review rules](artifact/references/languages/go.md) <br>
- [Rust review rules](artifact/references/languages/rust.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON or HTML review reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language findings with severity, file and line references when available, issue explanation, and actionable recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
