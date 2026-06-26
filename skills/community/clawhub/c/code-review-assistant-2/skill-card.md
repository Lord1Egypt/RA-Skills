## Description: <br>
AI-powered code review assistant that analyzes pull requests, identifies potential bugs, security issues, code quality problems, and provides actionable improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huajianjiu000](https://clawhub.ai/user/huajianjiu000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests, audit code changes, identify security and quality issues, and produce structured feedback with severity levels and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code review can expose code, diffs, secrets, private keys, production credentials, or unrelated sensitive files to the agent context. <br>
Mitigation: Share only the files needed for review, redact secrets and credentials before review, and avoid including unrelated sensitive project data. <br>
Risk: Review feedback may be incomplete or incorrect because the skill provides checklist-based guidance rather than executing tests or scanners. <br>
Mitigation: Treat findings as review assistance, verify important claims against the codebase, and run the project's normal tests and security checks before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huajianjiu000/code-review-assistant-2) <br>
- [Publisher profile](https://clawhub.ai/user/huajianjiu000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review summary with severity-grouped findings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewable code review feedback; no executable code or install steps are included in the artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and target metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
