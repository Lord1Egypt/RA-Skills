## Description: <br>
Reviews Python code for quality, style, and common bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dapan0902](https://clawhub.ai/user/dapan0902) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to review Python code for quality, style, common bugs, and concrete improvement opportunities before merging or sharing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code submitted for review may contain secrets or private credentials. <br>
Mitigation: Remove secrets, credentials, and sensitive business data before asking the skill to review code. <br>
Risk: Checklist-based review can miss security issues or provide incomplete guidance. <br>
Mitigation: Use the review as development feedback and run dedicated security review or scanning for high-risk code. <br>


## Reference(s): <br>
- [Python code review checklist](artifact/references:review-checklist.md) <br>
- [ClawHub skill page](https://clawhub.ai/dapan0902/code-reviewer-new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Structured Markdown review with a summary, severity-grouped findings, score, and top recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include error, warning, or info severity, location, rationale, and suggested fixes when applicable.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
