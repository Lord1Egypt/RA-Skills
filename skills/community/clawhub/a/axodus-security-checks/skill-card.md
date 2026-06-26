## Description: <br>
Perform security reviews of code to detect secrets exposure, auth issues, injection risks, unsafe dependencies, and improper execution paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before deployment, after auth changes, or when adding dependencies and integrations to review code for security weaknesses and produce evidence-based remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review inputs or reports may expose sensitive source code, credentials, or personal data. <br>
Mitigation: Invoke the skill with a clear scope, avoid pasting live secrets unnecessarily, and verify that any secrets in reports are redacted. <br>
Risk: Malformed trigger metadata may prevent expected automatic activation. <br>
Mitigation: Invoke the skill explicitly until the publisher fixes the trigger metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-security-checks) <br>
- [security-check.md](artifact/security-check.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [YAML-formatted security findings report in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include severity, location, issue, and remediation when evidence supports them.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
