## Description: <br>
A2A Code Audit scans Python and JavaScript or TypeScript code for security vulnerabilities, style issues, and potential bugs and returns a structured report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crftsmnd](https://clawhub.ai/user/crftsmnd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to request static code audits for Python and JavaScript or TypeScript snippets, focusing on common security issues, style violations, and bug patterns before deployment or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation phrases may cause code to be scanned when the user did not explicitly intend to send it to a paid third-party endpoint. <br>
Mitigation: Require explicit user consent before scanning and confirm that the user accepts the paid external submission. <br>
Risk: Submitted code may contain proprietary code, secrets, customer data, or private repository content. <br>
Mitigation: Ask the user to remove sensitive material or confirm that this data may be sent to the external endpoint before invoking the skill. <br>


## Reference(s): <br>
- [A2A Code Audit on ClawHub](https://clawhub.ai/crftsmnd/a2a-code-audit) <br>
- [Publisher profile: crftsmnd](https://clawhub.ai/user/crftsmnd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with summary table, severity-labeled issues, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include a score, PASS/WARN/FAIL verdict, issue count, issue details, and recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
