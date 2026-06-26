## Description: <br>
Use when reviewing frontend security risks such as XSS, CSRF, sensitive data exposure, unsafe DOM APIs, untrusted user input, authentication/token handling, payment flows, file upload, CSP, dependency risk, or third-party scripts; Chinese triggers include 安全审查, 安全检查. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review frontend code for XSS, CSRF, sensitive data exposure, unsafe DOM APIs, authentication/token handling, payment flows, file upload, CSP, dependency, and third-party script risks, then produce a severity-ranked security report with concrete fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect security-sensitive frontend code and produce reports that mention vulnerabilities, tokens, payment flows, or authentication logic. <br>
Mitigation: Use it only on repositories you are authorized to review and handle generated reports as sensitive project artifacts. <br>
Risk: Generated security findings can be incomplete or need contextual validation before they affect release decisions. <br>
Mitigation: Have qualified reviewers validate high-impact findings and confirm server-side security boundaries before relying on the report. <br>


## Reference(s): <br>
- [Security review report template](references/report-template.md) <br>
- [Frontend security review checklist](references/security-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown security review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report path follows reports/security-review-YYYY-MM-DD-HHmmss.md.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
