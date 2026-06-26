## Description: <br>
Reviews code for security, performance, and style issues and returns issue lists, improvement suggestions, and dimensional quality scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[467718584](https://clawhub.ai/user/467718584) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review code paths for security vulnerabilities, performance problems, style issues, and actionable remediation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewing a requested code path can expose project contents to the active agent context. <br>
Mitigation: Provide only code intended for review and avoid including secrets or unrelated sensitive files. <br>
Risk: Code review findings and remediation guidance can be incomplete or incorrect. <br>
Mitigation: Have a developer validate findings and proposed changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/467718584/eo-ability-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with scores, prioritized issues, suggestions, and summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include security, performance, style, and overall scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
