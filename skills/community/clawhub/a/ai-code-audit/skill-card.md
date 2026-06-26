## Description: <br>
AI-powered code review skill that analyzes code snippets, diffs, and PR changes across security, performance, maintainability, logic, and style and returns structured review findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caingao](https://clawhub.ai/user/caingao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review code snippets, local diffs, and PR-style changes for security, performance, maintainability, logic, and style issues before merge or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect sensitive repository code, PR diffs, or local git changes during review. <br>
Mitigation: For sensitive repositories, provide a specific pasted diff, staged change, commit, branch, or file rather than broad access to recent local changes. <br>
Risk: Review findings and suggested fixes can be incomplete or incorrect because they are generated from rule-guided agent analysis. <br>
Mitigation: Treat findings as review assistance and have maintainers verify severity, affected locations, and proposed fixes before merge or release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caingao/ai-code-audit) <br>
- [Publisher profile](https://clawhub.ai/user/caingao) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README.md](artifact/README.md) <br>
- [review-rules.md](artifact/review-rules.md) <br>
- [test-cases.md](artifact/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, guidance, shell commands] <br>
**Output Format:** [Markdown review reports with findings, risk ratings, and suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-first responses by default; supports full review, PR review, security review, and quick-check modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
