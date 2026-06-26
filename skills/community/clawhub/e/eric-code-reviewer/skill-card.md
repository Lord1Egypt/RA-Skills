## Description: <br>
Code Reviewer helps developers review pull requests, diffs, and code snippets for code quality, security issues, performance risks, and language-specific best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review PRs, git diffs, branch comparisons, file paths, and pasted code before merging or sharing changes. It supports review across Python, JavaScript/TypeScript, Java, Go, Rust, and Shell scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may review private repositories, secrets, credentials, regulated data, or proprietary code if the user provides or grants access to that material. <br>
Mitigation: Use only on code that the organization permits for agent review; avoid exposing secrets or sensitive repositories unless that review path is approved. <br>
Risk: Review findings or proposed fixes may be incorrect, incomplete, or false positives. <br>
Mitigation: Treat findings and patches as recommendations; have a developer verify issues, run tests, and review changes before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/eric-code-reviewer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ericlooi504) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with severity-ordered findings and optional inline code, patches, or shell commands when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized by critical, important, and suggested issues; large reviews may focus on changed lines or critical areas first.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
