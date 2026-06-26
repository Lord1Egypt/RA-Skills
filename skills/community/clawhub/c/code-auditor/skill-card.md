## Description: <br>
Audit any GitHub repo or raw code for security, quality, or gas optimization. Returns score, findings, severity counts, and summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use Code Auditor to assess GitHub repositories or pasted source code for security vulnerabilities, code quality issues, best practices, and Solidity gas optimization before deployment or dependency adoption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted repository references or pasted code are sent to aiprox.dev/LightningProx for analysis. <br>
Mitigation: Submit only code your organization permits for external analysis, and avoid secrets, private credentials, or confidential source code unless approved. <br>
Risk: The skill requires AIPROX_SPEND_TOKEN for paid API access. <br>
Mitigation: Use a scoped or monitored spend token and provide it only through the required environment variable. <br>
Risk: Audit findings and fixes are generated guidance and may be incomplete or incorrect. <br>
Mitigation: Have a qualified reviewer validate findings and proposed remediations before changing production code. <br>


## Reference(s): <br>
- [Code Auditor on ClawHub](https://clawhub.ai/unixlamadev-spec/code-auditor) <br>
- [AIProx](https://aiprox.dev) <br>
- [AIProx orchestration endpoint](https://aiprox.dev/api/orchestrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON response with score, severity counts, findings, recommended fixes, and summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIPROX_SPEND_TOKEN and sends submitted repository URLs or pasted code to aiprox.dev/LightningProx for analysis.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
